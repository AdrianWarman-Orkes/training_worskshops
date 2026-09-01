# Importing this repo into your own cluster

Two ways to get everything registered without hand-copying JSON through the
UI. Both register the same 14 metadata items and both **skip `agents/`** —
agents are deployed with the `conductor-agent-sdk` scripts in
`agents/agent_code/`, not a plain REST call (see
[`agents/README.md`](../agents/README.md)).

What gets registered:

- 9 workflows: `customer_order_workflow`, `payment_processing`, and the 7
  `ai_workflows/*`
- 1 event handler: `confirm_order_event`
- 3 user forms: `order_approval_form`, `customer_reply_review_form`,
  `expense_approval_form`
- 1 AI prompt: `meeting_summary_prompt`

Registering everything gets these examples *importable*, not automatically
*runnable* — several still need cluster-side config (your own OpenAI
integration, your own env vars, etc.) called out in each folder's README.
The `customer_order_workflow`/`payment_processing` HTTP tasks specifically
point at a private demo endpoint that only existed for Adrian's live demo and
won't respond for you — see [`workflows/README.md`](../workflows/README.md).

## Option A — Conductor bootstrap workflow

[`bootstrap_import_workflow.json`](bootstrap_import_workflow.json) is a
Conductor workflow that does the registering *from inside your cluster*: it
gets an API token, then fetches each file straight from
`raw.githubusercontent.com` and PUTs/POSTs it to the matching metadata
endpoint. No local clone, no CLI, no secrets stored anywhere but the one
execution's input.

1. In your Conductor UI: **Definitions → Workflow → Import from JSON**, and
   import `bootstrap_import_workflow.json`. (Or `POST` it yourself to
   `/api/metadata/workflow` if you'd rather not use the UI.)
2. Run it (**Run Workflow**) with input:
   ```json
   {
     "conductorApiUrl": "https://<your-cluster-url>",
     "keyId": "<your application key id>",
     "keySecret": "<your application key secret>"
   }
   ```
   (`keySecret` is masked in the UI/execution view, but it's still visible in
   plain text to anyone who can view this execution's input — use a
   throwaway/scoped application key if that matters for your cluster.)
3. Check the run: 14 `register_*` tasks should complete under the
   `register_metadata_join_ref` join. A failed branch means that one item
   didn't register — check that task's output for the response body/status
   code and fix just that one (see the caveats above).

Re-running is mostly safe: workflow and prompt registrations use `PUT`/bulk
`POST`, which upsert. If the event handler or a user form 409s on a rerun
instead of updating, delete the existing one first or switch that branch's
HTTP task from `POST` to `PUT` and re-run.

## Option B — GitHub Action

[`../.github/workflows/register-metadata.yml`](../.github/workflows/register-metadata.yml)
does the same 14 registrations from a GitHub Actions runner instead of from
inside Conductor. Useful if you'd rather keep the credentials in GitHub
secrets than paste them into a workflow execution input.

1. Fork this repo.
2. In your fork: **Settings → Secrets and variables → Actions**, add:
   - `CONDUCTOR_SERVER_URL` — e.g. `https://your-cluster.orkesconductor.io`
   - `CONDUCTOR_KEY_ID`
   - `CONDUCTOR_KEY_SECRET`
3. **Actions → Register workshop metadata → Run workflow.** It only runs on
   manual `workflow_dispatch` — it will never fire on a push or PR, since it
   writes into whatever cluster your secrets point at.

## Auth details, for reference

Both options get a short-lived token the same way:
`POST {conductorApiUrl}/api/token` with body `{"keyId": "...", "keySecret":
"..."}` returns `{"token": "..."}`; pass that back as an `X-Authorization`
header (not `Authorization: Bearer`) on every subsequent call.

Endpoint confidence: workflow (`/api/metadata/workflow`), auth (`/api/token`),
user form templates (`/api/human/template`), and AI prompts (`/api/prompts/`)
are documented in Orkes' reference docs. The event handler endpoint
(`/api/event`) matches the underlying OSS Conductor API and the field names
Orkes documents, but wasn't confirmed against an Orkes-branded reference page
— if it behaves unexpectedly on your cluster's version, that's the one to
double-check first.
