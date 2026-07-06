---
type: "Ontology Validation Record"
resource: "urn:ultracart:ontology:validation"
timestamp: "2026-07-06T00:00:00Z"
---

# Validation record

## 2026-07-06 — v0.1 initial build

**Offline** (`scripts/validate_ontology.py --offline`): PASS, 0 failures —
28 objects checked against OKF layer-1 field paths; 7 definitions; 17 actions;
79 links; coverage ledger total over all 112 canonical tables.

**Live** (first merchant instance, read-only BigQuery dry-runs): PASS —
the config-compiled output (35 view statements: 28 objects + 7 definitions,
definitions dependency-inlined) was dry-run against a production UltraCart
warehouse. All 35 validated with zero errors on the first full run. Merchant
identifiers are kept out of this public record; the merchant-side evidence lives
in that merchant's own workspace.

Notes from the live pass:
- The `dataset.medium` default binding proved PII-safe and complete: every bound
  field path resolved in the medium tier.
- Definitions compiled in correct dependency order (`revenue_order` → `customer`
  → `repeat_customer`).
- Bytes-processed estimates ranged from ~24 KB (coupons) to ~2.9 GB (order-scan
  definitions) — consumers should prefer object views over re-scanning
  definitions where possible.
