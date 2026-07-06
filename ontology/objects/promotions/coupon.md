---
type: "Ontology Object"
object: coupon
domain: promotions
tier: core
resource: "urn:ultracart:ontology:object:coupon"
version: 1
grain: "one row per coupon definition"
key:
  fields: [merchant_code]
  identity_family: coupon_code
source:
  binding: uc_coupons
  default_table: "{{source_project}}.{{dataset.medium}}.uc_coupons"
properties:
  - name: coupon_oid
    type: INTEGER
    source: coupon_oid
    meaning: "UltraCart internal primary key (NOT carried on orders — see prose)"
  - name: merchant_code
    type: STRING
    source: merchant_code
    meaning: "the coupon code customers type — the key orders join on"
  - name: coupon_type
    type: STRING
    source: coupon_type
    meaning: "which of the ~50 mutually-exclusive discount structs is populated"
  - name: description
    type: STRING
    source: description
    meaning: "merchant-entered description"
  - name: calculated_description
    type: STRING
    source: calculated_description
    meaning: "UltraCart-generated human-readable summary of the discount"
  - name: start_at
    type: DATETIME
    source: start_dts
    meaning: "validity window start (NULL = immediately valid)"
  - name: expires_at
    type: DATETIME
    source: expiration_dts
    meaning: "validity window end (NULL = never expires)"
  - name: is_live
    type: BOOLEAN
    source: "(start_dts IS NULL OR start_dts <= CURRENT_DATETIME()) AND (expiration_dts IS NULL OR expiration_dts > CURRENT_DATETIME())"
    meaning: "derived: inside the validity window right now"
  - name: usable_by
    type: STRING
    source: usable_by
    meaning: "audience restriction (anyone / one-per-customer style rules)"
  - name: is_super_coupon
    type: BOOLEAN
    source: super_coupon
    meaning: "bypasses item-level coupon exclusions"
  - name: hide_from_customer
    type: BOOLEAN
    source: hide_from_customer
    meaning: "discount applied without showing the customer the code"
  - name: skip_on_rebill
    type: BOOLEAN
    source: skip_on_rebill
    meaning: "discount applies to the first order only, not auto-order rebills"
  - name: stacks_with_other_coupons
    type: BOOLEAN
    source: can_be_used_with_other_coupons
    meaning: "may be combined with other coupons on one order"
  - name: allows_multiple_one_time_codes
    type: BOOLEAN
    source: allow_multiple_one_time_codes
    meaning: "multiple generated one-time codes of this coupon may stack"
  - name: affiliate_oid
    type: INTEGER
    source: affiliate_oid
    meaning: "affiliate the coupon is attributed to (NULL for house coupons)"
  - name: quickbooks_code
    type: STRING
    source: quickbooks_code
    meaning: "accounting export code for the discount"
  - name: merchant_notes
    type: STRING
    source: merchant_notes
    meaning: "internal merchant notes"
links:
  - to: order
    kind: referenced_by
    on: "coupon.merchant_code = order.coupon_code"
  - to: affiliate
    kind: belongs_to
    on: "coupon.affiliate_oid = affiliate.affiliate_oid"
pii: none
excluded_fields: [amount_off_items, amount_off_items_and_free_shipping, amount_off_shipping, amount_off_shipping_with_items_purchase, amount_off_subtotal, amount_off_subtotal_and_free_shipping, amount_off_subtotal_and_shipping, amount_off_subtotal_with_block_purchase, amount_off_subtotal_with_items_purchase, amount_off_subtotal_with_purchase, amount_shipping_with_subtotal, automatically_apply_coupon_codes, buy_one_get_one, discount_item_with_item_purchase, discount_items, free_item_and_shipping_with_subtotal, free_item_with_item_purchase, free_item_with_item_purchase_and_free_shipping, free_item_with_subtotal, free_items_with_item_purchase, free_items_with_mixmatch_purchase, free_shipping, free_shipping_specific_items, free_shipping_with_items_purchase, free_shipping_with_subtotal, more_loyalty_cashback, more_loyalty_points, multiple_amounts_off_items, no_discount, percent_more_loyalty_cashback, percent_more_loyalty_points, percent_off_item_with_items_quantity_purchase, percent_off_items, percent_off_items_and_free_shipping, percent_off_items_with_items_purchase, percent_off_items_with_minimum_item_amount, percent_off_msrp_items, percent_off_retail_price_items, percent_off_shipping, percent_off_subtotal, percent_off_subtotal_and_free_shipping, percent_off_subtotal_limit, percent_off_subtotal_with_items_purchase, percent_off_subtotal_with_subtotal, restrict_by_postal_codes, restrict_by_screen_branding_theme_codes, restrict_by_storefronts, tiered_amount_off_items, tiered_amount_off_subtotal, tiered_percent_off_items, tiered_percent_off_shipping, tiered_percent_off_subtotal, tiered_percent_off_subtotal_based_on_msrp]
consumers: []
---

# Coupon

A coupon **definition** — the configured discount, not its redemptions. Redemptions
live on orders (`uc_orders.coupons[]`). The discount mechanics are spread across ~50
mutually-exclusive structs (`percent_off_subtotal`, `buy_one_get_one`,
`tiered_amount_off_items`…); exactly one is populated per coupon and `coupon_type`
names it. The canonical view excludes all 50 — `calculated_description` is the
human-readable rendering, and anyone needing the exact mechanics should read the
type-specific struct from the source table.

**Join gotcha (the big one): orders join by coupon CODE string, not oid.**
`uc_orders.coupons[].coupon_code = uc_coupons.merchant_code`. There is no `coupon_oid`
on the order side at all. Codes are also case-normalized inconsistently in the wild —
compare with `UPPER(TRIM(...))` on both sides when redemption counts look low. The
ontology therefore keys this object on `merchant_code` (identity family
`coupon_code`), keeping `coupon_oid` as an internal property.

Naming decision: the property stays **`merchant_code`** (warehouse-native name) rather
than aliasing to `offer_code`; overlays that prefer marketing vocabulary can alias in
their own layer without changing the property contract.

Gotchas:
- **No `merchant_id` column** — uc_coupons is one of the few base tables without a
  tenant column, so the compiled view carries no merchant filter. In multi-merchant
  warehouse projects, scope coupon analysis through the orders that redeem them.
- The infamous source-schema typo `hdie_from_customer` is NOT here — this table spells
  `hide_from_customer` correctly. The typo'd field lives in the order-side embedded
  coupon snapshot (`uc_orders.coupons.hdie_from_customer`); the order/order_item
  objects must bind the typo'd name.
- `skip_on_rebill` is the flag that decides whether a discount erodes subscription
  economics — first-order-only offers vs forever-discounts.
- One-time generated codes: many merchants issue per-customer generated codes off a
  parent coupon; those redemptions appear under the generated code string on the
  order, not the parent `merchant_code`.

## Change log
- v1 (2026-07-06) — initial.
