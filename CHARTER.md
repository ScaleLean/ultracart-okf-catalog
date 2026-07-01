# project_ultracart_okf_catalog

**Owner:** data_warehouse
**Status:** active - public merchant-neutral ScaleLean GitHub repo published with standard OKF catalog
**Primary tool:** Codex
**Current agent:** Codex
**Asana:** -

## Outcome(s) (done = )
The UltraCart BigQuery warehouse OKF toolkit is a merchant-neutral public repository that contains the standard UltraCart warehouse OKF catalog and can generate metadata-only OKF v0.1 bundles for any authorized `ultracart-dw-*` merchant project.

Done means:
- The public repository contains reusable scripts, validation, viewer generation, and a template config.
- The public repository contains the merchant-neutral standard UltraCart warehouse OKF bundle.
- The public repository does not include merchant-specific generated OKF bundles or reports.
- The generator requires an explicit source BigQuery project instead of defaulting to one merchant.
- The active project card points to the public ScaleLean organization repo and states the next useful expansion.

## Next action
Review the standard catalog in GitHub, then decide whether V2 should add curated business-semantics templates for common UltraCart warehouse marts or add a multi-merchant orchestration wrapper that generates reviewed local bundles from a list of authorized `ultracart-dw-*` projects.

## Threads
- Merchant-neutral public repo — done — removed merchant-specific labels and generated merchant bundle output from the public branch.
- Standard warehouse catalog — done — generated the tracked `okf/ultracart_warehouse/` OKF bundle covering 8 standard datasets, 244 standard objects, 112 canonical table definitions, and full live schema paths for all standard objects.
- Single-merchant bundle generation — supported locally — use `configs/ultracart_merchant_template.yml` with an authorized source project.
- Downstream view augmentation — supported locally — pass explicit downstream and billing projects.
- Multi-merchant expansion — parked — requires a deliberate access/cost/sensitivity decision before inspecting multiple merchant projects.

## Time estimate
15-30 min to review the GitHub catalog; 1-2 hr to design the next V2 expansion.

## Context
This project implements an Open Knowledge Format layer for UltraCart BigQuery warehouse projects. It is a reusable catalog/read layer, not a competing source of truth for project status or dbt logic.

Guardrails:
- Do not query or store raw customer rows, raw emails, addresses, payment fields, session payloads, conversation bodies, or sampled rows.
- Generate concept docs from BigQuery metadata only.
- Treat generated bundles as merchant-specific local artifacts unless reviewed for public sharing.

## Log
- 2026-07-01 - Codex - Converted the public repository into a merchant-neutral UltraCart OKF toolkit: removed generated merchant-specific bundle output and reports, replaced the config with an explicit-project template, removed hardcoded merchant defaults from scripts, and prepared the public `main` branch for history rewrite.
- 2026-07-01 - Codex - Added the initial merchant-neutral UltraCart warehouse OKF catalog under `okf/ultracart_warehouse/`, including a static viewer, validation, and a self-test report. Verified no forbidden merchant-specific references in the repo tree or git object store.
- 2026-07-01 - Codex - Mirrored the standard OKF bundle directories to the repository root so GitHub links such as `tables/ultracart_dw_medium/uc_affiliate_clicks.md` resolve directly while preserving `okf/ultracart_warehouse/` for validation and regeneration workflows.
- 2026-07-01 - Codex - Corrected the standard scope by excluding the merchant-specific custom work dataset from the published standard catalog. Regenerated the root and nested bundles at 8 datasets, 244 standard objects, 112 canonical table definitions, and 48,633 flattened schema paths.
