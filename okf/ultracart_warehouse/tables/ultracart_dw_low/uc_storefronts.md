---
type: "BigQuery View"
title: "ultracart_dw_low.uc_storefronts"
description: "Host and storefront dimension."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_storefronts"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_storefronts"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_storefronts

Host and storefront dimension.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_storefronts`
- Object type: `VIEW`
- Table family: [storefront_content](/references/table_families.md#storefront-content)
- Grain: One storefront row per storefront_oid.
- Canonical definition: [uc_storefronts](/concepts/tables_by_name/uc_storefronts.md)

## Schema Coverage

- Field paths: 12
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `host_alias1` | `STRING` |
| `host_alias2` | `STRING` |
| `host_alias3` | `STRING` |
| `host_alias4` | `STRING` |
| `host_alias5` | `STRING` |
| `host_name` | `STRING` |
| `locked` | `BOOLEAN` |
| `merchant_id` | `STRING` |
| `partition_oid` | `INTEGER` |
| `redirect_aliases` | `BOOLEAN` |
| `storefront_oid` | `INTEGER` |
| `unlock_password` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_low.uc_storefronts`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
