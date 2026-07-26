---
url: https://openai.github.io/openai-agents-python/ref/extensions/sandbox/blaxel/mounts/
title: `Mounts`
framework: openai
---

# `Mounts`

Mount strategies for Blaxel sandboxes.

Two strategies are provided:

* **BlaxelCloudBucketMountStrategy** -- mounts S3, R2, and GCS buckets via
  FUSE tools (`s3fs`, `gcsfuse`) executed inside the sandbox. Credentials
  are written to ephemeral temp files, referenced by the FUSE tool, and deleted
  immediately after the mount succeeds.
* **BlaxelDriveMountStrategy** -- mounts Blaxel Drives (persistent network
  volumes) into the sandbox using the sandbox `drives` API
  (`POST /drives/mount`). Drives persist data across sandbox sessions and
  can be shared between sandboxes. See
  `Blaxel Drive docs <https://docs.blaxel.ai/Agent-drive/Overview>`\_.

### BlaxelCloudBucketMountConfig `dataclass`

Resolved mount config ready to be executed inside a Blaxel sandbox.

Source code in `src/agents/extensions/sandbox/blaxel/mounts.py`

|  |  |
| --- | --- |
| ``` 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 ``` | ``` @dataclass(frozen=True) class BlaxelCloudBucketMountConfig:     """Resolved mount config ready to be executed inside a Blaxel sandbox."""      provider: BlaxelBucketProvider     bucket: str     mount_path: str     read_only: bool = True      # S3 / R2 fields.     access_key_id: str | None = None     secret_access_key: str | None = None     session_token: str | None = None     region: str | None = None     endpoint_url: str | None = None     prefix: str | None = None      # GCS fields.     service_account_key: str | None = None ``` |

### BlaxelCloudBucketMountStrategy

Bases: `MountStrategyBase`

Mount S3/R2/GCS buckets inside Blaxel sandboxes via FUSE tools.

`activate` installs the FUSE tool (if needed) and runs the mount command
inside the sandbox. `deactivate` / `teardown_for_snapshot` unmount via
`fusermount` or `umount`.

Source code in `src/agents/extensions/sandbox/blaxel/mounts.py`

|  |  |
| --- | --- |
| ```  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 ``` | ``` class BlaxelCloudBucketMountStrategy(MountStrategyBase):     """Mount S3/R2/GCS buckets inside Blaxel sandboxes via FUSE tools.      ``activate`` installs the FUSE tool (if needed) and runs the mount command     inside the sandbox.  ``deactivate`` / ``teardown_for_snapshot`` unmount via     ``fusermount`` or ``umount``.     """      type: Literal["blaxel_cloud_bucket"] = "blaxel_cloud_bucket"      def validate_mount(self, mount: Mount) -> None:         _build_mount_config(mount, mount_path="/validate")      async def activate(         self,         mount: Mount,         session: BaseSandboxSession,         dest: Path,         base_dir: Path,     ) -> list[MaterializedFile]:         _assert_blaxel_session(session)         _ = base_dir         mount_path = mount._resolve_mount_path(session, dest)         config = _build_mount_config(mount, mount_path=mount_path.as_posix())         await _mount_bucket(session, config)         return []      async def deactivate(         self,         mount: Mount,         session: BaseSandboxSession,         dest: Path,         base_dir: Path,     ) -> None:         _assert_blaxel_session(session)         _ = base_dir         mount_path = mount._resolve_mount_path(session, dest)         await _unmount_bucket(session, mount_path.as_posix())      async def teardown_for_snapshot(         self,         mount: Mount,         session: BaseSandboxSession,         path: Path,     ) -> None:         _assert_blaxel_session(session)         _ = mount         await _unmount_bucket(session, sandbox_path_str(path))      async def restore_after_snapshot(         self,         mount: Mount,         session: BaseSandboxSession,         path: Path,     ) -> None:         _assert_blaxel_session(session)         config = _build_mount_config(mount, mount_path=sandbox_path_str(path))         await _mount_bucket(session, config)      def build_docker_volume_driver_config(         self,         mount: Mount,     ) -> tuple[str, dict[str, str], bool] | None:         _ = mount         return None ``` |

#### supports\_native\_snapshot\_detach

```
supports_native_snapshot_detach(mount: Mount) -> bool
```

Return whether native snapshot flows can safely detach this mount in-place.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 172 173 174 175 ``` | ``` def supports_native_snapshot_detach(self, mount: Mount) -> bool:     """Return whether native snapshot flows can safely detach this mount in-place."""     _ = mount     return True ``` |

### BlaxelDriveMountConfig `dataclass`

Configuration for mounting a Blaxel Drive into a sandbox.

Blaxel Drives are persistent network volumes managed by the Blaxel platform.
Data written to a drive persists across sandbox sessions and can be shared
between multiple sandboxes.

See https://docs.blaxel.ai/Agent-drive/Overview for details.

Source code in `src/agents/extensions/sandbox/blaxel/mounts.py`

|  |  |
| --- | --- |
| ``` 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 ``` | ``` @dataclass(frozen=True) class BlaxelDriveMountConfig:     """Configuration for mounting a Blaxel Drive into a sandbox.      Blaxel Drives are persistent network volumes managed by the Blaxel platform.     Data written to a drive persists across sandbox sessions and can be shared     between multiple sandboxes.      See https://docs.blaxel.ai/Agent-drive/Overview for details.     """      drive_name: str     mount_path: str     drive_path: str = "/"     read_only: bool = False ``` |

### BlaxelDriveMount

Bases: `Mount`

A concrete Mount entry for Blaxel Drives.

Carries the drive configuration fields directly on the mount, following
the same pattern as `S3Mount`, `R2Mount`, and `GCSMount`.

Usage::

```
from agents.extensions.sandbox.blaxel import (
    BlaxelDriveMount,
    BlaxelDriveMountStrategy,
)

mount = BlaxelDriveMount(
    drive_name="my-drive",
    drive_mount_path="/data",
    mount_strategy=BlaxelDriveMountStrategy(),
)
```

Source code in `src/agents/extensions/sandbox/blaxel/mounts.py`

|  |  |
| --- | --- |
| ``` 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 ``` | ``` class BlaxelDriveMount(Mount):     """A concrete Mount entry for Blaxel Drives.      Carries the drive configuration fields directly on the mount, following     the same pattern as ``S3Mount``, ``R2Mount``, and ``GCSMount``.      Usage::          from agents.extensions.sandbox.blaxel import (             BlaxelDriveMount,             BlaxelDriveMountStrategy,         )          mount = BlaxelDriveMount(             drive_name="my-drive",             drive_mount_path="/data",             mount_strategy=BlaxelDriveMountStrategy(),         )     """      type: Literal["blaxel_drive_mount"] = "blaxel_drive_mount"     drive_name: str     drive_mount_path: str = ""     drive_path: str = "/"     drive_read_only: bool = False      def model_post_init(self, context: object, /) -> None:         """Validate the mount strategy without requiring in-container or docker patterns.          Blaxel drives use a platform-level API (``POST /drives/mount``) rather         than in-container FUSE tools or Docker volume drivers, so the base         ``Mount`` validation for those patterns does not apply.         """         _ = context         default_permissions = Permissions(             owner=FileMode.ALL,             group=FileMode.READ | FileMode.EXEC,             other=FileMode.READ | FileMode.EXEC,         )         if (             self.permissions.owner != default_permissions.owner             or self.permissions.group != default_permissions.group             or self.permissions.other != default_permissions.other         ):             warnings.warn(                 "Mount permissions are not enforced. "                 "Please configure access in the cloud provider instead; "                 "mount-level permissions can be unreliable.",                 stacklevel=2,             )             self.permissions.owner = default_permissions.owner             self.permissions.group = default_permissions.group             self.permissions.other = default_permissions.other         self.permissions.directory = True         self.mount_strategy.validate_mount(self) ``` |

#### model\_post\_init

```
model_post_init(context: object) -> None
```

Validate the mount strategy without requiring in-container or docker patterns.

Blaxel drives use a platform-level API (`POST /drives/mount`) rather
than in-container FUSE tools or Docker volume drivers, so the base
`Mount` validation for those patterns does not apply.

Source code in `src/agents/extensions/sandbox/blaxel/mounts.py`

|  |  |
| --- | --- |
| ``` 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 ``` | ``` def model_post_init(self, context: object, /) -> None:     """Validate the mount strategy without requiring in-container or docker patterns.      Blaxel drives use a platform-level API (``POST /drives/mount``) rather     than in-container FUSE tools or Docker volume drivers, so the base     ``Mount`` validation for those patterns does not apply.     """     _ = context     default_permissions = Permissions(         owner=FileMode.ALL,         group=FileMode.READ | FileMode.EXEC,         other=FileMode.READ | FileMode.EXEC,     )     if (         self.permissions.owner != default_permissions.owner         or self.permissions.group != default_permissions.group         or self.permissions.other != default_permissions.other     ):         warnings.warn(             "Mount permissions are not enforced. "             "Please configure access in the cloud provider instead; "             "mount-level permissions can be unreliable.",             stacklevel=2,         )         self.permissions.owner = default_permissions.owner         self.permissions.group = default_permissions.group         self.permissions.other = default_permissions.other     self.permissions.directory = True     self.mount_strategy.validate_mount(self) ``` |

#### apply `async`

```
apply(
    session: BaseSandboxSession, dest: Path, base_dir: Path
) -> list[MaterializedFile]
```

Activate this mount for a manifest application pass.

In-container strategies run a live mount command here. Docker-volume strategies are
intentionally no-ops because the backend attaches them before the session starts.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 412 413 414 415 416 417 418 419 420 421 422 423 424 ``` | ``` async def apply(     self,     session: BaseSandboxSession,     dest: Path,     base_dir: Path, ) -> list[MaterializedFile]:     """Activate this mount for a manifest application pass.      In-container strategies run a live mount command here. Docker-volume strategies are     intentionally no-ops because the backend attaches them before the session starts.     """      return await self.mount_strategy.activate(self, session, dest, base_dir) ``` |

#### in\_container\_adapter

```
in_container_adapter() -> InContainerMountAdapter
```

Return the strategy adapter for in-container mount lifecycle.

Mount subclasses that do not support in-container mounts inherit this default unsupported
implementation.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 395 396 397 398 399 400 401 402 403 404 405 ``` | ``` def in_container_adapter(self) -> InContainerMountAdapter:     """Return the strategy adapter for in-container mount lifecycle.      Mount subclasses that do not support in-container mounts inherit this default unsupported     implementation.     """      raise MountConfigError(         message="in-container mounts are not supported for this mount type",         context={"mount_type": self.type},     ) ``` |

#### docker\_volume\_adapter

```
docker_volume_adapter() -> DockerVolumeMountAdapter
```

Return the strategy adapter for Docker volume lifecycle.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 407 408 409 410 ``` | ``` def docker_volume_adapter(self) -> DockerVolumeMountAdapter:     """Return the strategy adapter for Docker volume lifecycle."""      return DockerVolumeMountAdapter(self) ``` |

#### unmount `async`

```
unmount(
    session: BaseSandboxSession, dest: Path, base_dir: Path
) -> None
```

Deactivate this mount for manifest teardown.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 426 427 428 429 430 431 432 433 434 ``` | ``` async def unmount(     self,     session: BaseSandboxSession,     dest: Path,     base_dir: Path, ) -> None:     """Deactivate this mount for manifest teardown."""      await self.mount_strategy.deactivate(self, session, dest, base_dir) ``` |

#### build\_in\_container\_mount\_config `async`

```
build_in_container_mount_config(
    session: BaseSandboxSession,
    pattern: MountPattern,
    *,
    include_config_text: bool,
) -> MountPatternConfig | None
```

Return pattern runtime config for provider-backed in-container mounts.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 436 437 438 439 440 441 442 443 444 445 446 ``` | ``` async def build_in_container_mount_config(     self,     session: BaseSandboxSession,     pattern: MountPattern,     *,     include_config_text: bool, ) -> MountPatternConfig | None:     """Return pattern runtime config for provider-backed in-container mounts."""      _ = (session, pattern, include_config_text)     return None ``` |

#### supported\_in\_container\_patterns

```
supported_in_container_patterns() -> tuple[
    type[MountPatternBase], ...
]
```

Return the `MountPattern` classes accepted by `InContainerMountStrategy`.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 448 449 450 451 ``` | ``` def supported_in_container_patterns(self) -> tuple[builtins.type[MountPatternBase], ...]:     """Return the `MountPattern` classes accepted by `InContainerMountStrategy`."""      return () ``` |

#### supported\_docker\_volume\_drivers

```
supported_docker_volume_drivers() -> frozenset[str]
```

Return Docker volume driver names accepted by `DockerVolumeMountStrategy`.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 453 454 455 456 ``` | ``` def supported_docker_volume_drivers(self) -> frozenset[str]:     """Return Docker volume driver names accepted by `DockerVolumeMountStrategy`."""      return frozenset() ``` |

#### build\_docker\_volume\_driver\_config

```
build_docker_volume_driver_config(
    strategy: DockerVolumeMountStrategy,
) -> tuple[str, dict[str, str], bool]
```

Build the Docker volume driver tuple for Docker-volume mounts.

Mount subclasses that do not support Docker volumes inherit this default unsupported
implementation.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 ``` | ``` def build_docker_volume_driver_config(     self,     strategy: DockerVolumeMountStrategy, ) -> tuple[str, dict[str, str], bool]:     """Build the Docker volume driver tuple for Docker-volume mounts.      Mount subclasses that do not support Docker volumes inherit this default unsupported     implementation.     """      _ = strategy     raise MountConfigError(         message="docker-volume mounts are not supported for this mount type",         context={"mount_type": self.type},     ) ``` |

### BlaxelDriveMountStrategy

Bases: `MountStrategyBase`

Mount a Blaxel Drive into a sandbox via the sandbox drives API.

This strategy uses the sandbox's `drives` sub-system (which wraps
`POST /drives/mount` and `DELETE /drives/mount/<path>`) to attach
and detach persistent drives.

Usage with a `BlaxelDriveMount` entry::

```
from agents.extensions.sandbox.blaxel import (
    BlaxelDriveMount,
    BlaxelDriveMountStrategy,
)

mount = BlaxelDriveMount(
    drive_name="my-drive",
    drive_mount_path="/data",
    mount_strategy=BlaxelDriveMountStrategy(),
)
```

Source code in `src/agents/extensions/sandbox/blaxel/mounts.py`

|  |  |
| --- | --- |
| ``` 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 ``` | ``` class BlaxelDriveMountStrategy(MountStrategyBase):     """Mount a Blaxel Drive into a sandbox via the sandbox drives API.      This strategy uses the sandbox's ``drives`` sub-system (which wraps     ``POST /drives/mount`` and ``DELETE /drives/mount/<path>``) to attach     and detach persistent drives.      Usage with a ``BlaxelDriveMount`` entry::          from agents.extensions.sandbox.blaxel import (             BlaxelDriveMount,             BlaxelDriveMountStrategy,         )          mount = BlaxelDriveMount(             drive_name="my-drive",             drive_mount_path="/data",             mount_strategy=BlaxelDriveMountStrategy(),         )     """      type: Literal["blaxel_drive"] = "blaxel_drive"      def validate_mount(self, mount: Mount) -> None:         if not isinstance(mount, BlaxelDriveMount):             raise MountConfigError(                 message=("BlaxelDriveMountStrategy requires a BlaxelDriveMount entry"),                 context={"mount_type": mount.type},             )      async def activate(         self,         mount: Mount,         session: BaseSandboxSession,         dest: Path,         base_dir: Path,     ) -> list[MaterializedFile]:         _assert_blaxel_session(session)         _ = base_dir         config = self._resolve_config(mount, session, dest)         sandbox = getattr(session, "_sandbox", None)         if sandbox is None:             raise MountConfigError(                 message="cannot access sandbox instance for drive mount",                 context={"session_type": type(session).__name__},             )         await _attach_drive(sandbox, config)         return []      async def deactivate(         self,         mount: Mount,         session: BaseSandboxSession,         dest: Path,         base_dir: Path,     ) -> None:         _assert_blaxel_session(session)         _ = base_dir         config = self._resolve_config(mount, session, dest)         sandbox = getattr(session, "_sandbox", None)         if sandbox is not None:             await _detach_drive(sandbox, config.mount_path)      async def teardown_for_snapshot(         self,         mount: Mount,         session: BaseSandboxSession,         path: Path,     ) -> None:         _assert_blaxel_session(session)         effective_path = self._effective_mount_path(mount, path)         sandbox = getattr(session, "_sandbox", None)         if sandbox is not None:             await _detach_drive(sandbox, effective_path)      async def restore_after_snapshot(         self,         mount: Mount,         session: BaseSandboxSession,         path: Path,     ) -> None:         _assert_blaxel_session(session)         effective_path = self._effective_mount_path(mount, path)         config = self._resolve_config_from_source(mount, effective_path)         sandbox = getattr(session, "_sandbox", None)         if sandbox is None:             raise MountConfigError(                 message="cannot access sandbox instance for drive remount",                 context={"session_type": type(session).__name__},             )         await _attach_drive(sandbox, config)      def build_docker_volume_driver_config(         self,         mount: Mount,     ) -> tuple[str, dict[str, str], bool] | None:         _ = mount         return None      @staticmethod     def _resolve_config(         mount: Mount, session: BaseSandboxSession, dest: Path     ) -> BlaxelDriveMountConfig:         if not isinstance(mount, BlaxelDriveMount):             raise MountConfigError(                 message="BlaxelDriveMountStrategy requires a BlaxelDriveMount entry",                 context={"mount_type": mount.type},             )         mount_path = mount.drive_mount_path or sandbox_path_str(             mount._resolve_mount_path(session, dest)         )         return BlaxelDriveMountConfig(             drive_name=mount.drive_name,             mount_path=mount_path,             drive_path=mount.drive_path,             read_only=mount.drive_read_only,         )      @staticmethod     def _effective_mount_path(mount: Mount, fallback: Path) -> str:         """Return the actual mount path, preferring ``drive_mount_path`` over the manifest path."""         if isinstance(mount, BlaxelDriveMount) and mount.drive_mount_path:             return mount.drive_mount_path         return sandbox_path_str(fallback)      @staticmethod     def _resolve_config_from_source(mount: Mount, mount_path: str) -> BlaxelDriveMountConfig:         if not isinstance(mount, BlaxelDriveMount):             raise MountConfigError(                 message="BlaxelDriveMountStrategy requires a BlaxelDriveMount entry",                 context={"mount_type": mount.type},             )         return BlaxelDriveMountConfig(             drive_name=mount.drive_name,             mount_path=mount_path,             drive_path=mount.drive_path,             read_only=mount.drive_read_only,         ) ``` |

#### supports\_native\_snapshot\_detach

```
supports_native_snapshot_detach(mount: Mount) -> bool
```

Return whether native snapshot flows can safely detach this mount in-place.

Source code in `src/agents/sandbox/entries/mounts/base.py`

|  |  |
| --- | --- |
| ``` 172 173 174 175 ``` | ``` def supports_native_snapshot_detach(self, mount: Mount) -> bool:     """Return whether native snapshot flows can safely detach this mount in-place."""     _ = mount     return True ``` |