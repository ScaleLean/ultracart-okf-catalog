---
type: "Ontology Object"
object: email_list_membership
domain: marketing_comms
tier: supporting
resource: "urn:ultracart:ontology:object:email_list_membership"
version: 1
grain: "one row per current (list, marketing contact) membership"
key:
  fields: [list_uuid, esp_customer_uuid]
  identity_family: esp_customer_uuid
source:
  binding: uc_storefront_customer_lists
  default_table: "{{source_project}}.{{dataset.medium}}.uc_storefront_customer_lists"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: list_uuid
    type: STRING
    source: list_uuid
    meaning: "ESP list identifier"
  - name: list_name
    type: STRING
    source: list_name
    meaning: "human-facing list name (names can be renamed; uuid is stable)"
  - name: esp_customer_uuid
    type: STRING
    source: esp_customer_uuid
    meaning: "member marketing contact"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "member identity (base64 sha256 of normalized email; see identity spine)"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: membership_key
    type: STRING
    source: "CONCAT(list_uuid, ':', esp_customer_uuid)"
    meaning: "derived: single-column surrogate for the composite key"
  - name: added_at
    type: DATETIME
    source: add_dts
    meaning: "when the contact joined the list (the only timestamp this table has)"
  - name: added_date
    type: DATE
    source: "DATE(add_dts)"
    meaning: "join date, for signup cohorting"
  - name: days_since_added
    type: INTEGER
    source: "DATE_DIFF(CURRENT_DATE(), DATE(add_dts), DAY)"
    meaning: "derived: membership tenure in days (as of query time)"
  - name: is_member
    type: BOOLEAN
    source: "TRUE"
    meaning: "always true — row presence IS current membership; exits leave no row here (see prose)"
links:
  - to: marketing_contact
    kind: belongs_to
    on: "email_list_membership.esp_customer_uuid = marketing_contact.esp_customer_uuid"
  - to: customer
    kind: belongs_to
    on: "email_list_membership.email_hash_b64 = customer.email_hash_b64"
pii: pseudonymous
excluded_fields: [email]
consumers: []
---

# EmailListMembership

Link table: which marketing contacts are **currently** on which ESP email lists,
and when they joined. Lists are explicit opt-in/managed audiences (vs `segments`,
which are rule-computed — see `email_segment_membership` for the mirror pattern).

**Current-state only — no exit timing.** The base table carries `add_dts` and nothing
else: when a contact unsubscribes from a list (or is removed), the row simply
disappears from the current-state view. The **streaming twin
(`uc_storefront_customer_list_streaming`) is the only source of unsubscribe/exit
*timing*** — its `IsDelete` marker plus `RecordTime` is the removal event. If you need
list churn, unsubscribe curves, or "was on list X as of date D", you must model the
streaming twin; this object can only tell you who is on the list *now* and how long
they have been on it.

Gotchas:
- List membership is targeting, not consent: a member here can still be
  `global_unsubscribed` on `marketing_contact` — always intersect with
  `is_emailable` before counting a sendable audience.
- `uc_storefront_customers.lists[]` embeds the same memberships; this object is the
  canonical membership surface (and `marketing_contact.list_count` should equal the
  row count here per contact).
- Join lists to sends by program name, not key: sends carry
  `campaign_name`/`flow_name`, not `list_uuid`.

## Change log
- v1 (2026-07-06) — initial.
