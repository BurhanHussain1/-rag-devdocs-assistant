---
url: https://openai.github.io/openai-agents-python/ref/models/chatcmpl_helpers/
title: `Chatcmpl Helpers`
framework: openai
---

# `Chatcmpl Helpers`

### ChatCmplHelpers

Source code in `src/agents/models/chatcmpl_helpers.py`

|  |  |
| --- | --- |
| ```  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 ``` | ``` class ChatCmplHelpers:     @classmethod     def is_openai(cls, client: AsyncOpenAI) -> bool:         return is_official_openai_client(client)      @classmethod     def get_store_param(cls, client: AsyncOpenAI, model_settings: ModelSettings) -> bool | None:         # Match the behavior of Responses where store is True when not given         default_store = True if cls.is_openai(client) else None         return model_settings.store if model_settings.store is not None else default_store      @classmethod     def get_stream_options_param(         cls, client: AsyncOpenAI, model_settings: ModelSettings, stream: bool     ) -> dict[str, bool] | None:         if not stream:             return None          default_include_usage = True if cls.is_openai(client) else None         include_usage = (             model_settings.include_usage             if model_settings.include_usage is not None             else default_include_usage         )         stream_options = {"include_usage": include_usage} if include_usage is not None else None         return stream_options      @classmethod     def convert_logprobs_for_output_text(         cls, logprobs: list[ChatCompletionTokenLogprob] | None     ) -> list[Logprob] | None:         if not logprobs:             return None          converted: list[Logprob] = []         for token_logprob in logprobs:             converted.append(                 Logprob(                     token=token_logprob.token,                     logprob=token_logprob.logprob,                     bytes=token_logprob.bytes or [],                     top_logprobs=[                         LogprobTopLogprob(                             token=top_logprob.token,                             logprob=top_logprob.logprob,                             bytes=top_logprob.bytes or [],                         )                         for top_logprob in token_logprob.top_logprobs                     ],                 )             )         return converted      @classmethod     def convert_logprobs_for_text_delta(         cls, logprobs: list[ChatCompletionTokenLogprob] | None     ) -> list[DeltaLogprob] | None:         if not logprobs:             return None          converted: list[DeltaLogprob] = []         for token_logprob in logprobs:             converted.append(                 DeltaLogprob(                     token=token_logprob.token,                     logprob=token_logprob.logprob,                     top_logprobs=[                         DeltaTopLogprob(                             token=top_logprob.token,                             logprob=top_logprob.logprob,                         )                         for top_logprob in token_logprob.top_logprobs                     ]                     or None,                 )             )         return converted      @classmethod     def clean_gemini_tool_call_id(cls, tool_call_id: str, model: str | None = None) -> str:         """Clean up litellm's __thought__ suffix from Gemini tool call IDs.          LiteLLM adds a "__thought__" suffix to Gemini tool call IDs to track thought         signatures. This suffix is redundant since we can get thought_signature from         provider_specific_fields, and this hack causes validation errors when cross-model         passing to other models.          See: https://github.com/BerriAI/litellm/pull/16895          Args:             tool_call_id: The tool call ID to clean.             model: The model name (used to check if it's a Gemini model).          Returns:             The cleaned tool call ID with "__thought__" suffix removed if present.         """         if model and "gemini" in model.lower() and "__thought__" in tool_call_id:             return tool_call_id.split("__thought__")[0]         return tool_call_id ``` |

#### clean\_gemini\_tool\_call\_id `classmethod`

```
clean_gemini_tool_call_id(
    tool_call_id: str, model: str | None = None
) -> str
```

Clean up litellm's **thought** suffix from Gemini tool call IDs.

LiteLLM adds a "**thought**" suffix to Gemini tool call IDs to track thought
signatures. This suffix is redundant since we can get thought\_signature from
provider\_specific\_fields, and this hack causes validation errors when cross-model
passing to other models.

See: https://github.com/BerriAI/litellm/pull/16895

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `tool_call_id` | `str` | The tool call ID to clean. | *required* |
| `model` | `str | None` | The model name (used to check if it's a Gemini model). | `None` |

Returns:

| Type | Description |
| --- | --- |
| `str` | The cleaned tool call ID with "**thought**" suffix removed if present. |

Source code in `src/agents/models/chatcmpl_helpers.py`

|  |  |
| --- | --- |
| ``` 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 ``` | ``` @classmethod def clean_gemini_tool_call_id(cls, tool_call_id: str, model: str | None = None) -> str:     """Clean up litellm's __thought__ suffix from Gemini tool call IDs.      LiteLLM adds a "__thought__" suffix to Gemini tool call IDs to track thought     signatures. This suffix is redundant since we can get thought_signature from     provider_specific_fields, and this hack causes validation errors when cross-model     passing to other models.      See: https://github.com/BerriAI/litellm/pull/16895      Args:         tool_call_id: The tool call ID to clean.         model: The model name (used to check if it's a Gemini model).      Returns:         The cleaned tool call ID with "__thought__" suffix removed if present.     """     if model and "gemini" in model.lower() and "__thought__" in tool_call_id:         return tool_call_id.split("__thought__")[0]     return tool_call_id ``` |