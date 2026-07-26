---
url: https://openai.github.io/openai-agents-python/ref/prompts/
title: `Prompts`
framework: openai
---

# `Prompts`

### DynamicPromptFunction `module-attribute`

```
DynamicPromptFunction = Callable[
    [GenerateDynamicPromptData], MaybeAwaitable[Prompt]
]
```

A function that dynamically generates a prompt.

### Prompt

Bases: `TypedDict`

Prompt configuration to use for interacting with an OpenAI model.

Source code in `src/agents/prompts.py`

|  |  |
| --- | --- |
| ``` 23 24 25 26 27 28 29 30 31 32 33 ``` | ``` class Prompt(TypedDict):     """Prompt configuration to use for interacting with an OpenAI model."""      id: str     """The unique ID of the prompt."""      version: NotRequired[str]     """Optional version of the prompt."""      variables: NotRequired[dict[str, ResponsesPromptVariables]]     """Optional variables to substitute into the prompt.""" ``` |

#### id `instance-attribute`

```
id: str
```

The unique ID of the prompt.

#### version `instance-attribute`

```
version: NotRequired[str]
```

Optional version of the prompt.

#### variables `instance-attribute`

```
variables: NotRequired[dict[str, Variables]]
```

Optional variables to substitute into the prompt.

### GenerateDynamicPromptData `dataclass`

Inputs to a function that allows you to dynamically generate a prompt.

Source code in `src/agents/prompts.py`

|  |  |
| --- | --- |
| ``` 36 37 38 39 40 41 42 43 44 ``` | ``` @dataclass class GenerateDynamicPromptData:     """Inputs to a function that allows you to dynamically generate a prompt."""      context: RunContextWrapper[Any]     """The run context."""      agent: Agent[Any]     """The agent for which the prompt is being generated.""" ``` |

#### context `instance-attribute`

```
context: RunContextWrapper[Any]
```

The run context.

#### agent `instance-attribute`

```
agent: Agent[Any]
```

The agent for which the prompt is being generated.