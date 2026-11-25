<!-- GENERATED FILE — edit data/*.yaml or scripts/README.template.md, then run `python scripts/build.py`. -->

# Factory Floor

**Open source projects that run an AI software factory in production — with receipts.**

Everyone is writing about "software factories": agents that take work from an issue to a reviewed pull request. This list doesn't collect vendors or demos. It tracks **real, public open source repositories** where you can see the factory working: which stages are automated, where humans still gate the work, what it changed, and a GitHub query to check the claims yourself.

11 projects · 10 building blocks · live GitHub stats refreshed 2026-11-25

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
| **L1** | Triage | Agents classify, reproduce and diagnose. They do not push code to the project. | 2 |
| **L2** | On-demand | A human assigns work; agents open PRs; a human merges. | 3 |
| **L3** | Pipeline | Work flows from intake to PR without a human trigger; a human gates the merge. | 6 |
| **L4** | Lights-out | Agents merge without human review. | 0 |

## Projects

| Project | Level | Automated stages | Human gates | Factory code | Headline metric | ⭐ |
|---|---|---|---|---|---|---|
| [Astro](#withastroastro) | L3 · Pipeline | intake, triage, reproduce, diagnose, implement | merge | open | **200+ → ~30 (−85%)**<br><sub>Open issues (2026-08)</sub> | 64.2k |
| [Flue](#withastroflue) | L3 · Pipeline | intake, plan, implement, review | decision, merge | open | – | 8.7k |
| [GitHub Agentic Workflows (gh-aw)](#githubgh-aw) | L3 · Pipeline | intake, triage, implement, review, release, monitor | merge | open | **72 opened, 48 merged (72.7%)**<br><sub>Copilot agent PRs in 24h (daily report) (2026-08-05)</sub> | 5.7k |
| [Mastra](#mastra-aimastra) | L3 · Pipeline | intake, triage, reproduce, plan, implement, review, docs | decision, merge | open | **25–35%**<br><sub>Share of PRs automated by Factory (since July alpha) (2026-09)</sub> | 29.8k |
| [Vercel AI SDK](#vercelai) | L3 · Pipeline | intake, triage, reproduce, implement, review, backport, docs | merge | partial | **25–35%**<br><sub>Share of weekly merged PRs authored by the factory (2026-08)</sub> | 28.2k |
| [Warp](#warpdotdevwarp) | L3 · Pipeline | intake, triage, plan, implement, review, community | spec, merge | closed | – | 66.1k |
| [.NET runtime](#dotnetruntime) | L2 · On-demand | implement, review, test | trigger, merge | closed | **878 opened, 535 merged (67.9% success)**<br><sub>CCA PRs over ten months (2026-03)</sub> | 18.5k |
| [career-ops](#career-ops-hqcareer-ops) | L2 · On-demand | triage, review, test, release, community, docs | decision, merge, release, public-comms | closed | **16 PRs merged, ~25 issues triaged, 1 release**<br><sub>In one documented day (2026-07-02)</sub> | 84.8k |
| [EmDash](#emdash-cmsemdash) 🧪 | L2 · On-demand | reproduce, diagnose, implement | trigger, merge | open | – | 14.6k |
| [Bootstrap](#twbsbootstrap) | L1 · Triage | triage, reproduce, diagnose, implement | decision, merge, public-comms | unknown | **500+ → 230**<br><sub>Open issues + PRs (2026-10)</sub> | 175.1k |
| [Metabase](#metabasemetabase) | L1 · Triage | triage, reproduce | trigger, decision | closed | – | 50.5k |

🧪 = experimental. "Factory code" says whether the factory itself is published (open), partly published (partial) or internal (closed).

## Project details

### withastro/astro

**Astro** · L3 · Pipeline · license `MIT`

Isolated agents in GitHub Actions reproduce, diagnose and propose fixes for every new issue, passing context through a report.md; reporters verify the bot's fix before maintainers review it.

- **Factory:** Astro triage bot (triagebot-action + Flue) — code open ([withastro/triagebot-action](https://github.com/withastro/triagebot-action))
- **Stack:** orchestration: Flue, GitHub Actions; models: Cloudflare Workers AI (Kimi K2.6) for verification; Anthropic/OpenAI pluggable
- **Check it yourself:** [`is:issue label:"triage: fix verified"`](https://github.com/withastro/astro/issues?q=is%3Aissue+label%3A%22triage%3A+fix+verified%22) — **0** found
- Open issues: **200+ → ~30 (−85%)** (2026-08, [source](https://infoq.com/news/2026/08/cloudflare-astro-ai-agents))
- _Note:_ Fred Schott calls "fix" the hardest and least essential stage: triage first, hand a report to a human.
- **Sources:** [How we built a software factory to drive Astro's GitHub issue count to zero (Cloudflare)](https://blog.cloudflare.com/astro-issue-triage/), [Cloudflare Cuts Astro GitHub Issues by 85% with AI Agents (InfoQ)](https://infoq.com/news/2026/08/cloudflare-astro-ai-agents), [Cloudflare Astro triage bot (The New Stack)](https://thenewstack.io/cloudflare-astro-triage-bot/)

### withastro/flue

**Flue** · L3 · Pipeline · license `Apache-2.0`

Every external PR is auto-closed and turned into an issue or discussion. Once a maintainer decides, agents handle research, design, implementation and first review.

- _Note:_ Explicit goal is to prevent "drive-by AI slop PRs".
- **Sources:** [Flue contributing guide](https://github.com/withastro/flue?tab=contributing-ov-file), [PRs NOT Welcome (Latent Space)](https://www.latent.space/p/pr-not-welcome)

### github/gh-aw

**GitHub Agentic Workflows (gh-aw)** · L3 · Pipeline · license `MIT`

"Peli's Agent Factory": the repo runs its own agentic workflows on itself — Issue Monster feeds issues one at a time to Copilot Coding Agent, Mergefest keeps PR branches current, and a daily agent publishes PR analytics.

- **Factory:** Peli's Agent Factory — code open ([github/gh-aw](https://github.com/github/gh-aw))
- **Stack:** orchestration: GitHub Actions agentic workflows; agents: Copilot Coding Agent, copilot-pull-request-reviewer
- **Check it yourself:** [`is:pr head:copilot/`](https://github.com/github/gh-aw/issues?q=is%3Apr+head%3Acopilot%2F)
- Copilot agent PRs in 24h (daily report): **72 opened, 48 merged (72.7%)** (2026-08-05, [source](https://github.com/github/gh-aw/discussions/50669))
- **Sources:** [Meet the Workflows: Issue & PR Management](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-issue-management/), [Copilot Agent PR Analysis 2026-08-05](https://github.com/github/gh-aw/discussions/50669)

### mastra-ai/mastra

**Mastra** · L3 · Pipeline · license `Apache-2.0`

Mastra dogfoods its own open source Factory: GitHub, Linear and Slack feed a board (Intake → Triage → Planning → Build → Review → Done) where each stage runs in manual or auto mode.

- **Factory:** Mastra Factory — code open, since 2026-07
- **Stack:** orchestration: Mastra Factory (rules engine over "work" items); sandbox: Mastra platform cloud sandboxes
- Share of PRs automated by Factory (since July alpha): **25–35%** (2026-09, [source](https://mastra.ai/blog/announcing-mastra-factory-beta))
- Share of issues closed by Factory: **50–60%** (2026-09, [source](https://mastra.ai/blog/announcing-mastra-factory-beta))
- _Note:_ Full auto mode was dropped after bursty backlog imports produced hard-to-review work; stages are now configurable. Code under ee/ directories is source-available, the rest is Apache-2.0.
- **Sources:** [Announcing Mastra Factory Beta](https://mastra.ai/blog/announcing-mastra-factory-beta)

### vercel/ai

**Vercel AI SDK** · L3 · Pipeline · license `Apache-2.0`

Specialised agents classify every incoming issue, then reproduce and fix bugs, implement features, review PRs, backport to older majors and update docs. A maintainer merges every change.

- **Factory:** ai-sdk-factory — code partial, since 2026-07
- **Stack:** orchestration: Vercel Functions + Vercel Queues, GitHub webhooks; sandbox: Vercel Sandbox (per-task secrets)
- **Check it yourself:** [`is:pr author:app/ai-sdk-factory`](https://github.com/vercel/ai/issues?q=is%3Apr+author%3Aapp%2Fai-sdk-factory) — **2228** found
- Share of weekly merged PRs authored by the factory: **25–35%** (2026-08, [source](https://vercel.com/blog/building-a-software-factory-for-ai-sdk))
- Share of closed issues closed by the factory: **70–80%** (2026-08, [source](https://vercel.com/blog/building-a-software-factory-for-ai-sdk))
- Open issues: **1,022 → 844 (late June → early Aug)** (2026-08, [source](https://vercel.com/blog/building-a-software-factory-for-ai-sdk))
- _Note:_ The production factory is not published; Vercel links a deployable open source four-agent template (see tools/eve-software-factory).
- **Sources:** [Building a software factory for AI SDK (Vercel)](https://vercel.com/blog/building-a-software-factory-for-ai-sdk), [PRs NOT Welcome (Latent Space)](https://www.latent.space/p/pr-not-welcome)

### warpdotdev/warp

**Warp** · L3 · Pipeline · license `AGPL-3.0-only`

Open-sourced in April 2026 with an agent-first contribution model: Oz cloud agents triage issues, ask clarifying questions, write specs and code and open PRs in public; the community shapes specs and the Warp team reviews and ships.

- **Factory:** Oz — code closed, since 2026-04
- **Stack:** orchestration: Oz (proprietary); models: GPT models (OpenAI is founding sponsor of the repo)
- _Note:_ Client is open source; server, Warp Drive backend and Oz are proprietary. Some crates are MIT-licensed; the rest is AGPL-3.0.
- **Sources:** [Warp is now open-source (Zach Lloyd)](https://warp.dev/blog/warp-is-now-open-source), [Warp open-sources its agentic development environment (press release)](https://www.warp.dev/newsroom/2026/4/28/warp-open-sources-its-agentic-development-environment), [Live agent dashboard](https://build.warp.dev)

### dotnet/runtime

**.NET runtime** · L2 · On-demand · license `MIT`

Team members assign scoped issues to GitHub Copilot Coding Agent, which opens PRs; every PR (human, agent or external) gets automated AI review. The best public data set on agent PRs in a critical codebase.

- **Factory:** Copilot Coding Agent (CCA) — code closed, since 2025-05
- **Stack:** agents: GitHub Copilot Coding Agent
- **Check it yourself:** [`is:pr head:copilot/`](https://github.com/dotnet/runtime/issues?q=is%3Apr+head%3Acopilot%2F) — **1842** found
- CCA PRs over ten months: **878 opened, 535 merged (67.9% success)** (2026-03, [source](https://devblogs.microsoft.com/dotnet/ten-months-with-cca-in-dotnet-runtime/))
- Revert rate of merged CCA PRs: **0.6%** (2026-03, [source](https://startdebugging.net/2026/03/copilot-coding-agent-dotnet-runtime-ten-months-data/))
- **Sources:** [Ten Months with Copilot Coding Agent in dotnet/runtime (Stephen Toub)](https://devblogs.microsoft.com/dotnet/ten-months-with-cca-in-dotnet-runtime/)

### career-ops-hq/career-ops

**career-ops** · L2 · On-demand · license `MIT`

A solo maintainer runs an 80k-star repo with a fleet of Claude Code agents: maintainer/orchestrator, ephemeral verifiers in worktrees, dogfood, Discord and FAQ agents, plus Codex as cross-model auditor on sensitive PRs.

- **Factory:** Agentic maintenance fleet — code closed
- **Stack:** agents: Claude Code fleet; OpenAI Codex as independent auditor
- In one documented day: **16 PRs merged, ~25 issues triaged, 1 release** (2026-07-02, [source](https://santifer.io/ai-agent-fleet))
- Merged PRs since launch (all authors): **3,506** (2026-11-12, [source](https://santifer.io/ai-agent-fleet))
- _Note:_ Repo moved from santifer/career-ops to career-ops-hq/career-ops.
- **Sources:** [Agentic maintenance: how I run a 73,000-star open source repo with a fleet of AI agents](https://santifer.io/ai-agent-fleet), [career-ops CONTRIBUTING.md](https://raw.githubusercontent.com/santifer/career-ops/master/CONTRIBUTING.md)

### emdash-cms/emdash

**EmDash** · L2 · On-demand · license `MIT` · 🧪 experimental

Flue-powered investigation bot started by a maintainer label (bot:repro): it reproduces the issue, labels the outcome, and can push a fix and ask the reporter to verify. Modelled on Astro's setup.

- **Factory:** Investigate bot — code open
- **Stack:** orchestration: Flue in GitHub Actions
- **Check it yourself:** [`is:issue label:triage/verified`](https://github.com/emdash-cms/emdash/issues?q=is%3Aissue+label%3Atriage%2Fverified) — **57** found
- **Sources:** [.flue/README.md](https://cdn.jsdelivr.net/gh/emdash-cms/emdash@HEAD/.flue/README.md), [Design rationale (PR](https://github.com/emdash-cms/emdash/pull/1090)

### twbs/bootstrap

**Bootstrap** · L1 · Triage · license `MIT`

Claude Code agents analyse every open issue and PR, try to reproduce, and prepare draft answers and fix branches in a separate repo. Agents cannot comment, push or open PRs on Bootstrap itself; maintainers act.

- **Factory:** twbs/triage — code unknown
- **Stack:** agents: Claude Code background agents
- Open issues + PRs: **500+ → 230** (2026-10, [source](https://blog.getbootstrap.com/2026/10/15/triaging-bootstrap-with-claude-agents/))
- Labels applied by agents (allowlisted): **410 across 198 items** (2026-10, [source](https://blog.getbootstrap.com/2026/10/15/triaging-bootstrap-with-claude-agents/))
- _Note:_ Good reference for prompt-injection hygiene: contributor content is untrusted, no contributor code is run, suspicious items held for manual review.
- **Sources:** [Triaging open source with agents (Bootstrap blog)](https://blog.getbootstrap.com/2026/10/15/triaging-bootstrap-with-claude-agents/)

### metabase/metabase

**Metabase** · L1 · Triage · license `AGPL-3.0-only`

Repro-Bot is an issue triage agent that attempts to reproduce public GitHub issues. It is run by a human on purpose, to keep poisoned issue content from driving the agent.

- **Factory:** Repro-Bot — code closed, since 2026-04
- _Note:_ Enterprise directories are under a commercial license; core is AGPL.
- **Sources:** [Meet Repro-Bot, our GitHub issue triage agent (Metabase)](https://www.metabase.com/blog/reprobot-github-issue-triage-agent)

## Building blocks

Open source pieces you can use to build your own factory. Listed only if they come from, or are used by, a real factory.

| Name | Category | License | What it does | Used by | ⭐ |
|---|---|---|---|---|---|
| [CXDB](https://github.com/strongdm/cxdb) | context-store | `Apache-2.0` | Self-hosted context store for agents from StrongDM's factory: turn DAG, blob deduplication, dynamic types and visual debugging. | – | 527 |
| [AgentFactory](https://github.com/supaku/agentfactory) | factory-platform | `MIT` | TypeScript orchestrator for fleets of coding agents (Claude and others) driven from Linear: multi-agent fleet management for a software factory. | – | 66 |
| [Mastra Factory](https://factory.mastra.ai/) | factory-platform | `unknown` | Open source, configurable factory: connect GitHub, Linear and Slack, define how work moves through stages, run each stage in manual or auto mode. Scaffold with `npm create factory@latest`. | mastra-ai/mastra | – |
| [Attractor](https://github.com/strongdm/attractor) | spec | `Apache-2.0` | StrongDM's non-interactive coding agent published as natural-language specs (NLSpecs) that your own agent implements. Reference design behind the "lights-out" software factory; several community implementations exist. | – | 1.4k |
| [eve software factory template (Vercel)](https://vercel.fyi/eve-software-factory) | template | `unknown` | One-click deployable open source factory with four agents (Classifier, Analyzer, Implementer, Reviewer), derived from the AI SDK team's setup. | – | – |
| [software-factory (Jim Bennett / Arize)](https://github.com/jimbobbennett/software-factory) | template | `MIT` | Small reference factory (spec, build, review, release agents with CI and a merge gate) that also evaluates its own prompts; builds the ship-it-card demo app. | – | 2 |
| [triagebot-action](https://github.com/withastro/triagebot-action) | triage | `unknown` | GitHub Action extracted from Astro's factory: agents reproduce, diagnose and verify issues before a human sees them, driven by a project-specific triage skill in .agents/skills/triage. | withastro/astro | 234 |
| [Fabro](https://github.com/fabro-sh/fabro) | workflow-engine | `MIT` | Rust implementation of the Attractor ideas: processes as Graphviz DOT graphs with branching, loops and human approval gates, model routing via stylesheets, cloud sandboxes. | – | 1.9k |
| [Flue](https://github.com/withastro/flue) | workflow-engine | `Apache-2.0` | Framework for durable agent workflows that grew out of Astro's auto-triage; connects agents to GitHub, Slack and more. | withastro/astro, withastro/flue, emdash-cms/emdash | 8.7k |
| [GitHub Agentic Workflows](https://github.com/github/gh-aw) | workflow-engine | `MIT` | Agentic workflows written in Markdown and run on GitHub Actions; the githubnext/agentics repo ships ready-made workflows (Issue Arborist, Sub Issue Closer, ...). | github/gh-aw | 5.7k |

## Inclusion criteria

A project is listed when **all** of these are true:

1. **Open source:** the repository is public under an OSI-approved license. Source-available projects go to the watchlist in [CONTRIBUTING.md](CONTRIBUTING.md#watchlist).
2. **Factory, not autocomplete:** agents carry out at least one full stage of delivery (triage, reproduce, implement, review, backport, release...) on the project's own backlog. One-off agent PRs from outside contributors don't count.
3. **Visible:** the factory's work can be seen in the repo (bot accounts, labels, PRs, workflows) or in a first-party write-up by the maintainers.
4. **Sourced:** every metric and claim links to a primary source with a date. No source, no line.
5. **Alive:** the repo has been pushed to in the last 180 days (CI checks this every week).

## License

[CC0 1.0](LICENSE) — the data is yours to reuse.
