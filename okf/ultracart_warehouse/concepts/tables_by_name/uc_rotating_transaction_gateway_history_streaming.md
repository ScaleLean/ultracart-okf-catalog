---
type: "UltraCart Table Definition"
title: "uc_rotating_transaction_gateway_history_streaming"
description: "Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics."
resource: "urn:ultracart:bigquery:table-definition:uc_rotating_transaction_gateway_history_streaming"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_rotating_transaction_gateway_history_streaming"
  - "streaming"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_rotating_transaction_gateway_history_streaming

Physical ingestion object that supports the current-state view layers; prefer view layers for normal analytics.

## Grain

One physical streaming change row for uc_rotating_transaction_gateway_history.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_streaming` | `BASE TABLE` | [ultracart_dw_streaming.uc_rotating_transaction_gateway_history_streaming](/tables/ultracart_dw_streaming/uc_rotating_transaction_gateway_history_streaming.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `IsDelete` | `BOOLEAN` |
| `RecordTime` | `DATETIME` |
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

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
