---
type: "UltraCart Table Definition"
title: "uc_storefront_experiments"
description: "Experiment definitions, variations, daily statistics, and linked order IDs."
resource: "urn:ultracart:bigquery:table-definition:uc_storefront_experiments"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_storefront_experiments"
  - "storefront_content"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_storefront_experiments

Experiment definitions, variations, daily statistics, and linked order IDs.

## Grain

One experiment row per storefront_experiment_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_storefront_experiments](/tables/ultracart_dw/uc_storefront_experiments.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_storefront_experiments](/tables/ultracart_dw_low/uc_storefront_experiments.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_storefront_experiments](/tables/ultracart_dw_medium/uc_storefront_experiments.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_storefront_experiments](/tables/ultracart_dw_high/uc_storefront_experiments.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `container_id` | `STRING` |
| `duration_days` | `INTEGER` |
| `end_dts` | `DATETIME` |
| `equal_weighting` | `BOOLEAN` |
| `experiment_type` | `STRING` |
| `id` | `STRING` |
| `name` | `STRING` |
| `notes` | `STRING` |
| `objective` | `STRING` |
| `objective_parameter` | `STRING` |
| `openai_current_iteration` | `INTEGER` |
| `openai_element_type` | `STRING` |
| `openai_model` | `STRING` |
| `openai_total_iterations` | `INTEGER` |
| `optimization_type` | `STRING` |
| `p95_sessions_needed` | `INTEGER` |
| `p_value` | `NUMERIC` |
| `partition_oid` | `INTEGER` |
| `session_count` | `INTEGER` |
| `start_dts` | `DATETIME` |
| `status` | `STRING` |
| `storefront_experiment_oid` | `INTEGER` |
| `storefront_oid` | `INTEGER` |
| `uri` | `STRING` |
| `variations` | `ARRAY<STRUCT>` |
| `variations.add_to_cart_count` | `INTEGER` |
| `variations.average_duration_seconds` | `INTEGER` |
| `variations.average_objective_per_session` | `NUMERIC` |
| `variations.average_order_value` | `NUMERIC` |
| `variations.bounce_count` | `INTEGER` |
| `variations.conversion_rate` | `NUMERIC` |
| `variations.daily_statistics` | `ARRAY<STRUCT>` |
| `variations.daily_statistics.add_to_cart_count` | `INTEGER` |
| `variations.daily_statistics.bounce_count` | `INTEGER` |
| `variations.daily_statistics.duration_seconds_sum` | `INTEGER` |
| `variations.daily_statistics.event_count` | `INTEGER` |
| `variations.daily_statistics.initiate_checkout_count` | `INTEGER` |
| `variations.daily_statistics.order_count` | `INTEGER` |
| `variations.daily_statistics.order_ids` | `ARRAY<STRUCT>` |
| `variations.daily_statistics.order_ids.value` | `STRING` |
| `variations.daily_statistics.order_item_count` | `INTEGER` |
| `variations.daily_statistics.page_view_count` | `INTEGER` |
| `variations.daily_statistics.revenue` | `NUMERIC` |
| `variations.daily_statistics.session_count` | `INTEGER` |
| `variations.daily_statistics.sms_opt_in_count` | `INTEGER` |
| `variations.daily_statistics.stat_dts` | `DATETIME` |
| `variations.duration_seconds_sum` | `INTEGER` |
| `variations.event_count` | `INTEGER` |
| `variations.initiate_checkout_count` | `INTEGER` |
| `variations.order_count` | `INTEGER` |
| `variations.order_item_count` | `INTEGER` |
| `variations.original_traffic_percentage` | `NUMERIC` |
| `variations.page_view_count` | `INTEGER` |
| `variations.paused` | `BOOLEAN` |
| `variations.revenue` | `NUMERIC` |
| `variations.session_count` | `INTEGER` |
| `variations.sms_opt_ins` | `INTEGER` |
| `variations.traffic_percentage` | `NUMERIC` |
| `variations.url` | `STRING` |
| `variations.variation_name` | `STRING` |
| `variations.variation_number` | `INTEGER` |
| `variations.winner` | `BOOLEAN` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
