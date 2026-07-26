---
url: https://openai.github.io/openai-agents-python/ref/run/
title: `Runner`
framework: openai
---

# `Runner`

### Runner

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ``` 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 ``` | ``` class Runner:     @classmethod     async def run(         cls,         starting_agent: Agent[TContext],         input: str | list[TResponseInputItem] | RunState[TContext],         *,         context: TContext | None = None,         max_turns: int | None = DEFAULT_MAX_TURNS,         hooks: RunHooks[TContext] | None = None,         run_config: RunConfig | None = None,         error_handlers: RunErrorHandlers[TContext] | None = None,         previous_response_id: str | None = None,         auto_previous_response_id: bool = False,         conversation_id: str | None = None,         session: Session | None = None,     ) -> RunResult:         """         Run a workflow starting at the given agent.          The agent will run in a loop until a final output is generated. The loop runs like so:            1. The agent is invoked with the given input.           2. If there is a final output (i.e. the agent produces something of type              `agent.output_type`), the loop terminates.           3. If there's a handoff, we run the loop again, with the new agent.           4. Else, we run tool calls (if any), and re-run the loop.          In two cases, the agent may raise an exception:            1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.           2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered              exception is raised.          Note:             Only the first agent's input guardrails are run.          Args:             starting_agent: The starting agent to run.             input: The initial input to the agent. You can pass a single string for a                 user message, or a list of input items.             context: The context to run the agent with.             max_turns: The maximum number of turns to run the agent for. A turn is                 defined as one AI invocation (including any tool calls that might occur).                 Pass ``None`` to disable the turn limit.             hooks: An object that receives callbacks on various lifecycle events.             run_config: Global settings for the entire agent run.             error_handlers: Error handlers keyed by error kind.             previous_response_id: The ID of the previous response. If using OpenAI                 models via the Responses API, this allows you to skip passing in input                 from the previous turn.             auto_previous_response_id: If True, enable Responses API response chaining                 automatically for the first turn even when no                 ``previous_response_id`` is supplied yet.             conversation_id: The conversation ID                 (https://platform.openai.com/docs/guides/conversation-state?api-mode=responses).                 If provided, the conversation will be used to read and write items.                 Every agent will have access to the conversation history so far,                 and its output items will be written to the conversation.                 We recommend only using this if you are exclusively using OpenAI models;                 other model providers don't write to the Conversation object,                 so you'll end up having partial conversations stored.             session: A session for automatic conversation history management.          Returns:             A run result containing all the inputs, guardrail results and the output of             the last agent. Agents may perform handoffs, so we don't know the specific             type of the output.         """          runner = DEFAULT_AGENT_RUNNER         return await runner.run(             starting_agent,             input,             context=context,             max_turns=max_turns,             hooks=hooks,             run_config=run_config,             error_handlers=error_handlers,             previous_response_id=previous_response_id,             auto_previous_response_id=auto_previous_response_id,             conversation_id=conversation_id,             session=session,         )      @classmethod     def run_sync(         cls,         starting_agent: Agent[TContext],         input: str | list[TResponseInputItem] | RunState[TContext],         *,         context: TContext | None = None,         max_turns: int | None = DEFAULT_MAX_TURNS,         hooks: RunHooks[TContext] | None = None,         run_config: RunConfig | None = None,         error_handlers: RunErrorHandlers[TContext] | None = None,         previous_response_id: str | None = None,         auto_previous_response_id: bool = False,         conversation_id: str | None = None,         session: Session | None = None,     ) -> RunResult:         """         Run a workflow synchronously, starting at the given agent.          Note:             This just wraps the `run` method, so it will not work if there's already an             event loop (e.g. inside an async function, or in a Jupyter notebook or async             context like FastAPI). For those cases, use the `run` method instead.          The agent will run in a loop until a final output is generated. The loop runs:            1. The agent is invoked with the given input.           2. If there is a final output (i.e. the agent produces something of type              `agent.output_type`), the loop terminates.           3. If there's a handoff, we run the loop again, with the new agent.           4. Else, we run tool calls (if any), and re-run the loop.          In two cases, the agent may raise an exception:            1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.           2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered              exception is raised.          Note:             Only the first agent's input guardrails are run.          Args:             starting_agent: The starting agent to run.             input: The initial input to the agent. You can pass a single string for a                 user message, or a list of input items.             context: The context to run the agent with.             max_turns: The maximum number of turns to run the agent for. A turn is                 defined as one AI invocation (including any tool calls that might occur).                 Pass ``None`` to disable the turn limit.             hooks: An object that receives callbacks on various lifecycle events.             run_config: Global settings for the entire agent run.             error_handlers: Error handlers keyed by error kind.             previous_response_id: The ID of the previous response, if using OpenAI                 models via the Responses API, this allows you to skip passing in input                 from the previous turn.             auto_previous_response_id: If True, enable Responses API response chaining                 automatically for the first turn even when no                 ``previous_response_id`` is supplied yet.             conversation_id: The ID of the stored conversation, if any.             session: A session for automatic conversation history management.          Returns:             A run result containing all the inputs, guardrail results and the output of             the last agent. Agents may perform handoffs, so we don't know the specific             type of the output.         """          runner = DEFAULT_AGENT_RUNNER         return runner.run_sync(             starting_agent,             input,             context=context,             max_turns=max_turns,             hooks=hooks,             run_config=run_config,             error_handlers=error_handlers,             previous_response_id=previous_response_id,             conversation_id=conversation_id,             session=session,             auto_previous_response_id=auto_previous_response_id,         )      @classmethod     def run_streamed(         cls,         starting_agent: Agent[TContext],         input: str | list[TResponseInputItem] | RunState[TContext],         context: TContext | None = None,         max_turns: int | None = DEFAULT_MAX_TURNS,         hooks: RunHooks[TContext] | None = None,         run_config: RunConfig | None = None,         previous_response_id: str | None = None,         auto_previous_response_id: bool = False,         conversation_id: str | None = None,         session: Session | None = None,         *,         error_handlers: RunErrorHandlers[TContext] | None = None,     ) -> RunResultStreaming:         """         Run a workflow starting at the given agent in streaming mode.          The returned result object contains a method you can use to stream semantic         events as they are generated.          The agent will run in a loop until a final output is generated. The loop runs like so:            1. The agent is invoked with the given input.           2. If there is a final output (i.e. the agent produces something of type              `agent.output_type`), the loop terminates.           3. If there's a handoff, we run the loop again, with the new agent.           4. Else, we run tool calls (if any), and re-run the loop.          In two cases, the agent may raise an exception:            1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.           2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered              exception is raised.          Note:             Only the first agent's input guardrails are run.          Args:             starting_agent: The starting agent to run.             input: The initial input to the agent. You can pass a single string for a                 user message, or a list of input items.             context: The context to run the agent with.             max_turns: The maximum number of turns to run the agent for. A turn is                 defined as one AI invocation (including any tool calls that might occur).                 Pass ``None`` to disable the turn limit.             hooks: An object that receives callbacks on various lifecycle events.             run_config: Global settings for the entire agent run.             error_handlers: Error handlers keyed by error kind.             previous_response_id: The ID of the previous response, if using OpenAI                 models via the Responses API, this allows you to skip passing in input                 from the previous turn.             auto_previous_response_id: If True, enable Responses API response chaining                 automatically for the first turn even when no                 ``previous_response_id`` is supplied yet.             conversation_id: The ID of the stored conversation, if any.             session: A session for automatic conversation history management.          Returns:             A result object that contains data about the run, as well as a method to             stream events.         """          runner = DEFAULT_AGENT_RUNNER         return runner.run_streamed(             starting_agent,             input,             context=context,             max_turns=max_turns,             hooks=hooks,             run_config=run_config,             error_handlers=error_handlers,             previous_response_id=previous_response_id,             auto_previous_response_id=auto_previous_response_id,             conversation_id=conversation_id,             session=session,         ) ``` |

#### run `async` `classmethod`

```
run(
    starting_agent: Agent[TContext],
    input: str
    | list[TResponseInputItem]
    | RunState[TContext],
    *,
    context: TContext | None = None,
    max_turns: int | None = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    error_handlers: RunErrorHandlers[TContext]
    | None = None,
    previous_response_id: str | None = None,
    auto_previous_response_id: bool = False,
    conversation_id: str | None = None,
    session: Session | None = None,
) -> RunResult
```

Run a workflow starting at the given agent.

The agent will run in a loop until a final output is generated. The loop runs like so:

1. The agent is invoked with the given input.
2. If there is a final output (i.e. the agent produces something of type
   `agent.output_type`), the loop terminates.
3. If there's a handoff, we run the loop again, with the new agent.
4. Else, we run tool calls (if any), and re-run the loop.

In two cases, the agent may raise an exception:

1. If the max\_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.
2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered
   exception is raised.

Note

Only the first agent's input guardrails are run.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `starting_agent` | `Agent[TContext]` | The starting agent to run. | *required* |
| `input` | `str | list[TResponseInputItem] | RunState[TContext]` | The initial input to the agent. You can pass a single string for a user message, or a list of input items. | *required* |
| `context` | `TContext | None` | The context to run the agent with. | `None` |
| `max_turns` | `int | None` | The maximum number of turns to run the agent for. A turn is defined as one AI invocation (including any tool calls that might occur). Pass `None` to disable the turn limit. | `DEFAULT_MAX_TURNS` |
| `hooks` | `RunHooks[TContext] | None` | An object that receives callbacks on various lifecycle events. | `None` |
| `run_config` | `RunConfig | None` | Global settings for the entire agent run. | `None` |
| `error_handlers` | `RunErrorHandlers[TContext] | None` | Error handlers keyed by error kind. | `None` |
| `previous_response_id` | `str | None` | The ID of the previous response. If using OpenAI models via the Responses API, this allows you to skip passing in input from the previous turn. | `None` |
| `auto_previous_response_id` | `bool` | If True, enable Responses API response chaining automatically for the first turn even when no `previous_response_id` is supplied yet. | `False` |
| `conversation_id` | `str | None` | The conversation ID (https://platform.openai.com/docs/guides/conversation-state?api-mode=responses). If provided, the conversation will be used to read and write items. Every agent will have access to the conversation history so far, and its output items will be written to the conversation. We recommend only using this if you are exclusively using OpenAI models; other model providers don't write to the Conversation object, so you'll end up having partial conversations stored. | `None` |
| `session` | `Session | None` | A session for automatic conversation history management. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `RunResult` | A run result containing all the inputs, guardrail results and the output of |
| `RunResult` | the last agent. Agents may perform handoffs, so we don't know the specific |
| `RunResult` | type of the output. |

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ``` 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 ``` | ``` @classmethod async def run(     cls,     starting_agent: Agent[TContext],     input: str | list[TResponseInputItem] | RunState[TContext],     *,     context: TContext | None = None,     max_turns: int | None = DEFAULT_MAX_TURNS,     hooks: RunHooks[TContext] | None = None,     run_config: RunConfig | None = None,     error_handlers: RunErrorHandlers[TContext] | None = None,     previous_response_id: str | None = None,     auto_previous_response_id: bool = False,     conversation_id: str | None = None,     session: Session | None = None, ) -> RunResult:     """     Run a workflow starting at the given agent.      The agent will run in a loop until a final output is generated. The loop runs like so:        1. The agent is invoked with the given input.       2. If there is a final output (i.e. the agent produces something of type          `agent.output_type`), the loop terminates.       3. If there's a handoff, we run the loop again, with the new agent.       4. Else, we run tool calls (if any), and re-run the loop.      In two cases, the agent may raise an exception:        1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.       2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered          exception is raised.      Note:         Only the first agent's input guardrails are run.      Args:         starting_agent: The starting agent to run.         input: The initial input to the agent. You can pass a single string for a             user message, or a list of input items.         context: The context to run the agent with.         max_turns: The maximum number of turns to run the agent for. A turn is             defined as one AI invocation (including any tool calls that might occur).             Pass ``None`` to disable the turn limit.         hooks: An object that receives callbacks on various lifecycle events.         run_config: Global settings for the entire agent run.         error_handlers: Error handlers keyed by error kind.         previous_response_id: The ID of the previous response. If using OpenAI             models via the Responses API, this allows you to skip passing in input             from the previous turn.         auto_previous_response_id: If True, enable Responses API response chaining             automatically for the first turn even when no             ``previous_response_id`` is supplied yet.         conversation_id: The conversation ID             (https://platform.openai.com/docs/guides/conversation-state?api-mode=responses).             If provided, the conversation will be used to read and write items.             Every agent will have access to the conversation history so far,             and its output items will be written to the conversation.             We recommend only using this if you are exclusively using OpenAI models;             other model providers don't write to the Conversation object,             so you'll end up having partial conversations stored.         session: A session for automatic conversation history management.      Returns:         A run result containing all the inputs, guardrail results and the output of         the last agent. Agents may perform handoffs, so we don't know the specific         type of the output.     """      runner = DEFAULT_AGENT_RUNNER     return await runner.run(         starting_agent,         input,         context=context,         max_turns=max_turns,         hooks=hooks,         run_config=run_config,         error_handlers=error_handlers,         previous_response_id=previous_response_id,         auto_previous_response_id=auto_previous_response_id,         conversation_id=conversation_id,         session=session,     ) ``` |

#### run\_sync `classmethod`

```
run_sync(
    starting_agent: Agent[TContext],
    input: str
    | list[TResponseInputItem]
    | RunState[TContext],
    *,
    context: TContext | None = None,
    max_turns: int | None = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    error_handlers: RunErrorHandlers[TContext]
    | None = None,
    previous_response_id: str | None = None,
    auto_previous_response_id: bool = False,
    conversation_id: str | None = None,
    session: Session | None = None,
) -> RunResult
```

Run a workflow synchronously, starting at the given agent.

Note

This just wraps the `run` method, so it will not work if there's already an
event loop (e.g. inside an async function, or in a Jupyter notebook or async
context like FastAPI). For those cases, use the `run` method instead.

The agent will run in a loop until a final output is generated. The loop runs:

1. The agent is invoked with the given input.
2. If there is a final output (i.e. the agent produces something of type
   `agent.output_type`), the loop terminates.
3. If there's a handoff, we run the loop again, with the new agent.
4. Else, we run tool calls (if any), and re-run the loop.

In two cases, the agent may raise an exception:

1. If the max\_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.
2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered
   exception is raised.

Note

Only the first agent's input guardrails are run.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `starting_agent` | `Agent[TContext]` | The starting agent to run. | *required* |
| `input` | `str | list[TResponseInputItem] | RunState[TContext]` | The initial input to the agent. You can pass a single string for a user message, or a list of input items. | *required* |
| `context` | `TContext | None` | The context to run the agent with. | `None` |
| `max_turns` | `int | None` | The maximum number of turns to run the agent for. A turn is defined as one AI invocation (including any tool calls that might occur). Pass `None` to disable the turn limit. | `DEFAULT_MAX_TURNS` |
| `hooks` | `RunHooks[TContext] | None` | An object that receives callbacks on various lifecycle events. | `None` |
| `run_config` | `RunConfig | None` | Global settings for the entire agent run. | `None` |
| `error_handlers` | `RunErrorHandlers[TContext] | None` | Error handlers keyed by error kind. | `None` |
| `previous_response_id` | `str | None` | The ID of the previous response, if using OpenAI models via the Responses API, this allows you to skip passing in input from the previous turn. | `None` |
| `auto_previous_response_id` | `bool` | If True, enable Responses API response chaining automatically for the first turn even when no `previous_response_id` is supplied yet. | `False` |
| `conversation_id` | `str | None` | The ID of the stored conversation, if any. | `None` |
| `session` | `Session | None` | A session for automatic conversation history management. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `RunResult` | A run result containing all the inputs, guardrail results and the output of |
| `RunResult` | the last agent. Agents may perform handoffs, so we don't know the specific |
| `RunResult` | type of the output. |

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ``` 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 ``` | ``` @classmethod def run_sync(     cls,     starting_agent: Agent[TContext],     input: str | list[TResponseInputItem] | RunState[TContext],     *,     context: TContext | None = None,     max_turns: int | None = DEFAULT_MAX_TURNS,     hooks: RunHooks[TContext] | None = None,     run_config: RunConfig | None = None,     error_handlers: RunErrorHandlers[TContext] | None = None,     previous_response_id: str | None = None,     auto_previous_response_id: bool = False,     conversation_id: str | None = None,     session: Session | None = None, ) -> RunResult:     """     Run a workflow synchronously, starting at the given agent.      Note:         This just wraps the `run` method, so it will not work if there's already an         event loop (e.g. inside an async function, or in a Jupyter notebook or async         context like FastAPI). For those cases, use the `run` method instead.      The agent will run in a loop until a final output is generated. The loop runs:        1. The agent is invoked with the given input.       2. If there is a final output (i.e. the agent produces something of type          `agent.output_type`), the loop terminates.       3. If there's a handoff, we run the loop again, with the new agent.       4. Else, we run tool calls (if any), and re-run the loop.      In two cases, the agent may raise an exception:        1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.       2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered          exception is raised.      Note:         Only the first agent's input guardrails are run.      Args:         starting_agent: The starting agent to run.         input: The initial input to the agent. You can pass a single string for a             user message, or a list of input items.         context: The context to run the agent with.         max_turns: The maximum number of turns to run the agent for. A turn is             defined as one AI invocation (including any tool calls that might occur).             Pass ``None`` to disable the turn limit.         hooks: An object that receives callbacks on various lifecycle events.         run_config: Global settings for the entire agent run.         error_handlers: Error handlers keyed by error kind.         previous_response_id: The ID of the previous response, if using OpenAI             models via the Responses API, this allows you to skip passing in input             from the previous turn.         auto_previous_response_id: If True, enable Responses API response chaining             automatically for the first turn even when no             ``previous_response_id`` is supplied yet.         conversation_id: The ID of the stored conversation, if any.         session: A session for automatic conversation history management.      Returns:         A run result containing all the inputs, guardrail results and the output of         the last agent. Agents may perform handoffs, so we don't know the specific         type of the output.     """      runner = DEFAULT_AGENT_RUNNER     return runner.run_sync(         starting_agent,         input,         context=context,         max_turns=max_turns,         hooks=hooks,         run_config=run_config,         error_handlers=error_handlers,         previous_response_id=previous_response_id,         conversation_id=conversation_id,         session=session,         auto_previous_response_id=auto_previous_response_id,     ) ``` |

#### run\_streamed `classmethod`

```
run_streamed(
    starting_agent: Agent[TContext],
    input: str
    | list[TResponseInputItem]
    | RunState[TContext],
    context: TContext | None = None,
    max_turns: int | None = DEFAULT_MAX_TURNS,
    hooks: RunHooks[TContext] | None = None,
    run_config: RunConfig | None = None,
    previous_response_id: str | None = None,
    auto_previous_response_id: bool = False,
    conversation_id: str | None = None,
    session: Session | None = None,
    *,
    error_handlers: RunErrorHandlers[TContext]
    | None = None,
) -> RunResultStreaming
```

Run a workflow starting at the given agent in streaming mode.

The returned result object contains a method you can use to stream semantic
events as they are generated.

The agent will run in a loop until a final output is generated. The loop runs like so:

1. The agent is invoked with the given input.
2. If there is a final output (i.e. the agent produces something of type
   `agent.output_type`), the loop terminates.
3. If there's a handoff, we run the loop again, with the new agent.
4. Else, we run tool calls (if any), and re-run the loop.

In two cases, the agent may raise an exception:

1. If the max\_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.
2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered
   exception is raised.

Note

Only the first agent's input guardrails are run.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `starting_agent` | `Agent[TContext]` | The starting agent to run. | *required* |
| `input` | `str | list[TResponseInputItem] | RunState[TContext]` | The initial input to the agent. You can pass a single string for a user message, or a list of input items. | *required* |
| `context` | `TContext | None` | The context to run the agent with. | `None` |
| `max_turns` | `int | None` | The maximum number of turns to run the agent for. A turn is defined as one AI invocation (including any tool calls that might occur). Pass `None` to disable the turn limit. | `DEFAULT_MAX_TURNS` |
| `hooks` | `RunHooks[TContext] | None` | An object that receives callbacks on various lifecycle events. | `None` |
| `run_config` | `RunConfig | None` | Global settings for the entire agent run. | `None` |
| `error_handlers` | `RunErrorHandlers[TContext] | None` | Error handlers keyed by error kind. | `None` |
| `previous_response_id` | `str | None` | The ID of the previous response, if using OpenAI models via the Responses API, this allows you to skip passing in input from the previous turn. | `None` |
| `auto_previous_response_id` | `bool` | If True, enable Responses API response chaining automatically for the first turn even when no `previous_response_id` is supplied yet. | `False` |
| `conversation_id` | `str | None` | The ID of the stored conversation, if any. | `None` |
| `session` | `Session | None` | A session for automatic conversation history management. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `RunResultStreaming` | A result object that contains data about the run, as well as a method to |
| `RunResultStreaming` | stream events. |

Source code in `src/agents/run.py`

|  |  |
| --- | --- |
| ``` 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 ``` | ``` @classmethod def run_streamed(     cls,     starting_agent: Agent[TContext],     input: str | list[TResponseInputItem] | RunState[TContext],     context: TContext | None = None,     max_turns: int | None = DEFAULT_MAX_TURNS,     hooks: RunHooks[TContext] | None = None,     run_config: RunConfig | None = None,     previous_response_id: str | None = None,     auto_previous_response_id: bool = False,     conversation_id: str | None = None,     session: Session | None = None,     *,     error_handlers: RunErrorHandlers[TContext] | None = None, ) -> RunResultStreaming:     """     Run a workflow starting at the given agent in streaming mode.      The returned result object contains a method you can use to stream semantic     events as they are generated.      The agent will run in a loop until a final output is generated. The loop runs like so:        1. The agent is invoked with the given input.       2. If there is a final output (i.e. the agent produces something of type          `agent.output_type`), the loop terminates.       3. If there's a handoff, we run the loop again, with the new agent.       4. Else, we run tool calls (if any), and re-run the loop.      In two cases, the agent may raise an exception:        1. If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.       2. If a guardrail tripwire is triggered, a GuardrailTripwireTriggered          exception is raised.      Note:         Only the first agent's input guardrails are run.      Args:         starting_agent: The starting agent to run.         input: The initial input to the agent. You can pass a single string for a             user message, or a list of input items.         context: The context to run the agent with.         max_turns: The maximum number of turns to run the agent for. A turn is             defined as one AI invocation (including any tool calls that might occur).             Pass ``None`` to disable the turn limit.         hooks: An object that receives callbacks on various lifecycle events.         run_config: Global settings for the entire agent run.         error_handlers: Error handlers keyed by error kind.         previous_response_id: The ID of the previous response, if using OpenAI             models via the Responses API, this allows you to skip passing in input             from the previous turn.         auto_previous_response_id: If True, enable Responses API response chaining             automatically for the first turn even when no             ``previous_response_id`` is supplied yet.         conversation_id: The ID of the stored conversation, if any.         session: A session for automatic conversation history management.      Returns:         A result object that contains data about the run, as well as a method to         stream events.     """      runner = DEFAULT_AGENT_RUNNER     return runner.run_streamed(         starting_agent,         input,         context=context,         max_turns=max_turns,         hooks=hooks,         run_config=run_config,         error_handlers=error_handlers,         previous_response_id=previous_response_id,         auto_previous_response_id=auto_previous_response_id,         conversation_id=conversation_id,         session=session,     ) ``` |

### RunConfig `dataclass`

Configures settings for the entire agent run.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 ``` | ``` @dataclass class RunConfig:     """Configures settings for the entire agent run."""      model: str | Model | None = None     """The model to use for the entire agent run. If set, will override the model set on every     agent. The model_provider passed in below must be able to resolve this model name.     """      model_provider: ModelProvider = field(default_factory=MultiProvider)     """The model provider to use when looking up string model names. Defaults to OpenAI."""      model_settings: ModelSettings | None = None     """Configure global model settings. Any non-null values will override the agent-specific model     settings.     """      handoff_input_filter: HandoffInputFilter | None = None     """A global input filter to apply to all handoffs. If `Handoff.input_filter` is set, then that     will take precedence. The input filter allows you to edit the inputs that are sent to the new     agent. See the documentation in `Handoff.input_filter` for more details. Server-managed     conversations (`conversation_id`, `previous_response_id`, or `auto_previous_response_id`)     do not support handoff input filters.     """      nest_handoff_history: bool = False     """Opt-in beta: compact prior run history into ordered assistant summary segments while     preserving lossless message items in their original positions. This is disabled by default     while we stabilize nested handoffs; set to True to enable the compacted transcript behavior.     Server-managed conversations     (`conversation_id`, `previous_response_id`, or `auto_previous_response_id`) automatically     disable this behavior with a warning.     """      handoff_history_mapper: HandoffHistoryMapper | None = None     """Optional function that receives the normalized transcript (history + handoff items) and     returns the input history that should be passed to the next agent. When left as `None`, the     runner uses ordered summary segments around lossless message items. When supplied, the     function's return value is used as the exact input history. This function only runs when     `nest_handoff_history` is True.     """      input_guardrails: list[InputGuardrail[Any]] | None = None     """A list of input guardrails to run on the initial run input."""      output_guardrails: list[OutputGuardrail[Any]] | None = None     """A list of output guardrails to run on the final output of the run."""      tracing_disabled: bool = False     """Whether tracing is disabled for the agent run. If disabled, we will not trace the agent run.     """      tracing: TracingConfig | None = None     """Tracing configuration for this run."""      trace_include_sensitive_data: bool = field(         default_factory=_default_trace_include_sensitive_data     )     """Whether we include potentially sensitive data (for example: inputs/outputs of tool calls or     LLM generations) in traces. If False, we'll still create spans for these events, but the     sensitive data will not be included.     """      workflow_name: str = "Agent workflow"     """The name of the run, used for tracing. Should be a logical name for the run, like     "Code generation workflow" or "Customer support agent".     """      trace_id: str | None = None     """A custom trace ID to use for tracing. If not provided, we will generate a new trace ID."""      group_id: str | None = None     """     A grouping identifier to use for tracing, to link multiple traces from the same conversation     or process. For example, you might use a chat thread ID.     """      trace_metadata: dict[str, Any] | None = None     """     An optional dictionary of additional metadata to include with the trace.     """      session_input_callback: SessionInputCallback | None = None     """Defines how to handle session history when new input is provided.     - `None` (default): The new input is appended to the session history.     - `SessionInputCallback`: A custom function that receives the history and new input, and       returns the desired combined list of items.     """      call_model_input_filter: CallModelInputFilter | None = None     """     Optional callback that is invoked immediately before calling the model. It receives the current     agent, context and the model input (instructions and input items), and must return a possibly     modified `ModelInputData` to use for the model call.      This allows you to edit the input sent to the model e.g. to stay within a token limit.     For example, you can use this to add a system prompt to the input.     """      tool_error_formatter: ToolErrorFormatter | None = None     """Optional callback that formats tool error messages returned to the model.      Returning ``None`` falls back to the SDK default message.     """      session_settings: SessionSettings | None = None     """Configure session settings. Any non-null values will override the session's default     settings. Used to control session behavior like the number of items to retrieve.     """      reasoning_item_id_policy: ReasoningItemIdPolicy | None = None     """Controls how reasoning items are converted to next-turn model input.      - ``None`` / ``"preserve"`` keeps reasoning item IDs as-is.     - ``"omit"`` strips reasoning item IDs from model input built by the runner.     """      sandbox: SandboxRunConfig | None = None     """Optional sandbox runtime configuration for `SandboxAgent` execution."""      tool_execution: ToolExecutionConfig | None = None     """Optional SDK-side execution settings for local tool calls."""      tool_not_found_behavior: ToolNotFoundBehavior = "raise_error"     """Controls unresolved function tool calls emitted by the model.      - ``"raise_error"`` preserves the default behavior and raises ``ModelBehaviorError``.     - ``"return_error_to_model"`` returns a model-visible ``function_call_output`` error and lets       the run continue.     """ ``` |

#### model `class-attribute` `instance-attribute`

```
model: str | Model | None = None
```

The model to use for the entire agent run. If set, will override the model set on every
agent. The model\_provider passed in below must be able to resolve this model name.

#### model\_provider `class-attribute` `instance-attribute`

```
model_provider: ModelProvider = field(
    default_factory=MultiProvider
)
```

The model provider to use when looking up string model names. Defaults to OpenAI.

#### model\_settings `class-attribute` `instance-attribute`

```
model_settings: ModelSettings | None = None
```

Configure global model settings. Any non-null values will override the agent-specific model
settings.

#### handoff\_input\_filter `class-attribute` `instance-attribute`

```
handoff_input_filter: HandoffInputFilter | None = None
```

A global input filter to apply to all handoffs. If `Handoff.input_filter` is set, then that
will take precedence. The input filter allows you to edit the inputs that are sent to the new
agent. See the documentation in `Handoff.input_filter` for more details. Server-managed
conversations (`conversation_id`, `previous_response_id`, or `auto_previous_response_id`)
do not support handoff input filters.

#### nest\_handoff\_history `class-attribute` `instance-attribute`

```
nest_handoff_history: bool = False
```

Opt-in beta: compact prior run history into ordered assistant summary segments while
preserving lossless message items in their original positions. This is disabled by default
while we stabilize nested handoffs; set to True to enable the compacted transcript behavior.
Server-managed conversations
(`conversation_id`, `previous_response_id`, or `auto_previous_response_id`) automatically
disable this behavior with a warning.

#### handoff\_history\_mapper `class-attribute` `instance-attribute`

```
handoff_history_mapper: HandoffHistoryMapper | None = None
```

Optional function that receives the normalized transcript (history + handoff items) and
returns the input history that should be passed to the next agent. When left as `None`, the
runner uses ordered summary segments around lossless message items. When supplied, the
function's return value is used as the exact input history. This function only runs when
`nest_handoff_history` is True.

#### input\_guardrails `class-attribute` `instance-attribute`

```
input_guardrails: list[InputGuardrail[Any]] | None = None
```

A list of input guardrails to run on the initial run input.

#### output\_guardrails `class-attribute` `instance-attribute`

```
output_guardrails: list[OutputGuardrail[Any]] | None = None
```

A list of output guardrails to run on the final output of the run.

#### tracing\_disabled `class-attribute` `instance-attribute`

```
tracing_disabled: bool = False
```

Whether tracing is disabled for the agent run. If disabled, we will not trace the agent run.

#### tracing `class-attribute` `instance-attribute`

```
tracing: TracingConfig | None = None
```

Tracing configuration for this run.

#### trace\_include\_sensitive\_data `class-attribute` `instance-attribute`

```
trace_include_sensitive_data: bool = field(
    default_factory=_default_trace_include_sensitive_data
)
```

Whether we include potentially sensitive data (for example: inputs/outputs of tool calls or
LLM generations) in traces. If False, we'll still create spans for these events, but the
sensitive data will not be included.

#### workflow\_name `class-attribute` `instance-attribute`

```
workflow_name: str = 'Agent workflow'
```

The name of the run, used for tracing. Should be a logical name for the run, like
"Code generation workflow" or "Customer support agent".

#### trace\_id `class-attribute` `instance-attribute`

```
trace_id: str | None = None
```

A custom trace ID to use for tracing. If not provided, we will generate a new trace ID.

#### group\_id `class-attribute` `instance-attribute`

```
group_id: str | None = None
```

A grouping identifier to use for tracing, to link multiple traces from the same conversation
or process. For example, you might use a chat thread ID.

#### trace\_metadata `class-attribute` `instance-attribute`

```
trace_metadata: dict[str, Any] | None = None
```

An optional dictionary of additional metadata to include with the trace.

#### session\_input\_callback `class-attribute` `instance-attribute`

```
session_input_callback: SessionInputCallback | None = None
```

Defines how to handle session history when new input is provided.
- `None` (default): The new input is appended to the session history.
- `SessionInputCallback`: A custom function that receives the history and new input, and
returns the desired combined list of items.

#### call\_model\_input\_filter `class-attribute` `instance-attribute`

```
call_model_input_filter: CallModelInputFilter | None = None
```

Optional callback that is invoked immediately before calling the model. It receives the current
agent, context and the model input (instructions and input items), and must return a possibly
modified `ModelInputData` to use for the model call.

This allows you to edit the input sent to the model e.g. to stay within a token limit.
For example, you can use this to add a system prompt to the input.

#### tool\_error\_formatter `class-attribute` `instance-attribute`

```
tool_error_formatter: ToolErrorFormatter | None = None
```

Optional callback that formats tool error messages returned to the model.

Returning `None` falls back to the SDK default message.

#### session\_settings `class-attribute` `instance-attribute`

```
session_settings: SessionSettings | None = None
```

Configure session settings. Any non-null values will override the session's default
settings. Used to control session behavior like the number of items to retrieve.

#### reasoning\_item\_id\_policy `class-attribute` `instance-attribute`

```
reasoning_item_id_policy: ReasoningItemIdPolicy | None = (
    None
)
```

Controls how reasoning items are converted to next-turn model input.

* `None` / `"preserve"` keeps reasoning item IDs as-is.
* `"omit"` strips reasoning item IDs from model input built by the runner.

#### sandbox `class-attribute` `instance-attribute`

```
sandbox: SandboxRunConfig | None = None
```

Optional sandbox runtime configuration for `SandboxAgent` execution.

#### tool\_execution `class-attribute` `instance-attribute`

```
tool_execution: ToolExecutionConfig | None = None
```

Optional SDK-side execution settings for local tool calls.

#### tool\_not\_found\_behavior `class-attribute` `instance-attribute`

```
tool_not_found_behavior: ToolNotFoundBehavior = (
    "raise_error"
)
```

Controls unresolved function tool calls emitted by the model.

* `"raise_error"` preserves the default behavior and raises `ModelBehaviorError`.
* `"return_error_to_model"` returns a model-visible `function_call_output` error and lets
  the run continue.