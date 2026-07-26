---
url: https://docs.crewai.com/edge/en/enterprise/features/tools-and-integrations
title: Tools & Integrations
framework: crewai
---

# Tools & Integrations

> Connect external apps and manage internal tools your agents can use.

## Overview

Tools & Integrations is the central hub for connecting third‑party apps and managing internal tools that your agents can use at runtime.

<Frame>
  <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/crew_connectors.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=c31a4b9031f0f517fdce3baa48471f58" alt="Tools & Integrations Overview" width="1024" height="1024" data-path="images/enterprise/crew_connectors.png" />
</Frame>

## Explore

<Tabs>
  <Tab title="Integrations" icon="plug">
    ## Agent Apps (Integrations)

    Connect enterprise‑grade applications (e.g., Gmail, Google Drive, HubSpot, Slack) via OAuth to enable agent actions.

    {" "}

    <Steps>
      <Step title="Connect">
        Click <b>Connect</b> on an app and complete OAuth.
      </Step>

      <Step title="Configure">
        Optionally adjust scopes, triggers, and action availability.
      </Step>

      <Step title="Use in Agents">
        Connected services become available as tools for your agents.
      </Step>
    </Steps>

    {" "}

    <Frame>
      <img src="https://mintcdn.com/crewai/Grq_Qb7_m8o-TQ5O/images/enterprise/agent-apps.png?fit=max&auto=format&n=Grq_Qb7_m8o-TQ5O&q=85&s=43abfc4eae390e308bed0b8e15238a54" alt="Integrations Grid" width="3648" height="2266" data-path="images/enterprise/agent-apps.png" />
    </Frame>

    ### Connect your Account

    1. Go to <Link href="https://app.crewai.com/crewai_plus/connectors">Integrations</Link>
    2. Click <b>Connect</b> on the desired service
    3. Complete the OAuth flow and grant scopes
    4. Copy your Enterprise Token from <Link href="https://app.crewai.com/crewai_plus/settings/integrations">Integration Settings</Link>

    {" "}

    <Frame>
      <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/enterprise_action_auth_token.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=4e7388bcb76f3f8aa6c6802dd0a98956" alt="Enterprise Token" width="2264" height="540" data-path="images/enterprise/enterprise_action_auth_token.png" />
    </Frame>

    ### Install Integration Tools

    To use the integrations locally, you need to install the latest `crewai-tools` package.

    ```bash
    uv add crewai-tools
    ```

    ### Environment Variable Setup

    {" "}

    <Note>
      To use integrations with `Agent(apps=[])`, you must set the
      `CREWAI_PLATFORM_INTEGRATION_TOKEN` environment variable with your Enterprise
      Token.
    </Note>

    ```bash
    export CREWAI_PLATFORM_INTEGRATION_TOKEN="your_enterprise_token"
    ```

    Or add it to your `.env` file:

    ```
    CREWAI_PLATFORM_INTEGRATION_TOKEN=your_enterprise_token
    ```

    ### Usage Example

    {" "}

    <Tip>
      Use the new streamlined approach to integrate enterprise apps. Simply specify
      the app and its actions directly in the Agent configuration.
    </Tip>

    ```python
    from crewai import Agent, Task, Crew

    # Create an agent with Gmail capabilities
    email_agent = Agent(
        role="Email Manager",
        goal="Manage and organize email communications",
        backstory="An AI assistant specialized in email management and communication.",
        apps=['gmail', 'gmail/send_email']  # Using canonical name 'gmail'
    )

    # Task to send an email
    email_task = Task(
        description="Draft and send a follow-up email to john@example.com about the project update",
        agent=email_agent,
        expected_output="Confirmation that email was sent successfully"
    )

    # Run the task
    crew = Crew(
        agents=[email_agent],
        tasks=[email_task]
    )

    # Run the crew
    crew.kickoff()
    ```

    ### Filtering Tools

    ```python
    from crewai import Agent, Task, Crew

    # Create agent with specific Gmail actions only
    gmail_agent = Agent(
        role="Gmail Manager",
        goal="Manage gmail communications and notifications",
        backstory="An AI assistant that helps coordinate gmail communications.",
        apps=['gmail/fetch_emails']  # Using canonical name with specific action
    )

    notification_task = Task(
        description="Find the email from john@example.com",
        agent=gmail_agent,
        expected_output="Email found from john@example.com"
    )

    crew = Crew(
        agents=[gmail_agent],
        tasks=[notification_task]
    )
    ```

    On a deployed crew, you can specify which actions are available for each integration from the service settings page.

    {" "}

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/filtering_enterprise_action_tools.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=2e689397eabeacd23d0c226ff40566fd" alt="Filter Actions" width="3680" height="2382" data-path="images/enterprise/filtering_enterprise_action_tools.png" />
    </Frame>

    ### Scoped Deployments (multi‑user orgs)

    You can scope each integration to a specific user. For example, a crew that connects to Google can use a specific user’s Gmail account.

    {" "}

    <Tip>Useful when different teams/users must keep data access separated.</Tip>

    Use the `user_bearer_token` to scope authentication to the requesting user. If the user isn’t logged in, the crew won’t use connected integrations. Otherwise it falls back to the default bearer token configured for the deployment.

    {" "}

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/user_bearer_token.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=d62aed15392f304cfc16bfa38ab91a54" alt="User Bearer Token" width="532" height="732" data-path="images/enterprise/user_bearer_token.png" />
    </Frame>

    {" "}

    <div id="catalog" />

    ### Catalog

    #### Communication & Collaboration

    * Gmail — Manage emails and drafts
    * Slack — Workspace notifications and alerts
    * Microsoft — Office 365 and Teams integration

    #### Project Management

    * Jira — Issue tracking and project management
    * ClickUp — Task and productivity management
    * Asana — Team task and project coordination
    * Notion — Page and database management
    * Linear — Software project and bug tracking
    * GitHub — Repository and issue management

    #### Customer Relationship Management

    * Salesforce — CRM account and opportunity management
    * HubSpot — Sales pipeline and contact management
    * Zendesk — Customer support ticket management

    #### Business & Finance

    * Stripe — Payment processing and customer management
    * Shopify — E‑commerce store and product management

    #### Productivity & Storage

    * Google Sheets — Spreadsheet data synchronization
    * Google Calendar — Event and schedule management
    * Box — File storage and document management

    …and more to come!
  </Tab>

  <Tab title="Internal Tools" icon="toolbox">
    ## Internal Tools

    Create custom tools locally, publish them on CrewAI AMP Tool Repository and use them in your agents.

    {" "}

    <Tip>
      Before running the commands below, make sure you log in to your CrewAI AMP
      account by running this command: `bash crewai login `
    </Tip>

    {" "}

    <Frame>
      <img src="https://mintcdn.com/crewai/VGZ5vPOL3DPMThlg/images/enterprise/tools-integrations-internal.png?fit=max&auto=format&n=VGZ5vPOL3DPMThlg&q=85&s=b31a82341fb4dcd784c2ecfc1c3d576c" alt="Internal Tool Detail" width="3648" height="2266" data-path="images/enterprise/tools-integrations-internal.png" />
    </Frame>

    {" "}

    <Steps>
      <Step title="Create">
        Create a new tool locally. `bash crewai tool create your-tool `
      </Step>

      <Step title="Publish">
        Publish the tool to the CrewAI AMP Tool Repository. `bash crewai tool
                    publish `
      </Step>

      <Step title="Install">
        Install the tool from the CrewAI AMP Tool Repository. `bash crewai tool
                    install your-tool `
      </Step>
    </Steps>

    Manage:

    * Name and description
    * Visibility (Private / Public)
    * Required environment variables
    * Version history and downloads
    * Team and role access

    {" "}

    <Frame>
      <img src="https://mintcdn.com/crewai/VGZ5vPOL3DPMThlg/images/enterprise/tool-configs.png?fit=max&auto=format&n=VGZ5vPOL3DPMThlg&q=85&s=1896ebecec784bc15411a0309a0cf973" alt="Internal Tool Detail" width="3648" height="2266" data-path="images/enterprise/tool-configs.png" />
    </Frame>
  </Tab>
</Tabs>

## Related

<CardGroup cols={2}>
  <Card title="Tool Repository" href="/en/enterprise/guides/tool-repository#tool-repository" icon="toolbox">
    Create, publish, and version custom tools for your organization.
  </Card>

  <Card title="Webhook Automation" href="/en/enterprise/guides/webhook-automation" icon="bolt">
    Automate workflows and integrate with external platforms and services.
  </Card>
</CardGroup>