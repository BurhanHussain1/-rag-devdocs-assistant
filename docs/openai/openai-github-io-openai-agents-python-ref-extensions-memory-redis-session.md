---
url: https://openai.github.io/openai-agents-python/ref/extensions/memory/redis_session/
title: `RedisSession`
framework: openai
---

# `RedisSession`

Bases: `SessionABC`

Redis implementation of [`Session`](../../../memory/session/#agents.memory.session.Session "Session").

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ```  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 ``` | ``` class RedisSession(SessionABC):     """Redis implementation of [`Session`][agents.memory.session.Session]."""      session_settings: SessionSettings | None = None      def __init__(         self,         session_id: str,         *,         redis_client: Redis,         key_prefix: str = "agents:session",         ttl: int | None = None,         session_settings: SessionSettings | None = None,     ):         """Initializes a new RedisSession.          Args:             session_id (str): Unique identifier for the conversation.             redis_client (Redis[bytes]): A pre-configured Redis async client.             key_prefix (str, optional): Prefix for Redis keys to avoid collisions.                 Defaults to "agents:session".             ttl (int | None, optional): Time-to-live in seconds for session data.                 If None, data persists indefinitely. Defaults to None.             session_settings (SessionSettings | None): Session configuration settings including                 default limit for retrieving items. If None, uses default SessionSettings().         """         self.session_id = session_id         self.session_settings = session_settings or SessionSettings()         self._redis = redis_client         self._key_prefix = key_prefix         self._ttl = ttl         self._lock = asyncio.Lock()         self._owns_client = False  # Track if we own the Redis client          # Redis key patterns         self._session_key = f"{self._key_prefix}:{self.session_id}"         self._messages_key = f"{self._session_key}:messages"         self._counter_key = f"{self._session_key}:counter"      @classmethod     def from_url(         cls,         session_id: str,         *,         url: str,         redis_kwargs: dict[str, Any] | None = None,         session_settings: SessionSettings | None = None,         **kwargs: Any,     ) -> RedisSession:         """Create a session from a Redis URL string.          Args:             session_id (str): Conversation ID.             url (str): Redis URL, e.g. "redis://localhost:6379/0" or "rediss://host:6380".             redis_kwargs (dict[str, Any] | None): Additional keyword arguments forwarded to                 redis.asyncio.from_url.             session_settings (SessionSettings | None): Session configuration settings including                 default limit for retrieving items. If None, uses default SessionSettings().             **kwargs: Additional keyword arguments forwarded to the main constructor                 (e.g., key_prefix, ttl, etc.).          Returns:             RedisSession: An instance of RedisSession connected to the specified Redis server.         """         redis_kwargs = redis_kwargs or {}          redis_client = redis.from_url(url, **redis_kwargs)         session = cls(             session_id,             redis_client=redis_client,             session_settings=session_settings,             **kwargs,         )         session._owns_client = True  # We created the client, so we own it         return session      async def _serialize_item(self, item: TResponseInputItem) -> str:         """Serialize an item to JSON string. Can be overridden by subclasses."""         return json.dumps(item, separators=(",", ":"))      async def _deserialize_item(self, item: str) -> TResponseInputItem:         """Deserialize a JSON string to an item. Can be overridden by subclasses."""         return json.loads(item)  # type: ignore[no-any-return]  # json.loads returns Any but we know the structure      async def _get_next_id(self) -> int:         """Get the next message ID using Redis INCR for atomic increment."""         result = await self._redis.incr(self._counter_key)         return int(result)      async def _set_ttl_if_configured(self, *keys: str) -> None:         """Set TTL on keys if configured."""         if self._ttl is not None:             pipe = self._redis.pipeline()             for key in keys:                 pipe.expire(key, self._ttl)             await pipe.execute()      # ------------------------------------------------------------------     # Session protocol implementation     # ------------------------------------------------------------------      async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         """Retrieve the conversation history for this session.          Args:             limit: Maximum number of items to retrieve. If None, uses session_settings.limit.                    When specified, returns the latest N items in chronological order.          Returns:             List of input items representing the conversation history         """         session_limit = resolve_session_limit(limit, self.session_settings)          async with self._lock:             if session_limit is None:                 # Get all messages in chronological order                 raw_messages = await self._redis.lrange(self._messages_key, 0, -1)  # type: ignore[misc]  # Redis library returns Union[Awaitable[T], T] in async context             else:                 if session_limit <= 0:                     return []                 # Get the latest N messages (Redis list is ordered chronologically)                 # Use negative indices to get from the end - Redis uses -N to -1 for last N items                 raw_messages = await self._redis.lrange(self._messages_key, -session_limit, -1)  # type: ignore[misc]  # Redis library returns Union[Awaitable[T], T] in async context              items: list[TResponseInputItem] = []             for raw_msg in raw_messages:                 try:                     # Handle both bytes (default) and str (decode_responses=True) Redis clients                     if isinstance(raw_msg, bytes):                         msg_str = raw_msg.decode("utf-8")                     else:                         msg_str = raw_msg  # Already a string                     item = await self._deserialize_item(msg_str)                     items.append(item)                 except (json.JSONDecodeError, UnicodeDecodeError):                     # Skip corrupted messages                     continue              return items      async def add_items(self, items: list[TResponseInputItem]) -> None:         """Add new items to the conversation history.          Args:             items: List of input items to add to the history         """         if not items:             return          async with self._lock:             pipe = self._redis.pipeline()             now = str(int(time.time()))              # Set session metadata, preserving created_at across subsequent writes.             pipe.hset(self._session_key, "session_id", self.session_id)             pipe.hsetnx(self._session_key, "created_at", now)              # Add all items to the messages list             serialized_items = []             for item in items:                 serialized = await self._serialize_item(item)                 serialized_items.append(serialized)              if serialized_items:                 pipe.rpush(self._messages_key, *serialized_items)              # Update the session timestamp             pipe.hset(self._session_key, "updated_at", now)              # Execute all commands             await pipe.execute()              # Set TTL if configured             await self._set_ttl_if_configured(                 self._session_key, self._messages_key, self._counter_key             )      async def pop_item(self) -> TResponseInputItem | None:         """Remove and return the most recent item from the session.          Returns:             The most recent item if it exists, None if the session is empty         """         async with self._lock:             while True:                 # Use RPOP to atomically remove and return the rightmost (most recent) item                 raw_msg = await self._redis.rpop(self._messages_key)  # type: ignore[misc]  # Redis library returns Union[Awaitable[T], T] in async context                  if raw_msg is None:                     return None                  try:                     # Handle both bytes (default) and str (decode_responses=True) Redis clients                     if isinstance(raw_msg, bytes):                         msg_str = raw_msg.decode("utf-8")                     else:                         msg_str = raw_msg  # Already a string                     return await self._deserialize_item(msg_str)                 except (json.JSONDecodeError, UnicodeDecodeError):                     # Drop corrupted messages and keep looking for a valid item.                     continue      async def clear_session(self) -> None:         """Clear all items for this session."""         async with self._lock:             # Delete all keys associated with this session             await self._redis.delete(                 self._session_key,                 self._messages_key,                 self._counter_key,             )      async def close(self) -> None:         """Close the Redis connection.          Only closes the connection if this session owns the Redis client         (i.e., created via from_url). If the client was injected externally,         the caller is responsible for managing its lifecycle.         """         if self._owns_client:             await self._redis.aclose()      async def ping(self) -> bool:         """Test Redis connectivity.          Returns:             True if Redis is reachable, False otherwise.         """         try:             await self._redis.ping()  # type: ignore[misc]  # Redis library returns Union[Awaitable[T], T] in async context             return True         except Exception:             return False ``` |

### \_\_init\_\_

```
__init__(
    session_id: str,
    *,
    redis_client: Redis,
    key_prefix: str = "agents:session",
    ttl: int | None = None,
    session_settings: SessionSettings | None = None,
)
```

Initializes a new RedisSession.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Unique identifier for the conversation. | *required* |
| `redis_client` | `Redis[bytes]` | A pre-configured Redis async client. | *required* |
| `key_prefix` | `str` | Prefix for Redis keys to avoid collisions. Defaults to "agents:session". | `'agents:session'` |
| `ttl` | `int | None` | Time-to-live in seconds for session data. If None, data persists indefinitely. Defaults to None. | `None` |
| `session_settings` | `SessionSettings | None` | Session configuration settings including default limit for retrieving items. If None, uses default SessionSettings(). | `None` |

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ``` 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 ``` | ``` def __init__(     self,     session_id: str,     *,     redis_client: Redis,     key_prefix: str = "agents:session",     ttl: int | None = None,     session_settings: SessionSettings | None = None, ):     """Initializes a new RedisSession.      Args:         session_id (str): Unique identifier for the conversation.         redis_client (Redis[bytes]): A pre-configured Redis async client.         key_prefix (str, optional): Prefix for Redis keys to avoid collisions.             Defaults to "agents:session".         ttl (int | None, optional): Time-to-live in seconds for session data.             If None, data persists indefinitely. Defaults to None.         session_settings (SessionSettings | None): Session configuration settings including             default limit for retrieving items. If None, uses default SessionSettings().     """     self.session_id = session_id     self.session_settings = session_settings or SessionSettings()     self._redis = redis_client     self._key_prefix = key_prefix     self._ttl = ttl     self._lock = asyncio.Lock()     self._owns_client = False  # Track if we own the Redis client      # Redis key patterns     self._session_key = f"{self._key_prefix}:{self.session_id}"     self._messages_key = f"{self._session_key}:messages"     self._counter_key = f"{self._session_key}:counter" ``` |

### from\_url `classmethod`

```
from_url(
    session_id: str,
    *,
    url: str,
    redis_kwargs: dict[str, Any] | None = None,
    session_settings: SessionSettings | None = None,
    **kwargs: Any,
) -> RedisSession
```

Create a session from a Redis URL string.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | Conversation ID. | *required* |
| `url` | `str` | Redis URL, e.g. "redis://localhost:6379/0" or "rediss://host:6380". | *required* |
| `redis_kwargs` | `dict[str, Any] | None` | Additional keyword arguments forwarded to redis.asyncio.from\_url. | `None` |
| `session_settings` | `SessionSettings | None` | Session configuration settings including default limit for retrieving items. If None, uses default SessionSettings(). | `None` |
| `**kwargs` | `Any` | Additional keyword arguments forwarded to the main constructor (e.g., key\_prefix, ttl, etc.). | `{}` |

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `RedisSession` | `RedisSession` | An instance of RedisSession connected to the specified Redis server. |

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ```  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 ``` | ``` @classmethod def from_url(     cls,     session_id: str,     *,     url: str,     redis_kwargs: dict[str, Any] | None = None,     session_settings: SessionSettings | None = None,     **kwargs: Any, ) -> RedisSession:     """Create a session from a Redis URL string.      Args:         session_id (str): Conversation ID.         url (str): Redis URL, e.g. "redis://localhost:6379/0" or "rediss://host:6380".         redis_kwargs (dict[str, Any] | None): Additional keyword arguments forwarded to             redis.asyncio.from_url.         session_settings (SessionSettings | None): Session configuration settings including             default limit for retrieving items. If None, uses default SessionSettings().         **kwargs: Additional keyword arguments forwarded to the main constructor             (e.g., key_prefix, ttl, etc.).      Returns:         RedisSession: An instance of RedisSession connected to the specified Redis server.     """     redis_kwargs = redis_kwargs or {}      redis_client = redis.from_url(url, **redis_kwargs)     session = cls(         session_id,         redis_client=redis_client,         session_settings=session_settings,         **kwargs,     )     session._owns_client = True  # We created the client, so we own it     return session ``` |

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

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ``` 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 ``` | ``` async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:     """Retrieve the conversation history for this session.      Args:         limit: Maximum number of items to retrieve. If None, uses session_settings.limit.                When specified, returns the latest N items in chronological order.      Returns:         List of input items representing the conversation history     """     session_limit = resolve_session_limit(limit, self.session_settings)      async with self._lock:         if session_limit is None:             # Get all messages in chronological order             raw_messages = await self._redis.lrange(self._messages_key, 0, -1)  # type: ignore[misc]  # Redis library returns Union[Awaitable[T], T] in async context         else:             if session_limit <= 0:                 return []             # Get the latest N messages (Redis list is ordered chronologically)             # Use negative indices to get from the end - Redis uses -N to -1 for last N items             raw_messages = await self._redis.lrange(self._messages_key, -session_limit, -1)  # type: ignore[misc]  # Redis library returns Union[Awaitable[T], T] in async context          items: list[TResponseInputItem] = []         for raw_msg in raw_messages:             try:                 # Handle both bytes (default) and str (decode_responses=True) Redis clients                 if isinstance(raw_msg, bytes):                     msg_str = raw_msg.decode("utf-8")                 else:                     msg_str = raw_msg  # Already a string                 item = await self._deserialize_item(msg_str)                 items.append(item)             except (json.JSONDecodeError, UnicodeDecodeError):                 # Skip corrupted messages                 continue          return items ``` |

### add\_items `async`

```
add_items(items: list[TResponseInputItem]) -> None
```

Add new items to the conversation history.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `items` | `list[TResponseInputItem]` | List of input items to add to the history | *required* |

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ``` 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 ``` | ``` async def add_items(self, items: list[TResponseInputItem]) -> None:     """Add new items to the conversation history.      Args:         items: List of input items to add to the history     """     if not items:         return      async with self._lock:         pipe = self._redis.pipeline()         now = str(int(time.time()))          # Set session metadata, preserving created_at across subsequent writes.         pipe.hset(self._session_key, "session_id", self.session_id)         pipe.hsetnx(self._session_key, "created_at", now)          # Add all items to the messages list         serialized_items = []         for item in items:             serialized = await self._serialize_item(item)             serialized_items.append(serialized)          if serialized_items:             pipe.rpush(self._messages_key, *serialized_items)          # Update the session timestamp         pipe.hset(self._session_key, "updated_at", now)          # Execute all commands         await pipe.execute()          # Set TTL if configured         await self._set_ttl_if_configured(             self._session_key, self._messages_key, self._counter_key         ) ``` |

### pop\_item `async`

```
pop_item() -> TResponseInputItem | None
```

Remove and return the most recent item from the session.

Returns:

| Type | Description |
| --- | --- |
| `TResponseInputItem | None` | The most recent item if it exists, None if the session is empty |

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ``` 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 ``` | ``` async def pop_item(self) -> TResponseInputItem | None:     """Remove and return the most recent item from the session.      Returns:         The most recent item if it exists, None if the session is empty     """     async with self._lock:         while True:             # Use RPOP to atomically remove and return the rightmost (most recent) item             raw_msg = await self._redis.rpop(self._messages_key)  # type: ignore[misc]  # Redis library returns Union[Awaitable[T], T] in async context              if raw_msg is None:                 return None              try:                 # Handle both bytes (default) and str (decode_responses=True) Redis clients                 if isinstance(raw_msg, bytes):                     msg_str = raw_msg.decode("utf-8")                 else:                     msg_str = raw_msg  # Already a string                 return await self._deserialize_item(msg_str)             except (json.JSONDecodeError, UnicodeDecodeError):                 # Drop corrupted messages and keep looking for a valid item.                 continue ``` |

### clear\_session `async`

```
clear_session() -> None
```

Clear all items for this session.

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ``` 249 250 251 252 253 254 255 256 257 ``` | ``` async def clear_session(self) -> None:     """Clear all items for this session."""     async with self._lock:         # Delete all keys associated with this session         await self._redis.delete(             self._session_key,             self._messages_key,             self._counter_key,         ) ``` |

### close `async`

```
close() -> None
```

Close the Redis connection.

Only closes the connection if this session owns the Redis client
(i.e., created via from\_url). If the client was injected externally,
the caller is responsible for managing its lifecycle.

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ``` 259 260 261 262 263 264 265 266 267 ``` | ``` async def close(self) -> None:     """Close the Redis connection.      Only closes the connection if this session owns the Redis client     (i.e., created via from_url). If the client was injected externally,     the caller is responsible for managing its lifecycle.     """     if self._owns_client:         await self._redis.aclose() ``` |

### ping `async`

```
ping() -> bool
```

Test Redis connectivity.

Returns:

| Type | Description |
| --- | --- |
| `bool` | True if Redis is reachable, False otherwise. |

Source code in `src/agents/extensions/memory/redis_session.py`

|  |  |
| --- | --- |
| ``` 269 270 271 272 273 274 275 276 277 278 279 ``` | ``` async def ping(self) -> bool:     """Test Redis connectivity.      Returns:         True if Redis is reachable, False otherwise.     """     try:         await self._redis.ping()  # type: ignore[misc]  # Redis library returns Union[Awaitable[T], T] in async context         return True     except Exception:         return False ``` |