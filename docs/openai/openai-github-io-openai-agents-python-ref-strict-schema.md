---
url: https://openai.github.io/openai-agents-python/ref/strict_schema/
title: `Strict Schema`
framework: openai
---

# `Strict Schema`

### ensure\_strict\_json\_schema

```
ensure_strict_json_schema(
    schema: dict[str, Any],
) -> dict[str, Any]
```

Mutates the given JSON schema to ensure it conforms to the `strict` standard
that the OpenAI API expects.

Source code in `src/agents/strict_schema.py`

|  |  |
| --- | --- |
| ``` 40 41 42 43 44 45 46 47 48 49 50 ``` | ``` def ensure_strict_json_schema(     schema: dict[str, Any], ) -> dict[str, Any]:     """Mutates the given JSON schema to ensure it conforms to the `strict` standard     that the OpenAI API expects.     """     if schema == {}:         return copy.deepcopy(_EMPTY_SCHEMA)     return _ensure_strict_json_schema(         schema, path=(), root=schema, budget=_NodeBudget(_MAX_SCHEMA_NODES)     ) ``` |