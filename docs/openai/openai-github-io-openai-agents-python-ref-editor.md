---
url: https://openai.github.io/openai-agents-python/ref/editor/
title: `Editor`
framework: openai
---

# `Editor`

### ApplyPatchOperation `dataclass`

Represents a single apply\_patch editor operation requested by the model.

Source code in `src/agents/editor.py`

|  |  |
| --- | --- |
| ``` 15 16 17 18 19 20 21 22 23 ``` | ``` @dataclass(**_DATACLASS_KWARGS) class ApplyPatchOperation:     """Represents a single apply_patch editor operation requested by the model."""      type: ApplyPatchOperationType     path: str     diff: str | None = None     ctx_wrapper: RunContextWrapper | None = None     move_to: str | None = None ``` |

### ApplyPatchResult `dataclass`

Optional metadata returned by editor operations.

Source code in `src/agents/editor.py`

|  |  |
| --- | --- |
| ``` 26 27 28 29 30 31 ``` | ``` @dataclass(**_DATACLASS_KWARGS) class ApplyPatchResult:     """Optional metadata returned by editor operations."""      status: Literal["completed", "failed"] | None = None     output: str | None = None ``` |

### ApplyPatchEditor

Bases: `Protocol`

Host-defined editor that applies diffs on disk.

Source code in `src/agents/editor.py`

|  |  |
| --- | --- |
| ``` 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 ``` | ``` @runtime_checkable class ApplyPatchEditor(Protocol):     """Host-defined editor that applies diffs on disk."""      def create_file(         self, operation: ApplyPatchOperation     ) -> MaybeAwaitable[ApplyPatchResult | str | None]: ...      def update_file(         self, operation: ApplyPatchOperation     ) -> MaybeAwaitable[ApplyPatchResult | str | None]: ...      def delete_file(         self, operation: ApplyPatchOperation     ) -> MaybeAwaitable[ApplyPatchResult | str | None]: ... ``` |