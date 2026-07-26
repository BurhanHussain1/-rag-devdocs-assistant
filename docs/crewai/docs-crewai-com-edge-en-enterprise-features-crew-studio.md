---
url: https://docs.crewai.com/edge/en/enterprise/features/crew-studio
title: Crew Studio
framework: crewai
---

# Crew Studio

> Build new automations with AI assistance, a visual editor, and integrated testing.

## Overview

Crew Studio is an interactive, AI‑assisted workspace for creating new automations from scratch using natural language and a visual workflow editor.

<Frame>
  <img src="https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/crew-studio-overview.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=78db59d2d246ccbc7a5c53c8dc2ac9b2" alt="Crew Studio Overview" width="3648" height="2350" data-path="images/enterprise/crew-studio-overview.png" />
</Frame>

## Prompt‑based Creation

* Describe the automation you want; the AI generates agents, tasks, and tools.
* Use voice input via the microphone icon if preferred.
* Start from built‑in prompts for common use cases.

<Frame>
  <img src="https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/crew-studio-prompt.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=10394b6192b729f9e861a43515e2c636" alt="Prompt Builder" width="3648" height="2266" data-path="images/enterprise/crew-studio-prompt.png" />
</Frame>

## Visual Editor

The canvas reflects the workflow as nodes and edges with three supporting panels that allow you to configure the workflow easily without writing code; a.k.a. "**vibe coding AI Agents**".

You can use the drag-and-drop functionality to add agents, tasks, and tools to the canvas or you can use the chat section to build the agents. Both approaches share state and can be used interchangeably.

* **AI Thoughts (left)**: streaming reasoning as the workflow is designed
* **Canvas (center)**: agents and tasks as connected nodes
* **Resources (right)**: drag‑and‑drop components (agents, tasks, tools)

<Frame>
  <img src="https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/crew-studio-canvas.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=b112618b6609ddabc984955706b8365f" alt="Visual Canvas" width="3648" height="2266" data-path="images/enterprise/crew-studio-canvas.png" />
</Frame>

## Execution & Debugging

Switch to the <b>Execution</b> view to run and observe the workflow:

* Event timeline
* Detailed logs (Details, Messages, Raw Data)
* Local test runs before publishing

<Frame>
  <img src="https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/crew-studio-execution.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=6dc19227c8ad45cf3fed625a7b8ef47e" alt="Execution View" width="3648" height="2266" data-path="images/enterprise/crew-studio-execution.png" />
</Frame>

## Publish & Export

* <b>Publish</b> to deploy a live automation
* <b>Download</b> source as a ZIP for local development or customization

<Frame>
  <img src="https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/crew-studio-publish.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=576d6e2759a7289c0b5adf4e4511ec65" alt="Publish & Download" width="3648" height="2266" data-path="images/enterprise/crew-studio-publish.png" />
</Frame>

Once published, you can view the automation details and have the **Options** dropdown menu to `chat with this crew`, `Export React Component` and `Export as MCP`.

<Frame>
  <img src="https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/crew-studio-published.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=8c5d967e43092ee26185f391b0554c46" alt="Published Automation" width="3648" height="2266" data-path="images/enterprise/crew-studio-published.png" />
</Frame>

## Best Practices

* Iterate quickly in Studio; publish only when stable
* Keep tools constrained to minimum permissions needed
* Use Traces to validate behavior and performance

## Related

<CardGroup cols={4}>
  <Card title="Enable Crew Studio" href="/en/enterprise/guides/enable-crew-studio" icon="palette">
    Enable Crew Studio.
  </Card>

  <Card title="Build a Crew" href="/en/enterprise/guides/build-crew" icon="paintbrush">
    Build a Crew.
  </Card>

  <Card title="Deploy a Crew" href="/en/enterprise/guides/deploy-crew" icon="rocket">
    Deploy a Crew from GitHub or ZIP file.
  </Card>

  <Card title="Export a React Component" href="/en/enterprise/guides/react-component-export" icon="download">
    Export a React Component.
  </Card>
</CardGroup>