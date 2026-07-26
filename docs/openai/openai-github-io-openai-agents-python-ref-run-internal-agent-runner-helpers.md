---
url: https://openai.github.io/openai-agents-python/ref/run_internal/agent_runner_helpers/
title: `Agent Runner Helpers`
framework: openai
---

# `Agent Runner Helpers`

Internal helpers for AgentRunner.run.

### snapshot\_usage

```
snapshot_usage(usage: Usage) -> Usage
```

Create a usage snapshot for computing invocation-local deltas.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 ``` | ``` def snapshot_usage(usage: Usage) -> Usage:     """Create a usage snapshot for computing invocation-local deltas."""     return Usage(         requests=usage.requests,         input_tokens=usage.input_tokens,         output_tokens=usage.output_tokens,         total_tokens=usage.total_tokens,         input_tokens_details=_make_input_tokens_details(             cached_tokens=_cached_tokens(usage.input_tokens_details),             cache_write_tokens=_cache_write_tokens(usage.input_tokens_details),         ),         output_tokens_details=OutputTokensDetails(             reasoning_tokens=(                 usage.output_tokens_details.reasoning_tokens                 if usage.output_tokens_details and usage.output_tokens_details.reasoning_tokens                 else 0             )         ),     ) ``` |

### usage\_delta

```
usage_delta(start: Usage, end: Usage) -> Usage
```

Return the aggregate usage added between two snapshots.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ```  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 ``` | ``` def usage_delta(start: Usage, end: Usage) -> Usage:     """Return the aggregate usage added between two snapshots."""     return Usage(         requests=end.requests - start.requests,         input_tokens=end.input_tokens - start.input_tokens,         output_tokens=end.output_tokens - start.output_tokens,         total_tokens=end.total_tokens - start.total_tokens,         input_tokens_details=_make_input_tokens_details(             cached_tokens=(                 (end.input_tokens_details.cached_tokens or 0)                 - (start.input_tokens_details.cached_tokens or 0)             ),             cache_write_tokens=(                 _cache_write_tokens(end.input_tokens_details)                 - _cache_write_tokens(start.input_tokens_details)             ),         ),         output_tokens_details=OutputTokensDetails(             reasoning_tokens=(                 (end.output_tokens_details.reasoning_tokens or 0)                 - (start.output_tokens_details.reasoning_tokens or 0)             )         ),     ) ``` |

### attach\_usage\_to\_span

```
attach_usage_to_span(
    span: Span[Any] | None, usage: Usage
) -> None
```

Attach aggregate token usage to a span export metadata bag.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 ``` | ``` def attach_usage_to_span(     span: Span[Any] | None,     usage: Usage, ) -> None:     """Attach aggregate token usage to a span export metadata bag."""     cached_tokens = (         usage.input_tokens_details.cached_tokens         if usage.input_tokens_details and usage.input_tokens_details.cached_tokens         else 0     )     cache_write_tokens = _cache_write_tokens(usage.input_tokens_details)     reasoning_tokens = (         usage.output_tokens_details.reasoning_tokens         if usage.output_tokens_details and usage.output_tokens_details.reasoning_tokens         else 0     )     if span is None or (         usage.requests == 0         and usage.input_tokens == 0         and usage.output_tokens == 0         and usage.total_tokens == 0         and cached_tokens == 0         and cache_write_tokens == 0         and reasoning_tokens == 0     ):         return      if span.span_data.type == "turn":         span.span_data.usage = turn_usage_to_span_data(usage)         return      if span.span_data.type == "task":         span.span_data.usage = task_usage_to_span_data(usage)         return      metadata = dict(getattr(span.span_data, "metadata", None) or {})     metadata["usage"] = total_usage_to_span_metadata(usage)     span.span_data.metadata = metadata ``` |

### should\_cancel\_parallel\_model\_task\_on\_input\_guardrail\_trip

```
should_cancel_parallel_model_task_on_input_guardrail_trip() -> (
    bool
)
```

Return whether an in-flight model task should be cancelled on guardrail trip.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 ``` | ``` def should_cancel_parallel_model_task_on_input_guardrail_trip() -> bool:     """Return whether an in-flight model task should be cancelled on guardrail trip."""     try:         from temporalio import (             workflow as temporal_workflow,  # type: ignore[import-not-found,unused-ignore]         )     except Exception:         return True      try:         if not temporal_workflow.in_workflow():             return True         # Preserve replay compatibility for histories created before cancellation.         return bool(temporal_workflow.patched(_PARALLEL_INPUT_GUARDRAIL_CANCEL_PATCH_ID))     except Exception:         return True ``` |

### apply\_resumed\_conversation\_settings

```
apply_resumed_conversation_settings(
    *,
    run_state: RunState[TContext],
    conversation_id: str | None,
    previous_response_id: str | None,
    auto_previous_response_id: bool,
) -> tuple[str | None, str | None, bool]
```

Apply RunState conversation identifiers and return the resolved values.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 ``` | ``` def apply_resumed_conversation_settings(     *,     run_state: RunState[TContext],     conversation_id: str | None,     previous_response_id: str | None,     auto_previous_response_id: bool, ) -> tuple[str | None, str | None, bool]:     """Apply RunState conversation identifiers and return the resolved values."""     conversation_id = conversation_id or run_state._conversation_id     previous_response_id = previous_response_id or run_state._previous_response_id     if auto_previous_response_id is False and run_state._auto_previous_response_id:         auto_previous_response_id = True     run_state._conversation_id = conversation_id     run_state._previous_response_id = previous_response_id     run_state._auto_previous_response_id = auto_previous_response_id     return conversation_id, previous_response_id, auto_previous_response_id ``` |

### get\_unsent\_tool\_call\_ids\_for\_interrupted\_state

```
get_unsent_tool_call_ids_for_interrupted_state(
    run_state: RunState[Any] | None,
) -> set[str]
```

Return tool call IDs whose local outputs belong to the current interruption.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 ``` | ``` def get_unsent_tool_call_ids_for_interrupted_state(run_state: RunState[Any] | None) -> set[str]:     """Return tool call IDs whose local outputs belong to the current interruption."""     if run_state is None or not isinstance(run_state._current_step, NextStepInterruption):         return set()      processed_response = run_state._last_processed_response     if processed_response is None:         return set()      tool_call_ids: set[str] = set()     tool_run_groups = (         processed_response.handoffs,         processed_response.functions,         processed_response.computer_actions,         processed_response.custom_tool_calls,         processed_response.local_shell_calls,         processed_response.shell_calls,         processed_response.apply_patch_calls,     )     for tool_runs in tool_run_groups:         for tool_run in tool_runs:             call_id = _extract_tool_call_id(getattr(tool_run, "tool_call", None))             if call_id is not None:                 tool_call_ids.add(call_id)     return tool_call_ids ``` |

### resolve\_trace\_settings

```
resolve_trace_settings(
    *,
    run_state: RunState[TContext] | None,
    run_config: RunConfig,
) -> tuple[
    str,
    str | None,
    str | None,
    dict[str, Any] | None,
    TracingConfig | None,
]
```

Resolve tracing settings, preferring explicit run\_config overrides.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 ``` | ``` def resolve_trace_settings(     *,     run_state: RunState[TContext] | None,     run_config: RunConfig, ) -> tuple[str, str | None, str | None, dict[str, Any] | None, TracingConfig | None]:     """Resolve tracing settings, preferring explicit run_config overrides."""     trace_state: TraceState | None = run_state._trace_state if run_state is not None else None     default_workflow_name = RunConfig().workflow_name     workflow_name = run_config.workflow_name      trace_id: str | None = run_config.trace_id     group_id: str | None = run_config.group_id     metadata: dict[str, Any] | None = run_config.trace_metadata     tracing: TracingConfig | None = run_config.tracing      if trace_state:         if workflow_name == default_workflow_name and trace_state.workflow_name:             workflow_name = trace_state.workflow_name         if trace_id is None:             trace_id = trace_state.trace_id         if group_id is None:             group_id = trace_state.group_id         if metadata is None and trace_state.metadata is not None:             metadata = dict(trace_state.metadata)      metadata = add_openai_harness_id_to_metadata(         metadata,         model_provider=run_config.model_provider,     )      return workflow_name, trace_id, group_id, metadata, tracing ``` |

### resolve\_resumed\_context

```
resolve_resumed_context(
    *,
    run_state: RunState[TContext],
    context: RunContextWrapper[TContext] | TContext | None,
) -> RunContextWrapper[TContext]
```

Return the context wrapper for a resumed run, overriding when provided.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 ``` | ``` def resolve_resumed_context(     *,     run_state: RunState[TContext],     context: RunContextWrapper[TContext] | TContext | None, ) -> RunContextWrapper[TContext]:     """Return the context wrapper for a resumed run, overriding when provided."""     if context is not None:         context_wrapper = ensure_context_wrapper(context)         set_agent_tool_state_scope(context_wrapper, run_state._agent_tool_state_scope_id)         run_state._context = context_wrapper         return context_wrapper     if run_state._context is None:         run_state._context = ensure_context_wrapper(context)     set_agent_tool_state_scope(run_state._context, run_state._agent_tool_state_scope_id)     return run_state._context ``` |

### ensure\_context\_wrapper

```
ensure_context_wrapper(
    context: RunContextWrapper[TContext] | TContext | None,
) -> RunContextWrapper[TContext]
```

Normalize a context value into a RunContextWrapper.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 297 298 299 300 301 302 303 ``` | ``` def ensure_context_wrapper(     context: RunContextWrapper[TContext] | TContext | None, ) -> RunContextWrapper[TContext]:     """Normalize a context value into a RunContextWrapper."""     if isinstance(context, RunContextWrapper):         return context     return RunContextWrapper(context=cast(TContext, context)) ``` |

### describe\_run\_state\_step

```
describe_run_state_step(
    step: object | None,
) -> str | int | None
```

Return a debug-friendly label for the current run state step.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 306 307 308 309 310 311 312 313 314 315 316 317 318 ``` | ``` def describe_run_state_step(step: object | None) -> str | int | None:     """Return a debug-friendly label for the current run state step."""     if step is None:         return None     if isinstance(step, NextStepInterruption):         return "next_step_interruption"     if isinstance(step, NextStepHandoff):         return "next_step_handoff"     if isinstance(step, NextStepFinalOutput):         return "next_step_final_output"     if isinstance(step, NextStepRunAgain):         return "next_step_run_again"     return type(step).__name__ ``` |

### build\_generated\_items\_details

```
build_generated_items_details(
    items: list[RunItem], *, include_tool_output: bool
) -> list[dict[str, object]]
```

Return debug-friendly metadata for generated items.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 ``` | ``` def build_generated_items_details(     items: list[RunItem],     *,     include_tool_output: bool, ) -> list[dict[str, object]]:     """Return debug-friendly metadata for generated items."""     details: list[dict[str, object]] = []     for idx, item in enumerate(items):         item_info: dict[str, object] = {"index": idx, "type": item.type}         if hasattr(item, "raw_item") and isinstance(item.raw_item, dict):             item_info["raw_type"] = item.raw_item.get("type")             item_info["name"] = item.raw_item.get("name")             item_info["call_id"] = item.raw_item.get("call_id")             if item.type == "tool_call_output_item" and include_tool_output:                 output_str = str(item.raw_item.get("output", ""))[:100]                 item_info["output"] = output_str         details.append(item_info)     return details ``` |

### build\_resumed\_stream\_debug\_extra

```
build_resumed_stream_debug_extra(
    run_state: RunState[TContext],
    *,
    include_tool_output: bool,
) -> dict[str, object]
```

Build the logger extra payload when resuming a streamed run.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 ``` | ``` def build_resumed_stream_debug_extra(     run_state: RunState[TContext],     *,     include_tool_output: bool, ) -> dict[str, object]:     """Build the logger extra payload when resuming a streamed run."""     return {         "current_turn": run_state._current_turn,         "current_agent": run_state._current_agent.name if run_state._current_agent else None,         "generated_items_count": len(run_state._generated_items),         "generated_items_types": [item.type for item in run_state._generated_items],         "generated_items_details": build_generated_items_details(             run_state._generated_items,             include_tool_output=include_tool_output,         ),         "current_step_type": describe_run_state_step(run_state._current_step),     } ``` |

### finalize\_conversation\_tracking

```
finalize_conversation_tracking(
    result: RunResult,
    *,
    server_conversation_tracker: OpenAIServerConversationTracker
    | None,
    run_state: RunState | None,
) -> RunResult
```

Propagate conversation metadata to the result and run state.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 ``` | ``` def finalize_conversation_tracking(     result: RunResult,     *,     server_conversation_tracker: OpenAIServerConversationTracker | None,     run_state: RunState | None, ) -> RunResult:     """Propagate conversation metadata to the result and run state."""     if server_conversation_tracker is None:         return result     result._conversation_id = server_conversation_tracker.conversation_id     result._previous_response_id = server_conversation_tracker.previous_response_id     result._auto_previous_response_id = server_conversation_tracker.auto_previous_response_id     if run_state is not None:         run_state._conversation_id = server_conversation_tracker.conversation_id         run_state._previous_response_id = server_conversation_tracker.previous_response_id         run_state._auto_previous_response_id = server_conversation_tracker.auto_previous_response_id     return result ``` |

### build\_interruption\_result

```
build_interruption_result(
    *,
    result_input: str | list[TResponseInputItem],
    session_items: list[RunItem],
    model_responses: list[ModelResponse],
    current_agent: Agent[Any],
    input_guardrail_results: list[InputGuardrailResult],
    tool_input_guardrail_results: list[
        ToolInputGuardrailResult
    ],
    tool_output_guardrail_results: list[
        ToolOutputGuardrailResult
    ],
    context_wrapper: RunContextWrapper[TContext],
    interruptions: list[ToolApprovalItem],
    processed_response: ProcessedResponse | None,
    tool_use_tracker: AgentToolUseTracker,
    max_turns: int | None,
    current_turn: int,
    generated_items: list[RunItem],
    run_state: RunState | None,
    original_input: str | list[TResponseInputItem],
) -> RunResult
```

Create a RunResult for an interruption path.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 ``` | ``` def build_interruption_result(     *,     result_input: str | list[TResponseInputItem],     session_items: list[RunItem],     model_responses: list[ModelResponse],     current_agent: Agent[Any],     input_guardrail_results: list[InputGuardrailResult],     tool_input_guardrail_results: list[ToolInputGuardrailResult],     tool_output_guardrail_results: list[ToolOutputGuardrailResult],     context_wrapper: RunContextWrapper[TContext],     interruptions: list[ToolApprovalItem],     processed_response: ProcessedResponse | None,     tool_use_tracker: AgentToolUseTracker,     max_turns: int | None,     current_turn: int,     generated_items: list[RunItem],     run_state: RunState | None,     original_input: str | list[TResponseInputItem], ) -> RunResult:     """Create a RunResult for an interruption path."""     identity_root_agent = (         run_state._starting_agent         if run_state is not None and run_state._starting_agent is not None         else current_agent     )     result = RunResult(         input=result_input,         new_items=session_items,         raw_responses=model_responses,         final_output=None,         _last_agent=current_agent,         input_guardrail_results=input_guardrail_results,         output_guardrail_results=[],         tool_input_guardrail_results=tool_input_guardrail_results,         tool_output_guardrail_results=tool_output_guardrail_results,         context_wrapper=context_wrapper,         interruptions=interruptions,         _last_processed_response=processed_response,         _tool_use_tracker_snapshot=serialize_tool_use_tracker(             tool_use_tracker,             starting_agent=identity_root_agent,         ),         max_turns=max_turns,     )     result._current_turn = current_turn     result._model_input_items = list(generated_items)     result._replay_from_model_input_items = list(generated_items) != list(session_items)     if run_state is not None:         result._current_turn_persisted_item_count = run_state._current_turn_persisted_item_count         result._trace_state = run_state._trace_state     result._original_input = copy_input_items(original_input)     return result ``` |

### append\_model\_response\_if\_new

```
append_model_response_if_new(
    model_responses: list[ModelResponse],
    response: ModelResponse,
) -> None
```

Append a model response only when it is not already in the list tail.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 433 434 435 436 437 438 439 ``` | ``` def append_model_response_if_new(     model_responses: list[ModelResponse],     response: ModelResponse, ) -> None:     """Append a model response only when it is not already in the list tail."""     if not model_responses or model_responses[-1] is not response:         model_responses.append(response) ``` |

### input\_guardrails\_triggered

```
input_guardrails_triggered(
    results: list[InputGuardrailResult],
) -> bool
```

Return True when any guardrail tripwire has fired.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 442 443 444 ``` | ``` def input_guardrails_triggered(results: list[InputGuardrailResult]) -> bool:     """Return True when any guardrail tripwire has fired."""     return any(result.output.tripwire_triggered for result in results) ``` |

### update\_run\_state\_for\_interruption

```
update_run_state_for_interruption(
    *,
    run_state: RunState[TContext],
    model_responses: list[ModelResponse],
    processed_response: ProcessedResponse | None,
    generated_items: list[RunItem],
    session_items: list[RunItem] | None,
    current_turn: int,
    next_step: NextStepInterruption,
) -> None
```

Sync run-state fields needed to resume after an interruption.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 ``` | ``` def update_run_state_for_interruption(     *,     run_state: RunState[TContext],     model_responses: list[ModelResponse],     processed_response: ProcessedResponse | None,     generated_items: list[RunItem],     session_items: list[RunItem] | None,     current_turn: int,     next_step: NextStepInterruption, ) -> None:     """Sync run-state fields needed to resume after an interruption."""     run_state._model_responses = model_responses     run_state._last_processed_response = processed_response     run_state._generated_items = generated_items     if session_items is not None:         run_state._session_items = list(session_items)     run_state._current_step = next_step     run_state._current_turn = current_turn ``` |

### save\_turn\_items\_if\_needed `async`

```
save_turn_items_if_needed(
    *,
    session: Session | None,
    run_state: RunState | None,
    session_persistence_enabled: bool,
    input_guardrail_results: list[InputGuardrailResult],
    items: list[RunItem],
    response_id: str | None,
    store: bool | None = None,
) -> None
```

Persist turn items when persistence is enabled and guardrails allow it.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 ``` | ``` async def save_turn_items_if_needed(     *,     session: Session | None,     run_state: RunState | None,     session_persistence_enabled: bool,     input_guardrail_results: list[InputGuardrailResult],     items: list[RunItem],     response_id: str | None,     store: bool | None = None, ) -> None:     """Persist turn items when persistence is enabled and guardrails allow it."""     if not session_persistence_enabled:         return     if input_guardrails_triggered(input_guardrail_results):         return     if run_state is not None and run_state._current_turn_persisted_item_count > 0:         return     await save_result_to_session(         session,         [],         list(items),         run_state,         response_id=response_id,         store=store,     ) ``` |

### resolve\_processed\_response

```
resolve_processed_response(
    *,
    run_state: RunState | None,
    processed_response: ProcessedResponse | None,
) -> ProcessedResponse | None
```

Return a processed response, falling back to the run state when missing.

Source code in `src/agents/run_internal/agent_runner_helpers.py`

|  |  |
| --- | --- |
| ``` 494 495 496 497 498 499 500 501 502 ``` | ``` def resolve_processed_response(     *,     run_state: RunState | None,     processed_response: ProcessedResponse | None, ) -> ProcessedResponse | None:     """Return a processed response, falling back to the run state when missing."""     if processed_response is None and run_state is not None:         return run_state._last_processed_response     return processed_response ``` |