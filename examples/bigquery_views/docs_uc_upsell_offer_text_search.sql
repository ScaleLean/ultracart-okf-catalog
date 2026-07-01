-- Source inspiration: UltraCart public Data Warehouse sample query "Find Upsell Offers Containing Text".
-- Grain: one row per storefront/path/variation/offer match.
SELECT
  storefront.merchant_id,
  storefront.host_name AS storefront_host_name,
  path.name AS path_name,
  variation.name AS variation_name,
  offer.name AS offer_name,
  offer.storefront_upsell_offer_oid
FROM `{{ source_project }}.{{ access_dataset }}.uc_storefront_upsell_paths` AS path
CROSS JOIN UNNEST(path.variations) AS variation
CROSS JOIN UNNEST(variation.visibility_ordered_offer_oids) AS visible_offer
JOIN `{{ source_project }}.{{ access_dataset }}.uc_storefront_upsell_offers` AS offer
  ON offer.storefront_upsell_offer_oid = visible_offer.value
JOIN `{{ source_project }}.{{ access_dataset }}.uc_storefronts` AS storefront
  ON storefront.storefront_oid = path.storefront_oid
WHERE LOWER(offer.offer_container_cjson) LIKE CONCAT('%', LOWER('{{ search_text }}'), '%')
ORDER BY storefront.merchant_id, storefront.host_name, path.path_order, path_name, offer_name;
