---
type: "Ontology Identity Spine"
resource: "urn:ultracart:ontology:identity"
version: 1
timestamp: "2026-07-06T00:00:00Z"
---

# Identity Spine

Every key family in the UltraCart warehouse, its format, and the bridges between
systems. Objects reference these families by name (`key.identity_family`); nothing
else in the ontology restates identity rules.

## Customer identity — the one that bites

| Encoding | Format | Where |
|---|---|---|
| `email_hash_b64` | 44-char **base64** of sha256(lower(trim(email))) | UltraCart warehouse everywhere: `billing.email_hash`, `emails.email_hash`, towerdata, storefront customer tables |
| `customer_key_hex` | 64-char lowercase **hex** of the same digest | Common in downstream dbt/warehouse layers (e.g. `TO_HEX(SHA256(LOWER(TRIM(email))))`) |

**Bridges (verified live 2026-07-05, 97% join on a real merchant; naive string join = 0%):**

```sql
TO_BASE64(FROM_HEX(customer_key_hex)) = email_hash_b64
TO_HEX(SAFE.FROM_BASE64(email_hash_b64)) = customer_key_hex
```

Base-ontology convention: objects expose **`email_hash_b64`** (the warehouse-native
encoding). Merchant overlays that key on hex should add the bridge expression, not a
second identity. Raw `billing.email` exists in the warehouse next to the hash — the
ontology never selects it (see each object's `excluded_fields`).

## OID families (UltraCart internal primary keys)

| Family | Type | Identifies | Carried by |
|---|---|---|---|
| `auto_order_oid` | INTEGER | subscription container | uc_auto_orders (+ items[].auto_order_item_oid for the item) |
| `auto_order_item_oid` | INTEGER | subscription item | uc_auto_orders.items[] |
| `merchant_item_oid` | INTEGER | catalog item (internal) | uc_items; pair of public `merchant_item_id` (the SKU) |
| `coupon_oid` | INTEGER | coupon | uc_coupons |
| `customer_profile_oid` | INTEGER | registered customer profile (≠ every buyer) | uc_customers, order.customer_profile |
| `partition_oid` | INTEGER | warehouse load partition — **not** a business key; used for latest-row dedup `QUALIFY ROW_NUMBER() OVER (PARTITION BY <key> ORDER BY partition_oid DESC) = 1` | most base tables |

## Public / human identifiers

| Identifier | Format | Notes |
|---|---|---|
| `order_id` | STRING (e.g. `DEMO-0000001234`) | the public order number; `source_order_key` style synthetic keys are overlay conventions, not warehouse-native |
| `merchant_item_id` | STRING | the SKU as merchants know it |
| `auto_order_code` | STRING | human-facing subscription reference |
| `merchant_id` | STRING | UltraCart account code; **every base-table query must filter on it** — warehouse projects can host multiple merchants |
| `storefront` / storefront host | STRING | sales channel within a merchant |

## Dedup rule (base tables)

Warehouse base tables are partitioned loads: the same business row can appear under
multiple `partition_oid`s. Canonical views over base tables MUST dedup to latest via
the `QUALIFY` pattern above. (Tier views `ultracart_dw_low/medium/high` are already
current-state; the compiler binds `dataset.medium` by default, where dedup is not
required. Rebinding to raw/streaming tables re-introduces the dedup obligation.)

## Change log
- v1 (2026-07-06) — initial; encodings + bridge verified against a live merchant.
