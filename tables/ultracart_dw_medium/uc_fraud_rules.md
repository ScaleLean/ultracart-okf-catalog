---
type: "BigQuery View"
title: "ultracart_dw_medium.uc_fraud_rules"
description: "Fraud rule configuration."
resource: "urn:ultracart:bigquery:object:ultracart_dw_medium.uc_fraud_rules"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_medium"
  - "uc_fraud_rules"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_medium.uc_fraud_rules

Fraud rule configuration.

## Definition

- Dataset: [ultracart_dw_medium](/datasets/ultracart_dw_medium.md)
- Object name: `uc_fraud_rules`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One fraud rule row per fraud_rule_oid.
- Canonical definition: [uc_fraud_rules](/concepts/tables_by_name/uc_fraud_rules.md)

## Schema Coverage

- Field paths: 37
- Array fields: 3
- Struct fields: 3

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

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_medium.uc_fraud_rules`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
