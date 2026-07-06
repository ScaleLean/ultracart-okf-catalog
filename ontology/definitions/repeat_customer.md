---
type: "Ontology Definition"
definition: repeat_customer
resource: "urn:ultracart:ontology:definition:repeat_customer"
version: 1
summary: "A customer with at least repeat_min_orders (default 2) revenue orders — the standard repeat-rate numerator."
parameters:
  - name: repeat_min_orders
    default: 2
    meaning: "minimum revenue-order count to qualify as a repeat customer; merchants with bundled first purchases sometimes raise it"
sql: |
  SELECT *
  FROM {{ontology}}.customer
  WHERE order_count >= {{param.repeat_min_orders}}
---

# repeat_customer

A filter, deliberately thin: `{{ontology}}.customer` (the canonical email-grain
buyer rollup) restricted to `order_count >= {{param.repeat_min_orders}}`
(default 2). All columns of `customer` pass through, so repeat-cohort LTV and
AOV come free.

Because `customer` is built on `revenue_order`, the count only includes real,
paid, non-test, (by default) direct-sale orders — two checkout attempts or a test
plus a real order do NOT make a repeat customer. Auto-order rebills DO count:
each successful rebill is its own revenue order, so subscribers become repeat
customers on their first rebill. If a merchant wants "repeat" to mean *chose to
buy again* rather than *was billed again*, that is a different definition (repeat
one-off buyer) to declare in their overlay — do not quietly bend this one.

The classic **repeat rate** is `COUNT(repeat_customer) / COUNT(customer)` — both
sides from this pair of views, guaranteeing numerator and denominator share the
revenue convention and identity grain.

## Change log
- v1 (2026-07-06) — initial.
