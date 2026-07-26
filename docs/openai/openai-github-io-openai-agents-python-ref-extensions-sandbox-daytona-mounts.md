---
url: https://openai.github.io/openai-agents-python/ref/extensions/sandbox/daytona/mounts/
title: `Mounts`
framework: openai
---

# `Mounts`

Mount strategy for Daytona sandboxes.

Provides `DaytonaCloudBucketMountStrategy`, a wrapper around the generic
:class:`InContainerMountStrategy` that ensures `rclone` is installed inside
the sandbox before delegating to :class:`RcloneMountPattern`.

Supports S3, R2, GCS, Azure Blob, and Box mounts through a single code path.

### DaytonaCloudBucketMountStrategy

Bases: `MountStrategyBase`

Mount rclone-backed cloud storage in Daytona sandboxes.

Wraps :class:`InContainerMountStrategy` with automatic `rclone`
provisioning. Use with any rclone-backed provider mount (`S3Mount`,
`R2Mount`, `GCSMount`, `AzureBlobMount`, `BoxMount`) and let the
generic framework handle config generation and mount execution.

Usage::

```
from agents.extensions.sandbox.daytona import DaytonaCloudBucketMountStrategy
from agents.sandbox.entries import S3Mount

mount = S3Mount(
    bucket="my-bucket",
    access_key_id="...",
    secret_access_key="...",
    mount_path=Path("/mnt/bucket"),
    mount_strategy=DaytonaCloudBucketMountStrategy(),
)
```

Source code in `src/agents/extensions/sandbox/daytona/mounts.py`

|  |  |
| --- | --- |
| ``` 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 ``` | ``` class DaytonaCloudBucketMountStrategy(MountStrategyBase):     """Mount rclone-backed cloud storage in Daytona sandboxes.      Wraps :class:`InContainerMountStrategy` with automatic ``rclone``     provisioning.  Use with any rclone-backed provider mount (``S3Mount``,     ``R2Mount``, ``GCSMount``, ``AzureBlobMount``, ``BoxMount``) and let the     generic framework handle config generation and mount execution.      Usage::          from agents.extensions.sandbox.daytona import DaytonaCloudBucketMountStrategy         from agents.sandbox.entries import S3Mount          mount = S3Mount(             bucket="my-bucket",             access_key_id="...",             secret_access_key="...",             mount_path=Path("/mnt/bucket"),             mount_strategy=DaytonaCloudBucketMountStrategy(),         )     """      type: Literal["daytona_cloud_bucket"] = "daytona_cloud_bucket"     pattern: RcloneMountPattern = RcloneMountPattern(mode="fuse")      def _delegate(self) -> InContainerMountStrategy:         return InContainerMountStrategy(pattern=self.pattern)      def validate_mount(self, mount: Mount) -> None:         self._delegate().validate_mount(mount)      async def activate(         self,         mount: Mount,         session: BaseSandboxSession,         dest: Path,         base_dir: Path,     ) -> list[MaterializedFile]:         _assert_daytona_session(session)         if self.pattern.mode == "fuse":             await _ensure_fuse_support(session)         await _ensure_rclone(session)         return await self._delegate().activate(mount, session, dest, base_dir)      async def deactivate(         self,         mount: Mount,         session: BaseSandboxSession,         dest: Path,         base_dir: Path,     ) -> None:         _assert_daytona_session(session)         await self._delegate().deactivate(mount, session, dest, base_dir)      async def teardown_for_snapshot(         self,         mount: Mount,         session: BaseSandboxSession,         path: Path,     ) -> None:         _assert_daytona_session(session)         await self._delegate().teardown_for_snapshot(mount, session, path)      async def restore_after_snapshot(         self,         mount: Mount,         session: BaseSandboxSession,         path: Path,     ) -> None:         _assert_daytona_session(session)         if self.pattern.mode == "fuse":             await _ensure_fuse_support(session)         await _ensure_rclone(session)         await self._delegate().restore_after_snapshot(mount, session, path)      def build_docker_volume_driver_config(         self,         mount: Mount,     ) -> tuple[str, dict[str, str], bool] | None:         return None ``` |

#### supports\_native\_snapshot\_detach

```
supports_native_snapshot_detach(mount: Mount) -> bool
```

Return whether native snapshot flows can safely detach this mount in-place.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 172 173 174 175 ``` | ``` def supports_native_snapshot_detach(self, mount: Mount) -> bool:     """Return whether native snapshot flows can safely detach this mount in-place."""     _ = mount     return True ``` |