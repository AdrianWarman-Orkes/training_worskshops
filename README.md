# Orkes Conductor Training Workshops

Sample workflows, AI patterns, agents, and supporting metadata from Adrian
Warman's Orkes Conductor workshops. Use these to see how the common task
types fit together in a realistic workflow, to try out AI usage patterns in
isolation, and as a starting point for your own examples.

## What's here

| Folder | Contents |
|---|---|
| [`workflows/`](workflows/README.md) | `customer_order_workflow.json` — the main live-build demo, touching most of the common Conductor task types — plus its `payment_processing` sub-workflow. |
| [`workflows/ai_workflows/`](workflows/ai_workflows/README.md) | Seven small workflows, each isolating one AI-in-a-workflow pattern: classification, extraction, document processing, summarization, recommendations, approval assistant, human-review-after-AI. |
| [`ai_prompts/`](ai_prompts/README.md) | A server-stored AI Prompt template used by the summarization pattern. |
| [`agents/`](agents/README.md) | Three Conductor Agents (tool-calling, regex guardrail, LLM guardrail) plus the Python SDK scripts (`agent_code/`) used to create them. |
| [`event_handlers/`](event_handlers/README.md) | The event handler that acknowledges `customer_order_workflow`'s publish/retry loop. |
| [`user_forms/`](user_forms/README.md) | The three `HUMAN` task review screens used across the samples above. |
| [`workers/`](workers/README.md) | Python task workers backing the custom `SIMPLE` tasks and the weather agent's tool. |
| [`import/`](import/README.md) | Two ways to register all of the above into your own cluster in one shot. |

Start with [`workflows/README.md`](workflows/README.md) for a task-by-task
walkthrough of the main demo workflow, then browse the others depending on
what you want to see.

## Prerequisites

- A Conductor cluster you control (Orkes Cloud or self-hosted OSS) and an
  application key/secret with permission to create metadata.
- An AI Model Integration (OpenAI) configured server-side if you want to run
  anything under `workflows/ai_workflows/` or `agents/` — every LLM task here
  uses `llmProvider: "OpenAI"` / model `gpt-4o-mini`. That integration and its
  API key live in your cluster's config, never in this repo.
- Python 3.9+ if you want to run the workers or (re)deploy the agents.

## A note on secrets, env vars, and the "dummy service"

Nothing in this repo is a live, shared backend — every example that talks to
something external is either fully public/keyless, or was wired up against
throwaway infrastructure for a specific live demo:

- **`customer_order_workflow.json`** and **`payment_processing.json`** call
  `${workflow.env.inventoryBaseUrl}`, a small AWS Lambda + API Gateway
  endpoint Adrian stood up only for the workshop's live demo so the HTTP
  tasks would hit something real on stage. **It is not publicly available**
  — importing these workflows lets you see the task structure, but the HTTP
  calls will not succeed against that URL. Point `inventoryBaseUrl` at your
  own stub if you want it to run end-to-end.
- Anywhere you see `${workflow.env.*}` (env vars) or an integration name like
  `sendgridConfiguration: "sendgrid"` or `gcp_pubsub:GCP_pubSub:orders` (a
  secret-backed integration), that value is configured **server-side** in
  the cluster where the workflow runs — Conductor UI → Definitions →
  Environment Variables / Integrations, or your own cluster's equivalent.
  None of those values are, or should be, checked into this repo.
- The one fully keyless, fully runnable example end-to-end is the
  `weather_agent` + `weather_lookup` worker — it calls the free,
  no-API-key [Open-Meteo](https://open-meteo.com/) API.

See each folder's README for the specific gaps you'd need to fill to make a
given example actually execute, versus just importable to read.

## Importing into your own cluster

[`import/`](import/README.md) has two ready-made options:

- **A Conductor bootstrap workflow** you import once and run — it fetches
  every workflow, event handler, user form, and AI prompt straight from this
  repo's `raw.githubusercontent.com` URLs and registers them in your cluster.
- **A GitHub Action** you trigger manually (`workflow_dispatch`) after
  forking, using your own `CONDUCTOR_SERVER_URL`/key/secret as repo secrets.

Both skip `agents/` on purpose — those are registered by running the
`conductor-agent-sdk` scripts in `agents/agent_code/`, not a REST call. See
[`import/README.md`](import/README.md) for the full walkthrough and
[`agents/README.md`](agents/README.md) for deploying the agents.
