# System Engineering — portfolio state and rules of engagement

**Audience:** any engineer or AI system picking this work up cold.
**Verified:** 2026-09-05 against live GitHub and PyPI, not from memory.
**Full platform scope:** [`PLATFORM_INVENTORY.md`](PLATFORM_INVENTORY.md) — every
surface this work lives on (GitHub incl. 8 private repos, PyPI, HuggingFace,
Kaggle, Glama, MCP Registry, Dev.to, Streamlit, Apps Script/blognet, DPGA,
compute), and what breaks across platform boundaries.

**Companion:** `nature-ai-evolution-lab/docs/SYSTEM_ENGINEERING_COLLABORATION.md`
covers the model-evolution research programme in depth. This document covers the
whole estate and how to work in it.

---

## 1. What this is

Open coordination infrastructure for East Africa. The bet is that value sits in
**rails and measurement**, not in models or applications. Applications exist as
reference implementations that prove a rail works — not as the product.

> Build railroads, not trains.

The success metric is **increase in reusable engineering capability for future
builders**, not usage of anything here. A rail adopted by someone who never
mentions this project is a success, not a loss.

## 2. Doctrine (binding, not aspirational)

**Before creating anything, in order:** contribute upstream → extend existing →
fork and improve → standardize competing options → create new *only* if nothing
reusable exists. Every project originates from a validated gap in
`docs/GAP_REGISTER.md`.

**Builder invisible, problem visible.** No firsts, no counts, no
self-congratulation. The test for any output: *is this about a problem in the
world, or about what I built?*

**Ten-year maintenance horizon.** Docs, tests, governance and standards are code.
Every artifact must let another engineer continue without the original author.

**Verify, don't claim.** Parse gates before every push; live smoke-test against
real endpoints; never assert a command passed unless it ran. Downloads and stars
are not adoption — see §8.

## 3. Architecture

```
   signals in                 routing                    surfaces out
┌──────────────┐      ┌──────────────────┐      ┌──────────────────────┐
│ coord-ingest │─────▶│ africa-coord-bus │─────▶│ ~34 MCP servers      │
│ HDX · GDACS  │      │ routing tables   │      │ mpesa · wapimaji ... │
│ Open-Meteo   │      │ cascades         │      └──────────────────────┘
│ USGS · Kobo  │      │ offline queue    │      ┌──────────────────────┐
│ Flood Hub    │      │ CAP · HXL · IPC  │─────▶│ CAP 1.2 to existing  │
└──────────────┘      └──────────────────┘      │ emergency tooling    │
                               │                 └──────────────────────┘
                               ▼
                    ┌──────────────────┐
                    │ kipimo           │  independent measurement
                    │ Swahili benchmark│  ← nature-ai-evolution-lab
                    │ Pareto selector  │    evaluates here
                    └──────────────────┘
```

**The interoperability thesis.** The bus speaks CAP 1.2, HXL and an IPC-phase
hint. A ministry can therefore consume a drought alert **without adopting
anything here** — it arrives in a format its existing tools already read. That is
adoption without capture, and it is the distribution strategy: speak the
incumbent's schema and you do not need permission to be useful.

## 4. Repo map — live versions as of 2026-09-05

| Repo | PyPI | Role |
|---|---|---|
| `africa-coord-bus` | **0.4.0** | Event bus. Kenya + Tanzania routing, cross-border cascades, offline-first CRDT queue, CAP/HXL/IPC export, declared provenance |
| `coord-ingest` | **0.4.0** | Feed adapters → typed events: Open-Meteo, USGS, GDACS, HDX/OCHA, Kobo/ODK, Google Flood Hub |
| `kipimo` | **0.4.0** | Swahili agent-task benchmark; parallel harness; deployment-Pareto selector |
| `mpesa-mcp` | **0.2.7** | M-Pesa/Daraja + Africa's Talking. 23 tools. The most externally engaged repo |
| `wapimaji-mcp` | **0.1.8** | NDMA drought phases, 47 counties. DPGA submission pending |
| `reli-cli` | 0.1.1 | On-ramp: `reli up · list · doctor · demo drought` |
| `decision-intelligence-mcp` | 0.1.2 | Strategy/philosophy corpus as tools |
| `classical-strategy-mcp` | 0.1.1 | **Tombstone.** Renamed; import raises and redirects |
| `nairobi-stack` | — | This hub: gap register, doctrine, catalog, automations |
| `leapfrog-rd-foundry` | *private* | Global public-R&D → mechanism → recombination pipeline |
| `nature-ai-evolution-lab` | *private* | Small-model capability evolution, evaluated by kipimo |
| `AfriKaziOS` | — | Institutional architecture across 7 domains |

~34 MCP servers on the registry, 32 on Glama, 156 GitHub repos, 17 HuggingFace
datasets.

## 5. Engineering standards

**Gates before every push:** `ast.parse` / `py_compile`, `pytest`, cold-install in
a clean venv, and live smoke-test where an endpoint exists. Live testing catches
what offline tests miss — the HDX geometry bug and a dead ReliefWeb endpoint were
both found this way.

**Provenance is structural, not conventional.** Every `CoordinationEvent`
declares `reality` (REAL/DEMO) and `confidence` (CONFIRMED/PROBABLE/SPECULATIVE/
UNKNOWN). A DEMO event **cannot** export as a live CAP alert — it becomes
`status=Exercise`. Declared, not string-sniffed: the earlier sniffing approach let
a synthetic event without a "DEMO" prefix pass as real.

**Untested is not zero.** kipimo reports a target whose generator crashed,
timed out, or was unconfigured as UNKNOWN with a reason — never ranked at 0.0.
Conflating "the model failed" with "we never tested it" is how an evaluation
system starts measuring its own assumptions.

**Every MCP tool return carries a `source` field.** DEMO-labelled responses are
reference data; the response names the verifying authority (sasra.or.ke,
nema.go.ke, epra.go.ke, cob.go.ke).

**Licensing:** MIT for infrastructure, CC-BY-NC-ND for end-user apps, CC-BY for
data. **No agent changes licensing autonomously, ever.**

## 6. Automation that runs without anyone

Two GitHub Actions in this repo, Mondays 06:00 UTC:

- **`portfolio-audit.yml`** — build-breaking packaging (PEP 639), version drift
  between main and PyPI, unpinned SDK majors, repo hygiene. Opens one issue.
- **`awaiting-reply.yml`** — every open issue/PR authored in someone else's repo
  where a **human replied and we have not**. Bots excluded. Email-independent by
  design, because the failure it exists to catch was a dead mail forward.

Both currently green. The awaiting-reply detector found a 66-day-old unanswered
technical review on its first run.

## 7. Known failure classes (do not rediscover these)

| Failure | Detail |
|---|---|
| **PEP 639 build break** | A license *expression* plus a trove *classifier* makes current setuptools refuse to build. Silently broke `mpesa-mcp` and `wapimaji-mcp`; sdist, wheel and editable install all failed. Now audited weekly |
| **Unpinned SDK major** | `mcp>=1.0.0` resolved to 2.0.0, which removed `mcp.server.fastmcp`. Package installed but imported nothing. Pin upper bounds |
| **Silent wrong-value default** | `airtime_send` defaulted `currency_code="KES"` regardless of recipient country — a `+255` number received a KES amount with no error. Fixed by rejecting mismatches before the API call. **Look for this class elsewhere** |
| **Dead mail route** | GitHub notifications forwarded through an address that stopped working in 2023; two collaboration offers lost for 100+ days. Nobody reports mail they never got a reply to |
| **Stale exact-count test** | `test_tool_count` asserted 5 while 23 tools registered. Assert a floor, not an exact count |
| **Retirement debt** | Renamed packages leave abandoned predecessors. Publish a tombstone, don't just move on |

## 8. Honest adoption state

156 repos · **25 stars · 14 forks** · 1 HuggingFace like · 24 Dev.to reactions.

PyPI download counts (~1,300–4,400/month) are **mirror and crawler traffic, not
adoption**. The tell: `coord-ingest` recorded 331 downloads in its first week
while unannounced and known to nobody. A flat 4× band across a dozen obscure
packages is a bot fingerprint, not a power law. **Do not cite download counts as
evidence of anything.**

Real external engagement, total: `punkpeye` (Glama directory), `ainetwork-global`,
`kushdab` (Africa's Talking). Three humans.

**The constraint has never been code output. It is reach.** Rails are built and
sound; almost nobody is walking them yet.

## 9. Live human threads

- **kushdab (Africa's Talking)** — reviewed mpesa-mcp, found the currency bug.
  Answered; fix shipped in 0.2.7.
- **Anna Iosif (Ushahidi)** — offered a collaboration call. Replied on the issue;
  no public email, so Discord or the thread is the route.
- **Emma (Code for Africa)** — openAFRICA listings. Email sent.
- **Rose (Mozilla Fellow, Open Elections Kenya)** — parallel vote tabulation for
  2027. The CRDT merge and declared provenance map directly onto PVT. Politically
  sensitive: her arrest in 2025 is the threat model, and the maintainer is a US
  federal employee. **Contributing MIT rails ≠ participating in election
  monitoring.** Not actioned pending judgement.

## 10. Rules for collaborating agents

**Reality is the authority. No model is.** If you disagree with something here,
record: claim → evidence for → evidence against → falsifier → experiment. No
model voting; three agreeing systems is not evidence.

**Git is the memory bus.** Leave work in the repo, not in your context. The model
is replaceable; the accumulated intelligence is not.

**Verify before deferring.** Do not accept a prior handoff because a capable
system wrote it. Re-run the tests.

**Do autonomously:** code, tests, commits, PRs and merges on our own repos,
releases, dependency fixes, hygiene, audits.

**Never autonomously:** change licensing; promote a candidate in the evolution
lab; edit protected/hash-pinned files (file a proposal instead); delete published
packages; seed unverified records into a provenance-first ledger; act in the
maintainer's voice on a first approach to a new institution.

**Surface, don't execute:** anything touching his identity, federal posture, or
irreversible public exposure.

## 11. Current bottleneck

Not architecture. **Measurement, then reach.**

1. `nature-ai-evolution-lab` Generation 0 is unmeasured. `require_baseline()`
   raises until it exists, so no capability claim is possible — by design.
   Needs a machine that can load Qwen3-0.6B.
2. kipimo has never been run against live endpoints. Two targets — one API, one
   local small-open model — produce the first honest Swahili scorecard. That is
   evidence an institution responds to; 156 repos are not.
3. The frontier gaps (G2 data sovereignty, G3 measured pilot) need an
   institutional counterpart, not more code.
