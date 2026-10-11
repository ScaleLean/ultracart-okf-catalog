# Offline knowledge trust

The complete catalog remains OKF 0.2 at `okf/ultracart_warehouse/`; root catalog
paths remain its navigation mirror. `knowledge_manifest.json` is a separate
merchant-neutral sidecar, manifest version 1.0, ontology version 0.1. It preserves
resource URNs and per-concept versions. It does not turn the ontology into a
conformant OKF bundle or register any action implementation.

The sidecar records actual generation time, source commit and SHA-256 source
hashes. Hashes describe working-tree bytes; the commit identifies the baseline,
including when reviewed edits have not yet been committed. `source_captured_at`
and `verified_at` remain null because exact capture and current live verification
are unavailable. The catalog's reported July 1 generation date and ontology's
July 6 build/validation record remain historical evidence. No old concept was
marked fresh or verified. A format migration or sidecar rebuild is not capture.

New standard-catalog builds record their actual build time. Optional
`--source-captured-at` reports the caller's capture timestamp without attesting it;
when omitted, capture is unknown. Source input hashes and unverified states are
recorded separately. Original tracked metadata dates and bodies are preserved.

For machine consumption, objects include declared outputs/types, source bindings,
dataset-specific schema paths, key/grain and scope states. Definitions include
explicit outputs/types and object/definition dependencies. Source files are hashed,
including historical schema documents and relevant compiler/validator code.
The `trust` fields separate offline structural checks from unverified semantic
and live trust. Consumers must read `validation_limits`, not infer authority from
process success or a recent generation date.

Offline checks resolve each object's selected dataset, field references, direct
output types, historical source operand types and array unnest fields. They check
identity-family membership, explicit output names and wildcard projections
(including nested modifier forms). The sidecar builder additionally rejects
duplicate object/definition names and URNs, unavailable dependencies and cyclic
definition dependencies before assigning structural trust. Definition output-name
checking uses a limited explicit projection grammar and rejects unsupported forms, including SELECT AS STRUCT/VALUE
modifiers even inside nested expressions. Explicit `refs` on complex
expressions are author declarations. Direct source fields normalize whitespace, comments, individual/whole backtick
quoting and redundant parentheses. They are checked independently of refs, so refs cannot hide missing fields or type
mismatches. Neither refs nor declared output types prove that the SQL expression
is correct. Unclassifiable source shapes fail closed; recognized derived shapes
remain semantic declarations. A shared tokenizer extracts dependencies and rewrites
ontology paths, supporting bare, fully/partially backticked paths and comments or
whitespace around separators. Unsupported path suffixes, prefixes, decorators and
string quoting as table identifiers fail closed. Literal/comment text is preserved
and does not create dependencies. This is a limited grammar, not a general SQL
parser. No SQL is executed or dry-run by these checks.

The validator's default offline selection checks the dataset tier declared in each
object, currently medium. This is a schema-check context, not access approval or a
plugin fallback. With `--config`, dataset selection must be explicit; missing
required fields/types fail. Current-state standard/low/medium/high schemas are
supported. Arbitrary binding overrides, linked datasets, streaming sources and
unknown schemas fail closed. Merchant filters are preserved; they are never
implicitly removed. Six objects currently have no merchant filter and are marked
`unresolved_no_merchant_filter`, rather than assumed single-merchant.

Key uniqueness, current-state grain, tenant isolation, live freshness, permissions,
join cardinality, identity bridge coverage, derived SQL types and PII safety
cannot be established from this evidence. Ordinary compilation therefore refuses
all deployable output. `--offline-preview` emits unverified local review SQL and
`deployable: false` in its manifest. It does not authorize deployment or queries.
Identifiers and definition parameter types are bounded; missing/excluded
dependencies fail before writing output. Preview files belong in private scratch,
never the public catalog. A future validated deployment route needs separately
approved merchant evidence and explicit review of these unresolved properties.

Ledger validation checks canonical name coverage, not exactly-once roles. Link
validation checks target existence, not join expressions/cardinality. PII exclusions
and action approval/idempotency/audit requirements remain declarations. Hash
identities are pseudonymous, not permission to expose row-level output.

Revenue, identity, subscriber and marketing definitions are proposed conventions.
Subscriber pools omit aged-out and unknown-end populations. Marketing reachability
is suppression eligibility, not affirmative consent. Revenue totals remain gross,
current-state and direct-sale by default; currency consistency, merchant timezone,
as-of date and cohort/period policy remain unresolved. Reference SQL examples use
different order-admission and email-identity conventions. No merchant business
policy changes in this update.

Regenerate the sidecar after reviewing changes to its inputs:

```sh
python3 scripts/build_knowledge_manifest.py --out knowledge_manifest.json
python3 scripts/build_knowledge_manifest.py --check knowledge_manifest.json
```

The check validates hashes and contracts, plus a well-formed timezone-aware
`generated_at` timestamp (offset hours below 24 and minutes below 60) and
hexadecimal `source_commit`. It does not require
the historical timestamp or base commit to equal today or the current HEAD. It
does not change generation time or claim fresh warehouse evidence. CI blocks on
unit tests, catalog/conformance checks, ontology offline checks, sidecar integrity
and the usability audit.
