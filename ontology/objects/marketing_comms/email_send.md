---
type: "Ontology Object"
object: email_send
domain: marketing_comms
tier: core
resource: "urn:ultracart:ontology:object:email_send"
version: 1
grain: "one row per email/SMS send event to a marketing contact (per email_uuid)"
key:
  fields: [email_uuid]
  identity_family: email_uuid
source:
  binding: uc_storefront_customer_emails
  default_table: "{{source_project}}.{{dataset.medium}}.uc_storefront_customer_emails"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: email_uuid
    type: STRING
    source: email_uuid
    meaning: "per-send UUID (the send event identity)"
  - name: esp_customer_uuid
    type: STRING
    source: esp_customer_uuid
    meaning: "recipient marketing contact"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "recipient identity (base64 sha256 of normalized email; see identity spine)"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: commseq_uuid
    type: STRING
    source: commseq_uuid
    meaning: "communication sequence (flow/campaign container) that produced the send"
  - name: campaign_name
    type: STRING
    source: campaign_name
    meaning: "campaign attribution (one-shot blasts; NULL for flow sends)"
  - name: flow_name
    type: STRING
    source: flow_name
    meaning: "flow/automation attribution (triggered sends; NULL for campaign sends)"
  - name: subject
    type: STRING
    source: subject
    meaning: "subject line as sent (content, not identity — may embed personalization)"
  - name: transport
    type: STRING
    source: transport
    meaning: "delivery channel"
    enum_ref: transport
  - name: sent_at
    type: DATETIME
    source: sent_dts
    meaning: "when the send occurred (the event timestamp)"
  - name: opened
    type: BOOLEAN
    source: opened
    meaning: "recipient opened (pixel-based; undercounts image-blocking clients)"
  - name: opened_at
    type: DATETIME
    source: opened_dts
    meaning: "first open time (NULL if never opened)"
  - name: clicked
    type: BOOLEAN
    source: clicked
    meaning: "recipient clicked a tracked link"
  - name: clicked_at
    type: DATETIME
    source: clicked_dts
    meaning: "first click time (NULL if never clicked)"
  - name: converted
    type: BOOLEAN
    source: converted
    meaning: "send credited with an order (the comms-to-revenue link)"
  - name: conversion_order_id
    type: STRING
    source: order_id
    meaning: "order credited to this send (NULL unless converted)"
  - name: spam_complaint
    type: BOOLEAN
    source: spam_complaint
    meaning: "recipient reported spam — hard suppression signal"
  - name: spam_complaint_at
    type: DATETIME
    source: spam_complaint_dts
    meaning: "when the spam complaint was received (NULL if none)"
  - name: engagement_level
    type: STRING
    source: "CASE WHEN converted THEN 'converted' WHEN clicked THEN 'clicked' WHEN opened THEN 'opened' ELSE 'sent' END"
    meaning: "derived: deepest funnel stage reached by this send"
    enum_ref: engagement_level
links:
  - to: marketing_contact
    kind: belongs_to
    on: "email_send.esp_customer_uuid = marketing_contact.esp_customer_uuid"
  - to: customer
    kind: belongs_to
    on: "email_send.email_hash_b64 = customer.email_hash_b64"
  - to: order
    kind: converted_to
    on: "email_send.conversion_order_id = order.order_id"
enums:
  transport: [email, sms]
  engagement_level: [sent, opened, clicked, converted]
pii: pseudonymous
excluded_fields: [email]
consumers: []
---

# EmailSend

One **send event**: a single email (or SMS — see `transport`) delivered to one
marketing contact, with its engagement outcomes (open, click, conversion, spam
complaint) and its attribution (`campaign_name` for one-shot blasts, `flow_name` for
triggered automations, `commseq_uuid` for the underlying communication sequence).
The layer-1 doc labels the grain "email membership row"; operationally each row is a
send, identified by `email_uuid` (`esp_customer_uuid + sent_dts` is the effective
natural key if you ever need to dedupe).

`converted` + `conversion_order_id` make this **the** comms→revenue join: revenue per
flow/campaign is `email_send → order` on `conversion_order_id`. Treat it as UltraCart's
attribution opinion (last-touch style), not ground truth — cross-check against order
UTMs when it matters.

Gotchas:
- Email engagement also lives in `uc_orders.emails[]` and `uc_auto_orders.emails[]`;
  those are denormalized snapshots. **This object is the canonical per-send
  engagement surface** — never union or sum across the three surfaces.
- `opened` is pixel-based and undercounts (image-blocking, Apple MPP inflates in the
  other direction); prefer `clicked`/`converted` for decisions.
- Exactly one of `campaign_name`/`flow_name` is normally populated; group by
  `COALESCE(flow_name, campaign_name)` for a single program dimension.
- Enum casing for `transport` should be verified per merchant before filtering.
- Raw recipient `email` exists in permissive tiers and is excluded; `subject` is kept
  (needed for program analysis) but may contain personalization — treat as
  quasi-identifying content downstream.

## Change log
- v1 (2026-07-06) — initial.
