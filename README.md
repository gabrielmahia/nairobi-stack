# nairobi-stack

**The engineering guide for building software products in East Africa.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A practical, opinionated reference for developers — in Kenya, the diaspora, or anywhere building for East African users. Covers APIs, infrastructure choices, UX patterns, regulatory context, and the cultural nuances that documentation never mentions.

---

## Why this exists

Western developer documentation assumes broadband, credit cards, stable addresses, and English. East African users have M-Pesa, variable connectivity, shared phones, and six official languages in Kenya alone. Standard tutorials don't translate.

This is the document I wish existed when I started building for Nairobi.

---

## Contents

- [Payment Infrastructure](#payment-infrastructure)
- [SMS and Voice](#sms-and-voice)
- [Connectivity and Offline-First](#connectivity-and-offline-first)
- [Identity and KYC](#identity-and-kyc)
- [Maps and Location](#maps-and-location)
- [Data and Agriculture](#data-and-agriculture)
- [Regulatory Context](#regulatory-context)
- [UX Patterns that Work](#ux-patterns-that-work)
- [Infrastructure Choices](#infrastructure-choices)
- [The Diaspora Engineer Advantage](#the-diaspora-engineer-advantage)

---

## Payment Infrastructure

### M-Pesa (Safaricom Daraja v3)

The dominant payment rail. ~97% mobile money market share in Kenya. If you build one payment integration, it's this.

**Get started:** [developer.safaricom.co.ke](https://developer.safaricom.co.ke) — free sandbox, instant access.

**Python SDK:** [`mpesa-python`](https://github.com/gabrielmahia/mpesa-python) — production-grade, zero dependencies.

**Key flows:**
| Flow | Use case | Daraja API |
|------|----------|-----------|
| STK Push | Collect from customer | `/mpesa/stkpush/v1/processrequest` |
| C2B | Receive paybill payments | `/mpesa/c2b/v1/registerurl` |
| B2C | Disburse to customer | `/mpesa/b2c/v3/paymentrequest` |
| B2B | Pay a business | `/mpesa/b2b/v1/paymentrequest` |

**Common gotchas:**
- Phone numbers must be `2547XXXXXXXX` format — normalise on input
- `Amount` must be an integer (KES only, no decimals)
- `AccountReference` max 12 characters — silently truncated otherwise
- Sandbox and production use different base URLs and different credentials
- Tokens expire in 3600s — cache them, don't re-fetch on every request
- Webhooks are `POST` with `application/json` body — no signature verification (use IP allowlisting in production: Safaricom publishes their IP ranges)

**Production checklist:**
- [ ] Switch `sandbox=False` and use production credentials
- [ ] HTTPS on your callback URL (Daraja will not POST to HTTP in production)
- [ ] IP allowlisting for Safaricom's IP ranges on your callback endpoint
- [ ] Idempotency: Daraja can double-deliver callbacks — use `MpesaReceiptNumber` as your idempotency key
- [ ] Handle `ResultCode: 1032` (user cancelled) gracefully — it's common

### Airtel Money

Second payment rail. API via [developers.airtel.africa](https://developers.airtel.africa). Worth adding for ~20% market coverage that M-Pesa misses.

### Equity Bank / KCB / NCBA

Bank APIs exist but require business account and approval process (weeks to months). Not the first thing to build. M-Pesa first, bank rails later.

### Flutterwave / Paystack

Regional aggregators. Handle the M-Pesa integration for you (at a markup). Worthwhile if you need multi-country coverage quickly (Kenya, Nigeria, Ghana, Rwanda simultaneously). Build direct if Kenya-only.

---

## SMS and Voice

### Africa's Talking

The standard. Clean API, free sandbox, pay-as-you-go.

```python
import africastalking

africastalking.initialize("your_username", "your_api_key")
sms = africastalking.SMS

response = sms.send("Hello, habari!", ["+254712345678"])
```

**Gotchas:**
- Sender ID registration takes 5-10 business days in Kenya — start early
- Unregistered sender IDs default to `AFRICASTALKING` or a random shortcode
- Unicode (Kiswahili characters like special punctuation) costs more — test your charset detection
- Delivery reports are async webhooks — not part of the send response

**Bulk SMS pricing (Kenya, 2024):** ~KES 0.8/SMS standard, ~KES 1.2/SMS premium sender ID. Volume discounts at scale.

### USSD

The killer feature for feature phones. Africa's Talking handles USSD well. Your app exposes an HTTP endpoint that responds synchronously; AT handles the session state machine.

```
CON Welcome to MyApp
1. Check balance
2. Pay bill
0. Exit
```

See [`guides/ussd-patterns.md`](guides/ussd-patterns.md) for full session design guide.

### WhatsApp Business API

Meta's Cloud API is now free tier available. Worth adding for the middle segment (smartphone + WhatsApp, but not comfortable with web apps). Good for conversational flows.

---

## Connectivity and Offline-First

**Assume variable connectivity.** 4G penetration in Nairobi is high; rural Kenya is 2G/3G with frequent drops.

Design patterns that work:
- **Progressive enhancement** — core function works on slow connections; richer UX loads conditionally
- **Optimistic UI** — show success immediately, reconcile in background
- **Sync queues** — local-first storage that syncs when connected (PouchDB, SQLite + sync)
- **SMS fallback** — critical alerts go via SMS if push/web fails (see Africa's Talking above)
- **File sizes** — compress everything; a 3MB page load takes 30 seconds on 2G

**What this rules out:**
- Real-time video calls as a core feature
- Heavy JavaScript frameworks for users on low-end Android
- CDNs that don't have a Nairobi edge (Cloudflare does; Fastly coverage is thinner)

---

## Identity and KYC

### National ID

Kenya National ID (`Huduma Namba`) is the standard identity document. Most KYC flows collect it. There is no open API for verification — it goes through licensed KYC providers.

**KYC providers:**
- **IPRS via licensed partners** — Smile Identity, Onfido, Identitypass
- **Smile Identity** — good Africa coverage, SDKs available, used by fintechs
- **Metamap** (formerly Trulioo) — broader coverage including EAC countries

### Kenya Revenue Authority (KRA)

KRA PIN is required for any business registration and for tax compliance tooling. No public API for PIN verification — manual lookup at [kra.go.ke](https://www.kra.go.ke) or through licensed providers.

### Phone-based identity

For non-financial apps: phone number + OTP is the fastest identity layer. Most Kenyans use the same number for years. Airtime-based OTP via Africa's Talking is instant and trusted.

---

## Maps and Location

### Addresses don't work

Most Kenya addresses are relative: "next to the petrol station, past the market, behind the school." What3Words has traction but is not universal. GPS coordinates work best for infrastructure.

**What actually works:**
- GPS coordinates collected at point of service
- Plus Codes (Google's open alternative to What3Words)
- Landmark-based description field (always add one)
- County + ward selection dropdown (official administrative boundary)

### Kenya administrative boundaries

Kenya → 47 Counties → Sub-counties → Wards → Villages.

**Open data sources:**
- [africaopendata.org](https://africaopendata.org) — county and ward shapefiles
- [OpenStreetMap Kenya](https://wiki.openstreetmap.org/wiki/WikiProject_Kenya) — detailed but variable quality
- Kenya National Bureau of Statistics (KNBS) — official, downloadable

### OpenStreetMap

Good coverage in Nairobi, Mombasa, Kisumu. Sparse in rural areas. Best used for urban features and major roads. For parish/church location, OSM Overpass API works well (see `catholic-network-tools` for a production implementation).

---

## Data and Agriculture

### Kenya Meteorological Department (KMD)

Free historical and forecast data via [meteo.go.ke](https://meteo.go.ke). API access requires formal request and is slow. Third-party sources (Open-Meteo, WeatherAPI) are faster for most use cases.

### CHIRPS Rainfall Data

Climate Hazards Group InfraRed Precipitation with Station data. Free. 5km resolution across Africa. Downloadable at [chc.ucsb.edu/data/chirps](https://www.chc.ucsb.edu/data/chirps). Used in `openresilience`.

### USDA FEWS NET

Famine Early Warning Systems Network. Free food security bulletins, IPC phase maps, market data. API via [fews.net](https://fews.net). Best available public data for food insecurity in East Africa.

### Kenya Open Data

[opendata.go.ke](https://opendata.go.ke) — official portal. Variable quality and update frequency. Census data (2019) is reliable. Agricultural data is patchy.

---

## Regulatory Context

### Data protection

**Kenya Data Protection Act (2019)** — broadly similar to GDPR. Key requirements:
- Data protection policy required if you collect personal data
- Data Protection Officer required for large-scale processing
- Data residency preference for sensitive data (not strict requirement yet)
- Office of the Data Protection Commissioner ([odpc.go.ke](https://odpc.go.ke)) is active

**Practical minimum:**
- Privacy policy on your site
- Consent capture at registration
- Data deletion on request
- Don't store what you don't need

### Fintech licensing

Collecting and holding user funds requires Central Bank of Kenya (CBK) licensing. Building on top of licensed rails (M-Pesa, bank APIs) generally doesn't — but get legal advice for your specific case.

### Communications

Apps that send bulk SMS need a Communications Authority of Kenya (CA) shortcode registration. Africa's Talking handles most of the paperwork.

---

## UX Patterns that Work

**Phone-first, not mobile-first.** Design for the phone call model: quick, task-oriented, minimal cognitive load.

| Pattern | Why it works |
|---------|--------------|
| USSD menus | Feature phone compatible, works offline, familiar to all demographics |
| WhatsApp for support | Users already live in WhatsApp; beats email by 10x response rate |
| SMS confirmation | Trust signal; M-Pesa has conditioned users to expect SMS for any transaction |
| Kiswahili language option | Instant trust signal for government-adjacent or NGO products |
| M-Pesa as identity | "Pay KES 1 to verify" — unique phone-payment link is strong KYC for low-stakes flows |
| Local currency always | Never show USD to a Kenyan user unless they're in the diaspora flow |
| Data-lite mode | Offer a version that works on 2G; images optional, text-only fallback |

**What doesn't work:**
- Email-first flows (email open rates in Kenya are low; WhatsApp > email)
- Credit card payments as primary (M-Pesa first, card as secondary)
- Long forms on mobile (break into steps; collect only what you need)
- English-only for rural or elderly users

---

## Infrastructure Choices

### Hosting

| Choice | When | Why |
|--------|------|-----|
| **Streamlit Cloud** | Prototypes, internal tools | Free tier, GitHub deploy, good for data apps |
| **Railway / Render** | Small production APIs | Simple, free tier, auto-deploys |
| **DigitalOcean** | Serious production | Nairobi region (nbo1) — low latency for KE users |
| **AWS / GCP** | Enterprise | GCP has Johannesburg region; AWS Cape Town |
| **Vercel / Netlify** | Frontend | Fine, edge network includes Africa |

**For Kenya-focused apps:** DigitalOcean `nbo1` (Nairobi) is the right answer. Ping from Nairobi to London is ~140ms; to Nairobi datacenter is ~5ms.

### Database

SQLite is underrated for small apps (under 100 write/s). Scales further than people think.

Postgres on Supabase (free tier, `af-south-1` region via AWS) is the sweet spot for apps that need a proper database.

### SMS infrastructure

Africa's Talking for everything SMS. Don't build on Twilio unless you need global coverage — AT is cheaper, better-integrated with East African networks, and the API is clean.

---

## The Diaspora Engineer Advantage

Building for Kenya from the USA (or UK, Germany, Canada) gives you something most Kenya-based engineers don't have and most US-based engineers can't get:

**What you have:**
- Access to US-market tooling, pricing, and partnerships
- Experience with production engineering standards (CI/CD, testing, observability)
- Credibility with Western investors and international partners
- Fluency in both markets and their failure modes

**What to use it for:**
- Bridging Western B2B tools to East African contexts (M-Pesa integrations for global platforms)
- Building the infrastructure layer that East African developers need (like this SDK)
- Products that serve diaspora-to-Kenya flows (remittances, investment, family coordination)
- Consulting for Western companies entering East Africa

**What to avoid:**
- Parachuting in with solutions to problems you don't understand from lived experience
- Building for the Kenyan market you imagine rather than the one that exists
- Using diaspora status as a substitute for actually talking to users on the ground

---

## Contributing

Corrections, additions, and debate all welcome. Open an issue or PR.

Especially welcome: coverage of Tanzania, Uganda, Rwanda, Ethiopia contexts. This started Kenya-focused but East Africa is the scope.

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Related projects

- [`mpesa-python`](https://github.com/gabrielmahia/mpesa-python) — Python SDK for M-Pesa Daraja
- [`openresilience`](https://github.com/gabrielmahia/openresilience) — Water/food stress intelligence for Kenya
- [`catholic-network-tools`](https://github.com/gabrielmahia/catholic-network-tools) — Parish infrastructure (good USSD/SMS reference implementation)
- [`chama-protocol`](https://github.com/gabrielmahia/chama-protocol) — Digital chama (rotating credit) infrastructure
- [`remit-lens`](https://github.com/gabrielmahia/remit-lens) — Diaspora remittance comparison tool

---

*Maintained by Gabriel Mahia — contact@aikungfu.dev*
