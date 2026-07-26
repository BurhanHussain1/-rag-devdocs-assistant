---
url: https://openai.github.io/openai-agents-python/ref/handoffs/history/
title: `History`
framework: openai
---

# `History`

### set\_conversation\_history\_wrappers

```
set_conversation_history_wrappers(
    *, start: str | None = None, end: str | None = None
) -> None
```

Override the markers that wrap the generated conversation summary.

Pass `None` to leave either side unchanged.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 ``` | ``` def set_conversation_history_wrappers(     *,     start: str | None = None,     end: str | None = None, ) -> None:     """Override the markers that wrap the generated conversation summary.      Pass ``None`` to leave either side unchanged.     """      global _conversation_history_start, _conversation_history_end     if start is not None:         _conversation_history_start = start     if end is not None:         _conversation_history_end = end ``` |

### reset\_conversation\_history\_wrappers

```
reset_conversation_history_wrappers() -> None
```

Restore the default `<CONVERSATION HISTORY>` markers.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 69 70 71 72 73 74 ``` | ``` def reset_conversation_history_wrappers() -> None:     """Restore the default ``<CONVERSATION HISTORY>`` markers."""      global _conversation_history_start, _conversation_history_end     _conversation_history_start = _DEFAULT_CONVERSATION_HISTORY_START     _conversation_history_end = _DEFAULT_CONVERSATION_HISTORY_END ``` |

### get\_conversation\_history\_wrappers

```
get_conversation_history_wrappers() -> tuple[str, str]
```

Return the current start/end markers used for the nested conversation summary.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 77 78 79 80 ``` | ``` def get_conversation_history_wrappers() -> tuple[str, str]:     """Return the current start/end markers used for the nested conversation summary."""      return (_conversation_history_start, _conversation_history_end) ``` |

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