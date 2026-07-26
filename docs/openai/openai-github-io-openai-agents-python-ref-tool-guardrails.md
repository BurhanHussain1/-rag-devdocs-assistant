---
url: https://openai.github.io/openai-agents-python/ref/tool_guardrails/
title: `Tool Guardrails`
framework: openai
---

# `Tool Guardrails`

### ToolInputGuardrailResult `dataclass`

The result of a tool input guardrail run.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 18 19 20 21 22 23 24 25 26 ``` | ``` @dataclass class ToolInputGuardrailResult:     """The result of a tool input guardrail run."""      guardrail: ToolInputGuardrail[Any]     """The guardrail that was run."""      output: ToolGuardrailFunctionOutput     """The output of the guardrail function.""" ``` |

#### guardrail `instance-attribute`

```
guardrail: ToolInputGuardrail[Any]
```

The guardrail that was run.

#### output `instance-attribute`

```
output: ToolGuardrailFunctionOutput
```

The output of the guardrail function.

### ToolOutputGuardrailResult `dataclass`

The result of a tool output guardrail run.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 29 30 31 32 33 34 35 36 37 ``` | ``` @dataclass class ToolOutputGuardrailResult:     """The result of a tool output guardrail run."""      guardrail: ToolOutputGuardrail[Any]     """The guardrail that was run."""      output: ToolGuardrailFunctionOutput     """The output of the guardrail function.""" ``` |

#### guardrail `instance-attribute`

```
guardrail: ToolOutputGuardrail[Any]
```

The guardrail that was run.

#### output `instance-attribute`

```
output: ToolGuardrailFunctionOutput
```

The output of the guardrail function.

### RejectContentBehavior

Bases: `TypedDict`

Rejects the tool call/output but continues execution with a message to the model.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 40 41 42 43 44 ``` | ``` class RejectContentBehavior(TypedDict):     """Rejects the tool call/output but continues execution with a message to the model."""      type: Literal["reject_content"]     message: str ``` |

### RaiseExceptionBehavior

Bases: `TypedDict`

Raises an exception to halt execution.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 47 48 49 50 ``` | ``` class RaiseExceptionBehavior(TypedDict):     """Raises an exception to halt execution."""      type: Literal["raise_exception"] ``` |

### AllowBehavior

Bases: `TypedDict`

Allows normal tool execution to continue.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 53 54 55 56 ``` | ``` class AllowBehavior(TypedDict):     """Allows normal tool execution to continue."""      type: Literal["allow"] ``` |

### ToolGuardrailFunctionOutput `dataclass`

The output of a tool guardrail function.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ```  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 ``` | ``` @dataclass class ToolGuardrailFunctionOutput:     """The output of a tool guardrail function."""      output_info: Any     """     Optional data about checks performed. For example, the guardrail could include     information about the checks it performed and granular results.     """      behavior: RejectContentBehavior | RaiseExceptionBehavior | AllowBehavior = field(         default_factory=lambda: AllowBehavior(type="allow")     )     """     Defines how the system should respond when this guardrail result is processed.     - allow: Allow normal tool execution to continue without interference (default)     - reject_content: Reject the tool call/output but continue execution with a message to the model     - raise_exception: Halt execution by raising a ToolGuardrailTripwireTriggered exception     """      @classmethod     def allow(cls, output_info: Any = None) -> ToolGuardrailFunctionOutput:         """Create a guardrail output that allows the tool execution to continue normally.          Args:             output_info: Optional data about checks performed.          Returns:             ToolGuardrailFunctionOutput configured to allow normal execution.         """         return cls(output_info=output_info, behavior=AllowBehavior(type="allow"))      @classmethod     def reject_content(cls, message: str, output_info: Any = None) -> ToolGuardrailFunctionOutput:         """Create a guardrail output that rejects the tool call/output but continues execution.          Args:             message: Message to send to the model instead of the tool result.             output_info: Optional data about checks performed.          Returns:             ToolGuardrailFunctionOutput configured to reject the content.         """         return cls(             output_info=output_info,             behavior=RejectContentBehavior(type="reject_content", message=message),         )      @classmethod     def raise_exception(cls, output_info: Any = None) -> ToolGuardrailFunctionOutput:         """Create a guardrail output that raises an exception to halt execution.          Args:             output_info: Optional data about checks performed.          Returns:             ToolGuardrailFunctionOutput configured to raise an exception.         """         return cls(output_info=output_info, behavior=RaiseExceptionBehavior(type="raise_exception")) ``` |

#### output\_info `instance-attribute`

```
output_info: Any
```

Optional data about checks performed. For example, the guardrail could include
information about the checks it performed and granular results.

#### behavior `class-attribute` `instance-attribute`

```
behavior: (
    RejectContentBehavior
    | RaiseExceptionBehavior
    | AllowBehavior
) = field(
    default_factory=lambda: AllowBehavior(type="allow")
)
```

Defines how the system should respond when this guardrail result is processed.
- allow: Allow normal tool execution to continue without interference (default)
- reject\_content: Reject the tool call/output but continue execution with a message to the model
- raise\_exception: Halt execution by raising a ToolGuardrailTripwireTriggered exception

#### allow `classmethod`

```
allow(
    output_info: Any = None,
) -> ToolGuardrailFunctionOutput
```

Create a guardrail output that allows the tool execution to continue normally.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `output_info` | `Any` | Optional data about checks performed. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `ToolGuardrailFunctionOutput` | ToolGuardrailFunctionOutput configured to allow normal execution. |

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 79 80 81 82 83 84 85 86 87 88 89 ``` | ``` @classmethod def allow(cls, output_info: Any = None) -> ToolGuardrailFunctionOutput:     """Create a guardrail output that allows the tool execution to continue normally.      Args:         output_info: Optional data about checks performed.      Returns:         ToolGuardrailFunctionOutput configured to allow normal execution.     """     return cls(output_info=output_info, behavior=AllowBehavior(type="allow")) ``` |

#### reject\_content `classmethod`

```
reject_content(
    message: str, output_info: Any = None
) -> ToolGuardrailFunctionOutput
```

Create a guardrail output that rejects the tool call/output but continues execution.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `message` | `str` | Message to send to the model instead of the tool result. | *required* |
| `output_info` | `Any` | Optional data about checks performed. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `ToolGuardrailFunctionOutput` | ToolGuardrailFunctionOutput configured to reject the content. |

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ```  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 ``` | ``` @classmethod def reject_content(cls, message: str, output_info: Any = None) -> ToolGuardrailFunctionOutput:     """Create a guardrail output that rejects the tool call/output but continues execution.      Args:         message: Message to send to the model instead of the tool result.         output_info: Optional data about checks performed.      Returns:         ToolGuardrailFunctionOutput configured to reject the content.     """     return cls(         output_info=output_info,         behavior=RejectContentBehavior(type="reject_content", message=message),     ) ``` |

#### raise\_exception `classmethod`

```
raise_exception(
    output_info: Any = None,
) -> ToolGuardrailFunctionOutput
```

Create a guardrail output that raises an exception to halt execution.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `output_info` | `Any` | Optional data about checks performed. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `ToolGuardrailFunctionOutput` | ToolGuardrailFunctionOutput configured to raise an exception. |

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 107 108 109 110 111 112 113 114 115 116 117 ``` | ``` @classmethod def raise_exception(cls, output_info: Any = None) -> ToolGuardrailFunctionOutput:     """Create a guardrail output that raises an exception to halt execution.      Args:         output_info: Optional data about checks performed.      Returns:         ToolGuardrailFunctionOutput configured to raise an exception.     """     return cls(output_info=output_info, behavior=RaiseExceptionBehavior(type="raise_exception")) ``` |

### ToolInputGuardrailData `dataclass`

Input data passed to a tool input guardrail function.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 120 121 122 123 124 125 126 127 128 129 130 131 132 ``` | ``` @dataclass class ToolInputGuardrailData:     """Input data passed to a tool input guardrail function."""      context: ToolContext[Any]     """     The tool context containing information about the current tool execution.     """      agent: Agent[Any]     """     The agent that is executing the tool.     """ ``` |

#### context `instance-attribute`

```
context: ToolContext[Any]
```

The tool context containing information about the current tool execution.

#### agent `instance-attribute`

```
agent: Agent[Any]
```

The agent that is executing the tool.

### ToolOutputGuardrailData `dataclass`

Bases: `ToolInputGuardrailData`

Input data passed to a tool output guardrail function.

Extends input data with the tool's output.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 135 136 137 138 139 140 141 142 143 144 145 ``` | ``` @dataclass class ToolOutputGuardrailData(ToolInputGuardrailData):     """Input data passed to a tool output guardrail function.      Extends input data with the tool's output.     """      output: Any     """     The output produced by the tool function.     """ ``` |

#### output `instance-attribute`

```
output: Any
```

The output produced by the tool function.

#### context `instance-attribute`

```
context: ToolContext[Any]
```

The tool context containing information about the current tool execution.

#### agent `instance-attribute`

```
agent: Agent[Any]
```

The agent that is executing the tool.

### ToolInputGuardrail `dataclass`

Bases: `Generic[TContext_co]`

A guardrail that runs before a function tool is invoked.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 ``` | ``` @dataclass class ToolInputGuardrail(Generic[TContext_co]):     """A guardrail that runs before a function tool is invoked."""      guardrail_function: Callable[         [ToolInputGuardrailData], MaybeAwaitable[ToolGuardrailFunctionOutput]     ]     """     The function that implements the guardrail logic.     """      name: str | None = None     """     Optional name for the guardrail. If not provided, uses the function name.     """      def get_name(self) -> str:         return self.name or self.guardrail_function.__name__      async def run(self, data: ToolInputGuardrailData) -> ToolGuardrailFunctionOutput:         if not callable(self.guardrail_function):             raise UserError(f"Guardrail function must be callable, got {self.guardrail_function}")          result = self.guardrail_function(data)         if inspect.isawaitable(result):             return await result         return result ``` |

#### guardrail\_function `instance-attribute`

```
guardrail_function: Callable[
    [ToolInputGuardrailData],
    MaybeAwaitable[ToolGuardrailFunctionOutput],
]
```

The function that implements the guardrail logic.

#### name `class-attribute` `instance-attribute`

```
name: str | None = None
```

Optional name for the guardrail. If not provided, uses the function name.

### ToolOutputGuardrail `dataclass`

Bases: `Generic[TContext_co]`

A guardrail that runs after a function tool is invoked.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 ``` | ``` @dataclass class ToolOutputGuardrail(Generic[TContext_co]):     """A guardrail that runs after a function tool is invoked."""      guardrail_function: Callable[         [ToolOutputGuardrailData], MaybeAwaitable[ToolGuardrailFunctionOutput]     ]     """     The function that implements the guardrail logic.     """      name: str | None = None     """     Optional name for the guardrail. If not provided, uses the function name.     """      def get_name(self) -> str:         return self.name or self.guardrail_function.__name__      async def run(self, data: ToolOutputGuardrailData) -> ToolGuardrailFunctionOutput:         if not callable(self.guardrail_function):             raise UserError(f"Guardrail function must be callable, got {self.guardrail_function}")          result = self.guardrail_function(data)         if inspect.isawaitable(result):             return await result         return result ``` |

#### guardrail\_function `instance-attribute`

```
guardrail_function: Callable[
    [ToolOutputGuardrailData],
    MaybeAwaitable[ToolGuardrailFunctionOutput],
]
```

The function that implements the guardrail logic.

#### name `class-attribute` `instance-attribute`

```
name: str | None = None
```

Optional name for the guardrail. If not provided, uses the function name.

### tool\_input\_guardrail

```
tool_input_guardrail(func: _ToolInputFuncSync)
```

```
tool_input_guardrail(func: _ToolInputFuncAsync)
```

```
tool_input_guardrail(
    *, name: str | None = None
) -> Callable[
    [_ToolInputFuncSync | _ToolInputFuncAsync],
    ToolInputGuardrail[Any],
]
```

```
tool_input_guardrail(
    func: _ToolInputFuncSync
    | _ToolInputFuncAsync
    | None = None,
    *,
    name: str | None = None,
) -> (
    ToolInputGuardrail[Any]
    | Callable[
        [_ToolInputFuncSync | _ToolInputFuncAsync],
        ToolInputGuardrail[Any],
    ]
)
```

Decorator to create a ToolInputGuardrail from a function.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 ``` | ``` def tool_input_guardrail(     func: _ToolInputFuncSync | _ToolInputFuncAsync | None = None,     *,     name: str | None = None, ) -> (     ToolInputGuardrail[Any]     | Callable[[_ToolInputFuncSync | _ToolInputFuncAsync], ToolInputGuardrail[Any]] ):     """Decorator to create a ToolInputGuardrail from a function."""      def decorator(f: _ToolInputFuncSync | _ToolInputFuncAsync) -> ToolInputGuardrail[Any]:         return ToolInputGuardrail(guardrail_function=f, name=name or f.__name__)      if func is not None:         return decorator(func)     return decorator ``` |

### tool\_output\_guardrail

```
tool_output_guardrail(func: _ToolOutputFuncSync)
```

```
tool_output_guardrail(func: _ToolOutputFuncAsync)
```

```
tool_output_guardrail(
    *, name: str | None = None
) -> Callable[
    [_ToolOutputFuncSync | _ToolOutputFuncAsync],
    ToolOutputGuardrail[Any],
]
```

```
tool_output_guardrail(
    func: _ToolOutputFuncSync
    | _ToolOutputFuncAsync
    | None = None,
    *,
    name: str | None = None,
) -> (
    ToolOutputGuardrail[Any]
    | Callable[
        [_ToolOutputFuncSync | _ToolOutputFuncAsync],
        ToolOutputGuardrail[Any],
    ]
)
```

Decorator to create a ToolOutputGuardrail from a function.

Source code in `src/agents/tool_guardrails.py`

|  |  |
| --- | --- |
| ``` 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 ``` | ``` def tool_output_guardrail(     func: _ToolOutputFuncSync | _ToolOutputFuncAsync | None = None,     *,     name: str | None = None, ) -> (     ToolOutputGuardrail[Any]     | Callable[[_ToolOutputFuncSync | _ToolOutputFuncAsync], ToolOutputGuardrail[Any]] ):     """Decorator to create a ToolOutputGuardrail from a function."""      def decorator(f: _ToolOutputFuncSync | _ToolOutputFuncAsync) -> ToolOutputGuardrail[Any]:         return ToolOutputGuardrail(guardrail_function=f, name=name or f.__name__)      if func is not None:         return decorator(func)     return decorator ``` |