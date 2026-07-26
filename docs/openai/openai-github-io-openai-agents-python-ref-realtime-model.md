---
url: https://openai.github.io/openai-agents-python/ref/realtime/model/
title: `Model`
framework: openai
---

# `Model`

### RealtimePlaybackState

Bases: `TypedDict`

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 18 19 20 21 22 23 24 25 26 ``` | ``` class RealtimePlaybackState(TypedDict):     current_item_id: str | None     """The item ID of the current item being played."""      current_item_content_index: int | None     """The index of the current item content being played."""      elapsed_ms: float | None     """The number of milliseconds of audio that have been played.""" ``` |

#### current\_item\_id `instance-attribute`

```
current_item_id: str | None
```

The item ID of the current item being played.

#### current\_item\_content\_index `instance-attribute`

```
current_item_content_index: int | None
```

The index of the current item content being played.

#### elapsed\_ms `instance-attribute`

```
elapsed_ms: float | None
```

The number of milliseconds of audio that have been played.

### RealtimePlaybackTracker

If you have custom playback logic or expect that audio is played with delays or at different
speeds, create an instance of RealtimePlaybackTracker and pass it to the session. You are
responsible for tracking the audio playback progress and calling `on_play_bytes` or
`on_play_ms` when the user has played some audio.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 ``` | ``` class RealtimePlaybackTracker:     """If you have custom playback logic or expect that audio is played with delays or at different     speeds, create an instance of RealtimePlaybackTracker and pass it to the session. You are     responsible for tracking the audio playback progress and calling `on_play_bytes` or     `on_play_ms` when the user has played some audio."""      def __init__(self) -> None:         self._format: RealtimeAudioFormat | None = None         # (item_id, item_content_index)         self._current_item: tuple[str, int] | None = None         self._elapsed_ms: float | None = None      def on_play_bytes(self, item_id: str, item_content_index: int, bytes: bytes) -> None:         """Called by you when you have played some audio.          Args:             item_id: The item ID of the audio being played.             item_content_index: The index of the audio content in `item.content`             bytes: The audio bytes that have been fully played.         """         ms = calculate_audio_length_ms(self._format, bytes)         self.on_play_ms(item_id, item_content_index, ms)      def on_play_ms(self, item_id: str, item_content_index: int, ms: float) -> None:         """Called by you when you have played some audio.          Args:             item_id: The item ID of the audio being played.             item_content_index: The index of the audio content in `item.content`             ms: The number of milliseconds of audio that have been played.         """         if self._current_item != (item_id, item_content_index):             self._current_item = (item_id, item_content_index)             self._elapsed_ms = ms         else:             assert self._elapsed_ms is not None             self._elapsed_ms += ms      def on_interrupted(self) -> None:         """Called by the model when the audio playback has been interrupted."""         self._current_item = None         self._elapsed_ms = None      def set_audio_format(self, format: RealtimeAudioFormat) -> None:         """Will be called by the model to set the audio format.          Args:             format: The audio format to use.         """         self._format = format      def get_state(self) -> RealtimePlaybackState:         """Will be called by the model to get the current playback state."""         if self._current_item is None:             return {                 "current_item_id": None,                 "current_item_content_index": None,                 "elapsed_ms": None,             }         assert self._elapsed_ms is not None          item_id, item_content_index = self._current_item         return {             "current_item_id": item_id,             "current_item_content_index": item_content_index,             "elapsed_ms": self._elapsed_ms,         } ``` |

#### on\_play\_bytes

```
on_play_bytes(
    item_id: str, item_content_index: int, bytes: bytes
) -> None
```

Called by you when you have played some audio.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `item_id` | `str` | The item ID of the audio being played. | *required* |
| `item_content_index` | `int` | The index of the audio content in `item.content` | *required* |
| `bytes` | `bytes` | The audio bytes that have been fully played. | *required* |

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 41 42 43 44 45 46 47 48 49 50 ``` | ``` def on_play_bytes(self, item_id: str, item_content_index: int, bytes: bytes) -> None:     """Called by you when you have played some audio.      Args:         item_id: The item ID of the audio being played.         item_content_index: The index of the audio content in `item.content`         bytes: The audio bytes that have been fully played.     """     ms = calculate_audio_length_ms(self._format, bytes)     self.on_play_ms(item_id, item_content_index, ms) ``` |

#### on\_play\_ms

```
on_play_ms(
    item_id: str, item_content_index: int, ms: float
) -> None
```

Called by you when you have played some audio.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `item_id` | `str` | The item ID of the audio being played. | *required* |
| `item_content_index` | `int` | The index of the audio content in `item.content` | *required* |
| `ms` | `float` | The number of milliseconds of audio that have been played. | *required* |

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 52 53 54 55 56 57 58 59 60 61 62 63 64 65 ``` | ``` def on_play_ms(self, item_id: str, item_content_index: int, ms: float) -> None:     """Called by you when you have played some audio.      Args:         item_id: The item ID of the audio being played.         item_content_index: The index of the audio content in `item.content`         ms: The number of milliseconds of audio that have been played.     """     if self._current_item != (item_id, item_content_index):         self._current_item = (item_id, item_content_index)         self._elapsed_ms = ms     else:         assert self._elapsed_ms is not None         self._elapsed_ms += ms ``` |

#### on\_interrupted

```
on_interrupted() -> None
```

Called by the model when the audio playback has been interrupted.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 67 68 69 70 ``` | ``` def on_interrupted(self) -> None:     """Called by the model when the audio playback has been interrupted."""     self._current_item = None     self._elapsed_ms = None ``` |

#### set\_audio\_format

```
set_audio_format(format: RealtimeAudioFormat) -> None
```

Will be called by the model to set the audio format.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `format` | `RealtimeAudioFormat` | The audio format to use. | *required* |

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 72 73 74 75 76 77 78 ``` | ``` def set_audio_format(self, format: RealtimeAudioFormat) -> None:     """Will be called by the model to set the audio format.      Args:         format: The audio format to use.     """     self._format = format ``` |

#### get\_state

```
get_state() -> RealtimePlaybackState
```

Will be called by the model to get the current playback state.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 ``` | ``` def get_state(self) -> RealtimePlaybackState:     """Will be called by the model to get the current playback state."""     if self._current_item is None:         return {             "current_item_id": None,             "current_item_content_index": None,             "elapsed_ms": None,         }     assert self._elapsed_ms is not None      item_id, item_content_index = self._current_item     return {         "current_item_id": item_id,         "current_item_content_index": item_content_index,         "elapsed_ms": self._elapsed_ms,     } ``` |

### RealtimeModelListener

Bases: `ABC`

A listener for realtime transport events.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ```  98  99 100 101 102 103 104 ``` | ``` class RealtimeModelListener(abc.ABC):     """A listener for realtime transport events."""      @abc.abstractmethod     async def on_event(self, event: RealtimeModelEvent) -> None:         """Called when an event is emitted by the realtime transport."""         pass ``` |

#### on\_event `abstractmethod` `async`

```
on_event(event: RealtimeModelEvent) -> None
```

Called when an event is emitted by the realtime transport.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 101 102 103 104 ``` | ``` @abc.abstractmethod async def on_event(self, event: RealtimeModelEvent) -> None:     """Called when an event is emitted by the realtime transport."""     pass ``` |

### RealtimeModelConfig

Bases: `TypedDict`

Options for connecting to a realtime model.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 ``` | ``` class RealtimeModelConfig(TypedDict):     """Options for connecting to a realtime model."""      api_key: NotRequired[str | Callable[[], MaybeAwaitable[str]]]     """The API key (or function that returns a key) to use when connecting. If unset, the model will     try to use a sane default. For example, the OpenAI Realtime model will try to use the     `OPENAI_API_KEY`  environment variable.     """      url: NotRequired[str]     """The URL to use when connecting. If unset, the model will use a sane default. For example,     the OpenAI Realtime model will use the default OpenAI WebSocket URL.     """      headers: NotRequired[dict[str, str]]     """The headers to use when connecting. If unset, the model will use a sane default.     Note that, when you set this, authorization header won't be set under the hood.     e.g., {"api-key": "your api key here"} for Azure OpenAI Realtime WebSocket connections.     """      initial_model_settings: NotRequired[RealtimeSessionModelSettings]     """The initial model settings to use when connecting."""      playback_tracker: NotRequired[RealtimePlaybackTracker]     """The playback tracker to use when tracking audio playback progress. If not set, the model will     use a default implementation that assumes audio is played immediately, at realtime speed.      A playback tracker is useful for interruptions. The model generates audio much faster than     realtime playback speed. So if there's an interruption, its useful for the model to know how     much of the audio has been played by the user. In low-latency scenarios, it's fine to assume     that audio is played back immediately at realtime speed. But in scenarios like phone calls or     other remote interactions, you can set a playback tracker that lets the model know when audio     is played to the user.     """      call_id: NotRequired[str]     """Attach to an existing realtime call instead of creating a new session.      When provided, the transport connects using the `call_id` query string parameter rather than a     model name. In this repository, the shipped example for this flow is SIP via the Realtime     Calls API.     """ ``` |

#### api\_key `instance-attribute`

```
api_key: NotRequired[
    str | Callable[[], MaybeAwaitable[str]]
]
```

The API key (or function that returns a key) to use when connecting. If unset, the model will
try to use a sane default. For example, the OpenAI Realtime model will try to use the
`OPENAI_API_KEY` environment variable.

#### url `instance-attribute`

```
url: NotRequired[str]
```

The URL to use when connecting. If unset, the model will use a sane default. For example,
the OpenAI Realtime model will use the default OpenAI WebSocket URL.

#### headers `instance-attribute`

```
headers: NotRequired[dict[str, str]]
```

The headers to use when connecting. If unset, the model will use a sane default.
Note that, when you set this, authorization header won't be set under the hood.
e.g., {"api-key": "your api key here"} for Azure OpenAI Realtime WebSocket connections.

#### initial\_model\_settings `instance-attribute`

```
initial_model_settings: NotRequired[
    RealtimeSessionModelSettings
]
```

The initial model settings to use when connecting.

#### playback\_tracker `instance-attribute`

```
playback_tracker: NotRequired[RealtimePlaybackTracker]
```

The playback tracker to use when tracking audio playback progress. If not set, the model will
use a default implementation that assumes audio is played immediately, at realtime speed.

A playback tracker is useful for interruptions. The model generates audio much faster than
realtime playback speed. So if there's an interruption, its useful for the model to know how
much of the audio has been played by the user. In low-latency scenarios, it's fine to assume
that audio is played back immediately at realtime speed. But in scenarios like phone calls or
other remote interactions, you can set a playback tracker that lets the model know when audio
is played to the user.

#### call\_id `instance-attribute`

```
call_id: NotRequired[str]
```

Attach to an existing realtime call instead of creating a new session.

When provided, the transport connects using the `call_id` query string parameter rather than a
model name. In this repository, the shipped example for this flow is SIP via the Realtime
Calls API.

### RealtimeModel

Bases: `ABC`

Interface for connecting to a realtime model and sending/receiving events.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 ``` | ``` class RealtimeModel(abc.ABC):     """Interface for connecting to a realtime model and sending/receiving events."""      @abc.abstractmethod     async def connect(self, options: RealtimeModelConfig) -> None:         """Establish a connection to the model and keep it alive."""         pass      @abc.abstractmethod     def add_listener(self, listener: RealtimeModelListener) -> None:         """Add a listener to the model."""         pass      @abc.abstractmethod     def remove_listener(self, listener: RealtimeModelListener) -> None:         """Remove a listener from the model."""         pass      @abc.abstractmethod     async def send_event(self, event: RealtimeModelSendEvent) -> None:         """Send an event to the model."""         pass      @abc.abstractmethod     async def close(self) -> None:         """Close the session."""         pass ``` |

#### connect `abstractmethod` `async`

```
connect(options: RealtimeModelConfig) -> None
```

Establish a connection to the model and keep it alive.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 154 155 156 157 ``` | ``` @abc.abstractmethod async def connect(self, options: RealtimeModelConfig) -> None:     """Establish a connection to the model and keep it alive."""     pass ``` |

#### add\_listener `abstractmethod`

```
add_listener(listener: RealtimeModelListener) -> None
```

Add a listener to the model.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 159 160 161 162 ``` | ``` @abc.abstractmethod def add_listener(self, listener: RealtimeModelListener) -> None:     """Add a listener to the model."""     pass ``` |

#### remove\_listener `abstractmethod`

```
remove_listener(listener: RealtimeModelListener) -> None
```

Remove a listener from the model.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 164 165 166 167 ``` | ``` @abc.abstractmethod def remove_listener(self, listener: RealtimeModelListener) -> None:     """Remove a listener from the model."""     pass ``` |

#### send\_event `abstractmethod` `async`

```
send_event(event: RealtimeModelSendEvent) -> None
```

Send an event to the model.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 169 170 171 172 ``` | ``` @abc.abstractmethod async def send_event(self, event: RealtimeModelSendEvent) -> None:     """Send an event to the model."""     pass ``` |

#### close `abstractmethod` `async`

```
close() -> None
```

Close the session.

Source code in `src/agents/realtime/model.py`

|  |  |
| --- | --- |
| ``` 174 175 176 177 ``` | ``` @abc.abstractmethod async def close(self) -> None:     """Close the session."""     pass ``` |