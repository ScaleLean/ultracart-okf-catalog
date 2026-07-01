---
type: "BigQuery View"
title: "ultracart_dw.uc_affiliate_network_pixels"
description: "Affiliate and network pixel configuration."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_affiliate_network_pixels"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_affiliate_network_pixels"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_affiliate_network_pixels

Affiliate and network pixel configuration.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_affiliate_network_pixels`
- Object type: `VIEW`
- Table family: [affiliate_commissions](/references/table_families.md#affiliate-commissions)
- Grain: Affiliate network pixel definition records.
- Canonical definition: [uc_affiliate_network_pixels](/concepts/tables_by_name/uc_affiliate_network_pixels.md)

## Schema Coverage

- Field paths: 19
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
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
FROM `{{ source_project }}.ultracart_dw.uc_affiliate_network_pixels`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
