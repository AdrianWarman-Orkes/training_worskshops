# User Forms

JSON Schema + [JSONForms](https://jsonforms.io/)-style `templateUI` layouts
used by `HUMAN` tasks (`userFormTemplate: {name, version}`) to render a review
screen in the Conductor UI / Human Task inbox. Each form pairs a `jsonSchema`
(the data shape and validation) with a `templateUI` (how it's laid out —
groups, read-only fields, radio vs. free text, etc.).

| Form | Used by | What the reviewer sees |
|---|---|---|
| `order_approval_form.json` | `customer_order_workflow.json` → `human_approval_ref` | Read-only order details (ID, category, price, item count, discount, shipping) plus an approve/reject radio and optional comments. |
| `expense_approval_form.json` | `workflows/ai_workflows/approval_assistant.json` → `human_review_ref` | Read-only expense details **and** the AI's recommendation + reasoning, then a human approve/reject decision. |
| `customer_reply_review_form.json` | `workflows/ai_workflows/human_review_after_ai.json` → `human_review_draft_ref` | The customer's original email (read-only) and the AI-drafted reply as an **editable** text field, then approve/reject + notes. Rejection notes feed back into the next AI draft attempt. |

All three require the `decision` field (`approve`/`reject`); everything else
is optional or read-only context for the reviewer.

Register these before (or together with) the workflows that reference them —
a `HUMAN` task will fail to render if its `userFormTemplate` name/version
doesn't resolve to a form in your cluster.
