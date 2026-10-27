# Universal Vibe-Coding Engineering Toolkit

**One engineering setup for every AI coding tool.** Rules, 277 vetted skills and 22 MCP servers that behave the same in **Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Antigravity and GitHub Copilot**. The right skills are **picked automatically from your project**, and a script generates each tool's own configuration. Everything is free and openly licensed.

- **Superpowers workflow built in:** brainstorm → plan → test-first → debug → review → verify, on by default for every tool.
- **Automatic skill selection:** the sync reads your dependencies, platform folders, CI files and project brief, and enables only the matching profiles (Next.js → `web`, `nextjs`, `testing`, `interface-craft`; Expo → `react-native`; `go.mod` → `go`; Prisma → `prisma`; OpenAI SDK → `ai-apps`; …). `--explain` shows why.
- **277 vetted skills in 44 profiles from 46 upstream sources:** web, Next.js, Firebase, Cloudflare, Convex, Clerk, Neon, GSAP, React Native/Expo, native iOS and Android, Flutter, TypeScript, Python, Go, Rust, Java, .NET, PHP, Ruby, Vue, Angular, Postgres, Supabase, Prisma, API, DevOps, cloud, security, testing, AI apps, UI polish, interface craft, UX design and research, anti-AI-slop design, design memory, code intelligence. Each is pinned to an upstream commit, licensed and reviewed by hand; where two covered the same need, the best was kept.
- **22 MCP servers, written in each tool's own format:** documentation, browser, GitHub, databases, errors, issues and observability. Free ones are marked, and anything that can write is off by default.
- **Safety by default:** human approval for production, no secrets in config, read-only MCP modes, and CI that checks generated files stay in sync.

**New here? Start with [docs/GETTING-STARTED.md](docs/GETTING-STARTED.md):** build a full-stack app step by step, with copy-paste prompts for every phase.

## How it works

| You edit | What it is | How each tool gets it |
|---|---|---|
| `AGENTS.md` | Engineering rules | Read natively by Codex, Cursor, OpenCode, Antigravity and Copilot. Claude Code imports it via `CLAUDE.md`, Gemini CLI via `GEMINI.md`. |
| `toolkit.config.json` | Tools in use, skill profiles, MCP servers | `scripts/sync_toolkit.py` copies enabled skills into `.agents/skills/` and writes every tool's MCP file. |
| `.agents/skills/` | Your own skills | Read natively by Codex, Cursor, OpenCode, Gemini CLI, Antigravity and Copilot; mirrored to `.claude/skills/` for Claude Code. |

```json
{
  "tools": ["claude-code", "codex", "cursor", "opencode", "gemini-cli", "antigravity", "copilot"],
  "skillProfiles": ["core", "docs", "web", "testing", "postgres"],
  "skills": [],
  "mcpServers": { "context7": { "enabled": true, "...": "..." } }
}
```

```bash
python scripts/sync_toolkit.py          # apply
python scripts/sync_toolkit.py --check  # CI: fail if generated files are stale
```

Generated files (committed; never edit by hand): `.mcp.json` (Claude Code, Copilot), `.cursor/mcp.json`, `opencode.json`, `.codex/config.toml` (read after you trust the project), `.gemini/settings.json`, `.agents/mcp_config.json` (Antigravity), `.claude/skills/`, and library skills in `.agents/skills/` (marked with `.toolkit-generated`). The sync merges: your own servers, settings and hand-written skills are never overwritten.

## Quick start

Requires Python 3.11+ and Git (standard library only; no packages), plus Node.js for the default MCP servers.

```bash
mkdir my-app && cd my-app && git init
python <path-to-toolkit>/scripts/install_toolkit.py .
```

Then choose your tools, skill profiles and MCP servers in `toolkit.config.json`, run `python scripts/sync_toolkit.py`, and follow [GETTING-STARTED.md](docs/GETTING-STARTED.md). The installer never overwrites existing files; it lists them so you can merge.

## Skills

**Toolkit skills** (always on): `production-engineering`, `architecture-planning`, `release-verification`, `marketplace-skill-review`, `ai-application-engineering`, `select-skills`, which tells every agent to re-run the selection when requirements change, and `python-venv`, which makes every Python command run in the project's `.venv` (never the system Python).

**Library profiles** are chosen automatically (`"autoSkills": true`). `core` (the Superpowers workflow) and `docs` are always on; the rest switch on when the project needs them:

For a Next.js app with Prisma (Postgres), Stripe and the OpenAI SDK:

```bash
python scripts/sync_toolkit.py --explain
```
```text
Skill profiles enabled:
  core             toolkit.config.json skillProfiles; baseline workflow
  docs             toolkit.config.json skillProfiles; baseline
  web              dependency next, react-dom
  testing          web UI
  postgres         Prisma datasource postgresql
  prisma           @prisma/client
  nextjs           dependency next
  typescript       typescript
  ai-apps          dependency openai
  interface-craft  the project has a user interface
Individual skills enabled:
  vibe-security    handles stripe
Suggested, not enabled automatically (add to skillProfiles to accept):
  security         handles stripe -- security-review and gha-security-review pre-approve Bash in Claude Code
```

Profiles whose skills pre-approve shell commands (`security`, `ripwire`) are only suggested. Design, research and production-engineering profiles (`addy-engineering`, `ux-design`, `ux-research`, `ui-polish`, `anti-slop`, `cloud`, `authoring`) are added by name. The full list, what triggers each profile, cautions and the "keep the best" decisions: **[docs/SKILLS-CATALOG.md](docs/SKILLS-CATALOG.md)**. Commits and licenses: [skills-library/THIRD_PARTY_NOTICES.md](skills-library/THIRD_PARTY_NOTICES.md).

**Alternative workflows** that replace `core`: GitHub Spec Kit, GSD Core, pstack (see the catalog).

Update the library with `python scripts/vendor_skills.py --update`, review `git diff skills-library/`, then sync.

## MCP servers

On by default: **Context7** (library docs) and **Playwright** (browser), both free with no account.

| Server | Cost / account | Writes? |
|---|---|---|
| `deepwiki` | Free, no account | No |
| `microsoft-learn` | Free, no account | No |
| `aws-knowledge` | Free, no credentials (rate limited) | No |
| `cloudflare-docs` | Free | No |
| `exa` | Free tier without a key (rate limited) | No |
| `chrome-devtools` | Free, needs Chrome | Local browser only |
| `next-devtools` | Free, Next.js 16+ (telemetry disabled) | No |
| `shadcn` | Free | Adds component files |
| `magicui` | Free, no account | No (read-only registry lookups) |
| `21st` | Free key; retrieval and generation paid | Returns component code |
| `firecrawl` | Free plan (limited credits), API key | No (scrapes and searches the web) |
| `ripwire` | Free, local binary (v0.6.7) | No |
| `git` | Free, needs `uv` | Can commit and switch branches |
| `mobile-mcp` | Free, needs Xcode/ADB (telemetry disabled) | Drives devices |
| `semgrep` | Free CLI | No |
| `github` | Free, needs Docker + token | Read-only mode |
| `supabase` | Free tier account | `read_only=true`, one project |
| `linear` | Account | Read-only endpoint |
| `grafana` | Your Grafana | `--disable-write` |
| `sentry` | Account | Yes (no read-only mode) |

Secrets go in `envPassthrough` (variable names only); the sync writes each tool's reference syntax. Versions are pinned.

## Repository layout

```text
AGENTS.md                  rules for every tool
CLAUDE.md, GEMINI.md       adapters that import AGENTS.md
toolkit.config.json        tools, skill profiles, MCP servers
.agents/skills/            toolkit skills (+ generated library skills)
skills-library/            277 vendored skills, library.json, THIRD_PARTY_NOTICES.md
scripts/
  sync_toolkit.py          generate per-tool config; --check for CI
  vendor_skills.py         fetch/update library skills at pinned commits
  install_toolkit.py       copy the toolkit into a project
  validate_toolkit.py      validate this repository
templates/ci-node.yml      CI starter to copy into your app's .github/workflows/
docs/                      getting started, skills catalog, guides, research
tests/                     script tests (run in CI on Linux and Windows)
```

## Verify

```bash
python -m unittest discover -s tests
python scripts/validate_toolkit.py
```

## Production security defaults

- Never deploy to production from an unreviewed agent session; require human approval.
- Give agents only development or staging credentials; keep production keys out of every session.
- Start MCP servers read-only with minimum toolsets; treat everything they return as untrusted data.
- Require human review for data deletion/migration, IAM, DNS/network, billing, secret rotation and production deploys.
- Pin GitHub Actions to full commit SHAs, use least-privilege `permissions`, protect deployment environments.
- Run tests and security scans in CI; MCP tools do not replace them.

See [SECURITY.md](SECURITY.md) for how third-party skills are vetted and how to report problems.

## Documentation

| Doc | For |
|---|---|
| [GETTING-STARTED.md](docs/GETTING-STARTED.md) | Building an app with the toolkit, phase by phase |
| [SKILLS-CATALOG.md](docs/SKILLS-CATALOG.md) | Every library skill, profile, caution and exclusion |
| [TOOLKIT-GUIDE.md](docs/TOOLKIT-GUIDE.md) | Stack defaults, per-tool plugin installs, CI security tools, multi-agent rules |
| [AGENT-ADAPTERS.md](docs/AGENT-ADAPTERS.md) | Verified file locations per tool |
| [MARKETPLACE-DECISION-SUMMARY.md](docs/MARKETPLACE-DECISION-SUMMARY.md) / [MARKETPLACE-RESEARCH.md](docs/MARKETPLACE-RESEARCH.md) | Marketplace review and evidence |
| [QUALITY-GATES.md](docs/QUALITY-GATES.md) | Scenarios to test an agent setup |
| [CONTRIBUTING.md](CONTRIBUTING.md) / [CHANGELOG.md](CHANGELOG.md) | Changing the toolkit |

## License

The toolkit is released under the [MIT License](LICENSE). Third-party skills in `skills-library/` (and their generated copies in `.agents/skills/` and `.claude/skills/`) keep their own upstream licenses, included in each skill folder and listed in [THIRD_PARTY_NOTICES.md](skills-library/THIRD_PARTY_NOTICES.md).
