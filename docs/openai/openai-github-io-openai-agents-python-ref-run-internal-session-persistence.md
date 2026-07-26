---
url: https://openai.github.io/openai-agents-python/ref/run_internal/session_persistence/
title: `Session Persistence`
framework: openai
---

# `Session Persistence`

Session persistence helpers for the run pipeline. Only internal persistence/retry helpers
live here; public session interfaces stay in higher-level modules.

### resolve\_nested\_history\_owned\_session\_item\_refs

```
resolve_nested_history_owned_session_item_refs(
    session_items: Sequence[RunItem],
    current_input: str | Sequence[TResponseInputItem],
    history_owned_items: Sequence[NestedHistoryOwnedItem],
) -> list[NestedHistoryOwnedItemRef]
```

Locate explicitly owned nested-history occurrences in full session history.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ```  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 ``` | ``` def resolve_nested_history_owned_session_item_refs(     session_items: Sequence[RunItem],     current_input: str | Sequence[TResponseInputItem],     history_owned_items: Sequence[NestedHistoryOwnedItem], ) -> list[NestedHistoryOwnedItemRef]:     """Locate explicitly owned nested-history occurrences in full session history."""     if not history_owned_items or isinstance(current_input, str):         return []      session_indexes_by_identity: dict[int, deque[int]] = {}     session_indexes_by_occurrence_key: dict[str, deque[int]] = {}     for index, session_item in enumerate(session_items):         session_indexes_by_identity.setdefault(id(session_item), deque()).append(index)         occurrence_key = nested_history_run_item_occurrence_key(session_item)         if occurrence_key is not None:             session_indexes_by_occurrence_key.setdefault(occurrence_key, deque()).append(index)      used_session_indexes: set[int] = set()     resolved: list[NestedHistoryOwnedItemRef] = []      def _peek_unused(candidates: deque[int] | None) -> int | None:         while candidates and candidates[0] in used_session_indexes:             candidates.popleft()         return candidates[0] if candidates else None      for owned_item in history_owned_items:         if owned_item.input_index >= len(current_input):             continue         input_item = current_input[owned_item.input_index]         if digest_input_item(input_item) != owned_item.digest:             continue          occurrence_key = nested_history_run_item_occurrence_key(owned_item.run_item)         identity_index = (             _peek_unused(session_indexes_by_identity.get(id(owned_item.run_item)))             if owned_item.run_item is not None             else None         )         occurrence_index = (             _peek_unused(session_indexes_by_occurrence_key.get(occurrence_key))             if occurrence_key is not None             else None         )         candidate_indexes = [             index for index in (identity_index, occurrence_index) if index is not None         ]         if not candidate_indexes:             continue         session_index = min(candidate_indexes)         session_input = run_item_to_input_item(session_items[session_index])         if session_input is None or digest_input_item(session_input) != owned_item.digest:             continue         used_session_indexes.add(session_index)         session_item = session_items[session_index]         ensure_nested_history_run_item_occurrence_key(session_item)         resolved.append(             NestedHistoryOwnedItemRef(                 session_index=session_index,                 digest=owned_item.digest,                 input_index=owned_item.input_index,                 run_item=session_item,                 input_item=input_item,             )         )     return resolved ``` |

### reconcile\_nested\_history\_owned\_session\_item\_refs

```
reconcile_nested_history_owned_session_item_refs(
    session_items: Sequence[RunItem],
    previous_refs: Sequence[NestedHistoryOwnedItemRef],
    previous_input: str | Sequence[TResponseInputItem],
    current_input: str | Sequence[TResponseInputItem],
    history_owned_items: Sequence[NestedHistoryOwnedItem],
) -> list[NestedHistoryOwnedItemRef]
```

Retain surviving ownership and add provenance introduced by a history rewrite.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 ``` | ``` def reconcile_nested_history_owned_session_item_refs(     session_items: Sequence[RunItem],     previous_refs: Sequence[NestedHistoryOwnedItemRef],     previous_input: str | Sequence[TResponseInputItem],     current_input: str | Sequence[TResponseInputItem],     history_owned_items: Sequence[NestedHistoryOwnedItem], ) -> list[NestedHistoryOwnedItemRef]:     """Retain surviving ownership and add provenance introduced by a history rewrite."""     _, retained_refs = reconcile_nested_history_owned_input_after_rewrite(         previous_input,         current_input,         previous_refs,     )     new_refs = resolve_nested_history_owned_session_item_refs(         session_items,         current_input,         history_owned_items,     )     retained_set = set(retained_refs)     return retained_refs + [item_ref for item_ref in new_refs if item_ref not in retained_set] ``` |

### prepare\_input\_with\_session `async`

```
prepare_input_with_session(
    input: str | list[TResponseInputItem],
    session: Session | None,
    session_input_callback: SessionInputCallback | None,
    session_settings: SessionSettings | None = None,
    *,
    include_history_in_prepared_input: bool = True,
    preserve_dropped_new_items: bool = False,
) -> tuple[
    str | list[TResponseInputItem], list[TResponseInputItem]
]
```

Prepare model input from session history plus the new turn input.

Returns a tuple of:

1. The prepared input that should be sent to the model after normalization and dedupe.
2. The subset of items that should be appended to the session store for this turn.

The second value is intentionally not "everything returned by the callback". When a
`session_input_callback` reorders or filters history, we still need to persist only the
items that belong to the new turn. This function therefore compares the callback output
against deep-copied history and new-input lists, first by object identity and then by
content frequency, so retries and custom merge strategies do not accidentally re-persist
old history as fresh input.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 ``` | ``` async def prepare_input_with_session(     input: str | list[TResponseInputItem],     session: Session | None,     session_input_callback: SessionInputCallback | None,     session_settings: SessionSettings | None = None,     *,     include_history_in_prepared_input: bool = True,     preserve_dropped_new_items: bool = False, ) -> tuple[str | list[TResponseInputItem], list[TResponseInputItem]]:     """Prepare model input from session history plus the new turn input.      Returns a tuple of:      1. The prepared input that should be sent to the model after normalization and dedupe.     2. The subset of items that should be appended to the session store for this turn.      The second value is intentionally not "everything returned by the callback". When a     ``session_input_callback`` reorders or filters history, we still need to persist only the     items that belong to the new turn. This function therefore compares the callback output     against deep-copied history and new-input lists, first by object identity and then by     content frequency, so retries and custom merge strategies do not accidentally re-persist     old history as fresh input.     """      if session is None:         return input, []      resolved_settings = getattr(session, "session_settings", None) or SessionSettings()     if session_settings is not None:         resolved_settings = resolved_settings.resolve(session_settings)      if resolved_settings.limit is not None:         history = await session.get_items(limit=resolved_settings.limit)     else:         history = await session.get_items()     is_openai_conversation_session = isinstance(session, OpenAIConversationsSession)     converted_history = [         strip_internal_input_item_metadata(ensure_input_item_format(item)) for item in history     ]      new_input_list = [         ensure_input_item_format(item) for item in ItemHelpers.input_to_new_input_list(input)     ]      prune_history_indexes: set[int] = set()      if session_input_callback is None or not include_history_in_prepared_input:         prepared_items_raw: list[TResponseInputItem] = (             converted_history + new_input_list             if include_history_in_prepared_input             else list(new_input_list)         )         appended_items = list(new_input_list)         if include_history_in_prepared_input:             prune_history_indexes = set(range(len(converted_history)))     else:         if not callable(session_input_callback):             raise UserError(                 f"Invalid `session_input_callback` value: {session_input_callback}. "                 "Choose between `None` or a custom callable function."             )         history_for_callback = copy.deepcopy(converted_history)         new_items_for_callback = copy.deepcopy(new_input_list)         combined = session_input_callback(history_for_callback, new_items_for_callback)         if inspect.isawaitable(combined):             combined = await combined         if not isinstance(combined, list):             raise UserError("Session input callback must return a list of input items.")          # The callback may reorder, drop, or duplicate items. Keep separate reference maps for         # the copied history and copied new-input lists so we can reconstruct which output items         # belong to the new turn and therefore still need to be persisted.         history_refs = _build_reference_map(             history_for_callback,             ignore_openai_conversation_item_ids=is_openai_conversation_session,         )         new_refs = _build_reference_map(new_items_for_callback)         history_counts = _build_frequency_map(             history_for_callback,             ignore_openai_conversation_item_ids=is_openai_conversation_session,         )         new_counts = _build_frequency_map(new_items_for_callback)          appended: list[Any] = []         for combined_index, item in enumerate(combined):             history_key = _session_item_key(                 item,                 ignore_openai_conversation_item_ids=is_openai_conversation_session,             )             new_key = _session_item_key(item)             if _consume_reference(new_refs, new_key, item):                 new_counts[new_key] = max(new_counts.get(new_key, 0) - 1, 0)                 appended.append(item)                 continue             if _consume_reference(history_refs, history_key, item):                 history_counts[history_key] = max(history_counts.get(history_key, 0) - 1, 0)                 prune_history_indexes.add(combined_index)                 continue             if history_counts.get(history_key, 0) > 0:                 history_counts[history_key] = history_counts.get(history_key, 0) - 1                 prune_history_indexes.add(combined_index)                 continue             if new_counts.get(new_key, 0) > 0:                 new_counts[new_key] = max(new_counts.get(new_key, 0) - 1, 0)                 appended.append(item)                 continue             appended.append(item)          appended_items = [ensure_input_item_format(item) for item in appended]          if include_history_in_prepared_input:             prepared_items_raw = combined         elif appended_items:             prepared_items_raw = appended_items         else:             prepared_items_raw = new_items_for_callback if preserve_dropped_new_items else []      # Normalize exactly as the runtime does elsewhere so the prepared model input and the     # persisted session items are derived from the same item shape and dedupe rules.     if is_openai_conversation_session and prune_history_indexes:         prepared_items_raw = _sanitize_openai_conversation_history_items_for_model_input(             prepared_items_raw,             prune_history_indexes,         )     prepared_as_inputs = [ensure_input_item_format(item) for item in prepared_items_raw]     filtered = drop_orphan_function_calls(         prepared_as_inputs,         pruning_indexes=prune_history_indexes,     )     normalized = normalize_input_items_for_api(filtered)     deduplicated = deduplicate_input_items_preferring_latest(normalized)      appended_as_inputs = [ensure_input_item_format(item) for item in appended_items]     return deduplicated, normalize_input_items_for_api(appended_as_inputs) ``` |

### persist\_session\_items\_for\_guardrail\_trip `async`

```
persist_session_items_for_guardrail_trip(
    session: Session | None,
    server_conversation_tracker: OpenAIServerConversationTracker
    | None,
    session_input_items_for_persistence: list[
        TResponseInputItem
    ]
    | None,
    original_user_input: str
    | list[TResponseInputItem]
    | None,
    run_state: RunState | None,
    store: bool | None = None,
) -> list[TResponseInputItem] | None
```

Persist input items when a guardrail tripwire is triggered.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 ``` | ``` async def persist_session_items_for_guardrail_trip(     session: Session | None,     server_conversation_tracker: OpenAIServerConversationTracker | None,     session_input_items_for_persistence: list[TResponseInputItem] | None,     original_user_input: str | list[TResponseInputItem] | None,     run_state: RunState | None,     store: bool | None = None, ) -> list[TResponseInputItem] | None:     """     Persist input items when a guardrail tripwire is triggered.     """     if session is None or server_conversation_tracker is not None:         return session_input_items_for_persistence      updated_session_input_items = session_input_items_for_persistence     if updated_session_input_items is None and original_user_input is not None:         updated_session_input_items = ItemHelpers.input_to_new_input_list(original_user_input)      input_items_for_save: list[TResponseInputItem] = (         updated_session_input_items if updated_session_input_items is not None else []     )     await save_result_to_session(session, input_items_for_save, [], run_state, store=store)     return updated_session_input_items ``` |

### session\_items\_for\_turn

```
session_items_for_turn(
    turn_result: SingleStepResult,
) -> list[RunItem]
```

Return the items to persist for a turn, preferring session\_step\_items when set.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 313 314 315 316 317 318 319 320 ``` | ``` def session_items_for_turn(turn_result: SingleStepResult) -> list[RunItem]:     """Return the items to persist for a turn, preferring session_step_items when set."""     items = (         turn_result.session_step_items         if turn_result.session_step_items is not None         else turn_result.new_step_items     )     return list(items) ``` |

### resumed\_turn\_items

```
resumed_turn_items(
    turn_result: SingleStepResult,
) -> tuple[list[RunItem], list[RunItem]]
```

Return generated and session items for a resumed turn.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 323 324 325 326 327 ``` | ``` def resumed_turn_items(turn_result: SingleStepResult) -> tuple[list[RunItem], list[RunItem]]:     """Return generated and session items for a resumed turn."""     generated_items = list(turn_result.pre_step_items) + list(turn_result.new_step_items)     turn_session_items = session_items_for_turn(turn_result)     return generated_items, turn_session_items ``` |

### update\_run\_state\_after\_resume

```
update_run_state_after_resume(
    run_state: RunState,
    *,
    turn_result: SingleStepResult,
    generated_items: list[RunItem],
    session_items: list[RunItem] | None = None,
) -> None
```

Update run state fields after resolving an interruption.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 330 331 332 333 334 335 336 337 338 339 340 341 342 ``` | ``` def update_run_state_after_resume(     run_state: RunState,     *,     turn_result: SingleStepResult,     generated_items: list[RunItem],     session_items: list[RunItem] | None = None, ) -> None:     """Update run state fields after resolving an interruption."""     run_state._original_input = copy_input_items(turn_result.original_input)     run_state._generated_items = generated_items     if session_items is not None:         run_state._session_items = list(session_items)     run_state._current_step = turn_result.next_step  # type: ignore[assignment] ``` |

### save\_result\_to\_session `async`

```
save_result_to_session(
    session: Session | None,
    original_input: str | list[TResponseInputItem],
    new_items: list[RunItem],
    run_state: RunState | None = None,
    *,
    response_id: str | None = None,
    reasoning_item_id_policy: ReasoningItemIdPolicy
    | None = None,
    store: bool | None = None,
) -> int
```

Persist a turn to the session store, keeping track of what was already saved so retries
during streaming do not duplicate tool outputs or inputs.

Returns:

| Type | Description |
| --- | --- |
| `int` | The number of new run items persisted for this call. |

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 ``` | ``` async def save_result_to_session(     session: Session | None,     original_input: str | list[TResponseInputItem],     new_items: list[RunItem],     run_state: RunState | None = None,     *,     response_id: str | None = None,     reasoning_item_id_policy: ReasoningItemIdPolicy | None = None,     store: bool | None = None, ) -> int:     """     Persist a turn to the session store, keeping track of what was already saved so retries     during streaming do not duplicate tool outputs or inputs.      Returns:         The number of new run items persisted for this call.     """     already_persisted = run_state._current_turn_persisted_item_count if run_state else 0      if session is None:         return 0      new_run_items: list[RunItem]     if already_persisted >= len(new_items):         new_run_items = []     else:         new_run_items = new_items[already_persisted:]     if run_state and new_items and new_run_items:         missing_outputs = [             item             for item in new_items             if item.type == "tool_call_output_item" and item not in new_run_items         ]         if missing_outputs:             new_run_items = missing_outputs + new_run_items      input_list: list[TResponseInputItem] = []     if original_input:         input_list = normalize_input_items_for_api(             [                 ensure_input_item_format(item)                 for item in ItemHelpers.input_to_new_input_list(original_input)             ]         )      is_openai_conversation_session = isinstance(session, OpenAIConversationsSession)     resolved_reasoning_item_id_policy = (         reasoning_item_id_policy         if reasoning_item_id_policy is not None         else (run_state._reasoning_item_id_policy if run_state is not None else None)     )     persistence_reasoning_item_id_policy = (         None if is_openai_conversation_session else resolved_reasoning_item_id_policy     )     new_items_as_input: list[TResponseInputItem] = []     for run_item in new_run_items:         converted = run_item_to_input_item(run_item, persistence_reasoning_item_id_policy)         if converted is None:             continue         new_items_as_input.append(ensure_input_item_format(converted))      ignore_ids_for_matching = _ignore_ids_for_matching(session)      new_items_for_fingerprint = (         [_sanitize_openai_conversation_item(item) for item in new_items_as_input]         if is_openai_conversation_session         else new_items_as_input     )     serialized_new_items = [         _fingerprint_or_repr(item, ignore_ids_for_matching=ignore_ids_for_matching)         for item in new_items_for_fingerprint     ]      items_to_save = deduplicate_input_items_preferring_latest(input_list + new_items_as_input)      if is_openai_conversation_session and items_to_save:         items_to_save = [_sanitize_openai_conversation_item(item) for item in items_to_save]      serialized_to_save: list[str] = [         _fingerprint_or_repr(item, ignore_ids_for_matching=ignore_ids_for_matching)         for item in items_to_save     ]     serialized_to_save_counts: dict[str, int] = {}     for serialized in serialized_to_save:         serialized_to_save_counts[serialized] = serialized_to_save_counts.get(serialized, 0) + 1      saved_run_items_count = 0     for serialized in serialized_new_items:         if serialized_to_save_counts.get(serialized, 0) > 0:             serialized_to_save_counts[serialized] -= 1             saved_run_items_count += 1      if is_openai_conversation_session:         items_to_save = [             item for item in items_to_save if not _is_unpersistable_for_openai_conversation(item)         ]      if len(items_to_save) == 0:         if run_state:             run_state._current_turn_persisted_item_count = already_persisted + saved_run_items_count         return saved_run_items_count      await session.add_items(items_to_save)      if run_state:         run_state._current_turn_persisted_item_count = already_persisted + saved_run_items_count      if response_id and is_openai_responses_compaction_aware_session(session):         has_local_tool_outputs = any(             isinstance(item, ToolCallOutputItem | HandoffOutputItem) for item in new_items         )         if has_local_tool_outputs:             defer_compaction = getattr(session, "_defer_compaction", None)             if callable(defer_compaction):                 result = defer_compaction(response_id, store=store)                 if inspect.isawaitable(result):                     await result             logger.debug(                 "skip: deferring compaction for response %s due to local tool outputs",                 response_id,             )             return saved_run_items_count          deferred_response_id = None         get_deferred = getattr(session, "_get_deferred_compaction_response_id", None)         if callable(get_deferred):             deferred_response_id = get_deferred()         force_compaction = deferred_response_id is not None         if force_compaction:             logger.debug(                 "compact: forcing for response %s after deferred %s",                 response_id,                 deferred_response_id,             )         compaction_args: OpenAIResponsesCompactionArgs = {             "response_id": response_id,             "force": force_compaction,         }         if store is not None:             compaction_args["store"] = store         await session.run_compaction(compaction_args)      return saved_run_items_count ``` |

### save\_resumed\_turn\_items `async`

```
save_resumed_turn_items(
    *,
    session: Session | None,
    items: list[RunItem],
    persisted_count: int,
    response_id: str | None,
    reasoning_item_id_policy: ReasoningItemIdPolicy
    | None = None,
    store: bool | None = None,
) -> int
```

Persist resumed turn items and return the updated persisted count.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 ``` | ``` async def save_resumed_turn_items(     *,     session: Session | None,     items: list[RunItem],     persisted_count: int,     response_id: str | None,     reasoning_item_id_policy: ReasoningItemIdPolicy | None = None,     store: bool | None = None, ) -> int:     """Persist resumed turn items and return the updated persisted count."""     if session is None or not items:         return persisted_count     saved_count = await save_result_to_session(         session,         [],         list(items),         None,         response_id=response_id,         reasoning_item_id_policy=reasoning_item_id_policy,         store=store,     )     return persisted_count + saved_count ``` |

### rewind\_session\_items `async`

```
rewind_session_items(
    session: Session | None,
    items: Sequence[TResponseInputItem],
    server_tracker: OpenAIServerConversationTracker
    | None = None,
) -> None
```

Best-effort helper to roll back items recently persisted to a session when a conversation
retry is needed, so we do not accumulate duplicate inputs on lock errors.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 ``` | ``` async def rewind_session_items(     session: Session | None,     items: Sequence[TResponseInputItem],     server_tracker: OpenAIServerConversationTracker | None = None, ) -> None:     """     Best-effort helper to roll back items recently persisted to a session when a conversation     retry is needed, so we do not accumulate duplicate inputs on lock errors.     """     if session is None or not items:         return      pop_item = getattr(session, "pop_item", None)     if not callable(pop_item):         return      ignore_ids_for_matching = _ignore_ids_for_matching(session)     target_serializations: list[str] = []     for item in items:         serialized = fingerprint_input_item(item, ignore_ids_for_matching=ignore_ids_for_matching)         if serialized:             target_serializations.append(serialized)      if not target_serializations:         return      logger.debug(         "Rewinding session items due to conversation retry (targets=%d)",         len(target_serializations),     )      for i, target in enumerate(target_serializations):         logger.debug("Rewind target %d (first 300 chars): %s", i, target[:300])      snapshot_serializations = target_serializations.copy()     rewound = await _rewind_session_tail_suffix(         session=session,         pop_item=pop_item,         expected_serializations=target_serializations,         ignore_ids_for_matching=ignore_ids_for_matching,         mismatch_warning=(             "Skipping session rewind because the current tail does not match the retry-owned suffix"         ),         pop_failure_warning="Failed to rewind session item: %s",     )     if not rewound:         return      await wait_for_session_cleanup(         session,         snapshot_serializations,         ignore_ids_for_matching=ignore_ids_for_matching,     )      if session is None or server_tracker is None:         return      try:         latest_items = await session.get_items(limit=1)     except Exception as exc:         logger.debug("Failed to peek session items while rewinding: %s", exc)         return      if not latest_items:         return      latest_id = latest_items[0].get("id")     if isinstance(latest_id, str) and latest_id in server_tracker.server_item_ids:         return      try:         session_items = await session.get_items()     except Exception as exc:         logger.debug("Failed to inspect session tail while stripping stray items: %s", exc)         return      stray_serializations = _collect_retry_owned_tail_serializations(         session_items,         server_tracker=server_tracker,         ignore_ids_for_matching=ignore_ids_for_matching,     )     if not stray_serializations:         return      logger.debug(         "Stripping %d retry-owned conversation items until the session tail reaches "         "a known server item",         len(stray_serializations),     )     await _rewind_session_tail_suffix(         session=session,         pop_item=pop_item,         expected_serializations=stray_serializations,         ignore_ids_for_matching=ignore_ids_for_matching,         mismatch_warning=(             "Skipping stray session cleanup because the current tail no longer matches "             "retry-owned conversation items"         ),         pop_failure_warning="Failed to strip stray session item: %s",     ) ``` |

### wait\_for\_session\_cleanup `async`

```
wait_for_session_cleanup(
    session: Session | None,
    serialized_targets: Sequence[str],
    *,
    max_attempts: int = 5,
    ignore_ids_for_matching: bool = False,
) -> None
```

Confirm that rewound items are no longer present in the session tail so the store stays
consistent before the next retry attempt begins.

Source code in `src/agents/run_internal/session_persistence.py`

|  |  |
| --- | --- |
| ``` 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 ``` | ``` async def wait_for_session_cleanup(     session: Session | None,     serialized_targets: Sequence[str],     *,     max_attempts: int = 5,     ignore_ids_for_matching: bool = False, ) -> None:     """     Confirm that rewound items are no longer present in the session tail so the store stays     consistent before the next retry attempt begins.     """     if session is None or not serialized_targets:         return      window = len(serialized_targets) + 2      for attempt in range(max_attempts):         try:             tail_items = await session.get_items(limit=window)         except Exception as exc:             logger.debug("Failed to verify session cleanup (attempt %d): %s", attempt + 1, exc)             await asyncio.sleep(0.1 * (attempt + 1))             continue          serialized_tail: set[str] = set()         for item in tail_items:             serialized = fingerprint_input_item(                 item, ignore_ids_for_matching=ignore_ids_for_matching             )             if serialized:                 serialized_tail.add(serialized)          if not any(serial in serialized_tail for serial in serialized_targets):             return          await asyncio.sleep(0.1 * (attempt + 1))      logger.debug(         "Session cleanup verification exhausted attempts; targets may still linger temporarily"     ) ``` |