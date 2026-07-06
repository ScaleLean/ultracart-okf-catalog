---
type: "Ontology Object"
object: auto_order
domain: subscriptions
tier: core
resource: "urn:ultracart:ontology:object:auto_order"
version: 1
grain: "one row per auto-order (the subscription container; items live in auto_order_item)"
key:
  fields: [auto_order_oid]
  identity_family: auto_order_oid
source:
  binding: uc_auto_orders
  default_table: "{{source_project}}.{{dataset.medium}}.uc_auto_orders"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: auto_order_oid
    type: INTEGER
    source: auto_order_oid
    meaning: "UltraCart primary key for the subscription container"
  - name: auto_order_code
    type: STRING
    source: auto_order_code
    meaning: "human-facing subscription code"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: email_hash_b64
    type: STRING
    source: original_order.billing.email_hash
    meaning: "customer identity (base64 sha256 of normalized email; see identity spine)"
  - name: status
    type: STRING
    source: status
    meaning: "raw lifecycle status (API enum: active | canceled | disabled | merged)"
    enum_ref: auto_order_status
  - name: all_items_paused
    type: BOOLEAN
    source: "(SELECT LOGICAL_AND(COALESCE(i.paused, FALSE)) FROM UNNEST(items) AS i)"
    refs: [items.paused]
    meaning: "pause lives on ITEMS, not the container; true when every item is paused"
  - name: subscription_state
    type: STRING
    source: "CASE WHEN status = 'active' AND (SELECT LOGICAL_AND(COALESCE(i.paused, FALSE)) FROM UNNEST(items) AS i) THEN 'paused' WHEN status = 'active' THEN 'active' ELSE 'ended' END"
    refs: [status, items.paused]
    meaning: "canonical 3-state lifecycle: active | paused (all items paused) | ended"
  - name: enabled
    type: BOOLEAN
    source: enabled
    meaning: "raw enabled flag"
  - name: completed
    type: BOOLEAN
    source: completed
    meaning: "ran its full schedule to completion"
  - name: original_order_id
    type: STRING
    source: original_order_id
    meaning: "order that created the subscription"
  - name: next_attempt_at
    type: DATETIME
    source: next_attempt
    meaning: "next billing/shipment attempt"
  - name: canceled_at
    type: DATETIME
    source: canceled_dts
    meaning: "when canceled (NULL if not)"
  - name: canceled_by
    type: STRING
    source: canceled_by_user
    meaning: "who canceled (user/system)"
  - name: cancel_reason
    type: STRING
    source: cancel_reason
    meaning: "recorded cancellation reason"
  - name: disabled_at
    type: DATETIME
    source: disabled_dts
    meaning: "when disabled (NULL if not)"
  - name: ended_at
    type: DATETIME
    source: "COALESCE(canceled_dts, disabled_dts, merged_dts)"
    meaning: "canonical end timestamp across cancel/disable/merge"
  - name: failure_reason
    type: STRING
    source: failure_reason
    meaning: "last billing failure reason"
  - name: credit_card_attempt
    type: INTEGER
    source: credit_card_attempt
    meaning: "current dunning attempt count"
  - name: merged_into_auto_order_oid
    type: INTEGER
    source: merged_into_auto_order_oid
    meaning: "if merged, the surviving container"
  - name: item_count
    type: INTEGER
    source: "ARRAY_LENGTH(items)"
    meaning: "subscription items in the container"
links:
  - to: customer
    kind: belongs_to
    on: "auto_order.email_hash_b64 = customer.email_hash_b64"
  - to: order
    kind: originated_from
    on: "auto_order.original_order_id = order.order_id"
  - to: auto_order_item
    kind: has_many
    on: "auto_order.auto_order_oid = auto_order_item.auto_order_oid"
enums:
  auto_order_status: [active, canceled, disabled, merged]
pii: pseudonymous
excluded_fields: [original_order, emails, credit_card, items, logs, add_ons, properties]
consumers: []
---

# AutoOrder

The subscription **container**: one customer's recurring arrangement, holding one or
more subscription items (see `auto_order_item` for the item grain — frequency,
next-shipment, per-item pause, LTV all live there). Recurring revenue questions almost
always want the item grain; retention/churn questions usually want this container grain.

Lifecycle: the API enum for `status` is `active | canceled | disabled | merged`
(`disabled` = failed-rebill exhaustion, NOT a customer cancel; `merged` = container
absorbed into another). **Pause is item-level** (`items[].paused`) — a "paused
subscription" is an active container whose items are all paused; `subscription_state`
derives exactly that. **Paused is neither active nor lapsed** — treat it as its own
pool (observed at one merchant: the paused pool was 2× the active pool). `ended_at` is
the canonical end date; `failure_reason` + `credit_card_attempt` tell the dunning story.
Cancel reasons are **merchant-configured vocabularies** (API `GET
/auto_order/auto_orders/cancel_reasons`), not a fixed enum — never hard-code them.

Gotchas:
- The full `original_order` snapshot (1,130 field paths) is deliberately excluded from
  the canonical view; join to `order` via `original_order_id` instead.
- `emails` (engagement events) and `logs` are excluded arrays — model them separately
  if ever needed; they carry raw email addresses.
- Merged containers: rows with `merged_into_auto_order_oid` are superseded — exclude
  them from live counts (`subscription_state` already lands them in `ended`).

## Change log
- v1 (2026-07-06) — initial, from OKF field paths + UltraCart docs + CE field learnings.
