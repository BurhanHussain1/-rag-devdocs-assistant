---
url: https://docs.crewai.com/edge/en/api-reference/status
title: GET /status/{kickoff_id}
framework: crewai
---

# GET /status/{kickoff_id}

> Get execution status

## OpenAPI

````yaml enterprise-api.en.yaml GET /status/{kickoff_id}
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
  /status/{kickoff_id}:
    get:
      summary: Get Execution Status
      description: >
        **📋 Reference Example Only** - *This shows the request format. To test
        with your actual crew, copy the cURL example and replace the URL + token
        with your real values.*

        Retrieves the current status and results of a crew execution using its
        kickoff ID.

        The response structure varies depending on the execution state:

        - **running**: Execution in progress with current task info

        - **completed**: Execution finished with full results

        - **error**: Execution failed with error details
      operationId: getExecutionStatus
      parameters:
        - name: kickoff_id
          in: path
          required: true
          description: The kickoff ID returned from the /kickoff endpoint
          schema:
            type: string
            format: uuid
            example: abcd1234-5678-90ef-ghij-klmnopqrstuv
      responses:
        '200':
          description: Successfully retrieved execution status
          content:
            application/json:
              schema:
                oneOf:
                  - $ref: '#/components/schemas/ExecutionRunning'
                  - $ref: '#/components/schemas/ExecutionCompleted'
                  - $ref: '#/components/schemas/ExecutionError'
              examples:
                running:
                  summary: Execution in progress
                  value:
                    status: running
                    current_task: research_task
                    progress:
                      completed_tasks: 1
                      total_tasks: 3
                completed:
                  summary: Execution completed successfully
                  value:
                    status: completed
                    result:
                      output: >-
                        Comprehensive travel itinerary for 7 days in Japan
                        focusing on tech culture...
                      tasks:
                        - task_id: research_task
                          output: Research findings on tech destinations in Japan...
                          agent: Travel Researcher
                          execution_time: 45.2
                        - task_id: planning_task
                          output: >-
                            7-day detailed itinerary with activities and
                            recommendations...
                          agent: Trip Planner
                          execution_time: 62.8
                    execution_time: 108.5
                error:
                  summary: Execution failed
                  value:
                    status: error
                    error: >-
                      Task execution failed: Invalid API key for external
                      service
                    execution_time: 23.1
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '404':
          description: Kickoff ID not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: Execution not found
                message: >-
                  No execution found with ID:
                  abcd1234-5678-90ef-ghij-klmnopqrstuv
        '500':
          $ref: '#/components/responses/ServerError'
components:
  schemas:
    ExecutionRunning:
      type: object
      properties:
        status:
          type: string
          enum:
            - running
          example: running
        current_task:
          type: string
          description: Name of the currently executing task
          example: research_task
        progress:
          type: object
          properties:
            completed_tasks:
              type: integer
              description: Number of completed tasks
              example: 1
            total_tasks:
              type: integer
              description: Total number of tasks in the crew
              example: 3
    ExecutionCompleted:
      type: object
      properties:
        status:
          type: string
          enum:
            - completed
          example: completed
        result:
          type: object
          properties:
            output:
              type: string
              description: Final output from the crew execution
              example: Comprehensive travel itinerary...
            tasks:
              type: array
              items:
                $ref: '#/components/schemas/TaskResult'
        execution_time:
          type: number
          description: Total execution time in seconds
          example: 108.5
    ExecutionError:
      type: object
      properties:
        status:
          type: string
          enum:
            - error
          example: error
        error:
          type: string
          description: Error message describing what went wrong
          example: 'Task execution failed: Invalid API key'
        execution_time:
          type: number
          description: Time until error occurred in seconds
          example: 23.1
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
    TaskResult:
      type: object
      properties:
        task_id:
          type: string
          description: Unique identifier for the task
          example: research_task
        output:
          type: string
          description: Output generated by this task
          example: Research findings...
        agent:
          type: string
          description: Name of the agent that executed this task
          example: Travel Researcher
        execution_time:
          type: number
          description: Time taken to execute this task in seconds
          example: 45.2
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