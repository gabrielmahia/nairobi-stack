# Research Sensor Grid — multipolar intake, six channels, one reuse ledger
**Location:** `nairobi-stack/docs/RESEARCH_GRID.md`
**Method:** every entity feeds a channel; every finding passes the FUTURES_LENS
filter; anything adopted lands in the Reuse Ledger below with a target repo.
A reading list that doesn't change a repo is entertainment.

## The six channels and their anchors (40-node core)

| Channel | Primary anchors | Secondary |
|---|---|---|
| 1. Models & agents | Moonshot, DeepSeek, Qwen, Shanghai AI Lab (OpenCompass/LMDeploy), BAAI, Anthropic, DeepMind, OpenAI, Meta FAIR, Mistral | 01.AI, MiniMax, NAVER, LG AI |
| 2. Systems, deployment & physical intelligence | RIKEN AIP, AIST/ABCI, NII, DFKI, MPI Intelligent Systems, Fraunhofer, Sakana AI | ETH/EPFL, KAIST, Preferred Networks |
| 3. Security & governance | OpenSSF, MITRE, NIST, CISPA, IETF | AfricaCERT, Serianu, Shadowserver, Citizen Lab |
| 4. Digital public infrastructure | Centre for DPI (India), DPGA, GovStack, MOSIP, OpenG2P | DHIS2, OpenCRVS, Bhashini/AI4Bharat, GSMA M4D |
| 5. Domain science | CGIAR/ILRI, ECMWF, Copernicus/Digital Earth Africa, WHO/Africa CDC, JAXA/JAMSTEC | ICPAC, RCMRD, KEMRI, Eawag, Swiss TPH |
| 6. African adaptation & institutional reality | Masakhane, Deep Learning Indaba, CMU-Africa, Makerere AI Lab, AIMS, AfriDSAI | Lelapa AI, Research ICT Africa, UoN, APHRC, Lacuna Fund |

**Lane assignments (the strategic correction):** China dominates open models and
efficiency; Japan anchors reliability and physical systems; Germany anchors
applied translation and cybersecurity; India anchors population-scale DPI;
Switzerland anchors standards and privacy; **Africa defines problem conditions,
languages, and legitimate priorities — channel 6 outranks channel 1 in any
conflict.**

## Extraction protocol (per finding)
What changed? · What's technically novel? · What assumption does it break? ·
What can the stack reuse? · **What would fail under East African conditions?** ·
Does it imply a new server, standard, dataset, or reference implementation? ·
Durable architecture or model hype?

## Reuse Ledger

| # | Source entity | Artifact | Target | Status |
|---|---|---|---|---|
| R1 | OpenSSF (ch. 3) | Scorecard baseline + remediation (branch protection, dependabot, least-privilege workflow tokens) | 9 core repos | **EXECUTED 2026-07-17** — coord-bus baseline 3.7/10; wave script at interconnect/security_wave.py; remaining 32 servers queued |
| R2 | BAAI (ch. 1) | BGE-M3 multilingual embeddings (Swahili-capable, open) | swahili-civic-nlp / any RAG server | Adopt as default embedding recommendation; benchmark against kipimo term-grounding tasks |
| R3 | Shanghai AI Lab (ch. 1) | OpenCompass eval framework | kipimo | Ship an OpenCompass-format exporter (`kipimo tasks --format opencompass`) so the Swahili benchmark enters the Chinese eval ecosystem — distribution into the open-weight world's own instrument |
| R4 | Copernicus / Digital Earth Africa (ch. 5) | Free analysis-ready EO data for Africa | wapimaji-mcp, mazingira-mcp, kilimo-mcp | Document as primary data source; replaces ad-hoc satellite sourcing |
| R5 | DHIS2 (ch. 4) | Kenya's actual national health information system, open API | kenya-health-mcp, afya-mcp | Interop pattern doc: agents ground on the registry government already runs — genchi genbutsu applied |
| R6 | Masakhane (ch. 6) | Community model + African-language corpora | kipimo issue #1 (native-speaker review) | **Contribute upstream first (Baobab rule 3):** draft collaboration issue for G's review — external outreach stays human-approved |
| R7 | Centre for DPI / GovStack (ch. 4) | DPI building-block specifications | DPGA submissions, G2 framework | Frame mpesa-mcp/wapimaji-mcp as GovStack-aligned building blocks; strengthens pending DPGA reviews |
| R8 | NIST AI RMF (ch. 3) | Risk-management vocabulary institutions already trust | SCORECARD.md, DPGA docs | Map DEMO/REAL discipline onto RMF terms — translation, not adoption |
| R9 | Sakana AI (ch. 2) | Evolutionary model merging | ops-shield (private) | Watch-only; biomimicry alignment noted |
| R10 | AIST ABCI model (ch. 2) | Publicly accessible national AI compute as policy pattern | G2/G9 doctrine, Cassava engagement | Reference architecture for "sovereign compute without sovereign models" |

## Standing rules
1. Track frameworks and standards, not daily output.
2. One in-region reuse beats ten citations: every quarter, at least one ledger
   row must move to EXECUTED.
3. External outreach (issues, PRs, emails to entities) is drafted autonomously,
   sent by a human. Repos are ours; relationships are G's.
4. The grid is a sensor network, not a syllabus — prune any node that goes two
   quarters without producing a ledger row.
