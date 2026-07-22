# Gap Register — permanent, versioned

Every proposed project must originate here. Format: gap → why it exists → who
benefits → what exists → reusable form → status. Ranked by leverage (see
EXECUTION_BLUEPRINT.md §7 for the full multiplier analysis).

| # | Gap | Why it exists | Who benefits | What exists today | Reusable form | Status |
|---|---|---|---|---|---|---|
| G1 | Swahili agent-task evaluation suite | Global evals are English-first; no regional ground truth for agent quality | Every builder targeting 100M+ Swahili speakers | Generic LLM benchmarks only | Benchmark + dataset | **Seeded — kipimo v0.1** (PyPI: kipimo · HF: gmahia/kipimo · 46 tasks; native-speaker review = issue #1; live leaderboard Space now the public comparison surface; **v0.2 scope: open-weight scorecard** — K3/GLM/DeepSeek/Nemotron + small distilled deployment tier, per docs/OPEN_WEIGHTS_STRATEGY.md) |
| G2 | Live-data partnership framework (data-sovereignty terms) | Registries are paper/partial; no template for opening them without surrendering them | Counties, ministries, cooperatives | DEMO datasets on all 35 servers; reference corpus now exists: AU Continental AI Strategy + planned African Charter on Trustworthy AI, OECD Africa governance case studies, Karnak/Atlas sovereign-model precedents | Standard + legal template | Open — critical path |
| G3 | Measured pilot deployment with outcome study | Rails unproven in the field; the leapfrog thesis needs one honest data point | The entire thesis (falsification clock ~2027) | reli on-ramp, deploy-ready demo | Reference implementation + study | Open — **pilot must instrument human adaptation load** (time-to-competence, attention demand, non-specialist error recovery), not just task success; see docs/FUTURES_LENS.md |
| G4 | Registry-integrity monitoring (ground-truth defense) | Poisoned registries are the coming attack surface; open-weight diffusion (Kimi K3 et al., July 2026) creates a governance vacuum where third-party eval/certification becomes the operative trust layer | Anyone consuming institutional data | Nothing regional | MCP + monitoring standard | Open |
| G5 | Machine-readable Kenyan law corpus (bilingual, structured) | Laws exist as PDFs; agents can't ground on them | Citizens, courts, legal-aid builders | kenya-legal-rag (partial), HF datasets | Dataset + schema standard | Partial |
| G6 | University curriculum kit on the stack | Courses teach toys; real systems teach maintainers | Students, maintainer pipeline | Docs per repo | Template + course materials | Open |
| G7 | Consent / indigenous-knowledge governance framework | Extraction without governance repeats the old pattern | Communities holding the knowledge | CARE principles + Local Contexts TK/BC labels exist as reusable frameworks (adopt, don't invent — see docs/ENGINEERING_LINEAGES.md) | Standard | Open — governance-gated |
| G8 | Second-country routing table (bus standard port) | Kenya table proves the pattern; standard needs 2 implementations | Regional builders (TZ, UG, RW) | africa-coord-bus (KE) | Standard + implementation | **Shipped — africa-coord-bus 0.2.0** (Tanzania table + KE–TZ cross-border cascades + PORTING_GUIDE.md) |
| G9 | Maintenance endowment + maintainer pipeline | Open infra dies of unpaid maintenance, not bad code | Everything above | None | Governance + funding model | Open — survival-class; architect as harambee (pooled contribution to a named public good) + terra-preta test: does the artifact regenerate value without its author? |

| G10 | Type-level country lock-in in the event bus | `CoordinationEvent.location` is typed `KenyaLocation` (county/sub_county). The bus encodes Kenya in the type system, not merely as a default — invisible until a real second-country port | Every non-Kenya implementer | **Shipped — africa-coord-bus 0.3.0** (SubnationalLocation + unchanged KenyaLocation, shared accessors both directions, wire-compatible deserializer, `SubnationalLocation.tanzania()`; 17/17 tests) | Backwards-compatible `SubnationalLocation` with `KenyaLocation` retained as alias | **Open — surfaced by the G8 port** |

| G11 | World-signal → coordination-event ingest (region-scoped) | The stack routed events but nothing turned raw public world signals into them; global dashboards (worldmonitor) exist but are AGPL apps scoring Tier-1 countries — East Africa isn't Tier-1 | Any regional early-warning/coordination consumer | **Shipped — coord-ingest 0.1.0** (MIT; USGS/ReliefWeb/GDACS adapters + East-Africa filter; feeds africa-coord-bus) | connector/adapter library | **Shipped** |

**Closed gaps (for the record):** cross-domain event bus (africa-coord-bus) ·
domain server fleet (35) · on-ramp (reli-cli) · official MCP Registry presence
(33 servers) · console-script launch standard · portfolio governance baseline.

*Additions require the Baobab questionnaire answered in full. Removals require a
written reason. This file is append-mostly by design.*
