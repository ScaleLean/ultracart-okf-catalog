---
type: "Ontology Definition"
definition: marketing_reachable
resource: "urn:ultracart:ontology:definition:marketing_reachable"
version: 1
summary: "Contacts a merchant may actually email marketing to: positive consent state (not globally unsubscribed) minus anyone who has ever filed a spam complaint."
sql: |
  SELECT mc.*
  FROM {{ontology}}.marketing_contact AS mc
  LEFT JOIN (
    SELECT DISTINCT esp_customer_uuid
    FROM {{ontology}}.email_send
    WHERE spam_complaint
  ) AS complainers
    ON mc.esp_customer_uuid = complainers.esp_customer_uuid
  WHERE mc.is_emailable
    AND complainers.esp_customer_uuid IS NULL
---

# marketing_reachable

The honest audience size: who may **actually** be sent marketing email. Two
subtractions from the marketing-contact population:

1. **Consent**: `marketing_contact.is_emailable` — the derived positive of the
   person-level `global_unsubscribed` kill switch. List/segment membership is
   targeting, not consent, and does not appear here.
2. **Spam complainers**: anyone with a `spam_complaint` on any send in
   `{{ontology}}.email_send` — ever. A complaint is a hard suppression signal
   even when the ESP still shows the contact as emailable: mailing complainers
   again is how sending domains die. (`marketing_contact.spam_complaint_count`
   is the rollup of the same events; the join to `email_send` keeps this
   definition anchored to the event-grain source of truth.)

Uses:
- **Audience denominator** for open/click rates that mean something.
- **Pre-flight gate** for the send-side actions: `send_campaign` audience checks
  and any flow enrollment should intersect with this view.
- Reachability ≠ engagement: a contact ignored for two years
  (`consecutive_emails_unopened` high) is reachable but a sunset-policy
  candidate — engagement tiers are a separate (overlay) definition.

Edges: contacts are per-storefront ESP profiles (`esp_customer_uuid` grain, same
as `marketing_contact`); the same human under two storefronts is two rows, which
is correct for send-planning. Transactional email (receipts) is out of scope —
that surface ignores marketing consent by design.

## Change log
- v1 (2026-07-06) — initial.
