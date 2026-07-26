---
url: https://openai.github.io/openai-agents-python/ref/run_config/
title: `Run Config`
framework: openai
---

# `Run Config`

### ModelInputData `dataclass`

Container for the data that will be sent to the model.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 47 48 49 50 51 52 ``` | ``` @dataclass class ModelInputData:     """Container for the data that will be sent to the model."""      input: list[TResponseInputItem]     instructions: str | None ``` |

### CallModelData `dataclass`

Bases: `Generic[TContext]`

Data passed to `RunConfig.call_model_input_filter` prior to model call.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 55 56 57 58 59 60 61 ``` | ``` @dataclass class CallModelData(Generic[TContext]):     """Data passed to `RunConfig.call_model_input_filter` prior to model call."""      model_data: ModelInputData     agent: Agent[TContext]     context: TContext | None ``` |

### ToolErrorFormatterArgs `dataclass`

Bases: `Generic[TContext]`

Data passed to `RunConfig.tool_error_formatter` callbacks.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 ``` | ``` @dataclass class ToolErrorFormatterArgs(Generic[TContext]):     """Data passed to ``RunConfig.tool_error_formatter`` callbacks."""      kind: Literal["approval_rejected", "tool_not_found"]     """The category of tool error being formatted."""      tool_type: Literal["function", "computer", "shell", "apply_patch", "custom"]     """The tool runtime that produced the error."""      tool_name: str     """The name of the tool that produced the error."""      call_id: str     """The unique tool call identifier."""      default_message: str     """The SDK default message for this error kind."""      run_context: RunContextWrapper[TContext]     """The active run context for the current execution.""" ``` |

#### kind `instance-attribute`

```
kind: Literal['approval_rejected', 'tool_not_found']
```

The category of tool error being formatted.

#### tool\_type `instance-attribute`

```
tool_type: Literal[
    "function", "computer", "shell", "apply_patch", "custom"
]
```

The tool runtime that produced the error.

#### tool\_name `instance-attribute`

```
tool_name: str
```

The name of the tool that produced the error.

#### call\_id `instance-attribute`

```
call_id: str
```

The unique tool call identifier.

#### default\_message `instance-attribute`

```
default_message: str
```

The SDK default message for this error kind.

#### run\_context `instance-attribute`

```
run_context: RunContextWrapper[TContext]
```

The active run context for the current execution.

### ToolExecutionConfig `dataclass`

Grouped SDK-side execution settings for local tool calls.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ```  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 ``` | ``` @dataclass class ToolExecutionConfig:     """Grouped SDK-side execution settings for local tool calls."""      max_function_tool_concurrency: int | None = None     """Maximum number of local function tool calls to execute concurrently.      Set to `None` to preserve the default behavior, which starts all function tool calls     emitted in a turn. This does not change provider-side `parallel_tool_calls` behavior.     """      pre_approval_tool_input_guardrails: bool = False     """Run function tool input guardrails before emitting a pending approval interruption.      The same guardrails still run again immediately before tool execution after approval.     """      def __post_init__(self) -> None:         if self.max_function_tool_concurrency is not None and (             self.max_function_tool_concurrency < 1         ):             raise ValueError("tool_execution.max_function_tool_concurrency must be at least 1")         if not isinstance(self.pre_approval_tool_input_guardrails, bool):             raise ValueError("tool_execution.pre_approval_tool_input_guardrails must be a bool") ``` |

#### max\_function\_tool\_concurrency `class-attribute` `instance-attribute`

```
max_function_tool_concurrency: int | None = None
```

Maximum number of local function tool calls to execute concurrently.

Set to `None` to preserve the default behavior, which starts all function tool calls
emitted in a turn. This does not change provider-side `parallel_tool_calls` behavior.

#### pre\_approval\_tool\_input\_guardrails `class-attribute` `instance-attribute`

```
pre_approval_tool_input_guardrails: bool = False
```

Run function tool input guardrails before emitting a pending approval interruption.

The same guardrails still run again immediately before tool execution after approval.

### SandboxConcurrencyLimits `dataclass`

Concurrency limits for sandbox materialization work.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 ``` | ``` @dataclass class SandboxConcurrencyLimits:     """Concurrency limits for sandbox materialization work."""      manifest_entries: int | None = DEFAULT_MAX_MANIFEST_ENTRY_CONCURRENCY     """Maximum number of manifest entries to materialize concurrently per sandbox session.      Set to `None` to disable this manifest entry limit.     """      local_dir_files: int | None = DEFAULT_MAX_LOCAL_DIR_FILE_CONCURRENCY     """Maximum number of files to copy concurrently for each local_dir manifest entry.      Set to `None` to disable this per-local-dir file copy limit.     """      def validate(self) -> None:         if self.manifest_entries is not None and self.manifest_entries < 1:             raise ValueError("concurrency_limits.manifest_entries must be at least 1")         if self.local_dir_files is not None and self.local_dir_files < 1:             raise ValueError("concurrency_limits.local_dir_files must be at least 1") ``` |

#### manifest\_entries `class-attribute` `instance-attribute`

```
manifest_entries: int | None = (
    DEFAULT_MAX_MANIFEST_ENTRY_CONCURRENCY
)
```

Maximum number of manifest entries to materialize concurrently per sandbox session.

Set to `None` to disable this manifest entry limit.

#### local\_dir\_files `class-attribute` `instance-attribute`

```
local_dir_files: int | None = (
    DEFAULT_MAX_LOCAL_DIR_FILE_CONCURRENCY
)
```

Maximum number of files to copy concurrently for each local\_dir manifest entry.

Set to `None` to disable this per-local-dir file copy limit.

### SandboxArchiveLimits `dataclass`

Resource limits for sandbox archive extraction.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 ``` | ``` @dataclass class SandboxArchiveLimits:     """Resource limits for sandbox archive extraction."""      max_input_bytes: int | None = DEFAULT_MAX_ARCHIVE_INPUT_BYTES     """Maximum archive input bytes accepted by `BaseSandboxSession.extract()`.      Set to `None` to disable this input-size limit.     """      max_extracted_bytes: int | None = DEFAULT_MAX_ARCHIVE_EXTRACTED_BYTES     """Maximum declared bytes that an archive may extract.      Set to `None` to disable this extracted-size limit.     """      max_members: int | None = DEFAULT_MAX_ARCHIVE_MEMBERS     """Maximum number of extractable archive members.      Set to `None` to disable this member-count limit.     """      def __post_init__(self) -> None:         self.validate()      def validate(self) -> None:         if self.max_input_bytes is not None and self.max_input_bytes < 1:             raise ValueError("archive_limits.max_input_bytes must be at least 1")         if self.max_extracted_bytes is not None and self.max_extracted_bytes < 1:             raise ValueError("archive_limits.max_extracted_bytes must be at least 1")         if self.max_members is not None and self.max_members < 1:             raise ValueError("archive_limits.max_members must be at least 1") ``` |

#### max\_input\_bytes `class-attribute` `instance-attribute`

```
max_input_bytes: int | None = (
    DEFAULT_MAX_ARCHIVE_INPUT_BYTES
)
```

Maximum archive input bytes accepted by `BaseSandboxSession.extract()`.

Set to `None` to disable this input-size limit.

#### max\_extracted\_bytes `class-attribute` `instance-attribute`

```
max_extracted_bytes: int | None = (
    DEFAULT_MAX_ARCHIVE_EXTRACTED_BYTES
)
```

Maximum declared bytes that an archive may extract.

Set to `None` to disable this extracted-size limit.

#### max\_members `class-attribute` `instance-attribute`

```
max_members: int | None = DEFAULT_MAX_ARCHIVE_MEMBERS
```

Maximum number of extractable archive members.

Set to `None` to disable this member-count limit.

### SandboxRunConfig `dataclass`

Grouped sandbox runtime configuration for `Runner`.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 ``` | ``` @dataclass class SandboxRunConfig:     """Grouped sandbox runtime configuration for `Runner`."""      client: BaseSandboxClient[Any] | None = None     """Sandbox client used to create or resume sandbox sessions."""      options: Any | None = None     """Sandbox-client-specific options used when creating a fresh session."""      session: BaseSandboxSession | None = None     """Live sandbox session override for the current process."""      session_state: SandboxSessionState | None = None     """Explicit sandbox session state to resume from when not using `RunState` payloads."""      manifest: Manifest | None = None     """Optional sandbox manifest override for fresh session creation."""      snapshot: SnapshotSpec | SnapshotBase | None = None     """Optional sandbox snapshot used for fresh session creation."""      concurrency_limits: SandboxConcurrencyLimits = field(default_factory=SandboxConcurrencyLimits)     """Concurrency limits for sandbox materialization work."""      archive_limits: SandboxArchiveLimits | None = None     """Resource limits for sandbox archive extraction.      Set to `None` to preserve the default behavior with no SDK archive resource limits.     Use `SandboxArchiveLimits()` to enable SDK defaults.     """ ``` |

#### client `class-attribute` `instance-attribute`

```
client: BaseSandboxClient[Any] | None = None
```

Sandbox client used to create or resume sandbox sessions.

#### options `class-attribute` `instance-attribute`

```
options: Any | None = None
```

Sandbox-client-specific options used when creating a fresh session.

#### session `class-attribute` `instance-attribute`

```
session: BaseSandboxSession | None = None
```

Live sandbox session override for the current process.

#### session\_state `class-attribute` `instance-attribute`

```
session_state: SandboxSessionState | None = None
```

Explicit sandbox session state to resume from when not using `RunState` payloads.

#### manifest `class-attribute` `instance-attribute`

```
manifest: Manifest | None = None
```

Optional sandbox manifest override for fresh session creation.

#### snapshot `class-attribute` `instance-attribute`

```
snapshot: SnapshotSpec | SnapshotBase | None = None
```

Optional sandbox snapshot used for fresh session creation.

#### concurrency\_limits `class-attribute` `instance-attribute`

```
concurrency_limits: SandboxConcurrencyLimits = field(
    default_factory=SandboxConcurrencyLimits
)
```

Concurrency limits for sandbox materialization work.

#### archive\_limits `class-attribute` `instance-attribute`

```
archive_limits: SandboxArchiveLimits | None = None
```

Resource limits for sandbox archive extraction.

Set to `None` to preserve the default behavior with no SDK archive resource limits.
Use `SandboxArchiveLimits()` to enable SDK defaults.

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

### RunOptions

Bases: `TypedDict`, `Generic[TContext]`

Arguments for `AgentRunner` methods.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 ``` | ``` class RunOptions(TypedDict, Generic[TContext]):     """Arguments for ``AgentRunner`` methods."""      context: NotRequired[TContext | None]     """The context for the run."""      max_turns: NotRequired[int | None]     """The maximum number of turns to run for. Set to ``None`` to disable the limit."""      hooks: NotRequired[RunHooks[TContext] | None]     """Lifecycle hooks for the run."""      run_config: NotRequired[RunConfig | None]     """Run configuration."""      previous_response_id: NotRequired[str | None]     """The ID of the previous response, if any."""      auto_previous_response_id: NotRequired[bool]     """Enable automatic response chaining for the first turn."""      conversation_id: NotRequired[str | None]     """The ID of the stored conversation, if any."""      session: NotRequired[Session | None]     """The session for the run."""      error_handlers: NotRequired[RunErrorHandlers[TContext] | None]     """Error handlers keyed by error kind.""" ``` |

#### context `instance-attribute`

```
context: NotRequired[TContext | None]
```

The context for the run.

#### max\_turns `instance-attribute`

```
max_turns: NotRequired[int | None]
```

The maximum number of turns to run for. Set to `None` to disable the limit.

#### hooks `instance-attribute`

```
hooks: NotRequired[RunHooks[TContext] | None]
```

Lifecycle hooks for the run.

#### run\_config `instance-attribute`

```
run_config: NotRequired[RunConfig | None]
```

Run configuration.

#### previous\_response\_id `instance-attribute`

```
previous_response_id: NotRequired[str | None]
```

The ID of the previous response, if any.

#### auto\_previous\_response\_id `instance-attribute`

```
auto_previous_response_id: NotRequired[bool]
```

Enable automatic response chaining for the first turn.

#### conversation\_id `instance-attribute`

```
conversation_id: NotRequired[str | None]
```

The ID of the stored conversation, if any.

#### session `instance-attribute`

```
session: NotRequired[Session | None]
```

The session for the run.

#### error\_handlers `instance-attribute`

```
error_handlers: NotRequired[
    RunErrorHandlers[TContext] | None
]
```

Error handlers keyed by error kind.