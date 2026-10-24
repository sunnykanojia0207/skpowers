# Getting Started: Build a Full-Stack App with Any AI Coding Tool

This project uses the universal engineering toolkit. Its rules, skills and MCP servers live in files inside the repository, so **Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Antigravity and GitHub Copilot all behave the same way here**. You can switch tools at any point and the next one picks up where the last stopped.

| File | Purpose |
|---|---|
| `AGENTS.md` | The rules every tool follows |
| `.agents/skills/` | Skills every tool can load |
| `toolkit.config.json` | Which tools you use and which MCP servers are on |
| `docs/PROJECT_BRIEF.md` | What you want built (you write this) |

## 1. Create the project (once)

Requires Git, Python 3.11+ and Node.js.

```bash
mkdir my-app
cd my-app
git init
python <path-to-toolkit>/scripts/install_toolkit.py .
```

The installer copies the toolkit in and generates each tool's config. It never overwrites a file that already exists; it lists skipped files so you can merge them by hand.

## 2. Configure (about 5 minutes)

1. **Choose tools and MCP servers** in `toolkit.config.json`:
   - Keep only the tools you use in `tools`.
   - Set `"enabled": true` on the servers you need. Context7 (library docs) and Playwright (browser testing) are on by default. Free extras (DeepWiki, Microsoft Learn, AWS Knowledge, Cloudflare docs, Exa search, Next.js devtools, shadcn, Git, Chrome DevTools, Mobile MCP, Semgrep) and account-based ones (GitHub, Supabase, Linear, Grafana, Sentry) are ready but off.
   - Then generate the configs:
     ```bash
     python scripts/sync_toolkit.py
     ```
2. **Write the brief** in `docs/PROJECT_BRIEF.md`: product, users, platforms (web, iOS, Android, API, admin), the three most important user journeys, budget, deadline and data sensitivity. This is the most important input: agents build what the brief says.
3. **Let the toolkit pick the skills.** Tick your platforms in `docs/PROJECT_BRIEF.md` (`- [x] Web`, `- [x] iOS`, …), then run `python scripts/sync_toolkit.py --explain` to see what it picks and why, and `python scripts/sync_toolkit.py` to apply. It reads your dependencies and project files too, so rerun it whenever the stack changes (agents do this through the `select-skills` skill). The vetted skills are already in `skills-library/`; nothing is downloaded. To add more by hand, list profiles under `skillProfiles` in `toolkit.config.json`; typical additions:

   | App | Profiles |
   |---|---|
   | Next.js / React SaaS or dashboard | `core docs web ui-polish testing postgres api security devops` |
   | Expo / React Native app | `core docs react-native testing api` |
   | Native iOS / Android | `core docs ios` / `core docs android` |
   | Any app with LLM features | add `ai-apps` |
   | Supabase or Prisma backend | add `supabase` or `prisma` |

   `docs/SKILLS-CATALOG.md` lists every skill and its cautions. The `core` profile installs Superpowers for every tool at once, so you don't need the per-tool Superpowers plugin; don't add a second workflow pack.
4. **For apps with a UI, add a `DESIGN.md`** in the project root; every tool follows it. Start from a template in [awesome-design-md](https://github.com/VoltAgent/awesome-design-md), [designmd.app](https://designmd.app/) or [Refero Styles](https://styles.refero.design/) and replace the brand's colors, type and voice with your own. For Tailwind projects, add `@shadcn/lint` in Phase 1 so agents get design-system errors in lint and CI (see the toolkit's `docs/SKILLS-CATALOG.md`, "Design resources and guardrails").
5. **Commit everything**, including generated files:
   ```bash
   git add -A
   git commit -m "Add engineering toolkit"
   ```

## 3. Open your tool in the project folder

| Tool | One-time step |
|---|---|
| Claude Code | Approve the project MCP servers when prompted |
| Codex | Mark the project as trusted (otherwise it ignores `.codex/config.toml`) |
| Cursor, OpenCode, Gemini CLI, Antigravity, Copilot | None; everything loads automatically |

**Check it worked:** ask *"Which rules and skills are you using in this repo?"* The answer should mention `AGENTS.md` and the toolkit skills.

## 4. Build in phases

Paste these prompts in order. Do not start a phase until you have checked the result of the previous one.

### Phase 0: Spec and architecture (no code)

```text
Read AGENTS.md and docs/PROJECT_BRIEF.md. We are in Phase 0. Do not write code.
Ask me up to five clarifying questions, then write docs/SPEC.md (users, features,
non-goals, data model, API list) and docs/ARCHITECTURE.md (stack with reasons and
tradeoffs, folder tree, threat list, test strategy). Stop and wait for my approval.
```

Read both documents carefully. This is where you decide what gets built; correcting it here costs minutes, later it costs days.

### Phase 1: Foundation

```text
Phase 1: scaffold the approved architecture with strict types, linting, formatting,
environment validation, .env.example, a CI workflow at .github/workflows/ci.yml
(start from templates/ci-node.yml; add a security scan), and /healthz and /version endpoints. Fill in the "Project commands"
section of AGENTS.md with the real commands. Run every command and show me the output.
```

### Phase 2: Walking skeleton

```text
Phase 2: build one thin end-to-end slice: sign-in, one screen, one API route, one
database migration, and one Playwright E2E test (or one simulator flow for mobile).
Write the test first. Run lint, typecheck, tests and build, and show the output.
```

### Phase 3: Features (repeat for each feature, one branch each)

```text
Feature: <describe the feature and who uses it>.
Write acceptance criteria and a failing test first, then implement, run the app and
verify it in the browser or simulator, including loading, empty and error states.
Finish with the completion report from AGENTS.md.
```

### Phase 4: Hardening

```text
Phase 4: threat-model authentication, authorization, payments, file uploads and
webhooks; add rate limiting, input limits and security headers; run a dependency
audit, a performance pass and an accessibility pass. List findings by severity and
fix high and critical ones.
```

### Phase 5: Release

```text
Phase 5: prepare a staging deployment and a release checklist: migrations, health
checks, /version matching the commit, smoke tests, monitoring and a rollback plan.
Do not deploy to production.
```

Deploy to staging first. **You** approve production; `AGENTS.md` forbids the agent from deploying without that approval.

## 5. Switching tools mid-project

Everything an agent needs is in the repository: the spec, the architecture, the decisions log and the project commands. You can plan in one tool, build features in another and review in a third. Start the new tool with:

```text
Read AGENTS.md, docs/SPEC.md, docs/ARCHITECTURE.md and docs/ARCHITECTURE_DECISIONS.md,
check git log and git status, then continue with: <next task>.
```

Use one branch per tool or task so two agents never edit the same files.

## Rules that keep it working

- **Review the spec.** Phase 0 output is the highest-leverage thing you check.
- **Keep "Project commands" in `AGENTS.md` accurate.** Agents verify their work with them; wrong commands mean meaningless checks.
- **Edit sources, not outputs.** Change `toolkit.config.json` or `.agents/skills/`, then run `python scripts/sync_toolkit.py`. Never hand-edit `.mcp.json`, `.cursor/mcp.json`, `opencode.json`, `.codex/config.toml`, `.gemini/settings.json`, `.agents/mcp_config.json` or `.claude/skills/`.
- **Read every completion report.** Do not accept "tests pass" without the actual command output.
- **Give agents only development or staging credentials.** Never production keys.
- **Use `docs/QUALITY-GATES.md`** to test that your tool setup behaves before trusting it with real work.

## Troubleshooting

| Problem | Fix |
|---|---|
| A tool doesn't see an MCP server | Is it `enabled` in `toolkit.config.json`, and is the tool listed in `tools`? Run `python scripts/sync_toolkit.py`, then restart the tool. |
| Codex has no MCP servers | Trust the project in Codex. |
| Claude Code doesn't see a skill | Run `python scripts/sync_toolkit.py` (it mirrors `.agents/skills/` into `.claude/skills/`) and start a new session. |
| Cursor, OpenCode or Copilot shows each skill twice | They read both skill folders. If nobody uses Claude Code, remove `claude-code` from `tools` and sync. |
| Sync says a placeholder must be replaced | Edit the server's URL in `toolkit.config.json` (e.g. `YOUR_PROJECT_REF` for Supabase). |
| Sync refuses to overwrite a file | You have a hand-written entry with the same name; rename or remove it, then sync again. |
