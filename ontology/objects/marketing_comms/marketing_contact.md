---
type: "Ontology Object"
object: marketing_contact
domain: marketing_comms
tier: core
resource: "urn:ultracart:ontology:object:marketing_contact"
version: 1
grain: "one row per marketing-audience person (ESP customer profile, per esp_customer_uuid)"
key:
  fields: [esp_customer_uuid]
  identity_family: esp_customer_uuid
source:
  binding: uc_storefront_customers
  default_table: "{{source_project}}.{{dataset.medium}}.uc_storefront_customers"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: esp_customer_uuid
    type: STRING
    source: esp_customer_uuid
    meaning: "ESP (StoreFront Communications) customer UUID — the marketing-audience spine key"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "customer identity (base64 sha256 of normalized email; see identity spine); effectively unique per merchant here"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: global_unsubscribed
    type: BOOLEAN
    source: global_unsubscribed
    meaning: "person-level opt-out across ALL lists/flows/campaigns for this merchant"
  - name: is_emailable
    type: BOOLEAN
    source: "NOT global_unsubscribed"
    meaning: "derived: may currently be sent marketing email (consent surface for audience counts)"
  - name: consecutive_emails_unopened
    type: INTEGER
    source: consecutive_emails_unopened
    meaning: "deliverability decay counter: sends in a row without an open"
  - name: consecutive_emails_unclicked
    type: INTEGER
    source: consecutive_emails_unclicked
    meaning: "deliverability decay counter: sends in a row without a click"
  - name: email_send_count
    type: INTEGER
    source: "ARRAY_LENGTH(emails)"
    meaning: "lifetime sends to this person (rollup of the embedded emails[] array)"
  - name: emails_opened_count
    type: INTEGER
    source: "(SELECT COUNTIF(emails.opened) FROM UNNEST(emails) AS emails)"
    meaning: "lifetime sends opened"
  - name: emails_clicked_count
    type: INTEGER
    source: "(SELECT COUNTIF(emails.clicked) FROM UNNEST(emails) AS emails)"
    meaning: "lifetime sends clicked"
  - name: emails_converted_count
    type: INTEGER
    source: "(SELECT COUNTIF(emails.converted) FROM UNNEST(emails) AS emails)"
    meaning: "lifetime sends credited with an order conversion"
  - name: spam_complaint_count
    type: INTEGER
    source: "(SELECT COUNTIF(emails.spam_complaint) FROM UNNEST(emails) AS emails)"
    meaning: "lifetime spam complaints (any > 0 is a suppression signal)"
  - name: last_email_sent_at
    type: DATETIME
    source: "(SELECT MAX(emails.sent_dts) FROM UNNEST(emails) AS emails)"
    meaning: "most recent send"
  - name: last_email_opened_at
    type: DATETIME
    source: "(SELECT MAX(emails.opened_dts) FROM UNNEST(emails) AS emails)"
    meaning: "most recent open (engagement recency)"
  - name: last_email_clicked_at
    type: DATETIME
    source: "(SELECT MAX(emails.clicked_dts) FROM UNNEST(emails) AS emails)"
    meaning: "most recent click"
  - name: list_count
    type: INTEGER
    source: "ARRAY_LENGTH(lists)"
    meaning: "current list memberships (detail in email_list_membership)"
  - name: segment_count
    type: INTEGER
    source: "ARRAY_LENGTH(segments)"
    meaning: "current segment memberships (detail in email_segment_membership)"
  - name: session_count
    type: INTEGER
    source: "ARRAY_LENGTH(sessions)"
    meaning: "ESP-tracked site sessions for this person"
  - name: last_session_at
    type: DATETIME
    source: "(SELECT MAX(sessions.start_dts) FROM UNNEST(sessions) AS sessions)"
    meaning: "most recent ESP-tracked site visit"
links:
  - to: customer
    kind: same_person_as
    on: "marketing_contact.email_hash_b64 = customer.email_hash_b64"
  - to: email_send
    kind: has_many
    on: "marketing_contact.esp_customer_uuid = email_send.esp_customer_uuid"
  - to: email_list_membership
    kind: has_many
    on: "marketing_contact.esp_customer_uuid = email_list_membership.esp_customer_uuid"
  - to: email_segment_membership
    kind: has_many
    on: "marketing_contact.esp_customer_uuid = email_segment_membership.esp_customer_uuid"
pii: pseudonymous
excluded_fields: [email, emails, lists, segments, sessions]
consumers: []
---

# MarketingContact

The **marketing-audience person**: one row per ESP customer profile
(`esp_customer_uuid`), carrying consent state, deliverability counters, and lifetime
engagement rollups. This is who you may email, whether they still engage, and how
big your real audience is. It is distinct from `customer` (registered commerce
profile) and from mere buyers — a marketing contact may have never ordered, and a
buyer may have no ESP profile.

Consent semantics: `global_unsubscribed` is the person-level kill switch across every
list, flow, and campaign for the merchant; `is_emailable` is its derived positive.
List/segment membership (see the membership objects) is *targeting*, not consent —
leaving a list does not flip `global_unsubscribed`, and a globally-unsubscribed
contact can still appear in lists/segments. `consecutive_emails_unopened/_unclicked`
are the ESP's deliverability decay counters — sunset-policy candidates before they
become spam complaints.

Gotchas:
- Email engagement events also live in `uc_orders.emails[]` and
  `uc_auto_orders.emails[]` — those are convenience snapshots. **This object (and
  `email_send` at the per-send grain) is the canonical engagement surface**; do not
  sum engagement across the three or you will double-count.
- The giant nested arrays (`emails[]`, `lists[]`, `segments[]`, `sessions[]`) are
  excluded from the canonical view; they duplicate the four sibling tables and carry
  raw email in permissive tiers. Only scalar rollups over them are exposed here.
- `email_hash_b64` is effectively unique per merchant, but `esp_customer_uuid` is the
  key — use the hash only to bridge to commerce objects (`customer`, `order`).

## Change log
- v1 (2026-07-06) — initial.
