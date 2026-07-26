---
url: https://openai.github.io/openai-agents-python/ref/extensions/memory/dapr_session/
title: `DaprSession`
framework: openai
---

# `DaprSession`

Bases: `SessionABC`

Dapr State Store implementation of [`Session`](../../../memory/session/#agents.memory.session.Session "Session").

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ```  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 ``` | ``` class DaprSession(SessionABC):     """Dapr State Store implementation of [`Session`][agents.memory.session.Session]."""      session_settings: SessionSettings | None = None      def __init__(         self,         session_id: str,         *,         state_store_name: str,         dapr_client: DaprClient,         ttl: int | None = None,         consistency: ConsistencyLevel = DAPR_CONSISTENCY_EVENTUAL,         session_settings: SessionSettings | None = None,     ):         """Initializes a new DaprSession.          Args:             session_id (str): Unique identifier for the conversation.             state_store_name (str): Name of the Dapr state store component.             dapr_client (DaprClient): A pre-configured Dapr client.             ttl (int | None, optional): Time-to-live in seconds for session data.                 If None, data persists indefinitely. Note that TTL support depends on                 the underlying state store implementation. Defaults to None.             consistency (ConsistencyLevel, optional): Consistency level for state operations.                 Use DAPR_CONSISTENCY_EVENTUAL or DAPR_CONSISTENCY_STRONG constants.                 Defaults to DAPR_CONSISTENCY_EVENTUAL.             session_settings (SessionSettings | None): Session configuration settings including                 default limit for retrieving items. If None, uses default SessionSettings().         """         self.session_id = session_id         self.session_settings = session_settings or SessionSettings()         self._dapr_client = dapr_client         self._state_store_name = state_store_name         self._ttl = ttl         self._consistency = consistency         self._lock = asyncio.Lock()         self._owns_client = False  # Track if we own the Dapr client          # State keys         self._messages_key = f"{self.session_id}:messages"         self._metadata_key = f"{self.session_id}:metadata"      @classmethod     def from_address(         cls,         session_id: str,         *,         state_store_name: str,         dapr_address: str = "localhost:50001",         session_settings: SessionSettings | None = None,         **kwargs: Any,     ) -> DaprSession:         """Create a session from a Dapr sidecar address.          Args:             session_id (str): Conversation ID.             state_store_name (str): Name of the Dapr state store component.             dapr_address (str): Dapr sidecar gRPC address. Defaults to "localhost:50001".             session_settings (SessionSettings | None): Session configuration settings including                 default limit for retrieving items. If None, uses default SessionSettings().             **kwargs: Additional keyword arguments forwarded to the main constructor                 (e.g., ttl, consistency).          Returns:             DaprSession: An instance of DaprSession connected to the specified Dapr sidecar.          Note:             The Dapr Python SDK performs health checks on the HTTP endpoint (default: http://localhost:3500).             Ensure the Dapr sidecar is started with --dapr-http-port 3500. Alternatively, set one of             these environment variables: DAPR_HTTP_ENDPOINT (e.g., "http://localhost:3500") or             DAPR_HTTP_PORT (e.g., "3500") to avoid connection errors.         """         dapr_client = DaprClient(address=dapr_address)         session = cls(             session_id,             state_store_name=state_store_name,             dapr_client=dapr_client,             session_settings=session_settings,             **kwargs,         )         session._owns_client = True  # We created the client, so we own it         return session      def _get_read_metadata(self) -> dict[str, str]:         """Get metadata for read operations including consistency.          The consistency level is passed through state_metadata as per Dapr's state API.         """         metadata: dict[str, str] = {}         # Add consistency level to metadata for read operations         if self._consistency:             metadata["consistency"] = self._consistency         return metadata      def _get_state_options(self, *, concurrency: Concurrency | None = None) -> StateOptions | None:         """Get StateOptions configured with consistency and optional concurrency."""         options_kwargs: dict[str, Any] = {}         if self._consistency == DAPR_CONSISTENCY_STRONG:             options_kwargs["consistency"] = Consistency.strong         elif self._consistency == DAPR_CONSISTENCY_EVENTUAL:             options_kwargs["consistency"] = Consistency.eventual         if concurrency is not None:             options_kwargs["concurrency"] = concurrency         if options_kwargs:             return StateOptions(**options_kwargs)         return None      def _get_metadata(self) -> dict[str, str]:         """Get metadata for state operations including TTL if configured."""         metadata = {}         if self._ttl is not None:             metadata["ttlInSeconds"] = str(self._ttl)         return metadata      async def _serialize_item(self, item: TResponseInputItem) -> str:         """Serialize an item to JSON string. Can be overridden by subclasses."""         return json.dumps(item, separators=(",", ":"))      async def _deserialize_item(self, item: str) -> TResponseInputItem:         """Deserialize a JSON string to an item. Can be overridden by subclasses."""         return json.loads(item)  # type: ignore[no-any-return]      def _decode_messages(self, data: bytes | None, *, strict: bool = False) -> list[Any]:         if not data:             return []         try:             messages_json = data.decode("utf-8")             messages = json.loads(messages_json)             if isinstance(messages, list):                 return list(messages)         except (json.JSONDecodeError, UnicodeDecodeError) as error:             if strict:                 raise ValueError(                     "The stored Dapr session messages are not valid JSON and cannot be "                     "safely updated."                 ) from error             return []         if strict:             raise ValueError(                 "The stored Dapr session messages must be a JSON list and cannot be safely updated."             )         return []      def _decode_messages_for_update(self, data: bytes | None) -> list[Any]:         """Decode aggregate state before an operation that rewrites it."""         return self._decode_messages(data, strict=True)      def _calculate_retry_delay(self, attempt: int) -> float:         base: float = _RETRY_BASE_DELAY_SECONDS * (2 ** max(0, attempt - 1))         delay: float = min(base, _RETRY_MAX_DELAY_SECONDS)         # Add jitter (10%) similar to tracing processors to avoid thundering herd.         return delay + random.uniform(0, 0.1 * delay)      def _is_concurrency_conflict(self, error: Exception) -> bool:         code_attr = getattr(error, "code", None)         if callable(code_attr):             try:                 status_code = code_attr()             except Exception:                 status_code = None             if status_code is not None:                 status_name = getattr(status_code, "name", str(status_code))                 if status_name in {"ABORTED", "FAILED_PRECONDITION"}:                     return True         message = str(error).lower()         conflict_markers = (             "etag mismatch",             "etag does not match",             "precondition failed",             "concurrency conflict",             "invalid etag",             "failed to set key",  # Redis state store Lua script error during conditional write             "user_script",  # Redis script failure hint         )         return any(marker in message for marker in conflict_markers)      async def _handle_concurrency_conflict(self, error: Exception, attempt: int) -> bool:         if not self._is_concurrency_conflict(error):             return False         if attempt >= _MAX_WRITE_ATTEMPTS:             return False         delay = self._calculate_retry_delay(attempt)         if delay > 0:             await asyncio.sleep(delay)         return True      # ------------------------------------------------------------------     # Session protocol implementation     # ------------------------------------------------------------------      async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         """Retrieve the conversation history for this session.          Args:             limit: Maximum number of items to retrieve. If None, uses session_settings.limit.                    When specified, returns the latest N items in chronological order.          Returns:             List of input items representing the conversation history         """         session_limit = resolve_session_limit(limit, self.session_settings)          async with self._lock:             # Get messages from state store with consistency level             response = await self._dapr_client.get_state(                 store_name=self._state_store_name,                 key=self._messages_key,                 state_metadata=self._get_read_metadata(),             )              messages = self._decode_messages(response.data)             if not messages:                 return []             if session_limit is not None:                 if session_limit <= 0:                     return []                 messages = messages[-session_limit:]             items: list[TResponseInputItem] = []             for msg in messages:                 try:                     if isinstance(msg, str):                         item = await self._deserialize_item(msg)                     else:                         item = msg                     items.append(item)                 except (json.JSONDecodeError, TypeError):                     continue             return items      async def add_items(self, items: list[TResponseInputItem]) -> None:         """Add new items to the conversation history.          Args:             items: List of input items to add to the history         """         if not items:             return          async with self._lock:             serialized_items: list[str] = [await self._serialize_item(item) for item in items]             attempt = 0             while True:                 attempt += 1                 response = await self._dapr_client.get_state(                     store_name=self._state_store_name,                     key=self._messages_key,                     state_metadata=self._get_read_metadata(),                 )                 existing_messages = self._decode_messages_for_update(response.data)                 updated_messages = existing_messages + serialized_items                 messages_json = json.dumps(updated_messages, separators=(",", ":"))                 etag = response.etag                 try:                     await self._dapr_client.save_state(                         store_name=self._state_store_name,                         key=self._messages_key,                         value=messages_json,                         etag=etag,                         state_metadata=self._get_metadata(),                         options=self._get_state_options(concurrency=Concurrency.first_write),                     )                     break                 except Exception as error:                     should_retry = await self._handle_concurrency_conflict(error, attempt)                     if should_retry:                         continue                     raise              # Update metadata             metadata = {                 "session_id": self.session_id,                 "created_at": str(int(time.time())),                 "updated_at": str(int(time.time())),             }             await self._dapr_client.save_state(                 store_name=self._state_store_name,                 key=self._metadata_key,                 value=json.dumps(metadata),                 state_metadata=self._get_metadata(),                 options=self._get_state_options(),             )      async def pop_item(self) -> TResponseInputItem | None:         """Remove and return the most recent item from the session.          Returns:             The most recent item if it exists, None if the session is empty         """         async with self._lock:             while True:                 attempt = 0                 while True:                     attempt += 1                     response = await self._dapr_client.get_state(                         store_name=self._state_store_name,                         key=self._messages_key,                         state_metadata=self._get_read_metadata(),                     )                     messages = self._decode_messages(response.data)                     if not messages:                         return None                     last_item = messages.pop()                     messages_json = json.dumps(messages, separators=(",", ":"))                     etag = getattr(response, "etag", None) or None                     try:                         await self._dapr_client.save_state(                             store_name=self._state_store_name,                             key=self._messages_key,                             value=messages_json,                             etag=etag,                             state_metadata=self._get_metadata(),                             options=self._get_state_options(concurrency=Concurrency.first_write),                         )                         break                     except Exception as error:                         should_retry = await self._handle_concurrency_conflict(error, attempt)                         if should_retry:                             continue                         raise                 try:                     if isinstance(last_item, str):                         return await self._deserialize_item(last_item)                     return last_item  # type: ignore[no-any-return]                 except (json.JSONDecodeError, TypeError):                     continue      async def clear_session(self) -> None:         """Clear all items for this session."""         async with self._lock:             # Delete messages and metadata keys             await self._dapr_client.delete_state(                 store_name=self._state_store_name,                 key=self._messages_key,                 options=self._get_state_options(),             )              await self._dapr_client.delete_state(                 store_name=self._state_store_name,                 key=self._metadata_key,                 options=self._get_state_options(),             )      async def close(self) -> None:         """Close the Dapr client connection.          Only closes the connection if this session owns the Dapr client         (i.e., created via from_address). If the client was injected externally,         the caller is responsible for managing its lifecycle.         """         if self._owns_client:             await self._dapr_client.close()      async def __aenter__(self) -> DaprSession:         """Enter async context manager."""         return self      async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:         """Exit async context manager and close the connection."""         await self.close()      async def ping(self) -> bool:         """Test Dapr connectivity by checking metadata.          Returns:             True if Dapr is reachable, False otherwise.         """         try:             # First attempt a read; some stores may not be initialized yet.             await self._dapr_client.get_state(                 store_name=self._state_store_name,                 key="__ping__",                 state_metadata=self._get_read_metadata(),             )             return True         except Exception as initial_error:             # If relation/table is missing or store isn't initialized,             # attempt a write to initialize it, then read again.             try:                 await self._dapr_client.save_state(                     store_name=self._state_store_name,                     key="__ping__",                     value="ok",                     state_metadata=self._get_metadata(),                     options=self._get_state_options(),                 )                 # Read again after write.                 await self._dapr_client.get_state(                     store_name=self._state_store_name,                     key="__ping__",                     state_metadata=self._get_read_metadata(),                 )                 return True             except Exception:                 logger.error("Dapr connection failed: %s", initial_error)                 return False ``` |

### \_\_init\_\_

```
__init__(
    session_id: str,
    *,
    state_store_name: str,
    dapr_client: DaprClient,
    ttl: int | None = None,
    consistency: ConsistencyLevel = DAPR_CONSISTENCY_EVENTUAL,
    session_settings: SessionSettings | None = None,
)
```

Initializes a new DaprSession.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Unique identifier for the conversation. | *required* |
| `state_store_name` | `str` | Name of the Dapr state store component. | *required* |
| `dapr_client` | `DaprClient` | A pre-configured Dapr client. | *required* |
| `ttl` | `int | None` | Time-to-live in seconds for session data. If None, data persists indefinitely. Note that TTL support depends on the underlying state store implementation. Defaults to None. | `None` |
| `consistency` | `ConsistencyLevel` | Consistency level for state operations. Use DAPR\_CONSISTENCY\_EVENTUAL or DAPR\_CONSISTENCY\_STRONG constants. Defaults to DAPR\_CONSISTENCY\_EVENTUAL. | `DAPR_CONSISTENCY_EVENTUAL` |
| `session_settings` | `SessionSettings | None` | Session configuration settings including default limit for retrieving items. If None, uses default SessionSettings(). | `None` |

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ```  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 ``` | ``` def __init__(     self,     session_id: str,     *,     state_store_name: str,     dapr_client: DaprClient,     ttl: int | None = None,     consistency: ConsistencyLevel = DAPR_CONSISTENCY_EVENTUAL,     session_settings: SessionSettings | None = None, ):     """Initializes a new DaprSession.      Args:         session_id (str): Unique identifier for the conversation.         state_store_name (str): Name of the Dapr state store component.         dapr_client (DaprClient): A pre-configured Dapr client.         ttl (int | None, optional): Time-to-live in seconds for session data.             If None, data persists indefinitely. Note that TTL support depends on             the underlying state store implementation. Defaults to None.         consistency (ConsistencyLevel, optional): Consistency level for state operations.             Use DAPR_CONSISTENCY_EVENTUAL or DAPR_CONSISTENCY_STRONG constants.             Defaults to DAPR_CONSISTENCY_EVENTUAL.         session_settings (SessionSettings | None): Session configuration settings including             default limit for retrieving items. If None, uses default SessionSettings().     """     self.session_id = session_id     self.session_settings = session_settings or SessionSettings()     self._dapr_client = dapr_client     self._state_store_name = state_store_name     self._ttl = ttl     self._consistency = consistency     self._lock = asyncio.Lock()     self._owns_client = False  # Track if we own the Dapr client      # State keys     self._messages_key = f"{self.session_id}:messages"     self._metadata_key = f"{self.session_id}:metadata" ``` |

### from\_address `classmethod`

```
from_address(
    session_id: str,
    *,
    state_store_name: str,
    dapr_address: str = "localhost:50001",
    session_settings: SessionSettings | None = None,
    **kwargs: Any,
) -> DaprSession
```

Create a session from a Dapr sidecar address.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Conversation ID. | *required* |
| `state_store_name` | `str` | Name of the Dapr state store component. | *required* |
| `dapr_address` | `str` | Dapr sidecar gRPC address. Defaults to "localhost:50001". | `'localhost:50001'` |
| `session_settings` | `SessionSettings | None` | Session configuration settings including default limit for retrieving items. If None, uses default SessionSettings(). | `None` |
| `**kwargs` | `Any` | Additional keyword arguments forwarded to the main constructor (e.g., ttl, consistency). | `{}` |

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `DaprSession` | `DaprSession` | An instance of DaprSession connected to the specified Dapr sidecar. |

Note

The Dapr Python SDK performs health checks on the HTTP endpoint (default: http://localhost:3500).
Ensure the Dapr sidecar is started with --dapr-http-port 3500. Alternatively, set one of
these environment variables: DAPR\_HTTP\_ENDPOINT (e.g., "http://localhost:3500") or
DAPR\_HTTP\_PORT (e.g., "3500") to avoid connection errors.

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 ``` | ``` @classmethod def from_address(     cls,     session_id: str,     *,     state_store_name: str,     dapr_address: str = "localhost:50001",     session_settings: SessionSettings | None = None,     **kwargs: Any, ) -> DaprSession:     """Create a session from a Dapr sidecar address.      Args:         session_id (str): Conversation ID.         state_store_name (str): Name of the Dapr state store component.         dapr_address (str): Dapr sidecar gRPC address. Defaults to "localhost:50001".         session_settings (SessionSettings | None): Session configuration settings including             default limit for retrieving items. If None, uses default SessionSettings().         **kwargs: Additional keyword arguments forwarded to the main constructor             (e.g., ttl, consistency).      Returns:         DaprSession: An instance of DaprSession connected to the specified Dapr sidecar.      Note:         The Dapr Python SDK performs health checks on the HTTP endpoint (default: http://localhost:3500).         Ensure the Dapr sidecar is started with --dapr-http-port 3500. Alternatively, set one of         these environment variables: DAPR_HTTP_ENDPOINT (e.g., "http://localhost:3500") or         DAPR_HTTP_PORT (e.g., "3500") to avoid connection errors.     """     dapr_client = DaprClient(address=dapr_address)     session = cls(         session_id,         state_store_name=state_store_name,         dapr_client=dapr_client,         session_settings=session_settings,         **kwargs,     )     session._owns_client = True  # We created the client, so we own it     return session ``` |

### get\_items `async`

```
get_items(
    limit: int | None = None,
) -> list[TResponseInputItem]
```

Retrieve the conversation history for this session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `limit` | `int | None` | Maximum number of items to retrieve. If None, uses session\_settings.limit. When specified, returns the latest N items in chronological order. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `list[TResponseInputItem]` | List of input items representing the conversation history |

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 ``` | ``` async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:     """Retrieve the conversation history for this session.      Args:         limit: Maximum number of items to retrieve. If None, uses session_settings.limit.                When specified, returns the latest N items in chronological order.      Returns:         List of input items representing the conversation history     """     session_limit = resolve_session_limit(limit, self.session_settings)      async with self._lock:         # Get messages from state store with consistency level         response = await self._dapr_client.get_state(             store_name=self._state_store_name,             key=self._messages_key,             state_metadata=self._get_read_metadata(),         )          messages = self._decode_messages(response.data)         if not messages:             return []         if session_limit is not None:             if session_limit <= 0:                 return []             messages = messages[-session_limit:]         items: list[TResponseInputItem] = []         for msg in messages:             try:                 if isinstance(msg, str):                     item = await self._deserialize_item(msg)                 else:                     item = msg                 items.append(item)             except (json.JSONDecodeError, TypeError):                 continue         return items ``` |

### add\_items `async`

```
add_items(items: list[TResponseInputItem]) -> None
```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | *required* |

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 ``` | ``` async def add_items(self, items: list[TResponseInputItem]) -> None:     """Add new items to the conversation history.      Args:         items: List of input items to add to the history     """     if not items:         return      async with self._lock:         serialized_items: list[str] = [await self._serialize_item(item) for item in items]         attempt = 0         while True:             attempt += 1             response = await self._dapr_client.get_state(                 store_name=self._state_store_name,                 key=self._messages_key,                 state_metadata=self._get_read_metadata(),             )             existing_messages = self._decode_messages_for_update(response.data)             updated_messages = existing_messages + serialized_items             messages_json = json.dumps(updated_messages, separators=(",", ":"))             etag = response.etag             try:                 await self._dapr_client.save_state(                     store_name=self._state_store_name,                     key=self._messages_key,                     value=messages_json,                     etag=etag,                     state_metadata=self._get_metadata(),                     options=self._get_state_options(concurrency=Concurrency.first_write),                 )                 break             except Exception as error:                 should_retry = await self._handle_concurrency_conflict(error, attempt)                 if should_retry:                     continue                 raise          # Update metadata         metadata = {             "session_id": self.session_id,             "created_at": str(int(time.time())),             "updated_at": str(int(time.time())),         }         await self._dapr_client.save_state(             store_name=self._state_store_name,             key=self._metadata_key,             value=json.dumps(metadata),             state_metadata=self._get_metadata(),             options=self._get_state_options(),         ) ``` |

### pop\_item `async`

```
pop_item() -> TResponseInputItem | None
```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 ``` | ``` async def pop_item(self) -> TResponseInputItem | None:     """Remove and return the most recent item from the session.      Returns:         The most recent item if it exists, None if the session is empty     """     async with self._lock:         while True:             attempt = 0             while True:                 attempt += 1                 response = await self._dapr_client.get_state(                     store_name=self._state_store_name,                     key=self._messages_key,                     state_metadata=self._get_read_metadata(),                 )                 messages = self._decode_messages(response.data)                 if not messages:                     return None                 last_item = messages.pop()                 messages_json = json.dumps(messages, separators=(",", ":"))                 etag = getattr(response, "etag", None) or None                 try:                     await self._dapr_client.save_state(                         store_name=self._state_store_name,                         key=self._messages_key,                         value=messages_json,                         etag=etag,                         state_metadata=self._get_metadata(),                         options=self._get_state_options(concurrency=Concurrency.first_write),                     )                     break                 except Exception as error:                     should_retry = await self._handle_concurrency_conflict(error, attempt)                     if should_retry:                         continue                     raise             try:                 if isinstance(last_item, str):                     return await self._deserialize_item(last_item)                 return last_item  # type: ignore[no-any-return]             except (json.JSONDecodeError, TypeError):                 continue ``` |

### clear\_session `async`

```
clear_session() -> None
```

Clear all items for this session.

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 ``` | ``` async def clear_session(self) -> None:     """Clear all items for this session."""     async with self._lock:         # Delete messages and metadata keys         await self._dapr_client.delete_state(             store_name=self._state_store_name,             key=self._messages_key,             options=self._get_state_options(),         )          await self._dapr_client.delete_state(             store_name=self._state_store_name,             key=self._metadata_key,             options=self._get_state_options(),         ) ``` |

### close `async`

```
close() -> None
```

Close the Dapr client connection.

Only closes the connection if this session owns the Dapr client
(i.e., created via from\_address). If the client was injected externally,
the caller is responsible for managing its lifecycle.

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 405 406 407 408 409 410 411 412 413 ``` | ``` async def close(self) -> None:     """Close the Dapr client connection.      Only closes the connection if this session owns the Dapr client     (i.e., created via from_address). If the client was injected externally,     the caller is responsible for managing its lifecycle.     """     if self._owns_client:         await self._dapr_client.close() ``` |

### \_\_aenter\_\_ `async`

```
__aenter__() -> DaprSession
```

Enter async context manager.

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 415 416 417 ``` | ``` async def __aenter__(self) -> DaprSession:     """Enter async context manager."""     return self ``` |

### \_\_aexit\_\_ `async`

```
__aexit__(exc_type, exc_val, exc_tb) -> None
```

Exit async context manager and close the connection.

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 419 420 421 ``` | ``` async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:     """Exit async context manager and close the connection."""     await self.close() ``` |

### ping `async`

```
ping() -> bool
```

Test Dapr connectivity by checking metadata.

Returns:

| Type | Description |
| --- | --- |
| `bool` | True if Dapr is reachable, False otherwise. |

Source code in `src/agents/extensions/memory/dapr_session.py`

|  |  |
| --- | --- |
| ``` 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 ``` | ``` async def ping(self) -> bool:     """Test Dapr connectivity by checking metadata.      Returns:         True if Dapr is reachable, False otherwise.     """     try:         # First attempt a read; some stores may not be initialized yet.         await self._dapr_client.get_state(             store_name=self._state_store_name,             key="__ping__",             state_metadata=self._get_read_metadata(),         )         return True     except Exception as initial_error:         # If relation/table is missing or store isn't initialized,         # attempt a write to initialize it, then read again.         try:             await self._dapr_client.save_state(                 store_name=self._state_store_name,                 key="__ping__",                 value="ok",                 state_metadata=self._get_metadata(),                 options=self._get_state_options(),             )             # Read again after write.             await self._dapr_client.get_state(                 store_name=self._state_store_name,                 key="__ping__",                 state_metadata=self._get_read_metadata(),             )             return True         except Exception:             logger.error("Dapr connection failed: %s", initial_error)             return False ``` |