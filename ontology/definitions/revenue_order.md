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
sql: |
  SELECT *
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
