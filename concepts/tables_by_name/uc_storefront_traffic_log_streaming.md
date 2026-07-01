---
type: "UltraCart Table Definition"
title: "uc_storefront_traffic_log_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_traffic_log_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_traffic_log_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_traffic_log_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_storefront_traffic_log.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_storefront_traffic_log_streaming](/tables/ultracart_dw_streaming/uc_storefront_traffic_log_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
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
