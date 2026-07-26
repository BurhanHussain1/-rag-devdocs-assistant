---
url: https://openai.github.io/openai-agents-python/ref/run_internal/agent_bindings/
title: `Agent Bindings`
framework: openai
---

# `Agent Bindings`

### AgentBindings `dataclass`

Bases: `Generic[TContext]`

Carry the public and execution agent identities for a turn.

Source code in `src/agents/run_internal/agent_bindings.py`

|  |  |
| --- | --- |
| ``` 16 17 18 19 20 21 ``` | ``` @dataclass(frozen=True) class AgentBindings(Generic[TContext]):     """Carry the public and execution agent identities for a turn."""      public_agent: Agent[TContext]     execution_agent: Agent[TContext] ``` |

### bind\_public\_agent

```
bind_public_agent(
    agent: Agent[TContext],
) -> AgentBindings[TContext]
```

Build bindings for non-rewritten execution where both identities are the same.

Source code in `src/agents/run_internal/agent_bindings.py`

|  |  |
| --- | --- |
| ``` 24 25 26 ``` | ``` def bind_public_agent(agent: Agent[TContext]) -> AgentBindings[TContext]:     """Build bindings for non-rewritten execution where both identities are the same."""     return AgentBindings(public_agent=agent, execution_agent=agent) ``` |

### bind\_execution\_agent

```
bind_execution_agent(
    *,
    public_agent: Agent[TContext],
    execution_agent: Agent[TContext],
) -> AgentBindings[TContext]
```

Build bindings for execution-only clones such as sandbox-prepared agents.

Source code in `src/agents/run_internal/agent_bindings.py`

|  |  |
| --- | --- |
| ``` 29 30 31 32 33 34 35 36 37 38 ``` | ``` def bind_execution_agent(     *,     public_agent: Agent[TContext],     execution_agent: Agent[TContext], ) -> AgentBindings[TContext]:     """Build bindings for execution-only clones such as sandbox-prepared agents."""     return AgentBindings(         public_agent=public_agent,         execution_agent=execution_agent,     ) ``` |