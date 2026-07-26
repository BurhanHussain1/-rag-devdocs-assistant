---
url: https://docs.crewai.com/edge/en/enterprise/features/automations
title: Automations
framework: crewai
---

# Automations

> Manage, deploy, and monitor your live crews (automations) in one place.

## Overview

Automations is the live operations hub for your deployed crews. Use it to deploy from GitHub or a ZIP file, manage environment variables, re‑deploy when needed, and monitor the status of each automation.

<Frame>
  <img src="https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/automations-overview.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=a7d0655da82c70b0ca152715cb8253f4" alt="Automations Overview" width="3648" height="2266" data-path="images/enterprise/automations-overview.png" />
</Frame>

## Deployment Methods

### Deploy from GitHub

Use this for version‑controlled projects and continuous deployment.

<Steps>
  <Step title="Connect GitHub">
    Click <b>Configure GitHub</b> and authorize access.
  </Step>

  <Step title="Select Repository & Branch">
    Choose the <b>Repository</b> and <b>Branch</b> you want to deploy from.
  </Step>

  <Step title="Enable Auto‑deploy (optional)">
    Turn on <b>Automatically deploy new commits</b> to ship updates on every push.
  </Step>

  <Step title="Add Environment Variables">
    Add secrets individually or use <b>Bulk View</b> for multiple variables.
  </Step>

  <Step title="Deploy">
    Click <b>Deploy</b> to create your live automation.
  </Step>
</Steps>

<Frame>
  <img src="https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/deploy-from-github.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=4fb72dc68799d5a0c35e2e74f1a7cc6c" alt="GitHub Deployment" width="3648" height="2266" data-path="images/enterprise/deploy-from-github.png" />
</Frame>

### Deploy from ZIP

Ship quickly without Git—upload a compressed package of your project.

<Steps>
  <Step title="Choose File">
    Select the ZIP archive from your computer.
  </Step>

  <Step title="Add Environment Variables">
    Provide any required variables or keys.
  </Step>

  <Step title="Deploy">
    Click <b>Deploy</b> to create your live automation.
  </Step>
</Steps>

<Frame>
  <img src="https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/deploy-from-zip.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=8cea74868a553d34b0aa182ad5489099" alt="ZIP Deployment" width="3648" height="2266" data-path="images/enterprise/deploy-from-zip.png" />
</Frame>

## Automations Dashboard

The table lists all live automations with key details:

* **CREW**: Automation name
* **STATUS**: Online / Failed / In Progress
* **URL**: Endpoint for kickoff/status
* **TOKEN**: Automation token
* **ACTIONS**: Re‑deploy, delete, and more

Use the top‑right controls to filter and search:

* Search by name
* Filter by <b>Status</b>
* Filter by <b>Source</b> (GitHub / Studio / ZIP)

Once deployed, you can view the automation details and have the **Options** dropdown menu to `chat with this crew`, `Export React Component` and `Export as MCP`.

<Frame>
  <img src="https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/automations-table.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=f7fb571e8473f5cb7940c3e3bb34f95c" alt="Automations Table" width="2874" height="932" data-path="images/enterprise/automations-table.png" />
</Frame>

## Best Practices

* Prefer GitHub deployments for version control and CI/CD
* Use re‑deploy to roll forward after code or config updates or set it to auto-deploy on every push

## Related

<CardGroup cols={3}>
  <Card title="Deploy a Crew" href="/en/enterprise/guides/deploy-crew" icon="rocket">
    Deploy a Crew from GitHub or ZIP file.
  </Card>

  <Card title="Automation Triggers" href="/en/enterprise/guides/automation-triggers" icon="trigger">
    Trigger automations via webhooks or API.
  </Card>

  <Card title="Webhook Automation" href="/en/enterprise/guides/webhook-automation" icon="webhook">
    Stream real-time events and updates to your systems.
  </Card>
</CardGroup>