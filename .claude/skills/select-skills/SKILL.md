---
name: select-skills
description: Pick and enable the right skills for this project and for the current request. Use at the start of a session or new project, whenever the user's request touches an area the enabled skills may not cover (a new platform, framework, database, auth, payments, design, testing, deployment, AI feature…), after adding a significant dependency, or when the user asks which skills or MCP servers apply.
---

# Select skills for the project and the request

Skills come from two automatic sources: the **project** (dependencies, platform files, CI, the brief) and the **request** the user just made. Never hand-edit skill copies in `.agents/skills/` or generated MCP files.

## For each new request

0. **UI or design request?** (a page, screen, dashboard, landing page, brand, colours, fonts, animation, accessibility, forms…) Run:
   ```bash
   python scripts/sync_toolkit.py --pick "<the user's request, in their words>"
   ```
   It enables the design skills that fit that kind of UI and keeps one design style per project (switching off a previous style and saying so). Tell the user what was picked, then continue with step 3. For anything else, or if `--pick` finds no UI intent, go to step 1.

1. **Ask the toolkit what fits the request.**
   ```bash
   python scripts/sync_toolkit.py --suggest "<the user's request, in their words>"
   ```
   It answers in under a second. The first line lists **already enabled skills that match**: use those. Below it are the best library profiles and skills that are not enabled yet; stack-specific ones only appear when the request names that stack.

2. **Enable what the task clearly needs**, then continue with the task:
   ```bash
   python scripts/sync_toolkit.py --enable <profile-or-skill> [more…]
   ```
   This updates `toolkit.config.json` and copies the skills for every tool in one step. Tell the user in one line what you enabled and why. Profiles marked `suggest-only` (they pre-approve shell commands) need the user's yes first. Turn things off with `--disable`.

3. **Use the matching skills** (newly enabled or already active) before writing code. Some tools load new skills only at the next session; if a just-enabled skill isn't available, read its `SKILL.md` from `.agents/skills/<name>/` directly.

## When the project itself changes

1. If the user described requirements, reflect them in `docs/PROJECT_BRIEF.md` (tick `- [x] Web`, `iOS`, `Android`, `Public API`, `Admin portal`, `AI/LLM features`).
2. Run `python scripts/sync_toolkit.py --explain` to preview, then `python scripts/sync_toolkit.py` to apply. Profiles that match the stack are added; ones that stopped matching are removed. Hand-written skills are never touched.

## Notes

- MCP servers are never enabled automatically. If one would help (for example `supabase`, `next-devtools`, `magicui`, `github`), name it and ask; enabling means `"enabled": true` in `toolkit.config.json` and a sync.
- If the toolkit reports that the skills library was not found, the copied skills still work; to change them, the user clones the toolkit once (`git clone https://github.com/sunnykanojia0207/skpowers ~/.skpowers`) or sets `SKPOWERS_HOME`.
- `"autoSkills": false` in `toolkit.config.json` turns off detection from the project; `--suggest` and `--enable` keep working.
