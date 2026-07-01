---
type: "UltraCart Table Definition"
title: "uc_fraud_rules"
description: "Fraud rule configuration."
resource: "urn:ultracart:bigquery:table-definition:uc_fraud_rules"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_fraud_rules"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_fraud_rules

Fraud rule configuration.

## Grain

One fraud rule row per fraud_rule_oid.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_fraud_rules](/tables/ultracart_dw/uc_fraud_rules.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_fraud_rules](/tables/ultracart_dw_low/uc_fraud_rules.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_fraud_rules](/tables/ultracart_dw_medium/uc_fraud_rules.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_fraud_rules](/tables/ultracart_dw_high/uc_fraud_rules.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `affiliate_oid` | `INTEGER` |
| `auto_note` | `STRING` |
| `card_number` | `STRING` |
| `created_by` | `STRING` |
| `created_dts` | `DATETIME` |
| `decline_message` | `STRING` |
| `description` | `STRING` |
| `description_html` | `STRING` |
| `failure_action` | `STRING` |
| `fraud_rule_oid` | `INTEGER` |
| `item_filters` | `ARRAY<STRUCT>` |
| `item_filters.merchant_item_id` | `STRING` |
| `item_filters.merchant_item_oid` | `INTEGER` |
| `merchant_id` | `STRING` |
| `modify_custom_field1` | `STRING` |
| `modify_custom_field2` | `STRING` |
| `modify_custom_field3` | `STRING` |
| `modify_custom_field4` | `STRING` |
| `modify_custom_field5` | `STRING` |
| `modify_custom_field6` | `STRING` |
| `modify_custom_field7` | `STRING` |
| `modify_skip_affiliate` | `BOOLEAN` |
| `modify_skip_affiliate_network_pixel` | `BOOLEAN` |
| `param1` | `NUMERIC` |
| `param2` | `INTEGER` |
| `param3` | `STRING` |
| `param4` | `STRING` |
| `partition_oid` | `INTEGER` |
| `rotating_transaction_gateway_filters` | `ARRAY<STRUCT>` |
| `rotating_transaction_gateway_filters.code` | `STRING` |
| `rotating_transaction_gateway_filters.rotating_transaction_gateway_oid` | `INTEGER` |
| `rule_group` | `STRING` |
| `rule_type` | `STRING` |
| `storefront_filters` | `ARRAY<STRUCT>` |
| `storefront_filters.screen_branding_theme_code` | `STRING` |
| `storefront_filters.storefront_host_name` | `STRING` |
| `user_action` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
