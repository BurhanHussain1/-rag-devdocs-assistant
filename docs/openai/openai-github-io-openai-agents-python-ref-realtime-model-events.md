---
url: https://openai.github.io/openai-agents-python/ref/realtime/model_events/
title: `Model Events`
framework: openai
---

# `Model Events`

### RealtimeModelErrorEvent `dataclass`

Represents a transport‑layer error.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 12 13 14 15 16 17 18 ``` | ``` @dataclass class RealtimeModelErrorEvent:     """Represents a transport‑layer error."""      error: Any      type: Literal["error"] = "error" ``` |

### RealtimeModelToolCallEvent `dataclass`

Model attempted a tool/function call.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 21 22 23 24 25 26 27 28 29 30 31 32 ``` | ``` @dataclass class RealtimeModelToolCallEvent:     """Model attempted a tool/function call."""      name: str     call_id: str     arguments: str      id: str | None = None     previous_item_id: str | None = None      type: Literal["function_call"] = "function_call" ``` |

### RealtimeModelAudioEvent `dataclass`

Raw audio bytes emitted by the model.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 35 36 37 38 39 40 41 42 43 44 45 46 47 48 ``` | ``` @dataclass class RealtimeModelAudioEvent:     """Raw audio bytes emitted by the model."""      data: bytes     response_id: str      item_id: str     """The ID of the item containing audio."""      content_index: int     """The index of the audio content in `item.content`"""      type: Literal["audio"] = "audio" ``` |

#### item\_id `instance-attribute`

```
item_id: str
```

The ID of the item containing audio.

#### content\_index `instance-attribute`

```
content_index: int
```

The index of the audio content in `item.content`

### RealtimeModelAudioInterruptedEvent `dataclass`

Audio interrupted.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 51 52 53 54 55 56 57 58 59 60 61 ``` | ``` @dataclass class RealtimeModelAudioInterruptedEvent:     """Audio interrupted."""      item_id: str     """The ID of the item containing audio."""      content_index: int     """The index of the audio content in `item.content`"""      type: Literal["audio_interrupted"] = "audio_interrupted" ``` |

#### item\_id `instance-attribute`

```
item_id: str
```

The ID of the item containing audio.

#### content\_index `instance-attribute`

```
content_index: int
```

The index of the audio content in `item.content`

### RealtimeModelAudioDoneEvent `dataclass`

Audio done.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 64 65 66 67 68 69 70 71 72 73 74 ``` | ``` @dataclass class RealtimeModelAudioDoneEvent:     """Audio done."""      item_id: str     """The ID of the item containing audio."""      content_index: int     """The index of the audio content in `item.content`"""      type: Literal["audio_done"] = "audio_done" ``` |

#### item\_id `instance-attribute`

```
item_id: str
```

The ID of the item containing audio.

#### content\_index `instance-attribute`

```
content_index: int
```

The index of the audio content in `item.content`

### RealtimeModelInputAudioTranscriptionCompletedEvent `dataclass`

Input audio transcription completed.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 77 78 79 80 81 82 83 84 ``` | ``` @dataclass class RealtimeModelInputAudioTranscriptionCompletedEvent:     """Input audio transcription completed."""      item_id: str     transcript: str      type: Literal["input_audio_transcription_completed"] = "input_audio_transcription_completed" ``` |

### RealtimeModelInputAudioTimeoutTriggeredEvent `dataclass`

Input audio timeout triggered.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 87 88 89 90 91 92 93 94 95 ``` | ``` @dataclass class RealtimeModelInputAudioTimeoutTriggeredEvent:     """Input audio timeout triggered."""      item_id: str     audio_start_ms: int     audio_end_ms: int      type: Literal["input_audio_timeout_triggered"] = "input_audio_timeout_triggered" ``` |

### RealtimeModelTranscriptDeltaEvent `dataclass`

Partial transcript update.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ```  98  99 100 101 102 103 104 105 106 ``` | ``` @dataclass class RealtimeModelTranscriptDeltaEvent:     """Partial transcript update."""      item_id: str     delta: str     response_id: str      type: Literal["transcript_delta"] = "transcript_delta" ``` |

### RealtimeModelItemUpdatedEvent `dataclass`

Item added to the history or updated.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 109 110 111 112 113 114 115 ``` | ``` @dataclass class RealtimeModelItemUpdatedEvent:     """Item added to the history or updated."""      item: RealtimeItem      type: Literal["item_updated"] = "item_updated" ``` |

### RealtimeModelItemDeletedEvent `dataclass`

Item deleted from the history.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 118 119 120 121 122 123 124 ``` | ``` @dataclass class RealtimeModelItemDeletedEvent:     """Item deleted from the history."""      item_id: str      type: Literal["item_deleted"] = "item_deleted" ``` |

### RealtimeModelConnectionStatusEvent `dataclass`

Connection status changed.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 127 128 129 130 131 132 133 ``` | ``` @dataclass class RealtimeModelConnectionStatusEvent:     """Connection status changed."""      status: RealtimeConnectionStatus      type: Literal["connection_status"] = "connection_status" ``` |

### RealtimeModelTurnStartedEvent `dataclass`

Triggered when the model starts generating a response for a turn.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 136 137 138 139 140 ``` | ``` @dataclass class RealtimeModelTurnStartedEvent:     """Triggered when the model starts generating a response for a turn."""      type: Literal["turn_started"] = "turn_started" ``` |

### RealtimeModelCachedTokensDetails `dataclass`

Modality breakdown for cached Realtime input tokens.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 143 144 145 146 147 148 149 ``` | ``` @dataclass class RealtimeModelCachedTokensDetails:     """Modality breakdown for cached Realtime input tokens."""      text_tokens: int | None = None     audio_tokens: int | None = None     image_tokens: int | None = None ``` |

### RealtimeModelInputTokensDetails `dataclass`

Modality breakdown for Realtime input tokens.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 152 153 154 155 156 157 158 159 160 ``` | ``` @dataclass class RealtimeModelInputTokensDetails:     """Modality breakdown for Realtime input tokens."""      text_tokens: int | None = None     audio_tokens: int | None = None     image_tokens: int | None = None     cached_tokens: int | None = None     cached_tokens_details: RealtimeModelCachedTokensDetails | None = None ``` |

### RealtimeModelOutputTokensDetails `dataclass`

Modality breakdown for Realtime output tokens.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 163 164 165 166 167 168 ``` | ``` @dataclass class RealtimeModelOutputTokensDetails:     """Modality breakdown for Realtime output tokens."""      text_tokens: int | None = None     audio_tokens: int | None = None ``` |

### RealtimeModelUsageEvent `dataclass`

Token usage reported for a completed Realtime model response.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 171 172 173 174 175 176 177 178 179 180 181 182 183 184 ``` | ``` @dataclass class RealtimeModelUsageEvent:     """Token usage reported for a completed Realtime model response."""      usage: Usage     """Aggregate usage compatible with the shared SDK usage accounting."""      input_tokens_details: RealtimeModelInputTokensDetails | None = None     """Optional input-token modality details reported by the model provider."""      output_tokens_details: RealtimeModelOutputTokensDetails | None = None     """Optional output-token modality details reported by the model provider."""      type: Literal["usage"] = "usage" ``` |

#### usage `instance-attribute`

```
usage: Usage
```

Aggregate usage compatible with the shared SDK usage accounting.

#### input\_tokens\_details `class-attribute` `instance-attribute`

```
input_tokens_details: (
    RealtimeModelInputTokensDetails | None
) = None
```

Optional input-token modality details reported by the model provider.

#### output\_tokens\_details `class-attribute` `instance-attribute`

```
output_tokens_details: (
    RealtimeModelOutputTokensDetails | None
) = None
```

Optional output-token modality details reported by the model provider.

### RealtimeModelTurnEndedEvent `dataclass`

Triggered when the model finishes generating a response for a turn.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 187 188 189 190 191 ``` | ``` @dataclass class RealtimeModelTurnEndedEvent:     """Triggered when the model finishes generating a response for a turn."""      type: Literal["turn_ended"] = "turn_ended" ``` |

### RealtimeModelOtherEvent `dataclass`

Used as a catchall for vendor-specific events.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 194 195 196 197 198 199 200 ``` | ``` @dataclass class RealtimeModelOtherEvent:     """Used as a catchall for vendor-specific events."""      data: Any      type: Literal["other"] = "other" ``` |

### RealtimeModelExceptionEvent `dataclass`

Exception occurred during model operation.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 203 204 205 206 207 208 209 210 ``` | ``` @dataclass class RealtimeModelExceptionEvent:     """Exception occurred during model operation."""      exception: Exception     context: str | None = None      type: Literal["exception"] = "exception" ``` |

### RealtimeModelRawServerEvent `dataclass`

Raw events forwarded from the server.

Source code in `src/agents/realtime/model_events.py`

|  |  |
| --- | --- |
| ``` 213 214 215 216 217 218 219 ``` | ``` @dataclass class RealtimeModelRawServerEvent:     """Raw events forwarded from the server."""      data: Any      type: Literal["raw_server_event"] = "raw_server_event" ``` |