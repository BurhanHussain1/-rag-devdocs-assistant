---
url: https://openai.github.io/openai-agents-python/ref/models/interface/
title: `Model interface`
framework: openai
---

# `Model interface`

### ModelTracing

Bases: `Enum`

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 ``` | ``` class ModelTracing(enum.Enum):     DISABLED = 0     """Tracing is disabled entirely."""      ENABLED = 1     """Tracing is enabled, and all data is included."""      ENABLED_WITHOUT_DATA = 2     """Tracing is enabled, but inputs/outputs are not included."""      def is_disabled(self) -> bool:         return self == ModelTracing.DISABLED      def include_data(self) -> bool:         return self == ModelTracing.ENABLED ``` |

#### DISABLED `class-attribute` `instance-attribute`

```
DISABLED = 0
```

Tracing is disabled entirely.

#### ENABLED `class-attribute` `instance-attribute`

```
ENABLED = 1
```

Tracing is enabled, and all data is included.

#### ENABLED\_WITHOUT\_DATA `class-attribute` `instance-attribute`

```
ENABLED_WITHOUT_DATA = 2
```

Tracing is enabled, but inputs/outputs are not included.

### Model

Bases: `ABC`

The base interface for calling an LLM.

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ```  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 ``` | ``` class Model(abc.ABC):     """The base interface for calling an LLM."""      async def _cleanup_on_run_end(self, owner: object) -> None:         """Release run-scoped resources after the runner finishes using this model."""         return None      async def close(self) -> None:         """Release any resources held by the model.          Models that maintain persistent connections can override this. The default implementation         is a no-op.         """         return None      def get_retry_advice(self, request: ModelRetryAdviceRequest) -> ModelRetryAdvice | None:         """Return provider-specific retry guidance for a failed model request.          Models can override this to surface transport- or provider-specific hints such as replay         safety, retry-after delays, or explicit server retry guidance.         """         return None      @abc.abstractmethod     async def get_response(         self,         system_instructions: str | None,         input: str | list[TResponseInputItem],         model_settings: ModelSettings,         tools: list[Tool],         output_schema: AgentOutputSchemaBase | None,         handoffs: list[Handoff],         tracing: ModelTracing,         *,         previous_response_id: str | None,         conversation_id: str | None,         prompt: ResponsePromptParam | None,     ) -> ModelResponse:         """Get a response from the model.          Args:             system_instructions: The system instructions to use.             input: The input items to the model, in OpenAI Responses format.             model_settings: The model settings to use.             tools: The tools available to the model.             output_schema: The output schema to use.             handoffs: The handoffs available to the model.             tracing: Tracing configuration.             previous_response_id: the ID of the previous response. Generally not used by the model,                 except for the OpenAI Responses API.             conversation_id: The ID of the stored conversation, if any.             prompt: The prompt config to use for the model.          Returns:             The full model response.         """         pass      @abc.abstractmethod     def stream_response(         self,         system_instructions: str | None,         input: str | list[TResponseInputItem],         model_settings: ModelSettings,         tools: list[Tool],         output_schema: AgentOutputSchemaBase | None,         handoffs: list[Handoff],         tracing: ModelTracing,         *,         previous_response_id: str | None,         conversation_id: str | None,         prompt: ResponsePromptParam | None,     ) -> AsyncIterator[TResponseStreamEvent]:         """Stream a response from the model.          Args:             system_instructions: The system instructions to use.             input: The input items to the model, in OpenAI Responses format.             model_settings: The model settings to use.             tools: The tools available to the model.             output_schema: The output schema to use.             handoffs: The handoffs available to the model.             tracing: Tracing configuration.             previous_response_id: the ID of the previous response. Generally not used by the model,                 except for the OpenAI Responses API.             conversation_id: The ID of the stored conversation, if any.             prompt: The prompt config to use for the model.          Returns:             An iterator of response stream events, in OpenAI Responses format.         """         pass ``` |

#### close `async`

```
close() -> None
```

Release any resources held by the model.

Models that maintain persistent connections can override this. The default implementation
is a no-op.

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 44 45 46 47 48 49 50 ``` | ``` async def close(self) -> None:     """Release any resources held by the model.      Models that maintain persistent connections can override this. The default implementation     is a no-op.     """     return None ``` |

#### get\_retry\_advice

```
get_retry_advice(
    request: ModelRetryAdviceRequest,
) -> ModelRetryAdvice | None
```

Return provider-specific retry guidance for a failed model request.

Models can override this to surface transport- or provider-specific hints such as replay
safety, retry-after delays, or explicit server retry guidance.

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 52 53 54 55 56 57 58 ``` | ``` def get_retry_advice(self, request: ModelRetryAdviceRequest) -> ModelRetryAdvice | None:     """Return provider-specific retry guidance for a failed model request.      Models can override this to surface transport- or provider-specific hints such as replay     safety, retry-after delays, or explicit server retry guidance.     """     return None ``` |

#### get\_response `abstractmethod` `async`

```
get_response(
    system_instructions: str | None,
    input: str | list[TResponseInputItem],
    model_settings: ModelSettings,
    tools: list[Tool],
    output_schema: AgentOutputSchemaBase | None,
    handoffs: list[Handoff],
    tracing: ModelTracing,
    *,
    previous_response_id: str | None,
    conversation_id: str | None,
    prompt: ResponsePromptParam | None,
) -> ModelResponse
```

Get a response from the model.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `system_instructions` | `str | None` | The system instructions to use. | *required* |
| `input` | `str | list[TResponseInputItem]` | The input items to the model, in OpenAI Responses format. | *required* |
| `model_settings` | `ModelSettings` | The model settings to use. | *required* |
| `tools` | `list[Tool]` | The tools available to the model. | *required* |
| `output_schema` | `AgentOutputSchemaBase | None` | The output schema to use. | *required* |
| `handoffs` | `list[Handoff]` | The handoffs available to the model. | *required* |
| `tracing` | `ModelTracing` | Tracing configuration. | *required* |
| `previous_response_id` | `str | None` | the ID of the previous response. Generally not used by the model, except for the OpenAI Responses API. | *required* |
| `conversation_id` | `str | None` | The ID of the stored conversation, if any. | *required* |
| `prompt` | `ResponsePromptParam | None` | The prompt config to use for the model. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `ModelResponse` | The full model response. |

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 ``` | ``` @abc.abstractmethod async def get_response(     self,     system_instructions: str | None,     input: str | list[TResponseInputItem],     model_settings: ModelSettings,     tools: list[Tool],     output_schema: AgentOutputSchemaBase | None,     handoffs: list[Handoff],     tracing: ModelTracing,     *,     previous_response_id: str | None,     conversation_id: str | None,     prompt: ResponsePromptParam | None, ) -> ModelResponse:     """Get a response from the model.      Args:         system_instructions: The system instructions to use.         input: The input items to the model, in OpenAI Responses format.         model_settings: The model settings to use.         tools: The tools available to the model.         output_schema: The output schema to use.         handoffs: The handoffs available to the model.         tracing: Tracing configuration.         previous_response_id: the ID of the previous response. Generally not used by the model,             except for the OpenAI Responses API.         conversation_id: The ID of the stored conversation, if any.         prompt: The prompt config to use for the model.      Returns:         The full model response.     """     pass ``` |

#### stream\_response `abstractmethod`

```
stream_response(
    system_instructions: str | None,
    input: str | list[TResponseInputItem],
    model_settings: ModelSettings,
    tools: list[Tool],
    output_schema: AgentOutputSchemaBase | None,
    handoffs: list[Handoff],
    tracing: ModelTracing,
    *,
    previous_response_id: str | None,
    conversation_id: str | None,
    prompt: ResponsePromptParam | None,
) -> AsyncIterator[TResponseStreamEvent]
```

Stream a response from the model.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `system_instructions` | `str | None` | The system instructions to use. | *required* |
| `input` | `str | list[TResponseInputItem]` | The input items to the model, in OpenAI Responses format. | *required* |
| `model_settings` | `ModelSettings` | The model settings to use. | *required* |
| `tools` | `list[Tool]` | The tools available to the model. | *required* |
| `output_schema` | `AgentOutputSchemaBase | None` | The output schema to use. | *required* |
| `handoffs` | `list[Handoff]` | The handoffs available to the model. | *required* |
| `tracing` | `ModelTracing` | Tracing configuration. | *required* |
| `previous_response_id` | `str | None` | the ID of the previous response. Generally not used by the model, except for the OpenAI Responses API. | *required* |
| `conversation_id` | `str | None` | The ID of the stored conversation, if any. | *required* |
| `prompt` | `ResponsePromptParam | None` | The prompt config to use for the model. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `AsyncIterator[TResponseStreamEvent]` | An iterator of response stream events, in OpenAI Responses format. |

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ```  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 ``` | ``` @abc.abstractmethod def stream_response(     self,     system_instructions: str | None,     input: str | list[TResponseInputItem],     model_settings: ModelSettings,     tools: list[Tool],     output_schema: AgentOutputSchemaBase | None,     handoffs: list[Handoff],     tracing: ModelTracing,     *,     previous_response_id: str | None,     conversation_id: str | None,     prompt: ResponsePromptParam | None, ) -> AsyncIterator[TResponseStreamEvent]:     """Stream a response from the model.      Args:         system_instructions: The system instructions to use.         input: The input items to the model, in OpenAI Responses format.         model_settings: The model settings to use.         tools: The tools available to the model.         output_schema: The output schema to use.         handoffs: The handoffs available to the model.         tracing: Tracing configuration.         previous_response_id: the ID of the previous response. Generally not used by the model,             except for the OpenAI Responses API.         conversation_id: The ID of the stored conversation, if any.         prompt: The prompt config to use for the model.      Returns:         An iterator of response stream events, in OpenAI Responses format.     """     pass ``` |

### ModelProvider

Bases: `ABC`

The base interface for a model provider.

Model provider is responsible for looking up Models by name.

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 ``` | ``` class ModelProvider(abc.ABC):     """The base interface for a model provider.      Model provider is responsible for looking up Models by name.     """      @abc.abstractmethod     def get_model(self, model_name: str | None) -> Model:         """Get a model by name.          Args:             model_name: The name of the model to get.          Returns:             The model.         """      async def aclose(self) -> None:         """Release any resources held by the provider.          Providers that cache persistent models or network connections can override this. The         default implementation is a no-op.         """         return None ``` |

#### get\_model `abstractmethod`

```
get_model(model_name: str | None) -> Model
```

Get a model by name.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `model_name` | `str | None` | The name of the model to get. | *required* |

Returns:

| Type | Description |
| --- | --- |
| `Model` | The model. |

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 137 138 139 140 141 142 143 144 145 146 ``` | ``` @abc.abstractmethod def get_model(self, model_name: str | None) -> Model:     """Get a model by name.      Args:         model_name: The name of the model to get.      Returns:         The model.     """ ``` |

#### aclose `async`

```
aclose() -> None
```

Release any resources held by the provider.

Providers that cache persistent models or network connections can override this. The
default implementation is a no-op.

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 148 149 150 151 152 153 154 ``` | ``` async def aclose(self) -> None:     """Release any resources held by the provider.      Providers that cache persistent models or network connections can override this. The     default implementation is a no-op.     """     return None ``` |