#!/usr/bin/env python3
"""Weekly portfolio audit — the checks that catch breakage nobody reports.

The stack is built to be found years from now, often with no users in the
meantime to report a fault. That inverts normal priorities: a defect that only
appears on a *fresh install* is the most dangerous kind, because the first
person to hit it is the first person who ever cared. This script runs the
checks that catch exactly that class of failure, on a schedule, without anyone
remembering to.

Checks
  1. version drift   — GitHub main vs the published PyPI release
  2. packaging       — PEP 639 license expression + trove classifier (a
                       combination current setuptools REFUSES to build)
  3. dependency pins — unpinned SDKs that can resolve to a breaking major
  4. repo hygiene    — description, topics, LICENSE, SECURITY.md, README

Exits non-zero when findings exist so the workflow can surface them.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

OWNER = "gabrielmahia"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# repo -> PyPI distribution name (None = not a published package)
REPOS = {
    "africa-coord-bus": "africa-coord-bus", "coord-ingest": "coord-ingest",
    "kipimo": "kipimo", "reli": "reli-cli", "mpesa-mcp": "mpesa-mcp",
    "jumuia-mcp": "jumuia-mcp", "familia-mcp": "familia-mcp",
    "ardhi-mcp": "ardhi-mcp", "mazingira-mcp": "mazingira-mcp",
    "tafsiri-mcp": "tafsiri-mcp", "offline-mcp": "offline-mcp",
    "wapimaji-mcp": "wapimaji-mcp", "civic-agent-kit": "civic-agent-kit",
    "decision-intelligence-mcp": "classical-strategy-mcp",
    "swahili-civic-nlp": None, "kenya-legal-rag": None, "shamba-ai": None,
    "afyanipoa": None, "hakiyangu": None, "kenya-3d": None,
    "kenya-nowcast": None, "nairobi-stack": None,
}

# SDKs where a major bump has already broken imports once
RISKY_UNPINNED = ("mcp", "fastmcp")


def _get(url: str, raw: bool = False, timeout: int = 30):
    headers = {"User-Agent": "portfolio-audit"}
    if TOKEN and "api.github.com" in url:
        headers["Authorization"] = f"token {TOKEN}"
        headers["Accept"] = "application/vnd.github+json"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers),
                                    timeout=timeout) as r:
            body = r.read().decode()
            return body if raw else json.loads(body)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return None


def audit() -> list[dict]:
    findings: list[dict] = []
    for repo, dist in REPOS.items():
        meta = _get(f"https://api.github.com/repos/{OWNER}/{repo}")
        if meta is None:
            findings.append({"repo": repo, "kind": "unreachable",
                             "detail": "GitHub API did not return the repo"})
            continue

        # --- hygiene -------------------------------------------------------
        contents = _get(f"https://api.github.com/repos/{OWNER}/{repo}/contents")
        names = {f["name"] for f in contents} if isinstance(contents, list) else set()
        if not (meta.get("description") or "").strip():
            findings.append({"repo": repo, "kind": "hygiene", "detail": "no description"})
        if not meta.get("topics"):
            findings.append({"repo": repo, "kind": "hygiene", "detail": "no topics (discoverability)"})
        for required in ("LICENSE", "SECURITY.md"):
            if required not in names and names:
                findings.append({"repo": repo, "kind": "hygiene", "detail": f"missing {required}"})
        if names and not any(n.lower().startswith("readme") for n in names):
            findings.append({"repo": repo, "kind": "hygiene", "detail": "missing README"})

        # --- packaging + pins + drift --------------------------------------
        pyproject = _get(
            f"https://raw.githubusercontent.com/{OWNER}/{repo}/main/pyproject.toml", raw=True)
        if not pyproject:
            continue

        has_expr = bool(re.search(r'(?m)^license\s*=\s*"[^"]+"', pyproject))
        has_classifier = "License :: OSI Approved" in pyproject
        if has_expr and has_classifier:
            findings.append({
                "repo": repo, "kind": "BUILD BREAK",
                "detail": ("PEP 639: license expression + trove classifier — current "
                           "setuptools refuses to build (sdist, wheel and editable "
                           "install all fail)")})

        # Scan ONLY the dependencies array: a bare "mcp" in `keywords` is not a
        # dependency, and an audit that cries wolf gets ignored.
        dep_block = ""
        dm = re.search(r'(?ms)^dependencies\s*=\s*\[(.*?)\]', pyproject)
        if dm:
            dep_block = dm.group(1)
        for sdk in RISKY_UNPINNED:
            if re.search(rf'"{sdk}"\s*,', dep_block) or re.search(rf'"{sdk}"\s*$',
                                                                 dep_block.strip()):
                findings.append({
                    "repo": repo, "kind": "unpinned dependency",
                    "detail": (f"'{sdk}' in dependencies with no upper bound — a major "
                               f"release can remove APIs and break fresh installs "
                               f"(mcp 2.0.0 removed mcp.server.fastmcp)")})

        m = re.search(r'(?m)^version\s*=\s*"([^"]+)"', pyproject)
        gh_version = m.group(1) if m else None
        if dist and gh_version:
            pypi = _get(f"https://pypi.org/pypi/{dist}/json")
            live = pypi["info"]["version"] if pypi else None
            if live and live != gh_version:
                findings.append({
                    "repo": repo, "kind": "version drift",
                    "detail": f"main is {gh_version}, PyPI has {live} — unpublished release"})
    return findings


def render(findings: list[dict]) -> str:
    if not findings:
        return "# Portfolio audit\n\nNo findings. All repos clean.\n"
    order = {"BUILD BREAK": 0, "version drift": 1, "unpinned dependency": 2,
             "unreachable": 3, "hygiene": 4}
    findings.sort(key=lambda f: (order.get(f["kind"], 9), f["repo"]))
    out = ["# Portfolio audit", "",
           f"{len(findings)} finding(s). Ordered by severity — a BUILD BREAK means "
           "the package cannot be installed from source by anyone who finds it.", ""]
    current = None
    for f in findings:
        if f["kind"] != current:
            current = f["kind"]
            out.append(f"## {current}")
        out.append(f"- **{f['repo']}** — {f['detail']}")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    results = audit()
    report = render(results)
    print(report)
    if (path := os.environ.get("GITHUB_STEP_SUMMARY")):
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(report)
    with open("audit_report.md", "w", encoding="utf-8") as fh:
        fh.write(report)
    sys.exit(1 if results else 0)
