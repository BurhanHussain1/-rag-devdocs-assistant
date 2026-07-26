---
url: https://openai.github.io/openai-agents-python/ref/agent/
title: `Agents`
framework: openai
---

# `Agents`

### ToolsToFinalOutputFunction `module-attribute`

```
ToolsToFinalOutputFunction: TypeAlias = Callable[
    [RunContextWrapper[TContext], list[FunctionToolResult]],
    MaybeAwaitable[ToolsToFinalOutputResult],
]
```

A function that takes a run context and a list of tool results, and returns a
`ToolsToFinalOutputResult`.

### ToolsToFinalOutputResult `dataclass`

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 73 74 75 76 77 78 79 80 81 82 83 ``` | ``` @dataclass class ToolsToFinalOutputResult:     is_final_output: bool     """Whether this is the final output. If False, the LLM will run again and receive the tool call     output.     """      final_output: Any | None = None     """The final output. Can be None if `is_final_output` is False, otherwise must match the     `output_type` of the agent.     """ ``` |

#### is\_final\_output `instance-attribute`

```
is_final_output: bool
```

Whether this is the final output. If False, the LLM will run again and receive the tool call
output.

#### final\_output `class-attribute` `instance-attribute`

```
final_output: Any | None = None
```

The final output. Can be None if `is_final_output` is False, otherwise must match the
`output_type` of the agent.

### AgentToolStreamEvent

Bases: `TypedDict`

Streaming event emitted when an agent is invoked as a tool.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 121 122 123 124 125 126 127 128 129 130 131 ``` | ``` class AgentToolStreamEvent(TypedDict):     """Streaming event emitted when an agent is invoked as a tool."""      event: StreamEvent     """The streaming event from the nested agent run."""      agent: Agent[Any]     """The nested agent emitting the event."""      tool_call: ResponseFunctionToolCall | None     """The originating tool call, if available.""" ``` |

#### event `instance-attribute`

```
event: StreamEvent
```

The streaming event from the nested agent run.

#### agent `instance-attribute`

```
agent: Agent[Any]
```

The nested agent emitting the event.

#### tool\_call `instance-attribute`

```
tool_call: ResponseFunctionToolCall | None
```

The originating tool call, if available.

### StopAtTools

Bases: `TypedDict`

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 134 135 136 ``` | ``` class StopAtTools(TypedDict):     stop_at_tool_names: list[str]     """A list of tool names, any of which will stop the agent from running further.""" ``` |

#### stop\_at\_tool\_names `instance-attribute`

```
stop_at_tool_names: list[str]
```

A list of tool names, any of which will stop the agent from running further.

### MCPConfig

Bases: `TypedDict`

Configuration for MCP servers.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 ``` | ``` class MCPConfig(TypedDict):     """Configuration for MCP servers."""      convert_schemas_to_strict: NotRequired[bool]     """If True, we will attempt to convert the MCP schemas to strict-mode schemas. This is a     best-effort conversion, so some schemas may not be convertible. Defaults to False.     """      failure_error_function: NotRequired[ToolErrorFunction | None]     """Optional function to convert MCP tool failures into model-visible messages. If explicitly     set to None, tool errors will be raised instead. If unset, defaults to     default_tool_error_function.     """      include_server_in_tool_names: NotRequired[bool]     """If True, local MCP tools are exposed with server-prefixed public names to avoid name     collisions across multiple MCP servers. Defaults to False.     """ ``` |

#### convert\_schemas\_to\_strict `instance-attribute`

```
convert_schemas_to_strict: NotRequired[bool]
```

If True, we will attempt to convert the MCP schemas to strict-mode schemas. This is a
best-effort conversion, so some schemas may not be convertible. Defaults to False.

#### failure\_error\_function `instance-attribute`

```
failure_error_function: NotRequired[
    ToolErrorFunction | None
]
```

Optional function to convert MCP tool failures into model-visible messages. If explicitly
set to None, tool errors will be raised instead. If unset, defaults to
default\_tool\_error\_function.

#### include\_server\_in\_tool\_names `instance-attribute`

```
include_server_in_tool_names: NotRequired[bool]
```

If True, local MCP tools are exposed with server-prefixed public names to avoid name
collisions across multiple MCP servers. Defaults to False.

### AgentBase `dataclass`

Bases: `Generic[TContext]`

Base class for `Agent` and `RealtimeAgent`.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 ``` | ``` @dataclass class AgentBase(Generic[TContext]):     """Base class for `Agent` and `RealtimeAgent`."""      name: str     """The name of the agent."""      handoff_description: str | None = None     """A description of the agent. This is used when the agent is used as a handoff, so that an     LLM knows what it does and when to invoke it.     """      tools: list[Tool] = field(default_factory=list)     """A list of tools that the agent can use."""      mcp_servers: list[MCPServer] = field(default_factory=list)     """A list of [Model Context Protocol](https://modelcontextprotocol.io/) servers that     the agent can use. Every time the agent runs, it will include tools from these servers in the     list of available tools.      NOTE: You are expected to manage the lifecycle of these servers. Specifically, you must call     `server.connect()` before passing it to the agent, and `server.cleanup()` when the server is no     longer needed. Consider using `MCPServerManager` from `agents.mcp` to keep connect/cleanup     in the same task.     """      mcp_config: MCPConfig = field(default_factory=lambda: MCPConfig())     """Configuration for MCP servers."""      async def _get_mcp_tool_reserved_names(         self, run_context: RunContextWrapper[TContext]     ) -> set[str]:         reserved_tool_names = {tool.name for tool in self.tools if isinstance(tool, FunctionTool)}          async def _check_handoff_enabled(handoff_obj: Handoff[Any, Any]) -> bool:             attr = handoff_obj.is_enabled             if isinstance(attr, bool):                 return attr             res = attr(run_context, self)             if inspect.isawaitable(res):                 return bool(await res)             return bool(res)          for handoff_item in getattr(self, "handoffs", ()):             if isinstance(handoff_item, Handoff):                 if await _check_handoff_enabled(handoff_item):                     reserved_tool_names.add(handoff_item.tool_name)             elif isinstance(handoff_item, AgentBase):                 reserved_tool_names.add(Handoff.default_tool_name(handoff_item))         return reserved_tool_names      async def get_mcp_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:         """Fetches the available tools from the MCP servers."""         convert_schemas_to_strict = self.mcp_config.get("convert_schemas_to_strict", False)         failure_error_function = self.mcp_config.get(             "failure_error_function", default_tool_error_function         )         include_server_in_tool_names = self.mcp_config.get("include_server_in_tool_names", False)         reserved_tool_names = (             await self._get_mcp_tool_reserved_names(run_context)             if include_server_in_tool_names             else None         )         return await MCPUtil.get_all_function_tools(             self.mcp_servers,             convert_schemas_to_strict,             run_context,             self,             failure_error_function=failure_error_function,             include_server_in_tool_names=include_server_in_tool_names,             reserved_tool_names=reserved_tool_names,         )      async def get_all_tools(self, run_context: RunContextWrapper[TContext]) -> list[Tool]:         """All agent tools, including MCP tools and function tools."""         mcp_tools = await self.get_mcp_tools(run_context)          async def _check_tool_enabled(tool: Tool) -> bool:             if not isinstance(tool, FunctionTool):                 return True              attr = tool.is_enabled             if isinstance(attr, bool):                 return attr             res = attr(run_context, self)             if inspect.isawaitable(res):                 return bool(await res)             return bool(res)          results = await asyncio.gather(*(_check_tool_enabled(t) for t in self.tools))         enabled: list[Tool] = [t for t, ok in zip(self.tools, results, strict=False) if ok]         all_tools: list[Tool] = prune_orphaned_tool_search_tools([*mcp_tools, *enabled])         _validate_codex_tool_name_collisions(all_tools)         return all_tools ``` |

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

### Agent `dataclass`

Bases: `AgentBase`, `Generic[TContext]`

An agent is an AI model configured with instructions, tools, guardrails, handoffs and more.

We strongly recommend passing `instructions`, which is the "system prompt" for the agent. In
addition, you can pass `handoff_description`, which is a human-readable description of the
agent, used when the agent is used inside tools/handoffs.

Agents are generic on the context type. The context is a (mutable) object you create. It is
passed to tool functions, handoffs, guardrails, etc.

See `AgentBase` for base parameters that are shared with `RealtimeAgent`s.

Source code in `src/agents/agent.py`

|  |  |
| --- | --- |
| ``` 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 832 833 834 835 836 837 838 839 840 841 842 843 844 845 846 847 848 849 850 851 852 853 854 855 856 857 858 859 860 861 862 863 864 865 866 867 868 869 870 871 872 873 874 875 876 877 878 879 880 881 882 883 884 885 886 887 888 889 890 891 892 893 894 895 896 897 898 899 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 915 916 917 918 919 920 921 922 923 924 925 926 927 928 929 930 931 932 933 934 935 936 937 938 939 940 941 942 943 944 945 946 947 948 949 950 951 952 953 954 955 956 957 958 959 960 961 962 963 964 965 966 967 968 969 970 971 972 973 974 975 976 977 ``` | ``` @dataclass class Agent(AgentBase, Generic[TContext]):     """An agent is an AI model configured with instructions, tools, guardrails, handoffs and more.      We strongly recommend passing `instructions`, which is the "system prompt" for the agent. In     addition, you can pass `handoff_description`, which is a human-readable description of the     agent, used when the agent is used inside tools/handoffs.      Agents are generic on the context type. The context is a (mutable) object you create. It is     passed to tool functions, handoffs, guardrails, etc.      See `AgentBase` for base parameters that are shared with `RealtimeAgent`s.     """      instructions: (         str         | Callable[             [RunContextWrapper[TContext], Agent[TContext]],             MaybeAwaitable[str],         ]         | None     ) = None     """The instructions for the agent. Will be used as the "system prompt" when this agent is     invoked. Describes what the agent should do, and how it responds.      Can either be a string, or a function that dynamically generates instructions for the agent. If     you provide a function, it will be called with the context and the agent instance. It must     return a string.     """      prompt: Prompt | DynamicPromptFunction | None = None     """A prompt object (or a function that returns a Prompt). Prompts allow you to dynamically     configure the instructions, tools and other config for an agent outside of your code. Only     usable with OpenAI models, using the Responses API.     """      handoffs: list[Agent[Any] | Handoff[TContext, Any]] = field(default_factory=list)     """Handoffs are sub-agents that the agent can delegate to. You can provide a list of handoffs,     and the agent can choose to delegate to them if relevant. Allows for separation of concerns and     modularity.     """      model: str | Model | None = None     """The model implementation to use when invoking the LLM.      By default, if not set, the agent will use the default model configured in     `agents.models.get_default_model()` (currently "gpt-5.4-mini").     """      model_settings: ModelSettings = field(default_factory=get_default_model_settings)     """Configures model-specific tuning parameters (e.g. temperature, top_p).     """      input_guardrails: list[InputGuardrail[TContext]] = field(default_factory=list)     """A list of checks that run in parallel to the agent's execution, before generating a     response. Runs only if the agent is the first agent in the chain.     """      output_guardrails: list[OutputGuardrail[TContext]] = field(default_factory=list)     """A list of checks that run on the final output of the agent, after generating a response.     Runs only if the agent produces a final output.     """      output_type: type[Any] | AgentOutputSchemaBase | None = None     """The type of the output object. If not provided, the output will be `str`. In most cases,     you should pass a regular Python type (e.g. a dataclass, Pydantic model, TypedDict, etc).     You can customize this in two ways:     1. If you want non-strict schemas, pass `AgentOutputSchema(MyClass, strict_json_schema=False)`.     2. If you want to use a custom JSON schema (i.e. without using the SDK's automatic schema)        creation, subclass and pass an `AgentOutputSchemaBase` subclass.     """      hooks: AgentHooks[TContext] | None = None     """A class that receives callbacks on various lifecycle events for this agent.     """      tool_use_behavior: (         Literal["run_llm_again", "stop_on_first_tool"] | StopAtTools | ToolsToFinalOutputFunction     ) = "run_llm_again"     """     This lets you configure how tool use is handled.     - "run_llm_again": The default behavior. Tools are run, and then the LLM receives the results         and gets to respond.     - "stop_on_first_tool": The output from the first tool call is treated as the final result.         In other words, it isn’t sent back to the LLM for further processing but is used directly         as the final output.     - A StopAtTools object: The agent will stop running if any of the tools listed in         `stop_at_tool_names` is called.         The final output will be the output of the first matching tool call.         The LLM does not process the result of the tool call.     - A function: If you pass a function, it will be called with the run context and the list of       tool results. It must return a `ToolsToFinalOutputResult`, which determines whether the tool       calls result in a final output.        NOTE: This configuration is specific to FunctionTools. Hosted tools, such as file search,       web search, etc. are always processed by the LLM.     """      reset_tool_choice: bool = True     """Whether to reset the tool choice to the default value after a tool has been called. Defaults     to True. This ensures that the agent doesn't enter an infinite loop of tool usage."""      def __post_init__(self):         from typing import get_origin          if not isinstance(self.name, str):             raise TypeError(f"Agent name must be a string, got {type(self.name).__name__}")          if self.handoff_description is not None and not isinstance(self.handoff_description, str):             raise TypeError(                 f"Agent handoff_description must be a string or None, "                 f"got {type(self.handoff_description).__name__}"             )          if not isinstance(self.tools, list):             raise TypeError(f"Agent tools must be a list, got {type(self.tools).__name__}")          if not isinstance(self.mcp_servers, list):             raise TypeError(                 f"Agent mcp_servers must be a list, got {type(self.mcp_servers).__name__}"             )          if not isinstance(self.mcp_config, dict):             raise TypeError(                 f"Agent mcp_config must be a dict, got {type(self.mcp_config).__name__}"             )          if (             self.instructions is not None             and not isinstance(self.instructions, str)             and not callable(self.instructions)         ):             raise TypeError(                 f"Agent instructions must be a string, callable, or None, "                 f"got {type(self.instructions).__name__}"             )          if (             self.prompt is not None             and not callable(self.prompt)             and not hasattr(self.prompt, "get")         ):             raise TypeError(                 f"Agent prompt must be a Prompt, DynamicPromptFunction, or None, "                 f"got {type(self.prompt).__name__}"             )          if not isinstance(self.handoffs, list):             raise TypeError(f"Agent handoffs must be a list, got {type(self.handoffs).__name__}")          if self.model is not None and not isinstance(self.model, str):             from .models.interface import Model              if not isinstance(self.model, Model):                 raise TypeError(                     f"Agent model must be a string, Model, or None, got {type(self.model).__name__}"                 )          if not isinstance(self.model_settings, ModelSettings):             raise TypeError(                 f"Agent model_settings must be a ModelSettings instance, "                 f"got {type(self.model_settings).__name__}"             )          if self.model is not None and self.model_settings == get_default_model_settings():             self.model_settings = _initial_model_settings_for_model(self.model)          if not isinstance(self.input_guardrails, list):             raise TypeError(                 f"Agent input_guardrails must be a list, got {type(self.input_guardrails).__name__}"             )          if not isinstance(self.output_guardrails, list):             raise TypeError(                 f"Agent output_guardrails must be a list, "                 f"got {type(self.output_guardrails).__name__}"             )          if self.output_type is not None:             from .agent_output import AgentOutputSchemaBase              if not (                 isinstance(self.output_type, type | AgentOutputSchemaBase)                 or get_origin(self.output_type) is not None             ):                 raise TypeError(                     f"Agent output_type must be a type, AgentOutputSchemaBase, or None, "                     f"got {type(self.output_type).__name__}"                 )          if self.hooks is not None:             from .lifecycle import AgentHooksBase              if not isinstance(self.hooks, AgentHooksBase):                 raise TypeError(                     f"Agent hooks must be an AgentHooks instance or None, "                     f"got {type(self.hooks).__name__}"                 )          if (             not (                 isinstance(self.tool_use_behavior, str)                 and self.tool_use_behavior in ["run_llm_again", "stop_on_first_tool"]             )             and not isinstance(self.tool_use_behavior, dict)             and not callable(self.tool_use_behavior)         ):             raise TypeError(                 f"Agent tool_use_behavior must be 'run_llm_again', 'stop_on_first_tool', "                 f"StopAtTools dict, or callable, got {type(self.tool_use_behavior).__name__}"             )          if not isinstance(self.reset_tool_choice, bool):             raise TypeError(                 f"Agent reset_tool_choice must be a boolean, "                 f"got {type(self.reset_tool_choice).__name__}"             )      def clone(self, **kwargs: Any) -> Agent[TContext]:         """Make a copy of the agent, with the given arguments changed.         Notes:             - Uses `dataclasses.replace`, which performs a **shallow copy**.             - Mutable attributes like `tools` and `handoffs` are shallow-copied:               new list objects are created only if overridden, but their contents               (tool functions and handoff objects) are shared with the original.             - To modify these independently, pass new lists when calling `clone()`.         Example:             ```python             new_agent = agent.clone(instructions="New instructions")             ```         """         if (             "model" in kwargs             and "model_settings" not in kwargs             and _model_settings_match_implicit_model_defaults(self.model, self.model_settings)         ):             kwargs["model_settings"] = _initial_model_settings_for_model(kwargs["model"])         return dataclasses.replace(self, **kwargs)      def as_tool(         self,         tool_name: str | None,         tool_description: str | None,         custom_output_extractor: (             Callable[[RunResult | RunResultStreaming], Awaitable[str]] | None         ) = None,         is_enabled: bool         | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]] = True,         on_stream: Callable[[AgentToolStreamEvent], MaybeAwaitable[None]] | None = None,         run_config: RunConfig | None = None,         max_turns: int | None = None,         hooks: RunHooks[TContext] | None = None,         previous_response_id: str | None = None,         conversation_id: str | None = None,         session: Session | None = None,         failure_error_function: ToolErrorFunction | None = default_tool_error_function,         needs_approval: bool         | Callable[[RunContextWrapper[Any], dict[str, Any], str], Awaitable[bool]] = False,         parameters: type[Any] | None = None,         input_builder: StructuredToolInputBuilder | None = None,         include_input_schema: bool = False,     ) -> FunctionTool:         """Transform this agent into a tool, callable by other agents.          This is different from handoffs in two ways:         1. In handoffs, the new agent receives the conversation history. In this tool, the new agent            receives generated input.         2. In handoffs, the new agent takes over the conversation. In this tool, the new agent is            called as a tool, and the conversation is continued by the original agent.          Args:             tool_name: The name of the tool. If not provided, the agent's name will be used.             tool_description: The description of the tool, which should indicate what it does and                 when to use it.             custom_output_extractor: A function that extracts the output from the agent. If not                 provided, the last message from the agent will be used. Nested run results expose                 `agent_tool_invocation` metadata when this agent is invoked via `as_tool()`.             is_enabled: Whether the tool is enabled. Can be a bool or a callable that takes the run                 context and agent and returns whether the tool is enabled. Disabled tools are hidden                 from the LLM at runtime.             on_stream: Optional callback (sync or async) to receive streaming events from the nested                 agent run. The callback receives an `AgentToolStreamEvent` containing the nested                 agent, the originating tool call (when available), and each stream event. When                 provided, the nested agent is executed in streaming mode.             failure_error_function: If provided, generate an error message when the tool (agent) run                 fails. The message is sent to the LLM. If None, the exception is raised instead.             needs_approval: Bool or callable to decide if this agent tool should pause for approval.             parameters: Structured input type for the tool arguments (dataclass or Pydantic model).             input_builder: Optional function to build the nested agent input from structured data.             include_input_schema: Whether to include the full JSON schema in structured input.         """          def _is_supported_parameters(value: Any) -> bool:             if not isinstance(value, type):                 return False             if dataclasses.is_dataclass(value):                 return True             return issubclass(value, BaseModel)          tool_name_resolved = tool_name or _transforms.transform_string_function_style(self.name)         tool_description_resolved = tool_description or ""         has_custom_parameters = parameters is not None         include_schema = bool(include_input_schema and has_custom_parameters)         should_capture_tool_input = bool(             has_custom_parameters or include_schema or input_builder is not None         )          if parameters is None:             params_adapter = TypeAdapter(AgentAsToolInput)             params_schema = ensure_strict_json_schema(params_adapter.json_schema())         else:             if not _is_supported_parameters(parameters):                 raise TypeError("Agent tool parameters must be a dataclass or Pydantic model type.")             params_adapter = TypeAdapter(parameters)             params_schema = ensure_strict_json_schema(params_adapter.json_schema())          schema_info = build_structured_input_schema_info(             params_schema,             include_json_schema=include_schema,         )          def _normalize_tool_input(parsed: Any, tool_name: str) -> Any:             # Prefer JSON mode so structured params (datetime/UUID/Decimal, etc.) serialize cleanly.             try:                 return params_adapter.dump_python(parsed, mode="json")             except Exception as exc:                 raise ModelBehaviorError(                     f"Failed to serialize structured tool input for {tool_name}: {exc}"                 ) from exc          async def _run_agent_impl(context: ToolContext, input_json: str) -> Any:             from .run import DEFAULT_MAX_TURNS, Runner             from .tool_context import ToolContext              tool_name = (                 context.tool_name if isinstance(context, ToolContext) else tool_name_resolved             )             json_data = _parse_function_tool_json_input(                 tool_name=tool_name,                 input_json=input_json,             )             _log_function_tool_invocation(tool_name=tool_name, input_json=input_json)              try:                 parsed_params = params_adapter.validate_python(json_data)             except ValidationError as exc:                 raise ModelBehaviorError(f"Invalid JSON input for tool {tool_name}: {exc}") from exc              params_data = _normalize_tool_input(parsed_params, tool_name)             resolved_input = await resolve_agent_tool_input(                 params=params_data,                 schema_info=schema_info if should_capture_tool_input else None,                 input_builder=input_builder,             )             if not isinstance(resolved_input, str) and not isinstance(resolved_input, list):                 raise ModelBehaviorError("Agent tool called with invalid input")              resolved_max_turns = max_turns if max_turns is not None else DEFAULT_MAX_TURNS             resolved_run_config = run_config             if resolved_run_config is None and isinstance(context, ToolContext):                 resolved_run_config = context.run_config             tool_state_scope_id = get_agent_tool_state_scope(context)             if isinstance(context, ToolContext):                 # Use a fresh ToolContext to avoid sharing approval state with parent runs.                 nested_context = ToolContext(                     context=context.context,                     usage=context.usage,                     tool_name=context.tool_name,                     tool_call_id=context.tool_call_id,                     tool_arguments=context.tool_arguments,                     tool_call=context.tool_call,                     tool_namespace=context.tool_namespace,                     agent=context.agent,                     run_config=resolved_run_config,                 )                 set_agent_tool_state_scope(nested_context, tool_state_scope_id)                 if should_capture_tool_input:                     nested_context.tool_input = params_data             elif isinstance(context, RunContextWrapper):                 if should_capture_tool_input:                     nested_context = RunContextWrapper(context=context.context)                     set_agent_tool_state_scope(nested_context, tool_state_scope_id)                     nested_context.tool_input = params_data                 else:                     nested_context = context.context             else:                 if should_capture_tool_input:                     nested_context = RunContextWrapper(context=context)                     set_agent_tool_state_scope(nested_context, tool_state_scope_id)                     nested_context.tool_input = params_data                 else:                     nested_context = context             run_result: RunResult | RunResultStreaming | None = None             resume_state: RunState | None = None             should_record_run_result = True              def _nested_approvals_status(                 interruptions: list[ToolApprovalItem],             ) -> Literal["approved", "pending", "rejected"]:                 has_pending = False                 has_decision = False                 for interruption in interruptions:                     call_id = interruption.call_id                     if not call_id:                         has_pending = True                         continue                     tool_namespace = RunContextWrapper._resolve_tool_namespace(interruption)                     status = context.get_approval_status(                         interruption.tool_name or "",                         call_id,                         tool_namespace=tool_namespace,                         existing_pending=interruption,                     )                     if status is False:                         return "rejected"                     if status is True:                         has_decision = True                     if status is None:                         has_pending = True                 if has_decision:                     return "approved"                 if has_pending:                     return "pending"                 return "approved"              def _apply_nested_approvals(                 nested_context: RunContextWrapper[Any],                 parent_context: RunContextWrapper[Any],                 interruptions: list[ToolApprovalItem],             ) -> None:                 def _find_mirrored_approval_record(                     interruption: ToolApprovalItem,                     *,                     approved: bool,                 ) -> Any | None:                     candidate_keys = list(RunContextWrapper._resolve_approval_keys(interruption))                     for candidate_key in get_function_tool_approval_keys(                         tool_name=RunContextWrapper._resolve_tool_name(interruption),                         tool_namespace=RunContextWrapper._resolve_tool_namespace(interruption),                         tool_lookup_key=RunContextWrapper._resolve_tool_lookup_key(interruption),                         include_legacy_deferred_key=True,                     ):                         if candidate_key not in candidate_keys:                             candidate_keys.append(candidate_key)                     fallback: Any | None = None                     for candidate_key in candidate_keys:                         candidate = parent_context._approvals.get(candidate_key)                         if candidate is None:                             continue                         if approved and candidate.approved is True:                             return candidate                         if not approved and candidate.rejected is True:                             return candidate                         if fallback is None:                             fallback = candidate                     return fallback                  for interruption in interruptions:                     call_id = interruption.call_id                     if not call_id:                         continue                     tool_name = RunContextWrapper._resolve_tool_name(interruption)                     tool_namespace = RunContextWrapper._resolve_tool_namespace(interruption)                     approval_key = RunContextWrapper._resolve_approval_key(interruption)                     status = parent_context.get_approval_status(                         tool_name,                         call_id,                         tool_namespace=tool_namespace,                         existing_pending=interruption,                     )                     if status is None:                         continue                     approval_record = parent_context._approvals.get(approval_key)                     if approval_record is None:                         approval_record = _find_mirrored_approval_record(                             interruption,                             approved=status,                         )                     if status is True:                         always_approve = bool(approval_record and approval_record.approved is True)                         nested_context.approve_tool(                             interruption,                             always_approve=always_approve,                         )                     else:                         always_reject = bool(approval_record and approval_record.rejected is True)                         nested_context.reject_tool(                             interruption,                             always_reject=always_reject,                         )              if isinstance(context, ToolContext) and context.tool_call is not None:                 pending_run_result = peek_agent_tool_run_result(                     context.tool_call,                     scope_id=tool_state_scope_id,                 )                 if pending_run_result and getattr(pending_run_result, "interruptions", None):                     status = _nested_approvals_status(pending_run_result.interruptions)                     if status == "pending":                         run_result = pending_run_result                         should_record_run_result = False                     elif status in ("approved", "rejected"):                         resume_state = pending_run_result.to_state()                         if resume_state._context is not None:                             # Apply only explicit parent approvals to the nested resumed run.                             _apply_nested_approvals(                                 resume_state._context,                                 context,                                 pending_run_result.interruptions,                             )                         consume_agent_tool_run_result(                             context.tool_call,                             scope_id=tool_state_scope_id,                         )              if run_result is None:                 if on_stream is not None:                     stream_handler = on_stream                     run_result_streaming = Runner.run_streamed(                         starting_agent=cast(Agent[Any], self),                         input=resume_state or resolved_input,                         context=None if resume_state is not None else cast(Any, nested_context),                         run_config=resolved_run_config,                         max_turns=resolved_max_turns,                         hooks=hooks,                         previous_response_id=None                         if resume_state is not None                         else previous_response_id,                         conversation_id=None if resume_state is not None else conversation_id,                         session=session,                     )                     # Dispatch callbacks in the background so slow handlers do not block                     # event consumption.                     event_queue: asyncio.Queue[AgentToolStreamEvent | None] = asyncio.Queue()                      async def _run_handler(payload: AgentToolStreamEvent) -> None:                         """Execute the user callback while capturing exceptions."""                         try:                             maybe_result = stream_handler(payload)                             if inspect.isawaitable(maybe_result):                                 await maybe_result                         except Exception:                             logger.exception(                                 "Error while handling on_stream event for agent tool %s.",                                 self.name,                             )                      async def dispatch_stream_events() -> None:                         while True:                             payload = await event_queue.get()                             is_sentinel = payload is None  # None marks the end of the stream.                             try:                                 if payload is not None:                                     await _run_handler(payload)                             finally:                                 event_queue.task_done()                              if is_sentinel:                                 break                      dispatch_task = asyncio.create_task(dispatch_stream_events())                     stream_iteration_cancelled = False                      try:                         from .stream_events import AgentUpdatedStreamEvent                          current_agent = run_result_streaming.current_agent                         try:                             async for event in run_result_streaming.stream_events():                                 if isinstance(event, AgentUpdatedStreamEvent):                                     current_agent = event.new_agent                                  payload: AgentToolStreamEvent = {                                     "event": event,                                     "agent": current_agent,                                     "tool_call": context.tool_call,                                 }                                 await event_queue.put(payload)                         except asyncio.CancelledError:                             stream_iteration_cancelled = True                             raise                     finally:                         if stream_iteration_cancelled:                             dispatch_task.cancel()                             try:                                 await dispatch_task                             except asyncio.CancelledError:                                 pass                         else:                             await event_queue.put(None)                             await event_queue.join()                             await dispatch_task                     run_result = run_result_streaming                 else:                     run_result = await Runner.run(                         starting_agent=cast(Agent[Any], self),                         input=resume_state or resolved_input,                         context=None if resume_state is not None else cast(Any, nested_context),                         run_config=resolved_run_config,                         max_turns=resolved_max_turns,                         hooks=hooks,                         previous_response_id=None                         if resume_state is not None                         else previous_response_id,                         conversation_id=None if resume_state is not None else conversation_id,                         session=session,                     )             assert run_result is not None              # Store the run result by tool call identity so nested interruptions can be read later.             interruptions = getattr(run_result, "interruptions", None)             if isinstance(context, ToolContext) and context.tool_call is not None and interruptions:                 if should_record_run_result:                     record_agent_tool_run_result(                         context.tool_call,                         run_result,                         scope_id=tool_state_scope_id,                     )              if custom_output_extractor:                 return await custom_output_extractor(run_result)              if run_result.final_output is not None and (                 not isinstance(run_result.final_output, str) or run_result.final_output != ""             ):                 return run_result.final_output              from .items import ItemHelpers, MessageOutputItem, ToolCallOutputItem              for item in reversed(run_result.new_items):                 if isinstance(item, MessageOutputItem):                     text_output = ItemHelpers.text_message_output(item)                     if text_output:                         return text_output                  if (                     isinstance(item, ToolCallOutputItem)                     and isinstance(item.output, str)                     and item.output                 ):                     return item.output              return run_result.final_output          run_agent_tool = _build_wrapped_function_tool(             name=tool_name_resolved,             description=tool_description_resolved,             params_json_schema=params_schema,             invoke_tool_impl=_run_agent_impl,             on_handled_error=_build_handled_function_tool_error_handler(                 span_message="Error running tool (non-fatal)",                 span_message_for_json_decode_error="Error running tool",                 log_label="Tool",             ),             failure_error_function=failure_error_function,             strict_json_schema=True,             is_enabled=is_enabled,             needs_approval=needs_approval,             tool_origin=ToolOrigin(                 type=ToolOriginType.AGENT_AS_TOOL,                 agent_name=self.name,                 agent_tool_name=tool_name_resolved,             ),         )         run_agent_tool._is_agent_tool = True         run_agent_tool._agent_instance = self          return run_agent_tool      async def get_system_prompt(self, run_context: RunContextWrapper[TContext]) -> str | None:         if isinstance(self.instructions, str):             return self.instructions         elif callable(self.instructions):             # Inspect the signature of the instructions function             sig = inspect.signature(self.instructions)             params = list(sig.parameters.values())              # Enforce exactly 2 parameters             if len(params) != 2:                 raise TypeError(                     f"'instructions' callable must accept exactly 2 arguments (context, agent), "                     f"but got {len(params)}: {[p.name for p in params]}"                 )              # Call the instructions function properly             if inspect.iscoroutinefunction(self.instructions):                 return await cast(Awaitable[str], self.instructions(run_context, self))             else:                 return cast(str, self.instructions(run_context, self))          elif self.instructions is not None:             logger.error(                 "Instructions must be a string or a callable function, got %s",                 type(self.instructions).__name__,             )          return None      async def get_prompt(         self, run_context: RunContextWrapper[TContext]     ) -> ResponsePromptParam | None:         """Get the prompt for the agent."""         from ._public_agent import get_public_agent          return await PromptUtil.to_model_input(             self.prompt,             run_context,             cast(Agent[TContext], get_public_agent(self)),         ) ``` |

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