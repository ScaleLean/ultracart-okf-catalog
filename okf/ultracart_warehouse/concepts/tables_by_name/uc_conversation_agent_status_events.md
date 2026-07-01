---
type: "UltraCart Table Definition"
title: "uc_conversation_agent_status_events"
description: "Conversation agent status event log."
resource: "urn:ultracart:bigquery:table-definition:uc_conversation_agent_status_events"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_conversation_agent_status_events"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_conversation_agent_status_events

Conversation agent status event log.

## Grain

One conversation agent-status event row per event_uuid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_conversation_agent_status_events](/tables/ultracart_dw/uc_conversation_agent_status_events.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_conversation_agent_status_events](/tables/ultracart_dw_low/uc_conversation_agent_status_events.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_conversation_agent_status_events](/tables/ultracart_dw_medium/uc_conversation_agent_status_events.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_conversation_agent_status_events](/tables/ultracart_dw_high/uc_conversation_agent_status_events.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
