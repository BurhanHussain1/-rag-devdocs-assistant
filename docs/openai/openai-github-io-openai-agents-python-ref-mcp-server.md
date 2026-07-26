---
url: https://openai.github.io/openai-agents-python/ref/mcp/server/
title: `MCP Servers`
framework: openai
---

# `MCP Servers`

### MCPServer

Bases: `ABC`

Base class for Model Context Protocol servers.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 ``` | ``` class MCPServer(abc.ABC):     """Base class for Model Context Protocol servers."""      def __init__(         self,         use_structured_content: bool = False,         require_approval: RequireApprovalSetting = None,         failure_error_function: ToolErrorFunction | None | _UnsetType = _UNSET,         tool_meta_resolver: MCPToolMetaResolver | None = None,         custom_data_extractor: MCPToolCustomDataExtractor | None = None,     ):         """         Args:             use_structured_content: Whether to use `tool_result.structured_content` when calling an                 MCP tool. Defaults to False for backwards compatibility - most MCP servers still                 include the structured content in the `tool_result.content`, and using it by                 default will cause duplicate content. You can set this to True if you know the                 server will not duplicate the structured content in the `tool_result.content`.             require_approval: Approval policy for tools on this server. Accepts "always"/"never",                 a dict of tool names to those values, a boolean, an object with always/never                 tool lists (mirroring TS requireApproval), or a sync/async callable that receives                 `(run_context, agent, tool)` and returns whether the tool call needs approval.                 Normalized into a needs_approval policy.             failure_error_function: Optional function used to convert MCP tool failures into                 a model-visible error message. If explicitly set to None, tool errors will be                 raised instead of converted. If left unset, the agent-level configuration (or                 SDK default) will be used.             tool_meta_resolver: Optional callable that produces MCP request metadata (`_meta`) for                 tool calls. It is invoked by the Agents SDK before calling `call_tool`.             custom_data_extractor: Optional callable that produces SDK-only custom data for                 emitted MCP tool output items.         """         self.use_structured_content = use_structured_content         self._needs_approval_policy = self._normalize_needs_approval(             require_approval=require_approval         )         self._failure_error_function = failure_error_function         self.tool_meta_resolver = tool_meta_resolver         self.custom_data_extractor = custom_data_extractor      @abc.abstractmethod     async def connect(self):         """Connect to the server. For example, this might mean spawning a subprocess or         opening a network connection. The server is expected to remain connected until         `cleanup()` is called.         """         pass      @property     @abc.abstractmethod     def name(self) -> str:         """A readable name for the server."""         pass      @abc.abstractmethod     async def cleanup(self):         """Cleanup the server. For example, this might mean closing a subprocess or         closing a network connection.         """         pass      @abc.abstractmethod     async def list_tools(         self,         run_context: RunContextWrapper[Any] | None = None,         agent: AgentBase | None = None,     ) -> list[MCPTool]:         """List the tools available on the server."""         pass      @abc.abstractmethod     async def call_tool(         self,         tool_name: str,         arguments: dict[str, Any] | None,         meta: dict[str, Any] | None = None,     ) -> CallToolResult:         """Invoke a tool on the server."""         pass      @property     def cached_tools(self) -> list[MCPTool] | None:         """Return the most recently fetched tools list, if available.          Implementations may return `None` when tools have not been fetched yet or caching is         disabled.         """          return None      @abc.abstractmethod     async def list_prompts(         self,     ) -> ListPromptsResult:         """List the prompts available on the server."""         pass      @abc.abstractmethod     async def get_prompt(         self, name: str, arguments: dict[str, Any] | None = None     ) -> GetPromptResult:         """Get a specific prompt from the server."""         pass      async def list_resources(self, cursor: str | None = None) -> ListResourcesResult:         """List the resources available on the server.          Args:             cursor: An opaque pagination cursor returned in a previous                 :class:`~mcp.types.ListResourcesResult` as ``nextCursor``.  Pass it                 here to fetch the next page of results.  ``None`` fetches the first                 page.          Returns a :class:`~mcp.types.ListResourcesResult`.  When the result contains         a ``nextCursor`` field, call this method again with that cursor to retrieve         the next page.  Subclasses that do not support resources may leave this         unimplemented; it will raise :exc:`NotImplementedError` at call time.         """         raise NotImplementedError(             f"MCP server '{self.name}' does not support list_resources. "             "Override this method in your server implementation."         )      async def list_resource_templates(         self, cursor: str | None = None     ) -> ListResourceTemplatesResult:         """List the resource templates available on the server.          Args:             cursor: An opaque pagination cursor returned in a previous                 :class:`~mcp.types.ListResourceTemplatesResult` as ``nextCursor``.                 Pass it here to fetch the next page of results.  ``None`` fetches                 the first page.          Returns a :class:`~mcp.types.ListResourceTemplatesResult`.  When the result         contains a ``nextCursor`` field, call this method again with that cursor to         retrieve the next page.  Subclasses that do not support resource templates         may leave this unimplemented; it will raise :exc:`NotImplementedError` at         call time.         """         raise NotImplementedError(             f"MCP server '{self.name}' does not support list_resource_templates. "             "Override this method in your server implementation."         )      async def read_resource(self, uri: str) -> ReadResourceResult:         """Read the contents of a specific resource by URI.          Args:             uri: The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl`                 for the supported URI formats.          Returns a :class:`~mcp.types.ReadResourceResult`.  Subclasses that do not         support resources may leave this unimplemented; it will raise         :exc:`NotImplementedError` at call time.         """         raise NotImplementedError(             f"MCP server '{self.name}' does not support read_resource. "             "Override this method in your server implementation."         )      @staticmethod     def _normalize_needs_approval(         *,         require_approval: RequireApprovalSetting,     ) -> (         bool         | dict[str, bool]         | Callable[[RunContextWrapper[Any], AgentBase, MCPTool], MaybeAwaitable[bool]]     ):         """Normalize approval inputs to booleans or a name->bool map."""          if require_approval is None:             return False          def _to_bool(value: object, *, location: str) -> bool:             if value == "always":                 return True             if value == "never":                 return False             raise UserError(                 f"Invalid require_approval value at {location}: "                 f"expected 'always' or 'never', got {value!r}."             )          def _validate_tool_names(value: object, *, location: str) -> list[str]:             if not isinstance(value, list):                 raise UserError(                     f"Invalid require_approval tool_names at {location}: "                     f"expected a list of strings, got {type(value).__name__}."                 )              tool_names: list[str] = []             for index, tool_name in enumerate(value):                 if not isinstance(tool_name, str):                     raise UserError(                         f"Invalid require_approval tool name at {location}[{index}]: "                         f"expected a string, got {type(tool_name).__name__}."                     )                 tool_names.append(tool_name)             return tool_names          def _get_tool_names_entry(value: object, *, policy: str) -> list[str]:             if not isinstance(value, dict):                 raise UserError(                     f"Invalid require_approval.{policy}: "                     f"expected an object with tool_names, got {type(value).__name__}."                 )             return _validate_tool_names(                 value.get("tool_names", []),                 location=f"require_approval.{policy}.tool_names",             )          def _is_tool_list_schema(value: object) -> bool:             if not isinstance(value, dict):                 return False             for key in ("always", "never"):                 if key not in value:                     continue                 entry = value.get(key)                 if isinstance(entry, dict) and "tool_names" in entry:                     return True             return False          if isinstance(require_approval, dict) and _is_tool_list_schema(require_approval):             always_entry: RequireApprovalToolList | Any = require_approval.get("always", {})             never_entry: RequireApprovalToolList | Any = require_approval.get("never", {})             invalid_keys = sorted(set(require_approval) - {"always", "never"})             if invalid_keys:                 raise UserError(                     "Invalid require_approval tool list policy: "                     f"unexpected keys {invalid_keys!r}; expected only 'always' and 'never'."                 )             always_names = _get_tool_names_entry(always_entry, policy="always")             never_names = _get_tool_names_entry(never_entry, policy="never")             overlapping_names = sorted(set(always_names) & set(never_names))             if overlapping_names:                 raise UserError(                     "Invalid require_approval tool list policy: "                     f"tool names cannot appear in both always and never: {overlapping_names!r}."                 )             tool_list_mapping: dict[str, bool] = {}             for name in always_names:                 tool_list_mapping[name] = True             for name in never_names:                 tool_list_mapping[name] = False             return tool_list_mapping          if isinstance(require_approval, dict):             tool_mapping: dict[str, bool] = {}             for name, value in require_approval.items():                 if isinstance(value, bool):                     tool_mapping[str(name)] = value                 else:                     tool_mapping[str(name)] = _to_bool(                         value, location=f"require_approval[{name!r}]"                     )             return tool_mapping          if callable(require_approval):             return require_approval          if isinstance(require_approval, bool):             return require_approval          return _to_bool(require_approval, location="require_approval")      def _get_needs_approval_for_tool(         self,         tool: MCPTool,         agent: AgentBase | None,     ) -> bool | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]]:         """Return a FunctionTool.needs_approval value for a given MCP tool.          Legacy callers may omit ``agent`` when using ``MCPUtil.to_function_tool()`` directly.         When approval is configured with a callable policy and no agent is available, this method         returns ``True`` to preserve the historical fail-closed behavior.         """          policy = self._needs_approval_policy          if callable(policy):             if agent is None:                 return True              async def _needs_approval(                 run_context: RunContextWrapper[Any], _args: dict[str, Any], _call_id: str             ) -> bool:                 result = policy(run_context, agent, tool)                 if inspect.isawaitable(result):                     result = await result                 return bool(result)              return _needs_approval          if isinstance(policy, dict):             return bool(policy.get(tool.name, False))          return bool(policy)      def _get_failure_error_function(         self, agent_failure_error_function: ToolErrorFunction | None     ) -> ToolErrorFunction | None:         """Return the effective error handler for MCP tool failures."""         if self._failure_error_function is _UNSET:             return agent_failure_error_function         return cast(ToolErrorFunction | None, self._failure_error_function) ``` |

#### name `abstractmethod` `property`

```
name: str
```

A readable name for the server.

#### cached\_tools `property`

```
cached_tools: list[Tool] | None
```

Return the most recently fetched tools list, if available.

Implementations may return `None` when tools have not been fetched yet or caching is
disabled.

#### \_\_init\_\_

```
__init__(
    use_structured_content: bool = False,
    require_approval: RequireApprovalSetting = None,
    failure_error_function: ToolErrorFunction
    | None
    | _UnsetType = _UNSET,
    tool_meta_resolver: MCPToolMetaResolver | None = None,
    custom_data_extractor: MCPToolCustomDataExtractor
    | None = None,
)
```

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `use_structured_content` | `bool` | Whether to use `tool_result.structured_content` when calling an MCP tool. Defaults to False for backwards compatibility - most MCP servers still include the structured content in the `tool_result.content`, and using it by default will cause duplicate content. You can set this to True if you know the server will not duplicate the structured content in the `tool_result.content`. | `False` |
| `require_approval` | `RequireApprovalSetting` | Approval policy for tools on this server. Accepts "always"/"never", a dict of tool names to those values, a boolean, an object with always/never tool lists (mirroring TS requireApproval), or a sync/async callable that receives `(run_context, agent, tool)` and returns whether the tool call needs approval. Normalized into a needs\_approval policy. | `None` |
| `failure_error_function` | `ToolErrorFunction | None | _UnsetType` | Optional function used to convert MCP tool failures into a model-visible error message. If explicitly set to None, tool errors will be raised instead of converted. If left unset, the agent-level configuration (or SDK default) will be used. | `_UNSET` |
| `tool_meta_resolver` | `MCPToolMetaResolver | None` | Optional callable that produces MCP request metadata (`_meta`) for tool calls. It is invoked by the Agents SDK before calling `call_tool`. | `None` |
| `custom_data_extractor` | `MCPToolCustomDataExtractor | None` | Optional callable that produces SDK-only custom data for emitted MCP tool output items. | `None` |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 ``` | ``` def __init__(     self,     use_structured_content: bool = False,     require_approval: RequireApprovalSetting = None,     failure_error_function: ToolErrorFunction | None | _UnsetType = _UNSET,     tool_meta_resolver: MCPToolMetaResolver | None = None,     custom_data_extractor: MCPToolCustomDataExtractor | None = None, ):     """     Args:         use_structured_content: Whether to use `tool_result.structured_content` when calling an             MCP tool. Defaults to False for backwards compatibility - most MCP servers still             include the structured content in the `tool_result.content`, and using it by             default will cause duplicate content. You can set this to True if you know the             server will not duplicate the structured content in the `tool_result.content`.         require_approval: Approval policy for tools on this server. Accepts "always"/"never",             a dict of tool names to those values, a boolean, an object with always/never             tool lists (mirroring TS requireApproval), or a sync/async callable that receives             `(run_context, agent, tool)` and returns whether the tool call needs approval.             Normalized into a needs_approval policy.         failure_error_function: Optional function used to convert MCP tool failures into             a model-visible error message. If explicitly set to None, tool errors will be             raised instead of converted. If left unset, the agent-level configuration (or             SDK default) will be used.         tool_meta_resolver: Optional callable that produces MCP request metadata (`_meta`) for             tool calls. It is invoked by the Agents SDK before calling `call_tool`.         custom_data_extractor: Optional callable that produces SDK-only custom data for             emitted MCP tool output items.     """     self.use_structured_content = use_structured_content     self._needs_approval_policy = self._normalize_needs_approval(         require_approval=require_approval     )     self._failure_error_function = failure_error_function     self.tool_meta_resolver = tool_meta_resolver     self.custom_data_extractor = custom_data_extractor ``` |

#### connect `abstractmethod` `async`

```
connect()
```

Connect to the server. For example, this might mean spawning a subprocess or
opening a network connection. The server is expected to remain connected until
`cleanup()` is called.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 265 266 267 268 269 270 271 ``` | ``` @abc.abstractmethod async def connect(self):     """Connect to the server. For example, this might mean spawning a subprocess or     opening a network connection. The server is expected to remain connected until     `cleanup()` is called.     """     pass ``` |

#### cleanup `abstractmethod` `async`

```
cleanup()
```

Cleanup the server. For example, this might mean closing a subprocess or
closing a network connection.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 279 280 281 282 283 284 ``` | ``` @abc.abstractmethod async def cleanup(self):     """Cleanup the server. For example, this might mean closing a subprocess or     closing a network connection.     """     pass ``` |

#### list\_tools `abstractmethod` `async`

```
list_tools(
    run_context: RunContextWrapper[Any] | None = None,
    agent: AgentBase | None = None,
) -> list[Tool]
```

List the tools available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 286 287 288 289 290 291 292 293 ``` | ``` @abc.abstractmethod async def list_tools(     self,     run_context: RunContextWrapper[Any] | None = None,     agent: AgentBase | None = None, ) -> list[MCPTool]:     """List the tools available on the server."""     pass ``` |

#### call\_tool `abstractmethod` `async`

```
call_tool(
    tool_name: str,
    arguments: dict[str, Any] | None,
    meta: dict[str, Any] | None = None,
) -> CallToolResult
```

Invoke a tool on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 295 296 297 298 299 300 301 302 303 ``` | ``` @abc.abstractmethod async def call_tool(     self,     tool_name: str,     arguments: dict[str, Any] | None,     meta: dict[str, Any] | None = None, ) -> CallToolResult:     """Invoke a tool on the server."""     pass ``` |

#### list\_prompts `abstractmethod` `async`

```
list_prompts() -> ListPromptsResult
```

List the prompts available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 315 316 317 318 319 320 ``` | ``` @abc.abstractmethod async def list_prompts(     self, ) -> ListPromptsResult:     """List the prompts available on the server."""     pass ``` |

#### get\_prompt `abstractmethod` `async`

```
get_prompt(
    name: str, arguments: dict[str, Any] | None = None
) -> GetPromptResult
```

Get a specific prompt from the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 322 323 324 325 326 327 ``` | ``` @abc.abstractmethod async def get_prompt(     self, name: str, arguments: dict[str, Any] | None = None ) -> GetPromptResult:     """Get a specific prompt from the server."""     pass ``` |

#### list\_resources `async`

```
list_resources(
    cursor: str | None = None,
) -> ListResourcesResult
```

List the resources available on the server.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `cursor` | `str | None` | An opaque pagination cursor returned in a previous :class:`~mcp.types.ListResourcesResult` as `nextCursor`. Pass it here to fetch the next page of results. `None` fetches the first page. | `None` |

Returns a :class:`~mcp.types.ListResourcesResult`. When the result contains
a `nextCursor` field, call this method again with that cursor to retrieve
the next page. Subclasses that do not support resources may leave this
unimplemented; it will raise :exc:`NotImplementedError` at call time.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 ``` | ``` async def list_resources(self, cursor: str | None = None) -> ListResourcesResult:     """List the resources available on the server.      Args:         cursor: An opaque pagination cursor returned in a previous             :class:`~mcp.types.ListResourcesResult` as ``nextCursor``.  Pass it             here to fetch the next page of results.  ``None`` fetches the first             page.      Returns a :class:`~mcp.types.ListResourcesResult`.  When the result contains     a ``nextCursor`` field, call this method again with that cursor to retrieve     the next page.  Subclasses that do not support resources may leave this     unimplemented; it will raise :exc:`NotImplementedError` at call time.     """     raise NotImplementedError(         f"MCP server '{self.name}' does not support list_resources. "         "Override this method in your server implementation."     ) ``` |

#### list\_resource\_templates `async`

```
list_resource_templates(
    cursor: str | None = None,
) -> ListResourceTemplatesResult
```

List the resource templates available on the server.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `cursor` | `str | None` | An opaque pagination cursor returned in a previous :class:`~mcp.types.ListResourceTemplatesResult` as `nextCursor`. Pass it here to fetch the next page of results. `None` fetches the first page. | `None` |

Returns a :class:`~mcp.types.ListResourceTemplatesResult`. When the result
contains a `nextCursor` field, call this method again with that cursor to
retrieve the next page. Subclasses that do not support resource templates
may leave this unimplemented; it will raise :exc:`NotImplementedError` at
call time.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 ``` | ``` async def list_resource_templates(     self, cursor: str | None = None ) -> ListResourceTemplatesResult:     """List the resource templates available on the server.      Args:         cursor: An opaque pagination cursor returned in a previous             :class:`~mcp.types.ListResourceTemplatesResult` as ``nextCursor``.             Pass it here to fetch the next page of results.  ``None`` fetches             the first page.      Returns a :class:`~mcp.types.ListResourceTemplatesResult`.  When the result     contains a ``nextCursor`` field, call this method again with that cursor to     retrieve the next page.  Subclasses that do not support resource templates     may leave this unimplemented; it will raise :exc:`NotImplementedError` at     call time.     """     raise NotImplementedError(         f"MCP server '{self.name}' does not support list_resource_templates. "         "Override this method in your server implementation."     ) ``` |

#### read\_resource `async`

```
read_resource(uri: str) -> ReadResourceResult
```

Read the contents of a specific resource by URI.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `str` | The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl` for the supported URI formats. | *required* |

Returns a :class:`~mcp.types.ReadResourceResult`. Subclasses that do not
support resources may leave this unimplemented; it will raise
:exc:`NotImplementedError` at call time.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 ``` | ``` async def read_resource(self, uri: str) -> ReadResourceResult:     """Read the contents of a specific resource by URI.      Args:         uri: The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl`             for the supported URI formats.      Returns a :class:`~mcp.types.ReadResourceResult`.  Subclasses that do not     support resources may leave this unimplemented; it will raise     :exc:`NotImplementedError` at call time.     """     raise NotImplementedError(         f"MCP server '{self.name}' does not support read_resource. "         "Override this method in your server implementation."     ) ``` |

### MCPServerStdioParams

Bases: `TypedDict`

Mirrors `mcp.client.stdio.StdioServerParameters`, but lets you pass params without another
import.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1081 1082 1083 1084 1085 1086 1087 1088 1089 1090 1091 1092 1093 1094 1095 1096 1097 1098 1099 1100 1101 1102 1103 1104 1105 1106 1107 ``` | ``` class MCPServerStdioParams(TypedDict):     """Mirrors `mcp.client.stdio.StdioServerParameters`, but lets you pass params without another     import.     """      command: str     """The executable to run to start the server. For example, `python` or `node`."""      args: NotRequired[list[str]]     """Command line args to pass to the `command` executable. For example, `['foo.py']` or     `['server.js', '--port', '8080']`."""      env: NotRequired[dict[str, str]]     """The environment variables to set for the server."""      cwd: NotRequired[str | Path]     """The working directory to use when spawning the process."""      encoding: NotRequired[str]     """The text encoding used when sending/receiving messages to the server. Defaults to `utf-8`."""      encoding_error_handler: NotRequired[Literal["strict", "ignore", "replace"]]     """The text encoding error handler. Defaults to `strict`.      See https://docs.python.org/3/library/codecs.html#codec-base-classes for     explanations of possible values.     """ ``` |

#### command `instance-attribute`

```
command: str
```

The executable to run to start the server. For example, `python` or `node`.

#### args `instance-attribute`

```
args: NotRequired[list[str]]
```

Command line args to pass to the `command` executable. For example, `['foo.py']` or
`['server.js', '--port', '8080']`.

#### env `instance-attribute`

```
env: NotRequired[dict[str, str]]
```

The environment variables to set for the server.

#### cwd `instance-attribute`

```
cwd: NotRequired[str | Path]
```

The working directory to use when spawning the process.

#### encoding `instance-attribute`

```
encoding: NotRequired[str]
```

The text encoding used when sending/receiving messages to the server. Defaults to `utf-8`.

#### encoding\_error\_handler `instance-attribute`

```
encoding_error_handler: NotRequired[
    Literal["strict", "ignore", "replace"]
]
```

The text encoding error handler. Defaults to `strict`.

See https://docs.python.org/3/library/codecs.html#codec-base-classes for
explanations of possible values.

### MCPServerStdio

Bases: `_MCPServerWithClientSession`

MCP server implementation that uses the stdio transport. See the [spec]
(https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/#stdio) for
details.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1110 1111 1112 1113 1114 1115 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 1136 1137 1138 1139 1140 1141 1142 1143 1144 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 1194 1195 1196 1197 1198 1199 1200 1201 1202 1203 1204 1205 ``` | ``` class MCPServerStdio(_MCPServerWithClientSession):     """MCP server implementation that uses the stdio transport. See the [spec]     (https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/#stdio) for     details.     """      def __init__(         self,         params: MCPServerStdioParams,         cache_tools_list: bool = False,         name: str | None = None,         client_session_timeout_seconds: float | None = 5,         tool_filter: ToolFilter = None,         use_structured_content: bool = False,         max_retry_attempts: int = 0,         retry_backoff_seconds_base: float = 1.0,         message_handler: MessageHandlerFnT | None = None,         require_approval: RequireApprovalSetting = None,         failure_error_function: ToolErrorFunction | None | _UnsetType = _UNSET,         tool_meta_resolver: MCPToolMetaResolver | None = None,         custom_data_extractor: MCPToolCustomDataExtractor | None = None,     ):         """Create a new MCP server based on the stdio transport.          Args:             params: The params that configure the server. This includes the command to run to                 start the server, the args to pass to the command, the environment variables to                 set for the server, the working directory to use when spawning the process, and                 the text encoding used when sending/receiving messages to the server.             cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be                 cached and only fetched from the server once. If `False`, the tools list will be                 fetched from the server on each call to `list_tools()`. The cache can be                 invalidated by calling `invalidate_tools_cache()`. You should set this to `True`                 if you know the server will not change its tools list, because it can drastically                 improve latency (by avoiding a round-trip to the server every time).             name: A readable name for the server. If not provided, we'll create one from the                 command.             client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.             tool_filter: The tool filter to use for filtering tools.             use_structured_content: Whether to use `tool_result.structured_content` when calling an                 MCP tool. Defaults to False for backwards compatibility - most MCP servers still                 include the structured content in the `tool_result.content`, and using it by                 default will cause duplicate content. You can set this to True if you know the                 server will not duplicate the structured content in the `tool_result.content`.             max_retry_attempts: Number of times to retry failed list_tools/call_tool calls.                 Defaults to no retries.             retry_backoff_seconds_base: The base delay, in seconds, for exponential                 backoff between retries.             message_handler: Optional handler invoked for session messages as delivered by the                 ClientSession.             require_approval: Approval policy for tools on this server. Accepts "always"/"never",                 a dict of tool names to those values, or an object with always/never tool lists.             failure_error_function: Optional function used to convert MCP tool failures into                 a model-visible error message. If explicitly set to None, tool errors will be                 raised instead of converted. If left unset, the agent-level configuration (or                 SDK default) will be used.             tool_meta_resolver: Optional callable that produces MCP request metadata (`_meta`) for                 tool calls. It is invoked by the Agents SDK before calling `call_tool`.             custom_data_extractor: Optional callable that produces SDK-only custom data for                 emitted MCP tool output items.         """         super().__init__(             cache_tools_list=cache_tools_list,             client_session_timeout_seconds=client_session_timeout_seconds,             tool_filter=tool_filter,             use_structured_content=use_structured_content,             max_retry_attempts=max_retry_attempts,             retry_backoff_seconds_base=retry_backoff_seconds_base,             message_handler=message_handler,             require_approval=require_approval,             failure_error_function=failure_error_function,             tool_meta_resolver=tool_meta_resolver,             custom_data_extractor=custom_data_extractor,         )          self.params = StdioServerParameters(             command=params["command"],             args=params.get("args", []),             env=params.get("env"),             cwd=params.get("cwd"),             encoding=params.get("encoding", "utf-8"),             encoding_error_handler=params.get("encoding_error_handler", "strict"),         )          self._name = name or f"stdio: {self.params.command}"      def create_streams(         self,     ) -> AbstractAsyncContextManager[MCPStreamTransport]:         """Create the streams for the server."""         return stdio_client(self.params)      @property     def name(self) -> str:         """A readable name for the server."""         return self._name ``` |

#### name `property`

```
name: str
```

A readable name for the server.

#### \_\_init\_\_

```
__init__(
    params: MCPServerStdioParams,
    cache_tools_list: bool = False,
    name: str | None = None,
    client_session_timeout_seconds: float | None = 5,
    tool_filter: ToolFilter = None,
    use_structured_content: bool = False,
    max_retry_attempts: int = 0,
    retry_backoff_seconds_base: float = 1.0,
    message_handler: MessageHandlerFnT | None = None,
    require_approval: RequireApprovalSetting = None,
    failure_error_function: ToolErrorFunction
    | None
    | _UnsetType = _UNSET,
    tool_meta_resolver: MCPToolMetaResolver | None = None,
    custom_data_extractor: MCPToolCustomDataExtractor
    | None = None,
)
```

Create a new MCP server based on the stdio transport.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `params` | `MCPServerStdioParams` | The params that configure the server. This includes the command to run to start the server, the args to pass to the command, the environment variables to set for the server, the working directory to use when spawning the process, and the text encoding used when sending/receiving messages to the server. | *required* |
| `cache_tools_list` | `bool` | Whether to cache the tools list. If `True`, the tools list will be cached and only fetched from the server once. If `False`, the tools list will be fetched from the server on each call to `list_tools()`. The cache can be invalidated by calling `invalidate_tools_cache()`. You should set this to `True` if you know the server will not change its tools list, because it can drastically improve latency (by avoiding a round-trip to the server every time). | `False` |
| `name` | `str | None` | A readable name for the server. If not provided, we'll create one from the command. | `None` |
| `client_session_timeout_seconds` | `float | None` | the read timeout passed to the MCP ClientSession. | `5` |
| `tool_filter` | `ToolFilter` | The tool filter to use for filtering tools. | `None` |
| `use_structured_content` | `bool` | Whether to use `tool_result.structured_content` when calling an MCP tool. Defaults to False for backwards compatibility - most MCP servers still include the structured content in the `tool_result.content`, and using it by default will cause duplicate content. You can set this to True if you know the server will not duplicate the structured content in the `tool_result.content`. | `False` |
| `max_retry_attempts` | `int` | Number of times to retry failed list\_tools/call\_tool calls. Defaults to no retries. | `0` |
| `retry_backoff_seconds_base` | `float` | The base delay, in seconds, for exponential backoff between retries. | `1.0` |
| `message_handler` | `MessageHandlerFnT | None` | Optional handler invoked for session messages as delivered by the ClientSession. | `None` |
| `require_approval` | `RequireApprovalSetting` | Approval policy for tools on this server. Accepts "always"/"never", a dict of tool names to those values, or an object with always/never tool lists. | `None` |
| `failure_error_function` | `ToolErrorFunction | None | _UnsetType` | Optional function used to convert MCP tool failures into a model-visible error message. If explicitly set to None, tool errors will be raised instead of converted. If left unset, the agent-level configuration (or SDK default) will be used. | `_UNSET` |
| `tool_meta_resolver` | `MCPToolMetaResolver | None` | Optional callable that produces MCP request metadata (`_meta`) for tool calls. It is invoked by the Agents SDK before calling `call_tool`. | `None` |
| `custom_data_extractor` | `MCPToolCustomDataExtractor | None` | Optional callable that produces SDK-only custom data for emitted MCP tool output items. | `None` |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 1136 1137 1138 1139 1140 1141 1142 1143 1144 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 1194 ``` | ``` def __init__(     self,     params: MCPServerStdioParams,     cache_tools_list: bool = False,     name: str | None = None,     client_session_timeout_seconds: float | None = 5,     tool_filter: ToolFilter = None,     use_structured_content: bool = False,     max_retry_attempts: int = 0,     retry_backoff_seconds_base: float = 1.0,     message_handler: MessageHandlerFnT | None = None,     require_approval: RequireApprovalSetting = None,     failure_error_function: ToolErrorFunction | None | _UnsetType = _UNSET,     tool_meta_resolver: MCPToolMetaResolver | None = None,     custom_data_extractor: MCPToolCustomDataExtractor | None = None, ):     """Create a new MCP server based on the stdio transport.      Args:         params: The params that configure the server. This includes the command to run to             start the server, the args to pass to the command, the environment variables to             set for the server, the working directory to use when spawning the process, and             the text encoding used when sending/receiving messages to the server.         cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be             cached and only fetched from the server once. If `False`, the tools list will be             fetched from the server on each call to `list_tools()`. The cache can be             invalidated by calling `invalidate_tools_cache()`. You should set this to `True`             if you know the server will not change its tools list, because it can drastically             improve latency (by avoiding a round-trip to the server every time).         name: A readable name for the server. If not provided, we'll create one from the             command.         client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.         tool_filter: The tool filter to use for filtering tools.         use_structured_content: Whether to use `tool_result.structured_content` when calling an             MCP tool. Defaults to False for backwards compatibility - most MCP servers still             include the structured content in the `tool_result.content`, and using it by             default will cause duplicate content. You can set this to True if you know the             server will not duplicate the structured content in the `tool_result.content`.         max_retry_attempts: Number of times to retry failed list_tools/call_tool calls.             Defaults to no retries.         retry_backoff_seconds_base: The base delay, in seconds, for exponential             backoff between retries.         message_handler: Optional handler invoked for session messages as delivered by the             ClientSession.         require_approval: Approval policy for tools on this server. Accepts "always"/"never",             a dict of tool names to those values, or an object with always/never tool lists.         failure_error_function: Optional function used to convert MCP tool failures into             a model-visible error message. If explicitly set to None, tool errors will be             raised instead of converted. If left unset, the agent-level configuration (or             SDK default) will be used.         tool_meta_resolver: Optional callable that produces MCP request metadata (`_meta`) for             tool calls. It is invoked by the Agents SDK before calling `call_tool`.         custom_data_extractor: Optional callable that produces SDK-only custom data for             emitted MCP tool output items.     """     super().__init__(         cache_tools_list=cache_tools_list,         client_session_timeout_seconds=client_session_timeout_seconds,         tool_filter=tool_filter,         use_structured_content=use_structured_content,         max_retry_attempts=max_retry_attempts,         retry_backoff_seconds_base=retry_backoff_seconds_base,         message_handler=message_handler,         require_approval=require_approval,         failure_error_function=failure_error_function,         tool_meta_resolver=tool_meta_resolver,         custom_data_extractor=custom_data_extractor,     )      self.params = StdioServerParameters(         command=params["command"],         args=params.get("args", []),         env=params.get("env"),         cwd=params.get("cwd"),         encoding=params.get("encoding", "utf-8"),         encoding_error_handler=params.get("encoding_error_handler", "strict"),     )      self._name = name or f"stdio: {self.params.command}" ``` |

#### create\_streams

```
create_streams() -> AbstractAsyncContextManager[
    MCPStreamTransport
]
```

Create the streams for the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1196 1197 1198 1199 1200 ``` | ``` def create_streams(     self, ) -> AbstractAsyncContextManager[MCPStreamTransport]:     """Create the streams for the server."""     return stdio_client(self.params) ``` |

#### connect `async`

```
connect()
```

Connect to the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 ``` | ``` async def connect(self):     """Connect to the server."""     connection_succeeded = False     try:         transport = await self.exit_stack.enter_async_context(self.create_streams())         # streamablehttp_client returns (read, write, get_session_id)         # sse_client returns (read, write)          read, write, *rest = transport         # Capture the session-id callback when present (streamablehttp_client only).         self._get_session_id = rest[0] if rest and callable(rest[0]) else None          session = await self.exit_stack.enter_async_context(             ClientSession(                 read,                 write,                 timedelta(seconds=self.client_session_timeout_seconds)                 if self.client_session_timeout_seconds                 else None,                 message_handler=self.message_handler,             )         )         server_result = await session.initialize()         self.server_initialize_result = server_result         self.session = session         connection_succeeded = True     except Exception as e:         # Try to extract HTTP error from exception or ExceptionGroup         http_error = self._extract_http_error_from_exception(e)         if http_error:             self._raise_user_error_for_http_error(http_error)          # For CancelledError, preserve cancellation semantics - don't wrap it.         # If it's masking an HTTP error, cleanup() will extract and raise UserError.         if isinstance(e, asyncio.CancelledError):             raise          # For HTTP-related errors, wrap them         if isinstance(e, httpx.HTTPStatusError | httpx.ConnectError | httpx.TimeoutException):             self._raise_user_error_for_http_error(e)          # For other errors, re-raise as-is (don't wrap non-HTTP errors)         raise     finally:         # Always attempt cleanup on error, but suppress cleanup errors that mask the original         if not connection_succeeded:             try:                 await self.cleanup()             except UserError:                 # Re-raise UserError from cleanup (contains the real HTTP error)                 raise             except Exception as cleanup_error:                 # Suppress RuntimeError about cancel scopes during cleanup - this is a known                 # issue with the MCP library's async generator cleanup and shouldn't mask the                 # original error                 if isinstance(cleanup_error, RuntimeError) and "cancel scope" in str(                     cleanup_error                 ):                     logger.debug(                         "Ignoring cancel scope error during cleanup of MCP server '%s': %s",                         self.name,                         cleanup_error,                     )                 else:                     # Log other cleanup errors but don't raise - original error is more                     # important                     logger.warning(                         "Error during cleanup of MCP server '%s': %s", self.name, cleanup_error                     ) ``` |

#### cleanup `async`

```
cleanup()
```

Cleanup the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 ``` | ``` async def cleanup(self):     """Cleanup the server."""     async with self._cleanup_lock:         # Only raise HTTP errors if we're cleaning up after a failed connection.         # During normal teardown (via __aexit__), log but don't raise to avoid         # masking the original exception.         is_failed_connection_cleanup = self.session is None          try:             await self.exit_stack.aclose()         except asyncio.CancelledError as e:             logger.debug("Cleanup cancelled for MCP server '%s': %s", self.name, e)             raise         except BaseExceptionGroup as eg:             # Extract HTTP errors from ExceptionGroup raised during cleanup             # This happens when background tasks fail (e.g., HTTP errors)             http_error = None             connect_error = None             timeout_error = None             error_message = f"Failed to connect to MCP server '{self.name}': "              for exc in eg.exceptions:                 if isinstance(exc, httpx.HTTPStatusError):                     http_error = exc                 elif isinstance(exc, httpx.ConnectError):                     connect_error = exc                 elif isinstance(exc, httpx.TimeoutException):                     timeout_error = exc              # Only raise HTTP errors if we're cleaning up after a failed connection.             # During normal teardown, log them instead.             if http_error:                 if is_failed_connection_cleanup:                     error_message += f"HTTP error {http_error.response.status_code} ({http_error.response.reason_phrase})"  # noqa: E501                     raise UserError(error_message) from http_error                 else:                     # Normal teardown - log but don't raise                     logger.warning(                         "HTTP error during cleanup of MCP server '%s': %s",                         self.name,                         http_error,                     )             elif connect_error:                 if is_failed_connection_cleanup:                     error_message += "Could not reach the server."                     raise UserError(error_message) from connect_error                 else:                     logger.warning(                         "Connection error during cleanup of MCP server '%s': %s",                         self.name,                         connect_error,                     )             elif timeout_error:                 if is_failed_connection_cleanup:                     error_message += "Connection timeout."                     raise UserError(error_message) from timeout_error                 else:                     logger.warning(                         "Timeout error during cleanup of MCP server '%s': %s",                         self.name,                         timeout_error,                     )             else:                 # No HTTP error found, suppress RuntimeError about cancel scopes                 has_cancel_scope_error = any(                     isinstance(exc, RuntimeError) and "cancel scope" in str(exc)                     for exc in eg.exceptions                 )                 if has_cancel_scope_error:                     logger.debug("Ignoring cancel scope error during cleanup: %s", eg)                 else:                     logger.error("Error cleaning up server: %s", eg)         except Exception as e:             # Suppress RuntimeError about cancel scopes - this is a known issue with the MCP             # library when background tasks fail during async generator cleanup             if isinstance(e, RuntimeError) and "cancel scope" in str(e):                 logger.debug("Ignoring cancel scope error during cleanup: %s", e)             else:                 logger.error("Error cleaning up server: %s", e)         finally:             self.session = None             self._get_session_id = None ``` |

#### list\_tools `async`

```
list_tools(
    run_context: RunContextWrapper[Any] | None = None,
    agent: AgentBase | None = None,
) -> list[Tool]
```

List the tools available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 833 834 835 836 837 838 839 840 841 842 843 844 845 846 847 848 849 850 851 852 853 854 855 856 857 858 859 860 861 862 863 864 865 866 867 868 869 870 871 ``` | ``` async def list_tools(     self,     run_context: RunContextWrapper[Any] | None = None,     agent: AgentBase | None = None, ) -> list[MCPTool]:     """List the tools available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None      try:         # Return from cache if caching is enabled, we have tools, and the cache is not dirty         if self.cache_tools_list and not self._cache_dirty and self._tools_list:             tools = self._tools_list         else:             # Fetch the tools from the server             result = await self._run_with_retries(                 lambda: self._maybe_serialize_request(lambda: session.list_tools())             )             self._tools_list = result.tools             self._cache_dirty = False             tools = self._tools_list          # Filter tools based on tool_filter         filtered_tools = tools         if self.tool_filter is not None:             filtered_tools = await self._apply_tool_filter(filtered_tools, run_context, agent)         return filtered_tools     except httpx.HTTPStatusError as e:         status_code = e.response.status_code         raise UserError(             f"Failed to list tools from MCP server '{self.name}': HTTP error {status_code}"         ) from e     except httpx.ConnectError as e:         raise UserError(             f"Failed to list tools from MCP server '{self.name}': Connection lost. "             f"The server may have disconnected."         ) from e ``` |

#### call\_tool `async`

```
call_tool(
    tool_name: str,
    arguments: dict[str, Any] | None,
    meta: dict[str, Any] | None = None,
) -> CallToolResult
```

Invoke a tool on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 900 901 902 903 904 905 906 907 908 ``` | ``` async def call_tool(     self,     tool_name: str,     arguments: dict[str, Any] | None,     meta: dict[str, Any] | None = None, ) -> CallToolResult:     """Invoke a tool on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None      try:         self._validate_required_parameters(tool_name=tool_name, arguments=arguments)         if meta is None:             return await self._run_with_retries(                 lambda: self._maybe_serialize_request(                     lambda: session.call_tool(tool_name, arguments)                 )             )         return await self._run_with_retries(             lambda: self._maybe_serialize_request(                 lambda: session.call_tool(tool_name, arguments, meta=meta)             )         )     except httpx.HTTPStatusError as e:         status_code = e.response.status_code         raise UserError(             f"Failed to call tool '{tool_name}' on MCP server '{self.name}': "             f"HTTP error {status_code}"         ) from e     except httpx.ConnectError as e:         raise UserError(             f"Failed to call tool '{tool_name}' on MCP server '{self.name}': Connection lost. "             f"The server may have disconnected."         ) from e ``` |

#### list\_prompts `async`

```
list_prompts() -> ListPromptsResult
```

List the prompts available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 944 945 946 947 948 949 950 951 952 ``` | ``` async def list_prompts(     self, ) -> ListPromptsResult:     """List the prompts available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_prompts()) ``` |

#### get\_prompt `async`

```
get_prompt(
    name: str, arguments: dict[str, Any] | None = None
) -> GetPromptResult
```

Get a specific prompt from the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 954 955 956 957 958 959 960 961 962 ``` | ``` async def get_prompt(     self, name: str, arguments: dict[str, Any] | None = None ) -> GetPromptResult:     """Get a specific prompt from the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.get_prompt(name, arguments)) ``` |

#### list\_resources `async`

```
list_resources(
    cursor: str | None = None,
) -> ListResourcesResult
```

List the resources available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 964 965 966 967 968 969 970 ``` | ``` async def list_resources(self, cursor: str | None = None) -> ListResourcesResult:     """List the resources available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_resources(cursor)) ``` |

#### list\_resource\_templates `async`

```
list_resource_templates(
    cursor: str | None = None,
) -> ListResourceTemplatesResult
```

List the resource templates available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 972 973 974 975 976 977 978 979 980 ``` | ``` async def list_resource_templates(     self, cursor: str | None = None ) -> ListResourceTemplatesResult:     """List the resource templates available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_resource_templates(cursor)) ``` |

#### read\_resource `async`

```
read_resource(uri: str) -> ReadResourceResult
```

Read the contents of a specific resource by URI.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `str` | The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl` for the supported URI formats. | *required* |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 982 983 984 985 986 987 988 989 990 991 992 993 994 995 ``` | ``` async def read_resource(self, uri: str) -> ReadResourceResult:     """Read the contents of a specific resource by URI.      Args:         uri: The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl`             for the supported URI formats.     """     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     from pydantic import AnyUrl      return await self._maybe_serialize_request(lambda: session.read_resource(AnyUrl(uri))) ``` |

#### invalidate\_tools\_cache

```
invalidate_tools_cache()
```

Invalidate the tools cache.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 719 720 721 ``` | ``` def invalidate_tools_cache(self):     """Invalidate the tools cache."""     self._cache_dirty = True ``` |

### MCPServerSseParams

Bases: `TypedDict`

Mirrors the params in `mcp.client.sse.sse_client`.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1208 1209 1210 1211 1212 1213 1214 1215 1216 1217 1218 1219 1220 1221 1222 1223 1224 1225 1226 1227 1228 1229 1230 1231 1232 ``` | ``` class MCPServerSseParams(TypedDict):     """Mirrors the params in `mcp.client.sse.sse_client`."""      url: str     """The URL of the server."""      headers: NotRequired[dict[str, str]]     """The headers to send to the server."""      timeout: NotRequired[float]     """The timeout for the HTTP request. Defaults to 5 seconds."""      sse_read_timeout: NotRequired[float]     """The timeout for the SSE connection, in seconds. Defaults to 5 minutes."""      auth: NotRequired[httpx.Auth | None]     """Optional httpx authentication handler (e.g. ``httpx.BasicAuth``, a custom     ``httpx.Auth`` subclass for OAuth token refresh, etc.).  When provided, it is     passed directly to the underlying ``httpx.AsyncClient`` used by the SSE transport.     """      httpx_client_factory: NotRequired[HttpClientFactory]     """Custom HTTP client factory for configuring httpx.AsyncClient behavior (e.g.     to set custom SSL certificates, proxies, or other transport options).     """ ``` |

#### url `instance-attribute`

```
url: str
```

The URL of the server.

#### headers `instance-attribute`

```
headers: NotRequired[dict[str, str]]
```

The headers to send to the server.

#### timeout `instance-attribute`

```
timeout: NotRequired[float]
```

The timeout for the HTTP request. Defaults to 5 seconds.

#### sse\_read\_timeout `instance-attribute`

```
sse_read_timeout: NotRequired[float]
```

The timeout for the SSE connection, in seconds. Defaults to 5 minutes.

#### auth `instance-attribute`

```
auth: NotRequired[Auth | None]
```

Optional httpx authentication handler (e.g. `httpx.BasicAuth`, a custom
`httpx.Auth` subclass for OAuth token refresh, etc.). When provided, it is
passed directly to the underlying `httpx.AsyncClient` used by the SSE transport.

#### httpx\_client\_factory `instance-attribute`

```
httpx_client_factory: NotRequired[HttpClientFactory]
```

Custom HTTP client factory for configuring httpx.AsyncClient behavior (e.g.
to set custom SSL certificates, proxies, or other transport options).

### MCPServerSse

Bases: `_MCPServerWithClientSession`

MCP server implementation that uses the HTTP with SSE transport. See the [spec]
(https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/#http-with-sse)
for details.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1235 1236 1237 1238 1239 1240 1241 1242 1243 1244 1245 1246 1247 1248 1249 1250 1251 1252 1253 1254 1255 1256 1257 1258 1259 1260 1261 1262 1263 1264 1265 1266 1267 1268 1269 1270 1271 1272 1273 1274 1275 1276 1277 1278 1279 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1315 1316 1317 1318 1319 1320 1321 1322 1323 1324 1325 1326 1327 1328 1329 1330 1331 1332 1333 1334 1335 ``` | ``` class MCPServerSse(_MCPServerWithClientSession):     """MCP server implementation that uses the HTTP with SSE transport. See the [spec]     (https://spec.modelcontextprotocol.io/specification/2024-11-05/basic/transports/#http-with-sse)     for details.     """      def __init__(         self,         params: MCPServerSseParams,         cache_tools_list: bool = False,         name: str | None = None,         client_session_timeout_seconds: float | None = 5,         tool_filter: ToolFilter = None,         use_structured_content: bool = False,         max_retry_attempts: int = 0,         retry_backoff_seconds_base: float = 1.0,         message_handler: MessageHandlerFnT | None = None,         require_approval: RequireApprovalSetting = None,         failure_error_function: ToolErrorFunction | None | _UnsetType = _UNSET,         tool_meta_resolver: MCPToolMetaResolver | None = None,         custom_data_extractor: MCPToolCustomDataExtractor | None = None,     ):         """Create a new MCP server based on the HTTP with SSE transport.          Args:             params: The params that configure the server. This includes the URL of the server,                 the headers to send to the server, the timeout for the HTTP request, and the                 timeout for the SSE connection.              cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be                 cached and only fetched from the server once. If `False`, the tools list will be                 fetched from the server on each call to `list_tools()`. The cache can be                 invalidated by calling `invalidate_tools_cache()`. You should set this to `True`                 if you know the server will not change its tools list, because it can drastically                 improve latency (by avoiding a round-trip to the server every time).              name: A readable name for the server. If not provided, we'll create one from the                 URL.              client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.             tool_filter: The tool filter to use for filtering tools.             use_structured_content: Whether to use `tool_result.structured_content` when calling an                 MCP tool. Defaults to False for backwards compatibility - most MCP servers still                 include the structured content in the `tool_result.content`, and using it by                 default will cause duplicate content. You can set this to True if you know the                 server will not duplicate the structured content in the `tool_result.content`.             max_retry_attempts: Number of times to retry failed list_tools/call_tool calls.                 Defaults to no retries.             retry_backoff_seconds_base: The base delay, in seconds, for exponential                 backoff between retries.             message_handler: Optional handler invoked for session messages as delivered by the                 ClientSession.             require_approval: Approval policy for tools on this server. Accepts "always"/"never",                 a dict of tool names to those values, or an object with always/never tool lists.             failure_error_function: Optional function used to convert MCP tool failures into                 a model-visible error message. If explicitly set to None, tool errors will be                 raised instead of converted. If left unset, the agent-level configuration (or                 SDK default) will be used.             tool_meta_resolver: Optional callable that produces MCP request metadata (`_meta`) for                 tool calls. It is invoked by the Agents SDK before calling `call_tool`.             custom_data_extractor: Optional callable that produces SDK-only custom data for                 emitted MCP tool output items.         """         super().__init__(             cache_tools_list=cache_tools_list,             client_session_timeout_seconds=client_session_timeout_seconds,             tool_filter=tool_filter,             use_structured_content=use_structured_content,             max_retry_attempts=max_retry_attempts,             retry_backoff_seconds_base=retry_backoff_seconds_base,             message_handler=message_handler,             require_approval=require_approval,             failure_error_function=failure_error_function,             tool_meta_resolver=tool_meta_resolver,             custom_data_extractor=custom_data_extractor,         )          self.params = params         self._name = name or f"sse: {self.params['url']}"      def create_streams(         self,     ) -> AbstractAsyncContextManager[MCPStreamTransport]:         """Create the streams for the server."""         kwargs: dict[str, Any] = {             "url": self.params["url"],             "headers": self.params.get("headers", None),             "timeout": self.params.get("timeout", 5),             "sse_read_timeout": self.params.get("sse_read_timeout", 60 * 5),         }         if "auth" in self.params:             kwargs["auth"] = self.params["auth"]         kwargs["httpx_client_factory"] = (             self.params.get("httpx_client_factory") or _create_default_streamable_http_client         )         return sse_client(**kwargs)      @property     def name(self) -> str:         """A readable name for the server."""         return self._name ``` |

#### name `property`

```
name: str
```

A readable name for the server.

#### \_\_init\_\_

```
__init__(
    params: MCPServerSseParams,
    cache_tools_list: bool = False,
    name: str | None = None,
    client_session_timeout_seconds: float | None = 5,
    tool_filter: ToolFilter = None,
    use_structured_content: bool = False,
    max_retry_attempts: int = 0,
    retry_backoff_seconds_base: float = 1.0,
    message_handler: MessageHandlerFnT | None = None,
    require_approval: RequireApprovalSetting = None,
    failure_error_function: ToolErrorFunction
    | None
    | _UnsetType = _UNSET,
    tool_meta_resolver: MCPToolMetaResolver | None = None,
    custom_data_extractor: MCPToolCustomDataExtractor
    | None = None,
)
```

Create a new MCP server based on the HTTP with SSE transport.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `params` | `MCPServerSseParams` | The params that configure the server. This includes the URL of the server, the headers to send to the server, the timeout for the HTTP request, and the timeout for the SSE connection. | *required* |
| `cache_tools_list` | `bool` | Whether to cache the tools list. If `True`, the tools list will be cached and only fetched from the server once. If `False`, the tools list will be fetched from the server on each call to `list_tools()`. The cache can be invalidated by calling `invalidate_tools_cache()`. You should set this to `True` if you know the server will not change its tools list, because it can drastically improve latency (by avoiding a round-trip to the server every time). | `False` |
| `name` | `str | None` | A readable name for the server. If not provided, we'll create one from the URL. | `None` |
| `client_session_timeout_seconds` | `float | None` | the read timeout passed to the MCP ClientSession. | `5` |
| `tool_filter` | `ToolFilter` | The tool filter to use for filtering tools. | `None` |
| `use_structured_content` | `bool` | Whether to use `tool_result.structured_content` when calling an MCP tool. Defaults to False for backwards compatibility - most MCP servers still include the structured content in the `tool_result.content`, and using it by default will cause duplicate content. You can set this to True if you know the server will not duplicate the structured content in the `tool_result.content`. | `False` |
| `max_retry_attempts` | `int` | Number of times to retry failed list\_tools/call\_tool calls. Defaults to no retries. | `0` |
| `retry_backoff_seconds_base` | `float` | The base delay, in seconds, for exponential backoff between retries. | `1.0` |
| `message_handler` | `MessageHandlerFnT | None` | Optional handler invoked for session messages as delivered by the ClientSession. | `None` |
| `require_approval` | `RequireApprovalSetting` | Approval policy for tools on this server. Accepts "always"/"never", a dict of tool names to those values, or an object with always/never tool lists. | `None` |
| `failure_error_function` | `ToolErrorFunction | None | _UnsetType` | Optional function used to convert MCP tool failures into a model-visible error message. If explicitly set to None, tool errors will be raised instead of converted. If left unset, the agent-level configuration (or SDK default) will be used. | `_UNSET` |
| `tool_meta_resolver` | `MCPToolMetaResolver | None` | Optional callable that produces MCP request metadata (`_meta`) for tool calls. It is invoked by the Agents SDK before calling `call_tool`. | `None` |
| `custom_data_extractor` | `MCPToolCustomDataExtractor | None` | Optional callable that produces SDK-only custom data for emitted MCP tool output items. | `None` |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1241 1242 1243 1244 1245 1246 1247 1248 1249 1250 1251 1252 1253 1254 1255 1256 1257 1258 1259 1260 1261 1262 1263 1264 1265 1266 1267 1268 1269 1270 1271 1272 1273 1274 1275 1276 1277 1278 1279 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 ``` | ``` def __init__(     self,     params: MCPServerSseParams,     cache_tools_list: bool = False,     name: str | None = None,     client_session_timeout_seconds: float | None = 5,     tool_filter: ToolFilter = None,     use_structured_content: bool = False,     max_retry_attempts: int = 0,     retry_backoff_seconds_base: float = 1.0,     message_handler: MessageHandlerFnT | None = None,     require_approval: RequireApprovalSetting = None,     failure_error_function: ToolErrorFunction | None | _UnsetType = _UNSET,     tool_meta_resolver: MCPToolMetaResolver | None = None,     custom_data_extractor: MCPToolCustomDataExtractor | None = None, ):     """Create a new MCP server based on the HTTP with SSE transport.      Args:         params: The params that configure the server. This includes the URL of the server,             the headers to send to the server, the timeout for the HTTP request, and the             timeout for the SSE connection.          cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be             cached and only fetched from the server once. If `False`, the tools list will be             fetched from the server on each call to `list_tools()`. The cache can be             invalidated by calling `invalidate_tools_cache()`. You should set this to `True`             if you know the server will not change its tools list, because it can drastically             improve latency (by avoiding a round-trip to the server every time).          name: A readable name for the server. If not provided, we'll create one from the             URL.          client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.         tool_filter: The tool filter to use for filtering tools.         use_structured_content: Whether to use `tool_result.structured_content` when calling an             MCP tool. Defaults to False for backwards compatibility - most MCP servers still             include the structured content in the `tool_result.content`, and using it by             default will cause duplicate content. You can set this to True if you know the             server will not duplicate the structured content in the `tool_result.content`.         max_retry_attempts: Number of times to retry failed list_tools/call_tool calls.             Defaults to no retries.         retry_backoff_seconds_base: The base delay, in seconds, for exponential             backoff between retries.         message_handler: Optional handler invoked for session messages as delivered by the             ClientSession.         require_approval: Approval policy for tools on this server. Accepts "always"/"never",             a dict of tool names to those values, or an object with always/never tool lists.         failure_error_function: Optional function used to convert MCP tool failures into             a model-visible error message. If explicitly set to None, tool errors will be             raised instead of converted. If left unset, the agent-level configuration (or             SDK default) will be used.         tool_meta_resolver: Optional callable that produces MCP request metadata (`_meta`) for             tool calls. It is invoked by the Agents SDK before calling `call_tool`.         custom_data_extractor: Optional callable that produces SDK-only custom data for             emitted MCP tool output items.     """     super().__init__(         cache_tools_list=cache_tools_list,         client_session_timeout_seconds=client_session_timeout_seconds,         tool_filter=tool_filter,         use_structured_content=use_structured_content,         max_retry_attempts=max_retry_attempts,         retry_backoff_seconds_base=retry_backoff_seconds_base,         message_handler=message_handler,         require_approval=require_approval,         failure_error_function=failure_error_function,         tool_meta_resolver=tool_meta_resolver,         custom_data_extractor=custom_data_extractor,     )      self.params = params     self._name = name or f"sse: {self.params['url']}" ``` |

#### create\_streams

```
create_streams() -> AbstractAsyncContextManager[
    MCPStreamTransport
]
```

Create the streams for the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1315 1316 1317 1318 1319 1320 1321 1322 1323 1324 1325 1326 1327 1328 1329 1330 ``` | ``` def create_streams(     self, ) -> AbstractAsyncContextManager[MCPStreamTransport]:     """Create the streams for the server."""     kwargs: dict[str, Any] = {         "url": self.params["url"],         "headers": self.params.get("headers", None),         "timeout": self.params.get("timeout", 5),         "sse_read_timeout": self.params.get("sse_read_timeout", 60 * 5),     }     if "auth" in self.params:         kwargs["auth"] = self.params["auth"]     kwargs["httpx_client_factory"] = (         self.params.get("httpx_client_factory") or _create_default_streamable_http_client     )     return sse_client(**kwargs) ``` |

#### connect `async`

```
connect()
```

Connect to the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 ``` | ``` async def connect(self):     """Connect to the server."""     connection_succeeded = False     try:         transport = await self.exit_stack.enter_async_context(self.create_streams())         # streamablehttp_client returns (read, write, get_session_id)         # sse_client returns (read, write)          read, write, *rest = transport         # Capture the session-id callback when present (streamablehttp_client only).         self._get_session_id = rest[0] if rest and callable(rest[0]) else None          session = await self.exit_stack.enter_async_context(             ClientSession(                 read,                 write,                 timedelta(seconds=self.client_session_timeout_seconds)                 if self.client_session_timeout_seconds                 else None,                 message_handler=self.message_handler,             )         )         server_result = await session.initialize()         self.server_initialize_result = server_result         self.session = session         connection_succeeded = True     except Exception as e:         # Try to extract HTTP error from exception or ExceptionGroup         http_error = self._extract_http_error_from_exception(e)         if http_error:             self._raise_user_error_for_http_error(http_error)          # For CancelledError, preserve cancellation semantics - don't wrap it.         # If it's masking an HTTP error, cleanup() will extract and raise UserError.         if isinstance(e, asyncio.CancelledError):             raise          # For HTTP-related errors, wrap them         if isinstance(e, httpx.HTTPStatusError | httpx.ConnectError | httpx.TimeoutException):             self._raise_user_error_for_http_error(e)          # For other errors, re-raise as-is (don't wrap non-HTTP errors)         raise     finally:         # Always attempt cleanup on error, but suppress cleanup errors that mask the original         if not connection_succeeded:             try:                 await self.cleanup()             except UserError:                 # Re-raise UserError from cleanup (contains the real HTTP error)                 raise             except Exception as cleanup_error:                 # Suppress RuntimeError about cancel scopes during cleanup - this is a known                 # issue with the MCP library's async generator cleanup and shouldn't mask the                 # original error                 if isinstance(cleanup_error, RuntimeError) and "cancel scope" in str(                     cleanup_error                 ):                     logger.debug(                         "Ignoring cancel scope error during cleanup of MCP server '%s': %s",                         self.name,                         cleanup_error,                     )                 else:                     # Log other cleanup errors but don't raise - original error is more                     # important                     logger.warning(                         "Error during cleanup of MCP server '%s': %s", self.name, cleanup_error                     ) ``` |

#### cleanup `async`

```
cleanup()
```

Cleanup the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 ``` | ``` async def cleanup(self):     """Cleanup the server."""     async with self._cleanup_lock:         # Only raise HTTP errors if we're cleaning up after a failed connection.         # During normal teardown (via __aexit__), log but don't raise to avoid         # masking the original exception.         is_failed_connection_cleanup = self.session is None          try:             await self.exit_stack.aclose()         except asyncio.CancelledError as e:             logger.debug("Cleanup cancelled for MCP server '%s': %s", self.name, e)             raise         except BaseExceptionGroup as eg:             # Extract HTTP errors from ExceptionGroup raised during cleanup             # This happens when background tasks fail (e.g., HTTP errors)             http_error = None             connect_error = None             timeout_error = None             error_message = f"Failed to connect to MCP server '{self.name}': "              for exc in eg.exceptions:                 if isinstance(exc, httpx.HTTPStatusError):                     http_error = exc                 elif isinstance(exc, httpx.ConnectError):                     connect_error = exc                 elif isinstance(exc, httpx.TimeoutException):                     timeout_error = exc              # Only raise HTTP errors if we're cleaning up after a failed connection.             # During normal teardown, log them instead.             if http_error:                 if is_failed_connection_cleanup:                     error_message += f"HTTP error {http_error.response.status_code} ({http_error.response.reason_phrase})"  # noqa: E501                     raise UserError(error_message) from http_error                 else:                     # Normal teardown - log but don't raise                     logger.warning(                         "HTTP error during cleanup of MCP server '%s': %s",                         self.name,                         http_error,                     )             elif connect_error:                 if is_failed_connection_cleanup:                     error_message += "Could not reach the server."                     raise UserError(error_message) from connect_error                 else:                     logger.warning(                         "Connection error during cleanup of MCP server '%s': %s",                         self.name,                         connect_error,                     )             elif timeout_error:                 if is_failed_connection_cleanup:                     error_message += "Connection timeout."                     raise UserError(error_message) from timeout_error                 else:                     logger.warning(                         "Timeout error during cleanup of MCP server '%s': %s",                         self.name,                         timeout_error,                     )             else:                 # No HTTP error found, suppress RuntimeError about cancel scopes                 has_cancel_scope_error = any(                     isinstance(exc, RuntimeError) and "cancel scope" in str(exc)                     for exc in eg.exceptions                 )                 if has_cancel_scope_error:                     logger.debug("Ignoring cancel scope error during cleanup: %s", eg)                 else:                     logger.error("Error cleaning up server: %s", eg)         except Exception as e:             # Suppress RuntimeError about cancel scopes - this is a known issue with the MCP             # library when background tasks fail during async generator cleanup             if isinstance(e, RuntimeError) and "cancel scope" in str(e):                 logger.debug("Ignoring cancel scope error during cleanup: %s", e)             else:                 logger.error("Error cleaning up server: %s", e)         finally:             self.session = None             self._get_session_id = None ``` |

#### list\_tools `async`

```
list_tools(
    run_context: RunContextWrapper[Any] | None = None,
    agent: AgentBase | None = None,
) -> list[Tool]
```

List the tools available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 833 834 835 836 837 838 839 840 841 842 843 844 845 846 847 848 849 850 851 852 853 854 855 856 857 858 859 860 861 862 863 864 865 866 867 868 869 870 871 ``` | ``` async def list_tools(     self,     run_context: RunContextWrapper[Any] | None = None,     agent: AgentBase | None = None, ) -> list[MCPTool]:     """List the tools available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None      try:         # Return from cache if caching is enabled, we have tools, and the cache is not dirty         if self.cache_tools_list and not self._cache_dirty and self._tools_list:             tools = self._tools_list         else:             # Fetch the tools from the server             result = await self._run_with_retries(                 lambda: self._maybe_serialize_request(lambda: session.list_tools())             )             self._tools_list = result.tools             self._cache_dirty = False             tools = self._tools_list          # Filter tools based on tool_filter         filtered_tools = tools         if self.tool_filter is not None:             filtered_tools = await self._apply_tool_filter(filtered_tools, run_context, agent)         return filtered_tools     except httpx.HTTPStatusError as e:         status_code = e.response.status_code         raise UserError(             f"Failed to list tools from MCP server '{self.name}': HTTP error {status_code}"         ) from e     except httpx.ConnectError as e:         raise UserError(             f"Failed to list tools from MCP server '{self.name}': Connection lost. "             f"The server may have disconnected."         ) from e ``` |

#### call\_tool `async`

```
call_tool(
    tool_name: str,
    arguments: dict[str, Any] | None,
    meta: dict[str, Any] | None = None,
) -> CallToolResult
```

Invoke a tool on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 900 901 902 903 904 905 906 907 908 ``` | ``` async def call_tool(     self,     tool_name: str,     arguments: dict[str, Any] | None,     meta: dict[str, Any] | None = None, ) -> CallToolResult:     """Invoke a tool on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None      try:         self._validate_required_parameters(tool_name=tool_name, arguments=arguments)         if meta is None:             return await self._run_with_retries(                 lambda: self._maybe_serialize_request(                     lambda: session.call_tool(tool_name, arguments)                 )             )         return await self._run_with_retries(             lambda: self._maybe_serialize_request(                 lambda: session.call_tool(tool_name, arguments, meta=meta)             )         )     except httpx.HTTPStatusError as e:         status_code = e.response.status_code         raise UserError(             f"Failed to call tool '{tool_name}' on MCP server '{self.name}': "             f"HTTP error {status_code}"         ) from e     except httpx.ConnectError as e:         raise UserError(             f"Failed to call tool '{tool_name}' on MCP server '{self.name}': Connection lost. "             f"The server may have disconnected."         ) from e ``` |

#### list\_prompts `async`

```
list_prompts() -> ListPromptsResult
```

List the prompts available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 944 945 946 947 948 949 950 951 952 ``` | ``` async def list_prompts(     self, ) -> ListPromptsResult:     """List the prompts available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_prompts()) ``` |

#### get\_prompt `async`

```
get_prompt(
    name: str, arguments: dict[str, Any] | None = None
) -> GetPromptResult
```

Get a specific prompt from the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 954 955 956 957 958 959 960 961 962 ``` | ``` async def get_prompt(     self, name: str, arguments: dict[str, Any] | None = None ) -> GetPromptResult:     """Get a specific prompt from the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.get_prompt(name, arguments)) ``` |

#### list\_resources `async`

```
list_resources(
    cursor: str | None = None,
) -> ListResourcesResult
```

List the resources available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 964 965 966 967 968 969 970 ``` | ``` async def list_resources(self, cursor: str | None = None) -> ListResourcesResult:     """List the resources available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_resources(cursor)) ``` |

#### list\_resource\_templates `async`

```
list_resource_templates(
    cursor: str | None = None,
) -> ListResourceTemplatesResult
```

List the resource templates available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 972 973 974 975 976 977 978 979 980 ``` | ``` async def list_resource_templates(     self, cursor: str | None = None ) -> ListResourceTemplatesResult:     """List the resource templates available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_resource_templates(cursor)) ``` |

#### read\_resource `async`

```
read_resource(uri: str) -> ReadResourceResult
```

Read the contents of a specific resource by URI.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `str` | The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl` for the supported URI formats. | *required* |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 982 983 984 985 986 987 988 989 990 991 992 993 994 995 ``` | ``` async def read_resource(self, uri: str) -> ReadResourceResult:     """Read the contents of a specific resource by URI.      Args:         uri: The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl`             for the supported URI formats.     """     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     from pydantic import AnyUrl      return await self._maybe_serialize_request(lambda: session.read_resource(AnyUrl(uri))) ``` |

#### invalidate\_tools\_cache

```
invalidate_tools_cache()
```

Invalidate the tools cache.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 719 720 721 ``` | ``` def invalidate_tools_cache(self):     """Invalidate the tools cache."""     self._cache_dirty = True ``` |

### MCPServerStreamableHttpParams

Bases: `TypedDict`

Mirrors the params in `mcp.client.streamable_http.streamablehttp_client`.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1338 1339 1340 1341 1342 1343 1344 1345 1346 1347 1348 1349 1350 1351 1352 1353 1354 1355 1356 1357 1358 1359 1360 1361 1362 1363 1364 1365 1366 1367 1368 1369 1370 1371 1372 ``` | ``` class MCPServerStreamableHttpParams(TypedDict):     """Mirrors the params in `mcp.client.streamable_http.streamablehttp_client`."""      url: str     """The URL of the server."""      headers: NotRequired[dict[str, str]]     """The headers to send to the server."""      timeout: NotRequired[timedelta | float]     """The timeout for the HTTP request. Defaults to 5 seconds."""      sse_read_timeout: NotRequired[timedelta | float]     """The timeout for the SSE connection, in seconds. Defaults to 5 minutes."""      terminate_on_close: NotRequired[bool]     """Terminate on close"""      httpx_client_factory: NotRequired[HttpClientFactory]     """Custom HTTP client factory for configuring httpx.AsyncClient behavior."""      auth: NotRequired[httpx.Auth | None]     """Optional httpx authentication handler (e.g. ``httpx.BasicAuth``, a custom     ``httpx.Auth`` subclass for OAuth token refresh, etc.).  When provided, it is     passed directly to the underlying ``httpx.AsyncClient`` used by the Streamable HTTP     transport.     """      ignore_initialized_notification_failure: NotRequired[bool]     """Whether to ignore failures when sending the best-effort     ``notifications/initialized`` POST.      Defaults to ``False``. When set to ``True``, initialized-notification failures are     logged and ignored so subsequent requests on the same transport can continue.     """ ``` |

#### url `instance-attribute`

```
url: str
```

The URL of the server.

#### headers `instance-attribute`

```
headers: NotRequired[dict[str, str]]
```

The headers to send to the server.

#### timeout `instance-attribute`

```
timeout: NotRequired[timedelta | float]
```

The timeout for the HTTP request. Defaults to 5 seconds.

#### sse\_read\_timeout `instance-attribute`

```
sse_read_timeout: NotRequired[timedelta | float]
```

The timeout for the SSE connection, in seconds. Defaults to 5 minutes.

#### terminate\_on\_close `instance-attribute`

```
terminate_on_close: NotRequired[bool]
```

Terminate on close

#### httpx\_client\_factory `instance-attribute`

```
httpx_client_factory: NotRequired[HttpClientFactory]
```

Custom HTTP client factory for configuring httpx.AsyncClient behavior.

#### auth `instance-attribute`

```
auth: NotRequired[Auth | None]
```

Optional httpx authentication handler (e.g. `httpx.BasicAuth`, a custom
`httpx.Auth` subclass for OAuth token refresh, etc.). When provided, it is
passed directly to the underlying `httpx.AsyncClient` used by the Streamable HTTP
transport.

#### ignore\_initialized\_notification\_failure `instance-attribute`

```
ignore_initialized_notification_failure: NotRequired[bool]
```

Whether to ignore failures when sending the best-effort
`notifications/initialized` POST.

Defaults to `False`. When set to `True`, initialized-notification failures are
logged and ignored so subsequent requests on the same transport can continue.

### MCPServerStreamableHttp

Bases: `_MCPServerWithClientSession`

MCP server implementation that uses the Streamable HTTP transport. See the [spec]
(https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)
for details.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1375 1376 1377 1378 1379 1380 1381 1382 1383 1384 1385 1386 1387 1388 1389 1390 1391 1392 1393 1394 1395 1396 1397 1398 1399 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1415 1416 1417 1418 1419 1420 1421 1422 1423 1424 1425 1426 1427 1428 1429 1430 1431 1432 1433 1434 1435 1436 1437 1438 1439 1440 1441 1442 1443 1444 1445 1446 1447 1448 1449 1450 1451 1452 1453 1454 1455 1456 1457 1458 1459 1460 1461 1462 1463 1464 1465 1466 1467 1468 1469 1470 1471 1472 1473 1474 1475 1476 1477 1478 1479 1480 1481 1482 1483 1484 1485 1486 1487 1488 1489 1490 1491 1492 1493 1494 1495 1496 1497 1498 1499 1500 1501 1502 1503 1504 1505 1506 1507 1508 1509 1510 1511 1512 1513 1514 1515 1516 1517 1518 1519 1520 1521 1522 1523 1524 1525 1526 1527 1528 1529 1530 1531 1532 1533 1534 1535 1536 1537 1538 1539 1540 1541 1542 1543 1544 1545 1546 1547 1548 1549 1550 1551 1552 1553 1554 1555 1556 1557 1558 1559 1560 1561 1562 1563 1564 1565 1566 1567 1568 1569 1570 1571 1572 1573 1574 1575 1576 1577 1578 1579 1580 1581 1582 1583 1584 1585 1586 1587 1588 1589 1590 1591 1592 1593 1594 1595 1596 1597 1598 1599 1600 1601 1602 1603 1604 1605 1606 1607 1608 1609 1610 1611 1612 1613 1614 1615 1616 1617 1618 1619 1620 1621 1622 1623 1624 1625 1626 1627 1628 1629 1630 1631 1632 1633 1634 1635 1636 1637 1638 1639 1640 1641 1642 1643 1644 1645 1646 1647 1648 1649 1650 1651 1652 1653 1654 1655 1656 1657 1658 1659 1660 1661 1662 1663 1664 1665 1666 1667 1668 1669 1670 1671 1672 1673 1674 1675 1676 1677 1678 1679 1680 1681 1682 1683 1684 1685 1686 1687 1688 1689 1690 1691 1692 1693 1694 1695 1696 1697 1698 1699 1700 ``` | ``` class MCPServerStreamableHttp(_MCPServerWithClientSession):     """MCP server implementation that uses the Streamable HTTP transport. See the [spec]     (https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)     for details.     """      def __init__(         self,         params: MCPServerStreamableHttpParams,         cache_tools_list: bool = False,         name: str | None = None,         client_session_timeout_seconds: float | None = 5,         tool_filter: ToolFilter = None,         use_structured_content: bool = False,         max_retry_attempts: int = 0,         retry_backoff_seconds_base: float = 1.0,         message_handler: MessageHandlerFnT | None = None,         require_approval: RequireApprovalSetting = None,         failure_error_function: ToolErrorFunction | None | _UnsetType = _UNSET,         tool_meta_resolver: MCPToolMetaResolver | None = None,         custom_data_extractor: MCPToolCustomDataExtractor | None = None,     ):         """Create a new MCP server based on the Streamable HTTP transport.          Args:             params: The params that configure the server. This includes the URL of the server,                 the headers to send to the server, the timeout for the HTTP request, the                 timeout for the Streamable HTTP connection, whether we need to                 terminate on close, and an optional custom HTTP client factory.              cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be                 cached and only fetched from the server once. If `False`, the tools list will be                 fetched from the server on each call to `list_tools()`. The cache can be                 invalidated by calling `invalidate_tools_cache()`. You should set this to `True`                 if you know the server will not change its tools list, because it can drastically                 improve latency (by avoiding a round-trip to the server every time).              name: A readable name for the server. If not provided, we'll create one from the                 URL.              client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.             tool_filter: The tool filter to use for filtering tools.             use_structured_content: Whether to use `tool_result.structured_content` when calling an                 MCP tool. Defaults to False for backwards compatibility - most MCP servers still                 include the structured content in the `tool_result.content`, and using it by                 default will cause duplicate content. You can set this to True if you know the                 server will not duplicate the structured content in the `tool_result.content`.             max_retry_attempts: Number of times to retry failed list_tools/call_tool calls.                 Defaults to no retries.             retry_backoff_seconds_base: The base delay, in seconds, for exponential                 backoff between retries.             message_handler: Optional handler invoked for session messages as delivered by the                 ClientSession.             require_approval: Approval policy for tools on this server. Accepts "always"/"never",                 a dict of tool names to those values, or an object with always/never tool lists.             failure_error_function: Optional function used to convert MCP tool failures into                 a model-visible error message. If explicitly set to None, tool errors will be                 raised instead of converted. If left unset, the agent-level configuration (or                 SDK default) will be used.             tool_meta_resolver: Optional callable that produces MCP request metadata (`_meta`) for                 tool calls. It is invoked by the Agents SDK before calling `call_tool`.             custom_data_extractor: Optional callable that produces SDK-only custom data for                 emitted MCP tool output items.         """         super().__init__(             cache_tools_list=cache_tools_list,             client_session_timeout_seconds=client_session_timeout_seconds,             tool_filter=tool_filter,             use_structured_content=use_structured_content,             max_retry_attempts=max_retry_attempts,             retry_backoff_seconds_base=retry_backoff_seconds_base,             message_handler=message_handler,             require_approval=require_approval,             failure_error_function=failure_error_function,             tool_meta_resolver=tool_meta_resolver,             custom_data_extractor=custom_data_extractor,         )          self.params = params         self._name = name or f"streamable_http: {self.params['url']}"         self._serialize_session_requests = True      def create_streams(         self,     ) -> AbstractAsyncContextManager[MCPStreamTransport]:         """Create the streams for the server."""         kwargs: dict[str, Any] = {             "url": self.params["url"],             "headers": self.params.get("headers", None),             "timeout": self.params.get("timeout", 5),             "sse_read_timeout": self.params.get("sse_read_timeout", 60 * 5),             "terminate_on_close": self.params.get("terminate_on_close", True),         }         httpx_client_factory = self.params.get("httpx_client_factory")         if self.params.get("ignore_initialized_notification_failure", False):             return _streamablehttp_client_with_transport(                 **kwargs,                 httpx_client_factory=httpx_client_factory or _create_default_streamable_http_client,                 auth=self.params.get("auth"),                 transport_factory=_InitializedNotificationTolerantStreamableHTTPTransport,             )         kwargs["httpx_client_factory"] = (             httpx_client_factory or _create_default_streamable_http_client         )         if "auth" in self.params:             kwargs["auth"] = self.params["auth"]         return streamablehttp_client(**kwargs)      @asynccontextmanager     async def _isolated_client_session(self):         async with AsyncExitStack() as exit_stack:             transport = await exit_stack.enter_async_context(self.create_streams())             read, write, *_ = transport             session = await exit_stack.enter_async_context(                 ClientSession(                     read,                     write,                     timedelta(seconds=self.client_session_timeout_seconds)                     if self.client_session_timeout_seconds                     else None,                     message_handler=self.message_handler,                 )             )             await session.initialize()             yield session      async def _call_tool_with_session(         self,         session: ClientSession,         tool_name: str,         arguments: dict[str, Any] | None,         meta: dict[str, Any] | None = None,     ) -> CallToolResult:         if meta is None:             return await session.call_tool(tool_name, arguments)         return await session.call_tool(tool_name, arguments, meta=meta)      def _should_retry_in_isolated_session(self, exc: BaseException) -> bool:         if isinstance(             exc,             asyncio.CancelledError             | ClosedResourceError             | httpx.ConnectError             | httpx.TimeoutException,         ):             return True         if isinstance(exc, httpx.HTTPStatusError):             return exc.response.status_code >= 500         if isinstance(exc, McpError):             return exc.error.code == httpx.codes.REQUEST_TIMEOUT         if isinstance(exc, BaseExceptionGroup):             return bool(exc.exceptions) and all(                 self._should_retry_in_isolated_session(inner) for inner in exc.exceptions             )         return False      async def _call_tool_with_shared_session(         self,         tool_name: str,         arguments: dict[str, Any] | None,         meta: dict[str, Any] | None = None,         *,         allow_isolated_retry: bool,     ) -> CallToolResult:         session = self.session         assert session is not None         try:             return await self._maybe_serialize_request(                 lambda: self._call_tool_with_session(session, tool_name, arguments, meta)             )         except BaseException as exc:             if allow_isolated_retry and self._should_retry_in_isolated_session(exc):                 raise _SharedSessionRequestNeedsIsolation from exc             raise      async def _call_tool_with_isolated_retry(         self,         tool_name: str,         arguments: dict[str, Any] | None,         meta: dict[str, Any] | None = None,         *,         allow_isolated_retry: bool,     ) -> tuple[CallToolResult, bool]:         request_task = asyncio.create_task(             self._call_tool_with_shared_session(                 tool_name,                 arguments,                 meta,                 allow_isolated_retry=allow_isolated_retry,             )         )         try:             return await asyncio.shield(request_task), False         except _SharedSessionRequestNeedsIsolation:             exit_stack = AsyncExitStack()             try:                 session = await exit_stack.enter_async_context(self._isolated_client_session())             except asyncio.CancelledError:                 await exit_stack.aclose()                 raise             except BaseException as exc:                 await exit_stack.aclose()                 raise _IsolatedSessionRetryFailed() from exc             try:                 try:                     result = await self._call_tool_with_session(session, tool_name, arguments, meta)                     return result, True                 except asyncio.CancelledError:                     raise                 except BaseException as exc:                     raise _IsolatedSessionRetryFailed() from exc             finally:                 await exit_stack.aclose()         except asyncio.CancelledError:             if not request_task.done():                 request_task.cancel()             try:                 await request_task             except BaseException:                 pass             raise      async def call_tool(         self,         tool_name: str,         arguments: dict[str, Any] | None,         meta: dict[str, Any] | None = None,     ) -> CallToolResult:         if not self.session:             raise UserError("Server not initialized. Make sure you call `connect()` first.")          try:             self._validate_required_parameters(tool_name=tool_name, arguments=arguments)             retries_used = 0             first_attempt = True             while True:                 if not first_attempt and self.max_retry_attempts != -1:                     retries_used += 1                 allow_isolated_retry = (                     self.max_retry_attempts == -1 or retries_used < self.max_retry_attempts                 )                 try:                     result, used_isolated_retry = await self._call_tool_with_isolated_retry(                         tool_name,                         arguments,                         meta,                         allow_isolated_retry=allow_isolated_retry,                     )                     if used_isolated_retry and self.max_retry_attempts != -1:                         retries_used += 1                     return result                 except _IsolatedSessionRetryFailed as exc:                     retries_used += 1                     if self.max_retry_attempts != -1 and retries_used >= self.max_retry_attempts:                         if exc.__cause__ is not None:                             raise exc.__cause__ from exc                         raise exc                     backoff = self.retry_backoff_seconds_base * (2 ** (retries_used - 1))                     await asyncio.sleep(backoff)                 except Exception:                     if self.max_retry_attempts != -1 and retries_used >= self.max_retry_attempts:                         raise                     backoff = self.retry_backoff_seconds_base * (2**retries_used)                     await asyncio.sleep(backoff)                 first_attempt = False         except httpx.HTTPStatusError as e:             status_code = e.response.status_code             raise UserError(                 f"Failed to call tool '{tool_name}' on MCP server '{self.name}': "                 f"HTTP error {status_code}"             ) from e         except httpx.ConnectError as e:             raise UserError(                 f"Failed to call tool '{tool_name}' on MCP server '{self.name}': Connection lost. "                 f"The server may have disconnected."             ) from e         except BaseExceptionGroup as e:             http_error = self._extract_http_error_from_exception(e)             if isinstance(http_error, httpx.HTTPStatusError):                 status_code = http_error.response.status_code                 raise UserError(                     f"Failed to call tool '{tool_name}' on MCP server '{self.name}': "                     f"HTTP error {status_code}"                 ) from http_error             if isinstance(http_error, httpx.ConnectError):                 raise UserError(                     f"Failed to call tool '{tool_name}' on MCP server '{self.name}': "                     "Connection lost. The server may have disconnected."                 ) from http_error             if isinstance(http_error, httpx.TimeoutException):                 raise UserError(                     f"Failed to call tool '{tool_name}' on MCP server '{self.name}': "                     "Connection timeout."                 ) from http_error             raise      @property     def name(self) -> str:         """A readable name for the server."""         return self._name      @property     def session_id(self) -> str | None:         """The MCP session ID assigned by the server, or None if not yet connected         or if the server did not issue a session ID.          The session ID is stable for the lifetime of this server instance's connection.         You can persist it and pass it back via the Mcp-Session-Id request header         (params["headers"]) on a new MCPServerStreamableHttp instance to resume         the same server-side session across process restarts or stateless workers.          Example::              async with MCPServerStreamableHttp(params={"url": url}) as server:                 session_id = server.session_id              # In a new worker / process:             async with MCPServerStreamableHttp(                 params={"url": url, "headers": {"Mcp-Session-Id": session_id}}             ) as server:                 # Resumes the same server-side session.                 ...         """         if self._get_session_id is None:             return None         return self._get_session_id() ``` |

#### name `property`

```
name: str
```

A readable name for the server.

#### session\_id `property`

```
session_id: str | None
```

The MCP session ID assigned by the server, or None if not yet connected
or if the server did not issue a session ID.

The session ID is stable for the lifetime of this server instance's connection.
You can persist it and pass it back via the Mcp-Session-Id request header
(params["headers"]) on a new MCPServerStreamableHttp instance to resume
the same server-side session across process restarts or stateless workers.

Example::

```
async with MCPServerStreamableHttp(params={"url": url}) as server:
    session_id = server.session_id

# In a new worker / process:
async with MCPServerStreamableHttp(
    params={"url": url, "headers": {"Mcp-Session-Id": session_id}}
) as server:
    # Resumes the same server-side session.
    ...
```

#### \_\_init\_\_

```
__init__(
    params: MCPServerStreamableHttpParams,
    cache_tools_list: bool = False,
    name: str | None = None,
    client_session_timeout_seconds: float | None = 5,
    tool_filter: ToolFilter = None,
    use_structured_content: bool = False,
    max_retry_attempts: int = 0,
    retry_backoff_seconds_base: float = 1.0,
    message_handler: MessageHandlerFnT | None = None,
    require_approval: RequireApprovalSetting = None,
    failure_error_function: ToolErrorFunction
    | None
    | _UnsetType = _UNSET,
    tool_meta_resolver: MCPToolMetaResolver | None = None,
    custom_data_extractor: MCPToolCustomDataExtractor
    | None = None,
)
```

Create a new MCP server based on the Streamable HTTP transport.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `params` | `MCPServerStreamableHttpParams` | The params that configure the server. This includes the URL of the server, the headers to send to the server, the timeout for the HTTP request, the timeout for the Streamable HTTP connection, whether we need to terminate on close, and an optional custom HTTP client factory. | *required* |
| `cache_tools_list` | `bool` | Whether to cache the tools list. If `True`, the tools list will be cached and only fetched from the server once. If `False`, the tools list will be fetched from the server on each call to `list_tools()`. The cache can be invalidated by calling `invalidate_tools_cache()`. You should set this to `True` if you know the server will not change its tools list, because it can drastically improve latency (by avoiding a round-trip to the server every time). | `False` |
| `name` | `str | None` | A readable name for the server. If not provided, we'll create one from the URL. | `None` |
| `client_session_timeout_seconds` | `float | None` | the read timeout passed to the MCP ClientSession. | `5` |
| `tool_filter` | `ToolFilter` | The tool filter to use for filtering tools. | `None` |
| `use_structured_content` | `bool` | Whether to use `tool_result.structured_content` when calling an MCP tool. Defaults to False for backwards compatibility - most MCP servers still include the structured content in the `tool_result.content`, and using it by default will cause duplicate content. You can set this to True if you know the server will not duplicate the structured content in the `tool_result.content`. | `False` |
| `max_retry_attempts` | `int` | Number of times to retry failed list\_tools/call\_tool calls. Defaults to no retries. | `0` |
| `retry_backoff_seconds_base` | `float` | The base delay, in seconds, for exponential backoff between retries. | `1.0` |
| `message_handler` | `MessageHandlerFnT | None` | Optional handler invoked for session messages as delivered by the ClientSession. | `None` |
| `require_approval` | `RequireApprovalSetting` | Approval policy for tools on this server. Accepts "always"/"never", a dict of tool names to those values, or an object with always/never tool lists. | `None` |
| `failure_error_function` | `ToolErrorFunction | None | _UnsetType` | Optional function used to convert MCP tool failures into a model-visible error message. If explicitly set to None, tool errors will be raised instead of converted. If left unset, the agent-level configuration (or SDK default) will be used. | `_UNSET` |
| `tool_meta_resolver` | `MCPToolMetaResolver | None` | Optional callable that produces MCP request metadata (`_meta`) for tool calls. It is invoked by the Agents SDK before calling `call_tool`. | `None` |
| `custom_data_extractor` | `MCPToolCustomDataExtractor | None` | Optional callable that produces SDK-only custom data for emitted MCP tool output items. | `None` |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1381 1382 1383 1384 1385 1386 1387 1388 1389 1390 1391 1392 1393 1394 1395 1396 1397 1398 1399 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1415 1416 1417 1418 1419 1420 1421 1422 1423 1424 1425 1426 1427 1428 1429 1430 1431 1432 1433 1434 1435 1436 1437 1438 1439 1440 1441 1442 1443 1444 1445 1446 1447 1448 1449 1450 1451 1452 1453 1454 1455 ``` | ``` def __init__(     self,     params: MCPServerStreamableHttpParams,     cache_tools_list: bool = False,     name: str | None = None,     client_session_timeout_seconds: float | None = 5,     tool_filter: ToolFilter = None,     use_structured_content: bool = False,     max_retry_attempts: int = 0,     retry_backoff_seconds_base: float = 1.0,     message_handler: MessageHandlerFnT | None = None,     require_approval: RequireApprovalSetting = None,     failure_error_function: ToolErrorFunction | None | _UnsetType = _UNSET,     tool_meta_resolver: MCPToolMetaResolver | None = None,     custom_data_extractor: MCPToolCustomDataExtractor | None = None, ):     """Create a new MCP server based on the Streamable HTTP transport.      Args:         params: The params that configure the server. This includes the URL of the server,             the headers to send to the server, the timeout for the HTTP request, the             timeout for the Streamable HTTP connection, whether we need to             terminate on close, and an optional custom HTTP client factory.          cache_tools_list: Whether to cache the tools list. If `True`, the tools list will be             cached and only fetched from the server once. If `False`, the tools list will be             fetched from the server on each call to `list_tools()`. The cache can be             invalidated by calling `invalidate_tools_cache()`. You should set this to `True`             if you know the server will not change its tools list, because it can drastically             improve latency (by avoiding a round-trip to the server every time).          name: A readable name for the server. If not provided, we'll create one from the             URL.          client_session_timeout_seconds: the read timeout passed to the MCP ClientSession.         tool_filter: The tool filter to use for filtering tools.         use_structured_content: Whether to use `tool_result.structured_content` when calling an             MCP tool. Defaults to False for backwards compatibility - most MCP servers still             include the structured content in the `tool_result.content`, and using it by             default will cause duplicate content. You can set this to True if you know the             server will not duplicate the structured content in the `tool_result.content`.         max_retry_attempts: Number of times to retry failed list_tools/call_tool calls.             Defaults to no retries.         retry_backoff_seconds_base: The base delay, in seconds, for exponential             backoff between retries.         message_handler: Optional handler invoked for session messages as delivered by the             ClientSession.         require_approval: Approval policy for tools on this server. Accepts "always"/"never",             a dict of tool names to those values, or an object with always/never tool lists.         failure_error_function: Optional function used to convert MCP tool failures into             a model-visible error message. If explicitly set to None, tool errors will be             raised instead of converted. If left unset, the agent-level configuration (or             SDK default) will be used.         tool_meta_resolver: Optional callable that produces MCP request metadata (`_meta`) for             tool calls. It is invoked by the Agents SDK before calling `call_tool`.         custom_data_extractor: Optional callable that produces SDK-only custom data for             emitted MCP tool output items.     """     super().__init__(         cache_tools_list=cache_tools_list,         client_session_timeout_seconds=client_session_timeout_seconds,         tool_filter=tool_filter,         use_structured_content=use_structured_content,         max_retry_attempts=max_retry_attempts,         retry_backoff_seconds_base=retry_backoff_seconds_base,         message_handler=message_handler,         require_approval=require_approval,         failure_error_function=failure_error_function,         tool_meta_resolver=tool_meta_resolver,         custom_data_extractor=custom_data_extractor,     )      self.params = params     self._name = name or f"streamable_http: {self.params['url']}"     self._serialize_session_requests = True ``` |

#### create\_streams

```
create_streams() -> AbstractAsyncContextManager[
    MCPStreamTransport
]
```

Create the streams for the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 1457 1458 1459 1460 1461 1462 1463 1464 1465 1466 1467 1468 1469 1470 1471 1472 1473 1474 1475 1476 1477 1478 1479 1480 1481 ``` | ``` def create_streams(     self, ) -> AbstractAsyncContextManager[MCPStreamTransport]:     """Create the streams for the server."""     kwargs: dict[str, Any] = {         "url": self.params["url"],         "headers": self.params.get("headers", None),         "timeout": self.params.get("timeout", 5),         "sse_read_timeout": self.params.get("sse_read_timeout", 60 * 5),         "terminate_on_close": self.params.get("terminate_on_close", True),     }     httpx_client_factory = self.params.get("httpx_client_factory")     if self.params.get("ignore_initialized_notification_failure", False):         return _streamablehttp_client_with_transport(             **kwargs,             httpx_client_factory=httpx_client_factory or _create_default_streamable_http_client,             auth=self.params.get("auth"),             transport_factory=_InitializedNotificationTolerantStreamableHTTPTransport,         )     kwargs["httpx_client_factory"] = (         httpx_client_factory or _create_default_streamable_http_client     )     if "auth" in self.params:         kwargs["auth"] = self.params["auth"]     return streamablehttp_client(**kwargs) ``` |

#### connect `async`

```
connect()
```

Connect to the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 ``` | ``` async def connect(self):     """Connect to the server."""     connection_succeeded = False     try:         transport = await self.exit_stack.enter_async_context(self.create_streams())         # streamablehttp_client returns (read, write, get_session_id)         # sse_client returns (read, write)          read, write, *rest = transport         # Capture the session-id callback when present (streamablehttp_client only).         self._get_session_id = rest[0] if rest and callable(rest[0]) else None          session = await self.exit_stack.enter_async_context(             ClientSession(                 read,                 write,                 timedelta(seconds=self.client_session_timeout_seconds)                 if self.client_session_timeout_seconds                 else None,                 message_handler=self.message_handler,             )         )         server_result = await session.initialize()         self.server_initialize_result = server_result         self.session = session         connection_succeeded = True     except Exception as e:         # Try to extract HTTP error from exception or ExceptionGroup         http_error = self._extract_http_error_from_exception(e)         if http_error:             self._raise_user_error_for_http_error(http_error)          # For CancelledError, preserve cancellation semantics - don't wrap it.         # If it's masking an HTTP error, cleanup() will extract and raise UserError.         if isinstance(e, asyncio.CancelledError):             raise          # For HTTP-related errors, wrap them         if isinstance(e, httpx.HTTPStatusError | httpx.ConnectError | httpx.TimeoutException):             self._raise_user_error_for_http_error(e)          # For other errors, re-raise as-is (don't wrap non-HTTP errors)         raise     finally:         # Always attempt cleanup on error, but suppress cleanup errors that mask the original         if not connection_succeeded:             try:                 await self.cleanup()             except UserError:                 # Re-raise UserError from cleanup (contains the real HTTP error)                 raise             except Exception as cleanup_error:                 # Suppress RuntimeError about cancel scopes during cleanup - this is a known                 # issue with the MCP library's async generator cleanup and shouldn't mask the                 # original error                 if isinstance(cleanup_error, RuntimeError) and "cancel scope" in str(                     cleanup_error                 ):                     logger.debug(                         "Ignoring cancel scope error during cleanup of MCP server '%s': %s",                         self.name,                         cleanup_error,                     )                 else:                     # Log other cleanup errors but don't raise - original error is more                     # important                     logger.warning(                         "Error during cleanup of MCP server '%s': %s", self.name, cleanup_error                     ) ``` |

#### cleanup `async`

```
cleanup()
```

Cleanup the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ```  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 ``` | ``` async def cleanup(self):     """Cleanup the server."""     async with self._cleanup_lock:         # Only raise HTTP errors if we're cleaning up after a failed connection.         # During normal teardown (via __aexit__), log but don't raise to avoid         # masking the original exception.         is_failed_connection_cleanup = self.session is None          try:             await self.exit_stack.aclose()         except asyncio.CancelledError as e:             logger.debug("Cleanup cancelled for MCP server '%s': %s", self.name, e)             raise         except BaseExceptionGroup as eg:             # Extract HTTP errors from ExceptionGroup raised during cleanup             # This happens when background tasks fail (e.g., HTTP errors)             http_error = None             connect_error = None             timeout_error = None             error_message = f"Failed to connect to MCP server '{self.name}': "              for exc in eg.exceptions:                 if isinstance(exc, httpx.HTTPStatusError):                     http_error = exc                 elif isinstance(exc, httpx.ConnectError):                     connect_error = exc                 elif isinstance(exc, httpx.TimeoutException):                     timeout_error = exc              # Only raise HTTP errors if we're cleaning up after a failed connection.             # During normal teardown, log them instead.             if http_error:                 if is_failed_connection_cleanup:                     error_message += f"HTTP error {http_error.response.status_code} ({http_error.response.reason_phrase})"  # noqa: E501                     raise UserError(error_message) from http_error                 else:                     # Normal teardown - log but don't raise                     logger.warning(                         "HTTP error during cleanup of MCP server '%s': %s",                         self.name,                         http_error,                     )             elif connect_error:                 if is_failed_connection_cleanup:                     error_message += "Could not reach the server."                     raise UserError(error_message) from connect_error                 else:                     logger.warning(                         "Connection error during cleanup of MCP server '%s': %s",                         self.name,                         connect_error,                     )             elif timeout_error:                 if is_failed_connection_cleanup:                     error_message += "Connection timeout."                     raise UserError(error_message) from timeout_error                 else:                     logger.warning(                         "Timeout error during cleanup of MCP server '%s': %s",                         self.name,                         timeout_error,                     )             else:                 # No HTTP error found, suppress RuntimeError about cancel scopes                 has_cancel_scope_error = any(                     isinstance(exc, RuntimeError) and "cancel scope" in str(exc)                     for exc in eg.exceptions                 )                 if has_cancel_scope_error:                     logger.debug("Ignoring cancel scope error during cleanup: %s", eg)                 else:                     logger.error("Error cleaning up server: %s", eg)         except Exception as e:             # Suppress RuntimeError about cancel scopes - this is a known issue with the MCP             # library when background tasks fail during async generator cleanup             if isinstance(e, RuntimeError) and "cancel scope" in str(e):                 logger.debug("Ignoring cancel scope error during cleanup: %s", e)             else:                 logger.error("Error cleaning up server: %s", e)         finally:             self.session = None             self._get_session_id = None ``` |

#### list\_tools `async`

```
list_tools(
    run_context: RunContextWrapper[Any] | None = None,
    agent: AgentBase | None = None,
) -> list[Tool]
```

List the tools available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 833 834 835 836 837 838 839 840 841 842 843 844 845 846 847 848 849 850 851 852 853 854 855 856 857 858 859 860 861 862 863 864 865 866 867 868 869 870 871 ``` | ``` async def list_tools(     self,     run_context: RunContextWrapper[Any] | None = None,     agent: AgentBase | None = None, ) -> list[MCPTool]:     """List the tools available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None      try:         # Return from cache if caching is enabled, we have tools, and the cache is not dirty         if self.cache_tools_list and not self._cache_dirty and self._tools_list:             tools = self._tools_list         else:             # Fetch the tools from the server             result = await self._run_with_retries(                 lambda: self._maybe_serialize_request(lambda: session.list_tools())             )             self._tools_list = result.tools             self._cache_dirty = False             tools = self._tools_list          # Filter tools based on tool_filter         filtered_tools = tools         if self.tool_filter is not None:             filtered_tools = await self._apply_tool_filter(filtered_tools, run_context, agent)         return filtered_tools     except httpx.HTTPStatusError as e:         status_code = e.response.status_code         raise UserError(             f"Failed to list tools from MCP server '{self.name}': HTTP error {status_code}"         ) from e     except httpx.ConnectError as e:         raise UserError(             f"Failed to list tools from MCP server '{self.name}': Connection lost. "             f"The server may have disconnected."         ) from e ``` |

#### list\_prompts `async`

```
list_prompts() -> ListPromptsResult
```

List the prompts available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 944 945 946 947 948 949 950 951 952 ``` | ``` async def list_prompts(     self, ) -> ListPromptsResult:     """List the prompts available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_prompts()) ``` |

#### get\_prompt `async`

```
get_prompt(
    name: str, arguments: dict[str, Any] | None = None
) -> GetPromptResult
```

Get a specific prompt from the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 954 955 956 957 958 959 960 961 962 ``` | ``` async def get_prompt(     self, name: str, arguments: dict[str, Any] | None = None ) -> GetPromptResult:     """Get a specific prompt from the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.get_prompt(name, arguments)) ``` |

#### list\_resources `async`

```
list_resources(
    cursor: str | None = None,
) -> ListResourcesResult
```

List the resources available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 964 965 966 967 968 969 970 ``` | ``` async def list_resources(self, cursor: str | None = None) -> ListResourcesResult:     """List the resources available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_resources(cursor)) ``` |

#### list\_resource\_templates `async`

```
list_resource_templates(
    cursor: str | None = None,
) -> ListResourceTemplatesResult
```

List the resource templates available on the server.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 972 973 974 975 976 977 978 979 980 ``` | ``` async def list_resource_templates(     self, cursor: str | None = None ) -> ListResourceTemplatesResult:     """List the resource templates available on the server."""     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     return await self._maybe_serialize_request(lambda: session.list_resource_templates(cursor)) ``` |

#### read\_resource `async`

```
read_resource(uri: str) -> ReadResourceResult
```

Read the contents of a specific resource by URI.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `uri` | `str` | The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl` for the supported URI formats. | *required* |

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 982 983 984 985 986 987 988 989 990 991 992 993 994 995 ``` | ``` async def read_resource(self, uri: str) -> ReadResourceResult:     """Read the contents of a specific resource by URI.      Args:         uri: The URI of the resource to read. See :class:`~pydantic.networks.AnyUrl`             for the supported URI formats.     """     if not self.session:         raise UserError("Server not initialized. Make sure you call `connect()` first.")     session = self.session     assert session is not None     from pydantic import AnyUrl      return await self._maybe_serialize_request(lambda: session.read_resource(AnyUrl(uri))) ``` |

#### invalidate\_tools\_cache

```
invalidate_tools_cache()
```

Invalidate the tools cache.

Source code in `src/agents/mcp/server.py`

|  |  |
| --- | --- |
| ``` 719 720 721 ``` | ``` def invalidate_tools_cache(self):     """Invalidate the tools cache."""     self._cache_dirty = True ``` |