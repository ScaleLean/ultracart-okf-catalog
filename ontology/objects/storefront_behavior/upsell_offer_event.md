---
type: "Ontology Object"
object: upsell_offer_event
domain: storefront_behavior
tier: supporting
resource: "urn:ultracart:ontology:object:upsell_offer_event"
version: 1
grain: "one upsell offer impression/outcome event per storefront_upsell_offer_event_oid"
key:
  fields: [storefront_upsell_offer_event_oid]
  identity_family: storefront_upsell_offer_event_oid
source:
  binding: uc_storefront_upsell_offer_events
  default_table: "{{source_project}}.{{dataset.medium}}.uc_storefront_upsell_offer_events"
properties:
  - name: storefront_upsell_offer_event_oid
    type: INTEGER
    source: storefront_upsell_offer_event_oid
    meaning: "primary key for the upsell event"
  - name: storefront_upsell_offer_oid
    type: INTEGER
    source: storefront_upsell_offer_oid
    meaning: "which configured offer fired (offer/path config lives in uc_storefront_upsell_offers / _paths)"
  - name: event_at
    type: DATETIME
    source: event_dts
    meaning: "when the offer was shown"
  - name: session_id
    type: STRING
    source: session_id
    meaning: "storefront checkout session id (not the analytics ucacid)"
  - name: order_id
    type: STRING
    source: order_id
    meaning: "the order the upsell attached to"
  - name: item_id
    type: STRING
    source: item_id
    meaning: "offered SKU — joins item.merchant_item_id"
  - name: view_count
    type: INTEGER
    source: view_count
    meaning: "times the offer was viewed in the session"
  - name: decline_count
    type: INTEGER
    source: decline_count
    meaning: "times the shopper declined"
  - name: successful_charge
    type: INTEGER
    source: successful_charge
    meaning: "successful charge counter for the accepted offer (0 = never charged)"
  - name: converted
    type: BOOLEAN
    source: "successful_charge > 0"
    meaning: "derived: the offer was accepted and charged"
  - name: quantity
    type: INTEGER
    source: quantity
    meaning: "units sold via the offer"
  - name: revenue
    type: NUMERIC
    source: revenue
    meaning: "upsell revenue (base currency)"
  - name: profit
    type: NUMERIC
    source: profit
    meaning: "upsell profit (base currency)"
  - name: refund_quantity
    type: INTEGER
    source: refund_quantity
    meaning: "units later refunded"
  - name: refunded_revenue
    type: NUMERIC
    source: refunded_revenue
    meaning: "revenue later refunded"
  - name: refunded_profit
    type: NUMERIC
    source: refunded_profit
    meaning: "profit later refunded"
  - name: currency_code
    type: STRING
    source: currency_code
    meaning: "localized currency of the *_localized twins"
  - name: exchange_rate
    type: NUMERIC
    source: exchange_rate
    meaning: "exchange rate used for localization"
  - name: screen_size
    type: STRING
    source: screen_size
    meaning: "device screen-size bucket the offer rendered on"
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
    meaning: "UTM touches on the event (>1: consult the excluded utms array, which carries per-model attribution weights)"
  - name: first_click_at
    type: DATETIME
    source: "(SELECT MIN(utms.click_dts) FROM UNNEST(utms) AS utms)"
    meaning: "earliest recorded ad/UTM click behind the event"
links:
  - to: order
    kind: belongs_to
    on: "upsell_offer_event.order_id = order.order_id"
  - to: item
    kind: references
    on: "upsell_offer_event.item_id = item.merchant_item_id"
pii: none
excluded_fields:
  - utms                                # multi-touch array incl. first/last/linear/position-based attribution economics
  - profit_localized_formatted          # display strings; numeric twins retained via base-currency fields
  - revenue_localized_formatted
  - refunded_profit_localized_formatted
  - refunded_revenue_localized_formatted
consumers: []
---

# UpsellOfferEvent

The impression → decline → charge log for post-checkout upsell offers, with per-event
economics (revenue/profit and their refunded counterparts). This is the *outcome* side
of the upsell system: offer and funnel configuration live in
`uc_storefront_upsell_offers` / `uc_storefront_upsell_paths` (peripheral config tables,
not modeled as objects); orders record the accepted path via
`checkout.upsell_path_code`.

Standard questions: offer take rate (`converted` / events), net upsell revenue
(`revenue - refunded_revenue`), decline pressure (`decline_count`) by offer and by
`screen_size`.

Gotchas:
- **No `merchant_id` on this table** — the compiler applies no merchant filter. On a
  multi-merchant warehouse project, scope by joining `order_id` to `order` (which is
  merchant-filtered) before aggregating.
- `session_id` is the storefront checkout session, *not* the analytics `ucacid` and not
  a `screen_recording_uuid`; treat cross-surface session joins as going through
  `order_id`.
- The excluded `utms[]` array carries pre-computed first-click / last-click / linear /
  position-based revenue splits per touch — if multi-touch upsell attribution is ever
  needed, model that array rather than re-deriving.
- `revenue`/`profit` are base-currency; `*_localized` twins (excluded formatted strings,
  and localized numerics available in the source) use `currency_code`/`exchange_rate`.

## Change log
- v1 (2026-07-06) — initial.
