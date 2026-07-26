---
url: https://openai.github.io/openai-agents-python/ref/agent_tool_state/
title: `Agent Tool State`
framework: openai
---

# `Agent Tool State`

### get\_agent\_tool\_state\_scope

```
get_agent_tool_state_scope(context: Any) -> str | None
```

Read the private agent-tool cache scope id from a context wrapper.

Source code in `src/agents/agent_tool_state.py`

|  |  |
| --- | --- |
| ``` 30 31 32 33 ``` | ``` def get_agent_tool_state_scope(context: Any) -> str | None:     """Read the private agent-tool cache scope id from a context wrapper."""     scope_id = getattr(context, _AGENT_TOOL_STATE_SCOPE_ATTR, None)     return scope_id if isinstance(scope_id, str) else None ``` |

### set\_agent\_tool\_state\_scope

```
set_agent_tool_state_scope(
    context: Any, scope_id: str | None
) -> None
```

Attach or clear the private agent-tool cache scope id on a context wrapper.

Source code in `src/agents/agent_tool_state.py`

|  |  |
| --- | --- |
| ``` 36 37 38 39 40 41 42 43 44 45 46 47 48 49 ``` | ``` def set_agent_tool_state_scope(context: Any, scope_id: str | None) -> None:     """Attach or clear the private agent-tool cache scope id on a context wrapper."""     if context is None:         return     if scope_id is None:         try:             delattr(context, _AGENT_TOOL_STATE_SCOPE_ATTR)         except Exception:             return         return     try:         setattr(context, _AGENT_TOOL_STATE_SCOPE_ATTR, scope_id)     except Exception:         return ``` |

### record\_agent\_tool\_run\_result

```
record_agent_tool_run_result(
    tool_call: ResponseFunctionToolCall,
    run_result: RunResult | RunResultStreaming,
    *,
    scope_id: str | None = None,
) -> None
```

Store the nested agent run result by tool call identity.

Source code in `src/agents/agent_tool_state.py`

|  |  |
| --- | --- |
| ``` 119 120 121 122 123 124 125 126 127 128 129 ``` | ``` def record_agent_tool_run_result(     tool_call: ResponseFunctionToolCall,     run_result: RunResult | RunResultStreaming,     *,     scope_id: str | None = None, ) -> None:     """Store the nested agent run result by tool call identity."""     tool_call_obj_id = id(tool_call)     _agent_tool_run_results_by_obj[tool_call_obj_id] = run_result     _index_agent_tool_run_result(tool_call, tool_call_obj_id, scope_id=scope_id)     _register_tool_call_ref(tool_call, tool_call_obj_id) ``` |

### consume\_agent\_tool\_run\_result

```
consume_agent_tool_run_result(
    tool_call: ResponseFunctionToolCall,
    *,
    scope_id: str | None = None,
) -> RunResult | RunResultStreaming | None
```

Return and drop the stored nested agent run result for the given tool call.

Source code in `src/agents/agent_tool_state.py`

|  |  |
| --- | --- |
| ``` 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 ``` | ``` def consume_agent_tool_run_result(     tool_call: ResponseFunctionToolCall,     *,     scope_id: str | None = None, ) -> RunResult | RunResultStreaming | None:     """Return and drop the stored nested agent run result for the given tool call."""     obj_id = id(tool_call)     if _tool_call_obj_matches_scope(obj_id, scope_id=scope_id):         run_result = _agent_tool_run_results_by_obj.pop(obj_id, None)         if run_result is not None:             _drop_agent_tool_run_result(obj_id)             return run_result      signature = _scoped_tool_call_signature(tool_call, scope_id=scope_id)     candidate_ids = _agent_tool_run_results_by_signature.get(signature)     if not candidate_ids:         return None     if len(candidate_ids) != 1:         return None      candidate_id = next(iter(candidate_ids))     _agent_tool_run_results_by_signature.pop(signature, None)     _agent_tool_run_result_signature_by_obj.pop(candidate_id, None)     _agent_tool_call_refs_by_obj.pop(candidate_id, None)     return _agent_tool_run_results_by_obj.pop(candidate_id, None) ``` |

### peek\_agent\_tool\_run\_result

```
peek_agent_tool_run_result(
    tool_call: ResponseFunctionToolCall,
    *,
    scope_id: str | None = None,
) -> RunResult | RunResultStreaming | None
```

Return the stored nested agent run result without removing it.

Source code in `src/agents/agent_tool_state.py`

|  |  |
| --- | --- |
| ``` 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 ``` | ``` def peek_agent_tool_run_result(     tool_call: ResponseFunctionToolCall,     *,     scope_id: str | None = None, ) -> RunResult | RunResultStreaming | None:     """Return the stored nested agent run result without removing it."""     obj_id = id(tool_call)     if _tool_call_obj_matches_scope(obj_id, scope_id=scope_id):         run_result = _agent_tool_run_results_by_obj.get(obj_id)         if run_result is not None:             return run_result      signature = _scoped_tool_call_signature(tool_call, scope_id=scope_id)     candidate_ids = _agent_tool_run_results_by_signature.get(signature)     if not candidate_ids:         return None     if len(candidate_ids) != 1:         return None      candidate_id = next(iter(candidate_ids))     return _agent_tool_run_results_by_obj.get(candidate_id) ``` |

### drop\_agent\_tool\_run\_result

```
drop_agent_tool_run_result(
    tool_call: ResponseFunctionToolCall,
    *,
    scope_id: str | None = None,
) -> None
```

Drop the stored nested agent run result, if present.

Source code in `src/agents/agent_tool_state.py`

|  |  |
| --- | --- |
| ``` 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 ``` | ``` def drop_agent_tool_run_result(     tool_call: ResponseFunctionToolCall,     *,     scope_id: str | None = None, ) -> None:     """Drop the stored nested agent run result, if present."""     obj_id = id(tool_call)     if _tool_call_obj_matches_scope(obj_id, scope_id=scope_id):         run_result = _agent_tool_run_results_by_obj.pop(obj_id, None)         if run_result is not None:             _drop_agent_tool_run_result(obj_id)             return      signature = _scoped_tool_call_signature(tool_call, scope_id=scope_id)     candidate_ids = _agent_tool_run_results_by_signature.get(signature)     if not candidate_ids:         return     if len(candidate_ids) != 1:         return      candidate_id = next(iter(candidate_ids))     _agent_tool_run_results_by_signature.pop(signature, None)     _agent_tool_run_result_signature_by_obj.pop(candidate_id, None)     _agent_tool_call_refs_by_obj.pop(candidate_id, None)     _agent_tool_run_results_by_obj.pop(candidate_id, None) ``` |