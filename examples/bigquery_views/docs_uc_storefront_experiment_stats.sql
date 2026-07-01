-- Source inspiration: UltraCart public Data Warehouse sample query "StoreFront Experiment Statistics".
-- Grain: one row per storefront experiment variation, using the experiment summary table.
SELECT
  storefront.host_name AS storefront_host_name,
  experiment.name AS experiment_name,
  experiment.id AS experiment_id,
  experiment.storefront_experiment_oid,
  variation.variation_number,
  variation.variation_name,
  variation.traffic_percentage,
  variation.winner,
  variation.session_count,
  variation.page_view_count,
  variation.bounce_count,
  variation.add_to_cart_count,
  variation.initiate_checkout_count,
  variation.order_count,
  variation.order_item_count,
  variation.sms_opt_ins,
  variation.revenue,
  variation.conversion_rate,
  variation.average_order_value,
  variation.average_duration_seconds,
  ROUND(SAFE_DIVIDE(variation.revenue, variation.session_count), 2) AS revenue_per_session
FROM `{{ source_project }}.{{ access_dataset }}.uc_storefront_experiments` AS experiment
CROSS JOIN UNNEST(experiment.variations) AS variation
LEFT JOIN `{{ source_project }}.{{ access_dataset }}.uc_storefronts` AS storefront
  ON storefront.storefront_oid = experiment.storefront_oid
ORDER BY storefront_host_name, experiment_name, variation.variation_number;
