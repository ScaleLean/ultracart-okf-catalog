---
type: "BigQuery View"
title: "ultracart_dw_low.uc_rotating_transaction_gateways"
description: "Rotating transaction gateway configuration."
resource: "urn:ultracart:bigquery:object:ultracart_dw_low.uc_rotating_transaction_gateways"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_low"
  - "uc_rotating_transaction_gateways"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_low.uc_rotating_transaction_gateways

Rotating transaction gateway configuration.

## Definition

- Dataset: [ultracart_dw_low](/datasets/ultracart_dw_low.md)
- Object name: `uc_rotating_transaction_gateways`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One gateway row per rotating_transaction_gateway_oid.
- Canonical definition: [uc_rotating_transaction_gateways](/concepts/tables_by_name/uc_rotating_transaction_gateways.md)

## Schema Coverage

- Field paths: 65
- Array fields: 7
- Struct fields: 7

## Field Paths

| Field path | Data type |
|---|---|
| `additional_native_currency_codes` | `ARRAY<STRUCT>` |
| `additional_native_currency_codes.currency_code` | `STRING` |
| `additional_native_currency_codes.description` | `STRING` |
| `additional_native_currency_codes.selected` | `BOOLEAN` |
| `auto_order_cancel_unless_response_name` | `STRING` |
| `auto_order_cancel_unless_response_values` | `ARRAY<STRUCT>` |
| `auto_order_cancel_unless_response_values.value` | `STRING` |
| `base_currency_code` | `STRING` |
| `batch_cutoff_time` | `STRING` |
| `cascade_code` | `STRING` |
| `cascade_daily_auto_order_code` | `STRING` |
| `charge_appears_on_statement_as` | `STRING` |
| `code` | `STRING` |
| `cumulative_domestic_revenue` | `NUMERIC` |
| `cumulative_international_revenue` | `NUMERIC` |
| `currency_code_restrictions` | `ARRAY<STRUCT>` |
| `currency_code_restrictions.currency_code` | `STRING` |
| `currency_code_restrictions.restriction` | `STRING` |
| `current_daily` | `NUMERIC` |
| `current_daily_auto_order` | `NUMERIC` |
| `current_monthly` | `NUMERIC` |
| `customer_service_email` | `STRING` |
| `customer_service_phone` | `STRING` |
| `day_of_month_restrictions` | `ARRAY<STRUCT>` |
| `day_of_month_restrictions.day_of_month` | `INTEGER` |
| `day_of_month_restrictions.selected` | `BOOLEAN` |
| `day_of_week_restrictions` | `ARRAY<STRUCT>` |
| `day_of_week_restrictions.abbreviation` | `STRING` |
| `day_of_week_restrictions.day_of_week` | `INTEGER` |
| `day_of_week_restrictions.selected` | `BOOLEAN` |
| `deactivate_after_failures` | `INTEGER` |
| `end_date` | `DATETIME` |
| `maximum_daily` | `NUMERIC` |
| `maximum_daily_auto_order` | `NUMERIC` |
| `maximum_international_percentage` | `NUMERIC` |
| `maximum_monthly` | `NUMERIC` |
| `merchant_id` | `STRING` |
| `next_daily_auto_order_reset` | `DATETIME` |
| `next_daily_reset` | `DATETIME` |
| `next_monthly_reset` | `DATETIME` |
| `order_total` | `NUMERIC` |
| `order_total_comparison` | `STRING` |
| `partition_oid` | `INTEGER` |
| `preferred_for_auto_orders` | `BOOLEAN` |
| `prevent_cascade_if_response_name` | `STRING` |
| `prevent_cascade_if_response_values` | `ARRAY<STRUCT>` |
| `prevent_cascade_if_response_values.value` | `STRING` |
| `rebill_auto_orders_against_this_rtg_code` | `STRING` |
| `require_cvv2` | `BOOLEAN` |
| `reserve_days` | `INTEGER` |
| `reserve_percentage` | `NUMERIC` |
| `reserve_refunded` | `BOOLEAN` |
| `reserves_released_through` | `DATETIME` |
| `rotating_transaction_gateway_oid` | `INTEGER` |
| `start_date` | `DATETIME` |
| `status` | `STRING` |
| `theme_restrictions` | `ARRAY<STRUCT>` |
| `theme_restrictions.restriction` | `STRING` |
| `theme_restrictions.storefront_host_name` | `STRING` |
| `theme_restrictions.theme_code` | `STRING` |
| `traffic_percentage` | `NUMERIC` |
| `trial_daily_amount` | `INTEGER` |
| `trial_daily_limit` | `INTEGER` |
| `trial_monthly_amount` | `INTEGER` |
| `trial_monthly_limit` | `INTEGER` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_low.uc_rotating_transaction_gateways`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
