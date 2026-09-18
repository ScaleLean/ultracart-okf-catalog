# Agent Usability Audit

This report checks whether the repository is directly usable by AI agents reading GitHub paths and OKF Markdown concepts.

## Result

FAIL

## Coverage

- datasets: 8
- dataset_specific_objects: 244
- canonical_table_definitions: 112
- root_table_docs: 244
- root_concept_docs: 370
- internal_links_checked: 2105
- mirrored_files_checked: 386
- mirror_mismatches: 0
- safety_files_scanned: 889

## Gates

- Root catalog mirror matches the validated nested OKF bundle.
- All root catalog concept pages have parseable OKF frontmatter.
- All internal Markdown links resolve against repository-root GitHub paths.
- Every dataset-specific table page has definition, schema coverage, field paths, query pattern, and references.
- Expected agent entrypoints exist at root-level GitHub paths.
- Safety scan found no merchant-specific forbidden terms or unsafe SELECT star examples.

## Errors

- ontology/definitions/repeat_customer.md: unsafe SELECT star pattern
- ontology/definitions/revenue_order.md: unsafe SELECT star pattern
