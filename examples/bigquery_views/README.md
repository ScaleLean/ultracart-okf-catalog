# UltraCart Reference BigQuery Views

These SQL files are reference consumers for the public OKF catalog. They show how to turn the metadata bundle into practical, reusable query surfaces without copying merchant-specific warehouse SQL.

Use them as base queries before building dashboards, search indexes, or agent tools:

- `base_uc_orders.sql` - one row per order, with safe customer keys and order economics.
- `base_uc_order_items.sql` - one row per non-kit order item line.
- `base_uc_order_attribution_touches.sql` - one row per order attribution touch.
- `base_uc_customers.sql` - one row per customer profile, excluding raw contact fields.
- `base_uc_auto_orders.sql` - one row per subscription/auto-order.
- `base_uc_sessions.sql` - one row per screen-recording session.
- `base_uc_page_views.sql` - one row per page view inside a session.
- `base_uc_affiliate_commissions.sql` - one row per affiliate ledger event.
- `base_uc_item_catalog.sql` - one row per catalog item/SKU.
- `mart_uc_daily_commerce.sql` - daily commerce rollup.
- `mart_uc_landing_page_performance.sql` - landing-page session/order rollup.
- `mart_uc_customer_lifecycle.sql` - customer lifecycle/RFM example.

Docs-inspired examples mined from the public UltraCart Data Warehouse documentation:

- `docs_uc_auto_order_stats.sql` - subscription value, rebill count, AOV, and duration metrics.
- `docs_uc_auto_order_next_rebill.sql` - active auto-order next scheduled rebill queue.
- `docs_uc_auto_order_cohort_revenue.sql` - subscription cohort revenue by primary item and cohort month number.
- `docs_uc_item_revenue_period.sql` - item revenue and units sold for a bounded period.
- `docs_uc_coupon_usage_summary.sql` - coupon usage, order counts, and revenue.
- `docs_uc_utm_sales_by_week.sql` - weekly UTM revenue rollup.
- `docs_uc_affiliate_click_order_metrics.sql` - affiliate click-to-order conversion metrics.
- `docs_uc_conversion_rate_sessions.sql` - session funnel conversion by day.
- `docs_uc_inventory_month_start_value.sql` - month-start inventory value by item and distribution center.
- `docs_uc_upsell_path_statistics.sql` - upsell path/offer event performance.
- `docs_uc_upsell_offer_text_search.sql` - search upsell offer payloads for a text fragment.
- `docs_uc_storefront_experiment_stats.sql` - storefront experiment variation summary.
- `ops_query_cost_audit.sql` - BigQuery query cost audit from `INFORMATION_SCHEMA`.

The files use placeholders:

- `{{ source_project }}` - merchant UltraCart BigQuery project.
- `{{ access_dataset }}` - current-state access layer, often `ultracart_dw_medium`; use the least-privileged layer that contains the required fields.
- `{{ lookback_days }}` - bounded session lookback for partitioned behavior tables.
- `{{ time_zone }}` - reporting time zone, normally `America/New_York`.
- `{{ search_text }}` - text fragment for the upsell offer search example.
- `{{ billing_project }}`, `{{ bq_region }}`, `{{ cost_start_date }}`, `{{ cost_end_date }}` - operations query-cost audit controls.

Do not point these examples at `ultracart_dw_streaming` for ordinary reporting. Streaming tables are mutation logs, while `ultracart_dw`, `ultracart_dw_low`, `ultracart_dw_medium`, and `ultracart_dw_high` are current-state view layers. Parent accounts may also have linked-account datasets for consolidated reporting.

Dry-run them against an accessible warehouse:

```sh
python3 scripts/dry_run_example_views.py \
  --source-project YOUR_ULTRACART_PROJECT \
  --access-dataset ultracart_dw_medium \
  --billing-project YOUR_BILLING_PROJECT
```

Dry-run the public-docs-inspired examples too:

```sh
python3 scripts/dry_run_example_views.py \
  --source-project YOUR_ULTRACART_PROJECT \
  --access-dataset ultracart_dw_medium \
  --billing-project YOUR_BILLING_PROJECT \
  --include-docs
```

These examples intentionally separate order facts, item lines, attribution touches, sessions, and affiliate ledgers. Joining all of those grains in one query is the fastest path to double-counting.
