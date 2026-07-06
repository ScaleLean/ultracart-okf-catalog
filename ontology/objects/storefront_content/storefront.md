---
type: "Ontology Object"
object: storefront
domain: storefront_content
tier: supporting
resource: "urn:ultracart:ontology:object:storefront"
version: 1
grain: "one storefront (host) per storefront_oid"
key:
  fields: [storefront_oid]
  identity_family: storefront_oid
source:
  binding: uc_storefronts
  default_table: "{{source_project}}.{{dataset.medium}}.uc_storefronts"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: storefront_oid
    type: INTEGER
    source: storefront_oid
    meaning: "primary key; the hub for storefront_oid FKs across pages, experiments, upsells, recordings, ML registries"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: host_name
    type: STRING
    source: host_name
    meaning: "canonical host — THE join key from orders/carts: checkout.storefront_host_name matches this string, not the oid"
  - name: host_alias1
    type: STRING
    source: host_alias1
    meaning: "alternate host alias 1 (order host strings may match an alias instead of host_name)"
  - name: host_alias2
    type: STRING
    source: host_alias2
    meaning: "alternate host alias 2"
  - name: host_alias3
    type: STRING
    source: host_alias3
    meaning: "alternate host alias 3"
  - name: host_alias4
    type: STRING
    source: host_alias4
    meaning: "alternate host alias 4"
  - name: host_alias5
    type: STRING
    source: host_alias5
    meaning: "alternate host alias 5"
  - name: redirect_aliases
    type: BOOLEAN
    source: redirect_aliases
    meaning: "aliases 301-redirect to the canonical host (if true, order host strings should equal host_name)"
  - name: locked
    type: BOOLEAN
    source: locked
    meaning: "storefront is locked/gated"
links:
  - to: order
    kind: has_many
    on: "order.storefront_host_name = storefront.host_name"
  - to: cart_abandon
    kind: has_many
    on: "cart_abandon.storefront_host_name = storefront.host_name"
  - to: experiment
    kind: has_many
    on: "experiment.storefront_oid = storefront.storefront_oid"
  - to: screen_recording
    kind: has_many
    on: "screen_recording.storefront_oid = storefront.storefront_oid"
pii: none
excluded_fields:
  - unlock_password   # live credential for locked storefronts — leaks through analytics views; never expose
  - partition_oid     # warehouse load partition, not a business attribute
consumers: []
---

# Storefront

The sales-channel dimension: one row per storefront host within a merchant account.
Small table, big join surface — nearly every content/behavior table
(`uc_storefront_pages`, `uc_storefront_experiments`, upsell offers/paths, heatmaps,
screen recordings, even the ML dataset/model registries) hangs off `storefront_oid`.

**The join that bites:** orders and cart abandons do *not* carry `storefront_oid`.
They record `checkout.storefront_host_name` as a **string**, which must be matched
against `host_name` — and, when `redirect_aliases` is false, potentially against any
of `host_alias1..5`. A robust order→storefront bridge checks all six columns; the
canonical link above uses the common case (`host_name`) and the aliases are exposed
precisely so merchant overlays can widen the match.

**Security note — why `unlock_password` is excluded.** The source view stack exposes
`unlock_password` (the passcode for `locked` storefronts) all the way down into the
analytics tiers. It is a live credential, not analytics data: the canonical object
must never select it, and anything rebinding this object should re-verify the
exclusion. Treat any query result containing it as an incident, not a curiosity.

Gotchas:
- Alias columns are sparse (mostly NULL); do not use them as identity — `host_name` is
  the canonical label, `storefront_oid` the key.
- Multi-storefront merchants: per-storefront revenue cuts require the string join above;
  getting zero rows usually means the order host string matched an alias, not host_name.

## Change log
- v1 (2026-07-06) — initial.
