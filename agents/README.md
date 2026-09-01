# Agents

Three small [Conductor Agents](https://orkes.io/content/devguide/ai/conductor-agents) —
authored in Python, compiled by Conductor into an ordinary workflow definition
when deployed. Each `.json` file here is an **export of the registered
agent** for reference/inspection; the `.py` file next to it in `agent_code/`
is the actual source of truth you run to (re)create it.

| Agent | Definition | Source | Demonstrates |
|---|---|---|---|
| `weather_agent` | `weather_agent.json` | `agent_code/weather_agent.py` | A tool-calling agent: the LLM decides when to call the `weather_lookup` tool (backed by the `weather_lookup` worker in [`workers/`](../workers/README.md)) for each city the user asks about. |
| `support_reply_agent` | `support_reply_agent.json` | `agent_code/support_reply_agent.py` | An output **guardrail**: a `RegexGuardrail` (`no_pii`) blocks-and-retries any response containing an email address. |
| `support_agent_llm_guard` | `support_agent_llm_guard.json` | `agent_code/support_agent_llm_guard.py` | An `LLMGuardrail`: a *second* LLM call judges each response against a policy ("no specific financial/investment advice") and blocks-and-retries on failure — for policies too fuzzy for a regex. |

## Registering an agent in your cluster

Agents aren't registered via a plain REST metadata call the way workflows or
event handlers are — the SDK compiles and deploys them. To (re)create one:

```bash
pip install conductor-python conductor-agent-sdk
```

Then open the matching file in `agent_code/`, fill in your own
`server_api_url`, `key_id`, and `key_secret` (top of the file), and run it:

```bash
python agents/agent_code/weather_agent.py
```

`runtime.deploy(agent)` registers/updates the agent definition on your
cluster and exits — it's a one-shot deploy script, not a long-running
process (unlike the workers, which poll forever). `weather_agent.py` also
needs the `weather_lookup` worker (see [`workers/README.md`](../workers/README.md))
running somewhere for its tool calls to actually resolve.

The exported `.json` files are **not** meant to be imported directly through
the workflow/event-handler import paths described in the root
[README](../README.md#importing-into-your-own-cluster) — they're there so you
can read the registered shape without spinning up Python. The Automated
import options in the root README skip agents on purpose; the `agent_code/*.py`
scripts above are the supported way to bring these in.
