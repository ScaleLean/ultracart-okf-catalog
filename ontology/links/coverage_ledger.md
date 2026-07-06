---
type: "Ontology Coverage Ledger"
resource: "urn:ultracart:ontology:coverage"
generated: true
---

# Coverage ledger — every canonical warehouse table, placed

Tables: 112 · object sources: 26 · streaming twins: 4 · peripheral/link sources: 82

Totality is enforced by `validate_ontology.py --offline`. Regenerate with
`python3 scripts/generate_indexes.py` after adding objects.

| Table | Domain | Tier | Ontology role | Meaning |
|---|---|---|---|---|
| `SLAgent_content_versions` | storefront_content | peripheral | documented peripheral / property-link source | Imported/legacy content-version helper (headline/body/prompt per item/page). |
| `c90` | enrichment_analytics | supporting | documented peripheral / property-link source | Master customer ML feature table (~140 features: RFM, LTV targets, coupons/items top-10, sessions, demographics, churn). |
| `customer_auto_orders_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: subscription activity per customer (active/rebill counts, rebill revenue). |
| `customer_comms_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: email engagement counts (sent/open/click/conversion/spam/unsub). |
| `customer_comms_trends_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: regression-slope trends of open/click behavior. |
| `customer_orders_22382_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: order behavior (RFM, LTV, coupons/items top-10, day/daypart histograms) for storefront 22382. |
| `customer_orders_trends_22382_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: order-frequency trend regression per customer (storefront 22382). |
| `customer_profiles_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: loyalty points/ledger/redemptions + review counts per customer. |
| `customer_recent_comms_22382_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: recent-window email engagement counts (storefront 22382). |
| `customer_recent_sessions_22382_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: recent-window visit behavior (visits, page views, time on site, UTMs) for storefront 22382. |
| `customer_screen_recordings_22382_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: screen-recording presence, geo, language, last campaign/flow attribution (storefront 22382). |
| `customer_sessions_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: full-window visit behavior per customer (visit RFM, histograms, UTMs). |
| `customer_sessions_bounding_shape_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: activity envelope (days, density, magnitude) per customer. |
| `customer_sessions_trends_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML features: visit-trend regression (slope, intercept, magnitude) per customer. |
| `customer_targets_22382_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | ML training labels: churn, retention, target LTV / LTV-increase, target-period orders (storefront 22382). |
| `customer_tower_data` | enrichment_analytics | supporting | documented peripheral / property-link source | ML copy of TowerData demographics keyed by email_hash. |
| `dataset_registry` | enrichment_analytics | peripheral | documented peripheral / property-link source | ML dataset registry (name/version, GCS path, row counts, windows). |
| `model_monitor` | enrichment_analytics | peripheral | documented peripheral / property-link source | ML model monitoring snapshots (drift, MSE/RMSE over time). |
| `model_registry` | enrichment_analytics | peripheral | documented peripheral / property-link source | ML model registry (model name/version, linked dataset, GCS path, MSE/RMSE). |
| `retention_score_22382_365_90` | enrichment_analytics | supporting | documented peripheral / property-link source | Model output: retention score per customer (storefront 22382). |
| `segment_customers_autoOrders` | marketing_comms | peripheral | documented peripheral / property-link source | Imported/legacy segmentation helper: auto-order customers with completed-order counts by product category. |
| `segment_regular_1Month` | marketing_comms | peripheral | documented peripheral / property-link source | Imported/legacy segmentation helper: plain email list ("regular 1-month" segment). |
| `uc_affiliate_click_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_affiliate_clicks. |
| `uc_affiliate_clicks` | affiliates | core | object source: `affiliate_click` | Affiliate click/source event with landing page, referrer, and session linkage. |
| `uc_affiliate_commission_group_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_affiliate_commission_groups. |
| `uc_affiliate_commission_groups` | affiliates | supporting | documented peripheral / property-link source | Commission group definitions with per-item commission rules and exclusions. |
| `uc_affiliate_ledger_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_affiliate_ledgers. |
| `uc_affiliate_ledgers` | affiliates | core | object source: `affiliate_ledger` | Affiliate commission/transaction ledger with order linkage and payout state. |
| `uc_affiliate_network_pixel_postback_log_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_affiliate_network_pixel_postback_logs. |
| `uc_affiliate_network_pixel_postback_logs` | affiliates | peripheral | documented peripheral / property-link source | Fire log of network pixel postbacks (URL, response, status). |
| `uc_affiliate_network_pixel_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_affiliate_network_pixels. |
| `uc_affiliate_network_pixels` | affiliates | supporting | documented peripheral / property-link source | Third-party affiliate-network conversion pixel configuration. |
| `uc_affiliate_payment_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_affiliate_payments. |
| `uc_affiliate_payments` | affiliates | supporting | documented peripheral / property-link source | Affiliate payout records (checks/PayPal) aggregating ledger entries. |
| `uc_affiliate_postback_log_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_affiliate_postback_logs. |
| `uc_affiliate_postback_logs` | affiliates | peripheral | documented peripheral / property-link source | Server-to-server affiliate postback fire log. |
| `uc_affiliate_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_affiliates. |
| `uc_affiliates` | affiliates | core | object source: `affiliate` | Affiliate account dimension: identity, payout config, tracking prefs, tier relationships. |
| `uc_analytics_session_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_analytics_sessions. |
| `uc_analytics_sessions` | storefront_behavior | core | object source: `analytics_session` | UltraCart analytics session model with nested hits (page views, cart events, email events, towerdata) and session behavior. |
| `uc_auto_order_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_auto_orders. |
| `uc_auto_orders` | commerce_core | core | object source: `auto_order`, `auto_order_item` | Subscription (auto-order) lifecycle: original order snapshot, items, rebills, next attempt, cancellation context. |
| `uc_cart_abandon_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_cart_abandons. |
| `uc_cart_abandons` | storefront_behavior | core | object source: `cart_abandon` | Abandoned cart snapshot (items, billing/shipping, coupons, payment intent) — customer/address fields redacted in standard views. |
| `uc_conversation_agent_status_event_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_conversation_agent_status_events. |
| `uc_conversation_agent_status_events` | support_conversations | supporting | documented peripheral / property-link source | Agent presence/status change event log (available, custom statuses, routing effects). |
| `uc_conversation_pbx_call_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_conversation_pbx_calls. |
| `uc_conversation_pbx_calls` | support_conversations | core | object source: `pbx_call` | PBX phone-call records: routing, agents, holds/transfers, recordings, AI summary/engagements, Zoho ticket linkage. |
| `uc_conversation_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_conversations. |
| `uc_conversations` | support_conversations | core | object source: `conversation` | Chat/SMS conversation metadata with redacted message structure, participants, sentiment, virtual-agent usage. |
| `uc_coupon_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_coupons. |
| `uc_coupons` | promotions | core | object source: `coupon` | Coupon configuration — ~50 mutually-exclusive discount-type structs (amount/percent off items/subtotal/shipping, BOGO, tiered…). |
| `uc_customer_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_customers. |
| `uc_customers` | commerce_core | core | object source: `customer_profile` | Registered customer profile: billing/shipping books, cards, loyalty, order/quote summaries, pricing tiers, entitlements. |
| `uc_fraud_rule_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_fraud_rules. |
| `uc_fraud_rules` | risk_finance | supporting | documented peripheral / property-link source | Merchant fraud rule configuration (rule type, filters, actions). |
| `uc_gift_certificate_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_gift_certificates. |
| `uc_gift_certificates` | promotions | core | object source: `gift_certificate` | Gift certificate accounts with balances and ledger entries. |
| `uc_integration_log_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_integration_logs. |
| `uc_integration_logs` | platform_internal | peripheral | documented peripheral / property-link source | Integration event log (EDI/API/third-party actions) with raw content redacted in standard views. |
| `uc_item_inventory_history` | catalog | supporting | object source: `inventory_snapshot` | Inventory movement ledger (adjustments with before/after levels and reason). |
| `uc_item_inventory_history_streaming` | platform_internal | peripheral | streaming twin of `uc_item_inventory_history` (RecordTime/IsDelete change feed) | Streaming change-log twin of uc_item_inventory_history. |
| `uc_item_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_items. |
| `uc_items` | catalog | core | object source: `item` | Product/SKU catalog: pricing, costs, kits/components, variants, channel-partner SKU mappings, feeds, digital delivery. |
| `uc_order_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_orders. |
| `uc_order_summary_mv` | commerce_core | supporting | documented peripheral / property-link source | Dashboard rollup of order totals by channel/period. |
| `uc_orders` | commerce_core | core | object source: `order`, `order_item` | Order header + nested items, coupons, affiliates, UTMs, subscription markers, economics; primary source for orders/order-items/first-pass attribution. |
| `uc_rotating_transaction_gateway_history` | risk_finance | core | documented peripheral / property-link source | Per-transaction gateway attempt history: success/decline, card BIN/last4, 3DS, dual-vaulting, auto-order rebill context. |
| `uc_rotating_transaction_gateway_history_streaming` | platform_internal | peripheral | streaming twin of `uc_rotating_transaction_gateway_history` (RecordTime/IsDelete change feed) | Streaming change-log twin of uc_rotating_transaction_gateway_history. |
| `uc_rotating_transaction_gateway_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_rotating_transaction_gateways. |
| `uc_rotating_transaction_gateways` | risk_finance | supporting | object source: `payment_gateway` | Rotating payment gateway configuration: caps, cascades, reserves, traffic split. |
| `uc_screen_recording_heatmap_data` | storefront_behavior | supporting | documented peripheral / property-link source | Heatmap/click-position aggregates per URL × screen size for session behavior analysis. |
| `uc_screen_recording_heatmap_data_streaming` | platform_internal | peripheral | streaming twin of `uc_screen_recording_heatmap_data` (RecordTime/IsDelete change feed) | Streaming change-log twin of uc_screen_recording_heatmap_data. |
| `uc_screen_recording_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_screen_recordings. |
| `uc_screen_recordings` | storefront_behavior | core | object source: `screen_recording` | Session/page-view trail with URL & referrer params, ad-platform click IDs, UTM recovery, comms attribution, sparse order linkage. |
| `uc_shipping_method_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_shipping_methods. |
| `uc_shipping_methods` | fulfillment_ops | supporting | documented peripheral / property-link source | Shipping method configuration: markups, restrictions, cutoffs, per-item costs, least-cost routing. |
| `uc_storefront_blog_post_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_blog_posts. |
| `uc_storefront_blog_posts` | storefront_content | peripheral | documented peripheral / property-link source | Blog/content post metadata with page assignments. |
| `uc_storefront_communications_dataset_delta` | platform_internal | peripheral | documented peripheral / property-link source | Raw comms dataset delta feed: per-email JSON record changes (no parsed schema). |
| `uc_storefront_customer_email_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_customer_emails. |
| `uc_storefront_customer_emails` | marketing_comms | core | object source: `email_send` | Per-send email engagement events (sent/opened/clicked/converted/spam) with campaign & flow attribution. |
| `uc_storefront_customer_list_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_customer_lists. |
| `uc_storefront_customer_lists` | marketing_comms | supporting | object source: `email_list_membership` | Email list membership link table. |
| `uc_storefront_customer_segment_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_customer_segments. |
| `uc_storefront_customer_segments` | marketing_comms | supporting | object source: `email_segment_membership` | Customer segment membership link table. |
| `uc_storefront_customer_session_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_customer_sessions. |
| `uc_storefront_customer_sessions` | marketing_comms | supporting | documented peripheral / property-link source | ESP-side view of a visit: session window, UTMs, page_views, order linkage per marketing customer. |
| `uc_storefront_customer_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_customers. |
| `uc_storefront_customers` | marketing_comms | core | object source: `marketing_contact` | ESP/marketing-audience customer profile with nested email sends, list/segment memberships, and sessions. |
| `uc_storefront_experiment_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_experiments. |
| `uc_storefront_experiments` | storefront_behavior | supporting | object source: `experiment` | A/B experiment definitions, variations with daily stats, and linked order IDs. |
| `uc_storefront_page_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_pages. |
| `uc_storefront_pages` | storefront_content | supporting | documented peripheral / property-link source | Page, product-listing and page-item membership metadata (templates, selectors, permissions). |
| `uc_storefront_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefronts. |
| `uc_storefront_traffic_log_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_traffic_logs. |
| `uc_storefront_traffic_logs` | storefront_behavior | peripheral | documented peripheral / property-link source | Raw storefront HTTP traffic feed (request, bytes, bot flags, geo). |
| `uc_storefront_upsell_offer_event_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_upsell_offer_events. |
| `uc_storefront_upsell_offer_events` | storefront_behavior | supporting | object source: `upsell_offer_event` | Upsell offer impression/decline/charge event log with revenue & profit economics. |
| `uc_storefront_upsell_offer_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_upsell_offers. |
| `uc_storefront_upsell_offers` | storefront_behavior | supporting | documented peripheral / property-link source | Upsell offer configuration (trigger/suppression rules, per-weekday pricing, screenshots). |
| `uc_storefront_upsell_path_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_storefront_upsell_paths. |
| `uc_storefront_upsell_paths` | storefront_behavior | supporting | documented peripheral / property-link source | Upsell path (funnel) configuration grouping offers with variations. |
| `uc_storefronts` | storefront_content | supporting | object source: `storefront` | Storefront/host dimension (host name + aliases). |
| `uc_survey_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_surveys. |
| `uc_surveys` | storefront_behavior | supporting | documented peripheral / property-link source | Survey definitions + response structures (questions nested), tied to orders and incentives. |
| `uc_towerdata_email_intelligence` | enrichment_analytics | supporting | object source: `person_enrichment` | TowerData third-party demographic/interest enrichment per email (age, income, net worth, interests, RFM). |
| `uc_towerdata_email_intelligence_streaming` | platform_internal | peripheral | streaming twin of `uc_towerdata_email_intelligence` (RecordTime/IsDelete change feed) | Streaming change-log twin of uc_towerdata_email_intelligence. |
| `uc_workflow_task_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_workflow_tasks. |
| `uc_workflow_tasks` | fulfillment_ops | supporting | object source: `workflow_task` | Internal workflow/task queue mirror (assignment, priority, due dates, histories). |
| `uc_zoho_desk_ticket_streaming` | platform_internal | peripheral | documented peripheral / property-link source | Streaming change-log twin of uc_zoho_desk_tickets. |
| `uc_zoho_desk_tickets` | support_conversations | core | object source: `support_ticket` | Zoho Desk helpdesk ticket mirror (status, SLA, assignee, contact, threads/comments). |
