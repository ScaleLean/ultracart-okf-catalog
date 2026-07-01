---
type: "BigQuery View"
title: "ultracart_dw.uc_storefront_blog_posts"
description: "Storefront blog and content metadata."
resource: "urn:ultracart:bigquery:object:ultracart_dw.uc_storefront_blog_posts"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw"
  - "uc_storefront_blog_posts"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw.uc_storefront_blog_posts

Storefront blog and content metadata.

## Definition

- Dataset: [ultracart_dw](/datasets/ultracart_dw.md)
- Object name: `uc_storefront_blog_posts`
- Object type: `VIEW`
- Table family: [storefront_content](/references/table_families.md#storefront-content)
- Grain: One blog post row per storefront_blog_post_oid.
- Canonical definition: [uc_storefront_blog_posts](/concepts/tables_by_name/uc_storefront_blog_posts.md)

## Schema Coverage

- Field paths: 31
- Array fields: 4
- Struct fields: 4

## Field Paths

| Field path | Data type |
|---|---|
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
FROM `{{ source_project }}.ultracart_dw.uc_storefront_blog_posts`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
