---
type: "Ontology Object"
object: order
domain: commerce_core
tier: core
resource: "urn:ultracart:ontology:object:order"
version: 1
grain: "one row per order (header grain; lines live in order_item)"
key:
  fields: [order_id]
  identity_family: order_id
source:
  binding: uc_orders
  default_table: "{{source_project}}.{{dataset.medium}}.uc_orders"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: order_id
    type: STRING
    source: order_id
    meaning: "public order number (e.g. DEMO-0000001234); the cross-warehouse order key"
  - name: email_hash_b64
    type: STRING
    source: billing.email_hash
    meaning: "customer identity (base64 sha256 of normalized email; see identity spine)"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: order_date
    type: DATE
    source: "DATE(creation_dts)"
    meaning: "calendar date the order was placed (UTC — DW datetimes are UTC, unlike the EST back office)"
  - name: order_ts
    type: DATETIME
    source: creation_dts
    meaning: "order placed/created timestamp (UTC)"
  - name: current_stage
    type: STRING
    source: current_stage
    meaning: "order lifecycle stage (raw API enum; revenue truth = Shipping Department / Completed Order)"
    enum_ref: order_stage
  - name: payment_dts
    type: DATETIME
    source: payment.payment_dts
    meaning: "when payment was processed — the canonical 'paid' timestamp; NULL = never paid"
  - name: payment_method
    type: STRING
    source: payment.payment_method
    meaning: "how the customer paid"
    enum_ref: payment_method
  - name: payment_status
    type: STRING
    source: payment.payment_status
    meaning: "payment processing state"
    enum_ref: payment_status
  - name: is_test_order
    type: BOOLEAN
    source: payment.test_order
    meaning: "UltraCart test-order flag; exclude from all revenue metrics"
  - name: channel_partner_code
    type: STRING
    source: channel_partner.channel_partner_code
    meaning: "external order source (marketplace/call center); NULL = direct sale"
  - name: storefront_host_name
    type: STRING
    source: checkout.storefront_host_name
    meaning: "sales channel host; string-joins to storefront.host_name (no oid on orders)"
  - name: customer_profile_oid
    type: INTEGER
    source: customer_profile.customer_profile_oid
    meaning: "registered profile, when the buyer was logged in (NULL for guest checkout)"
  - name: auto_order_oid
    type: INTEGER
    source: auto_order.auto_order_oid
    meaning: "subscription container this order belongs to (original or rebill); NULL = one-time order"
  - name: subtotal
    type: NUMERIC
    source: summary.subtotal.value
    meaning: "merchandise subtotal before discounts/tax/shipping (account currency)"
  - name: total
    type: NUMERIC
    source: summary.total.value
    meaning: "grand total charged"
  - name: tax
    type: NUMERIC
    source: summary.tax.value
    meaning: "tax charged"
  - name: shipping_charged
    type: NUMERIC
    source: summary.shipping_handling_total.value
    meaning: "shipping & handling charged to the customer"
  - name: refunded
    type: NUMERIC
    source: summary.total_refunded.value
    meaning: "total amount refunded to date (0/NULL = no refund)"
  - name: refund_dts
    type: DATETIME
    source: refund_dts
    meaning: "when (last) refunded; NULL = never refunded"
  - name: refund_reason
    type: STRING
    source: refund_reason
    meaning: "order-level refund reason — a merchant-configured code list, not a fixed enum"
  - name: reject_dts
    type: DATETIME
    source: reject_dts
    meaning: "when rejected (fraud/decline path); NULL = not rejected"
  - name: fraud_score
    type: NUMERIC
    source: fraud_score.score
    meaning: "numeric fraud score (the scalar; the rest of the fraud_score struct is excluded)"
  - name: currency_code
    type: STRING
    source: currency_code
    meaning: "customer-facing currency of the order"
  - name: exchange_rate
    type: NUMERIC
    source: exchange_rate
    meaning: "exchange rate applied between customer currency and account currency"
  - name: coupon_count
    type: INTEGER
    source: "ARRAY_LENGTH(coupons)"
    meaning: "coupons applied (count only; codes join via the coupon object by coupon_code)"
  - name: item_count
    type: INTEGER
    source: "ARRAY_LENGTH(items)"
    meaning: "order lines (the lines themselves live in order_item)"
  - name: first_affiliate_oid
    type: INTEGER
    source: "(SELECT a.affiliate_oid FROM UNNEST(affiliates) AS a LIMIT 1)"
    refs: [affiliates.affiliate_oid]
    meaning: "attributed affiliate (first entry of the affiliates array); NULL = no affiliate"
  - name: utm_source_last_click
    type: STRING
    source: "(SELECT u.utm_source FROM UNNEST(utms) AS u ORDER BY u.click_dts DESC LIMIT 1)"
    refs: [utms.utm_source, utms.click_dts]
    meaning: "utm_source of the most recent recorded click before the order"
  - name: utm_campaign_last_click
    type: STRING
    source: "(SELECT u.utm_campaign FROM UNNEST(utms) AS u ORDER BY u.click_dts DESC LIMIT 1)"
    refs: [utms.utm_campaign, utms.click_dts]
    meaning: "utm_campaign of the most recent recorded click before the order"
  - name: upsell_path_code
    type: STRING
    source: checkout.upsell_path_code
    meaning: "post-checkout upsell funnel the order went through, if any"
links:
  - to: order_item
    kind: has_many
    on: "order.order_id = order_item.order_id"
  - to: customer_profile
    kind: belongs_to
    on: "order.customer_profile_oid = customer_profile.customer_profile_oid"
  - to: auto_order
    kind: belongs_to
    on: "order.auto_order_oid = auto_order.auto_order_oid"
  - to: affiliate
    kind: attributed_to
    on: "order.first_affiliate_oid = affiliate.affiliate_oid"
  - to: storefront
    kind: sold_via
    on: "order.storefront_host_name = storefront.host_name"
enums:
  order_stage: ["Accounts Receivable", "Pending Clearance", "Fraud Review", "Rejected", "Shipping Department", "Completed Order", "Quote Request", "Quote Sent", "Least Cost Routing", "Unknown", "Pre-ordered", "Advanced Order Routing", "Hold"]
  payment_status: ["Unprocessed", "Authorized", "Capture Failed", "Processed", "Declined", "Voided", "Refunded", "Skipped"]
  payment_method: ["Affirm", "Amazon", "Amazon Pay", "Amazon SC", "Cash", "Check", "COD", "Credit Card", "Crypto", "eBay", "eCheck", "Google Shopping", "Goldbelly", "GoHighLevel", "Insurance", "Link", "LoanHero", "Money Order", "PayPal", "Purchase Order", "Quote Request", "Unknown", "Wire Transfer", "Walmart", "Shop.com", "Sezzle", "Venmo", "Apple Pay", "Google Pay", "Health Benefit Card", "PayPal Fastlane", "Klarna"]
pii: pseudonymous
excluded_fields: [items, coupons, affiliates, utms, emails, customer_profile, billing, shipping, gift, checkout, payment.transactions, payment.credit_card, payment.echeck, payment.health_benefit_card, current_stage_histories, fraud_score, internal, point_of_sale, digital_order, edi, taxes, buysafe, linked_shipment, quote, salesforce, marketing, properties, Tags]
consumers: []
---

# Order

The order **header**: one completed (or attempted) checkout, carrying lifecycle stage,
payment, channel, attribution scalars, and the money summary. Lines live in
`order_item`; coupons, affiliates, UTMs and email engagement are nested arrays
deliberately excluded here — model them at their own grain.

**Revenue truth (the one convention everything downstream depends on):** an order counts
as real revenue only when

```
current_stage IN ('Shipping Department', 'Completed Order')
AND payment_dts IS NOT NULL
AND is_test_order IS NOT TRUE
AND channel_partner_code IS NULL        -- direct sales only; drop this clause to include marketplaces
```

This matches UltraCart's own DW sample queries (`Rejected` is excluded, quotes and
holds are not sales, unpaid A/R is not revenue). **Do not restate this filter in
downstream SQL — use the `revenue_order` named definition**, which compiles exactly
this convention (with the channel-partner clause as a parameter).

Gotchas:
- **Timestamps are UTC in the DW**; the REST API and the UltraCart back office run in
  EST. `order_date` is the UTC date — same-day comparisons against back-office reports
  can be off by up to 5 hours at day boundaries.
- `current_stage` is the *current* state; transition history is in the excluded
  `current_stage_histories[]` array (model separately if stage-timing is ever needed).
- `refunded`/`refund_dts` capture partial and full refunds; refund/reject reasons are
  merchant-configured code lists, never fixed enums.
- The full `customer_profile` snapshot embedded on the order (a copy of uc_customers)
  is excluded; join to `customer_profile` via `customer_profile_oid`. Buyer identity
  is `email_hash_b64` — the every-buyer `customer` concept is a named definition
  rolled up from orders, not an object.
- Storefront linkage is a **string join** on host name — orders carry no storefront_oid.

## Change log
- v1 (2026-07-06) — initial.
