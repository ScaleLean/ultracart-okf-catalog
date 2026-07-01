---
type: "BigQuery View"
title: "ultracart_dw.uc_affiliate_network_pixel_postback_logs"
description: "Affiliate network postback event log."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_affiliate_network_pixel_postback_logs"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_affiliate_network_pixel_postback_logs"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_affiliate_network_pixel_postback_logs

Affiliate network postback event log.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_affiliate_network_pixel_postback_logs`
- Object type: `VIEW`
- Table family: [affiliate_commissions](/references/table_families.md#affiliate-commissions)
- Grain: Network pixel postback log events.
- Canonical definition: [uc_affiliate_network_pixel_postback_logs](/concepts/tables_by_name/uc_affiliate_network_pixel_postback_logs.md)

## Schema Coverage

- Field paths: 29
- Array fields: 0
- Struct fields: 1

## Field Paths

| Field path | Data type |
|---|---|
| `affiliate_network_pixel_oid` | `INTEGER` |
| `affiliate_network_pixel_postback_log_uuid` | `STRING` |
| `merchant_id` | `STRING` |
| `network` | `STRUCT` |
| `network.affiliate_network_pixel_oid` | `INTEGER` |
| `network.assign_to_internal_affiliate_oid` | `INTEGER` |
| `network.commission_fixed` | `NUMERIC` |
| `network.conversion_pixel` | `STRING` |
| `network.conversion_type` | `STRING` |
| `network.cookie_lifetime_days` | `INTEGER` |
| `network.fire_percentage` | `NUMERIC` |
| `network.merchant_id` | `STRING` |
| `network.network_name` | `STRING` |
| `network.no_fire_assign_to_internal_affiliate_oid` | `INTEGER` |
| `network.no_fire_skip_internal_affiliate_system` | `BOOLEAN` |
| `network.parameter_name` | `STRING` |
| `network.parameter_value` | `STRING` |
| `network.record_fire_in_custom_field` | `INTEGER` |
| `network.record_name_in_custom_field` | `INTEGER` |
| `network.remove_empty_pixel_parameters` | `BOOLEAN` |
| `network.stomp_other_cookies` | `BOOLEAN` |
| `network.storefront_oid` | `INTEGER` |
| `order_id` | `STRING` |
| `partition_date` | `DATE` |
| `postback_dts` | `DATETIME` |
| `response` | `STRING` |
| `status_code` | `INTEGER` |
| `storefront_oid` | `INTEGER` |
| `url` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw.uc_affiliate_network_pixel_postback_logs`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
