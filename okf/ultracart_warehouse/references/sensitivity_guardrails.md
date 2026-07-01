---
type: "Reference"
title: "Sensitivity Guardrails"
description: "Safety rules for working with UltraCart warehouse metadata and generated OKF bundles."
resource: "urn:ultracart:okf:reference:sensitivity-guardrails"
tags:
  - "ultracart"
  - "bigquery"
  - "reference"
  - "safety"
timestamp: "2026-07-01T00:00:00Z"
---

# Sensitivity Guardrails

This public bundle is metadata-only. Do not add customer rows, raw emails, addresses, phone numbers, payment details, message bodies, sampled records, or merchant-specific project identifiers to this repository.

Generated merchant bundles should stay local unless explicitly reviewed for the intended audience.

Treat row-level samples from these objects as especially sensitive, even in medium-layer views:

- `uc_analytics_sessions`
- `uc_cart_abandons`
- `uc_customers`
- `uc_orders`
- `uc_screen_recordings`
- `uc_storefront_customer_emails`
- `uc_storefront_customers`
- `uc_storefront_customer_sessions`
- `uc_towerdata_email_intelligence`
