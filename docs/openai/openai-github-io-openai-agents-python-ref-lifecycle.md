---
url: https://openai.github.io/openai-agents-python/ref/lifecycle/
title: `Lifecycle`
framework: openai
---

# `Lifecycle`

### RunHooks `module-attribute`

```
RunHooks = RunHooksBase[TContext, Agent]
```

Run hooks when using `Agent`.

### AgentHooks `module-attribute`

```
AgentHooks = AgentHooksBase[TContext, Agent]
```

Agent hooks for `Agent`s.

### RunHooksBase

Bases: `Generic[TContext, TAgent]`

A class that receives callbacks on various lifecycle events in an agent run. Subclass and
override the methods you need.

#### on\_llm\_start `async`

```
on_llm_start(
    context: RunContextWrapper[TContext],
    agent: Agent[TContext],
    system_prompt: str | None,
    input_items: list[TResponseInputItem],
) -> None
```

Called just before invoking the LLM for this agent.

#### on\_llm\_end `async`

```
on_llm_end(
    context: RunContextWrapper[TContext],
    agent: Agent[TContext],
    response: ModelResponse,
) -> None
```

Called immediately after the LLM call returns for this agent.

#### on\_agent\_start `async`

```
on_agent_start(
    context: AgentHookContext[TContext], agent: TAgent
) -> None
```

Called before the agent is invoked. Called each time the current agent changes.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `context` | `AgentHookContext[TContext]` | The agent hook context. | *required* |
| `agent` | `TAgent` | The agent that is about to be invoked. | *required* |

#### on\_agent\_end `async`

```
on_agent_end(
    context: AgentHookContext[TContext],
    agent: TAgent,
    output: Any,
) -> None
```

Called when the agent produces a final output.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `context` | `AgentHookContext[TContext]` | The agent hook context. | *required* |
| `agent` | `TAgent` | The agent that produced the output. | *required* |
| `output` | `Any` | The final output produced by the agent. | *required* |

#### on\_handoff `async`

```
on_handoff(
    context: RunContextWrapper[TContext],
    from_agent: TAgent,
    to_agent: TAgent,
) -> None
```

Called when a handoff occurs.

#### on\_tool\_start `async`

```
on_tool_start(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
) -> None
```

Called immediately before a local tool is invoked.

For function-tool invocations, `context` is typically a `ToolContext` instance,
which exposes tool-call-specific metadata such as `tool_call_id`, `tool_name`,
and `tool_arguments`. Other local tool families may provide a plain
`RunContextWrapper` instead.

#### on\_tool\_end `async`

```
on_tool_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
    result: object,
) -> None
```

Called immediately after a local tool is invoked.

For function-tool invocations, `context` is typically a `ToolContext` instance,
which exposes tool-call-specific metadata such as `tool_call_id`, `tool_name`,
and `tool_arguments`. Other local tool families may provide a plain
`RunContextWrapper` instead.

Simple tool outputs are typically `str` values. Function tools may also return
structured tool output objects or any value the SDK can stringify before sending it to
the model.

### AgentHooksBase

Bases: `Generic[TContext, TAgent]`

A class that receives callbacks on various lifecycle events for a specific agent. You can
set this on `agent.hooks` to receive events for that specific agent.

Subclass and override the methods you need.

#### on\_start `async`

```
on_start(
    context: AgentHookContext[TContext], agent: TAgent
) -> None
```

Called before the agent is invoked. Called each time the running agent is changed to this
agent.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `context` | `AgentHookContext[TContext]` | The agent hook context. | *required* |
| `agent` | `TAgent` | This agent instance. | *required* |

#### on\_end `async`

```
on_end(
    context: AgentHookContext[TContext],
    agent: TAgent,
    output: Any,
) -> None
```

Called when the agent produces a final output.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `context` | `AgentHookContext[TContext]` | The agent hook context. | *required* |
| `agent` | `TAgent` | This agent instance. | *required* |
| `output` | `Any` | The final output produced by the agent. | *required* |

#### on\_handoff `async`

```
on_handoff(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    source: TAgent,
) -> None
```

Called when the agent is being handed off to. The `source` is the agent that is handing
off to this agent.

#### on\_tool\_start `async`

```
on_tool_start(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
) -> None
```

Called immediately before a local tool is invoked.

For function-tool invocations, `context` is typically a `ToolContext` instance,
which exposes tool-call-specific metadata such as `tool_call_id`, `tool_name`,
and `tool_arguments`. Other local tool families may provide a plain
`RunContextWrapper` instead.

#### on\_tool\_end `async`

```
on_tool_end(
    context: RunContextWrapper[TContext],
    agent: TAgent,
    tool: Tool,
    result: object,
) -> None
```

Called immediately after a local tool is invoked.

For function-tool invocations, `context` is typically a `ToolContext` instance,
which exposes tool-call-specific metadata such as `tool_call_id`, `tool_name`,
and `tool_arguments`. Other local tool families may provide a plain
`RunContextWrapper` instead.

Simple tool outputs are typically `str` values. Function tools may also return
structured tool output objects or any value the SDK can stringify before sending it to
the model.

#### on\_llm\_start `async`

```
on_llm_start(
    context: RunContextWrapper[TContext],
    agent: Agent[TContext],
    system_prompt: str | None,
    input_items: list[TResponseInputItem],
) -> None
```

Called immediately before the agent issues an LLM call.

#### on\_llm\_end `async`

```
on_llm_end(
    context: RunContextWrapper[TContext],
    agent: Agent[TContext],
    response: ModelResponse,
) -> None
```

Called immediately after the agent receives the LLM response.