---
type: "Ontology Object"
object: pbx_call
domain: support_conversations
tier: supporting
resource: "urn:ultracart:ontology:object:pbx_call"
version: 1
grain: "one row per PBX phone call per call_uuid"
key:
  fields: [call_uuid]
  identity_family: call_uuid
source:
  binding: uc_conversation_pbx_calls
  default_table: "{{source_project}}.{{dataset.medium}}.uc_conversation_pbx_calls"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: call_uuid
    type: STRING
    source: call_uuid
    meaning: "UltraCart primary key for the call"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "matched customer identity (base64 sha256 of normalized email; see identity spine)"
  - name: customer_profile_oid
    type: STRING
    source: customer_profile_oid
    meaning: "matched registered customer profile — STRING in this table (INTEGER elsewhere); SAFE_CAST before joining"
  - name: direction
    type: STRING
    source: routing.direction
    meaning: "inbound | outbound"
  - name: call_type
    type: STRING
    source: routing.call_type
    meaning: "routing call type"
  - name: queue_name
    type: STRING
    source: routing.queue.queue_name
    meaning: "queue the call landed in"
  - name: status
    type: STRING
    source: status
    meaning: "raw call status"
  - name: disposition
    type: STRING
    source: disposition
    meaning: "agent-recorded call outcome"
  - name: started_at
    type: DATETIME
    source: timeline.created_dts
    meaning: "call start"
  - name: answered_at
    type: DATETIME
    source: timeline.answer_dts
    meaning: "when answered (NULL = never answered)"
  - name: ended_at
    type: DATETIME
    source: timeline.end_dts
    meaning: "call end"
  - name: queue_wait_seconds
    type: INTEGER
    source: timeline.queue_wait_seconds
    meaning: "seconds waiting in queue"
  - name: talk_time_seconds
    type: INTEGER
    source: timeline.talk_time_seconds
    meaning: "seconds of actual conversation"
  - name: total_duration_seconds
    type: INTEGER
    source: timeline.total_duration_seconds
    meaning: "total call duration"
  - name: agent_count
    type: INTEGER
    source: "ARRAY_LENGTH(agents)"
    meaning: "human agents who joined the call"
  - name: hold_count
    type: INTEGER
    source: "ARRAY_LENGTH(holds)"
    meaning: "number of holds"
  - name: transfer_count
    type: INTEGER
    source: "ARRAY_LENGTH(transfers)"
    meaning: "number of transfers"
  - name: caller_phone_hash
    type: STRING
    source: caller.phone_number_hash
    meaning: "hashed caller phone number (raw twin excluded)"
  - name: caller_state
    type: STRING
    source: caller.state
    meaning: "coarse caller geo (state)"
  - name: caller_country
    type: STRING
    source: caller.country
    meaning: "coarse caller geo (country)"
  - name: ai_call_category
    type: STRING
    source: ai_summary.call_category
    meaning: "AI-classified call category"
  - name: ai_sentiment
    type: STRING
    source: ai_summary.sentiment
    meaning: "AI-detected sentiment of the call"
  - name: call_price
    type: NUMERIC
    source: financial.call_price
    meaning: "telephony cost of the call"
  - name: ai_agent_cost
    type: NUMERIC
    source: financial.ai_agent_cost
    meaning: "AI agent cost on this call"
  - name: zoho_desk_ticket_id
    type: STRING
    source: zoho_desk_ticket_id
    meaning: "Zoho Desk ticket created/linked for this call — the phone↔helpdesk bridge (= support_ticket.ticket_id)"
links:
  - to: support_ticket
    kind: belongs_to
    on: "pbx_call.zoho_desk_ticket_id = support_ticket.ticket_id"
  - to: customer
    kind: belongs_to
    on: "pbx_call.email_hash_b64 = customer.email_hash_b64"
pii: pseudonymous
excluded_fields: [caller.caller_id, caller.phone_number, customer_name, email, notes, recordings, recording_sids, agents, transfers, holds, ai_agent_engagements, ai_summary.summary, ai_summary.action_items, ai_summary.key_topics]
consumers: []
---

# PbxCall

One phone call through the UltraCart PBX: routing, queue wait, talk time,
holds/transfers, AI summary classification, and cost. This is the phone channel
of the support domain (chat/SMS live on `conversation`, helpdesk on
`support_ticket`).

**The bridge that matters:** `zoho_desk_ticket_id` equals
`support_ticket.ticket_id` (`uc_zoho_desk_tickets.id`). It is the ONLY key that
connects the phone channel to the helpdesk — chat conversations have no such
bridge. Call→ticket→email_hash lets you stitch a customer's full support
journey across phone and helpdesk, and both sides also carry `email_hash`
directly for the customer spine.

Timing: `queue_wait_seconds` + `talk_time_seconds` vs `total_duration_seconds`
give the service-level picture; `answered_at IS NULL` identifies abandoned
calls.

Gotchas:
- `customer_profile_oid` is a STRING here (INTEGER on `uc_customers`) —
  `SAFE_CAST(... AS INT64)` before joining a customer-profile object.
- Recordings, transcripts, agent rosters, raw caller numbers, free-text notes
  and the AI summary text are excluded — transcript segments are hash-redacted
  in standard views but still bulky and staff-identifying.
- Per-call AI spend: `ai_agent_cost` (agent minutes) is separate from
  `financial.ai_summary_cost`/transcription costs; `call_price` is telephony.

## Change log
- v1 (2026-07-06) — initial.
