# AI Prompts

Server-stored prompt templates (Conductor UI → Definitions → AI Prompts).
Storing a prompt here instead of inlining it in a workflow's `messages` lets
you edit/version the wording without touching the workflow definition, and
reuse the same prompt from multiple workflows.

## `meeting_summary_prompt.json`

Used by [`workflows/ai_workflows/summarization.json`](../workflows/ai_workflows/README.md)
via `"instructions": "meeting_summary_prompt"` on its `LLM_CHAT_COMPLETE` task.
Takes one variable, `transcript`, and asks for a JSON object with `summary`,
`key_points`, and `action_items`.

The `integrations` field (`["OpenAI:gpt-4o-mini"]`) ties this prompt to a
specific AI Model Integration + model in your cluster. Make sure your
cluster's OpenAI integration is named `OpenAI` (or update this field to match
whatever you name it) — same requirement as the `llmProvider`/`model` fields
used directly in the `ai_workflows/` definitions.
