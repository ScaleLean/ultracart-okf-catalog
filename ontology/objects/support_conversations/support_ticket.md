---
type: "Ontology Object"
object: support_ticket
domain: support_conversations
tier: core
resource: "urn:ultracart:ontology:object:support_ticket"
version: 1
grain: "one row per Zoho Desk helpdesk ticket per id"
key:
  fields: [ticket_id]
  identity_family: zoho_desk_ticket_id
source:
  binding: uc_zoho_desk_tickets
  default_table: "{{source_project}}.{{dataset.medium}}.uc_zoho_desk_tickets"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: ticket_id
    type: STRING
    source: id
    meaning: "Zoho Desk ticket id (system key; = pbx_call.zoho_desk_ticket_id)"
  - name: ticket_number
    type: STRING
    source: ticket_number
    meaning: "human-facing ticket number"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "requester identity (base64 sha256 of normalized email; see identity spine)"
  - name: status
    type: STRING
    source: status
    meaning: "raw Zoho status (merchant-configurable values)"
  - name: status_type
    type: STRING
    source: status_type
    meaning: "Zoho status family (Open/On Hold/Closed) — the stable lifecycle field"
  - name: channel
    type: STRING
    source: channel
    meaning: "intake channel (Email, Phone, Web, Chat, ...)"
  - name: subject_hash
    type: STRING
    source: subject_hash
    meaning: "hashed subject line (raw subject exists only in permissive tiers; excluded)"
  - name: priority
    type: STRING
    source: priority
    meaning: "ticket priority"
  - name: category
    type: STRING
    source: category
    meaning: "merchant-defined category"
  - name: sub_category
    type: STRING
    source: sub_category
    meaning: "merchant-defined sub-category"
  - name: classification
    type: STRING
    source: classification
    meaning: "Zoho classification (Question/Problem/Feature/Others)"
  - name: sentiment
    type: STRING
    source: sentiment
    meaning: "detected sentiment label"
  - name: created_at
    type: DATETIME
    source: created_time
    meaning: "ticket created"
  - name: closed_at
    type: DATETIME
    source: closed_time
    meaning: "ticket closed (NULL if open)"
  - name: modified_at
    type: DATETIME
    source: modified_time
    meaning: "last modification"
  - name: due_at
    type: DATETIME
    source: due_date
    meaning: "SLA resolution due date"
  - name: response_due_at
    type: DATETIME
    source: response_due_date
    meaning: "SLA first/next-response due date"
  - name: is_escalated
    type: BOOLEAN
    source: is_escalated
    meaning: "SLA-escalated"
  - name: is_overdue
    type: BOOLEAN
    source: is_over_due
    meaning: "past resolution due date"
  - name: is_spam
    type: BOOLEAN
    source: is_spam
    meaning: "marked spam — exclude from support KPIs"
  - name: assignee_id
    type: STRING
    source: assignee_id
    meaning: "assigned agent id (names/emails excluded; staff dimension key only)"
  - name: department_name
    type: STRING
    source: department.name
    meaning: "owning department"
  - name: thread_count
    type: INTEGER
    source: "SAFE_CAST(thread_count AS INT64)"
    meaning: "email threads on the ticket (stored as STRING upstream)"
  - name: comment_count
    type: INTEGER
    source: "SAFE_CAST(comment_count AS INT64)"
    meaning: "internal comments on the ticket (stored as STRING upstream)"
links:
  - to: customer
    kind: belongs_to
    on: "support_ticket.email_hash_b64 = customer.email_hash_b64"
  - to: pbx_call
    kind: has_many
    on: "support_ticket.ticket_id = pbx_call.zoho_desk_ticket_id"
pii: pseudonymous
excluded_fields: [contact, secondary_contacts, assignee, threads, comments, attachments, description, resolution, subject, email, phone, cf, custom_fields, channel_related_info]
consumers: []
---

# SupportTicket

Mirror of a Zoho Desk helpdesk ticket — the system-of-record grain for support
workload, SLA, and resolution reporting. Phone calls that spawn or attach to a
ticket point here via `pbx_call.zoho_desk_ticket_id = ticket_id`, making this
object the hub of the cross-channel support journey.

Two keys: `ticket_id` (Zoho system id, the join key) and `ticket_number` (what
humans quote in email subjects). Always join on `ticket_id`.

Lifecycle: `status` values are merchant-configurable in Zoho; use `status_type`
(Open / On Hold / Closed) for stable lifecycle logic and `closed_at` for
resolution timing. SLA surface: `due_at`, `response_due_at`, `is_overdue`,
`is_escalated`. Filter `is_spam` out of any KPI.

Content redaction: `subject`, `description`, `resolution`, threads and comments
are hash-redacted in standard views — the canonical view carries `subject_hash`
only, and the raw text columns (appended for permissive tiers) are excluded.

Gotchas:
- Zoho serializes several counters as STRING (`thread_count`, `comment_count`,
  `approval_count`…) — the canonical view SAFE_CASTs the two useful ones.
- `contact` / `secondary_contacts` structs carry names, emails, phones (with
  hash twins); the scalar `email_hash` covers the requester spine, so the whole
  structs are excluded.
- `assignee_id` is kept as an opaque staff key; the assignee struct (names,
  emails) is excluded.

## Change log
- v1 (2026-07-06) — initial.
