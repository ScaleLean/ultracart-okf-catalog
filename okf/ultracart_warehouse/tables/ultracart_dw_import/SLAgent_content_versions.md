---
type: "BigQuery Table"
title: "ultracart_dw_import.SLAgent_content_versions"
description: "Imported or legacy segmentation helper object."
resource: "urn:ultracart:bigquery:object:ultracart_dw_import.SLAgent_content_versions"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_import"
  - "SLAgent_content_versions"
  - "import"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_import.SLAgent_content_versions

Imported or legacy segmentation helper object.

## Definition

- Dataset: [ultracart_dw_import](/datasets/ultracart_dw_import.md)
- Object name: `SLAgent_content_versions`
- Object type: `BASE TABLE`
- Table family: [import](/references/table_families.md#import)
- Grain: Imported helper grain defined by the source import or segmentation view.
- Canonical definition: [SLAgent_content_versions](/concepts/tables_by_name/SLAgent_content_versions.md)

## Schema Coverage

- Field paths: 9
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `Body` | `STRING` |
| `Headline` | `STRING` |
| `Note` | `STRING` |
| `Prompt` | `STRING` |
| `content_version` | `STRING` |
| `item_oid` | `STRING` |
| `page_oid` | `STRING` |
| `start_dt` | `DATETIME` |
| `start_dts` | `TIMESTAMP` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_import.SLAgent_content_versions`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
