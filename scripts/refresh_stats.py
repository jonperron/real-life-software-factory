#!/usr/bin/env python3
"""Fetch live GitHub data for every entry and write data/generated/stats.json.

For each repo: stars, SPDX license, archived flag, last push.
For projects with factory.evidence_query: number of matching issues/PRs
(the query is run with `repo:<owner/name>` prepended).

Needs GITHUB_TOKEN (the Actions token is enough). Standard library only.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "generated" / "stats.json"
API = "https://api.github.com"
STALE_DAYS = 180


def gh(path: str, token: str) -> dict | None:
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "factory-floor-stats",
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (403, 429) and attempt < 2:
                time.sleep(30)
                continue
            raise
    return None


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is required", file=sys.stderr)
        return 1

    entries = []
    for kind in ("projects", "tools"):
        for path in sorted((ROOT / "data" / kind).glob("*.yaml")):
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            if doc.get("repo"):
                entries.append((path, doc))

    stats: dict = {}
    problems = []
    now = dt.datetime.now(dt.timezone.utc)
    for path, doc in entries:
        repo = doc["repo"]
        info = gh(f"/repos/{repo}", token)
        if info is None:
            problems.append(f"{path.name}: {repo} not found")
            continue
        if info.get("full_name", "").lower() != repo.lower():
            problems.append(f"{path.name}: {repo} redirects to {info.get('full_name')} — update the YAML")
        pushed = info.get("pushed_at")
        s = {
            "stars": info.get("stargazers_count"),
            "license": (info.get("license") or {}).get("spdx_id"),
            "archived": info.get("archived"),
            "pushed_at": pushed,
        }
        if info.get("archived"):
            problems.append(f"{path.name}: {repo} is archived")
        if pushed and (now - dt.datetime.fromisoformat(pushed.replace("Z", "+00:00"))).days > STALE_DAYS:
            problems.append(f"{path.name}: {repo} has no push for {STALE_DAYS}+ days")
        q = (doc.get("factory") or {}).get("evidence_query")
        if q:
            res = gh("/search/issues?per_page=1&q=" + urllib.parse.quote(f"repo:{repo} {q}"), token)
            s["evidence_total"] = res.get("total_count") if res else None
            time.sleep(2.5)  # search API: 30 req/min
        stats[repo] = s

    stats["_updated"] = now.strftime("%Y-%m-%d")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} for {len(stats) - 1} repos.")
    for p in problems:
        print(f"::warning::{p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
