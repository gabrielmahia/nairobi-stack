#!/usr/bin/env python3
"""Audit repositories for portfolio-wide AI agent coordination surfaces.

Uses only the Python standard library. If GITHUB_TOKEN (or PORTFOLIO_REPO_TOKEN
via the workflow) can access private repositories, they are included. Otherwise
GitHub returns only repositories visible to the token.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

REQUIRED = ("AGENTS.md", "agent-context.json")\nRECOMMENDED = (".github/copilot-instructions.md",)\nPOLICY_MARKER = "coverage-adaptive-reasoning:v2"

@dataclass
class RepoAudit:
    name: str
    full_name: str
    private: bool
    archived: bool
    default_branch: str
    missing_required: list[str]
    missing_recommended: list[str]\n    missing_policy_marker: bool\n\n    @property\n    def compliant(self) -> bool:\n        return not self.missing_required and not self.missing_policy_marker

def request_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "portfolio-agent-instructions-audit",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def list_repos(owner: str, token: str | None) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        if token:
            url = "https://api.github.com/user/repos?" + urllib.parse.urlencode({"per_page": 100, "page": page, "affiliation": "owner", "sort": "full_name"})
        else:
            url = f"https://api.github.com/users/{urllib.parse.quote(owner)}/repos?" + urllib.parse.urlencode({"per_page": 100, "page": page, "sort": "full_name"})
        batch = request_json(url, token)
        if not batch:
            break
        repos.extend(r for r in batch if r.get("owner", {}).get("login", "").lower() == owner.lower())
        if len(batch) < 100:
            break
        page += 1
    return repos

def get_file_text(full_name: str, path: str, ref: str, token: str | None) -> str | None:\n    quoted = urllib.parse.quote(path, safe="/")\n    url = f"https://api.github.com/repos/{full_name}/contents/{quoted}?ref={urllib.parse.quote(ref)}"\n    try:\n        payload = request_json(url, token)\n    except urllib.error.HTTPError as exc:\n        if exc.code == 404:\n            return None\n        raise\n    import base64\n    content = payload.get("content")\n    if payload.get("encoding") == "base64" and content is not None:\n        return base64.b64decode(content).decode("utf-8", errors="replace")\n    return None\n\ndef file_exists(full_name: str, path: str, ref: str, token: str | None) -> bool:
    quoted = urllib.parse.quote(path, safe="/")
    url = f"https://api.github.com/repos/{full_name}/contents/{quoted}?ref={urllib.parse.quote(ref)}"
    try:
        request_json(url, token)
        return True
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False
        raise

def audit(owner: str, token: str | None) -> list[RepoAudit]:
    results: list[RepoAudit] = []
    for repo in list_repos(owner, token):
        branch = repo.get("default_branch") or "main"
        full_name = repo["full_name"]
        missing_required = [p for p in REQUIRED if not file_exists(full_name, p, branch, token)]
        missing_recommended = [p for p in RECOMMENDED if not file_exists(full_name, p, branch, token)]\n        agents_text = get_file_text(full_name, "AGENTS.md", branch, token)\n        missing_policy_marker = bool(agents_text is not None and POLICY_MARKER not in agents_text)\n        results.append(RepoAudit(repo["name"], full_name, bool(repo.get("private")), bool(repo.get("archived")), branch, missing_required, missing_recommended, missing_policy_marker))
    return results

def render_markdown(owner: str, rows: list[RepoAudit], has_token: bool) -> str:
    active = [r for r in rows if not r.archived]
    compliant = [r for r in active if r.compliant]
    missing = [r for r in active if not r.compliant]
    lines = [
        "# AI agent coordination audit", "",
        f"Owner: `{owner}`",
        f"Repository visibility: {'token-scoped (may include private)' if has_token else 'public only'}",
        f"Active repositories checked: **{len(active)}**",
        f"Required-file compliant: **{len(compliant)}**",
        f"Missing required surfaces: **{len(missing)}**", "",
        "## Required", "", "- `AGENTS.md`", "- `agent-context.json`", f"- AGENTS.md marker: `{POLICY_MARKER}`", "",
        "## Recommended", "", "- `.github/copilot-instructions.md`", "",
        "## Non-compliant active repositories", "",
    ]
    if not missing:
        lines.append("All active repositories checked have required surfaces.")
    else:
        lines += ["| Repository | Missing required | Missing policy marker | Missing recommended |", "|---|---|---|---|"]
        for r in missing:
            req = ", ".join(f"`{x}`" for x in r.missing_required) or "—"
            rec = ", ".join(f"`{x}`" for x in r.missing_recommended) or "—"
            marker = "yes" if r.missing_policy_marker else "—"\n            lines.append(f"| `{r.full_name}` | {req} | {marker} | {rec} |")
    lines += ["", "## Policy", "", "A missing file does not authorize blind mass-editing. Inspect each repository's local architecture and tests before applying templates.", "", "This audit checks required-file presence and the canonical Coverage-Adaptive Reasoning v2 marker; it does not prove instruction quality."]
    return "\n".join(lines) + "\n"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", default="gabrielmahia")
    parser.add_argument("--output", default="agent-instructions-report.md")
    parser.add_argument("--fail-on-missing", action="store_true")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("PORTFOLIO_REPO_TOKEN")
    try:
        rows = audit(args.owner, token)
    except Exception as exc:
        print(f"audit failed: {exc}", file=sys.stderr)
        return 2
    report = render_markdown(args.owner, rows, bool(token))
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    active_missing = [r for r in rows if not r.archived and not r.compliant]
    return 1 if args.fail_on_missing and active_missing else 0

if __name__ == "__main__":
    raise SystemExit(main())
