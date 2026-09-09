# Ecological Portability Contract

**Date:** 2026-09-09  
**Purpose:** prevent Nairobi Stack from treating one Kenyan or African environment as the default human context.

## Rule

A local implementation is a **phenotype**, not the platform.

Nairobi Stack should preserve one stable rail while allowing environment-specific expression:

```text
stable service contract
+ environment manifest
+ local context pack
+ specialist tools/data
+ live state
→ local phenotype
```

Murang'a may be the first agricultural phenotype. It must not define the architecture for Turkana, Bunyala, the Sahel, coastal systems, rainforest systems, islands, megacities or informal economies.

## Required separation

**Core rail:** identity, location, time, authority, evidence, uncertainty, action, outcome, audit, offline/degraded-mode behavior.

**Local context:** languages, ecological regime, livelihoods, institutions, markets, transport, communications, current weather/water/disease/service state.

**Specialist organ:** crop model, livestock tool, hydrology model, market tool, service router, speech model, local atlas, human expert.

Never hard-code local context into a reusable core when a manifest/module boundary can represent it explicitly.

## Portability evidence

A rail should report:

- core changes required to move environments;
- local/context changes required;
- new data and tools;
- adaptation time;
- human validation time;
- retained task utility;
- offline/degraded-mode performance;
- newly introduced failure modes.

Call this **Transfer Efficiency** rather than assuming portability from common APIs.

## First ecology transfer sequence

For agriculture/livelihood protection:

1. African Ecological Node v0 — Murang'a phenotype;
2. Turkana ASAL/pastoral phenotype;
3. Bunyala floodplain/lake/river phenotype;
4. Sahel dryland/transhumance phenotype;
5. later an urban informal-economy phenotype.

The shared outcome can remain stable while the active capability graph changes.

## Critical anti-pattern

Do not solve transfer by accumulating location-specific `if/else` branches, one-off prompts or duplicated workflows inside the core. That creates **regulatory debt** and turns local adaptation into permanent maintenance burden.

When repeated uncertainty comes from missing state, improve the environment instead of asking the model to guess: publish the API, digitize the handbook, instrument the water point, cache the map, collect governed speech, standardize the schema, or create a validated atlas.

## Canonical research source

The underlying developmental-intelligence theory and compiler experiments live in `gabrielmahia/nature-ai-evolution-lab`. Nairobi Stack is the implementation proving ground, not the owner of the selection theory.
