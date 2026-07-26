---
url: https://docs.crewai.com/edge/en/api-reference/resume
title: POST /resume
framework: crewai
---

# POST /resume

> Resume crew execution with human feedback

## OpenAPI

````yaml enterprise-api.en.yaml POST /resume
openapi: 3.0.3
info:
  title: CrewAI AMP API
  description: >
    REST API for interacting with your deployed CrewAI crews on CrewAI AMP.

    ## Getting Started

    1. **Find your crew URL**: Get your unique crew URL from the CrewAI AMP
    dashboard

    2. **Copy examples**: Use the code examples from each endpoint page as
    templates

    3. **Replace placeholders**: Update URLs and tokens with your actual values

    4. **Test with your tools**: Use cURL, Postman, or your preferred API client

    ## Authentication

    All API requests require a bearer token for authentication. There are two
    types of tokens:

    - **Bearer Token**: Organization-level token for full crew operations

    - **User Bearer Token**: User-scoped token for individual access with
    limited permissions

    You can find your bearer tokens in the Status tab of your crew's detail page
    in the CrewAI AMP dashboard.

    ## Reference Documentation

    This documentation provides comprehensive examples for each endpoint:

    - **Request formats** with all required and optional parameters

    - **Response examples** for success and error scenarios

    - **Code samples** in multiple programming languages

    - **Authentication patterns** with proper Bearer token usage

    Copy the examples and customize them with your actual crew URL and
    authentication tokens.

    ## Workflow

    1. **Discover inputs** using `GET /inputs`

    2. **Start execution** using `POST /kickoff`

    3. **Monitor progress** using `GET /status/{kickoff_id}`
  version: 1.0.0
  contact:
    name: CrewAI Support
    email: support@crewai.com
    url: https://crewai.com
servers:
  - url: https://your-actual-crew-name.crewai.com
    description: Replace with your actual deployed crew URL from the CrewAI AMP dashboard
  - url: https://my-travel-crew.crewai.com
    description: Example travel planning crew (replace with your URL)
  - url: https://content-creation-crew.crewai.com
    description: Example content creation crew (replace with your URL)
  - url: https://research-assistant-crew.crewai.com
    description: Example research assistant crew (replace with your URL)
security:
  - BearerAuth: []
paths:
  /resume:
    post:
      summary: Resume Crew Execution with Human Feedback
      description: >
        **📋 Reference Example Only** - *This shows the request format. To test
        with your actual crew, copy the cURL example and replace the URL + token
        with your real values.*

        Resume a paused crew execution with human feedback for Human-in-the-Loop
        (HITL) workflows.

        When a task with `human_input=True` completes, the crew execution pauses
        and waits for human feedback.

        **IMPORTANT**: You must provide the same webhook URLs (`taskWebhookUrl`,
        `stepWebhookUrl`, `crewWebhookUrl`)

        that were used in the original kickoff call. Webhook configurations are
        NOT automatically carried over -

        they must be explicitly provided in the resume request to continue
        receiving notifications.
      operationId: resumeCrewExecution
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - execution_id
                - task_id
                - human_feedback
                - is_approve
              properties:
                execution_id:
                  type: string
                  format: uuid
                  description: The unique identifier for the crew execution (from kickoff)
                  example: abcd1234-5678-90ef-ghij-klmnopqrstuv
                task_id:
                  type: string
                  description: The ID of the task that requires human feedback
                  example: research_task
                human_feedback:
                  type: string
                  description: >-
                    Your feedback on the task output. This will be incorporated
                    as additional context for subsequent task executions.
                  example: >-
                    Great research! Please add more details about recent
                    developments in the field.
                is_approve:
                  type: boolean
                  description: >-
                    Whether you approve the task output: true = positive
                    feedback (continue), false = negative feedback (retry task)
                  example: true
                taskWebhookUrl:
                  type: string
                  format: uri
                  description: >-
                    Callback URL executed after each task completion. MUST be
                    provided to continue receiving task notifications.
                  example: https://your-server.com/webhooks/task
                stepWebhookUrl:
                  type: string
                  format: uri
                  description: >-
                    Callback URL executed after each agent thought/action. MUST
                    be provided to continue receiving step notifications.
                  example: https://your-server.com/webhooks/step
                crewWebhookUrl:
                  type: string
                  format: uri
                  description: >-
                    Callback URL executed when the crew execution completes.
                    MUST be provided to receive completion notification.
                  example: https://your-server.com/webhooks/crew
            examples:
              approve_and_continue:
                summary: Approve task and continue execution
                value:
                  execution_id: abcd1234-5678-90ef-ghij-klmnopqrstuv
                  task_id: research_task
                  human_feedback: Excellent research! Proceed to the next task.
                  is_approve: true
                  taskWebhookUrl: https://api.example.com/webhooks/task
                  stepWebhookUrl: https://api.example.com/webhooks/step
                  crewWebhookUrl: https://api.example.com/webhooks/crew
              request_revision:
                summary: Request task revision with feedback
                value:
                  execution_id: abcd1234-5678-90ef-ghij-klmnopqrstuv
                  task_id: analysis_task
                  human_feedback: Please include more quantitative data and cite your sources.
                  is_approve: false
                  taskWebhookUrl: https://api.example.com/webhooks/task
                  crewWebhookUrl: https://api.example.com/webhooks/crew
      responses:
        '200':
          description: Execution resumed successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    enum:
                      - resumed
                      - retrying
                      - completed
                    description: Status of the resumed execution
                    example: resumed
                  message:
                    type: string
                    description: Human-readable message about the resume operation
                    example: Execution resumed successfully
              examples:
                resumed:
                  summary: Execution resumed with positive feedback
                  value:
                    status: resumed
                    message: Execution resumed successfully
                retrying:
                  summary: Task will be retried with negative feedback
                  value:
                    status: retrying
                    message: Task will be retried with your feedback
        '400':
          description: Invalid request body or execution not in pending state
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: Invalid Request
                message: Execution is not in pending human input state
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '404':
          description: Execution ID or Task ID not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: Not Found
                message: Execution ID not found
        '500':
          $ref: '#/components/responses/ServerError'
components:
  schemas:
    Error:
      type: object
      properties:
        error:
          type: string
          description: Error type or title
          example: Authentication Error
        message:
          type: string
          description: Detailed error message
          example: Invalid bearer token provided
  responses:
    UnauthorizedError:
      description: Authentication failed - check your bearer token
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: Unauthorized
            message: Invalid or missing bearer token
    ServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: Internal Server Error
            message: An unexpected error occurred
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: >
        **📋 Reference Documentation** - *The tokens shown in examples are
        placeholders for reference only.*

        Use your actual Bearer Token or User Bearer Token from the CrewAI AMP
        dashboard for real API calls.

        **Bearer Token**: Organization-level access for full crew operations

        **User Bearer Token**: User-scoped access with limited permissions

````