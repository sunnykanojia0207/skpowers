# Changelog

## Unreleased

### Added (2026-10-31)
- **Project documentation system** adapted from "The Vibe Coding Blueprint": `docs/PROJECT_BRIEF.md` is now a full PRD (platform checkboxes kept), and `templates/docs/` adds ARCHITECTURE, ARCHITECTURE_DECISIONS, DATABASE, API, SECURITY, UX_FLOWS, CODE_STYLE and TESTING templates that `install_toolkit.py` copies into a project's `docs/` (index as `docs/DOCS-INDEX.md`). `AGENTS.md`: read the docs the change touches, don't invent what they don't contain, update them with behaviour changes, and ask when documents conflict. Getting started gains bug-fix and pre-release review prompts and before/during/after checklists.
- **Design skills:** official Vue (`vuejs-ai/skills`, 6) and Angular (`angular-developer`) skills replace jeffallan's; `ant-design` (auto with `antd`), `expo-design-system`, ibelick's `create-design-md` and `ui-fixes` profile, `hue`, `interface-design`, `color-expert`. `vendor_skills.py` supports skills at a repository root (path `"."`). Upstream updates pulled for Hallmark (two themes), UI UX Pro Max, Jakub Krehel, Emil Kowalski and Anthropic (`mcp-builder` now targets MCP TypeScript SDK v2); Taste Skill already current. Impeccable, Stitch and the shadcn skill stay excluded.

### Changed
- **Faster setup:** projects no longer get a copy of the 37 MB skills library. Clone the toolkit once to `~/.skpowers`; `install_toolkit.py` (target defaults to the current folder) copies only rules, config, toolkit skills and the sync script, records the library location in git-ignored `.agents/.toolkit-home`, and copies just the skills the project uses. Measured on a Next.js + Prisma project: 15.8 s / 43 MB / 3,093 files → 6.0 s / 4.8 MB / 977 files. `--update` refreshes toolkit-owned files without touching yours.
- The sync finds the library in this repo, `$SKPOWERS_HOME`, the recorded install location or `~/.skpowers`; without one it leaves copied skills in place instead of removing them.
- Test suite 195 s → 68 s by sharing the library.

### Added
- **Skills picked from the request:** `sync_toolkit.py --suggest "<task>"` lists matching skills that are already enabled, then ranks library profiles and skills (synonyms, best-member scoring, stack-specific results only when the request names the stack); `--enable` / `--disable` update the config and sync in one step. `select-skills` and `AGENTS.md` tell agents to do this for each new request. `--quiet` for short sync output.
- Python virtual environments: `AGENTS.md` rule plus toolkit skill `python-venv` — every Python command runs in the project's `.venv` (created with uv or `venv` if missing, interpreter called directly on Windows/macOS/Linux), never the global or system Python; `.venv/` ignored by git.
- Design batch (14 repositories reviewed): `ui-ux-pro-max`, `hallmark`, `dimensional-drawing` and `dimensional-drawing-motion` as individual skills; `AGENTS.md` now has agents lint `DESIGN.md` with Google's pinned `@google/design.md@0.4.0` CLI (spec, token references, WCAG contrast). React Bits, Canvas UI and the DESIGN.md spec added to design resources.
- taste-skill and elayadesign updated to upstream (copy, chart and inspector changes; no new network or process use). Emil Kowalski, Magic UI and GSAP already current.
- Not vendored: scroll-world (paid Higgsfield, broad tool pre-approval), open-design (an application), UI/UX Pro Max's paid-image-generation skills. Impeccable stays excluded; awesome-design-md stays a documented template source.

## 0.7.0

### Added
- Anthropic `claude-api` skill (Apache-2.0), auto-enabled when a project depends on the Anthropic SDK or Agent SDK. The rest of anthropics/skills reviewed: proprietary (`docx`, `pdf`, `pptx`, `xlsx`), unlicensed (`doc-coauthoring`) or not software delivery.

## 0.6.0

### Added
- `addy-engineering` profile: 14 production-engineering skills from addyosmani/agent-skills (security hardening, observability, performance, CI/CD, shipping, migration, API/frontend engineering, DevTools testing, source-driven development, context engineering, git workflow, simplification, docs/ADRs). Its workflow half stays an alternative to `core` (overlaps Superpowers; `test-driven-development` clashes by name).
- `vendor_skills.py` `sharedFiles`: repository-level files a skill links to (Addy's shared checklists) are copied in unmodified.

### Fixed
- Single-source vendoring left removed skills in `THIRD_PARTY_NOTICES.md`; the validator now checks notices match `library.json` exactly.

## 0.5.0

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
