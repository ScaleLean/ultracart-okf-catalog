---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_storefront_communications_dataset_delta"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_storefront_communications_dataset_delta"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_storefront_communications_dataset_delta"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_storefront_communications_dataset_delta

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_storefront_communications_dataset_delta`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical change or delta row from the source ingestion stream.
- Canonical definition: [uc_storefront_communications_dataset_delta](/concepts/tables_by_name/uc_storefront_communications_dataset_delta.md)

## Schema Coverage

- Field paths: 5
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `dataset_id` | `STRING` |
| `email` | `STRING` |
| `record_json` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_storefront_communications_dataset_delta`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
