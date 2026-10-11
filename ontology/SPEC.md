---
type: "OKF Ontology Specification"
title: "UltraCart Store Ontology — Format Specification"
okf_ontology_version: "0.1"
resource: "urn:ultracart:ontology:spec"
timestamp: "2026-07-06T00:00:00Z"
---

# UltraCart Store Ontology — Format Specification v0.1

The ontology is OKF layer 2. Layer 1 (the existing catalog) answers *"what tables and
fields exist?"* Layer 2 answers *"what business things exist, how do they relate, what
do words mean, and what may be done to them?"* It is merchant-neutral: everything
merchant-specific arrives through a config file at compile time.

## Design principles

1. **One file per concept, machine-complete frontmatter, human prose below.** Agents load
   the index, then only the files they need. The YAML alone must be sufficient to compile
   SQL; the prose alone must be sufficient for a human to understand the concept.
2. **SQL is compiled, never hand-written per merchant.** Object files declare property
   *source expressions* over named table bindings; `scripts/compile_ontology.py` +
   a merchant config emit the DDL. Hand-edited merchant SQL is a spec violation.
3. **Identity is first-class.** Key families, hash encodings, and cross-system bridges
   live in `identity/identity_spine.md` and are referenced, not restated.
4. **Total coverage, explicit tiers.** Every canonical warehouse table appears in
   `links/coverage_ledger.md` by name: as an object's primary source, a property/link
   source, or an explicitly-documented peripheral. Nothing is silently dropped.
5. **Actions are declared even when not implemented.** The base ships the catalog of
   *possible* governed writes (mapped to UltraCart REST API v2); merchants register
   implementations with guards. Declared ≠ permitted.
6. **Offline validation.** Source field references must resolve against the selected
   dataset-specific historical schema (`tables/<dataset>/`). Direct output types
   and source operand types are checked; derived expression types remain declarations.
   This detects recorded differences, not live drift.

## File format — object (`objects/<domain>/<name>.md`)

```yaml
---
type: "Ontology Object"
object: auto_order                    # snake_case singular
domain: subscriptions                 # one of the domain set in README
tier: core                            # core | supporting
resource: "urn:ultracart:ontology:object:auto_order"
version: 1
grain: "one row per auto-order (subscription container)"
key:
  fields: [auto_order_oid]
  identity_family: auto_order_oid     # -> identity/identity_spine.md
source:
  binding: uc_auto_orders             # -> bindings in this file or config override
  default_table: "{{source_project}}.{{dataset.medium}}.uc_auto_orders"
  merchant_filter: "merchant_id = '{{merchant_id}}'"   # omit if table has no merchant_id
  # optional, for objects whose grain is a nested array of the bound table:
  # unnest: {field: items, alias: item}  # FROM `<table>`, UNNEST(items) AS item
properties:                           # ordered; compiler emits SELECT in this order
  - name: auto_order_oid
    type: INTEGER
    source: auto_order_oid            # SQL expression over the bound table
    meaning: "UltraCart primary key"
  - name: status
    type: STRING
    source: status
    meaning: "raw lifecycle status"
    enum_ref: auto_order_status       # -> enums section below or identity file
  - name: is_live
    type: BOOLEAN
    source: "status IN ('active','paused')"
    meaning: "derived: still enrolled"
  - name: all_items_paused                # complex expression: declare refs explicitly
    type: BOOLEAN
    source: "(SELECT LOGICAL_AND(COALESCE(i.paused, FALSE)) FROM UNNEST(items) AS i)"
    refs: [items.paused]                  # validator checks these instead of parsing the SQL
links:
  - to: customer
    kind: belongs_to
    on: "email_hash_b64"              # join expression in identity-spine terms
  - to: order
    kind: originated_from
    on: "original_order_id = order.order_id"
enums:
  auto_order_status: [active, paused, canceled, disabled, completed]
pii: none | pseudonymous | contains_pii   # if contains_pii: list excluded_fields
excluded_fields: [credit_card, billing.*]  # fields the canonical view must never expose
consumers: []                          # filled in as things adopt the object
---
# AutoOrder
<prose: what it IS in business terms, lifecycle, gotchas, worked examples>
```

## File format — named definition (`definitions/<name>.md`)

Same envelope; adds `parameters:` (name, default, meaning) and `sql:` (a full SELECT
template over **ontology objects**, not raw tables). Example parameter:
`lapsed_window_days: 730`. Merchant configs may override parameters; the compiler
substitutes them. Definitions compile to views named `{{ontology_dataset}}.<name>`.

## File format — action (`actions/<family>/<name>.md`)

```yaml
---
type: "Ontology Action"
action: pause_auto_order
family: auto_order
object: auto_order
resource: "urn:ultracart:ontology:action:pause_auto_order"
api:
  method: PUT
  path: /auto_order/auto_orders/{auto_order_oid}
  effect: "sets item pause state / next attempt date"
  docs: <URL>
mutates: [auto_order.status, auto_order.next_attempt_date]
risk: low | medium | high             # high = touches money or outbound contact
required_guards:                      # template a merchant implementation MUST satisfy
  - idempotency_key
  - audit_row (action, actor, dry_run, payload)
  - approval_gate if risk >= medium
status: declared                      # declared | registered:<merchant>
---
<prose: semantics, failure modes, UltraCart quirks>
```

## Merchant config (`config/merchant_ontology_template.yml`)

Declares: `merchant_id`, `source_project`, dataset tier names, `ontology_project`,
`ontology_dataset`, optional `bindings:` overrides (
table, e.g. a merchant unified view), optional `parameters:` overrides, optional `exclude_objects:`.
Binding overrides are rejected offline: arbitrary views cannot establish tenant
scope, current-state grain or expression types. Supported dataset selections use
their own historical schemas, never the canonical cross-tier union. No filter is
removed implicitly. Missing declared grain/key or required fields/types fail the
structural checks. Declared keys do not prove uniqueness.

## Compiler & validator

- `scripts/compile_ontology.py --config <yml>` refuses deployable compilation:
  historical schemas cannot establish scope, uniqueness or derived SQL semantics.
- With `--offline-preview --out <scratch>`, it emits local unverified review SQL
  and a versioned manifest. Identifiers and parameter types are bounded; unsupported
  bindings and unavailable definition dependencies fail before output is written.
- `scripts/validate_ontology.py --offline [--config <yml>]` checks required object
  frontmatter, object URN uniqueness, link target existence, ledger name coverage,
  selected-dataset field/type references, identity-family membership and explicit
  definition output names/dependencies. It rejects wildcard projections.
- Link cardinality, exactly-once ledger roles, derived SQL types, PII safety, identity
  join coverage and merchant business approval are **not** established offline.
- The existing `--compiled` route needs auth and is outside offline validation;
  the compiler currently refuses its deployable output for the reasons above.
- Definition `outputs:` maps explicit output names to declared BigQuery types.
  These are structural declarations, not semantic attestation. See the sidecar and
  [offline trust limits](../docs/offline-trust.md) for the machine contract.

## Versioning

`version:` per file; breaking changes (key change, property removal/retype) bump the
version and must be logged in the file's prose under `## Change log`. The spec itself
carries `okf_ontology_version`.
