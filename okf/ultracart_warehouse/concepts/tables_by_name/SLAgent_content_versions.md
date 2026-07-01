---
type: "UltraCart Table Definition"
title: "SLAgent_content_versions"
description: "Imported or legacy segmentation helper object."
resource: "urn:ultracart:bigquery:table-definition:SLAgent_content_versions"
tags:
  - "ultracart"
  - "bigquery"
  - "canonical_table"
  - "SLAgent_content_versions"
  - "import"
timestamp: "2026-07-01T00:00:00Z"
---

# SLAgent_content_versions

Imported or legacy segmentation helper object.

## Grain

Imported helper grain defined by the source import or segmentation view.

## Dataset Occurrences

| Dataset | Object type | Object doc |
|---|---|---|
| `ultracart_dw_import` | `BASE TABLE` | [ultracart_dw_import.SLAgent_content_versions](/tables/ultracart_dw_import/SLAgent_content_versions.md) |

## Field Paths

| Field path | Data type |
|---|---|
| `Body` | `STRING` |
| `Headline` | `STRING` |
| `Note` | `STRING` |
| `Prompt` | `STRING` |
| `content_version` | `STRING` |
| `item_oid` | `STRING` |
| `page_oid` | `STRING` |
| `start_dt` | `DATETIME` |
| `start_dts` | `TIMESTAMP` |

## Notes

Treat the dataset-specific object doc as authoritative for access layer and object type. Treat this canonical definition as the cross-layer business definition for the UltraCart object name.
