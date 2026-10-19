# Curated Skills Installation

This is the compact install path for new projects. Read `MARKETPLACE-RESEARCH.md` for why each source was selected and the caveats.

## Recommended baseline

### 1. Install the Skills CLI (run through npx, no global install required)

```bash
npx skills --help
```

It supports many coding agents and the portable Agent Skills format. Review the current supported agent list before selecting targets.

### 2. Preview the primary full-lifecycle pack

```bash
npx skills add addyosmani/agent-skills --list
```

Then install interactively from the repository root:

```bash
npx skills add addyosmani/agent-skills
```

Choose the project-local location when the skills should be reviewed and shared with a repo/team. Use global installation only when the same skill should affect all projects. Keep this toolkit's `AGENTS.md` as the project's policy layer.

Upstream special-case: the Addy repository explains that per-skill CLI installs omit the top-level shared `references/` directory. If the chosen skill uses one of those checklists, install through the full/native repository integration or copy the specific needed reference into the installed skill and confirm the path is valid.

### 3. Add web/mobile framework skills

Preview:

```bash
npx skills add vercel-labs/agent-skills --list
```

Install the current specialist skills:

```bash
npx skills add vercel-labs/agent-skills --skill react-best-practices --skill web-design-guidelines --skill react-native-guidelines
```

These are relevant for React/Next.js web applications and React Native/Expo mobile applications. They are not a replacement for framework documentation, accessibility tests, or device testing.

### 4. Explicitly target multiple agents (optional)

Example with the Skills CLI's current target names:

```bash
npx skills add vercel-labs/agent-skills --skill react-best-practices -a antigravity -a cursor -a claude-code -a gemini-cli -a codex
```

Use only target IDs supported by the current CLI and by the installed agent version. `npx skills add --help` is authoritative if an identifier or flag changes.

### 5. Pick at most one primary workflow framework

Choose either:

- **Addy Osmani Agent Skills** for a comprehensive spec → plan → build → verify → review → ship workflow with explicit security, observability, and CI/CD skills; or
- **Superpowers** for an opinionated brainstorming → plan → TDD → debugging → branch-finish methodology, with parallel-agent patterns.

You can use focused Vercel framework skills alongside either workflow. Do not install both full workflows and make both mandatory without testing the resulting triggers; duplicated steps can increase context use and produce conflicting plans or completion criteria.

Superpowers native installation examples, always check the upstream README:

- Antigravity CLI: `agy plugin install https://github.com/obra/superpowers`
- Gemini CLI: `gemini extensions install https://github.com/obra/superpowers`
- Claude Code: `/plugin install superpowers@claude-plugins-official`
- Cursor: `/add-plugin superpowers`
- Codex: use its plugin interface and search for `superpowers`.

## MCP onboarding order

1. **Context7** for documentation lookup. Current guided setup: `npx ctx7 setup --project`.
2. **Playwright MCP** for browser interaction. Keep a dedicated automated Playwright test suite and execute it in CI.
3. **GitHub MCP** in read-only mode for repository metadata and CI diagnostics.
4. **Supabase MCP** only when the project uses Supabase, scoped to development/staging with least privilege.

Enable servers in `toolkit.config.json` and run `python scripts/sync_toolkit.py`; it writes each client's own schema and secret-reference syntax (see `docs/AGENT-ADAPTERS.md`).

## After installation

1. Run `npx skills list` and inspect installed paths.
2. Read each installed `SKILL.md` and any references it expects.
3. Confirm the skills do not conflict with `AGENTS.md` or each other.
4. Run an actual small task: ask the agent to plan a minor feature, implement it behind tests, run the tests, and report the exact output.
5. Do not enable production deployment or destructive database tools until explicit approval gates are tested.
