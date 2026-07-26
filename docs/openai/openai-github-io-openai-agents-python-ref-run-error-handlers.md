---
url: https://openai.github.io/openai-agents-python/ref/run_error_handlers/
title: `Run Error Handlers`
framework: openai
---

# `Run Error Handlers`

### RunErrorData `dataclass`

Snapshot of run data passed to error handlers.

Source code in `src/agents/run_error_handlers.py`

|  |  |
| --- | --- |
| ``` 16 17 18 19 20 21 22 23 24 25 ``` | ``` @dataclass class RunErrorData:     """Snapshot of run data passed to error handlers."""      input: str | list[TResponseInputItem]     new_items: list[RunItem]     history: list[TResponseInputItem]     output: list[TResponseInputItem]     raw_responses: list[ModelResponse]     last_agent: Agent[Any] ``` |

### RunErrorHandlerResult `dataclass`

Result returned by an error handler.

Source code in `src/agents/run_error_handlers.py`

|  |  |
| --- | --- |
| ``` 35 36 37 38 39 40 ``` | ``` @dataclass class RunErrorHandlerResult:     """Result returned by an error handler."""      final_output: Any     include_in_history: bool = True ``` |

### RunErrorHandlers

Bases: `TypedDict`, `Generic[TContext]`

Error handlers keyed by error kind.

Source code in `src/agents/run_error_handlers.py`

|  |  |
| --- | --- |
| ``` 50 51 52 53 54 55 ``` | ``` class RunErrorHandlers(TypedDict, Generic[TContext], total=False):     """Error handlers keyed by error kind."""      max_turns: RunErrorHandler[TContext]     model_refusal: RunErrorHandler[TContext]     invalid_final_output: RunErrorHandler[TContext] ``` |