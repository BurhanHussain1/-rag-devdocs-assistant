---
url: https://docs.crewai.com/edge/en/concepts/cli
title: CLI
framework: crewai
---

# CLI

> Learn how to use the CrewAI CLI to interact with CrewAI.

<Warning>
  Since release 0.140.0, CrewAI AMP started a process of migrating their login
  provider. As such, the authentication flow via CLI was updated. Users that use
  Google to login, or that created their account after July 3rd, 2025 will be
  unable to log in with older versions of the `crewai` library.
</Warning>

## Overview

The CrewAI CLI provides a set of commands to interact with CrewAI, allowing you to create, train, run, and manage crews & flows.

## Installation

To use the CrewAI CLI, make sure you have CrewAI installed:

```shell Terminal theme={null}
pip install crewai
```

## Basic Usage

The basic structure of a CrewAI CLI command is:

```shell Terminal theme={null}
crewai [COMMAND] [OPTIONS] [ARGUMENTS]
```

## Available Commands

### 1. Create

Create a new crew or flow.

```shell Terminal theme={null}
crewai create [OPTIONS] TYPE NAME
```

* `TYPE`: Choose between "crew" or "flow"
* `NAME`: Name of the crew or flow

Example:

```shell Terminal theme={null}
crewai create crew my_new_crew
crewai create flow my_new_flow
```

By default, `crewai create crew` creates a JSON-first crew project with `crew.jsonc` and `agents/*.jsonc`. Use `crewai create crew my_new_crew --classic` only when you want the older Python/YAML scaffold with `crew.py`, `config/agents.yaml`, and `config/tasks.yaml`.

### 2. Version

Show the installed version of CrewAI.

```shell Terminal theme={null}
crewai version [OPTIONS]
```

* `--tools`: (Optional) Show the installed version of CrewAI tools

Example:

```shell Terminal theme={null}
crewai version
crewai version --tools
```

### 3. Train

Train the crew for a specified number of iterations.

```shell Terminal theme={null}
crewai train [OPTIONS]
```

* `-n, --n_iterations INTEGER`: Number of iterations to train the crew (default: 5)
* `-f, --filename TEXT`: Path to a custom file for training (default: "trained\_agents\_data.pkl")

Example:

```shell Terminal theme={null}
crewai train -n 10 -f my_training_data.pkl
```

### 4. Replay

Replay the crew execution from a specific task.

```shell Terminal theme={null}
crewai replay [OPTIONS]
```

* `-t, --task_id TEXT`: Replay the crew from this task ID, including all subsequent tasks

Example:

```shell Terminal theme={null}
crewai replay -t task_123456
```

### 5. Log-tasks-outputs

Retrieve your latest crew\.kickoff() task outputs.

```shell Terminal theme={null}
crewai log-tasks-outputs
```

### 6. Reset-memories

Reset the crew memories (long, short, entity, latest\_crew\_kickoff\_outputs).

```shell Terminal theme={null}
crewai reset-memories [OPTIONS]
```

* `-l, --long`: Reset LONG TERM memory
* `-s, --short`: Reset SHORT TERM memory
* `-e, --entities`: Reset ENTITIES memory
* `-k, --kickoff-outputs`: Reset LATEST KICKOFF TASK OUTPUTS
* `-kn, --knowledge`: Reset KNOWLEDGE storage
* `-akn, --agent-knowledge`: Reset AGENT KNOWLEDGE storage
* `-a, --all`: Reset ALL memories

Example:

```shell Terminal theme={null}
crewai reset-memories --long --short
crewai reset-memories --all
```

### 7. Test

Test the crew and evaluate the results.

```shell Terminal theme={null}
crewai test [OPTIONS]
```

* `-n, --n_iterations INTEGER`: Number of iterations to test the crew (default: 3)
* `-m, --model TEXT`: LLM Model to run the tests on the Crew (default: "gpt-4o-mini")

Example:

```shell Terminal theme={null}
crewai test -n 5 -m gpt-3.5-turbo
```

### 8. Run

Run the crew or flow.

```shell Terminal theme={null}
crewai run
```

<Note>
  Starting from version 0.103.0, the `crewai run` command can be used to run
  both standard crews and flows. For flows, it automatically detects the type
  from pyproject.toml and runs the appropriate command. This is now the
  recommended way to run both crews and flows.
</Note>

<Note>
  Make sure to run these commands from the directory where your CrewAI project
  is set up. Some commands may require additional configuration or setup within
  your project structure.
</Note>

### 9. Chat

Starting in version `0.98.0`, when you run the `crewai chat` command, you start an interactive session with your crew. The AI assistant will guide you by asking for necessary inputs to execute the crew. Once all inputs are provided, the crew will execute its tasks.

After receiving the results, you can continue interacting with the assistant for further instructions or questions.

```shell Terminal theme={null}
crewai chat
```

<Note>
  Ensure you execute these commands from your CrewAI project's root directory.
</Note>

<Note>
  IMPORTANT: Set the `chat_llm` property in your crew definition to enable this command.

  For JSON-first crews, add it to `crew.jsonc`:

  ```jsonc
  {
    "name": "My Crew",
    "agents": ["researcher"],
    "tasks": [],
    "chat_llm": "openai/gpt-4o"
  }
  ```

  For classic Python/YAML crews, set it in `crew.py`:

  ```python
  @crew
  def crew(self) -> Crew:
      return Crew(
          agents=self.agents,
          tasks=self.tasks,
          process=Process.sequential,
          verbose=True,
          chat_llm="gpt-4o",  # LLM for chat orchestration
      )
  ```
</Note>

### 10. Deploy

Deploy the crew or flow to [CrewAI AMP](https://app.crewai.com).

* **Authentication**: You need to be authenticated to deploy to CrewAI AMP.
  You can login or create an account with:

  ```shell Terminal theme={null}
  crewai login
  ```

* **Create a deployment**: Once you are authenticated, you can create a deployment for your crew or flow from the root of your localproject.
  ```shell Terminal theme={null}
  crewai deploy create
  ```
  * Reads your local project configuration.
  * Prompts you to confirm the environment variables (like `OPENAI_API_KEY`, `SERPER_API_KEY`) found locally. These will be securely stored with the deployment on the Enterprise platform. Ensure your sensitive keys are correctly configured locally (e.g., in a `.env` file) before running this.

### 11. Organization Management

Manage your CrewAI AMP organizations.

```shell Terminal theme={null}
crewai org [COMMAND] [OPTIONS]
```

#### Commands:

* `list`: List all organizations you belong to

```shell Terminal theme={null}
crewai org list
```

* `current`: Display your currently active organization

```shell Terminal theme={null}
crewai org current
```

* `switch`: Switch to a specific organization

```shell Terminal theme={null}
crewai org switch <organization_id>
```

<Note>
  You must be authenticated to CrewAI AMP to use these organization management
  commands.
</Note>

* **Create a deployment** (continued):

  * Links the deployment to the corresponding remote GitHub repository (it usually detects this automatically).

* **Deploy the Crew**: Once you are authenticated, you can deploy your crew or flow to CrewAI AMP.

  ```shell Terminal theme={null}
  crewai deploy push
  ```

  * Initiates the deployment process on the CrewAI AMP platform.
  * Upon successful initiation, it will output the Deployment created successfully! message along with the Deployment Name and a unique Deployment ID (UUID).

* **Deployment Status**: You can check the status of your deployment with:

  ```shell Terminal theme={null}
  crewai deploy status
  ```

  This fetches the latest deployment status of your most recent deployment attempt (e.g., `Building Images for Crew`, `Deploy Enqueued`, `Online`).

* **Deployment Logs**: You can check the logs of your deployment with:

  ```shell Terminal theme={null}
  crewai deploy logs
  ```

  This streams the deployment logs to your terminal.

* **List deployments**: You can list all your deployments with:

  ```shell Terminal theme={null}
  crewai deploy list
  ```

  This lists all your deployments.

* **Delete a deployment**: You can delete a deployment with:

  ```shell Terminal theme={null}
  crewai deploy remove
  ```

  This deletes the deployment from the CrewAI AMP platform.

* **Help Command**: You can get help with the CLI with:
  ```shell Terminal theme={null}
  crewai deploy --help
  ```
  This shows the help message for the CrewAI Deploy CLI.

Watch this video tutorial for a step-by-step demonstration of deploying your crew to [CrewAI AMP](http://app.crewai.com) using the CLI.

<iframe className="w-full aspect-video rounded-xl" src="https://www.youtube.com/embed/3EqSV-CYDZA" title="CrewAI Deployment Guide" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen />

### 11. Login

Authenticate with CrewAI AMP using a secure device code flow (no email entry required).

```shell Terminal theme={null}
crewai login
```

What happens:

* A verification URL and short code are displayed in your terminal
* Your browser opens to the verification URL
* Enter/confirm the code to complete authentication

Notes:

* The OAuth2 provider and domain are configured via `crewai config` (defaults use `login.crewai.com`)
* After successful login, the CLI also attempts to authenticate to the Tool Repository automatically
* If you reset your configuration, run `crewai login` again to re-authenticate

### 12. API Keys

When running the `crewai create crew` command, the CLI shows a list of available LLM providers, followed by model selection for your chosen provider. The selected model is saved in the generated `.env` file and each generated agent JSONC file can set its own `llm`.

Once you've selected an LLM provider and model, you will be prompted for API keys.

#### Available LLM Providers

Here's a list of the most popular LLM providers suggested by the CLI:

* OpenAI
* Groq
* Anthropic
* Google Gemini
* SambaNova

When you select a provider, the CLI will then show you available models for that provider and prompt you to enter your API key.

#### Other Options

If you select "other", you will be able to select from a list of LiteLLM supported providers.

When you select a provider, the CLI will prompt you to enter the Key name and the API key.

See the following link for each provider's key name:

* [LiteLLM Providers](https://docs.litellm.ai/docs/providers)

### 13. Configuration Management

Manage CLI configuration settings for CrewAI.

```shell Terminal theme={null}
crewai config [COMMAND] [OPTIONS]
```

#### Commands:

* `list`: Display all CLI configuration parameters

```shell Terminal theme={null}
crewai config list
```

* `set`: Set a CLI configuration parameter

```shell Terminal theme={null}
crewai config set <key> <value>
```

* `reset`: Reset all CLI configuration parameters to default values

```shell Terminal theme={null}
crewai config reset
```

#### Available Configuration Parameters

* `enterprise_base_url`: Base URL of the CrewAI AMP instance
* `oauth2_provider`: OAuth2 provider used for authentication (e.g., workos, okta, auth0)
* `oauth2_audience`: OAuth2 audience value, typically used to identify the target API or resource
* `oauth2_client_id`: OAuth2 client ID issued by the provider, used during authentication requests
* `oauth2_domain`: OAuth2 provider's domain (e.g., your-org.auth0.com) used for issuing tokens

#### Examples

Display current configuration:

```shell Terminal theme={null}
crewai config list
```

Example output:

| Setting               | Value                                            | Description                                  |
| :-------------------- | :----------------------------------------------- | :------------------------------------------- |
| enterprise\_base\_url | [https://app.crewai.com](https://app.crewai.com) | Base URL of the CrewAI AMP instance          |
| org\_name             | Not set                                          | Name of the currently active organization    |
| org\_uuid             | Not set                                          | UUID of the currently active organization    |
| oauth2\_provider      | workos                                           | OAuth2 provider (e.g., workos, okta, auth0)  |
| oauth2\_audience      | client\_01YYY                                    | Audience identifying the target API/resource |
| oauth2\_client\_id    | client\_01XXX                                    | OAuth2 client ID issued by the provider      |
| oauth2\_domain        | login.crewai.com                                 | Provider domain (e.g., your-org.auth0.com)   |

Set the enterprise base URL:

```shell Terminal theme={null}
crewai config set enterprise_base_url https://my-enterprise.crewai.com
```

Set OAuth2 provider:

```shell Terminal theme={null}
crewai config set oauth2_provider auth0
```

Set OAuth2 domain:

```shell Terminal theme={null}
crewai config set oauth2_domain my-company.auth0.com
```

Reset all configuration to defaults:

```shell Terminal theme={null}
crewai config reset
```

<Tip>
  After resetting configuration, re-run `crewai login` to authenticate again.
</Tip>

### 14. Trace Management

Manage trace collection preferences for your Crew and Flow executions.

```shell Terminal theme={null}
crewai traces [COMMAND]
```

#### Commands:

* `enable`: Enable trace collection for crew/flow executions

```shell Terminal theme={null}
crewai traces enable
```

* `disable`: Disable trace collection for crew/flow executions

```shell Terminal theme={null}
crewai traces disable
```

* `status`: Show current trace collection status

```shell Terminal theme={null}
crewai traces status
```

#### How Tracing Works

Trace collection is controlled by checking three settings in priority order:

1. **Explicit flag in code** (highest priority - can enable OR disable):

   ```python
   crew = Crew(agents=[...], tasks=[...], tracing=True)   # Always enable
   crew = Crew(agents=[...], tasks=[...], tracing=False)  # Always disable
   crew = Crew(agents=[...], tasks=[...])                 # Check lower priorities (default)
   ```

   * `tracing=True` will **always enable** tracing (overrides everything)
   * `tracing=False` will **always disable** tracing (overrides everything)
   * `tracing=None` or omitted will check lower priority settings

2. **Environment variable** (second priority):

   ```env
   CREWAI_TRACING_ENABLED=true
   ```

   * Checked only if `tracing` is not explicitly set to `True` or `False` in code
   * Set to `true` or `1` to enable tracing

3. **User preference** (lowest priority):
   ```shell Terminal theme={null}
   crewai traces enable
   ```
   * Checked only if `tracing` is not set in code and `CREWAI_TRACING_ENABLED` is not set to `true`
   * Running `crewai traces enable` is sufficient to enable tracing by itself

<Note>
  **To enable tracing**, use any one of these methods:

  * Set `tracing=True` in your Crew/Flow code, OR
  * Add `CREWAI_TRACING_ENABLED=true` to your `.env` file, OR
  * Run `crewai traces enable`

  **To disable tracing**, use any ONE of these methods:

  * Set `tracing=False` in your Crew/Flow code (overrides everything), OR
  * Remove or set to `false` the `CREWAI_TRACING_ENABLED` env var, OR
  * Run `crewai traces disable`

  Higher priority settings override lower ones.
</Note>

<Tip>
  For more information about tracing, see the [Tracing
  documentation](/observability/tracing).
</Tip>

<Tip>
  CrewAI CLI handles authentication to the Tool Repository automatically when
  adding packages to your project. Just append `crewai` before any `uv` command
  to use it. E.g. `crewai uv add requests`. For more information, see [Tool
  Repository](https://docs.crewai.com/enterprise/features/tool-repository) docs.
</Tip>

<Note>
  Configuration settings are stored in `~/.config/crewai/settings.json`. Some
  settings like organization name and UUID are read-only and managed through
  authentication and organization commands. Tool repository related settings are
  hidden and cannot be set directly by users.
</Note>