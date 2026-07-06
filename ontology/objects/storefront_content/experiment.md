---
type: "Ontology Object"
object: experiment
domain: storefront_content
tier: supporting
resource: "urn:ultracart:ontology:object:experiment"
version: 1
grain: "one A/B experiment per storefront_experiment_oid"
key:
  fields: [storefront_experiment_oid]
  identity_family: storefront_experiment_oid
source:
  binding: uc_storefront_experiments
  default_table: "{{source_project}}.{{dataset.medium}}.uc_storefront_experiments"
properties:
  - name: storefront_experiment_oid
    type: INTEGER
    source: storefront_experiment_oid
    meaning: "primary key for the experiment"
  - name: storefront_oid
    type: INTEGER
    source: storefront_oid
    meaning: "storefront the experiment runs on"
  - name: experiment_id
    type: STRING
    source: id
    meaning: "public experiment id — matches hits.experiment.experiment_id inside analytics sessions"
  - name: container_id
    type: STRING
    source: container_id
    meaning: "experiment container (page/element scope)"
  - name: name
    type: STRING
    source: name
    meaning: "human-facing experiment name"
  - name: experiment_type
    type: STRING
    source: experiment_type
    meaning: "kind of experiment (e.g. URL/content test)"
  - name: objective
    type: STRING
    source: objective
    meaning: "declared objective/metric being optimized"
  - name: objective_parameter
    type: STRING
    source: objective_parameter
    meaning: "parameter qualifying the objective"
  - name: optimization_type
    type: STRING
    source: optimization_type
    meaning: "how traffic is optimized across variations"
  - name: status
    type: STRING
    source: status
    meaning: "raw lifecycle status of the experiment"
  - name: started_at
    type: DATETIME
    source: start_dts
    meaning: "experiment start"
  - name: ended_at
    type: DATETIME
    source: end_dts
    meaning: "experiment end (NULL while running)"
  - name: duration_days
    type: INTEGER
    source: duration_days
    meaning: "planned/actual duration in days"
  - name: equal_weighting
    type: BOOLEAN
    source: equal_weighting
    meaning: "variations receive equal traffic (vs optimized allocation)"
  - name: session_count
    type: INTEGER
    source: session_count
    meaning: "sessions exposed to the experiment"
  - name: p_value
    type: NUMERIC
    source: p_value
    meaning: "current statistical significance of the result"
  - name: p95_sessions_needed
    type: INTEGER
    source: p95_sessions_needed
    meaning: "estimated sessions needed for a 95%-confidence read"
  - name: uri
    type: STRING
    source: uri
    meaning: "URI under test"
  - name: variation_count
    type: INTEGER
    source: "ARRAY_LENGTH(variations)"
    meaning: "number of variations (incl. original)"
  - name: winning_variation_name
    type: STRING
    source: "(SELECT MAX(variations.variation_name) FROM UNNEST(variations) AS variations WHERE variations.winner)"
    meaning: "declared winner, if one has been picked"
  - name: total_revenue
    type: NUMERIC
    source: "(SELECT SUM(variations.revenue) FROM UNNEST(variations) AS variations)"
    meaning: "revenue across all variations"
  - name: total_order_count
    type: INTEGER
    source: "(SELECT SUM(variations.order_count) FROM UNNEST(variations) AS variations)"
    meaning: "orders across all variations"
  - name: openai_model
    type: STRING
    source: openai_model
    meaning: "LLM used when the experiment is AI-iterated (see prose)"
  - name: openai_element_type
    type: STRING
    source: openai_element_type
    meaning: "page element the AI iterates on"
  - name: openai_current_iteration
    type: INTEGER
    source: openai_current_iteration
    meaning: "current AI iteration number"
  - name: openai_total_iterations
    type: INTEGER
    source: openai_total_iterations
    meaning: "planned AI iterations"
  - name: notes
    type: STRING
    source: notes
    meaning: "merchant notes on the experiment"
links:
  - to: storefront
    kind: belongs_to
    on: "experiment.storefront_oid = storefront.storefront_oid"
pii: none
excluded_fields:
  - variations      # per-variation stats structs incl. daily_statistics[] and nested order_ids[]; rollups derived above
  - partition_oid   # warehouse load partition, not a business attribute
consumers: []
---

# Experiment

A storefront A/B experiment: definition, lifecycle, sample size, significance, and
per-variation performance. The canonical view keeps the definition plus cross-variation
rollups (`variation_count`, `winning_variation_name`, `total_revenue`,
`total_order_count`); the `variations[]` array — with per-variation conversion rates,
`daily_statistics[]`, and the linked `order_ids[]` — is excluded and should be modeled
at variation grain if per-arm analysis is ever needed.

Exposure data lives elsewhere: which *sessions* saw which variation is recorded in
`uc_analytics_sessions` under the (excluded) `hits.experiment` events, matching this
object's `experiment_id`. Orders attributable to an arm are inside the excluded
`variations[].daily_statistics[].order_ids[]`.

The `openai_*` fields are a curiosity worth knowing about: UltraCart can run
**AI-iterated experiments**, where an OpenAI model (`openai_model`) rewrites a page
element (`openai_element_type`) for `openai_total_iterations` rounds. When these are
non-NULL the "variations" were machine-generated, which matters when interpreting
winners — the hypothesis space was the model's, not the merchant's. They are NULL for
ordinary hand-built tests.

Gotchas:
- **No `merchant_id` on this table** — no merchant filter is compiled. Scope through
  the `storefront` link (uc_storefronts is merchant-filtered) on multi-merchant
  warehouse projects.
- `p_value` and `p95_sessions_needed` are UltraCart's own running stats; a NULL
  `winning_variation_name` with `status` still open means the test has not been called.
- `session_count` here is experiment-level; per-arm counts are in the excluded array.

## Change log
- v1 (2026-07-06) — initial.
