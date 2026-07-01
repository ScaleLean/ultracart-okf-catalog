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

Use the current-state view layers for normal analytics. Start with `ultracart_dw_medium` unless a lower or higher access layer is explicitly required.

Prefer these source surfaces for common marts:

- Orders: `uc_orders`
- Order items: `uc_orders.items` joined to `uc_items` when item catalog enrichment is needed
- Attribution: `uc_orders.utms` plus optional `uc_screen_recordings` URL and page-view parameters
- Subscriptions: `uc_auto_orders`
- Affiliate commissions: `uc_affiliate_ledgers` after freshness validation
- Product/catalog: `uc_items`, `uc_storefront_pages`, and storefront/feed metadata fields

Avoid direct streaming-table queries unless validating freshness, delete behavior, or the view layer itself. Avoid row sampling in public artifacts.
