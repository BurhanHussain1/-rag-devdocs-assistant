---
url: https://openai.github.io/openai-agents-python/ref/tool_context/
title: `Tool Context`
framework: openai
---

# `Tool Context`

### ToolContext `dataclass`

Bases: `RunContextWrapper[TContext]`

The context of a tool call.

Source code in `src/agents/tool_context.py`

|  |  |
| --- | --- |
| ```  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 ``` | ``` @dataclass(eq=False) class ToolContext(RunContextWrapper[TContext]):     """The context of a tool call."""      tool_name: str = field(default_factory=_assert_must_pass_tool_name)     """The name of the tool being invoked."""      tool_call_id: str = field(default_factory=_assert_must_pass_tool_call_id)     """The ID of the tool call."""      tool_arguments: str = field(default_factory=_assert_must_pass_tool_arguments)     """The raw arguments string of the tool call."""      tool_call: ResponseFunctionToolCall | None = None     """The tool call object associated with this invocation."""      tool_namespace: str | None = None     """The Responses API namespace for this tool call, when present."""      agent: AgentBase[Any] | None = None     """The active agent for this tool call, when available."""      run_config: RunConfig | None = None     """The active run config for this tool call, when available."""      def __init__(         self,         context: TContext,         usage: Usage | object = _MISSING,         tool_name: str | object = _MISSING,         tool_call_id: str | object = _MISSING,         tool_arguments: str | object = _MISSING,         tool_call: ResponseFunctionToolCall | None = None,         *,         tool_namespace: str | None = None,         agent: AgentBase[Any] | None = None,         run_config: RunConfig | None = None,         turn_input: list[TResponseInputItem] | None = None,         _approvals: dict[str, _ApprovalRecord] | None = None,         tool_input: Any | None = None,     ) -> None:         """Preserve the v0.7 positional constructor while accepting new context fields."""         resolved_usage = Usage() if usage is _MISSING else cast(Usage, usage)         super().__init__(             context=context,             usage=resolved_usage,             turn_input=list(turn_input or []),             _approvals={} if _approvals is None else _approvals,             tool_input=tool_input,         )         self.tool_name = (             _assert_must_pass_tool_name() if tool_name is _MISSING else cast(str, tool_name)         )         self.tool_arguments = (             _assert_must_pass_tool_arguments()             if tool_arguments is _MISSING             else cast(str, tool_arguments)         )         self.tool_call_id = (             _assert_must_pass_tool_call_id()             if tool_call_id is _MISSING             else cast(str, tool_call_id)         )         self.tool_call = tool_call         self.tool_namespace = (             tool_namespace             if isinstance(tool_namespace, str)             else get_tool_call_namespace(tool_call)         )         self.agent = agent         self.run_config = run_config         # Internal adapter hook used to attach SDK-only custom data to the emitted output item.         self._custom_data: dict[str, Any] | None = None      @property     def qualified_tool_name(self) -> str:         """Return the tool name qualified by namespace when available."""         return tool_trace_name(self.tool_name, self.tool_namespace) or self.tool_name      @classmethod     def from_agent_context(         cls,         context: RunContextWrapper[TContext],         tool_call_id: str,         tool_call: ResponseFunctionToolCall | None = None,         agent: AgentBase[Any] | None = None,         *,         tool_name: str | None = None,         tool_arguments: str | None = None,         tool_namespace: str | None = None,         run_config: RunConfig | None = None,     ) -> ToolContext:         """         Create a ToolContext from a RunContextWrapper.         """         # Grab the names of the RunContextWrapper's init=True fields         base_values: dict[str, Any] = {             f.name: getattr(context, f.name) for f in fields(RunContextWrapper) if f.init         }         resolved_tool_name = (             tool_name             if tool_name is not None             else (tool_call.name if tool_call is not None else _assert_must_pass_tool_name())         )         resolved_tool_args = (             tool_arguments             if tool_arguments is not None             else (                 tool_call.arguments if tool_call is not None else _assert_must_pass_tool_arguments()             )         )         tool_agent = agent         if tool_agent is None and isinstance(context, ToolContext):             tool_agent = context.agent         tool_run_config = run_config         if tool_run_config is None and isinstance(context, ToolContext):             tool_run_config = context.run_config          tool_context = cls(             tool_name=resolved_tool_name,             tool_call_id=tool_call_id,             tool_arguments=resolved_tool_args,             tool_call=tool_call,             tool_namespace=(                 tool_namespace                 if isinstance(tool_namespace, str)                 else (                     getattr(tool_call, "namespace", None)                     if tool_call is not None                     and isinstance(getattr(tool_call, "namespace", None), str)                     else None                 )             ),             agent=tool_agent,             run_config=tool_run_config,             **base_values,         )         set_agent_tool_state_scope(tool_context, get_agent_tool_state_scope(context))         return tool_context ``` |

#### tool\_name `class-attribute` `instance-attribute`

```
tool_name: str = (
    _assert_must_pass_tool_name()
    if tool_name is _MISSING
    else cast(str, tool_name)
)
```

The name of the tool being invoked.

#### tool\_arguments `class-attribute` `instance-attribute`

```
tool_arguments: str = (
    _assert_must_pass_tool_arguments()
    if tool_arguments is _MISSING
    else cast(str, tool_arguments)
)
```

The raw arguments string of the tool call.

#### tool\_call\_id `class-attribute` `instance-attribute`

```
tool_call_id: str = (
    _assert_must_pass_tool_call_id()
    if tool_call_id is _MISSING
    else cast(str, tool_call_id)
)
```

The ID of the tool call.

#### tool\_call `class-attribute` `instance-attribute`

```
tool_call: ResponseFunctionToolCall | None = tool_call
```

The tool call object associated with this invocation.

#### tool\_namespace `class-attribute` `instance-attribute`

```
tool_namespace: str | None = (
    tool_namespace
    if isinstance(tool_namespace, str)
    else get_tool_call_namespace(tool_call)
)
```

The Responses API namespace for this tool call, when present.

#### agent `class-attribute` `instance-attribute`

```
agent: AgentBase[Any] | None = agent
```

The active agent for this tool call, when available.

#### run\_config `class-attribute` `instance-attribute`

```
run_config: RunConfig | None = run_config
```

The active run config for this tool call, when available.

#### qualified\_tool\_name `property`

```
qualified_tool_name: str
```

Return the tool name qualified by namespace when available.

#### context `instance-attribute`

```
context: TContext
```

The context object (or None), passed by you to `Runner.run()`

#### usage `class-attribute` `instance-attribute`

```
usage: Usage = field(default_factory=Usage)
```

The usage of the agent run so far. For streamed responses, the usage will be stale until the
last chunk of the stream is processed.

#### tool\_input `class-attribute` `instance-attribute`

```
tool_input: Any | None = None
```

Structured input for the current agent tool run, when available.

#### \_\_init\_\_

```
__init__(
    context: TContext,
    usage: Usage | object = _MISSING,
    tool_name: str | object = _MISSING,
    tool_call_id: str | object = _MISSING,
    tool_arguments: str | object = _MISSING,
    tool_call: ResponseFunctionToolCall | None = None,
    *,
    tool_namespace: str | None = None,
    agent: AgentBase[Any] | None = None,
    run_config: RunConfig | None = None,
    turn_input: list[TResponseInputItem] | None = None,
    _approvals: dict[str, _ApprovalRecord] | None = None,
    tool_input: Any | None = None,
) -> None
```

Preserve the v0.7 positional constructor while accepting new context fields.

Source code in `src/agents/tool_context.py`

|  |  |
| --- | --- |
| ```  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 ``` | ``` def __init__(     self,     context: TContext,     usage: Usage | object = _MISSING,     tool_name: str | object = _MISSING,     tool_call_id: str | object = _MISSING,     tool_arguments: str | object = _MISSING,     tool_call: ResponseFunctionToolCall | None = None,     *,     tool_namespace: str | None = None,     agent: AgentBase[Any] | None = None,     run_config: RunConfig | None = None,     turn_input: list[TResponseInputItem] | None = None,     _approvals: dict[str, _ApprovalRecord] | None = None,     tool_input: Any | None = None, ) -> None:     """Preserve the v0.7 positional constructor while accepting new context fields."""     resolved_usage = Usage() if usage is _MISSING else cast(Usage, usage)     super().__init__(         context=context,         usage=resolved_usage,         turn_input=list(turn_input or []),         _approvals={} if _approvals is None else _approvals,         tool_input=tool_input,     )     self.tool_name = (         _assert_must_pass_tool_name() if tool_name is _MISSING else cast(str, tool_name)     )     self.tool_arguments = (         _assert_must_pass_tool_arguments()         if tool_arguments is _MISSING         else cast(str, tool_arguments)     )     self.tool_call_id = (         _assert_must_pass_tool_call_id()         if tool_call_id is _MISSING         else cast(str, tool_call_id)     )     self.tool_call = tool_call     self.tool_namespace = (         tool_namespace         if isinstance(tool_namespace, str)         else get_tool_call_namespace(tool_call)     )     self.agent = agent     self.run_config = run_config     # Internal adapter hook used to attach SDK-only custom data to the emitted output item.     self._custom_data: dict[str, Any] | None = None ``` |

#### from\_agent\_context `classmethod`

```
from_agent_context(
    context: RunContextWrapper[TContext],
    tool_call_id: str,
    tool_call: ResponseFunctionToolCall | None = None,
    agent: AgentBase[Any] | None = None,
    *,
    tool_name: str | None = None,
    tool_arguments: str | None = None,
    tool_namespace: str | None = None,
    run_config: RunConfig | None = None,
) -> ToolContext
```

Create a ToolContext from a RunContextWrapper.

Source code in `src/agents/tool_context.py`

|  |  |
| --- | --- |
| ``` 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 ``` | ``` @classmethod def from_agent_context(     cls,     context: RunContextWrapper[TContext],     tool_call_id: str,     tool_call: ResponseFunctionToolCall | None = None,     agent: AgentBase[Any] | None = None,     *,     tool_name: str | None = None,     tool_arguments: str | None = None,     tool_namespace: str | None = None,     run_config: RunConfig | None = None, ) -> ToolContext:     """     Create a ToolContext from a RunContextWrapper.     """     # Grab the names of the RunContextWrapper's init=True fields     base_values: dict[str, Any] = {         f.name: getattr(context, f.name) for f in fields(RunContextWrapper) if f.init     }     resolved_tool_name = (         tool_name         if tool_name is not None         else (tool_call.name if tool_call is not None else _assert_must_pass_tool_name())     )     resolved_tool_args = (         tool_arguments         if tool_arguments is not None         else (             tool_call.arguments if tool_call is not None else _assert_must_pass_tool_arguments()         )     )     tool_agent = agent     if tool_agent is None and isinstance(context, ToolContext):         tool_agent = context.agent     tool_run_config = run_config     if tool_run_config is None and isinstance(context, ToolContext):         tool_run_config = context.run_config      tool_context = cls(         tool_name=resolved_tool_name,         tool_call_id=tool_call_id,         tool_arguments=resolved_tool_args,         tool_call=tool_call,         tool_namespace=(             tool_namespace             if isinstance(tool_namespace, str)             else (                 getattr(tool_call, "namespace", None)                 if tool_call is not None                 and isinstance(getattr(tool_call, "namespace", None), str)                 else None             )         ),         agent=tool_agent,         run_config=tool_run_config,         **base_values,     )     set_agent_tool_state_scope(tool_context, get_agent_tool_state_scope(context))     return tool_context ``` |

#### is\_tool\_approved

```
is_tool_approved(
    tool_name: str, call_id: str
) -> bool | None
```

Return True/False/None for the given tool call.

Source code in `src/agents/run_context.py`

|  |  |
| --- | --- |
| ``` 178 179 180 ``` | ``` def is_tool_approved(self, tool_name: str, call_id: str) -> bool | None:     """Return True/False/None for the given tool call."""     return self._get_approval_status_for_key(tool_name, call_id) ``` |

#### get\_rejection\_message

```
get_rejection_message(
    tool_name: str,
    call_id: str,
    *,
    tool_namespace: str | None = None,
    existing_pending: ToolApprovalItem | None = None,
    tool_lookup_key: FunctionToolLookupKey | None = None,
) -> str | None
```

Return a stored rejection message for a tool call if one exists.

Source code in `src/agents/run_context.py`

|  |  |
| --- | --- |
| ``` 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 ``` | ``` def get_rejection_message(     self,     tool_name: str,     call_id: str,     *,     tool_namespace: str | None = None,     existing_pending: ToolApprovalItem | None = None,     tool_lookup_key: FunctionToolLookupKey | None = None, ) -> str | None:     """Return a stored rejection message for a tool call if one exists."""     candidates: list[str] = []     explicit_namespace = (         tool_namespace if isinstance(tool_namespace, str) and tool_namespace else None     )     pending_namespace = (         self._resolve_tool_namespace(existing_pending) if existing_pending is not None else None     )     pending_key = self._resolve_approval_key(existing_pending) if existing_pending else None     pending_tool_name = self._resolve_tool_name(existing_pending) if existing_pending else None     pending_keys = (         list(self._resolve_approval_keys(existing_pending))         if existing_pending is not None         else []     )      if existing_pending and pending_key is not None:         candidates.append(pending_key)     explicit_keys = (         list(             get_function_tool_approval_keys(                 tool_name=tool_name,                 tool_namespace=explicit_namespace,                 tool_lookup_key=tool_lookup_key,                 include_legacy_deferred_key=True,             )         )         if explicit_namespace is not None or tool_lookup_key is not None         else []     )     for explicit_key in explicit_keys:         if explicit_key not in candidates:             candidates.append(explicit_key)     if not explicit_keys and pending_namespace and pending_key is not None:         if pending_key not in candidates:             candidates.append(pending_key)     if (         explicit_namespace is None         and tool_lookup_key is None         and existing_pending is None         and tool_name not in candidates     ):         candidates.append(tool_name)     if existing_pending:         for pending_candidate in pending_keys:             if pending_candidate not in candidates:                 candidates.append(pending_candidate)         if (             pending_namespace is None             and pending_tool_name is not None             and pending_tool_name not in candidates         ):             candidates.append(pending_tool_name)      for candidate in candidates:         approval_entry = self._approvals.get(candidate)         if not approval_entry:             continue         message = self._get_rejection_message_for_key(approval_entry, call_id)         if message is not None:             return message     return None ``` |

#### approve\_tool

```
approve_tool(
    approval_item: ToolApprovalItem,
    always_approve: bool = False,
) -> None
```

Approve a tool call, optionally for all future calls.

Source code in `src/agents/run_context.py`

|  |  |
| --- | --- |
| ``` 355 356 357 358 359 360 361 ``` | ``` def approve_tool(self, approval_item: ToolApprovalItem, always_approve: bool = False) -> None:     """Approve a tool call, optionally for all future calls."""     self._apply_approval_decision(         approval_item,         always=always_approve,         approve=True,     ) ``` |

#### reject\_tool

```
reject_tool(
    approval_item: ToolApprovalItem,
    always_reject: bool = False,
    rejection_message: str | None = None,
) -> None
```

Reject a tool call, optionally for all future calls.

Source code in `src/agents/run_context.py`

|  |  |
| --- | --- |
| ``` 363 364 365 366 367 368 369 370 371 372 373 374 375 ``` | ``` def reject_tool(     self,     approval_item: ToolApprovalItem,     always_reject: bool = False,     rejection_message: str | None = None, ) -> None:     """Reject a tool call, optionally for all future calls."""     self._apply_approval_decision(         approval_item,         always=always_reject,         approve=False,         rejection_message=rejection_message,     ) ``` |

#### get\_approval\_status

```
get_approval_status(
    tool_name: str,
    call_id: str,
    *,
    tool_namespace: str | None = None,
    existing_pending: ToolApprovalItem | None = None,
    tool_lookup_key: FunctionToolLookupKey | None = None,
) -> bool | None
```

Return approval status, retrying with pending item's tool name if necessary.

Source code in `src/agents/run_context.py`

|  |  |
| --- | --- |
| ``` 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 ``` | ``` def get_approval_status(     self,     tool_name: str,     call_id: str,     *,     tool_namespace: str | None = None,     existing_pending: ToolApprovalItem | None = None,     tool_lookup_key: FunctionToolLookupKey | None = None, ) -> bool | None:     """Return approval status, retrying with pending item's tool name if necessary."""     candidates: list[str] = []     explicit_namespace = (         tool_namespace if isinstance(tool_namespace, str) and tool_namespace else None     )     pending_namespace = (         self._resolve_tool_namespace(existing_pending) if existing_pending is not None else None     )     pending_key = self._resolve_approval_key(existing_pending) if existing_pending else None     pending_tool_name = self._resolve_tool_name(existing_pending) if existing_pending else None     pending_keys = (         list(self._resolve_approval_keys(existing_pending))         if existing_pending is not None         else []     )      if existing_pending and pending_key is not None:         candidates.append(pending_key)     explicit_keys = (         list(             get_function_tool_approval_keys(                 tool_name=tool_name,                 tool_namespace=explicit_namespace,                 tool_lookup_key=tool_lookup_key,                 include_legacy_deferred_key=True,             )         )         if explicit_namespace is not None or tool_lookup_key is not None         else []     )     for explicit_key in explicit_keys:         if explicit_key not in candidates:             candidates.append(explicit_key)     if not explicit_keys and pending_namespace and pending_key is not None:         if pending_key not in candidates:             candidates.append(pending_key)     if (         explicit_namespace is None         and tool_lookup_key is None         and existing_pending is None         and tool_name not in candidates     ):         candidates.append(tool_name)     if existing_pending:         for pending_candidate in pending_keys:             if pending_candidate not in candidates:                 candidates.append(pending_candidate)         if (             pending_namespace is None             and pending_tool_name is not None             and pending_tool_name not in candidates         ):             candidates.append(pending_tool_name)      status: bool | None = None     for candidate in candidates:         status = self._get_approval_status_for_key(candidate, call_id)         if status is not None:             break     return status ``` |