---
url: https://openai.github.io/openai-agents-python/ref/handoffs/
title: `Handoffs`
framework: openai
---

# `Handoffs`

### HandoffInputFilter `module-attribute`

```
HandoffInputFilter: TypeAlias = Callable[
    [HandoffInputData], MaybeAwaitable[HandoffInputData]
]
```

A function that filters the input data passed to the next agent.

### HandoffHistoryMapper `module-attribute`

```
HandoffHistoryMapper: TypeAlias = Callable[
    [list[TResponseInputItem]], list[TResponseInputItem]
]
```

A function that maps the previous transcript to the nested summary payload.

### HandoffInputData `dataclass`

Source code in `src/agents/handoffs/__init__.py`

|  |  |
| --- | --- |
| ``` 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 ``` | ``` @dataclass(frozen=True) class HandoffInputData:     input_history: str | tuple[TResponseInputItem, ...]     """     The input history before `Runner.run()` was called.     """      pre_handoff_items: tuple[RunItem, ...]     """     The items generated before the agent turn where the handoff was invoked.     """      new_items: tuple[RunItem, ...]     """     The new items generated during the current agent turn, including the item that triggered the     handoff and the tool output message representing the response from the handoff output.     """      run_context: RunContextWrapper[Any] | None = None     """     The run context at the time the handoff was invoked. Note that, since this property was added     later on, it is optional for backwards compatibility.     """      input_items: tuple[RunItem, ...] | None = None     """     Items to include in the next agent's input. When set, these items are used instead of     new_items for building the input to the next agent. This allows filtering duplicates     from agent input while preserving all items in new_items for session history.     """      def clone(self, **kwargs: Any) -> HandoffInputData:         """         Make a copy of the handoff input data, with the given arguments changed. For example, you         could do:          ```         new_handoff_input_data = handoff_input_data.clone(new_items=())         ```         """          cloned = dataclasses_replace(self, **kwargs)         owned_items = getattr(self, "_nested_history_owned_items", ())         if owned_items:             object.__setattr__(cloned, "_nested_history_owned_items", owned_items)         return cloned ``` |

#### input\_history `instance-attribute`

```
input_history: str | tuple[TResponseInputItem, ...]
```

The input history before `Runner.run()` was called.

#### pre\_handoff\_items `instance-attribute`

```
pre_handoff_items: tuple[RunItem, ...]
```

The items generated before the agent turn where the handoff was invoked.

#### new\_items `instance-attribute`

```
new_items: tuple[RunItem, ...]
```

The new items generated during the current agent turn, including the item that triggered the
handoff and the tool output message representing the response from the handoff output.

#### run\_context `class-attribute` `instance-attribute`

```
run_context: RunContextWrapper[Any] | None = None
```

The run context at the time the handoff was invoked. Note that, since this property was added
later on, it is optional for backwards compatibility.

#### input\_items `class-attribute` `instance-attribute`

```
input_items: tuple[RunItem, ...] | None = None
```

Items to include in the next agent's input. When set, these items are used instead of
new\_items for building the input to the next agent. This allows filtering duplicates
from agent input while preserving all items in new\_items for session history.

#### clone

```
clone(**kwargs: Any) -> HandoffInputData
```

Make a copy of the handoff input data, with the given arguments changed. For example, you
could do:

```
new_handoff_input_data = handoff_input_data.clone(new_items=())
```

Source code in `src/agents/handoffs/__init__.py`

|  |  |
| --- | --- |
| ``` 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 ``` | ``` def clone(self, **kwargs: Any) -> HandoffInputData:     """     Make a copy of the handoff input data, with the given arguments changed. For example, you     could do:      ```     new_handoff_input_data = handoff_input_data.clone(new_items=())     ```     """      cloned = dataclasses_replace(self, **kwargs)     owned_items = getattr(self, "_nested_history_owned_items", ())     if owned_items:         object.__setattr__(cloned, "_nested_history_owned_items", owned_items)     return cloned ``` |

### Handoff `dataclass`

Bases: `Generic[TContext, TAgent]`

A handoff is when an agent delegates a task to another agent.

For example, in a customer support scenario you might have a "triage agent" that determines
which agent should handle the user's request, and sub-agents that specialize in different areas
like billing, account management, etc.

Source code in `src/agents/handoffs/__init__.py`

|  |  |
| --- | --- |
| ```  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 ``` | ``` @dataclass class Handoff(Generic[TContext, TAgent]):     """A handoff is when an agent delegates a task to another agent.      For example, in a customer support scenario you might have a "triage agent" that determines     which agent should handle the user's request, and sub-agents that specialize in different areas     like billing, account management, etc.     """      tool_name: str     """The name of the tool that represents the handoff."""      tool_description: str     """The description of the tool that represents the handoff."""      input_json_schema: dict[str, Any]     """The JSON schema for the handoff tool-call arguments.      This schema is exposed to the model as the handoff tool's ``parameters``. It only describes the     structured payload passed to ``on_invoke_handoff`` and does not replace the next agent's main     input.     """      on_invoke_handoff: Callable[[RunContextWrapper[Any], str], Awaitable[TAgent]]     """The function that invokes the handoff.      The parameters passed are: (1) the handoff run context, (2) the arguments from the LLM as a     JSON string (or an empty string if ``input_json_schema`` is empty). Must return an agent.     """      agent_name: str     """The name of the agent that is being handed off to."""      input_filter: HandoffInputFilter | None = None     """A function that filters the inputs that are passed to the next agent.      By default, the new agent sees the entire conversation history. In some cases, you may want to     filter inputs (for example, to remove older inputs or remove tools from existing inputs). The     function receives the entire conversation history so far, including the input item that     triggered the handoff and a tool call output item representing the handoff tool's output. You     are free to modify the input history or new items as you see fit. The next agent receives the     input history plus ``input_items`` when provided, otherwise it receives ``new_items``. Use     ``input_items`` to filter model input while keeping ``new_items`` intact for session history.     IMPORTANT: in streaming mode, we will not stream anything as a result of this function. The     items generated before will already have been streamed. Server-managed conversations     (`conversation_id`, `previous_response_id`, or `auto_previous_response_id`) do not support     handoff input filters.     """      nest_handoff_history: bool | None = None     """Override the run-level ``nest_handoff_history`` behavior for this handoff only.      Server-managed conversations (`conversation_id`, `previous_response_id`, or     `auto_previous_response_id`) automatically disable nested handoff history with a warning.     """      strict_json_schema: bool = True     """Whether the input JSON schema is in strict mode. We strongly recommend setting this to True     because it increases the likelihood of correct JSON input."""      is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]] = (         True     )     """Whether the handoff is enabled.      Either a bool or a callable that takes the run context and agent and returns whether the     handoff is enabled. You can use this to dynamically enable or disable a handoff based on your     context or state.     """      _agent_ref: weakref.ReferenceType[AgentBase[Any]] | None = field(         default=None, init=False, repr=False     )     """Weak reference to the target agent when constructed via `handoff()`."""      def get_transfer_message(self, agent: AgentBase[Any]) -> str:         return json.dumps({"assistant": agent.name})      @classmethod     def default_tool_name(cls, agent: AgentBase[Any]) -> str:         return _transforms.transform_string_function_style(             f"transfer_to_{agent.name}",             warn_on_whitespace=False,         )      @classmethod     def default_tool_description(cls, agent: AgentBase[Any]) -> str:         return (             f"Handoff to the {agent.name} agent to handle the request. "             f"{agent.handoff_description or ''}"         ) ``` |

#### tool\_name `instance-attribute`

```
tool_name: str
```

The name of the tool that represents the handoff.

#### tool\_description `instance-attribute`

```
tool_description: str
```

The description of the tool that represents the handoff.

#### input\_json\_schema `instance-attribute`

```
input_json_schema: dict[str, Any]
```

The JSON schema for the handoff tool-call arguments.

This schema is exposed to the model as the handoff tool's `parameters`. It only describes the
structured payload passed to `on_invoke_handoff` and does not replace the next agent's main
input.

#### on\_invoke\_handoff `instance-attribute`

```
on_invoke_handoff: Callable[
    [RunContextWrapper[Any], str], Awaitable[TAgent]
]
```

The function that invokes the handoff.

The parameters passed are: (1) the handoff run context, (2) the arguments from the LLM as a
JSON string (or an empty string if `input_json_schema` is empty). Must return an agent.

#### agent\_name `instance-attribute`

```
agent_name: str
```

The name of the agent that is being handed off to.

#### input\_filter `class-attribute` `instance-attribute`

```
input_filter: HandoffInputFilter | None = None
```

A function that filters the inputs that are passed to the next agent.

By default, the new agent sees the entire conversation history. In some cases, you may want to
filter inputs (for example, to remove older inputs or remove tools from existing inputs). The
function receives the entire conversation history so far, including the input item that
triggered the handoff and a tool call output item representing the handoff tool's output. You
are free to modify the input history or new items as you see fit. The next agent receives the
input history plus `input_items` when provided, otherwise it receives `new_items`. Use
`input_items` to filter model input while keeping `new_items` intact for session history.
IMPORTANT: in streaming mode, we will not stream anything as a result of this function. The
items generated before will already have been streamed. Server-managed conversations
(`conversation_id`, `previous_response_id`, or `auto_previous_response_id`) do not support
handoff input filters.

#### nest\_handoff\_history `class-attribute` `instance-attribute`

```
nest_handoff_history: bool | None = None
```

Override the run-level `nest_handoff_history` behavior for this handoff only.

Server-managed conversations (`conversation_id`, `previous_response_id`, or
`auto_previous_response_id`) automatically disable nested handoff history with a warning.

#### strict\_json\_schema `class-attribute` `instance-attribute`

```
strict_json_schema: bool = True
```

Whether the input JSON schema is in strict mode. We strongly recommend setting this to True
because it increases the likelihood of correct JSON input.

#### is\_enabled `class-attribute` `instance-attribute`

```
is_enabled: (
    bool
    | Callable[
        [RunContextWrapper[Any], AgentBase[Any]],
        MaybeAwaitable[bool],
    ]
) = True
```

Whether the handoff is enabled.

Either a bool or a callable that takes the run context and agent and returns whether the
handoff is enabled. You can use this to dynamically enable or disable a handoff based on your
context or state.

### default\_handoff\_history\_mapper

```
default_handoff_history_mapper(
    transcript: list[TResponseInputItem],
) -> list[TResponseInputItem]
```

Return a single assistant message summarizing the transcript.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 311 312 313 314 315 316 317 ``` | ``` def default_handoff_history_mapper(     transcript: list[TResponseInputItem], ) -> list[TResponseInputItem]:     """Return a single assistant message summarizing the transcript."""      summary_message = _build_summary_message(transcript)     return [summary_message] ``` |

### get\_conversation\_history\_wrappers

```
get_conversation_history_wrappers() -> tuple[str, str]
```

Return the current start/end markers used for the nested conversation summary.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 77 78 79 80 ``` | ``` def get_conversation_history_wrappers() -> tuple[str, str]:     """Return the current start/end markers used for the nested conversation summary."""      return (_conversation_history_start, _conversation_history_end) ``` |

### nest\_handoff\_history

```
nest_handoff_history(
    handoff_input_data: HandoffInputData,
    *,
    history_mapper: HandoffHistoryMapper | None = None,
) -> HandoffInputData
```

Summarize the previous transcript for the next agent.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 83 84 85 86 87 88 89 90 91 92 93 94 ``` | ``` def nest_handoff_history(     handoff_input_data: HandoffInputData,     *,     history_mapper: HandoffHistoryMapper | None = None, ) -> HandoffInputData:     """Summarize the previous transcript for the next agent."""      nested, _ = _nest_handoff_history_with_provenance(         handoff_input_data,         history_mapper=history_mapper,     )     return nested ``` |

### reset\_conversation\_history\_wrappers

```
reset_conversation_history_wrappers() -> None
```

Restore the default `<CONVERSATION HISTORY>` markers.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 69 70 71 72 73 74 ``` | ``` def reset_conversation_history_wrappers() -> None:     """Restore the default ``<CONVERSATION HISTORY>`` markers."""      global _conversation_history_start, _conversation_history_end     _conversation_history_start = _DEFAULT_CONVERSATION_HISTORY_START     _conversation_history_end = _DEFAULT_CONVERSATION_HISTORY_END ``` |

### set\_conversation\_history\_wrappers

```
set_conversation_history_wrappers(
    *, start: str | None = None, end: str | None = None
) -> None
```

Override the markers that wrap the generated conversation summary.

Pass `None` to leave either side unchanged.

Source code in `src/agents/handoffs/history.py`

|  |  |
| --- | --- |
| ``` 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 ``` | ``` def set_conversation_history_wrappers(     *,     start: str | None = None,     end: str | None = None, ) -> None:     """Override the markers that wrap the generated conversation summary.      Pass ``None`` to leave either side unchanged.     """      global _conversation_history_start, _conversation_history_end     if start is not None:         _conversation_history_start = start     if end is not None:         _conversation_history_end = end ``` |

### handoff

```
handoff(
    agent: Agent[TContext],
    *,
    tool_name_override: str | None = None,
    tool_description_override: str | None = None,
    input_filter: Callable[
        [HandoffInputData], HandoffInputData
    ]
    | None = None,
    nest_handoff_history: bool | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], Agent[Any]],
        MaybeAwaitable[bool],
    ] = True,
) -> Handoff[TContext, Agent[TContext]]
```

```
handoff(
    agent: Agent[TContext],
    *,
    on_handoff: OnHandoffWithInput[THandoffInput],
    input_type: type[THandoffInput],
    tool_description_override: str | None = None,
    tool_name_override: str | None = None,
    input_filter: Callable[
        [HandoffInputData], HandoffInputData
    ]
    | None = None,
    nest_handoff_history: bool | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], Agent[Any]],
        MaybeAwaitable[bool],
    ] = True,
) -> Handoff[TContext, Agent[TContext]]
```

```
handoff(
    agent: Agent[TContext],
    *,
    on_handoff: OnHandoffWithoutInput,
    tool_description_override: str | None = None,
    tool_name_override: str | None = None,
    input_filter: Callable[
        [HandoffInputData], HandoffInputData
    ]
    | None = None,
    nest_handoff_history: bool | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], Agent[Any]],
        MaybeAwaitable[bool],
    ] = True,
) -> Handoff[TContext, Agent[TContext]]
```

```
handoff(
    agent: Agent[TContext],
    tool_name_override: str | None = None,
    tool_description_override: str | None = None,
    on_handoff: OnHandoffWithInput[THandoffInput]
    | OnHandoffWithoutInput
    | None = None,
    input_type: type[THandoffInput] | None = None,
    input_filter: Callable[
        [HandoffInputData], HandoffInputData
    ]
    | None = None,
    nest_handoff_history: bool | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], Agent[TContext]],
        MaybeAwaitable[bool],
    ] = True,
) -> Handoff[TContext, Agent[TContext]]
```

Create a handoff from an agent.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `Agent[TContext]` | The agent to handoff to. | *required* |
| `tool_name_override` | `str | None` | Optional override for the name of the tool that represents the handoff. | `None` |
| `tool_description_override` | `str | None` | Optional override for the description of the tool that represents the handoff. | `None` |
| `on_handoff` | `OnHandoffWithInput[THandoffInput] | OnHandoffWithoutInput | None` | A function that runs when the handoff is invoked. The `handoff()` helper always returns the specific `agent` captured here, so use `on_handoff` for side effects or bookkeeping rather than dynamic destination selection. | `None` |
| `input_type` | `type[THandoffInput] | None` | The type of the handoff tool-call arguments. If provided, the model-generated JSON arguments are validated against this type and the parsed value is passed to `on_handoff`. This only affects the handoff tool payload, not the next agent's main input. | `None` |
| `input_filter` | `Callable[[HandoffInputData], HandoffInputData] | None` | A function that filters the inputs that are passed to the next agent. | `None` |
| `nest_handoff_history` | `bool | None` | Optional override for the RunConfig-level `nest_handoff_history` flag. If `None` we fall back to the run's configuration. | `None` |
| `is_enabled` | `bool | Callable[[RunContextWrapper[Any], Agent[TContext]], MaybeAwaitable[bool]]` | Whether the handoff is enabled. Can be a bool or a callable that takes the run context and agent and returns whether the handoff is enabled. Disabled handoffs are hidden from the LLM at runtime. | `True` |

Source code in `src/agents/handoffs/__init__.py`

|  |  |
| --- | --- |
| ``` 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 ``` | ``` def handoff(     agent: Agent[TContext],     tool_name_override: str | None = None,     tool_description_override: str | None = None,     on_handoff: OnHandoffWithInput[THandoffInput] | OnHandoffWithoutInput | None = None,     input_type: type[THandoffInput] | None = None,     input_filter: Callable[[HandoffInputData], HandoffInputData] | None = None,     nest_handoff_history: bool | None = None,     is_enabled: bool     | Callable[[RunContextWrapper[Any], Agent[TContext]], MaybeAwaitable[bool]] = True, ) -> Handoff[TContext, Agent[TContext]]:     """Create a handoff from an agent.      Args:         agent: The agent to handoff to.         tool_name_override: Optional override for the name of the tool that represents the handoff.         tool_description_override: Optional override for the description of the tool that             represents the handoff.         on_handoff: A function that runs when the handoff is invoked. The ``handoff()`` helper             always returns the specific ``agent`` captured here, so use ``on_handoff`` for side             effects or bookkeeping rather than dynamic destination selection.         input_type: The type of the handoff tool-call arguments. If provided, the model-generated             JSON arguments are validated against this type and the parsed value is passed to             ``on_handoff``. This only affects the handoff tool payload, not the next agent's main             input.         input_filter: A function that filters the inputs that are passed to the next agent.         nest_handoff_history: Optional override for the RunConfig-level ``nest_handoff_history``             flag. If ``None`` we fall back to the run's configuration.         is_enabled: Whether the handoff is enabled. Can be a bool or a callable that takes the run             context and agent and returns whether the handoff is enabled. Disabled handoffs are             hidden from the LLM at runtime.     """      if input_type is not None and on_handoff is None:         raise UserError("You must provide on_handoff when input_type is provided")     type_adapter: TypeAdapter[Any] | None     if input_type is not None:         if not callable(on_handoff):             raise UserError("on_handoff must be callable")         sig = inspect.signature(on_handoff)         if len(sig.parameters) != 2:             raise UserError("on_handoff must take two arguments: context and input")          type_adapter = TypeAdapter(input_type)         input_json_schema = type_adapter.json_schema()     else:         type_adapter = None         input_json_schema = {}         if on_handoff is not None:             sig = inspect.signature(on_handoff)             if len(sig.parameters) != 1:                 raise UserError("on_handoff must take one argument: context")      async def _invoke_handoff(         ctx: RunContextWrapper[Any], input_json: str | None = None     ) -> Agent[TContext]:         if input_type is not None and type_adapter is not None:             if input_json is None:                 _error_tracing.attach_error_to_current_span(                     SpanError(                         message="Handoff function expected non-null input, but got None",                         data={"details": "input_json is None"},                     )                 )                 raise ModelBehaviorError("Handoff function expected non-null input, but got None")              validated_input = _json.validate_json(                 json_str=input_json,                 type_adapter=type_adapter,                 partial=False,                 strict=True,             )             input_func = cast(OnHandoffWithInput[THandoffInput], on_handoff)             result = input_func(ctx, validated_input)             if inspect.isawaitable(result):                 await result         elif on_handoff is not None:             no_input_func = cast(OnHandoffWithoutInput, on_handoff)             result = no_input_func(ctx)             if inspect.isawaitable(result):                 await result          return agent      tool_name = tool_name_override or Handoff.default_tool_name(agent)     tool_description = tool_description_override or Handoff.default_tool_description(agent)      # Always ensure the input JSON schema is in strict mode. If needed, we can make this     # configurable in the future.     input_json_schema = ensure_strict_json_schema(input_json_schema)      async def _is_enabled(ctx: RunContextWrapper[Any], agent_base: AgentBase[Any]) -> bool:         from ..agent import Agent          assert callable(is_enabled), "is_enabled must be callable here"         assert isinstance(agent_base, Agent), "Can't handoff to a non-Agent"         result = is_enabled(ctx, agent_base)         if inspect.isawaitable(result):             return await result         return bool(result)      handoff_obj = Handoff(         tool_name=tool_name,         tool_description=tool_description,         input_json_schema=input_json_schema,         on_invoke_handoff=_invoke_handoff,         input_filter=input_filter,         nest_handoff_history=nest_handoff_history,         agent_name=agent.name,         is_enabled=_is_enabled if callable(is_enabled) else is_enabled,     )     handoff_obj._agent_ref = weakref.ref(agent)     return handoff_obj ``` |