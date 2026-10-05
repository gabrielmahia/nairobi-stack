# AI Agent Coordination Standard v1

## Purpose

Make every repository in the Gabriel Mahia / East Africa coordination estate safely workable by multiple AI systems without relying on shared chat context.

Supported in principle:
- ChatGPT / Codex / Work / Astra
- Claude / Claude Code
- Gemini / Gemini CLI
- Grok
- Muse and future agent systems
- open-weight/local coding agents

The standard is provider-neutral.

## Core doctrine

> **Git is the memory bus. GitHub Issues and draft PRs are the coordination bus. Tests and external reality are the authority.**

No model is authoritative because of identity, capability tier, or agreement with other models.

## Required repo surfaces

Every actively developed repo should expose:

### 1. AGENTS.md
Human-readable cold-start instructions:
- what the repo is,
- architecture,
- critical invariants,
- commands,
- destructive boundaries,
- collaboration rules.

### 2. agent-context.json
Machine-readable cold-start manifest:
- repo/project name,
- stable/integration branch,
- key docs,
- test commands,
- task registry,
- prohibited actions,
- current workstreams.

### 3. GitHub Issues
Canonical task registry.

### 4. Draft PR claim protocol
A draft PR is the visible concurrency lock.

Branch:
```
agent/<agent-name>/<issue-number>-<slug>
```

PR title:
```
[CLAIM #<issue>] <agent-name>: <scope>
```

### 5. Reproducible tests
No “done” handoff without commands another system can re-run.

## Collision avoidance

Before substantive work an agent must:
1. fetch latest target branch,
2. read AGENTS.md + agent-context.json,
3. inspect open Issues,
4. inspect open/draft PRs,
5. run baseline,
6. claim one bounded scope.

If scope overlaps an existing draft PR:
- review/test it,
- subdivide,
- or choose another task.

Do not independently implement competing versions unless the Issue explicitly calls for an experiment/tournament.

## Work decomposition

Prefer parallel lanes with minimal file overlap:
- research/data,
- ingestion,
- core model/schema,
- UI,
- testing/benchmarking,
- documentation,
- security,
- deployment.

## Handoff contract

Every agent must leave in Git:
- working code/docs,
- tests,
- failures,
- assumptions,
- exact next action.

Chat-only state is lost state.

## Epistemic disagreements

Use:
```
claim
→ evidence for
→ evidence against
→ falsifier
→ experiment
```

Do not resolve disagreements by model voting.

## Protected actions

Agents must not autonomously:
- change licensing,
- expose credentials,
- publish sensitive personal data,
- make irreversible external commitments,
- contact institutions in the maintainer's voice on a first approach,
- seed unverified data into provenance-first ledgers,
- weaken existing truth/safety labels,
- delete published packages/data without human authorization.

Repo-specific AGENTS.md may add stricter rules.

## Portfolio adoption sequence

1. Add/upgrade AGENTS.md.
2. Add agent-context.json.
3. Add PR/Issue templates.
4. Add audit to verify required surfaces.
5. Convert large work into Issue-scoped branches/draft PRs.
6. Keep runtime agent orchestration separate from engineering coordination.

## MCP / A2A / Git distinction

- **MCP**: agent ↔ tool/data service.
- **A2A**: runtime agent ↔ runtime agent.
- **africa-coord-bus**: application/domain events.
- **GitHub Issue/branch/PR protocol**: software-development coordination.

Do not use an application event bus as a substitute for code review, commit history, and test state.

## Maturity target

A repo satisfies v1 when an unfamiliar agent can answer, without prior chat:
- What is this?
- What must not be broken?
- What is currently being worked on?
- What may I safely claim?
- How do I test my work?
- How do I hand it off?
