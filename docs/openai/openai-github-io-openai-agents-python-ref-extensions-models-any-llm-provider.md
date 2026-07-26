---
url: https://openai.github.io/openai-agents-python/ref/extensions/models/any_llm_provider/
title: `Any Llm Provider`
framework: openai
---

# `Any Llm Provider`

### AnyLLMProvider

Bases: `ModelProvider`

A ModelProvider that routes model calls through any-llm.

API keys are typically sourced from the provider-specific environment variables expected by
any-llm, such as `OPENAI_API_KEY` or `OPENROUTER_API_KEY`. For custom wiring or explicit
credentials, instantiate `AnyLLMModel` directly.

Source code in `src/agents/extensions/models/any_llm_provider.py`

|  |  |
| --- | --- |
| ``` 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 ``` | ``` class AnyLLMProvider(ModelProvider):     """A ModelProvider that routes model calls through any-llm.      API keys are typically sourced from the provider-specific environment variables expected by     any-llm, such as `OPENAI_API_KEY` or `OPENROUTER_API_KEY`. For custom wiring or explicit     credentials, instantiate `AnyLLMModel` directly.     """      def __init__(         self,         *,         api_key: str | None = None,         base_url: str | None = None,         api: Literal["responses", "chat_completions"] | None = None,     ) -> None:         self.api_key = api_key         self.base_url = base_url         self.api = api      def get_model(self, model_name: str | None) -> Model:         return AnyLLMModel(             model=model_name or DEFAULT_MODEL,             api_key=self.api_key,             base_url=self.base_url,             api=self.api,         ) ``` |

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