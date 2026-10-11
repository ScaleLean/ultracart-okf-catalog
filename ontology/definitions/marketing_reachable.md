---
type: "Ontology Definition"
definition: marketing_reachable
resource: "urn:ultracart:ontology:definition:marketing_reachable"
version: 1
summary: "Modeled suppression eligibility: contacts not globally unsubscribed, excluding recorded spam complainers; no affirmative consent guarantee."
outputs:
  esp_customer_uuid: STRING
  email_hash_b64: STRING
  merchant_id: STRING
  global_unsubscribed: BOOLEAN
  is_emailable: BOOLEAN
  consecutive_emails_unopened: INTEGER
  consecutive_emails_unclicked: INTEGER
  email_send_count: INTEGER
  emails_opened_count: INTEGER
  emails_clicked_count: INTEGER
  emails_converted_count: INTEGER
  spam_complaint_count: INTEGER
  last_email_sent_at: DATETIME
  last_email_opened_at: DATETIME
  last_email_clicked_at: DATETIME
  list_count: INTEGER
  segment_count: INTEGER
  session_count: INTEGER
  last_session_at: DATETIME
sql: |
  SELECT
    mc.esp_customer_uuid,
    mc.email_hash_b64,
    mc.merchant_id,
    mc.global_unsubscribed,
    mc.is_emailable,
    mc.consecutive_emails_unopened,
    mc.consecutive_emails_unclicked,
    mc.email_send_count,
    mc.emails_opened_count,
    mc.emails_clicked_count,
    mc.emails_converted_count,
    mc.spam_complaint_count,
    mc.last_email_sent_at,
    mc.last_email_opened_at,
    mc.last_email_clicked_at,
    mc.list_count,
    mc.segment_count,
    mc.session_count,
    mc.last_session_at
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

A modeled suppression filter over `marketing_contact`: `is_emailable` is true
and no recorded `email_send.spam_complaint` exists for the ESP profile.
Absence of suppression is not affirmative consent, legal sendability, verified
deliverability or authorization for any action. Unknown/null eligibility is
excluded by SQL's WHERE semantics. Missing complaint events may affect coverage.

The grain remains `esp_customer_uuid`, per storefront ESP profile, rather than a
unique human across storefronts. Engagement and transactional email are separate
concerns. Merchants must apply their approved consent and send-time policies;
this change preserves the existing SQL suppression policy.

## Change log
- v1 (2026-07-06) — initial.
