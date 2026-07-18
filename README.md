# nairobi-stack

> *The largest open-source MCP coordination infrastructure for the Global South.*  
> *31 servers. Local-first. Data-sovereign. MIT licensed.*

**The engineering guide for building software products in East Africa — and everywhere institutions are under-resourced.**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightblue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A practical, opinionated reference for developers — in Kenya, the diaspora, or anywhere building for East African users. Covers APIs, infrastructure choices, UX patterns, regulatory context, and the cultural nuances that documentation never mentions.

---


## What Gets Built On This

These are not hypothetical. They are the trains for which these rails were built.

---

### Scenario 1: The rural health worker
A community health worker in Kisumu runs `afya-mcp` + `offline-mcp` on a tablet
with no internet. She asks: *"What is the correct malaria treatment for a 4-year-old
weighing 15kg?"* The query runs against a local Llama model. No data leaves the
tablet. The answer arrives in Swahili in under 3 seconds.
**Rails used:** `afya-mcp`, `offline-mcp`, `tafsiri-mcp`

---

### Scenario 2: The smallholder farmer
A maize farmer in Nakuru wants to know whether to sell now or hold for two weeks.
She opens WhatsApp, sends a voice note to a bot powered by `soko-mcp`. The bot
returns current prices across eight East African markets, trend direction, and a
sell/hold recommendation with the reasoning shown.
**Rails used:** `soko-mcp`, `kilimo-mcp`

---

### Scenario 3: The Kenyan diaspora member in Virginia
A Kenyan living in Manassas, Virginia discovers that a caretaker has encroached on
his father's land in Kiambu. He needs to understand his legal options, initiate a
dispute, and manage the process remotely. He uses `ardhi-mcp` + `familia-mcp` +
`fomu-mcp` to understand the legal path, draft the initial letter, and track
required documents — without hiring a Kenyan lawyer for the preliminary steps.
**Rails used:** `ardhi-mcp`, `familia-mcp`, `fomu-mcp`, `diaspora-mcp`

---

### Scenario 4: The first-time SACCO member
A 23-year-old boda boda rider in Nairobi wants to join a SACCO but doesn't know
which one fits his income profile, what the obligations are, or whether the
institution is legitimate. `jumuia-mcp` walks him through SACCO types, finds
SASRA-regulated options in his county, and explains what joining actually commits
him to. In Swahili. On his phone.
**Rails used:** `jumuia-mcp`, `sifa-mcp`, `tafsiri-mcp`

---

### Scenario 5: The county government AI deployment
A county government in Western Kenya wants to deploy an AI assistant for
citizen services — permit status, budget enquiries, ward information. They deploy
the SII Stack on a local server. Citizen queries hit the sovereign tier first.
Only complex reasoning escalates to cloud inference. Citizen data never leaves
the county server.
**Rails used:** `county-mcp`, `fomu-mcp`, `habari-mcp`, SII Stack sovereign tier

---

**Each scenario above can be built today.** The servers are live on PyPI.
The SII Stack is open-source. The architecture is documented.
What's needed is someone who wants to run the train.

→ [SII Stack](https://github.com/gabrielmahia/sii-stack) ·
[Browse all 31 servers](https://glama.ai/mcp/servers?query=author%3Agabrielmahia) ·
[PyPI](https://pypi.org/user/gmahia)


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



## Why This Exists

> *"Build Rails, Not Trains."*

TCP/IP didn't control the internet — it enabled it.
Railroads didn't control freight — they enabled an economy.
M-Pesa didn't control money — it enabled transactions at scale.

The 31 MCP servers in this stack are rails.

They give AI agents structured, authenticated, locally-processed access to:
the M-PESA API, Kenya's 47-county government layer, NDMA drought data,
land title systems, health infrastructure, education records, and civic institutions.

Any developer — anywhere — can `pip install mpesa-mcp` and give an AI agent
the ability to trigger a mobile payment in Kenya in under 120 seconds.

**That's the rail. What you build on it is the train.**

---

### Structural Absences, Not Competitive Gaps

These servers weren't built because no one had thought of payments, drought data, or land records.
They were built because the engineer with the right intersection of skills hadn't built them yet.

The intersection: Kenyan institutional knowledge + diaspora perspective + AI infrastructure fluency.

That intersection doesn't exist in San Francisco or London.
It exists here.

---

### The Stewardship Principle

Every decision in this stack was made with one question:
*"What should I preserve, improve, and hand forward?"*

- MIT license: so others can build on it without asking permission
- Local-first architecture: so communities steward their own data
- Human-in-the-loop: so AI assists, never decides unilaterally
- Offline sovereign tier: so the stack survives when the internet doesn't

This is not a product. It is infrastructure.
Infrastructure is built for the people who come after you.

---

## Built for Africa. Deployable Anywhere.

### The architecture is continent-generic. The data is local.

Every server in this stack separates **infrastructure** (tools, schemas, routing logic)
from **data** (the Kenya-specific records, county budgets, NDMA classifications).

Replace the data layer with Uganda's NSSF records, Nigeria's CAC registry,
Ghana's GhIPSS payment rails, or Tanzania's BRELA business registration —
and the same architecture works without changing a line of application code.

### Current depth: Kenya (31 servers)
Kenya is the starting point because it has the most developed data infrastructure
for this kind of tooling: M-Pesa, a mature Daraja API, NDMA drought data,
a 47-county government layer with structured data, and an active tech ecosystem.

### Expansion logic: depth before breadth
The right expansion sequence is not "build one thin server for every African country."
It is "build deep coverage in one country, then lift and replicate."

The next depth targets, in order:
1. **Tanzania** — 60M people, Swahili national language, fewer legacy constraints, quieter governance
2. **Uganda** — 48M people, mobile money penetration, East African Community integration
3. **Nigeria** — 220M people, largest African economy, fintech ecosystem (OPay, Flutterwave, Paystack)
4. **Ghana** — 33M people, GhIPSS, stable institutions, English-speaking

Each is a separate data layer on the same rail architecture.

### What "Africa-wide" actually means
Swahili covers East Africa and large parts of Central Africa (including DRC, Rwanda, Burundi).
`tafsiri-mcp` and `swahili-civic-nlp` are already cross-border tools.
`sifa-mcp` (portable reputation) and `soko-mcp` (market prices) have no inherent
Kenya boundary — the schema works for any East African market.

---
## 📊 Portfolio Stats — June 2026

| Platform | Status |
|----------|--------|
| PyPI packages | 31 live (v0.1.1 · v0.1.9 for mpesa-mcp) |
| Glama directory | 31 indexed |
| Smithery.ai | Indexed (3+ confirmed) |
| awesome-mcp-servers | mpesa-mcp listed · PR #8363 open |
| HuggingFace datasets | 5 datasets · 246 total downloads |
| Dev.to articles | 15 published · 244+ views |
| DPGA submissions | 2 under review · 1 pending completion |

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

## AGENTS.md — tell AI coding agents how to work with your repo

[AGENTS.md](https://github.com/aaif/agents.md) is a spec by OpenAI, now part of the
Agentic AI Foundation (Linux Foundation). It's been adopted by 60,000+ repos and is
supported by Cursor, GitHub Copilot, Claude Code, Devin, Gemini CLI, and VS Code.

Add it to any repo you want AI coding tools to understand correctly:

```markdown
# AGENTS.md

## What this is
[Brief description]

## Architecture
[Directory structure]

## Critical rules
[Things agents must not change or break]

## Running locally
[Commands]
```

All repos in the gabriel Mahia portfolio now have AGENTS.md files.

## MCP vs A2A — know the difference

Both are 2025-2026 protocol standards under the Linux Foundation:

| | MCP | A2A |
|---|---|---|
| What | Agent ↔ Tools | Agent ↔ Agent |
| Created by | Anthropic | Google |
| Use case | Connect Claude to M-Pesa | Orchestrate multiple agents |
| East Africa relevance | mpesa-mcp, WapiMaji SMS | Multi-agent payment workflows |

mpesa-mcp is MCP only. For multi-agent architectures (payment + notification + audit),
A2A would coordinate the agents while each agent uses MCP to reach its tools.

## MCP Dev Summit — April 2-3 2026, New York

The official MCP community event, now under the Agentic AI Foundation. CFP is open.
If you're building on MCP for African markets, this is the venue to present.

[events.linuxfoundation.org/mcp-dev-summit-north-america](https://events.linuxfoundation.org/mcp-dev-summit-north-america/)

## Community presence and contributions

### Where to find this work

| Platform | Link | What's there |
|----------|------|--------------|
| GitHub | [gabrielmahia](https://github.com/gabrielmahia) | 15 repos, 8+ packages |
| PyPI | [mpesa-mcp](https://pypi.org/project/mpesa-mcp/) | MCP server for M-Pesa + AT |
| MCP Registry | [io.github.gabrielmahia/mpesa-mcp](https://registry.modelcontextprotocol.io) | Official listing |
| Portfolio | [gabrielmahia.github.io](https://gabrielmahia.github.io) | All 13 apps |
| Engineering blog | [aikungfu.dev](https://aikungfu.dev) | Technical writing |

### Open source contributions

| Org | Issue/PR | What |
|-----|----------|------|
| [Gates Foundation / Mojaloop](https://github.com/mojaloop/documentation/issues/553) | #553 | MCP + payment rails integration guide |
| [OCHA / HDX](https://github.com/OCHA-DAP/data-grid-recipes/issues/194) | #194 | Kenya food security data recipe |
| [Andrew Ng / context-hub](https://github.com/andrewyng/context-hub/pull/52) | PR #52 | Africa's Talking + M-Pesa docs |
| [mySociety / theyworkforyou](https://github.com/mysociety/theyworkforyou/issues/1998) | #1998 | Kenya parliamentary data tools |
| [Code for Africa / openAFRICA](https://github.com/CodeForAfrica/openAFRICA/issues/55) | #55 | Kenya civic tools listing |
| [Open Knowledge Foundation](https://github.com/okfn/dataportals.org/issues/407) | #407 | Kenya open data portals |
| [Open Contracting](https://github.com/open-contracting/standard/issues/1745) | #1745 | Kenya procurement transparency |
| [Ushahidi](https://github.com/ushahidi/platform/issues/5048) | #5048 | Kenya crisis mapping tools |
| [Open Data Day](https://github.com/okfn/opendataday/issues/425) | #425 | Kenya civic tools showcase |
| [Africa's Talking SDK](https://github.com/AfricasTalkingLtd/africastalking-python/issues/72) | #72 | mpesa-mcp community project |

<!-- interconnect:v1 -->
## Part of the East Africa coordination stack

- **Install & run:** `pip install reli-cli && reli list` — 33 MCP servers on the [official MCP Registry](https://registry.modelcontextprotocol.io) under `io.github.gabrielmahia`
- **Evaluate any model on Swahili agent tasks:** [kipimo](https://github.com/gabrielmahia/kipimo) · [dataset](https://huggingface.co/datasets/gmahia/kipimo) · [leaderboard](https://huggingface.co/spaces/gmahia/kipimo-leaderboard)
- **Coordinate across servers:** [africa-coord-bus](https://pypi.org/project/africa-coord-bus/) — offline-first event bus with a built-in Kenya routing table
- **Datasets:** [huggingface.co/gmahia](https://huggingface.co/gmahia) · **Docs hub:** [nairobi-stack](https://github.com/gabrielmahia/nairobi-stack)

Model-agnostic by design: closed APIs, open-weight models, and small distilled models are all first-class citizens.
<!-- /interconnect:v1 -->
