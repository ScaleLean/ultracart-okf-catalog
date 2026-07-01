---
type: "UltraCart Table Definition"
title: "uc_storefront_blog_posts"
description: "Storefront blog and content metadata."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_blog_posts"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_blog_posts"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_blog_posts

Storefront blog and content metadata.

## Grain

One blog post row per storefront_blog_post_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_blog_posts](/tables/ultracart_dw/uc_storefront_blog_posts.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_blog_posts](/tables/ultracart_dw_low/uc_storefront_blog_posts.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_blog_posts](/tables/ultracart_dw_medium/uc_storefront_blog_posts.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_blog_posts](/tables/ultracart_dw_high/uc_storefront_blog_posts.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
