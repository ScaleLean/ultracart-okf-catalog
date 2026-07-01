-- Grain: one row per customer_profile_oid.
-- Purpose: safe customer lifecycle profile with hashed identity only.
SELECT
  customer_profile_oid,
  merchant_id,
  email_hash AS customer_hash,
  signup_dts,
  (SELECT b.state_region FROM UNNEST(billing) AS b WHERE COALESCE(b.default_billing, FALSE) LIMIT 1) AS billing_state_region,
  (SELECT b.country_code FROM UNNEST(billing) AS b WHERE COALESCE(b.default_billing, FALSE) LIMIT 1) AS billing_country_code,
  (SELECT s.state_region FROM UNNEST(shipping) AS s WHERE COALESCE(s.default_shipping, FALSE) LIMIT 1) AS shipping_state_region,
  (SELECT s.country_code FROM UNNEST(shipping) AS s WHERE COALESCE(s.default_shipping, FALSE) LIMIT 1) AS shipping_country_code,
  privacy.marketing AS marketing_consent,
  privacy.preference AS preference_consent,
  privacy.statistics AS statistics_consent,
  activity.global_unsubscribed,
  activity.sms_stop,
  activity.spam_complaint,
  orders_summary.first_order_dts,
  orders_summary.last_order_dts,
  orders_summary.order_count,
  orders_summary.total AS lifetime_order_total,
  loyalty.current_points AS loyalty_current_points,
  loyalty.pending_points AS loyalty_pending_points
FROM `{{ source_project }}.{{ access_dataset }}.uc_customers`;
