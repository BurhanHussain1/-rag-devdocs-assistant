---
url: https://openai.github.io/openai-agents-python/ref/apply_diff/
title: `Apply Diff`
framework: openai
---

# `Apply Diff`

Utility for applying V4A diffs against text inputs.

### apply\_diff

```
apply_diff(
    input: str, diff: str, mode: ApplyDiffMode = "default"
) -> str
```

Apply a V4A diff to the provided text.

This parser understands both the create-file syntax (only "+" prefixed
lines) and the default update syntax that includes context hunks.

Source code in `src/agents/apply_diff.py`

|  |  |
| --- | --- |
| ``` 52 53 54 55 56 57 58 59 60 61 62 63 64 65 ``` | ``` def apply_diff(input: str, diff: str, mode: ApplyDiffMode = "default") -> str:     """Apply a V4A diff to the provided text.      This parser understands both the create-file syntax (only "+" prefixed     lines) and the default update syntax that includes context hunks.     """     newline = _detect_newline(input, diff, mode)     diff_lines = _normalize_diff_lines(diff)     if mode == "create":         return _parse_create_diff(diff_lines, newline=newline)      normalized_input = _normalize_text_newlines(input)     parsed = _parse_update_diff(diff_lines, normalized_input)     return _apply_chunks(normalized_input, parsed.chunks, newline=newline) ``` |