---
url: https://openai.github.io/openai-agents-python/ref/extensions/memory/encrypt_session/
title: `EncryptedSession`
framework: openai
---

# `EncryptedSession`

Bases: `SessionABC`

Encrypted wrapper for Session implementations with TTL-based expiration.

This class wraps any SessionABC implementation to provide transparent
encryption/decryption of stored items using Fernet encryption with
per-session key derivation and automatic expiration of old data.

When items expire (exceed TTL), they are silently skipped during retrieval.

Note: Expired tokens are rejected based on the system clock of the application server.
To avoid valid tokens being rejected due to clock drift, ensure all servers in
your environment are synchronized using NTP.

Source code in `src/agents/extensions/memory/encrypt_session.py`

|  |  |
| --- | --- |
| ```  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 ``` | ``` class EncryptedSession(SessionABC):     """Encrypted wrapper for Session implementations with TTL-based expiration.      This class wraps any SessionABC implementation to provide transparent     encryption/decryption of stored items using Fernet encryption with     per-session key derivation and automatic expiration of old data.      When items expire (exceed TTL), they are silently skipped during retrieval.      Note: Expired tokens are rejected based on the system clock of the application server.     To avoid valid tokens being rejected due to clock drift, ensure all servers in     your environment are synchronized using NTP.     """      def __init__(         self,         session_id: str,         underlying_session: SessionABC,         encryption_key: str,         ttl: int = 600,     ):         """         Args:             session_id: ID for this session             underlying_session: The real session store (e.g. SQLiteSession, SQLAlchemySession)             encryption_key: Master key (Fernet key or raw secret)             ttl: Token time-to-live in seconds (default 10 min)         """         self.session_id = session_id         self.underlying_session = underlying_session         self.ttl = ttl          master = _ensure_fernet_key_bytes(encryption_key)         self.cipher = _derive_session_fernet_key(master, session_id)         self._kid = "hkdf-v1"         self._ver = 1      def __getattr__(self, name):         return getattr(self.underlying_session, name)      @property     def session_settings(self) -> SessionSettings | None:         """Get session settings from the underlying session."""         return self.underlying_session.session_settings      @session_settings.setter     def session_settings(self, value: SessionSettings | None) -> None:         """Set session settings on the underlying session."""         self.underlying_session.session_settings = value      def _wrap(self, item: TResponseInputItem) -> EncryptedEnvelope:         if isinstance(item, dict):             payload = item         elif hasattr(item, "model_dump"):             payload = item.model_dump()         elif hasattr(item, "__dict__"):             payload = item.__dict__         else:             payload = dict(item)          token = self.cipher.encrypt(_to_json_bytes(payload)).decode("utf-8")         return {"__enc__": 1, "v": self._ver, "kid": self._kid, "payload": token}      def _unwrap(self, item: TResponseInputItem | EncryptedEnvelope) -> TResponseInputItem | None:         if not _is_encrypted_envelope(item):             return cast(TResponseInputItem, item)          try:             token = item["payload"].encode("utf-8")             plaintext = self.cipher.decrypt(token, ttl=self.ttl)             return cast(TResponseInputItem, _from_json_bytes(plaintext))         except (InvalidToken, KeyError):             return None      def _unwrap_valid_items(         self, encrypted_items: list[TResponseInputItem]     ) -> list[TResponseInputItem]:         valid_items: list[TResponseInputItem] = []         for enc in encrypted_items:             item = self._unwrap(enc)             if item is not None:                 valid_items.append(item)         return valid_items      async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         effective_limit = resolve_session_limit(limit, self.session_settings)         if effective_limit is not None and effective_limit > 0:             window = effective_limit             while True:                 encrypted_items = await self.underlying_session.get_items(window)                 valid_items = self._unwrap_valid_items(encrypted_items)                 if len(valid_items) >= effective_limit:                     return valid_items[-effective_limit:]                 if len(encrypted_items) < window:                     return valid_items                 window *= 2          encrypted_items = await self.underlying_session.get_items(limit)         return self._unwrap_valid_items(encrypted_items)      async def add_items(self, items: list[TResponseInputItem]) -> None:         wrapped: list[EncryptedEnvelope] = [self._wrap(it) for it in items]         await self.underlying_session.add_items(cast(list[TResponseInputItem], wrapped))      async def pop_item(self) -> TResponseInputItem | None:         while True:             enc = await self.underlying_session.pop_item()             if not enc:                 return None             item = self._unwrap(enc)             if item is not None:                 return item      async def clear_session(self) -> None:         await self.underlying_session.clear_session() ``` |

### session\_settings `property` `writable`

```
session_settings: SessionSettings | None
```

Get session settings from the underlying session.

### \_\_init\_\_

```
__init__(
    session_id: str,
    underlying_session: SessionABC,
    encryption_key: str,
    ttl: int = 600,
)
```

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `session_id` | `str` | ID for this session | *required* |
| `underlying_session` | `SessionABC` | The real session store (e.g. SQLiteSession, SQLAlchemySession) | *required* |
| `encryption_key` | `str` | Master key (Fernet key or raw secret) | *required* |
| `ttl` | `int` | Token time-to-live in seconds (default 10 min) | `600` |

Source code in `src/agents/extensions/memory/encrypt_session.py`

|  |  |
| --- | --- |
| ``` 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 ``` | ``` def __init__(     self,     session_id: str,     underlying_session: SessionABC,     encryption_key: str,     ttl: int = 600, ):     """     Args:         session_id: ID for this session         underlying_session: The real session store (e.g. SQLiteSession, SQLAlchemySession)         encryption_key: Master key (Fernet key or raw secret)         ttl: Token time-to-live in seconds (default 10 min)     """     self.session_id = session_id     self.underlying_session = underlying_session     self.ttl = ttl      master = _ensure_fernet_key_bytes(encryption_key)     self.cipher = _derive_session_fernet_key(master, session_id)     self._kid = "hkdf-v1"     self._ver = 1 ``` |