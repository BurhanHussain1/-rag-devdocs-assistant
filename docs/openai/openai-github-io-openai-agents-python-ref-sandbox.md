---
url: https://openai.github.io/openai-agents-python/ref/sandbox/
title: `Sandbox`
framework: openai
---

# `Sandbox`

### SandboxAgent `dataclass`

Bases: `Agent[TContext]`

An `Agent` with sandbox-specific configuration.

Runtime transport details such as the sandbox client, client options, and live session are
provided at run time through `RunConfig(sandbox=...)`, not stored on the agent itself.

Source code in `src/agents/sandbox/sandbox_agent.py`

|  |  |
| --- | --- |
| ``` 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 ``` | ``` @dataclass class SandboxAgent(Agent[TContext]):     """An `Agent` with sandbox-specific configuration.      Runtime transport details such as the sandbox client, client options, and live session are     provided at run time through `RunConfig(sandbox=...)`, not stored on the agent itself.     """      default_manifest: Manifest | None = None     """Default sandbox manifest for new sessions created by `Runner` sandbox execution."""      base_instructions: (         str         | Callable[             [RunContextWrapper[TContext], Agent[TContext]], Awaitable[str | None] | str | None         ]         | None     ) = None     """Override for the SDK sandbox base prompt. Most callers should use `instructions`."""      capabilities: Sequence[Capability] = field(default_factory=Capabilities.default)     """Sandbox capabilities that can mutate the manifest, add instructions, and expose tools."""      run_as: User | str | None = None     """User identity used for model-facing sandbox tools such as shell, file reads, and patches."""      _sandbox_concurrency_guard: object | None = field(default=None, init=False, repr=False)      def __post_init__(self) -> None:         super().__post_init__()         if (             self.base_instructions is not None             and not isinstance(self.base_instructions, str)             and not callable(self.base_instructions)         ):             raise TypeError(                 f"SandboxAgent base_instructions must be a string, callable, or None, "                 f"got {type(self.base_instructions).__name__}"             )         if self.run_as is not None and not isinstance(self.run_as, str | User):             raise TypeError(                 f"SandboxAgent run_as must be a string, User, or None, "                 f"got {type(self.run_as).__name__}"             ) ``` |

#### name `instance-attribute`

```
name: str
```

The name of the agent.

#### handoff\_description `class-attribute` `instance-attribute`

```
handoff_description: str | None = None
```

A description of the agent. This is used when the agent is used as a handoff, so that an
LLM knows what it does and when to invoke it.

#### tools `class-attribute` `instance-attribute`

```
tools: list[Tool] = field(default_factory=list)
```

A list of tools that the agent can use.

#### mcp\_servers `class-attribute` `instance-attribute`

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

#### mcp\_config `class-attribute` `instance-attribute`

```
mcp_config: MCPConfig = field(
    default_factory=lambda: MCPConfig()
)
```

Configuration for MCP servers.

#### instructions `class-attribute` `instance-attribute`

```
instructions: (
    str
    | Callable[
        [RunContextWrapper[TContext], Agent[TContext]],
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

#### prompt `class-attribute` `instance-attribute`

```
prompt: Prompt | DynamicPromptFunction | None = None
```

A prompt object (or a function that returns a Prompt). Prompts allow you to dynamically
configure the instructions, tools and other config for an agent outside of your code. Only
usable with OpenAI models, using the Responses API.

#### handoffs `class-attribute` `instance-attribute`

```
handoffs: list[Agent[Any] | Handoff[TContext, Any]] = field(
    default_factory=list
)
```

Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,
and the agent can choose to delegate to them if relevant. Allows for separation of concerns and
modularity.

#### model `class-attribute` `instance-attribute`

```
model: str | Model | None = None
```

The model implementation to use when invoking the LLM.

By default, if not set, the agent will use the default model configured in
`agents.models.get_default_model()` (currently "gpt-5.4-mini").

#### model\_settings `class-attribute` `instance-attribute`

```
model_settings: ModelSettings = field(
    default_factory=get_default_model_settings
)
```

Configures model-specific tuning parameters (e.g. temperature, top\_p).

#### input\_guardrails `class-attribute` `instance-attribute`

```
input_guardrails: list[InputGuardrail[TContext]] = field(
    default_factory=list
)
```

A list of checks that run in parallel to the agent's execution, before generating a
response. Runs only if the agent is the first agent in the chain.

#### output\_guardrails `class-attribute` `instance-attribute`

```
output_guardrails: list[OutputGuardrail[TContext]] = field(
    default_factory=list
)
```

A list of checks that run on the final output of the agent, after generating a response.
Runs only if the agent produces a final output.

#### output\_type `class-attribute` `instance-attribute`

```
output_type: type[Any] | AgentOutputSchemaBase | None = None
```

The type of the output object. If not provided, the output will be `str`. In most cases,
you should pass a regular Python type (e.g. a dataclass, Pydantic model, TypedDict, etc).
You can customize this in two ways:
1. If you want non-strict schemas, pass `AgentOutputSchema(MyClass, strict_json_schema=False)`.
2. If you want to use a custom JSON schema (i.e. without using the SDK's automatic schema)
creation, subclass and pass an `AgentOutputSchemaBase` subclass.

#### hooks `class-attribute` `instance-attribute`

```
hooks: AgentHooks[TContext] | None = None
```

A class that receives callbacks on various lifecycle events for this agent.

#### tool\_use\_behavior `class-attribute` `instance-attribute`

```
tool_use_behavior: (
    Literal["run_llm_again", "stop_on_first_tool"]
    | StopAtTools
    | ToolsToFinalOutputFunction
) = "run_llm_again"
```

This lets you configure how tool use is handled.
- "run\_llm\_again": The default behavior. Tools are run, and then the LLM receives the results
and gets to respond.
- "stop\_on\_first\_tool": The output from the first tool call is treated as the final result.
In other words, it isn’t sent back to the LLM for further processing but is used directly
as the final output.
- A StopAtTools object: The agent will stop running if any of the tools listed in
`stop_at_tool_names` is called.
The final output will be the output of the first matching tool call.
The LLM does not process the result of the tool call.
- A function: If you pass a function, it will be called with the run context and the list of
tool results. It must return a `ToolsToFinalOutputResult`, which determines whether the tool
calls result in a final output.

NOTE: This configuration is specific to FunctionTools. Hosted tools, such as file search,
web search, etc. are always processed by the LLM.

#### reset\_tool\_choice `class-attribute` `instance-attribute`

```
reset_tool_choice: bool = True
```

Whether to reset the tool choice to the default value after a tool has been called. Defaults
to True. This ensures that the agent doesn't enter an infinite loop of tool usage.

#### default\_manifest `class-attribute` `instance-attribute`

```
default_manifest: Manifest | None = None
```

Default sandbox manifest for new sessions created by `Runner` sandbox execution.

#### base\_instructions `class-attribute` `instance-attribute`

```
base_instructions: (
    str
    | Callable[
        [RunContextWrapper[TContext], Agent[TContext]],
        Awaitable[str | None] | str | None,
    ]
    | None
) = None
```

Override for the SDK sandbox base prompt. Most callers should use `instructions`.

#### capabilities `class-attribute` `instance-attribute`

```
capabilities: Sequence[Capability] = field(
    default_factory=default
)
```

Sandbox capabilities that can mutate the manifest, add instructions, and expose tools.

#### run\_as `class-attribute` `instance-attribute`

```
run_as: User | str | None = None
```

User identity used for model-facing sandbox tools such as shell, file reads, and patches.

#### get\_mcp\_tools `async`

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

#### get\_all\_tools `async`

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

#### clone

```
clone(**kwargs: Any) -> Agent[TContext]
```

Make a copy of the agent, with the given arguments changed.
Notes:
- Uses `dataclasses.replace`, which performs a **shallow copy**.
- Mutable attributes like `tools` and `handoffs` are shallow-copied:
new list objects are created only if overridden, but their contents
(tool functions and handoff objects) are shared with the original.
- To modify these independently, pass new lists when calling `clone()`.
Example:

```
new_agent = agent.clone(instructions="New instructions")
```

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 ``` | ``` def clone(self, **kwargs: Any) -> Agent[TContext]:     """Make a copy of the agent, with the given arguments changed.     Notes:         - Uses `dataclasses.replace`, which performs a **shallow copy**.         - Mutable attributes like `tools` and `handoffs` are shallow-copied:           new list objects are created only if overridden, but their contents           (tool functions and handoff objects) are shared with the original.         - To modify these independently, pass new lists when calling `clone()`.     Example:         ```python         new_agent = agent.clone(instructions="New instructions")         ```     """     if (         "model" in kwargs         and "model_settings" not in kwargs         and _model_settings_match_implicit_model_defaults(self.model, self.model_settings)     ):         kwargs["model_settings"] = _initial_model_settings_for_model(kwargs["model"])     return dataclasses.replace(self, **kwargs) ``` |

#### as\_tool

```
as_tool(
    tool_name: str | None,
    tool_description: str | None,
    custom_output_extractor: Callable[
        [RunResult | RunResultStreaming], Awaitable[str]
    ]
    | None = None,
    is_enabled: bool
    | Callable[
        [RunContextWrapper[Any], AgentBase[Any]],
        MaybeAwaitable[bool],
    ] = True,
    on_stream: Callable[
        [AgentToolStreamEvent], MaybeAwaitable[None]
    ]
    | None = None,
    run_config: RunConfig | None = None,
    max_turns: int | None = None,
    hooks: RunHooks[TContext] | None = None,
    previous_response_id: str | None = None,
    conversation_id: str | None = None,
    session: Session | None = None,
    failure_error_function: ToolErrorFunction
    | None = default_tool_error_function,
    needs_approval: bool
    | Callable[
        [RunContextWrapper[Any], dict[str, Any], str],
        Awaitable[bool],
    ] = False,
    parameters: type[Any] | None = None,
    input_builder: StructuredToolInputBuilder | None = None,
    include_input_schema: bool = False,
) -> FunctionTool
```

Transform this agent into a tool, callable by other agents.

This is different from handoffs in two ways:
1. In handoffs, the new agent receives the conversation history. In this tool, the new agent
receives generated input.
2. In handoffs, the new agent takes over the conversation. In this tool, the new agent is
called as a tool, and the conversation is continued by the original agent.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `tool_name` | `str | None` | The name of the tool. If not provided, the agent's name will be used. | *required* |
| `tool_description` | `str | None` | The description of the tool, which should indicate what it does and when to use it. | *required* |
| `custom_output_extractor` | `Callable[[RunResult | RunResultStreaming], Awaitable[str]] | None` | A function that extracts the output from the agent. If not provided, the last message from the agent will be used. Nested run results expose `agent_tool_invocation` metadata when this agent is invoked via `as_tool()`. | `None` |
| `is_enabled` | `bool | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]]` | Whether the tool is enabled. Can be a bool or a callable that takes the run context and agent and returns whether the tool is enabled. Disabled tools are hidden from the LLM at runtime. | `True` |
| `on_stream` | `Callable[[AgentToolStreamEvent], MaybeAwaitable[None]] | None` | Optional callback (sync or async) to receive streaming events from the nested agent run. The callback receives an `AgentToolStreamEvent` containing the nested agent, the originating tool call (when available), and each stream event. When provided, the nested agent is executed in streaming mode. | `None` |
| `failure_error_function` | `ToolErrorFunction | None` | If provided, generate an error message when the tool (agent) run fails. The message is sent to the LLM. If None, the exception is raised instead. | `default_tool_error_function` |
| `needs_approval` | `bool | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]]` | Bool or callable to decide if this agent tool should pause for approval. | `False` |
| `parameters` | `type[Any] | None` | Structured input type for the tool arguments (dataclass or Pydantic model). | `None` |
| `input_builder` | `StructuredToolInputBuilder | None` | Optional function to build the nested agent input from structured data. | `None` |
| `include_input_schema` | `bool` | Whether to include the full JSON schema in structured input. | `False` |

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 832 833 834 835 836 837 838 839 840 841 842 843 844 845 846 847 848 849 850 851 852 853 854 855 856 857 858 859 860 861 862 863 864 865 866 867 868 869 870 871 872 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 915 916 917 918 919 920 921 922 923 924 925 926 927 928 929 930 931 932 933 934 935 936 ``` | ``` def as_tool(     self,     tool_name: str | None,     tool_description: str | None,     custom_output_extractor: (         Callable[[RunResult | RunResultStreaming], Awaitable[str]] | None     ) = None,     is_enabled: bool     | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]] = True,     on_stream: Callable[[AgentToolStreamEvent], MaybeAwaitable[None]] | None = None,     run_config: RunConfig | None = None,     max_turns: int | None = None,     hooks: RunHooks[TContext] | None = None,     previous_response_id: str | None = None,     conversation_id: str | None = None,     session: Session | None = None,     failure_error_function: ToolErrorFunction | None = default_tool_error_function,     needs_approval: bool     | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]] = False,     parameters: type[Any] | None = None,     input_builder: StructuredToolInputBuilder | None = None,     include_input_schema: bool = False, ) -> FunctionTool:     """Transform this agent into a tool, callable by other agents.      This is different from handoffs in two ways:     1. In handoffs, the new agent receives the conversation history. In this tool, the new agent        receives generated input.     2. In handoffs, the new agent takes over the conversation. In this tool, the new agent is        called as a tool, and the conversation is continued by the original agent.      Args:         tool_name: The name of the tool. If not provided, the agent's name will be used.         tool_description: The description of the tool, which should indicate what it does and             when to use it.         custom_output_extractor: A function that extracts the output from the agent. If not             provided, the last message from the agent will be used. Nested run results expose             `agent_tool_invocation` metadata when this agent is invoked via `as_tool()`.         is_enabled: Whether the tool is enabled. Can be a bool or a callable that takes the run             context and agent and returns whether the tool is enabled. Disabled tools are hidden             from the LLM at runtime.         on_stream: Optional callback (sync or async) to receive streaming events from the nested             agent run. The callback receives an `AgentToolStreamEvent` containing the nested             agent, the originating tool call (when available), and each stream event. When             provided, the nested agent is executed in streaming mode.         failure_error_function: If provided, generate an error message when the tool (agent) run             fails. The message is sent to the LLM. If None, the exception is raised instead.         needs_approval: Bool or callable to decide if this agent tool should pause for approval.         parameters: Structured input type for the tool arguments (dataclass or Pydantic model).         input_builder: Optional function to build the nested agent input from structured data.         include_input_schema: Whether to include the full JSON schema in structured input.     """      def _is_supported_parameters(value: Any) -> bool:         if not isinstance(value, type):             return False         if dataclasses.is_dataclass(value):             return True         return issubclass(value, BaseModel)      tool_name_resolved = tool_name or _transforms.transform_string_function_style(self.name)     tool_description_resolved = tool_description or ""     has_custom_parameters = parameters is not None     include_schema = bool(include_input_schema and has_custom_parameters)     should_capture_tool_input = bool(         has_custom_parameters or include_schema or input_builder is not None     )      if parameters is None:         params_adapter = TypeAdapter(AgentAsToolInput)         params_schema = ensure_strict_json_schema(params_adapter.json_schema())     else:         if not _is_supported_parameters(parameters):             raise TypeError("Agent tool parameters must be a dataclass or Pydantic model type.")         params_adapter = TypeAdapter(parameters)         params_schema = ensure_strict_json_schema(params_adapter.json_schema())      schema_info = build_structured_input_schema_info(         params_schema,         include_json_schema=include_schema,     )      def _normalize_tool_input(parsed: Any, tool_name: str) -> Any:         # Prefer JSON mode so structured params (datetime/UUID/Decimal, etc.) serialize cleanly.         try:             return params_adapter.dump_python(parsed, mode="json")         except Exception as exc:             raise ModelBehaviorError(                 f"Failed to serialize structured tool input for {tool_name}: {exc}"             ) from exc      async def _run_agent_impl(context: ToolContext, input_json: str) -> Any:         from .run import DEFAULT_MAX_TURNS, Runner         from .tool_context import ToolContext          tool_name = (             context.tool_name if isinstance(context, ToolContext) else tool_name_resolved         )         json_data = _parse_function_tool_json_input(             tool_name=tool_name,             input_json=input_json,         )         _log_function_tool_invocation(tool_name=tool_name, input_json=input_json)          try:             parsed_params = params_adapter.validate_python(json_data)         except ValidationError as exc:             raise ModelBehaviorError(f"Invalid JSON input for tool {tool_name}: {exc}") from exc          params_data = _normalize_tool_input(parsed_params, tool_name)         resolved_input = await resolve_agent_tool_input(             params=params_data,             schema_info=schema_info if should_capture_tool_input else None,             input_builder=input_builder,         )         if not isinstance(resolved_input, str) and not isinstance(resolved_input, list):             raise ModelBehaviorError("Agent tool called with invalid input")          resolved_max_turns = max_turns if max_turns is not None else DEFAULT_MAX_TURNS         resolved_run_config = run_config         if resolved_run_config is None and isinstance(context, ToolContext):             resolved_run_config = context.run_config         tool_state_scope_id = get_agent_tool_state_scope(context)         if isinstance(context, ToolContext):             # Use a fresh ToolContext to avoid sharing approval state with parent runs.             nested_context = ToolContext(                 context=context.context,                 usage=context.usage,                 tool_name=context.tool_name,                 tool_call_id=context.tool_call_id,                 tool_arguments=context.tool_arguments,                 tool_call=context.tool_call,                 tool_namespace=context.tool_namespace,                 agent=context.agent,                 run_config=resolved_run_config,             )             set_agent_tool_state_scope(nested_context, tool_state_scope_id)             if should_capture_tool_input:                 nested_context.tool_input = params_data         elif isinstance(context, RunContextWrapper):             if should_capture_tool_input:                 nested_context = RunContextWrapper(context=context.context)                 set_agent_tool_state_scope(nested_context, tool_state_scope_id)                 nested_context.tool_input = params_data             else:                 nested_context = context.context         else:             if should_capture_tool_input:                 nested_context = RunContextWrapper(context=context)                 set_agent_tool_state_scope(nested_context, tool_state_scope_id)                 nested_context.tool_input = params_data             else:                 nested_context = context         run_result: RunResult | RunResultStreaming | None = None         resume_state: RunState | None = None         should_record_run_result = True          def _nested_approvals_status(             interruptions: list[ToolApprovalItem],         ) -> Literal["approved", "pending", "rejected"]:             has_pending = False             has_decision = False             for interruption in interruptions:                 call_id = interruption.call_id                 if not call_id:                     has_pending = True                     continue                 tool_namespace = RunContextWrapper._resolve_tool_namespace(interruption)                 status = context.get_approval_status(                     interruption.tool_name or "",                     call_id,                     tool_namespace=tool_namespace,                     existing_pending=interruption,                 )                 if status is False:                     return "rejected"                 if status is True:                     has_decision = True                 if status is None:                     has_pending = True             if has_decision:                 return "approved"             if has_pending:                 return "pending"             return "approved"          def _apply_nested_approvals(             nested_context: RunContextWrapper[Any],             parent_context: RunContextWrapper[Any],             interruptions: list[ToolApprovalItem],         ) -> None:             def _find_mirrored_approval_record(                 interruption: ToolApprovalItem,                 *,                 approved: bool,             ) -> Any | None:                 candidate_keys = list(RunContextWrapper._resolve_approval_keys(interruption))                 for candidate_key in get_function_tool_approval_keys(                     tool_name=RunContextWrapper._resolve_tool_name(interruption),                     tool_namespace=RunContextWrapper._resolve_tool_namespace(interruption),                     tool_lookup_key=RunContextWrapper._resolve_tool_lookup_key(interruption),                     include_legacy_deferred_key=True,                 ):                     if candidate_key not in candidate_keys:                         candidate_keys.append(candidate_key)                 fallback: Any | None = None                 for candidate_key in candidate_keys:                     candidate = parent_context._approvals.get(candidate_key)                     if candidate is None:                         continue                     if approved and candidate.approved is True:                         return candidate                     if not approved and candidate.rejected is True:                         return candidate                     if fallback is None:                         fallback = candidate                 return fallback              for interruption in interruptions:                 call_id = interruption.call_id                 if not call_id:                     continue                 tool_name = RunContextWrapper._resolve_tool_name(interruption)                 tool_namespace = RunContextWrapper._resolve_tool_namespace(interruption)                 approval_key = RunContextWrapper._resolve_approval_key(interruption)                 status = parent_context.get_approval_status(                     tool_name,                     call_id,                     tool_namespace=tool_namespace,                     existing_pending=interruption,                 )                 if status is None:                     continue                 approval_record = parent_context._approvals.get(approval_key)                 if approval_record is None:                     approval_record = _find_mirrored_approval_record(                         interruption,                         approved=status,                     )                 if status is True:                     always_approve = bool(approval_record and approval_record.approved is True)                     nested_context.approve_tool(                         interruption,                         always_approve=always_approve,                     )                 else:                     always_reject = bool(approval_record and approval_record.rejected is True)                     nested_context.reject_tool(                         interruption,                         always_reject=always_reject,                     )          if isinstance(context, ToolContext) and context.tool_call is not None:             pending_run_result = peek_agent_tool_run_result(                 context.tool_call,                 scope_id=tool_state_scope_id,             )             if pending_run_result and getattr(pending_run_result, "interruptions", None):                 status = _nested_approvals_status(pending_run_result.interruptions)                 if status == "pending":                     run_result = pending_run_result                     should_record_run_result = False                 elif status in ("approved", "rejected"):                     resume_state = pending_run_result.to_state()                     if resume_state._context is not None:                         # Apply only explicit parent approvals to the nested resumed run.                         _apply_nested_approvals(                             resume_state._context,                             context,                             pending_run_result.interruptions,                         )                     consume_agent_tool_run_result(                         context.tool_call,                         scope_id=tool_state_scope_id,                     )          if run_result is None:             if on_stream is not None:                 stream_handler = on_stream                 run_result_streaming = Runner.run_streamed(                     starting_agent=cast(Agent[Any], self),                     input=resume_state or resolved_input,                     context=None if resume_state is not None else cast(Any, nested_context),                     run_config=resolved_run_config,                     max_turns=resolved_max_turns,                     hooks=hooks,                     previous_response_id=None                     if resume_state is not None                     else previous_response_id,                     conversation_id=None if resume_state is not None else conversation_id,                     session=session,                 )                 # Dispatch callbacks in the background so slow handlers do not block                 # event consumption.                 event_queue: asyncio.Queue[AgentToolStreamEvent | None] = asyncio.Queue()                  async def _run_handler(payload: AgentToolStreamEvent) -> None:                     """Execute the user callback while capturing exceptions."""                     try:                         maybe_result = stream_handler(payload)                         if inspect.isawaitable(maybe_result):                             await maybe_result                     except Exception:                         logger.exception(                             "Error while handling on_stream event for agent tool %s.",                             self.name,                         )                  async def dispatch_stream_events() -> None:                     while True:                         payload = await event_queue.get()                         is_sentinel = payload is None  # None marks the end of the stream.                         try:                             if payload is not None:                                 await _run_handler(payload)                         finally:                             event_queue.task_done()                          if is_sentinel:                             break                  dispatch_task = asyncio.create_task(dispatch_stream_events())                 stream_iteration_cancelled = False                  try:                     from .stream_events import AgentUpdatedStreamEvent                      current_agent = run_result_streaming.current_agent                     try:                         async for event in run_result_streaming.stream_events():                             if isinstance(event, AgentUpdatedStreamEvent):                                 current_agent = event.new_agent                              payload: AgentToolStreamEvent = {                                 "event": event,                                 "agent": current_agent,                                 "tool_call": context.tool_call,                             }                             await event_queue.put(payload)                     except asyncio.CancelledError:                         stream_iteration_cancelled = True                         raise                 finally:                     if stream_iteration_cancelled:                         dispatch_task.cancel()                         try:                             await dispatch_task                         except asyncio.CancelledError:                             pass                     else:                         await event_queue.put(None)                         await event_queue.join()                         await dispatch_task                 run_result = run_result_streaming             else:                 run_result = await Runner.run(                     starting_agent=cast(Agent[Any], self),                     input=resume_state or resolved_input,                     context=None if resume_state is not None else cast(Any, nested_context),                     run_config=resolved_run_config,                     max_turns=resolved_max_turns,                     hooks=hooks,                     previous_response_id=None                     if resume_state is not None                     else previous_response_id,                     conversation_id=None if resume_state is not None else conversation_id,                     session=session,                 )         assert run_result is not None          # Store the run result by tool call identity so nested interruptions can be read later.         interruptions = getattr(run_result, "interruptions", None)         if isinstance(context, ToolContext) and context.tool_call is not None and interruptions:             if should_record_run_result:                 record_agent_tool_run_result(                     context.tool_call,                     run_result,                     scope_id=tool_state_scope_id,                 )          if custom_output_extractor:             return await custom_output_extractor(run_result)          if run_result.final_output is not None and (             not isinstance(run_result.final_output, str) or run_result.final_output != ""         ):             return run_result.final_output          from .items import ItemHelpers, MessageOutputItem, ToolCallOutputItem          for item in reversed(run_result.new_items):             if isinstance(item, MessageOutputItem):                 text_output = ItemHelpers.text_message_output(item)                 if text_output:                     return text_output              if (                 isinstance(item, ToolCallOutputItem)                 and isinstance(item.output, str)                 and item.output             ):                 return item.output          return run_result.final_output      run_agent_tool = _build_wrapped_function_tool(         name=tool_name_resolved,         description=tool_description_resolved,         params_json_schema=params_schema,         invoke_tool_impl=_run_agent_impl,         on_handled_error=_build_handled_function_tool_error_handler(             span_message="Error running tool (non-fatal)",             span_message_for_json_decode_error="Error running tool",             log_label="Tool",         ),         failure_error_function=failure_error_function,         strict_json_schema=True,         is_enabled=is_enabled,         needs_approval=needs_approval,         tool_origin=ToolOrigin(             type=ToolOriginType.AGENT_AS_TOOL,             agent_name=self.name,             agent_tool_name=tool_name_resolved,         ),     )     run_agent_tool._is_agent_tool = True     run_agent_tool._agent_instance = self      return run_agent_tool ``` |

#### get\_prompt `async`

```
get_prompt(
    run_context: RunContextWrapper[TContext],
) -> ResponsePromptParam | None
```

Get the prompt for the agent.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 967 968 969 970 971 972 973 974 975 976 977 ``` | ``` async def get_prompt(     self, run_context: RunContextWrapper[TContext] ) -> ResponsePromptParam | None:     """Get the prompt for the agent."""     from ._public_agent import get_public_agent      return await PromptUtil.to_model_input(         self.prompt,         run_context,         cast(Agent[TContext], get_public_agent(self)),     ) ``` |

### Manifest

Bases: `BaseModel`

Source code in `src/agents/sandbox/manifest.py`

|  |  |
| --- | --- |
| ```  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 ``` | ``` class Manifest(BaseModel):     version: Literal[1] = 1     root: str = Field(default="/workspace")     entries: dict[str | Path, BaseEntry] = Field(default_factory=dict)     environment: Environment = Field(default_factory=Environment)     users: list[User] = Field(default_factory=list)     groups: list[Group] = Field(default_factory=list)     extra_path_grants: tuple[SandboxPathGrant, ...] = Field(default_factory=tuple)     remote_mount_command_allowlist: list[str] = Field(         default_factory=lambda: list(DEFAULT_REMOTE_MOUNT_COMMAND_ALLOWLIST)     )      @field_validator("entries", mode="before")     @classmethod     def _parse_entries(cls, value: object) -> dict[str | Path, BaseEntry]:         if value is None:             return {}         if not isinstance(value, Mapping):             raise TypeError(f"Artifact mapping must be a mapping, got {type(value).__name__}")         return {key: BaseEntry.parse(entry) for key, entry in value.items()}      @field_serializer("entries", when_used="json")     def _serialize_entries(self, entries: Mapping[str | Path, BaseEntry]) -> dict[str, object]:         out: dict[str, object] = {}         for key, entry in entries.items():             key_str = key.as_posix() if isinstance(key, Path) else str(key)             out[key_str] = entry.model_dump(mode="json")         return out      def validated_entries(self) -> dict[str | Path, BaseEntry]:         validated: dict[str | Path, BaseEntry] = dict(self.entries)         for _path, _artifact in self.iter_entries():             pass         return validated      def ephemeral_entry_paths(self, depth: int | None = 1) -> set[Path]:         _ = depth         return {path for path, artifact in self.iter_entries() if artifact.ephemeral}      def mount_targets(self) -> list[tuple[Mount, Path]]:         root = posix_path_as_path(coerce_posix_path(self.root))         mounts: list[tuple[Mount, Path]] = []         for rel_path, artifact in self.iter_entries():             if not isinstance(artifact, Mount):                 continue             dest = resolve_workspace_path(root, rel_path)             mount_path = artifact._resolve_mount_path_for_root(root, dest)             normalized_mount_path = self._normalize_in_workspace_path(root, mount_path)             if normalized_mount_path is not None:                 mount_path = normalized_mount_path             mounts.append((artifact, mount_path))         mounts.sort(key=lambda item: len(item[1].parts), reverse=True)         return mounts      def ephemeral_mount_targets(self) -> list[tuple[Mount, Path]]:         return [(artifact, path) for artifact, path in self.mount_targets() if artifact.ephemeral]      def ephemeral_persistence_paths(self, depth: int | None = 1) -> set[Path]:         _ = depth         root = posix_path_as_path(coerce_posix_path(self.root))         skip = self.ephemeral_entry_paths(depth=depth)         for _mount, mount_path in self.ephemeral_mount_targets():             try:                 rel_mount_path = mount_path.relative_to(root)             except ValueError:                 continue             if rel_mount_path.parts:                 skip.add(rel_mount_path)         return skip      @staticmethod     def _coerce_rel_path(path: str | PurePath) -> Path:         if (windows_path := windows_absolute_path(path)) is not None:             raise InvalidManifestPathError(rel=windows_path.as_posix(), reason="absolute")         return posix_path_as_path(coerce_posix_path(path))      @staticmethod     def _validate_rel_path(rel: Path) -> None:         if (windows_path := windows_absolute_path(rel)) is not None:             raise InvalidManifestPathError(rel=windows_path.as_posix(), reason="absolute")         rel_path = coerce_posix_path(rel)         if rel_path.is_absolute():             raise InvalidManifestPathError(rel=rel_path.as_posix(), reason="absolute")         if ".." in rel_path.parts:             raise InvalidManifestPathError(rel=rel_path.as_posix(), reason="escape_root")      @staticmethod     def _normalize_rel_path_within_root(rel: Path, *, original: Path) -> Path:         rel_path = coerce_posix_path(rel)         original_path = coerce_posix_path(original)         if (windows_path := windows_absolute_path(original)) is not None:             raise InvalidManifestPathError(rel=windows_path.as_posix(), reason="absolute")         if rel_path.is_absolute():             raise InvalidManifestPathError(rel=original_path.as_posix(), reason="absolute")          normalized_parts: list[str] = []         for part in rel_path.parts:             if part in ("", "."):                 continue             if part == "..":                 if not normalized_parts:                     raise InvalidManifestPathError(                         rel=original_path.as_posix(), reason="escape_root"                     )                 normalized_parts.pop()                 continue             normalized_parts.append(part)          return posix_path_as_path(PurePosixPath(*normalized_parts))      @classmethod     def _normalize_in_workspace_path(cls, root: Path, path: Path) -> Path | None:         root_path = coerce_posix_path(root)         if (windows_path := windows_absolute_path(path)) is not None:             raise InvalidManifestPathError(rel=windows_path.as_posix(), reason="absolute")         path_posix = coerce_posix_path(path)         if not path_posix.is_absolute():             normalized_rel = cls._normalize_rel_path_within_root(                 posix_path_as_path(path_posix),                 original=posix_path_as_path(path_posix),             )             return root / normalized_rel if normalized_rel.parts else root          try:             rel_path = path_posix.relative_to(root_path)         except ValueError:             return None          normalized_rel = cls._normalize_rel_path_within_root(             posix_path_as_path(rel_path),             original=posix_path_as_path(path_posix),         )         root_as_path = posix_path_as_path(root_path)         return root_as_path / normalized_rel if normalized_rel.parts else root_as_path      def iter_entries(self) -> Iterator[tuple[Path, BaseEntry]]:         stack = [             (self._coerce_rel_path(path), artifact)             for path, artifact in reversed(list(self.entries.items()))         ]         while stack:             rel_path, artifact = stack.pop()             self._validate_rel_path(rel_path)             yield rel_path, artifact             if not isinstance(artifact, Dir):                 continue              for child_name, child_artifact in reversed(list(artifact.children.items())):                 child_rel_path = rel_path / self._coerce_rel_path(child_name)                 stack.append((child_rel_path, child_artifact))      def describe(self, depth: int | None = 1) -> str:         """         print a nice fs representation of things inside root with inline descriptions         depth controls how deep the tree is rendered; None renders all levels         eg:          /workspace                      (root)         ├── repo/                       # /workspace/repo — my repo         │   └── README.md               # /workspace/repo/README.md         ├── data/                       # /workspace/data         │   └── config.json             # /workspace/data/config.json — config         ├── mount-data/                 # /workspace/mount-data (mount)         └── notes.txt                   # /workspace/notes.txt         ...         """         return render_manifest_description(             root=self.root,             entries=self.validated_entries(),             coerce_rel_path=self._coerce_rel_path,             depth=depth,         ) ``` |

#### describe

```
describe(depth: int | None = 1) -> str
```

print a nice fs representation of things inside root with inline descriptions
depth controls how deep the tree is rendered; None renders all levels
eg:

/workspace (root)
├── repo/ # /workspace/repo — my repo
│ └── README.md # /workspace/repo/README.md
├── data/ # /workspace/data
│ └── config.json # /workspace/data/config.json — config
├── mount-data/ # /workspace/mount-data (mount)
└── notes.txt # /workspace/notes.txt
...

Source code in `src/agents/sandbox/manifest.py`

|  |  |
| --- | --- |
| ``` 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 ``` | ``` def describe(self, depth: int | None = 1) -> str:     """     print a nice fs representation of things inside root with inline descriptions     depth controls how deep the tree is rendered; None renders all levels     eg:      /workspace                      (root)     ├── repo/                       # /workspace/repo — my repo     │   └── README.md               # /workspace/repo/README.md     ├── data/                       # /workspace/data     │   └── config.json             # /workspace/data/config.json — config     ├── mount-data/                 # /workspace/mount-data (mount)     └── notes.txt                   # /workspace/notes.txt     ...     """     return render_manifest_description(         root=self.root,         entries=self.validated_entries(),         coerce_rel_path=self._coerce_rel_path,         depth=depth,     ) ``` |

### SandboxRunConfig `dataclass`

Grouped sandbox runtime configuration for `Runner`.

Source code in `src/agents/run_config.py`

|  |  |
| --- | --- |
| ``` 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 ``` | ``` @dataclass class SandboxRunConfig:     """Grouped sandbox runtime configuration for `Runner`."""      client: BaseSandboxClient[Any] | None = None     """Sandbox client used to create or resume sandbox sessions."""      options: Any | None = None     """Sandbox-client-specific options used when creating a fresh session."""      session: BaseSandboxSession | None = None     """Live sandbox session override for the current process."""      session_state: SandboxSessionState | None = None     """Explicit sandbox session state to resume from when not using `RunState` payloads."""      manifest: Manifest | None = None     """Optional sandbox manifest override for fresh session creation."""      snapshot: SnapshotSpec | SnapshotBase | None = None     """Optional sandbox snapshot used for fresh session creation."""      concurrency_limits: SandboxConcurrencyLimits = field(default_factory=SandboxConcurrencyLimits)     """Concurrency limits for sandbox materialization work."""      archive_limits: SandboxArchiveLimits | None = None     """Resource limits for sandbox archive extraction.      Set to `None` to preserve the default behavior with no SDK archive resource limits.     Use `SandboxArchiveLimits()` to enable SDK defaults.     """ ``` |

#### client `class-attribute` `instance-attribute`

```
client: BaseSandboxClient[Any] | None = None
```

Sandbox client used to create or resume sandbox sessions.

#### options `class-attribute` `instance-attribute`

```
options: Any | None = None
```

Sandbox-client-specific options used when creating a fresh session.

#### session `class-attribute` `instance-attribute`

```
session: BaseSandboxSession | None = None
```

Live sandbox session override for the current process.

#### session\_state `class-attribute` `instance-attribute`

```
session_state: SandboxSessionState | None = None
```

Explicit sandbox session state to resume from when not using `RunState` payloads.

#### manifest `class-attribute` `instance-attribute`

```
manifest: Manifest | None = None
```

Optional sandbox manifest override for fresh session creation.

#### snapshot `class-attribute` `instance-attribute`

```
snapshot: SnapshotSpec | SnapshotBase | None = None
```

Optional sandbox snapshot used for fresh session creation.

#### concurrency\_limits `class-attribute` `instance-attribute`

```
concurrency_limits: SandboxConcurrencyLimits = field(
    default_factory=SandboxConcurrencyLimits
)
```

Concurrency limits for sandbox materialization work.

#### archive\_limits `class-attribute` `instance-attribute`

```
archive_limits: SandboxArchiveLimits | None = None
```

Resource limits for sandbox archive extraction.

Set to `None` to preserve the default behavior with no SDK archive resource limits.
Use `SandboxArchiveLimits()` to enable SDK defaults.

### Capability

Bases: `BaseModel`

Source code in `src/agents/sandbox/capabilities/capability.py`

|  |  |
| --- | --- |
| ``` 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 ``` | ``` class Capability(BaseModel):     model_config = ConfigDict(arbitrary_types_allowed=True)      type: str     session: BaseSandboxSession | None = Field(default=None, exclude=True)     run_as: User | None = Field(default=None, exclude=True)      def clone(self) -> "Capability":         """Return a per-run copy of this capability."""         cloned = self.model_copy(deep=False)         for name, value in self.__dict__.items():             cloned.__dict__[name] = _clone_capability_value(value)         return cloned      def bind(self, session: BaseSandboxSession) -> None:         """Bind a live session to this plugin (default no-op)."""         self.session = session      def bind_run_as(self, user: User | None) -> None:         """Bind the sandbox user identity for model-facing operations."""         self.run_as = user      def required_capability_types(self) -> set[str]:         """Return capability types that must be present alongside this capability."""         return set()      def tools(self) -> list[Tool]:         return []      def process_manifest(self, manifest: Manifest) -> Manifest:         return manifest      async def instructions(self, manifest: Manifest) -> str | None:         """Return a deterministic instruction fragment appended during run preparation."""         _ = manifest         return None      def sampling_params(self, sampling_params: dict[str, Any]) -> dict[str, Any]:         """Return additional model request parameters needed for this capability."""         _ = sampling_params         return {}      def process_context(self, context: list[TResponseInputItem]) -> list[TResponseInputItem]:         """Transform the model input context before sampling."""         return context ``` |

#### clone

```
clone() -> Capability
```

Return a per-run copy of this capability.

Source code in `src/agents/sandbox/capabilities/capability.py`

|  |  |
| --- | --- |
| ``` 22 23 24 25 26 27 ``` | ``` def clone(self) -> "Capability":     """Return a per-run copy of this capability."""     cloned = self.model_copy(deep=False)     for name, value in self.__dict__.items():         cloned.__dict__[name] = _clone_capability_value(value)     return cloned ``` |

#### bind

```
bind(session: BaseSandboxSession) -> None
```

Bind a live session to this plugin (default no-op).

Source code in `src/agents/sandbox/capabilities/capability.py`

|  |  |
| --- | --- |
| ``` 29 30 31 ``` | ``` def bind(self, session: BaseSandboxSession) -> None:     """Bind a live session to this plugin (default no-op)."""     self.session = session ``` |

#### bind\_run\_as

```
bind_run_as(user: User | None) -> None
```

Bind the sandbox user identity for model-facing operations.

Source code in `src/agents/sandbox/capabilities/capability.py`

|  |  |
| --- | --- |
| ``` 33 34 35 ``` | ``` def bind_run_as(self, user: User | None) -> None:     """Bind the sandbox user identity for model-facing operations."""     self.run_as = user ``` |

#### required\_capability\_types

```
required_capability_types() -> set[str]
```

Return capability types that must be present alongside this capability.

Source code in `src/agents/sandbox/capabilities/capability.py`

|  |  |
| --- | --- |
| ``` 37 38 39 ``` | ``` def required_capability_types(self) -> set[str]:     """Return capability types that must be present alongside this capability."""     return set() ``` |

#### instructions `async`

```
instructions(manifest: Manifest) -> str | None
```

Return a deterministic instruction fragment appended during run preparation.

Source code in `src/agents/sandbox/capabilities/capability.py`

|  |  |
| --- | --- |
| ``` 47 48 49 50 ``` | ``` async def instructions(self, manifest: Manifest) -> str | None:     """Return a deterministic instruction fragment appended during run preparation."""     _ = manifest     return None ``` |

#### sampling\_params

```
sampling_params(
    sampling_params: dict[str, Any],
) -> dict[str, Any]
```

Return additional model request parameters needed for this capability.

Source code in `src/agents/sandbox/capabilities/capability.py`

|  |  |
| --- | --- |
| ``` 52 53 54 55 ``` | ``` def sampling_params(self, sampling_params: dict[str, Any]) -> dict[str, Any]:     """Return additional model request parameters needed for this capability."""     _ = sampling_params     return {} ``` |

#### process\_context

```
process_context(
    context: list[TResponseInputItem],
) -> list[TResponseInputItem]
```

Transform the model input context before sampling.

Source code in `src/agents/sandbox/capabilities/capability.py`

|  |  |
| --- | --- |
| ``` 57 58 59 ``` | ``` def process_context(self, context: list[TResponseInputItem]) -> list[TResponseInputItem]:     """Transform the model input context before sampling."""     return context ``` |