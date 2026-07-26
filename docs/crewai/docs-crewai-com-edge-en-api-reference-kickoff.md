---
url: https://docs.crewai.com/edge/en/api-reference/kickoff
title: POST /kickoff
framework: crewai
---

# POST /kickoff

> Start a crew execution

## OpenAPI

````yaml enterprise-api.en.yaml POST /kickoff
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
  /kickoff:
    post:
      summary: Start Crew Execution
      description: >
        **📋 Reference Example Only** - *This shows the request format. To test
        with your actual crew, copy the cURL example and replace the URL + token
        with your real values.*

        Initiates a new crew execution with the provided inputs. Returns a
        kickoff ID that can be used

        to track the execution progress and retrieve results.

        Crew executions can take anywhere from seconds to minutes depending on
        their complexity.

        Consider using webhooks for real-time notifications or implement polling
        with the status endpoint.
      operationId: startCrewExecution
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - inputs
              properties:
                inputs:
                  type: object
                  description: Key-value pairs of all required inputs for your crew
                  additionalProperties:
                    type: string
                  example:
                    budget: 1000 USD
                    interests: games, tech, ai, relaxing hikes, amazing food
                    duration: 7 days
                    age: '35'
                meta:
                  type: object
                  description: Additional metadata to pass to the crew
                  additionalProperties: true
                  example:
                    requestId: user-request-12345
                    source: mobile-app
                taskWebhookUrl:
                  type: string
                  format: uri
                  description: Callback URL executed after each task completion
                  example: https://your-server.com/webhooks/task
                stepWebhookUrl:
                  type: string
                  format: uri
                  description: Callback URL executed after each agent thought/action
                  example: https://your-server.com/webhooks/step
                crewWebhookUrl:
                  type: string
                  format: uri
                  description: Callback URL executed when the crew execution completes
                  example: https://your-server.com/webhooks/crew
            examples:
              travel_planning:
                summary: Travel planning crew
                value:
                  inputs:
                    budget: 1000 USD
                    interests: games, tech, ai, relaxing hikes, amazing food
                    duration: 7 days
                    age: '35'
                  meta:
                    requestId: travel-req-123
                    source: web-app
              outreach_campaign:
                summary: Outreach crew with webhooks
                value:
                  inputs:
                    name: John Smith
                    title: CTO
                    company: TechCorp
                    industry: Software
                    our_product: AI Development Platform
                    linkedin_url: https://linkedin.com/in/johnsmith
                  taskWebhookUrl: https://api.example.com/webhooks/task
                  crewWebhookUrl: https://api.example.com/webhooks/crew
      responses:
        '200':
          description: Crew execution started successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  kickoff_id:
                    type: string
                    format: uuid
                    description: Unique identifier for tracking this execution
                    example: abcd1234-5678-90ef-ghij-klmnopqrstuv
        '400':
          description: Invalid request body or missing required inputs
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '422':
          description: Validation error - ensure all required inputs are provided
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ValidationError'
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
    ValidationError:
      type: object
      properties:
        error:
          type: string
          example: Validation Error
        message:
          type: string
          example: Missing required inputs
        details:
          type: object
          properties:
            missing_inputs:
              type: array
              items:
                type: string
              example:
                - budget
                - interests
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