---
url: https://openai.github.io/openai-agents-python/ref/usage/
title: `Usage`
framework: openai
---

# `Usage`

### RequestUsage

Usage details for a single API request.

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ```  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 ``` | ``` @dataclass class RequestUsage:     """Usage details for a single API request."""      input_tokens: int     """Input tokens for this individual request."""      output_tokens: int     """Output tokens for this individual request."""      total_tokens: int     """Total tokens (input + output) for this individual request."""      input_tokens_details: InputTokensDetails     """Details about the input tokens for this individual request."""      output_tokens_details: OutputTokensDetails     """Details about the output tokens for this individual request.""" ``` |

#### input\_tokens `instance-attribute`

```
input_tokens: int
```

Input tokens for this individual request.

#### output\_tokens `instance-attribute`

```
output_tokens: int
```

Output tokens for this individual request.

#### total\_tokens `instance-attribute`

```
total_tokens: int
```

Total tokens (input + output) for this individual request.

#### input\_tokens\_details `instance-attribute`

```
input_tokens_details: InputTokensDetails
```

Details about the input tokens for this individual request.

#### output\_tokens\_details `instance-attribute`

```
output_tokens_details: OutputTokensDetails
```

Details about the output tokens for this individual request.

### Usage

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 ``` | ``` @dataclass class Usage:     requests: int = 0     """Total requests made to the LLM API."""      input_tokens: int = 0     """Total input tokens sent, across all requests."""      input_tokens_details: Annotated[         InputTokensDetails, BeforeValidator(_normalize_input_tokens_details)     ] = field(default_factory=_make_input_tokens_details)     """Details about the input tokens, matching responses API usage details."""     output_tokens: int = 0     """Total output tokens received, across all requests."""      output_tokens_details: Annotated[         OutputTokensDetails, BeforeValidator(_normalize_output_tokens_details)     ] = field(default_factory=lambda: OutputTokensDetails(reasoning_tokens=0))     """Details about the output tokens, matching responses API usage details."""      total_tokens: int = 0     """Total tokens sent and received, across all requests."""      request_usage_entries: list[RequestUsage] = field(default_factory=list)     """List of RequestUsage entries for accurate per-request cost calculation.      Each call to `add()` automatically creates an entry in this list if the added usage     represents a new request (i.e., has non-zero tokens).      Example:         For a run that makes 3 API calls with 100K, 150K, and 80K input tokens each,         the aggregated `input_tokens` would be 330K, but `request_usage_entries` would         preserve the [100K, 150K, 80K] breakdown, which could be helpful for detailed         cost calculation or context window management.     """      def __post_init__(self) -> None:         # Some providers don't populate optional token detail fields         # (cached_tokens, cache_write_tokens, reasoning_tokens), and the OpenAI SDK's generated         # code can bypass Pydantic validation (e.g., via model_construct),         # allowing None values. We normalize these to 0 to prevent TypeErrors.         input_details_none = self.input_tokens_details is None         input_cached_none = (             not input_details_none and self.input_tokens_details.cached_tokens is None         )         input_cache_write_none = (             not input_details_none             and getattr(self.input_tokens_details, "cache_write_tokens", 0) is None         )         if input_details_none or input_cached_none or input_cache_write_none:             self.input_tokens_details = _make_input_tokens_details(                 cached_tokens=_cached_tokens(self.input_tokens_details),                 cache_write_tokens=_cache_write_tokens(self.input_tokens_details),             )          output_details_none = self.output_tokens_details is None         output_reasoning_none = (             not output_details_none and self.output_tokens_details.reasoning_tokens is None         )         if output_details_none or output_reasoning_none:             self.output_tokens_details = OutputTokensDetails(reasoning_tokens=0)      def add(self, other: Usage) -> None:         """Add another Usage object to this one, aggregating all fields.          This method automatically preserves request_usage_entries.          Args:             other: The Usage object to add to this one.         """         self.requests += other.requests if other.requests else 0         self.input_tokens += other.input_tokens if other.input_tokens else 0         self.output_tokens += other.output_tokens if other.output_tokens else 0         self.total_tokens += other.total_tokens if other.total_tokens else 0          # Null guards for nested token details (other may bypass validation via model_construct)         other_cached = _cached_tokens(other.input_tokens_details)         other_cache_write = _cache_write_tokens(other.input_tokens_details)         other_reasoning = (             other.output_tokens_details.reasoning_tokens             if other.output_tokens_details and other.output_tokens_details.reasoning_tokens             else 0         )         self_cached = _cached_tokens(self.input_tokens_details)         self_cache_write = _cache_write_tokens(self.input_tokens_details)         self_reasoning = (             self.output_tokens_details.reasoning_tokens             if self.output_tokens_details and self.output_tokens_details.reasoning_tokens             else 0         )          self.input_tokens_details = _make_input_tokens_details(             cached_tokens=self_cached + other_cached,             cache_write_tokens=self_cache_write + other_cache_write,         )          self.output_tokens_details = OutputTokensDetails(             reasoning_tokens=self_reasoning + other_reasoning         )          # Automatically preserve request_usage_entries.         # If the other Usage already has individual request breakdowns, merge them         # (this preserves nested token details that would otherwise be discarded         # when synthesizing an entry from only the top-level fields).         if other.request_usage_entries:             self.request_usage_entries.extend(other.request_usage_entries)         elif other.requests == 1 and other.total_tokens > 0:             # Otherwise, if the other Usage represents a single request with tokens, record it.             input_details = other.input_tokens_details or _make_input_tokens_details()             output_details = other.output_tokens_details or OutputTokensDetails(reasoning_tokens=0)             request_usage = RequestUsage(                 input_tokens=other.input_tokens,                 output_tokens=other.output_tokens,                 total_tokens=other.total_tokens,                 input_tokens_details=input_details,                 output_tokens_details=output_details,             )             self.request_usage_entries.append(request_usage) ``` |

#### requests `class-attribute` `instance-attribute`

```
requests: int = 0
```

Total requests made to the LLM API.

#### input\_tokens `class-attribute` `instance-attribute`

```
input_tokens: int = 0
```

Total input tokens sent, across all requests.

#### input\_tokens\_details `class-attribute` `instance-attribute`

```
input_tokens_details: Annotated[
    InputTokensDetails,
    BeforeValidator(_normalize_input_tokens_details),
] = field(default_factory=_make_input_tokens_details)
```

Details about the input tokens, matching responses API usage details.

#### output\_tokens `class-attribute` `instance-attribute`

```
output_tokens: int = 0
```

Total output tokens received, across all requests.

#### output\_tokens\_details `class-attribute` `instance-attribute`

```
output_tokens_details: Annotated[
    OutputTokensDetails,
    BeforeValidator(_normalize_output_tokens_details),
] = field(
    default_factory=lambda: OutputTokensDetails(
        reasoning_tokens=0
    )
)
```

Details about the output tokens, matching responses API usage details.

#### total\_tokens `class-attribute` `instance-attribute`

```
total_tokens: int = 0
```

Total tokens sent and received, across all requests.

#### request\_usage\_entries `class-attribute` `instance-attribute`

```
request_usage_entries: list[RequestUsage] = field(
    default_factory=list
)
```

List of RequestUsage entries for accurate per-request cost calculation.

Each call to `add()` automatically creates an entry in this list if the added usage
represents a new request (i.e., has non-zero tokens).

Example

For a run that makes 3 API calls with 100K, 150K, and 80K input tokens each,
the aggregated `input_tokens` would be 330K, but `request_usage_entries` would
preserve the [100K, 150K, 80K] breakdown, which could be helpful for detailed
cost calculation or context window management.

#### add

```
add(other: Usage) -> None
```

Add another Usage object to this one, aggregating all fields.

This method automatically preserves request\_usage\_entries.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `other` | `Usage` | The Usage object to add to this one. | *required* |

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 ``` | ``` def add(self, other: Usage) -> None:     """Add another Usage object to this one, aggregating all fields.      This method automatically preserves request_usage_entries.      Args:         other: The Usage object to add to this one.     """     self.requests += other.requests if other.requests else 0     self.input_tokens += other.input_tokens if other.input_tokens else 0     self.output_tokens += other.output_tokens if other.output_tokens else 0     self.total_tokens += other.total_tokens if other.total_tokens else 0      # Null guards for nested token details (other may bypass validation via model_construct)     other_cached = _cached_tokens(other.input_tokens_details)     other_cache_write = _cache_write_tokens(other.input_tokens_details)     other_reasoning = (         other.output_tokens_details.reasoning_tokens         if other.output_tokens_details and other.output_tokens_details.reasoning_tokens         else 0     )     self_cached = _cached_tokens(self.input_tokens_details)     self_cache_write = _cache_write_tokens(self.input_tokens_details)     self_reasoning = (         self.output_tokens_details.reasoning_tokens         if self.output_tokens_details and self.output_tokens_details.reasoning_tokens         else 0     )      self.input_tokens_details = _make_input_tokens_details(         cached_tokens=self_cached + other_cached,         cache_write_tokens=self_cache_write + other_cache_write,     )      self.output_tokens_details = OutputTokensDetails(         reasoning_tokens=self_reasoning + other_reasoning     )      # Automatically preserve request_usage_entries.     # If the other Usage already has individual request breakdowns, merge them     # (this preserves nested token details that would otherwise be discarded     # when synthesizing an entry from only the top-level fields).     if other.request_usage_entries:         self.request_usage_entries.extend(other.request_usage_entries)     elif other.requests == 1 and other.total_tokens > 0:         # Otherwise, if the other Usage represents a single request with tokens, record it.         input_details = other.input_tokens_details or _make_input_tokens_details()         output_details = other.output_tokens_details or OutputTokensDetails(reasoning_tokens=0)         request_usage = RequestUsage(             input_tokens=other.input_tokens,             output_tokens=other.output_tokens,             total_tokens=other.total_tokens,             input_tokens_details=input_details,             output_tokens_details=output_details,         )         self.request_usage_entries.append(request_usage) ``` |

### deserialize\_usage

```
deserialize_usage(usage_data: Mapping[str, Any]) -> Usage
```

Rebuild a Usage object from serialized JSON data.

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 ``` | ``` def deserialize_usage(usage_data: Mapping[str, Any]) -> Usage:     """Rebuild a Usage object from serialized JSON data."""     input_tokens_details_raw = usage_data.get("input_tokens_details")     output_tokens_details_raw = usage_data.get("output_tokens_details")     input_details = _coerce_input_token_details(input_tokens_details_raw)     output_details = _coerce_token_details(         TypeAdapter(OutputTokensDetails),         output_tokens_details_raw or {"reasoning_tokens": 0},         OutputTokensDetails(reasoning_tokens=0),     )      request_entries: list[RequestUsage] = []     request_entries_raw = usage_data.get("request_usage_entries") or []     for entry in request_entries_raw:         request_entries.append(             RequestUsage(                 input_tokens=entry.get("input_tokens", 0),                 output_tokens=entry.get("output_tokens", 0),                 total_tokens=entry.get("total_tokens", 0),                 input_tokens_details=_coerce_input_token_details(entry.get("input_tokens_details")),                 output_tokens_details=_coerce_token_details(                     TypeAdapter(OutputTokensDetails),                     entry.get("output_tokens_details") or {"reasoning_tokens": 0},                     OutputTokensDetails(reasoning_tokens=0),                 ),             )         )      return Usage(         requests=usage_data.get("requests", 0),         input_tokens=usage_data.get("input_tokens", 0),         output_tokens=usage_data.get("output_tokens", 0),         total_tokens=usage_data.get("total_tokens", 0),         input_tokens_details=input_details,         output_tokens_details=output_details,         request_usage_entries=request_entries,     ) ``` |

### serialize\_usage

```
serialize_usage(usage: Usage) -> dict[str, Any]
```

Serialize a Usage object into a JSON-friendly dictionary.

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 ``` | ``` def serialize_usage(usage: Usage) -> dict[str, Any]:     """Serialize a Usage object into a JSON-friendly dictionary."""     input_details = _serialize_input_tokens_details(usage.input_tokens_details)     output_details = _serialize_usage_details(usage.output_tokens_details, {"reasoning_tokens": 0})      def _serialize_request_entry(entry: RequestUsage) -> dict[str, Any]:         return {             "input_tokens": entry.input_tokens,             "output_tokens": entry.output_tokens,             "total_tokens": entry.total_tokens,             "input_tokens_details": _serialize_input_tokens_details(entry.input_tokens_details),             "output_tokens_details": _serialize_usage_details(                 entry.output_tokens_details, {"reasoning_tokens": 0}             ),         }      return {         "requests": usage.requests,         "input_tokens": usage.input_tokens,         "input_tokens_details": [input_details],         "output_tokens": usage.output_tokens,         "output_tokens_details": [output_details],         "total_tokens": usage.total_tokens,         "request_usage_entries": [             _serialize_request_entry(entry) for entry in usage.request_usage_entries         ],     } ``` |

### model\_usage\_to\_span\_usage

```
model_usage_to_span_usage(usage: Usage) -> dict[str, Any]
```

Serialize full per-model-call usage for tracing span data.

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 336 337 338 339 340 341 342 343 344 345 346 347 348 ``` | ``` def model_usage_to_span_usage(usage: Usage) -> dict[str, Any]:     """Serialize full per-model-call usage for tracing span data."""     return {         "requests": usage.requests,         "input_tokens": usage.input_tokens,         "output_tokens": usage.output_tokens,         "total_tokens": usage.total_tokens,         "input_tokens_details": _serialize_input_tokens_details(usage.input_tokens_details),         "output_tokens_details": _serialize_usage_details(             usage.output_tokens_details,             {"reasoning_tokens": 0},         ),     } ``` |

### total\_usage\_to\_span\_metadata

```
total_usage_to_span_metadata(
    usage: Usage,
) -> dict[str, int]
```

Serialize aggregate task/run usage for tracing span metadata.

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 351 352 353 354 355 356 357 358 359 360 ``` | ``` def total_usage_to_span_metadata(usage: Usage) -> dict[str, int]:     """Serialize aggregate task/run usage for tracing span metadata."""     return {         "requests": usage.requests,         "input_tokens": usage.input_tokens,         "output_tokens": usage.output_tokens,         "total_tokens": usage.total_tokens,         "cached_input_tokens": _cached_input_tokens(usage),         "cache_write_input_tokens": _cache_write_input_tokens(usage),     } ``` |

### turn\_usage\_to\_span\_data

```
turn_usage_to_span_data(usage: Usage) -> dict[str, int]
```

Serialize aggregate per-turn usage for custom turn span data.

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 371 372 373 374 375 376 377 378 ``` | ``` def turn_usage_to_span_data(usage: Usage) -> dict[str, int]:     """Serialize aggregate per-turn usage for custom turn span data."""     return {         "input_tokens": usage.input_tokens,         "output_tokens": usage.output_tokens,         "cached_input_tokens": _cached_input_tokens(usage),         "cache_write_input_tokens": _cache_write_input_tokens(usage),     } ``` |

### task\_usage\_to\_span\_data

```
task_usage_to_span_data(usage: Usage) -> dict[str, int]
```

Serialize aggregate per-task usage for custom task span data.

Source code in `src/agents/usage.py`

|  |  |
| --- | --- |
| ``` 381 382 383 384 385 386 387 ``` | ``` def task_usage_to_span_data(usage: Usage) -> dict[str, int]:     """Serialize aggregate per-task usage for custom task span data."""     return {         **turn_usage_to_span_data(usage),         "requests": usage.requests,         "total_tokens": usage.total_tokens,     } ``` |