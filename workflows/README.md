# Workflows

## `customer_order_workflow.json`

The main live-build demo workflow for the workshop. It's designed to touch most of
the common Conductor task types in one realistic order-processing flow, so you can
walk through it task-by-task and see each concept in context.

| Step | Task ref | Type | What it demos |
|---|---|---|---|
| 1 | `check_inventory_ref` | `HTTP` | Calling an external service |
| 2 | `business_rule_ref` | `BUSINESS_RULE` | Externalizing decision logic (discount/shipping/approval) into a decision table |
| 3 | `switch_approval_ref` | `SWITCH` | Branching on the business rule's output |
| 3a | `human_approval_ref` | `HUMAN` | Pausing for a person to review/approve, backed by a user form |
| 3b | `check_approval_decision_ref` | `SWITCH` | Branching on the human's decision |
| 3c | `terminate_order_rejected_ref` | `TERMINATE` | Ending the workflow early with a controlled status |
| 4 | `build_reservation_tasks_ref` | `JSON_JQ_TRANSFORM` | Building a list of tasks + inputs at runtime from `workflow.input.cartItems` |
| 5 | `reserve_fork_ref` / `reserve_join_ref` | `FORK_JOIN_DYNAMIC` / `JOIN` | Fanning out one HTTP call per cart item (count decided at runtime) and waiting for all of them |
| 6 | `set_order_status_ref` | `SET_VARIABLE` | Writing to workflow variables |
| 7 | `compute_total_ref` | `INLINE` | Inline JS math on task outputs/variables |
| 8 | `process_payment_ref` | `SUB_WORKFLOW` | Delegating to a separate, reusable workflow |
| 9 | `generate_invoice_ref` | `SIMPLE` | A custom worker task (see `workers/generate_invoice.py`) |
| 10 | `notify_fork_ref` / `notify_join_ref` | `FORK_JOIN` / `JOIN` | Two fixed parallel branches (customer + internal email) |
| 11 | `publish_event_loop_ref` | `DO_WHILE` (`EVENT` + `WAIT`) | A bounded retry loop: publish an event, wait for an ack, retry up to 5 times instead of trusting a fire-and-forget publish |
| 12 | `check_event_confirmed_ref` | `SWITCH` + `TERMINATE` | Failing the workflow loudly if the ack never came |

### Before you can run this one

This workflow was built for a live demo against infrastructure that's specific to
that demo, not to the pattern. If you import it as-is, several things will not
work until you either replace them with your own equivalents or accept that
this task's job is just to show you the JSON shape, not to execute successfully:

- **`check_inventory_ref` and the dynamic `reserve_*` HTTP tasks** call
  `${workflow.env.inventoryBaseUrl}`, a small AWS Lambda + API Gateway endpoint
  Adrian stood up only for the workshop demo. **It is not publicly available** —
  don't expect these HTTP tasks to succeed against it. Point `inventoryBaseUrl`
  at your own mock/stub if you want the workflow to actually run end-to-end.
- **`workflow.env.inventoryBaseUrl`**, **`workflow.env.ruleFileLocation`**,
  **`workflow.env.adrian_work_email`**, **`workflow.env.adrian_email_1`** are
  workflow environment variables. These live server-side (Conductor UI →
  Definitions → Environment Variables, or your own cluster's equivalent) —
  they are **not** stored in this repo and you'll need to set your own values
  in your cluster.
- **`sendgridConfiguration: "sendgrid"`** on the two `SENDGRID` tasks refers to
  an Integration named `sendgrid` that must exist in your cluster (Integrations
  → SendGrid) with a real API key. That key is a secret held by your cluster,
  never in this repo.
- **`business_rule_ref`** points at a decision table via `ruleFileLocation`.
  The actual rules file isn't part of this repo's exported metadata — you'll
  need to author your own (see the [BUSINESS_RULE task
  docs](https://orkes.io/content/reference-docs/tasks/business-rule)) and point
  `ruleFileLocation` at it.
- **`process_payment_ref`** calls the [`payment_processing`](#payment_processingjson)
  sub-workflow below (version 1) — register that workflow too, since it's a
  separate file. It also hits `${workflow.env.inventoryBaseUrl}/charge`, so it
  has the same "dummy endpoint" caveat as `check_inventory_ref`.
- **The `DO_WHILE` publish/ack loop** only resolves if the event handler in
  [`event_handlers/confirm_order_event.json`](../event_handlers/README.md) is
  also registered and your cluster has a working GCP Pub/Sub integration named
  `GCP_pubSub` with an `orders` topic. Without that, it'll retry 5 times, time
  out the `wait_event_ack_ref` task, and the workflow will terminate as FAILED
  by design — that's the retry-loop pattern working as intended, not a bug.
- **`human_approval_ref`** uses the [`order_approval_form`
  template](../user_forms/README.md) and assigns the task to
  `adrian.warman@orkes.io` — change the assignee to yourself before running it
  in your own cluster.

If you just want to see how the task types fit together, importing and reading
the JSON (or viewing it in the Conductor UI's workflow diagram) gets you there
without needing any of the above configured.

## `payment_processing.json`

A small standalone workflow (one `HTTP` task, `charge_payment_ref`) that
`customer_order_workflow.json` calls as a `SUB_WORKFLOW`. It's a separate file
because it's registered as its own workflow definition — both files need to be
imported for `process_payment_ref` to resolve. It shares the same
`${workflow.env.inventoryBaseUrl}` dummy-endpoint caveat described above.

## `ai_workflows/`

Seven small, single-purpose workflows, each isolating one common "AI in a
workflow" pattern. See [`ai_workflows/README.md`](ai_workflows/README.md).
