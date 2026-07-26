---
url: https://openai.github.io/openai-agents-python/ref/realtime/agent/
title: `RealtimeAgent`
framework: openai
---

# `RealtimeAgent`

Bases: `AgentBase`, `Generic[TContext]`

A specialized agent instance that is meant to be used within a `RealtimeSession` to build
voice agents. Due to the nature of this agent, some configuration options are not supported
that are supported by regular `Agent` instances. For example:
- `model` choice is not supported, as all RealtimeAgents will be handled by the same model
within a `RealtimeSession`.
- `modelSettings` is not supported, as all RealtimeAgents will be handled by the same model
within a `RealtimeSession`.
- `outputType` is not supported, as RealtimeAgents do not support structured outputs.
- `toolUseBehavior` is not supported, as all RealtimeAgents will be handled by the same model
within a `RealtimeSession`.
- `voice` can be configured on an `Agent` level; however, it cannot be changed after the first
agent within a `RealtimeSession` has spoken.

See `AgentBase` for base parameters that are shared with `Agent`s.

Source code in `src/agents/realtime/agent.py`

|  |  |
| --- | --- |
| ```  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 ``` | ``` @dataclass class RealtimeAgent(AgentBase, Generic[TContext]):     """A specialized agent instance that is meant to be used within a `RealtimeSession` to build     voice agents. Due to the nature of this agent, some configuration options are not supported     that are supported by regular `Agent` instances. For example:     - `model` choice is not supported, as all RealtimeAgents will be handled by the same model       within a `RealtimeSession`.     - `modelSettings` is not supported, as all RealtimeAgents will be handled by the same model       within a `RealtimeSession`.     - `outputType` is not supported, as RealtimeAgents do not support structured outputs.     - `toolUseBehavior` is not supported, as all RealtimeAgents will be handled by the same model       within a `RealtimeSession`.     - `voice` can be configured on an `Agent` level; however, it cannot be changed after the first       agent within a `RealtimeSession` has spoken.      See `AgentBase` for base parameters that are shared with `Agent`s.     """      instructions: (         str         | Callable[             [RunContextWrapper[TContext], RealtimeAgent[TContext]],             MaybeAwaitable[str],         ]         | None     ) = None     """The instructions for the agent. Will be used as the "system prompt" when this agent is     invoked. Describes what the agent should do, and how it responds.      Can either be a string, or a function that dynamically generates instructions for the agent. If     you provide a function, it will be called with the context and the agent instance. It must     return a string.     """      prompt: Prompt | None = None     """A prompt object. Prompts allow you to dynamically configure the instructions, tools     and other config for an agent outside of your code. Only usable with OpenAI models.     """      handoffs: list[RealtimeAgent[Any] | Handoff[TContext, RealtimeAgent[Any]]] = field(         default_factory=list     )     """Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,     and the agent can choose to delegate to them if relevant. Allows for separation of concerns and     modularity.     """      output_guardrails: list[OutputGuardrail[TContext]] = field(default_factory=list)     """A list of checks that run on the final output of the agent, after generating a response.     Runs only if the agent produces a final output.     """      hooks: RealtimeAgentHooks | None = None     """A class that receives callbacks on various lifecycle events for this agent.     """      def __post_init__(self) -> None:         if not isinstance(self.name, str):             raise TypeError(f"RealtimeAgent name must be a string, got {type(self.name).__name__}")         if not isinstance(self.tools, list):             raise TypeError(f"RealtimeAgent tools must be a list, got {type(self.tools).__name__}")         if not isinstance(self.handoffs, list):             raise TypeError(                 f"RealtimeAgent handoffs must be a list, got {type(self.handoffs).__name__}"             )         if (             self.instructions is not None             and not isinstance(self.instructions, str)             and not callable(self.instructions)         ):             raise TypeError(                 f"RealtimeAgent instructions must be a string, callable, or None, "                 f"got {type(self.instructions).__name__}"             )      def clone(self, **kwargs: Any) -> RealtimeAgent[TContext]:         """Make a copy of the agent, with the given arguments changed.          Notes:             - Uses `dataclasses.replace`, which performs a **shallow copy**.             - Mutable attributes like `tools` and `handoffs` are shallow-copied:               new list objects are created only if overridden, but their contents               (tool functions and handoff objects) are shared with the original.             - To modify these independently, pass new lists when calling `clone()`.          Example:             ```python             new_agent = agent.clone(instructions="New instructions")             ```         """         return dataclasses.replace(self, **kwargs)      async def get_system_prompt(self, run_context: RunContextWrapper[TContext]) -> str | None:         """Get the system prompt for the agent."""         if isinstance(self.instructions, str):             return self.instructions         elif callable(self.instructions):             if inspect.iscoroutinefunction(self.instructions):                 return await cast(Awaitable[str], self.instructions(run_context, self))             else:                 return cast(str, self.instructions(run_context, self))         elif self.instructions is not None:             logger.error("Instructions must be a string or a function, got %s", self.instructions)          return None ``` |

### instructions `class-attribute` `instance-attribute`

```
instructions: (
    str
    | Callable[
        [
            RunContextWrapper[TContext],
            RealtimeAgent[TContext],
        ],
        MaybeAwaitable[str],
    ]
    | None
) = None
```

The instructions for the agent. Will be used as the "system prompt" when this agent is
invoked. Describes what the agent should do, and how it responds.

Can either be a string, or a function that dynamically generates instructions for the agent. If
you provide a function, it will be called with the context and the agent instance. It must
return a string.

### prompt `class-attribute` `instance-attribute`

```
prompt: Prompt | None = None
```

A prompt object. Prompts allow you to dynamically configure the instructions, tools
and other config for an agent outside of your code. Only usable with OpenAI models.

### handoffs `class-attribute` `instance-attribute`

```
handoffs: list[
    RealtimeAgent[Any]
    | Handoff[TContext, RealtimeAgent[Any]]
] = field(default_factory=list)
```

Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,
and the agent can choose to delegate to them if relevant. Allows for separation of concerns and
modularity.

### output\_guardrails `class-attribute` `instance-attribute`

```
output_guardrails: list[OutputGuardrail[TContext]] = field(
    default_factory=list
)
```

A list of checks that run on the final output of the agent, after generating a response.
Runs only if the agent produces a final output.

### hooks `class-attribute` `instance-attribute`

```
hooks: RealtimeAgentHooks | None = None
```

A class that receives callbacks on various lifecycle events for this agent.

### name `instance-attribute`

```
name: str
```

The name of the agent.

### handoff\_description `class-attribute` `instance-attribute`

```
handoff_description: str | None = None
```

A description of the agent. This is used when the agent is used as a handoff, so that an
LLM knows what it does and when to invoke it.

### tools `class-attribute` `instance-attribute`

```
tools: list[Tool] = field(default_factory=list)
```

A list of tools that the agent can use.

### mcp\_servers `class-attribute` `instance-attribute`

```
mcp_servers: list[MCPServer] = field(default_factory=list)
```

A list of [Model Context Protocol](https://modelcontextprotocol.io/) servers that
the agent can use. Every time the agent runs, it will include tools from these servers in the
list of available tools.

NOTE: You are expected to manage the lifecycle of these servers. Specifically, you must call
`server.connect()` before passing it to the agent, and `server.cleanup()` when the server is no
longer needed. Consider using `MCPServerManager` from `agents.mcp` to keep connect/cleanup
in the same task.

### mcp\_config `class-attribute` `instance-attribute`

```
mcp_config: MCPConfig = field(
    default_factory=lambda: MCPConfig()
)
```

Configuration for MCP servers.

### clone

```
clone(**kwargs: Any) -> RealtimeAgent[TContext]
```

Make a copy of the agent, with the given arguments changed.

Notes

* Uses `dataclasses.replace`, which performs a **shallow copy**.
* Mutable attributes like `tools` and `handoffs` are shallow-copied:
  new list objects are created only if overridden, but their contents
  (tool functions and handoff objects) are shared with the original.
* To modify these independently, pass new lists when calling `clone()`.

Example

```
new_agent = agent.clone(instructions="New instructions")
```

Source code in `src/agents/realtime/agent.py`

|  |  |
| --- | --- |
| ``` 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 ``` | ``` def clone(self, **kwargs: Any) -> RealtimeAgent[TContext]:     """Make a copy of the agent, with the given arguments changed.      Notes:         - Uses `dataclasses.replace`, which performs a **shallow copy**.         - Mutable attributes like `tools` and `handoffs` are shallow-copied:           new list objects are created only if overridden, but their contents           (tool functions and handoff objects) are shared with the original.         - To modify these independently, pass new lists when calling `clone()`.      Example:         ```python         new_agent = agent.clone(instructions="New instructions")         ```     """     return dataclasses.replace(self, **kwargs) ``` |

### get\_system\_prompt `async`

```
get_system_prompt(
    run_context: RunContextWrapper[TContext],
) -> str | None
```

Get the system prompt for the agent.

Source code in `src/agents/realtime/agent.py`

|  |  |
| --- | --- |
| ``` 118 119 120 121 122 123 124 125 126 127 128 129 130 ``` | ``` async def get_system_prompt(self, run_context: RunContextWrapper[TContext]) -> str | None:     """Get the system prompt for the agent."""     if isinstance(self.instructions, str):         return self.instructions     elif callable(self.instructions):         if inspect.iscoroutinefunction(self.instructions):             return await cast(Awaitable[str], self.instructions(run_context, self))         else:             return cast(str, self.instructions(run_context, self))     elif self.instructions is not None:         logger.error("Instructions must be a string or a function, got %s", self.instructions)      return None ``` |

### get\_mcp\_tools `async`

```
get_mcp_tools(
    run_context: RunContextWrapper[TContext],
) -> list[Tool]
```

Fetches the available tools from the MCP servers.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 ``` | ``` async def get_mcp_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:     """Fetches the available tools from the MCP servers."""     convert_schemas_to_strict = self.mcp_config.get("convert_schemas_to_strict", False)     failure_error_function = self.mcp_config.get(         "failure_error_function", default_tool_error_function     )     include_server_in_tool_names = self.mcp_config.get("include_server_in_tool_names", False)     reserved_tool_names = (         await self._get_mcp_tool_reserved_names(run_context)         if include_server_in_tool_names         else None     )     return await MCPUtil.get_all_function_tools(         self.mcp_servers,         convert_schemas_to_strict,         run_context,         self,         failure_error_function=failure_error_function,         include_server_in_tool_names=include_server_in_tool_names,         reserved_tool_names=reserved_tool_names,     ) ``` |

### get\_all\_tools `async`

```
get_all_tools(
    run_context: RunContextWrapper[TContext],
) -> list[Tool]
```

All agent tools, including MCP tools and function tools.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 ``` | ``` async def get_all_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:     """All agent tools, including MCP tools and function tools."""     mcp_tools = await self.get_mcp_tools(run_context)      async def _check_tool_enabled(tool: Tool) -> bool:         if not isinstance(tool, FunctionTool):             return True          attr = tool.is_enabled         if isinstance(attr, bool):             return attr         res = attr(run_context, self)         if inspect.isawaitable(res):             return bool(await res)         return bool(res)      results = await asyncio.gather(*(_check_tool_enabled(t) for t in self.tools))     enabled: list[Tool] = [t for t, ok in zip(self.tools, results, strict=False) if ok]     all_tools: list[Tool] = prune_orphaned_tool_search_tools([*mcp_tools, *enabled])     _validate_codex_tool_name_collisions(all_tools)     return all_tools ``` |