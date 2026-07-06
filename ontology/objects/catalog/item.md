---
type: "Ontology Object"
object: item
domain: catalog
tier: core
resource: "urn:ultracart:ontology:object:item"
version: 1
grain: "one row per catalog item/SKU"
key:
  fields: [merchant_item_id]
  identity_family: merchant_item_id
source:
  binding: uc_items
  default_table: "{{source_project}}.{{dataset.medium}}.uc_items"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: merchant_item_oid
    type: INTEGER
    source: merchant_item_oid
    meaning: "UltraCart internal primary key for the item"
  - name: merchant_item_id
    type: STRING
    source: merchant_item_id
    meaning: "the SKU as merchants know it — the key orders and auto-orders join on"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: description
    type: STRING
    source: description
    meaning: "item display description/title"
  - name: parent_category_id
    type: INTEGER
    source: parent_category_id
    meaning: "catalog category the item lives under"
  - name: parent_category_path
    type: STRING
    source: parent_category_path
    meaning: "full category path string"
  - name: is_active
    type: BOOLEAN
    source: "NOT inactive"
    meaning: "derived: sellable/visible (source stores the inverted `inactive` flag)"
  - name: is_kit
    type: BOOLEAN
    source: kit
    meaning: "item is a kit that explodes into component items"
  - name: is_kit_component_only
    type: BOOLEAN
    source: kit_component_only
    meaning: "item exists only as a kit component, not sold standalone"
  - name: kit_component_count
    type: INTEGER
    source: "ARRAY_LENGTH(kit_definition.components)"
    meaning: "number of components in the kit definition (0/NULL for non-kits)"
  - name: price
    type: NUMERIC
    source: pricing.cost
    meaning: "the sell price — UltraCart calls the customer-facing price `cost`"
  - name: sale_price
    type: NUMERIC
    source: pricing.sale_cost
    meaning: "sale-window sell price"
  - name: sale_start_at
    type: DATETIME
    source: pricing.sale_start
    meaning: "sale price window start"
  - name: sale_end_at
    type: DATETIME
    source: pricing.sale_end
    meaning: "sale price window end"
  - name: auto_order_price
    type: NUMERIC
    source: pricing.auto_order_cost
    meaning: "recurring (auto-order/subscription) sell price"
  - name: cogs
    type: NUMERIC
    source: pricing.cogs
    meaning: "cost of goods sold — the actual unit cost, NOT `pricing.cost`"
  - name: msrp
    type: NUMERIC
    source: pricing.manufacturer_suggested_retail_price
    meaning: "manufacturer suggested retail price"
  - name: currency_code
    type: STRING
    source: pricing.currency_code
    meaning: "currency of the pricing fields"
  - name: mix_and_match_group
    type: STRING
    source: pricing.mix_and_match_group
    meaning: "mix-and-match pricing group name (coupons reference these groups)"
  - name: is_auto_orderable
    type: BOOLEAN
    source: auto_order.auto_orderable
    meaning: "can be purchased on a subscription"
  - name: is_auto_order_paused
    type: BOOLEAN
    source: auto_order.auto_order_paused
    meaning: "merchant has paused new/rebilling auto-orders for this item"
  - name: barcode
    type: STRING
    source: identifiers.barcode
    meaning: "UPC/EAN barcode"
  - name: manufacturer_name
    type: STRING
    source: identifiers.manufacturer_name
    meaning: "manufacturer/brand name"
  - name: manufacturer_sku
    type: STRING
    source: identifiers.manufacturer_sku
    meaning: "manufacturer's own SKU"
  - name: excludes_coupons
    type: BOOLEAN
    source: restriction.exclude_coupon
    meaning: "coupons may not discount this item"
  - name: excluded_from_loyalty
    type: BOOLEAN
    source: restriction.exclude_from_loyalty
    meaning: "purchases do not earn loyalty"
  - name: one_per_customer
    type: BOOLEAN
    source: restriction.one_per_customer
    meaning: "quantity restricted to one per customer"
  - name: minimum_quantity
    type: INTEGER
    source: restriction.minimum_quantity
    meaning: "minimum order quantity"
  - name: maximum_quantity
    type: INTEGER
    source: restriction.maximum_quantity
    meaning: "maximum order quantity"
  - name: created_at
    type: DATETIME
    source: creation_dts
    meaning: "item creation timestamp"
  - name: last_modified_at
    type: DATETIME
    source: last_modified_dts
    meaning: "last catalog modification timestamp"
links:
  - to: inventory_snapshot
    kind: has_many
    on: "item.merchant_item_id = inventory_snapshot.merchant_item_id"
  - to: order_item
    kind: referenced_by
    on: "item.merchant_item_id = order_item.merchant_item_id"
  - to: auto_order_item
    kind: referenced_by
    on: "item.merchant_item_id = auto_order_item.original_item_id"
pii: none
excluded_fields: [accounting, amember, auto_order.steps, ccbill, channel_partner_item_mappings, chargeback, checkout, content, digital_delivery, ebay, email_notifications, enrollment123, fulfillment_addons, gated_codes, gift_certificate, google_product_search, instant_payment_notifications, internal, kit_definition, options, payment_processing, physical, pricing.tiers, properties, realtime_pricing, related, reporting, revguard, reviews, salesforce, shipping, tags, tax, third_party_email_marketing, variant_items, variations, wishlist_member]
consumers: []
---

# Item

The product catalog: one row per SKU. This is the smallest "core" table by row count
but the widest by config surface — 716 field paths, almost all of them merchant
configuration structs (channel feeds, digital delivery, tax, shipping methods,
review syndication…). The canonical view keeps the ~30 analytically useful fields and
drops the rest via `excluded_fields`.

Identity: `merchant_item_oid` is the internal primary key, but **everything else in the
warehouse joins by the `merchant_item_id` string** (the SKU): `uc_orders.items[].merchant_item_id`,
auto-order items, affiliate ledgers, upsell events, inventory history. That is why the
ontology key is `merchant_item_id`, with the oid exposed as a plain property.

Lifecycle: the source flag is **`inactive`** — the ontology inverts it to `is_active`.
There is no deletion timestamp; retired SKUs simply flip `inactive` (watch
`last_modified_at` for when).

Gotchas:
- **`pricing.cost` is the SELL price, not the cost.** The actual unit cost is
  `pricing.cogs`. Margin = `price - cogs`, never `cost - cogs` naïvely read.
- `auto_order_price` (`pricing.auto_order_cost`) is what rebills charge; comparing it
  to `price` shows the subscription discount.
- Kits: `is_kit` items explode into `kit_definition.components` at order time;
  `is_kit_component_only` items never sell standalone — exclude them from
  catalog-breadth counts. Component detail stays in the excluded `kit_definition` struct.
- Variants live as separate item rows related through the excluded `variant_items`
  array; `options`/`variations` (buyer-choice config) are excluded too.
- `restriction.items[]` (cross-item purchase restrictions) is excluded; only the scalar
  restriction highlights are surfaced.

## Change log
- v1 (2026-07-06) — initial.
