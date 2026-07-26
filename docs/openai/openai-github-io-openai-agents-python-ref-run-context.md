---
url: https://openai.github.io/openai-agents-python/ref/run_context/
title: `Run context`
framework: openai
---

# `Run context`

### RunContextWrapper `dataclass`

Bases: `Generic[TContext]`

This wraps the context object that you passed to `Runner.run()`. It also contains
information about the usage of the agent run so far.

NOTE: Contexts are not passed to the LLM. They're a way to pass dependencies and data to code
you implement, like tool functions, callbacks, hooks, etc.

Source code in `src/agents/run_context.py`

|  |  |
| --- | --- |
| ```  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 ``` | ``` @dataclass(eq=False) class RunContextWrapper(Generic[TContext]):     """This wraps the context object that you passed to `Runner.run()`. It also contains     information about the usage of the agent run so far.      NOTE: Contexts are not passed to the LLM. They're a way to pass dependencies and data to code     you implement, like tool functions, callbacks, hooks, etc.     """      context: TContext     """The context object (or None), passed by you to `Runner.run()`"""      usage: Usage = field(default_factory=Usage)     """The usage of the agent run so far. For streamed responses, the usage will be stale until the     last chunk of the stream is processed.     """      turn_input: list[TResponseInputItem] = field(default_factory=list)     _approvals: dict[str, _ApprovalRecord] = field(default_factory=dict)     tool_input: Any | None = None     """Structured input for the current agent tool run, when available."""      @staticmethod     def _to_str_or_none(value: Any) -> str | None:         if isinstance(value, str):             return value         if value is not None:             try:                 return str(value)             except Exception:                 return None         return None      @staticmethod     def _resolve_tool_name(approval_item: ToolApprovalItem) -> str:         raw = approval_item.raw_item         if approval_item.tool_name:             return approval_item.tool_name         candidate: Any | None         if isinstance(raw, dict):             candidate = raw.get("name") or raw.get("type")         else:             candidate = getattr(raw, "name", None) or getattr(raw, "type", None)         return RunContextWrapper._to_str_or_none(candidate) or "unknown_tool"      @staticmethod     def _resolve_tool_namespace(approval_item: ToolApprovalItem) -> str | None:         raw = approval_item.raw_item         if isinstance(approval_item.tool_namespace, str) and approval_item.tool_namespace:             return approval_item.tool_namespace         if isinstance(raw, dict):             candidate = raw.get("namespace")         else:             candidate = getattr(raw, "namespace", None)         return RunContextWrapper._to_str_or_none(candidate)      @staticmethod     def _resolve_approval_key(approval_item: ToolApprovalItem) -> str:         tool_name = RunContextWrapper._resolve_tool_name(approval_item)         tool_namespace = RunContextWrapper._resolve_tool_namespace(approval_item)         lookup_key = RunContextWrapper._resolve_tool_lookup_key(approval_item)         approval_keys = get_function_tool_approval_keys(             tool_name=tool_name,             tool_namespace=tool_namespace,             tool_lookup_key=lookup_key,             prefer_legacy_same_name_namespace=lookup_key is None,         )         if approval_keys:             return approval_keys[-1]         return tool_qualified_name(tool_name, tool_namespace) or tool_name or "unknown_tool"      @staticmethod     def _resolve_approval_keys(approval_item: ToolApprovalItem) -> tuple[str, ...]:         """Return all approval keys that should mirror this approval record."""         lookup_key = RunContextWrapper._resolve_tool_lookup_key(approval_item)         return get_function_tool_approval_keys(             tool_name=RunContextWrapper._resolve_tool_name(approval_item),             tool_namespace=RunContextWrapper._resolve_tool_namespace(approval_item),             allow_bare_name_alias=getattr(approval_item, "_allow_bare_name_alias", False),             tool_lookup_key=lookup_key,             prefer_legacy_same_name_namespace=lookup_key is None,         )      @staticmethod     def _resolve_tool_lookup_key(approval_item: ToolApprovalItem) -> FunctionToolLookupKey | None:         candidate = getattr(approval_item, "tool_lookup_key", None)         if isinstance(candidate, tuple):             return candidate          raw = approval_item.raw_item         if isinstance(raw, dict):             raw_type = raw.get("type")         else:             raw_type = getattr(raw, "type", None)         if raw_type != "function_call":             return None          tool_name = RunContextWrapper._resolve_tool_name(approval_item)         tool_namespace = RunContextWrapper._resolve_tool_namespace(approval_item)         if is_reserved_synthetic_tool_namespace(tool_name, tool_namespace):             return None         return get_function_tool_lookup_key(tool_name, tool_namespace)      @staticmethod     def _resolve_call_id(approval_item: ToolApprovalItem) -> str | None:         raw = approval_item.raw_item         if isinstance(raw, dict):             provider_data = raw.get("provider_data")             if (                 isinstance(provider_data, dict)                 and provider_data.get("type") == "mcp_approval_request"             ):                 candidate = provider_data.get("id")                 if isinstance(candidate, str):                     return candidate             candidate = raw.get("call_id") or raw.get("id")         else:             provider_data = getattr(raw, "provider_data", None)             if (                 isinstance(provider_data, dict)                 and provider_data.get("type") == "mcp_approval_request"             ):                 candidate = provider_data.get("id")                 if isinstance(candidate, str):                     return candidate             candidate = getattr(raw, "call_id", None) or getattr(raw, "id", None)         return RunContextWrapper._to_str_or_none(candidate)      def _get_or_create_approval_entry(self, tool_name: str) -> _ApprovalRecord:         approval_entry = self._approvals.get(tool_name)         if approval_entry is None:             approval_entry = _ApprovalRecord()             self._approvals[tool_name] = approval_entry         return approval_entry      def is_tool_approved(self, tool_name: str, call_id: str) -> bool | None:         """Return True/False/None for the given tool call."""         return self._get_approval_status_for_key(tool_name, call_id)      def _get_approval_status_for_key(self, approval_key: str, call_id: str) -> bool | None:         """Return True/False/None for a concrete approval key and tool call."""         approval_entry = self._approvals.get(approval_key)         if not approval_entry:             return None          # Check for permanent approval/rejection         if approval_entry.approved is True and approval_entry.rejected is True:             # Approval takes precedence             return True          if approval_entry.approved is True:             return True          if approval_entry.rejected is True:             return False          approved_ids = (             set(approval_entry.approved) if isinstance(approval_entry.approved, list) else set()         )         rejected_ids = (             set(approval_entry.rejected) if isinstance(approval_entry.rejected, list) else set()         )          if call_id in approved_ids:             return True         if call_id in rejected_ids:             return False         # Per-call approvals are scoped to the exact call ID, so other calls require a new decision.         return None      @staticmethod     def _clear_rejection_message(record: _ApprovalRecord, call_id: str | None) -> None:         if call_id is None:             return         record.rejection_messages.pop(call_id, None)      @staticmethod     def _get_rejection_message_for_key(record: _ApprovalRecord, call_id: str) -> str | None:         if record.rejected is True:             if call_id in record.rejection_messages:                 return record.rejection_messages[call_id]             return record.sticky_rejection_message         if isinstance(record.rejected, list) and call_id in record.rejected:             return record.rejection_messages.get(call_id)         return None      @staticmethod     def _restore_approval_value(value: Any) -> bool | list[str]:         if isinstance(value, bool):             return value         if isinstance(value, list):             return [item for item in value if isinstance(item, str)]         return []      def get_rejection_message(         self,         tool_name: str,         call_id: str,         *,         tool_namespace: str | None = None,         existing_pending: ToolApprovalItem | None = None,         tool_lookup_key: FunctionToolLookupKey | None = None,     ) -> str | None:         """Return a stored rejection message for a tool call if one exists."""         candidates: list[str] = []         explicit_namespace = (             tool_namespace if isinstance(tool_namespace, str) and tool_namespace else None         )         pending_namespace = (             self._resolve_tool_namespace(existing_pending) if existing_pending is not None else None         )         pending_key = self._resolve_approval_key(existing_pending) if existing_pending else None         pending_tool_name = self._resolve_tool_name(existing_pending) if existing_pending else None         pending_keys = (             list(self._resolve_approval_keys(existing_pending))             if existing_pending is not None             else []         )          if existing_pending and pending_key is not None:             candidates.append(pending_key)         explicit_keys = (             list(                 get_function_tool_approval_keys(                     tool_name=tool_name,                     tool_namespace=explicit_namespace,                     tool_lookup_key=tool_lookup_key,                     include_legacy_deferred_key=True,                 )             )             if explicit_namespace is not None or tool_lookup_key is not None             else []         )         for explicit_key in explicit_keys:             if explicit_key not in candidates:                 candidates.append(explicit_key)         if not explicit_keys and pending_namespace and pending_key is not None:             if pending_key not in candidates:                 candidates.append(pending_key)         if (             explicit_namespace is None             and tool_lookup_key is None             and existing_pending is None             and tool_name not in candidates         ):             candidates.append(tool_name)         if existing_pending:             for pending_candidate in pending_keys:                 if pending_candidate not in candidates:                     candidates.append(pending_candidate)             if (                 pending_namespace is None                 and pending_tool_name is not None                 and pending_tool_name not in candidates             ):                 candidates.append(pending_tool_name)          for candidate in candidates:             approval_entry = self._approvals.get(candidate)             if not approval_entry:                 continue             message = self._get_rejection_message_for_key(approval_entry, call_id)             if message is not None:                 return message         return None      def _apply_approval_decision(         self,         approval_item: ToolApprovalItem,         *,         always: bool,         approve: bool,         rejection_message: str | None = None,     ) -> None:         """Record an approval or rejection decision."""         approval_keys = self._resolve_approval_keys(approval_item) or ("unknown_tool",)         exact_approval_key = self._resolve_approval_key(approval_item)         call_id = self._resolve_call_id(approval_item)         decision_keys = (exact_approval_key,) if always or call_id is None else approval_keys          for approval_key in decision_keys:             approval_entry = self._get_or_create_approval_entry(approval_key)             if always or call_id is None:                 approval_entry.approved = approve                 approval_entry.rejected = [] if approve else True                 if not approve:                     approval_entry.approved = False                     if rejection_message is not None and call_id is not None:                         approval_entry.rejection_messages[call_id] = rejection_message                     elif call_id is not None:                         self._clear_rejection_message(approval_entry, call_id)                     approval_entry.sticky_rejection_message = rejection_message                 else:                     approval_entry.rejection_messages.clear()                     approval_entry.sticky_rejection_message = None                 continue              opposite = approval_entry.rejected if approve else approval_entry.approved             if isinstance(opposite, list) and call_id in opposite:                 opposite.remove(call_id)              target = approval_entry.approved if approve else approval_entry.rejected             if isinstance(target, list) and call_id not in target:                 target.append(call_id)             if approve:                 self._clear_rejection_message(approval_entry, call_id)             elif call_id is not None:                 if rejection_message is not None:                     approval_entry.rejection_messages[call_id] = rejection_message                 else:                     self._clear_rejection_message(approval_entry, call_id)      def approve_tool(self, approval_item: ToolApprovalItem, always_approve: bool = False) -> None:         """Approve a tool call, optionally for all future calls."""         self._apply_approval_decision(             approval_item,             always=always_approve,             approve=True,         )      def reject_tool(         self,         approval_item: ToolApprovalItem,         always_reject: bool = False,         rejection_message: str | None = None,     ) -> None:         """Reject a tool call, optionally for all future calls."""         self._apply_approval_decision(             approval_item,             always=always_reject,             approve=False,             rejection_message=rejection_message,         )      def get_approval_status(         self,         tool_name: str,         call_id: str,         *,         tool_namespace: str | None = None,         existing_pending: ToolApprovalItem | None = None,         tool_lookup_key: FunctionToolLookupKey | None = None,     ) -> bool | None:         """Return approval status, retrying with pending item's tool name if necessary."""         candidates: list[str] = []         explicit_namespace = (             tool_namespace if isinstance(tool_namespace, str) and tool_namespace else None         )         pending_namespace = (             self._resolve_tool_namespace(existing_pending) if existing_pending is not None else None         )         pending_key = self._resolve_approval_key(existing_pending) if existing_pending else None         pending_tool_name = self._resolve_tool_name(existing_pending) if existing_pending else None         pending_keys = (             list(self._resolve_approval_keys(existing_pending))             if existing_pending is not None             else []         )          if existing_pending and pending_key is not None:             candidates.append(pending_key)         explicit_keys = (             list(                 get_function_tool_approval_keys(                     tool_name=tool_name,                     tool_namespace=explicit_namespace,                     tool_lookup_key=tool_lookup_key,                     include_legacy_deferred_key=True,                 )             )             if explicit_namespace is not None or tool_lookup_key is not None             else []         )         for explicit_key in explicit_keys:             if explicit_key not in candidates:                 candidates.append(explicit_key)         if not explicit_keys and pending_namespace and pending_key is not None:             if pending_key not in candidates:                 candidates.append(pending_key)         if (             explicit_namespace is None             and tool_lookup_key is None             and existing_pending is None             and tool_name not in candidates         ):             candidates.append(tool_name)         if existing_pending:             for pending_candidate in pending_keys:                 if pending_candidate not in candidates:                     candidates.append(pending_candidate)             if (                 pending_namespace is None                 and pending_tool_name is not None                 and pending_tool_name not in candidates             ):                 candidates.append(pending_tool_name)          status: bool | None = None         for candidate in candidates:             status = self._get_approval_status_for_key(candidate, call_id)             if status is not None:                 break         return status      def _rebuild_approvals(self, approvals: Any) -> None:         """Restore approvals from serialized state."""         self._approvals = {}         if not isinstance(approvals, Mapping):             return         for tool_name, record_dict in approvals.items():             if not isinstance(tool_name, str) or not isinstance(record_dict, dict):                 continue             record = _ApprovalRecord()             record.approved = self._restore_approval_value(record_dict.get("approved", []))             record.rejected = self._restore_approval_value(record_dict.get("rejected", []))             rejection_messages = record_dict.get("rejection_messages", {})             if isinstance(rejection_messages, dict):                 record.rejection_messages = {                     str(call_id): message                     for call_id, message in rejection_messages.items()                     if isinstance(message, str)                 }             sticky_rejection_message = record_dict.get("sticky_rejection_message")             if isinstance(sticky_rejection_message, str):                 record.sticky_rejection_message = sticky_rejection_message             self._approvals[tool_name] = record      def _fork_with_tool_input(self, tool_input: Any) -> RunContextWrapper[TContext]:         """Create a child context that shares approvals and usage with tool input set."""         fork = RunContextWrapper(context=self.context)         fork.usage = self.usage         fork._approvals = self._approvals         fork.turn_input = self.turn_input         fork.tool_input = tool_input         return fork      def _fork_without_tool_input(self) -> RunContextWrapper[TContext]:         """Create a child context that shares approvals and usage without tool input."""         fork = RunContextWrapper(context=self.context)         fork.usage = self.usage         fork._approvals = self._approvals         fork.turn_input = self.turn_input         return fork ``` |

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

### AgentHookContext `dataclass`

Bases: `RunContextWrapper[TContext]`

Context passed to agent hooks (on\_start, on\_end).

Source code in `src/agents/run_context.py`

|  |  |
| --- | --- |
| ``` 488 489 490 ``` | ``` @dataclass(eq=False) class AgentHookContext(RunContextWrapper[TContext]):     """Context passed to agent hooks (on_start, on_end).""" ``` |

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