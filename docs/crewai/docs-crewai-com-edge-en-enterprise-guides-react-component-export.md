---
url: https://docs.crewai.com/edge/en/enterprise/guides/react-component-export
title: React Component Export
framework: crewai
---

# React Component Export

> Learn how to export and integrate CrewAI AMP React components into your applications

This guide explains how to export CrewAI AMP crews as React components and integrate them into your own applications.

## Exporting a React Component

<Steps>
  <Step title="Export the Component">
    Click on the ellipsis (three dots on the right of your deployed crew) and select the export option and save the file locally. We will be using `CrewLead.jsx` for our example.

    <Frame>
      <img src="https://mintcdn.com/crewai/Tp3HEbbp9mp-dy3H/images/enterprise/export-react-component.png?fit=max&auto=format&n=Tp3HEbbp9mp-dy3H&q=85&s=e0c72184b57eeae414674023197fca1b" alt="Export React Component" width="493" height="359" data-path="images/enterprise/export-react-component.png" />
    </Frame>
  </Step>
</Steps>

## Setting Up Your React Environment

To run this React component locally, you'll need to set up a React development environment and integrate this component into a React project.

<Steps>
  <Step title="Install Node.js">
    * Download and install Node.js from the official website: [https://nodejs.org/](https://nodejs.org/)
    * Choose the LTS (Long Term Support) version for stability.
  </Step>

  <Step title="Create a new React project">
    * Open Command Prompt or PowerShell
    * Navigate to the directory where you want to create your project
    * Run the following command to create a new React project:

      ```bash
      npx create-react-app my-crew-app
      ```
    * Change into the project directory:

      ```bash
      cd my-crew-app
      ```
  </Step>

  <Step title="Install necessary dependencies">
    ```bash
    npm install react-dom
    ```
  </Step>

  <Step title="Create the CrewLead component">
    * Move the downloaded file `CrewLead.jsx` into the `src` folder of your project,
  </Step>

  <Step title="Modify your App.js to use the CrewLead component">
    * Open `src/App.js`
    * Replace its contents with something like this:

    ```jsx
    import React from 'react';
    import CrewLead from './CrewLead';

    function App() {
        return (
            <div className="App">
                <CrewLead baseUrl="YOUR_API_BASE_URL" bearerToken="YOUR_BEARER_TOKEN" />
            </div>
        );
    }

    export default App;
    ```

    * Replace `YOUR_API_BASE_URL` and `YOUR_BEARER_TOKEN` with the actual values for your API.
  </Step>

  <Step title="Start the development server">
    * In your project directory, run:

      ```bash
      npm start
      ```
    * This will start the development server, and your default web browser should open automatically to [http://localhost:3000](http://localhost:3000), where you'll see your React app running.
  </Step>
</Steps>

## Customization

You can then customise the `CrewLead.jsx` to add color, title etc

<Frame>
  <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/customise-react-component.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=4673fd3ac9eedc1c83b777afb8cf09c9" alt="Customise React Component" width="1119" height="939" data-path="images/enterprise/customise-react-component.png" />
</Frame>

<Frame>
  <img src="https://mintcdn.com/crewai/5SZbe87tsCWZY09V/images/enterprise/customise-react-component-2.png?fit=max&auto=format&n=5SZbe87tsCWZY09V&q=85&s=714c15d129b3db4bd96cdc55e80916dd" alt="Customise React Component" width="1058" height="427" data-path="images/enterprise/customise-react-component-2.png" />
</Frame>

## Next Steps

* Customize the component styling to match your application's design
* Add additional props for configuration
* Integrate with your application's state management
* Add error handling and loading states