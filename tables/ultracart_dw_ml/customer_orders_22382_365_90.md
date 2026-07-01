---
type: "BigQuery Table"
title: "ultracart_dw_ml.customer_orders_22382_365_90"
description: "Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring."
resource: "urn:ultracart:bigquery:object:ultracart_dw_ml.customer_orders_22382_365_90"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_ml"
  - "customer_orders_22382_365_90"
  - "ml"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_ml.customer_orders_22382_365_90

Derived customer-modeling or machine-learning object used for features, scoring, registry, or monitoring.

## Definition

- Dataset: [ultracart_dw_ml](/datasets/ultracart_dw_ml.md)
- Object name: `customer_orders_22382_365_90`
- Object type: `BASE TABLE`
- Table family: [ml](/references/table_families.md#ml)
- Grain: Derived customer-modeling or machine-learning feature grain; inspect fields before joining.
- Canonical definition: [customer_orders_22382_365_90](/concepts/tables_by_name/customer_orders_22382_365_90.md)

## Schema Coverage

- Field paths: 78
- Array fields: 0
- Struct fields: 0

## Field Paths

| Field path | Data type |
|---|---|
| `LTV` | `FLOAT` |
| `T` | `INTEGER` |
| `auto_order_count` | `INTEGER` |
| `avg_discount_value` | `FLOAT` |
| `avg_fraud_score` | `FLOAT` |
| `avg_subtotal_value` | `FLOAT` |
| `billing_country_code` | `STRING` |
| `browser` | `STRING` |
| `coupons_0` | `STRING` |
| `coupons_1` | `STRING` |
| `coupons_2` | `STRING` |
| `coupons_3` | `STRING` |
| `coupons_4` | `STRING` |
| `coupons_5` | `STRING` |
| `coupons_6` | `STRING` |
| `coupons_7` | `STRING` |
| `coupons_8` | `STRING` |
| `coupons_9` | `STRING` |
| `coupons_used_count` | `INTEGER` |
| `currency_code` | `STRING` |
| `days_since_last_order` | `INTEGER` |
| `device` | `STRING` |
| `discounted_order_count` | `INTEGER` |
| `distinct_coupons_used_count` | `INTEGER` |
| `distinct_item_count` | `INTEGER` |
| `email_hash` | `STRING` |
| `first_coupon` | `STRING` |
| `frequency` | `INTEGER` |
| `gift_card_purchase_count` | `INTEGER` |
| `gifts_purchased_count` | `INTEGER` |
| `item_0` | `STRING` |
| `item_1` | `STRING` |
| `item_2` | `STRING` |
| `item_3` | `STRING` |
| `item_4` | `STRING` |
| `item_5` | `STRING` |
| `item_6` | `STRING` |
| `item_7` | `STRING` |
| `item_8` | `STRING` |
| `item_9` | `STRING` |
| `item_count` | `INTEGER` |
| `language_iso_code` | `STRING` |
| `last_coupon` | `STRING` |
| `monetary_value` | `FLOAT` |
| `order_count` | `INTEGER` |
| `orders_per_day_0` | `INTEGER` |
| `orders_per_day_1` | `INTEGER` |
| `orders_per_day_2` | `INTEGER` |
| `orders_per_day_3` | `INTEGER` |
| `orders_per_day_4` | `INTEGER` |
| `orders_per_day_5` | `INTEGER` |
| `orders_per_day_6` | `INTEGER` |
| `orders_per_daypart_0` | `INTEGER` |
| `orders_per_daypart_1` | `INTEGER` |
| `orders_per_daypart_2` | `INTEGER` |
| `orders_per_daypart_3` | `INTEGER` |
| `orders_per_daypart_4` | `INTEGER` |
| `orders_per_daypart_5` | `INTEGER` |
| `os` | `STRING` |
| `preferred_payment_method` | `STRING` |
| `recency` | `INTEGER` |
| `refund_count` | `INTEGER` |
| `reject_count` | `INTEGER` |
| `screen_size` | `STRING` |
| `shipping_country_code` | `STRING` |
| `subtotal_refunded` | `FLOAT` |
| `total_refunded` | `FLOAT` |
| `upsell_count` | `INTEGER` |
| `upsell_item_0` | `STRING` |
| `upsell_item_1` | `STRING` |
| `upsell_item_2` | `STRING` |
| `upsell_item_3` | `STRING` |
| `upsell_item_4` | `STRING` |
| `upsell_item_5` | `STRING` |
| `upsell_item_6` | `STRING` |
| `upsell_item_7` | `STRING` |
| `upsell_item_8` | `STRING` |
| `upsell_item_9` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_ml.customer_orders_22382_365_90`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
