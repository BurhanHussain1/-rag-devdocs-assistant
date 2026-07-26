---
url: https://openai.github.io/openai-agents-python/ref/mcp/manager/
title: `Manager`
framework: openai
---

# `Manager`

### MCPServerManager

Bases: `AbstractAsyncContextManager['MCPServerManager']`

Manage MCP server lifecycles and expose only connected servers.

Use this helper to keep MCP connect/cleanup on the same task and avoid
run failures when a server is unavailable. The manager will attempt to
connect each server and then expose the connected subset via
`active_servers`.

Basic usage

async with MCPServerManager([server\_a, server\_b]) as manager:
agent = Agent(
name="Assistant",
instructions="...",
mcp\_servers=manager.active\_servers,
)

FastAPI lifespan example

@asynccontextmanager
async def lifespan(app: FastAPI):
async with MCPServerManager([server\_a, server\_b]) as manager:
app.state.mcp\_manager = manager
yield

app = FastAPI(lifespan=lifespan)

Important behaviors:
- `active_servers` only includes servers that connected successfully.
`failed_servers` holds the failures and `errors` maps servers to errors.
- `drop_failed_servers=True` removes failed servers from `active_servers`
(recommended). If False, `active_servers` will still include all servers.
- `strict=True` raises on the first connection failure. If False, failures
are recorded and the run can proceed with the remaining servers.
- `reconnect(failed_only=True)` retries failed servers and refreshes
`active_servers`.
- `connect_in_parallel=True` uses a dedicated worker task per server to
allow concurrent connects while preserving task affinity for cleanup.

Source code in `src/agents/mcp/manager.py`

|  |  |
| --- | --- |
| ``` 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 ``` | ``` class MCPServerManager(AbstractAsyncContextManager["MCPServerManager"]):     """Manage MCP server lifecycles and expose only connected servers.      Use this helper to keep MCP connect/cleanup on the same task and avoid     run failures when a server is unavailable. The manager will attempt to     connect each server and then expose the connected subset via     `active_servers`.      Basic usage:         async with MCPServerManager([server_a, server_b]) as manager:             agent = Agent(                 name="Assistant",                 instructions="...",                 mcp_servers=manager.active_servers,             )      FastAPI lifespan example:         @asynccontextmanager         async def lifespan(app: FastAPI):             async with MCPServerManager([server_a, server_b]) as manager:                 app.state.mcp_manager = manager                 yield          app = FastAPI(lifespan=lifespan)      Important behaviors:     - `active_servers` only includes servers that connected successfully.       `failed_servers` holds the failures and `errors` maps servers to errors.     - `drop_failed_servers=True` removes failed servers from `active_servers`       (recommended). If False, `active_servers` will still include all servers.     - `strict=True` raises on the first connection failure. If False, failures       are recorded and the run can proceed with the remaining servers.     - `reconnect(failed_only=True)` retries failed servers and refreshes       `active_servers`.     - `connect_in_parallel=True` uses a dedicated worker task per server to       allow concurrent connects while preserving task affinity for cleanup.     """      def __init__(         self,         servers: Iterable[MCPServer],         *,         connect_timeout_seconds: float | None = 10.0,         cleanup_timeout_seconds: float | None = 10.0,         drop_failed_servers: bool = True,         strict: bool = False,         suppress_cancelled_error: bool = True,         connect_in_parallel: bool = False,     ) -> None:         self._all_servers = list(servers)         self._active_servers = list(servers)         self.connect_timeout_seconds = connect_timeout_seconds         self.cleanup_timeout_seconds = cleanup_timeout_seconds         self.drop_failed_servers = drop_failed_servers         self.strict = strict         self.suppress_cancelled_error = suppress_cancelled_error         self.connect_in_parallel = connect_in_parallel         self._workers: dict[MCPServer, _ServerWorker] = {}          self.failed_servers: list[MCPServer] = []         self._failed_server_set: set[MCPServer] = set()         self._connected_servers: set[MCPServer] = set()         self.errors: dict[MCPServer, BaseException] = {}      @property     def active_servers(self) -> list[MCPServer]:         """Return the active MCP servers after connection attempts."""         return list(self._active_servers)      @property     def all_servers(self) -> list[MCPServer]:         """Return all MCP servers managed by this instance."""         return list(self._all_servers)      async def __aenter__(self) -> MCPServerManager:         await self.connect_all()         return self      async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool | None:         await self.cleanup_all()         return None      async def connect_all(self) -> list[MCPServer]:         """Connect all servers in order and return the active list."""         previous_connected_servers = set(self._connected_servers)         previous_active_servers = list(self._active_servers)         self.failed_servers = []         self._failed_server_set = set()         self.errors = {}          servers_to_connect = self._servers_to_connect(self._all_servers)         connected_servers: list[MCPServer] = []         try:             if self.connect_in_parallel:                 await self._connect_all_parallel(servers_to_connect)             else:                 for server in servers_to_connect:                     await self._attempt_connect(server)                     if server not in self._failed_server_set:                         connected_servers.append(server)         except BaseException:             if self.connect_in_parallel:                 await self._cleanup_servers(servers_to_connect)             else:                 servers_to_cleanup = self._unique_servers(                     [*connected_servers, *self.failed_servers]                 )                 await self._cleanup_servers(servers_to_cleanup)             if self.drop_failed_servers:                 self._active_servers = [                     server for server in self._all_servers if server in previous_connected_servers                 ]             else:                 self._active_servers = previous_active_servers             raise          self._refresh_active_servers()          return self._active_servers      async def reconnect(self, *, failed_only: bool = True) -> list[MCPServer]:         """Reconnect servers and return the active list.          Args:             failed_only: If True, only retry servers that previously failed.                 If False, cleanup and retry all servers.         """         if failed_only:             servers_to_retry = self._unique_servers(self.failed_servers)         else:             await self.cleanup_all()             servers_to_retry = list(self._all_servers)             self.failed_servers = []             self._failed_server_set = set()             self.errors = {}          servers_to_retry = self._servers_to_connect(servers_to_retry)         try:             if self.connect_in_parallel:                 await self._connect_all_parallel(servers_to_retry)             else:                 for server in servers_to_retry:                     await self._attempt_connect(server)         finally:             self._refresh_active_servers()         return self._active_servers      async def cleanup_all(self) -> None:         """Cleanup all servers in reverse order."""         for server in reversed(self._all_servers):             try:                 await self._cleanup_server(server)             except asyncio.CancelledError as exc:                 if not self.suppress_cancelled_error:                     raise                 logger.debug("Cleanup cancelled for MCP server '%s': %s", server.name, exc)                 self.errors[server] = exc             except Exception as exc:                 logger.exception("Failed to cleanup MCP server '%s': %s", server.name, exc)                 self.errors[server] = exc      async def _run_with_timeout(         self, func: Callable[[], Awaitable[Any]], timeout_seconds: float | None     ) -> None:         await _run_with_timeout_in_task(func, timeout_seconds)      async def _attempt_connect(         self, server: MCPServer, *, raise_on_error: bool | None = None     ) -> None:         if raise_on_error is None:             raise_on_error = self.strict         try:             await self._run_connect(server)             self._connected_servers.add(server)             if server in self.failed_servers:                 self._remove_failed_server(server)                 self.errors.pop(server, None)         except asyncio.CancelledError as exc:             if not self.suppress_cancelled_error:                 raise             self._record_failure(server, exc, phase="connect")         except Exception as exc:             self._record_failure(server, exc, phase="connect")             if raise_on_error:                 raise         except BaseException as exc:             self._record_failure(server, exc, phase="connect")             raise      def _refresh_active_servers(self) -> None:         if self.drop_failed_servers:             failed = set(self._failed_server_set)             self._active_servers = [server for server in self._all_servers if server not in failed]         else:             self._active_servers = list(self._all_servers)      def _record_failure(self, server: MCPServer, exc: BaseException, phase: str) -> None:         logger.exception("Failed to %s MCP server '%s': %s", phase, server.name, exc)         if server not in self._failed_server_set:             self.failed_servers.append(server)             self._failed_server_set.add(server)         self.errors[server] = exc      async def _run_connect(self, server: MCPServer) -> None:         if self.connect_in_parallel:             worker = self._get_worker(server)             await worker.connect()         else:             await self._run_with_timeout(server.connect, self.connect_timeout_seconds)      async def _cleanup_server(self, server: MCPServer) -> None:         if self.connect_in_parallel and server in self._workers:             worker = self._workers[server]             if worker.is_done:                 self._workers.pop(server, None)                 self._connected_servers.discard(server)                 return             try:                 await worker.cleanup()             finally:                 self._workers.pop(server, None)                 self._connected_servers.discard(server)             return         try:             await self._run_with_timeout(server.cleanup, self.cleanup_timeout_seconds)         finally:             self._connected_servers.discard(server)      async def _cleanup_servers(self, servers: Iterable[MCPServer]) -> None:         for server in reversed(list(servers)):             try:                 await self._cleanup_server(server)             except asyncio.CancelledError as exc:                 if not self.suppress_cancelled_error:                     raise                 logger.debug("Cleanup cancelled for MCP server '%s': %s", server.name, exc)                 self.errors[server] = exc             except Exception as exc:                 logger.exception("Failed to cleanup MCP server '%s': %s", server.name, exc)                 self.errors[server] = exc      async def _connect_all_parallel(self, servers: list[MCPServer]) -> None:         tasks = [             asyncio.create_task(self._attempt_connect(server, raise_on_error=False))             for server in servers         ]         results = await asyncio.gather(*tasks, return_exceptions=True)         if not self.suppress_cancelled_error:             for result in results:                 if isinstance(result, asyncio.CancelledError):                     raise result         for result in results:             if isinstance(result, BaseException) and not isinstance(result, asyncio.CancelledError):                 raise result         if self.strict and self.failed_servers:             first_failure = None             if self.suppress_cancelled_error:                 for server in self.failed_servers:                     error = self.errors.get(server)                     if error is None or isinstance(error, asyncio.CancelledError):                         continue                     first_failure = server                     break             else:                 first_failure = self.failed_servers[0]             if first_failure is not None:                 error = self.errors.get(first_failure)                 if error is not None:                     raise error                 raise RuntimeError(f"Failed to connect MCP server '{first_failure.name}'")      def _get_worker(self, server: MCPServer) -> _ServerWorker:         worker = self._workers.get(server)         if worker is None or worker.is_done:             worker = _ServerWorker(                 server=server,                 connect_timeout_seconds=self.connect_timeout_seconds,                 cleanup_timeout_seconds=self.cleanup_timeout_seconds,             )             self._workers[server] = worker         return worker      def _remove_failed_server(self, server: MCPServer) -> None:         if server in self._failed_server_set:             self._failed_server_set.remove(server)         self.failed_servers = [             failed_server for failed_server in self.failed_servers if failed_server != server         ]      def _servers_to_connect(self, servers: Iterable[MCPServer]) -> list[MCPServer]:         unique = self._unique_servers(servers)         if not self._connected_servers:             return unique         return [server for server in unique if server not in self._connected_servers]      @staticmethod     def _unique_servers(servers: Iterable[MCPServer]) -> list[MCPServer]:         seen: set[MCPServer] = set()         unique: list[MCPServer] = []         for server in servers:             if server not in seen:                 seen.add(server)                 unique.append(server)         return unique ``` |

#### active\_servers `property`

```
active_servers: list[MCPServer]
```

Return the active MCP servers after connection attempts.

#### all\_servers `property`

```
all_servers: list[MCPServer]
```

Return all MCP servers managed by this instance.

#### connect\_all `async`

```
connect_all() -> list[MCPServer]
```

Connect all servers in order and return the active list.

Source code in `src/agents/mcp/manager.py`

|  |  |
| --- | --- |
| ``` 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 ``` | ``` async def connect_all(self) -> list[MCPServer]:     """Connect all servers in order and return the active list."""     previous_connected_servers = set(self._connected_servers)     previous_active_servers = list(self._active_servers)     self.failed_servers = []     self._failed_server_set = set()     self.errors = {}      servers_to_connect = self._servers_to_connect(self._all_servers)     connected_servers: list[MCPServer] = []     try:         if self.connect_in_parallel:             await self._connect_all_parallel(servers_to_connect)         else:             for server in servers_to_connect:                 await self._attempt_connect(server)                 if server not in self._failed_server_set:                     connected_servers.append(server)     except BaseException:         if self.connect_in_parallel:             await self._cleanup_servers(servers_to_connect)         else:             servers_to_cleanup = self._unique_servers(                 [*connected_servers, *self.failed_servers]             )             await self._cleanup_servers(servers_to_cleanup)         if self.drop_failed_servers:             self._active_servers = [                 server for server in self._all_servers if server in previous_connected_servers             ]         else:             self._active_servers = previous_active_servers         raise      self._refresh_active_servers()      return self._active_servers ``` |

#### reconnect `async`

```
reconnect(*, failed_only: bool = True) -> list[MCPServer]
```

Reconnect servers and return the active list.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `failed_only` | `bool` | If True, only retry servers that previously failed. If False, cleanup and retry all servers. | `True` |

Source code in `src/agents/mcp/manager.py`

|  |  |
| --- | --- |
| ``` 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 ``` | ``` async def reconnect(self, *, failed_only: bool = True) -> list[MCPServer]:     """Reconnect servers and return the active list.      Args:         failed_only: If True, only retry servers that previously failed.             If False, cleanup and retry all servers.     """     if failed_only:         servers_to_retry = self._unique_servers(self.failed_servers)     else:         await self.cleanup_all()         servers_to_retry = list(self._all_servers)         self.failed_servers = []         self._failed_server_set = set()         self.errors = {}      servers_to_retry = self._servers_to_connect(servers_to_retry)     try:         if self.connect_in_parallel:             await self._connect_all_parallel(servers_to_retry)         else:             for server in servers_to_retry:                 await self._attempt_connect(server)     finally:         self._refresh_active_servers()     return self._active_servers ``` |

#### cleanup\_all `async`

```
cleanup_all() -> None
```

Cleanup all servers in reverse order.

Source code in `src/agents/mcp/manager.py`

|  |  |
| --- | --- |
| ``` 255 256 257 258 259 260 261 262 263 264 265 266 267 ``` | ``` async def cleanup_all(self) -> None:     """Cleanup all servers in reverse order."""     for server in reversed(self._all_servers):         try:             await self._cleanup_server(server)         except asyncio.CancelledError as exc:             if not self.suppress_cancelled_error:                 raise             logger.debug("Cleanup cancelled for MCP server '%s': %s", server.name, exc)             self.errors[server] = exc         except Exception as exc:             logger.exception("Failed to cleanup MCP server '%s': %s", server.name, exc)             self.errors[server] = exc ``` |