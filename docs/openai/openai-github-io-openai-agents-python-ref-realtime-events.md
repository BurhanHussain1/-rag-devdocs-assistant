---
url: https://openai.github.io/openai-agents-python/ref/realtime/events/
title: Realtime Events
framework: openai
---

# Realtime Events

## Session Events

An event emitted by the realtime session.

## Event Types

### Agent Events

A new agent has started.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 20 21 22 23 24 25 26 27 28 29 30 ``` | ``` @dataclass class RealtimeAgentStartEvent:     """A new agent has started."""      agent: RealtimeAgent     """The new agent."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["agent_start"] = "agent_start" ``` |

### agent `instance-attribute`

```
agent: RealtimeAgent
```

The new agent.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

An agent has ended.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 33 34 35 36 37 38 39 40 41 42 43 ``` | ``` @dataclass class RealtimeAgentEndEvent:     """An agent has ended."""      agent: RealtimeAgent     """The agent that ended."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["agent_end"] = "agent_end" ``` |

### agent `instance-attribute`

```
agent: RealtimeAgent
```

The agent that ended.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

### Audio Events

Triggered when the agent generates new audio to be played.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 ``` | ``` @dataclass class RealtimeAudio:     """Triggered when the agent generates new audio to be played."""      audio: RealtimeModelAudioEvent     """The audio event from the model layer."""      item_id: str     """The ID of the item containing audio."""      content_index: int     """The index of the audio content in `item.content`"""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["audio"] = "audio" ``` |

### audio `instance-attribute`

```
audio: RealtimeModelAudioEvent
```

The audio event from the model layer.

### item\_id `instance-attribute`

```
item_id: str
```

The ID of the item containing audio.

### content\_index `instance-attribute`

```
content_index: int
```

The index of the audio content in `item.content`

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

Triggered when the agent stops generating audio.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 138 139 140 141 142 143 144 145 146 147 148 149 150 151 ``` | ``` @dataclass class RealtimeAudioEnd:     """Triggered when the agent stops generating audio."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      item_id: str     """The ID of the item containing audio."""      content_index: int     """The index of the audio content in `item.content`"""      type: Literal["audio_end"] = "audio_end" ``` |

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

### item\_id `instance-attribute`

```
item_id: str
```

The ID of the item containing audio.

### content\_index `instance-attribute`

```
content_index: int
```

The index of the audio content in `item.content`

Triggered when the agent is interrupted. Can be listened to by the user to stop audio
playback or give visual indicators to the user.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 ``` | ``` @dataclass class RealtimeAudioInterrupted:     """Triggered when the agent is interrupted. Can be listened to by the user to stop audio     playback or give visual indicators to the user.     """      info: RealtimeEventInfo     """Common info for all events, such as the context."""      item_id: str     """The ID of the item containing audio."""      content_index: int     """The index of the audio content in `item.content`"""      type: Literal["audio_interrupted"] = "audio_interrupted" ``` |

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

### item\_id `instance-attribute`

```
item_id: str
```

The ID of the item containing audio.

### content\_index `instance-attribute`

```
content_index: int
```

The index of the audio content in `item.content`

### Tool Events

An agent is starting a tool call.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 ``` | ``` @dataclass class RealtimeToolStart:     """An agent is starting a tool call."""      agent: RealtimeAgent     """The agent that updated."""      tool: Tool     """The tool being called."""      arguments: str     """The arguments passed to the tool as a JSON string."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["tool_start"] = "tool_start" ``` |

### agent `instance-attribute`

```
agent: RealtimeAgent
```

The agent that updated.

### tool `instance-attribute`

```
tool: Tool
```

The tool being called.

### arguments `instance-attribute`

```
arguments: str
```

The arguments passed to the tool as a JSON string.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

An agent has ended a tool call.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ```  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 ``` | ``` @dataclass class RealtimeToolEnd:     """An agent has ended a tool call."""      agent: RealtimeAgent     """The agent that ended the tool call."""      tool: Tool     """The tool that was called."""      arguments: str     """The arguments passed to the tool as a JSON string."""      output: Any     """The output of the tool call."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["tool_end"] = "tool_end" ``` |

### agent `instance-attribute`

```
agent: RealtimeAgent
```

The agent that ended the tool call.

### tool `instance-attribute`

```
tool: Tool
```

The tool that was called.

### arguments `instance-attribute`

```
arguments: str
```

The arguments passed to the tool as a JSON string.

### output `instance-attribute`

```
output: Any
```

The output of the tool call.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

### Handoff Events

An agent has handed off to another agent.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 46 47 48 49 50 51 52 53 54 55 56 57 58 59 ``` | ``` @dataclass class RealtimeHandoffEvent:     """An agent has handed off to another agent."""      from_agent: RealtimeAgent     """The agent that handed off."""      to_agent: RealtimeAgent     """The agent that was handed off to."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["handoff"] = "handoff" ``` |

### from\_agent `instance-attribute`

```
from_agent: RealtimeAgent
```

The agent that handed off.

### to\_agent `instance-attribute`

```
to_agent: RealtimeAgent
```

The agent that was handed off to.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

### Guardrail Events

A guardrail has been tripped and the agent has been interrupted.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 230 231 232 233 234 235 236 237 238 239 240 241 242 243 ``` | ``` @dataclass class RealtimeGuardrailTripped:     """A guardrail has been tripped and the agent has been interrupted."""      guardrail_results: list[OutputGuardrailResult]     """The results from all triggered guardrails."""      message: str     """The message that was being generated when the guardrail was triggered."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["guardrail_tripped"] = "guardrail_tripped" ``` |

### guardrail\_results `instance-attribute`

```
guardrail_results: list[OutputGuardrailResult]
```

The results from all triggered guardrails.

### message `instance-attribute`

```
message: str
```

The message that was being generated when the guardrail was triggered.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

### History Events

A new item has been added to the history.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 217 218 219 220 221 222 223 224 225 226 227 ``` | ``` @dataclass class RealtimeHistoryAdded:     """A new item has been added to the history."""      item: RealtimeItem     """The new item that was added to the history."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["history_added"] = "history_added" ``` |

### item `instance-attribute`

```
item: RealtimeItem
```

The new item that was added to the history.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

The history has been updated. Contains the full history of the session.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 204 205 206 207 208 209 210 211 212 213 214 ``` | ``` @dataclass class RealtimeHistoryUpdated:     """The history has been updated. Contains the full history of the session."""      history: list[RealtimeItem]     """The full history of the session."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["history_updated"] = "history_updated" ``` |

### history `instance-attribute`

```
history: list[RealtimeItem]
```

The full history of the session.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

### Error Events

An error has occurred.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 191 192 193 194 195 196 197 198 199 200 201 ``` | ``` @dataclass class RealtimeError:     """An error has occurred."""      error: Any     """The error that occurred."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["error"] = "error" ``` |

### error `instance-attribute`

```
error: Any
```

The error that occurred.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.

### Raw Model Events

Forwards raw events from the model layer.

Source code in `src/agents/realtime/events.py`

|  |  |
| --- | --- |
| ``` 125 126 127 128 129 130 131 132 133 134 135 ``` | ``` @dataclass class RealtimeRawModelEvent:     """Forwards raw events from the model layer."""      data: RealtimeModelEvent     """The raw data from the model layer."""      info: RealtimeEventInfo     """Common info for all events, such as the context."""      type: Literal["raw_model_event"] = "raw_model_event" ``` |

### data `instance-attribute`

```
data: RealtimeModelEvent
```

The raw data from the model layer.

### info `instance-attribute`

```
info: RealtimeEventInfo
```

Common info for all events, such as the context.