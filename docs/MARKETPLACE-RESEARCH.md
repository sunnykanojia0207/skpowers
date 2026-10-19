# Best Skills and MCP Servers by Category

**Reviewed:** 2026-10-19, across [SkillsMP](https://skillsmp.com/), [MCP Market](https://mcpmarket.com/), [AI Skill Market](https://aiskill.market/) and [SkillsMK](https://skillsmk.com/).
**Method:** the marketplaces were used for discovery only. Every pick below was checked against its upstream repository through the GitHub API (license file, stars, last push, file tree, SKILL.md content). Nothing was installed or executed. Facts are as of the review date; re-check before installing.

## How to read this

- **One pick per category, at most one runner-up.** Install only the categories your project needs, and only the named skill folders, not whole packs.
- **Install project-locally** so the skill lands in `.agents/skills/`, then run `python scripts/sync_toolkit.py` so Claude Code gets it too. Preview every install with `--list` first.
- **"Scripts"** means the skill ships executable files or tells the agent to run commands. Read those before installing.

## Workflow (pick exactly one)

| Pick | Why |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) (MIT) | Highest install counts on every marketplace that shows them (`systematic-debugging` alone ~173K on AI Skill Market); native installs for Claude Code, Codex, Cursor, Gemini CLI, Copilot CLI and OpenCode; no reviewer found a better debugging or code-review skill. |
| or [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT) | More explicit spec → ship lifecycle with security, CI/CD and observability skills. Choose it if you prefer that structure; do not run both. |

## Best skill per category

| Category | Best pick | Runner-up | Notes |
|---|---|---|---|
| **Native iOS (SwiftUI)** | [twostraws/SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill) → `swiftui-pro`. MIT, 6.2k★, pushed 2026-10-16, Paul Hudson. Docs only. | [AvdLee/SwiftUI-Agent-Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill) → `swiftui-expert-skill`. MIT, 3.7k★. | Runner-up ships Python scripts that run `xctrace` / parse Instruments traces; review first. |
| **Native Android (Kotlin/Compose)** | [android/skills](https://github.com/android/skills) (Google, official). Apache-2.0, 8.9k★, pushed 2026-10-16. Pick individual skills, e.g. `jetpack-compose-performance`, `navigation-3`, `testing-setup`, `edge-to-edge`, `android-intent-security`. | [Kotlin/kotlin-agent-skills](https://github.com/Kotlin/kotlin-agent-skills) (JetBrains, official). Apache-2.0. Tooling/migration only. | **Do not install `android-cli`** (pipes a remote installer into the shell and installs other skills) or `play-policy-insights` (ships a scraper). Install needs the Android CLI; `npx skills` support is unverified. |
| **React Native** | [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills) → `react-native-best-practices`. MIT, 1.7k★. | `expo/skills` (already in the guide) | Pairs with Expo skills. |
| **Testing (Playwright, flaky tests)** | [currents-dev/playwright-best-practices-skill](https://github.com/currents-dev/playwright-best-practices-skill). MIT, vendor (Currents), pushed 2026-07-21. Docs only. | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) bundled skill. Apache-2.0, 14.4k★. | Runner-up needs a global CLI (`npm install -g @playwright/cli`). Microsoft positions the CLI as lower-token than Playwright MCP for coding agents. |
| **Security review** | [trailofbits/skills](https://github.com/trailofbits/skills) (already in the guide) | [getsentry/skills](https://github.com/getsentry/skills) → `security-review`. Apache-2.0, vendor, no scripts. | getsentry's repo says it is built for Sentry staff: cherry-pick `security-review`, `find-bugs`, `code-review` only. |
| **Threat modeling** | [trailofbits/skills-curated](https://github.com/trailofbits/skills-curated) (already in the guide) | [wshobson/agents](https://github.com/wshobson/agents) → `stride-analysis-patterns`, `threat-mitigation-mapping` | |
| **Debugging / code review** | Your workflow pack (Superpowers `systematic-debugging`, `requesting-code-review`) | getsentry `find-bugs` | No reviewer found a better standalone option. |
| **REST / OpenAPI design** | [wshobson/agents](https://github.com/wshobson/agents) → `api-design-principles`, `openapi-spec-generation`. MIT, 41k★, pushed 2026-10-19. | — | wshobson is a 185-skill, 94-plugin library: install single skills (`npx skills add wshobson/agents --skill <name>`), never the plugins, which add agents, commands and hooks. |
| **GraphQL** | [apollographql/skills](https://github.com/apollographql/skills) → `graphql-schema`, `graphql-operations`. MIT, vendor. | — | Avoid `graphos-factory` in the same repo (many shell scripts). |
| **Postgres / migrations** | [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) → `postgres`, `design-postgres-tables`, `postgres-database-migration`. Apache-2.0, vendor, 1.9k★. | `supabase/agent-skills` if you use Supabase | PlanetScale's `database-skills` was rejected as a pick: it fetches references from raw GitHub URLs and steers toward its own hosting. |
| **Docker** | [docker/skills](https://github.com/docker/skills) → `docker-build-strategies`, `docker-compose-patterns`, `docker-destructive-guardrails`. Apache-2.0, official, pushed 2026-10-19. | — | `docker-docs` fetches remote docs (optional). |
| **Kubernetes / CI / observability** | wshobson → `github-actions-templates`, `k8s-manifest-generator`, `slo-implementation`, `distributed-tracing`, `prometheus-configuration` | [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) → `terraform-style-guide`, `terraform-test` (MPL-2.0, official) for Terraform users | Some wshobson skills ship scripts (e.g. `helm-chart-scaffolding`); not every one was audited. |
| **AI apps: evals** | [ai-evals-course/evals-skills](https://github.com/ai-evals-course/evals-skills) → `eval-audit`, `evaluate-rag`, `write-judge-prompt`, `error-discovery`. Apache-2.0, 1.5k★, Hamel Husain & Shreya Shankar. No scripts. | [promptfoo](https://github.com/promptfoo/promptfoo) `promptfoo-evals` (MIT); no documented install | The old `hamelsmu/evals-skills` repo is archived; use the new one. |
| **AI apps: RAG** | wshobson → `rag-implementation`, `llm-evaluation`, `hybrid-search-implementation` | — | Avoid `prompt-engineering-patterns` unless you review its `optimize-prompt.py`. |
| **Web performance & accessibility** | [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) → `performance`, `core-web-vitals`, `accessibility`, `web-quality-audit`. MIT, 3.0k★. | wshobson → `wcag-audit-patterns`, `screen-reader-testing` | `web-quality-audit/scripts/analyze.sh` is a read-only analyzer (needs `jq`); `accessibility` suggests installing `@axe-core/cli` globally. |
| **Docs / ADRs** | Your workflow pack (Addy `documentation-and-adrs`) or this toolkit's `architecture-planning` | wshobson → `architecture-decision-records` | |
| **UI design** | See [TOOLKIT-GUIDE.md](TOOLKIT-GUIDE.md) §3.4: one of Impeccable, UI/UX Pro Max or Taste Skill; Apple Design for HIG reviews | | |

### Install commands for the picks

All from each repository's README. Preview with `--list` before installing; choose project scope.

```bash
npx skills add https://github.com/twostraws/swiftui-agent-skill --skill swiftui-pro
npx skills@latest add callstackincubator/agent-skills --skill react-native-best-practices
npx skills add https://github.com/currents-dev/playwright-best-practices-skill
npx skills add getsentry/skills --list            # then pick security-review / find-bugs
npx skills add wshobson/agents --skill api-design-principles
npx skills add apollographql/skills@graphql-schema
npx skills add timescale/pg-aiguide --skill postgres
npx skills add docker/skills --skill docker-compose-patterns
npx skills add https://github.com/ai-evals-course/evals-skills --skill eval-audit
npx skills add addyosmani/web-quality-skills
android skills add jetpack-compose-performance --project=.   # needs the Android CLI
```

After installing, read each new `SKILL.md`, then run `python scripts/sync_toolkit.py`.

## MCP servers

The reviewed servers are in `toolkit.config.json` (all optional ones are **off** by default). Changes from this review:

| Server | Status | Detail |
|---|---|---|
| Supabase | Updated | Canonical repo is now [supabase/mcp](https://github.com/supabase/mcp). URL adds `features=database,docs` to limit tool groups. |
| Mobile MCP | Updated | Sends PostHog/Scarf telemetry by default; config now sets `MOBILEMCP_DISABLE_TELEMETRY=1`. |
| Sentry | Added (off) | Official, `https://mcp.sentry.dev/mcp`, OAuth. **No read-only mode**: approve tool calls individually. Can be scoped with `/mcp/<org>/<project>`. |
| Linear | Added (off) | Official read-only endpoint `https://mcp.linear.app/mcp/readonly`, OAuth. |
| Grafana | Added (off) | Official `uvx mcp-grafana@2.0.2 --disable-write`; needs `GRAFANA_URL`, `GRAFANA_SERVICE_ACCOUNT_TOKEN`. Apache-2.0. |
| Semgrep | Kept | `semgrep mcp` (built into the Semgrep CLI) is current; the standalone `semgrep/mcp` repo and `uvx semgrep-mcp` are archived. |

Reviewed but **not added** (add manually only with a specific need):

| Server | Reason |
|---|---|
| Vercel (`https://mcp.vercel.com`), Cloudflare API (`https://mcp.cloudflare.com/mcp`) | Official but can deploy and make purchases; no read-only mode. Cloudflare's docs-only server `https://docs.mcp.cloudflare.com/mcp` is safe. |
| AWS ([awslabs/mcp](https://github.com/awslabs/mcp)) | Use the remote knowledge server `https://knowledge-mcp.global.api.aws` (no credentials) for docs; the Cloud Control API server is deprecated. |
| Atlassian (`https://mcp.atlassian.com/v2/mcp`) | Official; OAuth; delete/manage tools off by default. The old `/v1/sse` endpoint is past end of life. |
| Figma (`https://mcp.figma.com/mcp`) | Official, hosted; can write to the canvas; desktop server needs a paid seat. |
| Datadog | Official but endpoint path is still `unstable`. |
| Kubernetes ([containers/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server)) | Apache-2.0; set `read_only = true` in its TOML config. |
| Postgres ([crystaldba/postgres-mcp](https://github.com/crystaldba/postgres-mcp)) | MIT, `--access-mode=restricted` is read-only, but commits are sparse (Jan and Aug 2026); recheck before use. |
| Exa / Firecrawl / Tavily | Web search for AI features only; each has API-key costs. |
| XcodeBuildMCP (getsentry) | MIT, iOS builds; the npm package appears to have been renamed `mobilebuildmcp` and it sends error telemetry. Unverified; check before use. |
| Playwright CLI | Not an MCP server: Microsoft's lower-token alternative for coding agents. Keep Playwright MCP for long browser-state sessions. |

## Rejected

| Candidate | Reason |
|---|---|
| openai/skills, JetBrains/skills | No repository-level license |
| garrytan/gstack | All-in-one workflow pack; its setup builds binaries, downloads Chromium and includes a self-update skill |
| affaan-m/everything-claude-code, ruvnet/ruflo, modu-ai/moai-adk | Overlapping methodology mega-packs |
| CharlesWiltgen/Axiom (iOS) | 123 skills plus session hooks and MCP auto-discovery: too invasive |
| android/skills `android-cli` | Pipes a remote script to the shell and installs other skills |
| VoltAgent subagents, Jeffallan `*-expert`, davila7 templates | Persona-style prompts, not procedural skills |
| openclaw bundles | Personal automation (password manager, smart home), not software delivery |
| Aggregators (sickn33, Microck, majiayu000) | Copies of other repos; install from the original instead |
| ClawHub-only listings | No public repository or license to review |
| MCP Market "Fullstack" server | Broad write capabilities, no clear license |

## What the marketplaces are (and aren't) good for

- **Star and install counts are not per-skill.** SkillsMK and MCP Market show the whole repository's stars on every skill (e.g. 330k–392k on each openclaw skill); counts are stale (wshobson shows 31.6k vs 41k actual); AI Skill Market shows the same install count on every gstack skill.
- **Indexes are incomplete.** None of the four lists android/skills fully; SkillsMK indexes 97 of wshobson's 185 skills; currents-dev's Playwright skill is missing from SkillsMP and SkillsMK.
- **Categories are noisy.** SkillsMK files ~13k of ~15k skills under "Development"; search for "compose" returns writing skills. SkillsMP also indexes leaked system prompts and offensive tooling alongside everything else.
- **AI Skill Market's best signal is install counts on well-known repos**, which confirm Superpowers, Supabase and Azure as widely used. Its blog has no engineering comparisons.
- Use the sites to find names; decide from the repository.

## Review checklist before installing anything

- [ ] Open the upstream repository, not the marketplace page.
- [ ] Confirm a license file that fits your use.
- [ ] Check recent commits (reject >9 months without activity) and open issues.
- [ ] Read `SKILL.md`, its scripts and referenced files. Look for shell execution, global installs, remote fetches, telemetry, credentials, and instructions to install other skills.
- [ ] Install project-locally, run `python scripts/sync_toolkit.py`, and test on a small task from [QUALITY-GATES.md](QUALITY-GATES.md).
- [ ] Re-read the diff before accepting an update.
