---
url: https://openai.github.io/openai-agents-python/ref/models/default_models/
title: `Default Models`
framework: openai
---

# `Default Models`

### gpt\_5\_reasoning\_settings\_required

```
gpt_5_reasoning_settings_required(model_name: str) -> bool
```

Returns True if the model name is a GPT-5 model and reasoning settings are required.

Source code in `src/agents/models/default_models.py`

|  |  |
| --- | --- |
| ``` 79 80 81 82 83 84 85 86 87 ``` | ``` def gpt_5_reasoning_settings_required(model_name: str) -> bool:     """     Returns True if the model name is a GPT-5 model and reasoning settings are required.     """     if any(pattern.fullmatch(model_name) for pattern in _GPT_5_CHAT_MODEL_PATTERNS):         # Chat-latest aliases do not accept reasoning.effort.         return False     # matches any of gpt-5 models     return model_name.startswith("gpt-5") ``` |

### is\_gpt\_5\_default

```
is_gpt_5_default() -> bool
```

Returns True if the default model is a GPT-5 model.
This is used to determine if the default model settings are compatible with GPT-5 models.
If the default model is not a GPT-5 model, the model settings are compatible with other models.

Source code in `src/agents/models/default_models.py`

|  |  |
| --- | --- |
| ``` 90 91 92 93 94 95 96 ``` | ``` def is_gpt_5_default() -> bool:     """     Returns True if the default model is a GPT-5 model.     This is used to determine if the default model settings are compatible with GPT-5 models.     If the default model is not a GPT-5 model, the model settings are compatible with other models.     """     return gpt_5_reasoning_settings_required(get_default_model()) ``` |

### get\_default\_model

```
get_default_model() -> str
```

Returns the default model name.

Source code in `src/agents/models/default_models.py`

|  |  |
| --- | --- |
| ```  99 100 101 102 103 ``` | ``` def get_default_model() -> str:     """     Returns the default model name.     """     return os.getenv(OPENAI_DEFAULT_MODEL_ENV_VARIABLE_NAME, "gpt-5.4-mini").lower() ``` |

### get\_default\_model\_settings

```
get_default_model_settings(
    model: str | None = None,
) -> ModelSettings
```

Returns the default model settings.
If the default model is a GPT-5 model, returns the GPT-5 default model settings.
Otherwise, returns the legacy default model settings.

Source code in `src/agents/models/default_models.py`

|  |  |
| --- | --- |
| ``` 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 ``` | ``` def get_default_model_settings(model: str | None = None) -> ModelSettings:     """     Returns the default model settings.     If the default model is a GPT-5 model, returns the GPT-5 default model settings.     Otherwise, returns the legacy default model settings.     """     _model = model if model is not None else get_default_model()     if gpt_5_reasoning_settings_required(_model):         effort = _get_default_reasoning_effort(_model)         if effort is not None:             return copy.deepcopy(_GPT_5_DEFAULT_MODEL_SETTINGS_BY_REASONING_EFFORT[effort])         # Keep the GPT-5 verbosity default, but omit reasoning.effort for         # variants whose supported values are not confirmed yet.         return copy.deepcopy(_GPT_5_TEXT_ONLY_DEFAULT_MODEL_SETTINGS)     return ModelSettings() ``` |