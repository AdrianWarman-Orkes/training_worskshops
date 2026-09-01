# Workers

Python task workers, written with the [Conductor Python
SDK](https://orkes.io/content/sdks/python) (`pip install conductor-python`).
Each file polls your cluster for one task type by name and executes it when a
workflow reaches that task.

| Worker | Task name | Used by | What it does |
|---|---|---|---|
| `hello_world.py` | `hello_world` | — (standalone demo) | Minimal example: takes `name`, returns a `TaskResult` with a log line and `greeting` output. Good first worker to run to prove your connection/auth works. |
| `generate_invoice.py` | `generate_invoice` | `customer_order_workflow.json` → `generate_invoice_ref` | Deterministic, no external calls — builds an invoice number from `orderId` and echoes back the amount/transaction ID. Stand-in for a real invoicing system. |
| `weather_lookup.py` | `weather_lookup` | `agents/weather_agent.json`'s `weather_lookup` tool | Calls the free, keyless [Open-Meteo](https://open-meteo.com/) API to geocode a city and fetch current conditions. The one example in this repo that's fully runnable with **no secrets or accounts** required. |

## Running one

Each file has `SERVER_URL` / `KEY` / `SECRET` (or `CONDUCTOR_SERVER_URL` /
`CONDUCTOR_AUTH_KEY` / `CONDUCTOR_AUTH_SECRET`) placeholders near the top —
fill in your own cluster URL and application key/secret, then:

```bash
pip install conductor-python
python workers/hello_world.py
```

The process blocks and polls until you kill it (`Ctrl+C`) — that's expected,
it's a long-running worker, not a one-shot script. Leave it running in a
terminal while you start the matching workflow from the Conductor UI.
