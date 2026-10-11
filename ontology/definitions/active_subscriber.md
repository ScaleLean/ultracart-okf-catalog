---
type: "Ontology Definition"
definition: active_subscriber
resource: "urn:ultracart:ontology:definition:active_subscriber"
version: 1
summary: "A person (email identity) with at least one auto-order container in subscription_state 'active' — enrolled and not fully paused."
outputs:
  email_hash_b64: STRING
  active_container_count: INTEGER
  example_auto_order_oid: INTEGER
sql: |
  SELECT
    email_hash_b64,
    COUNT(*)                 AS active_container_count,
    MIN(auto_order_oid)      AS example_auto_order_oid
  FROM {{ontology}}.auto_order
  WHERE subscription_state = 'active'
    AND email_hash_b64 IS NOT NULL
  GROUP BY email_hash_b64
---

# active_subscriber

One row per **person** modeled as active: email grain
(`email_hash_b64`) over `{{ontology}}.auto_order`, keeping containers whose
canonical `subscription_state` is `'active'` — i.e. raw status `active` AND not
all items paused (the state derivation lives on the `auto_order` object; this
definition never re-implements it).

Grain matters: a person can hold several containers (multiple subscriptions,
historical merges); `active_container_count` carries that, and subscriber counts
are `COUNT(*)` over this view — never over `auto_order` directly, which counts
containers, not people.

The three subscriber pools use precedence and are **not exhaustive** over the
subscribed-ever population. People beyond the lapsed window or with unknown end
timestamps are omitted:
`active_subscriber` ∪ `paused_subscriber` ∪ `lapsed_subscriber` (a person with
both an active and a paused container is **active** — when combining pools,
precedence is active > paused > lapsed; the paused/lapsed definitions state their
own edges). Merged containers land in `ended` state on the object and never
inflate these counts. The active rule uses status and item pause aggregation,
not the exposed enabled/completed flags. Empty items and inconsistent lifecycle
states need merchant review; this update does not change that business rule.

## Change log
- v1 (2026-07-06) — initial.
