---
url: https://openai.github.io/openai-agents-python/ref/run_internal/approvals/
title: `Approvals`
framework: openai
---

# `Approvals`

Helpers for approval handling within the run loop. Keep only execution-time utilities that
coordinate approval placeholders and normalization; public APIs should stay in run.py or
peer modules.

### append\_approval\_error\_output

```
append_approval_error_output(
    *,
    generated_items: list[RunItem],
    agent: Agent[Any],
    tool_call: Any,
    tool_name: str,
    call_id: str | None,
    message: str,
    tool_origin: ToolOrigin | None = None,
) -> None
```

Emit a synthetic tool output so users see why an approval failed.

Source code in `src/agents/run_internal/approvals.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 ``` | ``` def append_approval_error_output(     *,     generated_items: list[RunItem],     agent: Agent[Any],     tool_call: Any,     tool_name: str,     call_id: str | None,     message: str,     tool_origin: ToolOrigin | None = None, ) -> None:     """Emit a synthetic tool output so users see why an approval failed."""     error_tool_call = _build_function_tool_call_for_approval_error(tool_call, tool_name, call_id)     generated_items.append(         ToolCallOutputItem(             output=message,             raw_item=ItemHelpers.tool_call_output_item(error_tool_call, message),             agent=agent,             tool_origin=tool_origin,         )     ) ``` |

### filter\_tool\_approvals

```
filter_tool_approvals(
    interruptions: Sequence[Any],
) -> list[ToolApprovalItem]
```

Keep only approval items from a mixed interruption payload.

Source code in `src/agents/run_internal/approvals.py`

|  |  |
| --- | --- |
| ``` 46 47 48 ``` | ``` def filter_tool_approvals(interruptions: Sequence[Any]) -> list[ToolApprovalItem]:     """Keep only approval items from a mixed interruption payload."""     return [item for item in interruptions if isinstance(item, ToolApprovalItem)] ``` |

### approvals\_from\_step

```
approvals_from_step(step: Any) -> list[ToolApprovalItem]
```

Return approvals from a step that may or may not contain interruptions.

Source code in `src/agents/run_internal/approvals.py`

|  |  |
| --- | --- |
| ``` 51 52 53 54 55 56 ``` | ``` def approvals_from_step(step: Any) -> list[ToolApprovalItem]:     """Return approvals from a step that may or may not contain interruptions."""     interruptions = getattr(step, "interruptions", None)     if interruptions is None:         return []     return filter_tool_approvals(interruptions) ``` |

### append\_input\_items\_excluding\_approvals

```
append_input_items_excluding_approvals(
    base_input: list[TResponseInputItem],
    items: Sequence[RunItem],
    reasoning_item_id_policy: ReasoningItemIdPolicy
    | None = None,
) -> None
```

Append tool outputs to model input while skipping approval placeholders.

Source code in `src/agents/run_internal/approvals.py`

|  |  |
| --- | --- |
| ``` 59 60 61 62 63 64 65 66 67 68 69 ``` | ``` def append_input_items_excluding_approvals(     base_input: list[TResponseInputItem],     items: Sequence[RunItem],     reasoning_item_id_policy: ReasoningItemIdPolicy | None = None, ) -> None:     """Append tool outputs to model input while skipping approval placeholders."""     for item in items:         converted = run_item_to_input_item(item, reasoning_item_id_policy)         if converted is None:             continue         base_input.append(converted) ``` |