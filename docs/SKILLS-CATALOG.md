# Skills Catalog

The toolkit ships **272 vetted third-party skills** in `skills-library/`, grouped into profiles. Every skill is free and openly licensed. **You don't have to pick them:** with `"autoSkills": true` (the default) `python scripts/sync_toolkit.py` reads the project and enables the matching profiles, and only those skills are copied into `.agents/skills/`, so every tool sees the same small, relevant set.

```bash
python scripts/sync_toolkit.py --explain   # what is picked and why
python scripts/sync_toolkit.py             # apply
```

**What triggers a profile** (the "Auto" column below): dependencies in `package.json`, `composer.json`, `pyproject.toml` / `requirements*.txt`; files such as `go.mod`, `Cargo.toml`, `*.csproj`, `pom.xml`, `Podfile`, `Dockerfile`, `.github/workflows/`, `*.tf`; and the platform checkboxes in `docs/PROJECT_BRIEF.md` (`- [x] Web`, `iOS`, `Android`, `Public API`, `Admin portal`, `AI/LLM features`). Rerun the sync when requirements change; profiles that no longer match are removed, hand-written skills never are. Agents do this through the `select-skills` skill.

To force something on regardless of detection, list it in `toolkit.config.json`; to switch detection off, set `"autoSkills": false`:

```json
"skillProfiles": ["core", "docs", "ux-design"],
"skills": ["landing-page-design"]
```

**Individual skills** (no profile): auto-enabled when detected: `vibe-security` (auth, payments or database code), `ask-sonner` (sonner), `magic-ui` (Magic UI registry), `ai-sdk` (Vercel AI SDK), `fastapi-expert`, `django-expert`, `pandas-pro`, `nestjs-expert`, `graphql-architect`, `websocket-engineer`, `laravel-specialist`, `terraform-engineer`, `turborepo` ([vercel/turborepo](https://github.com/vercel/turborepo), `turbo.json`), `fastify-best-practices` ([mcollina/skills](https://github.com/mcollina/skills), Fastify's lead maintainer), `mastra` ([mastra-ai/skills](https://github.com/mastra-ai/skills)). By name only: `landing-page-design` ([elayadesign](https://github.com/elayadesign/ai-design-skills)), `tastemaker` ([codeswithroh](https://github.com/codeswithroh/tastemaker)), `design-taste-frontend` ([Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) v2), `agent-browser` ([vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)), `migrate-ai-sdk-v6-to-v7` ([vercel/ai](https://github.com/vercel/ai)). Pair `magic-ui` with the read-only `magicui` MCP server.

**How skills were chosen:** a skills.sh registry sweep on 2026-10-24 (`npx skills find` over 129 engineering topics, 1,660 unique skills ranked by installs, reposts detected by the same skill name under several owners), an earlier 40-query sweep and the SkillsMP, MCP Market, AI Skill Market and SkillsMK reviews in [MARKETPLACE-RESEARCH.md](MARKETPLACE-RESEARCH.md), plus repositories suggested during review. Only original upstream repositories with a redistributable license and recent activity were accepted; where two skills covered the same need, the vendor's own or the more specific one was kept (see "Overlaps resolved"). Every included skill was read for prompt injection, remote execution, telemetry and destructive operations. Exact commits, licenses and automated review flags: [THIRD_PARTY_NOTICES.md](../skills-library/THIRD_PARTY_NOTICES.md).

## Profiles

| Profile | Auto | Skills | Source (license) |
|---|---|---|---|
| `core` | always | brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, test-driven-development, systematic-debugging, verification-before-completion, requesting-code-review, receiving-code-review, using-git-worktrees, finishing-a-development-branch, using-superpowers | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| `docs` | always | architecture-decision-records | [wshobson/agents](https://github.com/wshobson/agents) (MIT) |
| `web` | React/Next/Vue/Svelte/Astro/Angular/Vite dep, brief Web or Admin portal | vercel-react-best-practices, vercel-composition-patterns, vercel-react-view-transitions, frontend-design, performance, core-web-vitals, accessibility, best-practices, web-quality-audit | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (MIT per skill), [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0), [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) (MIT) |
| `nextjs` | `next` dep | next-dev-loop, next-bundle-optimizer, next-cache-components-adoption, next-cache-components-optimizer, next-partial-prefetching-adoption, next-partial-prefetching-optimizer | [vercel/next.js](https://github.com/vercel/next.js) (MIT, official) |
| `testing` | web UI or Playwright dep | playwright-best-practices, webapp-testing, property-based-testing | [currents-dev](https://github.com/currents-dev/playwright-best-practices-skill) (MIT), anthropics/skills (Apache-2.0), [trailofbits/skills](https://github.com/trailofbits/skills) (CC-BY-SA-4.0) |
| `interface-craft` | any UI platform | better-accessibility, better-colors, better-interface, better-layout, better-typography, better-ui, better-writing, interface-review, build-design, explain-interface, state-machine, break, variant | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| `ui-polish` | animation library (framer-motion, motion, gsap, reanimated…) | emil-design-eng, animate, animation-performance, animation-vocabulary, review-animations, improve-animations, find-animation-opportunities, apple-design, mobile-native, break-ui, pick-ui-library, prototype | [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT) |
| `react-native` | `expo` / `react-native` dep, brief iOS + Android | vercel-react-native-skills, react-native-best-practices, upgrading-react-native, expo-native-ui, expo-router, expo-data-fetching, expo-dev-client, expo-upgrade, animate-expo | vercel-labs (MIT), [callstackincubator](https://github.com/callstackincubator/agent-skills) (MIT), [expo/skills](https://github.com/expo/skills) (MIT), emilkowalski (MIT) |
| `ios` | `Package.swift`, `Podfile`, `.xcodeproj` (not React Native), brief iOS only | swiftui-pro, write-swift | [twostraws](https://github.com/twostraws/SwiftUI-Agent-Skill) (MIT), emilkowalski (MIT) |
| `android` | Gradle with `com.android`, `AndroidManifest.xml` (not React Native), brief Android only | jetpack-compose-performance, adaptive, navigation-3, edge-to-edge, testing-setup, android-intent-security, android-permissions-security | [android/skills](https://github.com/android/skills) (Apache-2.0, Google) |
| `flutter` | Flutter in `pubspec.yaml` | flutter-expert | [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) (MIT) |
| `typescript` | `typescript` dep or `tsconfig.json` | typescript-pro | jeffallan (MIT) |
| `python` | `pyproject.toml`, `requirements*.txt`, `setup.py`, `Pipfile` | python-pro (+ fastapi-expert, django-expert, pandas-pro when used) | jeffallan (MIT) |
| `go` / `rust` | `go.mod` / `Cargo.toml` | golang-pro / rust-engineer | jeffallan (MIT) |
| `java` | `pom.xml` or non-Android Gradle | java-architect, spring-boot-engineer | jeffallan (MIT) |
| `dotnet` | `*.csproj`, `*.fsproj`, `*.sln` | csharp-developer, dotnet-core-expert | jeffallan (MIT) |
| `php` / `ruby` | `composer.json` / Rails in `Gemfile` | php-pro (+ laravel-specialist) / rails-expert | jeffallan (MIT) |
| `vue` / `angular` | `vue`, `nuxt` / `@angular/core` dep | vue-expert / angular-architect | jeffallan (MIT) |
| `postgres` | pg drivers, Prisma `postgresql`, postgres container, Supabase | supabase-postgres-best-practices | [supabase/agent-skills](https://github.com/supabase/agent-skills) (MIT) |
| `supabase` | `@supabase/*` dep, `supabase/config.toml` | supabase | supabase/agent-skills (MIT) |
| `prisma` | `prisma` / `@prisma/client`, `schema.prisma` | prisma-client-api, prisma-cli, prisma-database-setup, prisma-orm-setup, prisma-upgrade-v7 | [prisma/skills](https://github.com/prisma/skills) (MIT) |
| `api` | Express, Fastify, Hono, NestJS, tRPC, GraphQL, FastAPI, Flask, Django; `openapi.*`; brief Public API | api-design-principles, openapi-spec-generation, document-api-endpoint | wshobson (MIT), [getsentry/skills](https://github.com/getsentry/skills) (Apache-2.0) |
| `devops` | `Dockerfile`, compose files, `.github/workflows/`, `*.tf`, `k8s/`, `helm/` | docker-build-strategies, docker-compose-patterns, docker-destructive-guardrails, github-actions-templates, k8s-manifest-generator | [docker/skills](https://github.com/docker/skills) (Apache-2.0), wshobson (MIT) |
| `cloud` | — (by name) | cloud-architect, terraform-engineer, sre-engineer, monitoring-expert | jeffallan (MIT) |
| `firebase` | `firebase`, `firebase-admin`, `firebase-functions` dep or `firebase.json` | firebase-basics, firebase-auth-basics, firebase-firestore, firestore-rules-creation, firebase-security-rules-auditor, firebase-hosting-basics, firebase-app-hosting-basics, firebase-ai-logic-basics, firebase-data-connect, firebase-remote-config-basics, firebase-crashlytics | [firebase/agent-skills](https://github.com/firebase/agent-skills) (Apache-2.0, official) |
| `cloudflare` | `wrangler.toml`/`wrangler.jsonc`, `wrangler` dep | cloudflare, wrangler, workers-best-practices, workers-profiling, durable-objects, agents-sdk, turnstile-spin | [cloudflare/skills](https://github.com/cloudflare/skills) (Apache-2.0, official) |
| `convex` | `convex` dep or `convex/schema.ts` | convex, convex-quickstart, convex-design, convex-auth, convex-authz, convex-optimize, convex-migrate, convex-test, convex-crons, convex-create-component, convex-reviewer, convex-deploy-guard | [convex/agent-skills](https://github.com/convex/agent-skills) (Apache-2.0, official) |
| `clerk` | any `@clerk/*` dep | clerk, clerk-setup, clerk-nextjs-patterns, clerk-react-patterns, clerk-expo, clerk-custom-ui, clerk-orgs, clerk-webhooks, clerk-testing | [clerk/skills](https://github.com/clerk/skills) (MIT per skill, official) |
| `neon` | `@neondatabase/serverless` dep | neon, neon-postgres, neon-postgres-branches, neon-auth, neon-postgres-egress-optimizer | [neondatabase/agent-skills](https://github.com/neondatabase/agent-skills) (Apache-2.0, official) |
| `gsap` | `gsap` dep | gsap-core, gsap-react, gsap-frameworks, gsap-timeline, gsap-scrolltrigger, gsap-plugins, gsap-performance, gsap-utils | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) (MIT, official) |
| `firecrawl` | Firecrawl SDK dep | firecrawl-build, firecrawl-build-scrape, firecrawl-build-search, firecrawl-build-interact | [firecrawl/skills](https://github.com/firecrawl/skills) (ISC, official) |
| `addy-engineering` | — (by name) | security-and-hardening, observability-and-instrumentation, performance-optimization, ci-cd-and-automation, shipping-and-launch, deprecation-and-migration, api-and-interface-design, frontend-ui-engineering, browser-testing-with-devtools, source-driven-development, context-engineering, git-workflow-and-versioning, code-simplification, documentation-and-adrs | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT). Shared checklists (`references/*-checklist.md`, `definition-of-done.md`) are copied into the skills that link to them. |
| `codebase-architecture` | — (by name) | improve-codebase-architecture, domain-modeling, codebase-design | [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) |
| `ai-apps` | OpenAI, Anthropic, AI SDK, LangChain, LlamaIndex, Google GenAI, MCP SDK dep; brief AI/LLM | evals-start, error-discovery, eval-audit, write-judge-prompt, evaluate-rag, validate-evaluator, mcp-builder, rag-architect, prompt-engineer | [ai-evals-course](https://github.com/ai-evals-course/evals-skills) (Apache-2.0), anthropics (Apache-2.0), jeffallan (MIT) |
| `security` | suggested only (see cautions) | security-review, find-bugs, gha-security-review, vibe-security, sharp-edges, entry-point-analyzer | getsentry (Apache-2.0), [raroque/vibe-security-skill](https://github.com/raroque/vibe-security-skill) (MIT), trailofbits (CC-BY-SA-4.0) |
| `design-memory` | `design-context/index.md` exists | init-design-context, update-design-context | [Owl-Listener/design-context](https://github.com/Owl-Listener/design-context) (MIT) |
| `ux-design` | — (by name) | form-design, error-handling-ux, loading-states, feedback-patterns, navigation-patterns, onboarding-design, search-ux, information-architecture, user-flow-diagram, wireframe-spec, heuristic-evaluation, handoff-spec, design-qa-checklist, component-spec, design-token, accessibility-audit, responsive-design, platform-conventions, dark-mode-design, data-visualization, ux-writing | [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) (MIT) |
| `ux-research` | — (by name) | design-brief, user-persona, jobs-to-be-done, journey-map, interview-script, summarize-interview, usability-test-plan, survey-design, affinity-diagram, competitive-analysis, metrics-definition, a-b-test-design | Owl-Listener/designer-skills (MIT) |
| `anti-slop` | — (by name) | audit-ai-design-slop, no-ai-design-slop, design-first-ui-prompting, animation-systems | [MengTo/Skills](https://github.com/MengTo/Skills) (MIT) |
| `authoring` | — (by name) | skill-creator, writing-skills, writing-for-agents | anthropics (Apache-2.0), obra/superpowers (MIT), mattpocock (MIT) |
| `ripwire` | suggested when `ripwire` is on PATH | 17 ripwire-* skills | [redhat-et/ripwire](https://github.com/redhat-et/ripwire) v0.6.7 (Apache-2.0). Needs the binary; see below. |

## Overlaps resolved ("keep the best")

When a newly suggested collection covered the same need as a library skill, the vendor's own or more specific skill was kept:

| Need | Kept | Not added |
|---|---|---|
| React / Next.js | Vercel `vercel-react-best-practices`, official `next-*` skills | jeffallan `react-expert`, `nextjs-developer` |
| React Native | Vercel, Callstack, Expo | jeffallan `react-native-expert` |
| iOS / Android | `swiftui-pro`, Google `android/skills` | jeffallan `swift-expert`, `kotlin-specialist` |
| Playwright | Currents `playwright-best-practices` | jeffallan `playwright-expert` |
| Review, debugging, TDD | Superpowers `core` | jeffallan `code-reviewer`, `debugging-wizard`, `test-master` |
| Security review | Sentry + vibe-security + Trail of Bits `sharp-edges` | jeffallan `security-reviewer`, `secure-code-guardian` |
| Docker / Kubernetes | Docker official, wshobson manifests | jeffallan `devops-engineer`, `kubernetes-specialist` |
| Postgres | Supabase `supabase-postgres-best-practices` | jeffallan `postgres-pro`, `sql-pro` |
| MCP servers | Anthropic `mcp-builder` | jeffallan `mcp-developer` |
| Architecture, API design | toolkit `architecture-planning`, wshobson `api-design-principles` | jeffallan `architecture-designer`, `api-designer` |
| Workflow | Superpowers | Addy Osmani's workflow half (`spec-driven-development`, `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `code-review-and-quality`, `debugging-and-error-recovery`, `idea-refine`, `interview-me`), GSD Core, pstack, jeffallan `feature-forge` / `spec-miner` (see alternatives) |

## Cautions on included skills

From the manual review. None of these instruct an agent to bypass the user, hide actions or exfiltrate data.

| Skill | Caution |
|---|---|
| `using-superpowers`, `brainstorming` | Deliberately aggressive triggers: Superpowers wants to check for a skill before every response and brainstorm before any creative work. This is how the `core` workflow works; if you prefer a different workflow pack, remove `core`. `brainstorming` can start a local web server (127.0.0.1) and open a browser; its page loads a logo from a remote site. |
| `finishing-a-development-branch` | Its "merge locally" option checks out the base branch, pulls and merges. It asks first, requires typing "discard" to delete work, and never force-pushes unless asked. `AGENTS.md` still forbids pushing to the default branch without approval. |
| `security-review`, `gha-security-review` | Their frontmatter pre-approves the `Bash` tool in Claude Code while the skill is active. This is why `security` is off by default. `curl \| sh` and `rm -rf` in their references are attack examples, not instructions. |
| `testing-setup` (android) | May add Hilt or Koin as a dependency; `AGENTS.md`'s "ask before adding dependencies" rule applies. |
| `webapp-testing` | Ships Python helpers that start your dev server (`shell=True` with the command the agent passes) and drive Playwright. |
| `skill-creator` | Runs evaluation loops with `claude -p`, temporarily writes to `.claude/commands/`, and serves a local review page. |
| `mcp-builder` | Fetches MCP documentation from GitHub as reference; its evaluation script calls the Anthropic API. |
| `docker-build-strategies` | `rm -rf /var/lib/apt/lists/*` appears only as standard Dockerfile cleanup. |
| `upgrading-react-native` | Its Xcode troubleshooting suggests `sudo xcode-select -s …` and `sudo xcodebuild -runFirstLaunch`; the agent must ask before running anything with `sudo`. |
| `web-quality-audit` | `scripts/analyze.sh` is a read-only HTML checker (greps files, prints JSON); needs `jq`. |
| `init-design-context` | Step 4 adds a session-start line ("read design-context/index.md…") to `CLAUDE.md`, `AGENTS.md` or equivalent, creating the file if absent. In this toolkit, have it add the line to `AGENTS.md` only: `CLAUDE.md` and `GEMINI.md` already import it. The skills otherwise only write inside `design-context/` and propose every decision entry before appending it. Complements `DESIGN.md`: the design system lives there, the decision history in `design-context/decisions.md`. |
| `tastemaker` | Broad trigger ("whenever the user asks to build, design, style, or improve a UI"), so it competes with `frontend-design`, `ui-polish` and `anti-slop`: enable one design workflow per project. Writes project memory in `.tastemaker/` and **cross-project memory in your home directory** (`~/.tastemaker/profile.md`, `structure-history.json`, and an illustration library in `~/.ideagram/`). Its scripts download photos from Openverse and icons from Iconify; the only `sudo` is an install hint in an error message. It uses an `inspo` MCP only if one is already connected; no source is published, so none is configured. |
| `interface-craft` vs `ui-polish` | Both include stress-test (`break` / `break-ui`) and variant/prototype pages. They complement each other, but enabling both gives agents two skills for the same job; pick one per project if suggestions conflict. |
| `firebase-basics` | If you use Genkit it suggests `npx skills add genkit-ai/skills` (unreviewed; ask first per `AGENTS.md`), and its setup references explain adding the Firebase MCP server to agent configs. `firebase-ai-logic-basics`, `firebase-remote-config-basics` and `neon` mention `sudo`/global CLI installs (`firebase-tools`, `neonctl`) in setup notes. |
| `clerk-*` | Each pre-approves `WebFetch` (reading Clerk's docs) in Claude Code; no shell pre-approval. `clerk-backend-api`, which pre-approves `Bash`, is not vendored. |
| `mastra` | Offers to install its companion `mastra-factory` skill with `npx skills add`; it asks first. |
| `firecrawl-build-*` | For apps that call the Firecrawl API: a paid service with a limited free plan. |
| jeffallan language skills (`python-pro`, `fastapi-expert`, `golang-pro`, …) | Procedural (workflow, checkpoints, references), but example code is not always correct: `fastapi-expert` imports a non-existent `pydantic.model_config`. Verify APIs against current docs, as `AGENTS.md` requires. Their references mention `sudo`, global installs and `appsettings.json` only as documentation. |
| `next-dev-loop`, `next-cache-components-adoption` | `next-dev-loop` asks for `agent-browser` on PATH and suggests `npm i -g agent-browser@latest` after telling the user to stop and upgrade; `next-cache-components-adoption` installs `next-dev-loop` with `npx skills add` only if it is missing, and the `nextjs` profile always ships it. Global installs still need approval. |
| `agent-browser` | Pre-approves only its own CLI (`Bash(agent-browser:*)`, `npx agent-browser`), and asks for a global `npm i -g agent-browser` install. Opt-in by name; Playwright MCP covers browser checks by default. |
| `design-taste-frontend` | taste-skill v2. Runs Node 22 scripts that drive your local Chrome headless (temporary profile), download openly licensed images from Openverse, Wikimedia, the Met, the Art Institute of Chicago, NASA and archive.org, and write `.taste-skill/` plus `~/.taste-skill/history.json`. Broad trigger for any public web page: one design workflow per project. |
| `vibe-security` | Deliberately broad trigger (any code touching auth, payments, data or secrets); that is why it is auto-enabled for such projects. Documentation only. |
| `sharp-edges`, `entry-point-analyzer`, `property-based-testing` | Trail of Bits, CC-BY-SA-4.0 (share-alike): vendored unmodified with the license; if you modify them, your changed versions must stay CC-BY-SA. `rm -rf` in `sharp-edges` references are examples of dangerous patterns. |
| Superpowers update (2026-10-24) | Upstream slimmed `writing-skills` (removed ~2,100 lines of reference essays) and shortened `subagent-driven-development`, `executing-plans` and `brainstorming`; no skills added or removed, no new risks. |
| `magic-ui` | Tells the agent to run unpinned `npx shadcn@latest init` and `npx shadcn@latest add @magicui/<component>`, which add component source and dependencies to the project. Unlike the excluded shadcn skill it runs nothing on load and pre-approves nothing; `AGENTS.md`'s "ask before adding dependencies" applies. Requires React/Next.js with Tailwind. |
| `writing-skills` | Ships `render-graphs.js`, which renders a skill's Graphviz diagrams to SVG with the local `dot` binary (no shell, no network). |
| `ripwire-*` (all 17) | Each pre-approves unrestricted `Bash` (and `ripwire-opt-remarks` also `Edit`) in Claude Code while active, not only `ripwire` commands. The skills only document the upstream installer, they never tell the agent to run it. Keep the profile opt-in, and install the binary yourself as described below. |
| `pick-ui-library` | An opinionated list that includes the author's own libraries (Sonner, Vaul). It runs only when invoked; adding any library is still a dependency change that `AGENTS.md` says to ask about first. |
| `emil-design-eng`, `apple-design` | Broad design-philosophy triggers that can overlap `frontend-design` in the `web` profile; they complement it (motion and polish vs. visual direction), but disable `ui-polish` if suggestions conflict. `apple-design` here is Emil Kowalski's MIT skill, not the unlicensed dickwu skill excluded below. |

## Reviewed and excluded

| Skill | Why it is not vendored | If you still want it |
|---|---|---|
| Impeccable (`pbakaus/impeccable`, [impeccable.style](https://impeccable.style/)) | Apache-2.0 and popular, but every session the skill runs a launcher that downloads a self-contained binary on first run (checksum comes from the same release), and its opt-in `hooks on` command writes agent hook/settings files including user-global `~/.claude/settings.json`. Re-checked 2026-10-19 (CLI v4.6.0) and 2026-10-24 (engine v0.1.17): unchanged. | `npx skills add pbakaus/impeccable --skill impeccable`, after reading its hooks documentation |
| shadcn (`shadcn-ui/ui`) | Runs unpinned `npx shadcn@latest` automatically when the skill loads and pre-approves every shadcn subcommand, including installs from community registries. It is `user-invocable: false`, so it auto-triggers in any project with `components.json`. Re-checked 2026-10-24 (upstream commit `4233ed1`, which added DESIGN.md support): unchanged, kept excluded. | Use the `shadcn` MCP server in `toolkit.config.json` (pinned, off by default) |
| Vercel `web-design-guidelines`, Anthropic `doc-coauthoring`, Vercel `use-ai-sdk` | No license declared, so they cannot be redistributed. | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines`; `npx skills add vercel/ai` |
| Trail of Bits skills | CC-BY-SA-4.0 (share-alike) and packaged as plugins. | `/plugin marketplace add trailofbits/skills` (Claude Code), `codex plugin marketplace add trailofbits/skills` |
| UI/UX Pro Max | Design-style data overlapping `frontend-design`, `design-taste-frontend` and `tastemaker`; not reviewed for vendoring. | See [TOOLKIT-GUIDE.md](TOOLKIT-GUIDE.md) §3.4 |
| `apple-design` (dickwu) | No license; bundles Apple's guideline text. | Install for personal use only |
| Registry reposts and off-topic leaders (2026-10-24 sweep) | Same-named "superpowers" skills under `101-skills`, `magentosh`, `qu-skills`, `skills-shell`, `its-a-skill-issue`, `bankai-skills` (AI video, Twitter automation); HeyGen video, Lark/Feishu, ML-paper reproduction, e-commerce and persona skills. | — |
| Microsoft `azure-skills` (MIT, 93 skills) | Built around the Azure MCP and Foundry MCP servers, which need an Azure subscription. | Microsoft's official Azure plugin, for Azure projects |
| `better-auth/skills` | No license in the repository or the skills. | `npx skills add better-auth/skills` per project |
| Google `stitch-skills` (Apache-2.0) | Every skill drives the Stitch MCP (`stitch*` tools), including `design-md`. | Install with the Stitch MCP if you use Google Stitch |
| Anthropic `docx`, `xlsx`, `pptx` | Proprietary (source-available) license. | Use them from Anthropic's own distribution |
| `nextjs-on-cloudflare`, `firecrawl-build-onboarding`, Firecrawl CLI skills | Install unreviewed skills or CLIs without asking (`npx skills add cloudflare/vinext`; Firecrawl CLI plus skills that pre-approve `Bash(firecrawl *)`). | Install by hand after reading |
| mattpocock `tdd`, `code-review`, `diagnosing-bugs`, `grill-me`, `to-spec`, `to-tickets`, `implement`, `prototype` | Compete with the `core` workflow (or clash by name); only architecture and writing skills are vendored. | Use Matt Pocock's set instead of `core`, not alongside it |
| gstack (`garrytan/gstack`, MIT) | Re-checked 2026-10-24: setup still compiles binaries and downloads Bun via `curl`, ships `/gstack-upgrade` plus team-mode auto-update, and `setup-browser-cookies` imports cookies from your real browser. | Browse for ideas only |
| context-mode (`mksglu/context-mode`) | Elastic License 2.0 (source-available, not open source) and a plugin built on MCP plus hooks that route every tool call. | `/plugin marketplace add mksglu/context-mode` in Claude Code, after reading its hooks |
| claude-mem (`thedotmack/claude-mem`, Apache-2.0) | A plugin, not a skill: lifecycle hooks plus a background worker capture everything the agent does, compress it with an AI model and inject it into later sessions; optional cloud sync and a hosted default on some hosts. Use `<private>` tags for secrets. | `/plugin marketplace add thedotmack/claude-mem`; review its privacy and provider settings first |
| Firecrawl skills (`firecrawl/firecrawl`) | AGPL-3.0 (strong copyleft) in the main repository. Its MIT MCP server is configured instead (`firecrawl`, off; free plan has limited credits). | `npx skills add firecrawl/firecrawl --skill <name>` per project |
| Vercel `deploy-to-vercel`, `vercel-cli-with-tokens`, `vercel-optimize`, `web-design-guidelines`, `writing-guidelines` | No license declared in the skill or repository, so they cannot be redistributed. | `npx skills add vercel-labs/agent-skills --skill <name>` |
| Vercel AI SDK and Next.js maintainer skills (`add-provider-package`, `backport-pr`, `react-vendoring`, …) | Written for developing those repositories, not for apps that use them. Only `ai-sdk`, `migrate-ai-sdk-v6-to-v7` and the six `next-*` skills are vendored. | — |
| `find-skills` (`vercel-labs/skills`) | Its final step installs skills globally with `npx skills add … -g -y` (no confirmation prompt, every project affected) and ranks candidates by install count, which reposted copies inflate. The toolkit's `marketplace-skill-review` skill and `vendor_skills.py` cover discovery with review. | Use the CLI directly: `npx skills find <query>`, then review and add to `skills-library/library.json` |
| garden-skills (`ConardLi/garden-skills`, MIT) | Mostly Chinese-language content-production skills (article layout, GPT Image 2 generation through an OpenAI-compatible API, motion showreels, web video presentations with TTS) with build scripts and global npm installs; its one UI skill, `web-design-engineer`, overlaps `frontend-design`. | `npx skills add ConardLi/garden-skills --skill <name>` for a specific content task |
| MengTo/Skills (remaining 173) | Niche creative collections: fixed visual styles, WebGL/Three.js effects, Three.js games and combat VFX, SVG illustration styles, 3D materials, Codex-specific workflows. Only the four general skills are in `anti-slop`. | Browse the repository and add a specific skill to `library.json` when a project needs it (for example a Three.js game) |
| `technical-drawing` (jakubkrehel) | Drawings of physical objects; outside app development. | — |
| Remaining designer-skills (78) | Team operations (critique facilitation, governance, negotiation, portfolio), single psychology laws (Fitts, Hick, Miller…) and visual critique variants already covered by `ux-design`, `interface-craft` and `ui-polish`. | Add individual ones to `library.json` as needed |
| prompts.chat (`f/prompts.chat`, formerly awesome-chatgpt-prompts) | Code MIT, prompts CC0. A community prompt library made mostly of "Act as…" persona prompts; its MCP server (`https://prompts.chat/api/mcp`) feeds community-submitted text straight into the agent's context, which is a prompt-injection route. | Browse it for ideas and copy a prompt into your own versioned files after reading it |
| Beautiful UI ([beautifului.dev](https://www.beautifului.dev/)) | A copy-paste component library (MIT) for AI-native interfaces: streaming text, thinking states, approval cards, tool traces, diff tables. Not a skill; the only GitHub skills and registries for it are unofficial ports with 2–21 stars. | When building chat or agent UIs, copy components from the site and record them in `DESIGN.md` |
| mattpocock/skills (`tdd`, `diagnosing-bugs`, `code-review`, `grill-with-docs`) | Very popular, but a competing workflow to `core`; running both produces conflicting instructions. | Use instead of `core`, not alongside it |
| `diagnosing-superpowers` (obra/superpowers) | Troubleshoots the Superpowers plugin itself; not useful inside projects. The other 14 Superpowers skills are vendored (`core` and `authoring`), pinned to v7.0.0. | — |
| Reposted Superpowers copies (`101-skills/superpowers`, `magentosh/superpowers`, `qu-skills/superpowers`, `skills-shell/superpowers`) | Copies of the original with inflated install counts. | Use `obra/superpowers` |
| `anti-detect-browser`, `playwright-stealth-verify` and similar | Bot-detection evasion tooling, not software delivery. | — |
| `android-cli`, `play-policy-insights` (android/skills) | Pipe a remote installer to the shell and install other skills; ship a scraper. | — |
| Claude Code Templates ([aitmpl.com](https://www.aitmpl.com/), `davila7/claude-code-templates`) | MIT and active, but an aggregator: ~900 skills largely collected from other repositories, plus ~590 hook and settings files; its `npx claude-code-templates` installer writes agents, hooks and settings into Claude Code only. | Browse it for ideas; install a skill from its original repository instead, and read any hook before adding it by hand |
| gstack, everything-claude-code, ruflo, moai-adk | All-in-one packs with self-update, binaries or overlapping methodologies. | — |

## ripwire: safe setup

[ripwire](https://github.com/redhat-et/ripwire) is a local C++ CLI and MCP server: a ranked map of the code before the agent reads files, and blast radius, tests-to-run and quality regressions after it edits. The library pins its skills to release **v0.6.7**, so install the same binary version.

Its one-line installer pipes an unpinned script from `main` into `bash` and activates skills **globally** (`~/.claude/skills`, `~/.agents/skills`). In this toolkit, do it pinned and project-local instead:

1. Download `ripwire-0.6.7-<os>-<arch>` and its `.sha256` file from the [v0.6.7 release](https://github.com/redhat-et/ripwire/releases/tag/v0.6.7), compare the checksum, extract, and put the `ripwire` binary on your `PATH`.
2. Add `ripwire` to `skillProfiles` and set `"enabled": true` on the `ripwire` MCP server in `toolkit.config.json`.
3. Run `python scripts/sync_toolkit.py`.
4. Don't run its `skills/install.sh` or `--hook`; the toolkit already provides the skills, and the hooks write to `~/.claude/settings.json` and `~/.codex/hooks.json`.

## Alternative workflow: GitHub Spec Kit

[Spec Kit](https://github.com/github/spec-kit) (MIT, GitHub) is a spec-driven workflow: `/speckit-constitution`, then `/speckit-specify` → `plan` → `tasks` → `implement` → `converge` per feature, plus bug and assessment tracks. It is **an alternative to `core` (Superpowers), not an addition**: both run their own planning loop.

It can't be vendored like the library skills: `specify init` generates its skills from templates together with `.specify/` scripts and memory files. To use it in every tool:

```bash
# 1. Commit first: init merges files into the existing directory.
git add -A && git commit -m "Before Spec Kit"
# 2. Turn off Superpowers: remove "core" from skillProfiles, then
python scripts/sync_toolkit.py
# 3. Install a pinned CLI and initialise with the codex integration, which writes
#    skills to .agents/skills (read by Codex, Cursor, OpenCode, Gemini CLI,
#    Antigravity and Copilot).
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.2
specify init --here --force --non-interactive --integration codex
# 4. Mirror the new skills into .claude/skills for Claude Code, then review.
python scripts/sync_toolkit.py
git diff
```

Check that `specify init` did not change `AGENTS.md`; if it added content, merge it so `AGENTS.md` stays the single rule file.

### Other alternative workflows

Like Spec Kit, these **replace** `core` (remove it from `skillProfiles` first) and install as plugins per tool rather than as library skills:

- **Addy Osmani Agent Skills** ([addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), MIT): the full spec → plan → build → test → review → ship workflow plus its session hooks, via its plugin or `npx skills add addyosmani/agent-skills`. Its 14 production-engineering skills are already in the library as `addy-engineering` and work with either workflow.

- **GSD Core** ([open-gsd/gsd-core](https://github.com/open-gsd/gsd-core), MIT): `npx @opengsd/gsd-core@latest`, which asks for your runtime and global or local install. The old `npx get-shit-done-cc` package points to an archived repository; don't use it.
- **pstack** ([cursor/plugins/pstack](https://github.com/cursor/plugins/tree/main/pstack), MIT, Lauren Tan): `/add-plugin pstack` in Cursor; in Claude Code `/plugin marketplace add cursor/plugins` then `/plugin install pstack@cursor-plugins`. Its setup writes `~/.claude/rules/pstack-models.md`.

## Design resources and guardrails

Not skills, but they work with the `AGENTS.md` rule that every tool follows a root `DESIGN.md`.

| Resource | What it gives you | How to use it safely |
|---|---|---|
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT) | 85 `DESIGN.md` files analysing well-known brands' design systems | Use one as a structural starting point, then replace colors, type and voice with your own. Shipping a UI that imitates a real brand risks trademark and trade-dress problems. |
| [designmd.app](https://designmd.app/) | Library of DESIGN.md templates in Google's format | Same: adapt, don't clone. No license is named. |
| [Refero Styles](https://styles.refero.design/) (beta) | Design systems (colors, type, spacing, components, DESIGN.md) taken from product sites such as Linear, Notion and Figma; also offers an MCP connection | Same: adapt, don't clone. No license or pricing is published, and its MCP setup could not be verified, so it is not in `toolkit.config.json`. |
| [shadcn-ui/lint](https://github.com/shadcn-ui/lint) (`@shadcn/lint`, MIT) | ESLint/Oxlint rules for Tailwind v4 design systems (React, Svelte, Vue). Errors tell the agent the allowed fix, e.g. "use a Button size, not padding". | Add it as a pinned dev dependency during Phase 1 and run it in CI. Read its `SETUP.md` yourself instead of telling an agent to fetch and follow it from `main`. |
| [habitat](https://github.com/Owl-Listener/habitat) (MIT, MC Dean) | Toolkit for making an existing design system legible to agents: AI reads the facts from Figma, interviews you for the reasons, marks unknowns `TODO`, and measures the improvement on real screens. Includes a validator, a code checker and a local MCP server (no network calls). | New (June 2026, no stars yet). Its quick start runs unpinned `npx github:Owl-Listener/habitat`; pin a commit instead (`npx github:Owl-Listener/habitat#7d5122d init`, reviewed 2026-10-19). `init` installs Claude Code skills and appends rule blocks to `AGENTS.md`, `CLAUDE.md` and `.cursor/rules/habitat.mdc`: keep the block in `AGENTS.md` and remove the duplicates. |
| [GetLayers](https://www.getlayers.ai/) (textura.agency) | Library of "cinematic" website prompts, templates, 3D scenes, palettes and fonts; free curated set, paid plans with a commercial licence | Copy prompts by hand on the free tier. Its MCP (`https://mcp.getlayers.ai/mcp`) needs a paid Full Stack Lifetime plan, so it is not configured: the toolkit only ships servers usable for free. Returned template code is third-party: review before committing. |
| [GSAPify](https://gsapify.com/) | Copy-paste GSAP text and UI animation effects, plugin guides, and a web AI generator (account; free tier, paid plans) | Copy effects by hand. Premium GSAP plugins (SplitText, MorphSVG) carry GreenSock's own license terms. No repository, skill or MCP. Pair with the `ui-polish` profile for motion judgement. |
| [Beautiful UI](https://www.beautifului.dev/) (MIT) | Copy-paste components for AI chat/agent interfaces | Copy components directly; record them in `DESIGN.md`. |
| 21st MCP (`21st` in `toolkit.config.json`, off) | Search 21st.dev's React/Tailwind component catalog; paid retrieval and generation | Enable with a key in `API_KEY_21ST`. Generated components are third-party code: review before committing. |

## Updating

```bash
python scripts/vendor_skills.py --update        # all sources to their latest commit
python scripts/vendor_skills.py --source expo   # one source
git diff skills-library/                        # review every change, including new review flags
python scripts/sync_toolkit.py
```
