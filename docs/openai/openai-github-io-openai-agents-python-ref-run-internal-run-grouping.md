---
url: https://openai.github.io/openai-agents-python/ref/run_internal/run_grouping/
title: `Run Grouping`
framework: openai
---

# `Run Grouping`

### resolve\_run\_grouping

```
resolve_run_grouping(
    *,
    conversation_id: str | None,
    session: Session | None,
    group_id: str | None,
) -> RunGrouping
```

Resolve the runner's stable grouping hierarchy.

The order matches prompt-cache grouping: server conversation, SDK session, trace group,
then a generated per-run value.

Source code in `src/agents/run_internal/run_grouping.py`

|  |  |
| --- | --- |
| ``` 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 ``` | ``` def resolve_run_grouping(     *,     conversation_id: str | None,     session: Session | None,     group_id: str | None, ) -> RunGrouping:     """Resolve the runner's stable grouping hierarchy.      The order matches prompt-cache grouping: server conversation, SDK session, trace group,     then a generated per-run value.     """      if conversation_id is not None and conversation_id.strip():         return "conversation", conversation_id.strip()      session_id = get_session_id_if_available(session)     if session_id is not None:         return "session", session_id      if group_id is not None and group_id.strip():         return "group", group_id.strip()      return "run", uuid4().hex ``` |