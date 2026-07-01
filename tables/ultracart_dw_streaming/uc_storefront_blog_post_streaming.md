---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_storefront_blog_post_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_storefront_blog_post_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_storefront_blog_post_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_storefront_blog_post_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_storefront_blog_post_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_storefront_blog_post.
- Canonical definition: [uc_storefront_blog_post_streaming](/concepts/tables_by_name/uc_storefront_blog_post_streaming.md)

## Schema Coverage

- Field paths: 33
- Array fields: 4
- Struct fields: 4

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
| `allow_comments` | `BOOLEAN` |
| `attributes` | `ARRAY<STRUCT>` |
| `attributes.name` | `STRING` |
| `attributes.type` | `STRING` |
| `attributes.value` | `STRING` |
| `author` | `STRING` |
| `body` | `STRING` |
| `creation_dts` | `DATETIME` |
| `excerpt` | `STRING` |
| `last_modified_dts` | `DATETIME` |
| `merchant_id` | `STRING` |
| `multimedia` | `ARRAY<STRUCT>` |
| `multimedia.code` | `STRING` |
| `multimedia.default` | `BOOLEAN` |
| `multimedia.description` | `STRING` |
| `multimedia.filename` | `STRING` |
| `multimedia.type` | `STRING` |
| `multimedia.url` | `STRING` |
| `page_assignments` | `ARRAY<STRUCT>` |
| `page_assignments.code` | `STRING` |
| `page_assignments.storefront_page_oid` | `INTEGER` |
| `page_assignments.title` | `STRING` |
| `partition_oid` | `INTEGER` |
| `publication_dts` | `DATETIME` |
| `storefront_blog_post_oid` | `INTEGER` |
| `storefront_oid` | `INTEGER` |
| `tags` | `ARRAY<STRUCT>` |
| `tags.value` | `STRING` |
| `title` | `STRING` |
| `url_part` | `STRING` |
| `visibility` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_streaming.uc_storefront_blog_post_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
