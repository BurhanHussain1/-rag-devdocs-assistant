---
url: https://docs.crewai.com/edge/en/enterprise/guides/webhook-automation
title: Webhook Automation
framework: crewai
---

# Webhook Automation

> Automate CrewAI AMP workflows using webhooks with platforms like ActivePieces, Zapier, and Make.com

CrewAI AMP allows you to automate your workflow using webhooks. This article will guide you through the process of setting up and using webhooks to kickoff your crew execution, with a focus on integration with ActivePieces, a workflow automation platform similar to Zapier and Make.com.

## Setting Up Webhooks

<Steps>
  <Step title="Accessing the Kickoff Interface">
    * Navigate to the CrewAI AMP dashboard
    * Look for the `/kickoff` section, which is used to start the crew execution
          <Frame>
            <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/kickoff-interface.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=4e6a4b1f098388c7f76e91c25ed4b077" alt="Kickoff Interface" width="670" height="358" data-path="images/enterprise/kickoff-interface.png" />
          </Frame>
  </Step>

  <Step title="Configuring the JSON Content">
    In the JSON Content section, you'll need to provide the following information:

    * **inputs**: A JSON object containing:
      * `company`: The name of the company (e.g., "tesla")
      * `product_name`: The name of the product (e.g., "crewai")
      * `form_response`: The type of response (e.g., "financial")
      * `icp_description`: A brief description of the Ideal Customer Profile
      * `product_description`: A short description of the product
      * `taskWebhookUrl`, `stepWebhookUrl`, `crewWebhookUrl`: URLs for various webhook endpoints (ActivePieces, Zapier, Make.com or another compatible platform)
  </Step>

  <Step title="Integrating with ActivePieces">
    In this example we will be using ActivePieces. You can use other platforms such as Zapier and Make.com

    To integrate with ActivePieces:

    1. Set up a new flow in ActivePieces

    2. Add a trigger (e.g., `Every Day` schedule)
           <Frame>
             <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/activepieces-trigger.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=1a52fc1bb47bef6228955360d00f190f" alt="ActivePieces Trigger" width="595" height="773" data-path="images/enterprise/activepieces-trigger.png" />
           </Frame>

    3. Add an HTTP action step
       * Set the action to `Send HTTP request`

       * Use `POST` as the method

       * Set the URL to your CrewAI AMP kickoff endpoint

       * Add necessary headers (e.g., `Bearer Token`)
             <Frame>
               <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/activepieces-headers.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=602a5ed1aa2b462b0a81a122a5e2d35f" alt="ActivePieces Headers" width="449" height="572" data-path="images/enterprise/activepieces-headers.png" />
             </Frame>

       * In the body, include the JSON content as configured in step 2
             <Frame>
               <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/activepieces-body.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=f238e1630f7be667cce2d208315ddc75" alt="ActivePieces Body" width="670" height="401" data-path="images/enterprise/activepieces-body.png" />
             </Frame>

       * The crew will then kickoff at the pre-defined time.
  </Step>

  <Step title="Setting Up the Webhook">
    1. Create a new flow in ActivePieces and name it
           <Frame>
             <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/activepieces-flow.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=c23af88ea2df7919f680706318eb1506" alt="ActivePieces Flow" width="544" height="683" data-path="images/enterprise/activepieces-flow.png" />
           </Frame>

    2. Add a webhook step as the trigger:
       * Select `Catch Webhook` as the trigger type

       * This will generate a unique URL that will receive HTTP requests and trigger your flow
             <Frame>
               <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/activepieces-webhook.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=8236fd9a97149eff4fd86f1c9a9b0f1a" alt="ActivePieces Webhook" width="451" height="488" data-path="images/enterprise/activepieces-webhook.png" />
             </Frame>

       * Configure the email to use crew webhook body text
             <Frame>
               <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/activepieces-email.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=484c8d88ed96322d21894e9663f5fc4a" alt="ActivePieces Email" width="461" height="518" data-path="images/enterprise/activepieces-email.png" />
             </Frame>
  </Step>
</Steps>

## Webhook Output Examples

**Note:** Any `meta` object provided in your kickoff request will be included in all webhook payloads, allowing you to track requests and maintain context across the entire crew execution lifecycle.

<Tabs>
  <Tab title="Step Webhook">
    `stepWebhookUrl` - Callback that will be executed upon each agent inner thought

    ```json
    {
        "prompt": "Research the financial industry for potential AI solutions",
        "thought": "I need to conduct preliminary research on the financial industry",
        "tool": "research_tool",
        "tool_input": "financial industry AI solutions",
        "result": "**Preliminary Research Report on the Financial Industry for crewai Enterprise Solution**\n1. Industry Overview and Trends\nThe financial industry in ....\nConclusion:\nThe financial industry presents a fertile ground for implementing AI solutions like crewai, particularly in areas such as digital customer engagement, risk management, and regulatory compliance. Further engagement with the lead is recommended to better tailor the crewai solution to their specific needs and scale.",
        "kickoff_id": "97eba64f-958c-40a0-b61c-625fe635a3c0",
        "meta": {
            "requestId": "travel-req-123",
            "source": "web-app"
        }
    }
    ```
  </Tab>

  <Tab title="Task Webhook">
    `taskWebhookUrl` - Callback that will be executed upon the end of each task

    ```json
    {
        "description": "Using the information gathered from the lead's data, conduct preliminary research on the lead's industry, company background, and potential use cases for crewai. Focus on finding relevant data that can aid in scoring the lead and planning a strategy to pitch them crewai.",
        "name": "Industry Research Task",
        "expected_output": "Detailed research report on the financial industry",
        "summary": "The financial industry presents a fertile ground for implementing AI solutions like crewai, particularly in areas such as digital customer engagement, risk management, and regulatory compliance. Further engagement with the lead is recommended to better tailor the crewai solution to their specific needs and scale.",
        "agent": "Research Agent",
        "output": "**Preliminary Research Report on the Financial Industry for crewai Enterprise Solution**\n1. Industry Overview and Trends\nThe financial industry in ....\nConclusion:\nThe financial industry presents a fertile ground for implementing AI solutions like crewai, particularly in areas such as digital customer engagement, risk management, and regulatory compliance.",
        "output_json": {
            "industry": "financial",
            "key_opportunities": ["digital customer engagement", "risk management", "regulatory compliance"]
        },
        "kickoff_id": "97eba64f-958c-40a0-b61c-625fe635a3c0",
        "meta": {
            "requestId": "travel-req-123",
            "source": "web-app"
        }
    }
    ```
  </Tab>

  <Tab title="Crew Webhook">
    `crewWebhookUrl` - Callback that will be executed upon the end of the crew execution

    ```json
    {
        "kickoff_id": "97eba64f-958c-40a0-b61c-625fe635a3c0",
        "result": "**Final Analysis Report**\n\nLead Score: Customer service enhancement and compliance are particularly relevant.\n\nTalking Points:\n- Highlight how crewai's AI solutions can transform customer service\n- Discuss crewai's potential for sustainability goals\n- Emphasize compliance capabilities\n- Stress adaptability for various operation scales",
        "result_json": {
            "lead_score": "Customer service enhancement, and compliance are particularly relevant.",
            "talking_points": [
                "Highlight how crewai's AI solutions can transform customer service with automated, personalized experiences and 24/7 support, improving both customer satisfaction and operational efficiency.",
                "Discuss crewai's potential to help the institution achieve its sustainability goals through better data analysis and decision-making, contributing to responsible investing and green initiatives.",
                "Emphasize crewai's ability to enhance compliance with evolving regulations through efficient data processing and reporting, reducing the risk of non-compliance penalties.",
                "Stress the adaptability of crewai to support both extensive multinational operations and smaller, targeted projects, ensuring the solution grows with the institution's needs."
            ]
        },
        "token_usage": {
            "total_tokens": 1250,
            "prompt_tokens": 800,
            "completion_tokens": 450
        },
        "meta": {
            "requestId": "travel-req-123",
            "source": "web-app"
        }
    }
    ```
  </Tab>
</Tabs>