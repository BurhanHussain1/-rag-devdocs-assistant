---
url: https://openai.github.io/openai-agents-python/ref/computer/
title: `Computer`
framework: openai
---

# `Computer`

### Computer

Bases: `ABC`

A computer implemented with sync operations.

Subclasses provide the local runtime behind `ComputerTool`. Mouse action methods may
also accept a keyword-only `keys` argument to receive held modifier keys when the
driver supports them.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ```  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 ``` | ``` class Computer(abc.ABC):     """A computer implemented with sync operations.      Subclasses provide the local runtime behind `ComputerTool`. Mouse action methods may     also accept a keyword-only `keys` argument to receive held modifier keys when the     driver supports them.     """      @property     def environment(self) -> Environment | None:         """Return preview tool metadata when the preview computer payload is required."""         return None      @property     def dimensions(self) -> tuple[int, int] | None:         """Return preview display dimensions when the preview computer payload is required."""         return None      @abc.abstractmethod     def screenshot(self) -> str:         """Return a base64-encoded PNG screenshot of the current display."""         pass      @abc.abstractmethod     def click(self, x: int, y: int, button: Button) -> None:         """Click `button` at the given `(x, y)` screen coordinates."""         pass      @abc.abstractmethod     def double_click(self, x: int, y: int) -> None:         """Double-click at the given `(x, y)` screen coordinates."""         pass      @abc.abstractmethod     def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:         """Scroll at `(x, y)` by `(scroll_x, scroll_y)` units."""         pass      @abc.abstractmethod     def type(self, text: str) -> None:         """Type `text` into the currently focused target."""         pass      @abc.abstractmethod     def wait(self) -> None:         """Wait until the computer is ready for the next action."""         pass      @abc.abstractmethod     def move(self, x: int, y: int) -> None:         """Move the mouse cursor to the given `(x, y)` screen coordinates."""         pass      @abc.abstractmethod     def keypress(self, keys: list[str]) -> None:         """Press the provided keys, such as `["ctrl", "c"]`."""         pass      @abc.abstractmethod     def drag(self, path: list[tuple[int, int]]) -> None:         """Click-and-drag the mouse along the given sequence of `(x, y)` waypoints."""         pass ``` |

#### environment `property`

```
environment: Environment | None
```

Return preview tool metadata when the preview computer payload is required.

#### dimensions `property`

```
dimensions: tuple[int, int] | None
```

Return preview display dimensions when the preview computer payload is required.

#### screenshot `abstractmethod`

```
screenshot() -> str
```

Return a base64-encoded PNG screenshot of the current display.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 26 27 28 29 ``` | ``` @abc.abstractmethod def screenshot(self) -> str:     """Return a base64-encoded PNG screenshot of the current display."""     pass ``` |

#### click `abstractmethod`

```
click(x: int, y: int, button: Button) -> None
```

Click `button` at the given `(x, y)` screen coordinates.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 31 32 33 34 ``` | ``` @abc.abstractmethod def click(self, x: int, y: int, button: Button) -> None:     """Click `button` at the given `(x, y)` screen coordinates."""     pass ``` |

#### double\_click `abstractmethod`

```
double_click(x: int, y: int) -> None
```

Double-click at the given `(x, y)` screen coordinates.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 36 37 38 39 ``` | ``` @abc.abstractmethod def double_click(self, x: int, y: int) -> None:     """Double-click at the given `(x, y)` screen coordinates."""     pass ``` |

#### scroll `abstractmethod`

```
scroll(
    x: int, y: int, scroll_x: int, scroll_y: int
) -> None
```

Scroll at `(x, y)` by `(scroll_x, scroll_y)` units.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 41 42 43 44 ``` | ``` @abc.abstractmethod def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:     """Scroll at `(x, y)` by `(scroll_x, scroll_y)` units."""     pass ``` |

#### type `abstractmethod`

```
type(text: str) -> None
```

Type `text` into the currently focused target.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 46 47 48 49 ``` | ``` @abc.abstractmethod def type(self, text: str) -> None:     """Type `text` into the currently focused target."""     pass ``` |

#### wait `abstractmethod`

```
wait() -> None
```

Wait until the computer is ready for the next action.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 51 52 53 54 ``` | ``` @abc.abstractmethod def wait(self) -> None:     """Wait until the computer is ready for the next action."""     pass ``` |

#### move `abstractmethod`

```
move(x: int, y: int) -> None
```

Move the mouse cursor to the given `(x, y)` screen coordinates.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 56 57 58 59 ``` | ``` @abc.abstractmethod def move(self, x: int, y: int) -> None:     """Move the mouse cursor to the given `(x, y)` screen coordinates."""     pass ``` |

#### keypress `abstractmethod`

```
keypress(keys: list[str]) -> None
```

Press the provided keys, such as `["ctrl", "c"]`.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 61 62 63 64 ``` | ``` @abc.abstractmethod def keypress(self, keys: list[str]) -> None:     """Press the provided keys, such as `["ctrl", "c"]`."""     pass ``` |

#### drag `abstractmethod`

```
drag(path: list[tuple[int, int]]) -> None
```

Click-and-drag the mouse along the given sequence of `(x, y)` waypoints.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 66 67 68 69 ``` | ``` @abc.abstractmethod def drag(self, path: list[tuple[int, int]]) -> None:     """Click-and-drag the mouse along the given sequence of `(x, y)` waypoints."""     pass ``` |

### AsyncComputer

Bases: `ABC`

A computer implemented with async operations.

Subclasses provide the local runtime behind `ComputerTool`. Mouse action methods may
also accept a keyword-only `keys` argument to receive held modifier keys when the
driver supports them.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ```  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 ``` | ``` class AsyncComputer(abc.ABC):     """A computer implemented with async operations.      Subclasses provide the local runtime behind `ComputerTool`. Mouse action methods may     also accept a keyword-only `keys` argument to receive held modifier keys when the     driver supports them.     """      @property     def environment(self) -> Environment | None:         """Return preview tool metadata when the preview computer payload is required."""         return None      @property     def dimensions(self) -> tuple[int, int] | None:         """Return preview display dimensions when the preview computer payload is required."""         return None      @abc.abstractmethod     async def screenshot(self) -> str:         """Return a base64-encoded PNG screenshot of the current display."""         pass      @abc.abstractmethod     async def click(self, x: int, y: int, button: Button) -> None:         """Click `button` at the given `(x, y)` screen coordinates."""         pass      @abc.abstractmethod     async def double_click(self, x: int, y: int) -> None:         """Double-click at the given `(x, y)` screen coordinates."""         pass      @abc.abstractmethod     async def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:         """Scroll at `(x, y)` by `(scroll_x, scroll_y)` units."""         pass      @abc.abstractmethod     async def type(self, text: str) -> None:         """Type `text` into the currently focused target."""         pass      @abc.abstractmethod     async def wait(self) -> None:         """Wait until the computer is ready for the next action."""         pass      @abc.abstractmethod     async def move(self, x: int, y: int) -> None:         """Move the mouse cursor to the given `(x, y)` screen coordinates."""         pass      @abc.abstractmethod     async def keypress(self, keys: list[str]) -> None:         """Press the provided keys, such as `["ctrl", "c"]`."""         pass      @abc.abstractmethod     async def drag(self, path: list[tuple[int, int]]) -> None:         """Click-and-drag the mouse along the given sequence of `(x, y)` waypoints."""         pass ``` |

#### environment `property`

```
environment: Environment | None
```

Return preview tool metadata when the preview computer payload is required.

#### dimensions `property`

```
dimensions: tuple[int, int] | None
```

Return preview display dimensions when the preview computer payload is required.

#### screenshot `abstractmethod` `async`

```
screenshot() -> str
```

Return a base64-encoded PNG screenshot of the current display.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 90 91 92 93 ``` | ``` @abc.abstractmethod async def screenshot(self) -> str:     """Return a base64-encoded PNG screenshot of the current display."""     pass ``` |

#### click `abstractmethod` `async`

```
click(x: int, y: int, button: Button) -> None
```

Click `button` at the given `(x, y)` screen coordinates.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 95 96 97 98 ``` | ``` @abc.abstractmethod async def click(self, x: int, y: int, button: Button) -> None:     """Click `button` at the given `(x, y)` screen coordinates."""     pass ``` |

#### double\_click `abstractmethod` `async`

```
double_click(x: int, y: int) -> None
```

Double-click at the given `(x, y)` screen coordinates.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 100 101 102 103 ``` | ``` @abc.abstractmethod async def double_click(self, x: int, y: int) -> None:     """Double-click at the given `(x, y)` screen coordinates."""     pass ``` |

#### scroll `abstractmethod` `async`

```
scroll(
    x: int, y: int, scroll_x: int, scroll_y: int
) -> None
```

Scroll at `(x, y)` by `(scroll_x, scroll_y)` units.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 105 106 107 108 ``` | ``` @abc.abstractmethod async def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:     """Scroll at `(x, y)` by `(scroll_x, scroll_y)` units."""     pass ``` |

#### type `abstractmethod` `async`

```
type(text: str) -> None
```

Type `text` into the currently focused target.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 110 111 112 113 ``` | ``` @abc.abstractmethod async def type(self, text: str) -> None:     """Type `text` into the currently focused target."""     pass ``` |

#### wait `abstractmethod` `async`

```
wait() -> None
```

Wait until the computer is ready for the next action.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 115 116 117 118 ``` | ``` @abc.abstractmethod async def wait(self) -> None:     """Wait until the computer is ready for the next action."""     pass ``` |

#### move `abstractmethod` `async`

```
move(x: int, y: int) -> None
```

Move the mouse cursor to the given `(x, y)` screen coordinates.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 120 121 122 123 ``` | ``` @abc.abstractmethod async def move(self, x: int, y: int) -> None:     """Move the mouse cursor to the given `(x, y)` screen coordinates."""     pass ``` |

#### keypress `abstractmethod` `async`

```
keypress(keys: list[str]) -> None
```

Press the provided keys, such as `["ctrl", "c"]`.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 125 126 127 128 ``` | ``` @abc.abstractmethod async def keypress(self, keys: list[str]) -> None:     """Press the provided keys, such as `["ctrl", "c"]`."""     pass ``` |

#### drag `abstractmethod` `async`

```
drag(path: list[tuple[int, int]]) -> None
```

Click-and-drag the mouse along the given sequence of `(x, y)` waypoints.

Source code in `src/agents/computer.py`

|  |  |
| --- | --- |
| ``` 130 131 132 133 ``` | ``` @abc.abstractmethod async def drag(self, path: list[tuple[int, int]]) -> None:     """Click-and-drag the mouse along the given sequence of `(x, y)` waypoints."""     pass ``` |