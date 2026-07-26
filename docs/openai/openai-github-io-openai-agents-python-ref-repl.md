---
url: https://openai.github.io/openai-agents-python/ref/repl/
title: `repl`
framework: openai
---

# `repl`

### run\_demo\_loop `async`

```
run_demo_loop(
    agent: Agent[Any],
    *,
    stream: bool = True,
    context: TContext | None = None,
    max_turns: int | None = DEFAULT_MAX_TURNS,
) -> None
```

Run a simple REPL loop with the given agent.

This utility allows quick manual testing and debugging of an agent from the
command line. Conversation state is preserved across turns. Enter `exit`
or `quit` to stop the loop.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `Agent[Any]` | The starting agent to run. | *required* |
| `stream` | `bool` | Whether to stream the agent output. | `True` |
| `context` | `TContext | None` | Additional context information to pass to the runner. | `None` |
| `max_turns` | `int | None` | Maximum number of turns for the runner to iterate. Pass `None` to disable the turn limit. | `DEFAULT_MAX_TURNS` |

Source code in `src/agents/repl.py`

|  |  |
| --- | --- |
| ``` 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 ``` | ``` async def run_demo_loop(     agent: Agent[Any],     *,     stream: bool = True,     context: TContext | None = None,     max_turns: int | None = DEFAULT_MAX_TURNS, ) -> None:     """Run a simple REPL loop with the given agent.      This utility allows quick manual testing and debugging of an agent from the     command line. Conversation state is preserved across turns. Enter ``exit``     or ``quit`` to stop the loop.      Args:         agent: The starting agent to run.         stream: Whether to stream the agent output.         context: Additional context information to pass to the runner.         max_turns: Maximum number of turns for the runner to iterate. Pass ``None`` to disable             the turn limit.     """      current_agent = agent     input_items: list[TResponseInputItem] = []     while True:         try:             user_input = input(" > ")         except (EOFError, KeyboardInterrupt):             print()             break         if user_input.strip().lower() in {"exit", "quit"}:             break         if not user_input:             continue          input_items.append({"role": "user", "content": user_input})          result: RunResultBase         if stream:             result = Runner.run_streamed(                 current_agent, input=input_items, context=context, max_turns=max_turns             )             async for event in result.stream_events():                 if isinstance(event, RawResponsesStreamEvent):                     if isinstance(event.data, ResponseTextDeltaEvent):                         print(event.data.delta, end="", flush=True)                 elif isinstance(event, RunItemStreamEvent):                     if event.item.type == "tool_call_item":                         print("\n[tool called]", flush=True)                     elif event.item.type == "tool_call_output_item":                         print(f"\n[tool output: {event.item.output}]", flush=True)                 elif isinstance(event, AgentUpdatedStreamEvent):                     print(f"\n[Agent updated: {event.new_agent.name}]", flush=True)             print()         else:             result = await Runner.run(                 current_agent, input_items, context=context, max_turns=max_turns             )             if result.final_output is not None:                 print(result.final_output)          current_agent = result.last_agent         input_items = result.to_input_list() ``` |