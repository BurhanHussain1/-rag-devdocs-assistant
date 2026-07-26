---
url: https://openai.github.io/openai-agents-python/ref/run_internal/items/
title: `Items`
framework: openai
---

# `Items`

Item utilities for the run pipeline. Hosts input normalization helpers and lightweight builders
for synthetic run items or IDs used during tool execution. Internal use only.

### NestedHistoryOwnedItem `dataclass`

A run item and the exact nested-input occurrence that represents it.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 86 87 88 89 90 91 92 93 ``` | ``` @dataclass(frozen=True) class NestedHistoryOwnedItem:     """A run item and the exact nested-input occurrence that represents it."""      run_item: RunItem | None     input_index: int     digest: str     input_item: TResponseInputItem | None = field(default=None, compare=False, repr=False) ``` |

### NestedHistoryOwnedItemRef `dataclass`

Durable coordinates plus the live object for one owned session occurrence.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ```  96  97  98  99 100 101 102 103 104 ``` | ``` @dataclass(frozen=True) class NestedHistoryOwnedItemRef:     """Durable coordinates plus the live object for one owned session occurrence."""      session_index: int     digest: str     input_index: int     run_item: RunItem | None = field(default=None, compare=False, repr=False)     input_item: TResponseInputItem | None = field(default=None, compare=False, repr=False) ``` |

### nested\_history\_run\_item\_occurrence\_key

```
nested_history_run_item_occurrence_key(
    run_item: RunItem | None,
) -> str | None
```

Return the private copy-lineage key for a run item, when one exists.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 107 108 109 110 111 112 ``` | ``` def nested_history_run_item_occurrence_key(run_item: RunItem | None) -> str | None:     """Return the private copy-lineage key for a run item, when one exists."""     if run_item is None:         return None     key = getattr(run_item, _NESTED_HISTORY_RUN_ITEM_OCCURRENCE_KEY, None)     return key if isinstance(key, str) and key else None ``` |

### ensure\_nested\_history\_run\_item\_occurrence\_key

```
ensure_nested_history_run_item_occurrence_key(
    run_item: RunItem,
) -> str
```

Bind an ephemeral key that survives object copies but never enters model payloads.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 115 116 117 118 119 120 121 ``` | ``` def ensure_nested_history_run_item_occurrence_key(run_item: RunItem) -> str:     """Bind an ephemeral key that survives object copies but never enters model payloads."""     key = nested_history_run_item_occurrence_key(run_item)     if key is None:         key = uuid4().hex         setattr(run_item, _NESTED_HISTORY_RUN_ITEM_OCCURRENCE_KEY, key)     return key ``` |

### copy\_input\_items

```
copy_input_items(
    value: str | list[TResponseInputItem],
) -> str | list[TResponseInputItem]
```

Return a shallow copy of input items so mutations do not leak between turns.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 127 128 129 ``` | ``` def copy_input_items(value: str | list[TResponseInputItem]) -> str | list[TResponseInputItem]:     """Return a shallow copy of input items so mutations do not leak between turns."""     return value if isinstance(value, str) else value.copy() ``` |

### run\_item\_to\_input\_item

```
run_item_to_input_item(
    run_item: RunItem,
    reasoning_item_id_policy: ReasoningItemIdPolicy
    | None = None,
) -> TResponseInputItem | None
```

Convert a run item to model input, optionally stripping reasoning IDs.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 ``` | ``` def run_item_to_input_item(     run_item: RunItem,     reasoning_item_id_policy: ReasoningItemIdPolicy | None = None, ) -> TResponseInputItem | None:     """Convert a run item to model input, optionally stripping reasoning IDs."""     if run_item.type == "tool_approval_item":         return None     to_input = getattr(run_item, "to_input_item", None)     input_item = to_input() if callable(to_input) else cast(TResponseInputItem, run_item.raw_item)     if isinstance(input_item, dict) and input_item.get("status") is None:         input_item = {k: v for k, v in input_item.items() if k != "status"}     if (         _should_omit_reasoning_item_ids(reasoning_item_id_policy)         and run_item.type == "reasoning_item"     ):         return _without_reasoning_item_id(input_item)     return cast(TResponseInputItem, input_item) ``` |

### run\_items\_to\_input\_items

```
run_items_to_input_items(
    run_items: Sequence[RunItem],
    reasoning_item_id_policy: ReasoningItemIdPolicy
    | None = None,
) -> list[TResponseInputItem]
```

Convert run items to model input items while skipping approvals.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 151 152 153 154 155 156 157 158 159 160 161 ``` | ``` def run_items_to_input_items(     run_items: Sequence[RunItem],     reasoning_item_id_policy: ReasoningItemIdPolicy | None = None, ) -> list[TResponseInputItem]:     """Convert run items to model input items while skipping approvals."""     converted: list[TResponseInputItem] = []     for run_item in run_items:         item = run_item_to_input_item(run_item, reasoning_item_id_policy)         if item is not None:             converted.append(item)     return converted ``` |

### drop\_orphan\_function\_calls

```
drop_orphan_function_calls(
    items: list[TResponseInputItem],
    *,
    pruning_indexes: set[int] | None = None,
) -> list[TResponseInputItem]
```

Remove tool and program call items that do not have corresponding outputs so resumptions or
retries do not replay stale calls. Program-owned items are removed with an orphan program,
while programs with retained hosted calls or tool outputs remain available for continuation.
Reasoning items that immediately precede a call dropped by this pass are also removed, since
the Responses API rejects reasoning items that are not followed by their associated
model-emitted item (`Item 'rs_...' of type 'reasoning' was provided without its required
following item`).

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 ``` | ``` def drop_orphan_function_calls(     items: list[TResponseInputItem],     *,     pruning_indexes: set[int] | None = None, ) -> list[TResponseInputItem]:     """     Remove tool and program call items that do not have corresponding outputs so resumptions or     retries do not replay stale calls. Program-owned items are removed with an orphan program,     while programs with retained hosted calls or tool outputs remain available for continuation.     Reasoning items that immediately precede a call dropped by this pass are also removed, since     the Responses API rejects reasoning items that are not followed by their associated     model-emitted item (``Item 'rs_...' of type 'reasoning' was provided without its required     following item``).     """      completed_call_ids = _completed_call_ids_by_type(items)     matched_anonymous_tool_search_calls = _matched_anonymous_tool_search_call_indexes(items)     active_program_call_ids: set[str] = set()     orphan_program_call_ids: set[str] = set()      for index, entry in enumerate(items):         if pruning_indexes is not None and index not in pruning_indexes:             continue         if not isinstance(entry, dict) or entry.get("type") != "program":             continue         call_id = entry.get("call_id")         if not isinstance(call_id, str):             continue         if call_id in completed_call_ids["program_output"]:             continue         if any(             _get_program_caller_id(candidate) == call_id             and _is_retained_program_owned_item(candidate, candidate_index, pruning_indexes)             for candidate_index, candidate in enumerate(items)         ):             active_program_call_ids.add(call_id)         else:             orphan_program_call_ids.add(call_id)      dropped_indexes: set[int] = set()     filtered: list[TResponseInputItem] = []     for index, entry in enumerate(items):         if not isinstance(entry, dict):             filtered.append(entry)             continue         entry_type = entry.get("type")         if not isinstance(entry_type, str):             filtered.append(entry)             continue         if pruning_indexes is not None and index not in pruning_indexes:             filtered.append(entry)             continue         program_caller_id = _get_program_caller_id(entry)         if program_caller_id is not None and program_caller_id in orphan_program_call_ids:             dropped_indexes.add(index)             continue         output_type = _TOOL_CALL_TO_OUTPUT_TYPE.get(entry_type)         if output_type is None:             filtered.append(entry)             continue         call_id = entry.get("call_id")         if program_caller_id is not None and _is_pending_hosted_shell_call(entry):             filtered.append(entry)             continue         if entry_type == "program" and call_id in active_program_call_ids:             filtered.append(entry)             continue         if isinstance(call_id, str) and call_id in completed_call_ids.get(output_type, set()):             filtered.append(entry)             continue         if (             entry_type == "tool_search_call"             and not isinstance(call_id, str)             and index in matched_anonymous_tool_search_calls         ):             filtered.append(entry)             continue         # Tool call entry will be dropped; record so we can also drop preceding reasoning items.         dropped_indexes.add(index)      if not dropped_indexes:         return filtered     return _drop_reasoning_items_preceding_dropped_calls(items, dropped_indexes) ``` |

### ensure\_input\_item\_format

```
ensure_input_item_format(
    item: TResponseInputItem,
) -> TResponseInputItem
```

Ensure a single item is normalized for model input.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 281 282 283 284 285 286 287 ``` | ``` def ensure_input_item_format(item: TResponseInputItem) -> TResponseInputItem:     """Ensure a single item is normalized for model input."""     coerced = _coerce_to_dict(item)     if coerced is None:         return item      return cast(TResponseInputItem, coerced) ``` |

### normalize\_input\_items\_for\_api

```
normalize_input_items_for_api(
    items: list[TResponseInputItem],
) -> list[TResponseInputItem]
```

Normalize input items for API submission.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 290 291 292 293 294 295 296 297 298 299 300 301 302 ``` | ``` def normalize_input_items_for_api(items: list[TResponseInputItem]) -> list[TResponseInputItem]:     """Normalize input items for API submission."""      normalized: list[TResponseInputItem] = []     for item in items:         coerced = _coerce_to_dict(item)         if coerced is None:             normalized.append(item)             continue          normalized_item = strip_internal_input_item_metadata(cast(TResponseInputItem, coerced))         normalized.append(normalized_item)     return normalized ``` |

### prepare\_model\_input\_items

```
prepare_model_input_items(
    caller_items: Sequence[TResponseInputItem],
    generated_items: Sequence[TResponseInputItem] = (),
) -> list[TResponseInputItem]
```

Normalize model input while pruning orphans only from runner-generated history.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 305 306 307 308 309 310 311 312 313 314 315 316 ``` | ``` def prepare_model_input_items(     caller_items: Sequence[TResponseInputItem],     generated_items: Sequence[TResponseInputItem] = (), ) -> list[TResponseInputItem]:     """Normalize model input while pruning orphans only from runner-generated history."""     normalized_caller_items = normalize_input_items_for_api(list(caller_items))     if not generated_items:         return normalized_caller_items      normalized_generated_items = normalize_input_items_for_api(list(generated_items))     filtered_generated_items = drop_orphan_function_calls(normalized_generated_items)     return normalized_caller_items + filtered_generated_items ``` |

### normalize\_resumed\_input

```
normalize_resumed_input(
    raw_input: str | list[TResponseInputItem],
) -> str | list[TResponseInputItem]
```

Normalize resumed list inputs and drop orphan tool calls.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 319 320 321 322 323 324 325 326 ``` | ``` def normalize_resumed_input(     raw_input: str | list[TResponseInputItem], ) -> str | list[TResponseInputItem]:     """Normalize resumed list inputs and drop orphan tool calls."""     if isinstance(raw_input, list):         normalized = normalize_input_items_for_api(raw_input)         return drop_orphan_function_calls(normalized)     return raw_input ``` |

### fingerprint\_input\_item

```
fingerprint_input_item(
    item: Any, *, ignore_ids_for_matching: bool = False
) -> str | None
```

Hashable fingerprint used to dedupe or rewind input items across resumes.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 ``` | ``` def fingerprint_input_item(item: Any, *, ignore_ids_for_matching: bool = False) -> str | None:     """Hashable fingerprint used to dedupe or rewind input items across resumes."""     if item is None:         return None      try:         payload: Any         if hasattr(item, "model_dump"):             payload = _model_dump_without_warnings(item)             if payload is None:                 return None             if isinstance(payload, dict):                 payload = cast(                     dict[str, Any],                     strip_internal_input_item_metadata(cast(TResponseInputItem, payload)),                 )         elif isinstance(item, dict):             payload = cast(                 dict[str, Any],                 strip_internal_input_item_metadata(cast(TResponseInputItem, item)),             )             if ignore_ids_for_matching:                 payload.pop("id", None)         else:             payload = ensure_input_item_format(item)             if isinstance(payload, dict):                 payload = cast(                     dict[str, Any],                     strip_internal_input_item_metadata(cast(TResponseInputItem, payload)),                 )             if ignore_ids_for_matching and isinstance(payload, dict):                 payload.pop("id", None)          return json.dumps(payload, sort_keys=True, default=str)     except Exception:         return None ``` |

### digest\_input\_item

```
digest_input_item(item: Any) -> str | None
```

Return a fixed-size digest of an input item for durable occurrence tracking.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 ``` | ``` def digest_input_item(item: Any) -> str | None:     """Return a fixed-size digest of an input item for durable occurrence tracking."""     coerced = _coerce_to_dict(item)     if coerced is not None:         coerced = cast(             dict[str, Any],             strip_internal_input_item_metadata(cast(TResponseInputItem, coerced)),         )         if coerced.get("role") == "assistant":             content = coerced.get("content")             if isinstance(content, str):                 coerced["content"] = [{"type": "output_text", "text": content}]             if coerced.get("status") in {None, "completed"}:                 coerced.pop("status", None)         item = coerced      fingerprint = fingerprint_input_item(item)     if fingerprint is None:         return None     return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest() ``` |

### filter\_nested\_history\_owned\_item\_refs\_for\_input

```
filter_nested_history_owned_item_refs_for_input(
    input: str | Sequence[TResponseInputItem],
    owned_item_refs: Sequence[NestedHistoryOwnedItemRef],
) -> list[NestedHistoryOwnedItemRef]
```

Keep ownership whose exact clean input occurrence is still present.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 ``` | ``` def filter_nested_history_owned_item_refs_for_input(     input: str | Sequence[TResponseInputItem],     owned_item_refs: Sequence[NestedHistoryOwnedItemRef], ) -> list[NestedHistoryOwnedItemRef]:     """Keep ownership whose exact clean input occurrence is still present."""     if isinstance(input, str) or not owned_item_refs:         return []      input_digests = [digest_input_item(item) for item in input]     input_indexes_by_identity: dict[tuple[int, str], deque[int]] = {}     for index, (item, digest) in enumerate(zip(input, input_digests, strict=True)):         if digest is not None:             input_indexes_by_identity.setdefault((id(item), digest), deque()).append(index)      retained: list[NestedHistoryOwnedItemRef] = []     used_input_indexes: set[int] = set()      def _take_unused(candidates: deque[int] | None) -> int | None:         while candidates:             candidate = candidates.popleft()             if candidate not in used_input_indexes:                 return candidate         return None      for item_ref in owned_item_refs:         input_index = (             _take_unused(input_indexes_by_identity.get((id(item_ref.input_item), item_ref.digest)))             if item_ref.input_item is not None             else None         )         if input_index is None and item_ref.input_item is None:             candidate_index = item_ref.input_index             if (                 0 <= candidate_index < len(input)                 and candidate_index not in used_input_indexes                 and input_digests[candidate_index] == item_ref.digest             ):                 input_index = candidate_index         if input_index is None:             continue         used_input_indexes.add(input_index)         retained.append(replace(item_ref, input_index=input_index, input_item=input[input_index]))     return retained ``` |

### reconcile\_nested\_history\_owned\_input\_after\_rewrite

```
reconcile_nested_history_owned_input_after_rewrite(
    previous_input: str | Sequence[TResponseInputItem],
    rewritten_input: str | Sequence[TResponseInputItem],
    owned_item_refs: Sequence[NestedHistoryOwnedItemRef],
) -> tuple[
    str | list[TResponseInputItem],
    list[NestedHistoryOwnedItemRef],
]
```

Rebind ownership after an unambiguous input rewrite.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 ``` | ``` def reconcile_nested_history_owned_input_after_rewrite(     previous_input: str | Sequence[TResponseInputItem],     rewritten_input: str | Sequence[TResponseInputItem],     owned_item_refs: Sequence[NestedHistoryOwnedItemRef], ) -> tuple[str | list[TResponseInputItem], list[NestedHistoryOwnedItemRef]]:     """Rebind ownership after an unambiguous input rewrite."""     if isinstance(rewritten_input, str) or not owned_item_refs:         return (             rewritten_input if isinstance(rewritten_input, str) else list(rewritten_input),             [],         )     if isinstance(previous_input, str):         return list(rewritten_input), []      rewritten = list(rewritten_input)     previous = list(previous_input)     previous_digests = [digest_input_item(item) for item in previous]     rewritten_digests = [digest_input_item(item) for item in rewritten]     previous_digest_counts: dict[str, int] = {}     rewritten_digest_counts: dict[str, int] = {}     previous_identity_digests: set[tuple[int, str]] = set()     rewritten_indexes_by_identity: dict[tuple[int, str], deque[int]] = {}     rewritten_indexes_by_digest: dict[str, deque[int]] = {}     for item, digest in zip(previous, previous_digests, strict=True):         if digest is None:             continue         previous_digest_counts[digest] = previous_digest_counts.get(digest, 0) + 1         previous_identity_digests.add((id(item), digest))     for index, (item, digest) in enumerate(zip(rewritten, rewritten_digests, strict=True)):         if digest is None:             continue         rewritten_digest_counts[digest] = rewritten_digest_counts.get(digest, 0) + 1         rewritten_indexes_by_identity.setdefault((id(item), digest), deque()).append(index)         rewritten_indexes_by_digest.setdefault(digest, deque()).append(index)      recoverable_ref_counts: dict[str, int] = {}     for item_ref in owned_item_refs:         if (             item_ref.input_item is not None             and (id(item_ref.input_item), item_ref.digest) in previous_identity_digests         ):             recoverable_ref_counts[item_ref.digest] = (                 recoverable_ref_counts.get(item_ref.digest, 0) + 1             )     used_indexes: set[int] = set()     used_digest_counts: dict[str, int] = {}     retained: list[NestedHistoryOwnedItemRef] = []      def _take_unused(candidates: deque[int] | None) -> int | None:         while candidates:             candidate = candidates.popleft()             if candidate not in used_indexes:                 return candidate         return None      for item_ref in owned_item_refs:         identity_match = (             _take_unused(                 rewritten_indexes_by_identity.get((id(item_ref.input_item), item_ref.digest))             )             if item_ref.input_item is not None             else None         )         if identity_match is not None:             used_indexes.add(identity_match)             used_digest_counts[item_ref.digest] = used_digest_counts.get(item_ref.digest, 0) + 1             retained.append(                 replace(                     item_ref,                     input_index=identity_match,                     input_item=rewritten[identity_match],                 )             )             continue          previous_match = (             item_ref.input_item is not None             and (id(item_ref.input_item), item_ref.digest) in previous_identity_digests         )         previous_count = previous_digest_counts.get(item_ref.digest, 0)         rewritten_count = rewritten_digest_counts.get(item_ref.digest, 0)         all_equal_occurrences_owned = (             previous_count == rewritten_count == recoverable_ref_counts.get(item_ref.digest, 0)         )         if (             not previous_match             or rewritten_count <= used_digest_counts.get(item_ref.digest, 0)             or not ((previous_count == 1 and rewritten_count == 1) or all_equal_occurrences_owned)         ):             continue          candidate_index = _take_unused(rewritten_indexes_by_digest.get(item_ref.digest))         if candidate_index is None:             continue         used_indexes.add(candidate_index)         used_digest_counts[item_ref.digest] = used_digest_counts.get(item_ref.digest, 0) + 1         retained.append(             replace(                 item_ref,                 input_index=candidate_index,                 input_item=rewritten[candidate_index],             )         )      return rewritten, retained ``` |

### resolve\_nested\_history\_owned\_item\_indexes

```
resolve_nested_history_owned_item_indexes(
    run_items: Sequence[RunItem],
    owned_item_refs: Sequence[NestedHistoryOwnedItemRef],
) -> set[int]
```

Resolve ownership references without dropping a different item after list mutation.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 ``` | ``` def resolve_nested_history_owned_item_indexes(     run_items: Sequence[RunItem],     owned_item_refs: Sequence[NestedHistoryOwnedItemRef], ) -> set[int]:     """Resolve ownership references without dropping a different item after list mutation."""     if not owned_item_refs:         return set()      indexes_by_identity_digest: dict[tuple[int, str], deque[int]] = {}     indexes_by_occurrence_digest: dict[tuple[str, str], deque[int]] = {}     run_item_digests: list[str | None] = []     for index, run_item in enumerate(run_items):         input_item = run_item_to_input_item(run_item)         digest = digest_input_item(input_item) if input_item is not None else None         run_item_digests.append(digest)         if digest is None:             continue         indexes_by_identity_digest.setdefault((id(run_item), digest), deque()).append(index)         occurrence_key = nested_history_run_item_occurrence_key(run_item)         if occurrence_key is not None:             indexes_by_occurrence_digest.setdefault((occurrence_key, digest), deque()).append(index)      resolved: set[int] = set()      def _peek_unused(candidates: deque[int] | None) -> int | None:         while candidates and candidates[0] in resolved:             candidates.popleft()         return candidates[0] if candidates else None      for item_ref in owned_item_refs:         occurrence_key = nested_history_run_item_occurrence_key(item_ref.run_item)         stored_index = item_ref.session_index         if (             0 <= stored_index < len(run_items)             and stored_index not in resolved             and run_item_digests[stored_index] == item_ref.digest             and item_ref.run_item is not None             and (                 run_items[stored_index] is item_ref.run_item                 or (                     occurrence_key is not None                     and nested_history_run_item_occurrence_key(run_items[stored_index])                     == occurrence_key                 )             )         ):             resolved.add(stored_index)             continue          identity_index = (             _peek_unused(indexes_by_identity_digest.get((id(item_ref.run_item), item_ref.digest)))             if item_ref.run_item is not None             else None         )         occurrence_index = (             _peek_unused(indexes_by_occurrence_digest.get((occurrence_key, item_ref.digest)))             if occurrence_key is not None             else None         )         candidates = [index for index in (identity_index, occurrence_index) if index is not None]         if candidates:             resolved.add(min(candidates))      return resolved ``` |

### rebase\_nested\_history\_owned\_item\_refs

```
rebase_nested_history_owned_item_refs(
    input: str | Sequence[TResponseInputItem],
    run_items: Sequence[RunItem],
    owned_item_refs: Sequence[NestedHistoryOwnedItemRef],
) -> list[NestedHistoryOwnedItemRef]
```

Rebase surviving ownership onto exact live input and session occurrences.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 ``` | ``` def rebase_nested_history_owned_item_refs(     input: str | Sequence[TResponseInputItem],     run_items: Sequence[RunItem],     owned_item_refs: Sequence[NestedHistoryOwnedItemRef], ) -> list[NestedHistoryOwnedItemRef]:     """Rebase surviving ownership onto exact live input and session occurrences."""     retained_refs = filter_nested_history_owned_item_refs_for_input(input, owned_item_refs)     indexes_by_identity_digest: dict[tuple[int, str], deque[int]] = {}     indexes_by_occurrence_digest: dict[tuple[str, str], deque[int]] = {}     for index, run_item in enumerate(run_items):         input_item = run_item_to_input_item(run_item)         digest = digest_input_item(input_item) if input_item is not None else None         if digest is None:             continue         indexes_by_identity_digest.setdefault((id(run_item), digest), deque()).append(index)         occurrence_key = nested_history_run_item_occurrence_key(run_item)         if occurrence_key is not None:             indexes_by_occurrence_digest.setdefault((occurrence_key, digest), deque()).append(index)      rebased: list[NestedHistoryOwnedItemRef] = []     used_indexes: set[int] = set()      def _peek_unused(candidates: deque[int] | None) -> int | None:         while candidates and candidates[0] in used_indexes:             candidates.popleft()         return candidates[0] if candidates else None      for item_ref in retained_refs:         occurrence_key = nested_history_run_item_occurrence_key(item_ref.run_item)         identity_index = (             _peek_unused(indexes_by_identity_digest.get((id(item_ref.run_item), item_ref.digest)))             if item_ref.run_item is not None             else None         )         occurrence_index = (             _peek_unused(indexes_by_occurrence_digest.get((occurrence_key, item_ref.digest)))             if occurrence_key is not None             else None         )         candidates = [index for index in (identity_index, occurrence_index) if index is not None]         if not candidates:             continue         index = min(candidates)         used_indexes.add(index)         rebased.append(replace(item_ref, session_index=index, run_item=run_items[index]))     return rebased ``` |

### strip\_internal\_input\_item\_metadata

```
strip_internal_input_item_metadata(
    item: TResponseInputItem,
) -> TResponseInputItem
```

Remove SDK-only session metadata before sending items back to the model.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 684 685 686 687 688 689 690 691 692 ``` | ``` def strip_internal_input_item_metadata(item: TResponseInputItem) -> TResponseInputItem:     """Remove SDK-only session metadata before sending items back to the model."""     if not isinstance(item, dict):         return item      cleaned = dict(item)     cleaned.pop(TOOL_CALL_SESSION_DESCRIPTION_KEY, None)     cleaned.pop(TOOL_CALL_SESSION_TITLE_KEY, None)     return cast(TResponseInputItem, cleaned) ``` |

### deduplicate\_input\_items

```
deduplicate_input_items(
    items: Sequence[TResponseInputItem],
) -> list[TResponseInputItem]
```

Remove duplicate items that share stable identifiers to avoid re-sending tool outputs.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 711 712 713 714 715 716 717 718 719 720 721 722 723 724 ``` | ``` def deduplicate_input_items(items: Sequence[TResponseInputItem]) -> list[TResponseInputItem]:     """Remove duplicate items that share stable identifiers to avoid re-sending tool outputs."""     seen_keys: set[str] = set()     deduplicated: list[TResponseInputItem] = []     for item in items:         dedupe_key = _dedupe_key(item)         if dedupe_key is None:             deduplicated.append(item)             continue         if dedupe_key in seen_keys:             continue         seen_keys.add(dedupe_key)         deduplicated.append(item)     return deduplicated ``` |

### deduplicate\_input\_items\_preferring\_latest

```
deduplicate_input_items_preferring_latest(
    items: Sequence[TResponseInputItem],
) -> list[TResponseInputItem]
```

Deduplicate by stable identifiers while keeping the latest occurrence.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 727 728 729 730 731 732 733 ``` | ``` def deduplicate_input_items_preferring_latest(     items: Sequence[TResponseInputItem], ) -> list[TResponseInputItem]:     """Deduplicate by stable identifiers while keeping the latest occurrence."""     # deduplicate_input_items keeps the first item per dedupe key. Reverse twice so that     # the latest item in the original order wins for duplicate IDs/call_ids.     return list(reversed(deduplicate_input_items(list(reversed(items))))) ``` |

### function\_rejection\_item

```
function_rejection_item(
    agent: Any,
    tool_call: Any,
    *,
    rejection_message: str = REJECTION_MESSAGE,
    scope_id: str | None = None,
    tool_origin: Any = None,
) -> ToolCallOutputItem
```

Build a ToolCallOutputItem representing a rejected function tool call.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 ``` | ``` def function_rejection_item(     agent: Any,     tool_call: Any,     *,     rejection_message: str = REJECTION_MESSAGE,     scope_id: str | None = None,     tool_origin: Any = None, ) -> ToolCallOutputItem:     """Build a ToolCallOutputItem representing a rejected function tool call."""     if isinstance(tool_call, ResponseFunctionToolCall):         drop_agent_tool_run_result(tool_call, scope_id=scope_id)     return ToolCallOutputItem(         output=rejection_message,         raw_item=ItemHelpers.tool_call_output_item(             tool_call,             rejection_message,         ),         agent=agent,         tool_origin=tool_origin,     ) ``` |

### shell\_rejection\_item

```
shell_rejection_item(
    agent: Any,
    call_id: str,
    *,
    tool_call: Any | None = None,
    rejection_message: str = REJECTION_MESSAGE,
) -> ToolCallOutputItem
```

Build a ToolCallOutputItem representing a rejected shell call.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 ``` | ``` def shell_rejection_item(     agent: Any,     call_id: str,     *,     tool_call: Any | None = None,     rejection_message: str = REJECTION_MESSAGE, ) -> ToolCallOutputItem:     """Build a ToolCallOutputItem representing a rejected shell call."""     rejection_output: dict[str, Any] = {         "stdout": "",         "stderr": rejection_message,         "outcome": {"type": "exit", "exit_code": 1},     }     rejection_raw_item: dict[str, Any] = {         "type": "shell_call_output",         "call_id": call_id,         "output": [rejection_output],     }     if tool_call is not None:         ItemHelpers.copy_tool_call_caller(tool_call, rejection_raw_item)     return ToolCallOutputItem(agent=agent, output=rejection_message, raw_item=rejection_raw_item) ``` |

### apply\_patch\_rejection\_item

```
apply_patch_rejection_item(
    agent: Any,
    call_id: str,
    *,
    tool_call: Any | None = None,
    output_type: Literal[
        "apply_patch_call_output", "custom_tool_call_output"
    ] = "apply_patch_call_output",
    rejection_message: str = REJECTION_MESSAGE,
) -> ToolCallOutputItem
```

Build a ToolCallOutputItem representing a rejected apply\_patch call.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 ``` | ``` def apply_patch_rejection_item(     agent: Any,     call_id: str,     *,     tool_call: Any | None = None,     output_type: Literal["apply_patch_call_output", "custom_tool_call_output"] = (         "apply_patch_call_output"     ),     rejection_message: str = REJECTION_MESSAGE, ) -> ToolCallOutputItem:     """Build a ToolCallOutputItem representing a rejected apply_patch call."""     rejection_raw_item: dict[str, Any] = {         "type": output_type,         "call_id": call_id,         "output": rejection_message,     }     if output_type == "apply_patch_call_output":         rejection_raw_item["status"] = "failed"     if tool_call is not None:         ItemHelpers.copy_tool_call_caller(tool_call, rejection_raw_item)     return ToolCallOutputItem(         agent=agent,         output=rejection_message,         raw_item=rejection_raw_item,     ) ``` |

### extract\_mcp\_request\_id

```
extract_mcp_request_id(raw_item: Any) -> str | None
```

Pull the request id from hosted MCP approval payloads.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 ``` | ``` def extract_mcp_request_id(raw_item: Any) -> str | None:     """Pull the request id from hosted MCP approval payloads."""     if isinstance(raw_item, dict):         provider_data = raw_item.get("provider_data")         if isinstance(provider_data, dict):             candidate = provider_data.get("id")             if isinstance(candidate, str):                 return candidate         candidate = raw_item.get("id") or raw_item.get("call_id")         return candidate if isinstance(candidate, str) else None     try:         provider_data = getattr(raw_item, "provider_data", None)     except Exception:         provider_data = None     if isinstance(provider_data, dict):         candidate = provider_data.get("id")         if isinstance(candidate, str):             return candidate     try:         candidate = getattr(raw_item, "id", None) or getattr(raw_item, "call_id", None)     except Exception:         candidate = None     return candidate if isinstance(candidate, str) else None ``` |

### extract\_mcp\_request\_id\_from\_run

```
extract_mcp_request_id_from_run(mcp_run: Any) -> str | None
```

Extract the hosted MCP request id from a streaming run item.

Source code in `src/agents/run_internal/items.py`

|  |  |
| --- | --- |
| ``` 833 834 835 836 837 838 839 840 841 842 843 844 845 846 847 848 849 850 ``` | ``` def extract_mcp_request_id_from_run(mcp_run: Any) -> str | None:     """Extract the hosted MCP request id from a streaming run item."""     request_item = getattr(mcp_run, "request_item", None) or getattr(mcp_run, "requestItem", None)     if isinstance(request_item, dict):         provider_data = request_item.get("provider_data")         if isinstance(provider_data, dict):             candidate = provider_data.get("id")             if isinstance(candidate, str):                 return candidate         candidate = request_item.get("id") or request_item.get("call_id")     else:         provider_data = getattr(request_item, "provider_data", None)         if isinstance(provider_data, dict):             candidate = provider_data.get("id")             if isinstance(candidate, str):                 return candidate         candidate = getattr(request_item, "id", None) or getattr(request_item, "call_id", None)     return candidate if isinstance(candidate, str) else None ``` |