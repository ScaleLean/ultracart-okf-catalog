---
type: "Ontology Definition"
definition: paused_subscriber
resource: "urn:ultracart:ontology:definition:paused_subscriber"
version: 1
summary: "A person whose subscription relationship is suspended but not ended: at least one auto-order container in subscription_state 'paused', and none active."
sql: |
  SELECT
    email_hash_b64,
    COUNTIF(subscription_state = 'paused')  AS paused_container_count,
    MIN(auto_order_oid)                     AS example_auto_order_oid
  FROM {{ontology}}.auto_order
  WHERE email_hash_b64 IS NOT NULL
  GROUP BY email_hash_b64
  HAVING COUNTIF(subscription_state = 'paused') > 0
     AND COUNTIF(subscription_state = 'active') = 0
---

# paused_subscriber

The middle pool: people whose subscription is suspended — **neither active nor
lapsed**. Email grain over `{{ontology}}.auto_order`, requiring at least one
container in `subscription_state = 'paused'` and no active container (a person
with any active container belongs to `active_subscriber`; precedence
active > paused > lapsed).

**Pause semantics are item-level.** UltraCart has no container pause flag: a
"paused subscription" is an `active`-status container in which **every item** has
`paused = true` (`auto_order.all_items_paused` → `subscription_state = 'paused'`;
per-item pause detail lives on `auto_order_item.paused`). A container with one
paused and one billing item is *active*, correctly.

Why the pool is worth naming: paused subscribers still have a standing
relationship and a payment method on file — they are reactivation targets
(`resume_auto_order_item` action), not churn. At one observed merchant the paused
pool was **2× the active pool**; folding it into either neighbor materially
misstates both retention and churn. Watch containers that sit paused with a
long-past `next_shipment_dts` — resuming those has a billing hazard (see the
resume action file).

## Change log
- v1 (2026-07-06) — initial.
