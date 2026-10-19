# Marketplace Decision Summary (2026-10-19)

Full evidence, runner-ups and rejections: [MARKETPLACE-RESEARCH.md](MARKETPLACE-RESEARCH.md).

**Workflow (pick one):** Superpowers (most installed, broadest native support) or Addy Osmani Agent Skills.

**Best skill per need:**

| Need | Pick |
|---|---|
| iOS / SwiftUI | `twostraws/SwiftUI-Agent-Skill` → `swiftui-pro` |
| Android / Compose | `android/skills` (Google), individual skills; skip `android-cli` |
| React Native | `callstackincubator/agent-skills` → `react-native-best-practices` (+ `expo/skills`) |
| Playwright testing | `currents-dev/playwright-best-practices-skill` |
| Security | `trailofbits/skills` (+ getsentry `security-review`) |
| API design | `wshobson/agents` → `api-design-principles` (single skill only) |
| Postgres | `timescale/pg-aiguide` → `postgres` |
| Docker | `docker/skills` |
| LLM evals | `ai-evals-course/evals-skills` |
| Web perf & a11y | `addyosmani/web-quality-skills` |
| UI design | one of Impeccable / UI/UX Pro Max / Taste Skill |

**MCP:** Context7 + Playwright on by default. Supabase (read-only), GitHub (read-only), Linear (read-only endpoint), Grafana (`--disable-write`), Sentry, Chrome DevTools, Mobile MCP (telemetry off) and Semgrep are preconfigured but off in `toolkit.config.json`.

**Avoid:** all-in-one packs (gstack, everything-claude-code), unlicensed repos (openai/skills, JetBrains/skills), ClawHub-only listings, persona prompts, and any skill that installs other skills or pipes remote scripts to a shell.

**Marketplace metrics are misleading** (repo-wide stars shown per skill, stale counts, incomplete indexes). Decide from the upstream repository.
