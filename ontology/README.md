---
type: "OKF Ontology Index"
title: "UltraCart Store Ontology"
okf_ontology_version: "0.1"
resource: "urn:ultracart:ontology:index"
timestamp: "2026-07-06T00:00:00Z"
---

# UltraCart Store Ontology

A merchant-neutral **semantic layer** over the standard UltraCart BigQuery warehouse:
business objects, links, named definitions, and a governed-actions catalog — compiled
into concrete BigQuery views per merchant from a single config file. This is OKF
layer 2; layer 1 (this repo's catalog) documents tables and fields, the ontology
defines what they *mean* and how a store reasons about them.

**Who it's for:** any UltraCart merchant (or agency running several). One `ontology.*`
dataset per merchant gives agents, dashboards, and analysts the same answer to "who is
an active subscriber," "what counts as revenue," "who can we email" — instead of every
project re-deriving those from 112 tables and 1,000+ field paths.

## Quick start (agents, read in this order)

1. `SPEC.md` — the file formats (5 min; skip if only consuming).
2. `identity/identity_spine.md` — key families, the base64/hex email-hash bridge,
   merchant_id scoping, dedup rules. **Read before writing any query.**
3. `objects/<domain>/` — the object you care about; frontmatter is machine-truth,
   prose has the gotchas.
4. `definitions/` — named definitions (revenue_order, customer, active_subscriber,
   lapsed_subscriber, …). **Never re-derive these in project SQL.**
5. `actions/` — what may be written back, and the guards required.
6. `links/link_graph.md` + `links/coverage_ledger.md` — generated indexes: the join
   graph, and every warehouse table's ontology role.

## Instantiating for a merchant

```bash
cp config/merchant_ontology_template.yml config/local/<merchant>.yml   # fill in
python3 scripts/validate_ontology.py --offline                        # no auth needed
python3 scripts/compile_ontology.py --config config/local/<merchant>.yml
bq query --project_id=<billing> --use_legacy_sql=false < build/<merchant>/ontology_views.sql
python3 scripts/validate_ontology.py --compiled config/local/<merchant>.yml
```

Merchant overlays may **rebind** an object to their own model (e.g. a view that
unifies Amazon + UltraCart orders) without changing the property contract — see
`bindings:` in the config template.

## How big is the warehouse, really?

Don't let the object count mislead you. The catalog lists **244 objects / 112 canonical
names**, but that is heavily inflated:

- **~44 real business tables** (orders, customers, items, auto-orders, coupons, sessions,
  support, affiliates, …) — the actual source entities.
- Each appears at **4 permission tiers** (`dw` / `low` / `medium` / `high`, increasing PII
  exposure) — that's ~176 objects that are really the same ~44 tables.
- **+44 streaming twins** — a change-feed copy (`*_streaming`) of each entity.
- **+19 ML outputs** (some with a merchant id baked into the name) and **~5** dashboard/import.

So the real distinct-entity count is **~44**, which this ontology distills to **28 business
objects** worth modeling. When describing the warehouse, say "~44 real tables across
permission tiers," not "112 tables."

## Domains

commerce_core · subscriptions · catalog · promotions · marketing_comms ·
storefront_behavior · storefront_content · support_conversations · affiliates ·
risk_finance · fulfillment_ops · enrichment_analytics
(platform plumbing — streaming twins, logs, ML feature tables — is documented in the
coverage ledger, deliberately not modeled as objects).

## Design commitments

- **Hash-keyed identity everywhere** (`email_hash_b64`); raw PII is never selected —
  the compiled views are safe at every dataset tier, including the redacted ones.
- **Compiled SQL only** — object files are the single source of truth; hand-edited
  merchant SQL is a spec violation.
- **Offline drift detection** — every property mapping is validated against layer-1
  field paths without BigQuery credentials; when UltraCart changes the warehouse,
  regenerate layer 1 and the validator pinpoints every broken mapping.
- **Declared ≠ permitted** — the actions catalog documents the API's full mutation
  surface; executing anything requires a merchant-registered implementation with
  guards (see `actions/README.md`).

## Maintenance

- After editing objects: `python3 scripts/generate_indexes.py && python3 scripts/validate_ontology.py --offline`
- After an UltraCart warehouse schema refresh (layer-1 regeneration): run the offline
  validator; it lists every mapping the change broke.
- Version bumps + change-log lines per file for breaking changes (see SPEC).

## Provenance

Built 2026-07-06 from: OKF layer-1 field paths (112 canonical tables), UltraCart's
live OpenAPI spec (446 paths; actions catalog), UltraCart's BigQuery DW documentation,
and verified live-merchant findings (identity bridge, paused-pool semantics). Assembled
by Claude (Fable) with subagent mining; see the workspace charter for the build log.
