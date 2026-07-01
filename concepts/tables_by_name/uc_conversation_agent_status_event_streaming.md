---
type: "UltraCart Table Definition"
title: "uc_conversation_agent_status_event_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_conversation_agent_status_event_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_conversation_agent_status_event_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_conversation_agent_status_event_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_conversation_agent_status_event.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_conversation_agent_status_event_streaming](/tables/ultracart_dw_streaming/uc_conversation_agent_status_event_streaming.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
