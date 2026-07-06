---
type: "Ontology Object"
object: cart_abandon
domain: storefront_behavior
tier: core
resource: "urn:ultracart:ontology:object:cart_abandon"
version: 1
grain: "one abandoned-cart snapshot per cart_abandon_uuid"
key:
  fields: [cart_abandon_uuid]
  identity_family: cart_abandon_uuid
source:
  binding: uc_cart_abandons
  default_table: "{{source_project}}.{{dataset.medium}}.uc_cart_abandons"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: cart_abandon_uuid
    type: STRING
    source: cart_abandon_uuid
    meaning: "primary key for the abandonment snapshot"
  - name: cart_id
    type: STRING
    source: cart_id
    meaning: "the underlying cart/checkout session id"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: abandoned_at
    type: DATETIME
    source: cart_abandon_dts
    meaning: "when the cart was declared abandoned"
  - name: email_hash_b64
    type: STRING
    source: billing.email_hash
    meaning: "customer identity captured at checkout (base64 sha256; see identity spine)"
  - name: customer_profile_oid
    type: INTEGER
    source: customer_profile.customer_profile_oid
    meaning: "registered profile if the shopper was logged in (NULL for guests)"
  - name: logged_in
    type: BOOLEAN
    source: logged_in
    meaning: "shopper was logged into a profile"
  - name: currency_code
    type: STRING
    source: currency_code
    meaning: "cart currency"
  - name: subtotal
    type: NUMERIC
    source: summary.subtotal.value
    meaning: "cart subtotal before discounts"
  - name: subtotal_discount
    type: NUMERIC
    source: summary.subtotal_discount.value
    meaning: "discount applied to the subtotal"
  - name: subtotal_with_discount
    type: NUMERIC
    source: summary.subtotal_with_discount.value
    meaning: "subtotal after discounts"
  - name: shipping_handling
    type: NUMERIC
    source: summary.shipping_handling.value
    meaning: "shipping and handling at abandonment"
  - name: tax
    type: NUMERIC
    source: summary.tax.value
    meaning: "tax at abandonment"
  - name: total
    type: NUMERIC
    source: summary.total.value
    meaning: "cart total at abandonment — the recoverable value"
  - name: item_count
    type: INTEGER
    source: "ARRAY_LENGTH(items)"
    meaning: "distinct line items in the cart"
  - name: unit_count
    type: NUMERIC
    source: "(SELECT SUM(items.quantity) FROM UNNEST(items) AS items)"
    meaning: "total units across line items"
  - name: has_subscription_intent
    type: BOOLEAN
    source: "(SELECT COUNT(items.auto_order_schedule) > 0 FROM UNNEST(items) AS items)"
    meaning: "any line item carried an auto-order schedule (abandoned subscription signup)"
  - name: coupon_code
    type: STRING
    source: "(SELECT MAX(coupons.coupon_code) FROM UNNEST(coupons) AS coupons)"
    meaning: "coupon in the cart at abandonment (MAX collapse; see coupon_count)"
  - name: coupon_count
    type: INTEGER
    source: "ARRAY_LENGTH(coupons)"
    meaning: "coupons attached (>1 is unusual)"
  - name: gift_certificate_code
    type: STRING
    source: gift_certificate.gift_certificate_code
    meaning: "gift certificate applied, if any (string-code join)"
  - name: storefront_host_name
    type: STRING
    source: checkout.storefront_host_name
    meaning: "storefront host — joins uc_storefronts by host_name string (no oid on carts)"
  - name: checkout_step
    type: STRING
    source: checkout.current_step
    meaning: "checkout step reached before abandoning"
  - name: return_code
    type: STRING
    source: checkout.return_code
    meaning: "code that rebuilds the cart URL for recovery campaigns"
  - name: payment_method
    type: STRING
    source: payment.payment_method
    meaning: "payment method selected before abandoning"
  - name: utm_source
    type: STRING
    source: "(SELECT MAX(utms.utm_source) FROM UNNEST(utms) AS utms)"
    meaning: "utm_source across recorded touches (MAX collapse; see utm_touch_count)"
  - name: utm_campaign
    type: STRING
    source: "(SELECT MAX(utms.utm_campaign) FROM UNNEST(utms) AS utms)"
    meaning: "utm_campaign across recorded touches (MAX collapse)"
  - name: utm_touch_count
    type: INTEGER
    source: "ARRAY_LENGTH(utms)"
    meaning: "UTM touches recorded (>1 means consult the excluded utms array for multi-touch)"
  - name: first_click_at
    type: DATETIME
    source: "(SELECT MIN(utms.click_dts) FROM UNNEST(utms) AS utms)"
    meaning: "earliest recorded ad/UTM click for this cart"
  - name: billing_country
    type: STRING
    source: billing.country_code
    meaning: "coarse geo: billing country"
  - name: billing_state
    type: STRING
    source: billing.state_region
    meaning: "coarse geo: billing state/region"
  - name: advertising_source
    type: STRING
    source: marketing.advertising_source
    meaning: "self-reported 'how did you hear about us'"
  - name: mailing_list_opt_in
    type: BOOLEAN
    source: marketing.mailing_list_opt_in
    meaning: "opted into email marketing before abandoning (recovery-contactable signal)"
links:
  - to: customer
    kind: belongs_to
    on: "cart_abandon.email_hash_b64 = customer.email_hash_b64"
  - to: customer_profile
    kind: belongs_to
    on: "cart_abandon.customer_profile_oid = customer_profile.customer_profile_oid"
  - to: coupon
    kind: references
    on: "cart_abandon.coupon_code = coupon.merchant_code"
  - to: gift_certificate
    kind: references
    on: "cart_abandon.gift_certificate_code = gift_certificate.code"
  - to: storefront
    kind: belongs_to
    on: "cart_abandon.storefront_host_name = storefront.host_name"
pii: pseudonymous
excluded_fields:
  - billing               # raw + hashed name/address/phone/email book; only email_hash, country_code, state_region surfaced
  - shipping              # raw + hashed ship-to book
  - customer_profile      # full embedded profile snapshot (addresses, cards); only customer_profile_oid surfaced
  - items                 # full line-item structs (options, kits, multimedia); scalars derived above
  - coupons               # array; coupon_code/coupon_count derived above
  - utms                  # multi-touch array with attribution weights; scalars derived above
  - settings              # checkout configuration snapshot, not behavior
  - gift                  # gift_email / gift_message are PII
  - properties            # arbitrary key/value payloads
  - taxes                 # county-level tax detail
  - checkout.ip_address   # raw IP — never expose
  - checkout.comments     # free text from the shopper
  - payment.credit_card   # card metadata; payment_method scalar is enough
consumers: []
---

# CartAbandon

A frozen snapshot of a checkout that never became an order: line items, applied
promotions, totals, checkout progress, and the marketing context that produced the
visit. The canonical view reduces the ~700-field snapshot to the analytical scalars —
who (hashed), when, how much (`total` = recoverable value), how far
(`checkout_step`), and how to win it back (`return_code`, `mailing_list_opt_in`,
`coupon_code`).

Recovery economics: `total` × abandon volume, segmented by `checkout_step` and
`has_subscription_intent`, is the standard sizing query. An abandoned cart with
subscription intent is worth far more than its face value — treat those as a separate
pool.

Gotchas:
- **No direct session key.** Unlike the other behavior surfaces, cart abandons carry no
  `ucacid` or `screen_recording_uuid`. Link to sessions via `email_hash_b64`, or via the
  `checkout_abandon` hit type inside `analytics_session`'s (excluded) hits trail;
  `cart_id` is the cart's own session-ish identifier.
- Storefront linkage is a **string join** on `storefront_host_name` →
  `storefront.host_name` — same pattern as orders; there is no storefront_oid here.
- Coupons appear by **code only** (no coupon_oid), matching the order-side convention:
  join `coupon_code` → `coupon.merchant_code`.
- The catalog's family file tags this table operations_config; it is behavioral and is
  modeled here.
- The embedded `customer_profile`, `billing`, and `shipping` structs duplicate
  `customer`/`customer_profile` data as-of abandonment — join to those objects for
  current state instead of trusting the snapshot.

## Change log
- v1 (2026-07-06) — initial.
