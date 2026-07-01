-- Source inspiration: UltraCart public Data Warehouse sample queries for upsell paths and offer events.
-- Grain: one row per storefront, upsell path, variation, and offer.
WITH path_offers AS (
  SELECT
    path.storefront_oid,
    path.storefront_upsell_path_oid,
    path.name AS path_name,
    path.path_order,
    variation.name AS variation_name,
    visible_offer.value AS storefront_upsell_offer_oid
  FROM `{{ source_project }}.{{ access_dataset }}.uc_storefront_upsell_paths` AS path
  CROSS JOIN UNNEST(path.variations) AS variation
  CROSS JOIN UNNEST(variation.visibility_ordered_offer_oids) AS visible_offer
),
offer_events AS (
  SELECT
    storefront_upsell_offer_oid,
    COUNT(*) AS event_count,
    SUM(COALESCE(view_count, 0)) AS view_count,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(IF(successful_charge = 1, 1, 0)) AS successful_charge_count,
    ROUND(SUM(COALESCE(revenue, 0)), 2) AS revenue,
    ROUND(SUM(COALESCE(profit, 0)), 2) AS profit
  FROM `{{ source_project }}.{{ access_dataset }}.uc_storefront_upsell_offer_events`
  WHERE DATE(TIMESTAMP(event_dts), "{{ time_zone }}")
    >= DATE_SUB(CURRENT_DATE("{{ time_zone }}"), INTERVAL {{ lookback_days }} DAY)
  GROUP BY storefront_upsell_offer_oid
)
SELECT
  storefront.host_name AS storefront_host_name,
  path_offers.path_name,
  path_offers.variation_name,
  offer.name AS offer_name,
  COALESCE(offer_events.event_count, 0) AS event_count,
  COALESCE(offer_events.view_count, 0) AS view_count,
  COALESCE(offer_events.order_count, 0) AS order_count,
  COALESCE(offer_events.successful_charge_count, 0) AS successful_charge_count,
  COALESCE(offer_events.revenue, 0) AS revenue,
  COALESCE(offer_events.profit, 0) AS profit,
  ROUND(SAFE_DIVIDE(COALESCE(offer_events.revenue, 0), NULLIF(offer_events.view_count, 0)), 2) AS revenue_per_view,
  ROUND(SAFE_DIVIDE(COALESCE(offer_events.successful_charge_count, 0), NULLIF(offer_events.event_count, 0)), 4) AS successful_charge_rate
FROM path_offers
JOIN `{{ source_project }}.{{ access_dataset }}.uc_storefront_upsell_offers` AS offer
  ON offer.storefront_upsell_offer_oid = path_offers.storefront_upsell_offer_oid
LEFT JOIN `{{ source_project }}.{{ access_dataset }}.uc_storefronts` AS storefront
  ON storefront.storefront_oid = path_offers.storefront_oid
LEFT JOIN offer_events
  ON offer_events.storefront_upsell_offer_oid = path_offers.storefront_upsell_offer_oid
ORDER BY storefront_host_name, path_offers.path_order, path_offers.path_name, path_offers.variation_name, offer_name;
