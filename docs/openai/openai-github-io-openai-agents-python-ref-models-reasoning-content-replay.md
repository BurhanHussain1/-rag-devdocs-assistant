---
url: https://openai.github.io/openai-agents-python/ref/models/reasoning_content_replay/
title: `Reasoning Content Replay`
framework: openai
---

# `Reasoning Content Replay`

### ReasoningContentSource `dataclass`

The reasoning item being considered for replay into the next request.

Source code in `src/agents/models/reasoning_content_replay.py`

|  |  |
| --- | --- |
| ```  8  9 10 11 12 13 14 15 16 17 18 19 ``` | ``` @dataclass class ReasoningContentSource:     """The reasoning item being considered for replay into the next request."""      item: Any     """The raw reasoning item."""      origin_model: str | None     """The model that originally produced the reasoning item, if known."""      provider_data: Mapping[str, Any]     """Provider-specific metadata captured on the reasoning item.""" ``` |

#### item `instance-attribute`

```
item: Any
```

The raw reasoning item.

#### origin\_model `instance-attribute`

```
origin_model: str | None
```

The model that originally produced the reasoning item, if known.

#### provider\_data `instance-attribute`

```
provider_data: Mapping[str, Any]
```

Provider-specific metadata captured on the reasoning item.

### ReasoningContentReplayContext `dataclass`

Context passed to reasoning-content replay hooks.

Source code in `src/agents/models/reasoning_content_replay.py`

|  |  |
| --- | --- |
| ``` 22 23 24 25 26 27 28 29 30 31 32 33 ``` | ``` @dataclass class ReasoningContentReplayContext:     """Context passed to reasoning-content replay hooks."""      model: str     """The model that will receive the next Chat Completions request."""      base_url: str | None     """The request base URL, if the SDK knows the concrete endpoint."""      reasoning: ReasoningContentSource     """The reasoning item candidate being evaluated for replay.""" ``` |

#### model `instance-attribute`

```
model: str
```

The model that will receive the next Chat Completions request.

#### base\_url `instance-attribute`

```
base_url: str | None
```

The request base URL, if the SDK knows the concrete endpoint.

#### reasoning `instance-attribute`

```
reasoning: ReasoningContentSource
```

The reasoning item candidate being evaluated for replay.

### default\_should\_replay\_reasoning\_content

```
default_should_replay_reasoning_content(
    context: ReasoningContentReplayContext,
) -> bool
```

Return whether the SDK should replay reasoning content by default.

Source code in `src/agents/models/reasoning_content_replay.py`

|  |  |
| --- | --- |
| ``` 39 40 41 42 43 44 45 46 47 48 49 50 51 ``` | ``` def default_should_replay_reasoning_content(context: ReasoningContentReplayContext) -> bool:     """Return whether the SDK should replay reasoning content by default."""      if "deepseek" not in context.model.lower():         return False      origin_model = context.reasoning.origin_model     # Replay only when the current request targets DeepSeek and the reasoning item either     # came from a DeepSeek model or predates provider tracking. This avoids mixing reasoning     # content from a different model family into the DeepSeek assistant message.     return (         origin_model is not None and "deepseek" in origin_model.lower()     ) or context.reasoning.provider_data == {} ``` |