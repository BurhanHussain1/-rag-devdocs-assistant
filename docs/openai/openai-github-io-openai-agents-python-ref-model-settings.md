---
url: https://openai.github.io/openai-agents-python/ref/model_settings/
title: `Model settings`
framework: openai
---

# `Model settings`

### ModelSettings

Settings to use when calling an LLM.

This class holds optional model configuration parameters (e.g. temperature,
top\_p, penalties, truncation, etc.).

Not all models/providers support all of these parameters, so please check the API documentation
for the specific model and provider you are using.

Source code in `src/agents/model_settings.py`

|  |  |
| --- | --- |
| ```  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 ``` | ``` @dataclass class ModelSettings:     """Settings to use when calling an LLM.      This class holds optional model configuration parameters (e.g. temperature,     top_p, penalties, truncation, etc.).      Not all models/providers support all of these parameters, so please check the API documentation     for the specific model and provider you are using.     """      temperature: float | None = None     """The temperature to use when calling the model."""      top_p: float | None = None     """The top_p to use when calling the model."""      frequency_penalty: float | None = None     """The frequency penalty to use when calling the model."""      presence_penalty: float | None = None     """The presence penalty to use when calling the model."""      tool_choice: ToolChoice | None = None     """The tool choice to use when calling the model."""      parallel_tool_calls: bool | None = None     """Controls whether the model can make multiple parallel tool calls in a single turn.     If not provided (i.e., set to None), this behavior defers to the underlying     model provider's default. For most current providers (e.g., OpenAI), this typically     means parallel tool calls are enabled (True).     Set to True to explicitly enable parallel tool calls, or False to restrict the     model to at most one tool call per turn.     """      truncation: Literal["auto", "disabled"] | None = None     """The truncation strategy to use when calling the model.     See [Responses API documentation](https://platform.openai.com/docs/api-reference/responses/create#responses_create-truncation)     for more details.     """      max_tokens: int | None = None     """The maximum number of output tokens to generate."""      reasoning: Reasoning | None = None     """Configuration options for     [reasoning models](https://platform.openai.com/docs/guides/reasoning).     """      verbosity: Literal["low", "medium", "high"] | None = None     """Constrains the verbosity of the model's response.     """      metadata: dict[str, str] | None = None     """Metadata to include with the model response call."""      store: bool | None = None     """Whether to store the generated model response for later retrieval.     For Responses API: automatically enabled when not specified.     For Chat Completions API: disabled when not specified."""      prompt_cache_retention: Literal["in_memory", "24h"] | None = None     """The retention policy for the prompt cache. Set to `24h` to enable extended     prompt caching, which keeps cached prefixes active for longer, up to a maximum     of 24 hours.     [Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention)."""      include_usage: bool | None = None     """Whether to include usage chunk.     Only available for Chat Completions API."""      # TODO: revisit ResponseIncludable | str if ResponseIncludable covers more cases     # We've added str to support missing ones like     # "web_search_call.action.sources" etc.     response_include: list[ResponseIncludable | str] | None = None     """Additional output data to include in the model response.     [include parameter](https://platform.openai.com/docs/api-reference/responses/create#responses-create-include)"""      top_logprobs: int | None = None     """Number of top tokens to return logprobs for. Setting this will     automatically include ``"message.output_text.logprobs"`` in the response."""      extra_query: Query | None = None     """Additional query fields to provide with the request.     Defaults to None if not provided."""      extra_body: Body | None = None     """Additional body fields to provide with the request.     Defaults to None if not provided."""      extra_headers: Headers | None = None     """Additional headers to provide with the request.     Defaults to None if not provided."""      extra_args: dict[str, Any] | None = None     """Arbitrary keyword arguments to pass to the model API call.     These will be passed directly to the underlying model provider's API.     Use with caution as not all models support all parameters."""      retry: ModelRetrySettings | None = None     """Opt-in runner-managed retry settings for model calls."""      context_management: list[ContextManagement] | None = None     """Context management entries for OpenAI Responses API requests.      For example, use ``[{"type": "compaction", "compact_threshold": 200000}]``     to enable server-side compaction when the rendered context crosses a token threshold.     """      prompt_cache_options: PromptCacheOptions | None = None     """Prompt-cache configuration for OpenAI API requests.      Use ``{"mode": "explicit", "ttl": "30m"}`` with content-part cache breakpoints to     control which prompt prefixes are eligible for caching.     """      def resolve(self, override: ModelSettings | None) -> ModelSettings:         """Produce a new ModelSettings by overlaying any non-None values from the         override on top of this instance."""         if override is None:             return self          changes = {             field.name: getattr(override, field.name)             for field in fields(self)             if getattr(override, field.name) is not None         }          # Handle extra_args merging specially - merge dictionaries instead of replacing.         if self.extra_args is not None or override.extra_args is not None:             merged_args = {}             if self.extra_args:                 merged_args.update(self.extra_args)             if override.extra_args:                 merged_args.update(override.extra_args)             changes["extra_args"] = merged_args if merged_args else None          if self.retry is not None or override.retry is not None:             changes["retry"] = _merge_retry_settings(self.retry, override.retry)          return replace(self, **changes)      def to_json_dict(self) -> dict[str, Any]:         return cast(dict[str, Any], TypeAdapter(ModelSettings).dump_python(self, mode="json"))      def to_traceable_dict(self) -> dict[str, Any]:         """Serialize settings for tracing without provider-specific request extras."""         payload = self.to_json_dict()         return {key: payload[key] for key in _TRACEABLE_MODEL_SETTING_FIELDS if key in payload} ``` |

#### temperature `class-attribute` `instance-attribute`

```
temperature: float | None = None
```

The temperature to use when calling the model.

#### top\_p `class-attribute` `instance-attribute`

```
top_p: float | None = None
```

The top\_p to use when calling the model.

#### frequency\_penalty `class-attribute` `instance-attribute`

```
frequency_penalty: float | None = None
```

The frequency penalty to use when calling the model.

#### presence\_penalty `class-attribute` `instance-attribute`

```
presence_penalty: float | None = None
```

The presence penalty to use when calling the model.

#### tool\_choice `class-attribute` `instance-attribute`

```
tool_choice: ToolChoice | None = None
```

The tool choice to use when calling the model.

#### parallel\_tool\_calls `class-attribute` `instance-attribute`

```
parallel_tool_calls: bool | None = None
```

Controls whether the model can make multiple parallel tool calls in a single turn.
If not provided (i.e., set to None), this behavior defers to the underlying
model provider's default. For most current providers (e.g., OpenAI), this typically
means parallel tool calls are enabled (True).
Set to True to explicitly enable parallel tool calls, or False to restrict the
model to at most one tool call per turn.

#### truncation `class-attribute` `instance-attribute`

```
truncation: Literal['auto', 'disabled'] | None = None
```

The truncation strategy to use when calling the model.
See [Responses API documentation](https://platform.openai.com/docs/api-reference/responses/create#responses_create-truncation)
for more details.

#### max\_tokens `class-attribute` `instance-attribute`

```
max_tokens: int | None = None
```

The maximum number of output tokens to generate.

#### reasoning `class-attribute` `instance-attribute`

```
reasoning: Reasoning | None = None
```

Configuration options for
[reasoning models](https://platform.openai.com/docs/guides/reasoning).

#### verbosity `class-attribute` `instance-attribute`

```
verbosity: Literal['low', 'medium', 'high'] | None = None
```

Constrains the verbosity of the model's response.

#### metadata `class-attribute` `instance-attribute`

```
metadata: dict[str, str] | None = None
```

Metadata to include with the model response call.

#### store `class-attribute` `instance-attribute`

```
store: bool | None = None
```

Whether to store the generated model response for later retrieval.
For Responses API: automatically enabled when not specified.
For Chat Completions API: disabled when not specified.

#### prompt\_cache\_retention `class-attribute` `instance-attribute`

```
prompt_cache_retention: (
    Literal["in_memory", "24h"] | None
) = None
```

The retention policy for the prompt cache. Set to `24h` to enable extended
prompt caching, which keeps cached prefixes active for longer, up to a maximum
of 24 hours.
[Learn more](https://platform.openai.com/docs/guides/prompt-caching#prompt-cache-retention).

#### include\_usage `class-attribute` `instance-attribute`

```
include_usage: bool | None = None
```

Whether to include usage chunk.
Only available for Chat Completions API.

#### response\_include `class-attribute` `instance-attribute`

```
response_include: list[ResponseIncludable | str] | None = (
    None
)
```

Additional output data to include in the model response.
[include parameter](https://platform.openai.com/docs/api-reference/responses/create#responses-create-include)

#### top\_logprobs `class-attribute` `instance-attribute`

```
top_logprobs: int | None = None
```

Number of top tokens to return logprobs for. Setting this will
automatically include `"message.output_text.logprobs"` in the response.

#### extra\_query `class-attribute` `instance-attribute`

```
extra_query: Query | None = None
```

Additional query fields to provide with the request.
Defaults to None if not provided.

#### extra\_body `class-attribute` `instance-attribute`

```
extra_body: Body | None = None
```

Additional body fields to provide with the request.
Defaults to None if not provided.

#### extra\_headers `class-attribute` `instance-attribute`

```
extra_headers: Headers | None = None
```

Additional headers to provide with the request.
Defaults to None if not provided.

#### extra\_args `class-attribute` `instance-attribute`

```
extra_args: dict[str, Any] | None = None
```

Arbitrary keyword arguments to pass to the model API call.
These will be passed directly to the underlying model provider's API.
Use with caution as not all models support all parameters.

#### retry `class-attribute` `instance-attribute`

```
retry: ModelRetrySettings | None = None
```

Opt-in runner-managed retry settings for model calls.

#### context\_management `class-attribute` `instance-attribute`

```
context_management: list[ContextManagement] | None = None
```

Context management entries for OpenAI Responses API requests.

For example, use `[{"type": "compaction", "compact_threshold": 200000}]`
to enable server-side compaction when the rendered context crosses a token threshold.

#### prompt\_cache\_options `class-attribute` `instance-attribute`

```
prompt_cache_options: PromptCacheOptions | None = None
```

Prompt-cache configuration for OpenAI API requests.

Use `{"mode": "explicit", "ttl": "30m"}` with content-part cache breakpoints to
control which prompt prefixes are eligible for caching.

#### resolve

```
resolve(override: ModelSettings | None) -> ModelSettings
```

Produce a new ModelSettings by overlaying any non-None values from the
override on top of this instance.

Source code in `src/agents/model_settings.py`

|  |  |
| --- | --- |
| ``` 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 ``` | ``` def resolve(self, override: ModelSettings | None) -> ModelSettings:     """Produce a new ModelSettings by overlaying any non-None values from the     override on top of this instance."""     if override is None:         return self      changes = {         field.name: getattr(override, field.name)         for field in fields(self)         if getattr(override, field.name) is not None     }      # Handle extra_args merging specially - merge dictionaries instead of replacing.     if self.extra_args is not None or override.extra_args is not None:         merged_args = {}         if self.extra_args:             merged_args.update(self.extra_args)         if override.extra_args:             merged_args.update(override.extra_args)         changes["extra_args"] = merged_args if merged_args else None      if self.retry is not None or override.retry is not None:         changes["retry"] = _merge_retry_settings(self.retry, override.retry)      return replace(self, **changes) ``` |

#### to\_traceable\_dict

```
to_traceable_dict() -> dict[str, Any]
```

Serialize settings for tracing without provider-specific request extras.

Source code in `src/agents/model_settings.py`

|  |  |
| --- | --- |
| ``` 231 232 233 234 ``` | ``` def to_traceable_dict(self) -> dict[str, Any]:     """Serialize settings for tracing without provider-specific request extras."""     payload = self.to_json_dict()     return {key: payload[key] for key in _TRACEABLE_MODEL_SETTING_FIELDS if key in payload} ``` |