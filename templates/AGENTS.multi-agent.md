# AGENTS.md — <repo>

## What this is
<brief>

## Read first
- README.md
- agent-context.json

## Critical rules
- <repo invariants>

## Multi-agent protocol
- Git is the memory bus.
- Read Issues and open/draft PRs before starting.
- Work from an Issue.
- Branch: `agent/<agent>/<issue>-<slug>`
- Open a draft PR immediately to claim scope.
- If another PR overlaps, review/subdivide rather than duplicate.
- Leave tests + handoff in Git.

## Commands
```bash
# install
# test
# lint
```

## Never autonomously
- change licensing
- expose credentials
- perform irreversible external actions
