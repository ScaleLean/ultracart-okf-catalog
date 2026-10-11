---
type: "Ontology Identity Spine"
resource: "urn:ultracart:ontology:identity"
version: 1
families:
  - affiliate_click_oid
  - affiliate_ledger_oid
  - affiliate_oid
  - auto_order_item_oid
  - auto_order_oid
  - call_uuid
  - cart_abandon_uuid
  - client_session_oid
  - conversation_uuid
  - coupon_code
  - customer_profile_oid
  - email_hash_b64
  - email_uuid
  - esp_customer_uuid
  - gift_certificate_oid
  - item_inventory_history_oid
  - merchant_item_id
  - order_id
  - rotating_transaction_gateway_oid
  - screen_recording_uuid
  - storefront_experiment_oid
  - storefront_oid
  - storefront_upsell_offer_event_oid
  - workflow_task_uuid
  - zoho_desk_ticket_id
timestamp: "2026-07-06T00:00:00Z"
---

# Identity Spine

Key families declared by the ontology, their documented formats, and proposed
bridges between systems. This is not an exhaustive warehouse-key inventory.
Objects reference these families by name (`key.identity_family`); nothing
else in the ontology restates identity rules.

## Customer identity — the one that bites

| Encoding | Format | Where |
|---|---|---|
| `email_hash_b64` | 44-char **base64** of sha256(lower(trim(email))) | UltraCart warehouse everywhere: `billing.email_hash`, `emails.email_hash`, towerdata, storefront customer tables |
| `customer_key_hex` | 64-char lowercase **hex** of the same digest | Common in downstream warehouse layers (not used by this ontology, which keys on the base64 hash) (e.g. `TO_HEX(SHA256(LOWER(TRIM(email))))`) |

**Historical bridge report (2026-07-05):** one merchant reportedly had a 97% join
with these conversions and 0% with a naive string join. The private evidence was
not rechecked offline; these percentages are not acceptance thresholds.

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
required. Raw/streaming and other binding overrides are rejected by the offline
compiler; their grain and scope cannot be established here.)

## Declared object-key families

These family types come from existing object properties; object keys may be
composite (for example, order_item also includes an item index). They are declarations,
not new observations of key uniqueness or cross-system equivalence.

| Family | Declared family type | Objects |
|---|---|---|
| `affiliate_click_oid` | INTEGER | `affiliate_click` |
| `affiliate_ledger_oid` | INTEGER | `affiliate_ledger` |
| `affiliate_oid` | INTEGER | `affiliate` |
| `auto_order_item_oid` | INTEGER | `auto_order_item` |
| `auto_order_oid` | INTEGER | `auto_order` |
| `call_uuid` | STRING | `pbx_call` |
| `cart_abandon_uuid` | STRING | `cart_abandon` |
| `client_session_oid` | INTEGER | `analytics_session` |
| `conversation_uuid` | STRING | `conversation` |
| `coupon_code` | STRING | `coupon` |
| `customer_profile_oid` | INTEGER | `customer_profile` |
| `email_hash_b64` | STRING | `person_enrichment` |
| `email_uuid` | STRING | `email_send` |
| `esp_customer_uuid` | STRING | `email_list_membership`, `email_segment_membership`, `marketing_contact` |
| `gift_certificate_oid` | INTEGER | `gift_certificate` |
| `item_inventory_history_oid` | INTEGER | `inventory_snapshot` |
| `merchant_item_id` | STRING | `item` |
| `order_id` | STRING | `order`, `order_item` |
| `rotating_transaction_gateway_oid` | INTEGER | `payment_gateway` |
| `screen_recording_uuid` | STRING | `screen_recording` |
| `storefront_experiment_oid` | INTEGER | `experiment` |
| `storefront_oid` | INTEGER | `storefront` |
| `storefront_upsell_offer_event_oid` | INTEGER | `upsell_offer_event` |
| `workflow_task_uuid` | STRING | `workflow_task` |
| `zoho_desk_ticket_id` | STRING | `support_ticket` |

## Change log
- v1 (2026-07-06) — initial; encodings + bridge verified against a live merchant.
