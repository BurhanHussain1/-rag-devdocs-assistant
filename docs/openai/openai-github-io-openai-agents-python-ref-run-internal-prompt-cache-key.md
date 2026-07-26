---
url: https://openai.github.io/openai-agents-python/ref/run_internal/prompt_cache_key/
title: `Prompt Cache Key`
framework: openai
---

# `Prompt Cache Key`

### PromptCacheKeyResolver `dataclass`

Provides one generated prompt cache key for a runner invocation.

The runner asks for a key on every model turn. This helper returns the same generated key each
time, persists it to RunState for resume flows, and opts out when the request already forwards
a user-supplied key through ModelSettings.

Source code in `src/agents/run_internal/prompt_cache_key.py`

|  |  |
| --- | --- |
| ``` 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 ``` | ``` @dataclass class PromptCacheKeyResolver:     """Provides one generated prompt cache key for a runner invocation.      The runner asks for a key on every model turn. This helper returns the same generated key each     time, persists it to RunState for resume flows, and opts out when the request already forwards     a user-supplied key through ModelSettings.     """      run_state: RunState[Any] | None = None     _generated_key: str | None = None      @classmethod     def from_run_state(         cls,         *,         run_state: RunState[Any] | None,     ) -> PromptCacheKeyResolver:         return cls(             run_state=run_state,             _generated_key=(                 run_state._generated_prompt_cache_key if run_state is not None else None             ),         )      def resolve(         self,         model_settings: ModelSettings,         *,         model: object,         conversation_id: str | None,         session: Session | None,         group_id: str | None,     ) -> str | None:         """Return the generated prompt cache key for this model call.          Returns None when the runner should not add one.         """         # A prompt_cache_key in ModelSettings extras is already forwarded to the model adapter, so         # the runner should not also generate one.         if _model_settings_has_prompt_cache_key(model_settings):             return None          if not _model_supports_default_prompt_cache_key(model):             return None          return self._get_or_create_generated_key(             conversation_id=conversation_id,             session=session,             group_id=group_id,         )      def _get_or_create_generated_key(         self,         *,         conversation_id: str | None,         session: Session | None,         group_id: str | None,     ) -> str:         if self._generated_key is not None:             return self._generated_key          grouping_kind, grouping_value = resolve_run_grouping(             conversation_id=conversation_id,             session=session,             group_id=group_id,         )         key = _prompt_cache_key_for_grouping(grouping_kind, grouping_value)          self._generated_key = key         if self.run_state is not None:             self.run_state._generated_prompt_cache_key = key         return key ``` |

#### resolve

```
resolve(
    model_settings: ModelSettings,
    *,
    model: object,
    conversation_id: str | None,
    session: Session | None,
    group_id: str | None,
) -> str | None
```

Return the generated prompt cache key for this model call.

Returns None when the runner should not add one.

Source code in `src/agents/run_internal/prompt_cache_key.py`

|  |  |
| --- | --- |
| ``` 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 ``` | ``` def resolve(     self,     model_settings: ModelSettings,     *,     model: object,     conversation_id: str | None,     session: Session | None,     group_id: str | None, ) -> str | None:     """Return the generated prompt cache key for this model call.      Returns None when the runner should not add one.     """     # A prompt_cache_key in ModelSettings extras is already forwarded to the model adapter, so     # the runner should not also generate one.     if _model_settings_has_prompt_cache_key(model_settings):         return None      if not _model_supports_default_prompt_cache_key(model):         return None      return self._get_or_create_generated_key(         conversation_id=conversation_id,         session=session,         group_id=group_id,     ) ``` |

### model\_settings\_with\_prompt\_cache\_key

```
model_settings_with_prompt_cache_key(
    model_settings: ModelSettings,
    prompt_cache_key: str | None,
) -> ModelSettings
```

Return model settings with the generated prompt cache key added to extra\_args.

Source code in `src/agents/run_internal/prompt_cache_key.py`

|  |  |
| --- | --- |
| ```  97  98  99 100 101 102 103 104 105 106 107 ``` | ``` def model_settings_with_prompt_cache_key(     model_settings: ModelSettings,     prompt_cache_key: str | None, ) -> ModelSettings:     """Return model settings with the generated prompt cache key added to extra_args."""     if prompt_cache_key is None or _model_settings_has_prompt_cache_key(model_settings):         return model_settings      extra_args = dict(model_settings.extra_args or {})     extra_args[PROMPT_CACHE_KEY_FIELD] = prompt_cache_key     return dataclass_replace(model_settings, extra_args=extra_args) ``` |