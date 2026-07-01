# Reference View Plan

This plan was derived from the public OKF catalog plus metadata inspection of a live ScaleLean BigQuery project. The public examples stay merchant-neutral: no client project names, no raw rows, and no sampled customer values.

## Design Principles

- Keep each base view at one clear grain.
- Expose hashed customer identifiers, not raw email, address, phone, or payment fields.
- Aggregate nested arrays before joining across grains.
- Use `ultracart_dw_medium` as the default access layer for examples.
- Use partition filters on session/traffic-style tables.
- Keep dashboard marts downstream of base views.

## View Spine

| View | Grain | Why it exists |
|---|---|---|
| `base_uc_orders` | One row per `order_id` | Stable commerce fact with status, customer hash, subscription markers, totals, costs, and item counts. |
| `base_uc_order_items` | One row per order item line | SKU/product revenue and COGS analysis without multiplying order-level fields. |
| `base_uc_order_attribution_touches` | One row per order attribution touch | Campaign/click analysis kept separate from item lines and affiliate ledger events. |
| `base_uc_customers` | One row per `customer_profile_oid` | Customer lifecycle surface with consent and order-summary fields. |
| `base_uc_auto_orders` | One row per `auto_order_oid` | Subscription status, original order, cancellation, and rebill markers. |
| `base_uc_sessions` | One row per screen-recording session | Behavior/session analysis with landing-page fields and order linkage. |
| `base_uc_page_views` | One row per page view | Page journey analysis, add-to-cart detection, and URL normalization. |
| `base_uc_affiliate_commissions` | One row per affiliate ledger event | Affiliate commission and click context without joining directly to item lines. |
| `base_uc_item_catalog` | One row per item/SKU | Product dimension for item enrichment. |

## Marts

| Mart | Grain | Inputs |
|---|---|---|
| `mart_uc_daily_commerce` | One row per order date | `base_uc_orders` |
| `mart_uc_landing_page_performance` | One row per date and landing page | `base_uc_sessions` |
| `mart_uc_customer_lifecycle` | One row per customer hash/profile | `base_uc_orders`, `base_uc_customers`, `base_uc_auto_orders` |

## Public Documentation Mining

UltraCart's public Data Warehouse documentation contains a large sample-query library. The docs examples were mined for reusable analytical intents, then rewritten here as merchant-neutral, agent-friendly SQL with explicit grains and placeholders:

| Example | Grain | Public-docs intent represented |
|---|---|---|
| `docs_uc_auto_order_stats` | One row per auto order | Add calculated subscription metrics to auto orders. |
| `docs_uc_auto_order_next_rebill` | One row per active auto-order item next rebill | Build an operational rebill queue. |
| `docs_uc_auto_order_cohort_revenue` | Cohort month, primary item, month number | Analyze subscription cohort revenue. |
| `docs_uc_item_revenue_period` | One row per merchant item | Measure item revenue over a period. |
| `docs_uc_coupon_usage_summary` | One row per base coupon code | Summarize coupon usage and sales. |
| `docs_uc_utm_sales_by_week` | Week, UTM source, UTM campaign | Roll up campaign revenue by week. |
| `docs_uc_affiliate_click_order_metrics` | Click date, affiliate, landing page, sub-id | Measure affiliate click-to-order performance. |
| `docs_uc_conversion_rate_sessions` | One row per session date | Measure website funnel conversion from analytics sessions. |
| `docs_uc_inventory_month_start_value` | Month, item, distribution center | Estimate inventory value at the start of each month. |
| `docs_uc_upsell_path_statistics` | Storefront, path, variation, offer | Evaluate upsell path and offer performance. |
| `docs_uc_storefront_experiment_stats` | Storefront experiment variation | Summarize experiment performance. |
| `ops_query_cost_audit` | Query text | Find expensive BigQuery queries for cost control. |

## Risks To Keep Explicit

- Kit components and upsell lines can double-count item revenue if mixed with parent items.
- Attribution arrays, coupon arrays, and item arrays must not be unnested together.
- Affiliate ledgers can have multiple transactions per order; aggregate before joining to orders.
- Customer profile grain and email-hash grain can diverge.
- Session order linkage is sparse; missing links are expected.
- Current-state UltraCart views are not historical snapshots unless the table itself is a ledger/event surface.
- Public documentation examples often demonstrate a technique in one compact query; keep this repo's versions safer for reuse by avoiding raw contact fields and keeping each output grain explicit.
