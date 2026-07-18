# Platform Interconnect: One Graph, Many Surfaces
**Candidate location:** `nairobi-stack/docs/PLATFORM_INTERCONNECT.md`
**Status:** v1 — partially executed July 17, 2026. Companion to OPEN_WEIGHTS_STRATEGY.md.

---

## 1. Thesis

The portfolio currently exists as **point assets** on nine platforms. Each platform is a
different audience with a different discovery mechanism:

| Platform | Audience | Discovery mechanism | Assets |
|---|---|---|---|
| PyPI | Python developers | `pip search`, project pages | 36 packages |
| MCP Registry (official) | Agent builders | registry search, `io.github.gabrielmahia` namespace | 33 servers |
| Hugging Face | ML/data community + **AI agents via HF MCP** | hub search, dataset cards, tags | 17 datasets + kipimo leaderboard Space |
| GitHub | Engineers, auditors | topics, READMEs, org graph | 36 public repos + private |
| Glama / Smithery | MCP discovery layer | server listings | mpesa-mcp seeded |
| Dev.to | Narrative / practitioners | tags, series | problem-first pipeline |
| Kaggle | Data scientists | datasets, notebooks | account ready, unused |
| DPGA | Governments, institutions | Digital Public Goods registry | 2 under review, 1 incomplete |
| Streamlit Cloud | End users | direct links | reference apps |

A visitor landing on any one node currently has no reliable path to the others. The fix is
not more content — it is **edges**. Every node should route to three hubs:

1. **On-ramp:** `pip install reli-cli` (how you run the stack)
2. **Evaluation:** kipimo (how you measure any model against it — including open weights)
3. **Bus:** africa-coord-bus (how pieces talk to each other)

This converts nine audiences into one funnel and makes the whole graph legible to the two
consumers that matter most going forward: **human developers and AI agents**. The Hugging
Face MCP server, the official MCP Registry, and the emerging `llms.txt` convention mean
agents now browse these platforms directly — cards, registries, and docs are agent-readable
distribution, which is precisely the audience an agent-coordination stack should optimize for.
The open-weight inflection (Kimi K3, GLM 5.2, DeepSeek V4, Nemotron 3) multiplies this:
model-agnostic rails and evals are the assets every new model's users need on day one.

## 2. Executed today (autonomous, verified)

- **Hugging Face — 16/17 dataset cards updated live.** Idempotent `<!-- interconnect:v1 -->`
  block appended to every card (kipimo's curated hub card intentionally skipped). Each card
  now routes to kipimo + leaderboard, reli-cli + official MCP Registry namespace,
  africa-coord-bus, and the full dataset collection, and explicitly states open-weight and
  small-model evaluation parity. Marker-based: re-runs update in place, never duplicate.
  Script preserved at `interconnect/hf_interconnect.py` for future v2 rollouts.
- **Dev.to — standards-body article staged as unpublished draft** (id 4170507) via API.
  Nothing publishes without review; internal draft notes stripped automatically.
- **Credential audit:** HF token (write) live; Dev.to key live (POST requires the
  `User-Agent` + Forem v1 `Accept` headers — recorded for future automation). Both GitHub
  tokens return 401: fine-grained expired ~June 30; classic also dead. PyPI untested this
  session (publishing not required today).

## 3. Blocked on GitHub token rotation (one manual step)

Once a new fine-grained token exists (repo contents + workflows scopes), execute as
commit-sized waves:

| # | Commit | Scope | Acceptance criteria |
|---|---|---|---|
| 1 | `pyproject.toml` project-urls standardization | all 36 packages | Every PyPI page shows: Docs (nairobi-stack), MCP Registry entry, Datasets (HF), Changelog. Wave-scripted via Git Trees API |
| 2 | README interconnect footer | all 36 repos | Same marker-based block as HF cards, problem-first wording; idempotent script |
| 3 | `llms.txt` at docs root | nairobi-stack | Agent-readable index of the whole graph: servers, packages, datasets, evals, entry points |
| 4 | MCP Registry `server.json` metadata pass | 33 servers | Each entry's homepage/docs URLs point into the graph, not just the repo |
| 5 | kipimo v0.2 open-weight scorecard | kipimo | Per OPEN_WEIGHTS_STRATEGY.md commits 3–4; results published to the HF leaderboard Space |
| 6 | Kaggle mirror + notebook | 2–3 flagship datasets | Datasets mirrored; one notebook: "Score any open-weight model on Swahili agent tasks" (DEMO-labeled) |
| 7 | Glama/Smithery listing pass | MCP servers beyond mpesa-mcp | Listings verified, linked into graph |

Also pending from before (manual, same settings session): delete stale PyPI token
`github-actions-all-repos`; verify Glama mpesa-mcp Dockerfile build steps; complete DPGA
wapimaji-mcp submission (institutional-trust edge — DPGA listing is the strongest signal
for the government/NGO audience the vision ultimately serves).

## 4. Design rules for all interconnect work

1. **Marker-based idempotence** (`<!-- interconnect:vN -->`) everywhere — cards, READMEs,
   footers. Re-runs replace; nothing duplicates. Version the marker, not the prose.
2. **Problem-first, builder-invisible** on every public surface. The block names problems
   and tools, never accomplishments. No counts, no "first," no personal framing.
3. **Every edge bidirectional where the platform allows.** HF→PyPI exists now; PyPI→HF
   comes with commit 1; Registry→docs with commit 4.
4. **Agents are a first-class audience.** llms.txt, machine-readable registry metadata,
   and model-agnostic eval instructions are edges for non-human readers.
5. **One canonical hub:** nairobi-stack docs. All roads lead there; it links everywhere
   else. No platform hosts unique doctrine.
6. **Dry-run before live, always.** Today's HF rollout ran dry first; every future wave does.

## 5. Risk notes

- **Token hygiene:** three live credentials were exercised today from an ephemeral
  container (HF write, Dev.to, and two dead GitHub tokens transmitted for status checks).
  All are stored in long-term memory/Bitwarden per existing practice — but the GitHub
  classic token is dead and should be deleted from Bitwarden, and rotation day is the right
  moment to regenerate the Dev.to key and HF token on principle, then update stored copies.
- **Platform ToS:** all writes today were owner-authorized edits to owner-controlled
  assets via official APIs at trivial volume. Keep future waves similarly low-volume and
  reviewable.
