---
url: https://openai.github.io/openai-agents-python/ref/extensions/sandbox/daytona/sandbox/
title: `Sandbox`
framework: openai
---

# `Sandbox`

Daytona sandbox (https://daytona.io) implementation.

This module provides a Daytona-backed sandbox client/session implementation backed by
`daytona.Sandbox` via the AsyncDaytona client.

The `daytona` dependency is optional, so package-level exports should guard imports of this
module. Within this module, Daytona SDK imports are lazy so users without the extra can still
import the package.

### DaytonaSandboxResources

Bases: `BaseModel`

Resource configuration for a Daytona sandbox.

Source code in `src/agents/extensions/sandbox/daytona/sandbox.py`

|  |  |
| --- | --- |
| ``` 284 285 286 287 288 289 290 291 ``` | ``` class DaytonaSandboxResources(BaseModel):     """Resource configuration for a Daytona sandbox."""      model_config = {"frozen": True}      cpu: int | None = None     memory: int | None = None     disk: int | None = None ``` |

### DaytonaSandboxTimeouts

Bases: `BaseModel`

Timeout configuration for Daytona sandbox operations.

Source code in `src/agents/extensions/sandbox/daytona/sandbox.py`

|  |  |
| --- | --- |
| ``` 294 295 296 297 298 299 300 301 302 303 ``` | ``` class DaytonaSandboxTimeouts(BaseModel):     """Timeout configuration for Daytona sandbox operations."""      exec_timeout_unbounded_s: int = Field(default=24 * 60 * 60, ge=1)     keepalive_s: int = Field(default=10, ge=1)     cleanup_s: int = Field(default=30, ge=1)     fast_op_s: int = Field(default=30, ge=1)     file_upload_s: int = Field(default=1800, ge=1)     file_download_s: int = Field(default=1800, ge=1)     workspace_tar_s: int = Field(default=300, ge=1) ``` |

### DaytonaSandboxClientOptions

Bases: `BaseSandboxClientOptions`

Client options for the Daytona sandbox.

Source code in `src/agents/extensions/sandbox/daytona/sandbox.py`

|  |  |
| --- | --- |
| ``` 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 ``` | ``` class DaytonaSandboxClientOptions(BaseSandboxClientOptions):     """Client options for the Daytona sandbox."""      type: Literal["daytona"] = "daytona"     sandbox_snapshot_name: str | None = None     image: str | None = None     resources: DaytonaSandboxResources | None = None     env_vars: dict[str, str] | None = None     pause_on_exit: bool = False     create_timeout: int = 60     start_timeout: int = 60     name: str | None = None     auto_stop_interval: int = 0     timeouts: DaytonaSandboxTimeouts | dict[str, object] | None = None     exposed_ports: tuple[int, ...] = ()     # This TTL applies to new connection setup only: Daytona checks signed preview URL expiry during     # the initial HTTP request / websocket upgrade handshake. In live testing, an already-open     # websocket stayed connected after the URL expired, but any reconnect or new handshake needed a     # freshly resolved URL.     exposed_port_url_ttl_s: int = 3600      def __init__(         self,         sandbox_snapshot_name: str | None = None,         image: str | None = None,         resources: DaytonaSandboxResources | None = None,         env_vars: dict[str, str] | None = None,         pause_on_exit: bool = False,         create_timeout: int = 60,         start_timeout: int = 60,         name: str | None = None,         auto_stop_interval: int = 0,         timeouts: DaytonaSandboxTimeouts | dict[str, object] | None = None,         exposed_ports: tuple[int, ...] = (),         exposed_port_url_ttl_s: int = 3600,         *,         type: Literal["daytona"] = "daytona",     ) -> None:         super().__init__(             type=type,             sandbox_snapshot_name=sandbox_snapshot_name,             image=image,             resources=resources,             env_vars=env_vars,             pause_on_exit=pause_on_exit,             create_timeout=create_timeout,             start_timeout=start_timeout,             name=name,             auto_stop_interval=auto_stop_interval,             timeouts=timeouts,             exposed_ports=exposed_ports,             exposed_port_url_ttl_s=exposed_port_url_ttl_s,         ) ``` |

### DaytonaSandboxSessionState

Bases: `SandboxSessionState`

Serializable state for a Daytona-backed session.

Source code in `src/agents/extensions/sandbox/daytona/sandbox.py`

|  |  |
| --- | --- |
| ``` 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 ``` | ``` class DaytonaSandboxSessionState(SandboxSessionState):     """Serializable state for a Daytona-backed session."""      type: Literal["daytona"] = "daytona"     sandbox_id: str     sandbox_snapshot_name: str | None = None     image: str | None = None     base_env_vars: dict[str, str] = Field(default_factory=dict)     pause_on_exit: bool = False     create_timeout: int = 60     start_timeout: int = 60     name: str | None = None     resources: DaytonaSandboxResources | None = None     auto_stop_interval: int = 0     timeouts: DaytonaSandboxTimeouts = Field(default_factory=DaytonaSandboxTimeouts)     exposed_port_url_ttl_s: int = 3600 ``` |

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

### DaytonaSandboxSession

Bases: `BaseSandboxSession`

Daytona-backed sandbox session implementation.

Source code in `src/agents/extensions/sandbox/daytona/sandbox.py`

|  |  |
| --- | --- |
| ```  394  395  396  397  398  399  400  401  402  403  404  405  406  407  408  409  410  411  412  413  414  415  416  417  418  419  420  421  422  423  424  425  426  427  428  429  430  431  432  433  434  435  436  437  438  439  440  441  442  443  444  445  446  447  448  449  450  451  452  453  454  455  456  457  458  459  460  461  462  463  464  465  466  467  468  469  470  471  472  473  474  475  476  477  478  479  480  481  482  483  484  485  486  487  488  489  490  491  492  493  494  495  496  497  498  499  500  501  502  503  504  505  506  507  508  509  510  511  512  513  514  515  516  517  518  519  520  521  522  523  524  525  526  527  528  529  530  531  532  533  534  535  536  537  538  539  540  541  542  543  544  545  546  547  548  549  550  551  552  553  554  555  556  557  558  559  560  561  562  563  564  565  566  567  568  569  570  571  572  573  574  575  576  577  578  579  580  581  582  583  584  585  586  587  588  589  590  591  592  593  594  595  596  597  598  599  600  601  602  603  604  605  606  607  608  609  610  611  612  613  614  615  616  617  618  619  620  621  622  623  624  625  626  627  628  629  630  631  632  633  634  635  636  637  638  639  640  641  642  643  644  645  646  647  648  649  650  651  652  653  654  655  656  657  658  659  660  661  662  663  664  665  666  667  668  669  670  671  672  673  674  675  676  677  678  679  680  681  682  683  684  685  686  687  688  689  690  691  692  693  694  695  696  697  698  699  700  701  702  703  704  705  706  707  708  709  710  711  712  713  714  715  716  717  718  719  720  721  722  723  724  725  726  727  728  729  730  731  732  733  734  735  736  737  738  739  740  741  742  743  744  745  746  747  748  749  750  751  752  753  754  755  756  757  758  759  760  761  762  763  764  765  766  767  768  769  770  771  772  773  774  775  776  777  778  779  780  781  782  783  784  785  786  787  788  789  790  791  792  793  794  795  796  797  798  799  800  801  802  803  804  805  806  807  808  809  810  811  812  813  814  815  816  817  818  819  820  821  822  823  824  825  826  827  828  829  830  831  832  833  834  835  836  837  838  839  840  841  842  843  844  845  846  847  848  849  850  851  852  853  854  855  856  857  858  859  860  861  862  863  864  865  866  867  868  869  870  871  872  873  874  875  876  877  878  879  880  881  882  883  884  885  886  887  888  889  890  891  892  893  894  895  896  897  898  899  900  901  902  903  904  905  906  907  908  909  910  911  912  913  914  915  916  917  918  919  920  921  922  923  924  925  926  927  928  929  930  931  932  933  934  935  936  937  938  939  940  941  942  943  944  945  946  947  948  949  950  951  952  953  954  955  956  957  958  959  960  961  962  963  964  965  966  967  968  969  970  971  972  973  974  975  976  977  978  979  980  981  982  983  984  985  986  987  988  989  990  991  992  993  994  995  996  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 1079 1080 1081 1082 1083 1084 1085 1086 1087 1088 1089 1090 1091 1092 1093 1094 1095 1096 1097 1098 1099 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 1136 1137 1138 1139 1140 1141 1142 1143 1144 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 ``` | ``` class DaytonaSandboxSession(BaseSandboxSession):     """Daytona-backed sandbox session implementation."""      state: DaytonaSandboxSessionState     _sandbox: Any     _pty_lock: asyncio.Lock     _pty_sessions: dict[int, _DaytonaPtySessionEntry]     _reserved_pty_process_ids: set[int]      def __init__(self, *, state: DaytonaSandboxSessionState, sandbox: Any) -> None:         self.state = state         self._sandbox = sandbox         self._pty_lock = asyncio.Lock()         self._pty_sessions = {}         self._reserved_pty_process_ids = set()      @classmethod     def from_state(         cls,         state: DaytonaSandboxSessionState,         *,         sandbox: Any,     ) -> DaytonaSandboxSession:         return cls(state=state, sandbox=sandbox)      @property     def sandbox_id(self) -> str:         return self.state.sandbox_id      async def _resolve_exposed_port(self, port: int) -> ExposedPortEndpoint:         try:             preview = await self._sandbox.create_signed_preview_url(                 port,                 expires_in_seconds=self.state.exposed_port_url_ttl_s,             )         except Exception as e:             raise ExposedPortUnavailableError(                 port=port,                 exposed_ports=self.state.exposed_ports,                 reason="backend_unavailable",                 context={"backend": "daytona", "detail": "create_signed_preview_url_failed"},                 cause=e,             ) from e          url = getattr(preview, "url", None)         if not isinstance(url, str) or not url:             raise ExposedPortUnavailableError(                 port=port,                 exposed_ports=self.state.exposed_ports,                 reason="backend_unavailable",                 context={"backend": "daytona", "detail": "invalid_preview_url", "url": url},             )          try:             split = urlsplit(url)             host = split.hostname             if host is None:                 raise ValueError("missing hostname")             port_value = split.port or (443 if split.scheme == "https" else 80)             return ExposedPortEndpoint(host=host, port=port_value, tls=split.scheme == "https")         except Exception as e:             raise ExposedPortUnavailableError(                 port=port,                 exposed_ports=self.state.exposed_ports,                 reason="backend_unavailable",                 context={"backend": "daytona", "detail": "invalid_preview_url", "url": url},                 cause=e,             ) from e      async def _shutdown_backend(self) -> None:         try:             if self.state.pause_on_exit:                 await self._sandbox.stop()             else:                 await self._sandbox.delete()         except Exception:             pass      async def _validate_path_access(self, path: Path | str, *, for_write: bool = False) -> Path:         return await self._validate_remote_path_access(path, for_write=for_write)      def _runtime_helpers(self) -> tuple[RuntimeHelperScript, ...]:         return (RESOLVE_WORKSPACE_PATH_HELPER,)      async def _prepare_workspace_root(self) -> None:         """Create the workspace root before SDK exec calls use it as cwd."""         root = sandbox_path_str(self.state.manifest.root)         error_root = posix_path_for_error(root)         try:             envs = await self._resolved_envs()             result = await self._sandbox.process.exec(                 f"mkdir -p -- {shlex.quote(root)}",                 env=envs or None,                 timeout=self.state.timeouts.fast_op_s,             )         except Exception as e:             detail = _daytona_provider_error_detail(e)             message = "failed to start session"             if detail:                 message = f"{message}: Daytona workspace root setup failed: {detail}"             raise WorkspaceStartError(                 path=error_root,                 context={"backend": "daytona", "reason": "workspace_root_setup_failed"},                 cause=e,                 message=message,             ) from e          exit_code = int(getattr(result, "exit_code", 0) or 0)         if exit_code != 0:             output = str(getattr(result, "result", "") or "")             message = (                 f"failed to start session: Daytona workspace root setup exited with {exit_code}"             )             if output:                 message = f"{message}: {output}"             raise WorkspaceStartError(                 path=error_root,                 context={                     "backend": "daytona",                     "reason": "workspace_root_nonzero_exit",                     "exit_code": exit_code,                     "output": output,                 },                 message=message,             )      async def _prepare_backend_workspace(self) -> None:         await self._prepare_workspace_root()      async def mkdir(         self,         path: Path | str,         *,         parents: bool = False,         user: str | User | None = None,     ) -> None:         if user is not None:             path = await self._check_mkdir_with_exec(path, parents=parents, user=user)         else:             path = await self._validate_path_access(path, for_write=True)         if path == Path("/"):             return         try:             await self._sandbox.fs.create_folder(sandbox_path_str(path), "755")         except Exception as e:             raise WorkspaceArchiveWriteError(                 path=path,                 context={"reason": "mkdir_failed"},                 cause=e,             ) from e      async def _resolved_envs(self) -> dict[str, str]:         manifest_envs = await self.state.manifest.environment.resolve()         return {**self.state.base_env_vars, **manifest_envs}      def _coerce_exec_timeout(self, timeout_s: float | None) -> float:         if timeout_s is None:             return float(self.state.timeouts.exec_timeout_unbounded_s)         if timeout_s <= 0:             return 0.001         return float(timeout_s)      async def _exec_internal(         self,         *command: str | Path,         timeout: float | None = None,     ) -> ExecResult:         cmd_str = shlex.join(str(c) for c in command)         envs = await self._resolved_envs()         cwd = sandbox_path_str(self.state.manifest.root)         env_args = (             " ".join(shlex.quote(f"{key}={value}") for key, value in envs.items()) if envs else ""         )         env_wrapper = f"env -- {env_args} " if env_args else ""         session_cmd = f"cd {shlex.quote(cwd)} && {env_wrapper}{cmd_str}"         daytona_session_id = f"sandbox-{uuid.uuid4().hex[:12]}"          caller_timeout = self._coerce_exec_timeout(timeout)         deadline = time.monotonic() + caller_timeout         SessionExecuteRequest = _import_session_execute_request()         timeout_error_types = _daytona_timeout_error_types()          def _remaining_timeout() -> float:             return max(0.0, deadline - time.monotonic())          try:             await asyncio.wait_for(                 self._sandbox.process.create_session(daytona_session_id),                 timeout=_remaining_timeout(),             )             command_timeout = _remaining_timeout()             sdk_timeout = max(1, math.ceil(command_timeout + 1.0))             result = await asyncio.wait_for(                 self._sandbox.process.execute_session_command(                     daytona_session_id,                     SessionExecuteRequest(command=session_cmd, run_async=False),                     timeout=sdk_timeout,                 ),                 timeout=caller_timeout,             )             exit_code = int(result.exit_code or 0)             stdout = getattr(result, "stdout", None)             stderr = getattr(result, "stderr", None)             if stdout is None and stderr is None:                 output = getattr(result, "output", "") or ""                 if exit_code == 0:                     stdout = output                     stderr = ""                 else:                     stdout = ""                     stderr = output             return ExecResult(                 stdout=(stdout or "").encode("utf-8", errors="replace"),                 stderr=(stderr or "").encode("utf-8", errors="replace"),                 exit_code=exit_code,             )         except asyncio.TimeoutError as e:             raise ExecTimeoutError(command=command, timeout_s=timeout, cause=e) from e         except Exception as e:             if timeout_error_types and isinstance(e, timeout_error_types):                 raise ExecTimeoutError(command=command, timeout_s=timeout, cause=e) from e             raise _daytona_exec_transport_error(command=command, cause=e) from e         finally:             try:                 await asyncio.wait_for(                     self._sandbox.process.delete_session(daytona_session_id),                     timeout=self.state.timeouts.cleanup_s,                 )             except Exception:                 pass      def supports_pty(self) -> bool:         return True      async def pty_exec_start(         self,         *command: str | Path,         timeout: float | None = None,         shell: bool | list[str] = True,         user: str | User | None = None,         tty: bool = False,         yield_time_s: float | None = None,         max_output_tokens: int | None = None,     ) -> PtyExecUpdate:         PtySize = _import_pty_size()         sanitized = self._prepare_exec_command(*command, shell=shell, user=user)         cmd_str = shlex.join(str(part) for part in sanitized)         envs = await self._resolved_envs()         cwd = sandbox_path_str(self.state.manifest.root)         exec_timeout = self._coerce_exec_timeout(timeout)         timeout_error_types = _daytona_timeout_error_types()          daytona_session_id = f"sandbox-{uuid.uuid4().hex[:12]}"         entry = _DaytonaPtySessionEntry(             daytona_session_id=daytona_session_id,             pty_handle=None,             tty=tty,         )          async def _on_data(chunk: bytes | str) -> None:             raw = (                 chunk.encode("utf-8", errors="replace") if isinstance(chunk, str) else bytes(chunk)             )             async with entry.output_lock:                 entry.output_chunks.append(raw)             entry.output_notify.set()          pruned: _DaytonaPtySessionEntry | None = None         registered = False         try:             if tty:                 pty_handle = await asyncio.wait_for(                     self._sandbox.process.create_pty_session(                         id=daytona_session_id,                         on_data=_on_data,                         cwd=cwd,                         envs=envs or None,                         pty_size=PtySize(cols=80, rows=24),                     ),                     timeout=exec_timeout,                 )                 entry.pty_handle = pty_handle                 entry.worker_task = asyncio.create_task(self._run_pty_waiter(entry))                 await asyncio.wait_for(pty_handle.wait_for_connection(), timeout=exec_timeout)                 await asyncio.wait_for(                     pty_handle.send_input(cmd_str + "\n"),                     timeout=self.state.timeouts.fast_op_s,                 )             else:                 SessionExecuteRequest = _import_session_execute_request()                 env_args = (                     " ".join(shlex.quote(f"{key}={value}") for key, value in envs.items())                     if envs                     else ""                 )                 env_wrapper = f"env -- {env_args} " if env_args else ""                 session_cmd = f"cd {shlex.quote(cwd)} && {env_wrapper}{cmd_str}"                 await asyncio.wait_for(                     self._sandbox.process.create_session(daytona_session_id),                     timeout=exec_timeout,                 )                 resp = await asyncio.wait_for(                     self._sandbox.process.execute_session_command(                         daytona_session_id,                         SessionExecuteRequest(command=session_cmd, run_async=True),                     ),                     timeout=exec_timeout,                 )                 entry.cmd_id = resp.cmd_id                 entry.worker_task = asyncio.create_task(                     self._run_session_reader(                         entry,                         daytona_session_id,                         resp.cmd_id,                         _on_data,                     )                 )              async with self._pty_lock:                 process_id = allocate_pty_process_id(self._reserved_pty_process_ids)                 self._reserved_pty_process_ids.add(process_id)                 pruned = self._prune_pty_sessions_if_needed()                 self._pty_sessions[process_id] = entry                 process_count = len(self._pty_sessions)                 registered = True         except asyncio.TimeoutError as e:             if not registered:                 cleanup_task = asyncio.ensure_future(self._terminate_pty_entry(entry))                 try:                     await asyncio.shield(cleanup_task)                 except BaseException:                     await asyncio.shield(cleanup_task)             raise ExecTimeoutError(command=command, timeout_s=timeout, cause=e) from e         except Exception as e:             if not registered:                 cleanup_task = asyncio.ensure_future(self._terminate_pty_entry(entry))                 try:                     await asyncio.shield(cleanup_task)                 except BaseException:                     await asyncio.shield(cleanup_task)             if timeout_error_types and isinstance(e, timeout_error_types):                 raise ExecTimeoutError(command=command, timeout_s=timeout, cause=e) from e             raise _daytona_exec_transport_error(command=command, cause=e) from e         except BaseException:             if not registered:                 cleanup_task = asyncio.ensure_future(self._terminate_pty_entry(entry))                 try:                     await asyncio.shield(cleanup_task)                 except BaseException:                     await asyncio.shield(cleanup_task)             raise          if pruned is not None:             await self._terminate_pty_entry(pruned)          if process_count >= PTY_PROCESSES_WARNING:             logger.warning(                 "PTY process count reached warning threshold: %s active sessions",                 process_count,             )          yield_time_ms = 10_000 if yield_time_s is None else int(yield_time_s * 1000)         output, original_token_count = await self._collect_pty_output(             entry=entry,             yield_time_ms=clamp_pty_yield_time_ms(yield_time_ms),             max_output_tokens=max_output_tokens,         )         return await self._finalize_pty_update(             process_id=process_id,             entry=entry,             output=output,             original_token_count=original_token_count,         )      async def _run_pty_waiter(self, entry: _DaytonaPtySessionEntry) -> None:         try:             await entry.pty_handle.wait()             ec = getattr(entry.pty_handle, "exit_code", None)             if ec is not None:                 entry.exit_code = int(ec)         except Exception:             pass         finally:             entry.done = True             entry.output_notify.set()      async def _run_session_reader(         self,         entry: _DaytonaPtySessionEntry,         session_id: str,         cmd_id: str,         on_data: Any,     ) -> None:         logs_failed = False         try:             await self._sandbox.process.get_session_command_logs_async(                 session_id,                 cmd_id,                 on_data,                 on_data,             )         except Exception:             logs_failed = True         finally:             try:                 cmd = await self._sandbox.process.get_session_command(session_id, cmd_id)                 if cmd.exit_code is not None:                     entry.exit_code = int(cmd.exit_code)                     entry.done = True             except Exception:                 pass             if not logs_failed:                 entry.done = True             entry.output_notify.set()      async def pty_write_stdin(         self,         *,         session_id: int,         chars: str,         yield_time_s: float | None = None,         max_output_tokens: int | None = None,     ) -> PtyExecUpdate:         async with self._pty_lock:             entry = self._resolve_pty_session_entry(                 pty_processes=self._pty_sessions,                 session_id=session_id,             )          if chars:             if not entry.tty:                 raise RuntimeError("stdin is not available for this process")             await asyncio.wait_for(                 entry.pty_handle.send_input(chars),                 timeout=self.state.timeouts.fast_op_s,             )             await asyncio.sleep(0.1)          yield_time_ms = 250 if yield_time_s is None else int(yield_time_s * 1000)         output, original_token_count = await self._collect_pty_output(             entry=entry,             yield_time_ms=resolve_pty_write_yield_time_ms(                 yield_time_ms=yield_time_ms, input_empty=chars == ""             ),             max_output_tokens=max_output_tokens,         )         entry.last_used = time.monotonic()         return await self._finalize_pty_update(             process_id=session_id,             entry=entry,             output=output,             original_token_count=original_token_count,         )      async def _finalize_pty_update(         self,         *,         process_id: int,         entry: _DaytonaPtySessionEntry,         output: bytes,         original_token_count: int | None,     ) -> PtyExecUpdate:         exit_code = entry.exit_code if entry.done else None         live_process_id: int | None = process_id          if entry.done:             async with self._pty_lock:                 removed = self._pty_sessions.pop(process_id, None)                 self._reserved_pty_process_ids.discard(process_id)             if removed is not None:                 await self._terminate_pty_entry(removed)             live_process_id = None          return PtyExecUpdate(             process_id=live_process_id,             output=output,             exit_code=exit_code,             original_token_count=original_token_count,         )      async def pty_terminate_all(self) -> None:         async with self._pty_lock:             entries = list(self._pty_sessions.values())             self._pty_sessions.clear()             self._reserved_pty_process_ids.clear()         for entry in entries:             await self._terminate_pty_entry(entry)      async def _collect_pty_output(         self,         *,         entry: _DaytonaPtySessionEntry,         yield_time_ms: int,         max_output_tokens: int | None,     ) -> tuple[bytes, int | None]:         return await collect_pty_output(             output_chunks=entry.output_chunks,             output_lock=entry.output_lock,             output_notify=entry.output_notify,             is_done=lambda: entry.done,             yield_time_ms=yield_time_ms,             max_output_tokens=max_output_tokens,         )      def _prune_pty_sessions_if_needed(self) -> _DaytonaPtySessionEntry | None:         if len(self._pty_sessions) < PTY_PROCESSES_MAX:             return None         meta: list[tuple[int, float, bool]] = [             (pid, entry.last_used, entry.done) for pid, entry in self._pty_sessions.items()         ]         pid = process_id_to_prune_from_meta(meta)         if pid is None:             return None         self._reserved_pty_process_ids.discard(pid)         return self._pty_sessions.pop(pid, None)      async def _terminate_pty_entry(self, entry: _DaytonaPtySessionEntry) -> None:         try:             if entry.tty:                 await self._sandbox.process.kill_pty_session(entry.daytona_session_id)             else:                 await self._sandbox.process.delete_session(entry.daytona_session_id)         except Exception:             pass         finally:             worker_task = entry.worker_task             entry.worker_task = None             if worker_task is not None and worker_task is not asyncio.current_task():                 if not worker_task.done():                     worker_task.cancel()                 try:                     await asyncio.wait_for(                         asyncio.gather(worker_task, return_exceptions=True),                         timeout=self.state.timeouts.cleanup_s,                     )                 except asyncio.TimeoutError:                     pass      async def read(self, path: Path | str, *, user: str | User | None = None) -> io.IOBase:         error_path = posix_path_as_path(coerce_posix_path(path))         if user is not None:             workspace_path = await self._check_read_with_exec(path, user=user)         else:             workspace_path = await self._validate_path_access(path)          not_found_error_types = _daytona_not_found_error_types()          try:             data: bytes = await self._sandbox.fs.download_file(                 sandbox_path_str(workspace_path),                 self.state.timeouts.file_download_s,             )             return io.BytesIO(data)         except Exception as e:             if not_found_error_types and isinstance(e, not_found_error_types):                 raise WorkspaceReadNotFoundError(path=error_path, cause=e) from e             raise WorkspaceArchiveReadError(path=error_path, cause=e) from e      async def write(         self,         path: Path | str,         data: io.IOBase,         *,         user: str | User | None = None,     ) -> None:         error_path = posix_path_as_path(coerce_posix_path(path))         if user is not None:             await self._check_write_with_exec(path, user=user)          payload = data.read()         if isinstance(payload, str):             payload = payload.encode("utf-8")         if not isinstance(payload, bytes | bytearray):             raise WorkspaceWriteTypeError(path=error_path, actual_type=type(payload).__name__)          workspace_path = await self._validate_path_access(path, for_write=True)         try:             await self._sandbox.fs.upload_file(                 bytes(payload),                 sandbox_path_str(workspace_path),                 timeout=self.state.timeouts.file_upload_s,             )         except Exception as e:             raise WorkspaceArchiveWriteError(path=workspace_path, cause=e) from e      async def running(self) -> bool:         try:             await asyncio.wait_for(                 self._sandbox.refresh_data(),                 timeout=self.state.timeouts.keepalive_s,             )             SandboxState = _import_sandbox_state()             if SandboxState is None:                 return False             return bool(getattr(self._sandbox, "state", None) == SandboxState.STARTED)         except Exception:             return False      def _tar_exclude_args(self) -> list[str]:         return shell_tar_exclude_args(self._persist_workspace_skip_relpaths())      @retry_async(         retry_if=lambda exc, self, tar_cmd, tar_path: (             exception_chain_contains_type(exc, _retryable_persist_workspace_error_types())             or exception_chain_has_status_code(exc, TRANSIENT_HTTP_STATUS_CODES)         )     )     async def _run_persist_workspace_command(self, tar_cmd: str, tar_path: str) -> bytes:         try:             envs = await self._resolved_envs()             result = await self._sandbox.process.exec(                 tar_cmd,                 env=envs or None,                 timeout=self.state.timeouts.workspace_tar_s,             )             if result.exit_code != 0:                 raise WorkspaceArchiveReadError(                     path=self._workspace_root_path(),                     context={"reason": "tar_failed", "output": result.result or ""},                     retryable=False,                 )             return cast(                 bytes,                 await self._sandbox.fs.download_file(                     tar_path,                     self.state.timeouts.file_download_s,                 ),             )         except WorkspaceArchiveReadError:             raise         except Exception as e:             detail = _daytona_provider_error_detail(e)             retryable, reason = _daytona_provider_retryability(e)             context: dict[str, object] = {"backend": "daytona"}             if reason is not None:                 context["reason"] = reason             if detail:                 context["provider_error"] = detail             provider_error_code = getattr(e, "error_code", None)             if isinstance(provider_error_code, str) and provider_error_code:                 context["provider_error_code"] = provider_error_code             raise WorkspaceArchiveReadError(                 path=self._workspace_root_path(),                 context=context,                 cause=e,                 retryable=retryable,             ) from e      async def persist_workspace(self) -> io.IOBase:         def _error_context_summary(error: WorkspaceArchiveReadError) -> dict[str, str]:             summary = {"message": error.message}             if error.cause is not None:                 summary["cause_type"] = type(error.cause).__name__                 summary["cause"] = str(error.cause)             return summary          root = self._workspace_root_path()         tar_path = f"/tmp/sandbox-persist-{self.state.session_id.hex}.tar"         excludes = " ".join(self._tar_exclude_args())         tar_cmd = (             f"tar {excludes} -C {shlex.quote(root.as_posix())} -cf {shlex.quote(tar_path)} ."         ).strip()          unmounted_mounts: list[tuple[Mount, Path]] = []         unmount_error: WorkspaceArchiveReadError | None = None         for mount_entry, mount_path in self.state.manifest.ephemeral_mount_targets():             try:                 await mount_entry.mount_strategy.teardown_for_snapshot(                     mount_entry, self, mount_path                 )             except Exception as e:                 unmount_error = WorkspaceArchiveReadError(path=root, cause=e)                 break             unmounted_mounts.append((mount_entry, mount_path))          snapshot_error: WorkspaceArchiveReadError | None = None         raw: bytes | None = None         if unmount_error is None:             try:                 raw = await self._run_persist_workspace_command(tar_cmd, tar_path)             except WorkspaceArchiveReadError as e:                 snapshot_error = e             finally:                 try:                     await self._sandbox.process.exec(                         f"rm -f -- {shlex.quote(tar_path)}",                         timeout=self.state.timeouts.cleanup_s,                     )                 except Exception:                     pass          remount_error: WorkspaceArchiveReadError | None = None         for mount_entry, mount_path in reversed(unmounted_mounts):             try:                 await mount_entry.mount_strategy.restore_after_snapshot(                     mount_entry, self, mount_path                 )             except Exception as e:                 current_error = WorkspaceArchiveReadError(path=root, cause=e)                 if remount_error is None:                     remount_error = current_error                     if unmount_error is not None:                         remount_error.context["earlier_unmount_error"] = _error_context_summary(                             unmount_error                         )                 else:                     additional_remount_errors = remount_error.context.setdefault(                         "additional_remount_errors",                         [],                     )                     assert isinstance(additional_remount_errors, list)                     additional_remount_errors.append(_error_context_summary(current_error))          if remount_error is not None:             if snapshot_error is not None:                 remount_error.context["snapshot_error_before_remount_corruption"] = (                     _error_context_summary(snapshot_error)                 )             raise remount_error         if unmount_error is not None:             raise unmount_error         if snapshot_error is not None:             raise snapshot_error          assert raw is not None         return io.BytesIO(raw)      async def hydrate_workspace(self, data: io.IOBase) -> None:         root = self._workspace_root_path()         tar_path = f"/tmp/sandbox-hydrate-{self.state.session_id.hex}.tar"         payload = data.read()         if isinstance(payload, str):             payload = payload.encode("utf-8")         if not isinstance(payload, bytes | bytearray):             raise WorkspaceWriteTypeError(path=Path(tar_path), actual_type=type(payload).__name__)          try:             validate_tar_bytes(                 bytes(payload),                 allow_external_symlink_targets=False,             )         except UnsafeTarMemberError as e:             raise WorkspaceArchiveWriteError(                 path=root,                 context={                     "reason": "unsafe_or_invalid_tar",                     "member": e.member,                     "detail": str(e),                 },                 cause=e,             ) from e          try:             await self.mkdir(root, parents=True)             envs = await self._resolved_envs()             await self._sandbox.fs.upload_file(                 bytes(payload),                 tar_path,                 timeout=self.state.timeouts.file_upload_s,             )             result = await self._sandbox.process.exec(                 f"tar -C {shlex.quote(root.as_posix())} -xf {shlex.quote(tar_path)}",                 env=envs or None,                 timeout=self.state.timeouts.workspace_tar_s,             )             if result.exit_code != 0:                 raise WorkspaceArchiveWriteError(                     path=root,                     context={"reason": "tar_extract_failed", "output": result.result or ""},                 )         except WorkspaceArchiveWriteError:             raise         except Exception as e:             raise WorkspaceArchiveWriteError(path=root, cause=e) from e         finally:             try:                 envs = await self._resolved_envs()                 await self._sandbox.process.exec(                     f"rm -f -- {shlex.quote(tar_path)}",                     env=envs or None,                     timeout=self.state.timeouts.cleanup_s,                 )             except Exception:                 pass ``` |

#### stop `async`

```
stop() -> None
```

Persist/snapshot the workspace.

Note: `stop()` is intentionally persistence-only. Sandboxes that need to tear down
sandbox resources (Docker containers, remote sessions, etc.) should implement
`shutdown()` instead.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 ``` | ``` async def stop(self) -> None:     """     Persist/snapshot the workspace.      Note: `stop()` is intentionally persistence-only. Sandboxes that need to tear down     sandbox resources (Docker containers, remote sessions, etc.) should implement     `shutdown()` instead.     """     try:         try:             await self._before_stop()             await self._persist_snapshot()         except Exception as e:             wrapped = self._wrap_stop_error(e)             if wrapped is e:                 raise             raise wrapped from e     finally:         await self._after_stop() ``` |

#### supports\_docker\_volume\_mounts

```
supports_docker_volume_mounts() -> bool
```

Return whether this backend attaches Docker volume mounts before manifest apply.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 401 402 403 404 ``` | ``` def supports_docker_volume_mounts(self) -> bool:     """Return whether this backend attaches Docker volume mounts before manifest apply."""      return False ``` |

#### shutdown `async`

```
shutdown() -> None
```

Tear down sandbox resources (best-effort).

Default is a no-op. Sandbox-specific sessions (e.g. Docker) should override.

Source code in `src/agents/sandbox/session/base_sandbox_session.py`

|  |  |
| --- | --- |
| ``` 409 410 411 412 413 414 415 416 417 ``` | ``` async def shutdown(self) -> None:     """     Tear down sandbox resources (best-effort).      Default is a no-op. Sandbox-specific sessions (e.g. Docker) should override.     """     await self._before_shutdown()     await self._shutdown_backend()     await self._after_shutdown() ``` |

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

### DaytonaSandboxClient

Bases: `BaseSandboxClient[DaytonaSandboxClientOptions]`

Daytona sandbox client managing sandbox lifecycle via AsyncDaytona.

Source code in `src/agents/extensions/sandbox/daytona/sandbox.py`

|  |  |
| --- | --- |
| ``` 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 1194 1195 1196 1197 1198 1199 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 1213 1214 1215 1216 1217 1218 1219 1220 1221 1222 1223 1224 1225 1226 1227 1228 1229 1230 1231 1232 1233 1234 1235 1236 1237 1238 1239 1240 1241 1242 1243 1244 1245 1246 1247 1248 1249 1250 1251 1252 1253 1254 1255 1256 1257 1258 1259 1260 1261 1262 1263 1264 1265 1266 1267 1268 1269 1270 1271 1272 1273 1274 1275 1276 1277 1278 1279 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1315 1316 1317 1318 1319 1320 1321 1322 1323 1324 1325 1326 1327 1328 1329 1330 1331 1332 1333 1334 1335 1336 1337 1338 1339 1340 1341 1342 1343 1344 1345 1346 1347 1348 1349 1350 1351 1352 1353 1354 1355 1356 1357 1358 1359 ``` | ``` class DaytonaSandboxClient(BaseSandboxClient[DaytonaSandboxClientOptions]):     """Daytona sandbox client managing sandbox lifecycle via AsyncDaytona."""      backend_id = "daytona"     _instrumentation: Instrumentation      def __init__(         self,         *,         api_key: str | None = None,         api_url: str | None = None,         instrumentation: Instrumentation | None = None,         dependencies: Dependencies | None = None,     ) -> None:         AsyncDaytona, DaytonaConfig, _, _ = _import_daytona_sdk()         config = DaytonaConfig(api_key=api_key, api_url=api_url) if (api_key or api_url) else None         self._daytona = AsyncDaytona(config)         self._instrumentation = instrumentation or Instrumentation()         self._dependencies = dependencies      async def _build_create_params(         self,         *,         sandbox_snapshot_name: str | None,         image: str | None,         env_vars: dict[str, str] | None,         manifest: Manifest,         name: str | None = None,         resources: DaytonaSandboxResources | None = None,         auto_stop_interval: int | None = None,     ) -> Any:         _, _, CreateSandboxFromSnapshotParams, CreateSandboxFromImageParams = _import_daytona_sdk()         base_envs = dict(env_vars or {})         creation_envs = base_envs or None          if sandbox_snapshot_name:             return CreateSandboxFromSnapshotParams(                 snapshot=sandbox_snapshot_name,                 env_vars=creation_envs,                 name=name,                 auto_stop_interval=auto_stop_interval,             )          if image:             sandbox_resources = None             if resources is not None and any(                 v is not None for v in (resources.cpu, resources.memory, resources.disk)             ):                 Resources = _import_sdk_resources()                 sandbox_resources = Resources(                     cpu=resources.cpu,                     memory=resources.memory,                     disk=resources.disk,                 )             return CreateSandboxFromImageParams(                 image=image,                 env_vars=creation_envs,                 name=name,                 resources=sandbox_resources,                 auto_stop_interval=auto_stop_interval,             )          return CreateSandboxFromSnapshotParams(             env_vars=creation_envs,             name=name,             auto_stop_interval=auto_stop_interval,         )      async def create(         self,         *,         snapshot: SnapshotSpec | SnapshotBase | None = None,         manifest: Manifest | None = None,         options: DaytonaSandboxClientOptions,     ) -> SandboxSession:         if manifest is None:             manifest = Manifest(root=DEFAULT_DAYTONA_WORKSPACE_ROOT)          timeouts_in = options.timeouts         if isinstance(timeouts_in, DaytonaSandboxTimeouts):             timeouts = timeouts_in         elif timeouts_in is None:             timeouts = DaytonaSandboxTimeouts()         else:             timeouts = DaytonaSandboxTimeouts.model_validate(timeouts_in)          session_id = uuid.uuid4()         sandbox_name = options.name or str(session_id)          params = await self._build_create_params(             sandbox_snapshot_name=options.sandbox_snapshot_name,             image=options.image,             env_vars=options.env_vars,             manifest=manifest,             name=sandbox_name,             resources=options.resources,             auto_stop_interval=options.auto_stop_interval,         )         daytona_sandbox = await self._daytona.create(params, timeout=options.create_timeout)          snapshot_instance = resolve_snapshot(snapshot, str(session_id))         state = DaytonaSandboxSessionState(             session_id=session_id,             manifest=manifest,             snapshot=snapshot_instance,             sandbox_id=daytona_sandbox.id,             sandbox_snapshot_name=options.sandbox_snapshot_name,             image=options.image,             base_env_vars=dict(options.env_vars or {}),             pause_on_exit=options.pause_on_exit,             create_timeout=options.create_timeout,             start_timeout=options.start_timeout,             name=sandbox_name,             resources=options.resources,             auto_stop_interval=options.auto_stop_interval,             timeouts=timeouts,             exposed_ports=options.exposed_ports,             exposed_port_url_ttl_s=options.exposed_port_url_ttl_s,         )         inner = DaytonaSandboxSession.from_state(state, sandbox=daytona_sandbox)         return self._wrap_session(inner, instrumentation=self._instrumentation)      async def close(self) -> None:         """Close the underlying AsyncDaytona HTTP client session."""         await self._daytona.close()      async def __aenter__(self) -> DaytonaSandboxClient:         return self      async def __aexit__(self, *_: object) -> None:         await self.close()      async def delete(self, session: SandboxSession) -> SandboxSession:         inner = session._inner         if not isinstance(inner, DaytonaSandboxSession):             raise TypeError("DaytonaSandboxClient.delete expects a DaytonaSandboxSession")         try:             await inner.shutdown()         except Exception:             pass         return session      async def resume(         self,         state: SandboxSessionState,     ) -> SandboxSession:         if not isinstance(state, DaytonaSandboxSessionState):             raise TypeError("DaytonaSandboxClient.resume expects a DaytonaSandboxSessionState")          daytona_sandbox = None         reconnected = False         try:             daytona_sandbox = await self._daytona.get(state.sandbox_id)             SandboxState = _import_sandbox_state()             if getattr(daytona_sandbox, "state", None) != SandboxState.STARTED:                 await daytona_sandbox.start(timeout=state.start_timeout)             reconnected = True         except Exception as e:             logger.debug("daytona sandbox get() failed, will recreate: %s", e)          if not reconnected or daytona_sandbox is None:             params = await self._build_create_params(                 sandbox_snapshot_name=state.sandbox_snapshot_name,                 image=state.image,                 env_vars=state.base_env_vars,                 manifest=state.manifest,                 name=state.name,                 resources=state.resources,                 auto_stop_interval=state.auto_stop_interval,             )             daytona_sandbox = await self._daytona.create(params, timeout=state.create_timeout)             state.sandbox_id = daytona_sandbox.id             state.workspace_root_ready = False          inner = DaytonaSandboxSession.from_state(state, sandbox=daytona_sandbox)         inner._set_start_state_preserved(reconnected, system=reconnected)         return self._wrap_session(inner, instrumentation=self._instrumentation)      def deserialize_session_state(self, payload: dict[str, object]) -> SandboxSessionState:         return DaytonaSandboxSessionState.model_validate(payload) ``` |

#### close `async`

```
close() -> None
```

Close the underlying AsyncDaytona HTTP client session.

Source code in `src/agents/extensions/sandbox/daytona/sandbox.py`

|  |  |
| --- | --- |
| ``` 1302 1303 1304 ``` | ``` async def close(self) -> None:     """Close the underlying AsyncDaytona HTTP client session."""     await self._daytona.close() ``` |

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