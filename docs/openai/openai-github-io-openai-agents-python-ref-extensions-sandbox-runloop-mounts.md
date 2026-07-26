---
url: https://openai.github.io/openai-agents-python/ref/extensions/sandbox/runloop/mounts/
title: `Mounts`
framework: openai
---

# `Mounts`

Mount strategy for Runloop sandboxes.

### RunloopCloudBucketMountStrategy

Bases: `MountStrategyBase`

Mount rclone-backed cloud storage in Runloop sandboxes.

Source code in `src/agents/extensions/sandbox/runloop/mounts.py`

|  |  |
| --- | --- |
| ``` 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 ``` | ``` class RunloopCloudBucketMountStrategy(MountStrategyBase):     """Mount rclone-backed cloud storage in Runloop sandboxes."""      type: Literal["runloop_cloud_bucket"] = "runloop_cloud_bucket"     pattern: RcloneMountPattern = RcloneMountPattern(mode="fuse")      def _delegate(self) -> InContainerMountStrategy:         return InContainerMountStrategy(pattern=self.pattern)      async def _delegate_for_session(self, session: BaseSandboxSession) -> InContainerMountStrategy:         return InContainerMountStrategy(             pattern=await _rclone_pattern_for_session(session, self.pattern)         )      def validate_mount(self, mount: Mount) -> None:         self._delegate().validate_mount(mount)      async def activate(         self,         mount: Mount,         session: BaseSandboxSession,         dest: Path,         base_dir: Path,     ) -> list[MaterializedFile]:         _assert_runloop_session(session)         if self.pattern.mode == "fuse":             await _ensure_fuse_support(session)         await _ensure_rclone(session)         delegate = await self._delegate_for_session(session)         return await delegate.activate(mount, session, dest, base_dir)      async def deactivate(         self,         mount: Mount,         session: BaseSandboxSession,         dest: Path,         base_dir: Path,     ) -> None:         _assert_runloop_session(session)         await self._delegate().deactivate(mount, session, dest, base_dir)      async def teardown_for_snapshot(         self,         mount: Mount,         session: BaseSandboxSession,         path: Path,     ) -> None:         _assert_runloop_session(session)         await self._delegate().teardown_for_snapshot(mount, session, path)      async def restore_after_snapshot(         self,         mount: Mount,         session: BaseSandboxSession,         path: Path,     ) -> None:         _assert_runloop_session(session)         if self.pattern.mode == "fuse":             await _ensure_fuse_support(session)         await _ensure_rclone(session)         delegate = await self._delegate_for_session(session)         await delegate.restore_after_snapshot(mount, session, path)      def build_docker_volume_driver_config(         self,         mount: Mount,     ) -> tuple[str, dict[str, str], bool] | None:         return None ``` |

#### supports\_native\_snapshot\_detach

```
supports_native_snapshot_detach(mount: Mount) -> bool
```

Return whether native snapshot flows can safely detach this mount in-place.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 172 173 174 175 ``` | ``` def supports_native_snapshot_detach(self, mount: Mount) -> bool:     """Return whether native snapshot flows can safely detach this mount in-place."""     _ = mount     return True ``` |