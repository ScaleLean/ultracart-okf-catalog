---
type: "Ontology Object"
object: conversation
domain: support_conversations
tier: core
resource: "urn:ultracart:ontology:object:conversation"
version: 1
grain: "one row per conversation (chat/SMS thread) per conversation_uuid"
key:
  fields: [conversation_uuid]
  identity_family: conversation_uuid
source:
  binding: uc_conversations
  default_table: "{{source_project}}.{{dataset.medium}}.uc_conversations"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: conversation_uuid
    type: STRING
    source: conversation_uuid
    meaning: "UltraCart primary key for the conversation thread"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: channel
    type: STRING
    source: medium
    meaning: "conversation medium/channel (chat, sms, ...)"
  - name: email_hash_b64
    type: STRING
    source: "(SELECT MIN(p.email_hash) FROM UNNEST(participants) p WHERE p.email_hash IS NOT NULL)"
    refs: [participants, participants.email_hash]
    meaning: "a participant email hash (base64 sha256; see identity spine). Conversations mix customer and staff participants — treat as candidate customer identity, not guaranteed"
  - name: participant_count
    type: INTEGER
    source: "ARRAY_LENGTH(participants)"
    meaning: "number of participants (customer + agents + virtual agents)"
  - name: message_count
    type: INTEGER
    source: message_count
    meaning: "messages in the thread"
  - name: started_at
    type: DATETIME
    source: start_dts
    meaning: "when the conversation started"
  - name: last_message_at
    type: DATETIME
    source: last_message_dts
    meaning: "most recent message timestamp"
  - name: last_interactive_message_at
    type: DATETIME
    source: last_interactive_message_dts
    meaning: "most recent human (non-automated) message"
  - name: first_unresponded_at
    type: DATETIME
    source: customer_first_message_unresponded_to_dts
    meaning: "oldest customer message still awaiting a response (SLA surface)"
  - name: closed
    type: BOOLEAN
    source: closed
    meaning: "raw closed flag"
  - name: conversation_status
    type: STRING
    source: "CASE WHEN closed THEN 'closed' ELSE 'open' END"
    meaning: "derived 2-state status; the table has no closed timestamp — use last_message_at as the practical end time"
  - name: unread_messages
    type: BOOLEAN
    source: unread_messages
    meaning: "merchant-side unread flag"
  - name: sentiment
    type: STRING
    source: sentiment.sentiment
    meaning: "overall detected sentiment label"
  - name: sentiment_negative_score
    type: NUMERIC
    source: sentiment.negative
    meaning: "negative-sentiment score component (0-1)"
  - name: virtual_agent
    type: BOOLEAN
    source: virtual_agent
    meaning: "a virtual (AI) agent participated"
  - name: virtual_agent_cost
    type: NUMERIC
    source: virtual_agent_cost
    meaning: "AI agent spend attributed to this conversation"
  - name: language_iso_code
    type: STRING
    source: base_language_iso_code
    meaning: "base conversation language"
  - name: visible
    type: BOOLEAN
    source: visible
    meaning: "visible in the merchant conversation UI (false = archived/hidden)"
links:
  - to: customer
    kind: belongs_to
    on: "conversation.email_hash_b64 = customer.email_hash_b64"
pii: pseudonymous
excluded_fields: [participants, messages, last_conversation_message_body, last_conversation_participant_name, conversation_arn]
consumers: []
---

# Conversation

A chat/SMS support thread between a customer and merchant agents (human or AI).
This is the **thread** grain; individual messages live only in the excluded
`messages[]` array (bodies are hash-redacted in standard views anyway).

Channel semantics: `channel` comes from the raw `medium` column (chat, sms, ...).
There is no explicit status enum or closed timestamp in the warehouse —
`conversation_status` is derived from the `closed` flag, and `last_message_at` is
the practical end-of-conversation time.

Identity: participants carry raw email / SMS numbers next to hash twins; the
canonical view exposes only a participant `email_hash_b64` (min non-null hash
across participants). Because staff participants can also carry hashes, treat it
as a candidate customer key — join to `customer` and verify, don't assume.
`participant_count` replaces the raw participant roster.

AI economics: `virtual_agent` + `virtual_agent_cost` make this the per-thread AI
support-spend surface (PBX AI costs live on `pbx_call.financial` instead).

Gotchas:
- `participants[]` and `messages[]` are excluded arrays — they carry raw email,
  `sms_phone_number`, participant names, and message bodies.
- No merchant-independent link to `pbx_call` or `support_ticket` exists at this
  grain; phone and helpdesk are separate objects bridged via
  `pbx_call.zoho_desk_ticket_id`.

## Change log
- v1 (2026-07-06) — initial.
