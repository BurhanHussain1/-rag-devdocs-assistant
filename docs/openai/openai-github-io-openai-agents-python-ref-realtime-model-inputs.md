---
url: https://openai.github.io/openai-agents-python/ref/realtime/model_inputs/
title: `Model Inputs`
framework: openai
---

# `Model Inputs`

### RealtimeModelUserInput `module-attribute`

```
RealtimeModelUserInput: TypeAlias = (
    str | RealtimeModelUserInputMessage
)
```

A user input to be sent to the model.

### RealtimeModelRawClientMessage

Bases: `TypedDict`

A raw message to be sent to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 12 13 14 15 16 17 ``` | ``` class RealtimeModelRawClientMessage(TypedDict):     """A raw message to be sent to the model."""      type: str  # explicitly required     other_data: NotRequired[dict[str, Any]]     """Merged into the message body.""" ``` |

#### other\_data `instance-attribute`

```
other_data: NotRequired[dict[str, Any]]
```

Merged into the message body.

### RealtimeModelInputTextContent

Bases: `TypedDict`

A piece of text to be sent to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 20 21 22 23 24 ``` | ``` class RealtimeModelInputTextContent(TypedDict):     """A piece of text to be sent to the model."""      type: Literal["input_text"]     text: str ``` |

### RealtimeModelInputImageContent

Bases: `TypedDict`

An image to be sent to the model.

The Realtime API expects `image_url` to be a string data/remote URL.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 27 28 29 30 31 32 33 34 35 36 37 38 ``` | ``` class RealtimeModelInputImageContent(TypedDict, total=False):     """An image to be sent to the model.      The Realtime API expects `image_url` to be a string data/remote URL.     """      type: Literal["input_image"]     image_url: str     """String URL (data:... or https:...)."""      detail: NotRequired[str]     """Optional detail hint such as 'high', 'low', or 'auto'.""" ``` |

#### image\_url `instance-attribute`

```
image_url: str
```

String URL (data:... or https:...).

#### detail `instance-attribute`

```
detail: NotRequired[str]
```

Optional detail hint such as 'high', 'low', or 'auto'.

### RealtimeModelUserInputMessage

Bases: `TypedDict`

A message to be sent to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 41 42 43 44 45 46 ``` | ``` class RealtimeModelUserInputMessage(TypedDict):     """A message to be sent to the model."""      type: Literal["message"]     role: Literal["user"]     content: list[RealtimeModelInputTextContent | RealtimeModelInputImageContent] ``` |

### RealtimeModelSendRawMessage `dataclass`

Send a raw message to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 56 57 58 59 60 61 ``` | ``` @dataclass class RealtimeModelSendRawMessage:     """Send a raw message to the model."""      message: RealtimeModelRawClientMessage     """The message to send.""" ``` |

#### message `instance-attribute`

```
message: RealtimeModelRawClientMessage
```

The message to send.

### RealtimeModelSendUserInput `dataclass`

Send a user input to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 64 65 66 67 68 69 ``` | ``` @dataclass class RealtimeModelSendUserInput:     """Send a user input to the model."""      user_input: RealtimeModelUserInput     """The user input to send.""" ``` |

#### user\_input `instance-attribute`

```
user_input: RealtimeModelUserInput
```

The user input to send.

### RealtimeModelSendAudio `dataclass`

Send audio to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 72 73 74 75 76 77 ``` | ``` @dataclass class RealtimeModelSendAudio:     """Send audio to the model."""      audio: bytes     commit: bool = False ``` |

### RealtimeModelSendToolOutput `dataclass`

Send tool output to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 80 81 82 83 84 85 86 87 88 89 90 91 ``` | ``` @dataclass class RealtimeModelSendToolOutput:     """Send tool output to the model."""      tool_call: RealtimeModelToolCallEvent     """The tool call to send."""      output: str     """The output to send."""      start_response: bool     """Whether to start a response.""" ``` |

#### tool\_call `instance-attribute`

```
tool_call: RealtimeModelToolCallEvent
```

The tool call to send.

#### output `instance-attribute`

```
output: str
```

The output to send.

#### start\_response `instance-attribute`

```
start_response: bool
```

Whether to start a response.

### RealtimeModelSendInterrupt `dataclass`

Send an interrupt to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 94 95 96 97 98 99 ``` | ``` @dataclass class RealtimeModelSendInterrupt:     """Send an interrupt to the model."""      force_response_cancel: bool = False     """Force sending a response.cancel event even if automatic cancellation is enabled.""" ``` |

#### force\_response\_cancel `class-attribute` `instance-attribute`

```
force_response_cancel: bool = False
```

Force sending a response.cancel event even if automatic cancellation is enabled.

### RealtimeModelSendSessionUpdate `dataclass`

Send a session update to the model.

Source code in `src/agents/realtime/model_inputs.py`

|  |  |
| --- | --- |
| ``` 102 103 104 105 106 107 ``` | ``` @dataclass class RealtimeModelSendSessionUpdate:     """Send a session update to the model."""      session_settings: RealtimeSessionModelSettings     """The updated session settings to send.""" ``` |

#### session\_settings `instance-attribute`

```
session_settings: RealtimeSessionModelSettings
```

The updated session settings to send.