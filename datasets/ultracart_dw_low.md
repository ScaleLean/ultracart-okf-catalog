---
type: "BigQuery Dataset"
title: "ultracart_dw_low"
description: "Lower-access current-state view layer for broad reporting use."
resource: "urn:ultracart:bigquery:dataset:ultracart_dw_low"
tags:
  - "ultracart"
  - "bigquery"
  - "dataset"
  - "ultracart_dw_low"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low

Lower-access current-state view layer for broad reporting use.

## Object Counts

- View: 43

## Objects

| Object | Type | Family | Field paths | Arrays | Structs |
|---|---|---|---:|---:|---:|
| [uc_affiliate_clicks](/tables/ultracart_dw_low/uc_affiliate_clicks.md) | View | affiliate_commissions | 28 | 0 | 1 |
| [uc_affiliate_commission_groups](/tables/ultracart_dw_low/uc_affiliate_commission_groups.md) | View | affiliate_commissions | 49 | 7 | 7 |
| [uc_affiliate_ledgers](/tables/ultracart_dw_low/uc_affiliate_ledgers.md) | View | affiliate_commissions | 60 | 0 | 3 |
| [uc_affiliate_network_pixel_postback_logs](/tables/ultracart_dw_low/uc_affiliate_network_pixel_postback_logs.md) | View | affiliate_commissions | 29 | 0 | 1 |
| [uc_affiliate_network_pixels](/tables/ultracart_dw_low/uc_affiliate_network_pixels.md) | View | affiliate_commissions | 19 | 0 | 0 |
| [uc_affiliate_payments](/tables/ultracart_dw_low/uc_affiliate_payments.md) | View | affiliate_commissions | 29 | 1 | 2 |
| [uc_affiliate_postback_logs](/tables/ultracart_dw_low/uc_affiliate_postback_logs.md) | View | affiliate_commissions | 15 | 1 | 1 |
| [uc_affiliates](/tables/ultracart_dw_low/uc_affiliates.md) | View | affiliate_commissions | 69 | 2 | 3 |
| [uc_analytics_sessions](/tables/ultracart_dw_low/uc_analytics_sessions.md) | View | attribution_sessions | 480 | 18 | 89 |
| [uc_auto_orders](/tables/ultracart_dw_low/uc_auto_orders.md) | View | commerce_core | 2282 | 104 | 309 |
| [uc_cart_abandons](/tables/ultracart_dw_low/uc_cart_abandons.md) | View | operations_config | 639 | 29 | 110 |
| [uc_conversation_agent_status_events](/tables/ultracart_dw_low/uc_conversation_agent_status_events.md) | View | customers_support | 18 | 0 | 0 |
| [uc_conversation_pbx_calls](/tables/ultracart_dw_low/uc_conversation_pbx_calls.md) | View | customers_support | 137 | 11 | 19 |
| [uc_conversations](/tables/ultracart_dw_low/uc_conversations.md) | View | customers_support | 62 | 4 | 5 |
| [uc_coupons](/tables/ultracart_dw_low/uc_coupons.md) | View | operations_config | 341 | 79 | 129 |
| [uc_customers](/tables/ultracart_dw_low/uc_customers.md) | View | customers_support | 1939 | 85 | 271 |
| [uc_fraud_rules](/tables/ultracart_dw_low/uc_fraud_rules.md) | View | operations_config | 37 | 3 | 3 |
| [uc_gift_certificates](/tables/ultracart_dw_low/uc_gift_certificates.md) | View | operations_config | 21 | 1 | 1 |
| [uc_integration_logs](/tables/ultracart_dw_low/uc_integration_logs.md) | View | operations_config | 28 | 5 | 5 |
| [uc_item_inventory_history](/tables/ultracart_dw_low/uc_item_inventory_history.md) | View | commerce_core | 13 | 0 | 0 |
| [uc_items](/tables/ultracart_dw_low/uc_items.md) | View | commerce_core | 712 | 52 | 99 |
| [uc_orders](/tables/ultracart_dw_low/uc_orders.md) | View | commerce_core | 1085 | 47 | 147 |
| [uc_rotating_transaction_gateway_history](/tables/ultracart_dw_low/uc_rotating_transaction_gateway_history.md) | View | operations_config | 50 | 1 | 2 |
| [uc_rotating_transaction_gateways](/tables/ultracart_dw_low/uc_rotating_transaction_gateways.md) | View | operations_config | 65 | 7 | 7 |
| [uc_screen_recording_heatmap_data](/tables/ultracart_dw_low/uc_screen_recording_heatmap_data.md) | View | attribution_sessions | 16 | 3 | 3 |
| [uc_screen_recordings](/tables/ultracart_dw_low/uc_screen_recordings.md) | View | attribution_sessions | 90 | 7 | 13 |
| [uc_shipping_methods](/tables/ultracart_dw_low/uc_shipping_methods.md) | View | operations_config | 197 | 17 | 28 |
| [uc_storefront_blog_posts](/tables/ultracart_dw_low/uc_storefront_blog_posts.md) | View | storefront_content | 31 | 4 | 4 |
| [uc_storefront_customer_emails](/tables/ultracart_dw_low/uc_storefront_customer_emails.md) | View | customers_support | 19 | 0 | 0 |
| [uc_storefront_customer_lists](/tables/ultracart_dw_low/uc_storefront_customer_lists.md) | View | customers_support | 7 | 0 | 0 |
| [uc_storefront_customer_segments](/tables/ultracart_dw_low/uc_storefront_customer_segments.md) | View | customers_support | 7 | 0 | 0 |
| [uc_storefront_customer_sessions](/tables/ultracart_dw_low/uc_storefront_customer_sessions.md) | View | customers_support | 19 | 1 | 1 |
| [uc_storefront_customers](/tables/ultracart_dw_low/uc_storefront_customers.md) | View | customers_support | 47 | 5 | 5 |
| [uc_storefront_experiments](/tables/ultracart_dw_low/uc_storefront_experiments.md) | View | storefront_content | 62 | 3 | 3 |
| [uc_storefront_pages](/tables/ultracart_dw_low/uc_storefront_pages.md) | View | storefront_content | 99 | 8 | 8 |
| [uc_storefront_traffic_logs](/tables/ultracart_dw_low/uc_storefront_traffic_logs.md) | View | attribution_sessions | 40 | 1 | 6 |
| [uc_storefront_upsell_offer_events](/tables/ultracart_dw_low/uc_storefront_upsell_offer_events.md) | View | storefront_content | 76 | 1 | 1 |
| [uc_storefront_upsell_offers](/tables/ultracart_dw_low/uc_storefront_upsell_offers.md) | View | storefront_content | 103 | 21 | 21 |
| [uc_storefront_upsell_paths](/tables/ultracart_dw_low/uc_storefront_upsell_paths.md) | View | storefront_content | 45 | 10 | 12 |
| [uc_storefronts](/tables/ultracart_dw_low/uc_storefronts.md) | View | storefront_content | 12 | 0 | 0 |
| [uc_towerdata_email_intelligence](/tables/ultracart_dw_low/uc_towerdata_email_intelligence.md) | View | customers_support | 52 | 0 | 5 |
| [uc_workflow_tasks](/tables/ultracart_dw_low/uc_workflow_tasks.md) | View | operations_config | 56 | 6 | 9 |
| [uc_zoho_desk_tickets](/tables/ultracart_dw_low/uc_zoho_desk_tickets.md) | View | customers_support | 242 | 19 | 27 |

## References

- [Source coverage](/references/source_coverage.md)
