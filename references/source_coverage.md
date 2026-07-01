---
type: "Reference"
title: "Source Coverage"
description: "Metadata-only evidence used to build the standard UltraCart warehouse OKF bundle."
resource: "urn:ultracart:okf:reference:source-coverage"
tags:
  - "ultracart"
  - "bigquery"
  - "reference"
  - "coverage"
timestamp: "2026-07-01T00:00:00Z"
---

# Source Coverage

This bundle was built from metadata-only evidence: dataset/object inventory, field-count metadata, and field-path metadata where available. It does not store row data, sampled records, customer values, merchant project IDs, billing project IDs, or view SQL.

Merchant-specific custom view/work areas are intentionally excluded from the standard catalog because they are not part of the shared UltraCart warehouse shape.

- Datasets represented: 8
- BigQuery objects represented: 244
- Objects with field-count evidence: 244
- Canonical table names with field-path rows: 112

Field-path evidence is attached by UltraCart object name and reused by canonical docs. Dataset-specific access layers may expose different field subsets; verify against live BigQuery metadata before making access-control claims.
