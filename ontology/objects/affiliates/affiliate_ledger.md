---
type: "Ontology Object"
object: affiliate_ledger
domain: affiliates
tier: core
resource: "urn:ultracart:ontology:object:affiliate_ledger"
version: 1
grain: "one row per affiliate commission ledger entry per affiliate_ledger_oid (one order item's commission for one affiliate at one tier)"
key:
  fields: [affiliate_ledger_oid]
  identity_family: affiliate_ledger_oid
source:
  binding: uc_affiliate_ledgers
  default_table: "{{source_project}}.{{dataset.medium}}.uc_affiliate_ledgers"
properties:
  - name: affiliate_ledger_oid
    type: INTEGER
    source: affiliate_ledger_oid
    meaning: "UltraCart primary key for the ledger entry"
  - name: affiliate_oid
    type: INTEGER
    source: affiliate_oid
    meaning: "affiliate earning (or being debited) the commission"
  - name: order_id
    type: STRING
    source: order_id
    meaning: "order that generated the commission"
  - name: item_id
    type: STRING
    source: item_id
    meaning: "item (SKU string) the commission applies to — joins item.merchant_item_id"
  - name: affiliate_click_oid
    type: INTEGER
    source: affiliate_click_oid
    meaning: "click that won attribution for this commission"
  - name: affiliate_link_oid
    type: INTEGER
    source: affiliate_link_oid
    meaning: "tracking link behind the attributed click"
  - name: tier_number
    type: INTEGER
    source: tier_number
    meaning: "commission tier (1 = direct; >1 = multi-tier/downline override)"
  - name: transaction_at
    type: DATETIME
    source: transaction_dts
    meaning: "when this ledger entry was recorded"
  - name: original_transaction_at
    type: DATETIME
    source: original_transaction_dts
    meaning: "original transaction time (differs on adjustments/reversals of an earlier entry)"
  - name: transaction_amount
    type: NUMERIC
    source: transaction_amount
    meaning: "commission amount earned (negative = reversal/chargeback)"
  - name: transaction_amount_paid
    type: NUMERIC
    source: transaction_amount_paid
    meaning: "portion of the amount already paid out"
  - name: unpaid_amount
    type: NUMERIC
    source: "transaction_amount - transaction_amount_paid"
    meaning: "derived: outstanding commission liability on this entry"
  - name: transaction_percentage
    type: NUMERIC
    source: transaction_percentage
    meaning: "commission rate applied"
  - name: transaction_state
    type: STRING
    source: transaction_state
    meaning: "commission lifecycle state (pending → approved/paid, declined…)"
  - name: transaction_memo
    type: STRING
    source: transaction_memo
    meaning: "free-text memo on the entry (manual adjustments explain themselves here)"
  - name: assigned_by_user
    type: STRING
    source: assigned_by_user
    meaning: "staff user who manually assigned the commission (NULL = system-attributed)"
  - name: sub_id
    type: STRING
    source: sub_id
    meaning: "affiliate sub-id carried from the click"
  - name: screen_recording_uuid
    type: STRING
    source: click.screen_recording_uuid
    meaning: "behavioral session of the attributed click (bridge to screen_recording)"
links:
  - to: affiliate
    kind: belongs_to
    on: "affiliate_ledger.affiliate_oid = affiliate.affiliate_oid"
  - to: order
    kind: belongs_to
    on: "affiliate_ledger.order_id = order.order_id"
  - to: item
    kind: belongs_to
    on: "affiliate_ledger.item_id = item.merchant_item_id"
  - to: affiliate_click
    kind: belongs_to
    on: "affiliate_ledger.affiliate_click_oid = affiliate_click.affiliate_click_oid"
pii: pseudonymous
excluded_fields: [click, link]
consumers: []
---

# AffiliateLedger

**This is money.** The commission ledger: every entry is one affiliate's
commission on one order item at one tier. Sum `transaction_amount` for
liability incurred, `transaction_amount_paid` for what has left the building,
and the derived `unpaid_amount` for the open payable. An order with N
commissionable items and a 2-tier program produces up to 2N rows — never count
ledger rows as "orders referred".

Lifecycle: `transaction_state` is the commission state machine
(pending → approved → paid; declined/reversed entries and negative
`transaction_amount` rows both occur). `original_transaction_at` differs from
`transaction_at` on adjustments — group by order_id + item_id to reconstruct an
entry's history. `assigned_by_user` being non-null flags manual attribution
overrides.

Attribution context rides along: `affiliate_click_oid` / `affiliate_link_oid` /
`sub_id` say *which click earned it*, and `screen_recording_uuid` (lifted from
the embedded click snapshot) bridges straight into the behavioral session. The
full `click` and `link` struct snapshots are excluded — join `affiliate_click`
for click detail (and note `click.ip_address` is the struct's PII).

**Tenant scoping:** no `merchant_id` on this table, so no merchant filter is
declared. Scope through `affiliate` (merchant-filtered) on `affiliate_oid`, or
through `order` on `order_id`.

## Change log
- v1 (2026-07-06) — initial.
