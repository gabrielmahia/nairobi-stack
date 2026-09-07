# Flourishing Intelligence Architecture — R1–R12 compliance matrix

**Response to** `Flourishing_Intelligence_Architecture_System_Engineering_Specification` v1.0
(7 Sep 2026), §17.1: *"A model receiving this specification should not merely
summarize it. It should instantiate the architecture against the target
environment."*

**Target environment:** East Africa, Kenya-first. The spec's canonical persona —
Daniel, a farm worker in Murang'a on an uncertain connection — is the same user
this stack was built for. That is not a coincidence to celebrate; it is the
reason the matrix below is unusually full on some rows and empty on one.

**Evidence labels** per §17.1(9): CONFIRMED (built, tested, published) ·
PROBABLE (built, not validated in field) · SPECULATIVE (designed, not built) ·
UNKNOWN.

---

## 1. Compliance matrix

| ID | Requirement | Status | What satisfies it | Gap |
|---|---|---|---|---|
| **R1** | Contextual differentiation | **PROBABLE** | ~34 domain MCP servers expressing different capability off one substrate; Kenya + Tanzania routing tables; `SubnationalLocation` | Differentiation is by *domain*, not by *user*. No per-user phenotype |
| **R2** | Low-friction interaction | **ABSENT** | Nothing. Every surface assumes a keyboard and literacy | **The single largest hole.** No voice, IVR, USSD, or SMS-in. `mpesa-mcp` sends SMS but cannot receive |
| **R3** | Sparse activation | **PROBABLE** | Event-driven bus; routing tables fire only matched rules; `coord-ingest` filters by region before emitting; alert engine has an explicit ARCHIVE level | No cost-aware regulator deciding *no inference needed* |
| **R4** | Locality | **CONFIRMED** | Swahili throughout; county-level routing; NEMA/EPRA/SASRA/KRA institutional grounding; Swahili tool responses carry `chanzo` | Kikuyu/Luo thin (`tafsiri-mcp` only) |
| **R5** | Human telos | **CONFIRMED** | Every MCP tool advises; none acts unilaterally. `mpesa-mcp` is the only actuator and requires explicit authorization | — |
| **R6** | Capability expansion | **PROBABLE** | `kipimo` measures *stack-routing competence*, and its Pareto selector asks the deployment question — cheapest self-hostable model clearing the bar | Measures model capability, not **human** capability. No time-returned or optionality metric |
| **R7** | Graceful degradation | **CONFIRMED** | Offline-first JSONL queue; **CRDT G-Set merge** (idempotent/commutative/associative — devices reconcile in any order); every adapter degrades to empty rather than halting the pipeline; `offline-mcp` for local inference | — |
| **R8** | Continual adaptation | **PROBABLE** | `nature-ai-evolution-lab`: LoRA epigenome over immutable genome, immune memory of fatal mutations, promotion gate rejecting general-capability loss | Generation 0 unmeasured. No claim is currently valid |
| **R9** | Least privilege | **PROBABLE** | Per-server tool scoping; `privacy_level` on every event; CAP `scope` derives from it | No typed cross-domain summaries; specialists can receive full slices |
| **R10** | Escalation | **PROBABLE** | Severity ladder INFO→CRITICAL; cross-domain cascade refs; IPC hint **never** assigns Phase 5 heuristically; rights gate blocks UNKNOWN-rights actions | No uncertainty-triggered escalation to a stronger model |
| **R11** | Auditable autonomy | **CONFIRMED** | `reality` (REAL/DEMO) + `confidence` (CONFIRMED/PROBABLE/SPECULATIVE/UNKNOWN) are **declared fields**, not inferred. A DEMO event cannot export as a live CAP alert. Append-only provenance | — |
| **R12** | Global affordability | **CONFIRMED** | MIT rails, no licence cost; `must_remain_self_hostable` is a promotion rule; compute ladder climbs cheapest-first; kipimo scores capability **per unit of deployment cost** | Device floor is still a smartphone — see R2 |

**Score: 4 CONFIRMED · 7 PROBABLE · 1 ABSENT.**

## 2. Layer mapping (spec §4.1 → this stack)

| Spec layer | Implementation | Status |
|---|---|---|
| L0 Human telos & policy | Doctrine + per-repo governance | PROBABLE |
| L1 Intelligence genome | Model-agnostic by design; `nature-ai-evolution-lab` grows a sovereign one | PROBABLE |
| L2 Sensory / connector fabric | **`coord-ingest`** — Open-Meteo, USGS, GDACS, HDX/OCHA, Kobo/ODK, Flood Hub | CONFIRMED |
| L3 Personal / local world model | Routing tables, county data, `SubnationalLocation` | PROBABLE — *local*, not *personal* |
| L4 Regulatory / attention | **`africa-coord-bus`** — routing, cascades, severity, alert levels | CONFIRMED |
| L5 Differentiated specialists | ~34 MCP servers | CONFIRMED |
| L6 Planning & action | `mpesa-mcp` (only actuator) | PARTIAL |
| L7 Homeostatic capability monitor | — | **ABSENT** |
| L8 Learning & consolidation | `nature-ai-evolution-lab` immune memory + promotion gate | PROBABLE |
| L9 Audit / safety / governance | Declared provenance, rights gate, hash-pinned constitution | CONFIRMED |

The spec's L2/L4/L5/L9 are already built and published. **L7 does not exist**, and
L3 is local rather than personal — the stack models a *county*, not a *household*.

## 3. The finding that matters

**R2 is the only ABSENT requirement, and it invalidates much of the rest for the
persona the spec names.**

Daniel speaks. Every surface in this portfolio reads and writes text on a screen.
An architecture that satisfies eleven of twelve requirements and fails the
interaction requirement delivers zero capability to the user it was designed for.
R1's differentiation, R4's locality, R7's offline resilience and R12's
affordability are all real — and all unreachable through a keyboard he may not
use.

This was independently identified as the portfolio's highest-value gap before
this specification arrived. Two analyses converging on the same missing rail from
different directions is the strongest signal available.

The spec's own Appendix F supplies the components: **UBC-NLP Simba** (open African
multilingual speech), and two GSMA case studies of voice-first delivery on basic
phones — **Farmerline Darli** (agronomic advisory) and **Viamo** (IVR generative
AI, Zambia). Prior art exists; the rail does not.

## 4. Implementation horizons (§17.1(2))

**Buildable now, no model training:**
- `sauti-mcp` — speech-in/speech-out Swahili over Simba/MMS/Common Voice, offline-capable. **Closes R2.** Extends every existing server rather than adding a domain.
- IVR/USSD ingress into the bus — Africa's Talking already provides the channel and `mpesa-mcp` already wraps that SDK.
- L7 capability monitor — the spec's `Outcome{capability_delta}` schema is implementable against existing event flow today.
- Typed cross-domain summaries to close R9 properly.

**Requires model-training research:** developmental curriculum, capability
homeostasis as a post-training objective, one genome differentiating globally.
The spec labels these SPECULATIVE and that labelling is correct.

**Research hypotheses, not commitments:** continual learning without harmful
forgetting at open-world scale; adaptive forgetting for personal AI.

## 5. Where I disagree with the spec

**"Tuesday should be better than last Tuesday"** is the right test and the spec
cannot currently measure it. §11's Human Agency Dividend — discretionary time +
security + capability + optionality + resilience — has no measurement protocol,
no instrument, and no baseline. It is a definition presented where a method is
needed. Until a field instrument exists, HAD is an aspiration and should carry
SPECULATIVE, not sit in the evaluation section as though it were operational.

**The Daniel Benchmark risks becoming the thing it warns against.** §11 proposes
eight personas across four continents. Building an eight-site benchmark before
one site works is breadth before depth. One instrumented deployment in Murang'a
that measurably returns time beats eight simulated personas, and the spec's own
principle — *"build for low-resource environments first; constraints expose
architectural waste"* — argues for the same narrowing.

**Recorded per §17.1(10):** these are objections to be settled by evidence, not
positions to defend. If a HAD instrument is built and validated, the first
objection dies.

## 6. Acceptance gate self-assessment (Appendix E)

| Gate question | Answer |
|---|---|
| User with no AI expertise obtains measurable benefit? | **No** — R2 blocks it |
| Operates on low bandwidth / cheap hardware? | **Yes** — offline queue, CRDT merge, self-hostable models |
| Same core architecture differentiates across environments? | **Partially** — Kenya→Tanzania port demonstrated |
| Returns time or increases options? | **Unmeasured** |
| User can inspect/override goals and permissions? | **Partially** — `privacy_level` exists; no user-facing control |
| Can remain quiet when intervention is unnecessary? | **Yes** — ARCHIVE level, region filters, `no material change` |
| Detects missing evidence and uncertainty? | **Yes** — declared confidence; untested ≠ zero; UNKNOWN rights block action |
| Fails gracefully and escalates? | **Yes** on degradation; **partially** on escalation |
| Benefits measured net of costs? | **Partially** — compute cost yes; attention and dependency no |
| Each nature-inspired mechanism beat a simpler baseline? | **No ablations run.** The lineage doctrine names mechanisms and Kenyan cognates but has not ablation-tested one |

That last row is the spec's sharpest contribution to this portfolio: *every nature
analogy must survive an ablation test.* Ostrom, Beer, mottainai and the rest are
currently reasoning aids, not validated engineering claims — and this document
now says so.
