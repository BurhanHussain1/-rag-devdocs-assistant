---
url: https://openai.github.io/openai-agents-python/ref/extensions/models/litellm_provider/
title: `LiteLLM Provider`
framework: openai
---

# `LiteLLM Provider`

### LitellmProvider

Bases: `ModelProvider`

A ModelProvider that uses LiteLLM to route to any model provider. You can use it via:

```
Runner.run(agent, input, run_config=RunConfig(model_provider=LitellmProvider()))
```

See supported models here: [litellm models](https://docs.litellm.ai/docs/providers).

NOTE: API keys must be set via environment variables. If you're using models that require
additional configuration (e.g. Azure API base or version), those must also be set via the
environment variables that LiteLLM expects. If you have more advanced needs, we recommend
copy-pasting this class and making any modifications you need.

Source code in `src/agents/extensions/models/litellm_provider.py`

|  |  |
| --- | --- |
| ```  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 ``` | ``` class LitellmProvider(ModelProvider):     """A ModelProvider that uses LiteLLM to route to any model provider. You can use it via:     ```python     Runner.run(agent, input, run_config=RunConfig(model_provider=LitellmProvider()))     ```     See supported models here: [litellm models](https://docs.litellm.ai/docs/providers).      NOTE: API keys must be set via environment variables. If you're using models that require     additional configuration (e.g. Azure API base or version), those must also be set via the     environment variables that LiteLLM expects. If you have more advanced needs, we recommend     copy-pasting this class and making any modifications you need.     """      def get_model(self, model_name: str | None) -> Model:         return LitellmModel(model_name or get_default_model()) ``` |

#### aclose `async`

```
aclose() -> None
```

Release any resources held by the provider.

Providers that cache persistent models or network connections can override this. The
default implementation is a no-op.

Source code in `src/agents/models/interface.py`

|  |  |
| --- | --- |
| ``` 148 149 150 151 152 153 154 ``` | ``` async def aclose(self) -> None:     """Release any resources held by the provider.      Providers that cache persistent models or network connections can override this. The     default implementation is a no-op.     """     return None ``` |