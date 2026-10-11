---
type: "Ontology Definition"
definition: revenue_order
resource: "urn:ultracart:ontology:definition:revenue_order"
version: 1
summary: "An order that counts as real revenue: reached Shipping Department or Completed Order, has a processed payment, is not a test order, and (by default) is a direct sale rather than a channel-partner import."
parameters:
  - name: include_channel_partner_orders
    default: false
    meaning: "when true, marketplace/call-center/reseller orders (channel_partner_code set) count as revenue too; default counts direct sales only"
outputs:
  order_id: STRING
  email_hash_b64: STRING
  merchant_id: STRING
  order_date: DATE
  order_ts: DATETIME
  current_stage: STRING
  payment_dts: DATETIME
  payment_method: STRING
  payment_status: STRING
  is_test_order: BOOLEAN
  channel_partner_code: STRING
  storefront_host_name: STRING
  customer_profile_oid: INTEGER
  auto_order_oid: INTEGER
  subtotal: NUMERIC
  total: NUMERIC
  tax: NUMERIC
  shipping_charged: NUMERIC
  refunded: NUMERIC
  refund_dts: DATETIME
  refund_reason: STRING
  reject_dts: DATETIME
  fraud_score: NUMERIC
  currency_code: STRING
  exchange_rate: NUMERIC
  coupon_count: INTEGER
  item_count: INTEGER
  first_affiliate_oid: INTEGER
  utm_source_last_click: STRING
  utm_campaign_last_click: STRING
  upsell_path_code: STRING
sql: |
  SELECT
    order_id,
    email_hash_b64,
    merchant_id,
    order_date,
    order_ts,
    current_stage,
    payment_dts,
    payment_method,
    payment_status,
    is_test_order,
    channel_partner_code,
    storefront_host_name,
    customer_profile_oid,
    auto_order_oid,
    subtotal,
    total,
    tax,
    shipping_charged,
    refunded,
    refund_dts,
    refund_reason,
    reject_dts,
    fraud_score,
    currency_code,
    exchange_rate,
    coupon_count,
    item_count,
    first_affiliate_oid,
    utm_source_last_click,
    utm_campaign_last_click,
    upsell_path_code
  FROM {{ontology}}.order
  WHERE current_stage IN ('Shipping Department', 'Completed Order')
    AND payment_dts IS NOT NULL
    AND NOT COALESCE(is_test_order, FALSE)
    AND ({{param.include_channel_partner_orders}} OR channel_partner_code IS NULL)
---

# revenue_order

The UltraCart **revenue-truth convention**, lifted directly from UltraCart's own
data-warehouse sample queries (LTV / repeat-rate queries on the Confluence DW
page): "real revenue" is `current_stage IN ('Shipping Department', 'Completed
Order')` — the two stages past all payment, fraud, and routing gates — with
`Rejected` and everything upstream (`Accounts Receivable`, `Pending Clearance`,
`Fraud Review`, `Hold`, quotes, pre-orders) excluded. On top of the stage gate:

- **`payment_dts IS NOT NULL`** — the canonical "paid" timestamp in DW queries;
  a shipped-stage order without a processed payment is not revenue yet.
- **`NOT COALESCE(is_test_order, FALSE)`** — test orders flow through the same
  pipeline and must be excluded explicitly.
- **Channel-partner filter** — UltraCart's DW queries filter
  `channel_partner is null` for direct sales; marketplace/imported orders often
  carry marketplace-side economics. `{{param.include_channel_partner_orders}}`
  (default `false`) flips them in for merchants that treat partners as revenue.

Every downstream money definition (`customer`, `repeat_customer`, and any AOV /
LTV / cohort work) selects from this view, never from `order` directly — that is
the point: one place holds the convention, disagreements get resolved by editing
one file.

Caveats:
- This is **gross** revenue truth at order grain: refunded orders normally remain
  in `Completed Order` (unless rejected after refund), so netting requires the
  order's refunded total — join back to `order` fields if netting matters.
- Stage is *current* stage; an order can regress (e.g. into a refund/reject flow)
  — counts are as-of-query-time, not immutable facts.

## Change log
- v1 (2026-07-06) — initial; convention per UltraCart DW sample queries (mining §2).
