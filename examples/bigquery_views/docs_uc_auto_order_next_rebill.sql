-- Source inspiration: UltraCart public Data Warehouse sample query "Active Auto Order Next Rebill".
-- Grain: one row per active auto-order item next scheduled rebill.
SELECT
  auto_order.auto_order_oid,
  auto_order.merchant_id,
  auto_order.auto_order_code,
  auto_order.status,
  auto_order.enabled,
  auto_order.original_order_id,
  order_header.current_stage AS original_order_current_stage,
  auto_order.original_order.billing.email_hash AS customer_hash,
  item_index,
  item.original_item_id,
  item.frequency,
  future_schedule.item_id AS scheduled_item_id,
  future_schedule.shipment_dts AS scheduled_shipment_dts,
  future_schedule.unit_cost AS scheduled_unit_cost,
  future_schedule.rebill_count AS scheduled_rebill_count,
  REGEXP_EXTRACT(auto_order.failure_reason, r'^[^\n]+') AS failure_reason_summary
FROM `{{ source_project }}.{{ access_dataset }}.uc_auto_orders` AS auto_order
JOIN `{{ source_project }}.{{ access_dataset }}.uc_orders` AS order_header
  ON order_header.order_id = auto_order.original_order_id
CROSS JOIN UNNEST(auto_order.items) AS item WITH OFFSET AS item_index
CROSS JOIN UNNEST(item.future_schedules) AS future_schedule WITH OFFSET AS future_schedule_index
WHERE auto_order.enabled IS TRUE
  AND future_schedule_index = 0
  AND order_header.payment.payment_dts IS NOT NULL
  AND order_header.current_stage NOT LIKE '%Rejected%'
  AND COALESCE(order_header.payment.test_order, FALSE) IS FALSE
  AND (item.no_order_after_dts IS NULL OR DATE(item.no_order_after_dts) >= CURRENT_DATE())
ORDER BY scheduled_shipment_dts ASC;
