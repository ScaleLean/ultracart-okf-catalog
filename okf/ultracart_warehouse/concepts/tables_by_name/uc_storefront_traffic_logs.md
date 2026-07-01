---
type: "UltraCart Table Definition"
title: "uc_storefront_traffic_logs"
description: "Storefront traffic log feed. Constrain by time and storefront when querying."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_traffic_logs"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_traffic_logs"
  - "attribution_sessions"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_traffic_logs

Storefront traffic log feed. Constrain by time and storefront when querying.

## Grain

One storefront traffic event row.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_traffic_logs](/tables/ultracart_dw/uc_storefront_traffic_logs.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_traffic_logs](/tables/ultracart_dw_low/uc_storefront_traffic_logs.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_traffic_logs](/tables/ultracart_dw_medium/uc_storefront_traffic_logs.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_traffic_logs](/tables/ultracart_dw_high/uc_storefront_traffic_logs.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `bot` | `BOOLEAN` |
| `browser` | `STRUCT` |
| `browser.device` | `STRUCT` |
| `browser.device.family` | `STRING` |
| `browser.os` | `STRUCT` |
| `browser.os.family` | `STRING` |
| `browser.os.major` | `STRING` |
| `browser.os.minor` | `STRING` |
| `browser.os.patch` | `STRING` |
| `browser.os.patch_minor` | `STRING` |
| `browser.user_agent` | `STRUCT` |
| `browser.user_agent.family` | `STRING` |
| `browser.user_agent.major` | `STRING` |
| `browser.user_agent.minor` | `STRING` |
| `browser.user_agent.patch` | `STRING` |
| `client_ip` | `STRING` |
| `domain_name` | `STRING` |
| `fake_bot` | `BOOLEAN` |
| `location` | `STRUCT` |
| `location.city` | `STRING` |
| `location.country_code` | `STRING` |
| `location.latitude` | `NUMERIC` |
| `location.longitude` | `NUMERIC` |
| `location.region` | `STRING` |
| `parameters` | `ARRAY<STRUCT>` |
| `parameters.name` | `STRING` |
| `parameters.value` | `STRING` |
| `partition_date` | `DATE` |
| `processing_time` | `NUMERIC` |
| `received_bytes` | `INTEGER` |
| `request_proto` | `STRING` |
| `request_url` | `STRING` |
| `request_uuid` | `STRING` |
| `request_verb` | `STRING` |
| `sent_bytes` | `INTEGER` |
| `status_code` | `INTEGER` |
| `subnet` | `STRING` |
| `time` | `DATETIME` |
| `type` | `STRING` |
| `user_agent` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
