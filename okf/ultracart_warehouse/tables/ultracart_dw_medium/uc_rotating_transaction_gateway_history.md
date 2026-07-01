---
type: "BigQuery View"
title: "ultracart_dw_medium.uc_rotating_transaction_gateway_history"
description: "Rotating transaction gateway history and events."
resource: "urn:ultracart:bigquery:object:ultracart_dw_medium.uc_rotating_transaction_gateway_history"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_medium"
  - "uc_rotating_transaction_gateway_history"
  - "operations_config"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_medium.uc_rotating_transaction_gateway_history

Rotating transaction gateway history and events.

## Definition

- Dataset: [ultracart_dw_medium](/datasets/ultracart_dw_medium.md)
- Object name: `uc_rotating_transaction_gateway_history`
- Object type: `VIEW`
- Table family: [operations_config](/references/table_families.md#operations-config)
- Grain: One gateway-history row per rotating_transaction_gateway_history_oid.
- Canonical definition: [uc_rotating_transaction_gateway_history](/concepts/tables_by_name/uc_rotating_transaction_gateway_history.md)

## Schema Coverage

- Field paths: 53
- Array fields: 1
- Struct fields: 2

## Field Paths

| Field path | Data type |
|---|---|
| `address_line1` | `STRING` |
| `address_line1_hash` | `STRING` |
| `affiliate_oid` | `INTEGER` |
| `affiliate_sub_id` | `STRING` |
| `auto_order_attempt` | `INTEGER` |
| `auto_order_cancel` | `BOOLEAN` |
| `auto_order_original_item_id` | `STRING` |
| `auto_order_original_order_id` | `STRING` |
| `auto_order_rebill_count` | `INTEGER` |
| `card_bin` | `STRING` |
| `card_bin_type` | `STRING` |
| `card_last4` | `STRING` |
| `card_type` | `STRING` |
| `cart_id` | `STRING` |
| `country_code` | `STRING` |
| `custom_field1` | `STRING` |
| `custom_field2` | `STRING` |
| `custom_field3` | `STRING` |
| `custom_field4` | `STRING` |
| `custom_field5` | `STRING` |
| `custom_field6` | `STRING` |
| `custom_field7` | `STRING` |
| `cvv2_present` | `BOOLEAN` |
| `extended_details` | `ARRAY<STRUCT>` |
| `extended_details.name` | `STRING` |
| `extended_details.value` | `STRING` |
| `first_item_id` | `STRING` |
| `first_name` | `STRING` |
| `first_name_hash` | `STRING` |
| `last_name` | `STRING` |
| `last_name_hash` | `STRING` |
| `merchant_id` | `STRING` |
| `order_id` | `STRING` |
| `partition_date` | `DATE` |
| `postal_code` | `STRING` |
| `returned_dual_vaulted_card` | `BOOLEAN` |
| `rotating_transaction_gateway_code` | `STRING` |
| `rotating_transaction_gateway_history_oid` | `INTEGER` |
| `success` | `BOOLEAN` |
| `three_ds` | `STRUCT` |
| `three_ds.acs_trans_id` | `STRING` |
| `three_ds.authentication_type` | `STRING` |
| `three_ds.authentication_value` | `STRING` |
| `three_ds.card_token` | `STRING` |
| `three_ds.ds_trans_id` | `STRING` |
| `three_ds.eci` | `STRING` |
| `three_ds.protocol_version` | `STRING` |
| `three_ds.sca_indicator` | `BOOLEAN` |
| `three_ds.status` | `STRING` |
| `transaction_amount` | `NUMERIC` |
| `transaction_date` | `DATETIME` |
| `transaction_type` | `STRING` |
| `used_dual_vaulted_card` | `BOOLEAN` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_medium.uc_rotating_transaction_gateway_history`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
