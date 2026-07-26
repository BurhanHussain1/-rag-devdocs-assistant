---
url: https://openai.github.io/openai-agents-python/ref/retry/
title: `Retry`
framework: openai
---

# `Retry`

### ModelRetryBackoffSettings

Backoff configuration for runner-managed model retries.

Source code in `src/agents/retry.py`

|  |  |
| --- | --- |
| ``` 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 ``` | ``` @pydantic_dataclass class ModelRetryBackoffSettings:     """Backoff configuration for runner-managed model retries."""      initial_delay: float | None = Field(default=None, ge=0)     """Delay in seconds before the first retry attempt."""      max_delay: float | None = Field(default=None, ge=0)     """Maximum delay in seconds between retry attempts."""      multiplier: float | None = Field(default=None, ge=0)     """Multiplier applied after each retry attempt."""      jitter: bool | None = None     """Whether to apply random jitter to the computed delay."""      def to_json_dict(self) -> dict[str, Any]:         return dataclasses.asdict(self) ``` |

#### initial\_delay `class-attribute` `instance-attribute`

```
initial_delay: float | None = Field(default=None, ge=0)
```

Delay in seconds before the first retry attempt.

#### max\_delay `class-attribute` `instance-attribute`

```
max_delay: float | None = Field(default=None, ge=0)
```

Maximum delay in seconds between retry attempts.

#### multiplier `class-attribute` `instance-attribute`

```
multiplier: float | None = Field(default=None, ge=0)
```

Multiplier applied after each retry attempt.

#### jitter `class-attribute` `instance-attribute`

```
jitter: bool | None = None
```

Whether to apply random jitter to the computed delay.

### ModelRetryNormalizedError `dataclass`

Normalized error facts exposed to retry policies.

Source code in `src/agents/retry.py`

|  |  |
| --- | --- |
| ``` 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 ``` | ``` @dataclass(init=False) class ModelRetryNormalizedError:     """Normalized error facts exposed to retry policies."""      status_code: int | None = None     error_code: str | None = None     message: str | None = None     request_id: str | None = None     retry_after: float | None = None     is_abort: bool = False     is_network_error: bool = False     is_timeout: bool = False      def __init__(         self,         status_code: int | None = _UNSET,         error_code: str | None = _UNSET,         message: str | None = _UNSET,         request_id: str | None = _UNSET,         retry_after: float | None = _UNSET,         is_abort: bool = _UNSET,         is_network_error: bool = _UNSET,         is_timeout: bool = _UNSET,     ) -> None:         explicit_fields: set[str] = set()          def assign(name: str, value: Any, default: Any) -> Any:             if value is _UNSET:                 return default             explicit_fields.add(name)             return value          self.status_code = assign("status_code", status_code, None)         self.error_code = assign("error_code", error_code, None)         self.message = assign("message", message, None)         self.request_id = assign("request_id", request_id, None)         self.retry_after = assign("retry_after", retry_after, None)         self.is_abort = assign("is_abort", is_abort, False)         self.is_network_error = assign("is_network_error", is_network_error, False)         self.is_timeout = assign("is_timeout", is_timeout, False)         self._explicit_fields = frozenset(explicit_fields) ``` |

### ModelRetryAdvice `dataclass`

Provider-specific retry guidance returned by model adapters.

Source code in `src/agents/retry.py`

|  |  |
| --- | --- |
| ```  92  93  94  95  96  97  98  99 100 ``` | ``` @dataclass class ModelRetryAdvice:     """Provider-specific retry guidance returned by model adapters."""      suggested: bool | None = None     retry_after: float | None = None     replay_safety: str | None = None     reason: str | None = None     normalized: ModelRetryNormalizedError | None = None ``` |

### ModelRetryAdviceRequest `dataclass`

Context passed to a model adapter when deriving retry advice.

Source code in `src/agents/retry.py`

|  |  |
| --- | --- |
| ``` 103 104 105 106 107 108 109 110 111 ``` | ``` @dataclass class ModelRetryAdviceRequest:     """Context passed to a model adapter when deriving retry advice."""      error: Exception     attempt: int     stream: bool     previous_response_id: str | None = None     conversation_id: str | None = None ``` |

### RetryDecision `dataclass`

Explicit retry decision returned by retry policies.

Source code in `src/agents/retry.py`

|  |  |
| --- | --- |
| ``` 114 115 116 117 118 119 120 121 122 ``` | ``` @dataclass class RetryDecision:     """Explicit retry decision returned by retry policies."""      retry: bool     delay: float | None = None     reason: str | None = None     _hard_veto: bool = field(default=False, init=False, repr=False, compare=False)     _approves_replay: bool = field(default=False, init=False, repr=False, compare=False) ``` |

### RetryPolicyContext `dataclass`

Context passed to runtime retry policy callbacks.

Source code in `src/agents/retry.py`

|  |  |
| --- | --- |
| ``` 125 126 127 128 129 130 131 132 133 134 ``` | ``` @dataclass class RetryPolicyContext:     """Context passed to runtime retry policy callbacks."""      error: Exception     attempt: int     max_retries: int     stream: bool     normalized: ModelRetryNormalizedError     provider_advice: ModelRetryAdvice | None = None ``` |

### ModelRetrySettings

Opt-in runner-managed retry settings for model calls.

Source code in `src/agents/retry.py`

|  |  |
| --- | --- |
| ``` 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 ``` | ``` @pydantic_dataclass class ModelRetrySettings:     """Opt-in runner-managed retry settings for model calls."""      max_retries: int | None = None     """Retries allowed after the initial model request."""      backoff: ModelRetryBackoffInput | None = None     """Backoff settings applied when the policy retries without an explicit delay."""      policy: Callable[..., Any] | None = Field(default=None, exclude=True, repr=False)     """Runtime-only retry policy callback. This field is not serialized."""      def __post_init__(self) -> None:         self.backoff = _coerce_backoff_settings(self.backoff)      def to_json_dict(self) -> dict[str, Any]:         backoff = _coerce_backoff_settings(self.backoff)         return {             "max_retries": self.max_retries,             "backoff": backoff.to_json_dict() if backoff is not None else None,         } ``` |

#### max\_retries `class-attribute` `instance-attribute`

```
max_retries: int | None = None
```

Retries allowed after the initial model request.

#### backoff `class-attribute` `instance-attribute`

```
backoff: ModelRetryBackoffInput | None = None
```

Backoff settings applied when the policy retries without an explicit delay.

#### policy `class-attribute` `instance-attribute`

```
policy: Callable[..., Any] | None = Field(
    default=None, exclude=True, repr=False
)
```

Runtime-only retry policy callback. This field is not serialized.