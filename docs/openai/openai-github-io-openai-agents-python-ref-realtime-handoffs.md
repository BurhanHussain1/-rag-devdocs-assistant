---
url: https://openai.github.io/openai-agents-python/ref/realtime/handoffs/
title: `Handoffs`
framework: openai
---

# `Handoffs`

### realtime\_handoff

```
realtime_handoff(
    agent: RealtimeAgent[TContext],
    *,
    tool_name_override: str | None = None,
    tool_description_override: str | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], RealtimeAgent[Any]],
        MaybeAwaitable[bool],
    ] = True,
) -> Handoff[TContext, RealtimeAgent[TContext]]
```

```
realtime_handoff(
    agent: RealtimeAgent[TContext],
    *,
    on_handoff: OnHandoffWithInput[THandoffInput],
    input_type: type[THandoffInput],
    tool_description_override: str | None = None,
    tool_name_override: str | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], RealtimeAgent[Any]],
        MaybeAwaitable[bool],
    ] = True,
) -> Handoff[TContext, RealtimeAgent[TContext]]
```

```
realtime_handoff(
    agent: RealtimeAgent[TContext],
    *,
    on_handoff: OnHandoffWithoutInput,
    tool_description_override: str | None = None,
    tool_name_override: str | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], RealtimeAgent[Any]],
        MaybeAwaitable[bool],
    ] = True,
) -> Handoff[TContext, RealtimeAgent[TContext]]
```

```
realtime_handoff(
    agent: RealtimeAgent[TContext],
    tool_name_override: str | None = None,
    tool_description_override: str | None = None,
    on_handoff: OnHandoffWithInput[THandoffInput]
    | OnHandoffWithoutInput
    | None = None,
    input_type: type[THandoffInput] | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], RealtimeAgent[Any]],
        MaybeAwaitable[bool],
    ] = True,
) -> Handoff[TContext, RealtimeAgent[TContext]]
```

Create a handoff from a RealtimeAgent.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `RealtimeAgent[TContext]` | The RealtimeAgent to handoff to. | *required* |
| `tool_name_override` | `str | None` | Optional override for the name of the tool that represents the handoff. | `None` |
| `tool_description_override` | `str | None` | Optional override for the description of the tool that represents the handoff. | `None` |
| `on_handoff` | `OnHandoffWithInput[THandoffInput] | OnHandoffWithoutInput | None` | A function that runs when the handoff is invoked. | `None` |
| `input_type` | `type[THandoffInput] | None` | the type of the input to the handoff. If provided, the input will be validated against this type. Only relevant if you pass a function that takes an input. | `None` |
| `is_enabled` | `bool | Callable[[RunContextWrapper[Any], RealtimeAgent[Any]], MaybeAwaitable[bool]]` | Whether the handoff is enabled. Can be a bool or a callable that takes the run context and agent and returns whether the handoff is enabled. Disabled handoffs are hidden from the LLM at runtime. | `True` |

Note: input\_filter is not supported for RealtimeAgent handoffs.

Source code in `src/agents/realtime/handoffs.py`

|  |  |
| --- | --- |
| ``` 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 ``` | ``` def realtime_handoff(     agent: RealtimeAgent[TContext],     tool_name_override: str | None = None,     tool_description_override: str | None = None,     on_handoff: OnHandoffWithInput[THandoffInput] | OnHandoffWithoutInput | None = None,     input_type: type[THandoffInput] | None = None,     is_enabled: bool     | Callable[[RunContextWrapper[Any], RealtimeAgent[Any]], MaybeAwaitable[bool]] = True, ) -> Handoff[TContext, RealtimeAgent[TContext]]:     """Create a handoff from a RealtimeAgent.      Args:         agent: The RealtimeAgent to handoff to.         tool_name_override: Optional override for the name of the tool that represents the handoff.         tool_description_override: Optional override for the description of the tool that             represents the handoff.         on_handoff: A function that runs when the handoff is invoked.         input_type: the type of the input to the handoff. If provided, the input will be validated             against this type. Only relevant if you pass a function that takes an input.         is_enabled: Whether the handoff is enabled. Can be a bool or a callable that takes the run             context and agent and returns whether the handoff is enabled. Disabled handoffs are             hidden from the LLM at runtime.      Note: input_filter is not supported for RealtimeAgent handoffs.     """     if input_type is not None and on_handoff is None:         raise UserError("You must provide on_handoff when input_type is provided")     type_adapter: TypeAdapter[Any] | None     if input_type is not None:         if not callable(on_handoff):             raise UserError("on_handoff must be callable")         sig = inspect.signature(on_handoff)         if len(sig.parameters) != 2:             raise UserError("on_handoff must take two arguments: context and input")          type_adapter = TypeAdapter(input_type)         input_json_schema = type_adapter.json_schema()     else:         type_adapter = None         input_json_schema = {}         if on_handoff is not None:             sig = inspect.signature(on_handoff)             if len(sig.parameters) != 1:                 raise UserError("on_handoff must take one argument: context")      async def _invoke_handoff(         ctx: RunContextWrapper[Any], input_json: str | None = None     ) -> RealtimeAgent[TContext]:         if input_type is not None and type_adapter is not None:             if input_json is None:                 _error_tracing.attach_error_to_current_span(                     SpanError(                         message="Handoff function expected non-null input, but got None",                         data={"details": "input_json is None"},                     )                 )                 raise ModelBehaviorError("Handoff function expected non-null input, but got None")              validated_input = _json.validate_json(                 json_str=input_json,                 type_adapter=type_adapter,                 partial=False,                 strict=True,             )             input_func = cast(OnHandoffWithInput[THandoffInput], on_handoff)             if inspect.iscoroutinefunction(input_func):                 await input_func(ctx, validated_input)             else:                 input_func(ctx, validated_input)         elif on_handoff is not None:             no_input_func = cast(OnHandoffWithoutInput, on_handoff)             if inspect.iscoroutinefunction(no_input_func):                 await no_input_func(ctx)             else:                 no_input_func(ctx)          return agent      tool_name = tool_name_override or Handoff.default_tool_name(agent)     tool_description = tool_description_override or Handoff.default_tool_description(agent)      # Always ensure the input JSON schema is in strict mode     # If there is a need, we can make this configurable in the future     input_json_schema = ensure_strict_json_schema(input_json_schema)      async def _is_enabled(ctx: RunContextWrapper[Any], agent_base: AgentBase[Any]) -> bool:         assert callable(is_enabled), "is_enabled must be non-null here"         assert isinstance(agent_base, RealtimeAgent), "Can't handoff to a non-RealtimeAgent"         result = is_enabled(ctx, agent_base)         if inspect.isawaitable(result):             return await result         return result      return Handoff(         tool_name=tool_name,         tool_description=tool_description,         input_json_schema=input_json_schema,         on_invoke_handoff=_invoke_handoff,         input_filter=None,  # Not supported for RealtimeAgent handoffs         agent_name=agent.name,         is_enabled=_is_enabled if callable(is_enabled) else is_enabled,     ) ``` |