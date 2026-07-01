---
type: "Reference"
title: "Warehouse Access Layers"
description: "Official UltraCart BigQuery dataset groups, access levels, and query implications."
resource: "urn:ultracart:okf:reference:warehouse-layers"
tags:
  - "ultracart"
  - "bigquery"
  - "reference"
  - "datasets"
  - "access"
timestamp: "2026-07-01T00:00:00Z"
---

# Warehouse Access Layers

UltraCart BigQuery warehouses expose physical streaming tables plus current-state view datasets. For normal reporting, query the current-state view layer that matches the user's approved data access. Use the streaming layer only for freshness, delete behavior, or view-validation work.

Official UltraCart documentation: https://ultracart.atlassian.net/wiki/spaces/ucdoc/pages/994705409/Data+Warehouse+BigQuery

## Primary access layers

| Dataset | Access level | Reporting use |
|---|---|---|
| `ultracart_dw` | Level 1 - Standard | Current-state reporting views without sensitive information. |
| `ultracart_dw_low` | Level 2 - Low | Current-state reporting views with additional affiliate information while excluding highly restricted identifiers. |
| `ultracart_dw_medium` | Level 3 - Medium | Current-state reporting views with customer PII fields. |
| `ultracart_dw_high` | Level 4 - High | Current-state reporting views with the most restricted affiliate and wholesale customer identifiers. |

`ultracart_dw_medium` is a practical default for many adapter and reporting examples because it includes customer fields used in lifecycle and attribution analysis. Use `ultracart_dw` or `ultracart_dw_low` when the analysis does not need those fields. Use `ultracart_dw_high` only when the restricted fields are explicitly approved and required.

## Linked-account layers

Parent accounts with linked UltraCart accounts can have parallel linked datasets for consolidated reporting across child accounts. These follow the same access-level pattern as the primary datasets, but should only be used when the business question explicitly asks for linked-account rollups.

| Dataset | Access level | Reporting use |
|---|---|---|
| `ultracart_dw_linked` | Level 1 - Standard | Linked-account current-state reporting views. |
| `ultracart_dw_linked_low` | Level 2 - Low | Linked-account low-access reporting views. |
| `ultracart_dw_linked_medium` | Level 3 - Medium | Linked-account medium-access reporting views. |
| `ultracart_dw_linked_high` | Level 4 - High | Linked-account high-access reporting views. |

Linked datasets are not part of this standard catalog unless they are present in the metadata inventory used to generate a bundle.

## Streaming layer

`ultracart_dw_streaming` contains one row per object mutation. It is near-real-time, but it is not the safe grain for ordinary reports because multiple mutation rows can exist for the same business object. The current-state view layers collapse those mutations into the reporting snapshot and remove fields the user is not allowed to access.

## Query implications

- Access level changes the columns a user can see; verify live `INFORMATION_SCHEMA` or `bq show --schema` metadata before claiming a field is unavailable.
- When raw PII is restricted, use available hash fields for joins and deduplication when the business question does not require raw contact data.
- UltraCart BigQuery date-time values are UTC. Convert to the merchant's reporting time zone before grouping by business day, week, or hour.
- UltraCart records are nested hierarchical objects. Use `UNNEST` deliberately and preserve the intended grain to avoid multiplying orders, items, sessions, or affiliate events.
- Cross-project joins are supported by BigQuery when the querying principal has permission to all referenced projects and datasets.
- Helper datasets such as `ultracart_dw_dashboard`, `ultracart_dw_import`, and `ultracart_dw_ml` are implementation or derived layers. Start from the primary current-state datasets unless the use case specifically calls for those helpers.
