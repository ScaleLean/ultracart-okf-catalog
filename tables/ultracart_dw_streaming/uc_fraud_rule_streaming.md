---
type: "BigQuery Table"
title: "ultracart_dw_streaming.uc_fraud_rule_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:object:ultracart_dw_streaming.uc_fraud_rule_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "base_table"
  - "ultracart_dw_streaming"
  - "uc_fraud_rule_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_streaming.uc_fraud_rule_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Definition

- Dataset: [ultracart_dw_streaming](/datasets/ultracart_dw_streaming.md)
- Object name: `uc_fraud_rule_streaming`
- Object type: `BASE TABLE`
- Table family: [streaming](/references/table_families.md#streaming)
- Grain: One physical streaming change row for uc_fraud_rule.
- Canonical definition: [uc_fraud_rule_streaming](/concepts/tables_by_name/uc_fraud_rule_streaming.md)

## Schema Coverage

- Field paths: 39
- Array fields: 3
- Struct fields: 3

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
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
FROM `{{ source_project }}.ultracart_dw_streaming.uc_fraud_rule_streaming`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
