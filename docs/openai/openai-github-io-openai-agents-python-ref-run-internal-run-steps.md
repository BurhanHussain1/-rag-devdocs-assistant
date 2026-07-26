---
url: https://openai.github.io/openai-agents-python/ref/run_internal/run_steps/
title: `Run Steps`
framework: openai
---

# `Run Steps`

Internal step/result data structures used by the run loop orchestration.
These types are not part of the public SDK surface.

### QueueCompleteSentinel

Sentinel used to signal completion when streaming run loop results.

Source code in `src/agents/run_internal/run_steps.py`

|  |  |
| --- | --- |
| ``` 53 54 ``` | ``` class QueueCompleteSentinel:     """Sentinel used to signal completion when streaming run loop results.""" ``` |

### ProcessedResponse `dataclass`

Source code in `src/agents/run_internal/run_steps.py`

|  |  |
| --- | --- |
| ``` 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 ``` | ``` @dataclass class ProcessedResponse:     new_items: list[RunItem]     handoffs: list[ToolRunHandoff]     functions: list[ToolRunFunction]     computer_actions: list[ToolRunComputerAction]     local_shell_calls: list[ToolRunLocalShellCall]     shell_calls: list[ToolRunShellCall]     apply_patch_calls: list[ToolRunApplyPatchCall]     tools_used: list[str]  # Names of all tools used, including hosted tools     mcp_approval_requests: list[ToolRunMCPApprovalRequest]  # Only requests with callbacks     interruptions: list[ToolApprovalItem]  # Tool approval items awaiting user decision     function_tools_not_found: list[ToolRunFunctionNotFound] = dataclasses.field(         default_factory=list     )     custom_tool_calls: list[ToolRunCustom] = dataclasses.field(default_factory=list)      def has_tools_or_approvals_to_run(self) -> bool:         # Handoffs, functions and computer actions need local processing         # Hosted tools have already run, so there's nothing to do.         return any(             [                 self.handoffs,                 self.functions,                 self.computer_actions,                 self.custom_tool_calls,                 self.local_shell_calls,                 self.shell_calls,                 self.apply_patch_calls,                 self.mcp_approval_requests,                 self.function_tools_not_found,             ]         )      def has_interruptions(self) -> bool:         """Check if there are tool calls awaiting approval."""         return len(self.interruptions) > 0 ``` |

#### has\_interruptions

```
has_interruptions() -> bool
```

Check if there are tool calls awaiting approval.

Source code in `src/agents/run_internal/run_steps.py`

|  |  |
| --- | --- |
| ``` 150 151 152 ``` | ``` def has_interruptions(self) -> bool:     """Check if there are tool calls awaiting approval."""     return len(self.interruptions) > 0 ``` |

### NextStepInterruption `dataclass`

Represents an interruption in the agent run due to tool approval requests.

Source code in `src/agents/run_internal/run_steps.py`

|  |  |
| --- | --- |
| ``` 170 171 172 173 174 175 ``` | ``` @dataclass class NextStepInterruption:     """Represents an interruption in the agent run due to tool approval requests."""      interruptions: list[ToolApprovalItem]     """The list of tool calls awaiting approval.""" ``` |

#### interruptions `instance-attribute`

```
interruptions: list[ToolApprovalItem]
```

The list of tool calls awaiting approval.

### SingleStepResult `dataclass`

Source code in `src/agents/run_internal/run_steps.py`

|  |  |
| --- | --- |
| ``` 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 ``` | ``` @dataclass class SingleStepResult:     original_input: str | list[TResponseInputItem]     """The input items i.e. the items before run() was called. May be mutated by handoff input     filters."""      model_response: ModelResponse     """The model response for the current step."""      pre_step_items: list[RunItem]     """Items generated before the current step."""      new_step_items: list[RunItem]     """Items generated during this current step."""      next_step: NextStepHandoff | NextStepFinalOutput | NextStepRunAgain | NextStepInterruption     """The next step to take."""      tool_input_guardrail_results: list[ToolInputGuardrailResult]     """Tool input guardrail results from this step."""      tool_output_guardrail_results: list[ToolOutputGuardrailResult]     """Tool output guardrail results from this step."""      session_step_items: list[RunItem] | None = None     """Full unfiltered items for session history. When set, these are used instead of     new_step_items for session saving and generated_items property."""      nested_history_owned_items: list[NestedHistoryOwnedItem] | None = None     """Items moved verbatim into SDK-default nested history for this handoff.      ``None`` means this step did not replace handoff history. A list means the handoff rewrote     history, so prior ownership must be reconciled against the new input before adding these items.     """      output_guardrail_results: list[OutputGuardrailResult] = dataclasses.field(default_factory=list)     """Output guardrail results (populated when a final output is produced)."""      processed_response: ProcessedResponse | None = None     """The processed model response. This is needed for resuming from interruptions."""      @property     def generated_items(self) -> list[RunItem]:         """Items generated during the agent run (i.e. everything generated after         `original_input`). Uses session_step_items when available for full observability."""         items = (             self.session_step_items if self.session_step_items is not None else self.new_step_items         )         return self.pre_step_items + items ``` |

#### original\_input `instance-attribute`

```
original_input: str | list[TResponseInputItem]
```

The input items i.e. the items before run() was called. May be mutated by handoff input
filters.

#### model\_response `instance-attribute`

```
model_response: ModelResponse
```

The model response for the current step.

#### pre\_step\_items `instance-attribute`

```
pre_step_items: list[RunItem]
```

Items generated before the current step.

#### new\_step\_items `instance-attribute`

```
new_step_items: list[RunItem]
```

Items generated during this current step.

#### next\_step `instance-attribute`

```
next_step: (
    NextStepHandoff
    | NextStepFinalOutput
    | NextStepRunAgain
    | NextStepInterruption
)
```

The next step to take.

#### tool\_input\_guardrail\_results `instance-attribute`

```
tool_input_guardrail_results: list[ToolInputGuardrailResult]
```

Tool input guardrail results from this step.

#### tool\_output\_guardrail\_results `instance-attribute`

```
tool_output_guardrail_results: list[
    ToolOutputGuardrailResult
]
```

Tool output guardrail results from this step.

#### session\_step\_items `class-attribute` `instance-attribute`

```
session_step_items: list[RunItem] | None = None
```

Full unfiltered items for session history. When set, these are used instead of
new\_step\_items for session saving and generated\_items property.

#### nested\_history\_owned\_items `class-attribute` `instance-attribute`

```
nested_history_owned_items: (
    list[NestedHistoryOwnedItem] | None
) = None
```

Items moved verbatim into SDK-default nested history for this handoff.

`None` means this step did not replace handoff history. A list means the handoff rewrote
history, so prior ownership must be reconciled against the new input before adding these items.

#### output\_guardrail\_results `class-attribute` `instance-attribute`

```
output_guardrail_results: list[OutputGuardrailResult] = (
    field(default_factory=list)
)
```

Output guardrail results (populated when a final output is produced).

#### processed\_response `class-attribute` `instance-attribute`

```
processed_response: ProcessedResponse | None = None
```

The processed model response. This is needed for resuming from interruptions.

#### generated\_items `property`

```
generated_items: list[RunItem]
```

Items generated during the agent run (i.e. everything generated after
`original_input`). Uses session\_step\_items when available for full observability.