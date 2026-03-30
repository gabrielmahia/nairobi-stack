# nairobi-stack

**The engineering guide for building software products in East Africa.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A practical, opinionated reference for developers — in Kenya, the diaspora, or anywhere building for East African users. Covers APIs, infrastructure choices, UX patterns, regulatory context, and the cultural nuances that documentation never mentions.

---

## Why this exists

Western developer documentation assumes broadband, credit cards, app stores, and English-only users. East African users may have any combination of: feature phones, sporadic 2G, M-Pesa (no bank account), Kiswahili or Sheng as primary language, prepaid data, and screen sizes that haven't been in a Western product review since 2014.

This guide is built from real integration work across three production systems — [Catholic Network Tools](https://github.com/gabrielmahia/jumuia), [OpenResilience](https://github.com/gabrielmahia/openresilience), and [RemitLens](https://github.com/gabrielmahia/remit-lens) — plus field experience in Nairobi, Mombasa, and across Kenya's 47 counties.

---

## Guides

### Payments
- [M-Pesa Integration](guides/mpesa-integration.md) — STK Push, B2C, webhooks, sandbox-to-live
- [Remittance APIs](guides/remittance-apis.md) — Wise, Remitly, Sendwave: what's available, what's not

### Communication
- [USSD Patterns](guides/ussd-patterns.md) — menus, sessions, Africa's Talking
- [SMS Infrastructure](guides/sms-infrastructure.md) — Africa's Talking, shortcodes, DLT registration

### Data & Live APIs
- [Live Data APIs](guides/live-data-apis.md) — 11 free keyless APIs confirmed working in Kenya: Open-Meteo, NDMA, COB, World Bank, WFP/HDX, LSK/FIDA/Judiciary RSS, open.er-api.com, Yahoo Finance

### Design
- [Mobile-First UX for Kenya](guides/mobile-first-ux.md) — offline, low-data, feature phone realities
- [Kiswahili in Your Product](guides/kiswahili-in-products.md) — translation, tone, Sheng, code-switching

### Infrastructure
- [Deploying in East Africa](guides/deploying-in-east-africa.md) — latency, CDN, AWS vs local hosting
- [Kenya Data Protection Act](guides/kenya-dpa.md) — ODPC compliance, consent, cross-border data

### Finance & Regulatory
- [Regulatory Landscape](guides/regulatory-landscape.md) — CBK, CMA, Communications Authority
- [Chama Digitisation](guides/chama-digitisation.md) — domain model, M-Pesa integration, ROSCAs

---

## Contributing

This is a living document. If you've built something in East Africa and learned something the hard way, open a PR. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

*Maintained by [Gabriel Mahia](https://github.com/gabrielmahia). Kenya × USA.*

## MCP ecosystem updates (2026)

Key developments relevant to East African developers building on mpesa-mcp:

### Tool annotations (spec 2025-03-26)

All MCP tools should declare behavioral hints. For payment/SMS servers this is critical:

```python
@mcp.tool(annotations={
    'title': 'M-Pesa STK Push',
    'readOnlyHint': False,      # modifies state (moves money)
    'destructiveHint': True,    # irreversible financial operation
    'idempotentHint': False,    # each call creates a new transaction
    'openWorldHint': True,      # reaches Safaricom's external API
})
def mpesa_stk_push(phone: str, amount: int, ...):
```

Without these, Claude Desktop and ChatGPT treat all tools as potentially destructive and may add unnecessary friction on read operations.

### Server Cards / .well-known (roadmap Q2 2026)

Servers can advertise capabilities via `.well-known/mcp.json` — a static JSON file at the repo root that registries can index without connecting to your server. Add this to any MCP server you publish.

### MCP accuracy benchmark

CData's 2026 benchmark found MCP servers accurate 60–75% on complex queries. Write operations (payments, SMS) are the highest-risk category — test for:
- All phone number formats: `0712345678`, `254712345678`, `+254712345678`
- Boundary amounts (minimum 1 KES, maximum per API limit)
- Missing optional fields (reference, description)

### Streamlit 1.55.0 (March 2026)

Key changes for East African app builders:
- `st.metric` now has `delta_description` parameter — add context like "vs last month"
- `st.tabs` supports `on_change` — dynamic loading of heavy data only when tab is opened
- `st.image` has `link` parameter — clickable images for maps and charts
- Widget binding (`bind` parameter) — sync widget state with URL query params for shareable links
