---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_affiliate_network_pixel_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_affiliate_network_pixel_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_affiliate_network_pixel_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_affiliate_network_pixel_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_affiliate_network_pixel_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_affiliate_network_pixel.
- Canonical definition: [uc_affiliate_network_pixel_streaming](/concepts/tables_by_name/uc_affiliate_network_pixel_streaming.md)

## Schema Coverage

- Field paths: 21
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `affiliate_network_pixel_oid` | `INTEGER` |
| `assign_to_internal_affiliate_oid` | `INTEGER` |
| `commission_fixed` | `NUMERIC` |
| `conversion_pixel` | `STRING` |
| `conversion_type` | `STRING` |
| `cookie_lifetime_days` | `INTEGER` |
| `fire_percentage` | `NUMERIC` |
| `merchant_id` | `STRING` |
| `network_name` | `STRING` |
| `no_fire_assign_to_internal_affiliate_oid` | `INTEGER` |
| `no_fire_skip_internal_affiliate_system` | `BOOLEAN` |
| `parameter_name` | `STRING` |
| `parameter_value` | `STRING` |
| `partition_oid` | `INTEGER` |
| `record_fire_in_custom_field` | `INTEGER` |
| `record_name_in_custom_field` | `INTEGER` |
| `remove_empty_pixel_parameters` | `BOOLEAN` |
| `stomp_other_cookies` | `BOOLEAN` |
| `storefront_oid` | `INTEGER` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_affiliate_network_pixel_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
