---
type: "UltraCart Table Definition"
title: "uc_workflow_tasks"
description: "Workflow task mirror for analytics and operational review."
resource: "urn:ultracart:bigquery:table-definition:uc_workflow_tasks"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_workflow_tasks"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_workflow_tasks

Workflow task mirror for analytics and operational review.

## Grain

One workflow task row per workflow_task_uuid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_workflow_tasks](/tables/ultracart_dw/uc_workflow_tasks.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_workflow_tasks](/tables/ultracart_dw_low/uc_workflow_tasks.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_workflow_tasks](/tables/ultracart_dw_medium/uc_workflow_tasks.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_workflow_tasks](/tables/ultracart_dw_high/uc_workflow_tasks.md) |

## Field Paths

| Field path | Data type |
|---|---|
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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
