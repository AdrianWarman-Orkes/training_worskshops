# Event Handlers

## `confirm_order_event.json`

Listens on the `gcp_pubsub:GCP_pubSub:orders` event sink and completes the
retry loop in [`customer_order_workflow.json`](../workflows/README.md): when
a message arrives whose payload has `fromWorkflow == true` and whose
`workflowType` is `customer_order_workflow`, it

1. writes the payload onto that workflow instance's variables
   (`update_workflow_variables`, `appendArray: true`), and
2. completes the `wait_event_ack_ref` task with `{"event_published": true}`
   (`complete_task`), which lets that workflow's `DO_WHILE` loop exit
   immediately instead of retrying up to 5 times / ~75 seconds.

It exists to demonstrate acknowledging an async event *back into* the
workflow that published it, rather than trusting a fire-and-forget publish.

### Before you register this one

- It only fires for a sink named `gcp_pubsub:GCP_pubSub:orders` — your cluster
  needs a GCP Pub/Sub integration named `GCP_pubSub` (Integrations → Message
  Broker → GCP Pub/Sub) with an `orders` topic, and your own GCP service
  account credentials. None of that is stored in this repo.
- Without it registered *and* wired up, `customer_order_workflow.json`'s
  publish/ack loop will simply exhaust its retries and terminate as `FAILED`
  — that's the timeout-and-fail path working as designed, not a broken
  import.
