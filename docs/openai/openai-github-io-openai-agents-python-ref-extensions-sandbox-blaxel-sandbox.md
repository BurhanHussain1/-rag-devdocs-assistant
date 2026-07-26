---
url: https://openai.github.io/openai-agents-python/ref/extensions/sandbox/blaxel/sandbox/
title: `Sandbox`
framework: openai
---

# `Sandbox`

Blaxel sandbox (https://blaxel.ai) implementation.

This module provides a Blaxel-backed sandbox client/session implementation backed by
`blaxel.core.sandbox.SandboxInstance`.

The `blaxel` dependency is optional, so package-level exports should guard imports of this
module. Within this module, Blaxel SDK imports are lazy so users without the extra can still
import the package.

### BlaxelTimeouts

Bases: `BaseModel`

Timeout configuration for Blaxel sandbox operations.

Source code in `src/agents/extensions/sandbox/blaxel/sandbox.py`

|  |  |
| --- | --- |
| ``` 247 248 249 250 251 252 253 254 255 256 257 ``` | ``` class BlaxelTimeouts(BaseModel):     """Timeout configuration for Blaxel sandbox operations."""      model_config = {"frozen": True}      exec_timeout_s: float = Field(default=300.0, ge=1)     cleanup_s: float = Field(default=30.0, ge=1)     file_upload_s: float = Field(default=1800.0, ge=1)     file_download_s: float = Field(default=1800.0, ge=1)     workspace_tar_s: float = Field(default=300.0, ge=1)     fast_op_s: float = Field(default=30.0, ge=1) ``` |

### BlaxelSandboxClientOptions `dataclass`

Client options for the Blaxel sandbox.

Source code in `src/agents/extensions/sandbox/blaxel/sandbox.py`

|  |  |
| --- | --- |
| ``` 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 ``` | ``` @dataclass(frozen=True) class BlaxelSandboxClientOptions:     """Client options for the Blaxel sandbox."""      image: str | None = None     memory: int | None = None     region: str | None = None     ports: tuple[dict[str, Any], ...] | None = None     env_vars: dict[str, str] | None = None     labels: dict[str, str] | None = None     ttl: str | None = None     name: str | None = None     pause_on_exit: bool = False     timeouts: BlaxelTimeouts | dict[str, object] | None = None     exposed_port_public: bool = True     exposed_port_url_ttl_s: int = 3600 ``` |

### BlaxelSandboxSessionState

Bases: `SandboxSessionState`

Serializable state for a Blaxel-backed session.

Source code in `src/agents/extensions/sandbox/blaxel/sandbox.py`

|  |  |
| --- | --- |
| ``` 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 ``` | ``` class BlaxelSandboxSessionState(SandboxSessionState):     """Serializable state for a Blaxel-backed session."""      type: Literal["blaxel"] = "blaxel"     sandbox_name: str     image: str | None = None     memory: int | None = None     region: str | None = None     base_env_vars: dict[str, str] = Field(default_factory=dict)     labels: dict[str, str] = Field(default_factory=dict)     ttl: str | None = None     pause_on_exit: bool = False     timeouts: BlaxelTimeouts = Field(default_factory=BlaxelTimeouts)     sandbox_url: str | None = None     exposed_port_public: bool = True     exposed_port_url_ttl_s: int = 3600 ``` |

#### \_\_pydantic\_init\_subclass\_\_ `classmethod`

```
__pydantic_init_subclass__(**kwargs: Any) -> None
```

Auto-register every subclass by its `type` field default.

Source code in `src/agents/sandbox/session/sandbox_session_state.py`

|  |  |
| --- | --- |
| ``` 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 ``` | ``` @classmethod def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:     """Auto-register every subclass by its ``type`` field default."""     super().__pydantic_init_subclass__(**kwargs)      type_field = cls.model_fields.get("type")     if type_field is None:         return      annotation = type_field.annotation     if get_origin(annotation) is not Literal:         return      args = get_args(annotation)     if not args:         return      type_default = type_field.default     if not isinstance(type_default, str) or type_default == "":         return      SandboxSessionState._subclass_registry[type_default] = cls ``` |

#### parse `classmethod`

```
parse(payload: object) -> SandboxSessionState
```

Deserialize *payload* into the correct registered subclass.

Accepts a `SandboxSessionState` instance (returned as-is if already a
subclass, or upgraded via `model_dump` -> registry lookup if it is a
bare base instance) or a plain `dict`.

Source code in `src/agents/sandbox/session/sandbox_session_state.py`

|  |  |
| --- | --- |
| ``` 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 ``` | ``` @classmethod def parse(cls, payload: object) -> SandboxSessionState:     """Deserialize *payload* into the correct registered subclass.      Accepts a ``SandboxSessionState`` instance (returned as-is if already a     subclass, or upgraded via ``model_dump`` -> registry lookup if it is a     bare base instance) or a plain ``dict``.     """     if isinstance(payload, SandboxSessionState):         if type(payload) is not SandboxSessionState:             return payload         payload = payload.model_dump()      if isinstance(payload, dict):         state_type = payload.get("type")         if not isinstance(state_type, str):             raise ValueError("sandbox session state payload must include a string `type`")          subclass = SandboxSessionState._subclass_registry.get(state_type)         if subclass is None:             raise ValueError(f"unknown sandbox session state type `{state_type}`")          return subclass.model_validate(payload)      raise TypeError("session state payload must be a SandboxSessionState or dict") ``` |

### BlaxelSandboxSession

Bases: `BaseSandboxSession`

Blaxel-backed sandbox session implementation.

Source code in `src/agents/extensions/sandbox/blaxel/sandbox.py`

|  |  |
| --- | --- |
| ```  321  322  323  324  325  326  327  328  329  330  331  332  333  334  335  336  337  338  339  340  341  342  343  344  345  346  347  348  349  350  351  352  353  354  355  356  357  358  359  360  361  362  363  364  365  366  367  368  369  370  371  372  373  374  375  376  377  378  379  380  381  382  383  384  385  386  387  388  389  390  391  392  393  394  395  396  397  398  399  400  401  402  403  404  405  406  407  408  409  410  411  412  413  414  415  416  417  418  419  420  421  422  423  424  425  426  427  428  429  430  431  432  433  434  435  436  437  438  439  440  441  442  443  444  445  446  447  448  449  450  451  452  453  454  455  456  457  458  459  460  461  462  463  464  465  466  467  468  469  470  471  472  473  474  475  476  477  478  479  480  481  482  483  484  485  486  487  488  489  490  491  492  493  494  495  496  497  498  499  500  501  502  503  504  505  506  507  508  509  510  511  512  513  514  515  516  517  518  519  520  521  522  523  524  525  526  527  528  529  530  531  532  533  534  535  536  537  538  539  540  541  542  543  544  545  546  547  548  549  550  551  552  553  554  555  556  557  558  559  560  561  562  563  564  565  566  567  568  569  570  571  572  573  574  575  576  577  578  579  580  581  582  583  584  585  586  587  588  589  590  591  592  593  594  595  596  597  598  599  600  601  602  603  604  605  606  607  608  609  610  611  612  613  614  615  616  617  618  619  620  621  622  623  624  625  626  627  628  629  630  631  632  633  634  635  636  637  638  639  640  641  642  643  644  645  646  647  648  649  650  651  652  653  654  655  656  657  658  659  660  661  662  663  664  665  666  667  668  669  670  671  672  673  674  675  676  677  678  679  680  681  682  683  684  685  686  687  688  689  690  691  692  693  694  695  696  697  698  699  700  701  702  703  704  705  706  707  708  709  710  711  712  713  714  715  716  717  718  719  720  721  722  723  724  725  726  727  728  729  730  731  732  733  734  735  736  737  738  739  740  741  742  743  744  745  746  747  748  749  750  751  752  753  754  755  756  757  758  759  760  761  762  763  764  765  766  767  768  769  770  771  772  773  774  775  776  777  778  779  780  781  782  783  784  785  786  787  788  789  790  791  792  793  794  795  796  797  798  799  800  801  802  803  804  805  806  807  808  809  810  811  812  813  814  815  816  817  818  819  820  821  822  823  824  825  826  827  828  829  830  831  832  833  834  835  836  837  838  839  840  841  842  843  844  845  846  847  848  849  850  851  852  853  854  855  856  857  858  859  860  861  862  863  864  865  866  867  868  869  870  871  872  873  874  875  876  877  878  879  880  881  882  883  884  885  886  887  888  889  890  891  892  893  894  895  896  897  898  899  900  901  902  903  904  905  906  907  908  909  910  911  912  913  914  915  916  917  918  919  920  921  922  923  924  925  926  927  928  929  930  931  932  933  934  935  936  937  938  939  940  941  942  943  944  945  946  947  948  949  950  951  952  953  954  955  956  957  958  959  960  961  962  963  964  965  966  967  968  969  970  971  972  973  974  975  976  977  978  979  980  981  982  983  984  985  986  987  988  989  990  991  992  993  994  995  996  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 ``` | ``` class BlaxelSandboxSession(BaseSandboxSession):     """Blaxel-backed sandbox session implementation."""      state: BlaxelSandboxSessionState     _sandbox: Any  # SandboxInstance     _token: str | None     _pty_lock: asyncio.Lock     _pty_sessions: dict[int, _BlaxelPtySessionEntry]     _reserved_pty_process_ids: set[int]      def __init__(         self,         *,         state: BlaxelSandboxSessionState,         sandbox: Any,         token: str | None = None,     ) -> None:         self.state = state         self._sandbox = sandbox         self._token = token         self._pty_lock = asyncio.Lock()         self._pty_sessions = {}         self._reserved_pty_process_ids = set()      @classmethod     def from_state(         cls,         state: BlaxelSandboxSessionState,         *,         sandbox: Any,         token: str | None = None,     ) -> BlaxelSandboxSession:         return cls(state=state, sandbox=sandbox, token=token)      @property     def sandbox_name(self) -> str:         return self.state.sandbox_name      # -- exposed ports -------------------------------------------------------      def _assert_exposed_port_configured(self, port: int) -> None:         # Blaxel previews can be created for any port on demand; no pre-declaration needed.         pass      async def _resolve_exposed_port(self, port: int) -> ExposedPortEndpoint:         is_public = self.state.exposed_port_public         try:             preview = await self._sandbox.previews.create_if_not_exists(                 {                     "metadata": {"name": f"port-{port}"},                     "spec": {"port": port, "public": is_public},                 }             )         except Exception as e:             raise ExposedPortUnavailableError(                 port=port,                 exposed_ports=self.state.exposed_ports,                 reason="backend_unavailable",                 context={"backend": "blaxel", "detail": "preview_creation_failed"},                 cause=e,             ) from e          url = _extract_preview_url(preview)         if not isinstance(url, str) or not url:             raise ExposedPortUnavailableError(                 port=port,                 exposed_ports=self.state.exposed_ports,                 reason="backend_unavailable",                 context={"backend": "blaxel", "detail": "invalid_preview_url", "url": url},             )          # For private previews, create a time-limited token.         query = ""         if not is_public:             try:                 expires_at = datetime.now(timezone.utc) + timedelta(                     seconds=self.state.exposed_port_url_ttl_s,                 )                 token = await preview.tokens.create(expires_at)                 token_value = getattr(token, "value", None) or getattr(token, "token", None)                 if isinstance(token_value, str) and token_value:                     query = f"bl_preview_token={token_value}"             except Exception as e:                 raise ExposedPortUnavailableError(                     port=port,                     exposed_ports=self.state.exposed_ports,                     reason="backend_unavailable",                     context={"backend": "blaxel", "detail": "preview_token_creation_failed"},                     cause=e,                 ) from e          try:             split = urlsplit(url)             host = split.hostname             if host is None:                 raise ValueError("missing hostname")             port_value = split.port or (443 if split.scheme == "https" else 80)             return ExposedPortEndpoint(                 host=host,                 port=port_value,                 tls=split.scheme == "https",                 query=query,             )         except Exception as e:             raise ExposedPortUnavailableError(                 port=port,                 exposed_ports=self.state.exposed_ports,                 reason="backend_unavailable",                 context={"backend": "blaxel", "detail": "url_parse_failed", "url": url},                 cause=e,             ) from e      # -- lifecycle -----------------------------------------------------------      async def start(self) -> None:         # When resuming a paused sandbox, _skip_start is set by the client to         # avoid reapplying the full manifest over files that may have changed         # while the sandbox was paused.         if getattr(self, "_skip_start", False):             return          # Ensure workspace root exists before BaseSandboxSession.start() materializes         # the manifest.  Blaxel base images run as root and do not ship a pre-created         # workspace directory.         root = sandbox_path_str(self.state.manifest.root)         try:             await self._sandbox.process.exec(                 {                     "command": f"mkdir -p {shlex.quote(root)}",                     "working_dir": "/",                     "wait_for_completion": True,                     "timeout": 10000,                 }             )         except Exception as e:             logger.debug("workspace root mkdir failed (will retry during materialization): %s", e)         await super().start()      async def stop(self) -> None:         await super().stop()      async def shutdown(self) -> None:         await self.pty_terminate_all()         try:             if not self.state.pause_on_exit:                 await self._sandbox.delete()             # When pause_on_exit is True the sandbox is kept alive.  Blaxel             # automatically resumes it on the next connection.         except Exception as e:             logger.warning("sandbox delete failed during shutdown: %s", e)      async def _validate_path_access(self, path: Path | str, *, for_write: bool = False) -> Path:         return await self._validate_remote_path_access(path, for_write=for_write)      def _runtime_helpers(self) -> tuple[RuntimeHelperScript, ...]:         return (RESOLVE_WORKSPACE_PATH_HELPER,)      # -- file operations -----------------------------------------------------      async def mkdir(         self,         path: Path | str,         *,         parents: bool = False,         user: str | User | None = None,     ) -> None:         if user is not None:             path = await self._check_mkdir_with_exec(path, parents=parents, user=user)         else:             path = await self._validate_path_access(path, for_write=True)         if path == Path("/"):             return         try:             await self._sandbox.fs.mkdir(sandbox_path_str(path))         except Exception as e:             raise WorkspaceArchiveWriteError(                 path=path,                 context={"reason": "mkdir_failed"},                 cause=e,             ) from e      async def read(self, path: Path | str, *, user: str | User | None = None) -> io.IOBase:         error_path = posix_path_as_path(coerce_posix_path(path))         if user is not None:             workspace_path = await self._check_read_with_exec(path, user=user)         else:             workspace_path = await self._validate_path_access(path)          try:             data: Any = await self._sandbox.fs.read_binary(sandbox_path_str(workspace_path))             if isinstance(data, str):                 data = data.encode("utf-8")             return io.BytesIO(bytes(data))         except Exception as e:             # Blaxel SDK raises ResponseError with status 404 for missing files.             status = getattr(e, "status", None)             if status is None and hasattr(e, "args") and e.args:                 first_arg = e.args[0]                 if isinstance(first_arg, dict):                     status = first_arg.get("status")             error_str = str(e).lower()             if status == 404 or "not found" in error_str or "no such file" in error_str:                 raise WorkspaceReadNotFoundError(path=error_path, cause=e) from e             raise WorkspaceArchiveReadError(path=error_path, cause=e) from e      async def write(         self,         path: Path | str,         data: io.IOBase,         *,         user: str | User | None = None,     ) -> None:         error_path = posix_path_as_path(coerce_posix_path(path))         if user is not None:             await self._check_write_with_exec(path, user=user)          payload = data.read()         if isinstance(payload, str):             payload = payload.encode("utf-8")         if not isinstance(payload, bytes | bytearray):             raise WorkspaceWriteTypeError(path=error_path, actual_type=type(payload).__name__)          workspace_path = await self._validate_path_access(path, for_write=True)         try:             await self._sandbox.fs.write_binary(sandbox_path_str(workspace_path), bytes(payload))         except Exception as e:             raise WorkspaceArchiveWriteError(path=workspace_path, cause=e) from e      # -- exec ----------------------------------------------------------------      async def _resolved_envs(self) -> dict[str, str]:         manifest_envs = await self.state.manifest.environment.resolve()         return {**self.state.base_env_vars, **manifest_envs}      def _coerce_exec_timeout(self, timeout_s: float | None) -> float:         """Resolve the effective exec timeout in seconds."""         if timeout_s is None:             return float(self.state.timeouts.exec_timeout_s)         if timeout_s <= 0:             return 0.001         return float(timeout_s)      async def _exec_internal(         self,         *command: str | Path,         timeout: float | None = None,     ) -> ExecResult:         cmd_str = shlex.join(str(c) for c in command)         cwd = self.state.manifest.root         exec_timeout = self._coerce_exec_timeout(timeout)         timeout_ms = int(max(1, math.ceil(exec_timeout)) * 1000)          # Resolve manifest + base env vars and prepend them so the executed         # process sees them.         envs = await self._resolved_envs()         if envs:             env_prefix = " ".join(f"{shlex.quote(k)}={shlex.quote(v)}" for k, v in envs.items())             cmd_str = f"env {env_prefix} {cmd_str}"          try:             result = await asyncio.wait_for(                 self._sandbox.process.exec(                     {                         "command": cmd_str,                         "working_dir": cwd,                         "wait_for_completion": True,                         "timeout": timeout_ms,                     }                 ),                 timeout=exec_timeout,             )              exit_code = int(getattr(result, "exit_code", 0) or 0)             # Blaxel ProcessResponse uses .stdout / .stderr / .logs attributes. Prefer             # split streams when available, and only fall back to logs/output for older SDKs.             has_split_streams = hasattr(result, "stdout") or hasattr(result, "stderr")             stdout = str(getattr(result, "stdout", "") or "")             stderr = str(getattr(result, "stderr", "") or "")             fallback = str(getattr(result, "logs", "") or getattr(result, "output", "") or "")             stdout_bytes = stdout.encode("utf-8", errors="replace")             stderr_bytes = stderr.encode("utf-8", errors="replace")              if has_split_streams:                 return ExecResult(stdout=stdout_bytes, stderr=stderr_bytes, exit_code=exit_code)              fallback_bytes = fallback.encode("utf-8", errors="replace")             if exit_code == 0:                 return ExecResult(stdout=fallback_bytes, stderr=b"", exit_code=exit_code)             return ExecResult(stdout=b"", stderr=fallback_bytes, exit_code=exit_code)         except asyncio.TimeoutError as e:             raise ExecTimeoutError(command=command, timeout_s=exec_timeout, cause=e) from e         except (ExecTimeoutError, ExecTransportError):             raise         except Exception as e:             api_error_cls = _import_sandbox_api_error()             if api_error_cls is not None and isinstance(e, api_error_cls):                 status = getattr(e, "status_code", None)                 if status in (408, 504):                     raise ExecTimeoutError(command=command, timeout_s=exec_timeout, cause=e) from e             raise _blaxel_exec_transport_error(command=command, cause=e) from e      # -- running check -------------------------------------------------------      async def running(self) -> bool:         try:             await asyncio.wait_for(self._sandbox.fs.ls("/"), timeout=10.0)             return True         except Exception as e:             logger.debug("sandbox health check failed: %s", e)             return False      # -- workspace persistence -----------------------------------------------      def _tar_exclude_args(self) -> list[str]:         return shell_tar_exclude_args(self._persist_workspace_skip_relpaths())      @retry_async(         retry_if=lambda exc, self: (             exception_chain_contains_type(exc, (asyncio.TimeoutError,))             or exception_chain_has_status_code(exc, TRANSIENT_HTTP_STATUS_CODES)         )     )     async def persist_workspace(self) -> io.IOBase:         root = self._workspace_root_path()         tar_path = f"/tmp/bl-persist-{self.state.session_id.hex}.tar"         excludes = " ".join(self._tar_exclude_args())         tar_cmd = (             f"tar {excludes} -C {shlex.quote(root.as_posix())} -cf {shlex.quote(tar_path)} ."         ).strip()          unmounted_mounts: list[tuple[Mount, Path]] = []         unmount_error: WorkspaceArchiveReadError | None = None         for mount_entry, mount_path in self.state.manifest.ephemeral_mount_targets():             try:                 await mount_entry.mount_strategy.teardown_for_snapshot(                     mount_entry, self, mount_path                 )             except Exception as e:                 unmount_error = WorkspaceArchiveReadError(path=root, cause=e)                 break             unmounted_mounts.append((mount_entry, mount_path))          snapshot_error: WorkspaceArchiveReadError | None = None         raw: bytes | None = None         if unmount_error is None:             try:                 result = await self._exec_internal(                     "sh", "-c", tar_cmd, timeout=self.state.timeouts.workspace_tar_s                 )                 if result.exit_code != 0:                     raise WorkspaceArchiveReadError(                         path=root,                         context={                             "reason": "tar_failed",                             "output": result.stderr.decode("utf-8", errors="replace"),                         },                         retryable=False,                     )                 raw_data: Any = await self._sandbox.fs.read_binary(tar_path)                 if isinstance(raw_data, str):                     raw_data = raw_data.encode("utf-8")                 raw = bytes(raw_data)             except WorkspaceArchiveReadError as e:                 snapshot_error = e             except Exception as e:                 snapshot_error = WorkspaceArchiveReadError(path=root, cause=e)             finally:                 try:                     await self._exec_internal(                         "rm", "-f", "--", tar_path, timeout=self.state.timeouts.cleanup_s                     )                 except Exception as e:                     logger.debug("persist cleanup rm failed (non-fatal): %s", e)          remount_error: WorkspaceArchiveReadError | None = None         for mount_entry, mount_path in reversed(unmounted_mounts):             try:                 await mount_entry.mount_strategy.restore_after_snapshot(                     mount_entry, self, mount_path                 )             except Exception as e:                 if remount_error is None:                     remount_error = WorkspaceArchiveReadError(path=root, cause=e)          if remount_error is not None:             raise remount_error         if unmount_error is not None:             raise unmount_error         if snapshot_error is not None:             raise snapshot_error          assert raw is not None         return io.BytesIO(raw)      async def hydrate_workspace(self, data: io.IOBase) -> None:         root = self._workspace_root_path()         tar_path = f"/tmp/bl-hydrate-{self.state.session_id.hex}.tar"         payload = data.read()         if isinstance(payload, str):             payload = payload.encode("utf-8")         if not isinstance(payload, bytes | bytearray):             raise WorkspaceWriteTypeError(path=Path(tar_path), actual_type=type(payload).__name__)          try:             validate_tar_bytes(                 bytes(payload),                 allow_external_symlink_targets=False,             )         except UnsafeTarMemberError as e:             raise WorkspaceArchiveWriteError(                 path=root,                 context={                     "reason": "unsafe_or_invalid_tar",                     "member": e.member,                     "detail": str(e),                 },                 cause=e,             ) from e          try:             await self.mkdir(root, parents=True)             await self._sandbox.fs.write_binary(tar_path, bytes(payload))             result = await self._exec_internal(                 "sh",                 "-c",                 f"tar -C {shlex.quote(root.as_posix())} -xf {shlex.quote(tar_path)}",                 timeout=self.state.timeouts.workspace_tar_s,             )             if result.exit_code != 0:                 raise WorkspaceArchiveWriteError(                     path=root,                     context={                         "reason": "tar_extract_failed",                         "output": result.stderr.decode("utf-8", errors="replace"),                     },                 )         except WorkspaceArchiveWriteError:             raise         except Exception as e:             raise WorkspaceArchiveWriteError(path=root, cause=e) from e         finally:             try:                 await self._exec_internal(                     "rm", "-f", "--", tar_path, timeout=self.state.timeouts.cleanup_s                 )             except Exception as e:                 logger.debug("hydrate cleanup rm failed (non-fatal): %s", e)      # -- PTY -----------------------------------------------------------------      def supports_pty(self) -> bool:         return self.state.sandbox_url is not None and self._token is not None and _has_aiohttp()      async def pty_exec_start(         self,         *command: str | Path,         timeout: float | None = None,         shell: bool | list[str] = True,         user: str | User | None = None,         tty: bool = False,         yield_time_s: float | None = None,         max_output_tokens: int | None = None,     ) -> PtyExecUpdate:         aiohttp = _import_aiohttp()         sanitized = self._prepare_exec_command(*command, shell=shell, user=user)         cmd_str = shlex.join(str(part) for part in sanitized)         cwd = self.state.manifest.root         exec_timeout = timeout if timeout is not None else self.state.timeouts.exec_timeout_s          ws_session_id = f"pty-{uuid.uuid4().hex[:12]}"         ws_url = _build_ws_url(             sandbox_url=self.state.sandbox_url or "",             token=self._token or "",             session_id=ws_session_id,             cwd=cwd,         )          entry = _BlaxelPtySessionEntry(             ws_session_id=ws_session_id,             ws=None,             http_session=None,             tty=True,         )          registered = False         pruned: _BlaxelPtySessionEntry | None = None         process_count = 0          try:             http_session = aiohttp.ClientSession()             entry.http_session = http_session             ws = await asyncio.wait_for(                 http_session.ws_connect(ws_url),                 timeout=exec_timeout,             )             entry.ws = ws              # Start background reader.             entry.reader_task = asyncio.create_task(self._pty_ws_reader(entry))              # Send command.             await asyncio.wait_for(                 ws.send_str(json.dumps({"type": "input", "data": cmd_str + "\n"})),                 timeout=self.state.timeouts.fast_op_s,             )              async with self._pty_lock:                 process_id = allocate_pty_process_id(self._reserved_pty_process_ids)                 self._reserved_pty_process_ids.add(process_id)                 pruned = self._prune_pty_sessions_if_needed()                 self._pty_sessions[process_id] = entry                 process_count = len(self._pty_sessions)                 registered = True         except asyncio.TimeoutError as e:             if not registered:                 await self._terminate_pty_entry(entry)             raise ExecTimeoutError(command=command, timeout_s=exec_timeout, cause=e) from e         except Exception as e:             if not registered:                 await self._terminate_pty_entry(entry)             raise _blaxel_exec_transport_error(command=command, cause=e) from e          if pruned is not None:             await self._terminate_pty_entry(pruned)          if process_count >= PTY_PROCESSES_WARNING:             logger.warning(                 "PTY process count reached warning threshold: %s active sessions",                 process_count,             )          yield_time_ms = 10_000 if yield_time_s is None else int(yield_time_s * 1000)         output, original_token_count = await self._collect_pty_output(             entry=entry,             yield_time_ms=clamp_pty_yield_time_ms(yield_time_ms),             max_output_tokens=max_output_tokens,         )         return await self._finalize_pty_update(             process_id=process_id,             entry=entry,             output=output,             original_token_count=original_token_count,         )      async def pty_write_stdin(         self,         *,         session_id: int,         chars: str,         yield_time_s: float | None = None,         max_output_tokens: int | None = None,     ) -> PtyExecUpdate:         async with self._pty_lock:             entry = self._resolve_pty_session_entry(                 pty_processes=self._pty_sessions,                 session_id=session_id,             )          if chars and entry.ws is not None:             await asyncio.wait_for(                 entry.ws.send_str(json.dumps({"type": "input", "data": chars})),                 timeout=self.state.timeouts.fast_op_s,             )             await asyncio.sleep(0.1)          yield_time_ms = 250 if yield_time_s is None else int(yield_time_s * 1000)         output, original_token_count = await self._collect_pty_output(             entry=entry,             yield_time_ms=resolve_pty_write_yield_time_ms(                 yield_time_ms=yield_time_ms, input_empty=chars == ""             ),             max_output_tokens=max_output_tokens,         )         entry.last_used = time.monotonic()         return await self._finalize_pty_update(             process_id=session_id,             entry=entry,             output=output,             original_token_count=original_token_count,         )      async def pty_terminate_all(self) -> None:         async with self._pty_lock:             entries = list(self._pty_sessions.values())             self._pty_sessions.clear()             self._reserved_pty_process_ids.clear()         for entry in entries:             await self._terminate_pty_entry(entry)      # -- PTY internals -------------------------------------------------------      async def _pty_ws_reader(self, entry: _BlaxelPtySessionEntry) -> None:         """Background task that reads WebSocket messages into *entry.output_chunks*."""         try:             aiohttp = _import_aiohttp()             async for msg in entry.ws:                 if msg.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):                     try:                         raw_text = (                             msg.data                             if isinstance(msg.data, str)                             else msg.data.decode("utf-8", errors="replace")                         )                         data = json.loads(raw_text)                         msg_type = data.get("type", "") or data.get("Type", "")                         if msg_type == "output":                             raw = (data.get("data", "") or data.get("Data", "")).encode(                                 "utf-8", errors="replace"                             )                             async with entry.output_lock:                                 entry.output_chunks.append(raw)                             entry.output_notify.set()                         elif msg_type == "error":                             raw = (data.get("data", "") or data.get("Data", "")).encode(                                 "utf-8", errors="replace"                             )                             async with entry.output_lock:                                 entry.output_chunks.append(raw)                             entry.done = True                             entry.output_notify.set()                     except (json.JSONDecodeError, UnicodeDecodeError):                         logger.debug("PTY ws reader: ignoring malformed message")                 elif msg.type in (                     aiohttp.WSMsgType.ERROR,                     aiohttp.WSMsgType.CLOSE,                     aiohttp.WSMsgType.CLOSING,                 ):                     break         except Exception as e:             logger.debug("PTY ws reader terminated with error: %s", e)         finally:             entry.done = True             entry.output_notify.set()      async def _collect_pty_output(         self,         *,         entry: _BlaxelPtySessionEntry,         yield_time_ms: int,         max_output_tokens: int | None,     ) -> tuple[bytes, int | None]:         return await collect_pty_output(             output_chunks=entry.output_chunks,             output_lock=entry.output_lock,             output_notify=entry.output_notify,             is_done=lambda: entry.done,             yield_time_ms=yield_time_ms,             max_output_tokens=max_output_tokens,         )      async def _finalize_pty_update(         self,         *,         process_id: int,         entry: _BlaxelPtySessionEntry,         output: bytes,         original_token_count: int | None,     ) -> PtyExecUpdate:         exit_code = entry.exit_code if entry.done else None         live_process_id: int | None = process_id          if entry.done:             async with self._pty_lock:                 removed = self._pty_sessions.pop(process_id, None)                 self._reserved_pty_process_ids.discard(process_id)             if removed is not None:                 await self._terminate_pty_entry(removed)             live_process_id = None          return PtyExecUpdate(             process_id=live_process_id,             output=output,             exit_code=exit_code,             original_token_count=original_token_count,         )      def _prune_pty_sessions_if_needed(self) -> _BlaxelPtySessionEntry | None:         if len(self._pty_sessions) < PTY_PROCESSES_MAX:             return None         meta: list[tuple[int, float, bool]] = [             (pid, e.last_used, e.done) for pid, e in self._pty_sessions.items()         ]         pid = process_id_to_prune_from_meta(meta)         if pid is None:             return None         self._reserved_pty_process_ids.discard(pid)         return self._pty_sessions.pop(pid, None)      async def _terminate_pty_entry(self, entry: _BlaxelPtySessionEntry) -> None:         try:             if entry.reader_task is not None and not entry.reader_task.done():                 entry.reader_task.cancel()                 try:                     await entry.reader_task                 except (asyncio.CancelledError, Exception):                     pass             if entry.ws is not None:                 try:                     await entry.ws.close()                 except Exception as e:                     logger.debug("PTY ws close error (non-fatal): %s", e)             if entry.http_session is not None:                 try:                     await entry.http_session.close()                 except Exception as e:                     logger.debug("PTY http session close error (non-fatal): %s", e)         except Exception as e:             logger.debug("PTY entry termination error (non-fatal): %s", e) ``` |

#### supports\_docker\_volume\_mounts

```
supports_docker_volume_mounts() -> bool
```

Return whether this backend attaches Docker volume mounts before manifest apply.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 401 402 403 404 ``` | ``` def supports_docker_volume_mounts(self) -> bool:     """Return whether this backend attaches Docker volume mounts before manifest apply."""      return False ``` |

#### aclose `async`

```
aclose() -> None
```

Run the session cleanup lifecycle outside of `async with`.

This performs the same session-owned cleanup as `__aexit__()`: persist/snapshot the
workspace via `stop()`, tear down session resources via `shutdown()`, and close
session-scoped dependencies. If the session came from a sandbox client, call the client's
`delete()` separately for backend-specific deletion such as removing a Docker container
or deleting a temporary host workspace.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 ``` | ``` async def aclose(self) -> None:     """Run the session cleanup lifecycle outside of ``async with``.      This performs the same session-owned cleanup as ``__aexit__()``: persist/snapshot the     workspace via ``stop()``, tear down session resources via ``shutdown()``, and close     session-scoped dependencies. If the session came from a sandbox client, call the client's     ``delete()`` separately for backend-specific deletion such as removing a Docker container     or deleting a temporary host workspace.     """     try:         await self.run_pre_stop_hooks()         await self.stop()         await self.shutdown()     finally:         await self._aclose_dependencies() ``` |

#### register\_pre\_stop\_hook

```
register_pre_stop_hook(
    hook: Callable[[], Awaitable[None]],
) -> None
```

Register an async hook to run once before the session workspace is persisted.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 477 478 479 480 481 482 483 484 485 ``` | ``` def register_pre_stop_hook(self, hook: Callable[[], Awaitable[None]]) -> None:     """Register an async hook to run once before the session workspace is persisted."""      hooks = self._pre_stop_hooks     if hooks is None:         hooks = []         self._pre_stop_hooks = hooks     hooks.append(hook)     self._pre_stop_hooks_ran = False ``` |

#### run\_pre\_stop\_hooks `async`

```
run_pre_stop_hooks() -> None
```

Run registered pre-stop hooks once before workspace persistence.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 ``` | ``` async def run_pre_stop_hooks(self) -> None:     """Run registered pre-stop hooks once before workspace persistence."""      hooks = self._pre_stop_hooks     if hooks is None or self._pre_stop_hooks_ran:         return     self._pre_stop_hooks_ran = True     cleanup_error: BaseException | None = None     for hook in hooks:         try:             await hook()         except BaseException as exc:             if cleanup_error is None:                 cleanup_error = exc     if cleanup_error is not None:         raise cleanup_error ``` |

#### register\_persist\_workspace\_skip\_path

```
register_persist_workspace_skip_path(
    path: Path | str,
) -> Path
```

Exclude a runtime-created workspace path from future workspace snapshots.

Use this for session side effects that are not part of durable workspace state, such as
generated mount config or ephemeral sink output.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 ``` | ``` def register_persist_workspace_skip_path(self, path: Path | str) -> Path:     """Exclude a runtime-created workspace path from future workspace snapshots.      Use this for session side effects that are not part of durable workspace state, such as     generated mount config or ephemeral sink output.     """      rel_path = Manifest._coerce_rel_path(path)     Manifest._validate_rel_path(rel_path)     if rel_path in (Path(""), Path(".")):         raise ValueError("Persist workspace skip paths must target a concrete relative path.")     overlapping_mounts = self._overlapping_mount_relpaths(rel_path)     if overlapping_mounts:         overlapping_mount = min(overlapping_mounts, key=lambda p: (len(p.parts), p.as_posix()))         raise MountConfigError(             message="persist workspace skip path must not overlap mount path",             context={                 "skip_path": rel_path.as_posix(),                 "mount_path": overlapping_mount.as_posix(),             },         )      if self._runtime_persist_workspace_skip_relpaths is None:         self._runtime_persist_workspace_skip_relpaths = set()     self._runtime_persist_workspace_skip_relpaths.add(rel_path)     return rel_path ``` |

#### exec `async`

```
exec(
    *command: str | Path,
    timeout: float | None = None,
    shell: bool | list[str] = True,
    user: str | User | None = None,
) -> ExecResult
```

Execute a command inside the session.

:param command: Command and args (will be stringified).
:param timeout: Optional wall-clock timeout in seconds.
:param shell: Whether to run this command in a shell. If `True` is provided,
the command will be run prefixed by `sh -lc`. A custom shell prefix may be used
by providing a list.

:returns: An `ExecResult` containing stdout/stderr and exit code.

:raises TimeoutError: If the sandbox cannot complete within `timeout`.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 ``` | ``` async def exec(     self,     *command: str | Path,     timeout: float | None = None,     shell: bool | list[str] = True,     user: str | User | None = None, ) -> ExecResult:     """Execute a command inside the session.      :param command: Command and args (will be stringified).     :param timeout: Optional wall-clock timeout in seconds.     :param shell: Whether to run this command in a shell. If ``True`` is provided,         the command will be run prefixed by ``sh -lc``. A custom shell prefix may be used         by providing a list.      :returns: An ``ExecResult`` containing stdout/stderr and exit code.      :raises TimeoutError: If the sandbox cannot complete within `timeout`.     """      sanitized_command = self._prepare_exec_command(*command, shell=shell, user=user)     return await self._exec_internal(*sanitized_command, timeout=timeout) ``` |

#### ls `async`

```
ls(
    path: Path | str, *, user: str | User | None = None
) -> list[FileEntry]
```

List directory contents.

:param path: Path to list.
:param user: Optional sandbox user to list as.
:returns: A list of `FileEntry` objects.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 ``` | ``` async def ls(     self,     path: Path | str,     *,     user: str | User | None = None, ) -> list[FileEntry]:     """List directory contents.      :param path: Path to list.     :param user: Optional sandbox user to list as.     :returns: A list of `FileEntry` objects.     """     path = await self._validate_path_access(path)      path_arg = sandbox_path_str(path)     cmd = ("ls", "-la", "--", path_arg)     result = await self.exec(*cmd, shell=False, user=user)     if not result.ok():         raise ExecNonZeroError(result, command=cmd)      return parse_ls_la(result.stdout.decode("utf-8", errors="replace"), base=path_arg) ``` |

#### rm `async`

```
rm(
    path: Path | str,
    *,
    recursive: bool = False,
    user: str | User | None = None,
) -> None
```

Remove a file or directory.

:param path: Path to remove.
:param recursive: If true, remove directories recursively.
:param user: Optional sandbox user to remove as.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 ``` | ``` async def rm(     self,     path: Path | str,     *,     recursive: bool = False,     user: str | User | None = None, ) -> None:     """Remove a file or directory.      :param path: Path to remove.     :param recursive: If true, remove directories recursively.     :param user: Optional sandbox user to remove as.     """     path = await self._validate_path_access(path, for_write=True)      cmd: list[str] = ["rm"]     if recursive:         cmd.append("-rf")     cmd.extend(["--", sandbox_path_str(path)])      result = await self.exec(*cmd, shell=False, user=user)     if not result.ok():         raise ExecNonZeroError(result, command=cmd) ``` |

#### extract `async`

```
extract(
    path: Path | str,
    data: IOBase,
    *,
    compression_scheme: Literal["tar", "zip"] | None = None,
    archive_limits: SandboxArchiveLimits | None = None,
) -> None
```

Write a compressed archive to a destination on the remote.
Optionally extract the archive once written.

:param path: Path on the host machine to extract to
:param data: a file-like io stream.
:param compression\_scheme: either "tar" or "zip". If not provided,
it will try to infer from the path.
:param archive\_limits: optional per-call archive resource limits. If omitted,
the session default is used.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 ``` | ``` async def extract(     self,     path: Path | str,     data: io.IOBase,     *,     compression_scheme: Literal["tar", "zip"] | None = None,     archive_limits: SandboxArchiveLimits | None = None, ) -> None:     """     Write a compressed archive to a destination on the remote.     Optionally extract the archive once written.      :param path: Path on the host machine to extract to     :param data: a file-like io stream.     :param compression_scheme: either "tar" or "zip". If not provided,         it will try to infer from the path.     :param archive_limits: optional per-call archive resource limits. If omitted,         the session default is used.     """     if archive_limits is not None:         archive_limits.validate()     effective_archive_limits = (         archive_limits if archive_limits is not None else self._archive_limits     )      await archive_ops.extract_archive(         self,         path,         data,         compression_scheme=compression_scheme,         archive_limits=effective_archive_limits,     ) ``` |

#### should\_provision\_manifest\_accounts\_on\_resume

```
should_provision_manifest_accounts_on_resume() -> bool
```

Return whether resume should reprovision manifest-managed users and groups.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 1215 1216 1217 1218 ``` | ``` def should_provision_manifest_accounts_on_resume(self) -> bool:     """Return whether resume should reprovision manifest-managed users and groups."""      return not self._system_state_preserved_on_start() ``` |

### BlaxelSandboxClient

Bases: `BaseSandboxClient['BlaxelSandboxClientOptions']`

Blaxel sandbox client managing sandbox lifecycle via the Blaxel SDK.

Source code in `src/agents/extensions/sandbox/blaxel/sandbox.py`

|  |  |
| --- | --- |
| ``` 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 1079 1080 1081 1082 1083 1084 1085 1086 1087 1088 1089 1090 1091 1092 1093 1094 1095 1096 1097 1098 1099 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 1136 1137 1138 1139 1140 1141 1142 1143 1144 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 ``` | ``` class BlaxelSandboxClient(BaseSandboxClient["BlaxelSandboxClientOptions"]):     """Blaxel sandbox client managing sandbox lifecycle via the Blaxel SDK."""      backend_id = "blaxel"     _instrumentation: Instrumentation     _token: str | None      def __init__(         self,         *,         token: str | None = None,         instrumentation: Instrumentation | None = None,         dependencies: Dependencies | None = None,     ) -> None:         # Validate that the Blaxel SDK is importable.         _import_blaxel_sdk()         self._instrumentation = instrumentation or Instrumentation()         self._dependencies = dependencies         self._token = token or os.environ.get("BL_API_KEY")      async def create(         self,         *,         snapshot: SnapshotSpec | SnapshotBase | None = None,         manifest: Manifest | None = None,         options: BlaxelSandboxClientOptions,     ) -> SandboxSession:         if manifest is None:             manifest = Manifest(root=DEFAULT_BLAXEL_WORKSPACE_ROOT)          timeouts_in = options.timeouts         if isinstance(timeouts_in, BlaxelTimeouts):             timeouts = timeouts_in         elif timeouts_in is None:             timeouts = BlaxelTimeouts()         else:             timeouts = BlaxelTimeouts.model_validate(timeouts_in)          session_id = uuid.uuid4()         sandbox_name = options.name or f"agents-{session_id.hex[:12]}"          SandboxInstance = _import_blaxel_sdk()         create_config = _build_create_config(             name=sandbox_name,             image=options.image,             memory=options.memory,             region=options.region,             ports=options.ports,             env_vars=options.env_vars,             labels=options.labels,             ttl=options.ttl,             manifest=manifest,         )         blaxel_sandbox = await SandboxInstance.create_if_not_exists(create_config)          sandbox_url = _get_sandbox_url(blaxel_sandbox)         snapshot_instance = resolve_snapshot(snapshot, str(session_id))         state = BlaxelSandboxSessionState(             session_id=session_id,             manifest=manifest,             snapshot=snapshot_instance,             sandbox_name=sandbox_name,             image=options.image,             memory=options.memory,             region=options.region,             base_env_vars=dict(options.env_vars or {}),             labels=dict(options.labels or {}),             ttl=options.ttl,             pause_on_exit=options.pause_on_exit,             timeouts=timeouts,             sandbox_url=sandbox_url,             exposed_port_public=options.exposed_port_public,             exposed_port_url_ttl_s=options.exposed_port_url_ttl_s,         )         inner = BlaxelSandboxSession.from_state(state, sandbox=blaxel_sandbox, token=self._token)         return self._wrap_session(inner, instrumentation=self._instrumentation)      async def close(self) -> None:         """No persistent HTTP client to close; provided for API symmetry."""      async def __aenter__(self) -> BlaxelSandboxClient:         return self      async def __aexit__(self, *_: object) -> None:         await self.close()      async def delete(self, session: SandboxSession) -> SandboxSession:         inner = session._inner         if not isinstance(inner, BlaxelSandboxSession):             raise TypeError("BlaxelSandboxClient.delete expects a BlaxelSandboxSession")         try:             await inner.shutdown()         except Exception as e:             logger.warning("shutdown error during delete (non-fatal): %s", e)         return session      async def resume(         self,         state: SandboxSessionState,     ) -> SandboxSession:         """Resume a sandbox from persisted state.          When ``pause_on_exit`` is set, Blaxel automatically resumes the paused         sandbox on connection -- this method simply reconnects by sandbox name         via ``SandboxInstance.get()``.  If the sandbox is no longer available         (e.g. it expired), a fresh one is created with the same configuration.         """         if not isinstance(state, BlaxelSandboxSessionState):             raise TypeError("BlaxelSandboxClient.resume expects a BlaxelSandboxSessionState")          SandboxInstance = _import_blaxel_sdk()         blaxel_sandbox = None         reconnected = False          if state.pause_on_exit:             try:                 blaxel_sandbox = await SandboxInstance.get(state.sandbox_name)                 reconnected = True             except Exception as e:                 logger.debug("sandbox get() failed, will recreate: %s", e)          if not reconnected or blaxel_sandbox is None:             create_config = _build_create_config(                 name=state.sandbox_name,                 image=state.image,                 memory=state.memory,                 region=state.region,                 env_vars=state.base_env_vars or None,                 labels=state.labels or None,                 ttl=state.ttl,             )             blaxel_sandbox = await SandboxInstance.create_if_not_exists(create_config)          sandbox_url = _get_sandbox_url(blaxel_sandbox)         if sandbox_url:             state.sandbox_url = sandbox_url          inner = BlaxelSandboxSession.from_state(state, sandbox=blaxel_sandbox, token=self._token)         if state.pause_on_exit and reconnected:             inner._skip_start = True  # type: ignore[attr-defined]         return self._wrap_session(inner, instrumentation=self._instrumentation)      def deserialize_session_state(self, payload: dict[str, object]) -> SandboxSessionState:         return BlaxelSandboxSessionState.model_validate(payload) ``` |

#### close `async`

```
close() -> None
```

No persistent HTTP client to close; provided for API symmetry.

Source code in `src/agents/extensions/sandbox/blaxel/sandbox.py`

|  |  |
| --- | --- |
| ``` 1113 1114 ``` | ``` async def close(self) -> None:     """No persistent HTTP client to close; provided for API symmetry.""" ``` |

#### resume `async`

```
resume(state: SandboxSessionState) -> SandboxSession
```

Resume a sandbox from persisted state.

When `pause_on_exit` is set, Blaxel automatically resumes the paused
sandbox on connection -- this method simply reconnects by sandbox name
via `SandboxInstance.get()`. If the sandbox is no longer available
(e.g. it expired), a fresh one is created with the same configuration.

Source code in `src/agents/extensions/sandbox/blaxel/sandbox.py`

|  |  |
| --- | --- |
| ``` 1132 1133 1134 1135 1136 1137 1138 1139 1140 1141 1142 1143 1144 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 ``` | ``` async def resume(     self,     state: SandboxSessionState, ) -> SandboxSession:     """Resume a sandbox from persisted state.      When ``pause_on_exit`` is set, Blaxel automatically resumes the paused     sandbox on connection -- this method simply reconnects by sandbox name     via ``SandboxInstance.get()``.  If the sandbox is no longer available     (e.g. it expired), a fresh one is created with the same configuration.     """     if not isinstance(state, BlaxelSandboxSessionState):         raise TypeError("BlaxelSandboxClient.resume expects a BlaxelSandboxSessionState")      SandboxInstance = _import_blaxel_sdk()     blaxel_sandbox = None     reconnected = False      if state.pause_on_exit:         try:             blaxel_sandbox = await SandboxInstance.get(state.sandbox_name)             reconnected = True         except Exception as e:             logger.debug("sandbox get() failed, will recreate: %s", e)      if not reconnected or blaxel_sandbox is None:         create_config = _build_create_config(             name=state.sandbox_name,             image=state.image,             memory=state.memory,             region=state.region,             env_vars=state.base_env_vars or None,             labels=state.labels or None,             ttl=state.ttl,         )         blaxel_sandbox = await SandboxInstance.create_if_not_exists(create_config)      sandbox_url = _get_sandbox_url(blaxel_sandbox)     if sandbox_url:         state.sandbox_url = sandbox_url      inner = BlaxelSandboxSession.from_state(state, sandbox=blaxel_sandbox, token=self._token)     if state.pause_on_exit and reconnected:         inner._skip_start = True  # type: ignore[attr-defined]     return self._wrap_session(inner, instrumentation=self._instrumentation) ``` |

#### serialize\_session\_state

```
serialize_session_state(
    state: SandboxSessionState,
) -> dict[str, object]
```

Serialize backend-specific sandbox state into a JSON-compatible payload.

Source code in `src/agents/sandbox/session/sandbox_client.py`

|  |  |
| --- | --- |
| ``` 173 174 175 ``` | ``` def serialize_session_state(self, state: SandboxSessionState) -> dict[str, object]:     """Serialize backend-specific sandbox state into a JSON-compatible payload."""     return state.model_dump(mode="json") ``` |