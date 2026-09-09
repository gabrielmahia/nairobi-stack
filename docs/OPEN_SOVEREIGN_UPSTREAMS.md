# Open Sovereign Upstreams for Nairobi Stack

**Date:** 2026-09-09  
**Purpose:** make proprietary services optional accelerators rather than structural dependencies.

## Core rule

Nairobi Stack should behave more like Linux than like a vertically integrated SaaS product.

Every major capability should prefer:

`CONTRIBUTE → EXTEND → ADAPT → FORK → STANDARDIZE → CREATE NEW`

and every critical dependency should have an open/self-hostable fallback.

A service is not sovereign merely because its application code is open. If it depends at runtime on one closed model API, proprietary map, inaccessible identity service, cloud-only database, or vendor-specific workflow engine, the rent has only moved down the stack.

## Sovereignty Closure

For each rail, maintain:

- an implementation-neutral interface;
- an open/self-hostable implementation where feasible;
- a documented export format;
- a degraded/offline mode;
- a migration test;
- authoritative data provenance;
- a clear human escalation path.

Proposed metric:

`SovereigntyClosure = critical dependencies with tested open fallback / total critical dependencies`

Pair it with **Recovery Half-Life**: time and cost required to restore validated service after a vendor or network dependency disappears.

## High-value global upstreams

### Identity, civil registration, social protection

- **MOSIP** — modular national identity infrastructure: https://github.com/mosip
- **OpenCRVS** — civil registration digital public good: https://github.com/opencrvs/opencrvs-core
- **OpenG2P** — registries, program management, cash transfers, farmer registry and offline inclusion: https://github.com/openg2p

### Payments and financial inclusion

- **Mojaloop** — Apache-2.0 interoperable payment rail: https://github.com/mojaloop
- **Apache Fineract** — open core banking foundation: https://github.com/apache/fineract

Do not reproduce M-Pesa itself. Build interoperable public rails around the reality that mobile money already exists.

### Health

- **DHIS2** — open health-information public good: https://github.com/dhis2
- **OpenMRS** — customizable EMR for resource-constrained settings: https://github.com/openmrs/openmrs-core

The AI layer should retrieve, route, summarize and escalate; clinical truth remains in authoritative systems and human care pathways.

### Field data and offline operation

- **ODK** — offline-capable mobile data collection: https://github.com/getodk/getodk
- **OpenStreetMap** — open map data under ODbL: https://www.openstreetmap.org/copyright
- **QGIS/PostGIS-class open geospatial infrastructure** should be preferred for local control of spatial data.

### Agriculture

- **AgStack / OpenAgri** — modular farm calendar, weather, irrigation, pest/disease and reporting services: https://github.com/agstack
- **FarmVibes.AI** — local multimodal satellite/weather/field workflows: https://github.com/microsoft/farmvibes-ai
- **TorchGeo** — open geospatial ML toolkit: https://github.com/torchgeo/torchgeo
- **Prithvi-EO-2.0** — NASA/IBM open Earth-observation models: https://github.com/NASA-IMPACT/Prithvi-EO-2.0
- **OlmoEarth** — Ai2 open Earth-observation models/data/code: https://allenai.org/olmoearth

Open data base layer:

- Copernicus Sentinel — free/full/open satellite data
- USGS Landsat — no-cost archive
- SoilGrids — CC BY 4.0 global soil maps with uncertainty
- CHIRPS — rainfall history/monitoring
- FAOSTAT — free agricultural statistics/API

### Weather and disaster intelligence

- **GraphCast / GenCast** — DeepMind research code/weights/examples: https://github.com/google-deepmind/graphcast
- **Aurora** — open Earth-system model implementation: https://github.com/microsoft/aurora
- **Earth2Studio** — model-agnostic open weather/climate workflow framework: https://github.com/NVIDIA/earth2studio
- **WeatherBench-X / WeatherBench2** — open evaluation and ground-truth framework: https://github.com/google-research/weatherbench2

Nairobi Stack should expose a weather contract that can swap these models rather than binding one commercial weather API into domain logic.

### Language and voice

- **Mozilla Common Voice** — community speech/text commons: https://commonvoice.mozilla.org/
- **Masakhane** — African-led NLP research/data/evaluation: https://github.com/masakhane-io/masakhane-community
- **VoiceLink** — open low-resource African speech-data pipeline: https://github.com/Neuravox-Foundation/voicelink-core

Voice should degrade gracefully:

`local-language speech → Swahili speech → text/WhatsApp → SMS/USSD → human intermediary`

## Open model substrate

Nairobi Stack should not depend on one “African model.” Preserve model biodiversity behind a stable inference/tool interface.

Preferred research/practical families to track:

- Ai2 **OLMo 3 / OLMo 2** — fully open developmental trail
- IFM **K2 Horizon** — fully open compact research lineage; verify artifacts file-by-file
- Swiss AI **Apertus** — Apache-2.0 open training infrastructure and models
- **Qwen3** — strong Apache-2.0 open-weight family
- **DeepSeek** — high-capability self-hostable lineage; verify exact model license and developmental openness per release

Model serving should remain portable across llama.cpp / vLLM / SGLang / ONNX-class runtimes.

## Intelligence atlases

Do not ask a language model to repeatedly rediscover stable knowledge.

Precompute and version high-cost stable reasoning into local artifacts:

- farm × soil × season × weather → intervention priors;
- county service × citizen state → authoritative process path;
- health symptom/context → navigation/escalation path;
- crop × market × transport → selling/aggregation options;
- curriculum × mastery × language → next learning unit.

Pattern:

`expensive model/simulation/expert → verified atlas → cheap local query → targeted action`

This is the AlphaGenome lesson generalized to public capability.

## Deployment ladder

Prefer the cheapest owned substrate that clears the capability threshold:

`phone/edge → local laptop → institution server → university/co-op cluster → national/shared African compute → rented burst compute`

Rented frontier compute can be economically rational for training or difficult one-off reasoning. It should not become the permanent heartbeat of routine public services.

## Frontier systems as teachers, not landlords

Use proprietary frontier models where they create high information value, but convert repeated capability into durable local artifacts when lawful and technically feasible:

- adapters;
- datasets;
- deterministic tools;
- schemas;
- tests;
- local workflows;
- precomputed atlases;
- open model fine-tunes.

The desired trajectory is **rent once, inherit repeatedly**, not permanent API dependency.

## Near-term field tests

### Murang'a Farm Node

Build one narrow end-to-end farmer workflow from open components:

`voice/photo + field polygon + Sentinel/Landsat + SoilGrids + open weather → calibrated recommendation/escalation`

Test useful decisions, latency, energy, connectivity loss and extension-worker handoff.

### Daniel SME Node

Build voice-first bookkeeping/inventory support where accounting is deterministic and the model only handles language/orchestration. Keep the local ledger authoritative and usable offline.

### Vendor failure drill

For one live Nairobi Stack rail, intentionally remove one external dependency and measure what breaks, recovery time and whether the open fallback actually works.

## Relationship to the Evolution Lab

The canonical research map, openness taxonomy and model/science upstream registry live in `gabrielmahia/nature-ai-evolution-lab` under:

- `docs/SOVEREIGN_OPEN_INTELLIGENCE_COMMONS_2026-09-09.md`
- `data/research/sovereign-open-intelligence-upstreams-2026-09-09.json`

Nairobi Stack should consume those findings as implementation guidance rather than independently maintaining a competing model-research doctrine.
