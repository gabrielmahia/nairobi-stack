#!/usr/bin/env python3
"""Audit repositories for portfolio-wide AI agent coordination surfaces.

Uses only the Python standard library. If GITHUB_TOKEN (or PORTFOLIO_REPO_TOKEN
via the workflow) can access private repositories, they are included. Otherwise
GitHub returns only repositories visible to the token.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

REQUIRED = ("AGENTS.md", "agent-context.json")
RECOMMENDED = (".github/copilot-instructions.md",)
POLICY_MARKER = "coverage-adaptive-reasoning:v2"


@dataclass
class RepoAudit:
    name: str
    full_name: str
    private: bool
    archived: bool
    default_branch: str
    missing_required: list[str]
    missing_recommended: list[str]
    missing_policy_marker: bool

    @property
    def compliant(self) -> bool:
        return not self.missing_required and not self.missing_policy_marker


def request_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "portfolio-agent-instructions-audit",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def list_repos(owner: str, token: str | None) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        if token:
            url = "https://api.github.com/user/repos?" + urllib.parse.urlencode(
                {
                    "per_page": 100,
                    "page": page,
                    "affiliation": "owner",
                    "sort": "full_name",
                }
            )
        else:
            url = (
                f"https://api.github.com/users/{urllib.parse.quote(owner)}/repos?"
                + urllib.parse.urlencode(
                    {"per_page": 100, "page": page, "sort": "full_name"}
                )
            )
        batch = request_json(url, token)
        if not batch:
            break
        repos.extend(
            repo
            for repo in batch
            if repo.get("owner", {}).get("login", "").lower() == owner.lower()
        )
        if len(batch) < 100:
            break
        page += 1
    return repos


def get_file_text(full_name: str, path: str, ref: str, token: str | None) -> str | None:
    quoted = urllib.parse.quote(path, safe="/")
    url = (
        f"https://api.github.com/repos/{full_name}/contents/{quoted}"
        f"?ref={urllib.parse.quote(ref)}"
    )
    try:
        payload = request_json(url, token)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    content = payload.get("content")
    if payload.get("encoding") == "base64" and content is not None:
        return base64.b64decode(content).decode("utf-8", errors="replace")
    return None


def file_exists(full_name: str, path: str, ref: str, token: str | None) -> bool:
    return get_file_text(full_name, path, ref, token) is not None


def audit(owner: str, token: str | None) -> list[RepoAudit]:
    results: list[RepoAudit] = []
    for repo in list_repos(owner, token):
        branch = repo.get("default_branch") or "main"
        full_name = repo["full_name"]
        missing_required = [
            path for path in REQUIRED if not file_exists(full_name, path, branch, token)
        ]
        missing_recommended = [
            path for path in RECOMMENDED if not file_exists(full_name, path, branch, token)
        ]
        agents_text = get_file_text(full_name, "AGENTS.md", branch, token)
        missing_policy_marker = bool(
            agents_text is not None and POLICY_MARKER not in agents_text
        )
        results.append(
            RepoAudit(
                name=repo["name"],
                full_name=full_name,
                private=bool(repo.get("private")),
                archived=bool(repo.get("archived")),
                default_branch=branch,
                missing_required=missing_required,
                missing_recommended=missing_recommended,
                missing_policy_marker=missing_policy_marker,
            )
        )
    return results


def render_markdown(owner: str, rows: list[RepoAudit], has_token: bool) -> str:
    active = [row for row in rows if not row.archived]
    compliant = [row for row in active if row.compliant]
    missing = [row for row in active if not row.compliant]
    lines = [
        "# AI agent coordination audit",
        "",
        f"Owner: `{owner}`",
        (
            "Repository visibility: "
            + (
                "token-scoped (may include private)"
                if has_token
                else "public only"
            )
        ),
        f"Active repositories checked: **{len(active)}**",
        f"Required/policy compliant: **{len(compliant)}**",
        f"Missing required surfaces or policy marker: **{len(missing)}**",
        "",
        "## Required",
        "",
        "- `AGENTS.md`",
        "- `agent-context.json`",
        f"- AGENTS.md marker: `{POLICY_MARKER}`",
        "",
        "## Recommended",
        "",
        "- `.github/copilot-instructions.md`",
        "",
        "## Non-compliant active repositories",
        "",
    ]
    if not missing:
        lines.append("All active repositories checked have required surfaces and policy marker.")
    else:
        lines.extend(
            [
                "| Repository | Missing required | Missing policy marker | Missing recommended |",
                "|---|---|---|---|",
            ]
        )
        for row in missing:
            req = ", ".join(f"`{x}`" for x in row.missing_required) or "—"
            rec = ", ".join(f"`{x}`" for x in row.missing_recommended) or "—"
            marker = "yes" if row.missing_policy_marker else "—"
            lines.append(f"| `{row.full_name}` | {req} | {marker} | {rec} |")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            (
                "A missing file or marker does not authorize blind mass-editing. "
                "Inspect each repository's local architecture and tests before applying templates."
            ),
            "",
            (
                "This audit checks required-file presence and the canonical "
                "Coverage-Adaptive Reasoning v2 marker; it does not prove instruction quality."
            ),
        ]
    )
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
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(report)
    print(report)

    active_missing = [row for row in rows if not row.archived and not row.compliant]
    return 1 if args.fail_on_missing and active_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
