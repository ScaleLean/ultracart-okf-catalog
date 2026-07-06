---
type: "Ontology Object"
object: payment_gateway
domain: risk_finance
tier: supporting
resource: "urn:ultracart:ontology:object:payment_gateway"
version: 1
grain: "one row per rotating transaction gateway configuration"
key:
  fields: [rotating_transaction_gateway_oid]
  identity_family: rotating_transaction_gateway_oid
source:
  binding: uc_rotating_transaction_gateways
  default_table: "{{source_project}}.{{dataset.medium}}.uc_rotating_transaction_gateways"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: rotating_transaction_gateway_oid
    type: INTEGER
    source: rotating_transaction_gateway_oid
    meaning: "UltraCart primary key for the gateway"
  - name: code
    type: STRING
    source: code
    meaning: "gateway code — the string orders and gateway history join on"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: status
    type: STRING
    source: status
    meaning: "raw gateway status (source enum, not normalized here)"
  - name: start_date
    type: DATETIME
    source: start_date
    meaning: "in-service window start"
  - name: end_date
    type: DATETIME
    source: end_date
    meaning: "in-service window end (NULL = open-ended)"
  - name: is_in_service_window
    type: BOOLEAN
    source: "(start_date IS NULL OR start_date <= CURRENT_DATETIME()) AND (end_date IS NULL OR end_date > CURRENT_DATETIME())"
    meaning: "derived: inside the configured start/end window right now"
  - name: traffic_percentage
    type: NUMERIC
    source: traffic_percentage
    meaning: "share of new transactions routed to this gateway"
  - name: preferred_for_auto_orders
    type: BOOLEAN
    source: preferred_for_auto_orders
    meaning: "rotation prefers this gateway for subscription rebills"
  - name: charge_appears_on_statement_as
    type: STRING
    source: charge_appears_on_statement_as
    meaning: "card-statement descriptor"
  - name: base_currency_code
    type: STRING
    source: base_currency_code
    meaning: "gateway settlement currency"
  - name: require_cvv2
    type: BOOLEAN
    source: require_cvv2
    meaning: "CVV2 required on transactions"
  - name: maximum_daily
    type: NUMERIC
    source: maximum_daily
    meaning: "daily processing cap"
  - name: current_daily
    type: NUMERIC
    source: current_daily
    meaning: "volume consumed against the daily cap"
  - name: maximum_monthly
    type: NUMERIC
    source: maximum_monthly
    meaning: "monthly processing cap"
  - name: current_monthly
    type: NUMERIC
    source: current_monthly
    meaning: "volume consumed against the monthly cap"
  - name: maximum_daily_auto_order
    type: NUMERIC
    source: maximum_daily_auto_order
    meaning: "daily cap specifically for auto-order rebill volume"
  - name: current_daily_auto_order
    type: NUMERIC
    source: current_daily_auto_order
    meaning: "rebill volume consumed against the auto-order daily cap"
  - name: deactivate_after_failures
    type: INTEGER
    source: deactivate_after_failures
    meaning: "consecutive failures before the rotation pulls this gateway"
  - name: cascade_code
    type: STRING
    source: cascade_code
    meaning: "gateway code to cascade declined transactions to"
  - name: cascade_daily_auto_order_code
    type: STRING
    source: cascade_daily_auto_order_code
    meaning: "cascade target when the auto-order daily cap is hit"
  - name: rebill_against_gateway_code
    type: STRING
    source: rebill_auto_orders_against_this_rtg_code
    meaning: "rebills stick to this gateway code regardless of rotation"
  - name: reserve_percentage
    type: NUMERIC
    source: reserve_percentage
    meaning: "processor rolling-reserve percentage withheld"
  - name: reserve_days
    type: INTEGER
    source: reserve_days
    meaning: "days reserve funds are held"
  - name: reserves_released_through
    type: DATETIME
    source: reserves_released_through
    meaning: "reserve funds released up to this date"
  - name: cumulative_domestic_revenue
    type: NUMERIC
    source: cumulative_domestic_revenue
    meaning: "lifetime domestic volume processed"
  - name: cumulative_international_revenue
    type: NUMERIC
    source: cumulative_international_revenue
    meaning: "lifetime international volume processed"
  - name: maximum_international_percentage
    type: NUMERIC
    source: maximum_international_percentage
    meaning: "cap on international share of volume"
links:
  - to: order
    kind: referenced_by
    on: "payment_gateway.code = order.payment_gateway_code"
pii: none
excluded_fields: [customer_service_email, customer_service_phone, additional_native_currency_codes, auto_order_cancel_unless_response_values, currency_code_restrictions, day_of_month_restrictions, day_of_week_restrictions, prevent_cascade_if_response_values, theme_restrictions]
consumers: []
---

# PaymentGateway

A rotating-gateway slot: high-risk/subscription merchants spread card volume across
multiple merchant accounts ("MIDs"), and this table is the routing config for each —
traffic split (`traffic_percentage`), daily/monthly caps with live counters, decline
cascades (`cascade_code`), auto-deactivation thresholds, and processor rolling-reserve
terms. It is a **config-with-live-counters** table, not a transaction log; the
per-attempt history is `uc_rotating_transaction_gateway_history` (not an object in
this batch).

**Join gotcha: orders reference gateways by CODE string, not oid.**
`uc_orders.payment.rotating_transaction_gateway_code = uc_rotating_transaction_gateways.code`,
and the same code string appears on auto-orders and in the gateway history. The oid is
the primary key of this table only — expose it, key on it, but join by `code`.

Gotchas:
- `status` is passed through raw; the source enum values are not documented in the
  OKF field paths, so no derived live-flag is built on it. `is_in_service_window`
  covers the date-window half of "is this gateway live".
- Cap counters (`current_daily`, `current_monthly`, `current_daily_auto_order`) reset
  on the `next_*_reset` schedule in the source — they are point-in-time as of the
  warehouse load, not historical series.
- `customer_service_email`/`customer_service_phone` are merchant-staff contact
  strings, not customer PII, but they are still raw email/phone fields — excluded per
  ontology PII policy; `pii: none` describes the canonical view.

## Change log
- v1 (2026-07-06) — initial.
