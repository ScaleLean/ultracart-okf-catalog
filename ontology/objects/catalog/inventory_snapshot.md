---
type: "Ontology Object"
object: inventory_snapshot
domain: catalog
tier: supporting
resource: "urn:ultracart:ontology:object:inventory_snapshot"
version: 1
grain: "one row per inventory movement event (with before/after levels)"
key:
  fields: [item_inventory_history_oid]
  identity_family: item_inventory_history_oid
source:
  binding: uc_item_inventory_history
  default_table: "{{source_project}}.{{dataset.medium}}.uc_item_inventory_history"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: item_inventory_history_oid
    type: INTEGER
    source: item_inventory_history_oid
    meaning: "UltraCart primary key for the inventory event"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: merchant_item_id
    type: STRING
    source: merchant_item_id
    meaning: "the SKU the movement applies to (join key to item)"
  - name: merchant_item_oid
    type: INTEGER
    source: merchant_item_oid
    meaning: "internal item key (same item as merchant_item_id)"
  - name: occurred_at
    type: DATETIME
    source: history_dts
    meaning: "when the inventory movement happened"
  - name: adjustment
    type: NUMERIC
    source: adjustment
    meaning: "signed quantity change (negative = stock out, positive = stock in)"
  - name: before_level
    type: NUMERIC
    source: before_inventory_level
    meaning: "inventory level immediately before the movement"
  - name: after_level
    type: NUMERIC
    source: after_inventory_level
    meaning: "inventory level immediately after the movement — the point-in-time snapshot"
  - name: reason
    type: STRING
    source: reason
    meaning: "movement reason (order, manual adjustment, receiving…)"
  - name: order_id
    type: STRING
    source: order_id
    meaning: "order that caused the movement (NULL for non-order adjustments)"
  - name: distribution_center_code
    type: STRING
    source: distribution_center_code
    meaning: "warehouse/DC code the level applies to"
  - name: distribution_center_oid
    type: INTEGER
    source: distribution_center_oid
    meaning: "internal DC key"
links:
  - to: item
    kind: belongs_to
    on: "inventory_snapshot.merchant_item_id = item.merchant_item_id"
  - to: order
    kind: caused_by
    on: "inventory_snapshot.order_id = order.order_id"
pii: none
excluded_fields: []
consumers: []
---

# InventorySnapshot

The stock audit trail. Despite the object name, the grain is a **movement event**, not
a periodic snapshot: every adjustment writes one row carrying the signed `adjustment`
plus the `before_level`/`after_level` pair — so the latest row per item × distribution
center IS the current snapshot, and any historical level can be reconstructed by
picking the last event at or before a timestamp.

Levels are per **item × distribution center**: merchants with multiple DCs have
parallel event streams; summing `after_level` across DCs at a point in time gives
total stock. `reason` separates order-driven depletion (rows with `order_id`) from
manual adjustments, receiving, and sync corrections.

Gotchas:
- No `sku`-less rows, but `order_id` is NULL on non-order movements — don't inner-join
  to orders when computing net flow.
- `adjustment` should equal `after_level - before_level`; rows where it doesn't are a
  data-quality signal (concurrent adjustments in the source).
- This table has no nested arrays and no PII — the full field list is exposed.

## Change log
- v1 (2026-07-06) — initial.
