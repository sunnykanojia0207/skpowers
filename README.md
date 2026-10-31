# Universal Vibe-Coding Engineering Toolkit

**One engineering setup for every AI coding tool.** Rules, 300 vetted skills and 22 MCP servers that behave the same in **Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Antigravity and GitHub Copilot**. The right skills are **picked automatically from your project**, and a script generates each tool's own configuration. Everything is free and openly licensed.

- **Superpowers workflow built in:** brainstorm → plan → test-first → debug → review → verify, on by default for every tool.
- **Automatic skill selection:** the sync reads your dependencies, platform folders, CI files and project brief, and enables only the matching profiles (Next.js → `web`, `nextjs`, `testing`, `interface-craft`; Expo → `react-native`; `go.mod` → `go`; Prisma → `prisma`; OpenAI SDK → `ai-apps`; …). `--explain` shows why.
- **300 vetted skills in 45 profiles from 57 upstream sources:** web, Next.js, Firebase, Cloudflare, Convex, Clerk, Neon, GSAP, React Native/Expo, native iOS and Android, Flutter, TypeScript, Python, Go, Rust, Java, .NET, PHP, Ruby, Vue, Angular, Postgres, Supabase, Prisma, API, DevOps, cloud, security, testing, AI apps, UI polish, interface craft, UX design and research, anti-AI-slop design, design memory, code intelligence. Each is pinned to an upstream commit, licensed and reviewed by hand; where two covered the same need, the best was kept.
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

**Once per machine** (a shared copy of the toolkit and its skills library):

```bash
git clone --depth 1 https://github.com/sunnykanojia0207/skpowers ~/.skpowers
```

**In any project** (new or existing), one command:

```bash
cd my-app
python ~/.skpowers/scripts/install_toolkit.py
```

It takes a few seconds: it copies the rules, config and toolkit skills, reads the project to pick the right skill profiles, copies only those skills for every tool, and writes each tool's MCP config. Existing files (your `AGENTS.md`, configs) are never overwritten; they are listed so you can merge. Commit the result so teammates and CI get the same skills without the toolkit.

**While you work, skills follow the request too.** Agents run `--pick` for UI requests and `--suggest` for everything else, and enable what fits; you can do the same:

```bash
python scripts/sync_toolkit.py --pick "build a landing page that doesn't look generic"
python scripts/sync_toolkit.py --suggest "add stripe payments and email login"
python scripts/sync_toolkit.py --enable clerk          # or --disable
```

See [Using skills](#using-skills) for how agents pick and use skills.

**Update later:** `git -C ~/.skpowers pull`, then in the project `python ~/.skpowers/scripts/install_toolkit.py --update` (refreshes the sync script and toolkit skills, never your files) and `python scripts/sync_toolkit.py`.

## Using skills

You don't have to memorise skill names. Skills reach your agent in three automatic ways, and you can always name one to be sure.

### 1. From the project (on install and every sync)
The sync reads your dependencies, project files and the platform boxes in `docs/PROJECT_BRIEF.md`, and enables the matching profiles. A Next.js app gets `web`, `nextjs`, `testing` and `interface-craft`; an Expo app gets `react-native`; Prisma adds `prisma`; an OpenAI or Anthropic SDK adds `ai-apps`. `core` (the Superpowers workflow), `docs` and the toolkit's own skills are always on.

```bash
python scripts/sync_toolkit.py --explain    # what is enabled and why
```

### 2. From your request (the agent does this for you)
For each new request, agents follow `AGENTS.md` and the `select-skills` skill:

- **UI and design requests:** `python scripts/sync_toolkit.py --pick "<request>"` reads what kind of UI you want and enables the right design skills, keeping one design style per project (a new style switches the old one off):

  | Your request mentions | Skills picked |
  |---|---|
  | landing page, homepage, hero, marketing site, portfolio | `design-taste-frontend` + `landing-page-design` |
  | dashboard, admin, settings page, SaaS screens | `interface-design` + `ux-design` |
  | branding, brand identity, logo, rebrand | `hue` |
  | references, inspiration, "make it look like…" | `tastemaker` |
  | colour palette, fonts, style guide | `ui-ux-pro-max` + `color-expert` |
  | generic, premium, polished, redesign | `design-taste-frontend` + `anti-slop` |
  | original look, art direction, editorial, publication | `bencium-innovative-ux-designer` |
  | animation, transitions, smooth, scroll effects | `ui-polish` + `interaction-design` |
  | mascot, illustration, "make it feel alive" | `rossark-motion-skill` |
  | isometric figure, exploded view, cutaway | `anatomy` |
  | component canvas, storybook, component variants | `component-canvas` |
  | design canvas, explore ideas, compare designs | `create-canvas` |
  | DESIGN.md, design system, tokens | `create-design-md` |
  | accessibility, contrast, keyboard, screen reader | `ui-fixes` |
  | forms, onboarding, checkout, empty/error/loading states | `ux-design` |

- **Everything else:** `python scripts/sync_toolkit.py --suggest "<request>"` lists the enabled skills that already match (use those), then the best library matches; the agent enables what clearly fits with `--enable <name>` and tells you. Stack-specific skills only appear when you name the stack. Profiles that pre-approve shell commands (`security`, `ripwire`) and all MCP servers need your yes.

### 3. Inside each session (automatic)
Every tool reads each installed skill's name and description at session start. When your request matches a description, the agent opens that skill and follows it; Superpowers' `using-superpowers` makes it check before every reply. **You don't need to mention skills.**

### Naming a skill (optional, to be certain)
- In any tool: "use the `interface-design` skill to build the settings page".
- In Claude Code: type `/interface-design`.
- Nine skills only run when named: `review-animations`, `pick-ui-library`, `prototype`, `interface-review`, `explain-interface`, `state-machine`, `break`, `variant`, `improve-codebase-architecture`.

### Prompts that pick the right skills
| Say | What happens |
|---|---|
| "Build a landing page for our product, it shouldn't look generic" | `design-taste-frontend`, `landing-page-design`, `anti-slop`; Vercel React rules if it is React |
| "Design the admin dashboard with filters and empty states" | `interface-design`, `ux-design` |
| "Add Clerk sign-in to the Next.js app" | `clerk` profile (and `vibe-security` once `@clerk/*` is installed) |
| "Write E2E tests for checkout" | the enabled `playwright-best-practices` / `webapp-testing` |
| "The app is slow" | the enabled `performance` and Next.js cache skills, then `addy-engineering` |
| "Build a RAG chatbot over our docs" | `ai-apps` (evals, RAG), plus `claude-api` or `ai-sdk` for your SDK |

### Commands
```bash
python scripts/sync_toolkit.py --explain                 # what's enabled and why
python scripts/sync_toolkit.py --pick "<UI request>"     # enable design skills for a UI request
python scripts/sync_toolkit.py --suggest "<request>"     # best matches for any request
python scripts/sync_toolkit.py --enable <name> [...]     # turn on profiles/skills (also --disable)
python scripts/sync_toolkit.py                           # apply after editing toolkit.config.json
```

To force a profile on, list it under `skillProfiles` in `toolkit.config.json`; `"autoSkills": false` turns off detection from the project.

**What's in the library:** 300 vetted skills in 45 profiles, plus 7 toolkit skills (`production-engineering`, `architecture-planning`, `release-verification`, `marketplace-skill-review`, `ai-application-engineering`, `select-skills`, `python-venv`). Every profile, what switches it on, cautions and the "keep the best" decisions: **[docs/SKILLS-CATALOG.md](docs/SKILLS-CATALOG.md)**. Commits and licenses: [skills-library/THIRD_PARTY_NOTICES.md](skills-library/THIRD_PARTY_NOTICES.md).

**Alternative workflows** that replace `core`: GitHub Spec Kit, GSD Core, pstack, Addy Osmani's workflow (see the catalog). Update the library with `python scripts/vendor_skills.py --update`, review `git diff skills-library/`, then sync.

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
skills-library/            300 vendored skills, library.json, THIRD_PARTY_NOTICES.md
scripts/
  sync_toolkit.py          generate per-tool config; --check for CI
  vendor_skills.py         fetch/update library skills at pinned commits
  install_toolkit.py       copy the toolkit into a project
  validate_toolkit.py      validate this repository
templates/ci-node.yml      CI starter to copy into your app's .github/workflows/
docs/                      getting started, skills catalog, guides, research
templates/docs/            project doc templates (architecture, database, API, security, UX flows, code style, testing)
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
