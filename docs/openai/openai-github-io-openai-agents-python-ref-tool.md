---
url: https://openai.github.io/openai-agents-python/ref/tool/
title: `Tools`
framework: openai
---

# `Tools`

### MCPToolApprovalFunction `module-attribute`

```
MCPToolApprovalFunction = Callable[
    [MCPToolApprovalRequest],
    MaybeAwaitable[MCPToolApprovalFunctionResult],
]
```

A function that approves or rejects a tool call.

### ShellApprovalFunction `module-attribute`

```
ShellApprovalFunction = Callable[
    [RunContextWrapper[Any], "ShellActionRequest", str],
    MaybeAwaitable[bool],
]
```

A function that determines whether a shell action requires approval.
Takes (run\_context, action, call\_id) and returns whether approval is needed.

### ShellOnApprovalFunction `module-attribute`

```
ShellOnApprovalFunction = Callable[
    [RunContextWrapper[Any], "ToolApprovalItem"],
    MaybeAwaitable[ShellOnApprovalFunctionResult],
]
```

A function that auto-approves or rejects a shell tool call when approval is needed.
Takes (run\_context, approval\_item) and returns approval decision.

### ApplyPatchApprovalFunction `module-attribute`

```
ApplyPatchApprovalFunction = Callable[
    [RunContextWrapper[Any], ApplyPatchOperation, str],
    MaybeAwaitable[bool],
]
```

A function that determines whether an apply\_patch operation requires approval.
Takes (run\_context, operation, call\_id) and returns whether approval is needed.

### ApplyPatchOnApprovalFunction `module-attribute`

```
ApplyPatchOnApprovalFunction = Callable[
    [RunContextWrapper[Any], "ToolApprovalItem"],
    MaybeAwaitable[ApplyPatchOnApprovalFunctionResult],
]
```

A function that auto-approves or rejects an apply\_patch tool call when approval is needed.
Takes (run\_context, approval\_item) and returns approval decision.

### CustomToolOnApprovalFunction `module-attribute`

```
CustomToolOnApprovalFunction = Callable[
    [RunContextWrapper[Any], "ToolApprovalItem"],
    MaybeAwaitable[CustomToolOnApprovalFunctionResult],
]
```

A function that auto-approves or rejects a custom tool call when approval is needed.
Takes (run\_context, approval\_item) and returns approval decision.

### LocalShellExecutor `module-attribute`

```
LocalShellExecutor = Callable[
    [LocalShellCommandRequest], MaybeAwaitable[str]
]
```

A function that executes a command on a shell.

### ShellToolContainerSkill `module-attribute`

```
ShellToolContainerSkill = (
    ShellToolSkillReference | ShellToolInlineSkill
)
```

Container skill configuration.

### ShellToolContainerNetworkPolicy `module-attribute`

```
ShellToolContainerNetworkPolicy = (
    ShellToolContainerNetworkPolicyAllowlist
    | ShellToolContainerNetworkPolicyDisabled
)
```

Network policy configuration for hosted shell containers.

### ShellToolHostedEnvironment `module-attribute`

```
ShellToolHostedEnvironment = (
    ShellToolContainerAutoEnvironment
    | ShellToolContainerReferenceEnvironment
)
```

Hosted shell environment variants.

### ShellToolEnvironment `module-attribute`

```
ShellToolEnvironment = (
    ShellToolLocalEnvironment | ShellToolHostedEnvironment
)
```

All supported shell environments.

### ShellExecutor `module-attribute`

```
ShellExecutor = Callable[
    [ShellCommandRequest], MaybeAwaitable[str | ShellResult]
]
```

Executes a shell command sequence and returns either text or structured output.

### Tool `module-attribute`

```
Tool = (
    FunctionTool
    | FileSearchTool
    | WebSearchTool
    | ComputerTool[Any]
    | HostedMCPTool
    | CustomTool
    | ShellTool
    | ApplyPatchTool
    | LocalShellTool
    | ImageGenerationTool
    | CodeInterpreterTool
    | ToolSearchTool
    | ProgrammaticToolCallingTool
)
```

A tool that can be used in an agent.

### FunctionToolCustomDataContext `dataclass`

Context passed to function-tool custom data extractors.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 ``` | ``` @dataclass(frozen=True) class FunctionToolCustomDataContext:     """Context passed to function-tool custom data extractors."""      tool_context: ToolContext[Any]     """The tool invocation context."""      tool: FunctionTool     """The function tool that was invoked."""      output: Any     """The model-visible tool output."""      raw_item: Mapping[str, Any]     """The raw tool output item that will be replayed to the model.""" ``` |

#### tool\_context `instance-attribute`

```
tool_context: ToolContext[Any]
```

The tool invocation context.

#### tool `instance-attribute`

```
tool: FunctionTool
```

The function tool that was invoked.

#### output `instance-attribute`

```
output: Any
```

The model-visible tool output.

#### raw\_item `instance-attribute`

```
raw_item: Mapping[str, Any]
```

The raw tool output item that will be replayed to the model.

### CustomToolCustomDataContext `dataclass`

Context passed to custom-tool custom data extractors.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 ``` | ``` @dataclass(frozen=True) class CustomToolCustomDataContext:     """Context passed to custom-tool custom data extractors."""      tool_context: ToolContext[Any]     """The tool invocation context."""      tool: CustomTool     """The custom tool that was invoked."""      input: str     """The raw model-provided custom tool input."""      output: str     """The model-visible custom tool output."""      raw_item: Mapping[str, Any]     """The raw custom tool output item that will be replayed to the model.""" ``` |

#### tool\_context `instance-attribute`

```
tool_context: ToolContext[Any]
```

The tool invocation context.

#### tool `instance-attribute`

```
tool: CustomTool
```

The custom tool that was invoked.

#### input `instance-attribute`

```
input: str
```

The raw model-provided custom tool input.

#### output `instance-attribute`

```
output: str
```

The model-visible custom tool output.

#### raw\_item `instance-attribute`

```
raw_item: Mapping[str, Any]
```

The raw custom tool output item that will be replayed to the model.

### ComputerToolCustomDataContext `dataclass`

Context passed to computer-tool custom data extractors.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 ``` | ``` @dataclass(frozen=True) class ComputerToolCustomDataContext:     """Context passed to computer-tool custom data extractors."""      run_context: RunContextWrapper[Any]     """The current run context."""      tool: ComputerTool[Any]     """The computer tool that was invoked."""      tool_call: ResponseComputerToolCall     """The computer tool call produced by the model."""      output: str     """The screenshot data URL returned to the model."""      raw_item: Any     """The raw computer call output item that will be replayed to the model.""" ``` |

#### run\_context `instance-attribute`

```
run_context: RunContextWrapper[Any]
```

The current run context.

#### tool `instance-attribute`

```
tool: ComputerTool[Any]
```

The computer tool that was invoked.

#### tool\_call `instance-attribute`

```
tool_call: ResponseComputerToolCall
```

The computer tool call produced by the model.

#### output `instance-attribute`

```
output: str
```

The screenshot data URL returned to the model.

#### raw\_item `instance-attribute`

```
raw_item: Any
```

The raw computer call output item that will be replayed to the model.

### ApplyPatchToolCustomDataContext `dataclass`

Context passed to apply-patch custom data extractors.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 ``` | ``` @dataclass(frozen=True) class ApplyPatchToolCustomDataContext:     """Context passed to apply-patch custom data extractors."""      run_context: RunContextWrapper[Any]     """The current run context."""      tool: ApplyPatchTool     """The apply_patch tool that was invoked."""      operations: list[ApplyPatchOperation]     """The patch operations requested by the model."""      output: str     """The model-visible apply_patch output."""      status: Literal["completed", "failed"]     """The serialized apply_patch output status."""      raw_item: Mapping[str, Any]     """The raw apply_patch output item that will be replayed to the model.""" ``` |

#### run\_context `instance-attribute`

```
run_context: RunContextWrapper[Any]
```

The current run context.

#### tool `instance-attribute`

```
tool: ApplyPatchTool
```

The apply\_patch tool that was invoked.

#### operations `instance-attribute`

```
operations: list[ApplyPatchOperation]
```

The patch operations requested by the model.

#### output `instance-attribute`

```
output: str
```

The model-visible apply\_patch output.

#### status `instance-attribute`

```
status: Literal['completed', 'failed']
```

The serialized apply\_patch output status.

#### raw\_item `instance-attribute`

```
raw_item: Mapping[str, Any]
```

The raw apply\_patch output item that will be replayed to the model.

### ToolOutputText

Bases: `BaseModel`

Represents a tool output that should be sent to the model as text.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 192 193 194 195 196 ``` | ``` class ToolOutputText(BaseModel):     """Represents a tool output that should be sent to the model as text."""      type: Literal["text"] = "text"     text: str ``` |

### ToolOutputTextDict

Bases: `TypedDict`

TypedDict variant for text tool outputs.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 199 200 201 202 203 ``` | ``` class ToolOutputTextDict(TypedDict, total=False):     """TypedDict variant for text tool outputs."""      type: Literal["text"]     text: str ``` |

### ToolOutputImage

Bases: `BaseModel`

Represents a tool output that should be sent to the model as an image.

You can provide either an `image_url` (URL or data URL) or a `file_id` for previously uploaded
content. The optional `detail` can control vision detail.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 ``` | ``` class ToolOutputImage(BaseModel):     """Represents a tool output that should be sent to the model as an image.      You can provide either an `image_url` (URL or data URL) or a `file_id` for previously uploaded     content. The optional `detail` can control vision detail.     """      type: Literal["image"] = "image"     image_url: str | None = None     file_id: str | None = None     detail: Literal["low", "high", "auto"] | None = None      @model_validator(mode="after")     def check_at_least_one_required_field(self) -> ToolOutputImage:         """Validate that at least one of image_url or file_id is provided."""         if self.image_url is None and self.file_id is None:             raise ValueError("At least one of image_url or file_id must be provided")         return self ``` |

#### check\_at\_least\_one\_required\_field

```
check_at_least_one_required_field() -> ToolOutputImage
```

Validate that at least one of image\_url or file\_id is provided.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 218 219 220 221 222 223 ``` | ``` @model_validator(mode="after") def check_at_least_one_required_field(self) -> ToolOutputImage:     """Validate that at least one of image_url or file_id is provided."""     if self.image_url is None and self.file_id is None:         raise ValueError("At least one of image_url or file_id must be provided")     return self ``` |

### ToolOutputImageDict

Bases: `TypedDict`

TypedDict variant for image tool outputs.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 226 227 228 229 230 231 232 ``` | ``` class ToolOutputImageDict(TypedDict, total=False):     """TypedDict variant for image tool outputs."""      type: Literal["image"]     image_url: NotRequired[str]     file_id: NotRequired[str]     detail: NotRequired[Literal["low", "high", "auto"]] ``` |

### ToolOutputFileContent

Bases: `BaseModel`

Represents a tool output that should be sent to the model as a file.

Provide one of `file_data` (base64), `file_url`, or `file_id`. You may also
provide an optional `filename` when using `file_data` to hint file name.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 ``` | ``` class ToolOutputFileContent(BaseModel):     """Represents a tool output that should be sent to the model as a file.      Provide one of `file_data` (base64), `file_url`, or `file_id`. You may also     provide an optional `filename` when using `file_data` to hint file name.     """      type: Literal["file"] = "file"     file_data: str | None = None     file_url: str | None = None     file_id: str | None = None     filename: str | None = None      @model_validator(mode="after")     def check_at_least_one_required_field(self) -> ToolOutputFileContent:         """Validate that at least one of file_data, file_url, or file_id is provided."""         if self.file_data is None and self.file_url is None and self.file_id is None:             raise ValueError("At least one of file_data, file_url, or file_id must be provided")         return self ``` |

#### check\_at\_least\_one\_required\_field

```
check_at_least_one_required_field() -> (
    ToolOutputFileContent
)
```

Validate that at least one of file\_data, file\_url, or file\_id is provided.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 248 249 250 251 252 253 ``` | ``` @model_validator(mode="after") def check_at_least_one_required_field(self) -> ToolOutputFileContent:     """Validate that at least one of file_data, file_url, or file_id is provided."""     if self.file_data is None and self.file_url is None and self.file_id is None:         raise ValueError("At least one of file_data, file_url, or file_id must be provided")     return self ``` |

### ToolOutputFileContentDict

Bases: `TypedDict`

TypedDict variant for file content tool outputs.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 256 257 258 259 260 261 262 263 ``` | ``` class ToolOutputFileContentDict(TypedDict, total=False):     """TypedDict variant for file content tool outputs."""      type: Literal["file"]     file_data: NotRequired[str]     file_url: NotRequired[str]     file_id: NotRequired[str]     filename: NotRequired[str] ``` |

### ToolOriginType

Bases: `str`, `Enum`

Enumerates the runtime source of a function-tool-backed run item.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 272 273 274 275 276 277 ``` | ``` class ToolOriginType(str, Enum):     """Enumerates the runtime source of a function-tool-backed run item."""      FUNCTION = "function"     MCP = "mcp"     AGENT_AS_TOOL = "agent_as_tool" ``` |

### ToolOrigin `dataclass`

Serializable metadata describing where a function-tool-backed item came from.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 ``` | ``` @dataclass(frozen=True) class ToolOrigin:     """Serializable metadata describing where a function-tool-backed item came from."""      type: ToolOriginType     mcp_server_name: str | None = None     agent_name: str | None = None     agent_tool_name: str | None = None      def to_json_dict(self) -> dict[str, str]:         """Convert the metadata to a JSON-compatible dict."""         result: dict[str, str] = {"type": self.type.value}         if self.mcp_server_name is not None:             result["mcp_server_name"] = self.mcp_server_name         if self.agent_name is not None:             result["agent_name"] = self.agent_name         if self.agent_tool_name is not None:             result["agent_tool_name"] = self.agent_tool_name         return result      @classmethod     def from_json_dict(cls, data: Any) -> ToolOrigin | None:         """Deserialize tool origin metadata from JSON-compatible data."""         if not isinstance(data, Mapping):             return None          raw_type = data.get("type")         if not isinstance(raw_type, str):             return None          try:             origin_type = ToolOriginType(raw_type)         except ValueError:             return None          def _optional_string(key: str) -> str | None:             value = data.get(key)             return value if isinstance(value, str) else None          return cls(             type=origin_type,             mcp_server_name=_optional_string("mcp_server_name"),             agent_name=_optional_string("agent_name"),             agent_tool_name=_optional_string("agent_tool_name"),         ) ``` |

#### to\_json\_dict

```
to_json_dict() -> dict[str, str]
```

Convert the metadata to a JSON-compatible dict.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 289 290 291 292 293 294 295 296 297 298 ``` | ``` def to_json_dict(self) -> dict[str, str]:     """Convert the metadata to a JSON-compatible dict."""     result: dict[str, str] = {"type": self.type.value}     if self.mcp_server_name is not None:         result["mcp_server_name"] = self.mcp_server_name     if self.agent_name is not None:         result["agent_name"] = self.agent_name     if self.agent_tool_name is not None:         result["agent_tool_name"] = self.agent_tool_name     return result ``` |

#### from\_json\_dict `classmethod`

```
from_json_dict(data: Any) -> ToolOrigin | None
```

Deserialize tool origin metadata from JSON-compatible data.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 ``` | ``` @classmethod def from_json_dict(cls, data: Any) -> ToolOrigin | None:     """Deserialize tool origin metadata from JSON-compatible data."""     if not isinstance(data, Mapping):         return None      raw_type = data.get("type")     if not isinstance(raw_type, str):         return None      try:         origin_type = ToolOriginType(raw_type)     except ValueError:         return None      def _optional_string(key: str) -> str | None:         value = data.get(key)         return value if isinstance(value, str) else None      return cls(         type=origin_type,         mcp_server_name=_optional_string("mcp_server_name"),         agent_name=_optional_string("agent_name"),         agent_tool_name=_optional_string("agent_tool_name"),     ) ``` |

### ComputerCreate

Bases: `Protocol[ComputerT_co]`

Initializes a computer for the current run context.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 333 334 335 336 ``` | ``` class ComputerCreate(Protocol[ComputerT_co]):     """Initializes a computer for the current run context."""      def __call__(self, *, run_context: RunContextWrapper[Any]) -> MaybeAwaitable[ComputerT_co]: ... ``` |

### ComputerDispose

Bases: `Protocol[ComputerT_contra]`

Cleans up a computer initialized for a run context.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 339 340 341 342 343 344 345 346 347 ``` | ``` class ComputerDispose(Protocol[ComputerT_contra]):     """Cleans up a computer initialized for a run context."""      def __call__(         self,         *,         run_context: RunContextWrapper[Any],         computer: ComputerT_contra,     ) -> MaybeAwaitable[None]: ... ``` |

### ComputerProvider `dataclass`

Bases: `Generic[ComputerT]`

Configures create/dispose hooks for per-run computer lifecycle management.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 350 351 352 353 354 355 ``` | ``` @dataclass class ComputerProvider(Generic[ComputerT]):     """Configures create/dispose hooks for per-run computer lifecycle management."""      create: ComputerCreate[ComputerT]     dispose: ComputerDispose[ComputerT] | None = None ``` |

### FunctionToolResult `dataclass`

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 ``` | ``` @dataclass class FunctionToolResult:     tool: FunctionTool     """The tool that was run."""      output: Any     """The output of the tool."""      run_item: RunItem | None     """The run item that was produced as a result of the tool call.      This can be None when the tool run is interrupted and no output item should be emitted yet.     """      interruptions: list[ToolApprovalItem] = field(default_factory=list)     """Interruptions from nested agent runs (for agent-as-tool)."""      agent_run_result: Any = None  # RunResult | None, but avoid circular import     """Nested agent run result (for agent-as-tool).""" ``` |

#### tool `instance-attribute`

```
tool: FunctionTool
```

The tool that was run.

#### output `instance-attribute`

```
output: Any
```

The output of the tool.

#### run\_item `instance-attribute`

```
run_item: RunItem | None
```

The run item that was produced as a result of the tool call.

This can be None when the tool run is interrupted and no output item should be emitted yet.

#### interruptions `class-attribute` `instance-attribute`

```
interruptions: list[ToolApprovalItem] = field(
    default_factory=list
)
```

Interruptions from nested agent runs (for agent-as-tool).

#### agent\_run\_result `class-attribute` `instance-attribute`

```
agent_run_result: Any = None
```

Nested agent run result (for agent-as-tool).

### FunctionTool `dataclass`

A tool that wraps a function. In most cases, you should use the `function_tool` helpers to
create a FunctionTool, as they let you easily wrap a Python function.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 ``` | ``` @dataclass class FunctionTool:     """A tool that wraps a function. In most cases, you should use  the `function_tool` helpers to     create a FunctionTool, as they let you easily wrap a Python function.     """      name: str     """The name of the tool, as shown to the LLM. Generally the name of the function."""      description: str     """A description of the tool, as shown to the LLM."""      params_json_schema: dict[str, Any]     """The JSON schema for the tool's parameters."""      on_invoke_tool: Callable[[ToolContext[Any], str], Awaitable[Any]]     """A function that invokes the tool with the given context and parameters. The params passed     are:     1. The tool run context.     2. The arguments from the LLM, as a JSON string.      You must return one of the structured tool output types (e.g. ToolOutputText, ToolOutputImage,     ToolOutputFileContent) or a string representation of the tool output, or a list of them,     or something we can call `str()` on.     In case of errors, you can either raise an Exception (which will cause the run to fail) or     return a string error message (which will be sent back to the LLM).     """      strict_json_schema: bool = True     """Whether the JSON schema is in strict mode. We **strongly** recommend setting this to True,     as it increases the likelihood of correct JSON input."""      is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase], MaybeAwaitable[bool]] = True     """Whether the tool is enabled. Either a bool or a Callable that takes the run context and agent     and returns whether the tool is enabled. You can use this to dynamically enable/disable a tool     based on your context/state."""      # Keep guardrail fields before needs_approval to preserve v0.7.0 positional     # constructor compatibility for public FunctionTool callers.     # Tool-specific guardrails.     tool_input_guardrails: list[ToolInputGuardrail[Any]] | None = None     """Optional list of input guardrails to run before invoking this tool."""      tool_output_guardrails: list[ToolOutputGuardrail[Any]] | None = None     """Optional list of output guardrails to run after invoking this tool."""      needs_approval: (         bool | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]]     ) = False     """Whether the tool needs approval before execution. If True, the run will be interrupted     and the tool call will need to be approved using RunState.approve() or rejected using     RunState.reject() before continuing. Can be a bool (always/never needs approval) or a     function that takes (run_context, tool_parameters, call_id) and returns whether this     specific call needs approval."""      # Keep timeout fields after needs_approval to preserve positional constructor compatibility.     timeout_seconds: float | None = None     """Optional timeout (seconds) for each tool invocation."""      timeout_behavior: ToolTimeoutBehavior = "error_as_result"     """How to handle timeout events.      - "error_as_result": return a model-visible timeout error string.     - "raise_exception": raise a ToolTimeoutError and fail the run.     """      timeout_error_function: ToolErrorFunction | None = None     """Optional formatter for timeout errors when timeout_behavior is "error_as_result"."""      defer_loading: bool = False     """Whether the Responses API should hide this tool definition until tool search loads it."""      custom_data_extractor: FunctionToolCustomDataExtractor | None = field(         default=None,         kw_only=True,     )     """Optional callback that attaches SDK-only custom data to the tool output item."""      allowed_callers: list[ToolCaller] | None = field(default=None, kw_only=True)     """Callers that may invoke this tool on OpenAI Responses models."""      output_json_schema: dict[str, Any] | None = field(default=None, kw_only=True)     """Optional JSON Schema describing this tool's output for programmatic callers."""      _output_type_adapter: TypeAdapter[Any] | None = field(         default=None,         kw_only=True,         repr=False,     )     """Internal adapter used to validate and JSON-serialize typed function outputs."""      _failure_error_function: ToolErrorFunction | None = field(         default=None,         kw_only=True,         repr=False,     )     """Internal error formatter metadata used for synthetic tool-failure outputs."""      _use_default_failure_error_function: bool = field(         default=True,         kw_only=True,         repr=False,     )     """Whether runtime-generated tool failures should use the default formatter."""      _is_agent_tool: bool = field(default=False, kw_only=True, repr=False)     """Internal flag indicating if this tool is an agent-as-tool."""      _is_codex_tool: bool = field(default=False, kw_only=True, repr=False)     """Internal flag indicating if this tool is a Codex tool wrapper."""      _agent_instance: Any = field(default=None, kw_only=True, repr=False)     """Internal reference to the agent instance if this is an agent-as-tool."""      _tool_namespace: str | None = field(default=None, kw_only=True, repr=False)     """Internal namespace metadata used to group function tools for the Responses API."""      _tool_namespace_description: str | None = field(default=None, kw_only=True, repr=False)     """Internal namespace description used when serializing grouped function tools."""      _mcp_title: str | None = field(default=None, kw_only=True, repr=False)     """Internal MCP display title used for ToolCallItem metadata."""      _tool_origin: ToolOrigin | None = field(default=None, kw_only=True, repr=False)     """Internal scalar metadata describing the origin of function-tool-backed items."""      _emit_tool_origin: bool = field(default=True, kw_only=True, repr=False)     """Whether runtime item generation should emit tool origin metadata for this tool."""      @property     def qualified_name(self) -> str:         """Return the public qualified name used to identify this function tool."""         return (             tool_qualified_name(self.name, get_explicit_function_tool_namespace(self)) or self.name         )      def __post_init__(self):         self.allowed_callers = _normalize_tool_allowed_callers(             self.allowed_callers,             tool_name=self.qualified_name,         )         if self.output_json_schema is not None:             self.output_json_schema = _normalize_function_tool_output_json_schema(                 self.output_json_schema             )         bind_to_function_tool = getattr(self.on_invoke_tool, "__agents_bind_function_tool__", None)         if callable(bind_to_function_tool):             self.on_invoke_tool = bind_to_function_tool(self)         if self.strict_json_schema:             self.params_json_schema = ensure_strict_json_schema(                 copy.deepcopy(self.params_json_schema)             )         _validate_function_tool_timeout_config(self)      def __copy__(self) -> FunctionTool:         copied_tool = dataclasses.replace(self)         dataclass_field_names = {tool_field.name for tool_field in dataclasses.fields(FunctionTool)}         for tool_field in dataclasses.fields(FunctionTool):             if tool_field.init:                 continue             setattr(copied_tool, tool_field.name, getattr(self, tool_field.name))         for attr_name, attr_value in self.__dict__.items():             if attr_name not in dataclass_field_names:                 setattr(copied_tool, attr_name, attr_value)         return copied_tool ``` |

#### name `instance-attribute`

```
name: str
```

The name of the tool, as shown to the LLM. Generally the name of the function.

#### description `instance-attribute`

```
description: str
```

A description of the tool, as shown to the LLM.

#### params\_json\_schema `instance-attribute`

```
params_json_schema: dict[str, Any]
```

The JSON schema for the tool's parameters.

#### on\_invoke\_tool `instance-attribute`

```
on_invoke_tool: Callable[
    [ToolContext[Any], str], Awaitable[Any]
]
```

A function that invokes the tool with the given context and parameters. The params passed
are:
1. The tool run context.
2. The arguments from the LLM, as a JSON string.

You must return one of the structured tool output types (e.g. ToolOutputText, ToolOutputImage,
ToolOutputFileContent) or a string representation of the tool output, or a list of them,
or something we can call `str()` on.
In case of errors, you can either raise an Exception (which will cause the run to fail) or
return a string error message (which will be sent back to the LLM).

#### strict\_json\_schema `class-attribute` `instance-attribute`

```
strict_json_schema: bool = True
```

Whether the JSON schema is in strict mode. We **strongly** recommend setting this to True,
as it increases the likelihood of correct JSON input.

#### is\_enabled `class-attribute` `instance-attribute`

```
is_enabled: (
    bool
    | Callable[
        [RunContextWrapper[Any], AgentBase],
        MaybeAwaitable[bool],
    ]
) = True
```

Whether the tool is enabled. Either a bool or a Callable that takes the run context and agent
and returns whether the tool is enabled. You can use this to dynamically enable/disable a tool
based on your context/state.

#### tool\_input\_guardrails `class-attribute` `instance-attribute`

```
tool_input_guardrails: (
    list[ToolInputGuardrail[Any]] | None
) = None
```

Optional list of input guardrails to run before invoking this tool.

#### tool\_output\_guardrails `class-attribute` `instance-attribute`

```
tool_output_guardrails: (
    list[ToolOutputGuardrail[Any]] | None
) = None
```

Optional list of output guardrails to run after invoking this tool.

#### needs\_approval `class-attribute` `instance-attribute`

```
needs_approval: (
    bool
    | Callable[
        [RunContextWrapper[Any], dict[str, Any], str],
        Awaitable[bool],
    ]
) = False
```

Whether the tool needs approval before execution. If True, the run will be interrupted
and the tool call will need to be approved using RunState.approve() or rejected using
RunState.reject() before continuing. Can be a bool (always/never needs approval) or a
function that takes (run\_context, tool\_parameters, call\_id) and returns whether this
specific call needs approval.

#### timeout\_seconds `class-attribute` `instance-attribute`

```
timeout_seconds: float | None = None
```

Optional timeout (seconds) for each tool invocation.

#### timeout\_behavior `class-attribute` `instance-attribute`

```
timeout_behavior: ToolTimeoutBehavior = 'error_as_result'
```

How to handle timeout events.

* "error\_as\_result": return a model-visible timeout error string.
* "raise\_exception": raise a ToolTimeoutError and fail the run.

#### timeout\_error\_function `class-attribute` `instance-attribute`

```
timeout_error_function: ToolErrorFunction | None = None
```

Optional formatter for timeout errors when timeout\_behavior is "error\_as\_result".

#### defer\_loading `class-attribute` `instance-attribute`

```
defer_loading: bool = False
```

Whether the Responses API should hide this tool definition until tool search loads it.

#### custom\_data\_extractor `class-attribute` `instance-attribute`

```
custom_data_extractor: (
    FunctionToolCustomDataExtractor | None
) = field(default=None, kw_only=True)
```

Optional callback that attaches SDK-only custom data to the tool output item.

#### allowed\_callers `class-attribute` `instance-attribute`

```
allowed_callers: list[ToolCaller] | None = field(
    default=None, kw_only=True
)
```

Callers that may invoke this tool on OpenAI Responses models.

#### output\_json\_schema `class-attribute` `instance-attribute`

```
output_json_schema: dict[str, Any] | None = field(
    default=None, kw_only=True
)
```

Optional JSON Schema describing this tool's output for programmatic callers.

#### qualified\_name `property`

```
qualified_name: str
```

Return the public qualified name used to identify this function tool.

### FileSearchTool `dataclass`

A hosted tool that lets the LLM search through a vector store. Currently only supported with
OpenAI models, using the Responses API.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 ``` | ``` @dataclass class FileSearchTool:     """A hosted tool that lets the LLM search through a vector store. Currently only supported with     OpenAI models, using the Responses API.     """      vector_store_ids: list[str]     """The IDs of the vector stores to search."""      max_num_results: int | None = None     """The maximum number of results to return."""      include_search_results: bool = False     """Whether to include the search results in the output produced by the LLM."""      ranking_options: RankingOptions | None = None     """Ranking options for search."""      filters: Filters | None = None     """A filter to apply based on file attributes."""      @property     def name(self):         return "file_search" ``` |

#### vector\_store\_ids `instance-attribute`

```
vector_store_ids: list[str]
```

The IDs of the vector stores to search.

#### max\_num\_results `class-attribute` `instance-attribute`

```
max_num_results: int | None = None
```

The maximum number of results to return.

#### include\_search\_results `class-attribute` `instance-attribute`

```
include_search_results: bool = False
```

Whether to include the search results in the output produced by the LLM.

#### ranking\_options `class-attribute` `instance-attribute`

```
ranking_options: RankingOptions | None = None
```

Ranking options for search.

#### filters `class-attribute` `instance-attribute`

```
filters: Filters | None = None
```

A filter to apply based on file attributes.

### WebSearchTool `dataclass`

A hosted tool that lets the LLM search the web. Currently only supported with OpenAI models,
using the Responses API.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 ``` | ``` @dataclass class WebSearchTool:     """A hosted tool that lets the LLM search the web. Currently only supported with OpenAI models,     using the Responses API.     """      user_location: UserLocation | None = None     """Optional location for the search. Lets you customize results to be relevant to a location."""      filters: WebSearchToolFilters | None = None     """A filter to apply based on file attributes."""      search_context_size: Literal["low", "medium", "high"] = "medium"     """The amount of context to use for the search."""      external_web_access: bool | None = None     """Whether the web search tool may fetch live internet content.      When omitted, the API default is used. Set to `False` to request cached or     indexed-only behavior where supported.     """      @property     def name(self):         return "web_search" ``` |

#### user\_location `class-attribute` `instance-attribute`

```
user_location: UserLocation | None = None
```

Optional location for the search. Lets you customize results to be relevant to a location.

#### filters `class-attribute` `instance-attribute`

```
filters: Filters | None = None
```

A filter to apply based on file attributes.

#### search\_context\_size `class-attribute` `instance-attribute`

```
search_context_size: Literal["low", "medium", "high"] = (
    "medium"
)
```

The amount of context to use for the search.

#### external\_web\_access `class-attribute` `instance-attribute`

```
external_web_access: bool | None = None
```

Whether the web search tool may fetch live internet content.

When omitted, the API default is used. Set to `False` to request cached or
indexed-only behavior where supported.

### ComputerTool `dataclass`

Bases: `Generic[ComputerT]`

A local computer harness exposed through the Responses API computer tool.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 ``` | ``` @dataclass(eq=False) class ComputerTool(Generic[ComputerT]):     """A local computer harness exposed through the Responses API computer tool."""      computer: ComputerT | ComputerCreate[ComputerT] | ComputerProvider[ComputerT]     """The computer implementation, or a factory that produces a computer per run."""      on_safety_check: Callable[[ComputerToolSafetyCheckData], MaybeAwaitable[bool]] | None = None     """Optional callback to acknowledge computer tool safety checks."""      custom_data_extractor: ComputerToolCustomDataExtractor | None = field(         default=None,         kw_only=True,     )     """Optional callback that attaches SDK-only custom data to the tool output item."""      def __post_init__(self) -> None:         _store_computer_initializer(self)      @property     def name(self):         # Keep the released preview-era runtime name for hooks and persisted         # RunState compatibility. The Responses serializer selects the actual         # wire tool type separately.         return "computer_use_preview"      @property     def trace_name(self):         # Tracing should display the GA tool alias even while runtime names preserve compatibility.         return "computer" ``` |

#### computer `instance-attribute`

```
computer: (
    ComputerT
    | ComputerCreate[ComputerT]
    | ComputerProvider[ComputerT]
)
```

The computer implementation, or a factory that produces a computer per run.

#### on\_safety\_check `class-attribute` `instance-attribute`

```
on_safety_check: (
    Callable[
        [ComputerToolSafetyCheckData], MaybeAwaitable[bool]
    ]
    | None
) = None
```

Optional callback to acknowledge computer tool safety checks.

#### custom\_data\_extractor `class-attribute` `instance-attribute`

```
custom_data_extractor: (
    ComputerToolCustomDataExtractor | None
) = field(default=None, kw_only=True)
```

Optional callback that attaches SDK-only custom data to the tool output item.

### ComputerToolSafetyCheckData `dataclass`

Information about a computer tool safety check.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 ``` | ``` @dataclass class ComputerToolSafetyCheckData:     """Information about a computer tool safety check."""      ctx_wrapper: RunContextWrapper[Any]     """The run context."""      agent: Agent[Any]     """The agent performing the computer action."""      tool_call: ResponseComputerToolCall     """The computer tool call."""      safety_check: PendingSafetyCheck     """The pending safety check to acknowledge.""" ``` |

#### ctx\_wrapper `instance-attribute`

```
ctx_wrapper: RunContextWrapper[Any]
```

The run context.

#### agent `instance-attribute`

```
agent: Agent[Any]
```

The agent performing the computer action.

#### tool\_call `instance-attribute`

```
tool_call: ResponseComputerToolCall
```

The computer tool call.

#### safety\_check `instance-attribute`

```
safety_check: PendingSafetyCheck
```

The pending safety check to acknowledge.

### MCPToolApprovalRequest `dataclass`

A request to approve a tool call.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 891 892 893 894 895 896 897 898 899 ``` | ``` @dataclass class MCPToolApprovalRequest:     """A request to approve a tool call."""      ctx_wrapper: RunContextWrapper[Any]     """The run context."""      data: McpApprovalRequest     """The data from the MCP tool approval request.""" ``` |

#### ctx\_wrapper `instance-attribute`

```
ctx_wrapper: RunContextWrapper[Any]
```

The run context.

#### data `instance-attribute`

```
data: McpApprovalRequest
```

The data from the MCP tool approval request.

### MCPToolApprovalFunctionResult

Bases: `TypedDict`

The result of an MCP tool approval function.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 902 903 904 905 906 907 908 909 ``` | ``` class MCPToolApprovalFunctionResult(TypedDict):     """The result of an MCP tool approval function."""      approve: bool     """Whether to approve the tool call."""      reason: NotRequired[str]     """An optional reason, if rejected.""" ``` |

#### approve `instance-attribute`

```
approve: bool
```

Whether to approve the tool call.

#### reason `instance-attribute`

```
reason: NotRequired[str]
```

An optional reason, if rejected.

### ShellOnApprovalFunctionResult

Bases: `TypedDict`

The result of a shell tool on\_approval callback.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 926 927 928 929 930 931 932 933 ``` | ``` class ShellOnApprovalFunctionResult(TypedDict):     """The result of a shell tool on_approval callback."""      approve: bool     """Whether to approve the tool call."""      reason: NotRequired[str]     """An optional reason, if rejected.""" ``` |

#### approve `instance-attribute`

```
approve: bool
```

Whether to approve the tool call.

#### reason `instance-attribute`

```
reason: NotRequired[str]
```

An optional reason, if rejected.

### ApplyPatchOnApprovalFunctionResult

Bases: `TypedDict`

The result of an apply\_patch tool on\_approval callback.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 952 953 954 955 956 957 958 959 ``` | ``` class ApplyPatchOnApprovalFunctionResult(TypedDict):     """The result of an apply_patch tool on_approval callback."""      approve: bool     """Whether to approve the tool call."""      reason: NotRequired[str]     """An optional reason, if rejected.""" ``` |

#### approve `instance-attribute`

```
approve: bool
```

Whether to approve the tool call.

#### reason `instance-attribute`

```
reason: NotRequired[str]
```

An optional reason, if rejected.

### CustomToolOnApprovalFunctionResult

Bases: `TypedDict`

The result of a custom tool on\_approval callback.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 970 971 972 973 974 975 976 977 ``` | ``` class CustomToolOnApprovalFunctionResult(TypedDict):     """The result of a custom tool on_approval callback."""      approve: bool     """Whether to approve the tool call."""      reason: NotRequired[str]     """An optional reason, if rejected.""" ``` |

#### approve `instance-attribute`

```
approve: bool
```

Whether to approve the tool call.

#### reason `instance-attribute`

```
reason: NotRequired[str]
```

An optional reason, if rejected.

### HostedMCPTool `dataclass`

A tool that allows the LLM to use a remote MCP server. The LLM will automatically list and
call tools, without requiring a round trip back to your code.
If you want to run MCP servers locally via stdio, in a VPC or other non-publicly-accessible
environment, or you just prefer to run tool calls locally, then you can instead use the servers
in `agents.mcp` and pass `Agent(mcp_servers=[...])` to the agent.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ```  988  989  990  991  992  993  994  995  996  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 ``` | ``` @dataclass class HostedMCPTool:     """A tool that allows the LLM to use a remote MCP server. The LLM will automatically list and     call tools, without requiring a round trip back to your code.     If you want to run MCP servers locally via stdio, in a VPC or other non-publicly-accessible     environment, or you just prefer to run tool calls locally, then you can instead use the servers     in `agents.mcp` and pass `Agent(mcp_servers=[...])` to the agent."""      tool_config: Mcp     """The MCP tool config, which includes the server URL and other settings."""      on_approval_request: MCPToolApprovalFunction | None = None     """An optional function that will be called if approval is requested for an MCP tool. If not     provided, you will need to manually add approvals/rejections to the input and call     `Runner.run(...)` again."""      def __post_init__(self) -> None:         tool_config = dict(self.tool_config)         allowed_callers = tool_config.get("allowed_callers")         if allowed_callers is not None:             tool_config["allowed_callers"] = _normalize_tool_allowed_callers(                 allowed_callers,                 tool_name=f"hosted MCP server `{tool_config.get('server_label', 'unknown')}`",             )         self.tool_config = cast(Mcp, tool_config)      @property     def name(self):         return "hosted_mcp" ``` |

#### tool\_config `instance-attribute`

```
tool_config: Mcp
```

The MCP tool config, which includes the server URL and other settings.

#### on\_approval\_request `class-attribute` `instance-attribute`

```
on_approval_request: MCPToolApprovalFunction | None = None
```

An optional function that will be called if approval is requested for an MCP tool. If not
provided, you will need to manually add approvals/rejections to the input and call
`Runner.run(...)` again.

### CodeInterpreterTool `dataclass`

A tool that allows the LLM to execute code in a sandboxed environment.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 ``` | ``` @dataclass class CodeInterpreterTool:     """A tool that allows the LLM to execute code in a sandboxed environment."""      tool_config: CodeInterpreter     """The tool config, which includes the container and other settings."""      def __post_init__(self) -> None:         tool_config = dict(self.tool_config)         allowed_callers = tool_config.get("allowed_callers")         if allowed_callers is not None:             tool_config["allowed_callers"] = _normalize_tool_allowed_callers(                 allowed_callers,                 tool_name="code_interpreter",             )         self.tool_config = cast(CodeInterpreter, tool_config)      @property     def name(self):         return "code_interpreter" ``` |

#### tool\_config `instance-attribute`

```
tool_config: CodeInterpreter
```

The tool config, which includes the container and other settings.

### ImageGenerationTool `dataclass`

A tool that allows the LLM to generate images.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 ``` | ``` @dataclass class ImageGenerationTool:     """A tool that allows the LLM to generate images."""      tool_config: ImageGeneration     """The tool config, which includes image generation settings."""      @property     def name(self):         return "image_generation" ``` |

#### tool\_config `instance-attribute`

```
tool_config: ImageGeneration
```

The tool config, which includes image generation settings.

### LocalShellCommandRequest `dataclass`

A request to execute a command on a shell.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1053 1054 1055 1056 1057 1058 1059 1060 1061 ``` | ``` @dataclass class LocalShellCommandRequest:     """A request to execute a command on a shell."""      ctx_wrapper: RunContextWrapper[Any]     """The run context."""      data: LocalShellCall     """The data from the local shell tool call.""" ``` |

#### ctx\_wrapper `instance-attribute`

```
ctx_wrapper: RunContextWrapper[Any]
```

The run context.

#### data `instance-attribute`

```
data: LocalShellCall
```

The data from the local shell tool call.

### LocalShellTool `dataclass`

A tool that allows the LLM to execute commands on a shell.

For more details, see:
https://platform.openai.com/docs/guides/tools-local-shell

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 1079 1080 1081 ``` | ``` @dataclass class LocalShellTool:     """A tool that allows the LLM to execute commands on a shell.      For more details, see:     https://platform.openai.com/docs/guides/tools-local-shell     """      executor: LocalShellExecutor     """A function that executes a command on a shell."""      @property     def name(self):         return "local_shell" ``` |

#### executor `instance-attribute`

```
executor: LocalShellExecutor
```

A function that executes a command on a shell.

### ShellToolLocalSkill

Bases: `TypedDict`

Skill metadata for local shell environments.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1084 1085 1086 1087 1088 1089 ``` | ``` class ShellToolLocalSkill(TypedDict):     """Skill metadata for local shell environments."""      description: str     name: str     path: str ``` |

### ShellToolSkillReference

Bases: `TypedDict`

Reference to a hosted shell skill.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1092 1093 1094 1095 1096 1097 ``` | ``` class ShellToolSkillReference(TypedDict):     """Reference to a hosted shell skill."""      type: Literal["skill_reference"]     skill_id: str     version: NotRequired[str] ``` |

### ShellToolInlineSkillSource

Bases: `TypedDict`

Inline skill source payload.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1100 1101 1102 1103 1104 1105 ``` | ``` class ShellToolInlineSkillSource(TypedDict):     """Inline skill source payload."""      data: str     media_type: Literal["application/zip"]     type: Literal["base64"] ``` |

### ShellToolInlineSkill

Bases: `TypedDict`

Inline hosted shell skill bundle.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1108 1109 1110 1111 1112 1113 1114 ``` | ``` class ShellToolInlineSkill(TypedDict):     """Inline hosted shell skill bundle."""      description: str     name: str     source: ShellToolInlineSkillSource     type: Literal["inline"] ``` |

### ShellToolContainerNetworkPolicyDomainSecret

Bases: `TypedDict`

A secret bound to a single domain in allowlist mode.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1121 1122 1123 1124 1125 1126 ``` | ``` class ShellToolContainerNetworkPolicyDomainSecret(TypedDict):     """A secret bound to a single domain in allowlist mode."""      domain: str     name: str     value: str ``` |

### ShellToolContainerNetworkPolicyAllowlist

Bases: `TypedDict`

Allowlist network policy for hosted containers.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1129 1130 1131 1132 1133 1134 ``` | ``` class ShellToolContainerNetworkPolicyAllowlist(TypedDict):     """Allowlist network policy for hosted containers."""      allowed_domains: list[str]     type: Literal["allowlist"]     domain_secrets: NotRequired[list[ShellToolContainerNetworkPolicyDomainSecret]] ``` |

### ShellToolContainerNetworkPolicyDisabled

Bases: `TypedDict`

Disabled network policy for hosted containers.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1137 1138 1139 1140 ``` | ``` class ShellToolContainerNetworkPolicyDisabled(TypedDict):     """Disabled network policy for hosted containers."""      type: Literal["disabled"] ``` |

### ShellToolLocalEnvironment

Bases: `TypedDict`

Local shell execution environment.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1149 1150 1151 1152 1153 ``` | ``` class ShellToolLocalEnvironment(TypedDict):     """Local shell execution environment."""      type: Literal["local"]     skills: NotRequired[list[ShellToolLocalSkill]] ``` |

### ShellToolContainerAutoEnvironment

Bases: `TypedDict`

Auto-provisioned hosted container environment.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1156 1157 1158 1159 1160 1161 1162 1163 ``` | ``` class ShellToolContainerAutoEnvironment(TypedDict):     """Auto-provisioned hosted container environment."""      type: Literal["container_auto"]     file_ids: NotRequired[list[str]]     memory_limit: NotRequired[Literal["1g", "4g", "16g", "64g"] | None]     network_policy: NotRequired[ShellToolContainerNetworkPolicy]     skills: NotRequired[list[ShellToolContainerSkill]] ``` |

### ShellToolContainerReferenceEnvironment

Bases: `TypedDict`

Reference to an existing hosted container.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1166 1167 1168 1169 1170 ``` | ``` class ShellToolContainerReferenceEnvironment(TypedDict):     """Reference to an existing hosted container."""      type: Literal["container_reference"]     container_id: str ``` |

### ShellCallOutcome `dataclass`

Describes the terminal condition of a shell command.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1182 1183 1184 1185 1186 1187 ``` | ``` @dataclass class ShellCallOutcome:     """Describes the terminal condition of a shell command."""      type: Literal["exit", "timeout"]     exit_code: int | None = None ``` |

### ShellCommandOutput `dataclass`

Structured output for a single shell command execution.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1190 1191 1192 1193 1194 1195 1196 1197 1198 1199 1200 1201 1202 1203 1204 1205 1206 ``` | ``` @dataclass class ShellCommandOutput:     """Structured output for a single shell command execution."""      stdout: str = ""     stderr: str = ""     outcome: ShellCallOutcome = field(default_factory=lambda: ShellCallOutcome(type="exit"))     command: str | None = None     provider_data: dict[str, Any] | None = None      @property     def exit_code(self) -> int | None:         return self.outcome.exit_code      @property     def status(self) -> Literal["completed", "timeout"]:         return "timeout" if self.outcome.type == "timeout" else "completed" ``` |

### ShellResult `dataclass`

Result returned by a shell executor.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1209 1210 1211 1212 1213 1214 1215 ``` | ``` @dataclass class ShellResult:     """Result returned by a shell executor."""      output: list[ShellCommandOutput]     max_output_length: int | None = None     provider_data: dict[str, Any] | None = None ``` |

### ShellActionRequest `dataclass`

Action payload for a next-generation shell call.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1218 1219 1220 1221 1222 1223 1224 ``` | ``` @dataclass class ShellActionRequest:     """Action payload for a next-generation shell call."""      commands: list[str]     timeout_ms: int | None = None     max_output_length: int | None = None ``` |

### ShellCallData `dataclass`

Normalized shell call data provided to shell executors.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1227 1228 1229 1230 1231 1232 1233 1234 ``` | ``` @dataclass class ShellCallData:     """Normalized shell call data provided to shell executors."""      call_id: str     action: ShellActionRequest     status: Literal["in_progress", "completed"] | None = None     raw: Any | None = None ``` |

### ShellCommandRequest `dataclass`

A request to execute a modern shell call.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1237 1238 1239 1240 1241 1242 ``` | ``` @dataclass class ShellCommandRequest:     """A request to execute a modern shell call."""      ctx_wrapper: RunContextWrapper[Any]     data: ShellCallData ``` |

### ShellTool `dataclass`

Next-generation shell tool. LocalShellTool will be deprecated in favor of this.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1264 1265 1266 1267 1268 1269 1270 1271 1272 1273 1274 1275 1276 1277 1278 1279 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1315 1316 ``` | ``` @dataclass class ShellTool:     """Next-generation shell tool. LocalShellTool will be deprecated in favor of this."""      executor: ShellExecutor | None = None     name: str = "shell"     needs_approval: bool | ShellApprovalFunction = False     """Whether the shell tool needs approval before execution. If True, the run will be interrupted     and the tool call will need to be approved using RunState.approve() or rejected using     RunState.reject() before continuing. Can be a bool (always/never needs approval) or a     function that takes (run_context, action, call_id) and returns whether this specific call     needs approval.     """     on_approval: ShellOnApprovalFunction | None = None     """Optional handler to auto-approve or reject when approval is required.     If provided, it will be invoked immediately when an approval is needed.     """     environment: ShellToolEnvironment | None = None     """Execution environment for shell commands.      If omitted, local mode is used.     """      allowed_callers: list[ToolCaller] | None = field(default=None, kw_only=True)     """Callers that may invoke this tool on OpenAI Responses models."""      def __post_init__(self) -> None:         """Validate shell tool configuration and normalize environment fields."""         self.allowed_callers = _normalize_tool_allowed_callers(             self.allowed_callers,             tool_name=self.name,         )         normalized_environment = _normalize_shell_tool_environment(self.environment)         self.environment = normalized_environment          environment_type = normalized_environment["type"]         if environment_type == "local":             if self.executor is None:                 raise UserError("ShellTool with local environment requires an executor.")             return          if self.executor is not None:             raise UserError("ShellTool with hosted environment does not accept an executor.")         if self.needs_approval is not False or self.on_approval is not None:             raise UserError(                 "ShellTool with hosted environment does not support needs_approval or on_approval."             )         self.needs_approval = False         self.on_approval = None      @property     def type(self) -> str:         return "shell" ``` |

#### needs\_approval `class-attribute` `instance-attribute`

```
needs_approval: bool | ShellApprovalFunction = False
```

Whether the shell tool needs approval before execution. If True, the run will be interrupted
and the tool call will need to be approved using RunState.approve() or rejected using
RunState.reject() before continuing. Can be a bool (always/never needs approval) or a
function that takes (run\_context, action, call\_id) and returns whether this specific call
needs approval.

#### on\_approval `class-attribute` `instance-attribute`

```
on_approval: ShellOnApprovalFunction | None = None
```

Optional handler to auto-approve or reject when approval is required.
If provided, it will be invoked immediately when an approval is needed.

#### environment `class-attribute` `instance-attribute`

```
environment: ShellToolEnvironment | None = None
```

Execution environment for shell commands.

If omitted, local mode is used.

#### allowed\_callers `class-attribute` `instance-attribute`

```
allowed_callers: list[ToolCaller] | None = field(
    default=None, kw_only=True
)
```

Callers that may invoke this tool on OpenAI Responses models.

#### \_\_post\_init\_\_

```
__post_init__() -> None
```

Validate shell tool configuration and normalize environment fields.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 ``` | ``` def __post_init__(self) -> None:     """Validate shell tool configuration and normalize environment fields."""     self.allowed_callers = _normalize_tool_allowed_callers(         self.allowed_callers,         tool_name=self.name,     )     normalized_environment = _normalize_shell_tool_environment(self.environment)     self.environment = normalized_environment      environment_type = normalized_environment["type"]     if environment_type == "local":         if self.executor is None:             raise UserError("ShellTool with local environment requires an executor.")         return      if self.executor is not None:         raise UserError("ShellTool with hosted environment does not accept an executor.")     if self.needs_approval is not False or self.on_approval is not None:         raise UserError(             "ShellTool with hosted environment does not support needs_approval or on_approval."         )     self.needs_approval = False     self.on_approval = None ``` |

### ApplyPatchTool `dataclass`

Hosted apply\_patch tool. Lets the model request file mutations via unified diffs.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1319 1320 1321 1322 1323 1324 1325 1326 1327 1328 1329 1330 1331 1332 1333 1334 1335 1336 1337 1338 1339 1340 1341 1342 1343 1344 1345 1346 1347 1348 1349 1350 1351 1352 1353 1354 ``` | ``` @dataclass class ApplyPatchTool:     """Hosted apply_patch tool. Lets the model request file mutations via unified diffs."""      editor: ApplyPatchEditor     name: str = "apply_patch"     needs_approval: bool | ApplyPatchApprovalFunction = False     """Whether the apply_patch tool needs approval before execution. If True, the run will be     interrupted and the tool call will need to be approved using RunState.approve() or rejected     using RunState.reject() before continuing. Can be a bool (always/never needs approval) or a     function that takes (run_context, operation, call_id) and returns whether this specific call     needs approval.     """     on_approval: ApplyPatchOnApprovalFunction | None = None     """Optional handler to auto-approve or reject when approval is required.     If provided, it will be invoked immediately when an approval is needed.     """      custom_data_extractor: ApplyPatchToolCustomDataExtractor | None = field(         default=None,         kw_only=True,     )     """Optional callback that attaches SDK-only custom data to the tool output item."""      allowed_callers: list[ToolCaller] | None = field(default=None, kw_only=True)     """Callers that may invoke this tool on OpenAI Responses models."""      def __post_init__(self) -> None:         self.allowed_callers = _normalize_tool_allowed_callers(             self.allowed_callers,             tool_name=self.name,         )      @property     def type(self) -> str:         return "apply_patch" ``` |

#### needs\_approval `class-attribute` `instance-attribute`

```
needs_approval: bool | ApplyPatchApprovalFunction = False
```

Whether the apply\_patch tool needs approval before execution. If True, the run will be
interrupted and the tool call will need to be approved using RunState.approve() or rejected
using RunState.reject() before continuing. Can be a bool (always/never needs approval) or a
function that takes (run\_context, operation, call\_id) and returns whether this specific call
needs approval.

#### on\_approval `class-attribute` `instance-attribute`

```
on_approval: ApplyPatchOnApprovalFunction | None = None
```

Optional handler to auto-approve or reject when approval is required.
If provided, it will be invoked immediately when an approval is needed.

#### custom\_data\_extractor `class-attribute` `instance-attribute`

```
custom_data_extractor: (
    ApplyPatchToolCustomDataExtractor | None
) = field(default=None, kw_only=True)
```

Optional callback that attaches SDK-only custom data to the tool output item.

#### allowed\_callers `class-attribute` `instance-attribute`

```
allowed_callers: list[ToolCaller] | None = field(
    default=None, kw_only=True
)
```

Callers that may invoke this tool on OpenAI Responses models.

### CustomTool `dataclass`

A Responses custom tool that uses one raw string input instead of JSON arguments.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1357 1358 1359 1360 1361 1362 1363 1364 1365 1366 1367 1368 1369 1370 1371 1372 1373 1374 1375 1376 1377 1378 1379 1380 1381 1382 1383 1384 1385 1386 1387 1388 1389 1390 1391 1392 1393 1394 1395 1396 1397 1398 1399 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 ``` | ``` @dataclass class CustomTool:     """A Responses custom tool that uses one raw string input instead of JSON arguments."""      name: str     description: str     on_invoke_tool: CustomToolExecutor     format: object | None = None     needs_approval: bool | CustomToolApprovalFunction = False     """Whether the raw custom tool call needs approval before execution."""     on_approval: CustomToolOnApprovalFunction | None = None     """Optional handler to auto-approve or reject when approval is required."""     defer_loading: bool = False     custom_data_extractor: CustomToolCustomDataExtractor | None = field(         default=None,         kw_only=True,     )     """Optional callback that attaches SDK-only custom data to the tool output item."""      allowed_callers: list[ToolCaller] | None = field(default=None, kw_only=True)     """Callers that may invoke this tool on OpenAI Responses models."""      tool_config: CustomToolParam = field(init=False, repr=False)      def __post_init__(self) -> None:         self.allowed_callers = _normalize_tool_allowed_callers(             self.allowed_callers,             tool_name=self.name,         )         tool_config: CustomToolParam = {             "type": "custom",             "name": self.name,             "description": self.description,         }         if self.format is not None:             tool_config["format"] = self.format  # type: ignore[typeddict-item]         if self.defer_loading:             tool_config["defer_loading"] = True         if self.allowed_callers is not None:             tool_config["allowed_callers"] = self.allowed_callers         self.tool_config = tool_config      def runtime_needs_approval(self) -> bool | CustomToolApprovalFunction:         """Return the callable/bool approval setting used by runtime execution."""         return self.needs_approval      def runtime_on_approval(self) -> CustomToolOnApprovalFunction | None:         """Return the approval callback used by runtime execution."""         return self.on_approval      @property     def type(self) -> str:         return "custom" ``` |

#### needs\_approval `class-attribute` `instance-attribute`

```
needs_approval: bool | CustomToolApprovalFunction = False
```

Whether the raw custom tool call needs approval before execution.

#### on\_approval `class-attribute` `instance-attribute`

```
on_approval: CustomToolOnApprovalFunction | None = None
```

Optional handler to auto-approve or reject when approval is required.

#### custom\_data\_extractor `class-attribute` `instance-attribute`

```
custom_data_extractor: (
    CustomToolCustomDataExtractor | None
) = field(default=None, kw_only=True)
```

Optional callback that attaches SDK-only custom data to the tool output item.

#### allowed\_callers `class-attribute` `instance-attribute`

```
allowed_callers: list[ToolCaller] | None = field(
    default=None, kw_only=True
)
```

Callers that may invoke this tool on OpenAI Responses models.

#### runtime\_needs\_approval

```
runtime_needs_approval() -> (
    bool | CustomToolApprovalFunction
)
```

Return the callable/bool approval setting used by runtime execution.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1399 1400 1401 ``` | ``` def runtime_needs_approval(self) -> bool | CustomToolApprovalFunction:     """Return the callable/bool approval setting used by runtime execution."""     return self.needs_approval ``` |

#### runtime\_on\_approval

```
runtime_on_approval() -> (
    CustomToolOnApprovalFunction | None
)
```

Return the approval callback used by runtime execution.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1403 1404 1405 ``` | ``` def runtime_on_approval(self) -> CustomToolOnApprovalFunction | None:     """Return the approval callback used by runtime execution."""     return self.on_approval ``` |

### ToolSearchTool `dataclass`

A hosted Responses API tool that lets the model search deferred tools by namespace.

`execution="client"` is supported for manual Responses orchestration, but the standard
OpenAI Agents runner does not auto-execute client tool search calls.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1412 1413 1414 1415 1416 1417 1418 1419 1420 1421 1422 1423 1424 1425 1426 ``` | ``` @dataclass class ToolSearchTool:     """A hosted Responses API tool that lets the model search deferred tools by namespace.      `execution="client"` is supported for manual Responses orchestration, but the standard     OpenAI Agents runner does not auto-execute client tool search calls.     """      description: str | None = None     execution: Literal["server", "client"] | None = None     parameters: object | None = None      @property     def name(self) -> str:         return "tool_search" ``` |

### ProgrammaticToolCallingTool `dataclass`

A hosted Responses tool that lets generated JavaScript orchestrate other tools.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1429 1430 1431 1432 1433 1434 1435 ``` | ``` @dataclass class ProgrammaticToolCallingTool:     """A hosted Responses tool that lets generated JavaScript orchestrate other tools."""      @property     def name(self) -> str:         return "programmatic_tool_calling" ``` |

### with\_function\_tool\_failure\_error\_handler

```
with_function_tool_failure_error_handler(
    invoke_tool_impl: Callable[
        [ToolContext[Any], str], Awaitable[Any]
    ],
    on_handled_error: Callable[
        [FunctionTool, Exception, str], None
    ],
) -> Callable[[ToolContext[Any], str], Awaitable[Any]]
```

Wrap a tool invoker so copied FunctionTools resolve failure policy against themselves.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 ``` | ``` def with_function_tool_failure_error_handler(     invoke_tool_impl: Callable[[ToolContext[Any], str], Awaitable[Any]],     on_handled_error: Callable[[FunctionTool, Exception, str], None], ) -> Callable[[ToolContext[Any], str], Awaitable[Any]]:     """Wrap a tool invoker so copied FunctionTools resolve failure policy against themselves."""      def _on_handled_error_with_context(         function_tool: FunctionTool,         error: Exception,         input_json: str,         _context: ToolContext[Any],     ) -> None:         on_handled_error(function_tool, error, input_json)      return _with_context_function_tool_failure_error_handler(         invoke_tool_impl,         _on_handled_error_with_context,     ) ``` |

### get\_function\_tool\_origin

```
get_function_tool_origin(
    function_tool: FunctionTool,
) -> ToolOrigin | None
```

Return scalar origin metadata for a function tool.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 683 684 685 686 687 ``` | ``` def get_function_tool_origin(function_tool: FunctionTool) -> ToolOrigin | None:     """Return scalar origin metadata for a function tool."""     if not function_tool._emit_tool_origin:         return None     return function_tool._tool_origin or ToolOrigin(type=ToolOriginType.FUNCTION) ``` |

### resolve\_computer `async`

```
resolve_computer(
    *,
    tool: ComputerTool[Any],
    run_context: RunContextWrapper[Any],
) -> ComputerLike
```

Resolve a computer for a given run context, initializing it if needed.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 832 833 834 835 836 837 838 839 840 841 842 ``` | ``` async def resolve_computer(     *, tool: ComputerTool[Any], run_context: RunContextWrapper[Any] ) -> ComputerLike:     """Resolve a computer for a given run context, initializing it if needed."""     per_context = _computer_cache.get(tool)     if per_context is None:         per_context = weakref.WeakKeyDictionary()         _computer_cache[tool] = per_context      cached = per_context.get(run_context)     if cached is not None:         _track_resolved_computer(tool=tool, run_context=run_context, resolved=cached)         return cached.computer      initializer_config = _get_computer_initializer(tool)     lifecycle: ComputerProvider[Any] | None = (         cast(ComputerProvider[Any], initializer_config)         if _is_computer_provider(initializer_config)         else None     )     initializer: ComputerCreate[Any] | None = None     disposer: ComputerDispose[Any] | None = lifecycle.dispose if lifecycle else None      if lifecycle is not None:         initializer = lifecycle.create     elif callable(initializer_config):         initializer = initializer_config     elif _is_computer_provider(tool.computer):         lifecycle_provider = cast(ComputerProvider[Any], tool.computer)         initializer = lifecycle_provider.create         disposer = lifecycle_provider.dispose      if initializer:         computer_candidate = initializer(run_context=run_context)         computer = (             await computer_candidate             if inspect.isawaitable(computer_candidate)             else computer_candidate         )     else:         computer = cast(ComputerLike, tool.computer)      if not isinstance(computer, Computer | AsyncComputer):         raise UserError("The computer tool did not provide a computer instance.")      resolved = _ResolvedComputer(computer=computer, dispose=disposer)     per_context[run_context] = resolved     _track_resolved_computer(tool=tool, run_context=run_context, resolved=resolved)     tool.computer = computer     return computer ``` |

### dispose\_resolved\_computers `async`

```
dispose_resolved_computers(
    *, run_context: RunContextWrapper[Any]
) -> None
```

Dispose any computer instances created for the provided run context.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 845 846 847 848 849 850 851 852 853 854 855 856 857 858 859 860 861 862 863 864 865 866 867 868 869 870 871 ``` | ``` async def dispose_resolved_computers(*, run_context: RunContextWrapper[Any]) -> None:     """Dispose any computer instances created for the provided run context."""     resolved_by_tool = _computers_by_run_context.pop(run_context, None)     if not resolved_by_tool:         return      disposers: list[tuple[ComputerDispose[ComputerLike], ComputerLike]] = []      for tool, _resolved in resolved_by_tool.items():         per_context = _computer_cache.get(tool)         if per_context is not None:             per_context.pop(run_context, None)          initializer = _get_computer_initializer(tool)         if initializer is not None:             tool.computer = initializer          if _resolved.dispose is not None:             disposers.append((_resolved.dispose, _resolved.computer))      for dispose, computer in disposers:         try:             result = dispose(run_context=run_context, computer=computer)             if inspect.isawaitable(result):                 await result         except Exception as exc:             logger.warning("Failed to dispose computer for run context: %s", exc) ``` |

### tool\_namespace

```
tool_namespace(
    *,
    name: str,
    description: str | None,
    tools: list[FunctionTool],
) -> list[FunctionTool]
```

Attach namespace metadata to function tools for OpenAI Responses tool search.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1456 1457 1458 1459 1460 1461 1462 1463 1464 1465 1466 1467 1468 1469 1470 1471 1472 1473 1474 1475 1476 1477 1478 1479 ``` | ``` def tool_namespace(     *,     name: str,     description: str | None,     tools: list[FunctionTool], ) -> list[FunctionTool]:     """Attach namespace metadata to function tools for OpenAI Responses tool search."""     if not isinstance(name, str) or not name.strip():         raise UserError("tool_namespace() requires a non-empty namespace name.")     if not isinstance(description, str) or not description.strip():         raise UserError("tool_namespace() requires a non-empty description.")     if any(not isinstance(tool, FunctionTool) for tool in tools):         raise UserError("tool_namespace() only supports FunctionTool instances.")      namespace_name = name.strip()     normalized_description = description.strip()     namespaced_tools: list[FunctionTool] = []     for tool in tools:         validate_function_tool_namespace_shape(tool.name, namespace_name)         namespaced_tool = copy.copy(tool)         namespaced_tool._tool_namespace = namespace_name         namespaced_tool._tool_namespace_description = normalized_description         namespaced_tools.append(namespaced_tool)     return namespaced_tools ``` |

### get\_function\_tool\_responses\_only\_features

```
get_function_tool_responses_only_features(
    tool: FunctionTool,
) -> tuple[str, ...]
```

Return Responses-only features used by a function tool.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1482 1483 1484 1485 1486 1487 1488 1489 1490 1491 1492 1493 ``` | ``` def get_function_tool_responses_only_features(tool: FunctionTool) -> tuple[str, ...]:     """Return Responses-only features used by a function tool."""     features: list[str] = []     if get_explicit_function_tool_namespace(tool) is not None:         features.append("tool_namespace()")     if tool.defer_loading:         features.append("defer_loading=True")     if tool.allowed_callers is not None:         features.append("allowed_callers")     if tool.output_json_schema is not None:         features.append("output_json_schema")     return tuple(features) ``` |

### ensure\_function\_tool\_supports\_responses\_only\_features

```
ensure_function_tool_supports_responses_only_features(
    tool: FunctionTool, *, backend_name: str
) -> None
```

Reject Responses-only function-tool features on unsupported backends.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1496 1497 1498 1499 1500 1501 1502 1503 1504 1505 1506 1507 1508 1509 1510 1511 ``` | ``` def ensure_function_tool_supports_responses_only_features(     tool: FunctionTool,     *,     backend_name: str, ) -> None:     """Reject Responses-only function-tool features on unsupported backends."""     unsupported_features = get_function_tool_responses_only_features(tool)     if not unsupported_features:         return      tool_name = tool.qualified_name     raise UserError(         "The following function-tool features are only supported with OpenAI Responses "         f"models: {', '.join(unsupported_features)}. "         f"Tool `{tool_name}` cannot be used with {backend_name}."     ) ``` |

### ensure\_tool\_choice\_supports\_backend

```
ensure_tool_choice_supports_backend(
    tool_choice: Literal["auto", "required", "none"]
    | str
    | Any
    | None,
    *,
    backend_name: str,
) -> None
```

Backend-specific converters should validate reserved tool choices.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1514 1515 1516 1517 1518 1519 1520 1521 1522 1523 1524 ``` | ``` def ensure_tool_choice_supports_backend(     tool_choice: Literal["auto", "required", "none"] | str | Any | None,     *,     backend_name: str, ) -> None:     """Backend-specific converters should validate reserved tool choices."""     if tool_choice == "programmatic_tool_calling":         raise UserError(             "tool_choice='programmatic_tool_calling' is only supported with OpenAI Responses "             f"models and cannot be used with {backend_name}."         ) ``` |

### is\_responses\_tool\_search\_surface

```
is_responses_tool_search_surface(tool: Tool) -> bool
```

Return True when a tool can be exposed through hosted Responses tool search.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1527 1528 1529 1530 1531 1532 1533 ``` | ``` def is_responses_tool_search_surface(tool: Tool) -> bool:     """Return True when a tool can be exposed through hosted Responses tool search."""     if isinstance(tool, FunctionTool):         return tool.defer_loading or get_explicit_function_tool_namespace(tool) is not None     if isinstance(tool, HostedMCPTool):         return bool(tool.tool_config.get("defer_loading"))     return False ``` |

### has\_responses\_tool\_search\_surface

```
has_responses_tool_search_surface(
    tools: list[Tool],
) -> bool
```

Return True when tool search has at least one eligible searchable surface.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1536 1537 1538 ``` | ``` def has_responses_tool_search_surface(tools: list[Tool]) -> bool:     """Return True when tool search has at least one eligible searchable surface."""     return any(is_responses_tool_search_surface(tool) for tool in tools) ``` |

### is\_required\_tool\_search\_surface

```
is_required_tool_search_surface(tool: Tool) -> bool
```

Return True when a tool requires ToolSearchTool() to stay reachable.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1541 1542 1543 1544 1545 1546 1547 ``` | ``` def is_required_tool_search_surface(tool: Tool) -> bool:     """Return True when a tool requires ToolSearchTool() to stay reachable."""     if isinstance(tool, FunctionTool):         return tool.defer_loading     if isinstance(tool, HostedMCPTool):         return bool(tool.tool_config.get("defer_loading"))     return False ``` |

### has\_required\_tool\_search\_surface

```
has_required_tool_search_surface(tools: list[Tool]) -> bool
```

Return True when any enabled surface requires ToolSearchTool().

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1550 1551 1552 ``` | ``` def has_required_tool_search_surface(tools: list[Tool]) -> bool:     """Return True when any enabled surface requires ToolSearchTool()."""     return any(is_required_tool_search_surface(tool) for tool in tools) ``` |

### validate\_responses\_tool\_search\_configuration

```
validate_responses_tool_search_configuration(
    tools: list[Tool],
    *,
    allow_opaque_search_surface: bool = False,
) -> None
```

Validate the Responses-only tool\_search and defer-loading contract.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1555 1556 1557 1558 1559 1560 1561 1562 1563 1564 1565 1566 1567 1568 1569 1570 1571 1572 1573 1574 1575 1576 1577 1578 1579 1580 1581 ``` | ``` def validate_responses_tool_search_configuration(     tools: list[Tool],     *,     allow_opaque_search_surface: bool = False, ) -> None:     """Validate the Responses-only tool_search and defer-loading contract."""     tool_search_tools = [tool for tool in tools if isinstance(tool, ToolSearchTool)]     tool_search_count = len(tool_search_tools)     has_tool_search = tool_search_count > 0     has_tool_search_surface = has_responses_tool_search_surface(tools)     has_required_tool_search = has_required_tool_search_surface(tools)      if tool_search_count > 1:         raise UserError("Only one ToolSearchTool() is allowed when using OpenAI Responses models.")     validate_function_tool_lookup_configuration(tools)     if has_required_tool_search and not has_tool_search:         raise UserError(             "Deferred-loading Responses tools require ToolSearchTool() when using OpenAI "             "Responses models."         )     if has_tool_search and not has_tool_search_surface and not allow_opaque_search_surface:         raise UserError(             "ToolSearchTool() requires at least one searchable Responses surface: a "             "tool_namespace(...) function tool, a deferred-loading function tool "             "(`function_tool(..., defer_loading=True)`), or a deferred-loading hosted MCP "             "server (`HostedMCPTool(tool_config={..., 'defer_loading': True})`)."         ) ``` |

### validate\_responses\_programmatic\_tool\_calling\_configuration

```
validate_responses_programmatic_tool_calling_configuration(
    tools: list[Tool],
    *,
    tool_choice: Literal["auto", "required", "none"]
    | str
    | Any
    | None = None,
    allow_opaque_tool_search_surface: bool = False,
) -> None
```

Validate the complete Responses Programmatic Tool Calling configuration.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1602 1603 1604 1605 1606 1607 1608 1609 1610 1611 1612 1613 1614 1615 1616 1617 1618 1619 1620 1621 1622 1623 1624 1625 1626 1627 1628 1629 1630 1631 1632 1633 1634 1635 1636 1637 1638 1639 1640 1641 1642 1643 1644 1645 ``` | ``` def validate_responses_programmatic_tool_calling_configuration(     tools: list[Tool],     *,     tool_choice: Literal["auto", "required", "none"] | str | Any | None = None,     allow_opaque_tool_search_surface: bool = False, ) -> None:     """Validate the complete Responses Programmatic Tool Calling configuration."""     programmatic_tools = [tool for tool in tools if isinstance(tool, ProgrammaticToolCallingTool)]     if len(programmatic_tools) > 1:         raise UserError(             "Only one ProgrammaticToolCallingTool() is allowed when using OpenAI Responses models."         )      has_programmatic_tool = bool(programmatic_tools)     if tool_choice == "programmatic_tool_calling" and not has_programmatic_tool:         raise UserError(             "tool_choice='programmatic_tool_calling' requires ProgrammaticToolCallingTool() "             "when using OpenAI Responses models."         )      eligible_tools: list[Tool] = []     for tool in tools:         allowed_callers = _get_tool_allowed_callers(tool)         if allowed_callers is None or "programmatic" not in allowed_callers:             continue         eligible_tools.append(tool)         if "direct" not in allowed_callers and not has_programmatic_tool:             raise UserError(                 f"Tool `{_get_tool_display_name(tool)}` only allows programmatic callers and "                 "requires ProgrammaticToolCallingTool() when using OpenAI Responses models."             )      has_tool_search = any(isinstance(tool, ToolSearchTool) for tool in tools)     if (         has_programmatic_tool         and not eligible_tools         and not has_tool_search         and not allow_opaque_tool_search_surface     ):         raise UserError(             "ProgrammaticToolCallingTool() requires at least one tool whose allowed_callers "             "includes 'programmatic', a ToolSearchTool(), or an opaque prompt-managed tool "             "surface."         ) ``` |

### prune\_orphaned\_tool\_search\_tools

```
prune_orphaned_tool_search_tools(
    tools: list[Tool],
) -> list[Tool]
```

Preserve explicit ToolSearchTool entries until request conversion validates them.

Whether a tool\_search definition is valid can depend on prompt-managed surfaces that are
only known during request conversion, so pruning here hides misconfiguration instead of
surfacing a clear error.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1648 1649 1650 1651 1652 1653 1654 1655 ``` | ``` def prune_orphaned_tool_search_tools(tools: list[Tool]) -> list[Tool]:     """Preserve explicit ToolSearchTool entries until request conversion validates them.      Whether a tool_search definition is valid can depend on prompt-managed surfaces that are     only known during request conversion, so pruning here hides misconfiguration instead of     surfacing a clear error.     """     return tools ``` |

### default\_tool\_error\_function

```
default_tool_error_function(
    ctx: RunContextWrapper[Any], error: Exception
) -> str
```

The default tool error function, which just returns a generic error message.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1765 1766 1767 1768 1769 1770 1771 1772 1773 1774 ``` | ``` def default_tool_error_function(ctx: RunContextWrapper[Any], error: Exception) -> str:     """The default tool error function, which just returns a generic error message."""     json_decode_error = _extract_tool_argument_json_error(error)     if json_decode_error is not None:         return (             "An error occurred while parsing tool arguments. "             "Please try again with valid JSON. "             f"Error: {json_decode_error}"         )     return f"An error occurred while running the tool. Please try again. Error: {str(error)}" ``` |

### default\_tool\_timeout\_error\_message

```
default_tool_timeout_error_message(
    *, tool_name: str, timeout_seconds: float
) -> str
```

Build the default message returned to the model when a tool times out.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1783 1784 1785 ``` | ``` def default_tool_timeout_error_message(*, tool_name: str, timeout_seconds: float) -> str:     """Build the default message returned to the model when a tool times out."""     return f"Tool '{tool_name}' timed out after {timeout_seconds:g} seconds." ``` |

### set\_function\_tool\_failure\_error\_function

```
set_function_tool_failure_error_function(
    function_tool: FunctionTool,
    failure_error_function: ToolErrorFunction
    | None
    | object = _UNSET_FAILURE_ERROR_FUNCTION,
) -> FunctionTool
```

Store internal failure formatter config for tool wrappers and runtime fallbacks.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1788 1789 1790 1791 1792 1793 1794 1795 1796 1797 1798 1799 1800 1801 ``` | ``` def set_function_tool_failure_error_function(     function_tool: FunctionTool,     failure_error_function: ToolErrorFunction | None | object = _UNSET_FAILURE_ERROR_FUNCTION, ) -> FunctionTool:     """Store internal failure formatter config for tool wrappers and runtime fallbacks."""     function_tool._use_default_failure_error_function = (         failure_error_function is _UNSET_FAILURE_ERROR_FUNCTION     )     function_tool._failure_error_function = (         None         if failure_error_function is _UNSET_FAILURE_ERROR_FUNCTION         else cast(ToolErrorFunction | None, failure_error_function)     )     return function_tool ``` |

### resolve\_function\_tool\_failure\_error\_function

```
resolve_function_tool_failure_error_function(
    function_tool: FunctionTool,
    context: RunContextWrapper[Any] | None = None,
) -> ToolErrorFunction | None
```

Return the configured tool failure formatter for runtime-generated error handling.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1804 1805 1806 1807 1808 1809 1810 1811 1812 1813 ``` | ``` def resolve_function_tool_failure_error_function(     function_tool: FunctionTool,     context: RunContextWrapper[Any] | None = None, ) -> ToolErrorFunction | None:     """Return the configured tool failure formatter for runtime-generated error handling."""     if function_tool._use_default_failure_error_function:         if function_tool.output_json_schema is not None and _is_programmatic_tool_context(context):             return None         return default_tool_error_function     return function_tool._failure_error_function ``` |

### maybe\_invoke\_function\_tool\_failure\_error\_function `async`

```
maybe_invoke_function_tool_failure_error_function(
    *,
    function_tool: FunctionTool,
    context: RunContextWrapper[Any],
    error: BaseException,
) -> str | None
```

Invoke the configured failure formatter, if one exists.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1866 1867 1868 1869 1870 1871 1872 1873 1874 1875 1876 1877 1878 1879 1880 1881 1882 1883 ``` | ``` async def maybe_invoke_function_tool_failure_error_function(     *,     function_tool: FunctionTool,     context: RunContextWrapper[Any],     error: BaseException, ) -> str | None:     """Invoke the configured failure formatter, if one exists."""     failure_error_function = resolve_function_tool_failure_error_function(function_tool, context)     if failure_error_function is None:         return None      formatter_error = _coerce_tool_error_for_failure_error_function(error)     result = failure_error_function(context, formatter_error)     if inspect.isawaitable(result):         result = await result     if function_tool._use_default_failure_error_function and isinstance(context, ToolContext):         setattr(context, _DEFAULT_FAILURE_HANDLED_ATTR, True)     return result ``` |

### invoke\_function\_tool `async`

```
invoke_function_tool(
    *,
    function_tool: FunctionTool,
    context: ToolContext[Any],
    arguments: str,
) -> Any
```

Invoke a function tool, enforcing timeout configuration when provided.

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 1997 1998 1999 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 ``` | ``` async def invoke_function_tool(     *,     function_tool: FunctionTool,     context: ToolContext[Any],     arguments: str, ) -> Any:     """Invoke a function tool, enforcing timeout configuration when provided."""     invocation_result = await _invoke_function_tool_with_metadata(         function_tool=function_tool,         context=context,         arguments=arguments,     )     return invocation_result.output ``` |

### function\_tool

```
function_tool(
    func: ToolFunction[...],
    *,
    name_override: str | None = None,
    description_override: str | None = None,
    docstring_style: DocstringStyle | None = None,
    use_docstring_info: bool = True,
    failure_error_function: ToolErrorFunction | None = None,
    strict_mode: bool = True,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], AgentBase],
        MaybeAwaitable[bool],
    ] = True,
    needs_approval: bool
    | Callable[
        [RunContextWrapper[Any], dict[str, Any], str],
        Awaitable[bool],
    ] = False,
    tool_input_guardrails: list[ToolInputGuardrail[Any]]
    | None = None,
    tool_output_guardrails: list[ToolOutputGuardrail[Any]]
    | None = None,
    timeout: float | None = None,
    timeout_behavior: ToolTimeoutBehavior = "error_as_result",
    timeout_error_function: ToolErrorFunction | None = None,
    defer_loading: bool = False,
    custom_data_extractor: FunctionToolCustomDataExtractor
    | None = None,
    allowed_callers: list[ToolCaller] | None = None,
    output_type: Any | None = None,
    output_json_schema: dict[str, Any] | None = None,
) -> FunctionTool
```

```
function_tool(
    *,
    name_override: str | None = None,
    description_override: str | None = None,
    docstring_style: DocstringStyle | None = None,
    use_docstring_info: bool = True,
    failure_error_function: ToolErrorFunction | None = None,
    strict_mode: bool = True,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], AgentBase],
        MaybeAwaitable[bool],
    ] = True,
    needs_approval: bool
    | Callable[
        [RunContextWrapper[Any], dict[str, Any], str],
        Awaitable[bool],
    ] = False,
    tool_input_guardrails: list[ToolInputGuardrail[Any]]
    | None = None,
    tool_output_guardrails: list[ToolOutputGuardrail[Any]]
    | None = None,
    timeout: float | None = None,
    timeout_behavior: ToolTimeoutBehavior = "error_as_result",
    timeout_error_function: ToolErrorFunction | None = None,
    defer_loading: bool = False,
    custom_data_extractor: FunctionToolCustomDataExtractor
    | None = None,
    allowed_callers: list[ToolCaller] | None = None,
    output_type: Any | None = None,
    output_json_schema: dict[str, Any] | None = None,
) -> Callable[[ToolFunction[...]], FunctionTool]
```

```
function_tool(
    func: ToolFunction[...] | None = None,
    *,
    name_override: str | None = None,
    description_override: str | None = None,
    docstring_style: DocstringStyle | None = None,
    use_docstring_info: bool = True,
    failure_error_function: ToolErrorFunction
    | None
    | object = _UNSET_FAILURE_ERROR_FUNCTION,
    strict_mode: bool = True,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], AgentBase],
        MaybeAwaitable[bool],
    ] = True,
    needs_approval: bool
    | Callable[
        [RunContextWrapper[Any], dict[str, Any], str],
        Awaitable[bool],
    ] = False,
    tool_input_guardrails: list[ToolInputGuardrail[Any]]
    | None = None,
    tool_output_guardrails: list[ToolOutputGuardrail[Any]]
    | None = None,
    timeout: float | None = None,
    timeout_behavior: ToolTimeoutBehavior = "error_as_result",
    timeout_error_function: ToolErrorFunction | None = None,
    defer_loading: bool = False,
    custom_data_extractor: FunctionToolCustomDataExtractor
    | None = None,
    allowed_callers: list[ToolCaller] | None = None,
    output_type: Any | None = None,
    output_json_schema: dict[str, Any] | None = None,
) -> (
    FunctionTool
    | Callable[[ToolFunction[...]], FunctionTool]
)
```

Decorator to create a FunctionTool from a function. By default, we will:
1. Parse the function signature to create a JSON schema for the tool's parameters.
2. Use the function's docstring to populate the tool's description.
3. Use the function's docstring to populate argument descriptions.
The docstring style is detected automatically, but you can override it.

If the function takes a `RunContextWrapper` as the first argument, it *must* match the
context type of the agent that uses the tool.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `func` | `ToolFunction[...] | None` | The function to wrap. | `None` |
| `name_override` | `str | None` | If provided, use this name for the tool instead of the function's name. | `None` |
| `description_override` | `str | None` | If provided, use this description for the tool instead of the function's docstring. | `None` |
| `docstring_style` | `DocstringStyle | None` | If provided, use this style for the tool's docstring. If not provided, we will attempt to auto-detect the style. | `None` |
| `use_docstring_info` | `bool` | If True, use the function's docstring to populate the tool's description and argument descriptions. | `True` |
| `failure_error_function` | `ToolErrorFunction | None | object` | If provided, use this function to generate an error message when the tool call fails. The error message is sent to the LLM. If you pass None, then no error message will be sent and instead an Exception will be raised. | `_UNSET_FAILURE_ERROR_FUNCTION` |
| `strict_mode` | `bool` | Whether to enable strict mode for the tool's JSON schema. We *strongly* recommend setting this to True, as it increases the likelihood of correct JSON input. If False, it allows non-strict JSON schemas. For example, if a parameter has a default value, it will be optional, additional properties are allowed, etc. See here for more: https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses#supported-schemas | `True` |
| `is_enabled` | `bool | Callable[[RunContextWrapper[Any], AgentBase], MaybeAwaitable[bool]]` | Whether the tool is enabled. Can be a bool or a callable that takes the run context and agent and returns whether the tool is enabled. Disabled tools are hidden from the LLM at runtime. | `True` |
| `needs_approval` | `bool | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]]` | Whether the tool needs approval before execution. If True, the run will be interrupted and the tool call will need to be approved using RunState.approve() or rejected using RunState.reject() before continuing. Can be a bool (always/never needs approval) or a function that takes (run\_context, tool\_parameters, call\_id) and returns whether this specific call needs approval. | `False` |
| `tool_input_guardrails` | `list[ToolInputGuardrail[Any]] | None` | Optional list of guardrails to run before invoking the tool. | `None` |
| `tool_output_guardrails` | `list[ToolOutputGuardrail[Any]] | None` | Optional list of guardrails to run after the tool returns. | `None` |
| `timeout` | `float | None` | Optional timeout in seconds for each tool call. | `None` |
| `timeout_behavior` | `ToolTimeoutBehavior` | Timeout handling mode. "error\_as\_result" returns a model-visible message, while "raise\_exception" raises ToolTimeoutError and fails the run. | `'error_as_result'` |
| `timeout_error_function` | `ToolErrorFunction | None` | Optional formatter used for timeout messages when timeout\_behavior="error\_as\_result". | `None` |
| `defer_loading` | `bool` | Whether to hide this tool definition until Responses API tool search explicitly loads it. | `False` |
| `custom_data_extractor` | `FunctionToolCustomDataExtractor | None` | Optional callback that returns SDK-only custom data to attach to the emitted `ToolCallOutputItem`. The returned mapping is not sent to the model. | `None` |
| `allowed_callers` | `list[ToolCaller] | None` | Callers that may invoke the tool on OpenAI Responses models. Include `"programmatic"` to allow generated programs to call it. | `None` |
| `output_type` | `Any | None` | Optional Python output type used to generate and validate a strict output schema. For programmatic tools this is inferred from a structured return annotation when omitted. Use this override when the callable has no usable return annotation. | `None` |
| `output_json_schema` | `dict[str, Any] | None` | Optional JSON Schema describing the tool's output for programmatic callers. This low-level escape hatch is mutually exclusive with `output_type`. | `None` |

Source code in `src/agents/tool.py`

|  |  |
| --- | --- |
| ``` 2237 2238 2239 2240 2241 2242 2243 2244 2245 2246 2247 2248 2249 2250 2251 2252 2253 2254 2255 2256 2257 2258 2259 2260 2261 2262 2263 2264 2265 2266 2267 2268 2269 2270 2271 2272 2273 2274 2275 2276 2277 2278 2279 2280 2281 2282 2283 2284 2285 2286 2287 2288 2289 2290 2291 2292 2293 2294 2295 2296 2297 2298 2299 2300 2301 2302 2303 2304 2305 2306 2307 2308 2309 2310 2311 2312 2313 2314 2315 2316 2317 2318 2319 2320 2321 2322 2323 2324 2325 2326 2327 2328 2329 2330 2331 2332 2333 2334 2335 2336 2337 2338 2339 2340 2341 2342 2343 2344 2345 2346 2347 2348 2349 2350 2351 2352 2353 2354 2355 2356 2357 2358 2359 2360 2361 2362 2363 2364 2365 2366 2367 2368 2369 2370 2371 2372 2373 2374 2375 2376 2377 2378 2379 2380 2381 2382 2383 2384 2385 2386 2387 2388 2389 2390 2391 2392 2393 2394 2395 2396 2397 2398 2399 2400 2401 2402 2403 2404 2405 2406 2407 2408 2409 2410 2411 ``` | ``` def function_tool(     func: ToolFunction[...] | None = None,     *,     name_override: str | None = None,     description_override: str | None = None,     docstring_style: DocstringStyle | None = None,     use_docstring_info: bool = True,     failure_error_function: ToolErrorFunction | None | object = _UNSET_FAILURE_ERROR_FUNCTION,     strict_mode: bool = True,     is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase], MaybeAwaitable[bool]] = True,     needs_approval: bool     | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]] = False,     tool_input_guardrails: list[ToolInputGuardrail[Any]] | None = None,     tool_output_guardrails: list[ToolOutputGuardrail[Any]] | None = None,     timeout: float | None = None,     timeout_behavior: ToolTimeoutBehavior = "error_as_result",     timeout_error_function: ToolErrorFunction | None = None,     defer_loading: bool = False,     custom_data_extractor: FunctionToolCustomDataExtractor | None = None,     allowed_callers: list[ToolCaller] | None = None,     output_type: Any | None = None,     output_json_schema: dict[str, Any] | None = None, ) -> FunctionTool | Callable[[ToolFunction[...]], FunctionTool]:     """     Decorator to create a FunctionTool from a function. By default, we will:     1. Parse the function signature to create a JSON schema for the tool's parameters.     2. Use the function's docstring to populate the tool's description.     3. Use the function's docstring to populate argument descriptions.     The docstring style is detected automatically, but you can override it.      If the function takes a `RunContextWrapper` as the first argument, it *must* match the     context type of the agent that uses the tool.      Args:         func: The function to wrap.         name_override: If provided, use this name for the tool instead of the function's name.         description_override: If provided, use this description for the tool instead of the             function's docstring.         docstring_style: If provided, use this style for the tool's docstring. If not provided,             we will attempt to auto-detect the style.         use_docstring_info: If True, use the function's docstring to populate the tool's             description and argument descriptions.         failure_error_function: If provided, use this function to generate an error message when             the tool call fails. The error message is sent to the LLM. If you pass None, then no             error message will be sent and instead an Exception will be raised.         strict_mode: Whether to enable strict mode for the tool's JSON schema. We *strongly*             recommend setting this to True, as it increases the likelihood of correct JSON input.             If False, it allows non-strict JSON schemas. For example, if a parameter has a default             value, it will be optional, additional properties are allowed, etc. See here for more:             https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses#supported-schemas         is_enabled: Whether the tool is enabled. Can be a bool or a callable that takes the run             context and agent and returns whether the tool is enabled. Disabled tools are hidden             from the LLM at runtime.         needs_approval: Whether the tool needs approval before execution. If True, the run will             be interrupted and the tool call will need to be approved using RunState.approve() or             rejected using RunState.reject() before continuing. Can be a bool (always/never needs             approval) or a function that takes (run_context, tool_parameters, call_id) and returns             whether this specific call needs approval.         tool_input_guardrails: Optional list of guardrails to run before invoking the tool.         tool_output_guardrails: Optional list of guardrails to run after the tool returns.         timeout: Optional timeout in seconds for each tool call.         timeout_behavior: Timeout handling mode. "error_as_result" returns a model-visible message,             while "raise_exception" raises ToolTimeoutError and fails the run.         timeout_error_function: Optional formatter used for timeout messages when             timeout_behavior="error_as_result".         defer_loading: Whether to hide this tool definition until Responses API tool search             explicitly loads it.         custom_data_extractor: Optional callback that returns SDK-only custom data to attach to             the emitted ``ToolCallOutputItem``. The returned mapping is not sent to the model.         allowed_callers: Callers that may invoke the tool on OpenAI Responses models. Include             ``"programmatic"`` to allow generated programs to call it.         output_type: Optional Python output type used to generate and validate a strict output             schema. For programmatic tools this is inferred from a structured return annotation             when omitted. Use this override when the callable has no usable return annotation.         output_json_schema: Optional JSON Schema describing the tool's output for programmatic             callers. This low-level escape hatch is mutually exclusive with ``output_type``.     """      def _create_function_tool(the_func: ToolFunction[...]) -> FunctionTool:         is_sync_function_tool = not inspect.iscoroutinefunction(the_func)         schema = function_schema(             func=the_func,             name_override=name_override,             description_override=description_override,             docstring_style=docstring_style,             use_docstring_info=use_docstring_info,             strict_json_schema=strict_mode,         )         resolved_output_json_schema, output_type_adapter = _resolve_function_tool_output(             return_annotation=schema.return_annotation,             allowed_callers=allowed_callers,             output_type=output_type,             output_json_schema=output_json_schema,         )          async def _on_invoke_tool_impl(ctx: ToolContext[Any], input: str) -> Any:             tool_name = ctx.tool_name             json_data = _parse_function_tool_json_input(tool_name=tool_name, input_json=input)             _log_function_tool_invocation(tool_name=tool_name, input_json=input)              try:                 parsed = (                     schema.params_pydantic_model(**json_data)                     if json_data                     else schema.params_pydantic_model()                 )             except ValidationError as e:                 raise ModelBehaviorError(f"Invalid JSON input for tool {tool_name}: {e}") from e              args, kwargs_dict = schema.to_call_args(parsed)              if not _debug.DONT_LOG_TOOL_DATA:                 logger.debug("Tool call args: %s, kwargs: %s", args, kwargs_dict)              if not is_sync_function_tool:                 if schema.takes_context:                     result = await the_func(ctx, *args, **kwargs_dict)                 else:                     result = await the_func(*args, **kwargs_dict)             else:                 if schema.takes_context:                     result = await asyncio.to_thread(the_func, ctx, *args, **kwargs_dict)                 else:                     result = await asyncio.to_thread(the_func, *args, **kwargs_dict)              result = _validate_function_tool_output(                 tool_name=tool_name,                 output=result,                 output_type_adapter=output_type_adapter,             )              if _debug.DONT_LOG_TOOL_DATA:                 logger.debug("Tool %s completed.", tool_name)             else:                 logger.debug("Tool %s returned %s", tool_name, result)              return result          function_tool = _build_wrapped_function_tool(             name=schema.name,             description=schema.description or "",             params_json_schema=schema.params_json_schema,             invoke_tool_impl=_on_invoke_tool_impl,             on_handled_error=_build_handled_function_tool_error_handler(                 span_message="Error running tool (non-fatal)",                 span_message_for_json_decode_error="Error running tool",                 log_label="Tool",             ),             failure_error_function=failure_error_function,             strict_json_schema=strict_mode,             is_enabled=is_enabled,             needs_approval=needs_approval,             tool_input_guardrails=tool_input_guardrails,             tool_output_guardrails=tool_output_guardrails,             timeout_seconds=timeout,             timeout_behavior=timeout_behavior,             timeout_error_function=timeout_error_function,             defer_loading=defer_loading,             custom_data_extractor=custom_data_extractor,             allowed_callers=allowed_callers,             output_json_schema=resolved_output_json_schema,             output_type_adapter=output_type_adapter,             sync_invoker=is_sync_function_tool,         )         return function_tool      # If func is actually a callable, we were used as @function_tool with no parentheses     if callable(func):         return _create_function_tool(func)      # Otherwise, we were used as @function_tool(...), so return a decorator     def decorator(real_func: ToolFunction[...]) -> FunctionTool:         return _create_function_tool(real_func)      return decorator ``` |