---
url: https://openai.github.io/openai-agents-python/ref/guardrail/
title: `Guardrails`
framework: openai
---

# `Guardrails`

### GuardrailFunctionOutput `dataclass`

The output of a guardrail function.

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ``` 19 20 21 22 23 24 25 26 27 28 29 30 31 32 ``` | ``` @dataclass class GuardrailFunctionOutput:     """The output of a guardrail function."""      output_info: Any     """     Optional information about the guardrail's output. For example, the guardrail could include     information about the checks it performed and granular results.     """      tripwire_triggered: bool     """     Whether the tripwire was triggered. If triggered, the agent's execution will be halted.     """ ``` |

#### output\_info `instance-attribute`

```
output_info: Any
```

Optional information about the guardrail's output. For example, the guardrail could include
information about the checks it performed and granular results.

#### tripwire\_triggered `instance-attribute`

```
tripwire_triggered: bool
```

Whether the tripwire was triggered. If triggered, the agent's execution will be halted.

### InputGuardrailResult `dataclass`

The result of a guardrail run.

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ``` 35 36 37 38 39 40 41 42 43 44 45 ``` | ``` @dataclass class InputGuardrailResult:     """The result of a guardrail run."""      guardrail: InputGuardrail[Any]     """     The guardrail that was run.     """      output: GuardrailFunctionOutput     """The output of the guardrail function.""" ``` |

#### guardrail `instance-attribute`

```
guardrail: InputGuardrail[Any]
```

The guardrail that was run.

#### output `instance-attribute`

```
output: GuardrailFunctionOutput
```

The output of the guardrail function.

### OutputGuardrailResult `dataclass`

The result of a guardrail run.

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ``` 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 ``` | ``` @dataclass class OutputGuardrailResult:     """The result of a guardrail run."""      guardrail: OutputGuardrail[Any]     """     The guardrail that was run.     """      agent_output: Any     """     The output of the agent that was checked by the guardrail.     """      agent: Agent[Any]     """     The agent that was checked by the guardrail.     """      output: GuardrailFunctionOutput     """The output of the guardrail function.""" ``` |

#### guardrail `instance-attribute`

```
guardrail: OutputGuardrail[Any]
```

The guardrail that was run.

#### agent\_output `instance-attribute`

```
agent_output: Any
```

The output of the agent that was checked by the guardrail.

#### agent `instance-attribute`

```
agent: Agent[Any]
```

The agent that was checked by the guardrail.

#### output `instance-attribute`

```
output: GuardrailFunctionOutput
```

The output of the guardrail function.

### InputGuardrail `dataclass`

Bases: `Generic[TContext]`

Input guardrails are checks that run either in parallel with the agent or before it starts.
They can be used to do things like:
- Check if input messages are off-topic
- Take over control of the agent's execution if an unexpected input is detected

You can use the `@input_guardrail()` decorator to turn a function into an `InputGuardrail`, or
create an `InputGuardrail` manually.

Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`,
the agent's execution will immediately stop, and
an `InputGuardrailTripwireTriggered` exception will be raised

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ```  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 ``` | ``` @dataclass class InputGuardrail(Generic[TContext]):     """Input guardrails are checks that run either in parallel with the agent or before it starts.     They can be used to do things like:     - Check if input messages are off-topic     - Take over control of the agent's execution if an unexpected input is detected      You can use the `@input_guardrail()` decorator to turn a function into an `InputGuardrail`, or     create an `InputGuardrail` manually.      Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`,     the agent's execution will immediately stop, and     an `InputGuardrailTripwireTriggered` exception will be raised     """      guardrail_function: Callable[         [RunContextWrapper[TContext], Agent[Any], str | list[TResponseInputItem]],         MaybeAwaitable[GuardrailFunctionOutput],     ]     """A function that receives the agent input and the context, and returns a      `GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally      include information about the guardrail's output.     """      name: str | None = None     """The name of the guardrail, used for tracing. If not provided, we'll use the guardrail     function's name.     """      run_in_parallel: bool = True     """Whether the guardrail runs concurrently with the agent (True, default) or before     the agent starts (False).     """      def get_name(self) -> str:         if self.name:             return self.name          return self.guardrail_function.__name__      async def run(         self,         agent: Agent[Any],         input: str | list[TResponseInputItem],         context: RunContextWrapper[TContext],     ) -> InputGuardrailResult:         if not callable(self.guardrail_function):             raise UserError(f"Guardrail function must be callable, got {self.guardrail_function}")          output = self.guardrail_function(context, agent, input)         if inspect.isawaitable(output):             return InputGuardrailResult(                 guardrail=self,                 output=await output,             )          return InputGuardrailResult(             guardrail=self,             output=output,         ) ``` |

#### guardrail\_function `instance-attribute`

```
guardrail_function: Callable[
    [
        RunContextWrapper[TContext],
        Agent[Any],
        str | list[TResponseInputItem],
    ],
    MaybeAwaitable[GuardrailFunctionOutput],
]
```

A function that receives the agent input and the context, and returns a
`GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally
include information about the guardrail's output.

#### name `class-attribute` `instance-attribute`

```
name: str | None = None
```

The name of the guardrail, used for tracing. If not provided, we'll use the guardrail
function's name.

#### run\_in\_parallel `class-attribute` `instance-attribute`

```
run_in_parallel: bool = True
```

Whether the guardrail runs concurrently with the agent (True, default) or before
the agent starts (False).

### OutputGuardrail `dataclass`

Bases: `Generic[TContext]`

Output guardrails are checks that run on the final output of an agent.
They can be used to do check if the output passes certain validation criteria

You can use the `@output_guardrail()` decorator to turn a function into an `OutputGuardrail`,
or create an `OutputGuardrail` manually.

Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, an
`OutputGuardrailTripwireTriggered` exception will be raised.

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ``` 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 ``` | ``` @dataclass class OutputGuardrail(Generic[TContext]):     """Output guardrails are checks that run on the final output of an agent.     They can be used to do check if the output passes certain validation criteria      You can use the `@output_guardrail()` decorator to turn a function into an `OutputGuardrail`,     or create an `OutputGuardrail` manually.      Guardrails return a `GuardrailResult`. If `result.tripwire_triggered` is `True`, an     `OutputGuardrailTripwireTriggered` exception will be raised.     """      guardrail_function: Callable[         [RunContextWrapper[TContext], Agent[Any], Any],         MaybeAwaitable[GuardrailFunctionOutput],     ]     """A function that receives the final agent, its output, and the context, and returns a      `GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally      include information about the guardrail's output.     """      name: str | None = None     """The name of the guardrail, used for tracing. If not provided, we'll use the guardrail     function's name.     """      def get_name(self) -> str:         if self.name:             return self.name          return self.guardrail_function.__name__      async def run(         self, context: RunContextWrapper[TContext], agent: Agent[Any], agent_output: Any     ) -> OutputGuardrailResult:         if not callable(self.guardrail_function):             raise UserError(f"Guardrail function must be callable, got {self.guardrail_function}")          output = self.guardrail_function(context, agent, agent_output)         if inspect.isawaitable(output):             return OutputGuardrailResult(                 guardrail=self,                 agent=agent,                 agent_output=agent_output,                 output=await output,             )          return OutputGuardrailResult(             guardrail=self,             agent=agent,             agent_output=agent_output,             output=output,         ) ``` |

#### guardrail\_function `instance-attribute`

```
guardrail_function: Callable[
    [RunContextWrapper[TContext], Agent[Any], Any],
    MaybeAwaitable[GuardrailFunctionOutput],
]
```

A function that receives the final agent, its output, and the context, and returns a
`GuardrailResult`. The result marks whether the tripwire was triggered, and can optionally
include information about the guardrail's output.

#### name `class-attribute` `instance-attribute`

```
name: str | None = None
```

The name of the guardrail, used for tracing. If not provided, we'll use the guardrail
function's name.

### input\_guardrail

```
input_guardrail(
    func: _InputGuardrailFuncSync[TContext_co],
) -> InputGuardrail[TContext_co]
```

```
input_guardrail(
    func: _InputGuardrailFuncAsync[TContext_co],
) -> InputGuardrail[TContext_co]
```

```
input_guardrail(
    *, name: str | None = None, run_in_parallel: bool = True
) -> Callable[
    [
        _InputGuardrailFuncSync[TContext_co]
        | _InputGuardrailFuncAsync[TContext_co]
    ],
    InputGuardrail[TContext_co],
]
```

```
input_guardrail(
    func: _InputGuardrailFuncSync[TContext_co]
    | _InputGuardrailFuncAsync[TContext_co]
    | None = None,
    *,
    name: str | None = None,
    run_in_parallel: bool = True,
) -> (
    InputGuardrail[TContext_co]
    | Callable[
        [
            _InputGuardrailFuncSync[TContext_co]
            | _InputGuardrailFuncAsync[TContext_co]
        ],
        InputGuardrail[TContext_co],
    ]
)
```

Decorator that transforms a sync or async function into an `InputGuardrail`.
It can be used directly (no parentheses) or with keyword args, e.g.:

```
@input_guardrail
def my_sync_guardrail(...): ...

@input_guardrail(name="guardrail_name", run_in_parallel=False)
async def my_async_guardrail(...): ...
```

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `func` | `_InputGuardrailFuncSync[TContext_co] | _InputGuardrailFuncAsync[TContext_co] | None` | The guardrail function to wrap. | `None` |
| `name` | `str | None` | Optional name for the guardrail. If not provided, uses the function's name. | `None` |
| `run_in_parallel` | `bool` | Whether to run the guardrail concurrently with the agent (True, default) or before the agent starts (False). | `True` |

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ``` 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 ``` | ``` def input_guardrail(     func: _InputGuardrailFuncSync[TContext_co]     | _InputGuardrailFuncAsync[TContext_co]     | None = None,     *,     name: str | None = None,     run_in_parallel: bool = True, ) -> (     InputGuardrail[TContext_co]     | Callable[         [_InputGuardrailFuncSync[TContext_co] | _InputGuardrailFuncAsync[TContext_co]],         InputGuardrail[TContext_co],     ] ):     """     Decorator that transforms a sync or async function into an `InputGuardrail`.     It can be used directly (no parentheses) or with keyword args, e.g.:          @input_guardrail         def my_sync_guardrail(...): ...          @input_guardrail(name="guardrail_name", run_in_parallel=False)         async def my_async_guardrail(...): ...      Args:         func: The guardrail function to wrap.         name: Optional name for the guardrail. If not provided, uses the function's name.         run_in_parallel: Whether to run the guardrail concurrently with the agent (True, default)             or before the agent starts (False).     """      def decorator(         f: _InputGuardrailFuncSync[TContext_co] | _InputGuardrailFuncAsync[TContext_co],     ) -> InputGuardrail[TContext_co]:         return InputGuardrail(             guardrail_function=f,             # If not set, guardrail name uses the function’s name by default.             name=name if name else f.__name__,             run_in_parallel=run_in_parallel,         )      if func is not None:         # Decorator was used without parentheses         return decorator(func)      # Decorator used with keyword arguments     return decorator ``` |

### output\_guardrail

```
output_guardrail(
    func: _OutputGuardrailFuncSync[TContext_co],
) -> OutputGuardrail[TContext_co]
```

```
output_guardrail(
    func: _OutputGuardrailFuncAsync[TContext_co],
) -> OutputGuardrail[TContext_co]
```

```
output_guardrail(
    *, name: str | None = None
) -> Callable[
    [
        _OutputGuardrailFuncSync[TContext_co]
        | _OutputGuardrailFuncAsync[TContext_co]
    ],
    OutputGuardrail[TContext_co],
]
```

```
output_guardrail(
    func: _OutputGuardrailFuncSync[TContext_co]
    | _OutputGuardrailFuncAsync[TContext_co]
    | None = None,
    *,
    name: str | None = None,
) -> (
    OutputGuardrail[TContext_co]
    | Callable[
        [
            _OutputGuardrailFuncSync[TContext_co]
            | _OutputGuardrailFuncAsync[TContext_co]
        ],
        OutputGuardrail[TContext_co],
    ]
)
```

Decorator that transforms a sync or async function into an `OutputGuardrail`.
It can be used directly (no parentheses) or with keyword args, e.g.:

```
@output_guardrail
def my_sync_guardrail(...): ...

@output_guardrail(name="guardrail_name")
async def my_async_guardrail(...): ...
```

Source code in `src/agents/guardrail.py`

|  |  |
| --- | --- |
| ``` 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 ``` | ``` def output_guardrail(     func: _OutputGuardrailFuncSync[TContext_co]     | _OutputGuardrailFuncAsync[TContext_co]     | None = None,     *,     name: str | None = None, ) -> (     OutputGuardrail[TContext_co]     | Callable[         [_OutputGuardrailFuncSync[TContext_co] | _OutputGuardrailFuncAsync[TContext_co]],         OutputGuardrail[TContext_co],     ] ):     """     Decorator that transforms a sync or async function into an `OutputGuardrail`.     It can be used directly (no parentheses) or with keyword args, e.g.:          @output_guardrail         def my_sync_guardrail(...): ...          @output_guardrail(name="guardrail_name")         async def my_async_guardrail(...): ...     """      def decorator(         f: _OutputGuardrailFuncSync[TContext_co] | _OutputGuardrailFuncAsync[TContext_co],     ) -> OutputGuardrail[TContext_co]:         return OutputGuardrail(             guardrail_function=f,             # Guardrail name defaults to function's name when not specified (None).             name=name if name else f.__name__,         )      if func is not None:         # Decorator was used without parentheses         return decorator(func)      # Decorator used with keyword arguments     return decorator ``` |