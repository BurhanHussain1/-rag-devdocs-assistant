---
url: https://openai.github.io/openai-agents-python/ref/memory/openai_responses_compaction_session/
title: `OpenAI Responses Compaction Session`
framework: openai
---

# `OpenAI Responses Compaction Session`

### OpenAIResponsesCompactionSession

Bases: `SessionABC`, `OpenAIResponsesCompactionAwareSession`

Session decorator that triggers responses.compact when stored history grows.

Works with OpenAI Responses API models only. Wraps any Session (except
OpenAIConversationsSession) and automatically calls the OpenAI responses.compact
API after each turn when the decision hook returns True.

Source code in `src/agents/memory/openai_responses_compaction_session.py`

|  |  |
| --- | --- |
| ```  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 ``` | ``` class OpenAIResponsesCompactionSession(SessionABC, OpenAIResponsesCompactionAwareSession):     """Session decorator that triggers responses.compact when stored history grows.      Works with OpenAI Responses API models only. Wraps any Session (except     OpenAIConversationsSession) and automatically calls the OpenAI responses.compact     API after each turn when the decision hook returns True.     """      def __init__(         self,         session_id: str,         underlying_session: Session,         *,         client: AsyncOpenAI | None = None,         model: str = "gpt-4.1",         compaction_mode: OpenAIResponsesCompactionMode = "auto",         should_trigger_compaction: Callable[[dict[str, Any]], bool] | None = None,     ):         """Initialize the compaction session.          Args:             session_id: Identifier for this session.             underlying_session: Session store that holds the compacted history. Cannot be                 OpenAIConversationsSession.             client: OpenAI client for responses.compact API calls. Defaults to                 get_default_openai_client() or new AsyncOpenAI().             model: Model to use for responses.compact. Defaults to "gpt-4.1". Must be an                 OpenAI model name (gpt-*, o*, or ft:gpt-*).             compaction_mode: Controls how the compaction request provides conversation                 history. "auto" (default) uses input when the last response was not                 stored or no response_id is available.             should_trigger_compaction: Custom decision hook. Defaults to triggering when                 10+ compaction candidates exist.         """         if isinstance(underlying_session, OpenAIConversationsSession):             raise ValueError(                 "OpenAIResponsesCompactionSession cannot wrap OpenAIConversationsSession "                 "because it manages its own history on the server."             )          if not is_openai_model_name(model):             raise ValueError(f"Unsupported model for OpenAI responses compaction: {model}")          self.session_id = session_id         self.underlying_session = underlying_session         self._client = client         self.model = model         self.compaction_mode = compaction_mode         self.should_trigger_compaction = (             should_trigger_compaction or default_should_trigger_compaction         )          # cache for incremental candidate tracking         self._compaction_candidate_items: list[TResponseInputItem] | None = None         self._session_items: list[TResponseInputItem] | None = None         self._response_id: str | None = None         self._deferred_response_id: str | None = None         self._last_unstored_response_id: str | None = None      @property     def client(self) -> AsyncOpenAI:         if self._client is None:             self._client = get_default_openai_client() or AsyncOpenAI()         return self._client      def _resolve_compaction_mode_for_response(         self,         *,         response_id: str | None,         store: bool | None,         requested_mode: OpenAIResponsesCompactionMode | None,     ) -> _ResolvedCompactionMode:         mode = requested_mode or self.compaction_mode         if (             mode == "auto"             and store is None             and response_id is not None             and response_id == self._last_unstored_response_id         ):             return "input"         return _resolve_compaction_mode(mode, response_id=response_id, store=store)      async def run_compaction(self, args: OpenAIResponsesCompactionArgs | None = None) -> None:         """Run compaction using responses.compact API."""         if args and args.get("response_id"):             self._response_id = args["response_id"]         requested_mode = args.get("compaction_mode") if args else None         if args and "store" in args:             store = args["store"]             if store is False and self._response_id:                 self._last_unstored_response_id = self._response_id             elif store is True and self._response_id == self._last_unstored_response_id:                 self._last_unstored_response_id = None         else:             store = None         resolved_mode = self._resolve_compaction_mode_for_response(             response_id=self._response_id,             store=store,             requested_mode=requested_mode,         )          if resolved_mode == "previous_response_id" and not self._response_id:             raise ValueError(                 "OpenAIResponsesCompactionSession.run_compaction requires a response_id "                 "when using previous_response_id compaction."             )          compaction_candidate_items, session_items = await self._ensure_compaction_candidates()          force = args.get("force", False) if args else False         should_compact = force or self.should_trigger_compaction(             {                 "response_id": self._response_id,                 "compaction_mode": resolved_mode,                 "compaction_candidate_items": compaction_candidate_items,                 "session_items": session_items,             }         )          if not should_compact:             logger.debug(                 "skip: decision hook declined compaction for %s (mode=%s)",                 self._response_id,                 resolved_mode,             )             return          self._deferred_response_id = None         logger.debug(             "compact: start for %s using %s (mode=%s)",             self._response_id,             self.model,             resolved_mode,         )          compact_kwargs: dict[str, Any] = {"model": self.model}         if resolved_mode == "previous_response_id":             compact_kwargs["previous_response_id"] = self._response_id         else:             compact_kwargs["input"] = session_items          compacted = await self.client.responses.compact(**compact_kwargs)          output_items = _strip_orphaned_assistant_ids(             _normalize_compaction_output_items(compacted.output or [])         )          previous_items = await self._get_all_underlying_session_items()         await self._replace_underlying_session_items(             output_items=output_items,             previous_items=previous_items,         )          self._compaction_candidate_items = select_compaction_candidate_items(output_items)         self._session_items = output_items          logger.debug(             "compact: done for %s (mode=%s, output=%s, candidates=%s)",             self._response_id,             resolved_mode,             len(output_items),             len(self._compaction_candidate_items),         )      async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         return await self.underlying_session.get_items(limit)      async def _get_all_underlying_session_items(self) -> list[TResponseInputItem]:         return await self.underlying_session.get_items(limit=_ALL_SESSION_ITEMS_LIMIT)      async def _replace_underlying_session_items(         self,         *,         output_items: list[TResponseInputItem],         previous_items: list[TResponseInputItem],     ) -> None:         try:             await self.underlying_session.clear_session()         except Exception as clear_error:             await self._restore_underlying_session_items_after_failed_clear(                 previous_items, clear_error             )             raise          try:             if output_items:                 await self.underlying_session.add_items(output_items)         except Exception as replacement_error:             await self._restore_underlying_session_items(previous_items, replacement_error)             raise      async def _restore_underlying_session_items_after_failed_clear(         self,         previous_items: list[TResponseInputItem],         clear_error: Exception,     ) -> None:         try:             current_items = await self._get_all_underlying_session_items()         except Exception:             logger.warning(                 "Failed to inspect session history after compaction replacement clear failed.",                 exc_info=True,             )             return          if current_items == previous_items:             return          await self._restore_underlying_session_items(             previous_items, clear_error, clear_existing_items=False         )      async def _restore_underlying_session_items(         self,         previous_items: list[TResponseInputItem],         replacement_error: Exception,         *,         clear_existing_items: bool = True,     ) -> None:         try:             if clear_existing_items:                 await self.underlying_session.clear_session()             if previous_items:                 await self.underlying_session.add_items(list(previous_items))         except Exception:             logger.warning(                 "Failed to restore session history after compaction replacement failed.",                 exc_info=True,             )             return          logger.warning(             "Restored previous session history after compaction replacement failed: %s",             replacement_error,         )      async def _defer_compaction(self, response_id: str, store: bool | None = None) -> None:         if self._deferred_response_id is not None:             return         compaction_candidate_items, session_items = await self._ensure_compaction_candidates()         resolved_mode = self._resolve_compaction_mode_for_response(             response_id=response_id,             store=store,             requested_mode=None,         )         should_compact = self.should_trigger_compaction(             {                 "response_id": response_id,                 "compaction_mode": resolved_mode,                 "compaction_candidate_items": compaction_candidate_items,                 "session_items": session_items,             }         )         if should_compact:             self._deferred_response_id = response_id      def _get_deferred_compaction_response_id(self) -> str | None:         return self._deferred_response_id      def _clear_deferred_compaction(self) -> None:         self._deferred_response_id = None      async def add_items(self, items: list[TResponseInputItem]) -> None:         await self.underlying_session.add_items(items)         if self._compaction_candidate_items is not None:             new_items = _normalize_compaction_session_items(items)             new_candidates = select_compaction_candidate_items(new_items)             if new_candidates:                 self._compaction_candidate_items.extend(new_candidates)         if self._session_items is not None:             self._session_items.extend(_normalize_compaction_session_items(items))      async def pop_item(self) -> TResponseInputItem | None:         popped = await self.underlying_session.pop_item()         if popped:             self._compaction_candidate_items = None             self._session_items = None         return popped      async def clear_session(self) -> None:         await self.underlying_session.clear_session()         self._compaction_candidate_items = []         self._session_items = []         self._deferred_response_id = None      async def _ensure_compaction_candidates(         self,     ) -> tuple[list[TResponseInputItem], list[TResponseInputItem]]:         """Lazy-load and cache compaction candidates."""         if self._compaction_candidate_items is not None and self._session_items is not None:             return (self._compaction_candidate_items[:], self._session_items[:])          history = _normalize_compaction_session_items(await self.underlying_session.get_items())         candidates = select_compaction_candidate_items(history)         self._compaction_candidate_items = candidates         self._session_items = history          logger.debug(             "candidates: initialized (history=%s, candidates=%s)",             len(history),             len(candidates),         )         return (candidates[:], history[:]) ``` |

#### \_\_init\_\_

```
__init__(
    session_id: str,
    underlying_session: Session,
    *,
    client: AsyncOpenAI | None = None,
    model: str = "gpt-4.1",
    compaction_mode: OpenAIResponsesCompactionMode = "auto",
    should_trigger_compaction: Callable[
        [dict[str, Any]], bool
    ]
    | None = None,
)
```

Initialize the compaction session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Identifier for this session. | *required* |
| `underlying_session` | `Session` | Session store that holds the compacted history. Cannot be OpenAIConversationsSession. | *required* |
| `client` | `AsyncOpenAI | None` | OpenAI client for responses.compact API calls. Defaults to get\_default\_openai\_client() or new AsyncOpenAI(). | `None` |
| `model` | `str` | Model to use for responses.compact. Defaults to "gpt-4.1". Must be an OpenAI model name (gpt-*, o*, or ft:gpt-\*). | `'gpt-4.1'` |
| `compaction_mode` | `OpenAIResponsesCompactionMode` | Controls how the compaction request provides conversation history. "auto" (default) uses input when the last response was not stored or no response\_id is available. | `'auto'` |
| `should_trigger_compaction` | `Callable[[dict[str, Any]], bool] | None` | Custom decision hook. Defaults to triggering when 10+ compaction candidates exist. | `None` |

Source code in `src/agents/memory/openai_responses_compaction_session.py`

|  |  |
| --- | --- |
| ```  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 ``` | ``` def __init__(     self,     session_id: str,     underlying_session: Session,     *,     client: AsyncOpenAI | None = None,     model: str = "gpt-4.1",     compaction_mode: OpenAIResponsesCompactionMode = "auto",     should_trigger_compaction: Callable[[dict[str, Any]], bool] | None = None, ):     """Initialize the compaction session.      Args:         session_id: Identifier for this session.         underlying_session: Session store that holds the compacted history. Cannot be             OpenAIConversationsSession.         client: OpenAI client for responses.compact API calls. Defaults to             get_default_openai_client() or new AsyncOpenAI().         model: Model to use for responses.compact. Defaults to "gpt-4.1". Must be an             OpenAI model name (gpt-*, o*, or ft:gpt-*).         compaction_mode: Controls how the compaction request provides conversation             history. "auto" (default) uses input when the last response was not             stored or no response_id is available.         should_trigger_compaction: Custom decision hook. Defaults to triggering when             10+ compaction candidates exist.     """     if isinstance(underlying_session, OpenAIConversationsSession):         raise ValueError(             "OpenAIResponsesCompactionSession cannot wrap OpenAIConversationsSession "             "because it manages its own history on the server."         )      if not is_openai_model_name(model):         raise ValueError(f"Unsupported model for OpenAI responses compaction: {model}")      self.session_id = session_id     self.underlying_session = underlying_session     self._client = client     self.model = model     self.compaction_mode = compaction_mode     self.should_trigger_compaction = (         should_trigger_compaction or default_should_trigger_compaction     )      # cache for incremental candidate tracking     self._compaction_candidate_items: list[TResponseInputItem] | None = None     self._session_items: list[TResponseInputItem] | None = None     self._response_id: str | None = None     self._deferred_response_id: str | None = None     self._last_unstored_response_id: str | None = None ``` |

#### run\_compaction `async`

```
run_compaction(
    args: OpenAIResponsesCompactionArgs | None = None,
) -> None
```

Run compaction using responses.compact API.

Source code in `src/agents/memory/openai_responses_compaction_session.py`

|  |  |
| --- | --- |
| ``` 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 ``` | ``` async def run_compaction(self, args: OpenAIResponsesCompactionArgs | None = None) -> None:     """Run compaction using responses.compact API."""     if args and args.get("response_id"):         self._response_id = args["response_id"]     requested_mode = args.get("compaction_mode") if args else None     if args and "store" in args:         store = args["store"]         if store is False and self._response_id:             self._last_unstored_response_id = self._response_id         elif store is True and self._response_id == self._last_unstored_response_id:             self._last_unstored_response_id = None     else:         store = None     resolved_mode = self._resolve_compaction_mode_for_response(         response_id=self._response_id,         store=store,         requested_mode=requested_mode,     )      if resolved_mode == "previous_response_id" and not self._response_id:         raise ValueError(             "OpenAIResponsesCompactionSession.run_compaction requires a response_id "             "when using previous_response_id compaction."         )      compaction_candidate_items, session_items = await self._ensure_compaction_candidates()      force = args.get("force", False) if args else False     should_compact = force or self.should_trigger_compaction(         {             "response_id": self._response_id,             "compaction_mode": resolved_mode,             "compaction_candidate_items": compaction_candidate_items,             "session_items": session_items,         }     )      if not should_compact:         logger.debug(             "skip: decision hook declined compaction for %s (mode=%s)",             self._response_id,             resolved_mode,         )         return      self._deferred_response_id = None     logger.debug(         "compact: start for %s using %s (mode=%s)",         self._response_id,         self.model,         resolved_mode,     )      compact_kwargs: dict[str, Any] = {"model": self.model}     if resolved_mode == "previous_response_id":         compact_kwargs["previous_response_id"] = self._response_id     else:         compact_kwargs["input"] = session_items      compacted = await self.client.responses.compact(**compact_kwargs)      output_items = _strip_orphaned_assistant_ids(         _normalize_compaction_output_items(compacted.output or [])     )      previous_items = await self._get_all_underlying_session_items()     await self._replace_underlying_session_items(         output_items=output_items,         previous_items=previous_items,     )      self._compaction_candidate_items = select_compaction_candidate_items(output_items)     self._session_items = output_items      logger.debug(         "compact: done for %s (mode=%s, output=%s, candidates=%s)",         self._response_id,         resolved_mode,         len(output_items),         len(self._compaction_candidate_items),     ) ``` |

### select\_compaction\_candidate\_items

```
select_compaction_candidate_items(
    items: list[TResponseInputItem],
) -> list[TResponseInputItem]
```

Select compaction candidate items.

Excludes user messages and compaction items.

Source code in `src/agents/memory/openai_responses_compaction_session.py`

|  |  |
| --- | --- |
| ``` 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 ``` | ``` def select_compaction_candidate_items(     items: list[TResponseInputItem], ) -> list[TResponseInputItem]:     """Select compaction candidate items.      Excludes user messages and compaction items.     """      def _is_user_message(item: TResponseInputItem) -> bool:         if not isinstance(item, dict):             return False         if item.get("type") == "message":             return item.get("role") == "user"         return item.get("role") == "user" and "content" in item      return [         item         for item in items         if not (             _is_user_message(item) or (isinstance(item, dict) and item.get("type") == "compaction")         )     ] ``` |

### default\_should\_trigger\_compaction

```
default_should_trigger_compaction(
    context: dict[str, Any],
) -> bool
```

Default decision: compact when >= 10 candidate items exist.

Source code in `src/agents/memory/openai_responses_compaction_session.py`

|  |  |
| --- | --- |
| ``` 54 55 56 ``` | ``` def default_should_trigger_compaction(context: dict[str, Any]) -> bool:     """Default decision: compact when >= 10 candidate items exist."""     return len(context["compaction_candidate_items"]) >= DEFAULT_COMPACTION_THRESHOLD ``` |

### is\_openai\_model\_name

```
is_openai_model_name(model: str) -> bool
```

Validate model name follows OpenAI conventions.

Source code in `src/agents/memory/openai_responses_compaction_session.py`

|  |  |
| --- | --- |
| ``` 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 ``` | ``` def is_openai_model_name(model: str) -> bool:     """Validate model name follows OpenAI conventions."""     trimmed = model.strip()     if not trimmed:         return False      # Handle fine-tuned models: ft:gpt-4.1:org:proj:suffix     without_ft_prefix = trimmed[3:] if trimmed.startswith("ft:") else trimmed     root = without_ft_prefix.split(":", 1)[0]      # Allow gpt-* and o* models     if root.startswith("gpt-"):         return True     if root.startswith("o") and root[1:2].isdigit():         return True      return False ``` |