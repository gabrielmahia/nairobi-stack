#!/usr/bin/env python3
"""Awaiting-reply detector — the blindside catcher.

Two collaboration offers were lost not because the work was weak but because
someone replied and nobody answered. Ushahidi offered a call (142 days, silent).
Code for Africa followed up twice (100 days, silent). Both were visible the whole
time in public threads; nothing was watching.

This watches. It finds every issue or PR the user authored in someone ELSE's
repo where the most recent comment is from someone else — i.e. the ball is in
the user's court — and reports it ranked by how long they have been waiting.

Deliberately GitHub-API-only. It needs no mailbox access, so it keeps working
regardless of how email routing is configured — which is exactly the failure it
exists to survive.
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import urllib.error
import urllib.request

USER = os.environ.get("AUDIT_USER", "gabrielmahia")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
BOTS = {"dependabot[bot]", "github-actions[bot]", "linear[bot]", "codecov[bot]",
        "renovate[bot]", "sonarcloud[bot]", "vercel[bot]"}
# a human waiting this long is a relationship problem, not an inbox problem
URGENT_DAYS = 14


def _get(url: str):
    h = {"User-Agent": "awaiting-reply", "Accept": "application/vnd.github+json"}
    if TOKEN:
        h["Authorization"] = f"token {TOKEN}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
            return json.load(r)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return None


def scan(today: datetime.date | None = None) -> list[dict]:
    today = today or datetime.date.today()
    q = (f"https://api.github.com/search/issues?q=author:{USER}+-user:{USER}"
         f"+state:open&per_page=100&sort=updated")
    res = _get(q) or {}
    waiting = []
    for it in res.get("items", []):
        if not it.get("comments"):
            continue
        repo = "/".join(it["repository_url"].split("/")[-2:])
        comments = _get(f"https://api.github.com/repos/{repo}/issues/{it['number']}/comments"
                        "?per_page=100")
        if not comments:
            continue
        human = [c for c in comments if c["user"]["login"] not in BOTS]
        if not human:
            continue
        last = human[-1]
        if last["user"]["login"] == USER:
            continue                      # ball is in their court, not ours
        waited = (today - datetime.date.fromisoformat(last["created_at"][:10])).days
        waiting.append({
            "repo": repo, "number": it["number"], "title": it["title"],
            "url": it["html_url"], "last_from": last["user"]["login"],
            "last_at": last["created_at"][:10], "days_waiting": waited,
            "excerpt": " ".join(last["body"].split())[:220],
            "urgent": waited >= URGENT_DAYS,
        })
    return sorted(waiting, key=lambda w: w["days_waiting"], reverse=True)


def render(rows: list[dict]) -> str:
    if not rows:
        return "# Awaiting your reply\n\nNothing waiting. Every thread is with them.\n"
    out = ["# Awaiting your reply", "",
           f"{len(rows)} thread(s) where a **person replied and you haven't**. "
           "Ranked by how long they've waited.", ""]
    for w in rows:
        mark = "🔴" if w["urgent"] else "•"
        out += [f"{mark} **[{w['repo']}#{w['number']}]({w['url']})** — "
                f"@{w['last_from']} replied {w['days_waiting']} days ago "
                f"({w['last_at']})",
                f"  > {w['excerpt']}", ""]
    out.append("_A person waiting is worth more than any repo in the portfolio._")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    rows = scan()
    report = render(rows)
    print(report)
    if (p := os.environ.get("GITHUB_STEP_SUMMARY")):
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(report)
    with open("awaiting_reply.md", "w", encoding="utf-8") as fh:
        fh.write(report)
    sys.exit(1 if any(r["urgent"] for r in rows) else 0)
