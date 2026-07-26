---
url: https://openai.github.io/openai-agents-python/ref/mcp/util/
title: `MCP Util`
framework: openai
---

# `MCP Util`

### HttpClientFactory

Bases: `Protocol`

Protocol for HTTP client factory functions.

This interface matches the MCP SDK's McpHttpClientFactory but is defined locally
to avoid accessing internal MCP SDK modules.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 74 75 76 77 78 79 80 81 82 83 84 85 86 ``` | ``` class HttpClientFactory(Protocol):     """Protocol for HTTP client factory functions.      This interface matches the MCP SDK's McpHttpClientFactory but is defined locally     to avoid accessing internal MCP SDK modules.     """      def __call__(         self,         headers: dict[str, str] | None = None,         timeout: httpx.Timeout | None = None,         auth: httpx.Auth | None = None,     ) -> httpx.AsyncClient: ... ``` |

### ToolFilterContext `dataclass`

Context information available to tool filter functions.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ```  89  90  91  92  93  94  95  96  97  98  99 100 ``` | ``` @dataclass class ToolFilterContext:     """Context information available to tool filter functions."""      run_context: RunContextWrapper[Any]     """The current run context."""      agent: AgentBase     """The agent that is requesting the tool list."""      server_name: str     """The name of the MCP server.""" ``` |

#### run\_context `instance-attribute`

```
run_context: RunContextWrapper[Any]
```

The current run context.

#### agent `instance-attribute`

```
agent: AgentBase
```

The agent that is requesting the tool list.

#### server\_name `instance-attribute`

```
server_name: str
```

The name of the MCP server.

### ToolFilterStatic

Bases: `TypedDict`

Static tool filter configuration using allowlists and blocklists.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 118 119 120 121 122 123 124 125 126 127 ``` | ``` class ToolFilterStatic(TypedDict):     """Static tool filter configuration using allowlists and blocklists."""      allowed_tool_names: NotRequired[list[str]]     """Optional list of tool names to allow (whitelist).     If set, only these tools will be available."""      blocked_tool_names: NotRequired[list[str]]     """Optional list of tool names to exclude (blacklist).     If set, these tools will be filtered out.""" ``` |

#### allowed\_tool\_names `instance-attribute`

```
allowed_tool_names: NotRequired[list[str]]
```

Optional list of tool names to allow (whitelist).
If set, only these tools will be available.

#### blocked\_tool\_names `instance-attribute`

```
blocked_tool_names: NotRequired[list[str]]
```

Optional list of tool names to exclude (blacklist).
If set, these tools will be filtered out.

### MCPToolMetaContext `dataclass`

Context information available to MCP tool meta resolver functions.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 ``` | ``` @dataclass class MCPToolMetaContext:     """Context information available to MCP tool meta resolver functions."""      run_context: RunContextWrapper[Any]     """The current run context."""      server_name: str     """The name of the MCP server."""      tool_name: str     """The name of the tool being invoked."""      arguments: dict[str, Any] | None     """The parsed tool arguments.""" ``` |

#### run\_context `instance-attribute`

```
run_context: RunContextWrapper[Any]
```

The current run context.

#### server\_name `instance-attribute`

```
server_name: str
```

The name of the MCP server.

#### tool\_name `instance-attribute`

```
tool_name: str
```

The name of the tool being invoked.

#### arguments `instance-attribute`

```
arguments: dict[str, Any] | None
```

The parsed tool arguments.

### MCPToolCustomDataContext `dataclass`

Context passed to MCP tool custom data extractors.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 ``` | ``` @dataclass(frozen=True) class MCPToolCustomDataContext:     """Context passed to MCP tool custom data extractors."""      run_context: RunContextWrapper[Any]     """The current run context."""      server_name: str     """The name of the MCP server."""      tool_name: str     """The original MCP tool name invoked on the server."""      tool_display_name: str     """The public tool name exposed through the Agents SDK."""      arguments: Mapping[str, Any]     """The parsed tool arguments."""      result_meta: Mapping[str, Any] | None     """The MCP tool result ``_meta`` payload, if present."""      structured_content: Mapping[str, Any] | None     """The MCP tool result ``structuredContent`` payload, if present."""      is_error: bool | None     """The MCP tool result ``isError`` flag, if present."""      tool_output: ToolOutput     """The model-visible tool output produced by the Agents SDK.""" ``` |

#### run\_context `instance-attribute`

```
run_context: RunContextWrapper[Any]
```

The current run context.

#### server\_name `instance-attribute`

```
server_name: str
```

The name of the MCP server.

#### tool\_name `instance-attribute`

```
tool_name: str
```

The original MCP tool name invoked on the server.

#### tool\_display\_name `instance-attribute`

```
tool_display_name: str
```

The public tool name exposed through the Agents SDK.

#### arguments `instance-attribute`

```
arguments: Mapping[str, Any]
```

The parsed tool arguments.

#### result\_meta `instance-attribute`

```
result_meta: Mapping[str, Any] | None
```

The MCP tool result `_meta` payload, if present.

#### structured\_content `instance-attribute`

```
structured_content: Mapping[str, Any] | None
```

The MCP tool result `structuredContent` payload, if present.

#### is\_error `instance-attribute`

```
is_error: bool | None
```

The MCP tool result `isError` flag, if present.

#### tool\_output `instance-attribute`

```
tool_output: ToolOutput
```

The model-visible tool output produced by the Agents SDK.

### MCPUtil

Set of utilities for interop between MCP and Agents SDK tools.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 ``` | ``` class MCPUtil:     """Set of utilities for interop between MCP and Agents SDK tools."""      @staticmethod     def _extract_static_meta(tool: Any) -> dict[str, Any] | None:         meta = getattr(tool, "meta", None)         if isinstance(meta, dict):             return copy.deepcopy(meta)          model_extra = getattr(tool, "model_extra", None)         if isinstance(model_extra, dict):             extra_meta = model_extra.get("meta")             if isinstance(extra_meta, dict):                 return copy.deepcopy(extra_meta)          model_dump = getattr(tool, "model_dump", None)         if callable(model_dump):             dumped = model_dump()             if isinstance(dumped, dict):                 dumped_meta = dumped.get("meta")                 if isinstance(dumped_meta, dict):                     return copy.deepcopy(dumped_meta)          return None      @classmethod     async def get_all_function_tools(         cls,         servers: list[MCPServer],         convert_schemas_to_strict: bool,         run_context: RunContextWrapper[Any],         agent: AgentBase,         failure_error_function: ToolErrorFunction | None = default_tool_error_function,         include_server_in_tool_names: bool = False,         reserved_tool_names: set[str] | None = None,     ) -> list[Tool]:         """Get all function tools from a list of MCP servers."""         tools: list[Tool] = []         tool_names: set[str] = set()          if include_server_in_tool_names:             server_tool_batches = []             for server_index, server in enumerate(servers):                 listed_tools = await cls._list_tools_with_span(server, run_context, agent)                 server_tool_batches.append((server_index, server, listed_tools))              prefixed_tool_name_overrides = cls._build_prefixed_tool_name_overrides(                 server_tool_batches,                 reserved_names=set(reserved_tool_names or set()),             )              for server_index, server, mcp_tools in server_tool_batches:                 tool_name_overrides = [                     prefixed_tool_name_overrides[(server_index, tool_index)]                     for tool_index in range(len(mcp_tools))                 ]                 function_tools = cls._convert_mcp_tools_to_function_tools(                     mcp_tools,                     server,                     convert_schemas_to_strict,                     agent,                     failure_error_function=failure_error_function,                     tool_name_overrides=tool_name_overrides,                 )                 server_tool_names = {tool.name for tool in function_tools}                 duplicate_tool_names = sorted(server_tool_names & tool_names)                 if duplicate_tool_names:                     raise UserError(                         "Duplicate tool names found across MCP servers: "                         f"{', '.join(duplicate_tool_names)}"                     )                 tool_names.update(server_tool_names)                 tools.extend(function_tools)              return tools          for server in servers:             server_tools = await cls.get_function_tools(                 server,                 convert_schemas_to_strict,                 run_context,                 agent,                 failure_error_function=failure_error_function,             )             server_tool_names = {tool.name for tool in server_tools}             duplicate_tool_names = sorted(server_tool_names & tool_names)             if duplicate_tool_names:                 raise UserError(                     "Duplicate tool names found across MCP servers: "                     f"{', '.join(duplicate_tool_names)}. "                     "Pass `include_server_in_tool_names=True` to "                     "`MCPUtil.get_all_function_tools()` or set "                     "`mcp_config={'include_server_in_tool_names': True}` on the "                     "agent to prefix tool names with their server name and avoid "                     "collisions."                 )             tool_names.update(server_tool_names)             tools.extend(server_tools)          return tools      @classmethod     async def _list_tools_with_span(         cls,         server: MCPServer,         run_context: RunContextWrapper[Any],         agent: AgentBase,     ) -> list[MCPTool]:         with mcp_tools_span(server=server.name) as span:             tools = await server.list_tools(run_context, agent)             span.span_data.result = [tool.name for tool in tools]             return tools      @classmethod     def _convert_mcp_tools_to_function_tools(         cls,         tools: list[MCPTool],         server: MCPServer,         convert_schemas_to_strict: bool,         agent: AgentBase,         failure_error_function: ToolErrorFunction | None = default_tool_error_function,         tool_name_overrides: list[str] | None = None,     ) -> list[Tool]:         return [             cls.to_function_tool(                 tool,                 server,                 convert_schemas_to_strict,                 agent,                 failure_error_function=failure_error_function,                 tool_name_override=(                     tool_name_overrides[index] if tool_name_overrides is not None else None                 ),             )             for index, tool in enumerate(tools)         ]      @classmethod     async def get_function_tools(         cls,         server: MCPServer,         convert_schemas_to_strict: bool,         run_context: RunContextWrapper[Any],         agent: AgentBase,         failure_error_function: ToolErrorFunction | None = default_tool_error_function,         include_server_in_tool_names: bool = False,         tool_name_override: Callable[[MCPTool], str] | None = None,         reserved_tool_names: set[str] | None = None,         server_index: int = 0,     ) -> list[Tool]:         """Get all function tools from a single MCP server."""          tools = await cls._list_tools_with_span(server, run_context, agent)          tool_name_overrides: list[str] | None = None         if tool_name_override is not None:             tool_name_overrides = [tool_name_override(tool) for tool in tools]         elif include_server_in_tool_names:             prefixed_tool_name_overrides = cls._build_prefixed_tool_name_overrides(                 [(server_index, server, tools)],                 reserved_names=set(reserved_tool_names or set()),             )             tool_name_overrides = [                 prefixed_tool_name_overrides[(server_index, tool_index)]                 for tool_index in range(len(tools))             ]          return cls._convert_mcp_tools_to_function_tools(             tools,             server,             convert_schemas_to_strict,             agent,             failure_error_function=failure_error_function,             tool_name_overrides=tool_name_overrides,         )      @staticmethod     def _safe_tool_name_part(value: str, fallback: str) -> str:         safe = "".join(             char if char.isascii() and (char.isalnum() or char in {"_", "-"}) else "_"             for char in value         )         safe = safe.strip("_-")         return safe or fallback      @staticmethod     def _shorten_tool_name(base_name: str, seed: str, *, force_hash: bool = False) -> str:         if not force_hash and len(base_name) <= _MCP_FUNCTION_TOOL_NAME_MAX_LENGTH:             return base_name          hash_suffix = hashlib.sha1(seed.encode("utf-8")).hexdigest()[             :_MCP_FUNCTION_TOOL_HASH_LENGTH         ]         suffix = f"_{hash_suffix}"         stem_length = _MCP_FUNCTION_TOOL_NAME_MAX_LENGTH - len(suffix)         stem = base_name[:stem_length].rstrip("_-") or "mcp"         return f"{stem}{suffix}"      @classmethod     def _build_prefixed_tool_base_name(cls, server_name: str, tool_name: str) -> str:         server_part = cls._safe_tool_name_part(server_name, "server")         tool_part = cls._safe_tool_name_part(tool_name, "tool")         return f"mcp_{server_part}__{tool_part}"      @classmethod     def _build_prefixed_tool_name_overrides(         cls,         server_tool_batches: list[tuple[int, MCPServer, list[MCPTool]]],         *,         reserved_names: set[str],     ) -> dict[tuple[int, int], str]:         """Allocate public tool names for one in-memory MCP listing batch.          Keys are batch-local `(server_index, tool_index)` coordinates, so this mapping does         not depend on object identity or cross any serialization boundary.         """         base_names = [             cls._build_prefixed_tool_base_name(server.name, tool.name)             for _, server, tools in server_tool_batches             for tool in tools         ]         base_name_counts = Counter(base_names)          candidates: list[_PrefixedToolNameCandidate] = []         for server_index, server, tools in server_tool_batches:             for tool_index, tool in enumerate(tools):                 base_name = cls._build_prefixed_tool_base_name(server.name, tool.name)                 seed = f"{server.name}\0{tool.name}"                 force_hash = base_name_counts[base_name] > 1 or base_name in reserved_names                 initial_name = cls._shorten_tool_name(base_name, seed, force_hash=force_hash)                 candidates.append(                     _PrefixedToolNameCandidate(                         batch_key=(server_index, tool_index),                         base_name=base_name,                         seed=seed,                         initial_name=initial_name,                         server_index=server_index,                         tool_index=tool_index,                     )                 )          used_names = set(reserved_names)         tool_name_overrides: dict[tuple[int, int], str] = {}         for candidate in sorted(             candidates,             key=lambda item: (                 item.initial_name,                 item.seed,                 item.server_index,                 item.tool_index,             ),         ):             public_name = candidate.initial_name             collision_index = 1             while public_name in used_names:                 public_name = cls._shorten_tool_name(                     candidate.base_name,                     f"{candidate.seed}\0{collision_index}",                     force_hash=True,                 )                 collision_index += 1              used_names.add(public_name)             tool_name_overrides[candidate.batch_key] = public_name          return tool_name_overrides      @classmethod     def to_function_tool(         cls,         tool: MCPTool,         server: MCPServer,         convert_schemas_to_strict: bool,         agent: AgentBase | None = None,         failure_error_function: ToolErrorFunction | None = default_tool_error_function,         tool_name_override: str | None = None,     ) -> FunctionTool:         """Convert an MCP tool to an Agents SDK function tool.          The ``agent`` parameter is optional for backward compatibility with older         call sites that used ``MCPUtil.to_function_tool(tool, server, strict)``.         When omitted, this helper preserves the historical behavior for static         policies. If the server uses a callable approval policy, approvals default         to required to avoid bypassing dynamic checks.         """         tool_public_name = tool_name_override or tool.name         static_meta = cls._extract_static_meta(tool)         invoke_func_impl = functools.partial(             cls.invoke_mcp_tool,             server,             tool,             tool_display_name=tool_public_name,             meta=static_meta,         )         effective_failure_error_function = server._get_failure_error_function(             failure_error_function         )         schema, is_strict = copy.deepcopy(tool.inputSchema), False          # MCP spec doesn't require the inputSchema to have `properties`, but OpenAI spec does.         if "properties" not in schema:             schema["properties"] = {}          if convert_schemas_to_strict:             # ``ensure_strict_json_schema`` mutates the schema in place and may raise             # partway through, leaving strict-mode artifacts (e.g. ``required`` or             # ``additionalProperties: false``) on a schema we still serve as             # non-strict. Convert a separate copy so the non-strict fallback keeps             # the original schema intact.             try:                 schema = ensure_strict_json_schema(copy.deepcopy(schema))                 is_strict = True             except Exception as e:                 logger.info("Error converting MCP schema to strict mode: %s", e)          needs_approval: (             bool | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]]         ) = server._get_needs_approval_for_tool(tool, agent)          function_tool = _build_wrapped_function_tool(             name=tool_public_name,             description=resolve_mcp_tool_description_for_model(tool),             params_json_schema=schema,             invoke_tool_impl=invoke_func_impl,             on_handled_error=_build_handled_function_tool_error_handler(                 span_message="Error running tool (non-fatal)",                 log_label="MCP tool",             ),             failure_error_function=effective_failure_error_function,             strict_json_schema=is_strict,             needs_approval=needs_approval,             mcp_title=resolve_mcp_tool_title(tool),             tool_origin=ToolOrigin(                 type=ToolOriginType.MCP,                 mcp_server_name=server.name,             ),         )         return function_tool      @staticmethod     def _merge_mcp_meta(         resolved_meta: dict[str, Any] | None,         explicit_meta: dict[str, Any] | None,     ) -> dict[str, Any] | None:         if resolved_meta is None and explicit_meta is None:             return None         merged: dict[str, Any] = {}         if resolved_meta is not None:             merged.update(copy.deepcopy(resolved_meta))         if explicit_meta is not None:             merged.update(copy.deepcopy(explicit_meta))         return merged      @staticmethod     def _copy_mapping_proxy(value: Any) -> Mapping[str, Any] | None:         if not isinstance(value, dict):             return None         return MappingProxyType(copy.deepcopy(value))      @classmethod     async def _extract_custom_data(         cls,         *,         server: MCPServer,         context: RunContextWrapper[Any],         tool_name: str,         tool_display_name: str,         arguments: dict[str, Any],         result: Any,         tool_output: ToolOutput,     ) -> dict[str, Any] | None:         extractor = getattr(server, "custom_data_extractor", None)         if extractor is None:             return None          extractor_context = MCPToolCustomDataContext(             run_context=context,             server_name=server.name,             tool_name=tool_name,             tool_display_name=tool_display_name,             arguments=MappingProxyType(copy.deepcopy(arguments)),             result_meta=cls._copy_mapping_proxy(getattr(result, "meta", None)),             structured_content=cls._copy_mapping_proxy(getattr(result, "structuredContent", None)),             is_error=getattr(result, "isError", None),             tool_output=copy.deepcopy(tool_output),         )         return await maybe_extract_custom_data(extractor, extractor_context)      @classmethod     async def _resolve_meta(         cls,         server: MCPServer,         context: RunContextWrapper[Any],         tool_name: str,         arguments: dict[str, Any] | None,     ) -> dict[str, Any] | None:         meta_resolver = getattr(server, "tool_meta_resolver", None)         if meta_resolver is None:             return None          arguments_copy = copy.deepcopy(arguments) if arguments is not None else None         resolver_context = MCPToolMetaContext(             run_context=context,             server_name=server.name,             tool_name=tool_name,             arguments=arguments_copy,         )         result = meta_resolver(resolver_context)         if inspect.isawaitable(result):             result = await result         if result is None:             return None         if not isinstance(result, dict):             raise TypeError("MCP meta resolver must return a dict or None.")         return result      @classmethod     async def invoke_mcp_tool(         cls,         server: MCPServer,         tool: MCPTool,         context: RunContextWrapper[Any],         input_json: str,         *,         meta: dict[str, Any] | None = None,         tool_display_name: str | None = None,     ) -> ToolOutput:         """Invoke an MCP tool and return the result as ToolOutput."""         tool_name_for_display = tool_display_name or tool.name         json_decode_error: Exception | None = None         try:             json_data = json.loads(input_json) if input_json else {}         except Exception as e:             json_decode_error = e          if json_decode_error is not None:             error_message = f"Invalid JSON input for tool {tool_name_for_display}"             if _debug.DONT_LOG_TOOL_DATA:                 logger.debug(error_message)                 raise ModelBehaviorError(error_message)             else:                 error_message = f"{error_message}: {input_json}"                 logger.debug(error_message)             raise ModelBehaviorError(error_message) from json_decode_error          if not isinstance(json_data, dict):             raise ModelBehaviorError(                 f"Invalid JSON input for tool {tool_name_for_display}: expected a JSON object"             )          if _debug.DONT_LOG_TOOL_DATA:             logger.debug("Invoking MCP tool %s", tool_name_for_display)         else:             logger.debug("Invoking MCP tool %s with input %s", tool_name_for_display, input_json)          try:             resolved_meta = await cls._resolve_meta(server, context, tool.name, json_data)             merged_meta = cls._merge_mcp_meta(resolved_meta, meta)             call_task = asyncio.create_task(                 server.call_tool(tool.name, json_data)                 if merged_meta is None                 else server.call_tool(tool.name, json_data, meta=merged_meta)             )             try:                 done, _ = await asyncio.wait({call_task}, return_when=asyncio.FIRST_COMPLETED)                 finished_task = done.pop()                 if finished_task.cancelled():                     raise MCPToolCancellationError(                         f"Failed to call tool '{tool.name}' on MCP server '{server.name}': "                         "tool execution was cancelled."                     )                 result = finished_task.result()             except asyncio.CancelledError:                 if not call_task.done():                     call_task.cancel()                 try:                     await call_task                 except (asyncio.CancelledError, Exception):                     pass                 raise         except (UserError, MCPToolCancellationError):             # Re-raise handled tool-call errors as-is; the FunctionTool failure pipeline             # will format them into model-visible tool errors when appropriate.             raise         except Exception as e:             if _McpError is not None and isinstance(e, _McpError):                 # An MCP-level error (e.g. upstream HTTP 4xx/5xx, tool not found, etc.)                 # is not a programming error – re-raise so the FunctionTool failure                 # pipeline (failure_error_function) can handle it.  The default handler                 # will surface the message as a structured error result; callers who set                 # failure_error_function=None will have the error raised as documented.                 error_text = e.error.message if hasattr(e, "error") and e.error else str(e)                 logger.warning(                     "MCP tool %s on server '%s' returned an error: %s",                     tool_name_for_display,                     server.name,                     error_text,                 )                 raise              logger.error(                 "Error invoking MCP tool %s on server '%s': %s",                 tool_name_for_display,                 server.name,                 e,             )             raise AgentsException(                 f"Error invoking MCP tool {tool_name_for_display} on server '{server.name}': {e}"             ) from e          if _debug.DONT_LOG_TOOL_DATA:             logger.debug("MCP tool %s completed.", tool_name_for_display)         else:             logger.debug("MCP tool %s returned %s", tool_name_for_display, result)          # If structured content is requested and available, use it exclusively         tool_output: ToolOutput         if server.use_structured_content and result.structuredContent:             tool_output = json.dumps(result.structuredContent)         else:             tool_output_list: list[ToolOutputItem] = []             for item in result.content:                 if item.type == "text":                     tool_output_list.append(ToolOutputTextDict(type="text", text=item.text))                 elif item.type == "image":                     tool_output_list.append(                         ToolOutputImageDict(                             type="image", image_url=f"data:{item.mimeType};base64,{item.data}"                         )                     )                 else:                     # Fall back to regular text content                     tool_output_list.append(                         ToolOutputTextDict(type="text", text=str(item.model_dump(mode="json")))                     )             if len(tool_output_list) == 1:                 tool_output = tool_output_list[0]             else:                 tool_output = tool_output_list          custom_data = await cls._extract_custom_data(             server=server,             context=context,             tool_name=tool.name,             tool_display_name=tool_name_for_display,             arguments=json_data,             result=result,             tool_output=tool_output,         )         if custom_data and isinstance(context, ToolContext):             context._custom_data = custom_data          current_span = get_current_span()         if current_span:             if isinstance(current_span.span_data, FunctionSpanData):                 if not isinstance(context, ToolContext) or (                     context.run_config is None or context.run_config.trace_include_sensitive_data                 ):                     current_span.span_data.output = tool_output                 current_span.span_data.mcp_data = {                     "server": server.name,                 }             else:                 logger.warning(                     "Current span is not a FunctionSpanData, skipping tool output: %s", current_span                 )          return tool_output ``` |

#### get\_all\_function\_tools `async` `classmethod`

```
get_all_function_tools(
    servers: list[MCPServer],
    convert_schemas_to_strict: bool,
    run_context: RunContextWrapper[Any],
    agent: AgentBase,
    failure_error_function: ToolErrorFunction
    | None = default_tool_error_function,
    include_server_in_tool_names: bool = False,
    reserved_tool_names: set[str] | None = None,
) -> list[Tool]
```

Get all function tools from a list of MCP servers.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 ``` | ``` @classmethod async def get_all_function_tools(     cls,     servers: list[MCPServer],     convert_schemas_to_strict: bool,     run_context: RunContextWrapper[Any],     agent: AgentBase,     failure_error_function: ToolErrorFunction | None = default_tool_error_function,     include_server_in_tool_names: bool = False,     reserved_tool_names: set[str] | None = None, ) -> list[Tool]:     """Get all function tools from a list of MCP servers."""     tools: list[Tool] = []     tool_names: set[str] = set()      if include_server_in_tool_names:         server_tool_batches = []         for server_index, server in enumerate(servers):             listed_tools = await cls._list_tools_with_span(server, run_context, agent)             server_tool_batches.append((server_index, server, listed_tools))          prefixed_tool_name_overrides = cls._build_prefixed_tool_name_overrides(             server_tool_batches,             reserved_names=set(reserved_tool_names or set()),         )          for server_index, server, mcp_tools in server_tool_batches:             tool_name_overrides = [                 prefixed_tool_name_overrides[(server_index, tool_index)]                 for tool_index in range(len(mcp_tools))             ]             function_tools = cls._convert_mcp_tools_to_function_tools(                 mcp_tools,                 server,                 convert_schemas_to_strict,                 agent,                 failure_error_function=failure_error_function,                 tool_name_overrides=tool_name_overrides,             )             server_tool_names = {tool.name for tool in function_tools}             duplicate_tool_names = sorted(server_tool_names & tool_names)             if duplicate_tool_names:                 raise UserError(                     "Duplicate tool names found across MCP servers: "                     f"{', '.join(duplicate_tool_names)}"                 )             tool_names.update(server_tool_names)             tools.extend(function_tools)          return tools      for server in servers:         server_tools = await cls.get_function_tools(             server,             convert_schemas_to_strict,             run_context,             agent,             failure_error_function=failure_error_function,         )         server_tool_names = {tool.name for tool in server_tools}         duplicate_tool_names = sorted(server_tool_names & tool_names)         if duplicate_tool_names:             raise UserError(                 "Duplicate tool names found across MCP servers: "                 f"{', '.join(duplicate_tool_names)}. "                 "Pass `include_server_in_tool_names=True` to "                 "`MCPUtil.get_all_function_tools()` or set "                 "`mcp_config={'include_server_in_tool_names': True}` on the "                 "agent to prefix tool names with their server name and avoid "                 "collisions."             )         tool_names.update(server_tool_names)         tools.extend(server_tools)      return tools ``` |

#### get\_function\_tools `async` `classmethod`

```
get_function_tools(
    server: MCPServer,
    convert_schemas_to_strict: bool,
    run_context: RunContextWrapper[Any],
    agent: AgentBase,
    failure_error_function: ToolErrorFunction
    | None = default_tool_error_function,
    include_server_in_tool_names: bool = False,
    tool_name_override: Callable[[Tool], str] | None = None,
    reserved_tool_names: set[str] | None = None,
    server_index: int = 0,
) -> list[Tool]
```

Get all function tools from a single MCP server.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 ``` | ``` @classmethod async def get_function_tools(     cls,     server: MCPServer,     convert_schemas_to_strict: bool,     run_context: RunContextWrapper[Any],     agent: AgentBase,     failure_error_function: ToolErrorFunction | None = default_tool_error_function,     include_server_in_tool_names: bool = False,     tool_name_override: Callable[[MCPTool], str] | None = None,     reserved_tool_names: set[str] | None = None,     server_index: int = 0, ) -> list[Tool]:     """Get all function tools from a single MCP server."""      tools = await cls._list_tools_with_span(server, run_context, agent)      tool_name_overrides: list[str] | None = None     if tool_name_override is not None:         tool_name_overrides = [tool_name_override(tool) for tool in tools]     elif include_server_in_tool_names:         prefixed_tool_name_overrides = cls._build_prefixed_tool_name_overrides(             [(server_index, server, tools)],             reserved_names=set(reserved_tool_names or set()),         )         tool_name_overrides = [             prefixed_tool_name_overrides[(server_index, tool_index)]             for tool_index in range(len(tools))         ]      return cls._convert_mcp_tools_to_function_tools(         tools,         server,         convert_schemas_to_strict,         agent,         failure_error_function=failure_error_function,         tool_name_overrides=tool_name_overrides,     ) ``` |

#### to\_function\_tool `classmethod`

```
to_function_tool(
    tool: Tool,
    server: MCPServer,
    convert_schemas_to_strict: bool,
    agent: AgentBase | None = None,
    failure_error_function: ToolErrorFunction
    | None = default_tool_error_function,
    tool_name_override: str | None = None,
) -> FunctionTool
```

Convert an MCP tool to an Agents SDK function tool.

The `agent` parameter is optional for backward compatibility with older
call sites that used `MCPUtil.to_function_tool(tool, server, strict)`.
When omitted, this helper preserves the historical behavior for static
policies. If the server uses a callable approval policy, approvals default
to required to avoid bypassing dynamic checks.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 ``` | ``` @classmethod def to_function_tool(     cls,     tool: MCPTool,     server: MCPServer,     convert_schemas_to_strict: bool,     agent: AgentBase | None = None,     failure_error_function: ToolErrorFunction | None = default_tool_error_function,     tool_name_override: str | None = None, ) -> FunctionTool:     """Convert an MCP tool to an Agents SDK function tool.      The ``agent`` parameter is optional for backward compatibility with older     call sites that used ``MCPUtil.to_function_tool(tool, server, strict)``.     When omitted, this helper preserves the historical behavior for static     policies. If the server uses a callable approval policy, approvals default     to required to avoid bypassing dynamic checks.     """     tool_public_name = tool_name_override or tool.name     static_meta = cls._extract_static_meta(tool)     invoke_func_impl = functools.partial(         cls.invoke_mcp_tool,         server,         tool,         tool_display_name=tool_public_name,         meta=static_meta,     )     effective_failure_error_function = server._get_failure_error_function(         failure_error_function     )     schema, is_strict = copy.deepcopy(tool.inputSchema), False      # MCP spec doesn't require the inputSchema to have `properties`, but OpenAI spec does.     if "properties" not in schema:         schema["properties"] = {}      if convert_schemas_to_strict:         # ``ensure_strict_json_schema`` mutates the schema in place and may raise         # partway through, leaving strict-mode artifacts (e.g. ``required`` or         # ``additionalProperties: false``) on a schema we still serve as         # non-strict. Convert a separate copy so the non-strict fallback keeps         # the original schema intact.         try:             schema = ensure_strict_json_schema(copy.deepcopy(schema))             is_strict = True         except Exception as e:             logger.info("Error converting MCP schema to strict mode: %s", e)      needs_approval: (         bool | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]]     ) = server._get_needs_approval_for_tool(tool, agent)      function_tool = _build_wrapped_function_tool(         name=tool_public_name,         description=resolve_mcp_tool_description_for_model(tool),         params_json_schema=schema,         invoke_tool_impl=invoke_func_impl,         on_handled_error=_build_handled_function_tool_error_handler(             span_message="Error running tool (non-fatal)",             log_label="MCP tool",         ),         failure_error_function=effective_failure_error_function,         strict_json_schema=is_strict,         needs_approval=needs_approval,         mcp_title=resolve_mcp_tool_title(tool),         tool_origin=ToolOrigin(             type=ToolOriginType.MCP,             mcp_server_name=server.name,         ),     )     return function_tool ``` |

#### invoke\_mcp\_tool `async` `classmethod`

```
invoke_mcp_tool(
    server: MCPServer,
    tool: Tool,
    context: RunContextWrapper[Any],
    input_json: str,
    *,
    meta: dict[str, Any] | None = None,
    tool_display_name: str | None = None,
) -> ToolOutput
```

Invoke an MCP tool and return the result as ToolOutput.

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 ``` | ``` @classmethod async def invoke_mcp_tool(     cls,     server: MCPServer,     tool: MCPTool,     context: RunContextWrapper[Any],     input_json: str,     *,     meta: dict[str, Any] | None = None,     tool_display_name: str | None = None, ) -> ToolOutput:     """Invoke an MCP tool and return the result as ToolOutput."""     tool_name_for_display = tool_display_name or tool.name     json_decode_error: Exception | None = None     try:         json_data = json.loads(input_json) if input_json else {}     except Exception as e:         json_decode_error = e      if json_decode_error is not None:         error_message = f"Invalid JSON input for tool {tool_name_for_display}"         if _debug.DONT_LOG_TOOL_DATA:             logger.debug(error_message)             raise ModelBehaviorError(error_message)         else:             error_message = f"{error_message}: {input_json}"             logger.debug(error_message)         raise ModelBehaviorError(error_message) from json_decode_error      if not isinstance(json_data, dict):         raise ModelBehaviorError(             f"Invalid JSON input for tool {tool_name_for_display}: expected a JSON object"         )      if _debug.DONT_LOG_TOOL_DATA:         logger.debug("Invoking MCP tool %s", tool_name_for_display)     else:         logger.debug("Invoking MCP tool %s with input %s", tool_name_for_display, input_json)      try:         resolved_meta = await cls._resolve_meta(server, context, tool.name, json_data)         merged_meta = cls._merge_mcp_meta(resolved_meta, meta)         call_task = asyncio.create_task(             server.call_tool(tool.name, json_data)             if merged_meta is None             else server.call_tool(tool.name, json_data, meta=merged_meta)         )         try:             done, _ = await asyncio.wait({call_task}, return_when=asyncio.FIRST_COMPLETED)             finished_task = done.pop()             if finished_task.cancelled():                 raise MCPToolCancellationError(                     f"Failed to call tool '{tool.name}' on MCP server '{server.name}': "                     "tool execution was cancelled."                 )             result = finished_task.result()         except asyncio.CancelledError:             if not call_task.done():                 call_task.cancel()             try:                 await call_task             except (asyncio.CancelledError, Exception):                 pass             raise     except (UserError, MCPToolCancellationError):         # Re-raise handled tool-call errors as-is; the FunctionTool failure pipeline         # will format them into model-visible tool errors when appropriate.         raise     except Exception as e:         if _McpError is not None and isinstance(e, _McpError):             # An MCP-level error (e.g. upstream HTTP 4xx/5xx, tool not found, etc.)             # is not a programming error – re-raise so the FunctionTool failure             # pipeline (failure_error_function) can handle it.  The default handler             # will surface the message as a structured error result; callers who set             # failure_error_function=None will have the error raised as documented.             error_text = e.error.message if hasattr(e, "error") and e.error else str(e)             logger.warning(                 "MCP tool %s on server '%s' returned an error: %s",                 tool_name_for_display,                 server.name,                 error_text,             )             raise          logger.error(             "Error invoking MCP tool %s on server '%s': %s",             tool_name_for_display,             server.name,             e,         )         raise AgentsException(             f"Error invoking MCP tool {tool_name_for_display} on server '{server.name}': {e}"         ) from e      if _debug.DONT_LOG_TOOL_DATA:         logger.debug("MCP tool %s completed.", tool_name_for_display)     else:         logger.debug("MCP tool %s returned %s", tool_name_for_display, result)      # If structured content is requested and available, use it exclusively     tool_output: ToolOutput     if server.use_structured_content and result.structuredContent:         tool_output = json.dumps(result.structuredContent)     else:         tool_output_list: list[ToolOutputItem] = []         for item in result.content:             if item.type == "text":                 tool_output_list.append(ToolOutputTextDict(type="text", text=item.text))             elif item.type == "image":                 tool_output_list.append(                     ToolOutputImageDict(                         type="image", image_url=f"data:{item.mimeType};base64,{item.data}"                     )                 )             else:                 # Fall back to regular text content                 tool_output_list.append(                     ToolOutputTextDict(type="text", text=str(item.model_dump(mode="json")))                 )         if len(tool_output_list) == 1:             tool_output = tool_output_list[0]         else:             tool_output = tool_output_list      custom_data = await cls._extract_custom_data(         server=server,         context=context,         tool_name=tool.name,         tool_display_name=tool_name_for_display,         arguments=json_data,         result=result,         tool_output=tool_output,     )     if custom_data and isinstance(context, ToolContext):         context._custom_data = custom_data      current_span = get_current_span()     if current_span:         if isinstance(current_span.span_data, FunctionSpanData):             if not isinstance(context, ToolContext) or (                 context.run_config is None or context.run_config.trace_include_sensitive_data             ):                 current_span.span_data.output = tool_output             current_span.span_data.mcp_data = {                 "server": server.name,             }         else:             logger.warning(                 "Current span is not a FunctionSpanData, skipping tool output: %s", current_span             )      return tool_output ``` |

### create\_static\_tool\_filter

```
create_static_tool_filter(
    allowed_tool_names: list[str] | None = None,
    blocked_tool_names: list[str] | None = None,
) -> ToolFilterStatic | None
```

Create a static tool filter from allowlist and blocklist parameters.

This is a convenience function for creating a ToolFilterStatic.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `allowed_tool_names` | `list[str] | None` | Optional list of tool names to allow (whitelist). | `None` |
| `blocked_tool_names` | `list[str] | None` | Optional list of tool names to exclude (blacklist). | `None` |

Returns:

| Type | Description |
| --- | --- |
| `ToolFilterStatic | None` | A ToolFilterStatic if any filtering is specified, None otherwise. |

Source code in `src/agents/mcp/util.py`

|  |  |
| --- | --- |
| ``` 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 ``` | ``` def create_static_tool_filter(     allowed_tool_names: list[str] | None = None,     blocked_tool_names: list[str] | None = None, ) -> ToolFilterStatic | None:     """Create a static tool filter from allowlist and blocklist parameters.      This is a convenience function for creating a ToolFilterStatic.      Args:         allowed_tool_names: Optional list of tool names to allow (whitelist).         blocked_tool_names: Optional list of tool names to exclude (blacklist).      Returns:         A ToolFilterStatic if any filtering is specified, None otherwise.     """     if allowed_tool_names is None and blocked_tool_names is None:         return None      filter_dict: ToolFilterStatic = {}     if allowed_tool_names is not None:         filter_dict["allowed_tool_names"] = allowed_tool_names     if blocked_tool_names is not None:         filter_dict["blocked_tool_names"] = blocked_tool_names      return filter_dict ``` |