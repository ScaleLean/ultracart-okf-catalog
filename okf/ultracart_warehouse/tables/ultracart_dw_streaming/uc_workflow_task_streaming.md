---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_workflow_task_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_workflow_task_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_workflow_task_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_workflow_task_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_workflow_task_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_workflow_task.
- Canonical definition: [uc_workflow_task_streaming](/concepts/tables_by_name/uc_workflow_task_streaming.md)

## Schema Coverage

- Field paths: 58
- Array fields: 6
- Struct fields: 9

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `assigned_to_group` | `STRING` |
| `assigned_to_user` | `STRING` |
| `assigned_to_user_or_group` | `STRING` |
| `attachments` | `ARRAY<STRUCT>` |
| `attachments.file_name` | `STRING` |
| `attachments.file_uuid` | `STRING` |
| `attachments.mime_type` | `STRING` |
| `created_by` | `STRUCT` |
| `created_by.user` | `STRING` |
| `created_by.user_icon_url` | `STRING` |
| `created_dts` | `DATETIME` |
| `delay_until_dts` | `DATETIME` |
| `dependant_workflow_task_uuid` | `STRING` |
| `due_dts` | `DATETIME` |
| `expiration_dts` | `DATETIME` |
| `global_task_number` | `INTEGER` |
| `histories` | `ARRAY<STRUCT>` |
| `histories.activity_dts` | `DATETIME` |
| `histories.description` | `STRING` |
| `histories.ip_address` | `STRING` |
| `histories.user` | `STRUCT` |
| `histories.user.user` | `STRING` |
| `histories.user.user_icon_url` | `STRING` |
| `last_update_dts` | `DATETIME` |
| `merchant_id` | `STRING` |
| `notes` | `ARRAY<STRUCT>` |
| `notes.attachments` | `ARRAY<STRUCT>` |
| `notes.attachments.file_name` | `STRING` |
| `notes.attachments.file_uuid` | `STRING` |
| `notes.attachments.mime_type` | `STRING` |
| `notes.edit_dts` | `DATETIME` |
| `notes.note` | `STRING` |
| `notes.note_dts` | `DATETIME` |
| `notes.original_note` | `STRING` |
| `notes.user` | `STRUCT` |
| `notes.user.user` | `STRING` |
| `notes.user.user_icon_url` | `STRING` |
| `object_email` | `STRING` |
| `object_id` | `STRING` |
| `object_task_number` | `INTEGER` |
| `object_type` | `STRING` |
| `object_url` | `STRING` |
| `partition_oid` | `INTEGER` |
| `priority` | `STRING` |
| `properties` | `ARRAY<STRUCT>` |
| `properties.name` | `STRING` |
| `properties.value` | `STRING` |
| `related_workflow_task_uuid` | `STRING` |
| `status` | `STRING` |
| `system_task_type` | `STRING` |
| `tags` | `ARRAY<STRUCT>` |
| `tags.value` | `STRING` |
| `task_context` | `STRING` |
| `task_details` | `STRING` |
| `task_name` | `STRING` |
| `workflow_task_uuid` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_workflow_task_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
