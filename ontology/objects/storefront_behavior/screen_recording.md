---
type: "Ontology Object"
object: screen_recording
domain: storefront_behavior
tier: supporting
resource: "urn:ultracart:ontology:object:screen_recording"
version: 1
grain: "one current session/recording row per screen_recording_uuid"
key:
  fields: [screen_recording_uuid]
  identity_family: screen_recording_uuid
source:
  binding: uc_screen_recordings
  default_table: "{{source_project}}.{{dataset.medium}}.uc_screen_recordings"
  merchant_filter: "merchant_id = '{{merchant_id}}'"
properties:
  - name: screen_recording_uuid
    type: STRING
    source: screen_recording_uuid
    meaning: "primary key; the behavioral session spine referenced by affiliate_clicks and ESP customer sessions"
  - name: merchant_id
    type: STRING
    source: merchant_id
    meaning: "UltraCart merchant account"
  - name: ucacid
    type: STRING
    source: ucacid
    meaning: "analytics client id — joins analytics_session.client_id"
  - name: email_hash_b64
    type: STRING
    source: email_hash
    meaning: "customer identity when identified (base64 sha256; raw email deliberately excluded)"
  - name: order_id
    type: STRING
    source: order_id
    meaning: "order placed during the recorded session, if any (sparse)"
  - name: started_at
    type: DATETIME
    source: start_timestamp
    meaning: "session start"
  - name: ended_at
    type: DATETIME
    source: end_timestamp
    meaning: "session end"
  - name: time_on_site
    type: INTEGER
    source: time_on_site
    meaning: "time on site as reported by the tracker"
  - name: page_view_count
    type: INTEGER
    source: page_view_count
    meaning: "pages viewed in the session"
  - name: visitor_number
    type: INTEGER
    source: visitor_number
    meaning: "sequential visitor number for the merchant"
  - name: visitor_first_seen_at
    type: DATETIME
    source: visitor_first_seen
    meaning: "when this visitor was first ever seen"
  - name: utm_source
    type: STRING
    source: utm_source
    meaning: "recovered utm_source for the session"
  - name: utm_campaign
    type: STRING
    source: utm_campaign
    meaning: "recovered utm_campaign for the session"
  - name: referrer_domain
    type: STRING
    source: referrer_domain
    meaning: "referring domain"
  - name: language_iso_code
    type: STRING
    source: language_iso_code
    meaning: "browser language"
  - name: geo_country
    type: STRING
    source: geolocation_country
    meaning: "coarse geo: country (raw lat/lon excluded)"
  - name: geo_state
    type: STRING
    source: geolocation_state
    meaning: "coarse geo: state"
  - name: device_name
    type: STRING
    source: user_agent.device.name
    meaning: "parsed device name"
  - name: browser_name
    type: STRING
    source: user_agent.name
    meaning: "parsed browser name"
  - name: os_name
    type: STRING
    source: user_agent.os.name
    meaning: "parsed operating system"
  - name: window_width
    type: INTEGER
    source: window_width
    meaning: "viewport width"
  - name: window_height
    type: INTEGER
    source: window_height
    meaning: "viewport height"
  - name: gclid
    type: STRING
    source: ad_platform.glcid
    meaning: "Google click id (source schema misspells the field as glcid)"
  - name: fbclid
    type: STRING
    source: ad_platform.fbclid
    meaning: "Facebook/Meta click id"
  - name: msclkid
    type: STRING
    source: ad_platform.msclkid
    meaning: "Microsoft Ads click id"
  - name: ttclid
    type: STRING
    source: ad_platform.ttclid
    meaning: "TikTok click id"
  - name: missing_external_tracking
    type: BOOLEAN
    source: missing_external_tracking
    meaning: "session lacked external tracker coverage — the UTM/click-id recovery use case"
  - name: communications_campaign_uuid
    type: STRING
    source: communications_campaign_uuid
    meaning: "attributed ESP campaign (comms attribution surface)"
  - name: communications_campaign_name
    type: STRING
    source: communications_campaign_name
    meaning: "attributed ESP campaign name"
  - name: communications_flow_uuid
    type: STRING
    source: communications_flow_uuid
    meaning: "attributed ESP flow"
  - name: communications_flow_name
    type: STRING
    source: communications_flow_name
    meaning: "attributed ESP flow name"
  - name: communications_email_uuid
    type: STRING
    source: communications_email_uuid
    meaning: "the specific email send that drove the session — joins email_send"
  - name: storefront_oid
    type: INTEGER
    source: "(SELECT MAX(storefronts.storefront_oid) FROM UNNEST(storefronts) AS storefronts)"
    meaning: "storefront visited (MAX collapse; sessions almost never span storefronts — see storefront_count)"
  - name: storefront_count
    type: INTEGER
    source: "ARRAY_LENGTH(storefronts)"
    meaning: "storefronts touched in the session (>1 is rare; consult the array if it happens)"
links:
  - to: analytics_session
    kind: belongs_to
    on: "screen_recording.ucacid = analytics_session.client_id"
  - to: order
    kind: converted_to
    on: "screen_recording.order_id = order.order_id"
  - to: customer
    kind: belongs_to
    on: "screen_recording.email_hash_b64 = customer.email_hash_b64"
  - to: email_send
    kind: attributed_to
    on: "screen_recording.communications_email_uuid = email_send.email_uuid"
  - to: storefront
    kind: belongs_to
    on: "screen_recording.storefront_oid = storefront.storefront_oid"
pii: pseudonymous
excluded_fields:
  - email                          # RAW email — this table carries it even in mid tiers; use email_hash_b64
  - user_ip                        # RAW IP address — never expose
  - email_domain                   # quasi-identifier flagged as PII in the catalog
  - geolocation                    # fine-grained lat/lon; coarse country/state exposed instead
  - communications_email_subject   # subject lines can carry personal content
  - merchant_notes                 # free text
  - user_agent_raw                 # fingerprint-grade raw UA; parsed device/browser/os exposed instead
  - page_views                     # page-view array incl. nested events[], params, referrers
  - user_properties                # arbitrary key/value payloads
consumers: []
---

# ScreenRecording

The page-view/acquisition surface of a storefront visit, keyed by
`screen_recording_uuid` — which doubles as the **behavioral session spine**:
`uc_affiliate_clicks`, `uc_storefront_customer_sessions`, and
`uc_storefront_customers.sessions[]` all point at it. Beyond replay metadata it is the
best *attribution recovery* surface: ad-platform click IDs (`gclid`/`fbclid`/
`msclkid`/`ttclid`), recovered UTMs, referrer domain, and ESP campaign/flow/email
attribution live here even when external trackers were blocked
(`missing_external_tracking`).

**PII warning — this is the hottest table in storefront_behavior.** Unlike its
siblings, `uc_screen_recordings` carries **raw `user_ip` and raw `email`** in the
standard view stack, plus fine-grained `geolocation` lat/lon and email subjects. The
canonical object excludes all of them and keeps only `email_hash_b64` and coarse
country/state. Do not rebind this object to a wider table without re-checking those
exclusions.

**Three overlapping session surfaces — pick the right one:**

- **screen_recording** (this object): "where did the session come from, what pages did
  it hit?" — acquisition channels, click-id recovery, comms attribution, replay.
- **analytics_session** (`uc_analytics_sessions`): "what did the visitor do?" — the
  event/funnel trail (checkout steps, cart events, bot flags, in-session revenue).
- **storefront_customer_session** (`uc_storefront_customer_sessions`, marketing_comms):
  the ESP audience's view of the same visit — use for campaign-audience questions.

Bridges: `ucacid` ↔ `analytics_session.client_id`; `screen_recording_uuid` is carried
by the ESP session table and affiliate clicks; `order_id` when the visit converted.

Gotchas:
- `page_views[]` (and its nested `events[]`) are excluded; model page-level analysis
  separately if needed — `page_view_count`/`time_on_site` cover session-level rollups.
- The Google click id field is misspelled `glcid` in the source schema; the ontology
  exposes it under the correct name `gclid`.
- `storefronts[]` is an array; `storefront_oid` collapses it with MAX. Check
  `storefront_count` before trusting single-storefront assumptions.

## Change log
- v1 (2026-07-06) — initial.
