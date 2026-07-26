---
url: https://openai.github.io/openai-agents-python/ref/responses_websocket_session/
title: `Responses WebSocket Session`
framework: openai
---

# `Responses WebSocket Session`

### ResponsesWebSocketSession `dataclass`

Helper that pins runs to a shared OpenAI websocket-capable provider.

Source code in `src/agents/responses_websocket_session.py`

|  |  |
| --- | --- |
| ``` 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 ``` | ``` @dataclass(frozen=True) class ResponsesWebSocketSession:     """Helper that pins runs to a shared OpenAI websocket-capable provider."""      provider: OpenAIProvider     run_config: RunConfig      def __post_init__(self) -> None:         self._validate_provider_alignment()      def _validate_provider_alignment(self) -> MultiProvider:         model_provider = self.run_config.model_provider         if not isinstance(model_provider, MultiProvider):             raise TypeError(                 "ResponsesWebSocketSession.run_config.model_provider must be a MultiProvider."             )         if model_provider.openai_provider is not self.provider:             raise ValueError(                 "ResponsesWebSocketSession provider and run_config.model_provider are not aligned."             )         return model_provider      async def aclose(self) -> None:         """Close cached provider model resources (including websocket connections)."""         await self._validate_provider_alignment().aclose()      def _prepare_runner_kwargs(self, method_name: str, kwargs: Mapping[str, Any]) -> dict[str, Any]:         self._validate_provider_alignment()         if "run_config" in kwargs:             raise ValueError(                 f"Do not pass `run_config` to ResponsesWebSocketSession.{method_name}()."             )         runner_kwargs = dict(kwargs)         runner_kwargs["run_config"] = self.run_config         return runner_kwargs      async def run(         self,         starting_agent: Agent[Any],         input: str | list[TResponseInputItem] | RunState[Any],         **kwargs: Any,     ) -> RunResult:         """Call ``Runner.run`` with the session's shared ``RunConfig``."""         runner_kwargs = self._prepare_runner_kwargs("run", kwargs)         return await Runner.run(starting_agent, input, **runner_kwargs)      def run_streamed(         self,         starting_agent: Agent[Any],         input: str | list[TResponseInputItem] | RunState[Any],         **kwargs: Any,     ) -> RunResultStreaming:         """Call ``Runner.run_streamed`` with the session's shared ``RunConfig``."""         runner_kwargs = self._prepare_runner_kwargs("run_streamed", kwargs)         return Runner.run_streamed(starting_agent, input, **runner_kwargs) ``` |

#### aclose `async`

```
aclose() -> None
```

Close cached provider model resources (including websocket connections).

Source code in `src/agents/responses_websocket_session.py`

|  |  |
| --- | --- |
| ``` 45 46 47 ``` | ``` async def aclose(self) -> None:     """Close cached provider model resources (including websocket connections)."""     await self._validate_provider_alignment().aclose() ``` |

#### run `async`

```
run(
    starting_agent: Agent[Any],
    input: str | list[TResponseInputItem] | RunState[Any],
    **kwargs: Any,
) -> RunResult
```

Call `Runner.run` with the session's shared `RunConfig`.

Source code in `src/agents/responses_websocket_session.py`

|  |  |
| --- | --- |
| ``` 59 60 61 62 63 64 65 66 67 ``` | ``` async def run(     self,     starting_agent: Agent[Any],     input: str | list[TResponseInputItem] | RunState[Any],     **kwargs: Any, ) -> RunResult:     """Call ``Runner.run`` with the session's shared ``RunConfig``."""     runner_kwargs = self._prepare_runner_kwargs("run", kwargs)     return await Runner.run(starting_agent, input, **runner_kwargs) ``` |

#### run\_streamed

```
run_streamed(
    starting_agent: Agent[Any],
    input: str | list[TResponseInputItem] | RunState[Any],
    **kwargs: Any,
) -> RunResultStreaming
```

Call `Runner.run_streamed` with the session's shared `RunConfig`.

Source code in `src/agents/responses_websocket_session.py`

|  |  |
| --- | --- |
| ``` 69 70 71 72 73 74 75 76 77 ``` | ``` def run_streamed(     self,     starting_agent: Agent[Any],     input: str | list[TResponseInputItem] | RunState[Any],     **kwargs: Any, ) -> RunResultStreaming:     """Call ``Runner.run_streamed`` with the session's shared ``RunConfig``."""     runner_kwargs = self._prepare_runner_kwargs("run_streamed", kwargs)     return Runner.run_streamed(starting_agent, input, **runner_kwargs) ``` |

### responses\_websocket\_session `async`

```
responses_websocket_session(
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    websocket_base_url: str | None = None,
    organization: str | None = None,
    project: str | None = None,
    openai_prefix_mode: MultiProviderOpenAIPrefixMode = "alias",
    unknown_prefix_mode: MultiProviderUnknownPrefixMode = "error",
    responses_websocket_options: OpenAIResponsesWebSocketOptions
    | None = None,
) -> AsyncIterator[ResponsesWebSocketSession]
```

Create a shared OpenAI Responses websocket session for multiple Runner calls.

The helper returns a session object that injects one shared `RunConfig` backed by a
websocket-configured `MultiProvider` with one shared `OpenAIProvider`. This preserves
prefix-based model routing (for example `openai/gpt-4.1`) while keeping websocket
connections warm across turns and nested agent-as-tool runs that inherit the same
`run_config`.

Use `openai_prefix_mode="model_id"` and/or `unknown_prefix_mode="model_id"` when the
configured OpenAI-compatible endpoint expects literal namespaced model IDs instead of the SDK's
historical routing-prefix behavior.

Pass `responses_websocket_options` to customize low-level websocket keepalive behavior such
as `ping_interval` and `ping_timeout`.

Drain or close streamed iterators before the context exits. Exiting the context while a
websocket request is still in flight may force-close the shared connection.

Source code in `src/agents/responses_websocket_session.py`

|  |  |
| --- | --- |
| ```  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 ``` | ``` @asynccontextmanager async def responses_websocket_session(     *,     api_key: str | None = None,     base_url: str | None = None,     websocket_base_url: str | None = None,     organization: str | None = None,     project: str | None = None,     openai_prefix_mode: MultiProviderOpenAIPrefixMode = "alias",     unknown_prefix_mode: MultiProviderUnknownPrefixMode = "error",     responses_websocket_options: OpenAIResponsesWebSocketOptions | None = None, ) -> AsyncIterator[ResponsesWebSocketSession]:     """Create a shared OpenAI Responses websocket session for multiple Runner calls.      The helper returns a session object that injects one shared ``RunConfig`` backed by a     websocket-configured ``MultiProvider`` with one shared ``OpenAIProvider``. This preserves     prefix-based model routing (for example ``openai/gpt-4.1``) while keeping websocket     connections warm across turns and nested agent-as-tool runs that inherit the same     ``run_config``.      Use ``openai_prefix_mode="model_id"`` and/or ``unknown_prefix_mode="model_id"`` when the     configured OpenAI-compatible endpoint expects literal namespaced model IDs instead of the SDK's     historical routing-prefix behavior.      Pass ``responses_websocket_options`` to customize low-level websocket keepalive behavior such     as ``ping_interval`` and ``ping_timeout``.      Drain or close streamed iterators before the context exits. Exiting the context while a     websocket request is still in flight may force-close the shared connection.     """     model_provider = MultiProvider(         openai_api_key=api_key,         openai_base_url=base_url,         openai_websocket_base_url=websocket_base_url,         openai_organization=organization,         openai_project=project,         openai_use_responses=True,         openai_use_responses_websocket=True,         openai_prefix_mode=openai_prefix_mode,         unknown_prefix_mode=unknown_prefix_mode,         openai_responses_websocket_options=responses_websocket_options,     )     provider = model_provider.openai_provider     session = ResponsesWebSocketSession(         provider=provider,         run_config=RunConfig(model_provider=model_provider),     )     try:         yield session     finally:         await session.aclose() ``` |