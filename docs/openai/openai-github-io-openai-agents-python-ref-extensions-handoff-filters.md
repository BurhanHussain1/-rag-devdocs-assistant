---
url: https://openai.github.io/openai-agents-python/ref/extensions/handoff_filters/
title: `Handoff filters`
framework: openai
---

# `Handoff filters`

Contains common handoff input filters, for convenience.

### default\_handoff\_history\_mapper

```
default_handoff_history_mapper(
    transcript: list[TResponseInputItem],
) -> list[TResponseInputItem]
```

Return a single assistant message summarizing the transcript.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 311 312 313 314 315 316 317 ``` | ``` def default_handoff_history_mapper(     transcript: list[TResponseInputItem], ) -> list[TResponseInputItem]:     """Return a single assistant message summarizing the transcript."""      summary_message = _build_summary_message(transcript)     return [summary_message] ``` |

### nest\_handoff\_history

```
nest_handoff_history(
    handoff_input_data: HandoffInputData,
    *,
    history_mapper: HandoffHistoryMapper | None = None,
) -> HandoffInputData
```

Summarize the previous transcript for the next agent.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 83 84 85 86 87 88 89 90 91 92 93 94 ``` | ``` def nest_handoff_history(     handoff_input_data: HandoffInputData,     *,     history_mapper: HandoffHistoryMapper | None = None, ) -> HandoffInputData:     """Summarize the previous transcript for the next agent."""      nested, _ = _nest_handoff_history_with_provenance(         handoff_input_data,         history_mapper=history_mapper,     )     return nested ``` |

### remove\_all\_tools

```
remove_all_tools(
    handoff_input_data: HandoffInputData,
) -> HandoffInputData
```

Filters out all tool items: file search, web search and function calls+output.

Source code in `src/agents/extensions/handoff_filters.py`

|  |  |
| --- | --- |
| ``` 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 ``` | ``` def remove_all_tools(handoff_input_data: HandoffInputData) -> HandoffInputData:     """Filters out all tool items: file search, web search and function calls+output."""      history = handoff_input_data.input_history     new_items = handoff_input_data.new_items      filtered_history = (         _remove_tool_types_from_input(history) if isinstance(history, tuple) else history     )     filtered_pre_handoff_items = _remove_tools_from_items(handoff_input_data.pre_handoff_items)     filtered_new_items = _remove_tools_from_items(new_items)     # Preserve and filter input_items so chained filters (e.g. after     # nest_handoff_history) don't drop or re-introduce tool items.     existing_input_items = handoff_input_data.input_items     filtered_input_items = (         _remove_tools_from_items(existing_input_items) if existing_input_items is not None else None     )      return handoff_input_data.clone(         input_history=filtered_history,         pre_handoff_items=filtered_pre_handoff_items,         new_items=filtered_new_items,         input_items=filtered_input_items,     ) ``` |