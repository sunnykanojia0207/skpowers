# Changelog

## Unreleased

### Added
- skills.sh registry sweep (129 topics, 1,660 skills): 64 more skills (258 total, 43 profiles). Official vendor profiles auto-selected from the stack: `firebase`, `cloudflare`, `convex`, `clerk`, `neon`, `gsap`, `firecrawl`; auto skills `turborepo`, `fastify-best-practices` (Matteo Collina), `mastra`; `codebase-architecture` profile and `writing-for-agents` from mattpocock/skills; `prisma-upgrade-v7`. Rejected: registry reposts, off-topic leaders, Azure (needs a paid subscription), better-auth (no license), Stitch (needs Stitch MCP), Anthropic document skills (proprietary), skills that install unreviewed skills or CLIs.

## 0.4.0

### Added
- **Automatic skill selection** (`"autoSkills": true`): `sync_toolkit.py` detects the stack from dependencies (npm, Composer, Python), platform files (`go.mod`, `Cargo.toml`, `*.csproj`, `pom.xml`, Gradle, `Podfile`, `pubspec.yaml`, Dockerfile, CI, Terraform) and `docs/PROJECT_BRIEF.md` checkboxes, enables matching profiles and individual skills, and removes ones that stop matching. `--explain` prints the reasons. Profiles that pre-approve shell commands (`security`, `ripwire`) are only suggested. New toolkit skill `select-skills`; `AGENTS.md` tells agents when to rerun it.
- 41 more skills (194 total, 35 profiles): language/framework profiles from jeffallan/claude-skills (`typescript`, `python`, `go`, `rust`, `java`, `dotnet`, `php`, `ruby`, `vue`, `angular`, `flutter`, `cloud`, plus FastAPI, Django, pandas, NestJS, GraphQL, WebSocket, Laravel, Terraform skills and RAG/prompt engineering in `ai-apps`); official Next.js skills (`nextjs`); Vercel `react-view-transitions`, AI SDK skills and `agent-browser`; `vibe-security`, Trail of Bits `sharp-edges`, `entry-point-analyzer`, `property-based-testing`; taste-skill v2 (`design-taste-frontend`). Overlaps resolved in favour of vendor/official skills.
- `firecrawl` MCP server (off; free plan with limited credits). Superpowers updated to upstream `2ce8aa1`.

### Changed
- Removed the paid-only `getlayers` MCP server: every configured server is usable for free.
- Re-checked and still excluded: gstack, Impeccable. Documented, not vendored: GSD Core and pstack (alternative workflows), context-mode (Elastic License), claude-mem (plugin with hooks and a worker), Firecrawl skills (AGPL), unlicensed Vercel skills.

## 0.3.0

### Added
- `ui-polish` profile with 15 MIT skills from Emil Kowalski (`emilkowalski/skills`): animation craft, performance and reviews, Apple-style interaction, worst-case data testing, mobile-web polish; `animate-expo` added to `react-native`, `write-swift` to `ios`, `ask-sonner` available individually.
- 52 design skills in four new profiles: `interface-craft` (jakubkrehel/skills), `ux-design` and `ux-research` (Owl-Listener/designer-skills), `anti-slop` (MengTo/Skills); individual `landing-page-design` (elayadesign) and `tastemaker` (codeswithroh). Emil Kowalski's skills confirmed current. garden-skills and the rest of MengTo's and designer-skills' collections documented, not vendored. None of these repositories publishes an MCP server.
- `magic-ui` skill from `magicuidesign/magicui` (MIT), available individually via `"skills": ["magic-ui"]`, and the read-only `magicui` MCP server (`@magicuidesign/mcp@2.0.0`, off by default).
- GetLayers and GSAPify listed as design resources (the paid-only `getlayers` MCP server was later removed to keep every configured server free to use).
- `design-memory` profile (MC Dean's `design-context` skills, MIT); `writing-skills` from Superpowers v7.0.0 added to `authoring`; habitat documented as a design-system tool with a pinned commit.
- `ripwire` profile (17 Apache-2.0 skills from Red Hat's ripwire, pinned to v0.6.7) and `ripwire` MCP server (off by default), with a pinned, checksum-verified, project-local setup instead of the upstream `curl | bash` global installer.
- GitHub Spec Kit v1.2.2 documented as an alternative to the `core` workflow, using the `codex` integration so its skills reach every tool.
- `21st` MCP server (off by default) via the pinned `@21st-dev/magic` proxy with `API_KEY_21ST`.
- "Design resources and guardrails" in `docs/SKILLS-CATALOG.md`: awesome-design-md and designmd.app templates, `@shadcn/lint`, Beautiful UI; `DESIGN.md` step in the getting-started guide.
- Reviewed and not vendored: prompts.chat (community persona prompts; MCP feeds untrusted text to agents), `find-skills` (global `-y` installs), Beautiful UI (no official skill), Claude Code Templates (aggregator writing hooks/settings).

## 0.2.0

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
