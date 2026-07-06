---
type: "Ontology Object"
object: gift_certificate
domain: promotions
tier: core
resource: "urn:ultracart:ontology:object:gift_certificate"
version: 1
grain: "one row per gift certificate account"
key:
  fields: [gift_certificate_oid]
  identity_family: gift_certificate_oid
source:
  binding: uc_gift_certificates
  default_table: "{{source_project}}.{{dataset.medium}}.uc_gift_certificates"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: gift_certificate_oid
    type: INTEGER
    source: gift_certificate_oid
    meaning: "UltraCart primary key for the certificate account"
  - name: code
    type: STRING
    source: code
    meaning: "the certificate code — the string orders redeem"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "recipient identity (base64 sha256 of normalized email; see identity spine)"
  - name: customer_profile_oid
    type: INTEGER
    source: customer_profile_oid
    meaning: "registered customer profile the certificate is attached to (NULL if none)"
  - name: is_activated
    type: BOOLEAN
    source: activated
    meaning: "certificate is activated and usable"
  - name: is_deleted
    type: BOOLEAN
    source: deleted
    meaning: "soft-deleted by the merchant"
  - name: is_internal
    type: BOOLEAN
    source: internal
    meaning: "issued internally by the loyalty/store-credit system rather than purchased"
  - name: expires_at
    type: DATETIME
    source: expiration_dts
    meaning: "expiration (NULL = never expires)"
  - name: original_balance
    type: NUMERIC
    source: original_balance
    meaning: "issued amount"
  - name: remaining_balance
    type: NUMERIC
    source: remaining_balance
    meaning: "current unspent balance"
  - name: is_redeemable
    type: BOOLEAN
    source: "activated AND NOT deleted AND (expiration_dts IS NULL OR expiration_dts > CURRENT_DATETIME()) AND remaining_balance > 0"
    meaning: "derived: can be spent right now"
  - name: reference_order_id
    type: STRING
    source: reference_order_id
    meaning: "order that purchased/created the certificate (NULL for internal issues)"
  - name: merchant_note
    type: STRING
    source: merchant_note
    meaning: "internal note on the account"
  - name: ledger_entry_count
    type: INTEGER
    source: "ARRAY_LENGTH(ledger_entries)"
    meaning: "number of ledger movements (issues, redemptions, adjustments)"
links:
  - to: customer
    kind: belongs_to
    on: "gift_certificate.email_hash_b64 = customer.email_hash_b64"
  - to: customer_profile
    kind: belongs_to
    on: "gift_certificate.customer_profile_oid = customer_profile.customer_profile_oid"
  - to: order
    kind: originated_from
    on: "gift_certificate.reference_order_id = order.order_id"
pii: pseudonymous
excluded_fields: [email, ledger_entries]
consumers: []
---

# GiftCertificate

A stored-value account: issued once (purchased on an order, or granted internally by
the loyalty/store-credit machinery), then drawn down by redemptions until the balance
hits zero or it expires. `original_balance` vs `remaining_balance` gives outstanding
liability; the per-movement detail lives in the excluded `ledger_entries[]` array
(each entry carries `amount`, `entry_dts`, and a `reference_order_id` pointing at the
redeeming order).

Lifecycle: `activated` → spendable; `deleted` is a soft delete; `expiration_dts` is
NULL for non-expiring certificates. `is_redeemable` collapses all of that plus a
positive balance into one flag.

Identity & joins:
- Gift certificates are **the only promotion carrying BOTH code and oid on the order
  side** (`uc_orders.gift_certificate.gift_certificate_oid` + `_code`), so unlike
  coupons you can join by oid — the ontology keys on `gift_certificate_oid`.
- `is_internal = TRUE` rows are loyalty-issued store credit
  (`uc_customers.loyalty.internal_gift_certificate_oid` points here) — exclude them
  when analyzing purchased gift-certificate revenue, include them when analyzing
  liability.

PII: the table carries raw `email` next to `email_hash` (permissive tiers append the
raw column). The canonical view exposes only the hash twin, surfaced as
`email_hash_b64` per the identity spine.

## Change log
- v1 (2026-07-06) — initial.
