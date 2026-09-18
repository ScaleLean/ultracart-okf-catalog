# OKF 0.2 migration

## Authority

- Upstream: https://github.com/GoogleCloudPlatform/open-knowledge-format
- Version: **0.2**, from `SPEC.md`, sections 11 through 13.
- Commit: `ad30107c31c06aec8a7d5636e0d1058118604e6f`.
- Specification: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/ad30107c31c06aec8a7d5636e0d1058118604e6f/SPEC.md
- Reference validator: `src/reference_agent/bundle/document.py` at the same commit.
- The remote `main` SHA matched this pin during the migration.
- Catalog repository: https://github.com/ScaleLean/ultracart-okf-catalog

## Changes

The migration converts each catalog `timestamp` to `generated.at`.
It records `process:build_standard_okf_catalog` as the known producer.
It preserves the original timestamp. A format conversion does not prove fresh warehouse metadata.
It does not add `verified`, human approval, freshness deadlines, or attested computations.
All catalog concepts remain unverified.

The root version declaration, merchant configuration template, and source summary now use `0.2`.
A headless Chromium check passed for loading, search, concept selection, trust display, generation time, and dataset filtering.
The viewer reported no JavaScript errors during these checks.
The nested bundle and root mirror remain byte-identical.
The shared YAML parser supports nested mappings, lists, and unknown extension fields.
The producer writers convert legacy citation sections to `sources`.
The standard catalog has no legacy citation sections to convert.
Its existing body reference sections remain unchanged.

The viewer preserves structured frontmatter and displays sources, generation time, trust, lifecycle, and staleness.
The viewer still accepts legacy timestamps for older bundles.
It escapes embedded JSON against HTML script termination.

The local validator has two modes:

- Default: UltraCart producer quality gates, link checks, safety checks, and coverage checks.
- `--conformance-only`: specification section 11. Optional fields, unknown types, and broken links do not cause rejection.

Only `okf/ultracart_warehouse/` is the complete OKF bundle.
The root catalog is a navigation mirror within a larger repository.
Repository guidance, migration documentation, reports, and ontology documents are outside the bundle.

## Preservation evidence

The baseline manifest comes from the original committed catalog, not new warehouse queries.
The tests compare all 370 concept bodies and all original frontmatter values after reversing the timestamp conversion.
The tests also compare the complete source summary, except the declared format version.
The manifest stores SHA-256 digests as decimal integers to avoid false positives in the existing substring safety scan.

The preserved catalog contains 8 datasets, 244 dataset-specific objects, and 112 canonical definitions.
No concept IDs, schema fields, links, body content, or recorded source dates change.
No live BigQuery commands ran during this migration.

## Reproducible checks

```sh
python3 -m pip install -r requirements.txt
python3 scripts/migrate_okf_02.py
python3 scripts/validate_okf_bundle.py okf/ultracart_warehouse --expect-table-count 244
python3 scripts/validate_okf_bundle.py okf/ultracart_warehouse --conformance-only
python3 scripts/self_test_standard_catalog.py okf/ultracart_warehouse
python3 -m unittest discover -s tests -v
python3 scripts/audit_agent_usability.py
```

The migration uses only tracked metadata and is idempotent.
Run it twice. The second run reports zero changed Markdown files.
The private source CSV exports are not in this repository.
Use the migration script to reproduce this format-only change without those exports.
The tests exercise the serialization path in all three producer scripts without network access.

To run the authoritative document validator:

```sh
git clone https://github.com/GoogleCloudPlatform/open-knowledge-format /tmp/okf-reference
git -C /tmp/okf-reference checkout ad30107c31c06aec8a7d5636e0d1058118604e6f
python3 scripts/validate_upstream_okf.py /tmp/okf-reference okf/ultracart_warehouse
```

The wrapper checks the upstream commit before it imports the reference implementation.
The local conformance check separately tests reserved index and log files.
CI runs the same offline tests and the pinned upstream validator.
CI also runs the full usability audit as a non-blocking step because of the known baseline defects below.

## Baseline and remaining issues

Before the migration, bundle validation and the standard self-test passed.
The agent-usability audit failed on these existing SQL wildcard projections:

- `ontology/definitions/repeat_customer.md`
- `ontology/definitions/revenue_order.md`

The same two audit failures remain. This migration does not change ontology semantics or weaken the audit.
Review those projections in separate ontology work.

The Notion governance page required sign-in. Its private instructions were unavailable.
No Notion records, governance text, or ownership settings changed.
No new task records were created.
