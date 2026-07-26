---
url: https://docs.crewai.com/edge/en/enterprise/guides/zapier-trigger
title: Zapier Trigger
framework: crewai
---

# Zapier Trigger

> Trigger CrewAI crews from Zapier workflows to automate cross-app workflows

This guide will walk you through the process of setting up Zapier triggers for CrewAI AMP, allowing you to automate workflows between CrewAI AMP and other applications.

## Prerequisites

* A CrewAI AMP account
* A Zapier account
* A Slack account (for this specific example)

## Step-by-Step Setup

<Steps>
  <Step title="Set Up the Slack Trigger">
    * In Zapier, create a new Zap.

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-1.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=d7602ce90ddcd4f0365fd821f4ff1ff2" alt="Zapier 1" width="621" height="463" data-path="images/enterprise/zapier-1.png" />
    </Frame>
  </Step>

  <Step title="Choose Slack as your trigger app">
    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-2.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e5cdc5705b87b4e06178fa12fb5ef64b" alt="Zapier 2" width="670" height="684" data-path="images/enterprise/zapier-2.png" />
    </Frame>

    * Select `New Pushed Message` as the Trigger Event.
    * Connect your Slack account if you haven't already.
  </Step>

  <Step title="Configure the CrewAI AMP Action">
    * Add a new action step to your Zap.
    * Choose CrewAI+ as your action app and Kickoff as the Action Event

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-3.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e52e2404a73623df30d125873bd8ff42" alt="Zapier 5" width="670" height="670" data-path="images/enterprise/zapier-3.png" />
    </Frame>
  </Step>

  <Step title="Connect your CrewAI AMP account">
    * Connect your CrewAI AMP account.
    * Select the appropriate Crew for your workflow.

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-4.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=13aac37fdb67ee1c9f841a602ac3abf5" alt="Zapier 6" width="670" height="657" data-path="images/enterprise/zapier-4.png" />
    </Frame>

    * Configure the inputs for the Crew using the data from the Slack message.
  </Step>

  <Step title="Format the CrewAI AMP Output">
    * Add another action step to format the text output from CrewAI AMP.
    * Use Zapier's formatting tools to convert the Markdown output to HTML.

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-5.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e772b4803dfffe4de12d9a7ea21484ce" alt="Zapier 8" width="670" height="674" data-path="images/enterprise/zapier-5.png" />
    </Frame>

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-6.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=9fa4a34d5c511b6bb76f276348928699" alt="Zapier 9" width="670" height="675" data-path="images/enterprise/zapier-6.png" />
    </Frame>
  </Step>

  <Step title="Send the Output via Email">
    * Add a final action step to send the formatted output via email.
    * Choose your preferred email service (e.g., Gmail, Outlook).
    * Configure the email details, including recipient, subject, and body.
    * Insert the formatted CrewAI AMP output into the email body.

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-7.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=f3d2a0c67b29888cfdc5b0d81ba5c29b" alt="Zapier 7" width="670" height="673" data-path="images/enterprise/zapier-7.png" />
    </Frame>
  </Step>

  <Step title="Kick Off the crew from Slack">
    * Enter the text in your Slack channel

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-7b.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=916dbdffd171dc52c40ebc74cc39a38f" alt="Zapier 10" width="509" height="85" data-path="images/enterprise/zapier-7b.png" />
    </Frame>

    * Select the 3 ellipsis button and then chose Push to Zapier

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/zapier-8.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=a6a6e2fd0b0b239af4c17ae1f34ad720" alt="Zapier 11" width="405" height="260" data-path="images/enterprise/zapier-8.png" />
    </Frame>
  </Step>

  <Step title="Select the crew and then Push to Kick Off">
    <Frame>
      <img src="https://mintcdn.com/crewai/qVjgZHKAyEOgSSUS/images/enterprise/zapier-9.png?fit=max&auto=format&n=qVjgZHKAyEOgSSUS&q=85&s=eda865381d7121d38025c2b13abeccdf" alt="Zapier 12" width="659" height="531" data-path="images/enterprise/zapier-9.png" />
    </Frame>
  </Step>
</Steps>

## Tips for Success

* Ensure that your CrewAI AMP inputs are correctly mapped from the Slack message.
* Test your Zap thoroughly before turning it on to catch any potential issues.
* Consider adding error handling steps to manage potential failures in the workflow.

By following these steps, you'll have successfully set up Zapier triggers for CrewAI AMP, allowing for automated workflows triggered by Slack messages and resulting in email notifications with CrewAI AMP output.