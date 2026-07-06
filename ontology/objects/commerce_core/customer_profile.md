---
type: "Ontology Object"
object: customer_profile
domain: commerce_core
tier: core
resource: "urn:ultracart:ontology:object:customer_profile"
version: 1
grain: "one row per registered customer profile (customer_profile_oid)"
key:
  fields: [customer_profile_oid]
  identity_family: customer_profile_oid
source:
  binding: uc_customers
  default_table: "{{source_project}}.{{dataset.medium}}.uc_customers"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: customer_profile_oid
    type: INTEGER
    source: customer_profile_oid
    meaning: "UltraCart primary key for the registered profile"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "profile email identity (base64 sha256 of normalized email; see identity spine)"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: signup_dts
    type: STRING
    source: signup_dts
    meaning: "when the profile was created (DW types this column STRING, not DATETIME — cast downstream if needed)"
  - name: last_modified_dts
    type: DATETIME
    source: last_modified_dts
    meaning: "last profile mutation"
  - name: pricing_tier_name
    type: STRING
    source: "(SELECT pt.name FROM UNNEST(pricing_tiers) AS pt LIMIT 1)"
    refs: [pricing_tiers.name]
    meaning: "first assigned pricing tier; NULL = retail"
  - name: is_wholesale
    type: BOOLEAN
    source: "ARRAY_LENGTH(pricing_tiers) > 0"
    meaning: "any pricing tier assigned — UltraCart's own DW convention for flagging wholesale customers"
  - name: tax_exempt
    type: BOOLEAN
    source: tax_exempt
    meaning: "profile is tax exempt"
  - name: tax_id_hash
    type: STRING
    source: tax_id_hash
    meaning: "hash twin of the tax id (raw tax_id is high-tier PII and excluded)"
  - name: do_not_send_mail
    type: BOOLEAN
    source: do_not_send_mail
    meaning: "postal do-not-mail flag"
  - name: track_separately
    type: BOOLEAN
    source: track_separately
    meaning: "merchant flag to segregate this profile in tracking/reporting"
  - name: privacy_marketing
    type: BOOLEAN
    source: privacy.marketing
    meaning: "consent: marketing cookies/processing"
  - name: privacy_preference
    type: BOOLEAN
    source: privacy.preference
    meaning: "consent: preference cookies/processing"
  - name: privacy_statistics
    type: BOOLEAN
    source: privacy.statistics
    meaning: "consent: statistics cookies/processing"
  - name: privacy_last_update_dts
    type: DATETIME
    source: privacy.last_update_dts
    meaning: "when consent flags last changed"
  - name: loyalty_current_points
    type: INTEGER
    source: loyalty.current_points
    meaning: "loyalty points balance (points-style programs)"
  - name: loyalty_pending_points
    type: INTEGER
    source: loyalty.pending_points
    meaning: "loyalty points not yet vested"
  - name: loyalty_tier_name
    type: STRING
    source: loyalty.loyalty_tier_name
    meaning: "current loyalty tier"
  - name: loyalty_tier_oid
    type: INTEGER
    source: loyalty.loyalty_tier_oid
    meaning: "current loyalty tier oid"
  - name: internal_gift_certificate_oid
    type: INTEGER
    source: loyalty.internal_gift_certificate_oid
    meaning: "store-credit loyalty programs are backed by an internal gift certificate — this is it"
  - name: internal_gift_certificate_balance
    type: STRING
    source: loyalty.internal_gift_certificate_balance
    meaning: "store-credit balance (DW types this STRING — cast downstream if needed)"
  - name: first_order_dts
    type: DATETIME
    source: orders_summary.first_order_dts
    meaning: "first order timestamp per UltraCart's own rollup on the profile"
  - name: last_order_dts
    type: DATETIME
    source: orders_summary.last_order_dts
    meaning: "most recent order timestamp per the profile rollup"
  - name: lifetime_order_count
    type: INTEGER
    source: orders_summary.order_count
    meaning: "order count per the profile rollup (profile-attached orders only)"
  - name: lifetime_total
    type: NUMERIC
    source: orders_summary.total
    meaning: "lifetime order total per the profile rollup (profile-attached orders only)"
  - name: embedded_order_count
    type: INTEGER
    source: "ARRAY_LENGTH(orders)"
    meaning: "orders embedded on the profile (count only — order contents are excluded; use the order object)"
  - name: quote_count
    type: INTEGER
    source: "ARRAY_LENGTH(quotes)"
    meaning: "quotes embedded on the profile (count only)"
  - name: stored_card_count
    type: INTEGER
    source: "ARRAY_LENGTH(cards)"
    meaning: "stored payment cards on file (count only — card contents are never exposed)"
  - name: affiliate_oid
    type: INTEGER
    source: affiliate_oid
    meaning: "affiliate permanently attached to this profile, if any"
  - name: referral_source
    type: STRING
    source: referral_source
    meaning: "recorded referral source"
  - name: terms
    type: STRING
    source: terms
    meaning: "B2B payment terms (e.g. Net 30); NULL for consumer profiles"
  - name: allow_purchase_order
    type: BOOLEAN
    source: allow_purchase_order
    meaning: "B2B: may pay by purchase order"
  - name: unapproved
    type: BOOLEAN
    source: unapproved
    meaning: "profile awaiting merchant approval (wholesale signup gating)"
links:
  - to: order
    kind: has_many
    on: "customer_profile.customer_profile_oid = order.customer_profile_oid"
  - to: affiliate
    kind: referred_by
    on: "customer_profile.affiliate_oid = affiliate.affiliate_oid"
  - to: gift_certificate
    kind: has_one
    on: "customer_profile.internal_gift_certificate_oid = gift_certificate.gift_certificate_oid"
  - to: marketing_contact
    kind: same_person_as
    on: "customer_profile.email_hash_b64 = marketing_contact.email_hash_b64"
pii: pseudonymous
excluded_fields: [email, tax_id, fax, website_url, billing, shipping, cards, cc_emails, orders, quotes, software_entitlements, attachments, properties, tags, activity, edi, reviewer, pricing_tiers, loyalty.ledger_entries, loyalty.redemptions, automatic_merchant_notes, business_notes, dhl_account_number, dhl_duty_account_number, fedex_account_number, ups_account_number]
consumers: []
---

# CustomerProfile

The **registered account** object — a stored login/profile with address books, stored
cards, loyalty state, wholesale tiering and B2B permissions. **This is NOT "every
buyer."** Most UltraCart orders are guest checkouts with no profile; the every-buyer
`customer` concept is a **named definition** rolled up from `order` on
`email_hash_b64` (email-first identity, per UltraCart's own DW LTV queries). Use this
object when the question is about accounts: stored cards, loyalty balances, wholesale
tiers, terms, consent.

Curation: uc_customers has 2,006 field paths; this object exposes ~30 scalars. All
nested arrays (address books, cards, embedded order/quote copies, loyalty ledger,
software entitlements) are excluded — the embedded orders are a denormalized copy of
uc_orders and must never be double-counted; only ARRAY_LENGTH counts are exposed.
There is **no auto_orders array on this table** — subscription counts come from the
`auto_order` object by `email_hash_b64`.

Gotchas:
- `orders_summary.*` (and `lifetime_total`) covers **profile-attached orders only** —
  guest orders by the same email are invisible to it. For true LTV, roll up `order`
  by `email_hash_b64`; treat these fields as UltraCart's own convenience rollup.
- `signup_dts` and `internal_gift_certificate_balance` are typed STRING in the DW —
  honest passthrough here; cast downstream.
- Wholesale flagging follows UltraCart's DW sample convention: any `pricing_tiers`
  entry ⇒ wholesale (`is_wholesale`).
- Store-credit loyalty is an internal gift certificate (`internal_gift_certificate_oid`
  → `gift_certificate`); points programs use the `loyalty_*_points` scalars.

## Change log
- v1 (2026-07-06) — initial.
