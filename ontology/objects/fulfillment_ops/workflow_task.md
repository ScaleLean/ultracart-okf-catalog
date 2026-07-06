---
type: "Ontology Object"
object: workflow_task
domain: fulfillment_ops
tier: supporting
resource: "urn:ultracart:ontology:object:workflow_task"
version: 1
grain: "one row per workflow task"
key:
  fields: [workflow_task_uuid]
  identity_family: workflow_task_uuid
source:
  binding: uc_workflow_tasks
  default_table: "{{source_project}}.{{dataset.medium}}.uc_workflow_tasks"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: workflow_task_uuid
    type: STRING
    source: workflow_task_uuid
    meaning: "UltraCart primary key for the task"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: global_task_number
    type: INTEGER
    source: global_task_number
    meaning: "human-facing task number across the merchant account"
  - name: object_task_number
    type: INTEGER
    source: object_task_number
    meaning: "sequence of this task within its linked object"
  - name: task_name
    type: STRING
    source: task_name
    meaning: "task title"
  - name: task_context
    type: STRING
    source: task_context
    meaning: "context/category the task was raised in"
  - name: task_details
    type: STRING
    source: task_details
    meaning: "free-text task body (merchant-authored; may mention customers — see prose)"
  - name: system_task_type
    type: STRING
    source: system_task_type
    meaning: "type code for system-generated tasks (NULL for manual tasks)"
  - name: status
    type: STRING
    source: status
    meaning: "raw task status (source enum, not normalized here)"
  - name: priority
    type: STRING
    source: priority
    meaning: "raw task priority"
  - name: assigned_to_user
    type: STRING
    source: assigned_to_user
    meaning: "assigned staff username"
  - name: assigned_to_group
    type: STRING
    source: assigned_to_group
    meaning: "assigned staff group"
  - name: assigned_to_user_or_group
    type: STRING
    source: assigned_to_user_or_group
    meaning: "convenience assignee (user if set, else group)"
  - name: created_by_user
    type: STRING
    source: created_by.user
    meaning: "staff username (or system) that created the task"
  - name: created_at
    type: DATETIME
    source: created_dts
    meaning: "task creation timestamp"
  - name: due_at
    type: DATETIME
    source: due_dts
    meaning: "due date"
  - name: delay_until_at
    type: DATETIME
    source: delay_until_dts
    meaning: "snoozed/hidden until this timestamp"
  - name: expires_at
    type: DATETIME
    source: expiration_dts
    meaning: "task auto-expires at this timestamp"
  - name: last_updated_at
    type: DATETIME
    source: last_update_dts
    meaning: "last modification timestamp"
  - name: object_type
    type: STRING
    source: object_type
    meaning: "type of the linked business object (order, auto order, item…)"
  - name: object_id
    type: STRING
    source: object_id
    meaning: "identifier of the linked object, interpreted per object_type"
  - name: object_url
    type: STRING
    source: object_url
    meaning: "UltraCart back-office deep link to the linked object"
  - name: related_workflow_task_uuid
    type: STRING
    source: related_workflow_task_uuid
    meaning: "related task (self-reference)"
  - name: dependant_workflow_task_uuid
    type: STRING
    source: dependant_workflow_task_uuid
    meaning: "task that depends on this one (self-reference; source spelling)"
  - name: note_count
    type: INTEGER
    source: "ARRAY_LENGTH(notes)"
    meaning: "number of discussion notes on the task"
  - name: attachment_count
    type: INTEGER
    source: "ARRAY_LENGTH(attachments)"
    meaning: "number of file attachments"
links:
  - to: order
    kind: references
    on: "workflow_task.object_id = order.order_id"
  - to: auto_order
    kind: references
    on: "workflow_task.object_id = auto_order.auto_order_code"
pii: none
excluded_fields: [object_email, histories, notes, attachments, properties, tags, created_by.user_icon_url]
consumers: []
---

# WorkflowTask

UltraCart's built-in ops task queue: manual to-dos and system-generated follow-ups
(review order, address decline, respond to customer) assigned to back-office staff
users/groups. Useful for operational-load analytics — task volume by context, aging
(`created_at` vs `due_at` vs `status`), and which objects generate the most manual
work.

**Polymorphic object link.** A task points at its subject through the triple
`object_type` + `object_id` + `object_url` (plus `object_email` in the source).
`object_id` must be interpreted per `object_type` — it is an `order_id` for order
tasks, an auto-order reference for subscription tasks, and so on. The `links:` entries
above are therefore **conditional**: apply them only where `object_type` matches the
target (e.g. join to `order` only on order-typed tasks). `object_url` is the ground
truth when in doubt about which entity the id means.

Gotchas:
- **`object_email` is excluded because it exists only raw** — the OKF field paths show
  `object_email STRING` with no `object_email_hash` twin, so there is no
  tier-safe way to expose it. Person-level joins must instead route through the linked
  object (e.g. task → order → `email_hash_b64`).
- `histories[]` is excluded (carries `histories.ip_address`); `notes[]` and
  `attachments[]` are excluded as free-form staff content — the canonical view keeps
  only their counts.
- `task_details` is merchant-authored free text and can incidentally mention customer
  names or emails; it is retained for operational usefulness, but do not treat the
  canonical view as PII-free for external export without scanning this column.
- `status`/`priority` enums are passed through raw; the source docs don't enumerate
  values, so no derived open/closed flag is built yet.
- `dependant_workflow_task_uuid` keeps the source's spelling ("dependant") — binding
  the real field name, aliased nowhere.

## Change log
- v1 (2026-07-06) — initial.
