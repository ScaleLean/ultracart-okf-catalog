---
type: "UltraCart Table Definition"
title: "uc_storefront_pages"
description: "Page, product listing, page item membership, feed, and storefront content metadata."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_pages"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_pages"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_pages

Page, product listing, page item membership, feed, and storefront content metadata.

## Grain

One page row per storefront_page_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_pages](/tables/ultracart_dw/uc_storefront_pages.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_pages](/tables/ultracart_dw_low/uc_storefront_pages.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_pages](/tables/ultracart_dw_medium/uc_storefront_pages.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_pages](/tables/ultracart_dw_high/uc_storefront_pages.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `attributes` | `ARRAY<STRUCT>` |
| `attributes.deprecated_by_current_theme` | `BOOLEAN` |
| `attributes.name` | `STRING` |
| `attributes.storefront_page_attribute_oid` | `INTEGER` |
| `attributes.type` | `STRING` |
| `attributes.used_by` | `STRING` |
| `attributes.used_by_current_theme` | `BOOLEAN` |
| `attributes.value` | `STRING` |
| `blog_post_selectors` | `ARRAY<STRUCT>` |
| `blog_post_selectors.attribute_name` | `STRING` |
| `blog_post_selectors.attribute_value` | `STRING` |
| `blog_post_selectors.author_name` | `STRING` |
| `blog_post_selectors.selector_type` | `STRING` |
| `blog_post_selectors.storefront_page_blog_post_selector_oid` | `INTEGER` |
| `blog_post_selectors.tag` | `STRING` |
| `blog_post_template` | `STRING` |
| `blog_posts` | `ARRAY<STRUCT>` |
| `blog_posts.author_name` | `STRING` |
| `blog_posts.storefront_blog_post_oid` | `INTEGER` |
| `blog_posts.tags` | `ARRAY<STRUCT>` |
| `blog_posts.tags.value` | `STRING` |
| `blog_posts.title` | `STRING` |
| `code` | `STRING` |
| `description` | `STRING` |
| `exclude_from_sitemap` | `BOOLEAN` |
| `group_template` | `STRING` |
| `group_template_supports_pagination` | `BOOLEAN` |
| `has_blog_post_selectors` | `BOOLEAN` |
| `has_selectors` | `BOOLEAN` |
| `item_template` | `STRING` |
| `items` | `ARRAY<STRUCT>` |
| `items.canonical` | `BOOLEAN` |
| `items.cost` | `STRING` |
| `items.description` | `STRING` |
| `items.inactive` | `BOOLEAN` |
| `items.item_id` | `STRING` |
| `items.manufacturer_name` | `STRING` |
| `items.merchant_item_oid` | `INTEGER` |
| `items.sort_order` | `INTEGER` |
| `items.thumbnail_url` | `STRING` |
| `items.url_part` | `STRING` |
| `items_per_page` | `INTEGER` |
| `match_all_blog_post_selectors` | `BOOLEAN` |
| `match_all_selectors` | `BOOLEAN` |
| `merchant_id` | `STRING` |
| `multimedia` | `ARRAY<STRUCT>` |
| `multimedia.cloud_url` | `STRING` |
| `multimedia.cloud_url_expiration` | `DATETIME` |
| `multimedia.code` | `STRING` |
| `multimedia.current_theme` | `BOOLEAN` |
| `multimedia.default_multimedia` | `BOOLEAN` |
| `multimedia.description` | `STRING` |
| `multimedia.dimensions` | `STRING` |
| `multimedia.filename` | `STRING` |
| `multimedia.image_type` | `STRING` |
| `multimedia.last_modified` | `STRING` |
| `multimedia.mime_type` | `STRING` |
| `multimedia.orphan` | `BOOLEAN` |
| `multimedia.preview_html` | `STRING` |
| `multimedia.size` | `STRING` |
| `multimedia.storefront_page_multimedia_oid` | `INTEGER` |
| `multimedia.used_by` | `STRING` |
| `no_item_pages` | `BOOLEAN` |
| `page_type` | `STRING` |
| `parent_storefront_page_oid` | `INTEGER` |
| `partition_oid` | `INTEGER` |
| `path` | `STRING` |
| `permissions` | `ARRAY<STRUCT>` |
| `permissions.pricing_tier_name` | `STRING` |
| `permissions.pricing_tier_oid` | `INTEGER` |
| `permissions.storefront_page_permission_oid` | `INTEGER` |
| `review_template` | `STRING` |
| `root` | `BOOLEAN` |
| `selectors` | `ARRAY<STRUCT>` |
| `selectors.attribute_name` | `STRING` |
| `selectors.attribute_value` | `STRING` |
| `selectors.manufacturer_name` | `STRING` |
| `selectors.merchant_category_id` | `INTEGER` |
| `selectors.retail_cost_high` | `NUMERIC` |
| `selectors.retail_cost_low` | `NUMERIC` |
| `selectors.sale_item` | `BOOLEAN` |
| `selectors.selector_type` | `STRING` |
| `selectors.storefront_page_selector_oid` | `INTEGER` |
| `selectors.tag_value` | `STRING` |
| `selectors.top_seller_count` | `INTEGER` |
| `selectors.top_seller_days` | `INTEGER` |
| `selectors.variation_name` | `STRING` |
| `selectors.variation_value` | `STRING` |
| `sort_order` | `INTEGER` |
| `sort_order_child_items` | `STRING` |
| `sort_order_child_pages` | `STRING` |
| `storefront_oid` | `INTEGER` |
| `storefront_page_oid` | `INTEGER` |
| `supports_blog_posts` | `BOOLEAN` |
| `supports_items` | `BOOLEAN` |
| `supports_sub_pages` | `BOOLEAN` |
| `title` | `STRING` |
| `visible` | `BOOLEAN` |
| `visible_dts` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
