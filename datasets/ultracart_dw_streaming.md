---
type: "BigQuery Dataset"
title: "ultracart_dw_streaming"
description: "Physical streaming layer with record-time and delete-marker fields; use mainly for freshness, delete behavior, and view validation."
resource: "urn:ultracart:bigquery:dataset:ultracart_dw_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "dataset"
  - "ultracart_dw_streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming

Physical streaming layer with record-time and delete-marker fields; use mainly for freshness, delete behavior, and view validation.

## Object Counts

- Base Table: 45

## Objects

| Object | Type | Family | Field paths | Arrays | Structs |
|---|---|---|---:|---:|---:|
| [uc_affiliate_click_streaming](/tables/ultracart_dw_streaming/uc_affiliate_click_streaming.md) | Base Table | streaming | 30 | 0 | 1 |
| [uc_affiliate_commission_group_streaming](/tables/ultracart_dw_streaming/uc_affiliate_commission_group_streaming.md) | Base Table | streaming | 51 | 7 | 7 |
| [uc_affiliate_ledger_streaming](/tables/ultracart_dw_streaming/uc_affiliate_ledger_streaming.md) | Base Table | streaming | 62 | 0 | 3 |
| [uc_affiliate_network_pixel_postback_log_streaming](/tables/ultracart_dw_streaming/uc_affiliate_network_pixel_postback_log_streaming.md) | Base Table | streaming | 31 | 0 | 1 |
| [uc_affiliate_network_pixel_streaming](/tables/ultracart_dw_streaming/uc_affiliate_network_pixel_streaming.md) | Base Table | streaming | 21 | 0 | 0 |
| [uc_affiliate_payment_streaming](/tables/ultracart_dw_streaming/uc_affiliate_payment_streaming.md) | Base Table | streaming | 34 | 1 | 2 |
| [uc_affiliate_postback_log_streaming](/tables/ultracart_dw_streaming/uc_affiliate_postback_log_streaming.md) | Base Table | streaming | 17 | 1 | 1 |
| [uc_affiliate_streaming](/tables/ultracart_dw_streaming/uc_affiliate_streaming.md) | Base Table | streaming | 81 | 2 | 3 |
| [uc_analytics_session_streaming](/tables/ultracart_dw_streaming/uc_analytics_session_streaming.md) | Base Table | streaming | 482 | 18 | 89 |
| [uc_auto_order_streaming](/tables/ultracart_dw_streaming/uc_auto_order_streaming.md) | Base Table | streaming | 2368 | 112 | 311 |
| [uc_cart_abandon_streaming](/tables/ultracart_dw_streaming/uc_cart_abandon_streaming.md) | Base Table | streaming | 688 | 30 | 111 |
| [uc_conversation_agent_status_event_streaming](/tables/ultracart_dw_streaming/uc_conversation_agent_status_event_streaming.md) | Base Table | streaming | 20 | 0 | 0 |
| [uc_conversation_pbx_call_streaming](/tables/ultracart_dw_streaming/uc_conversation_pbx_call_streaming.md) | Base Table | streaming | 145 | 11 | 19 |
| [uc_conversation_streaming](/tables/ultracart_dw_streaming/uc_conversation_streaming.md) | Base Table | streaming | 71 | 5 | 6 |
| [uc_coupon_streaming](/tables/ultracart_dw_streaming/uc_coupon_streaming.md) | Base Table | streaming | 343 | 79 | 129 |
| [uc_customer_streaming](/tables/ultracart_dw_streaming/uc_customer_streaming.md) | Base Table | streaming | 2004 | 87 | 273 |
| [uc_fraud_rule_streaming](/tables/ultracart_dw_streaming/uc_fraud_rule_streaming.md) | Base Table | streaming | 39 | 3 | 3 |
| [uc_gift_certificate_streaming](/tables/ultracart_dw_streaming/uc_gift_certificate_streaming.md) | Base Table | streaming | 24 | 1 | 1 |
| [uc_integration_log_streaming](/tables/ultracart_dw_streaming/uc_integration_log_streaming.md) | Base Table | streaming | 37 | 5 | 5 |
| [uc_item_inventory_history_streaming](/tables/ultracart_dw_streaming/uc_item_inventory_history_streaming.md) | Base Table | streaming | 15 | 0 | 0 |
| [uc_item_streaming](/tables/ultracart_dw_streaming/uc_item_streaming.md) | Base Table | streaming | 714 | 52 | 99 |
| [uc_order_streaming](/tables/ultracart_dw_streaming/uc_order_streaming.md) | Base Table | streaming | 1129 | 50 | 148 |
| [uc_rotating_transaction_gateway_history_streaming](/tables/ultracart_dw_streaming/uc_rotating_transaction_gateway_history_streaming.md) | Base Table | streaming | 55 | 1 | 2 |
| [uc_rotating_transaction_gateway_streaming](/tables/ultracart_dw_streaming/uc_rotating_transaction_gateway_streaming.md) | Base Table | streaming | 67 | 7 | 7 |
| [uc_screen_recording_heatmap_data_streaming](/tables/ultracart_dw_streaming/uc_screen_recording_heatmap_data_streaming.md) | Base Table | streaming | 18 | 3 | 3 |
| [uc_screen_recording_streaming](/tables/ultracart_dw_streaming/uc_screen_recording_streaming.md) | Base Table | streaming | 99 | 7 | 14 |
| [uc_shipping_method_streaming](/tables/ultracart_dw_streaming/uc_shipping_method_streaming.md) | Base Table | streaming | 199 | 17 | 28 |
| [uc_storefront_blog_post_streaming](/tables/ultracart_dw_streaming/uc_storefront_blog_post_streaming.md) | Base Table | streaming | 33 | 4 | 4 |
| [uc_storefront_communications_dataset_delta](/tables/ultracart_dw_streaming/uc_storefront_communications_dataset_delta.md) | Base Table | streaming | 5 | 0 | 0 |
| [uc_storefront_customer_email_streaming](/tables/ultracart_dw_streaming/uc_storefront_customer_email_streaming.md) | Base Table | streaming | 22 | 0 | 0 |
| [uc_storefront_customer_list_streaming](/tables/ultracart_dw_streaming/uc_storefront_customer_list_streaming.md) | Base Table | streaming | 10 | 0 | 0 |
| [uc_storefront_customer_segment_streaming](/tables/ultracart_dw_streaming/uc_storefront_customer_segment_streaming.md) | Base Table | streaming | 10 | 0 | 0 |
| [uc_storefront_customer_session_streaming](/tables/ultracart_dw_streaming/uc_storefront_customer_session_streaming.md) | Base Table | streaming | 22 | 1 | 1 |
| [uc_storefront_customer_streaming](/tables/ultracart_dw_streaming/uc_storefront_customer_streaming.md) | Base Table | streaming | 50 | 5 | 5 |
| [uc_storefront_experiment_streaming](/tables/ultracart_dw_streaming/uc_storefront_experiment_streaming.md) | Base Table | streaming | 64 | 3 | 3 |
| [uc_storefront_page_streaming](/tables/ultracart_dw_streaming/uc_storefront_page_streaming.md) | Base Table | streaming | 101 | 8 | 8 |
| [uc_storefront_streaming](/tables/ultracart_dw_streaming/uc_storefront_streaming.md) | Base Table | streaming | 14 | 0 | 0 |
| [uc_storefront_traffic_log_streaming](/tables/ultracart_dw_streaming/uc_storefront_traffic_log_streaming.md) | Base Table | streaming | 42 | 1 | 6 |
| [uc_storefront_upsell_offer_event_streaming](/tables/ultracart_dw_streaming/uc_storefront_upsell_offer_event_streaming.md) | Base Table | streaming | 78 | 1 | 1 |
| [uc_storefront_upsell_offer_streaming](/tables/ultracart_dw_streaming/uc_storefront_upsell_offer_streaming.md) | Base Table | streaming | 105 | 21 | 21 |
| [uc_storefront_upsell_path_streaming](/tables/ultracart_dw_streaming/uc_storefront_upsell_path_streaming.md) | Base Table | streaming | 47 | 10 | 12 |
| [uc_survey_streaming](/tables/ultracart_dw_streaming/uc_survey_streaming.md) | Base Table | streaming | 45 | 4 | 5 |
| [uc_towerdata_email_intelligence_streaming](/tables/ultracart_dw_streaming/uc_towerdata_email_intelligence_streaming.md) | Base Table | streaming | 55 | 0 | 5 |
| [uc_workflow_task_streaming](/tables/ultracart_dw_streaming/uc_workflow_task_streaming.md) | Base Table | streaming | 58 | 6 | 9 |
| [uc_zoho_desk_ticket_streaming](/tables/ultracart_dw_streaming/uc_zoho_desk_ticket_streaming.md) | Base Table | streaming | 244 | 20 | 28 |

## References

- [Source coverage](/references/source_coverage.md)
