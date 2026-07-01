---
type: "BigQuery View"
title: "ultracart_dw_import.segment_regular_1Month"
description: "Imported or legacy segmentation helper object."
resource: "urn:ultracart:bigquery:object:ultracart_dw_import.segment_regular_1Month"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_import"
  - "segment_regular_1Month"
  - "import"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_import.segment_regular_1Month

Imported or legacy segmentation helper object.

## Definition

- Dataset: [ultracart_dw_import](/datasets/ultracart_dw_import.md)
- Object name: `segment_regular_1Month`
- Object type: `VIEW`
- Table family: [import](/references/table_families.md#import)
- Grain: Imported helper grain defined by the source import or segmentation view.
- Canonical definition: [segment_regular_1Month](/concepts/tables_by_name/segment_regular_1Month.md)

## Schema Coverage

- Field paths: 1
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `email` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_import.segment_regular_1Month`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
