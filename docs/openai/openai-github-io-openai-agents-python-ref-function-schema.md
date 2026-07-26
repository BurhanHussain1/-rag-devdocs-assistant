---
url: https://openai.github.io/openai-agents-python/ref/function_schema/
title: `Function schema`
framework: openai
---

# `Function schema`

### FuncSchema `dataclass`

Captures the schema for a python function, in preparation for sending it to an LLM as a tool.

Source code in `src/agents/function_schema.py`

|  |  |
| --- | --- |
| ``` 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 ``` | ``` @dataclass class FuncSchema:     """     Captures the schema for a python function, in preparation for sending it to an LLM as a tool.     """      name: str     """The name of the function."""     description: str | None     """The description of the function."""     params_pydantic_model: type[BaseModel]     """A Pydantic model that represents the function's parameters."""     params_json_schema: dict[str, Any]     """The JSON schema for the function's parameters, derived from the Pydantic model."""     signature: inspect.Signature     """The signature of the function."""     takes_context: bool = False     """Whether the function takes a RunContextWrapper argument (must be the first argument)."""     strict_json_schema: bool = True     """Whether the JSON schema is in strict mode. We **strongly** recommend setting this to True,     as it increases the likelihood of correct JSON input."""     return_annotation: Any = inspect.Signature.empty     """The resolved return annotation, including `Annotated` metadata when present."""      def to_call_args(self, data: BaseModel) -> tuple[list[Any], dict[str, Any]]:         """         Converts validated data from the Pydantic model into (args, kwargs), suitable for calling         the original function.         """         positional_args: list[Any] = []         keyword_args: dict[str, Any] = {}         seen_var_positional = False          # Use enumerate() so we can skip the first parameter if it's context.         for idx, (name, param) in enumerate(self.signature.parameters.items()):             # If the function takes a RunContextWrapper and this is the first parameter, skip it.             if self.takes_context and idx == 0:                 continue              value = getattr(data, name, None)             if param.kind == param.VAR_POSITIONAL:                 # e.g. *args: extend positional args and mark that *args is now seen                 positional_args.extend(value or [])                 seen_var_positional = True             elif param.kind == param.VAR_KEYWORD:                 # e.g. **kwargs handling                 keyword_args.update(value or {})             elif param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):                 # Before *args, add to positional args. After *args, add to keyword args.                 if not seen_var_positional:                     positional_args.append(value)                 else:                     keyword_args[name] = value             else:                 # For KEYWORD_ONLY parameters, always use keyword args.                 keyword_args[name] = value         return positional_args, keyword_args ``` |

#### name `instance-attribute`

```
name: str
```

The name of the function.

#### description `instance-attribute`

```
description: str | None
```

The description of the function.

#### params\_pydantic\_model `instance-attribute`

```
params_pydantic_model: type[BaseModel]
```

A Pydantic model that represents the function's parameters.

#### params\_json\_schema `instance-attribute`

```
params_json_schema: dict[str, Any]
```

The JSON schema for the function's parameters, derived from the Pydantic model.

#### signature `instance-attribute`

```
signature: Signature
```

The signature of the function.

#### takes\_context `class-attribute` `instance-attribute`

```
takes_context: bool = False
```

Whether the function takes a RunContextWrapper argument (must be the first argument).

#### strict\_json\_schema `class-attribute` `instance-attribute`

```
strict_json_schema: bool = True
```

Whether the JSON schema is in strict mode. We **strongly** recommend setting this to True,
as it increases the likelihood of correct JSON input.

#### return\_annotation `class-attribute` `instance-attribute`

```
return_annotation: Any = empty
```

The resolved return annotation, including `Annotated` metadata when present.

#### to\_call\_args

```
to_call_args(
    data: BaseModel,
) -> tuple[list[Any], dict[str, Any]]
```

Converts validated data from the Pydantic model into (args, kwargs), suitable for calling
the original function.

Source code in `src/agents/function_schema.py`

|  |  |
| --- | --- |
| ``` 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 ``` | ``` def to_call_args(self, data: BaseModel) -> tuple[list[Any], dict[str, Any]]:     """     Converts validated data from the Pydantic model into (args, kwargs), suitable for calling     the original function.     """     positional_args: list[Any] = []     keyword_args: dict[str, Any] = {}     seen_var_positional = False      # Use enumerate() so we can skip the first parameter if it's context.     for idx, (name, param) in enumerate(self.signature.parameters.items()):         # If the function takes a RunContextWrapper and this is the first parameter, skip it.         if self.takes_context and idx == 0:             continue          value = getattr(data, name, None)         if param.kind == param.VAR_POSITIONAL:             # e.g. *args: extend positional args and mark that *args is now seen             positional_args.extend(value or [])             seen_var_positional = True         elif param.kind == param.VAR_KEYWORD:             # e.g. **kwargs handling             keyword_args.update(value or {})         elif param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):             # Before *args, add to positional args. After *args, add to keyword args.             if not seen_var_positional:                 positional_args.append(value)             else:                 keyword_args[name] = value         else:             # For KEYWORD_ONLY parameters, always use keyword args.             keyword_args[name] = value     return positional_args, keyword_args ``` |

### FuncDocumentation `dataclass`

Contains metadata about a Python function, extracted from its docstring.

Source code in `src/agents/function_schema.py`

|  |  |
| --- | --- |
| ``` 81 82 83 84 85 86 87 88 89 90 ``` | ``` @dataclass class FuncDocumentation:     """Contains metadata about a Python function, extracted from its docstring."""      name: str     """The name of the function, via `__name__`."""     description: str | None     """The description of the function, derived from the docstring."""     param_descriptions: dict[str, str] | None     """The parameter descriptions of the function, derived from the docstring.""" ``` |

#### name `instance-attribute`

```
name: str
```

The name of the function, via `__name__`.

#### description `instance-attribute`

```
description: str | None
```

The description of the function, derived from the docstring.

#### param\_descriptions `instance-attribute`

```
param_descriptions: dict[str, str] | None
```

The parameter descriptions of the function, derived from the docstring.

### generate\_func\_documentation

```
generate_func_documentation(
    func: Callable[..., Any],
    style: DocstringStyle | None = None,
) -> FuncDocumentation
```

Extracts metadata from a function docstring, in preparation for sending it to an LLM as a tool.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `func` | `Callable[..., Any]` | The function to extract documentation from. | *required* |
| `style` | `DocstringStyle | None` | The style of the docstring to use for parsing. If not provided, we will attempt to auto-detect the style. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `FuncDocumentation` | A FuncDocumentation object containing the function's name, description, and parameter |
| `FuncDocumentation` | descriptions. |

Source code in `src/agents/function_schema.py`

|  |  |
| --- | --- |
| ``` 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 ``` | ``` def generate_func_documentation(     func: Callable[..., Any], style: DocstringStyle | None = None ) -> FuncDocumentation:     """     Extracts metadata from a function docstring, in preparation for sending it to an LLM as a tool.      Args:         func: The function to extract documentation from.         style: The style of the docstring to use for parsing. If not provided, we will attempt to             auto-detect the style.      Returns:         A FuncDocumentation object containing the function's name, description, and parameter         descriptions.     """     name = func.__name__     doc = inspect.getdoc(func)     if not doc:         return FuncDocumentation(name=name, description=None, param_descriptions=None)      # Resolve the style against the original docstring before any normalization.     resolved_style = style or _detect_docstring_style(doc)     if resolved_style == "google":         doc = _ensure_blank_line_before_google_sections(doc)      with _suppress_griffe_logging():         docstring = Docstring(doc, lineno=1, parser=resolved_style)         parsed = docstring.parse()      description: str | None = next(         (section.value for section in parsed if section.kind == DocstringSectionKind.text), None     )      param_descriptions: dict[str, str] = {         param.name: param.description         for section in parsed         if section.kind == DocstringSectionKind.parameters         for param in section.value     }      return FuncDocumentation(         name=func.__name__,         description=description,         param_descriptions=param_descriptions or None,     ) ``` |

### function\_schema

```
function_schema(
    func: Callable[..., Any],
    docstring_style: DocstringStyle | None = None,
    name_override: str | None = None,
    description_override: str | None = None,
    use_docstring_info: bool = True,
    strict_json_schema: bool = True,
) -> FuncSchema
```

Given a Python function, extracts a `FuncSchema` from it, capturing the name, description,
parameter descriptions, and other metadata.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `func` | `Callable[..., Any]` | The function to extract the schema from. | *required* |
| `docstring_style` | `DocstringStyle | None` | The style of the docstring to use for parsing. If not provided, we will attempt to auto-detect the style. | `None` |
| `name_override` | `str | None` | If provided, use this name instead of the function's `__name__`. | `None` |
| `description_override` | `str | None` | If provided, use this description instead of the one derived from the docstring. | `None` |
| `use_docstring_info` | `bool` | If True, uses the docstring to generate the description and parameter descriptions. | `True` |
| `strict_json_schema` | `bool` | Whether the JSON schema is in strict mode. If True, we'll ensure that the schema adheres to the "strict" standard the OpenAI API expects. We **strongly** recommend setting this to True, as it increases the likelihood of the LLM producing correct JSON input. | `True` |

Returns:

| Type | Description |
| --- | --- |
| `FuncSchema` | A `FuncSchema` object containing the function's name, description, parameter descriptions, |
| `FuncSchema` | and other metadata. |

Source code in `src/agents/function_schema.py`

|  |  |
| --- | --- |
| ``` 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 ``` | ``` def function_schema(     func: Callable[..., Any],     docstring_style: DocstringStyle | None = None,     name_override: str | None = None,     description_override: str | None = None,     use_docstring_info: bool = True,     strict_json_schema: bool = True, ) -> FuncSchema:     """     Given a Python function, extracts a `FuncSchema` from it, capturing the name, description,     parameter descriptions, and other metadata.      Args:         func: The function to extract the schema from.         docstring_style: The style of the docstring to use for parsing. If not provided, we will             attempt to auto-detect the style.         name_override: If provided, use this name instead of the function's `__name__`.         description_override: If provided, use this description instead of the one derived from the             docstring.         use_docstring_info: If True, uses the docstring to generate the description and parameter             descriptions.         strict_json_schema: Whether the JSON schema is in strict mode. If True, we'll ensure that             the schema adheres to the "strict" standard the OpenAI API expects. We **strongly**             recommend setting this to True, as it increases the likelihood of the LLM producing             correct JSON input.      Returns:         A `FuncSchema` object containing the function's name, description, parameter descriptions,         and other metadata.     """      # 1. Grab docstring info     if use_docstring_info:         doc_info = generate_func_documentation(func, docstring_style)         param_descs = dict(doc_info.param_descriptions or {})     else:         doc_info = None         param_descs = {}      type_hints_with_extras = get_type_hints(func, include_extras=True)     type_hints: dict[str, Any] = {}     annotated_param_descs: dict[str, str] = {}     param_metadata: dict[str, tuple[Any, ...]] = {}      for name, annotation in type_hints_with_extras.items():         if name == "return":             continue          stripped_ann, metadata = _strip_annotated(annotation)         type_hints[name] = stripped_ann         param_metadata[name] = metadata          description = _extract_description_from_metadata(metadata)         if description is not None:             annotated_param_descs[name] = description      for name, description in annotated_param_descs.items():         param_descs.setdefault(name, description)      # Ensure name_override takes precedence even if docstring info is disabled.     func_name = name_override or (doc_info.name if doc_info else func.__name__)      # 2. Inspect function signature and get type hints     sig = inspect.signature(func)     params = list(sig.parameters.items())     takes_context = False     filtered_params = []      if params:         first_name, first_param = params[0]         # Prefer the evaluated type hint if available         ann = type_hints.get(first_name, first_param.annotation)         if ann != inspect._empty:             origin = get_origin(ann) or ann             if origin is RunContextWrapper or origin is ToolContext:                 takes_context = True  # Mark that the function takes context             else:                 filtered_params.append((first_name, first_param))         else:             filtered_params.append((first_name, first_param))      # For parameters other than the first, raise error if any use RunContextWrapper or ToolContext.     for name, param in params[1:]:         ann = type_hints.get(name, param.annotation)         if ann != inspect._empty:             origin = get_origin(ann) or ann             if origin is RunContextWrapper or origin is ToolContext:                 raise UserError(                     f"RunContextWrapper/ToolContext param found at non-first position in function"                     f" {func.__name__}"                 )         filtered_params.append((name, param))      # We will collect field definitions for create_model as a dict:     #   field_name -> (type_annotation, default_value_or_Field(...))     fields: dict[str, Any] = {}      for name, param in filtered_params:         ann = type_hints.get(name, param.annotation)         default = param.default          # If there's no type hint, assume `Any`         if ann == inspect._empty:             ann = Any          # If a docstring param description exists, use it         field_description = param_descs.get(name, None)          # Handle different parameter kinds         if param.kind == param.VAR_POSITIONAL:             # e.g. *args: extend positional args             if get_origin(ann) is tuple:                 # e.g. def foo(*args: tuple[int, ...]) -> treat as List[int]                 args_of_tuple = get_args(ann)                 if len(args_of_tuple) == 2 and args_of_tuple[1] is Ellipsis:                     ann = list[args_of_tuple[0]]  # type: ignore                 else:                     ann = list[Any]             else:                 # If user wrote *args: int, treat as List[int]                 ann = list[ann]  # type: ignore              # Default factory to empty list             fields[name] = (                 ann,                 Field(default_factory=list, description=field_description),             )          elif param.kind == param.VAR_KEYWORD:             # **kwargs handling             if get_origin(ann) is dict:                 # e.g. def foo(**kwargs: dict[str, int])                 dict_args = get_args(ann)                 if len(dict_args) == 2:                     ann = dict[dict_args[0], dict_args[1]]  # type: ignore                 else:                     ann = dict[str, Any]             else:                 # e.g. def foo(**kwargs: int) -> Dict[str, int]                 ann = dict[str, ann]  # type: ignore              fields[name] = (                 ann,                 Field(default_factory=dict, description=field_description),             )          else:             # Normal parameter             metadata = param_metadata.get(name, ())             field_info_from_annotated = _extract_field_info_from_metadata(metadata)              if field_info_from_annotated is not None:                 merged = FieldInfo.merge_field_infos(                     field_info_from_annotated,                     description=field_description or field_info_from_annotated.description,                 )                 if default != inspect._empty and not isinstance(default, FieldInfo):                     merged = FieldInfo.merge_field_infos(merged, default=default)                 elif isinstance(default, FieldInfo):                     merged = FieldInfo.merge_field_infos(merged, default)                 fields[name] = (ann, merged)             elif default == inspect._empty:                 # Required field                 fields[name] = (                     ann,                     Field(..., description=field_description),                 )             elif isinstance(default, FieldInfo):                 # Parameter with a default value that is a Field(...)                 fields[name] = (                     ann,                     FieldInfo.merge_field_infos(                         default, description=field_description or default.description                     ),                 )             else:                 # Parameter with a default value                 fields[name] = (                     ann,                     Field(default=default, description=field_description),                 )      # 3. Dynamically build a Pydantic model     dynamic_model = create_model(f"{func_name}_args", __base__=BaseModel, **fields)      # 4. Build JSON schema from that model     json_schema = dynamic_model.model_json_schema()     if strict_json_schema:         json_schema = ensure_strict_json_schema(json_schema)      # 5. Return as a FuncSchema dataclass     return FuncSchema(         name=func_name,         # Ensure description_override takes precedence even if docstring info is disabled.         description=description_override or (doc_info.description if doc_info else None),         params_pydantic_model=dynamic_model,         params_json_schema=json_schema,         signature=sig,         takes_context=takes_context,         strict_json_schema=strict_json_schema,         return_annotation=type_hints_with_extras.get("return", sig.return_annotation),     ) ``` |