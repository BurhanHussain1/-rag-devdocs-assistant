---
url: https://openai.github.io/openai-agents-python/ref/memory/util/
title: `Util`
framework: openai
---

# `Util`

### SessionInputCallback `module-attribute`

```
SessionInputCallback = Callable[
    [list[TResponseInputItem], list[TResponseInputItem]],
    MaybeAwaitable[list[TResponseInputItem]],
]
```

A function that combines session history with new input items.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `history_items` |  | The list of items from the session history. | *required* |
| `new_items` |  | The list of new input items for the current turn. | *required* |

Returns:

| Type | Description |
| --- | --- |
|  | A list of combined items to be used as input for the agent. Can be sync or async. |