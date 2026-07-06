---
type: "Ontology Definition"
definition: customer
resource: "urn:ultracart:ontology:definition:customer"
version: 1
summary: "THE canonical customer: every buyer, at email-identity grain — a rollup of revenue orders per email_hash_b64 with first/last order, count, lifetime total, and recency."
sql: |
  SELECT
    email_hash_b64,
    MIN(order_date)                                                  AS first_order_date,
    MAX(order_date)                                                  AS last_order_date,
    COUNT(*)                                                         AS order_count,
    SUM(total)                                                       AS lifetime_total,
    AVG(total)                                                       AS avg_order_value,
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY)                  AS days_since_last_order,
    ARRAY_AGG(order_id ORDER BY order_ts ASC  LIMIT 1)[SAFE_OFFSET(0)] AS first_order_id,
    ARRAY_AGG(order_id ORDER BY order_ts DESC LIMIT 1)[SAFE_OFFSET(0)] AS last_order_id
  FROM {{ontology}}.revenue_order
  WHERE email_hash_b64 IS NOT NULL
  GROUP BY email_hash_b64
---

# customer

**The** canonical answer to "how many customers do we have": one row per buyer,
where a buyer is an email identity (`email_hash_b64`, see
`identity/identity_spine.md`) with at least one **revenue order**. Built over
`{{ontology}}.revenue_order`, so the revenue-truth convention (paid, real stage,
non-test, direct-sale by default) is inherited, not restated.

This follows UltraCart's own DW practice: their LTV and repeat-rate queries key on
**order billing email hash**, not on registered accounts. A **registered account
is `customer_profile`** (keyed `customer_profile_oid` — login, stored cards,
address books); most buyers never register, so profile counts undercount
customers badly. When someone asks "customers," this definition is the source of
truth; when they ask "accounts," point them at `customer_profile`.

Column notes:
- `lifetime_total` / `avg_order_value` are **gross** (see `revenue_order` — netting
  refunds requires the refunded totals).
- `first_order_id` / `last_order_id` use the `ARRAY_AGG … ORDER BY order_ts …
  LIMIT 1` pattern (ties broken arbitrarily but deterministically enough for
  reporting; `order_ts` is the timestamp, `order_date` the date).
- `days_since_last_order` is computed at query time — this compiles to a view, so
  recency is always current.
- Rows with a NULL email hash (rare imports) are excluded — they cannot be a
  customer identity.

Consumers: `repeat_customer` selects from this view; marketing objects bridge to
it via `email_hash_b64` (`marketing_contact.same_person_as`).

## Change log
- v1 (2026-07-06) — initial.
