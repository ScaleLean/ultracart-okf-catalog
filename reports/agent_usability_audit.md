# Agent Usability Audit

This report checks whether the repository is directly usable by AI agents reading GitHub paths and OKF Markdown concepts.

## Result

PASS

## Coverage

- datasets: 8
- dataset_specific_objects: 244
- canonical_table_definitions: 112
- root_table_docs: 244
- root_concept_docs: 368
- internal_links_checked: 2099
- mirrored_files_checked: 384
- mirror_mismatches: 0
- safety_files_scanned: 812

## Gates

- Root catalog mirror matches the validated nested OKF bundle.
- All root catalog concept pages have parseable OKF frontmatter.
- All internal Markdown links resolve against repository-root GitHub paths.
- Every dataset-specific table page has definition, schema coverage, field paths, query pattern, and references.
- Expected agent entrypoints exist at root-level GitHub paths.
- Safety scan found no merchant-specific forbidden terms or unsafe SELECT star examples.

## Errors

- None.
