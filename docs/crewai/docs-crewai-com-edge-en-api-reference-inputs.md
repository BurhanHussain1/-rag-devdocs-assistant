---
url: https://docs.crewai.com/edge/en/api-reference/inputs
title: GET /inputs
framework: crewai
---

# GET /inputs

> Get required inputs for your crew

## OpenAPI

````yaml enterprise-api.en.yaml GET /inputs
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
  /inputs:
    get:
      summary: Get Required Inputs
      description: >
        **📋 Reference Example Only** - *This shows the request format. To test
        with your actual crew, copy the cURL example and replace the URL + token
        with your real values.*

        Retrieves the list of all required input parameters that your crew
        expects for execution.

        Use this endpoint to discover what inputs you need to provide when
        starting a crew execution.
      operationId: getRequiredInputs
      responses:
        '200':
          description: Successfully retrieved required inputs
          content:
            application/json:
              schema:
                type: object
                properties:
                  inputs:
                    type: array
                    items:
                      type: string
                    description: Array of required input parameter names
                    example:
                      - budget
                      - interests
                      - duration
                      - age
              examples:
                travel_crew:
                  summary: Travel planning crew inputs
                  value:
                    inputs:
                      - budget
                      - interests
                      - duration
                      - age
                outreach_crew:
                  summary: Outreach crew inputs
                  value:
                    inputs:
                      - name
                      - title
                      - company
                      - industry
                      - our_product
                      - linkedin_url
        '401':
          $ref: '#/components/responses/UnauthorizedError'
        '404':
          $ref: '#/components/responses/NotFoundError'
        '500':
          $ref: '#/components/responses/ServerError'
components:
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
    NotFoundError:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: Not Found
            message: The requested resource was not found
    ServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: Internal Server Error
            message: An unexpected error occurred
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