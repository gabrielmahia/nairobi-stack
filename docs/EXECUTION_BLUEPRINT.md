# Execution Blueprint — The Open African AI Stack

**Version 1.0 · July 2026 · Status: living document**

This blueprint translates a civilizational analysis (Project Prometheus, Working Edition I)
into an engineering program. It is written for anyone who wants to build on or extend the
stack — no permission required. Claims about current state are live-verified as of July 2026;
roadmap items beyond five years are labeled Speculative, because honesty compounds and hype
does not.

**Success criterion (25-year):** thousands of developers, governments, schools, clinics,
cooperatives, and churches building on these foundations without needing permission from —
or knowledge of — the original builders.

---

## 1. Ecosystem map: what exists, what's missing, what's duplicated

**Exists today (verified):**
- 35 pip-installable coordination packages spanning finance (M-PESA, KRA, credit, insurance),
  health, agriculture/drought, land, counties, labour rights, diaspora workflows, and Swahili
  language infrastructure — MIT-licensed, CI-tested, smoke-tested.
- 33 servers listed on the official Model Context Protocol registry under an open namespace,
  discoverable by any MCP client.
- A cross-domain event bus (`africa-coord-bus`) with a Kenya routing table and offline-first
  queue: drought signals reach insurance, crop, health, county, and market tools without a
  human relay.
- A one-command on-ramp (`pip install reli-cli && reli up`) that installs, wires, and verifies
  the stack in an MCP client in under two minutes.
- 16 open datasets on Hugging Face (civic, legal, agricultural, historical Swahili corpora).

**Missing (the gaps this blueprint targets):**
- **Live institutional data.** Every server ships DEMO datasets, clearly labeled. The rails
  exist; the trains carry sample freight. Data partnerships under local data sovereignty are
  the critical path.
- **Adoption evidence.** No measured deployment yet (a county, a SACCO federation, a CHW
  program). Until one exists, the leapfrog thesis is a well-built hypothesis.
- **Evaluation infrastructure.** No Swahili-first benchmark suite for agent tasks; no
  registry-integrity monitoring.
- **Layer 1 dependencies** (energy, connectivity, compute) are outside this stack's scope but
  bound everything above them — see §7 red-team.

**Duplicated across the wider ecosystem (avoid rebuilding):** foundation models, vector
databases, generic agent frameworks, cloud orchestration. The stack's unique contribution is
**domain ground truth + cross-domain routing for East African institutional reality** —
nothing else in the global ecosystem occupies that cell.

---

## 2. The African AI Stack — four layers

| Layer | Contents | Current state | This stack's role |
|---|---|---|---|
| **L1 Physical** | energy, connectivity, compute, edge | External dependency; Rift Valley geothermal + Sahel solar are strategic endowments | Consume; design offline-first so L1 gaps degrade gracefully |
| **L2 Digital public infrastructure** | identity, payments, registries, consent | Payments strong (M-PESA); registries paper/partial | Expose via protocol servers; never own — wrap and open |
| **L3 AI infrastructure** | models, embeddings, evals, safety | Global models adequate; Swahili evals missing | Model-agnostic by design; build the eval layer (multiplier #4) |
| **L4 Coordination ecosystem** | MCP servers, event bus, on-ramp, registries | **Built and live** (35 pkgs, 33 registry entries, bus, reli) | The core asset; extend by domain, harden by adoption |

Design consequence: every component must survive intermittent L1 (offline queues, low
bandwidth) and absent L2 (DEMO-labeled fallbacks) — which is exactly how the current stack
is built.

---

## 3. MCP server standard (the per-server spec)

Every current and future server must be able to answer the Part IX questionnaire. Convention:
a `SPEC.md` per repository covering — purpose (the coordination gap, stated problem-first);
users (who benefits, technical and non-technical); datasets (DEMO vs REAL, provenance,
licensing); APIs wrapped; governance (who can change what); interoperability (bus event types
emitted/consumed); security posture; license (MIT for infrastructure); sustainability
(maintenance model); success metrics (usage is vanity — outcome deltas are the metric).

Current servers satisfy this partially through README + IP_POLICY + server.json;
`SPEC.md` roll-out is a queued wave, not retrofit theater.

---

## 4. Knowledge infrastructure priorities

Public, machine-readable, in order of leverage: (1) laws and regulations (Swahili + English,
structured); (2) clinical and CHW guidelines; (3) agricultural calendars and practices per
agro-ecological zone; (4) government procedures and forms (partially served by fomu-mcp);
(5) curricula; (6) indigenous knowledge — **only** under community-governed consent frameworks;
extraction without governance is the old pattern wearing new clothes.

Formats: plain JSON/JSONL + open schemas over bespoke ontologies. Boring survives.

---

## 5. Developer ecosystem — 20-year strategy, compressed

Sequenced, each stage funding the next: **Documentation-first** (every server a teaching
artifact) → **University integration** (the stack as coursework substrate — real systems beat
toy assignments) → **Certification by portfolio** (verified contributions, not seat time —
consistent with the credential-collapse forecast) → **Maintainer pipeline** (paid maintenance
before paid features; grants and institutional endowments over VC) → **Community governance**
(neutral foundation stewardship once >50 external contributors; measured by the bus factor,
not stars).

---

## 6. Roadmaps with measurable milestones

**1 year (2026–27) — Prove.** One measured deployment (county drought desk, SACCO federation,
or CHW pilot) with outcome deltas; Swahili agent-task benchmark v1; SPEC.md wave; live-data
partnership #1 under data-sovereignty terms. *Milestone: the falsification clock from
Prometheus Part X is answered.*

**3 years (2029) — Standardize.** Bus event schema published as an open standard with ≥2
independent implementations; 10+ external contributors; first government department consuming
registry data. [Probable]

**5 years (2031) — Institutionalize.** Foundation governance; national-scale deployment in ≥1
service line; the stack taught in ≥5 universities; eval suite is the regional reference.
[Probable]

**10 years (2036) — Compound.** Formal-grade coordination running on open rails in mostly
informal economies; maintainers majority African-resident; net documentation/knowledge
exporter. [Speculative]

**25 years (2051) — Disappear.** The infrastructure is boring, assumed, and maintained by
people who never met its originators. Success is anonymity. [Speculative]

---

## 7. Multiplier analysis — top 20 by civilizational leverage

Ranked by (impact × compounding) ÷ (difficulty × adoption barrier). ✅ = exists, live-verified.

| # | Project | Difficulty | Impact | Depends on | Status |
|---|---|---|---|---|---|
| 1 | Cross-domain event bus + routing standard | M | Very high | — | ✅ built; standardize |
| 2 | Domain server fleet (36 domains) | M | Very high | 1 | ✅ built; extend |
| 3 | On-ramp / installer (reli) | L | High | 2 | ✅ built |
| 4 | Swahili agent-eval benchmark suite | M | Very high | — | Missing — top gap |
| 5 | Live-data partnership framework (sovereignty terms) | H | Very high | 2 | Missing — critical path |
| 6 | Measured pilot deployment + outcome study | H | Very high | 3,5 | Missing — falsification test |
| 7 | Registry-integrity monitoring (ground-truth defense) | M | High | 2 | Missing |
| 8 | Machine-readable law corpus (KE, structured, bilingual) | H | High | — | Partial (datasets) |
| 9 | CHW protocol server w/ clinical governance | H | Very high | 5,6 | DEMO only |
| 10 | SACCO/chama governance tooling | M | High | 2 | Partial (jumuia) |
| 11 | Offline-first sync standard for L1-degraded zones | M | High | 1 | Partial (bus queue) |
| 12 | University curriculum kit built on the stack | L | High | 2,3 | Missing |
| 13 | Consent/data-sovereignty reference implementation | H | High | — | Missing |
| 14 | County dashboard reference app (proof-of-use) | L | Medium | 1–3 | Repo ready; undeployed |
| 15 | Agricultural calendar open dataset per AEZ | M | High | — | Partial |
| 16 | Diaspora capital → infrastructure endowment vehicle | H | High | governance | Missing |
| 17 | Faith-institution transparency tooling | M | Medium-high | 2 | DEMO (church-mcp) |
| 18 | Indigenous-knowledge governance framework | H | Medium-high | 13 | Missing |
| 19 | Bus-event standard int'l port (2nd country routing table) | M | High | 1 | Missing |
| 20 | Maintenance endowment + maintainer pipeline | H | Very high (survival) | all | Missing |

Reading of the table: **the built layer (#1–3) was the right first move by dependency order;
the entire frontier now runs through #4–6** — evaluation, data partnerships, and one honest
pilot. Everything else compounds only after those.

---

## 8. Design-principles gate

Every future component must pass all eight, or state why not in its SPEC.md: open where
possible · interoperable by default · modular over monolithic · local-first, globally
compatible · African languages first-class · privacy and security by design · sustainable
beyond any single government, company, or donor · compounding through community contribution.

## 9. Red-team (standing)

The strongest objection remains: **cognition was never the binding constraint — energy,
logistics, and political economy are.** This blueprint's answer is sequencing, not denial:
the stack is deliberately cheap to build and cheap to abandon; the expensive bets (#5, #6,
#9) are gated behind the 1-year falsification milestone. If the pilot shows no outcome delta,
the correct move is to publish that result openly and tilt effort toward L1 — and this
document commits to that in writing.

---

*MIT-licensed like the stack it describes. Feedback via GitHub Issues. This document will be
wrong in places; versioned corrections are the point.*
