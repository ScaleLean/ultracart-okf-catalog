---
type: "Reference"
title: "BigQuery Usage Patterns"
description: "Safe usage patterns for querying the UltraCart warehouse from OKF concepts."
resource: "urn:ultracart:okf:reference:bigquery-usage"
tags:
  - "ultracart"
  - "bigquery"
  - "reference"
  - "usage"
timestamp: "2026-07-01T00:00:00Z"
---

# BigQuery Usage Patterns

Use the current-state view layers for normal analytics. Start with [Warehouse access layers](/references/warehouse_layers.md) to choose the least-privileged dataset that answers the business question. `ultracart_dw_medium` is a practical default for many lifecycle and attribution examples, but `ultracart_dw`, `ultracart_dw_low`, or `ultracart_dw_high` may be the right access layer depending on permissions and required fields.

UltraCart BigQuery records are nested hierarchical objects, not fully flattened relational tables. Use `UNNEST` deliberately, preserve the intended output grain, and convert UTC date-time fields into the merchant's reporting time zone before grouping by day, week, or hour.

Prefer these source surfaces for common marts:

- Orders: `uc_orders`
- Order items: `uc_orders.items` joined to `uc_items` when item catalog enrichment is needed
- Attribution: `uc_orders.utms` plus optional `uc_screen_recordings` URL and page-view parameters
- Subscriptions: `uc_auto_orders`
- Affiliate commissions: `uc_affiliate_ledgers` after freshness validation
- Product/catalog: `uc_items`, `uc_storefront_pages`, and storefront/feed metadata fields

For revenue, cost, refund, gift-certificate, surcharge, and other currency-aware values, start with [Monetary field patterns](/references/monetary_fields.md).

Avoid direct streaming-table queries unless validating freshness, delete behavior, or the view layer itself. Streaming rows represent mutations, not one safe reporting row per business object. Avoid row sampling in public artifacts.

## Sampling And Profiling

A few current-state views can scan substantial underlying data even when returning only a handful of rows. When sampling or profiling, use explicit field lists plus date, partition, storefront, status, or business-key filters before querying these objects:

- `uc_analytics_sessions`
- `uc_cart_abandons`
- `uc_screen_recording_heatmap_data`
- `uc_screen_recordings`
- `uc_storefront_customer_emails`
- `uc_storefront_customers`
- `uc_storefront_traffic_logs`

Standard objects can also be present but empty when a merchant does not use a related UltraCart feature or module. Treat empty results as a feature-usage signal to verify, not as catalog breakage.

- `uc_affiliate_network_pixel_postback_logs`
- `uc_affiliate_network_pixels`
- `uc_conversation_agent_status_events`
- `uc_conversation_pbx_calls`
- `uc_conversations`
- `uc_storefront_blog_posts`
