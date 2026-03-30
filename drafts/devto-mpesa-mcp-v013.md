---
title: "mpesa-mcp v0.1.3: tool annotations, Server Cards, and what the MCP accuracy benchmark means for payment tools"
date: 2026-03-30
platform: dev.to
tags: [kenya, mcp, python, africa]
status: ready-to-publish
cross_post: hashnode, safaricom-developer-forum
---

*Follow-up to: [Why M-Pesa, Africa's Talking, and USSD are missing from AI agent tooling](https://dev.to/gabrielmahia/why-m-pesa-africas-talking-and-ussd-are-missing-from-ai-agent-tooling-and-what-i-did-about-it)*

---

v0.1.3 of mpesa-mcp shipped this week. Three things in it that are worth explaining.

## 1. Tool annotations

The MCP 2025-03-26 spec introduced `ToolAnnotations` — a way for servers to declare how each tool behaves: read-only, destructive, idempotent, or open-world. All five tools in mpesa-mcp now declare these explicitly.

```python
@mcp.tool(annotations={
    'title': 'M-Pesa STK Push',
    'readOnlyHint': False,     # moves money — modifies state
    'destructiveHint': True,   # irreversible financial operation
    'idempotentHint': False,   # each call creates a new transaction
    'openWorldHint': True,     # reaches Safaricom's external API
})
def mpesa_stk_push(phone: str, amount: int, ...):
```

Without this, Claude Desktop and ChatGPT treated `mpesa_stk_query` — which only checks a transaction status — the same as `mpesa_stk_push`, which moves real money. Both showed as write operations requiring confirmation. That friction is wrong for a read-only status check.

Now:
- `mpesa_stk_query` and `mpesa_transaction_status` are read-only → auto-approved
- `mpesa_stk_push`, `sms_send`, `airtime_send` are destructive → confirmation required

For payment tools this isn't cosmetic. A user shouldn't have to confirm "check if my payment went through." They should absolutely have to confirm "send KES 500 to this number."

## 2. Server Cards / .well-known

Capabilities are now advertised at `.well-known/mcp.json` in the repo — the emerging MCP Server Cards standard that's a roadmap priority for 2026:

```bash
curl https://raw.githubusercontent.com/gabrielmahia/mpesa-mcp/main/.well-known/mcp.json
```

This lets registries and browsers index the server's tools, input schemas, and install instructions without connecting to the server. It's the MCP equivalent of `robots.txt` — a machine-readable signal to the ecosystem.

## 3. The accuracy benchmark and why it matters more for payment tools

CData published a benchmark in early 2026 finding most MCP servers accurate 60–75% of the time on complex queries. The specific failure modes: silent parameter drops, multi-condition queries half-applied, write operations failing validation without surfacing an error.

For a weather or calendar MCP, 70% accuracy is annoying. For a payment MCP, it's dangerous.

mpesa-mcp's test suite specifically covers the failure patterns the benchmark identified:

**Phone number format normalization** — Kenyan numbers appear in three formats in the wild:
- `0712345678` (local format)
- `254712345678` (E.164 without +)
- `+254712345678` (full E.164)

The Daraja API requires `254712345678`. All three inputs must produce the same result.

**Boundary amounts** — M-Pesa has a minimum transaction (KES 1) and per-transaction maximum. Tests cover both boundaries and the values immediately adjacent.

**Missing optional fields** — `account_reference` and `transaction_desc` are optional in the tool signature. Tests confirm omitting them produces a clean default, not a silent failure.

```bash
pytest tests/ -v
pytest tests/test_phone_formats.py
pytest tests/test_boundary_amounts.py
```

## Install

```bash
pip install mpesa-mcp==0.1.3
# or
uvx mpesa-mcp
```

MCP Registry: `io.github.gabrielmahia/mpesa-mcp`

GitHub: [github.com/gabrielmahia/mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp)

---

*Gabriel Mahia builds decision infrastructure for East Africa. All tools at [gabrielmahia.github.io](https://gabrielmahia.github.io).*
