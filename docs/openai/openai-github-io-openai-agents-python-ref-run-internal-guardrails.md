---
url: https://openai.github.io/openai-agents-python/ref/run_internal/guardrails/
title: `Guardrails`
framework: openai
---

# `Guardrails`

### run\_input\_guardrails\_with\_queue `async`

```
run_input_guardrails_with_queue(
    agent: Agent[Any],
    guardrails: list[InputGuardrail[TContext]],
    input: str | list[TResponseInputItem],
    context: RunContextWrapper[TContext],
    streamed_result: RunResultStreaming,
    parent_span: Span[Any] | None,
) -> None
```

Run guardrails concurrently and stream results into the queue.

Source code in `src/agents/run_internal/guardrails.py`

|  |  |
| --- | --- |
| ```  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 ``` | ``` async def run_input_guardrails_with_queue(     agent: Agent[Any],     guardrails: list[InputGuardrail[TContext]],     input: str | list[TResponseInputItem],     context: RunContextWrapper[TContext],     streamed_result: RunResultStreaming,     parent_span: Span[Any] | None, ) -> None:     """Run guardrails concurrently and stream results into the queue."""     queue = streamed_result._input_guardrail_queue      guardrail_tasks = [         asyncio.create_task(run_single_input_guardrail(agent, guardrail, input, context))         for guardrail in guardrails     ]     guardrail_results = []     try:         for done in asyncio.as_completed(guardrail_tasks):             result = await done             guardrail_results.append(result)             if result.output.tripwire_triggered:                 streamed_result.input_guardrail_results = (                     streamed_result.input_guardrail_results + guardrail_results                 )                 guardrail_results = []                 streamed_result._triggered_input_guardrail_result = result                 queue.put_nowait(result)                 for t in guardrail_tasks:                     t.cancel()                 await asyncio.gather(*guardrail_tasks, return_exceptions=True)                 span_error = SpanError(                     message="Guardrail tripwire triggered",                     data={                         "guardrail": result.guardrail.get_name(),                         "type": "input_guardrail",                     },                 )                 if parent_span is not None:                     _error_tracing.attach_error_to_span(parent_span, span_error)                 else:                     # Early first-turn streamed guardrails can run before the agent span exists.                     _error_tracing.attach_error_to_current_span(span_error)                 break             queue.put_nowait(result)     except BaseException:         for t in guardrail_tasks:             if not t.done():                 t.cancel()         await asyncio.gather(*guardrail_tasks, return_exceptions=True)         raise      streamed_result.input_guardrail_results = (         streamed_result.input_guardrail_results + guardrail_results     ) ``` |

### run\_input\_guardrails `async`

```
run_input_guardrails(
    agent: Agent[Any],
    guardrails: list[InputGuardrail[TContext]],
    input: str | list[TResponseInputItem],
    context: RunContextWrapper[TContext],
) -> list[InputGuardrailResult]
```

Run input guardrails concurrently and raise on tripwires.

Source code in `src/agents/run_internal/guardrails.py`

|  |  |
| --- | --- |
| ``` 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 ``` | ``` async def run_input_guardrails(     agent: Agent[Any],     guardrails: list[InputGuardrail[TContext]],     input: str | list[TResponseInputItem],     context: RunContextWrapper[TContext], ) -> list[InputGuardrailResult]:     """Run input guardrails concurrently and raise on tripwires."""     if not guardrails:         return []      guardrail_tasks = [         asyncio.create_task(run_single_input_guardrail(agent, guardrail, input, context))         for guardrail in guardrails     ]      guardrail_results: list[InputGuardrailResult] = []      try:         for done in asyncio.as_completed(guardrail_tasks):             result = await done             if result.output.tripwire_triggered:                 for t in guardrail_tasks:                     t.cancel()                 await asyncio.gather(*guardrail_tasks, return_exceptions=True)                 _error_tracing.attach_error_to_current_span(                     SpanError(                         message="Guardrail tripwire triggered",                         data={"guardrail": result.guardrail.get_name()},                     )                 )                 raise InputGuardrailTripwireTriggered(result)             guardrail_results.append(result)     except BaseException:         # On any error (including a guardrail raising or the caller being cancelled),         # cancel and await siblings so they don't leak past this function's return.         for t in guardrail_tasks:             if not t.done():                 t.cancel()         await asyncio.gather(*guardrail_tasks, return_exceptions=True)         raise      return guardrail_results ``` |

### run\_output\_guardrails `async`

```
run_output_guardrails(
    guardrails: list[OutputGuardrail[TContext]],
    agent: Agent[TContext],
    agent_output: Any,
    context: RunContextWrapper[TContext],
) -> list[OutputGuardrailResult]
```

Run output guardrails in parallel and raise on tripwires.

Source code in `src/agents/run_internal/guardrails.py`

|  |  |
| --- | --- |
| ``` 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 ``` | ``` async def run_output_guardrails(     guardrails: list[OutputGuardrail[TContext]],     agent: Agent[TContext],     agent_output: Any,     context: RunContextWrapper[TContext], ) -> list[OutputGuardrailResult]:     """Run output guardrails in parallel and raise on tripwires."""     if not guardrails:         return []      guardrail_tasks = [         asyncio.create_task(run_single_output_guardrail(guardrail, agent, agent_output, context))         for guardrail in guardrails     ]      guardrail_results: list[OutputGuardrailResult] = []      try:         for done in asyncio.as_completed(guardrail_tasks):             result = await done             if result.output.tripwire_triggered:                 for t in guardrail_tasks:                     t.cancel()                 await asyncio.gather(*guardrail_tasks, return_exceptions=True)                 _error_tracing.attach_error_to_current_span(                     SpanError(                         message="Guardrail tripwire triggered",                         data={"guardrail": result.guardrail.get_name()},                     )                 )                 raise OutputGuardrailTripwireTriggered(result)             guardrail_results.append(result)     except BaseException:         # On any error (including a guardrail raising or the caller being cancelled),         # cancel and await siblings so they don't leak past this function's return.         for t in guardrail_tasks:             if not t.done():                 t.cancel()         await asyncio.gather(*guardrail_tasks, return_exceptions=True)         raise      return guardrail_results ``` |

### input\_guardrail\_tripwire\_triggered\_for\_stream `async`

```
input_guardrail_tripwire_triggered_for_stream(
    streamed_result: RunResultStreaming,
) -> bool
```

Return True if any input guardrail triggered during a streamed run.

Source code in `src/agents/run_internal/guardrails.py`

|  |  |
| --- | --- |
| ``` 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 ``` | ``` async def input_guardrail_tripwire_triggered_for_stream(     streamed_result: RunResultStreaming, ) -> bool:     """Return True if any input guardrail triggered during a streamed run."""     task = streamed_result._input_guardrails_task     if task is None:         return False      if not task.done():         await task      return any(         guardrail_result.output.tripwire_triggered         for guardrail_result in streamed_result.input_guardrail_results     ) ``` |