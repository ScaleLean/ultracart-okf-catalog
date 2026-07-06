---
type: "Ontology Object"
object: affiliate_click
domain: affiliates
tier: supporting
resource: "urn:ultracart:ontology:object:affiliate_click"
version: 1
grain: "one row per affiliate click event per affiliate_click_oid"
key:
  fields: [affiliate_click_oid]
  identity_family: affiliate_click_oid
source:
  binding: uc_affiliate_clicks
  default_table: "{{source_project}}.{{dataset.medium}}.uc_affiliate_clicks"
properties:
  - name: affiliate_click_oid
    type: INTEGER
    source: affiliate_click_oid
    meaning: "UltraCart primary key for the click event"
  - name: affiliate_oid
    type: INTEGER
    source: affiliate_oid
    meaning: "affiliate credited with the click"
  - name: affiliate_link_oid
    type: INTEGER
    source: affiliate_link_oid
    meaning: "tracking link that was clicked"
  - name: clicked_at
    type: DATETIME
    source: click_dts
    meaning: "when the click happened"
  - name: landing_page
    type: STRING
    source: landing_page
    meaning: "landing page URL"
  - name: landing_page_query_string
    type: STRING
    source: landing_page_query_string
    meaning: "landing page query string (raw campaign params)"
  - name: referrer
    type: STRING
    source: referrer
    meaning: "HTTP referrer of the click"
  - name: referrer_query_string
    type: STRING
    source: referrer_query_string
    meaning: "referrer query string"
  - name: sub_id
    type: STRING
    source: sub_id
    meaning: "affiliate-supplied sub-id (their own campaign/placement tag)"
  - name: screen_recording_uuid
    type: STRING
    source: screen_recording_uuid
    meaning: "behavioral session that carried the click (bridge to screen_recording)"
  - name: ucacid
    type: STRING
    source: ucacid
    meaning: "UltraCart analytics client id (bridge to analytics_session visitor)"
  - name: link_code
    type: STRING
    source: link.code
    meaning: "tracking link code"
  - name: link_name
    type: STRING
    source: link.name
    meaning: "merchant-facing link name"
  - name: link_type
    type: STRING
    source: link.type
    meaning: "link type (standard / managed / invisible ...)"
links:
  - to: affiliate
    kind: belongs_to
    on: "affiliate_click.affiliate_oid = affiliate.affiliate_oid"
  - to: screen_recording
    kind: belongs_to
    on: "affiliate_click.screen_recording_uuid = screen_recording.screen_recording_uuid"
  - to: analytics_session
    kind: belongs_to
    on: "affiliate_click.ucacid = analytics_session.ucacid"
  - to: affiliate_ledger
    kind: has_many
    on: "affiliate_click.affiliate_click_oid = affiliate_ledger.affiliate_click_oid"
pii: pseudonymous
excluded_fields: [ip_address, link.custom_html]
consumers: []
---

# AffiliateClick

Top of the affiliate funnel: one row per tracked click on an affiliate link,
with the landing/referrer context and — crucially — two bridges into the
behavioral domain: `screen_recording_uuid` (the session recording) and
`ucacid` (the analytics visitor). Click → session → order is how affiliate
traffic quality gets audited beyond raw commission counts.

Attribution flow: a click sets the affiliate cookie; if a purchase follows
within the cookie window, an `affiliate_ledger` row is written pointing back at
this click (`affiliate_ledger.affiliate_click_oid`). Clicks with no ledger rows
are unconverted traffic. `sub_id` is the affiliate's own campaign tag — the
grain at which partners want performance reported back.

**Tenant scoping:** this table has **no `merchant_id`** column, so the object
declares no merchant filter. Scope by joining `affiliate` (which is merchant-
filtered) on `affiliate_oid` — never treat unfiltered click counts as
merchant-scoped in a multi-merchant warehouse project.

Gotchas:
- `ip_address` is the only PII on the row (no hash twin) — excluded.
- The `link` struct is a config snapshot at click time; only its stable
  descriptors (code/name/type) are surfaced. `link.custom_html` (arbitrary
  affiliate HTML) is excluded.

## Change log
- v1 (2026-07-06) — initial.
