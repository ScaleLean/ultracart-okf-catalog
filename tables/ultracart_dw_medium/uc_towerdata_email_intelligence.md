---
type: "BigQuery View"
title: "ultracart_dw_medium.uc_towerdata_email_intelligence"
description: "Customer enrichment and email intelligence surface. Treat as optional and sensitive."
resource: "urn:ultracart:bigquery:object:ultracart_dw_medium.uc_towerdata_email_intelligence"
tags:
  - "ultracart"
  - "bigquery"
  - "view"
  - "ultracart_dw_medium"
  - "uc_towerdata_email_intelligence"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# ultracart_dw_medium.uc_towerdata_email_intelligence

Customer enrichment and email intelligence surface. Treat as optional and sensitive.

## Definition

- Dataset: [ultracart_dw_medium](/datasets/ultracart_dw_medium.md)
- Object name: `uc_towerdata_email_intelligence`
- Object type: `VIEW`
- Table family: [customers_support](/references/table_families.md#customers-support)
- Grain: One email intelligence enrichment row.
- Canonical definition: [uc_towerdata_email_intelligence](/concepts/tables_by_name/uc_towerdata_email_intelligence.md)

## Schema Coverage

- Field paths: 53
- Array fields: 0
- Struct fields: 5

## Field Paths

| Field path | Data type |
|---|---|
| `aci` | `STRUCT` |
| `aci.big_spender` | `STRUCT` |
| `aci.big_spender.value` | `STRING` |
| `aci.deal_seeker` | `STRUCT` |
| `aci.deal_seeker.value` | `STRING` |
| `age` | `STRING` |
| `eam` | `STRUCT` |
| `eam.dateFirstSeen` | `STRING` |
| `eam.longevity` | `INTEGER` |
| `eam.month_last_open` | `STRING` |
| `eam.popularity` | `INTEGER` |
| `eam.velocity` | `INTEGER` |
| `education` | `STRING` |
| `email` | `STRING` |
| `email_hash` | `STRING` |
| `financial_group` | `STRING` |
| `financial_segment` | `STRING` |
| `gender` | `STRING` |
| `home_owner_status` | `STRING` |
| `household_income` | `STRING` |
| `interests` | `STRUCT` |
| `interests.arts_and_crafts` | `STRING` |
| `interests.automotive` | `STRING` |
| `interests.baby_product_buyer` | `STRING` |
| `interests.beauty` | `STRING` |
| `interests.blogging` | `STRING` |
| `interests.books` | `STRING` |
| `interests.business` | `STRING` |
| `interests.charitable_donors` | `STRING` |
| `interests.cooking` | `STRING` |
| `interests.discount_shopper` | `STRING` |
| `interests.health_and_wellness` | `STRING` |
| `interests.high_end_brand_buyer` | `STRING` |
| `interests.home_and_garden` | `STRING` |
| `interests.home_improvement` | `STRING` |
| `interests.luxury_goods` | `STRING` |
| `interests.magazine_buyer` | `STRING` |
| `interests.news_and_current_events` | `STRING` |
| `interests.outdoor_and_adventure` | `STRING` |
| `interests.pets` | `STRING` |
| `interests.sports` | `STRING` |
| `interests.technology` | `STRING` |
| `interests.travel` | `STRING` |
| `length_of_residence` | `STRING` |
| `life_stage_group` | `STRING` |
| `life_stage_segment` | `STRING` |
| `marital_status` | `STRING` |
| `net_worth` | `STRING` |
| `occupation` | `STRING` |
| `partition_oid` | `INTEGER` |
| `presence_of_children` | `STRING` |
| `rfm_avg_dollars` | `STRING` |
| `rfm_online_avg_days` | `STRING` |

## Query Pattern

```sql
SELECT
  COUNT(1) AS row_count
FROM `{{ source_project }}.ultracart_dw_medium.uc_towerdata_email_intelligence`;
```

Use explicit field lists and time, storefront, status, or business-key filters when querying large behavioral, streaming, or customer-support objects.

## References

- [BigQuery usage patterns](/references/bigquery_usage.md)
- [Source coverage](/references/source_coverage.md)
