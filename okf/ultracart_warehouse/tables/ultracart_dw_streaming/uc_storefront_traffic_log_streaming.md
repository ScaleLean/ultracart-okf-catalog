---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_storefront_traffic_log_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_storefront_traffic_log_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_storefront_traffic_log_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_storefront_traffic_log_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_storefront_traffic_log_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_storefront_traffic_log.
- Canonical definition: [uc_storefront_traffic_log_streaming](/concepts/tables_by_name/uc_storefront_traffic_log_streaming.md)

## Schema Coverage

- Field paths: 42
- Array fields: 1
- Struct fields: 6

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_storefront_traffic_log_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
