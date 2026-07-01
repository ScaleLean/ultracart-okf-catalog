# UltraCart OKF Catalog

This repository contains a merchant-neutral Open Knowledge Format toolkit for UltraCart BigQuery warehouses. It includes a public standard OKF catalog for the UltraCart warehouse shape, plus scripts that can build metadata-only OKF bundles from live `ultracart-dw-*` BigQuery projects so humans, agents, git review, and static graph viewers can inspect warehouse structure without exposing raw merchant data.

The tracked standard catalog lives at the repository root so GitHub links like `tables/ultracart_dw_medium/uc_orders.md` resolve directly. The same generated bundle is also kept at `okf/ultracart_warehouse/` for local generation and validation workflows. Merchant-specific generated bundles should stay local unless they have been reviewed for the intended audience.

## Standard Catalog

The public standard catalog currently defines:

- 8 standard UltraCart warehouse datasets.
- 244 dataset-specific BigQuery objects.
- 112 canonical table definitions by object name.
- 48,633 flattened schema field paths from live BigQuery schema metadata.
- A self-contained viewer at `viz.html`.

## OKF Workflow

This repository follows the basic OKF adoption path:

1. **Producer:** `scripts/build_ultracart_okf.py` exports a metadata-only OKF bundle from an UltraCart BigQuery warehouse. `scripts/build_standard_okf_catalog.py` builds the public standard catalog from reviewed schema metadata.
2. **Consumer:** `viz.html` and `scripts/build_okf_viewer.py` provide a static bundle viewer. `scripts/audit_agent_usability.py` checks that the bundle is usable by AI agents, search indexes, and other downstream consumers.
3. **Reference implementation:** `scripts/validate_okf_bundle.py` validates bundle structure, and `scripts/self_test_standard_catalog.py` checks the public UltraCart catalog against expected standard-merchant coverage.

The repo also includes [reference BigQuery views](examples/bigquery_views/README.md) that act as practical OKF consumers: they show how an agent or analytics engineer can turn the bundle into safe, reusable base queries and marts.

For dataset group selection, start with [warehouse access layers](references/warehouse_layers.md). It maps UltraCart's standard, low, medium, high, linked-account, and streaming layers to safe reporting use.

Inspect and test the standard catalog with:

```sh
python3 scripts/validate_okf_bundle.py okf/ultracart_warehouse --expect-table-count 244
python3 scripts/self_test_standard_catalog.py okf/ultracart_warehouse
python3 scripts/audit_agent_usability.py
```

## Commands

Copy the template config and fill in your own source and billing projects:

```sh
cp configs/ultracart_merchant_template.yml configs/local.yml
```

Then run:

```sh
python3 scripts/build_ultracart_okf.py --config configs/local.yml --out okf/local_merchant
python3 scripts/validate_okf_bundle.py okf/local_merchant
```

To add downstream view relationships from another BigQuery project:

```sh
python3 scripts/augment_okf_scalelean_views.py okf/local_merchant --project YOUR_DOWNSTREAM_PROJECT --billing-project YOUR_BILLING_PROJECT
python3 scripts/validate_okf_bundle.py okf/local_merchant
```

To regenerate the static viewer only:

```sh
python3 scripts/build_okf_viewer.py okf/local_merchant
```

## Outputs

The tracked standard catalog and generated local bundles normally include:

- `index.md` - bundle entrypoint.
- `datasets/*.md` - one concept per discovered BigQuery dataset.
- `tables/<dataset>/*.md` - one concept per discovered table, view, or materialized view.
- `concepts/tables_by_name/*.md` - canonical table definitions across access layers.
- `references/*.md` - warehouse access, usage, monetary field, sensitivity, and source-metadata references.
- `downstream_views/<project>/` - optional downstream views that reference UltraCart-style sources.
- `viz.html` - self-contained static viewer.

## Safety

The exporter intentionally uses BigQuery metadata APIs through `bq ls` and BigQuery `INFORMATION_SCHEMA` metadata views. It does not run row-level queries, call `sample_rows`, print customer records, store raw UltraCart data, or include full view SQL in generated bundles.

Generated bundles and reports can contain merchant-specific project names, dataset names, table names, and schema field names. Keep generated output local unless it has been reviewed for the audience you intend to share it with.
