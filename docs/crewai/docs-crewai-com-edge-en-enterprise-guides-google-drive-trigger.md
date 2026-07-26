---
url: https://docs.crewai.com/edge/en/enterprise/guides/google-drive-trigger
title: Google Drive Trigger
framework: crewai
---

# Google Drive Trigger

> Respond to Google Drive file events with automated crews

## Overview

Trigger your automations when files are created, updated, or removed in Google Drive. Typical workflows include summarizing newly uploaded content, enforcing sharing policies, or notifying owners when critical files change.

<Tip>
  Connect Google Drive in **Tools & Integrations** and confirm the trigger is
  enabled for the automation you want to monitor.
</Tip>

## Enabling the Google Drive Trigger

1. Open your deployment in CrewAI AMP
2. Go to the **Triggers** tab
3. Locate **Google Drive** and switch the toggle to enable

<Frame>
  <img src="https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/gdrive-trigger.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=caef65990821bbc38454b46ca8f7bc46" alt="Enable or disable triggers with toggle" width="2208" height="1540" data-path="images/enterprise/gdrive-trigger.png" />
</Frame>

## Example: Summarize file activity

The drive example crews parse the payload to extract file metadata, evaluate permissions, and publish a summary.

```python
from drive_file_crew import GoogleDriveFileTrigger

crew = GoogleDriveFileTrigger().crew()
crew.kickoff({
    "crewai_trigger_payload": drive_payload,
})
```

## Testing Locally

Test your Google Drive trigger integration locally using the CrewAI CLI:

```bash
# View all available triggers
crewai triggers list

# Simulate a Google Drive trigger with realistic payload
crewai triggers run google_drive/file_changed
```

The `crewai triggers run` command will execute your crew with a complete Drive payload, allowing you to test your parsing logic before deployment.

<Warning>
  Use `crewai triggers run google_drive/file_changed` (not `crewai run`) to
  simulate trigger execution during development. After deployment, your crew
  will automatically receive the trigger payload.
</Warning>

## Monitoring Executions

Track history and performance of triggered runs with the **Executions** list in the deployment dashboard.

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/list-executions.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=be7efd03eb810139e42a10815402158d" alt="List of executions triggered by automation" width="1950" height="1358" data-path="images/enterprise/list-executions.png" />
</Frame>

## Troubleshooting

* Verify Google Drive is connected and the trigger toggle is enabled
* Test locally with `crewai triggers run google_drive/file_changed` to see the exact payload structure
* If a payload is missing permission data, ensure the connected account has access to the file or folder
* The trigger sends file IDs only; use the Drive API if you need to fetch binary content during the crew run
* Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution