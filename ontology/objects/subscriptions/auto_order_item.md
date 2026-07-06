---
type: "Ontology Object"
object: auto_order_item
domain: subscriptions
tier: core
resource: "urn:ultracart:ontology:object:auto_order_item"
version: 1
grain: "one row per subscription item (uc_auto_orders × UNNEST(items)) — the recurring-revenue grain"
key:
  fields: [auto_order_item_oid]
  identity_family: auto_order_item_oid
source:
  binding: uc_auto_orders
  default_table: "{{source_project}}.{{dataset.medium}}.uc_auto_orders"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
  unnest: {field: items, alias: it}
properties:
  - name: auto_order_item_oid
    type: INTEGER
    source: it.auto_order_item_oid
    meaning: "UltraCart primary key for the subscription item"
  - name: auto_order_oid
    type: INTEGER
    source: auto_order_oid
    meaning: "parent subscription container"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: email_hash_b64
    type: STRING
    source: original_order.billing.email_hash
    meaning: "subscriber identity (base64 sha256 of normalized email; see identity spine)"
  - name: auto_order_status
    type: STRING
    source: status
    meaning: "container lifecycle status carried down for filtering (active | canceled | disabled | merged)"
    enum_ref: auto_order_status
  - name: original_item_id
    type: STRING
    source: it.original_item_id
    meaning: "the SKU that controls scheduling — API schedule updates address the item by this id"
  - name: next_item_id
    type: STRING
    source: it.next_item_id
    meaning: "calculated SKU of the next rebill (differs from original after an item swap)"
  - name: arbitrary_item_id
    type: STRING
    source: it.arbitrary_item_id
    meaning: "item swap: SKU to rebill instead of the normal schedule, when set"
  - name: paused
    type: BOOLEAN
    source: it.paused
    meaning: "ITEM-level pause — pause state lives here, not on the container"
  - name: frequency
    type: STRING
    source: it.frequency
    meaning: "rebill cadence (fixed enum; N-day cycles use arbitrary_schedule_days)"
    enum_ref: auto_order_item_frequency
  - name: arbitrary_schedule_days
    type: INTEGER
    source: it.arbitrary_schedule_days
    meaning: "custom every-N-days cadence when frequency alone doesn't express it"
  - name: next_shipment_dts
    type: DATETIME
    source: it.calculated_next_shipment_dts
    meaning: "next rebill (the read-only calculated_ variant — retry-aware; NULL when no more shipments are coming)"
  - name: scheduled_next_shipment_dts
    type: DATETIME
    source: it.next_shipment_dts
    meaning: "raw scheduled field — the one 'change ship date'/'skip' API updates write to; can be stale vs calculated"
  - name: first_order_dts
    type: DATETIME
    source: it.first_order_dts
    meaning: "first order of this subscription item"
  - name: last_order_dts
    type: DATETIME
    source: it.last_order_dts
    meaning: "most recent rebill of this item"
  - name: cancel_dts
    type: DATETIME
    source: it.cancel_dts
    meaning: "ITEM-level cancel timestamp (single-item cancel; container may stay active)"
  - name: cancel_reason
    type: STRING
    source: it.cancel_reason
    meaning: "item cancel reason — merchant-configured vocabulary, not a fixed enum"
  - name: no_order_after_dts
    type: DATETIME
    source: it.no_order_after_dts
    meaning: "stop-after date; no rebills scheduled past this"
  - name: number_of_rebills
    type: INTEGER
    source: it.number_of_rebills
    meaning: "rebills executed so far"
  - name: remaining_repeat_count
    type: INTEGER
    source: it.remaining_repeat_count
    meaning: "rebills left on fixed-length schedules (NULL = open-ended)"
  - name: life_time_value
    type: NUMERIC
    source: it.life_time_value
    meaning: "cumulative revenue attributed to this subscription item"
  - name: rebill_value
    type: NUMERIC
    source: it.rebill_value
    meaning: "value of a single rebill at current terms"
  - name: arbitrary_unit_cost
    type: NUMERIC
    source: it.arbitrary_unit_cost
    meaning: "price override applied to rebills, when set"
  - name: original_quantity
    type: NUMERIC
    source: it.original_quantity
    meaning: "quantity per rebill as originally established"
  - name: arbitrary_quantity
    type: NUMERIC
    source: it.arbitrary_quantity
    meaning: "quantity override for future rebills, when set"
  - name: preshipment_notice_sent
    type: BOOLEAN
    source: it.preshipment_notice_sent
    meaning: "customer was notified ahead of the next rebill"
links:
  - to: auto_order
    kind: belongs_to
    on: "auto_order_item.auto_order_oid = auto_order.auto_order_oid"
  - to: item
    kind: refers_to
    on: "auto_order_item.original_item_id = item.merchant_item_id"
enums:
  auto_order_status: [active, canceled, disabled, merged]
  auto_order_item_frequency: ["Weekly", "Biweekly", "Every 10 Days", "Every 24 Days", "Every 28 Days", "Monthly", "Every 45 Days", "Every 2 Months", "Every 3 Months", "Every 4 Months", "Every 5 Months", "Every 6 Months", "Yearly", "Every 4 Weeks", "Every 6 Weeks", "Every 8 Weeks"]
pii: pseudonymous
excluded_fields: [original_order, rebill_orders, emails, logs, add_ons, properties, items.add_ons, items.options, items.properties, items.future_schedules, items.simple_schedule, items.paypal_payer_id, items.paypal_recurring_payment_profile_id]
consumers: []
---

# AutoOrderItem

**THIS is the recurring-revenue grain.** The `auto_order` container holds the customer
and lifecycle status; everything that determines *what ships next, when, at what price*
lives on the item: frequency, next shipment, per-item pause, per-item cancel, LTV,
price/quantity overrides. MRR, rebill forecasting, pause/skip analytics — all of it is
computed here, then rolled up to the container or the customer.

Schedule-state semantics (from the REST API, which the DW mirrors):
- **"Skip a shipment" and "change ship date" are not endpoints** — they are field
  updates on this item: advancing `items[].next_shipment_dts` via
  `PUT /auto_order/auto_orders/{auto_order_oid}`. That is why
  `scheduled_next_shipment_dts` is exposed alongside the preferred `next_shipment_dts`
  (the read-only **calculated** variant, which is retry-aware and goes NULL when the
  schedule is exhausted — the honest "is anything actually coming?" signal).
- **Pause is item-level** (`paused`); a "paused subscription" is a container whose
  items are all paused (`auto_order.subscription_state` derives it from here).
- **Item swap**: `arbitrary_item_id` overrides the schedule; `next_item_id` is the
  calculated result. Revenue by SKU should use `next_item_id` for forward-looking and
  `original_item_id` for cohort views.
- Item-level `cancel_dts` ends one item while siblings continue — container
  `canceled_dts` alone under-counts item churn.

Gotchas: the projected rebill calendar (`items[].future_schedules`, next 10 rebills)
is excluded — model it separately for future-revenue views. `life_time_value` /
`rebill_value` are UltraCart-maintained aggregates, not recomputed from orders; treat
them as convenience fields and reconcile against `order` for audits. Frequency is a
fixed enum, but N-day cadences ride in `arbitrary_schedule_days`.

## Change log
- v1 (2026-07-06) — initial.
