---
url: https://docs.crewai.com/edge/en/enterprise/guides/outlook-trigger
title: Outlook Trigger
framework: crewai
---

# Outlook Trigger

> Launch automations from Outlook emails and calendar updates

## Overview

Automate responses when Outlook delivers a new message or when an event is removed from the calendar. Teams commonly route escalations, file tickets, or alert attendees of cancellations.

<Tip>
  Connect Outlook in **Tools & Integrations** and ensure the trigger is enabled
  for your deployment.
</Tip>

## Enabling the Outlook Trigger

1. Open your deployment in CrewAI AMP
2. Go to the **Triggers** tab
3. Locate **Outlook** and switch the toggle to enable

<Frame caption="Microsoft Outlook trigger connection">
  <img src="https://mintcdn.com/crewai/oMMe1eXJrzmWf3MN/images/enterprise/outlook-trigger.png?fit=max&auto=format&n=oMMe1eXJrzmWf3MN&q=85&s=f8a739ad0963ccddafeed60f21366628" alt="Enable or disable triggers with toggle" width="2186" height="508" data-path="images/enterprise/outlook-trigger.png" />
</Frame>

## Example: Summarize a new email

```python
from outlook_message_crew import OutlookMessageTrigger

crew = OutlookMessageTrigger().crew()
crew.kickoff({
    "crewai_trigger_payload": outlook_payload,
})
```

The crew extracts sender details, subject, body preview, and attachments before generating a structured response.

## Testing Locally

Test your Outlook trigger integration locally using the CrewAI CLI:

```bash
# View all available triggers
crewai triggers list

# Simulate an Outlook trigger with realistic payload
crewai triggers run microsoft_outlook/email_received
```

The `crewai triggers run` command will execute your crew with a complete Outlook payload, allowing you to test your parsing logic before deployment.

<Warning>
  Use `crewai triggers run microsoft_outlook/email_received` (not `crewai run`)
  to simulate trigger execution during development. After deployment, your crew
  will automatically receive the trigger payload.
</Warning>

## Troubleshooting

* Verify the Outlook connector is still authorized; the subscription must be renewed periodically
* Test locally with `crewai triggers run microsoft_outlook/email_received` to see the exact payload structure
* If attachments are missing, confirm the webhook subscription includes the `includeResourceData` flag
* Review execution logs when events fail to match—cancellation payloads lack attendee lists by design and the crew should account for that
* Remember: use `crewai triggers run` (not `crewai run`) to simulate trigger execution