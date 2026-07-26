---
url: https://openai.github.io/openai-agents-python/ref/memory/session/
title: `Session`
framework: openai
---

# `Session`

### Session

Bases: `Protocol`

Protocol for session implementations.

Session stores conversation history for a specific session, allowing
agents to maintain context without requiring explicit manual memory management.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 ``` | ``` @runtime_checkable class Session(Protocol):     """Protocol for session implementations.      Session stores conversation history for a specific session, allowing     agents to maintain context without requiring explicit manual memory management.     """      session_id: str     session_settings: SessionSettings | None = None      async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         """Retrieve the conversation history for this session.          Args:             limit: Maximum number of items to retrieve. If None, retrieves all items.                    When specified, returns the latest N items in chronological order.          Returns:             List of input items representing the conversation history         """         ...      async def add_items(self, items: list[TResponseInputItem]) -> None:         """Add new items to the conversation history.          Args:             items: List of input items to add to the history         """         ...      async def pop_item(self) -> TResponseInputItem | None:         """Remove and return the most recent item from the session.          Returns:             The most recent item if it exists, None if the session is empty         """         ...      async def clear_session(self) -> None:         """Clear all items for this session."""         ... ``` |

#### get\_items `async`

```
get_items(
    limit: int | None = None,
) -> list[TResponseInputItem]
```

Retrieve the conversation history for this session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `limit` | `int | None` | Maximum number of items to retrieve. If None, retrieves all items. When specified, returns the latest N items in chronological order. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `list[TResponseInputItem]` | List of input items representing the conversation history |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 ``` | ``` async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:     """Retrieve the conversation history for this session.      Args:         limit: Maximum number of items to retrieve. If None, retrieves all items.                When specified, returns the latest N items in chronological order.      Returns:         List of input items representing the conversation history     """     ... ``` |

#### add\_items `async`

```
add_items(items: list[TResponseInputItem]) -> None
```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | *required* |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 36 37 38 39 40 41 42 ``` | ``` async def add_items(self, items: list[TResponseInputItem]) -> None:     """Add new items to the conversation history.      Args:         items: List of input items to add to the history     """     ... ``` |

#### pop\_item `async`

```
pop_item() -> TResponseInputItem | None
```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 44 45 46 47 48 49 50 ``` | ``` async def pop_item(self) -> TResponseInputItem | None:     """Remove and return the most recent item from the session.      Returns:         The most recent item if it exists, None if the session is empty     """     ... ``` |

#### clear\_session `async`

```
clear_session() -> None
```

Clear all items for this session.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 52 53 54 ``` | ``` async def clear_session(self) -> None:     """Clear all items for this session."""     ... ``` |

### SessionABC

Bases: `ABC`

Abstract base class for session implementations.

Session stores conversation history for a specific session, allowing
agents to maintain context without requiring explicit manual memory management.

This ABC is intended for internal use and as a base class for concrete implementations.
Third-party libraries should implement the Session protocol instead.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ```  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 ``` | ``` class SessionABC(ABC):     """Abstract base class for session implementations.      Session stores conversation history for a specific session, allowing     agents to maintain context without requiring explicit manual memory management.      This ABC is intended for internal use and as a base class for concrete implementations.     Third-party libraries should implement the Session protocol instead.     """      session_id: str     session_settings: SessionSettings | None = None      @abstractmethod     async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         """Retrieve the conversation history for this session.          Args:             limit: Maximum number of items to retrieve. If None, retrieves all items.                    When specified, returns the latest N items in chronological order.          Returns:             List of input items representing the conversation history         """         ...      @abstractmethod     async def add_items(self, items: list[TResponseInputItem]) -> None:         """Add new items to the conversation history.          Args:             items: List of input items to add to the history         """         ...      @abstractmethod     async def pop_item(self) -> TResponseInputItem | None:         """Remove and return the most recent item from the session.          Returns:             The most recent item if it exists, None if the session is empty         """         ...      @abstractmethod     async def clear_session(self) -> None:         """Clear all items for this session."""         ... ``` |

#### get\_items `abstractmethod` `async`

```
get_items(
    limit: int | None = None,
) -> list[TResponseInputItem]
```

Retrieve the conversation history for this session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `limit` | `int | None` | Maximum number of items to retrieve. If None, retrieves all items. When specified, returns the latest N items in chronological order. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `list[TResponseInputItem]` | List of input items representing the conversation history |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 70 71 72 73 74 75 76 77 78 79 80 81 ``` | ``` @abstractmethod async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:     """Retrieve the conversation history for this session.      Args:         limit: Maximum number of items to retrieve. If None, retrieves all items.                When specified, returns the latest N items in chronological order.      Returns:         List of input items representing the conversation history     """     ... ``` |

#### add\_items `abstractmethod` `async`

```
add_items(items: list[TResponseInputItem]) -> None
```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | *required* |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 83 84 85 86 87 88 89 90 ``` | ``` @abstractmethod async def add_items(self, items: list[TResponseInputItem]) -> None:     """Add new items to the conversation history.      Args:         items: List of input items to add to the history     """     ... ``` |

#### pop\_item `abstractmethod` `async`

```
pop_item() -> TResponseInputItem | None
```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 92 93 94 95 96 97 98 99 ``` | ``` @abstractmethod async def pop_item(self) -> TResponseInputItem | None:     """Remove and return the most recent item from the session.      Returns:         The most recent item if it exists, None if the session is empty     """     ... ``` |

#### clear\_session `abstractmethod` `async`

```
clear_session() -> None
```

Clear all items for this session.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 101 102 103 104 ``` | ``` @abstractmethod async def clear_session(self) -> None:     """Clear all items for this session."""     ... ``` |

### OpenAIResponsesCompactionArgs

Bases: `TypedDict`

Arguments for the run\_compaction method.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 ``` | ``` class OpenAIResponsesCompactionArgs(TypedDict, total=False):     """Arguments for the run_compaction method."""      response_id: str     """The ID of the last response to use for compaction."""      compaction_mode: Literal["previous_response_id", "input", "auto"]     """How to provide history for compaction.      - "auto": Use input when the last response was not stored or no response ID is available.     - "previous_response_id": Use server-managed response history.     - "input": Send locally stored session items as input.     """      store: bool     """Whether the last model response was stored on the server.      When set to False, compaction should avoid "previous_response_id" unless explicitly requested.     """      force: bool     """Whether to force compaction even if the threshold is not met.""" ``` |

#### response\_id `instance-attribute`

```
response_id: str
```

The ID of the last response to use for compaction.

#### compaction\_mode `instance-attribute`

```
compaction_mode: Literal[
    "previous_response_id", "input", "auto"
]
```

How to provide history for compaction.

* "auto": Use input when the last response was not stored or no response ID is available.
* "previous\_response\_id": Use server-managed response history.
* "input": Send locally stored session items as input.

#### store `instance-attribute`

```
store: bool
```

Whether the last model response was stored on the server.

When set to False, compaction should avoid "previous\_response\_id" unless explicitly requested.

#### force `instance-attribute`

```
force: bool
```

Whether to force compaction even if the threshold is not met.

### OpenAIResponsesCompactionAwareSession

Bases: `Session`, `Protocol`

Protocol for session implementations that support responses compaction.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 131 132 133 134 135 136 137 ``` | ``` @runtime_checkable class OpenAIResponsesCompactionAwareSession(Session, Protocol):     """Protocol for session implementations that support responses compaction."""      async def run_compaction(self, args: OpenAIResponsesCompactionArgs | None = None) -> None:         """Run the compaction process for the session."""         ... ``` |

#### run\_compaction `async`

```
run_compaction(
    args: OpenAIResponsesCompactionArgs | None = None,
) -> None
```

Run the compaction process for the session.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 135 136 137 ``` | ``` async def run_compaction(self, args: OpenAIResponsesCompactionArgs | None = None) -> None:     """Run the compaction process for the session."""     ... ``` |

#### get\_items `async`

```
get_items(
    limit: int | None = None,
) -> list[TResponseInputItem]
```

Retrieve the conversation history for this session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `limit` | `int | None` | Maximum number of items to retrieve. If None, retrieves all items. When specified, returns the latest N items in chronological order. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `list[TResponseInputItem]` | List of input items representing the conversation history |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 ``` | ``` async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:     """Retrieve the conversation history for this session.      Args:         limit: Maximum number of items to retrieve. If None, retrieves all items.                When specified, returns the latest N items in chronological order.      Returns:         List of input items representing the conversation history     """     ... ``` |

#### add\_items `async`

```
add_items(items: list[TResponseInputItem]) -> None
```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | *required* |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 36 37 38 39 40 41 42 ``` | ``` async def add_items(self, items: list[TResponseInputItem]) -> None:     """Add new items to the conversation history.      Args:         items: List of input items to add to the history     """     ... ``` |

#### pop\_item `async`

```
pop_item() -> TResponseInputItem | None
```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 44 45 46 47 48 49 50 ``` | ``` async def pop_item(self) -> TResponseInputItem | None:     """Remove and return the most recent item from the session.      Returns:         The most recent item if it exists, None if the session is empty     """     ... ``` |

#### clear\_session `async`

```
clear_session() -> None
```

Clear all items for this session.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 52 53 54 ``` | ``` async def clear_session(self) -> None:     """Clear all items for this session."""     ... ``` |

### is\_openai\_responses\_compaction\_aware\_session

```
is_openai_responses_compaction_aware_session(
    session: Session | None,
) -> TypeGuard[OpenAIResponsesCompactionAwareSession]
```

Check if a session supports responses compaction.

Source code in `src/agents/memory/session.py`

|  |  |
| --- | --- |
| ``` 140 141 142 143 144 145 146 147 148 149 150 ``` | ``` def is_openai_responses_compaction_aware_session(     session: Session | None, ) -> TypeGuard[OpenAIResponsesCompactionAwareSession]:     """Check if a session supports responses compaction."""     if session is None:         return False     try:         run_compaction = getattr(session, "run_compaction", None)     except Exception:         return False     return callable(run_compaction) ``` |