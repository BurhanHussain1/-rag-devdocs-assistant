---
url: https://openai.github.io/openai-agents-python/ref/extensions/sandbox/modal/mounts/
title: `Mounts`
framework: openai
---

# `Mounts`

### ModalCloudBucketMountConfig `dataclass`

Backend-neutral config for Modal's native cloud bucket mounts.

Source code in `src/agents/extensions/sandbox/modal/mounts.py`

|  |  |
| --- | --- |
| ``` 14 15 16 17 18 19 20 21 22 23 24 ``` | ``` @dataclass(frozen=True) class ModalCloudBucketMountConfig:     """Backend-neutral config for Modal's native cloud bucket mounts."""      bucket_name: str     bucket_endpoint_url: str | None = None     key_prefix: str | None = None     credentials: dict[str, str] | None = None     secret_name: str | None = None     secret_environment_name: str | None = None     read_only: bool = True ``` |