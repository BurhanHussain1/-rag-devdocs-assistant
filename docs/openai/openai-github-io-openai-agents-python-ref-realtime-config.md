---
url: https://openai.github.io/openai-agents-python/ref/realtime/config/
title: Realtime Configuration
framework: openai
---

# Realtime Configuration

## Run Configuration

Bases: `TypedDict`

Configuration for running a realtime agent session.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 ``` | ``` class RealtimeRunConfig(TypedDict):     """Configuration for running a realtime agent session."""      model_settings: NotRequired[RealtimeSessionModelSettings]     """Settings for the realtime model session."""      output_guardrails: NotRequired[list[OutputGuardrail[Any]]]     """List of output guardrails to run on the agent's responses."""      guardrails_settings: NotRequired[RealtimeGuardrailsSettings]     """Settings for guardrail execution."""      tracing_disabled: NotRequired[bool]     """Whether tracing is disabled for this run."""      async_tool_calls: NotRequired[bool]     """Whether function tool calls should run asynchronously. Defaults to True."""      tool_execution: NotRequired[RealtimeToolExecutionConfig]     """SDK-side execution settings for local realtime tool calls."""      tool_error_formatter: NotRequired[ToolErrorFormatter]     """Optional callback that formats tool error messages returned to the model.""" ``` |

### model\_settings `instance-attribute`

```
model_settings: NotRequired[RealtimeSessionModelSettings]
```

Settings for the realtime model session.

### output\_guardrails `instance-attribute`

```
output_guardrails: NotRequired[list[OutputGuardrail[Any]]]
```

List of output guardrails to run on the agent's responses.

### guardrails\_settings `instance-attribute`

```
guardrails_settings: NotRequired[RealtimeGuardrailsSettings]
```

Settings for guardrail execution.

### tracing\_disabled `instance-attribute`

```
tracing_disabled: NotRequired[bool]
```

Whether tracing is disabled for this run.

### async\_tool\_calls `instance-attribute`

```
async_tool_calls: NotRequired[bool]
```

Whether function tool calls should run asynchronously. Defaults to True.

### tool\_execution `instance-attribute`

```
tool_execution: NotRequired[RealtimeToolExecutionConfig]
```

SDK-side execution settings for local realtime tool calls.

### tool\_error\_formatter `instance-attribute`

```
tool_error_formatter: NotRequired[ToolErrorFormatter]
```

Optional callback that formats tool error messages returned to the model.

## Model Settings

Bases: `TypedDict`

Model settings for a realtime model session.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 ``` | ``` class RealtimeSessionModelSettings(TypedDict):     """Model settings for a realtime model session."""      model_name: NotRequired[RealtimeModelName]     """The name of the realtime model to use."""      instructions: NotRequired[str]     """System instructions for the model."""      prompt: NotRequired[Prompt]     """The prompt to use for the model."""      modalities: NotRequired[list[Literal["text", "audio"]]]     """The modalities the model should support."""      output_modalities: NotRequired[list[Literal["text", "audio"]]]     """The output modalities the model should support."""      audio: NotRequired[RealtimeAudioConfig]     """The audio configuration for the session."""      voice: NotRequired[RealtimeVoice]     """The voice to use for audio output."""      speed: NotRequired[float]     """The speed of the model's responses."""      max_output_tokens: NotRequired[int | Literal["inf"]]     """Maximum number of output tokens for a single assistant response, inclusive of tool calls.      Provide an integer between 1 and 4096 to limit output tokens, or ``"inf"`` for the maximum     available tokens for a given model. Defaults to ``"inf"`` server-side.     """      input_audio_format: NotRequired[RealtimeAudioFormat | OpenAIRealtimeAudioFormats]     """The format for input audio streams."""      output_audio_format: NotRequired[RealtimeAudioFormat | OpenAIRealtimeAudioFormats]     """The format for output audio streams."""      input_audio_transcription: NotRequired[RealtimeInputAudioTranscriptionConfig]     """Configuration for transcribing input audio."""      input_audio_noise_reduction: NotRequired[RealtimeInputAudioNoiseReductionConfig | None]     """Noise reduction configuration for input audio."""      turn_detection: NotRequired[RealtimeTurnDetectionConfig]     """Configuration for detecting conversation turns."""      tool_choice: NotRequired[ToolChoice]     """How the model should choose which tools to call."""      parallel_tool_calls: NotRequired[bool]     """Whether the model may make parallel tool calls."""      reasoning: NotRequired[RealtimeReasoningConfig]     """Reasoning configuration for realtime model responses."""      tools: NotRequired[list[Tool]]     """List of tools available to the model."""      handoffs: NotRequired[list[Handoff]]     """List of handoff configurations."""      tracing: NotRequired[RealtimeModelTracingConfig | None]     """Configuration for request tracing.""" ``` |

### model\_name `instance-attribute`

```
model_name: NotRequired[RealtimeModelName]
```

The name of the realtime model to use.

### instructions `instance-attribute`

```
instructions: NotRequired[str]
```

System instructions for the model.

### prompt `instance-attribute`

```
prompt: NotRequired[Prompt]
```

The prompt to use for the model.

### modalities `instance-attribute`

```
modalities: NotRequired[list[Literal['text', 'audio']]]
```

The modalities the model should support.

### output\_modalities `instance-attribute`

```
output_modalities: NotRequired[
    list[Literal["text", "audio"]]
]
```

The output modalities the model should support.

### audio `instance-attribute`

```
audio: NotRequired[RealtimeAudioConfig]
```

The audio configuration for the session.

### voice `instance-attribute`

```
voice: NotRequired[RealtimeVoice]
```

The voice to use for audio output.

### speed `instance-attribute`

```
speed: NotRequired[float]
```

The speed of the model's responses.

### max\_output\_tokens `instance-attribute`

```
max_output_tokens: NotRequired[int | Literal['inf']]
```

Maximum number of output tokens for a single assistant response, inclusive of tool calls.

Provide an integer between 1 and 4096 to limit output tokens, or `"inf"` for the maximum
available tokens for a given model. Defaults to `"inf"` server-side.

### input\_audio\_format `instance-attribute`

```
input_audio_format: NotRequired[
    RealtimeAudioFormat | RealtimeAudioFormats
]
```

The format for input audio streams.

### output\_audio\_format `instance-attribute`

```
output_audio_format: NotRequired[
    RealtimeAudioFormat | RealtimeAudioFormats
]
```

The format for output audio streams.

### input\_audio\_transcription `instance-attribute`

```
input_audio_transcription: NotRequired[
    RealtimeInputAudioTranscriptionConfig
]
```

Configuration for transcribing input audio.

### input\_audio\_noise\_reduction `instance-attribute`

```
input_audio_noise_reduction: NotRequired[
    RealtimeInputAudioNoiseReductionConfig | None
]
```

Noise reduction configuration for input audio.

### turn\_detection `instance-attribute`

```
turn_detection: NotRequired[RealtimeTurnDetectionConfig]
```

Configuration for detecting conversation turns.

### tool\_choice `instance-attribute`

```
tool_choice: NotRequired[ToolChoice]
```

How the model should choose which tools to call.

### parallel\_tool\_calls `instance-attribute`

```
parallel_tool_calls: NotRequired[bool]
```

Whether the model may make parallel tool calls.

### reasoning `instance-attribute`

```
reasoning: NotRequired[RealtimeReasoningConfig]
```

Reasoning configuration for realtime model responses.

### tools `instance-attribute`

```
tools: NotRequired[list[Tool]]
```

List of tools available to the model.

### handoffs `instance-attribute`

```
handoffs: NotRequired[list[Handoff]]
```

List of handoff configurations.

### tracing `instance-attribute`

```
tracing: NotRequired[RealtimeModelTracingConfig | None]
```

Configuration for request tracing.

## Audio Configuration

Bases: `TypedDict`

Configuration for audio transcription in realtime sessions.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 76 77 78 79 80 81 82 83 84 85 86 ``` | ``` class RealtimeInputAudioTranscriptionConfig(TypedDict):     """Configuration for audio transcription in realtime sessions."""      language: NotRequired[str]     """The language code for transcription."""      model: NotRequired[Literal["gpt-4o-transcribe", "gpt-4o-mini-transcribe", "whisper-1"] | str]     """The transcription model to use."""      prompt: NotRequired[str]     """An optional prompt to guide transcription.""" ``` |

### language `instance-attribute`

```
language: NotRequired[str]
```

The language code for transcription.

### model `instance-attribute`

```
model: NotRequired[
    Literal[
        "gpt-4o-transcribe",
        "gpt-4o-mini-transcribe",
        "whisper-1",
    ]
    | str
]
```

The transcription model to use.

### prompt `instance-attribute`

```
prompt: NotRequired[str]
```

An optional prompt to guide transcription.

Bases: `TypedDict`

Noise reduction configuration for input audio.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 89 90 91 92 93 ``` | ``` class RealtimeInputAudioNoiseReductionConfig(TypedDict):     """Noise reduction configuration for input audio."""      type: NotRequired[Literal["near_field", "far_field"]]     """Noise reduction mode to apply to input audio.""" ``` |

### type `instance-attribute`

```
type: NotRequired[Literal['near_field', 'far_field']]
```

Noise reduction mode to apply to input audio.

Bases: `TypedDict`

Turn detection config. Allows extra vendor keys if needed.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ```  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 ``` | ``` class RealtimeTurnDetectionConfig(TypedDict):     """Turn detection config. Allows extra vendor keys if needed."""      type: NotRequired[Literal["semantic_vad", "server_vad"]]     """The type of voice activity detection to use."""      create_response: NotRequired[bool]     """Whether to create a response when a turn is detected."""      eagerness: NotRequired[Literal["auto", "low", "medium", "high"]]     """How eagerly to detect turn boundaries."""      interrupt_response: NotRequired[bool]     """Whether to allow interrupting the assistant's response."""      prefix_padding_ms: NotRequired[int]     """Padding time in milliseconds before turn detection."""      silence_duration_ms: NotRequired[int]     """Duration of silence in milliseconds to trigger turn detection."""      threshold: NotRequired[float]     """The threshold for voice activity detection."""      idle_timeout_ms: NotRequired[int]     """Threshold for server-vad to trigger a response if the user is idle for this duration."""      model_version: NotRequired[str]     """Optional backend-specific VAD model identifier.""" ``` |

### type `instance-attribute`

```
type: NotRequired[Literal['semantic_vad', 'server_vad']]
```

The type of voice activity detection to use.

### create\_response `instance-attribute`

```
create_response: NotRequired[bool]
```

Whether to create a response when a turn is detected.

### eagerness `instance-attribute`

```
eagerness: NotRequired[
    Literal["auto", "low", "medium", "high"]
]
```

How eagerly to detect turn boundaries.

### interrupt\_response `instance-attribute`

```
interrupt_response: NotRequired[bool]
```

Whether to allow interrupting the assistant's response.

### prefix\_padding\_ms `instance-attribute`

```
prefix_padding_ms: NotRequired[int]
```

Padding time in milliseconds before turn detection.

### silence\_duration\_ms `instance-attribute`

```
silence_duration_ms: NotRequired[int]
```

Duration of silence in milliseconds to trigger turn detection.

### threshold `instance-attribute`

```
threshold: NotRequired[float]
```

The threshold for voice activity detection.

### idle\_timeout\_ms `instance-attribute`

```
idle_timeout_ms: NotRequired[int]
```

Threshold for server-vad to trigger a response if the user is idle for this duration.

### model\_version `instance-attribute`

```
model_version: NotRequired[str]
```

Optional backend-specific VAD model identifier.

## Guardrails Settings

Bases: `TypedDict`

Settings for output guardrails in realtime sessions.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 226 227 228 229 230 231 232 233 234 ``` | ``` class RealtimeGuardrailsSettings(TypedDict):     """Settings for output guardrails in realtime sessions."""      debounce_text_length: NotRequired[int]     """     The minimum number of characters to accumulate before running guardrails on transcript     deltas. Defaults to 100. Guardrails run every time the accumulated text reaches     1x, 2x, 3x, etc. times this threshold.     """ ``` |

### debounce\_text\_length `instance-attribute`

```
debounce_text_length: NotRequired[int]
```

The minimum number of characters to accumulate before running guardrails on transcript
deltas. Defaults to 100. Guardrails run every time the accumulated text reaches
1x, 2x, 3x, etc. times this threshold.

## Model Configuration

Bases: `TypedDict`

Options for connecting to a realtime model.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 ``` | ``` class RealtimeModelConfig(TypedDict):     """Options for connecting to a realtime model."""      api_key: NotRequired[str | Callable[[], MaybeAwaitable[str]]]     """The API key (or function that returns a key) to use when connecting. If unset, the model will     try to use a sane default. For example, the OpenAI Realtime model will try to use the     `OPENAI_API_KEY`  environment variable.     """      url: NotRequired[str]     """The URL to use when connecting. If unset, the model will use a sane default. For example,     the OpenAI Realtime model will use the default OpenAI WebSocket URL.     """      headers: NotRequired[dict[str, str]]     """The headers to use when connecting. If unset, the model will use a sane default.     Note that, when you set this, authorization header won't be set under the hood.     e.g., {"api-key": "your api key here"} for Azure OpenAI Realtime WebSocket connections.     """      initial_model_settings: NotRequired[RealtimeSessionModelSettings]     """The initial model settings to use when connecting."""      playback_tracker: NotRequired[RealtimePlaybackTracker]     """The playback tracker to use when tracking audio playback progress. If not set, the model will     use a default implementation that assumes audio is played immediately, at realtime speed.      A playback tracker is useful for interruptions. The model generates audio much faster than     realtime playback speed. So if there's an interruption, its useful for the model to know how     much of the audio has been played by the user. In low-latency scenarios, it's fine to assume     that audio is played back immediately at realtime speed. But in scenarios like phone calls or     other remote interactions, you can set a playback tracker that lets the model know when audio     is played to the user.     """      call_id: NotRequired[str]     """Attach to an existing realtime call instead of creating a new session.      When provided, the transport connects using the `call_id` query string parameter rather than a     model name. In this repository, the shipped example for this flow is SIP via the Realtime     Calls API.     """ ``` |

### api\_key `instance-attribute`

```
api_key: NotRequired[
    str | Callable[[], MaybeAwaitable[str]]
]
```

The API key (or function that returns a key) to use when connecting. If unset, the model will
try to use a sane default. For example, the OpenAI Realtime model will try to use the
`OPENAI_API_KEY` environment variable.

### url `instance-attribute`

```
url: NotRequired[str]
```

The URL to use when connecting. If unset, the model will use a sane default. For example,
the OpenAI Realtime model will use the default OpenAI WebSocket URL.

### headers `instance-attribute`

```
headers: NotRequired[dict[str, str]]
```

The headers to use when connecting. If unset, the model will use a sane default.
Note that, when you set this, authorization header won't be set under the hood.
e.g., {"api-key": "your api key here"} for Azure OpenAI Realtime WebSocket connections.

### initial\_model\_settings `instance-attribute`

```
initial_model_settings: NotRequired[
    RealtimeSessionModelSettings
]
```

The initial model settings to use when connecting.

### playback\_tracker `instance-attribute`

```
playback_tracker: NotRequired[RealtimePlaybackTracker]
```

The playback tracker to use when tracking audio playback progress. If not set, the model will
use a default implementation that assumes audio is played immediately, at realtime speed.

A playback tracker is useful for interruptions. The model generates audio much faster than
realtime playback speed. So if there's an interruption, its useful for the model to know how
much of the audio has been played by the user. In low-latency scenarios, it's fine to assume
that audio is played back immediately at realtime speed. But in scenarios like phone calls or
other remote interactions, you can set a playback tracker that lets the model know when audio
is played to the user.

### call\_id `instance-attribute`

```
call_id: NotRequired[str]
```

Attach to an existing realtime call instead of creating a new session.

When provided, the transport connects using the `call_id` query string parameter rather than a
model name. In this repository, the shipped example for this flow is SIP via the Realtime
Calls API.

## Tracing Configuration

Bases: `TypedDict`

Configuration for tracing in realtime model sessions.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 247 248 249 250 251 252 253 254 255 256 257 ``` | ``` class RealtimeModelTracingConfig(TypedDict):     """Configuration for tracing in realtime model sessions."""      workflow_name: NotRequired[str]     """The workflow name to use for tracing."""      group_id: NotRequired[str]     """A group identifier to use for tracing, to link multiple traces together."""      metadata: NotRequired[dict[str, Any]]     """Additional metadata to include with the trace.""" ``` |

### workflow\_name `instance-attribute`

```
workflow_name: NotRequired[str]
```

The workflow name to use for tracing.

### group\_id `instance-attribute`

```
group_id: NotRequired[str]
```

A group identifier to use for tracing, to link multiple traces together.

### metadata `instance-attribute`

```
metadata: NotRequired[dict[str, Any]]
```

Additional metadata to include with the trace.

## User Input Types

User input that can be a string or structured message.

Bases: `TypedDict`

A text input from the user.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 287 288 289 290 291 292 293 294 ``` | ``` class RealtimeUserInputText(TypedDict):     """A text input from the user."""      type: Literal["input_text"]     """The type identifier for text input."""      text: str     """The text content from the user.""" ``` |

### type `instance-attribute`

```
type: Literal['input_text']
```

The type identifier for text input.

### text `instance-attribute`

```
text: str
```

The text content from the user.

Bases: `TypedDict`

A message input from the user.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 305 306 307 308 309 310 311 312 313 314 315 ``` | ``` class RealtimeUserInputMessage(TypedDict):     """A message input from the user."""      type: Literal["message"]     """The type identifier for message inputs."""      role: Literal["user"]     """The role identifier for user messages."""      content: list[RealtimeUserInputText | RealtimeUserInputImage]     """List of content items (text and image) in the message.""" ``` |

### type `instance-attribute`

```
type: Literal['message']
```

The type identifier for message inputs.

### role `instance-attribute`

```
role: Literal['user']
```

The role identifier for user messages.

### content `instance-attribute`

```
content: list[
    RealtimeUserInputText | RealtimeUserInputImage
]
```

List of content items (text and image) in the message.

## Client Messages

Bases: `TypedDict`

A raw message to be sent to the model.

Source code in `src/agents/realtime/config.py`

|  |  |
| --- | --- |
| ``` 66 67 68 69 70 71 72 73 ``` | ``` class RealtimeClientMessage(TypedDict):     """A raw message to be sent to the model."""      type: str  # explicitly required     """The type of the message."""      other_data: NotRequired[dict[str, Any]]     """Merged into the message body.""" ``` |

### type `instance-attribute`

```
type: str
```

The type of the message.

### other\_data `instance-attribute`

```
other_data: NotRequired[dict[str, Any]]
```

Merged into the message body.

## Type Aliases

The name of a realtime model.

The audio format for realtime audio streams.