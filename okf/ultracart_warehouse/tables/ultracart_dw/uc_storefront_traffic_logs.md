---
type: "BigQuery View"
title: "ultracart_dw.uc_storefront_traffic_logs"
description: "Storefront traffic log feed. Constrain by time and storefront when querying."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_storefront_traffic_logs"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_storefront_traffic_logs"
  - "attribution_sessions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_storefront_traffic_logs

Storefront traffic log feed. Constrain by time and storefront when querying.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_storefront_traffic_logs`
- Object type: `VIEW`
- Table family: [attribution_sessions](/references/table_families.md#attribution-sessions)
- Grain: One storefront traffic event row.
- Canonical definition: [uc_storefront_traffic_logs](/concepts/tables_by_name/uc_storefront_traffic_logs.md)

## Schema Coverage

- Field paths: 40
- Array fields: 1
- Struct fields: 6

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw.uc_storefront_traffic_logs`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
