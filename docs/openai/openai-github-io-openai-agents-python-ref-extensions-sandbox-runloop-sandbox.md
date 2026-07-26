---
url: https://openai.github.io/openai-agents-python/ref/extensions/sandbox/runloop/sandbox/
title: `Sandbox`
framework: openai
---

# `Sandbox`

Runloop sandbox (https://runloop.ai) implementation.

This module provides a Runloop-backed sandbox client/session implementation backed by
`runloop_api_client.sdk.AsyncRunloopSDK`.

The `runloop_api_client` dependency is optional, so package-level exports should guard imports of
this module. Within this module, Runloop SDK imports are lazy so users without the extra can still
import the package.

### RunloopTimeouts

Bases: `BaseModel`

Timeout configuration for Runloop sandbox operations.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 ``` | ``` class RunloopTimeouts(BaseModel):     """Timeout configuration for Runloop sandbox operations."""      model_config = {"frozen": True}      exec_timeout_unbounded_s: float = Field(default=24 * 60 * 60, ge=1)     create_s: float = Field(default=300.0, ge=1)     keepalive_s: float = Field(default=10.0, ge=1)     cleanup_s: float = Field(default=30.0, ge=1)     fast_op_s: float = Field(default=30.0, ge=1)     file_upload_s: float = Field(default=1800.0, ge=1)     file_download_s: float = Field(default=1800.0, ge=1)     snapshot_s: float = Field(default=300.0, ge=1)     suspend_s: float = Field(default=120.0, ge=1)     resume_s: float = Field(default=300.0, ge=1) ``` |

### RunloopTunnelConfig

Bases: `BaseModel`

Runloop public tunnel configuration.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 396 397 398 399 400 401 402 403 ``` | ``` class RunloopTunnelConfig(BaseModel):     """Runloop public tunnel configuration."""      model_config = {"frozen": True}      auth_mode: Literal["open", "authenticated"] | None = None     http_keep_alive: bool | None = None     wake_on_http: bool | None = None ``` |

### RunloopGatewaySpec

Bases: `BaseModel`

Runloop agent gateway binding.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 406 407 408 409 410 411 412 ``` | ``` class RunloopGatewaySpec(BaseModel):     """Runloop agent gateway binding."""      model_config = {"frozen": True}      gateway: str = Field(min_length=1)     secret: str = Field(min_length=1) ``` |

### RunloopMcpSpec

Bases: `BaseModel`

Runloop MCP gateway binding.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 415 416 417 418 419 420 421 ``` | ``` class RunloopMcpSpec(BaseModel):     """Runloop MCP gateway binding."""      model_config = {"frozen": True}      mcp_config: str = Field(min_length=1)     secret: str = Field(min_length=1) ``` |

### RunloopSandboxClientOptions

Bases: `BaseSandboxClientOptions`

Client options for the Runloop sandbox.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 ``` | ``` class RunloopSandboxClientOptions(BaseSandboxClientOptions):     """Client options for the Runloop sandbox."""      type: Literal["runloop"] = "runloop"     blueprint_id: str | None = None     blueprint_name: str | None = None     env_vars: dict[str, str] | None = None     pause_on_exit: bool = False     name: str | None = None     timeouts: RunloopTimeouts | dict[str, object] | None = None     exposed_ports: tuple[int, ...] = ()     user_parameters: RunloopUserParameters | dict[str, object] | None = None     launch_parameters: RunloopLaunchParameters | dict[str, object] | None = None     tunnel: RunloopTunnelConfig | dict[str, object] | None = None     gateways: dict[str, RunloopGatewaySpec] | None = None     mcp: dict[str, RunloopMcpSpec] | None = None     metadata: dict[str, str] | None = None     managed_secrets: dict[str, str] | None = None      def __init__(         self,         blueprint_id: str | None = None,         blueprint_name: str | None = None,         env_vars: dict[str, str] | None = None,         pause_on_exit: bool = False,         name: str | None = None,         timeouts: RunloopTimeouts | dict[str, object] | None = None,         exposed_ports: tuple[int, ...] = (),         user_parameters: RunloopUserParameters | dict[str, object] | None = None,         launch_parameters: RunloopLaunchParameters | dict[str, object] | None = None,         tunnel: RunloopTunnelConfig | dict[str, object] | None = None,         gateways: dict[str, RunloopGatewaySpec] | None = None,         mcp: dict[str, RunloopMcpSpec] | None = None,         metadata: dict[str, str] | None = None,         managed_secrets: dict[str, str] | None = None,         *,         type: Literal["runloop"] = "runloop",     ) -> None:         super().__init__(             type=type,             blueprint_id=blueprint_id,             blueprint_name=blueprint_name,             env_vars=env_vars,             pause_on_exit=pause_on_exit,             name=name,             timeouts=timeouts,             exposed_ports=exposed_ports,             user_parameters=user_parameters,             launch_parameters=launch_parameters,             tunnel=tunnel,             gateways=gateways,             mcp=mcp,             metadata=metadata,             managed_secrets=managed_secrets,         ) ``` |

### RunloopSandboxSessionState

Bases: `SandboxSessionState`

Serializable state for a Runloop-backed session.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 ``` | ``` class RunloopSandboxSessionState(SandboxSessionState):     """Serializable state for a Runloop-backed session."""      type: Literal["runloop"] = "runloop"     devbox_id: str     blueprint_id: str | None = None     blueprint_name: str | None = None     base_env_vars: dict[str, str] = Field(default_factory=dict)     pause_on_exit: bool = False     name: str | None = None     timeouts: RunloopTimeouts = Field(default_factory=RunloopTimeouts)     user_parameters: RunloopUserParameters | None = None     launch_parameters: RunloopLaunchParameters | None = None     tunnel: RunloopTunnelConfig | None = None     gateways: dict[str, RunloopGatewaySpec] = Field(default_factory=dict)     mcp: dict[str, RunloopMcpSpec] = Field(default_factory=dict)     metadata: dict[str, str] = Field(default_factory=dict)     secret_refs: dict[str, str] = Field(default_factory=dict) ``` |

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

### RunloopPlatformClient `dataclass`

Thin facade over the Runloop SDK's non-devbox platform resources.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 ``` | ``` @dataclass(frozen=True) class RunloopPlatformClient:     """Thin facade over the Runloop SDK's non-devbox platform resources."""      _sdk: Any      @property     def blueprints(self) -> RunloopPlatformBlueprintsClient:         return RunloopPlatformBlueprintsClient(self._sdk)      @property     def benchmarks(self) -> RunloopPlatformBenchmarksClient:         return RunloopPlatformBenchmarksClient(self._sdk)      @property     def secrets(self) -> RunloopPlatformSecretsClient:         return RunloopPlatformSecretsClient(self._sdk)      @property     def network_policies(self) -> RunloopPlatformNetworkPoliciesClient:         return RunloopPlatformNetworkPoliciesClient(self._sdk)      @property     def axons(self) -> RunloopPlatformAxonsClient:         return RunloopPlatformAxonsClient(self._sdk) ``` |

### RunloopSandboxSession

Bases: `BaseSandboxSession`

Runloop-backed sandbox session implementation.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ```  694  695  696  697  698  699  700  701  702  703  704  705  706  707  708  709  710  711  712  713  714  715  716  717  718  719  720  721  722  723  724  725  726  727  728  729  730  731  732  733  734  735  736  737  738  739  740  741  742  743  744  745  746  747  748  749  750  751  752  753  754  755  756  757  758  759  760  761  762  763  764  765  766  767  768  769  770  771  772  773  774  775  776  777  778  779  780  781  782  783  784  785  786  787  788  789  790  791  792  793  794  795  796  797  798  799  800  801  802  803  804  805  806  807  808  809  810  811  812  813  814  815  816  817  818  819  820  821  822  823  824  825  826  827  828  829  830  831  832  833  834  835  836  837  838  839  840  841  842  843  844  845  846  847  848  849  850  851  852  853  854  855  856  857  858  859  860  861  862  863  864  865  866  867  868  869  870  871  872  873  874  875  876  877  878  879  880  881  882  883  884  885  886  887  888  889  890  891  892  893  894  895  896  897  898  899  900  901  902  903  904  905  906  907  908  909  910  911  912  913  914  915  916  917  918  919  920  921  922  923  924  925  926  927  928  929  930  931  932  933  934  935  936  937  938  939  940  941  942  943  944  945  946  947  948  949  950  951  952  953  954  955  956  957  958  959  960  961  962  963  964  965  966  967  968  969  970  971  972  973  974  975  976  977  978  979  980  981  982  983  984  985  986  987  988  989  990  991  992  993  994  995  996  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 1023 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 1055 1056 1057 1058 1059 1060 1061 1062 1063 1064 1065 1066 1067 1068 1069 1070 1071 1072 1073 1074 1075 1076 1077 1078 1079 1080 1081 1082 1083 1084 1085 1086 1087 1088 1089 1090 1091 1092 1093 1094 1095 1096 1097 1098 1099 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 1117 1118 1119 1120 1121 1122 1123 1124 1125 1126 1127 1128 1129 1130 1131 1132 1133 1134 1135 1136 1137 1138 1139 1140 1141 1142 1143 1144 1145 1146 1147 1148 1149 1150 1151 1152 1153 1154 1155 1156 1157 1158 1159 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 1194 1195 1196 1197 1198 1199 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 1213 1214 1215 1216 1217 1218 1219 1220 1221 1222 1223 1224 1225 1226 1227 1228 1229 1230 1231 1232 1233 1234 1235 1236 1237 1238 1239 1240 1241 1242 1243 1244 1245 1246 1247 1248 1249 1250 1251 1252 1253 1254 1255 1256 1257 1258 1259 1260 1261 1262 1263 1264 1265 1266 1267 1268 1269 1270 1271 1272 1273 1274 1275 1276 1277 1278 1279 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1315 1316 1317 1318 1319 1320 1321 1322 1323 1324 1325 1326 1327 1328 1329 1330 1331 1332 1333 1334 1335 1336 1337 1338 1339 1340 1341 1342 1343 1344 1345 1346 1347 1348 1349 1350 1351 1352 1353 1354 1355 1356 1357 1358 1359 1360 1361 1362 1363 1364 1365 1366 1367 1368 1369 1370 1371 1372 1373 1374 1375 1376 1377 1378 1379 1380 1381 1382 1383 1384 1385 1386 1387 1388 1389 1390 1391 1392 1393 1394 1395 1396 1397 1398 1399 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1415 1416 1417 1418 ``` | ``` class RunloopSandboxSession(BaseSandboxSession):     """Runloop-backed sandbox session implementation."""      state: RunloopSandboxSessionState     _sdk: Any     _devbox: Any     _skip_start: bool      def __init__(self, *, state: RunloopSandboxSessionState, sdk: Any, devbox: Any) -> None:         self.state = state         self._sdk = sdk         self._devbox = devbox         self._skip_start = False      @classmethod     def from_state(         cls,         state: RunloopSandboxSessionState,         *,         sdk: Any,         devbox: Any,     ) -> RunloopSandboxSession:         return cls(state=state, sdk=sdk, devbox=devbox)      @property     def devbox_id(self) -> str:         return self.state.devbox_id      @property     def runloop_home(self) -> PurePosixPath:         return _effective_runloop_home(self.state.user_parameters)      async def _resolved_envs(self) -> dict[str, str]:         manifest_envs = await self.state.manifest.environment.resolve()         return {**self.state.base_env_vars, **manifest_envs}      def _coerce_exec_timeout(self, timeout_s: float | None) -> float:         if timeout_s is None:             return float(self.state.timeouts.exec_timeout_unbounded_s)         if timeout_s <= 0:             return 0.001         return float(timeout_s)      async def start(self) -> None:         """Resume a reconnected Runloop devbox without replaying full setup when possible.          `resume()` marks `_skip_start` when it successfully reconnects to a suspended devbox.         In that path, Runloop reuses the live machine and only reapplies snapshot or ephemeral         manifest state if the cached workspace fingerprint no longer matches.         """         if self._skip_start:             if await self.state.snapshot.restorable(dependencies=self.dependencies):                 is_running = await self.running()                 fingerprints_match = await self._can_skip_snapshot_restore_on_resume(                     is_running=is_running                 )                 if fingerprints_match:                     await self._reapply_ephemeral_manifest_on_resume()                 else:                     await self._restore_snapshot_into_workspace_on_resume()                     if self.should_provision_manifest_accounts_on_resume():                         await self.provision_manifest_accounts()                     await self._reapply_ephemeral_manifest_on_resume()             else:                 await self._reapply_ephemeral_manifest_on_resume()             return         await super().start()      async def shutdown(self) -> None:         """Suspend or delete the underlying Runloop devbox as the final session cleanup step.          `pause_on_exit=True` maps to Runloop suspension so the same devbox can be resumed later.         Otherwise the session shuts the devbox down and treats it as disposable.         """         try:             if self.state.pause_on_exit:                 await self._devbox.suspend(timeout=self.state.timeouts.suspend_s)                 await self._devbox.await_suspended()             else:                 await self._devbox.shutdown(timeout=self.state.timeouts.cleanup_s)         except Exception:             pass      def supports_pty(self) -> bool:         return False      async def _validate_path_access(self, path: Path | str, *, for_write: bool = False) -> Path:         return await self._validate_remote_path_access(path, for_write=for_write)      def _runtime_helpers(self) -> tuple[RuntimeHelperScript, ...]:         return (RESOLVE_WORKSPACE_PATH_HELPER,)      async def _wrap_command_in_workspace_context(self, command: str) -> str:         root_q = shlex.quote(self.state.manifest.root)         envs = await self._resolved_envs()         if not envs:             return f"cd {root_q} && {command}"          env_assignments = " ".join(             shlex.quote(f"{key}={value}") for key, value in sorted(envs.items())         )         return f"cd {root_q} && env -- {env_assignments} {command}"      async def _exec_internal(         self,         *command: str | Path,         timeout: float | None = None,     ) -> ExecResult:         cmd_str = await self._wrap_command_in_workspace_context(shlex.join(str(c) for c in command))         return await self._run_exec_command(             cmd_str,             command=command,             timeout=timeout,         )      async def _run_exec_command(         self,         cmd_str: str,         *,         command: tuple[str | Path, ...],         timeout: float | None,     ) -> ExecResult:         caller_timeout = self._coerce_exec_timeout(timeout)         request_timeout = min(caller_timeout, self.state.timeouts.fast_op_s)         polling_config = _runloop_polling_config(timeout_s=caller_timeout)          try:             result: RunloopAsyncExecutionResult = await asyncio.wait_for(                 self._devbox.cmd.exec(                     cmd_str,                     timeout=request_timeout,                     polling_config=polling_config,                 ),                 timeout=caller_timeout,             )             stdout = (await result.stdout()).encode("utf-8", errors="replace")             stderr = (await result.stderr()).encode("utf-8", errors="replace")             exit_code = int(result.exit_code or 0)             return ExecResult(stdout=stdout, stderr=stderr, exit_code=exit_code)         except asyncio.TimeoutError as e:             raise ExecTimeoutError(                 command=command,                 timeout_s=timeout,                 context=_runloop_error_context(e, backend_detail="exec_timeout"),                 cause=e,             ) from e         except Exception as e:             if _is_runloop_timeout(e):                 raise ExecTimeoutError(                     command=command,                     timeout_s=timeout,                     context=_runloop_error_context(e, backend_detail="exec_timeout"),                     cause=e,                 ) from e             if _is_runloop_provider_error(e):                 raise ExecTransportError(                     command=command,                     context=_runloop_error_context(e, backend_detail="exec_failed"),                     cause=e,                     retryable=_runloop_provider_retryability(e),                 ) from e             raise ExecTransportError(command=command, cause=e) from e      async def _ensure_tunnel_url(self, port: int) -> str:         try:             url = await self._devbox.get_tunnel_url(port, timeout=self.state.timeouts.fast_op_s)         except Exception as e:             if _is_runloop_provider_error(e):                 raise ExposedPortUnavailableError(                     port=port,                     exposed_ports=self.state.exposed_ports,                     reason="backend_unavailable",                     context=_runloop_error_context(e, backend_detail="get_tunnel_url_failed"),                     cause=e,                     retryable=_runloop_provider_retryability(e),                 ) from e             raise         if isinstance(url, str) and url:             return url          try:             await self._devbox.net.enable_tunnel(                 auth_mode="open",                 http_keep_alive=True,                 wake_on_http=False,                 timeout=self.state.timeouts.fast_op_s,             )         except Exception as e:             if _is_runloop_provider_error(e):                 raise ExposedPortUnavailableError(                     port=port,                     exposed_ports=self.state.exposed_ports,                     reason="backend_unavailable",                     context=_runloop_error_context(e, backend_detail="enable_tunnel_failed"),                     cause=e,                     retryable=_runloop_provider_retryability(e),                 ) from e             raise         try:             url = await self._devbox.get_tunnel_url(port, timeout=self.state.timeouts.fast_op_s)         except Exception as e:             if _is_runloop_provider_error(e):                 context = _runloop_error_context(e, backend_detail="get_tunnel_url_failed")                 context["phase"] = "post_enable"                 raise ExposedPortUnavailableError(                     port=port,                     exposed_ports=self.state.exposed_ports,                     reason="backend_unavailable",                     context=context,                     cause=e,                     retryable=_runloop_provider_retryability(e),                 ) from e             raise         if not isinstance(url, str) or not url:             raise ExposedPortUnavailableError(                 port=port,                 exposed_ports=self.state.exposed_ports,                 reason="backend_unavailable",                 context={"backend": "runloop", "detail": "missing_tunnel_url"},             )         return url      async def resolve_exposed_port(self, port: int) -> ExposedPortEndpoint:         """Resolve an exposed Runloop port through the provider-managed tunnel endpoint.          Runloop may not have a tunnel enabled for a devbox yet, so exposed-port resolution can         trigger tunnel creation before returning the public host, port, and TLS settings.         """          return await super().resolve_exposed_port(port)      async def _resolve_exposed_port(self, port: int) -> ExposedPortEndpoint:         try:             url = await self._ensure_tunnel_url(port)             split = urlsplit(url)             host = split.hostname             if host is None:                 raise ValueError("missing hostname")             port_value = split.port or (443 if split.scheme == "https" else 80)             return ExposedPortEndpoint(host=host, port=port_value, tls=split.scheme == "https")         except ExposedPortUnavailableError:             raise         except Exception as e:             raise ExposedPortUnavailableError(                 port=port,                 exposed_ports=self.state.exposed_ports,                 reason="backend_unavailable",                 context={"backend": "runloop", "detail": "invalid_tunnel_url"},                 cause=e,             ) from e      async def read(self, path: Path | str, *, user: str | User | None = None) -> io.IOBase:         """Read a file via Runloop's binary file API."""         error_path = posix_path_as_path(coerce_posix_path(path))         if user is not None:             await self._check_read_with_exec(path, user=user)          normalized_path = await self._validate_path_access(path)         try:             payload = await self._devbox.file.download(                 path=sandbox_path_str(normalized_path),                 timeout=self.state.timeouts.file_download_s,             )             return io.BytesIO(bytes(payload))         except Exception as e:             if _is_runloop_not_found(e):                 raise WorkspaceReadNotFoundError(                     path=error_path,                     context=_runloop_error_context(e, backend_detail="file_download_failed"),                     cause=e,                 ) from e             if _is_runloop_provider_error(e):                 raise WorkspaceArchiveReadError(                     path=error_path,                     context=_runloop_error_context(e, backend_detail="file_download_failed"),                     cause=e,                     retryable=_runloop_provider_retryability(e),                 ) from e             raise WorkspaceArchiveReadError(path=error_path, cause=e) from e      async def write(         self,         path: Path | str,         data: io.IOBase,         *,         user: str | User | None = None,     ) -> None:         """Write a file through Runloop's upload API using manifest-root workspace paths."""         error_path = posix_path_as_path(coerce_posix_path(path))         if user is not None:             await self._check_write_with_exec(path, user=user)          payload = data.read()         if isinstance(payload, str):             payload = payload.encode("utf-8")         if not isinstance(payload, bytes | bytearray):             raise WorkspaceWriteTypeError(path=error_path, actual_type=type(payload).__name__)          workspace_path = await self._validate_path_access(path, for_write=True)         await self.mkdir(workspace_path.parent, parents=True)         try:             await self._devbox.file.upload(                 path=sandbox_path_str(workspace_path),                 file=bytes(payload),                 timeout=self.state.timeouts.file_upload_s,             )         except Exception as e:             if _is_runloop_provider_error(e):                 raise WorkspaceArchiveWriteError(                     path=workspace_path,                     context=_runloop_error_context(e, backend_detail="file_upload_failed"),                     cause=e,                     retryable=_runloop_provider_retryability(e),                 ) from e             raise WorkspaceArchiveWriteError(path=workspace_path, cause=e) from e      async def running(self) -> bool:         """Report whether the current Runloop devbox is still in the `running` backend state.          Resume logic relies on this backend status check before deciding whether a suspended devbox         can be reused directly or whether snapshot restore must rebuild the workspace elsewhere.         """         try:             info: RunloopDevboxView = await self._devbox.get_info(                 timeout=self.state.timeouts.keepalive_s             )             return cast(str, info.status) == "running"         except Exception:             return False      async def mkdir(         self,         path: Path | str,         *,         parents: bool = False,         user: str | User | None = None,     ) -> None:         """Create directories via raw exec so workspace-root creation does not depend on `cd`."""          if user is not None:             path = await self._check_mkdir_with_exec(path, parents=parents, user=user)         else:             path = await self._validate_path_access(path, for_write=True)         cmd = ["mkdir"]         if parents:             cmd.append("-p")         cmd.extend(["--", sandbox_path_str(path)])         result = await self._run_exec_command(             shlex.join(cmd),             command=tuple(cmd),             timeout=self.state.timeouts.fast_op_s,         )         if not result.ok():             raise WorkspaceArchiveWriteError(                 path=path,                 context={                     "reason": "mkdir_failed",                     "exit_code": result.exit_code,                     "stderr": result.stderr.decode("utf-8", "replace"),                 },             )      async def _backup_plain_skip_paths(self, plain_skip: set[Path]) -> bytes | None:         if not plain_skip:             return None          root = sandbox_path_str(self.state.manifest.root)         root_q = shlex.quote(root)         checks = "\n".join(             (                 f"if [ -e {shlex.quote(rel.as_posix())} ]; then "                 f'set -- "$@" {shlex.quote(rel.as_posix())}; fi'             )             for rel in sorted(plain_skip, key=lambda p: p.as_posix())         )         command = (             f"cd {root_q}\n"             "set --\n"             f"{checks}\n"             'if [ "$#" -eq 0 ]; then exit 0; fi\n'             'tar -cf - "$@" | base64 -w0\n'         )         result = await self.exec(command, shell=True, timeout=self.state.timeouts.snapshot_s)         if not result.ok():             raise WorkspaceArchiveReadError(                 path=self._workspace_root_path(),                 context={                     "reason": "ephemeral_backup_failed",                     "exit_code": result.exit_code,                     "stderr": result.stderr.decode("utf-8", "replace"),                 },             )         encoded = result.stdout.decode("utf-8", "replace").strip()         if not encoded:             return None         try:             return io.BytesIO(base64.b64decode(encoded.encode("utf-8"), validate=True)).read()         except Exception as e:             raise WorkspaceArchiveReadError(                 path=self._workspace_root_path(),                 context={"reason": "ephemeral_backup_invalid_base64"},                 cause=e,             ) from e      async def _remove_plain_skip_paths(self, plain_skip: set[Path]) -> None:         if not plain_skip:             return         root = self._workspace_root_path()         command = ["rm", "-rf", "--"] + [(root / rel).as_posix() for rel in sorted(plain_skip)]         result = await self.exec(*command, shell=False, timeout=self.state.timeouts.cleanup_s)         if not result.ok():             raise WorkspaceArchiveReadError(                 path=root,                 context={                     "reason": "ephemeral_remove_failed",                     "exit_code": result.exit_code,                     "stderr": result.stderr.decode("utf-8", "replace"),                 },             )      async def _restore_plain_skip_paths(self, backup: bytes | None) -> None:         if not backup:             return         root = self._workspace_root_path()         temp_path = root / f".sandbox-runloop-restore-{self.state.session_id.hex}.tar"         await self.write(temp_path, io.BytesIO(backup))         try:             result = await self.exec(                 "mkdir",                 "-p",                 root.as_posix(),                 shell=False,                 timeout=self.state.timeouts.cleanup_s,             )             if not result.ok():                 raise WorkspaceArchiveReadError(                     path=root,                     context={                         "reason": "ephemeral_restore_mkdir_failed",                         "exit_code": result.exit_code,                     },                 )             result = await self.exec(                 "tar",                 "-xf",                 sandbox_path_str(temp_path),                 "-C",                 root.as_posix(),                 shell=False,                 timeout=self.state.timeouts.snapshot_s,             )             if not result.ok():                 raise WorkspaceArchiveReadError(                     path=root,                     context={                         "reason": "ephemeral_restore_failed",                         "exit_code": result.exit_code,                         "stderr": result.stderr.decode("utf-8", "replace"),                     },                 )         finally:             try:                 await self.exec("rm", "-f", "--", sandbox_path_str(temp_path), shell=False)             except Exception:                 pass      async def persist_workspace(self) -> io.IOBase:         """Persist the workspace with a native Runloop disk snapshot.          Before snapshotting, the session temporarily removes ephemeral skip paths and tears down         ephemeral mounts so the saved disk image contains only durable workspace state, then it         restores those local-only artifacts afterward.         """         root = self._workspace_root_path()         skip = self._persist_workspace_skip_relpaths()         mount_targets = self.state.manifest.ephemeral_mount_targets()         mount_skip_rel_paths: set[Path] = set()         for _mount_entry, mount_path in mount_targets:             try:                 mount_skip_rel_paths.add(mount_path.relative_to(root))             except ValueError:                 continue         plain_skip = skip - mount_skip_rel_paths          backup: bytes | None = None         unmounted_mounts: list[tuple[Mount, Path]] = []         snapshot_error: WorkspaceArchiveReadError | None = None         snapshot_id: str | None = None          try:             backup = await self._backup_plain_skip_paths(plain_skip)             await self._remove_plain_skip_paths(plain_skip)              for mount_entry, mount_path in mount_targets:                 await mount_entry.mount_strategy.teardown_for_snapshot(                     mount_entry,                     self,                     mount_path,                 )                 unmounted_mounts.append((mount_entry, mount_path))              snapshot: RunloopAsyncSnapshot = await self._devbox.snapshot_disk(                 name=f"sandbox-{self.state.session_id.hex[:12]}",                 metadata={"openai_agents_session_id": self.state.session_id.hex},                 timeout=self.state.timeouts.snapshot_s,             )             snapshot_id = snapshot.id             if not snapshot_id:                 raise WorkspaceArchiveReadError(                     path=root,                     context={                         "reason": "snapshot_unexpected_return",                         "type": type(snapshot).__name__,                     },                 )         except WorkspaceArchiveReadError as e:             snapshot_error = e         except Exception as e:             retryable = None             if _is_runloop_provider_error(e):                 retryable = _runloop_provider_retryability(e)             snapshot_error = WorkspaceArchiveReadError(                 path=root,                 context={"reason": "snapshot_failed"},                 cause=e,                 retryable=retryable,             )         finally:             remount_error: WorkspaceArchiveReadError | None = None             for mount_entry, mount_path in reversed(unmounted_mounts):                 try:                     await mount_entry.mount_strategy.restore_after_snapshot(                         mount_entry, self, mount_path                     )                 except Exception as e:                     current_error = WorkspaceArchiveReadError(path=root, cause=e)                     if remount_error is None:                         remount_error = current_error                     else:                         additional = remount_error.context.setdefault(                             "additional_remount_errors", []                         )                         assert isinstance(additional, list)                         additional.append(                             {                                 "message": current_error.message,                                 "cause_type": type(e).__name__,                                 "cause": str(e),                             }                         )             try:                 await self._restore_plain_skip_paths(backup)             except Exception as e:                 restore_error = WorkspaceArchiveReadError(path=root, cause=e)                 if remount_error is None:                     remount_error = restore_error                 else:                     additional = remount_error.context.setdefault("additional_restore_errors", [])                     assert isinstance(additional, list)                     additional.append(                         {                             "message": restore_error.message,                             "cause_type": type(e).__name__,                             "cause": str(e),                         }                     )              if remount_error is not None:                 if snapshot_error is not None:                     remount_error.context["snapshot_error_before_restore_corruption"] = {                         "message": snapshot_error.message                     }                 raise remount_error          if snapshot_error is not None:             raise snapshot_error          assert snapshot_id is not None         return io.BytesIO(_encode_runloop_snapshot_ref(snapshot_id=snapshot_id))      async def hydrate_workspace(self, data: io.IOBase) -> None:         """Replace the current devbox from a Runloop snapshot reference or tar archive.          Runloop restore creates a new devbox from the saved disk snapshot and treats that snapshot         filesystem as authoritative, including any tools or files that originally came from the         source blueprint, so restore does not reselect a blueprint. Non-native payloads fall back         to tar hydration so cross-provider snapshots and file snapshots keep working.         """         root = self._workspace_root_path()         raw = data.read()         if isinstance(raw, str):             raw = raw.encode("utf-8")         if not isinstance(raw, bytes | bytearray):             raise WorkspaceWriteTypeError(path=root, actual_type=type(raw).__name__)          snapshot_id = _decode_runloop_snapshot_ref(bytes(raw))         if snapshot_id is None:             await self._hydrate_workspace_via_tar(bytes(raw))             return          try:             try:                 await self._devbox.shutdown(timeout=self.state.timeouts.cleanup_s)             except Exception:                 pass             envs = await self._resolved_envs()             create_kwargs = _runloop_create_kwargs(                 blueprint_id=None,                 blueprint_name=None,                 env_vars=envs,                 name=self.state.name,                 user_parameters=self.state.user_parameters,                 launch_parameters=self.state.launch_parameters,                 tunnel=self.state.tunnel,                 gateways=self.state.gateways,                 mcp=self.state.mcp,                 metadata=self.state.metadata,                 secrets=self.state.secret_refs,             )             devbox = await self._sdk.devbox.create_from_snapshot(                 snapshot_id,                 timeout=self.state.timeouts.resume_s,                 **create_kwargs,             )             self._devbox = devbox             self.state.devbox_id = devbox.id         except Exception as e:             context: dict[str, object] = {                 "reason": "snapshot_restore_failed",                 "snapshot_id": snapshot_id,             }             if _is_runloop_provider_error(e):                 context.update(_runloop_error_context(e, backend_detail="snapshot_restore_failed"))             raise WorkspaceArchiveWriteError(                 path=root,                 context=context,                 cause=e,                 retryable=_runloop_provider_retryability(e)                 if _is_runloop_provider_error(e)                 else None,             ) from e      async def _restore_snapshot_into_workspace_on_resume(self) -> None:         """Restore snapshots on resume, preserving Runloop's native disk-snapshot fast path."""          root = self._workspace_root_path()         workspace_archive = await self.state.snapshot.restore(dependencies=self.dependencies)         try:             raw = workspace_archive.read()             if isinstance(raw, str):                 raw = raw.encode("utf-8")             if not isinstance(raw, bytes | bytearray):                 raise WorkspaceWriteTypeError(path=root, actual_type=type(raw).__name__)              payload = bytes(raw)             if _decode_runloop_snapshot_ref(payload) is None:                 # Most providers restore tar snapshots by clearing the workspace first, then                 # extracting into an empty root. Runloop differs only for its native snapshot                 # refs, which already replace the entire devbox disk and therefore should not                 # pre-clear the workspace root on resume.                 await self._clear_workspace_root_on_resume()             await self.hydrate_workspace(io.BytesIO(payload))         finally:             try:                 workspace_archive.close()             except Exception:                 pass      async def _hydrate_workspace_via_tar(self, payload: bytes) -> None:         root = self._workspace_root_path()         archive_path = root / f".sandbox-runloop-hydrate-{self.state.session_id.hex}.tar"          try:             validate_tar_bytes(                 payload,                 allow_external_symlink_targets=False,             )         except UnsafeTarMemberError as e:             raise WorkspaceArchiveWriteError(                 path=root,                 context={                     "reason": "unsafe_or_invalid_tar",                     "member": e.member,                     "detail": str(e),                 },                 cause=e,             ) from e          try:             await self.mkdir(root, parents=True)             await self.write(archive_path, io.BytesIO(payload))             result = await self.exec(                 "tar",                 "-C",                 root.as_posix(),                 "-xf",                 archive_path.as_posix(),                 shell=False,                 timeout=self.state.timeouts.snapshot_s,             )             if not result.ok():                 raise WorkspaceArchiveWriteError(                     path=root,                     context={                         "reason": "tar_extract_failed",                         "exit_code": result.exit_code,                         "stderr": result.stderr.decode("utf-8", errors="replace"),                     },                 )         except WorkspaceArchiveWriteError:             raise         except Exception as e:             raise WorkspaceArchiveWriteError(path=root, cause=e) from e         finally:             try:                 await self.exec(                     "rm",                     "-f",                     "--",                     archive_path.as_posix(),                     shell=False,                     timeout=self.state.timeouts.cleanup_s,                 )             except Exception:                 pass ``` |

#### start `async`

```
start() -> None
```

Resume a reconnected Runloop devbox without replaying full setup when possible.

`resume()` marks `_skip_start` when it successfully reconnects to a suspended devbox.
In that path, Runloop reuses the live machine and only reapplies snapshot or ephemeral
manifest state if the cached workspace fingerprint no longer matches.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 ``` | ``` async def start(self) -> None:     """Resume a reconnected Runloop devbox without replaying full setup when possible.      `resume()` marks `_skip_start` when it successfully reconnects to a suspended devbox.     In that path, Runloop reuses the live machine and only reapplies snapshot or ephemeral     manifest state if the cached workspace fingerprint no longer matches.     """     if self._skip_start:         if await self.state.snapshot.restorable(dependencies=self.dependencies):             is_running = await self.running()             fingerprints_match = await self._can_skip_snapshot_restore_on_resume(                 is_running=is_running             )             if fingerprints_match:                 await self._reapply_ephemeral_manifest_on_resume()             else:                 await self._restore_snapshot_into_workspace_on_resume()                 if self.should_provision_manifest_accounts_on_resume():                     await self.provision_manifest_accounts()                 await self._reapply_ephemeral_manifest_on_resume()         else:             await self._reapply_ephemeral_manifest_on_resume()         return     await super().start() ``` |

#### shutdown `async`

```
shutdown() -> None
```

Suspend or delete the underlying Runloop devbox as the final session cleanup step.

`pause_on_exit=True` maps to Runloop suspension so the same devbox can be resumed later.
Otherwise the session shuts the devbox down and treats it as disposable.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 762 763 764 765 766 767 768 769 770 771 772 773 774 775 ``` | ``` async def shutdown(self) -> None:     """Suspend or delete the underlying Runloop devbox as the final session cleanup step.      `pause_on_exit=True` maps to Runloop suspension so the same devbox can be resumed later.     Otherwise the session shuts the devbox down and treats it as disposable.     """     try:         if self.state.pause_on_exit:             await self._devbox.suspend(timeout=self.state.timeouts.suspend_s)             await self._devbox.await_suspended()         else:             await self._devbox.shutdown(timeout=self.state.timeouts.cleanup_s)     except Exception:         pass ``` |

#### resolve\_exposed\_port `async`

```
resolve_exposed_port(port: int) -> ExposedPortEndpoint
```

Resolve an exposed Runloop port through the provider-managed tunnel endpoint.

Runloop may not have a tunnel enabled for a devbox yet, so exposed-port resolution can
trigger tunnel creation before returning the public host, port, and TLS settings.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 916 917 918 919 920 921 922 923 ``` | ``` async def resolve_exposed_port(self, port: int) -> ExposedPortEndpoint:     """Resolve an exposed Runloop port through the provider-managed tunnel endpoint.      Runloop may not have a tunnel enabled for a devbox yet, so exposed-port resolution can     trigger tunnel creation before returning the public host, port, and TLS settings.     """      return await super().resolve_exposed_port(port) ``` |

#### read `async`

```
read(
    path: Path | str, *, user: str | User | None = None
) -> IOBase
```

Read a file via Runloop's binary file API.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 945 946 947 948 949 950 951 952 953 954 955 956 957 958 959 960 961 962 963 964 965 966 967 968 969 970 971 972 ``` | ``` async def read(self, path: Path | str, *, user: str | User | None = None) -> io.IOBase:     """Read a file via Runloop's binary file API."""     error_path = posix_path_as_path(coerce_posix_path(path))     if user is not None:         await self._check_read_with_exec(path, user=user)      normalized_path = await self._validate_path_access(path)     try:         payload = await self._devbox.file.download(             path=sandbox_path_str(normalized_path),             timeout=self.state.timeouts.file_download_s,         )         return io.BytesIO(bytes(payload))     except Exception as e:         if _is_runloop_not_found(e):             raise WorkspaceReadNotFoundError(                 path=error_path,                 context=_runloop_error_context(e, backend_detail="file_download_failed"),                 cause=e,             ) from e         if _is_runloop_provider_error(e):             raise WorkspaceArchiveReadError(                 path=error_path,                 context=_runloop_error_context(e, backend_detail="file_download_failed"),                 cause=e,                 retryable=_runloop_provider_retryability(e),             ) from e         raise WorkspaceArchiveReadError(path=error_path, cause=e) from e ``` |

#### write `async`

```
write(
    path: Path | str,
    data: IOBase,
    *,
    user: str | User | None = None,
) -> None
```

Write a file through Runloop's upload API using manifest-root workspace paths.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ```  974  975  976  977  978  979  980  981  982  983  984  985  986  987  988  989  990  991  992  993  994  995  996  997  998  999 1000 1001 1002 1003 1004 1005 1006 1007 1008 ``` | ``` async def write(     self,     path: Path | str,     data: io.IOBase,     *,     user: str | User | None = None, ) -> None:     """Write a file through Runloop's upload API using manifest-root workspace paths."""     error_path = posix_path_as_path(coerce_posix_path(path))     if user is not None:         await self._check_write_with_exec(path, user=user)      payload = data.read()     if isinstance(payload, str):         payload = payload.encode("utf-8")     if not isinstance(payload, bytes | bytearray):         raise WorkspaceWriteTypeError(path=error_path, actual_type=type(payload).__name__)      workspace_path = await self._validate_path_access(path, for_write=True)     await self.mkdir(workspace_path.parent, parents=True)     try:         await self._devbox.file.upload(             path=sandbox_path_str(workspace_path),             file=bytes(payload),             timeout=self.state.timeouts.file_upload_s,         )     except Exception as e:         if _is_runloop_provider_error(e):             raise WorkspaceArchiveWriteError(                 path=workspace_path,                 context=_runloop_error_context(e, backend_detail="file_upload_failed"),                 cause=e,                 retryable=_runloop_provider_retryability(e),             ) from e         raise WorkspaceArchiveWriteError(path=workspace_path, cause=e) from e ``` |

#### running `async`

```
running() -> bool
```

Report whether the current Runloop devbox is still in the `running` backend state.

Resume logic relies on this backend status check before deciding whether a suspended devbox
can be reused directly or whether snapshot restore must rebuild the workspace elsewhere.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1010 1011 1012 1013 1014 1015 1016 1017 1018 1019 1020 1021 1022 ``` | ``` async def running(self) -> bool:     """Report whether the current Runloop devbox is still in the `running` backend state.      Resume logic relies on this backend status check before deciding whether a suspended devbox     can be reused directly or whether snapshot restore must rebuild the workspace elsewhere.     """     try:         info: RunloopDevboxView = await self._devbox.get_info(             timeout=self.state.timeouts.keepalive_s         )         return cast(str, info.status) == "running"     except Exception:         return False ``` |

#### mkdir `async`

```
mkdir(
    path: Path | str,
    *,
    parents: bool = False,
    user: str | User | None = None,
) -> None
```

Create directories via raw exec so workspace-root creation does not depend on `cd`.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1024 1025 1026 1027 1028 1029 1030 1031 1032 1033 1034 1035 1036 1037 1038 1039 1040 1041 1042 1043 1044 1045 1046 1047 1048 1049 1050 1051 1052 1053 1054 ``` | ``` async def mkdir(     self,     path: Path | str,     *,     parents: bool = False,     user: str | User | None = None, ) -> None:     """Create directories via raw exec so workspace-root creation does not depend on `cd`."""      if user is not None:         path = await self._check_mkdir_with_exec(path, parents=parents, user=user)     else:         path = await self._validate_path_access(path, for_write=True)     cmd = ["mkdir"]     if parents:         cmd.append("-p")     cmd.extend(["--", sandbox_path_str(path)])     result = await self._run_exec_command(         shlex.join(cmd),         command=tuple(cmd),         timeout=self.state.timeouts.fast_op_s,     )     if not result.ok():         raise WorkspaceArchiveWriteError(             path=path,             context={                 "reason": "mkdir_failed",                 "exit_code": result.exit_code,                 "stderr": result.stderr.decode("utf-8", "replace"),             },         ) ``` |

#### persist\_workspace `async`

```
persist_workspace() -> IOBase
```

Persist the workspace with a native Runloop disk snapshot.

Before snapshotting, the session temporarily removes ephemeral skip paths and tears down
ephemeral mounts so the saved disk image contains only durable workspace state, then it
restores those local-only artifacts afterward.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1160 1161 1162 1163 1164 1165 1166 1167 1168 1169 1170 1171 1172 1173 1174 1175 1176 1177 1178 1179 1180 1181 1182 1183 1184 1185 1186 1187 1188 1189 1190 1191 1192 1193 1194 1195 1196 1197 1198 1199 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 1213 1214 1215 1216 1217 1218 1219 1220 1221 1222 1223 1224 1225 1226 1227 1228 1229 1230 1231 1232 1233 1234 1235 1236 1237 1238 1239 1240 1241 1242 1243 1244 1245 1246 1247 1248 1249 1250 1251 1252 1253 1254 1255 1256 1257 1258 1259 1260 1261 1262 1263 1264 1265 1266 1267 1268 1269 1270 1271 1272 ``` | ``` async def persist_workspace(self) -> io.IOBase:     """Persist the workspace with a native Runloop disk snapshot.      Before snapshotting, the session temporarily removes ephemeral skip paths and tears down     ephemeral mounts so the saved disk image contains only durable workspace state, then it     restores those local-only artifacts afterward.     """     root = self._workspace_root_path()     skip = self._persist_workspace_skip_relpaths()     mount_targets = self.state.manifest.ephemeral_mount_targets()     mount_skip_rel_paths: set[Path] = set()     for _mount_entry, mount_path in mount_targets:         try:             mount_skip_rel_paths.add(mount_path.relative_to(root))         except ValueError:             continue     plain_skip = skip - mount_skip_rel_paths      backup: bytes | None = None     unmounted_mounts: list[tuple[Mount, Path]] = []     snapshot_error: WorkspaceArchiveReadError | None = None     snapshot_id: str | None = None      try:         backup = await self._backup_plain_skip_paths(plain_skip)         await self._remove_plain_skip_paths(plain_skip)          for mount_entry, mount_path in mount_targets:             await mount_entry.mount_strategy.teardown_for_snapshot(                 mount_entry,                 self,                 mount_path,             )             unmounted_mounts.append((mount_entry, mount_path))          snapshot: RunloopAsyncSnapshot = await self._devbox.snapshot_disk(             name=f"sandbox-{self.state.session_id.hex[:12]}",             metadata={"openai_agents_session_id": self.state.session_id.hex},             timeout=self.state.timeouts.snapshot_s,         )         snapshot_id = snapshot.id         if not snapshot_id:             raise WorkspaceArchiveReadError(                 path=root,                 context={                     "reason": "snapshot_unexpected_return",                     "type": type(snapshot).__name__,                 },             )     except WorkspaceArchiveReadError as e:         snapshot_error = e     except Exception as e:         retryable = None         if _is_runloop_provider_error(e):             retryable = _runloop_provider_retryability(e)         snapshot_error = WorkspaceArchiveReadError(             path=root,             context={"reason": "snapshot_failed"},             cause=e,             retryable=retryable,         )     finally:         remount_error: WorkspaceArchiveReadError | None = None         for mount_entry, mount_path in reversed(unmounted_mounts):             try:                 await mount_entry.mount_strategy.restore_after_snapshot(                     mount_entry, self, mount_path                 )             except Exception as e:                 current_error = WorkspaceArchiveReadError(path=root, cause=e)                 if remount_error is None:                     remount_error = current_error                 else:                     additional = remount_error.context.setdefault(                         "additional_remount_errors", []                     )                     assert isinstance(additional, list)                     additional.append(                         {                             "message": current_error.message,                             "cause_type": type(e).__name__,                             "cause": str(e),                         }                     )         try:             await self._restore_plain_skip_paths(backup)         except Exception as e:             restore_error = WorkspaceArchiveReadError(path=root, cause=e)             if remount_error is None:                 remount_error = restore_error             else:                 additional = remount_error.context.setdefault("additional_restore_errors", [])                 assert isinstance(additional, list)                 additional.append(                     {                         "message": restore_error.message,                         "cause_type": type(e).__name__,                         "cause": str(e),                     }                 )          if remount_error is not None:             if snapshot_error is not None:                 remount_error.context["snapshot_error_before_restore_corruption"] = {                     "message": snapshot_error.message                 }             raise remount_error      if snapshot_error is not None:         raise snapshot_error      assert snapshot_id is not None     return io.BytesIO(_encode_runloop_snapshot_ref(snapshot_id=snapshot_id)) ``` |

#### hydrate\_workspace `async`

```
hydrate_workspace(data: IOBase) -> None
```

Replace the current devbox from a Runloop snapshot reference or tar archive.

Runloop restore creates a new devbox from the saved disk snapshot and treats that snapshot
filesystem as authoritative, including any tools or files that originally came from the
source blueprint, so restore does not reselect a blueprint. Non-native payloads fall back
to tar hydration so cross-provider snapshots and file snapshots keep working.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1274 1275 1276 1277 1278 1279 1280 1281 1282 1283 1284 1285 1286 1287 1288 1289 1290 1291 1292 1293 1294 1295 1296 1297 1298 1299 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1315 1316 1317 1318 1319 1320 1321 1322 1323 1324 1325 1326 1327 1328 1329 1330 1331 1332 1333 1334 ``` | ``` async def hydrate_workspace(self, data: io.IOBase) -> None:     """Replace the current devbox from a Runloop snapshot reference or tar archive.      Runloop restore creates a new devbox from the saved disk snapshot and treats that snapshot     filesystem as authoritative, including any tools or files that originally came from the     source blueprint, so restore does not reselect a blueprint. Non-native payloads fall back     to tar hydration so cross-provider snapshots and file snapshots keep working.     """     root = self._workspace_root_path()     raw = data.read()     if isinstance(raw, str):         raw = raw.encode("utf-8")     if not isinstance(raw, bytes | bytearray):         raise WorkspaceWriteTypeError(path=root, actual_type=type(raw).__name__)      snapshot_id = _decode_runloop_snapshot_ref(bytes(raw))     if snapshot_id is None:         await self._hydrate_workspace_via_tar(bytes(raw))         return      try:         try:             await self._devbox.shutdown(timeout=self.state.timeouts.cleanup_s)         except Exception:             pass         envs = await self._resolved_envs()         create_kwargs = _runloop_create_kwargs(             blueprint_id=None,             blueprint_name=None,             env_vars=envs,             name=self.state.name,             user_parameters=self.state.user_parameters,             launch_parameters=self.state.launch_parameters,             tunnel=self.state.tunnel,             gateways=self.state.gateways,             mcp=self.state.mcp,             metadata=self.state.metadata,             secrets=self.state.secret_refs,         )         devbox = await self._sdk.devbox.create_from_snapshot(             snapshot_id,             timeout=self.state.timeouts.resume_s,             **create_kwargs,         )         self._devbox = devbox         self.state.devbox_id = devbox.id     except Exception as e:         context: dict[str, object] = {             "reason": "snapshot_restore_failed",             "snapshot_id": snapshot_id,         }         if _is_runloop_provider_error(e):             context.update(_runloop_error_context(e, backend_detail="snapshot_restore_failed"))         raise WorkspaceArchiveWriteError(             path=root,             context=context,             cause=e,             retryable=_runloop_provider_retryability(e)             if _is_runloop_provider_error(e)             else None,         ) from e ``` |

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

### RunloopSandboxClient

Bases: `BaseSandboxClient[RunloopSandboxClientOptions | None]`

Runloop sandbox client managing devbox lifecycle via AsyncRunloopSDK.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1530 1531 1532 1533 1534 1535 1536 1537 1538 1539 1540 1541 1542 1543 1544 1545 1546 1547 1548 1549 1550 1551 1552 1553 1554 1555 1556 1557 1558 1559 1560 1561 1562 1563 1564 1565 1566 1567 1568 1569 1570 1571 1572 1573 1574 1575 1576 1577 1578 1579 1580 1581 1582 1583 1584 1585 1586 1587 1588 1589 1590 1591 1592 1593 1594 1595 1596 1597 1598 1599 1600 1601 1602 1603 1604 1605 1606 1607 1608 1609 1610 1611 1612 1613 1614 1615 1616 1617 1618 1619 1620 1621 1622 1623 1624 1625 1626 1627 1628 1629 1630 1631 1632 1633 1634 1635 1636 1637 1638 1639 1640 1641 1642 1643 1644 1645 1646 1647 1648 1649 1650 1651 1652 1653 1654 1655 1656 1657 1658 1659 1660 1661 1662 1663 1664 1665 1666 1667 1668 1669 1670 1671 1672 1673 1674 1675 1676 1677 1678 1679 1680 1681 1682 1683 1684 1685 1686 1687 1688 1689 1690 1691 1692 1693 1694 1695 1696 1697 1698 1699 1700 1701 1702 1703 1704 1705 1706 1707 1708 1709 1710 1711 1712 1713 1714 1715 1716 1717 1718 1719 1720 ``` | ``` class RunloopSandboxClient(BaseSandboxClient[RunloopSandboxClientOptions | None]):     """Runloop sandbox client managing devbox lifecycle via AsyncRunloopSDK."""      backend_id = "runloop"     supports_default_options = True     _instrumentation: Instrumentation     _platform: RunloopPlatformClient      def __init__(         self,         *,         bearer_token: str | None = None,         base_url: str | None = None,         instrumentation: Instrumentation | None = None,         dependencies: Dependencies | None = None,     ) -> None:         self._sdk = _import_runloop_sdk().async_sdk(bearer_token=bearer_token, base_url=base_url)         self._platform = RunloopPlatformClient(self._sdk)         self._instrumentation = instrumentation or Instrumentation()         self._dependencies = dependencies      @property     def platform(self) -> RunloopPlatformClient:         return self._platform      async def create(         self,         *,         snapshot: SnapshotSpec | SnapshotBase | None = None,         manifest: Manifest | None = None,         options: RunloopSandboxClientOptions | None,     ) -> SandboxSession:         """Create a Runloop devbox and bind it to a manifest rooted under the active home.          Runloop defaults to the `user` account at `/home/user`, but explicit user parameters can         switch the active home, including root launch at `/root`. Client creation validates the         manifest root against that effective home, merges environment variables, and applies any         configured blueprint selection or user profile when provisioning the devbox. The returned         session follows the shared sandbox lifecycle and must be started before direct operations.         """         resolved_options = options or RunloopSandboxClientOptions()         if (             resolved_options.blueprint_id is not None             and resolved_options.blueprint_name is not None         ):             raise ValueError(                 "RunloopSandboxClientOptions cannot set both blueprint_id and blueprint_name"             )          user_parameters = _normalize_runloop_user_parameters(resolved_options.user_parameters)         manifest = manifest or Manifest(root=_default_runloop_manifest_root(user_parameters))         _validate_runloop_manifest_root(manifest, user_parameters=user_parameters)          timeouts_in = resolved_options.timeouts         if isinstance(timeouts_in, RunloopTimeouts):             timeouts = timeouts_in         elif timeouts_in is None:             timeouts = RunloopTimeouts()         else:             timeouts = RunloopTimeouts.model_validate(timeouts_in)          secret_refs = await _upsert_runloop_managed_secrets(             self._sdk,             managed_secrets=resolved_options.managed_secrets,             timeout_s=timeouts.fast_op_s,         )         launch_parameters = _normalize_runloop_launch_parameters(resolved_options.launch_parameters)         tunnel = _normalize_runloop_tunnel_config(resolved_options.tunnel)         base_envs = dict(resolved_options.env_vars or {})         manifest_envs = await manifest.environment.resolve()         envs = {**base_envs, **manifest_envs} or None          create_kwargs = _runloop_create_kwargs(             blueprint_id=resolved_options.blueprint_id,             blueprint_name=resolved_options.blueprint_name,             env_vars=envs,             name=resolved_options.name,             user_parameters=user_parameters,             launch_parameters=launch_parameters,             tunnel=tunnel,             gateways=dict(resolved_options.gateways or {}),             mcp=dict(resolved_options.mcp or {}),             metadata=dict(resolved_options.metadata or {}),             secrets=secret_refs,         )         devbox = await self._sdk.devbox.create(timeout=timeouts.create_s, **create_kwargs)          session_id = uuid.uuid4()         snapshot_instance = resolve_snapshot(snapshot, str(session_id))         state = RunloopSandboxSessionState(             session_id=session_id,             manifest=manifest,             snapshot=snapshot_instance,             devbox_id=devbox.id,             blueprint_id=resolved_options.blueprint_id,             blueprint_name=resolved_options.blueprint_name,             base_env_vars=base_envs,             pause_on_exit=resolved_options.pause_on_exit,             name=resolved_options.name,             timeouts=timeouts,             exposed_ports=resolved_options.exposed_ports,             user_parameters=user_parameters,             launch_parameters=launch_parameters,             tunnel=tunnel,             gateways=dict(resolved_options.gateways or {}),             mcp=dict(resolved_options.mcp or {}),             metadata=dict(resolved_options.metadata or {}),             secret_refs=secret_refs,         )         inner = RunloopSandboxSession.from_state(state, sdk=self._sdk, devbox=devbox)         return self._wrap_session(inner, instrumentation=self._instrumentation)      async def close(self) -> None:         """Close the shared AsyncRunloopSDK client used for devbox operations."""         await self._sdk.aclose()      async def __aenter__(self) -> RunloopSandboxClient:         return self      async def __aexit__(self, *_: object) -> None:         await self.close()      async def delete(self, session: SandboxSession) -> SandboxSession:         """Best-effort release the Runloop devbox when callers delete the session."""         inner = session._inner         if not isinstance(inner, RunloopSandboxSession):             raise TypeError("RunloopSandboxClient.delete expects a RunloopSandboxSession")         try:             await inner.shutdown()         except Exception:             pass         return session      async def resume(         self,         state: SandboxSessionState,     ) -> SandboxSession:         """Resume a persisted Runloop session by reconnecting or reprovisioning a devbox.          The client first tries to reconnect to the stored devbox id, including after an unclean         process/client shutdown where the devbox is still running and `shutdown()` was never         called. If reconnect fails, it creates a fresh devbox with the stored blueprint and         environment settings.         """         if not isinstance(state, RunloopSandboxSessionState):             raise TypeError("RunloopSandboxClient.resume expects a RunloopSandboxSessionState")          devbox = None         reconnected = False         try:             devbox = self._sdk.devbox.from_id(state.devbox_id)             info: RunloopDevboxView = await devbox.get_info(timeout=state.timeouts.keepalive_s)             status = info.status             resume_polling_config = _runloop_polling_config(timeout_s=state.timeouts.resume_s)             if status == "suspended":                 await devbox.resume(timeout=state.timeouts.resume_s)                 await devbox.await_running(polling_config=resume_polling_config)             elif status == "resuming":                 await devbox.await_running(polling_config=resume_polling_config)             elif status != "running":                 raise RuntimeError(f"unexpected_status:{status}")             reconnected = True         except Exception:             devbox = None          if devbox is None:             manifest_envs = await state.manifest.environment.resolve()             envs = {**state.base_env_vars, **manifest_envs} or None             create_kwargs = _runloop_create_kwargs(                 blueprint_id=state.blueprint_id,                 blueprint_name=state.blueprint_name,                 env_vars=envs,                 name=state.name,                 user_parameters=state.user_parameters,                 launch_parameters=state.launch_parameters,                 tunnel=state.tunnel,                 gateways=state.gateways,                 mcp=state.mcp,                 metadata=state.metadata,                 secrets=state.secret_refs,             )             devbox = await self._sdk.devbox.create(timeout=state.timeouts.create_s, **create_kwargs)             state.devbox_id = devbox.id          inner = RunloopSandboxSession.from_state(state, sdk=self._sdk, devbox=devbox)         inner._skip_start = state.pause_on_exit and reconnected         inner._set_start_state_preserved(reconnected, system=reconnected)         return self._wrap_session(inner, instrumentation=self._instrumentation)      def deserialize_session_state(self, payload: dict[str, object]) -> SandboxSessionState:         return RunloopSandboxSessionState.model_validate(payload) ``` |

#### create `async`

```
create(
    *,
    snapshot: SnapshotSpec | SnapshotBase | None = None,
    manifest: Manifest | None = None,
    options: RunloopSandboxClientOptions | None,
) -> SandboxSession
```

Create a Runloop devbox and bind it to a manifest rooted under the active home.

Runloop defaults to the `user` account at `/home/user`, but explicit user parameters can
switch the active home, including root launch at `/root`. Client creation validates the
manifest root against that effective home, merges environment variables, and applies any
configured blueprint selection or user profile when provisioning the devbox. The returned
session follows the shared sandbox lifecycle and must be started before direct operations.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1555 1556 1557 1558 1559 1560 1561 1562 1563 1564 1565 1566 1567 1568 1569 1570 1571 1572 1573 1574 1575 1576 1577 1578 1579 1580 1581 1582 1583 1584 1585 1586 1587 1588 1589 1590 1591 1592 1593 1594 1595 1596 1597 1598 1599 1600 1601 1602 1603 1604 1605 1606 1607 1608 1609 1610 1611 1612 1613 1614 1615 1616 1617 1618 1619 1620 1621 1622 1623 1624 1625 1626 1627 1628 1629 1630 1631 1632 1633 1634 1635 1636 1637 1638 1639 1640 ``` | ``` async def create(     self,     *,     snapshot: SnapshotSpec | SnapshotBase | None = None,     manifest: Manifest | None = None,     options: RunloopSandboxClientOptions | None, ) -> SandboxSession:     """Create a Runloop devbox and bind it to a manifest rooted under the active home.      Runloop defaults to the `user` account at `/home/user`, but explicit user parameters can     switch the active home, including root launch at `/root`. Client creation validates the     manifest root against that effective home, merges environment variables, and applies any     configured blueprint selection or user profile when provisioning the devbox. The returned     session follows the shared sandbox lifecycle and must be started before direct operations.     """     resolved_options = options or RunloopSandboxClientOptions()     if (         resolved_options.blueprint_id is not None         and resolved_options.blueprint_name is not None     ):         raise ValueError(             "RunloopSandboxClientOptions cannot set both blueprint_id and blueprint_name"         )      user_parameters = _normalize_runloop_user_parameters(resolved_options.user_parameters)     manifest = manifest or Manifest(root=_default_runloop_manifest_root(user_parameters))     _validate_runloop_manifest_root(manifest, user_parameters=user_parameters)      timeouts_in = resolved_options.timeouts     if isinstance(timeouts_in, RunloopTimeouts):         timeouts = timeouts_in     elif timeouts_in is None:         timeouts = RunloopTimeouts()     else:         timeouts = RunloopTimeouts.model_validate(timeouts_in)      secret_refs = await _upsert_runloop_managed_secrets(         self._sdk,         managed_secrets=resolved_options.managed_secrets,         timeout_s=timeouts.fast_op_s,     )     launch_parameters = _normalize_runloop_launch_parameters(resolved_options.launch_parameters)     tunnel = _normalize_runloop_tunnel_config(resolved_options.tunnel)     base_envs = dict(resolved_options.env_vars or {})     manifest_envs = await manifest.environment.resolve()     envs = {**base_envs, **manifest_envs} or None      create_kwargs = _runloop_create_kwargs(         blueprint_id=resolved_options.blueprint_id,         blueprint_name=resolved_options.blueprint_name,         env_vars=envs,         name=resolved_options.name,         user_parameters=user_parameters,         launch_parameters=launch_parameters,         tunnel=tunnel,         gateways=dict(resolved_options.gateways or {}),         mcp=dict(resolved_options.mcp or {}),         metadata=dict(resolved_options.metadata or {}),         secrets=secret_refs,     )     devbox = await self._sdk.devbox.create(timeout=timeouts.create_s, **create_kwargs)      session_id = uuid.uuid4()     snapshot_instance = resolve_snapshot(snapshot, str(session_id))     state = RunloopSandboxSessionState(         session_id=session_id,         manifest=manifest,         snapshot=snapshot_instance,         devbox_id=devbox.id,         blueprint_id=resolved_options.blueprint_id,         blueprint_name=resolved_options.blueprint_name,         base_env_vars=base_envs,         pause_on_exit=resolved_options.pause_on_exit,         name=resolved_options.name,         timeouts=timeouts,         exposed_ports=resolved_options.exposed_ports,         user_parameters=user_parameters,         launch_parameters=launch_parameters,         tunnel=tunnel,         gateways=dict(resolved_options.gateways or {}),         mcp=dict(resolved_options.mcp or {}),         metadata=dict(resolved_options.metadata or {}),         secret_refs=secret_refs,     )     inner = RunloopSandboxSession.from_state(state, sdk=self._sdk, devbox=devbox)     return self._wrap_session(inner, instrumentation=self._instrumentation) ``` |

#### close `async`

```
close() -> None
```

Close the shared AsyncRunloopSDK client used for devbox operations.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1642 1643 1644 ``` | ``` async def close(self) -> None:     """Close the shared AsyncRunloopSDK client used for devbox operations."""     await self._sdk.aclose() ``` |

#### delete `async`

```
delete(session: SandboxSession) -> SandboxSession
```

Best-effort release the Runloop devbox when callers delete the session.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1652 1653 1654 1655 1656 1657 1658 1659 1660 1661 ``` | ``` async def delete(self, session: SandboxSession) -> SandboxSession:     """Best-effort release the Runloop devbox when callers delete the session."""     inner = session._inner     if not isinstance(inner, RunloopSandboxSession):         raise TypeError("RunloopSandboxClient.delete expects a RunloopSandboxSession")     try:         await inner.shutdown()     except Exception:         pass     return session ``` |

#### resume `async`

```
resume(state: SandboxSessionState) -> SandboxSession
```

Resume a persisted Runloop session by reconnecting or reprovisioning a devbox.

The client first tries to reconnect to the stored devbox id, including after an unclean
process/client shutdown where the devbox is still running and `shutdown()` was never
called. If reconnect fails, it creates a fresh devbox with the stored blueprint and
environment settings.

Source code in `src/agents/extensions/sandbox/runloop/sandbox.py`

|  |  |
| --- | --- |
| ``` 1663 1664 1665 1666 1667 1668 1669 1670 1671 1672 1673 1674 1675 1676 1677 1678 1679 1680 1681 1682 1683 1684 1685 1686 1687 1688 1689 1690 1691 1692 1693 1694 1695 1696 1697 1698 1699 1700 1701 1702 1703 1704 1705 1706 1707 1708 1709 1710 1711 1712 1713 1714 1715 1716 1717 ``` | ``` async def resume(     self,     state: SandboxSessionState, ) -> SandboxSession:     """Resume a persisted Runloop session by reconnecting or reprovisioning a devbox.      The client first tries to reconnect to the stored devbox id, including after an unclean     process/client shutdown where the devbox is still running and `shutdown()` was never     called. If reconnect fails, it creates a fresh devbox with the stored blueprint and     environment settings.     """     if not isinstance(state, RunloopSandboxSessionState):         raise TypeError("RunloopSandboxClient.resume expects a RunloopSandboxSessionState")      devbox = None     reconnected = False     try:         devbox = self._sdk.devbox.from_id(state.devbox_id)         info: RunloopDevboxView = await devbox.get_info(timeout=state.timeouts.keepalive_s)         status = info.status         resume_polling_config = _runloop_polling_config(timeout_s=state.timeouts.resume_s)         if status == "suspended":             await devbox.resume(timeout=state.timeouts.resume_s)             await devbox.await_running(polling_config=resume_polling_config)         elif status == "resuming":             await devbox.await_running(polling_config=resume_polling_config)         elif status != "running":             raise RuntimeError(f"unexpected_status:{status}")         reconnected = True     except Exception:         devbox = None      if devbox is None:         manifest_envs = await state.manifest.environment.resolve()         envs = {**state.base_env_vars, **manifest_envs} or None         create_kwargs = _runloop_create_kwargs(             blueprint_id=state.blueprint_id,             blueprint_name=state.blueprint_name,             env_vars=envs,             name=state.name,             user_parameters=state.user_parameters,             launch_parameters=state.launch_parameters,             tunnel=state.tunnel,             gateways=state.gateways,             mcp=state.mcp,             metadata=state.metadata,             secrets=state.secret_refs,         )         devbox = await self._sdk.devbox.create(timeout=state.timeouts.create_s, **create_kwargs)         state.devbox_id = devbox.id      inner = RunloopSandboxSession.from_state(state, sdk=self._sdk, devbox=devbox)     inner._skip_start = state.pause_on_exit and reconnected     inner._set_start_state_preserved(reconnected, system=reconnected)     return self._wrap_session(inner, instrumentation=self._instrumentation) ``` |

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