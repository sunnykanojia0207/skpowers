# Skills Catalog

The toolkit ships **101 vetted third-party skills** in `skills-library/`, grouped into profiles. Turn profiles on per project in `toolkit.config.json`, then run `python scripts/sync_toolkit.py`; only enabled skills are copied into `.agents/skills/`, so every tool sees the same small, relevant set.

```json
"skillProfiles": ["core", "docs", "web", "testing", "postgres"],
"skills": ["mcp-builder"]
```

`skills` adds individual library skills without their whole profile. Skills in no profile: `ask-sonner` (add it if the app uses the Sonner toast library) and `magic-ui` (add it if the app uses [Magic UI](https://magicui.design) animated components; [magicuidesign/magicui](https://github.com/magicuidesign/magicui), MIT). Pair `magic-ui` with the read-only `magicui` MCP server ([magicuidesign/mcp](https://github.com/magicuidesign/mcp), MIT, pinned 2.0.0) to let agents search the component registry.

**How skills were chosen (2026-10-19):** discovery with `npx skills find` across 40 engineering queries (install counts from the skills.sh registry), cross-checked against the SkillsMP, MCP Market, AI Skill Market and SkillsMK reviews in [MARKETPLACE-RESEARCH.md](MARKETPLACE-RESEARCH.md). Only original upstream repositories with a redistributable license and recent activity were accepted; reposted copies (for example the several `*/superpowers` forks with inflated install counts) and browser-evasion skills were rejected. Every included skill was read by hand for prompt injection, remote execution, telemetry and destructive operations. Exact commits, licenses and automated review flags: [THIRD_PARTY_NOTICES.md](../skills-library/THIRD_PARTY_NOTICES.md).

## Profiles

| Profile | Default | Skills | Source (license) |
|---|---|---|---|
| `core` | **on** | brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, test-driven-development, systematic-debugging, verification-before-completion, requesting-code-review, receiving-code-review, using-git-worktrees, finishing-a-development-branch, using-superpowers | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| `docs` | **on** | architecture-decision-records | [wshobson/agents](https://github.com/wshobson/agents) (MIT) |
| `security` | off | security-review, find-bugs, gha-security-review | [getsentry/skills](https://github.com/getsentry/skills) (Apache-2.0) |
| `web` | off | vercel-react-best-practices, vercel-composition-patterns, frontend-design, performance, core-web-vitals, accessibility, best-practices, web-quality-audit | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (MIT), [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0), [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) (MIT) |
| `ui-polish` | off | emil-design-eng, animate, animation-performance, animation-vocabulary, review-animations, improve-animations, find-animation-opportunities, apple-design, mobile-native, break-ui, pick-ui-library, prototype | [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT) |
| `testing` | off | playwright-best-practices, webapp-testing | [currents-dev/playwright-best-practices-skill](https://github.com/currents-dev/playwright-best-practices-skill) (MIT), anthropics/skills (Apache-2.0) |
| `react-native` | off | vercel-react-native-skills, react-native-best-practices, upgrading-react-native, expo-native-ui, expo-router, expo-data-fetching, expo-dev-client, expo-upgrade, animate-expo | vercel-labs/agent-skills (MIT), [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills) (MIT), [expo/skills](https://github.com/expo/skills) (MIT), emilkowalski/skills (MIT) |
| `ios` | off | swiftui-pro, write-swift | [twostraws/SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill) (MIT), emilkowalski/skills (MIT) |
| `android` | off | jetpack-compose-performance, adaptive, navigation-3, edge-to-edge, testing-setup, android-intent-security, android-permissions-security | [android/skills](https://github.com/android/skills) (Apache-2.0, Google) |
| `postgres` | off | supabase-postgres-best-practices | [supabase/agent-skills](https://github.com/supabase/agent-skills) (MIT) |
| `supabase` | off | supabase | supabase/agent-skills (MIT) |
| `prisma` | off | prisma-client-api, prisma-cli, prisma-database-setup, prisma-orm-setup | [prisma/skills](https://github.com/prisma/skills) (MIT) |
| `api` | off | api-design-principles, openapi-spec-generation, document-api-endpoint | wshobson/agents (MIT), getsentry/skills (Apache-2.0) |
| `devops` | off | docker-build-strategies, docker-compose-patterns, docker-destructive-guardrails, github-actions-templates, k8s-manifest-generator | [docker/skills](https://github.com/docker/skills) (Apache-2.0), wshobson/agents (MIT) |
| `ai-apps` | off | evals-start, error-discovery, eval-audit, write-judge-prompt, evaluate-rag, validate-evaluator, mcp-builder | [ai-evals-course/evals-skills](https://github.com/ai-evals-course/evals-skills) (Apache-2.0), anthropics/skills (Apache-2.0) |
| `authoring` | off | skill-creator, writing-skills | anthropics/skills (Apache-2.0), obra/superpowers (MIT) |
| `design-memory` | off | init-design-context, update-design-context | [Owl-Listener/design-context](https://github.com/Owl-Listener/design-context) (MIT, MC Dean) |
| `ripwire` | off | ripwire-router, -orient, -navigate, -graph-query, -layers, -before-you-build, -reuse-first, -change-check, -quality-bar, -fresh-eyes, -find-bug, -security-scan, -write-tests, -perf-target, -opt-remarks, -handoff, -mcp | [redhat-et/ripwire](https://github.com/redhat-et/ripwire) v0.6.7 (Apache-2.0, Red Hat). Needs the ripwire binary; see below. |

**Typical combinations:** Next.js SaaS → `core docs web ui-polish testing postgres api security devops`. Expo mobile app → `core docs react-native testing api`. Native iOS → `core docs ios`. Native Android → `core docs android`. LLM product → add `ai-apps`.

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
| `magic-ui` | Tells the agent to run unpinned `npx shadcn@latest init` and `npx shadcn@latest add @magicui/<component>`, which add component source and dependencies to the project. Unlike the excluded shadcn skill it runs nothing on load and pre-approves nothing; `AGENTS.md`'s "ask before adding dependencies" applies. Requires React/Next.js with Tailwind. |
| `writing-skills` | Ships `render-graphs.js`, which renders a skill's Graphviz diagrams to SVG with the local `dot` binary (no shell, no network). |
| `ripwire-*` (all 17) | Each pre-approves unrestricted `Bash` (and `ripwire-opt-remarks` also `Edit`) in Claude Code while active, not only `ripwire` commands. The skills only document the upstream installer, they never tell the agent to run it. Keep the profile opt-in, and install the binary yourself as described below. |
| `pick-ui-library` | An opinionated list that includes the author's own libraries (Sonner, Vaul). It runs only when invoked; adding any library is still a dependency change that `AGENTS.md` says to ask about first. |
| `emil-design-eng`, `apple-design` | Broad design-philosophy triggers that can overlap `frontend-design` in the `web` profile; they complement it (motion and polish vs. visual direction), but disable `ui-polish` if suggestions conflict. `apple-design` here is Emil Kowalski's MIT skill, not the unlicensed dickwu skill excluded below. |

## Reviewed and excluded

| Skill | Why it is not vendored | If you still want it |
|---|---|---|
| Impeccable (`pbakaus/impeccable`, [impeccable.style](https://impeccable.style/)) | Apache-2.0 and popular, but every session the skill runs a launcher that downloads a self-contained binary on first run (checksum comes from the same release), and its opt-in `hooks on` command writes agent hook/settings files including user-global `~/.claude/settings.json`. Re-checked 2026-10-19 against CLI v4.6.0: unchanged. | `npx skills add pbakaus/impeccable --skill impeccable`, after reading its hooks documentation |
| shadcn (`shadcn-ui/ui`) | Runs unpinned `npx shadcn@latest` automatically when the skill loads and pre-approves every shadcn subcommand, including installs from community registries. It is `user-invocable: false`, so it auto-triggers in any project with `components.json`. Re-checked 2026-10-24 (upstream commit `4233ed1`, which added DESIGN.md support): unchanged, kept excluded. | Use the `shadcn` MCP server in `toolkit.config.json` (pinned, off by default) |
| Vercel `web-design-guidelines`, Anthropic `doc-coauthoring`, Vercel `use-ai-sdk` | No license declared, so they cannot be redistributed. | `npx skills add vercel-labs/agent-skills --skill web-design-guidelines`; `npx skills add vercel/ai` |
| Trail of Bits skills | CC-BY-SA-4.0 (share-alike) and packaged as plugins. | `/plugin marketplace add trailofbits/skills` (Claude Code), `codex plugin marketplace add trailofbits/skills` |
| Taste Skill, UI/UX Pro Max | Design-style skills overlap `frontend-design`; pick one per project. | See [TOOLKIT-GUIDE.md](TOOLKIT-GUIDE.md) §3.4 |
| `apple-design` (dickwu) | No license; bundles Apple's guideline text. | Install for personal use only |
| `find-skills` (`vercel-labs/skills`) | Its final step installs skills globally with `npx skills add … -g -y` (no confirmation prompt, every project affected) and ranks candidates by install count, which reposted copies inflate. The toolkit's `marketplace-skill-review` skill and `vendor_skills.py` cover discovery with review. | Use the CLI directly: `npx skills find <query>`, then review and add to `skills-library/library.json` |
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

## Design resources and guardrails

Not skills, but they work with the `AGENTS.md` rule that every tool follows a root `DESIGN.md`.

| Resource | What it gives you | How to use it safely |
|---|---|---|
| [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT) | 85 `DESIGN.md` files analysing well-known brands' design systems | Use one as a structural starting point, then replace colors, type and voice with your own. Shipping a UI that imitates a real brand risks trademark and trade-dress problems. |
| [designmd.app](https://designmd.app/) | Library of DESIGN.md templates in Google's format | Same: adapt, don't clone. No license is named. |
| [Refero Styles](https://styles.refero.design/) (beta) | Design systems (colors, type, spacing, components, DESIGN.md) taken from product sites such as Linear, Notion and Figma; also offers an MCP connection | Same: adapt, don't clone. No license or pricing is published, and its MCP setup could not be verified, so it is not in `toolkit.config.json`. |
| [shadcn-ui/lint](https://github.com/shadcn-ui/lint) (`@shadcn/lint`, MIT) | ESLint/Oxlint rules for Tailwind v4 design systems (React, Svelte, Vue). Errors tell the agent the allowed fix, e.g. "use a Button size, not padding". | Add it as a pinned dev dependency during Phase 1 and run it in CI. Read its `SETUP.md` yourself instead of telling an agent to fetch and follow it from `main`. |
| [habitat](https://github.com/Owl-Listener/habitat) (MIT, MC Dean) | Toolkit for making an existing design system legible to agents: AI reads the facts from Figma, interviews you for the reasons, marks unknowns `TODO`, and measures the improvement on real screens. Includes a validator, a code checker and a local MCP server (no network calls). | New (June 2026, no stars yet). Its quick start runs unpinned `npx github:Owl-Listener/habitat`; pin a commit instead (`npx github:Owl-Listener/habitat#7d5122d init`, reviewed 2026-10-19). `init` installs Claude Code skills and appends rule blocks to `AGENTS.md`, `CLAUDE.md` and `.cursor/rules/habitat.mdc`: keep the block in `AGENTS.md` and remove the duplicates. |
| [GetLayers](https://www.getlayers.ai/) (textura.agency) | Library of "cinematic" website prompts, templates, 3D scenes, palettes and fonts; free curated set, paid plans with a commercial licence | Copy prompts by hand on the free tier. Its MCP (`getlayers` in `toolkit.config.json`, off) needs a paid Full Stack Lifetime plan and browser sign-in; the published pages don't say what data it receives, so check its privacy policy first. Returned template code is third-party: review before committing. |
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
