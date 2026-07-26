---
url: https://openai.github.io/openai-agents-python/ref/memory/openai_conversations_session/
title: `OpenAI Conversations Session`
framework: openai
---

# `OpenAI Conversations Session`

### OpenAIConversationsSession

Bases: `SessionABC`

Source code in `src/agents/memory/openai_conversations_session.py`

|  |  |
| --- | --- |
| ```  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 ``` | ``` class OpenAIConversationsSession(SessionABC):     session_settings: SessionSettings | None = None      def __init__(         self,         *,         conversation_id: str | None = None,         openai_client: AsyncOpenAI | None = None,         session_settings: SessionSettings | None = None,     ):         self._session_id: str | None = conversation_id         self._session_id_lock = asyncio.Lock()         self.session_settings = session_settings or SessionSettings()         _openai_client = openai_client         if _openai_client is None:             _openai_client = get_default_openai_client() or AsyncOpenAI()         # this never be None here         self._openai_client: AsyncOpenAI = _openai_client      @property     def session_id(self) -> str:         """Get the session ID (conversation ID).          Returns:             The conversation ID for this session.          Raises:             ValueError: If the session has not been initialized yet.                 Call any session method (get_items, add_items, etc.) first                 to trigger lazy initialization.         """         if self._session_id is None:             raise ValueError(                 "Session ID not yet available. The session is lazily initialized "                 "on first API call. Call get_items(), add_items(), or similar first."             )         return self._session_id      @session_id.setter     def session_id(self, value: str) -> None:         """Set the session ID (conversation ID)."""         self._session_id = value      async def _get_session_id(self) -> str:         if self._session_id is None:             async with self._session_id_lock:                 if self._session_id is None:                     self._session_id = await start_openai_conversations_session(self._openai_client)         return self._session_id      async def _clear_session_id(self) -> None:         self._session_id = None      async def get_items(self, limit: int | None = None) -> list[TResponseInputItem]:         session_id = await self._get_session_id()          session_limit = resolve_session_limit(limit, self.session_settings)          all_items = []         if session_limit is None:             async for item in self._openai_client.conversations.items.list(                 conversation_id=session_id,                 order="asc",             ):                 # calling model_dump() to make this serializable                 all_items.append(item.model_dump(exclude_unset=True))         else:             async for item in self._openai_client.conversations.items.list(                 conversation_id=session_id,                 limit=session_limit,                 order="desc",             ):                 # calling model_dump() to make this serializable                 all_items.append(item.model_dump(exclude_unset=True))                 if session_limit is not None and len(all_items) >= session_limit:                     break             all_items.reverse()          return all_items  # type: ignore      async def add_items(self, items: list[TResponseInputItem]) -> None:         session_id = await self._get_session_id()         if not items:             return          await self._openai_client.conversations.items.create(             conversation_id=session_id,             items=items,         )      async def pop_item(self) -> TResponseInputItem | None:         session_id = await self._get_session_id()         items = await self.get_items(limit=1)         if not items:             return None         item_id: str = str(items[0]["id"])  # type: ignore [typeddict-item]         await self._openai_client.conversations.items.delete(             conversation_id=session_id, item_id=item_id         )         return items[0]      async def clear_session(self) -> None:         session_id = await self._get_session_id()         await self._openai_client.conversations.delete(             conversation_id=session_id,         )         await self._clear_session_id() ``` |

#### session\_id `property` `writable`

```
session_id: str
```

Get the session ID (conversation ID).

Returns:

| Type | Description |
| --- | --- |
| `str` | The conversation ID for this session. |

Raises:

| Type | Description |
| --- | --- |
| `ValueError` | If the session has not been initialized yet. Call any session method (get\_items, add\_items, etc.) first to trigger lazy initialization. |