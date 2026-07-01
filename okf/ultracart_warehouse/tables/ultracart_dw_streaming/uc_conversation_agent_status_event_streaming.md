---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_conversation_agent_status_event_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_conversation_agent_status_event_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_conversation_agent_status_event_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_conversation_agent_status_event_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_conversation_agent_status_event_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_conversation_agent_status_event.
- Canonical definition: [uc_conversation_agent_status_event_streaming](/concepts/tables_by_name/uc_conversation_agent_status_event_streaming.md)

## Schema Coverage

- Field paths: 20
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `agent_identifier` | `STRING` |
| `agent_name` | `STRING` |
| `agent_type` | `STRING` |
| `agent_user_id` | `STRING` |
| `channel` | `STRING` |
| `custom_status_name` | `STRING` |
| `custom_status_uuid` | `STRING` |
| `duration_in_previous_seconds` | `INTEGER` |
| `event_dts` | `DATETIME` |
| `event_uuid` | `STRING` |
| `merchant_id` | `STRING` |
| `new_routing_effect` | `STRING` |
| `new_status` | `STRING` |
| `parent_merchant_id` | `STRING` |
| `partition_date` | `DATE` |
| `previous_routing_effect` | `STRING` |
| `previous_status` | `STRING` |
| `trigger` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_conversation_agent_status_event_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
