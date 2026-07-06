---
type: "Ontology Object"
object: person_enrichment
domain: enrichment_analytics
tier: supporting
resource: "urn:ultracart:ontology:object:person_enrichment"
version: 1
grain: "one row per enriched person per email_hash (TowerData third-party demographics)"
key:
  fields: [email_hash_b64]
  identity_family: email_hash_b64
source:
  binding: uc_towerdata_email_intelligence
  default_table: "{{source_project}}.{{dataset.medium}}.uc_towerdata_email_intelligence"
properties:
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "person identity (base64 sha256 of normalized email; see identity spine) — the only key on this table"
  - name: age
    type: STRING
    source: age
    meaning: "age bucket (coarse string, not a birthdate)"
  - name: gender
    type: STRING
    source: gender
    meaning: "inferred gender"
  - name: education
    type: STRING
    source: education
    meaning: "education-level bucket"
  - name: occupation
    type: STRING
    source: occupation
    meaning: "occupation category"
  - name: marital_status
    type: STRING
    source: marital_status
    meaning: "marital-status bucket"
  - name: presence_of_children
    type: STRING
    source: presence_of_children
    meaning: "children in household (bucketed)"
  - name: household_income
    type: STRING
    source: household_income
    meaning: "household-income band"
  - name: net_worth
    type: STRING
    source: net_worth
    meaning: "net-worth band"
  - name: home_owner_status
    type: STRING
    source: home_owner_status
    meaning: "own vs rent"
  - name: length_of_residence
    type: STRING
    source: length_of_residence
    meaning: "years at current residence (bucketed)"
  - name: financial_group
    type: STRING
    source: financial_group
    meaning: "TowerData financial cluster (coarse)"
  - name: financial_segment
    type: STRING
    source: financial_segment
    meaning: "TowerData financial sub-segment"
  - name: life_stage_group
    type: STRING
    source: life_stage_group
    meaning: "life-stage cluster (coarse)"
  - name: life_stage_segment
    type: STRING
    source: life_stage_segment
    meaning: "life-stage sub-segment"
  - name: big_spender
    type: STRING
    source: aci.big_spender.value
    meaning: "audience-characteristic flag: big spender"
  - name: deal_seeker
    type: STRING
    source: aci.deal_seeker.value
    meaning: "audience-characteristic flag: deal seeker"
  - name: interest_health_and_wellness
    type: STRING
    source: interests.health_and_wellness
    meaning: "interest bucket: health & wellness"
  - name: interest_beauty
    type: STRING
    source: interests.beauty
    meaning: "interest bucket: beauty"
  - name: interest_cooking
    type: STRING
    source: interests.cooking
    meaning: "interest bucket: cooking"
  - name: interest_pets
    type: STRING
    source: interests.pets
    meaning: "interest bucket: pets"
  - name: interest_sports
    type: STRING
    source: interests.sports
    meaning: "interest bucket: sports"
  - name: interest_travel
    type: STRING
    source: interests.travel
    meaning: "interest bucket: travel"
  - name: interest_discount_shopper
    type: STRING
    source: interests.discount_shopper
    meaning: "interest bucket: discount shopper"
  - name: interest_high_end_brand_buyer
    type: STRING
    source: interests.high_end_brand_buyer
    meaning: "interest bucket: high-end brand buyer"
  - name: email_longevity
    type: INTEGER
    source: eam.longevity
    meaning: "email-address age metric (TowerData EAM)"
  - name: email_popularity
    type: INTEGER
    source: eam.popularity
    meaning: "email-address activity/popularity metric (TowerData EAM)"
  - name: rfm_avg_dollars
    type: STRING
    source: rfm_avg_dollars
    meaning: "TowerData cross-merchant RFM: average order dollars (bucketed string)"
  - name: rfm_online_avg_days
    type: STRING
    source: rfm_online_avg_days
    meaning: "TowerData cross-merchant RFM: average days between online purchases (bucketed string)"
links:
  - to: customer
    kind: belongs_to
    on: "person_enrichment.email_hash_b64 = customer.email_hash_b64"
  - to: marketing_contact
    kind: belongs_to
    on: "person_enrichment.email_hash_b64 = marketing_contact.email_hash_b64"
pii: pseudonymous
excluded_fields: [email]
consumers: []
---

# PersonEnrichment

Third-party (TowerData) demographic and interest enrichment keyed on the email
hash — the person-level *appended* attributes, as opposed to anything observed
in the store. Everything here is a coarse bucket (age bands, income bands,
interest flags), never raw values: no birthdates, no exact income, and the raw
`email` column (present only in permissive tiers) is excluded.

**Canonical surface note:** these demographics exist **twice** in the
warehouse — here (`uc_towerdata_email_intelligence`) and as the ML copy
`ultracart_dw_ml.customer_tower_data` (same attributes, minus raw email, frozen
for feature pipelines). **This object is the canonical surface**; the ML twin
is a peripheral training artifact and should not be modeled or joined for
analytics.

Sensitivity: although pseudonymous, these are inferred personal characteristics
(income, children, marital status). The layer-1 doc flags the table "optional
and sensitive" — treat every use as opt-in, and prefer the coarse group fields
(`financial_group`, `life_stage_group`) over stacking many attributes when a
segment will be acted on.

Latest-row semantics: the base table carries `partition_oid`, but the default
binding (`dataset.medium` tier view) is already current-state — no dedup
required. If a merchant rebinds to a raw/partitioned load, apply the identity-
spine QUALIFY dedup on `email_hash` (latest `partition_oid` wins).

Coverage is partial by nature: only emails TowerData recognizes get a row —
LEFT JOIN from `customer`, and never treat missing enrichment as a signal.

## Change log
- v1 (2026-07-06) — initial.
