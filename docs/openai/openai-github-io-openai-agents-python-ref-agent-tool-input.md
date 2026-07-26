---
url: https://openai.github.io/openai-agents-python/ref/agent_tool_input/
title: `Agent Tool Input`
framework: openai
---

# `Agent Tool Input`

### AgentAsToolInput

Bases: `BaseModel`

Default input schema for agent-as-tool calls.

Source code in `src/agents/agent_tool_input.py`

|  |  |
| --- | --- |
| ``` 21 22 23 24 ``` | ``` class AgentAsToolInput(BaseModel):     """Default input schema for agent-as-tool calls."""      input: str ``` |

### StructuredInputSchemaInfo `dataclass`

Optional schema details used to build structured tool input.

Source code in `src/agents/agent_tool_input.py`

|  |  |
| --- | --- |
| ``` 27 28 29 30 31 32 ``` | ``` @dataclass(frozen=True) class StructuredInputSchemaInfo:     """Optional schema details used to build structured tool input."""      summary: str | None = None     json_schema: dict[str, Any] | None = None ``` |

### StructuredToolInputBuilderOptions

Bases: `TypedDict`

Options passed to structured tool input builders.

Source code in `src/agents/agent_tool_input.py`

|  |  |
| --- | --- |
| ``` 35 36 37 38 39 40 ``` | ``` class StructuredToolInputBuilderOptions(TypedDict, total=False):     """Options passed to structured tool input builders."""      params: Any     summary: str | None     json_schema: dict[str, Any] | None ``` |

### default\_tool\_input\_builder

```
default_tool_input_builder(
    options: StructuredToolInputBuilderOptions,
) -> str
```

Build a default message for structured agent tool input.

Source code in `src/agents/agent_tool_input.py`

|  |  |
| --- | --- |
| ``` 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 ``` | ``` def default_tool_input_builder(options: StructuredToolInputBuilderOptions) -> str:     """Build a default message for structured agent tool input."""     sections: list[str] = [STRUCTURED_INPUT_PREAMBLE]      sections.append("## Structured Input Data:")     sections.append("")     sections.append("```")     sections.append(json.dumps(options.get("params"), indent=2) or "null")     sections.append("```")     sections.append("")      json_schema = options.get("json_schema")     if json_schema is not None:         sections.append("## Input JSON Schema:")         sections.append("")         sections.append("```")         sections.append(json.dumps(json_schema, indent=2))         sections.append("```")         sections.append("")     else:         summary = options.get("summary")         if summary:             sections.append("## Input Schema Summary:")             sections.append(summary)             sections.append("")      return "\n".join(sections) ``` |

### resolve\_agent\_tool\_input `async`

```
resolve_agent_tool_input(
    *,
    params: Any,
    schema_info: StructuredInputSchemaInfo | None = None,
    input_builder: StructuredToolInputBuilder | None = None,
) -> str | list[TResponseInputItem]
```

Resolve structured tool input into a string or list of input items.

Source code in `src/agents/agent_tool_input.py`

|  |  |
| --- | --- |
| ```  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 ``` | ``` async def resolve_agent_tool_input(     *,     params: Any,     schema_info: StructuredInputSchemaInfo | None = None,     input_builder: StructuredToolInputBuilder | None = None, ) -> str | list[TResponseInputItem]:     """Resolve structured tool input into a string or list of input items."""     should_build_structured_input = bool(         input_builder or (schema_info and (schema_info.summary or schema_info.json_schema))     )     if should_build_structured_input:         builder = input_builder or default_tool_input_builder         result = builder(             {                 "params": params,                 "summary": schema_info.summary if schema_info else None,                 "json_schema": schema_info.json_schema if schema_info else None,             }         )         if inspect.isawaitable(result):             result = await result         if isinstance(result, str) or isinstance(result, list):             return result         return cast(StructuredToolInputResult, result)      if is_agent_tool_input(params) and _has_only_input_field(params):         return cast(str, params["input"])      return json.dumps(params) ``` |

### build\_structured\_input\_schema\_info

```
build_structured_input_schema_info(
    params_schema: dict[str, Any] | None,
    *,
    include_json_schema: bool,
) -> StructuredInputSchemaInfo
```

Build schema details used for structured input rendering.

Source code in `src/agents/agent_tool_input.py`

|  |  |
| --- | --- |
| ``` 110 111 112 113 114 115 116 117 118 119 120 ``` | ``` def build_structured_input_schema_info(     params_schema: dict[str, Any] | None,     *,     include_json_schema: bool, ) -> StructuredInputSchemaInfo:     """Build schema details used for structured input rendering."""     if not params_schema:         return StructuredInputSchemaInfo()     summary = _build_schema_summary(params_schema)     json_schema = params_schema if include_json_schema else None     return StructuredInputSchemaInfo(summary=summary, json_schema=json_schema) ``` |

### is\_agent\_tool\_input

```
is_agent_tool_input(value: Any) -> bool
```

Return True if the value looks like the default agent tool input.

Source code in `src/agents/agent_tool_input.py`

|  |  |
| --- | --- |
| ``` 123 124 125 ``` | ``` def is_agent_tool_input(value: Any) -> bool:     """Return True if the value looks like the default agent tool input."""     return isinstance(value, dict) and isinstance(value.get("input"), str) ``` |