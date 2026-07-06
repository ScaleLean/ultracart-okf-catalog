---
type: "Ontology Object"
object: affiliate
domain: affiliates
tier: core
resource: "urn:ultracart:ontology:object:affiliate"
version: 1
grain: "one row per affiliate account per affiliate_oid"
key:
  fields: [affiliate_oid]
  identity_family: affiliate_oid
source:
  binding: uc_affiliates
  default_table: "{{source_project}}.{{dataset.medium}}.uc_affiliates"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: affiliate_oid
    type: INTEGER
    source: affiliate_oid
    meaning: "UltraCart primary key for the affiliate account"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "affiliate contact identity (base64 sha256 of normalized email; see identity spine)"
  - name: status
    type: STRING
    source: status
    meaning: "raw affiliate account status"
  - name: terminated_for_spam
    type: BOOLEAN
    source: terminated_for_spam
    meaning: "kicked out for spamming — exclude from partner outreach"
  - name: member_type
    type: INTEGER
    source: member_type
    meaning: "raw membership type code"
  - name: short_code
    type: STRING
    source: short_code
    meaning: "affiliate short code used in tracking links"
  - name: last_terms_accepted_at
    type: DATETIME
    source: last_terms_acceptance
    meaning: "most recent program-terms acceptance — closest thing to a join/activation timestamp in the warehouse (no signup dts exists)"
  - name: affiliate_commission_group_oid
    type: INTEGER
    source: affiliate_commission_group_oid
    meaning: "commission group defining per-item rates"
  - name: auto_apply_coupon_code
    type: STRING
    source: auto_apply_coupon_code
    meaning: "coupon auto-applied to carts arriving via this affiliate (string-code join to coupon)"
  - name: auto_apply_coupon_oid
    type: INTEGER
    source: auto_apply_coupon_oid
    meaning: "oid of the auto-apply coupon"
  - name: pay_commissions_on_auto_orders
    type: BOOLEAN
    source: pay_commissions_on_auto_orders
    meaning: "earns commission on subscription rebills (LTV-shaping flag)"
  - name: pay_commissions_on_repeat_orders_by_email
    type: BOOLEAN
    source: pay_commissions_on_repeat_orders_by_email
    meaning: "earns commission on any repeat order by the same email"
  - name: auto_approve_commissions
    type: BOOLEAN
    source: auto_approve_commissions
    meaning: "ledger entries skip manual approval"
  - name: payment_adjustment
    type: NUMERIC
    source: payment_adjustment
    meaning: "standing payout adjustment applied at payment time"
  - name: minimum_payout
    type: NUMERIC
    source: minimum_payout
    meaning: "payout threshold before a payment is cut"
  - name: pay_via_paypal
    type: BOOLEAN
    source: pay_via_paypal
    meaning: "paid by PayPal rather than check"
  - name: cookie_ttl
    type: INTEGER
    source: cookie_ttl
    meaning: "attribution cookie lifetime"
  - name: prevent_cookie_stomping
    type: BOOLEAN
    source: prevent_cookie_stomping
    meaning: "first-click keeps attribution (later affiliate clicks don't overwrite)"
  - name: tier_relationship_count
    type: INTEGER
    source: "ARRAY_LENGTH(tier_relationships)"
    meaning: "downline/upline relationships (multi-tier program participation)"
  - name: state
    type: STRING
    source: state
    meaning: "coarse contact geo (state/province)"
  - name: country_code
    type: STRING
    source: country_code
    meaning: "coarse contact geo (country)"
links:
  - to: affiliate_click
    kind: has_many
    on: "affiliate.affiliate_oid = affiliate_click.affiliate_oid"
  - to: affiliate_ledger
    kind: has_many
    on: "affiliate.affiliate_oid = affiliate_ledger.affiliate_oid"
  - to: coupon
    kind: belongs_to
    on: "affiliate.auto_apply_coupon_code = coupon.merchant_code"
pii: pseudonymous
excluded_fields: [email, paypal_email, first_name, last_name, phone, fax, dob, address_1, address_2, company_name, tax_id, check_payable_to, city, postal_code, attributes, marketing_strategy, tier_relationships, salesforce_account_id, salesforce_contact_id]
consumers: []
---

# Affiliate

The affiliate/partner account dimension: who they are (pseudonymously), whether
they're active, and the commission mechanics that shape every downstream ledger
row. Money movements live on `affiliate_ledger`; click traffic on
`affiliate_click`; this object is the slowly-changing config + identity hub.

Commission economics to read together: `pay_commissions_on_auto_orders` and
`pay_commissions_on_repeat_orders_by_email` decide whether an affiliate earns
on the *lifetime* of a referred customer or only the first order — the single
biggest driver of per-affiliate payout differences. `auto_apply_coupon_code`
ties the affiliate to a coupon (string-code join to `coupon.merchant_code`, no
oid on the order side), which is also how affiliate-attributed discounting
shows up on orders.

There is **no signup timestamp** in the warehouse; `last_terms_accepted_at` is
the closest activation proxy (re-acceptance moves it forward).

PII: the raw row carries full contact identity — email, PayPal email, name,
phone, DOB, street address, tax id, `check_payable_to`. All excluded; hash
twins cover identity (`email_hash_b64`) and the rest is not exposed at all.
Note `paypal_email` and `check_payable_to` have **no hash twins** — never
rebind this object to a wider tier without re-checking exclusions.

Latest-row semantics: the base table carries `partition_oid`, but the default
binding (`dataset.medium` tier view) is already current-state — no dedup
needed. Rebinding to a raw/partitioned table re-introduces the identity-spine
QUALIFY dedup obligation on `affiliate_oid`.

## Change log
- v1 (2026-07-06) — initial.
