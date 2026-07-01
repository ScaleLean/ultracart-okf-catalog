---
type: "UltraCart Table Definition"
title: "uc_towerdata_email_intelligence"
description: "Customer enrichment and email intelligence surface. Treat as optional and sensitive."
resource: "urn:ultracart:bigquery:table-definition:uc_towerdata_email_intelligence"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "uc_towerdata_email_intelligence"
  - "customers_support"
timestamp: "2026-07-01T00:00:00Z"
---

# uc_towerdata_email_intelligence

Customer enrichment and email intelligence surface. Treat as optional and sensitive.

## Grain

One email intelligence enrichment row.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw` | `VIEW` | [ultracart_dw.uc_towerdata_email_intelligence](/tables/ultracart_dw/uc_towerdata_email_intelligence.md) |
| `ultracart_dw_low` | `VIEW` | [ultracart_dw_low.uc_towerdata_email_intelligence](/tables/ultracart_dw_low/uc_towerdata_email_intelligence.md) |
| `ultracart_dw_medium` | `VIEW` | [ultracart_dw_medium.uc_towerdata_email_intelligence](/tables/ultracart_dw_medium/uc_towerdata_email_intelligence.md) |
| `ultracart_dw_high` | `VIEW` | [ultracart_dw_high.uc_towerdata_email_intelligence](/tables/ultracart_dw_high/uc_towerdata_email_intelligence.md) |

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
| `email` | `STRING` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
