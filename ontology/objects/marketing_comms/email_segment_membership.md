---
type: "Ontology Object"
object: email_segment_membership
domain: marketing_comms
tier: supporting
resource: "urn:ultracart:ontology:object:email_segment_membership"
version: 1
grain: "one row per current (segment, marketing contact) membership"
key:
  fields: [segment_uuid, esp_customer_uuid]
  identity_family: esp_customer_uuid
source:
  binding: uc_storefront_customer_segments
  default_table: "{{source_project}}.{{dataset.medium}}.uc_storefront_customer_segments"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: segment_uuid
    type: STRING
    source: segment_uuid
    meaning: "ESP segment identifier"
  - name: segment_name
    type: STRING
    source: segment_name
    meaning: "human-facing segment name (names can be renamed; uuid is stable)"
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
    source: "CONCAT(segment_uuid, ':', esp_customer_uuid)"
    meaning: "derived: single-column surrogate for the composite key"
  - name: added_at
    type: DATETIME
    source: add_dts
    meaning: "when the contact entered the segment (the only timestamp this table has)"
  - name: added_date
    type: DATE
    source: "DATE(add_dts)"
    meaning: "entry date, for cohorting"
  - name: days_since_added
    type: INTEGER
    source: "DATE_DIFF(CURRENT_DATE(), DATE(add_dts), DAY)"
    meaning: "derived: time in segment in days (as of query time)"
  - name: is_member
    type: BOOLEAN
    source: "TRUE"
    meaning: "always true — row presence IS current membership; exits leave no row here (see prose)"
links:
  - to: marketing_contact
    kind: belongs_to
    on: "email_segment_membership.esp_customer_uuid = marketing_contact.esp_customer_uuid"
  - to: customer
    kind: belongs_to
    on: "email_segment_membership.email_hash_b64 = customer.email_hash_b64"
pii: pseudonymous
excluded_fields: [email]
consumers: []
---

# EmailSegmentMembership

Link table: which marketing contacts are **currently** in which ESP segments.
Structural mirror of `email_list_membership`, with one semantic difference: segments
are **rule-computed, dynamic** audiences (the ESP re-evaluates criteria and moves
contacts in and out), whereas lists are explicit/managed. That makes segment
membership even more volatile — `added_at` is the *latest* entry the current state
knows about, not necessarily the first time the contact ever qualified.

**Current-state only — no exit timing.** Only `add_dts` exists here; when a contact
falls out of a segment the row vanishes from the current-state view. The **streaming
twin (`uc_storefront_customer_segment_streaming`) is the only source of segment-exit
*timing*** — `IsDelete` + `RecordTime` is the exit event. Segment flow analysis
(entries/exits over time, dwell time in a segment) requires the streaming twin; this
object answers only "who is in it now".

Gotchas:
- Segment membership is targeting, not consent — intersect with
  `marketing_contact.is_emailable` before counting a sendable audience.
- `uc_storefront_customers.segments[]` embeds the same memberships; this object is
  the canonical surface (`marketing_contact.segment_count` should reconcile).
- Because segments are dynamic, never treat a snapshot of this table as a historical
  audience for a past send — the membership at send time is unrecoverable from the
  base table.

## Change log
- v1 (2026-07-06) — initial.
