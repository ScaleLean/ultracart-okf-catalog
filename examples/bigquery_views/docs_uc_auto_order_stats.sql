-- Source inspiration: UltraCart public Data Warehouse sample query "Adding Calculations to Auto Orders".
-- Grain: one row per auto_order_oid with subscription value and duration calculations.
WITH auto_order_value AS (
  SELECT
    auto_order_oid,
    merchant_id,
    auto_order_code,
    original_order_id,
    original_order.creation_dts AS original_order_dts,
    original_order.billing.email_hash AS customer_hash,
    status,
    enabled,
    canceled_dts,
    disabled_dts,
    ARRAY_LENGTH(rebill_orders) AS rebill_order_count,
    COALESCE(original_order.summary.total.value, 0)
      - COALESCE(original_order.summary.total_refunded.value, 0) AS original_order_net_total,
    COALESCE((
      SELECT
        SUM(COALESCE(rebill.summary.total.value, 0) - COALESCE(rebill.summary.total_refunded.value, 0))
      FROM UNNEST(rebill_orders) AS rebill
      WHERE rebill.payment.payment_dts IS NOT NULL
    ), 0) AS rebill_net_total,
    IF(
      COALESCE(canceled_dts, disabled_dts) IS NULL,
      NULL,
      DATETIME_DIFF(COALESCE(canceled_dts, disabled_dts), original_order.creation_dts, DAY)
    ) AS duration_days
  FROM `{{ source_project }}.{{ access_dataset }}.uc_auto_orders`
  WHERE COALESCE(original_order.payment.test_order, FALSE) IS FALSE
)
SELECT
  auto_order_oid,
  merchant_id,
  auto_order_code,
  original_order_id,
  original_order_dts,
  customer_hash,
  status,
  enabled,
  canceled_dts,
  disabled_dts,
  rebill_order_count,
  original_order_net_total,
  rebill_net_total,
  original_order_net_total + rebill_net_total AS subscription_lifetime_value,
  ROUND(SAFE_DIVIDE(original_order_net_total + rebill_net_total, 1 + rebill_order_count), 2) AS average_order_value,
  duration_days
FROM auto_order_value;
