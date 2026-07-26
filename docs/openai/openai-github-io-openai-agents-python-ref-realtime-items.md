---
url: https://openai.github.io/openai-agents-python/ref/realtime/items/
title: `Items`
framework: openai
---

# `Items`

### RealtimeMessageItem `module-attribute`

```
RealtimeMessageItem = Annotated[
    SystemMessageItem
    | UserMessageItem
    | AssistantMessageItem,
    Field(discriminator="role"),
]
```

A message item that can be from system, user, or assistant.

### RealtimeItem `module-attribute`

```
RealtimeItem = RealtimeMessageItem | RealtimeToolCallItem
```

A realtime item that can be a message or tool call.

### InputText

Bases: `BaseModel`

Text input content for realtime messages.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ```  8  9 10 11 12 13 14 15 16 17 18 ``` | ``` class InputText(BaseModel):     """Text input content for realtime messages."""      type: Literal["input_text"] = "input_text"     """The type identifier for text input."""      text: str | None = None     """The text content."""      # Allow extra data     model_config = ConfigDict(extra="allow") ``` |

#### type `class-attribute` `instance-attribute`

```
type: Literal['input_text'] = 'input_text'
```

The type identifier for text input.

#### text `class-attribute` `instance-attribute`

```
text: str | None = None
```

The text content.

### InputAudio

Bases: `BaseModel`

Audio input content for realtime messages.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ``` 21 22 23 24 25 26 27 28 29 30 31 32 33 34 ``` | ``` class InputAudio(BaseModel):     """Audio input content for realtime messages."""      type: Literal["input_audio"] = "input_audio"     """The type identifier for audio input."""      audio: str | None = None     """The base64-encoded audio data."""      transcript: str | None = None     """The transcript of the audio, if available."""      # Allow extra data     model_config = ConfigDict(extra="allow") ``` |

#### type `class-attribute` `instance-attribute`

```
type: Literal['input_audio'] = 'input_audio'
```

The type identifier for audio input.

#### audio `class-attribute` `instance-attribute`

```
audio: str | None = None
```

The base64-encoded audio data.

#### transcript `class-attribute` `instance-attribute`

```
transcript: str | None = None
```

The transcript of the audio, if available.

### InputImage

Bases: `BaseModel`

Image input content for realtime messages.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ``` 37 38 39 40 41 42 43 44 45 46 47 48 49 50 ``` | ``` class InputImage(BaseModel):     """Image input content for realtime messages."""      type: Literal["input_image"] = "input_image"     """The type identifier for image input."""      image_url: str | None = None     """Data/remote URL string (data:... or https:...)."""      detail: str | None = None     """Optional detail hint (e.g., 'auto', 'high', 'low')."""      # Allow extra data (e.g., `detail`)     model_config = ConfigDict(extra="allow") ``` |

#### type `class-attribute` `instance-attribute`

```
type: Literal['input_image'] = 'input_image'
```

The type identifier for image input.

#### image\_url `class-attribute` `instance-attribute`

```
image_url: str | None = None
```

Data/remote URL string (data:... or https:...).

#### detail `class-attribute` `instance-attribute`

```
detail: str | None = None
```

Optional detail hint (e.g., 'auto', 'high', 'low').

### AssistantText

Bases: `BaseModel`

Text content from the assistant in realtime responses.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ``` 53 54 55 56 57 58 59 60 61 62 63 ``` | ``` class AssistantText(BaseModel):     """Text content from the assistant in realtime responses."""      type: Literal["text"] = "text"     """The type identifier for text content."""      text: str | None = None     """The text content from the assistant."""      # Allow extra data     model_config = ConfigDict(extra="allow") ``` |

#### type `class-attribute` `instance-attribute`

```
type: Literal['text'] = 'text'
```

The type identifier for text content.

#### text `class-attribute` `instance-attribute`

```
text: str | None = None
```

The text content from the assistant.

### AssistantAudio

Bases: `BaseModel`

Audio content from the assistant in realtime responses.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ``` 66 67 68 69 70 71 72 73 74 75 76 77 78 79 ``` | ``` class AssistantAudio(BaseModel):     """Audio content from the assistant in realtime responses."""      type: Literal["audio"] = "audio"     """The type identifier for audio content."""      audio: str | None = None     """The base64-encoded audio data from the assistant."""      transcript: str | None = None     """The transcript of the audio response."""      # Allow extra data     model_config = ConfigDict(extra="allow") ``` |

#### type `class-attribute` `instance-attribute`

```
type: Literal['audio'] = 'audio'
```

The type identifier for audio content.

#### audio `class-attribute` `instance-attribute`

```
audio: str | None = None
```

The base64-encoded audio data from the assistant.

#### transcript `class-attribute` `instance-attribute`

```
transcript: str | None = None
```

The transcript of the audio response.

### SystemMessageItem

Bases: `BaseModel`

A system message item in realtime conversations.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ```  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 ``` | ``` class SystemMessageItem(BaseModel):     """A system message item in realtime conversations."""      item_id: str     """Unique identifier for this message item."""      previous_item_id: str | None = None     """ID of the previous item in the conversation."""      type: Literal["message"] = "message"     """The type identifier for message items."""      role: Literal["system"] = "system"     """The role identifier for system messages."""      content: list[InputText]     """List of text content for the system message."""      # Allow extra data     model_config = ConfigDict(extra="allow") ``` |

#### item\_id `instance-attribute`

```
item_id: str
```

Unique identifier for this message item.

#### previous\_item\_id `class-attribute` `instance-attribute`

```
previous_item_id: str | None = None
```

ID of the previous item in the conversation.

#### type `class-attribute` `instance-attribute`

```
type: Literal['message'] = 'message'
```

The type identifier for message items.

#### role `class-attribute` `instance-attribute`

```
role: Literal['system'] = 'system'
```

The role identifier for system messages.

#### content `instance-attribute`

```
content: list[InputText]
```

List of text content for the system message.

### UserMessageItem

Bases: `BaseModel`

A user message item in realtime conversations.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ``` 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 ``` | ``` class UserMessageItem(BaseModel):     """A user message item in realtime conversations."""      item_id: str     """Unique identifier for this message item."""      previous_item_id: str | None = None     """ID of the previous item in the conversation."""      type: Literal["message"] = "message"     """The type identifier for message items."""      role: Literal["user"] = "user"     """The role identifier for user messages."""      content: list[Annotated[InputText | InputAudio | InputImage, Field(discriminator="type")]]     """List of content items, can be text or audio."""      # Allow extra data     model_config = ConfigDict(extra="allow") ``` |

#### item\_id `instance-attribute`

```
item_id: str
```

Unique identifier for this message item.

#### previous\_item\_id `class-attribute` `instance-attribute`

```
previous_item_id: str | None = None
```

ID of the previous item in the conversation.

#### type `class-attribute` `instance-attribute`

```
type: Literal['message'] = 'message'
```

The type identifier for message items.

#### role `class-attribute` `instance-attribute`

```
role: Literal['user'] = 'user'
```

The role identifier for user messages.

#### content `instance-attribute`

```
content: list[
    Annotated[
        InputText | InputAudio | InputImage,
        Field(discriminator="type"),
    ]
]
```

List of content items, can be text or audio.

### AssistantMessageItem

Bases: `BaseModel`

An assistant message item in realtime conversations.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ``` 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 ``` | ``` class AssistantMessageItem(BaseModel):     """An assistant message item in realtime conversations."""      item_id: str     """Unique identifier for this message item."""      previous_item_id: str | None = None     """ID of the previous item in the conversation."""      type: Literal["message"] = "message"     """The type identifier for message items."""      role: Literal["assistant"] = "assistant"     """The role identifier for assistant messages."""      status: Literal["in_progress", "completed", "incomplete"] | None = None     """The status of the assistant's response."""      content: list[Annotated[AssistantText | AssistantAudio, Field(discriminator="type")]]     """List of content items from the assistant, can be text or audio."""      # Allow extra data     model_config = ConfigDict(extra="allow") ``` |

#### item\_id `instance-attribute`

```
item_id: str
```

Unique identifier for this message item.

#### previous\_item\_id `class-attribute` `instance-attribute`

```
previous_item_id: str | None = None
```

ID of the previous item in the conversation.

#### type `class-attribute` `instance-attribute`

```
type: Literal['message'] = 'message'
```

The type identifier for message items.

#### role `class-attribute` `instance-attribute`

```
role: Literal['assistant'] = 'assistant'
```

The role identifier for assistant messages.

#### status `class-attribute` `instance-attribute`

```
status: (
    Literal["in_progress", "completed", "incomplete"] | None
) = None
```

The status of the assistant's response.

#### content `instance-attribute`

```
content: list[
    Annotated[
        AssistantText | AssistantAudio,
        Field(discriminator="type"),
    ]
]
```

List of content items from the assistant, can be text or audio.

### RealtimeToolCallItem

Bases: `BaseModel`

A tool call item in realtime conversations.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ``` 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 ``` | ``` class RealtimeToolCallItem(BaseModel):     """A tool call item in realtime conversations."""      item_id: str     """Unique identifier for this tool call item."""      previous_item_id: str | None = None     """ID of the previous item in the conversation."""      call_id: str | None     """The call ID for this tool invocation."""      type: Literal["function_call"] = "function_call"     """The type identifier for function call items."""      status: Literal["in_progress", "completed"]     """The status of the tool call execution."""      arguments: str     """The JSON string arguments passed to the tool."""      name: str     """The name of the tool being called."""      output: str | None = None     """The output result from the tool execution."""      # Allow extra data     model_config = ConfigDict(extra="allow") ``` |

#### item\_id `instance-attribute`

```
item_id: str
```

Unique identifier for this tool call item.

#### previous\_item\_id `class-attribute` `instance-attribute`

```
previous_item_id: str | None = None
```

ID of the previous item in the conversation.

#### call\_id `instance-attribute`

```
call_id: str | None
```

The call ID for this tool invocation.

#### type `class-attribute` `instance-attribute`

```
type: Literal['function_call'] = 'function_call'
```

The type identifier for function call items.

#### status `instance-attribute`

```
status: Literal['in_progress', 'completed']
```

The status of the tool call execution.

#### arguments `instance-attribute`

```
arguments: str
```

The JSON string arguments passed to the tool.

#### name `instance-attribute`

```
name: str
```

The name of the tool being called.

#### output `class-attribute` `instance-attribute`

```
output: str | None = None
```

The output result from the tool execution.

### RealtimeResponse

Bases: `BaseModel`

A response from the realtime model.

Source code in `src/agents/realtime/items.py`

|  |  |
| --- | --- |
| ``` 193 194 195 196 197 198 199 200 ``` | ``` class RealtimeResponse(BaseModel):     """A response from the realtime model."""      id: str     """Unique identifier for this response."""      output: list[RealtimeMessageItem]     """List of message items in the response.""" ``` |

#### id `instance-attribute`

```
id: str
```

Unique identifier for this response.

#### output `instance-attribute`

```
output: list[RealtimeMessageItem]
```

List of message items in the response.