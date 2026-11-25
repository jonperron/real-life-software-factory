#!/usr/bin/env python3
"""Validate data/ against the schemas and regenerate README.md.

Usage:
  python scripts/build.py            # validate + write README.md
  python scripts/build.py --check    # validate + fail if README.md is out of date
  python scripts/build.py --strict   # also fail on warnings (unknown licenses...)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMA = ROOT / "schema"
README = ROOT / "README.md"
TEMPLATE = ROOT / "scripts" / "README.template.md"
STATS = DATA / "generated" / "stats.json"

# OSI-approved licenses we expect to meet. Extend as needed (https://opensource.org/licenses).
OSI = {
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0",
    "GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only", "GPL-3.0-or-later",
    "LGPL-2.1-only", "LGPL-3.0-only", "AGPL-3.0-only", "AGPL-3.0-or-later",
    "EPL-2.0", "Unlicense", "0BSD", "Zlib", "BSL-1.0",
}

LEVELS = {
    1: ("Triage", "Agents classify, reproduce and diagnose. They do not push code to the project."),
    2: ("On-demand", "A human assigns work; agents open PRs; a human merges."),
    3: ("Pipeline", "Work flows from intake to PR without a human trigger; a human gates the merge."),
    4: ("Lights-out", "Agents merge without human review."),
}
LEVEL_BADGE = {1: "L1 · Triage", 2: "L2 · On-demand", 3: "L3 · Pipeline", 4: "L4 · Lights-out"}
FACTORY_CODE = {"open": "open", "partial": "partial", "closed": "closed", None: "unknown"}


class StrLoader(yaml.SafeLoader):
    """SafeLoader that keeps dates as plain strings (2026-08-12 stays '2026-08-12')."""


StrLoader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load(kind: str) -> list[dict]:
    items = []
    for path in sorted((DATA / kind).glob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            doc = yaml.load(fh, Loader=StrLoader)
        doc["_file"] = str(path.relative_to(ROOT))
        items.append(doc)
    return items


def validate(kind: str, items: list[dict]) -> tuple[list[str], list[str]]:
    schema = json.loads((SCHEMA / f"{kind}.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors, warnings = [], []
    seen = set()
    for item in items:
        f = item.pop("_file")
        for err in validator.iter_errors(item):
            loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
            errors.append(f"{f}: {loc}: {err.message}")
        key = item.get("repo") or item.get("url")
        if key in seen:
            errors.append(f"{f}: duplicate entry {key}")
        seen.add(key)
        lic = item.get("license")
        if lic == "unknown":
            warnings.append(f"{f}: license is 'unknown' (refresh_stats.py fills it from GitHub)")
        elif lic and lic not in OSI:
            errors.append(f"{f}: license '{lic}' is not in the OSI allowlist")
        if kind == "project":
            fac = item.get("factory", {})
            if fac.get("level") == 4 and "merge" in fac.get("human_gates", []):
                errors.append(f"{f}: level 4 (lights-out) cannot have a 'merge' human gate")
            if fac.get("level") == 1 and "implement" in fac.get("stages", []) and "merge" not in fac.get("human_gates", []):
                warnings.append(f"{f}: level 1 with 'implement' stage but no merge gate")
        item["_file"] = f
    return errors, warnings


def stars(stats: dict, repo: str | None) -> str:
    s = stats.get(repo or "", {})
    n = s.get("stars")
    if n is None:
        return "–"
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def effective_license(stats: dict, item: dict) -> str:
    lic = item.get("license")
    if lic == "unknown":
        lic = stats.get(item.get("repo") or "", {}).get("license") or "unknown"
    return lic


def gh_anchor(heading: str) -> str:
    """Reproduce GitHub's heading slug: lowercase, drop punctuation, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ").strip()


def render(projects: list[dict], tools: list[dict], stats: dict) -> str:
    projects = sorted(projects, key=lambda p: (-p["factory"]["level"], p["status"] != "production", p["name"].lower()))
    tools = sorted(tools, key=lambda t: (t["category"], t["name"].lower()))

    levels = "\n".join(
        f"| **L{n}** | {name} | {desc} | {sum(1 for p in projects if p['factory']['level'] == n)} |"
        for n, (name, desc) in LEVELS.items()
    )

    rows = []
    for p in projects:
        fac = p["factory"]
        anchor = gh_anchor(p["repo"])
        exp = " 🧪" if p.get("status") == "experimental" else ""
        metric = p.get("metrics", [{}])[0] if p.get("metrics") else {}
        metric_txt = (f"**{md_escape(metric['value'])}**<br><sub>{md_escape(metric['label'])} "
                      f"({metric['as_of']})</sub>") if metric else "–"
        rows.append(
            f"| [{p['name']}](#{anchor}){exp} | {LEVEL_BADGE[fac['level']]} | "
            f"{', '.join(fac['stages'])} | {', '.join(fac['human_gates'])} | "
            f"{FACTORY_CODE[fac.get('factory_code')]} | {metric_txt} | {stars(stats, p['repo'])} |"
        )

    details = []
    for p in projects:
        fac = p["factory"]
        anchor_title = p["repo"]
        lines = [f"### {anchor_title}", ""]
        lines.append(f"**{p['name']}** · {LEVEL_BADGE[fac['level']]} · license `{effective_license(stats, p)}`"
                     + (" · 🧪 experimental" if p.get("status") == "experimental" else ""))
        lines += ["", p["summary"].strip(), ""]
        if fac.get("name"):
            code = FACTORY_CODE[fac.get("factory_code")]
            repo = f" ([{fac['factory_repo']}](https://github.com/{fac['factory_repo']}))" if fac.get("factory_repo") else ""
            lines.append(f"- **Factory:** {fac['name']} — code {code}{repo}" + (f", since {fac['since']}" if fac.get("since") else ""))
        stack = fac.get("stack") or {}
        if stack:
            lines.append("- **Stack:** " + "; ".join(f"{k}: {v}" for k, v in stack.items()))
        s = stats.get(p["repo"], {})
        if fac.get("evidence_query"):
            q = fac["evidence_query"]
            url = f"https://github.com/{p['repo']}/issues?q={urllib.parse.quote_plus(q)}"
            counted = f" — **{s['evidence_total']}** found" if s.get("evidence_total") is not None else ""
            lines.append(f"- **Check it yourself:** [`{q}`]({url}){counted}")
        for m in p.get("metrics", []):
            lines.append(f"- {m['label']}: **{m['value']}** ({m['as_of']}, [source]({m['source']}))")
        if p.get("notes"):
            lines.append(f"- _Note:_ {p['notes'].strip()}")
        src = ", ".join(f"[{x['title']}]({x['url']})" for x in p["sources"])
        lines.append(f"- **Sources:** {src}")
        details.append("\n".join(lines))

    trows = []
    for t in tools:
        used = ", ".join(t.get("used_by", [])) or "–"
        trows.append(
            f"| [{t['name']}]({t['url']}) | {t['category']} | `{effective_license(stats, t)}` | "
            f"{md_escape(t['summary'])} | {used} | {stars(stats, t.get('repo'))} |"
        )

    updated = stats.get("_updated", "never (run scripts/refresh_stats.py)")
    tpl = TEMPLATE.read_text(encoding="utf-8")
    return (tpl
            .replace("{{LEVELS}}", levels)
            .replace("{{PROJECT_ROWS}}", "\n".join(rows))
            .replace("{{PROJECT_DETAILS}}", "\n\n".join(details))
            .replace("{{TOOL_ROWS}}", "\n".join(trows))
            .replace("{{COUNT_PROJECTS}}", str(len(projects)))
            .replace("{{COUNT_TOOLS}}", str(len(tools)))
            .replace("{{STATS_UPDATED}}", updated))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    projects, tools = load("projects"), load("tools")
    e1, w1 = validate("project", projects)
    e2, w2 = validate("tool", tools)
    errors, warnings = e1 + e2, w1 + w2
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if errors or (args.strict and warnings):
        return 1

    stats = json.loads(STATS.read_text(encoding="utf-8")) if STATS.exists() else {}
    out = render(projects, tools, stats)
    if args.check:
        if not README.exists() or README.read_text(encoding="utf-8") != out:
            print("README.md is out of date: run `python scripts/build.py` and commit.", file=sys.stderr)
            return 1
        print("README.md is up to date.")
        return 0
    README.write_text(out, encoding="utf-8")
    print(f"README.md written: {len(projects)} projects, {len(tools)} tools.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
