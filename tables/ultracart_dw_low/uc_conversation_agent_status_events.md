---
type: "BigQuery View"
title: "ultracart_dw_low.uc_conversation_agent_status_events"
description: "Conversation agent status event log."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_conversation_agent_status_events"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_conversation_agent_status_events"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_conversation_agent_status_events

Conversation agent status event log.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_conversation_agent_status_events`
- Object type: `VIEW`
- Table family: [customers_support](/references/table_families.md#customers-support)
- Grain: One conversation agent-status event row per event_uuid.
- Canonical definition: [uc_conversation_agent_status_events](/concepts/tables_by_name/uc_conversation_agent_status_events.md)

## Schema Coverage

- Field paths: 18
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
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
FROM `{{ source_project }}.ultracart_dw_low.uc_conversation_agent_status_events`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
