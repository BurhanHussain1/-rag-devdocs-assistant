---
url: https://openai.github.io/openai-agents-python/ref/models/openai_agent_registration/
title: `OpenAI Agent Registration`
framework: openai
---

# `OpenAI Agent Registration`

### resolve\_openai\_harness\_id\_for\_model\_provider

```
resolve_openai_harness_id_for_model_provider(
    model_provider: Any,
) -> str | None
```

Return the configured harness ID for OpenAI-backed model providers.

Source code in `src/agents/models/openai_agent_registration.py`

|  |  |
| --- | --- |
| ``` 49 50 51 52 53 54 55 ``` | ``` def resolve_openai_harness_id_for_model_provider(model_provider: Any) -> str | None:     """Return the configured harness ID for OpenAI-backed model providers."""     harness_id = _harness_id_from_model_provider(model_provider)     if harness_id is not None:         return harness_id     resolved = resolve_openai_agent_registration_config(None)     return resolved.harness_id if resolved is not None else None ``` |