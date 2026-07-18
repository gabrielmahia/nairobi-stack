# Open-Weight Inflection: Strategic Doctrine Amendment
**Candidate location:** `nairobi-stack/docs/OPEN_WEIGHTS_STRATEGY.md`
**Status:** DRAFT for review — July 17, 2026
**Relationship to doctrine:** Extends BAOBAB_DNA.md; amends Gap Register; does not replace either.

---

## 1. What changed (facts, with confidence labels)

- **Confirmed:** Moonshot AI released Kimi K3 on July 16–17, 2026 — a 2.8T-parameter sparse-MoE open-weight model with 1M context. Weights become downloadable ~July 27. Priced ~$12/M output tokens (~40% below Opus 4.8). Ranked #1 on Arena's frontend-coding benchmark; broader claims of near-parity with top US closed models are **self-reported by Moonshot** and should be treated as Probable-at-best until independent evals land.
- **Confirmed:** The open-weight tier is now multipolar and dense: GLM 5.2 (China), DeepSeek V4 Pro (China), MiniMax M3 (China), Nemotron 3 Ultra (US/NVIDIA, released with data, recipes, and eval tooling). Independent trackers describe the open-vs-closed gap as "real but narrow, and not widening."
- **Confirmed (Tier B):** DeepSeek already holds 11–14% assistant market share in Ethiopia, Uganda, Zimbabwe, and Niger per Microsoft analysis. Chinese open weights are not a future scenario in Africa; they are the present install base.
- **Probable:** Cassava/NVIDIA "AI factory" build-out (15k GPUs across South Africa, Nigeria, **Kenya**, Egypt, Morocco; Johannesburg live Q3 2026, full network Q4 2026), with stated focus on Swahili/Zulu/Afrikaans tuning. Announced and funded; execution risk remains.
- **Confirmed:** Sovereign-model precedents exist on the continent: Egypt's Karnak (open-weight national platform), Nigeria's Atlas (multilingual). The AU Continental AI Strategy calls for an African Charter on Trustworthy AI.
- **Context from July 14:** the proposed US Frontier AI Standards Body claims jurisdiction over frontier models "no matter their country of origin or whether open or closed" — but its enforcement lever is **US market access**. A downloadable weight file is outside that lever the moment it leaves the US market.

## 2. First-principles decomposition

Strip "AI capability for East Africa" to its irreducible layers:

| Layer | Status July 2026 | Direction |
|---|---|---|
| Intelligence (weights) | Commoditizing; frontier-adjacent quality now downloadable | Price → marginal cost of inference |
| Compute | The real scarcity; first in-region GPU capacity arriving (Cassava, Q3–Q4) | Scarce → merely expensive |
| Data & language | Swahili absent from training priorities and eval suites alike | Unmeasured → whoever measures it, defines it |
| Coordination & tools | MCP layer, routing tables, event bus, payments rails | **Where displaced value migrates** |
| Governance & trust | US body governs US market; open weights create a governance vacuum elsewhere | Vacuum → filled by certification/eval infrastructure |

**The core theorem:** when a layer commoditizes, value migrates to adjacent non-commoditized layers (Christensen's conservation of attractive profits). Model weights are commoditizing. Compute is being capitalized by others (Cassava, NVIDIA, hyperscalers). Data governance is a state function. The layers open to an independent open-source builder are exactly two: **coordination/tools** and **evaluation/trust**. These are the two layers this portfolio already occupies. The market just validated the railroad thesis.

## 3. Systems dynamics

**Reinforcing loop (work with it):** cheap open inference → more African agent deployments → more demand for local rails (M-Pesa, USSD, routing, Swahili grounding) → MCP layer becomes default interface → usage reveals failure modes → evals improve (kipimo) → evals inform which models get adopted → eval suite becomes de facto certification in the governance vacuum → more deployments route through the rails. Every turn of this loop compounds; none of it requires owning a model.

**Balancing risk (guard against it):** dependency swap. Replacing US API dependency with Chinese weight dependency is not sovereignty — it is a change of landlord. True sovereignty is **the ability to switch**: neutral tool layer + independent evals + local compute + local data governance. Three of those four are Gap Register items.

**Power dynamics:** US export controls failed to prevent K3; expect Washington's next moves to target open-weight *diffusion* (distillation accusations against Moonshot are the opening salvo) — meaning access to any single weight source, US or Chinese, should be treated as revocable. Model-agnosticism is therefore a **resilience requirement**, not a convenience. Beijing will showcase open weights at WAIC Shanghai as soft-power infrastructure for the Global South — the Belt-and-Road playbook applied to intelligence. East Africa's historical answer to bloc competition was non-alignment. MIT-licensed, bloc-neutral rails are the software expression of that same strategy.

**Second-order effect most analysts miss:** a 2.8T model will never run on African edge infrastructure — even Cassava's 15k GPUs serve enterprises, not villages. The actual deployment path for the continent is **distilled small models** derived from open frontier weights. Nobody measures small-model Swahili task performance. That is the highest-leverage unmeasured quantity in the region.

## 4. Doctrine amendments (Baobab-filtered)

Each item passed through Baobab rule 3 (extend, don't duplicate) and rule 8 (railroad test):

**A1 — kipimo v0.2: open-weight scorecard (extends G1, seeds G4).**
Add open-weight targets: Kimi K3 (post-Jul 27), GLM 5.2, DeepSeek V4 Pro, Nemotron 3 Ultra, plus 2–3 small distilled models (the actual African deployment tier). Publish a recurring "Swahili agent-task scorecard." This makes kipimo the reference instrument in the governance vacuum — third-party evaluation infrastructure of exactly the kind the July 14 standards proposal says it wants to exist.
*Railroad verdict: extends. Highest priority.*

**A2 — Model-endpoint neutrality pattern (extends africa-coord-bus + reli; do NOT build new).**
Mature solutions exist (LiteLLM, OpenRouter). Per Baobab rule 3, do not write a router. Instead: document and test a recommended pattern so any agent on the coord-bus can swap between cloud APIs and future in-region endpoints (Cassava-hosted open weights) via config, not code. One docs page + one smoke test + one `reli demo` path.
*Railroad verdict: extends via upstream reuse.*

**A3 — G8 shipped; G10 is the real port blocker.**
Ground truth correction: africa-coord-bus 0.2.0 already ships the Tanzania routing table,
KE–TZ cross-border cascades, and PORTING_GUIDE.md — G8 is closed. The operative gap is G10:
`CoordinationEvent.location` is typed `KenyaLocation`, encoding Kenya in the type system.
Third-country ports (UG, RW) and the Cassava inference-locality dimension both land on this
type. Fix G10 (backwards-compatible location abstraction) before any third table.

**A4 — G2 (data sovereignty) now has a corpus.**
AU Continental AI Strategy, OECD Africa governance case studies, Karnak/Atlas precedents, Brookings "managed interdependence," CSIS sovereign-cloud analysis. G2 shifts from blank page to synthesis task — and connects to G5 (machine-readable law corpus).

**A5 — App-layer cost resilience.**
End-user Streamlit apps currently ride Gemini's free tier — a single-vendor exposure. The A2 pattern, applied at app level, converts vendor generosity from a dependency into one option among several. No immediate work; note as design constraint for next app touch.

**Explicitly rejected:** training or fine-tuning any model (duplicates Cassava/Karnak/Atlas efforts; violates Baobab 3); building a new inference router (LiteLLM exists); a "model marketplace" (train, not railroad).

## 5. Execution plan — commit-sized, FULL AUTO ready

Blocked on one manual step: **rotate the expired GitHub fine-grained token** (expired ~June 30). Once live:

| # | Commit | Files | Acceptance criteria | Validation |
|---|---|---|---|---|
| 1 | Adopt this doctrine doc | `nairobi-stack/docs/OPEN_WEIGHTS_STRATEGY.md` | Doc merged; Gap Register cross-links added | Link check |
| 2 | Gap Register update | `docs/GAP_REGISTER.md` | G1 annotated (v0.2 scope), G4 seeded via A1, G8 note, new refs for G2 | Diff review |
| 3 | kipimo: target registry | `kipimo/targets.py` (or equiv), config schema | Open-weight targets declared behind API-key/endpoint config; no scoring change | `ruff` + `pytest` green |
| 4 | kipimo: scorecard runner | runner + `docs/SCORECARD.md` template | One command produces per-model Swahili task scores incl. ≥1 small model | Dry-run on 5-task subset |
| 5 | coord-bus: endpoint-neutrality docs + smoke test | `docs/MODEL_ENDPOINTS.md`, one test | LiteLLM-pattern documented; smoke test proves endpoint swap via env var only | `pytest` green |
| 6 | reli: demo path | `reli demo swahili-scorecard` | Non-technical user gets a readable result in <120s (DEMO-labeled) | Timed run |
| 7 | (post-Jul 27) First public scorecard run | scorecard output, DEMO/REAL labeled | K3 + 3 peers + 1 small model scored on 46 tasks; results reproducible | Independent re-run matches |

Sequencing note: commits 1–6 can be executed autonomously before July 27; commit 7 waits for K3 weights/API availability. Nothing here requires attended time beyond token rotation and review.

## 6. Red team

The thesis fails if: (a) frontier labs vertically integrate the tool layer fast enough that independent rails get bypassed — mitigation: the rails here are *African-context-specific* (M-Pesa, USSD, Swahili grounding), the least attractive integration target for US/Chinese labs and the hardest to replicate remotely; (b) open-weight Swahili quality stays so poor that African deployments remain on closed APIs — but that outcome is precisely what the scorecard would document, making the eval valuable in both branches; (c) Cassava slips — plausible, but A1/A2 pay off regardless since they are compute-location-agnostic. The plan is robust across all three branches, which is the property that matters given the STOP-condition discipline: no element depends on a single unverified premise.

## 7. Content pipeline note (do not over-publish)

One article already queued this week (standards-body/benchmarks). This development supports a *second* problem-first piece — working angle: "Africa's AI governance will be written in weight files, not in Washington" — but hold it for the August slot behind the agricultural-data piece, or fold its strongest paragraph into the standards article. Two structural-absence articles in one week dilutes both.
