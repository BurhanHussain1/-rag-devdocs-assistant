---
url: https://docs.crewai.com/edge/en/enterprise/guides/slack-trigger
title: Slack Trigger
framework: crewai
---

# Slack Trigger

> Trigger CrewAI crews directly from Slack using slash commands

This guide explains how to start a crew directly from Slack using CrewAI triggers.

## Prerequisites

* CrewAI Slack trigger installed and connected to your Slack workspace
* At least one crew configured in CrewAI

## Setup Steps

<Steps>
  <Step title="Ensure the CrewAI Slack trigger is set up">
    In the CrewAI dashboard, navigate to the **Triggers** section.

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/slack-integration.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=6d976bf9516d737af0b7ea3a77aa2b2a" alt="CrewAI Slack Integration" width="1962" height="1052" data-path="images/enterprise/slack-integration.png" />
    </Frame>

    Verify that Slack is listed and is connected.
  </Step>

  <Step title="Open your Slack channel">
    * Navigate to the channel where you want to kickoff the crew.
    * Type the slash command "**/kickoff**" to initiate the crew kickoff process.
    * You should see a  "**Kickoff crew**" appear as you type:
          <Frame>
            <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/kickoff-slack-crew.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=cf16579e88e59903af9ac3f2ef374555" alt="Kickoff crew" width="601" height="157" data-path="images/enterprise/kickoff-slack-crew.png" />
          </Frame>
    * Press Enter or select the "**Kickoff crew**" option. A dialog box titled "**Kickoff an AI Crew**" will appear.
  </Step>

  <Step title="Select the crew you want to start">
    * In the dropdown menu labeled "**Select of the crews online:**", choose the crew you want to start.
    * In the example below, "**prep-for-meeting**" is selected:
          <Frame>
            <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/kickoff-slack-crew-dropdown.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=7c92f688fcd7f1f0251cd90670014e34" alt="Kickoff crew dropdown" width="631" height="333" data-path="images/enterprise/kickoff-slack-crew-dropdown.png" />
          </Frame>
    * If your crew requires any inputs, click the "**Add Inputs**" button to provide them.
          <Note>
            The "**Add Inputs**" button is shown in the example above but is not yet clicked.
          </Note>
  </Step>

  <Step title="Click Kickoff and wait for the crew to complete">
    * Once you've selected the crew and added any necessary inputs, click "**Kickoff**" to start the crew.
          <Frame>
            <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/kickoff-slack-crew-kickoff.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e5bebbf61fb92832dc1ebef0a77d5654" alt="Kickoff crew" width="628" height="771" data-path="images/enterprise/kickoff-slack-crew-kickoff.png" />
          </Frame>
    * The crew will start executing and you will see the results in the Slack channel.
          <Frame>
            <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/kickoff-slack-crew-results.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=a3d451c03c3ff7ebf64eb9bb1b41c18c" alt="Kickoff crew results" width="653" height="678" data-path="images/enterprise/kickoff-slack-crew-results.png" />
          </Frame>
  </Step>
</Steps>

## Tips

* Make sure you have the necessary permissions to use the `/kickoff` command in your Slack workspace.
* If you don't see your desired crew in the dropdown, ensure it's properly configured and online in CrewAI.