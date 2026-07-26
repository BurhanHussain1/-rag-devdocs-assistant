---
url: https://openai.github.io/openai-agents-python/ref/realtime/runner/
title: `RealtimeRunner`
framework: openai
---

# `RealtimeRunner`

A `RealtimeRunner` is the equivalent of `Runner` for realtime agents. It automatically
handles multiple turns by maintaining a persistent connection with the underlying model
layer.

The session manages the local history copy, executes tools, runs guardrails and facilitates
handoffs between agents.

Since this code runs on your server, it uses WebSockets by default. You can optionally create
your own custom model layer by implementing the `RealtimeModel` interface.

Source code in `src/agents/realtime/runner.py`

|  |  |
| --- | --- |
| ``` 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 ``` | ``` class RealtimeRunner:     """A `RealtimeRunner` is the equivalent of `Runner` for realtime agents. It automatically     handles multiple turns by maintaining a persistent connection with the underlying model     layer.      The session manages the local history copy, executes tools, runs guardrails and facilitates     handoffs between agents.      Since this code runs on your server, it uses WebSockets by default. You can optionally create     your own custom model layer by implementing the `RealtimeModel` interface.     """      def __init__(         self,         starting_agent: RealtimeAgent,         *,         model: RealtimeModel | None = None,         config: RealtimeRunConfig | None = None,     ) -> None:         """Initialize the realtime runner.          Args:             starting_agent: The agent to start the session with.             model: The model to use. If not provided, will use a default OpenAI realtime model.             config: Override parameters to use for the entire run.         """         self._starting_agent = starting_agent         self._config = config         self._model = model or OpenAIRealtimeWebSocketModel()      async def run(         self, *, context: TContext | None = None, model_config: RealtimeModelConfig | None = None     ) -> RealtimeSession:         """Start and returns a realtime session.          Args:             context: The context to use for the session.             model_config: Override parameters to use for this session's model.          Returns:             RealtimeSession: A session object that allows bidirectional communication with the             realtime model.          Example:             ```python             runner = RealtimeRunner(agent)             async with await runner.run() as session:                 await session.send_message("Hello")                 async for event in session:                     print(event)             ```         """         # Create and return the connection         session = RealtimeSession(             model=self._model,             agent=self._starting_agent,             context=context,             model_config=model_config,             run_config=self._config,         )          return session ``` |

### \_\_init\_\_

```
__init__(
    starting_agent: RealtimeAgent,
    *,
    model: RealtimeModel | None = None,
    config: RealtimeRunConfig | None = None,
) -> None
```

Initialize the realtime runner.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `starting_agent` | `RealtimeAgent` | The agent to start the session with. | *required* |
| `model` | `RealtimeModel | None` | The model to use. If not provided, will use a default OpenAI realtime model. | `None` |
| `config` | `RealtimeRunConfig | None` | Override parameters to use for the entire run. | `None` |

Source code in `src/agents/realtime/runner.py`

|  |  |
| --- | --- |
| ``` 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 ``` | ``` def __init__(     self,     starting_agent: RealtimeAgent,     *,     model: RealtimeModel | None = None,     config: RealtimeRunConfig | None = None, ) -> None:     """Initialize the realtime runner.      Args:         starting_agent: The agent to start the session with.         model: The model to use. If not provided, will use a default OpenAI realtime model.         config: Override parameters to use for the entire run.     """     self._starting_agent = starting_agent     self._config = config     self._model = model or OpenAIRealtimeWebSocketModel() ``` |

### run `async`

```
run(
    *,
    context: TContext | None = None,
    model_config: RealtimeModelConfig | None = None,
) -> RealtimeSession
```

Start and returns a realtime session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `context` | `TContext | None` | The context to use for the session. | `None` |
| `model_config` | `RealtimeModelConfig | None` | Override parameters to use for this session's model. | `None` |

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `RealtimeSession` | `RealtimeSession` | A session object that allows bidirectional communication with the |
|  | `RealtimeSession` | realtime model. |

Example

```
runner = RealtimeRunner(agent)
async with await runner.run() as session:
    await session.send_message("Hello")
    async for event in session:
        print(event)
```

Source code in `src/agents/realtime/runner.py`

|  |  |
| --- | --- |
| ``` 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 ``` | ``` async def run(     self, *, context: TContext | None = None, model_config: RealtimeModelConfig | None = None ) -> RealtimeSession:     """Start and returns a realtime session.      Args:         context: The context to use for the session.         model_config: Override parameters to use for this session's model.      Returns:         RealtimeSession: A session object that allows bidirectional communication with the         realtime model.      Example:         ```python         runner = RealtimeRunner(agent)         async with await runner.run() as session:             await session.send_message("Hello")             async for event in session:                 print(event)         ```     """     # Create and return the connection     session = RealtimeSession(         model=self._model,         agent=self._starting_agent,         context=context,         model_config=model_config,         run_config=self._config,     )      return session ``` |