# Changelog

## Unreleased

### Added
- **Skill library:** 65 third-party skills from 15 upstream repositories in `skills-library/`, each pinned to a commit with its license, grouped into 15 profiles (`core`, `docs`, `security`, `web`, `testing`, `react-native`, `ios`, `android`, `postgres`, `supabase`, `prisma`, `api`, `devops`, `ai-apps`, `authoring`).
- `skillProfiles` and `skills` in `toolkit.config.json`; `sync_toolkit.py` copies enabled skills into `.agents/skills/` for every tool and removes disabled ones without touching hand-written skills.
- `scripts/vendor_skills.py`: sparse, shallow, pinned fetch of library skills; refuses unlicensed skills; flags remote execution, skill installation, tool pre-approval, load-time commands and settings/hooks writes for review.
- Superpowers workflow (`core` profile) on by default.
- Free MCP servers (off by default): DeepWiki, Microsoft Learn, AWS Knowledge, Cloudflare docs, Exa, Next.js devtools (telemetry disabled), shadcn, Git.
- MIT license for the toolkit (vendored skills keep their upstream licenses).
- Toolkit CI on Linux and Windows with pinned actions; `SECURITY.md`, `CONTRIBUTING.md`, `docs/SKILLS-CATALOG.md`.

### Security
- Excluded after manual review: Impeccable (downloads a closed binary; can write agent hook/settings files) and shadcn skill (runs unpinned `npx shadcn@latest` on load). `security` profile is opt-in because two of its skills pre-approve `Bash`.

## 0.1.0

- Universal rules (`AGENTS.md`) with adapters for Claude Code and Gemini CLI.
- `toolkit.config.json` + `sync_toolkit.py` generating MCP configs for Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Antigravity and Copilot, plus the Claude Code skill mirror.
- `install_toolkit.py`, getting-started guide, marketplace research, per-tool adapter documentation.
