---
url: https://docs.crewai.com/edge/en/enterprise/guides/hubspot-trigger
title: HubSpot Trigger
framework: crewai
---

# HubSpot Trigger

> Trigger CrewAI crews directly from HubSpot Workflows

This guide provides a step-by-step process to set up HubSpot triggers for CrewAI AMP, enabling you to initiate crews directly from HubSpot Workflows.

## Prerequisites

* A CrewAI AMP account
* A HubSpot account with the [HubSpot Workflows](https://knowledge.hubspot.com/workflows/create-workflows) feature

## Setup Steps

<Steps>
  <Step title="Connect your HubSpot account with CrewAI AMP">
    * Log in to your `CrewAI AMP account > Triggers` - Select `HubSpot` from the
      list of available triggers - Choose the HubSpot account you want to connect
      with CrewAI AMP - Follow the on-screen prompts to authorize CrewAI AMP
      access to your HubSpot account - A confirmation message will appear once
      HubSpot is successfully connected with CrewAI AMP
  </Step>

  <Step title="Create a HubSpot Workflow">
    * Log in to your `HubSpot account > Automations > Workflows > New workflow`
    * Select the workflow type that fits your needs (e.g., Start from scratch) -
      In the workflow builder, click the Plus (+) icon to add a new action. -
      Choose `Integrated apps > CrewAI > Kickoff a Crew`. - Select the Crew you
      want to initiate. - Click `Save` to add the action to your workflow

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/hubspot-workflow-1.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=d53acad518d2e330bd4a69ca76808b11" alt="HubSpot Workflow 1" width="670" height="556" data-path="images/enterprise/hubspot-workflow-1.png" />
    </Frame>
  </Step>

  <Step title="Use Crew results with other actions">
    * After the Kickoff a Crew step, click the Plus (+) icon to add a new
      action. - For example, to send an internal email notification, choose
      `Communications > Send internal email notification` - In the Body field,
      click `Insert data`, select `View properties or action outputs from > Action
          outputs > Crew Result` to include Crew data in the email

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/hubspot-workflow-2.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=a096e4d667b63a65b1061bdc5f659199" alt="HubSpot Workflow 2" width="670" height="437" data-path="images/enterprise/hubspot-workflow-2.png" />
    </Frame>

    * Configure any additional actions as needed - Review your workflow
      steps to ensure everything is set up correctly - Activate the workflow
          <Frame>
            <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/hubspot-workflow-3.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=b8e6f426200408867d0a09526a93f32f" alt="HubSpot Workflow 3" width="670" height="647" data-path="images/enterprise/hubspot-workflow-3.png" />
          </Frame>
  </Step>
</Steps>

For more detailed information on available actions and customization options, refer to the [HubSpot Workflows Documentation](https://knowledge.hubspot.com/workflows/create-workflows).