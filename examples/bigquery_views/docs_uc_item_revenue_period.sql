-- Source inspiration: UltraCart public Data Warehouse sample query "Revenue Per Item Over a Certain Time Period".
-- Grain: one row per merchant item for a bounded order period.
SELECT
  item.merchant_item_id,
  ANY_VALUE(item.description) AS item_description,
  COUNT(DISTINCT order_header.order_id) AS order_count,
  SUM(COALESCE(item.quantity, 0)) AS units_sold,
  ROUND(SUM(COALESCE(item.total_cost_with_discount.value, item.quantity * item.cost.value, 0)), 2) AS item_revenue_after_discount,
  ROUND(SUM(COALESCE(item.cogs, 0) * COALESCE(item.quantity, 0)), 2) AS item_cogs
FROM `{{ source_project }}.{{ access_dataset }}.uc_orders` AS order_header
CROSS JOIN UNNEST(order_header.items) AS item
WHERE DATE(TIMESTAMP(order_header.creation_dts), "{{ time_zone }}")
    >= DATE_SUB(CURRENT_DATE("{{ time_zone }}"), INTERVAL {{ lookback_days }} DAY)
  AND COALESCE(order_header.payment.test_order, FALSE) IS FALSE
  AND COALESCE(item.kit_component, FALSE) IS FALSE
GROUP BY item.merchant_item_id
ORDER BY item_revenue_after_discount DESC, item.merchant_item_id;
