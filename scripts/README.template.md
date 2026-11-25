<!-- GENERATED FILE — edit data/*.yaml or scripts/README.template.md, then run `python scripts/build.py`. -->

# Factory Floor

**Open source projects that run an AI software factory in production — with receipts.**

Everyone is writing about "software factories": agents that take work from an issue to a reviewed pull request. This list doesn't collect vendors or demos. It tracks **real, public open source repositories** where you can see the factory working: which stages are automated, where humans still gate the work, what it changed, and a GitHub query to check the claims yourself.

{{COUNT_PROJECTS}} projects · {{COUNT_TOOLS}} building blocks · live GitHub stats refreshed {{STATS_UPDATED}}

- [Factory levels](#factory-levels)
- [Projects](#projects)
- [Project details](#project-details)
- [Building blocks](#building-blocks)
- [Inclusion criteria](#inclusion-criteria)
- [Contributing](CONTRIBUTING.md)

## Factory levels

Every project is graded on what its agents are actually allowed to do, not on what the vendor claims.

| Level | Name | What it means | Projects |
|---|---|---|---|
{{LEVELS}}

## Projects

| Project | Level | Automated stages | Human gates | Factory code | Headline metric | ⭐ |
|---|---|---|---|---|---|---|
{{PROJECT_ROWS}}

🧪 = experimental. "Factory code" says whether the factory itself is published (open), partly published (partial) or internal (closed).

## Project details

{{PROJECT_DETAILS}}

## Building blocks

Open source pieces you can use to build your own factory. Listed only if they come from, or are used by, a real factory.

| Name | Category | License | What it does | Used by | ⭐ |
|---|---|---|---|---|---|
{{TOOL_ROWS}}

## Inclusion criteria

A project is listed when **all** of these are true:

1. **Open source:** the repository is public under an OSI-approved license. Source-available projects go to the watchlist in [CONTRIBUTING.md](CONTRIBUTING.md#watchlist).
2. **Factory, not autocomplete:** agents carry out at least one full stage of delivery (triage, reproduce, implement, review, backport, release...) on the project's own backlog. One-off agent PRs from outside contributors don't count.
3. **Visible:** the factory's work can be seen in the repo (bot accounts, labels, PRs, workflows) or in a first-party write-up by the maintainers.
4. **Sourced:** every metric and claim links to a primary source with a date. No source, no line.
5. **Alive:** the repo has been pushed to in the last 180 days (CI checks this every week).

## License

[CC0 1.0](LICENSE) — the data is yours to reuse.
