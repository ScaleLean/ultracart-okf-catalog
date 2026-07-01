-- Grain: one row per order attribution touch.
-- Purpose: campaign and click analysis kept separate from item and affiliate grains.
SELECT
  o.order_id,
  o.merchant_id,
  o.creation_dts AS order_creation_dts,
  DATE(o.creation_dts) AS order_date,
  COALESCE(o.customer_profile.email_hash, o.billing.email_hash) AS customer_hash,
  touch.click_dts,
  touch.utm_source,
  touch.utm_medium,
  touch.utm_campaign,
  touch.utm_content,
  touch.utm_term,
  touch.utm_id,
  touch.fbclid,
  touch.glcid,
  touch.gbraid,
  touch.wbraid,
  touch.msclkid,
  touch.ttclid,
  touch.attribution_first_click_subtotal,
  touch.attribution_last_click_subtotal,
  touch.attribution_linear_subtotal,
  touch.attribution_position_based_subtotal
FROM `{{ source_project }}.{{ access_dataset }}.uc_orders` AS o
CROSS JOIN UNNEST(o.utms) AS touch
WHERE COALESCE(o.payment.test_order, FALSE) IS FALSE;
