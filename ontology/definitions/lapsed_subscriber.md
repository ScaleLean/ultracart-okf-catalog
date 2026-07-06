---
type: "Ontology Definition"
definition: lapsed_subscriber
resource: "urn:ultracart:ontology:definition:lapsed_subscriber"
version: 1
summary: "A former subscriber: no live (active or paused) auto-order container, with the most recent container ending within the lapsed window (default 730 days)."
parameters:
  - name: lapsed_window_days
    default: 730
    meaning: "how far back an ended subscription still counts as 'lapsed' (reactivation-relevant) rather than gone; beyond it the person ages out of the pool"
sql: |
  WITH per_email AS (
    SELECT
      email_hash_b64,
      COUNTIF(subscription_state IN ('active', 'paused')) AS live_container_count,
      MAX(ended_at)                                       AS last_ended_at
    FROM {{ontology}}.auto_order
    WHERE email_hash_b64 IS NOT NULL
    GROUP BY email_hash_b64
  )
  SELECT
    email_hash_b64,
    last_ended_at,
    DATE_DIFF(CURRENT_DATE(), DATE(last_ended_at), DAY) AS days_since_ended
  FROM per_email
  WHERE live_container_count = 0
    AND last_ended_at IS NOT NULL
    AND DATE(last_ended_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL {{param.lapsed_window_days}} DAY)
---

# lapsed_subscriber

The reactivation pool: people who **had** a subscription and now have nothing
live. Email grain via a `WITH` over `{{ontology}}.auto_order`: zero containers in
a live state (`active` or `paused` — a paused person is `paused_subscriber`, not
lapsed), and the most recent ending (`MAX(ended_at)` — the object's canonical end
timestamp across cancel / disable / merge) inside the last
`{{param.lapsed_window_days}}` days (default **730** — two years).

Edges worth knowing:
- The window makes this an **actionable** pool, not an archive: someone whose
  last subscription ended six years ago is a cold prospect, not a lapsed
  subscriber. Merchants tune the parameter to their product cycle.
- `ended_at` covers all three endings: customer/merchant cancel (`canceled_dts`),
  system disable after failed rebills (`disabled_dts` — dunning exhaustion, a
  very different churn story), and merges. Merged containers usually belong to a
  person who still has the surviving container — the `live_container_count = 0`
  gate handles that correctly.
- People with an ended container but `last_ended_at` NULL (data edge) are
  excluded rather than guessed at.
- Win-back targeting must still cross `marketing_reachable` — lapsed and
  globally-unsubscribed is a person you may NOT email.

## Change log
- v1 (2026-07-06) — initial.
