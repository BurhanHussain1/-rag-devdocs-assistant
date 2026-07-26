---
url: https://openai.github.io/openai-agents-python/ref/memory/session_settings/
title: `Session Settings`
framework: openai
---

# `Session Settings`

Session configuration settings.

### SessionSettings

Settings for session operations.

This class holds optional session configuration parameters that can be used
when interacting with session methods.

Source code in `src/agents/memory/session_settings.py`

|  |  |
| --- | --- |
| ``` 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 ``` | ``` @dataclass class SessionSettings:     """Settings for session operations.      This class holds optional session configuration parameters that can be used     when interacting with session methods.     """      limit: int | None = None     """Maximum number of items to retrieve. If None, retrieves all items."""      def resolve(self, override: SessionSettings | None) -> SessionSettings:         """Produce a new SessionSettings by overlaying any non-None values from the         override on top of this instance."""         if override is None:             return self          changes = {             field.name: getattr(override, field.name)             for field in fields(self)             if getattr(override, field.name) is not None         }          return replace(self, **changes)      def to_dict(self) -> dict[str, Any]:         """Convert settings to a dictionary."""         return dataclasses.asdict(self) ``` |

#### limit `class-attribute` `instance-attribute`

```
limit: int | None = None
```

Maximum number of items to retrieve. If None, retrieves all items.

#### resolve

```
resolve(
    override: SessionSettings | None,
) -> SessionSettings
```

Produce a new SessionSettings by overlaying any non-None values from the
override on top of this instance.

Source code in `src/agents/memory/session_settings.py`

|  |  |
| --- | --- |
| ``` 35 36 37 38 39 40 41 42 43 44 45 46 47 ``` | ``` def resolve(self, override: SessionSettings | None) -> SessionSettings:     """Produce a new SessionSettings by overlaying any non-None values from the     override on top of this instance."""     if override is None:         return self      changes = {         field.name: getattr(override, field.name)         for field in fields(self)         if getattr(override, field.name) is not None     }      return replace(self, **changes) ``` |

#### to\_dict

```
to_dict() -> dict[str, Any]
```

Convert settings to a dictionary.

Source code in `src/agents/memory/session_settings.py`

|  |  |
| --- | --- |
| ``` 49 50 51 ``` | ``` def to_dict(self) -> dict[str, Any]:     """Convert settings to a dictionary."""     return dataclasses.asdict(self) ``` |

### resolve\_session\_limit

```
resolve_session_limit(
    explicit_limit: int | None,
    settings: SessionSettings | None,
) -> int | None
```

Safely resolve the effective limit for session operations.

Source code in `src/agents/memory/session_settings.py`

|  |  |
| --- | --- |
| ``` 12 13 14 15 16 17 18 19 20 21 ``` | ``` def resolve_session_limit(     explicit_limit: int | None,     settings: SessionSettings | None, ) -> int | None:     """Safely resolve the effective limit for session operations."""     if explicit_limit is not None:         return explicit_limit     if settings is not None:         return settings.limit     return None ``` |