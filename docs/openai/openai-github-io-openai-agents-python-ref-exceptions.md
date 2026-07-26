---
url: https://openai.github.io/openai-agents-python/ref/exceptions/
title: `Exceptions`
framework: openai
---

# `Exceptions`

### RunErrorDetails `dataclass`

Data collected from an agent run when an exception occurs.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 30 31 32 33 34 35 36 37 38 39 40 41 42 43 ``` | ``` @dataclass class RunErrorDetails:     """Data collected from an agent run when an exception occurs."""      input: str | list[TResponseInputItem]     new_items: list[RunItem]     raw_responses: list[ModelResponse]     last_agent: Agent[Any]     context_wrapper: RunContextWrapper[Any]     input_guardrail_results: list[InputGuardrailResult]     output_guardrail_results: list[OutputGuardrailResult]      def __str__(self) -> str:         return pretty_print_run_error_details(self) ``` |

### AgentsException

Bases: `Exception`

Base class for all exceptions in the Agents SDK.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 46 47 48 49 50 51 52 53 ``` | ``` class AgentsException(Exception):     """Base class for all exceptions in the Agents SDK."""      run_data: RunErrorDetails | None      def __init__(self, *args: object) -> None:         super().__init__(*args)         self.run_data = None ``` |

### MaxTurnsExceeded

Bases: `AgentsException`

Exception raised when the maximum number of turns is exceeded.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 56 57 58 59 60 61 62 63 ``` | ``` class MaxTurnsExceeded(AgentsException):     """Exception raised when the maximum number of turns is exceeded."""      message: str      def __init__(self, message: str):         self.message = message         super().__init__(message) ``` |

### ModelBehaviorError

Bases: `AgentsException`

Exception raised when the model does something unexpected, e.g. calling a tool that doesn't
exist, or providing malformed JSON.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 66 67 68 69 70 71 72 73 74 75 ``` | ``` class ModelBehaviorError(AgentsException):     """Exception raised when the model does something unexpected, e.g. calling a tool that doesn't     exist, or providing malformed JSON.     """      message: str      def __init__(self, message: str):         self.message = message         super().__init__(message) ``` |

### ModelRefusalError

Bases: `AgentsException`

Exception raised when the model refuses to produce the requested output.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 78 79 80 81 82 83 84 85 86 ``` | ``` class ModelRefusalError(AgentsException):     """Exception raised when the model refuses to produce the requested output."""      refusal: str     """The refusal text returned by the model."""      def __init__(self, refusal: str):         self.refusal = refusal         super().__init__(f"Model refused to produce output: {refusal}") ``` |

#### refusal `instance-attribute`

```
refusal: str = refusal
```

The refusal text returned by the model.

### UserError

Bases: `AgentsException`

Exception raised when the user makes an error using the SDK.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 89 90 91 92 93 94 95 96 ``` | ``` class UserError(AgentsException):     """Exception raised when the user makes an error using the SDK."""      message: str      def __init__(self, message: str):         self.message = message         super().__init__(message) ``` |

### MCPToolCancellationError

Bases: `AgentsException`

Exception raised when an MCP tool call is internally cancelled.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ```  99 100 101 102 103 104 105 106 ``` | ``` class MCPToolCancellationError(AgentsException):     """Exception raised when an MCP tool call is internally cancelled."""      message: str      def __init__(self, message: str):         self.message = message         super().__init__(message) ``` |

### ToolTimeoutError

Bases: `AgentsException`

Exception raised when a function tool invocation exceeds its timeout.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 109 110 111 112 113 114 115 116 117 118 ``` | ``` class ToolTimeoutError(AgentsException):     """Exception raised when a function tool invocation exceeds its timeout."""      tool_name: str     timeout_seconds: float      def __init__(self, tool_name: str, timeout_seconds: float):         self.tool_name = tool_name         self.timeout_seconds = timeout_seconds         super().__init__(f"Tool '{tool_name}' timed out after {timeout_seconds:g} seconds.") ``` |

### InputGuardrailTripwireTriggered

Bases: `AgentsException`

Exception raised when a guardrail tripwire is triggered.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 121 122 123 124 125 126 127 128 129 130 131 ``` | ``` class InputGuardrailTripwireTriggered(AgentsException):     """Exception raised when a guardrail tripwire is triggered."""      guardrail_result: InputGuardrailResult     """The result data of the guardrail that was triggered."""      def __init__(self, guardrail_result: InputGuardrailResult):         self.guardrail_result = guardrail_result         super().__init__(             f"Guardrail {guardrail_result.guardrail.__class__.__name__} triggered tripwire"         ) ``` |

#### guardrail\_result `instance-attribute`

```
guardrail_result: InputGuardrailResult = guardrail_result
```

The result data of the guardrail that was triggered.

### OutputGuardrailTripwireTriggered

Bases: `AgentsException`

Exception raised when a guardrail tripwire is triggered.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 134 135 136 137 138 139 140 141 142 143 144 ``` | ``` class OutputGuardrailTripwireTriggered(AgentsException):     """Exception raised when a guardrail tripwire is triggered."""      guardrail_result: OutputGuardrailResult     """The result data of the guardrail that was triggered."""      def __init__(self, guardrail_result: OutputGuardrailResult):         self.guardrail_result = guardrail_result         super().__init__(             f"Guardrail {guardrail_result.guardrail.__class__.__name__} triggered tripwire"         ) ``` |

#### guardrail\_result `instance-attribute`

```
guardrail_result: OutputGuardrailResult = guardrail_result
```

The result data of the guardrail that was triggered.

### ToolInputGuardrailTripwireTriggered

Bases: `AgentsException`

Exception raised when a tool input guardrail tripwire is triggered.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 147 148 149 150 151 152 153 154 155 156 157 158 159 ``` | ``` class ToolInputGuardrailTripwireTriggered(AgentsException):     """Exception raised when a tool input guardrail tripwire is triggered."""      guardrail: ToolInputGuardrail[Any]     """The guardrail that was triggered."""      output: ToolGuardrailFunctionOutput     """The output from the guardrail function."""      def __init__(self, guardrail: ToolInputGuardrail[Any], output: ToolGuardrailFunctionOutput):         self.guardrail = guardrail         self.output = output         super().__init__(f"Tool input guardrail {guardrail.__class__.__name__} triggered tripwire") ``` |

#### guardrail `instance-attribute`

```
guardrail: ToolInputGuardrail[Any] = guardrail
```

The guardrail that was triggered.

#### output `instance-attribute`

```
output: ToolGuardrailFunctionOutput = output
```

The output from the guardrail function.

### ToolOutputGuardrailTripwireTriggered

Bases: `AgentsException`

Exception raised when a tool output guardrail tripwire is triggered.

Source code in `src/agents/exceptions.py`

|  |  |
| --- | --- |
| ``` 162 163 164 165 166 167 168 169 170 171 172 173 174 ``` | ``` class ToolOutputGuardrailTripwireTriggered(AgentsException):     """Exception raised when a tool output guardrail tripwire is triggered."""      guardrail: ToolOutputGuardrail[Any]     """The guardrail that was triggered."""      output: ToolGuardrailFunctionOutput     """The output from the guardrail function."""      def __init__(self, guardrail: ToolOutputGuardrail[Any], output: ToolGuardrailFunctionOutput):         self.guardrail = guardrail         self.output = output         super().__init__(f"Tool output guardrail {guardrail.__class__.__name__} triggered tripwire") ``` |

#### guardrail `instance-attribute`

```
guardrail: ToolOutputGuardrail[Any] = guardrail
```

The guardrail that was triggered.

#### output `instance-attribute`

```
output: ToolGuardrailFunctionOutput = output
```

The output from the guardrail function.