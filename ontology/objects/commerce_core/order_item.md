---
type: "Ontology Object"
object: order_item
domain: commerce_core
tier: core
resource: "urn:ultracart:ontology:object:order_item"
version: 1
grain: "one row per order line (uc_orders × UNNEST(items))"
key:
  fields: [order_id, item_index]
  identity_family: order_id
source:
  binding: uc_orders
  default_table: "{{source_project}}.{{dataset.medium}}.uc_orders"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
  unnest: {field: items, alias: item}
properties:
  - name: order_id
    type: STRING
    source: order_id
    meaning: "parent order (public order number)"
  - name: item_index
    type: INTEGER
    source: item.item_index
    meaning: "line position within the order; (order_id, item_index) is the line key"
  - name: email_hash_b64
    type: STRING
    source: billing.email_hash
    meaning: "customer identity carried down to line grain (base64 sha256; see identity spine)"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: order_date
    type: DATE
    source: "DATE(creation_dts)"
    meaning: "calendar date the parent order was placed (UTC)"
  - name: current_stage
    type: STRING
    source: current_stage
    meaning: "parent order lifecycle stage — carried down so line-grain revenue can filter without a join"
    enum_ref: order_stage
  - name: payment_dts
    type: DATETIME
    source: payment.payment_dts
    meaning: "parent order paid timestamp — NULL means the line never generated revenue"
  - name: is_test_order
    type: BOOLEAN
    source: payment.test_order
    meaning: "parent order test flag; exclude from revenue at line grain too"
  - name: item_id
    type: STRING
    source: item.merchant_item_id
    meaning: "the SKU as sold (joins to item.merchant_item_id)"
  - name: description
    type: STRING
    source: item.description
    meaning: "line description at time of sale"
  - name: quantity
    type: NUMERIC
    source: item.quantity
    meaning: "units ordered on this line"
  - name: unit_cost
    type: NUMERIC
    source: item.cost.value
    meaning: "per-unit price before line discount (account currency)"
  - name: unit_cost_with_discount
    type: NUMERIC
    source: item.unit_cost_with_discount.value
    meaning: "per-unit price after line discount"
  - name: discount
    type: NUMERIC
    source: item.discount.value
    meaning: "line-level discount amount"
  - name: total_with_discount
    type: NUMERIC
    source: item.total_cost_with_discount.value
    meaning: "extended line total after discount — the line-grain revenue amount"
  - name: quantity_refunded
    type: NUMERIC
    source: item.quantity_refunded
    meaning: "units refunded on this line"
  - name: total_refunded
    type: NUMERIC
    source: item.total_refunded.value
    meaning: "amount refunded on this line"
  - name: refund_reason
    type: STRING
    source: item.refund_reason
    meaning: "item-level refund reason — merchant-configured code list, not a fixed enum"
  - name: cogs
    type: NUMERIC
    source: item.cogs
    meaning: "cost of goods sold per unit as recorded at order time"
  - name: auto_order_schedule
    type: STRING
    source: item.auto_order_schedule
    meaning: "subscription frequency marker on the line; NULL = one-time purchase line"
  - name: auto_order_last_rebill_dts
    type: DATETIME
    source: item.auto_order_last_rebill_dts
    meaning: "last rebill timestamp when the line is a subscription rebill"
  - name: upsell
    type: BOOLEAN
    source: item.upsell
    meaning: "line was added via a post-checkout upsell offer"
  - name: kit
    type: BOOLEAN
    source: item.kit
    meaning: "line is a kit parent"
  - name: kit_component
    type: BOOLEAN
    source: item.kit_component
    meaning: "line is a kit component (beware double-counting revenue with the parent)"
  - name: shipped_dts
    type: DATETIME
    source: item.shipped_dts
    meaning: "when this line shipped (NULL if not shipped)"
links:
  - to: order
    kind: belongs_to
    on: "order_item.order_id = order.order_id"
  - to: item
    kind: refers_to
    on: "order_item.item_id = item.merchant_item_id"
enums:
  order_stage: ["Accounts Receivable", "Pending Clearance", "Fraud Review", "Rejected", "Shipping Department", "Completed Order", "Quote Request", "Quote Sent", "Least Cost Routing", "Unknown", "Pre-ordered", "Advanced Order Routing", "Hold"]
pii: pseudonymous
excluded_fields: [billing, shipping, customer_profile, coupons, affiliates, utms, emails, payment.transactions, items.options, items.properties, items.edi, items.tags, items.activation_codes, items.activation_code_hashes]
consumers: []
---

# OrderItem

One **order line**: the product-grain view of commerce. Compiled as
`FROM uc_orders, UNNEST(items) AS item`, so every line carries its parent's stage,
payment timestamp and test flag — line-grain revenue filtering needs no join back to
the header:

```
current_stage IN ('Shipping Department', 'Completed Order') AND payment_dts IS NOT NULL
AND is_test_order IS NOT TRUE
```

(Channel-partner exclusion still lives at the order level — join to `order` or use the
`revenue_order` definition when direct-sales-only line revenue is required.)

Notes:
- `total_with_discount` is the extended line amount; `unit_cost` × `quantity` −
  `discount` reconciles to it. Line amounts are in the account currency (`value`
  fields), matching the order header summary.
- **Kits**: a kit sale produces a parent line (`kit`) plus component lines
  (`kit_component`); sum only one side when totaling revenue.
- `auto_order_schedule` is the line-level subscription marker — the cleanest way to
  split new/one-time vs recurring revenue at product grain. The subscription itself is
  `auto_order_item` (schedule state) via the parent order's `auto_order_oid`.
- Item identity is the string SKU `merchant_item_id`; there is no merchant_item_oid on
  order lines.

## Change log
- v1 (2026-07-06) — initial.
