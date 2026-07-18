# Engineering Lineages — what we borrow, and the Kenyan cognate of each
**Location:** `nairobi-stack/docs/ENGINEERING_LINEAGES.md`
**Premise:** the strongest engineering cultures encode the same few insights in
different vocabularies — and East Africa already practices most of them under
its own names. We borrow the *discipline*, then name the local cognate, because
infrastructure adopted in a community's own conceptual vocabulary outlives
infrastructure imported in someone else's. Japan's postwar quality revolution is
the founding precedent: Deming's methods, imported and metabolized better by the
adopter than the originator. That is what leapfrog actually looks like.

## German lineage → discipline: standards and generational maintenance
- **DIN-style standardization as public infrastructure.** A standard is a gift to
  strangers. Our routing-table schema, event wire format, and scorecard protocol
  are DIN-style artifacts: boring, versioned, and more valuable than any single
  implementation. *(Applied: coordination_event wire shape held stable across the
  v0.3.0 G10 fix — legacy queues parse unchanged.)*
- **Mittelstand posture.** Small, deep, unglamorous, generational. Repos are run
  like hidden champions: narrow scope, 10-year maintenance, no growth theater.
  **Kenyan cognate: jua kali** — the informal engineering sector already builds
  this way; the stack's job is to give jua kali-grade builders formal-grade rails.
- **Duale Ausbildung (apprenticeship).** Competence is transmitted by doing under
  supervision, certified by craft not credential. G6's curriculum kit is an
  apprenticeship design, not a lecture design.

## Japanese lineage → discipline: mistake-proofing and dignified maintenance
- **Poka-yoke** (make the error impossible, not discouraged): AST-parse gates,
  TOML-parse gates, schema-dispatching deserializers, typed events. *(G10 was a
  poka-yoke lesson: the type system was mistake-proofing the wrong invariant —
  Kenya-ness instead of well-formedness.)*
- **Jidoka + andon** (halt on anomaly; anyone may pull the cord): agents must
  stop and surface rather than plow on; error reporting is a first-class user
  action, not a log line. The offline-first queue is jidoka for connectivity.
- **Kaizen** under constraint: commit-sized improvement, forever. **Kenyan
  cognate: jua kali iteration** — relentless refinement with whatever is at hand.
- **Genchi genbutsu** (go and see): G3's pilot is at the site with real clerks
  and real registries, instrumented for human adaptation load — never simulated.
- **Shuhari** (learn → detach → transcend): the maturity model for G6 cohorts;
  identical in spirit to learn/unlearn/relearn (see FUTURES_LENS.md §4).

## Amazonian / indigenous lineage → discipline: regenerative, distributed, reciprocal
- **Terra preta** (engineered soil that grows richer for a millennium): the G9
  ideal named. Build soil, not crops — datasets, standards, and evals that
  compound with use and outlive their makers. The test of any artifact: does it
  regenerate value without its author?
- **Forest-garden polyculture** (resilience through diversity, not monoculture
  yield): model-agnosticism, multi-provider endpoints, 33 narrow servers instead
  of one platform. Monocultures fail totally; polycultures fail partially.
  **Kenyan cognate: the shamba.**
- **Distributed observation** (communities as sensor networks reading river,
  forest, season): wapimaji's pattern generalized — citizen ground-truthing is
  the regional answer to G4 registry integrity; many eyes, local calibration.
- **Reciprocity economics** (minga work-parties): **Kenyan cognate: harambee.**
  G9's endowment should be architected as harambee — pooled contribution toward
  a named public good — not as a grant pipeline. And adoption follows the same
  social physics: **trust travels in groups** (chama-scale, not individual-scale),
  so pilots recruit chamas and cooperatives, never lone users.
- **Governed knowledge** (not all knowledge is open; some is held in trust):
  G7 now anchors on the CARE principles (Collective benefit, Authority to
  control, Responsibility, Ethics) and Local Contexts TK/BC labels — existing,
  reusable frameworks. Openness is our default for code; *consent* is our
  default for community knowledge. The two defaults are not in tension; they
  are the same respect applied to different owners.

## The socio-psychographic bottom line
Adoption in this region is relational before it is functional: tools spread
chama-to-chama, are trusted when a known person vouches, and are kept when they
close loops in under two minutes on a cheap phone. Every design rule above
serves that reality. The lineages converge on one sentence: **build boring,
mistake-proofed, regenerative rails; transmit them by apprenticeship; let
communities govern what is theirs; and let the work stay quieter than the
problem it solves.**
