---
url: https://openai.github.io/openai-agents-python/ref/
title: Agents module
framework: openai
---

# Agents module

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

### set\_default\_openai\_key

```
set_default_openai_key(
    key: str, use_for_tracing: bool = True
) -> None
```

Set the default OpenAI API key to use for LLM requests (and optionally tracing()). This is
only necessary if the OPENAI\_API\_KEY environment variable is not already set.

If provided, this key will be used instead of the OPENAI\_API\_KEY environment variable.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `key` | `str` | The OpenAI key to use. | *required* |
| `use_for_tracing` | `bool` | Whether to also use this key to send traces to OpenAI. Defaults to True If False, you'll either need to set the OPENAI\_API\_KEY environment variable or call set\_tracing\_export\_api\_key() with the API key you want to use for tracing. | `True` |

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ``` 272 273 274 275 276 277 278 279 280 281 282 283 284 ``` | ``` def set_default_openai_key(key: str, use_for_tracing: bool = True) -> None:     """Set the default OpenAI API key to use for LLM requests (and optionally tracing()). This is     only necessary if the OPENAI_API_KEY environment variable is not already set.      If provided, this key will be used instead of the OPENAI_API_KEY environment variable.      Args:         key: The OpenAI key to use.         use_for_tracing: Whether to also use this key to send traces to OpenAI. Defaults to True             If False, you'll either need to set the OPENAI_API_KEY environment variable or call             set_tracing_export_api_key() with the API key you want to use for tracing.     """     _config.set_default_openai_key(key, use_for_tracing) ``` |

### set\_default\_openai\_client

```
set_default_openai_client(
    client: AsyncOpenAI, use_for_tracing: bool = True
) -> None
```

Set the default OpenAI client to use for LLM requests and/or tracing. If provided, this
client will be used instead of the default OpenAI client.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `client` | `AsyncOpenAI` | The OpenAI client to use. | *required* |
| `use_for_tracing` | `bool` | Whether to use the API key from this client for uploading traces. If False, you'll either need to set the OPENAI\_API\_KEY environment variable or call set\_tracing\_export\_api\_key() with the API key you want to use for tracing. | `True` |

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ``` 287 288 289 290 291 292 293 294 295 296 297 ``` | ``` def set_default_openai_client(client: AsyncOpenAI, use_for_tracing: bool = True) -> None:     """Set the default OpenAI client to use for LLM requests and/or tracing. If provided, this     client will be used instead of the default OpenAI client.      Args:         client: The OpenAI client to use.         use_for_tracing: Whether to use the API key from this client for uploading traces. If False,             you'll either need to set the OPENAI_API_KEY environment variable or call             set_tracing_export_api_key() with the API key you want to use for tracing.     """     _config.set_default_openai_client(client, use_for_tracing) ``` |

### set\_default\_openai\_api

```
set_default_openai_api(
    api: Literal["chat_completions", "responses"],
) -> None
```

Set the default API to use for OpenAI LLM requests. By default, we will use the responses API
but you can set this to use the chat completions API instead.

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ``` 300 301 302 303 304 ``` | ``` def set_default_openai_api(api: Literal["chat_completions", "responses"]) -> None:     """Set the default API to use for OpenAI LLM requests. By default, we will use the responses API     but you can set this to use the chat completions API instead.     """     _config.set_default_openai_api(api) ``` |

### set\_default\_openai\_responses\_transport

```
set_default_openai_responses_transport(
    transport: Literal["http", "websocket"],
) -> None
```

Set the default transport for OpenAI Responses API requests.

By default, the Responses API uses the HTTP transport. Set this to `"websocket"` to use
websocket transport when the OpenAI provider resolves a Responses model.

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ``` 307 308 309 310 311 312 313 ``` | ``` def set_default_openai_responses_transport(transport: Literal["http", "websocket"]) -> None:     """Set the default transport for OpenAI Responses API requests.      By default, the Responses API uses the HTTP transport. Set this to ``"websocket"`` to use     websocket transport when the OpenAI provider resolves a Responses model.     """     _config.set_default_openai_responses_transport(transport) ``` |

### set\_tracing\_export\_api\_key

```
set_tracing_export_api_key(api_key: str) -> None
```

Set the OpenAI API key for the backend exporter.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ``` 115 116 117 118 119 ``` | ``` def set_tracing_export_api_key(api_key: str) -> None:     """     Set the OpenAI API key for the backend exporter.     """     default_exporter().set_api_key(api_key) ``` |

### set\_tracing\_disabled

```
set_tracing_disabled(disabled: bool) -> None
```

Set whether tracing is globally disabled.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ``` 108 109 110 111 112 ``` | ``` def set_tracing_disabled(disabled: bool) -> None:     """     Set whether tracing is globally disabled.     """     get_trace_provider().set_disabled(disabled) ``` |

### set\_trace\_processors

```
set_trace_processors(
    processors: list[TracingProcessor],
) -> None
```

Set the list of trace processors. This will replace the current list of processors.

Source code in `src/agents/tracing/__init__.py`

|  |  |
| --- | --- |
| ``` 101 102 103 104 105 ``` | ``` def set_trace_processors(processors: list[TracingProcessor]) -> None:     """     Set the list of trace processors. This will replace the current list of processors.     """     get_trace_provider().set_processors(processors) ``` |

### enable\_verbose\_stdout\_logging

```
enable_verbose_stdout_logging()
```

Enables verbose logging to stdout. This is useful for debugging.

Source code in `src/agents/__init__.py`

|  |  |
| --- | --- |
| ``` 335 336 337 338 339 ``` | ``` def enable_verbose_stdout_logging():     """Enables verbose logging to stdout. This is useful for debugging."""     logger = logging.getLogger("openai.agents")     logger.setLevel(logging.DEBUG)     logger.addHandler(logging.StreamHandler(sys.stdout)) ``` |