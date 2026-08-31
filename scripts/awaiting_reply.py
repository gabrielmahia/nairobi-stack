#!/usr/bin/env python3
"""Awaiting-reply detector — find the humans waiting on a response.

Two collaboration offers (Ushahidi, Code for Africa) sat unanswered for 100+ days
because they arrived by email through a forward that had been dead since 2023.
Nobody reports mail they never got a reply to; they just move on. That failure is
silent by construction, so it needs a detector that does not depend on email at all.

This queries the GitHub API for every issue or PR authored by the user in someone
else's repository, then compares the timestamp of their last comment against the
last comment by anyone else. If someone else spoke last, they are waiting.

Deliberately narrow: it reports only "a human is waiting", never what to say.
A templated reply to a collaboration offer is worse than silence.

Bots are excluded — dependabot waiting on you is not a relationship.
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

USER = os.environ.get("GH_USER", "gabrielmahia")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
BOT_MARKERS = ("[bot]", "dependabot", "github-actions", "codecov", "linear")
# a maintainer reply older than this is a relationship going cold, not a fresh ping
STALE_DAYS = 14


def _get(path: str):
    url = f"https://api.github.com/{path}"
    headers = {"User-Agent": "awaiting-reply", "Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
            return json.load(r)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return None


def _is_bot(login: str) -> bool:
    low = (login or "").lower()
    return any(m in low for m in BOT_MARKERS)


def find_awaiting(today: datetime.date) -> list[dict]:
    q = urllib.parse.quote(f"author:{USER} -user:{USER} state:open")
    res = _get(f"search/issues?q={q}&per_page=100&sort=updated")
    if not res:
        return []
    waiting = []
    for it in res.get("items", []):
        repo = "/".join(it["repository_url"].split("/")[-2:])
        num = it["number"]
        comments = _get(f"repos/{repo}/issues/{num}/comments?per_page=100")
        if not isinstance(comments, list) or not comments:
            continue
        mine = [c for c in comments if c["user"]["login"].lower() == USER.lower()]
        theirs = [c for c in comments
                  if c["user"]["login"].lower() != USER.lower() and not _is_bot(c["user"]["login"])]
        if not theirs:
            continue
        last_theirs = max(theirs, key=lambda c: c["created_at"])
        last_mine = max(mine, key=lambda c: c["created_at"])["created_at"] if mine else ""
        # they spoke last -> the ball is in your court
        if last_theirs["created_at"] > last_mine:
            when = datetime.date.fromisoformat(last_theirs["created_at"][:10])
            waiting.append({
                "repo": repo, "number": num, "title": it["title"],
                "url": it["html_url"],
                "who": last_theirs["user"]["login"],
                "waiting_days": (today - when).days,
                "since": when.isoformat(),
                "excerpt": " ".join(last_theirs["body"].split())[:220],
            })
    waiting.sort(key=lambda w: w["waiting_days"], reverse=True)
    return waiting


def render(waiting: list[dict], today: datetime.date) -> str:
    if not waiting:
        return "# Awaiting reply\n\nNobody is waiting on a response. Clear.\n"
    cold = [w for w in waiting if w["waiting_days"] >= STALE_DAYS]
    fresh = [w for w in waiting if w["waiting_days"] < STALE_DAYS]
    out = ["# Awaiting reply", "",
           f"{len(waiting)} thread(s) where a person replied and you have not. "
           "Sorted oldest first — these are relationships, not tickets.", ""]
    for label, group in (("## Going cold (14+ days)", cold), ("## Recent", fresh)):
        if not group:
            continue
        out.append(label)
        for w in group:
            out.append(f"- **{w['repo']}#{w['number']}** — @{w['who']} replied "
                       f"**{w['waiting_days']} days ago** ({w['since']})  ")
            out.append(f"  [{w['title'][:70]}]({w['url']})  ")
            out.append(f"  > {w['excerpt']}")
        out.append("")
    out.append("_This detector reports only that someone is waiting. What to say is yours._")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    today = datetime.date.today()
    waiting = find_awaiting(today)
    report = render(waiting, today)
    print(report)
    if (p := os.environ.get("GITHUB_STEP_SUMMARY")):
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(report)
    with open("awaiting_report.md", "w", encoding="utf-8") as fh:
        fh.write(report)
    sys.exit(1 if waiting else 0)
