-- Grain: one row per auto_order_oid.
-- Purpose: subscription lifecycle and rebill status.
SELECT
  auto_order_oid,
  merchant_id,
  original_order.customer_profile.customer_profile_oid AS customer_profile_oid,
  COALESCE(original_order.customer_profile.email_hash, original_order.billing.email_hash) AS customer_hash,
  original_order.order_id AS original_order_id,
  original_order.creation_dts AS original_order_creation_dts,
  original_order.creation_dts AS creation_dts,
  canceled_dts,
  disabled_dts,
  status,
  enabled,
  completed,
  failure_reason,
  cancel_reason,
  next_attempt,
  (SELECT MIN(item.next_shipment_dts) FROM UNNEST(items) AS item) AS next_shipment_dts,
  (SELECT SUM(COALESCE(item.rebill_value, 0)) FROM UNNEST(items) AS item) AS item_rebill_value,
  (SELECT SUM(COALESCE(item.number_of_rebills, 0)) FROM UNNEST(items) AS item) AS item_rebill_count,
  ARRAY_LENGTH(items) AS auto_order_item_count,
  ARRAY_LENGTH(add_ons) AS add_on_count
FROM `{{ source_project }}.{{ access_dataset }}.uc_auto_orders`;
