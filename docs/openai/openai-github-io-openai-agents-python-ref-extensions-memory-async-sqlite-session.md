---
url: https://openai.github.io/openai-agents-python/ref/extensions/memory/async_sqlite_session/
title: `Async Sqlite Session`
framework: openai
---

# `Async Sqlite Session`

### AsyncSQLiteSession

Bases: `SessionABC`

Async SQLite-based implementation of session storage.

This implementation stores conversation history in a SQLite database.
By default, uses an in-memory database that is lost when the process ends.
For persistent storage, provide a file path.

Source code in `src/agents/extensions/memory/async_sqlite_session.py`

|  |  |
| --- | --- |
| ```  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 ``` | ``` class AsyncSQLiteSession(SessionABC):     """Async SQLite-based implementation of session storage.      This implementation stores conversation history in a SQLite database.     By default, uses an in-memory database that is lost when the process ends.     For persistent storage, provide a file path.     """      session_settings: SessionSettings | None = None      def __init__(         self,         session_id: str,         db_path: str | Path = ":memory:",         sessions_table: str = "agent_sessions",         messages_table: str = "agent_messages",         session_settings: SessionSettings | None = None,     ):         """Initialize the async SQLite session.          Args:             session_id: Unique identifier for the conversation session             db_path: Path to the SQLite database file. Defaults to ':memory:' (in-memory database)             sessions_table: Name of the table to store session metadata. Defaults to                 'agent_sessions'             messages_table: Name of the table to store message data. Defaults to 'agent_messages'             session_settings: Session configuration settings including default limit for                 retrieving items. If None, uses default SessionSettings().         """         self.session_id = session_id         self.session_settings = session_settings or SessionSettings()         self.db_path = db_path         self.sessions_table = sessions_table         self.messages_table = messages_table         self._connection: aiosqlite.Connection | None = None         self._lock = asyncio.Lock()         self._init_lock = asyncio.Lock()      async def _init_db_for_connection(self, conn: aiosqlite.Connection) -> None:         """Initialize the database schema for a specific connection."""         await conn.execute(             f"""             CREATE TABLE IF NOT EXISTS {self.sessions_table} (                 session_id TEXT PRIMARY KEY,                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                 updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP             )         """         )          await conn.execute(             f"""             CREATE TABLE IF NOT EXISTS {self.messages_table} (                 id INTEGER PRIMARY KEY AUTOINCREMENT,                 session_id TEXT NOT NULL,                 message_data TEXT NOT NULL,                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                 FOREIGN KEY (session_id) REFERENCES {self.sessions_table} (session_id)                     ON DELETE CASCADE             )         """         )          await conn.execute(             f"""             CREATE INDEX IF NOT EXISTS idx_{self.messages_table}_session_id             ON {self.messages_table} (session_id, id)         """         )          await conn.commit()      async def _get_connection(self) -> aiosqlite.Connection:         """Get or create a database connection."""         if self._connection is not None:             return self._connection          async with self._init_lock:             if self._connection is None:                 self._connection = await aiosqlite.connect(str(self.db_path))                 await self._connection.execute("PRAGMA journal_mode=WAL")                 await self._init_db_for_connection(self._connection)          return self._connection      @asynccontextmanager     async def _locked_connection(self) -> AsyncIterator[aiosqlite.Connection]:         """Provide a connection under the session lock."""         async with self._lock:             conn = await self._get_connection()             yield conn      async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         """Retrieve the conversation history for this session.          Args:             limit: Maximum number of items to retrieve. If None, uses session_settings.limit.                    When specified, returns the latest N items in chronological order.          Returns:             List of input items representing the conversation history         """          session_limit = resolve_session_limit(limit, self.session_settings)          async with self._locked_connection() as conn:             if session_limit is None:                 cursor = await conn.execute(                     f"""                     SELECT message_data FROM {self.messages_table}                     WHERE session_id = ?                     ORDER BY id ASC                 """,                     (self.session_id,),                 )             else:                 cursor = await conn.execute(                     f"""                     SELECT message_data FROM {self.messages_table}                     WHERE session_id = ?                     ORDER BY id DESC                     LIMIT ?                     """,                     (self.session_id, session_limit),                 )              rows = list(await cursor.fetchall())             await cursor.close()          if session_limit is not None:             rows = rows[::-1]          items: list[TResponseInputItem] = []         for (message_data,) in rows:             try:                 item = json.loads(message_data)                 items.append(item)             except json.JSONDecodeError:                 continue          return items      async def add_items(self, items: list[TResponseInputItem]) -> None:         """Add new items to the conversation history.          Args:             items: List of input items to add to the history         """         if not items:             return          async with self._locked_connection() as conn:             await conn.execute(                 f"""                 INSERT OR IGNORE INTO {self.sessions_table} (session_id) VALUES (?)             """,                 (self.session_id,),             )              message_data = [(self.session_id, json.dumps(item)) for item in items]             await conn.executemany(                 f"""                 INSERT INTO {self.messages_table} (session_id, message_data) VALUES (?, ?)             """,                 message_data,             )              await conn.execute(                 f"""                 UPDATE {self.sessions_table}                 SET updated_at = CURRENT_TIMESTAMP                 WHERE session_id = ?             """,                 (self.session_id,),             )              await conn.commit()      async def pop_item(self) -> TResponseInputItem | None:         """Remove and return the most recent item from the session.          Returns:             The most recent item if it exists, None if the session is empty         """         async with self._locked_connection() as conn:             cursor = await conn.execute(                 f"""                 DELETE FROM {self.messages_table}                 WHERE id = (                     SELECT id FROM {self.messages_table}                     WHERE session_id = ?                     ORDER BY id DESC                     LIMIT 1                 )                 RETURNING message_data                 """,                 (self.session_id,),             )              result = await cursor.fetchone()             await cursor.close()             await conn.commit()              while result:                 message_data = result[0]                 try:                     return cast(TResponseInputItem, json.loads(message_data))                 except (json.JSONDecodeError, TypeError):                     cursor = await conn.execute(                         f"""                         DELETE FROM {self.messages_table}                         WHERE id = (                             SELECT id FROM {self.messages_table}                             WHERE session_id = ?                             ORDER BY id DESC                             LIMIT 1                         )                         RETURNING message_data                         """,                         (self.session_id,),                     )                     result = await cursor.fetchone()                     await cursor.close()                     await conn.commit()          return None      async def clear_session(self) -> None:         """Clear all items for this session."""         async with self._locked_connection() as conn:             await conn.execute(                 f"DELETE FROM {self.messages_table} WHERE session_id = ?",                 (self.session_id,),             )             await conn.execute(                 f"DELETE FROM {self.sessions_table} WHERE session_id = ?",                 (self.session_id,),             )             await conn.commit()      async def close(self) -> None:         """Close the database connection."""         if self._connection is None:             return         async with self._lock:             await self._connection.close()             self._connection = None ``` |

#### \_\_init\_\_

```
__init__(
    session_id: str,
    db_path: str | Path = ":memory:",
    sessions_table: str = "agent_sessions",
    messages_table: str = "agent_messages",
    session_settings: SessionSettings | None = None,
)
```

Initialize the async SQLite session.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Unique identifier for the conversation session | *required* |
| `db_path` | `str | Path` | Path to the SQLite database file. Defaults to ':memory:' (in-memory database) | `':memory:'` |
| `sessions_table` | `str` | Name of the table to store session metadata. Defaults to 'agent\_sessions' | `'agent_sessions'` |
| `messages_table` | `str` | Name of the table to store message data. Defaults to 'agent\_messages' | `'agent_messages'` |
| `session_settings` | `SessionSettings | None` | Session configuration settings including default limit for retrieving items. If None, uses default SessionSettings(). | `None` |

Source code in `src/agents/extensions/memory/async_sqlite_session.py`

|  |  |
| --- | --- |
| ``` 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 ``` | ``` def __init__(     self,     session_id: str,     db_path: str | Path = ":memory:",     sessions_table: str = "agent_sessions",     messages_table: str = "agent_messages",     session_settings: SessionSettings | None = None, ):     """Initialize the async SQLite session.      Args:         session_id: Unique identifier for the conversation session         db_path: Path to the SQLite database file. Defaults to ':memory:' (in-memory database)         sessions_table: Name of the table to store session metadata. Defaults to             'agent_sessions'         messages_table: Name of the table to store message data. Defaults to 'agent_messages'         session_settings: Session configuration settings including default limit for             retrieving items. If None, uses default SessionSettings().     """     self.session_id = session_id     self.session_settings = session_settings or SessionSettings()     self.db_path = db_path     self.sessions_table = sessions_table     self.messages_table = messages_table     self._connection: aiosqlite.Connection | None = None     self._lock = asyncio.Lock()     self._init_lock = asyncio.Lock() ``` |

#### get\_items `async`

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

Source code in `src/agents/extensions/memory/async_sqlite_session.py`

|  |  |
| --- | --- |
| ``` 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 ``` | ``` async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:     """Retrieve the conversation history for this session.      Args:         limit: Maximum number of items to retrieve. If None, uses session_settings.limit.                When specified, returns the latest N items in chronological order.      Returns:         List of input items representing the conversation history     """      session_limit = resolve_session_limit(limit, self.session_settings)      async with self._locked_connection() as conn:         if session_limit is None:             cursor = await conn.execute(                 f"""                 SELECT message_data FROM {self.messages_table}                 WHERE session_id = ?                 ORDER BY id ASC             """,                 (self.session_id,),             )         else:             cursor = await conn.execute(                 f"""                 SELECT message_data FROM {self.messages_table}                 WHERE session_id = ?                 ORDER BY id DESC                 LIMIT ?                 """,                 (self.session_id, session_limit),             )          rows = list(await cursor.fetchall())         await cursor.close()      if session_limit is not None:         rows = rows[::-1]      items: list[TResponseInputItem] = []     for (message_data,) in rows:         try:             item = json.loads(message_data)             items.append(item)         except json.JSONDecodeError:             continue      return items ``` |

#### add\_items `async`

```
add_items(items: list[TResponseInputItem]) -> None
```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | *required* |

Source code in `src/agents/extensions/memory/async_sqlite_session.py`

|  |  |
| --- | --- |
| ``` 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 ``` | ``` async def add_items(self, items: list[TResponseInputItem]) -> None:     """Add new items to the conversation history.      Args:         items: List of input items to add to the history     """     if not items:         return      async with self._locked_connection() as conn:         await conn.execute(             f"""             INSERT OR IGNORE INTO {self.sessions_table} (session_id) VALUES (?)         """,             (self.session_id,),         )          message_data = [(self.session_id, json.dumps(item)) for item in items]         await conn.executemany(             f"""             INSERT INTO {self.messages_table} (session_id, message_data) VALUES (?, ?)         """,             message_data,         )          await conn.execute(             f"""             UPDATE {self.sessions_table}             SET updated_at = CURRENT_TIMESTAMP             WHERE session_id = ?         """,             (self.session_id,),         )          await conn.commit() ``` |

#### pop\_item `async`

```
pop_item() -> TResponseInputItem | None
```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/extensions/memory/async_sqlite_session.py`

|  |  |
| --- | --- |
| ``` 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 ``` | ``` async def pop_item(self) -> TResponseInputItem | None:     """Remove and return the most recent item from the session.      Returns:         The most recent item if it exists, None if the session is empty     """     async with self._locked_connection() as conn:         cursor = await conn.execute(             f"""             DELETE FROM {self.messages_table}             WHERE id = (                 SELECT id FROM {self.messages_table}                 WHERE session_id = ?                 ORDER BY id DESC                 LIMIT 1             )             RETURNING message_data             """,             (self.session_id,),         )          result = await cursor.fetchone()         await cursor.close()         await conn.commit()          while result:             message_data = result[0]             try:                 return cast(TResponseInputItem, json.loads(message_data))             except (json.JSONDecodeError, TypeError):                 cursor = await conn.execute(                     f"""                     DELETE FROM {self.messages_table}                     WHERE id = (                         SELECT id FROM {self.messages_table}                         WHERE session_id = ?                         ORDER BY id DESC                         LIMIT 1                     )                     RETURNING message_data                     """,                     (self.session_id,),                 )                 result = await cursor.fetchone()                 await cursor.close()                 await conn.commit()      return None ``` |

#### clear\_session `async`

```
clear_session() -> None
```

Clear all items for this session.

Source code in `src/agents/extensions/memory/async_sqlite_session.py`

|  |  |
| --- | --- |
| ``` 244 245 246 247 248 249 250 251 252 253 254 255 ``` | ``` async def clear_session(self) -> None:     """Clear all items for this session."""     async with self._locked_connection() as conn:         await conn.execute(             f"DELETE FROM {self.messages_table} WHERE session_id = ?",             (self.session_id,),         )         await conn.execute(             f"DELETE FROM {self.sessions_table} WHERE session_id = ?",             (self.session_id,),         )         await conn.commit() ``` |

#### close `async`

```
close() -> None
```

Close the database connection.

Source code in `src/agents/extensions/memory/async_sqlite_session.py`

|  |  |
| --- | --- |
| ``` 257 258 259 260 261 262 263 ``` | ``` async def close(self) -> None:     """Close the database connection."""     if self._connection is None:         return     async with self._lock:         await self._connection.close()         self._connection = None ``` |