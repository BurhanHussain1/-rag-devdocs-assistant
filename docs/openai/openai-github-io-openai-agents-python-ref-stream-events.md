---
url: https://openai.github.io/openai-agents-python/ref/stream_events/
title: `Streaming events`
framework: openai
---

# `Streaming events`

### StreamEvent `module-attribute`

```
StreamEvent: TypeAlias = (
    RawResponsesStreamEvent
    | RunItemStreamEvent
    | AgentUpdatedStreamEvent
)
```

A streaming event from an agent.

### RawResponsesStreamEvent `dataclass`

Streaming event from the LLM. These are 'raw' events, i.e. they are directly passed through
from the LLM.

Source code in `src/agents/stream_events.py`

|  |  |
| --- | --- |
| ``` 10 11 12 13 14 15 16 17 18 19 20 ``` | ``` @dataclass class RawResponsesStreamEvent:     """Streaming event from the LLM. These are 'raw' events, i.e. they are directly passed through     from the LLM.     """      data: TResponseStreamEvent     """The raw responses streaming event from the LLM."""      type: Literal["raw_response_event"] = "raw_response_event"     """The type of the event.""" ``` |

#### data `instance-attribute`

```
data: TResponseStreamEvent
```

The raw responses streaming event from the LLM.

#### type `class-attribute` `instance-attribute`

```
type: Literal['raw_response_event'] = 'raw_response_event'
```

The type of the event.

### RunItemStreamEvent `dataclass`

Streaming events that wrap a `RunItem`. As the agent processes the LLM response, it will
generate these events for new messages, tool calls, tool outputs, handoffs, etc.

Source code in `src/agents/stream_events.py`

|  |  |
| --- | --- |
| ``` 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 ``` | ``` @dataclass class RunItemStreamEvent:     """Streaming events that wrap a `RunItem`. As the agent processes the LLM response, it will     generate these events for new messages, tool calls, tool outputs, handoffs, etc.     """      name: Literal[         "message_output_created",         "handoff_requested",         # This is misspelled, but we can't change it because that would be a breaking change         "handoff_occured",         "tool_called",         "tool_search_called",         "tool_search_output_created",         "tool_output",         "reasoning_item_created",         "mcp_approval_requested",         "mcp_approval_response",         "mcp_list_tools",     ]     """The name of the event."""      item: RunItem     """The item that was created."""      type: Literal["run_item_stream_event"] = "run_item_stream_event" ``` |

#### name `instance-attribute`

```
name: Literal[
    "message_output_created",
    "handoff_requested",
    "handoff_occured",
    "tool_called",
    "tool_search_called",
    "tool_search_output_created",
    "tool_output",
    "reasoning_item_created",
    "mcp_approval_requested",
    "mcp_approval_response",
    "mcp_list_tools",
]
```

The name of the event.

#### item `instance-attribute`

```
item: RunItem
```

The item that was created.

### AgentUpdatedStreamEvent `dataclass`

Event that notifies that there is a new agent running.

Source code in `src/agents/stream_events.py`

|  |  |
| --- | --- |
| ``` 51 52 53 54 55 56 57 58 ``` | ``` @dataclass class AgentUpdatedStreamEvent:     """Event that notifies that there is a new agent running."""      new_agent: Agent[Any]     """The new agent."""      type: Literal["agent_updated_stream_event"] = "agent_updated_stream_event" ``` |

#### new\_agent `instance-attribute`

```
new_agent: Agent[Any]
```

The new agent.