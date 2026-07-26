---
url: https://openai.github.io/openai-agents-python/ref/extensions/memory/sqlalchemy_session/
title: `SQLAlchemySession`
framework: openai
---

# `SQLAlchemySession`

Bases: `SessionABC`

SQLAlchemy implementation of [`Session`](../../../memory/session/#agents.memory.session.Session "Session").

Source code in `src/agents/extensions/memory/sqlalchemy_session.py`

|  |  |
| --- | --- |
| ```  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 ``` | ``` class SQLAlchemySession(SessionABC):     """SQLAlchemy implementation of [`Session`][agents.memory.session.Session]."""      _table_init_locks: ClassVar[dict[tuple[str, str, str], threading.Lock]] = {}     _table_init_locks_guard: ClassVar[threading.Lock] = threading.Lock()     _sqlite_configured_engines: ClassVar[set[int]] = set()     _sqlite_configured_engines_guard: ClassVar[threading.Lock] = threading.Lock()     _SQLITE_BUSY_TIMEOUT_MS: ClassVar[int] = 5000     _SQLITE_LOCK_RETRY_DELAYS: ClassVar[tuple[float, ...]] = (0.05, 0.1, 0.2, 0.4, 0.8)     _metadata: MetaData     _sessions: Table     _messages: Table     session_settings: SessionSettings | None = None      @classmethod     def _get_table_init_lock(         cls, engine: AsyncEngine, sessions_table: str, messages_table: str     ) -> threading.Lock:         lock_key = (             engine.url.render_as_string(hide_password=True),             sessions_table,             messages_table,         )         with cls._table_init_locks_guard:             lock = cls._table_init_locks.get(lock_key)             if lock is None:                 lock = threading.Lock()                 cls._table_init_locks[lock_key] = lock             return lock      @classmethod     def _configure_sqlite_engine(cls, engine: AsyncEngine) -> None:         """Apply SQLite settings that reduce transient lock failures."""         if engine.dialect.name != "sqlite":             return          engine_key = id(engine.sync_engine)         with cls._sqlite_configured_engines_guard:             if engine_key in cls._sqlite_configured_engines:                 return              @event.listens_for(engine.sync_engine, "connect")             def _configure_sqlite_connection(dbapi_connection: Any, _: Any) -> None:                 cursor = dbapi_connection.cursor()                 try:                     cursor.execute(f"PRAGMA busy_timeout = {cls._SQLITE_BUSY_TIMEOUT_MS}")                     cursor.execute("PRAGMA journal_mode = WAL")                 finally:                     cursor.close()              cls._sqlite_configured_engines.add(engine_key)      @staticmethod     def _is_sqlite_lock_error(exc: OperationalError) -> bool:         return "database is locked" in str(exc).lower()      async def _run_sqlite_write_with_retry(self, operation: Any) -> None:         """Retry transient SQLite write lock failures with bounded backoff."""         if self._engine.dialect.name != "sqlite":             await operation()             return          for attempt, delay in enumerate((0.0, *self._SQLITE_LOCK_RETRY_DELAYS)):             if delay:                 await asyncio.sleep(delay)             try:                 await operation()                 return             except OperationalError as exc:                 if not self._is_sqlite_lock_error(exc):                     raise                 if attempt == len(self._SQLITE_LOCK_RETRY_DELAYS):                     raise      def __init__(         self,         session_id: str,         *,         engine: AsyncEngine,         create_tables: bool = False,         sessions_table: str = "agent_sessions",         messages_table: str = "agent_messages",         session_settings: SessionSettings | None = None,         ensure_ascii: bool = True,     ):         """Initializes a new SQLAlchemySession.          Args:             session_id (str): Unique identifier for the conversation.             engine (AsyncEngine): A pre-configured SQLAlchemy async engine. The engine                 must be created with an async driver (e.g., 'postgresql+asyncpg://',                 'mysql+aiomysql://', or 'sqlite+aiosqlite://').             create_tables (bool, optional): Whether to automatically create the required                 tables and indexes. Defaults to False for production use. Set to True for                 development and testing when migrations aren't used.             sessions_table (str, optional): Override the default table name for sessions if needed.             messages_table (str, optional): Override the default table name for messages if needed.             session_settings (SessionSettings | None, optional): Session configuration settings             ensure_ascii (bool, optional): Whether to escape non-ASCII characters when serializing                 session items to JSON. Defaults to True to preserve the historical storage format.         """         self.session_id = session_id         self.session_settings = session_settings or SessionSettings()         self._engine = engine         self._ensure_ascii = ensure_ascii         self._configure_sqlite_engine(engine)         self._init_lock = (             self._get_table_init_lock(engine, sessions_table, messages_table)             if create_tables             else None         )          self._metadata = MetaData()         self._sessions = Table(             sessions_table,             self._metadata,             Column("session_id", String, primary_key=True),             Column(                 "created_at",                 TIMESTAMP(timezone=False),                 server_default=sql_text("CURRENT_TIMESTAMP"),                 nullable=False,             ),             Column(                 "updated_at",                 TIMESTAMP(timezone=False),                 server_default=sql_text("CURRENT_TIMESTAMP"),                 onupdate=sql_text("CURRENT_TIMESTAMP"),                 nullable=False,             ),         )          self._messages = Table(             messages_table,             self._metadata,             Column("id", Integer, primary_key=True, autoincrement=True),             Column(                 "session_id",                 String,                 ForeignKey(f"{sessions_table}.session_id", ondelete="CASCADE"),                 nullable=False,             ),             Column("message_data", Text, nullable=False),             Column(                 "created_at",                 TIMESTAMP(timezone=False),                 server_default=sql_text("CURRENT_TIMESTAMP"),                 nullable=False,             ),             Index(                 f"idx_{messages_table}_session_time",                 "session_id",                 "created_at",             ),             sqlite_autoincrement=True,         )          # Async session factory         self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)          self._create_tables = create_tables      # ---------------------------------------------------------------------     # Convenience constructors     # ---------------------------------------------------------------------     @classmethod     def from_url(         cls,         session_id: str,         *,         url: str,         engine_kwargs: dict[str, Any] | None = None,         session_settings: SessionSettings | None = None,         **kwargs: Any,     ) -> SQLAlchemySession:         """Create a session from a database URL string.          Args:             session_id (str): Conversation ID.             url (str): Any SQLAlchemy async URL, e.g. "postgresql+asyncpg://user:pass@host/db".             engine_kwargs (dict[str, Any] | None): Additional keyword arguments forwarded to                 sqlalchemy.ext.asyncio.create_async_engine.             session_settings (SessionSettings | None): Session configuration settings including                 default limit for retrieving items. If None, uses default SessionSettings().             **kwargs: Additional keyword arguments forwarded to the main constructor                 (e.g., create_tables, custom table names, etc.).          Returns:             SQLAlchemySession: An instance of SQLAlchemySession connected to the specified database.         """         engine_kwargs = engine_kwargs or {}         engine = create_async_engine(url, **engine_kwargs)         return cls(session_id, engine=engine, session_settings=session_settings, **kwargs)      async def _serialize_item(self, item: TResponseInputItem) -> str:         """Serialize an item to JSON string. Can be overridden by subclasses."""         return json.dumps(item, ensure_ascii=self._ensure_ascii, separators=(",", ":"))      async def _deserialize_item(self, item: str) -> TResponseInputItem:         """Deserialize a JSON string to an item. Can be overridden by subclasses."""         return json.loads(item)  # type: ignore[no-any-return]      # ------------------------------------------------------------------     # Session protocol implementation     # ------------------------------------------------------------------     async def _ensure_tables(self) -> None:         """Ensure tables are created before any database operations."""         if not self._create_tables:             return          assert self._init_lock is not None         while not self._init_lock.acquire(blocking=False):  # noqa: ASYNC110             # Poll without handing lock acquisition to a background thread so             # cancellation cannot strand the shared init lock in the acquired state.             await asyncio.sleep(0.01)         try:             if not self._create_tables:                 return              async with self._engine.begin() as conn:                 await conn.run_sync(self._metadata.create_all)             self._create_tables = False  # Only create once         finally:             self._init_lock.release()      async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         """Retrieve the conversation history for this session.          Args:             limit: Maximum number of items to retrieve. If None, uses session_settings.limit.                    When specified, returns the latest N items in chronological order.          Returns:             List of input items representing the conversation history         """         await self._ensure_tables()          session_limit = resolve_session_limit(limit, self.session_settings)          async with self._session_factory() as sess:             if session_limit is None:                 stmt = (                     select(self._messages.c.message_data)                     .where(self._messages.c.session_id == self.session_id)                     .order_by(                         self._messages.c.created_at.asc(),                         self._messages.c.id.asc(),                     )                 )             else:                 stmt = (                     select(self._messages.c.message_data)                     .where(self._messages.c.session_id == self.session_id)                     # Use DESC + LIMIT to get the latest N                     # then reverse later for chronological order.                     .order_by(                         self._messages.c.created_at.desc(),                         self._messages.c.id.desc(),                     )                     .limit(session_limit)                 )              result = await sess.execute(stmt)             rows: list[str] = [row[0] for row in result.all()]              if session_limit is not None:                 rows.reverse()              items: list[TResponseInputItem] = []             for raw in rows:                 try:                     items.append(await self._deserialize_item(raw))                 except json.JSONDecodeError:                     # Skip corrupted rows                     continue             return items      async def add_items(self, items: list[TResponseInputItem]) -> None:         """Add new items to the conversation history.          Args:             items: List of input items to add to the history         """         if not items:             return          await self._ensure_tables()         payload = [             {                 "session_id": self.session_id,                 "message_data": await self._serialize_item(item),             }             for item in items         ]          async def _write_items() -> None:             async with self._session_factory() as sess:                 async with sess.begin():                     # Avoid check-then-insert races on the first write while keeping                     # the common path free of avoidable integrity exceptions.                     existing = await sess.execute(                         select(self._sessions.c.session_id).where(                             self._sessions.c.session_id == self.session_id                         )                     )                     if not existing.scalar_one_or_none():                         try:                             async with sess.begin_nested():                                 await sess.execute(                                     insert(self._sessions).values({"session_id": self.session_id})                                 )                         except IntegrityError:                             # Another concurrent writer created the parent row first.                             pass                      # Insert messages in bulk                     await sess.execute(insert(self._messages), payload)                      # Touch updated_at column                     await sess.execute(                         update(self._sessions)                         .where(self._sessions.c.session_id == self.session_id)                         .values(updated_at=sql_text("CURRENT_TIMESTAMP"))                     )          await self._run_sqlite_write_with_retry(_write_items)      async def pop_item(self) -> TResponseInputItem | None:         """Remove and return the most recent item from the session.          Returns:             The most recent item if it exists, None if the session is empty         """         await self._ensure_tables()         async with self._session_factory() as sess:             async with sess.begin():                 while True:                     # Fallback for all dialects - get ID first, then delete                     subq = (                         select(self._messages.c.id)                         .where(self._messages.c.session_id == self.session_id)                         .order_by(                             self._messages.c.created_at.desc(),                             self._messages.c.id.desc(),                         )                         .limit(1)                     )                     res = await sess.execute(subq)                     row_id = res.scalar_one_or_none()                     if row_id is None:                         return None                     # Fetch data before deleting                     res_data = await sess.execute(                         select(self._messages.c.message_data).where(self._messages.c.id == row_id)                     )                     row = res_data.scalar_one_or_none()                     await sess.execute(delete(self._messages).where(self._messages.c.id == row_id))                      if row is None:                         continue                     try:                         return await self._deserialize_item(row)                     except (json.JSONDecodeError, TypeError):                         continue      async def clear_session(self) -> None:         """Clear all items for this session."""         await self._ensure_tables()         async with self._session_factory() as sess:             async with sess.begin():                 await sess.execute(                     delete(self._messages).where(self._messages.c.session_id == self.session_id)                 )                 await sess.execute(                     delete(self._sessions).where(self._sessions.c.session_id == self.session_id)                 )      @property     def engine(self) -> AsyncEngine:         """Access the underlying SQLAlchemy AsyncEngine.          This property provides direct access to the engine for advanced use cases,         such as checking connection pool status, configuring engine settings,         or manually disposing the engine when needed.          Returns:             AsyncEngine: The SQLAlchemy async engine instance.         """         return self._engine ``` |

### engine `property`

```
engine: AsyncEngine
```

Access the underlying SQLAlchemy AsyncEngine.

This property provides direct access to the engine for advanced use cases,
such as checking connection pool status, configuring engine settings,
or manually disposing the engine when needed.

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `AsyncEngine` | `AsyncEngine` | The SQLAlchemy async engine instance. |

### \_\_init\_\_

```
__init__(
    session_id: str,
    *,
    engine: AsyncEngine,
    create_tables: bool = False,
    sessions_table: str = "agent_sessions",
    messages_table: str = "agent_messages",
    session_settings: SessionSettings | None = None,
    ensure_ascii: bool = True,
)
```

Initializes a new SQLAlchemySession.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Unique identifier for the conversation. | *required* |
| `engine` | `AsyncEngine` | A pre-configured SQLAlchemy async engine. The engine must be created with an async driver (e.g., 'postgresql+asyncpg://', 'mysql+aiomysql://', or 'sqlite+aiosqlite://'). | *required* |
| `create_tables` | `bool` | Whether to automatically create the required tables and indexes. Defaults to False for production use. Set to True for development and testing when migrations aren't used. | `False` |
| `sessions_table` | `str` | Override the default table name for sessions if needed. | `'agent_sessions'` |
| `messages_table` | `str` | Override the default table name for messages if needed. | `'agent_messages'` |
| `session_settings` | `SessionSettings | None` | Session configuration settings | `None` |
| `ensure_ascii` | `bool` | Whether to escape non-ASCII characters when serializing session items to JSON. Defaults to True to preserve the historical storage format. | `True` |

Source code in `src/agents/extensions/memory/sqlalchemy_session.py`

|  |  |
| --- | --- |
| ``` 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 ``` | ``` def __init__(     self,     session_id: str,     *,     engine: AsyncEngine,     create_tables: bool = False,     sessions_table: str = "agent_sessions",     messages_table: str = "agent_messages",     session_settings: SessionSettings | None = None,     ensure_ascii: bool = True, ):     """Initializes a new SQLAlchemySession.      Args:         session_id (str): Unique identifier for the conversation.         engine (AsyncEngine): A pre-configured SQLAlchemy async engine. The engine             must be created with an async driver (e.g., 'postgresql+asyncpg://',             'mysql+aiomysql://', or 'sqlite+aiosqlite://').         create_tables (bool, optional): Whether to automatically create the required             tables and indexes. Defaults to False for production use. Set to True for             development and testing when migrations aren't used.         sessions_table (str, optional): Override the default table name for sessions if needed.         messages_table (str, optional): Override the default table name for messages if needed.         session_settings (SessionSettings | None, optional): Session configuration settings         ensure_ascii (bool, optional): Whether to escape non-ASCII characters when serializing             session items to JSON. Defaults to True to preserve the historical storage format.     """     self.session_id = session_id     self.session_settings = session_settings or SessionSettings()     self._engine = engine     self._ensure_ascii = ensure_ascii     self._configure_sqlite_engine(engine)     self._init_lock = (         self._get_table_init_lock(engine, sessions_table, messages_table)         if create_tables         else None     )      self._metadata = MetaData()     self._sessions = Table(         sessions_table,         self._metadata,         Column("session_id", String, primary_key=True),         Column(             "created_at",             TIMESTAMP(timezone=False),             server_default=sql_text("CURRENT_TIMESTAMP"),             nullable=False,         ),         Column(             "updated_at",             TIMESTAMP(timezone=False),             server_default=sql_text("CURRENT_TIMESTAMP"),             onupdate=sql_text("CURRENT_TIMESTAMP"),             nullable=False,         ),     )      self._messages = Table(         messages_table,         self._metadata,         Column("id", Integer, primary_key=True, autoincrement=True),         Column(             "session_id",             String,             ForeignKey(f"{sessions_table}.session_id", ondelete="CASCADE"),             nullable=False,         ),         Column("message_data", Text, nullable=False),         Column(             "created_at",             TIMESTAMP(timezone=False),             server_default=sql_text("CURRENT_TIMESTAMP"),             nullable=False,         ),         Index(             f"idx_{messages_table}_session_time",             "session_id",             "created_at",         ),         sqlite_autoincrement=True,     )      # Async session factory     self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)      self._create_tables = create_tables ``` |

### from\_url `classmethod`

```
from_url(
    session_id: str,
    *,
    url: str,
    engine_kwargs: dict[str, Any] | None = None,
    session_settings: SessionSettings | None = None,
    **kwargs: Any,
) -> SQLAlchemySession
```

Create a session from a database URL string.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Conversation ID. | *required* |
| `url` | `str` | Any SQLAlchemy async URL, e.g. "postgresql+asyncpg://user:pass@host/db". | *required* |
| `engine_kwargs` | `dict[str, Any] | None` | Additional keyword arguments forwarded to sqlalchemy.ext.asyncio.create\_async\_engine. | `None` |
| `session_settings` | `SessionSettings | None` | Session configuration settings including default limit for retrieving items. If None, uses default SessionSettings(). | `None` |
| `**kwargs` | `Any` | Additional keyword arguments forwarded to the main constructor (e.g., create\_tables, custom table names, etc.). | `{}` |

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `SQLAlchemySession` | `SQLAlchemySession` | An instance of SQLAlchemySession connected to the specified database. |

Source code in `src/agents/extensions/memory/sqlalchemy_session.py`

|  |  |
| --- | --- |
| ``` 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 ``` | ``` @classmethod def from_url(     cls,     session_id: str,     *,     url: str,     engine_kwargs: dict[str, Any] | None = None,     session_settings: SessionSettings | None = None,     **kwargs: Any, ) -> SQLAlchemySession:     """Create a session from a database URL string.      Args:         session_id (str): Conversation ID.         url (str): Any SQLAlchemy async URL, e.g. "postgresql+asyncpg://user:pass@host/db".         engine_kwargs (dict[str, Any] | None): Additional keyword arguments forwarded to             sqlalchemy.ext.asyncio.create_async_engine.         session_settings (SessionSettings | None): Session configuration settings including             default limit for retrieving items. If None, uses default SessionSettings().         **kwargs: Additional keyword arguments forwarded to the main constructor             (e.g., create_tables, custom table names, etc.).      Returns:         SQLAlchemySession: An instance of SQLAlchemySession connected to the specified database.     """     engine_kwargs = engine_kwargs or {}     engine = create_async_engine(url, **engine_kwargs)     return cls(session_id, engine=engine, session_settings=session_settings, **kwargs) ``` |

### get\_items `async`

```
get_items(
    limit: int | None = None,
) -> list[TResponseInputItem]
```

Retrieve the conversation history for this session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `limit` | `int | None` | Maximum number of items to retrieve. If None, uses session\_settings.limit. When specified, returns the latest N items in chronological order. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `list[TResponseInputItem]` | List of input items representing the conversation history |

Source code in `src/agents/extensions/memory/sqlalchemy_session.py`

|  |  |
| --- | --- |
| ``` 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 ``` | ``` async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:     """Retrieve the conversation history for this session.      Args:         limit: Maximum number of items to retrieve. If None, uses session_settings.limit.                When specified, returns the latest N items in chronological order.      Returns:         List of input items representing the conversation history     """     await self._ensure_tables()      session_limit = resolve_session_limit(limit, self.session_settings)      async with self._session_factory() as sess:         if session_limit is None:             stmt = (                 select(self._messages.c.message_data)                 .where(self._messages.c.session_id == self.session_id)                 .order_by(                     self._messages.c.created_at.asc(),                     self._messages.c.id.asc(),                 )             )         else:             stmt = (                 select(self._messages.c.message_data)                 .where(self._messages.c.session_id == self.session_id)                 # Use DESC + LIMIT to get the latest N                 # then reverse later for chronological order.                 .order_by(                     self._messages.c.created_at.desc(),                     self._messages.c.id.desc(),                 )                 .limit(session_limit)             )          result = await sess.execute(stmt)         rows: list[str] = [row[0] for row in result.all()]          if session_limit is not None:             rows.reverse()          items: list[TResponseInputItem] = []         for raw in rows:             try:                 items.append(await self._deserialize_item(raw))             except json.JSONDecodeError:                 # Skip corrupted rows                 continue         return items ``` |

### add\_items `async`

```
add_items(items: list[TResponseInputItem]) -> None
```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | *required* |

Source code in `src/agents/extensions/memory/sqlalchemy_session.py`

|  |  |
| --- | --- |
| ``` 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 ``` | ``` async def add_items(self, items: list[TResponseInputItem]) -> None:     """Add new items to the conversation history.      Args:         items: List of input items to add to the history     """     if not items:         return      await self._ensure_tables()     payload = [         {             "session_id": self.session_id,             "message_data": await self._serialize_item(item),         }         for item in items     ]      async def _write_items() -> None:         async with self._session_factory() as sess:             async with sess.begin():                 # Avoid check-then-insert races on the first write while keeping                 # the common path free of avoidable integrity exceptions.                 existing = await sess.execute(                     select(self._sessions.c.session_id).where(                         self._sessions.c.session_id == self.session_id                     )                 )                 if not existing.scalar_one_or_none():                     try:                         async with sess.begin_nested():                             await sess.execute(                                 insert(self._sessions).values({"session_id": self.session_id})                             )                     except IntegrityError:                         # Another concurrent writer created the parent row first.                         pass                  # Insert messages in bulk                 await sess.execute(insert(self._messages), payload)                  # Touch updated_at column                 await sess.execute(                     update(self._sessions)                     .where(self._sessions.c.session_id == self.session_id)                     .values(updated_at=sql_text("CURRENT_TIMESTAMP"))                 )      await self._run_sqlite_write_with_retry(_write_items) ``` |

### pop\_item `async`

```
pop_item() -> TResponseInputItem | None
```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/extensions/memory/sqlalchemy_session.py`

|  |  |
| --- | --- |
| ``` 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 ``` | ``` async def pop_item(self) -> TResponseInputItem | None:     """Remove and return the most recent item from the session.      Returns:         The most recent item if it exists, None if the session is empty     """     await self._ensure_tables()     async with self._session_factory() as sess:         async with sess.begin():             while True:                 # Fallback for all dialects - get ID first, then delete                 subq = (                     select(self._messages.c.id)                     .where(self._messages.c.session_id == self.session_id)                     .order_by(                         self._messages.c.created_at.desc(),                         self._messages.c.id.desc(),                     )                     .limit(1)                 )                 res = await sess.execute(subq)                 row_id = res.scalar_one_or_none()                 if row_id is None:                     return None                 # Fetch data before deleting                 res_data = await sess.execute(                     select(self._messages.c.message_data).where(self._messages.c.id == row_id)                 )                 row = res_data.scalar_one_or_none()                 await sess.execute(delete(self._messages).where(self._messages.c.id == row_id))                  if row is None:                     continue                 try:                     return await self._deserialize_item(row)                 except (json.JSONDecodeError, TypeError):                     continue ``` |

### clear\_session `async`

```
clear_session() -> None
```

Clear all items for this session.

Source code in `src/agents/extensions/memory/sqlalchemy_session.py`

|  |  |
| --- | --- |
| ``` 421 422 423 424 425 426 427 428 429 430 431 ``` | ``` async def clear_session(self) -> None:     """Clear all items for this session."""     await self._ensure_tables()     async with self._session_factory() as sess:         async with sess.begin():             await sess.execute(                 delete(self._messages).where(self._messages.c.session_id == self.session_id)             )             await sess.execute(                 delete(self._sessions).where(self._sessions.c.session_id == self.session_id)             ) ``` |