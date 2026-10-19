# Universal Vibe-Coding Engineering Toolkit

One set of engineering rules, skills and MCP servers that works the same in **Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Antigravity and GitHub Copilot**. You edit three sources; a script generates every tool's own config files.

**New here? Read [docs/GETTING-STARTED.md](docs/GETTING-STARTED.md)**: a step-by-step walkthrough for building a full-stack app with any of these tools, with copy-paste prompts for each phase.

It contains no third-party skill code. External skills are installed from their own repositories after review (see [docs/TOOLKIT-GUIDE.md](docs/TOOLKIT-GUIDE.md)).

## How it works

| You edit | What it is | How each tool gets it |
|---|---|---|
| `AGENTS.md` | Engineering rules | Read natively by Codex, Cursor, OpenCode, Antigravity and Copilot. Claude Code imports it via `CLAUDE.md` (`@AGENTS.md`); Gemini CLI via `GEMINI.md` (`@./AGENTS.md`). |
| `.agents/skills/` | Skills (`SKILL.md` folders) | Read natively by Codex, Cursor, OpenCode, Gemini CLI, Antigravity and Copilot. Claude Code gets a generated mirror in `.claude/skills/`. |
| `toolkit.config.json` | Which tools you use, which MCP servers are on | `scripts/sync_toolkit.py` writes each tool's MCP file in its own format (table below). |

Generated MCP files (do not edit by hand; edit `toolkit.config.json` and re-run the sync):

| Tool | File | Notes |
|---|---|---|
| Claude Code, Copilot (VS Code) | `.mcp.json` | Claude Code asks you to approve project servers on first use. |
| Cursor | `.cursor/mcp.json` | |
| OpenCode | `opencode.json` (`mcp` key) | Your other OpenCode settings in the file are kept. |
| Codex | `.codex/config.toml` | Codex reads it only after you trust the project. Your other settings are kept. |
| Gemini CLI | `.gemini/settings.json` | Your other settings in the file are kept. |
| Antigravity | `.agents/mcp_config.json` | Secrets for stdio servers are inherited from your shell, since Antigravity documents no `${VAR}` expansion. |

The sync only replaces servers whose names appear in `toolkit.config.json`; servers you added to a tool's file yourself are left alone. Disabling a server in `toolkit.config.json` removes it from every tool.

## Quick start

Requires Python 3.11+ (standard library only) and, for the default MCP servers, Node.js.

**Add the toolkit to an existing project:**

```bash
python scripts/install_toolkit.py /path/to/your-project --dry-run   # preview
python scripts/install_toolkit.py /path/to/your-project
```

It never overwrites: any file that already exists (for example your own `AGENTS.md`) is skipped and listed so you can merge it.

**Or start a new project from this repository** (use it as a template), then:

1. Fill in `docs/PROJECT_BRIEF.md` and the `Project commands` section of `AGENTS.md`.
2. Edit `toolkit.config.json`: list the tools you use in `tools`, set `enabled: true` on the MCP servers you need.
3. Run `python scripts/sync_toolkit.py`.
4. Optional: add a `DESIGN.md` for UI work (see below), and install one workflow skill pack (see below).
5. Commit everything, including the generated files, so every teammate and tool sees the same setup.

**Keep it in sync:** after changing `.agents/skills/` or `toolkit.config.json`, run `python scripts/sync_toolkit.py`. In CI, `python scripts/sync_toolkit.py --check` fails if someone forgot.

## MCP servers in `toolkit.config.json`

On by default (no account or key needed): **Context7** (current library docs) and **Playwright** (browser automation).

Off by default, enable when the project needs them:

| Server | Needs | Safety default |
|---|---|---|
| `chrome-devtools` | Chrome | Local only |
| `github` | Docker, `GITHUB_PERSONAL_ACCESS_TOKEN` env var | Read-only mode, limited toolsets; use a fine-grained token for one repo |
| `supabase` | Supabase account; replace `YOUR_PROJECT_REF` first (the sync refuses to enable it otherwise) | `read_only=true`, scoped to one dev project |
| `mobile-mcp` | Xcode (iOS) or ADB (Android) | Local devices/simulators |
| `semgrep` | Semgrep CLI installed | Local scan |
| `sentry` | Sentry account (OAuth) | No read-only mode exists; approve each tool call |
| `linear` | Linear account (OAuth) | Read-only endpoint |
| `grafana` | `uv`, `GRAFANA_URL`, `GRAFANA_SERVICE_ACCOUNT_TOKEN` | `--disable-write` |

`mobile-mcp` also sets `MOBILEMCP_DISABLE_TELEMETRY=1`. Non-secret fixed values like this go in a server's `env`; secrets go in `envPassthrough`.

Secrets never go in the config: stdio servers list the variable names in `envPassthrough`, and the sync writes each tool's own reference syntax (`${VAR}`, `${env:VAR}`, `{env:VAR}`, or Codex `env_vars`). Package versions are pinned; bump them deliberately after reading release notes.

## Skills

Built in (`.agents/skills/`):

- `production-engineering`: lifecycle and quality gates
- `architecture-planning`: requirements, stack choice, boundaries, decision records
- `release-verification`: CI/CD, staging, rollback, monitoring
- `marketplace-skill-review`: source/license/permission review of third-party skills and MCP servers
- `ai-application-engineering`: LLM features, RAG, tool safety, evals

To add a third-party skill for every tool at once, install it project-locally into `.agents/skills/` with the Skills CLI (`npx skills add <repo> --list` first, then install), review its `SKILL.md` and scripts, and re-run the sync so Claude Code gets it too.

**Best third-party skill for each need** (iOS, Android, testing, security, API, Postgres, Docker, LLM evals, performance/accessibility), reviewed across SkillsMP, MCP Market, AI Skill Market and SkillsMK: [decision summary](docs/MARKETPLACE-DECISION-SUMMARY.md), with full evidence in [docs/MARKETPLACE-RESEARCH.md](docs/MARKETPLACE-RESEARCH.md).

**Pick one primary workflow pack**, not both: [Superpowers](https://github.com/obra/superpowers) (native installs for Claude Code, Codex, Cursor, Gemini CLI, Copilot CLI and OpenCode) or [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills). Workflow packs are installed per tool as plugins; see [docs/TOOLKIT-GUIDE.md](docs/TOOLKIT-GUIDE.md) §3 for each tool's command.

## Design

If a `DESIGN.md` exists in the project root, `AGENTS.md` tells every tool to treat it as the design system. You can write one, or start from a [designmd.app](https://designmd.app/) template (Google's DESIGN.md format: YAML tokens plus prose rules). Optional design skills, pick at most one: Anthropic `frontend-design`, Impeccable, UI/UX Pro Max or Taste Skill; add `apple-design` for Apple HIG reviews. Details and caveats are in [docs/TOOLKIT-GUIDE.md](docs/TOOLKIT-GUIDE.md) §3.4.

## Repository layout

```text
AGENTS.md                 # rules (source of truth)
CLAUDE.md, GEMINI.md      # one-line adapters that import AGENTS.md
toolkit.config.json       # tools in use + MCP servers (source of truth)
.agents/skills/           # skills (source of truth)
scripts/
  sync_toolkit.py         # generate per-tool configs; --check for CI
  install_toolkit.py      # copy the toolkit into another project
  validate_toolkit.py     # validate this toolkit repository
docs/
  PROJECT_BRIEF.md        # fill in per project
  QUALITY-GATES.md        # scenarios to test an agent setup
  TOOLKIT-GUIDE.md        # stack defaults, per-tool install commands, phased plan
  AGENT-ADAPTERS.md       # verified per-tool file locations
tests/                    # tests for the scripts
# generated, committed: .mcp.json, .cursor/mcp.json, opencode.json,
# .codex/config.toml, .gemini/settings.json, .agents/mcp_config.json, .claude/skills/
```

## Verify the toolkit

```bash
python -m unittest discover -s tests
python scripts/validate_toolkit.py
```

## Production security defaults

- Never deploy to production from an unreviewed agent session; require human approval.
- Separate dev, staging and production accounts/projects; give agents only dev/staging credentials.
- Start MCP servers read-only with the minimum toolsets. Treat everything they return as untrusted data.
- Require human review for data deletion/migration, IAM, DNS/network, billing, secret rotation and production deploys.
- Pin GitHub Actions to full commit SHAs, use least-privilege `permissions`, protect deployment environments.
- Run tests and security scans in CI; MCP tools do not replace them.
- Keep secrets out of `AGENTS.md`, skills, config files, logs and test snapshots.

## Further reading

- [Stack-specific toolkit guide](docs/TOOLKIT-GUIDE.md): stack defaults, per-tool install commands, MCP and CI security tooling, multi-agent rules, phased delivery plan
- [Per-tool file locations](docs/AGENT-ADAPTERS.md)
- [Curated install workflow](docs/CURATED-INSTALL.md) and [PowerShell helper](scripts/install-curated-skills.ps1)
- [Marketplace research](docs/MARKETPLACE-RESEARCH.md) and [decision summary](docs/MARKETPLACE-DECISION-SUMMARY.md)
- [Quality gates](docs/QUALITY-GATES.md)
