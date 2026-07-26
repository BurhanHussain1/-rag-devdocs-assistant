---
url: https://openai.github.io/openai-agents-python/ref/extensions/experimental/codex/output_schema_file/
title: `Output Schema File`
framework: openai
---

# `Output Schema File`

### create\_output\_schema\_file

```
create_output_schema_file(
    schema: dict[str, Any] | None,
) -> OutputSchemaFile
```

Materialize a JSON schema into a temp file for the Codex CLI.

Source code in `src/agents/extensions/experimental/codex/output_schema_file.py`

|  |  |
| --- | --- |
| ``` 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 ``` | ``` def create_output_schema_file(schema: dict[str, Any] | None) -> OutputSchemaFile:     """Materialize a JSON schema into a temp file for the Codex CLI."""     if schema is None:         # No schema means there is no temp file to manage.         return OutputSchemaFile(schema_path=None, cleanup=lambda: None)      if not _is_plain_json_object(schema):         raise UserError("output_schema must be a plain JSON object")      # The Codex CLI expects a schema file path, so write to a temp directory.     schema_dir = tempfile.mkdtemp(prefix="codex-output-schema-")     schema_path = os.path.join(schema_dir, "schema.json")      def cleanup() -> None:         # Best-effort cleanup since this runs in finally blocks.         try:             shutil.rmtree(schema_dir, ignore_errors=True)         except Exception:             pass      try:         with open(schema_path, "w", encoding="utf-8") as handle:             json.dump(schema, handle)         return OutputSchemaFile(schema_path=schema_path, cleanup=cleanup)     except Exception:         cleanup()         raise ``` |