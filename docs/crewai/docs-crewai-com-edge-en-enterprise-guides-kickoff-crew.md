---
url: https://docs.crewai.com/edge/en/enterprise/guides/kickoff-crew
title: Kickoff Crew
framework: crewai
---

# Kickoff Crew

> Kickoff a Crew on CrewAI AMP

## Overview

Once you've deployed your crew to the CrewAI AMP platform, you can kickoff executions through the web interface or the API. This guide covers both approaches.

## Method 1: Using the Web Interface

### Step 1: Navigate to Your Deployed Crew

1. Log in to [CrewAI AMP](https://app.crewai.com)
2. Click on the crew name from your projects list
3. You'll be taken to the crew's detail page

<Frame>
  <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/crew-dashboard.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=6dfd552914d3ed5ec24abb1ba606ff7d" alt="Crew Dashboard" width="1492" height="872" data-path="images/enterprise/crew-dashboard.png" />
</Frame>

### Step 2: Initiate Execution

From your crew's detail page, you have two options to kickoff an execution:

#### Option A: Quick Kickoff

1. Click the `Kickoff` link in the Test Endpoints section
2. Enter the required input parameters for your crew in the JSON editor
3. Click the `Send Request` button

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/kickoff-endpoint.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=39603fac859ca2a602c51c585c2a4861" alt="Kickoff Endpoint" width="2794" height="1390" data-path="images/enterprise/kickoff-endpoint.png" />
</Frame>

#### Option B: Using the Visual Interface

1. Click the `Run` tab in the crew detail page
2. Enter the required inputs in the form fields
3. Click the `Run Crew` button

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/run-crew.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=87b09919c9210c7ca8fb0b0952d99005" alt="Run Crew" width="2808" height="1764" data-path="images/enterprise/run-crew.png" />
</Frame>

### Step 3: Monitor Execution Progress

After initiating the execution:

1. You'll receive a response containing a `kickoff_id` - **copy this ID**
2. This ID is essential for tracking your execution

<Frame>
  <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/copy-task-id.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=f5d6e458d4773fb94590d7accdde8499" alt="Copy Task ID" width="2790" height="1040" data-path="images/enterprise/copy-task-id.png" />
</Frame>

### Step 4: Check Execution Status

To monitor the progress of your execution:

1. Click the "Status" endpoint in the Test Endpoints section
2. Paste the `kickoff_id` into the designated field
3. Click the "Get Status" button

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/get-status.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=f8c8f553fd5797fab5fbec2993f5d745" alt="Get Status" width="2774" height="452" data-path="images/enterprise/get-status.png" />
</Frame>

The status response will show:

* Current execution state (`running`, `completed`, etc.)
* Details about which tasks are in progress
* Any outputs produced so far

### Step 5: View Final Results

Once execution is complete:

1. The status will change to `completed`
2. You can view the full execution results and outputs
3. For a more detailed view, check the `Executions` tab in the crew detail page

## Method 2: Using the API

You can also kickoff crews programmatically using the CrewAI AMP REST API.

### Authentication

All API requests require a bearer token for authentication:

```bash
curl -H "Authorization: Bearer YOUR_CREW_TOKEN" https://your-crew-url.crewai.com
```

Your bearer token is available on the Status tab of your crew's detail page.

### Checking Crew Health

Before executing operations, you can verify that your crew is running properly:

```bash
curl -H "Authorization: Bearer YOUR_CREW_TOKEN" https://your-crew-url.crewai.com
```

A successful response will return a message indicating the crew is operational:

```
Healthy%
```

### Step 1: Retrieve Required Inputs

First, determine what inputs your crew requires:

```bash
curl -X GET \
  -H "Authorization: Bearer YOUR_CREW_TOKEN" \
  https://your-crew-url.crewai.com/inputs
```

The response will be a JSON object containing an array of required input parameters, for example:

```json
{ "inputs": ["topic", "current_year"] }
```

This example shows that this particular crew requires two inputs: `topic` and `current_year`.

### Step 2: Kickoff Execution

Initiate execution by providing the required inputs:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_CREW_TOKEN" \
  -d '{"inputs": {"topic": "AI Agent Frameworks", "current_year": "2025"}}' \
  https://your-crew-url.crewai.com/kickoff
```

The response will include a `kickoff_id` that you'll need for tracking:

```json
{ "kickoff_id": "abcd1234-5678-90ef-ghij-klmnopqrstuv" }
```

### Step 3: Check Execution Status

Monitor the execution progress using the kickoff\_id:

```bash
curl -X GET \
  -H "Authorization: Bearer YOUR_CREW_TOKEN" \
  https://your-crew-url.crewai.com/status/abcd1234-5678-90ef-ghij-klmnopqrstuv
```

## Handling Executions

### Long-Running Executions

For executions that may take a long time:

1. Consider implementing a polling mechanism to check status periodically
2. Use webhooks (if available) for notification when execution completes
3. Implement error handling for potential timeouts

### Execution Context

The execution context includes:

* Inputs provided at kickoff
* Environment variables configured during deployment
* Any state maintained between tasks

### Debugging Failed Executions

If an execution fails:

1. Check the "Executions" tab for detailed logs
2. Review the "Traces" tab for step-by-step execution details
3. Look for LLM responses and tool usage in the trace details

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with execution issues or questions
  about the Enterprise platform.
</Card>