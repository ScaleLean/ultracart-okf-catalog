---
type: "UltraCart Table Definition"
title: "uc_storefront_blog_post_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_blog_post_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_blog_post_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_blog_post_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_storefront_blog_post.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_storefront_blog_post_streaming](/tables/ultracart_dw_streaming/uc_storefront_blog_post_streaming.md) |

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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
