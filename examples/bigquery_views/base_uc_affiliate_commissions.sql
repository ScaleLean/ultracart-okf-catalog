-- Grain: one row per affiliate_ledger_oid.
-- Purpose: affiliate commission events with click context.
SELECT
  affiliate_ledger_oid,
  order_id,
  item_id,
  affiliate_oid,
  affiliate_click_oid,
  affiliate_link_oid,
  transaction_dts,
  DATE(transaction_dts) AS transaction_date,
  transaction_state,
  transaction_amount,
  transaction_amount_paid,
  transaction_percentage,
  click.click_dts,
  click.screen_recording_uuid,
  click.ucacid,
  click.link.code AS affiliate_link_code,
  click.link.name AS affiliate_link_name,
  click.landing_page,
  click.referrer
FROM `{{ source_project }}.{{ access_dataset }}.uc_affiliate_ledgers`;
