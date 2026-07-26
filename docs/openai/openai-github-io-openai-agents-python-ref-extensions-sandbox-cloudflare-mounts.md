---
url: https://openai.github.io/openai-agents-python/ref/extensions/sandbox/cloudflare/mounts/
title: `Mounts`
framework: openai
---

# `Mounts`

### CloudflareBucketMountConfig `dataclass`

Backend-neutral config for Cloudflare bucket mounts.

Source code in `src/agents/extensions/sandbox/cloudflare/mounts.py`

|  |  |
| --- | --- |
| ``` 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 ``` | ``` @dataclass(frozen=True) class CloudflareBucketMountConfig:     """Backend-neutral config for Cloudflare bucket mounts."""      bucket_name: str     bucket_endpoint_url: str     provider: CloudflareBucketProvider     key_prefix: str | None = None     credentials: dict[str, str] | None = None     read_only: bool = True      def to_request_options(self) -> dict[str, object]:         options: dict[str, object] = {             "endpoint": self.bucket_endpoint_url,             "readOnly": self.read_only,         }         if self.key_prefix is not None:             options["prefix"] = self.key_prefix         if self.credentials is not None:             options["credentials"] = {                 "accessKeyId": self.credentials["access_key_id"],                 "secretAccessKey": self.credentials["secret_access_key"],             }         return options ``` |