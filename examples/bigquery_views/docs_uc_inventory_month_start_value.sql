-- Source inspiration: UltraCart public Data Warehouse sample query "Inventory Value at Start Of Each Month".
-- Grain: one row per month, item, and distribution center.
WITH months AS (
  SELECT month_start
  FROM UNNEST(
    GENERATE_DATE_ARRAY(
      DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH), MONTH),
      DATE_TRUNC(CURRENT_DATE(), MONTH),
      INTERVAL 1 MONTH
    )
  ) AS month_start
),
item_distribution_centers AS (
  SELECT
    item.merchant_item_id,
    distribution_center.distribution_center_code,
    COALESCE(distribution_center.cogs, item.pricing.cogs, 0) AS unit_cogs,
    COALESCE(distribution_center.inventory_level, 0) AS current_inventory_level
  FROM `{{ source_project }}.{{ access_dataset }}.uc_items` AS item
  CROSS JOIN UNNEST(item.shipping.distribution_centers) AS distribution_center
  WHERE COALESCE(distribution_center.handles, FALSE) IS TRUE
),
month_item_distribution_centers AS (
  SELECT
    months.month_start,
    item_distribution_centers.merchant_item_id,
    item_distribution_centers.distribution_center_code,
    item_distribution_centers.unit_cogs,
    item_distribution_centers.current_inventory_level
  FROM months
  CROSS JOIN item_distribution_centers
),
latest_history AS (
  SELECT
    base.month_start,
    base.merchant_item_id,
    base.distribution_center_code,
    ARRAY_AGG(
      STRUCT(history.history_dts, history.after_inventory_level)
      ORDER BY history.history_dts DESC
      LIMIT 1
    )[SAFE_OFFSET(0)] AS latest_record
  FROM month_item_distribution_centers AS base
  LEFT JOIN `{{ source_project }}.{{ access_dataset }}.uc_item_inventory_history` AS history
    ON history.merchant_item_id = base.merchant_item_id
    AND history.distribution_center_code = base.distribution_center_code
    AND DATE(history.history_dts) <= base.month_start
  GROUP BY base.month_start, base.merchant_item_id, base.distribution_center_code
)
SELECT
  base.month_start,
  base.merchant_item_id,
  base.distribution_center_code,
  COALESCE(latest_history.latest_record.after_inventory_level, base.current_inventory_level, 0) AS inventory_level,
  base.unit_cogs,
  ROUND(COALESCE(latest_history.latest_record.after_inventory_level, base.current_inventory_level, 0) * base.unit_cogs, 2) AS inventory_value
FROM month_item_distribution_centers AS base
LEFT JOIN latest_history
  ON latest_history.month_start = base.month_start
  AND latest_history.merchant_item_id = base.merchant_item_id
  AND latest_history.distribution_center_code = base.distribution_center_code
WHERE COALESCE(latest_history.latest_record.after_inventory_level, base.current_inventory_level, 0) <> 0
ORDER BY base.month_start DESC, inventory_value DESC;
