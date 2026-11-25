# Contributing

Thanks for helping map how open source projects really use agents. The bar is **evidence**, not enthusiasm.

## Add a project

1. Check the [inclusion criteria](README.md#inclusion-criteria).
2. Copy an existing file in `data/projects/` (for example `vercel-ai-sdk.yaml`) to `data/projects/<short-name>.yaml`.
3. Fill it in. The schema is in [`schema/project.schema.json`](schema/project.schema.json). Required: `name`, `repo`, `license`, `summary`, `factory.level`, `factory.stages`, `factory.human_gates`, `sources`.
4. Run locally:
   ```bash
   pip install pyyaml jsonschema
   python scripts/build.py
   ```
5. Commit both your YAML file and the regenerated `README.md`, then open a PR.

Building blocks (`data/tools/`) follow the same flow with [`schema/tool.schema.json`](schema/tool.schema.json).

## Rules for data

- **Every metric has a source and a date.** Use the maintainers' own write-up when possible, not a vendor's case study about them.
- **Grade conservatively.** Pick the level the evidence proves, not the one the blog post hints at:

  | Level | Proof needed |
  |---|---|
  | L1 · Triage | Agents label, reproduce or diagnose issues; no agent code lands without a human rewriting it. |
  | L2 · On-demand | Agent-authored PRs are merged, but a human starts each task (assigns an issue, applies a label). |
  | L3 · Pipeline | New work reaches an agent without a human trigger; a human still approves merges. |
  | L4 · Lights-out | Agent PRs are merged without human review. |

- **Add an `evidence_query`** when you can: GitHub search qualifiers (without `repo:`) that list the factory's PRs or issues, such as `is:pr author:app/my-bot`. CI counts the results weekly, so readers can check the claim.
- **Leave `license: unknown`** if you're unsure; the weekly job reads the SPDX id from GitHub.
- Write in English, neutral tone. No marketing adjectives.

## Watchlist

Interesting, but not listed yet. Open a PR with a source if that changes.

- **tldraw** (`tldraw/tldraw`): auto-closes external PRs since January 2026 and leans on agents internally, but it is source-available (not OSI) and the agent setup isn't documented.
- **Prisma**: runs an internal factory (Gremlin, Gizmo, Sherlog on Mastra), but its write-ups don't say which public repos it works on.
- **StrongDM**: the reference "lights-out" factory; its components are open (see Attractor, CXDB) but the factory runs on internal code.

## Automation

| Workflow | When | What |
|---|---|---|
| `validate.yml` | every PR | schema + rules, README up to date, link check |
| `refresh.yml` | weekly + manual | refreshes stars/licenses/evidence counts, flags archived or stale repos, opens a PR |
