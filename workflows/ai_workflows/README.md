# AI Workflow Patterns

Seven small workflows, each isolating one common pattern for using an LLM
inside a Conductor workflow. They're deliberately minimal — most take no
input and have the sample data baked in via `SET_VARIABLE`, so you can import
one, click Run, and see the pattern work without wiring anything up.

**Shared prerequisite:** every workflow here uses an `LLM_CHAT_COMPLETE` task
with `"llmProvider": "OpenAI"`. That means your cluster needs an **AI Model
Integration** for OpenAI configured server-side (Conductor UI → Integrations →
AI Model Providers → OpenAI, or your own cluster's equivalent) with your own
API key. The key lives in your cluster's integration config, never in this
repo.

| Workflow | Pattern | Tasks | Notes |
|---|---|---|---|
| `classification.json` (`ai_pattern_classification`) | **Classification** — sort freeform text into a fixed set of categories | `SET_VARIABLE` → `LLM_CHAT_COMPLETE` → `SWITCH` | Only `ticket_1` is classified by default — edit `classify_ticket_ref`'s user message to point at `ticket_2` or `ticket_3` (or your own text) to see a different category come back and a different `SWITCH` branch fire. |
| `extraction.json` (`ai_pattern_extraction`) | **Extraction** — pull structured fields out of freeform text | `SET_VARIABLE` → `LLM_CHAT_COMPLETE` | Compare with Document Processing below: same idea, but no file/PDF step — the email text is already there. |
| `document_processing.json` (`ai_pattern_document_processing`) | **Document processing** — unstructured file → structured record | `GENERATE_PDF` → `GET_DOCUMENT` → `LLM_CHAT_COMPLETE` | Renders a markdown invoice to a real PDF, reads its text back out, then extracts structured fields from that text. Needs the `GENERATE_PDF`/`GET_DOCUMENT` system tasks available on your cluster. |
| `summarization.json` (`ai_pattern_summarization`) | **Summarization** | `SET_VARIABLE` → `LLM_CHAT_COMPLETE` | References a **server-stored prompt** named `meeting_summary_prompt` (Conductor UI → Definitions → AI Prompts) via the task's `instructions` field, instead of inlining the prompt text. The prompt itself is exported at [`../../ai_prompts/meeting_summary_prompt.json`](../../ai_prompts/README.md) — register that too, or this workflow has nothing to call. |
| `recommendations.json` (`ai_pattern_recommendations`) | **Recommendations** | `SET_VARIABLE` → `JSON_JQ_TRANSFORM` → `LLM_CHAT_COMPLETE` | The `JSON_JQ_TRANSFORM` step exists to turn the catalog/profile objects into a JSON string via `tojson` before handing them to the LLM — passing Java objects to a prompt directly stringifies them with `toString()`, which is not valid JSON. Worth calling out live as a common gotcha. |
| `approval_assistant.json` (`ai_pattern_approval_assistant`) | **Approval assistant** — AI recommends, human decides | `JSON_JQ_TRANSFORM` → `LLM_CHAT_COMPLETE` → `HUMAN` → `SWITCH`/`TERMINATE` | Uses the [`expense_approval_form`](../../user_forms/README.md) template, which shows the approver both the raw expense and the AI's recommendation + reasoning before they decide. |
| `human_review_after_ai.json` (`ai_pattern_human_review_after_ai`, v2) | **Human review after AI, with self-correction** | `SET_VARIABLE` → `DO_WHILE` (`LLM_CHAT_COMPLETE` → `HUMAN` → `SET_VARIABLE`) → `SWITCH`/`TERMINATE` | If the reviewer rejects a draft with notes, those notes are threaded back into the *next* LLM attempt as `workflow.variables.priorFeedback`, so the AI actually revises instead of repeating itself. Bounded to 3 attempts (`maxIterations`) before it terminates as FAILED and escalates to a human to write manually. Uses the [`customer_reply_review_form`](../../user_forms/README.md) template. |

All seven share `adrian.warman@orkes.io` (or an app-owner email) as the
`ownerEmail`/task assignee where a `HUMAN` task is involved — reassign to
yourself after importing.
