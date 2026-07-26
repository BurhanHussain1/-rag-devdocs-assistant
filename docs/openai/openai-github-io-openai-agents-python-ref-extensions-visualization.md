---
url: https://openai.github.io/openai-agents-python/ref/extensions/visualization/
title: `Visualization`
framework: openai
---

# `Visualization`

### get\_main\_graph

```
get_main_graph(agent: Agent) -> str
```

Generates the main graph structure in DOT format for the given agent.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `Agent` | The agent for which the graph is to be generated. | *required* |

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `str` | `str` | The DOT format string representing the graph. |

Source code in `src/agents/extensions/visualization.py`

|  |  |
| --- | --- |
| ``` 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 ``` | ``` def get_main_graph(agent: Agent) -> str:     """     Generates the main graph structure in DOT format for the given agent.      Args:         agent (Agent): The agent for which the graph is to be generated.      Returns:         str: The DOT format string representing the graph.     """     parts = [         """     digraph G {         graph [splines=true];         node [fontname="Arial"];         edge [penwidth=1.5];     """     ]     parts.append(get_all_nodes(agent))     parts.append(get_all_edges(agent))     parts.append("}")     return "".join(parts) ``` |

### get\_all\_nodes

```
get_all_nodes(
    agent: Agent,
    parent: Agent | None = None,
    visited: set[str] | None = None,
) -> str
```

Recursively generates the nodes for the given agent and its handoffs in DOT format.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `Agent` | The agent for which the nodes are to be generated. | *required* |

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `str` | `str` | The DOT format string representing the nodes. |

Source code in `src/agents/extensions/visualization.py`

|  |  |
| --- | --- |
| ```  49  50  51  52  53  54  55  56  57  58  59  60  61  62  63  64  65  66  67  68  69  70  71  72  73  74  75  76  77  78  79  80  81  82  83  84  85  86  87  88  89  90  91  92  93  94  95  96  97  98  99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 ``` | ``` def get_all_nodes(     agent: Agent, parent: Agent | None = None, visited: set[str] | None = None ) -> str:     """     Recursively generates the nodes for the given agent and its handoffs in DOT format.      Args:         agent (Agent): The agent for which the nodes are to be generated.      Returns:         str: The DOT format string representing the nodes.     """     if visited is None:         visited = set()     if agent.name in visited:         return ""     visited.add(agent.name)      parts = []      # Start and end the graph     if not parent:         parts.append(             '"__start__" [label="__start__", shape=ellipse, style=filled, '             "fillcolor=lightblue, width=0.5, height=0.3];"             '"__end__" [label="__end__", shape=ellipse, style=filled, '             "fillcolor=lightblue, width=0.5, height=0.3];"         )         # Ensure parent agent node is colored         name = _escape_label(agent.name)         parts.append(             f'"{name}" [label="{name}", '             "shape=box, style=filled, "             "fillcolor=lightyellow, width=1.5, height=0.8];"         )      for tool in agent.tools:         name = _escape_label(tool.name)         parts.append(             f'"{name}" [label="{name}", '             "shape=ellipse, style=filled, "             "fillcolor=lightgreen, width=0.5, height=0.3];"         )      for mcp_server in agent.mcp_servers:         name = _escape_label(mcp_server.name)         parts.append(             f'"{name}" [label="{name}", '             "shape=box, style=filled, "             "fillcolor=lightgrey, width=1, height=0.5];"         )      for handoff in agent.handoffs:         if isinstance(handoff, Handoff):             name = _escape_label(handoff.agent_name)             parts.append(                 f'"{name}" [label="{name}", '                 f'shape=box, style="filled,rounded", '                 f"fillcolor=lightyellow, width=1.5, height=0.8];"             )         if isinstance(handoff, Agent):             if handoff.name not in visited:                 name = _escape_label(handoff.name)                 parts.append(                     f'"{name}" [label="{name}", '                     f'shape=box, style="filled,rounded", '                     f"fillcolor=lightyellow, width=1.5, height=0.8];"                 )             parts.append(get_all_nodes(handoff, agent, visited))      return "".join(parts) ``` |

### get\_all\_edges

```
get_all_edges(
    agent: Agent,
    parent: Agent | None = None,
    visited: set[str] | None = None,
) -> str
```

Recursively generates the edges for the given agent and its handoffs in DOT format.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `Agent` | The agent for which the edges are to be generated. | *required* |
| `parent` | `Agent` | The parent agent. Defaults to None. | `None` |

Returns:

| Name | Type | Description |
| --- | --- | --- |
| `str` | `str` | The DOT format string representing the edges. |

Source code in `src/agents/extensions/visualization.py`

|  |  |
| --- | --- |
| ``` 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 ``` | ``` def get_all_edges(     agent: Agent, parent: Agent | None = None, visited: set[str] | None = None ) -> str:     """     Recursively generates the edges for the given agent and its handoffs in DOT format.      Args:         agent (Agent): The agent for which the edges are to be generated.         parent (Agent, optional): The parent agent. Defaults to None.      Returns:         str: The DOT format string representing the edges.     """     if visited is None:         visited = set()     if agent.name in visited:         return ""     visited.add(agent.name)      parts = []      agent_name = _escape_label(agent.name)      if not parent:         parts.append(f'"__start__" -> "{agent_name}";')      for tool in agent.tools:         tool_name = _escape_label(tool.name)         parts.append(f"""         "{agent_name}" -> "{tool_name}" [style=dotted, penwidth=1.5];         "{tool_name}" -> "{agent_name}" [style=dotted, penwidth=1.5];""")      for mcp_server in agent.mcp_servers:         server_name = _escape_label(mcp_server.name)         parts.append(f"""         "{agent_name}" -> "{server_name}" [style=dashed, penwidth=1.5];         "{server_name}" -> "{agent_name}" [style=dashed, penwidth=1.5];""")      for handoff in agent.handoffs:         if isinstance(handoff, Handoff):             parts.append(f"""             "{agent_name}" -> "{_escape_label(handoff.agent_name)}";""")         if isinstance(handoff, Agent):             parts.append(f"""             "{agent_name}" -> "{_escape_label(handoff.name)}";""")             parts.append(get_all_edges(handoff, agent, visited))      if not agent.handoffs:         parts.append(f'"{agent_name}" -> "__end__";')      return "".join(parts) ``` |

### draw\_graph

```
draw_graph(
    agent: Agent, filename: str | None = None
) -> Source
```

Draws the graph for the given agent and optionally saves it as a PNG file.

Parameters:

| Name | Type | Description | Default |
| --- | --- | --- | --- |
| `agent` | `Agent` | The agent for which the graph is to be drawn. | *required* |
| `filename` | `str` | The name of the file to save the graph as a PNG. | `None` |

Returns:

| Type | Description |
| --- | --- |
| `Source` | graphviz.Source: The graphviz Source object representing the graph. |

Source code in `src/agents/extensions/visualization.py`

|  |  |
| --- | --- |
| ``` 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 ``` | ``` def draw_graph(agent: Agent, filename: str | None = None) -> graphviz.Source:     """     Draws the graph for the given agent and optionally saves it as a PNG file.      Args:         agent (Agent): The agent for which the graph is to be drawn.         filename (str): The name of the file to save the graph as a PNG.      Returns:         graphviz.Source: The graphviz Source object representing the graph.     """     dot_code = get_main_graph(agent)     graph = graphviz.Source(dot_code)      if filename:         graph.render(filename, format="png", cleanup=True)      return graph ``` |