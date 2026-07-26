---
url: https://docs.crewai.com/edge/en/enterprise/features/traces
title: Traces
framework: crewai
---

# Traces

> Using Traces to monitor your Crews

## Overview

Traces provide comprehensive visibility into your crew executions, helping you monitor performance, debug issues, and optimize your AI agent workflows.

## What are Traces?

Traces in CrewAI AMP are detailed execution records that capture every aspect of your crew's operation, from initial inputs to final outputs. They record:

* Agent thoughts and reasoning
* Task execution details
* Tool usage and outputs
* Token consumption metrics
* Execution times
* Cost estimates

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/traces-overview.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=9c02d5b7306bf7adaeadd77a018f8fea" alt="Traces Overview" width="2244" height="1422" data-path="images/enterprise/traces-overview.png" />
</Frame>

## Accessing Traces

<Steps>
  <Step title="Navigate to the Traces Tab">
    Once in your CrewAI AMP dashboard, click on the **Traces** to view all execution records.
  </Step>

  <Step title="Select an Execution">
    You'll see a list of all crew executions, sorted by date. Click on any execution to view its detailed trace.
  </Step>
</Steps>

## Understanding the Trace Interface

The trace interface is divided into several sections, each providing different insights into your crew's execution:

### 1. Execution Summary

The top section displays high-level metrics about the execution:

* **Total Tokens**: Number of tokens consumed across all tasks
* **Prompt Tokens**: Tokens used in prompts to the LLM
* **Completion Tokens**: Tokens generated in LLM responses
* **Requests**: Number of API calls made
* **Execution Time**: Total duration of the crew run
* **Estimated Cost**: Approximate cost based on token usage

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/trace-summary.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=a6a26eda2add26a6f649b1727bf90d8d" alt="Execution Summary" width="2576" height="916" data-path="images/enterprise/trace-summary.png" />
</Frame>

### 2. Tasks & Agents

This section shows all tasks and agents that were part of the crew execution:

* Task name and agent assignment
* Agents and LLMs used for each task
* Status (completed/failed)
* Individual execution time of the task

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/trace-tasks.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=f0358b4a17e78532500b4a14964bc30c" alt="Task List" width="1778" height="594" data-path="images/enterprise/trace-tasks.png" />
</Frame>

### 3. Final Output

Displays the final result produced by the crew after all tasks are completed.

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/final-output.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=5ca9ef8e4071ee570c3e0c8f93ff4253" alt="Final Output" width="2212" height="1572" data-path="images/enterprise/final-output.png" />
</Frame>

### 4. Execution Timeline

A visual representation of when each task started and ended, helping you identify bottlenecks or parallel execution patterns.

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/trace-timeline.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=c860975d3e15e3a6988bedc7d1bf6ba4" alt="Execution Timeline" width="2210" height="1406" data-path="images/enterprise/trace-timeline.png" />
</Frame>

### 5. Detailed Task View

When you click on a specific task in the timeline or task list, you'll see:

<Frame>
  <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/trace-detailed-task.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=74f5e92354196325edca8d62c29363c7" alt="Detailed Task View" width="2036" height="1572" data-path="images/enterprise/trace-detailed-task.png" />
</Frame>

* **Task Key**: Unique identifier for the task
* **Task ID**: Technical identifier in the system
* **Status**: Current state (completed/running/failed)
* **Agent**: Which agent performed the task
* **LLM**: Language model used for this task
* **Start/End Time**: When the task began and completed
* **Execution Time**: Duration of this specific task
* **Task Description**: What the agent was instructed to do
* **Expected Output**: What output format was requested
* **Input**: Any input provided to this task from previous tasks
* **Output**: The actual result produced by the agent

## Using Traces for Debugging

Traces are invaluable for troubleshooting issues with your crews:

<Steps>
  <Step title="Identify Failure Points">
    When a crew execution doesn't produce the expected results, examine the trace to find where things went wrong. Look for:

    * Failed tasks
    * Unexpected agent decisions
    * Tool usage errors
    * Misinterpreted instructions

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/failure.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=c892a75b7a22a57949a2641a0fe45bfa" alt="Failure Points" width="820" height="924" data-path="images/enterprise/failure.png" />
    </Frame>
  </Step>

  <Step title="Optimize Performance">
    Use execution metrics to identify performance bottlenecks:

    * Tasks that took longer than expected
    * Excessive token usage
    * Redundant tool operations
    * Unnecessary API calls
  </Step>

  <Step title="Improve Cost Efficiency">
    Analyze token usage and cost estimates to optimize your crew's efficiency:

    * Consider using smaller models for simpler tasks
    * Refine prompts to be more concise
    * Cache frequently accessed information
    * Structure tasks to minimize redundant operations
  </Step>
</Steps>

## Performance and batching

CrewAI batches trace uploads to reduce overhead on high-volume runs:

* A TraceBatchManager buffers events and sends them in batches via the Plus API client
* Reduces network chatter and improves reliability on flaky connections
* Automatically enabled in the default trace listener; no configuration needed

This yields more stable tracing under load while preserving detailed task/agent telemetry.

<Card title="Need Help?" icon="headset" href="mailto:support@crewai.com">
  Contact our support team for assistance with trace analysis or any other
  CrewAI AMP features.
</Card>