---
type: "BigQuery View"
title: "ultracart_dw_high.uc_affiliates"
description: "Affiliate dimension and affiliate account metadata."
resource: "urn:ultracart:bigquery:object:ultracart_dw_high.uc_affiliates"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_high"
  - "uc_affiliates"
  - "affiliate_commissions"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_high.uc_affiliates

Affiliate dimension and affiliate account metadata.

## Definition

- Dataset: [ultracart_dw_high](/datasets/ultracart_dw_high.md)
- Object name: `uc_affiliates`
- Object type: `VIEW`
- Table family: [affiliate_commissions](/references/table_families.md#affiliate-commissions)
- Grain: One affiliate row per affiliate_oid.
- Canonical definition: [uc_affiliates](/concepts/tables_by_name/uc_affiliates.md)

## Schema Coverage

- Field paths: 79
- Array fields: 2
- Struct fields: 3

## Field Paths

| Field path | Data type |
|---|---|
| `accepted_downline_recruiting_terms` | `BOOLEAN` |
| `address_1` | `STRING` |
| `address_1_hash` | `STRING` |
| `address_2` | `STRING` |
| `address_2_hash` | `STRING` |
| `affiliate_commission_group_oid` | `INTEGER` |
| `affiliate_oid` | `INTEGER` |
| `allow_downline_recruiting` | `BOOLEAN` |
| `allow_google_adwords_tracking` | `BOOLEAN` |
| `allow_yahoo_search_marketing_tracking` | `BOOLEAN` |
| `analytics_internal_tracking` | `BOOLEAN` |
| `attributes` | `ARRAY<STRUCT>` |
| `attributes.name` | `STRING` |
| `attributes.type` | `STRING` |
| `attributes.value` | `STRING` |
| `auto_apply_coupon_code` | `STRING` |
| `auto_apply_coupon_oid` | `INTEGER` |
| `auto_approve_commissions` | `BOOLEAN` |
| `check_payable_to` | `STRING` |
| `city` | `STRING` |
| `company_name` | `STRING` |
| `company_name_hash` | `STRING` |
| `cookie_ttl` | `INTEGER` |
| `country_code` | `STRING` |
| `dob` | `DATETIME` |
| `dob_hash` | `STRING` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `email_notification_schedule` | `STRING` |
| `fax` | `STRING` |
| `fax_hash` | `STRING` |
| `first_name` | `STRING` |
| `first_name_hash` | `STRING` |
| `google_conversion_id` | `STRING` |
| `html_permitted` | `BOOLEAN` |
| `last_name` | `STRING` |
| `last_name_hash` | `STRING` |
| `last_terms_acceptance` | `DATETIME` |
| `marketing_strategy` | `STRUCT` |
| `marketing_strategy.marketing_strategy` | `STRING` |
| `marketing_strategy.using_ad_network` | `BOOLEAN` |
| `marketing_strategy.using_adware` | `BOOLEAN` |
| `marketing_strategy.using_blog` | `BOOLEAN` |
| `marketing_strategy.using_other` | `STRING` |
| `marketing_strategy.using_per_acquisition` | `BOOLEAN` |
| `marketing_strategy.using_ppc` | `BOOLEAN` |
| `marketing_strategy.using_seo` | `BOOLEAN` |
| `marketing_strategy.using_website` | `BOOLEAN` |
| `marketing_strategy.website_name` | `STRING` |
| `marketing_strategy.website_url` | `STRING` |
| `member_type` | `INTEGER` |
| `merchant_id` | `STRING` |
| `minimum_payout` | `NUMERIC` |
| `partition_oid` | `INTEGER` |
| `pay_commissions_on_auto_orders` | `BOOLEAN` |
| `pay_commissions_on_repeat_orders_by_email` | `BOOLEAN` |
| `pay_via_paypal` | `BOOLEAN` |
| `payment_adjustment` | `NUMERIC` |
| `paypal_email` | `STRING` |
| `phone` | `STRING` |
| `phone_hash` | `STRING` |
| `postal_code` | `STRING` |
| `prevent_cookie_stomping` | `BOOLEAN` |
| `prevent_sending_all_emails` | `BOOLEAN` |
| `refund_server_to_server_postback_url` | `STRING` |
| `remove_cookie_after_purchase` | `BOOLEAN` |
| `salesforce_account_id` | `STRING` |
| `salesforce_contact_id` | `STRING` |
| `server_to_server_postback_url` | `STRING` |
| `short_code` | `STRING` |
| `state` | `STRING` |
| `status` | `STRING` |
| `tax_id` | `STRING` |
| `tax_id_hash` | `STRING` |
| `terminated_for_spam` | `BOOLEAN` |
| `tier_relationships` | `ARRAY<STRUCT>` |
| `tier_relationships.affiliate_oid` | `INTEGER` |
| `tier_relationships.tier_number` | `INTEGER` |
| `ysm_account_id` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_high.uc_affiliates`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
