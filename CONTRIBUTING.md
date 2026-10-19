# Contributing

## Setup

Requires Python 3.11+ and Git. No packages to install: every script uses the standard library.

```bash
python -m unittest discover -s tests
python scripts/validate_toolkit.py
```

Both must pass before you open a pull request; CI runs them on Linux and Windows.

## What to edit

| Change | Edit | Then run |
|---|---|---|
| Rules for every tool | `AGENTS.md` | nothing |
| The toolkit's own skills | `.agents/skills/<name>/SKILL.md` | `python scripts/sync_toolkit.py` |
| Which library skills / MCP servers are on | `toolkit.config.json` | `python scripts/sync_toolkit.py` |
| Add or remove a third-party skill | `skills-library/library.json` (source + profile) | `python scripts/vendor_skills.py --source <name>`, then `sync_toolkit.py` |
| Update third-party skills | nothing | `python scripts/vendor_skills.py --update`, review the diff, then `sync_toolkit.py` |

Never hand-edit generated files: `.mcp.json`, `.cursor/mcp.json`, `opencode.json`, `.codex/config.toml`, `.gemini/settings.json`, `.agents/mcp_config.json`, `.claude/skills/`, `skills-library/THIRD_PARTY_NOTICES.md`, or any skill folder containing `.toolkit-generated`.

## Adding a third-party skill

A skill is accepted when it:

1. Comes from its original upstream repository (not a copy or aggregator) with recent activity.
2. Has a license that allows redistribution (`vendor_skills.py` refuses skills without one).
3. Fills a gap no existing library skill covers, without competing with the `core` workflow.
4. Passes a manual read of `SKILL.md`, its references and scripts: no instructions to bypass the user, install other skills, run remote scripts, write agent settings/hooks, phone home, or pre-approve broad tool access. Review flags in `THIRD_PARTY_NOTICES.md` must be explained in [`docs/SKILLS-CATALOG.md`](docs/SKILLS-CATALOG.md).

Record the decision (accepted with cautions, or rejected and why) in `docs/SKILLS-CATALOG.md`.

## Adding an MCP server

Add it to `toolkit.config.json` with `"enabled": false`, a pinned package version, the read-only mode if the server has one, and a `description` that states cost and write capabilities. Verify the command, URL and auth against the vendor's official documentation, and put secrets only in `envPassthrough`.

## Commits

Small, focused commits with an imperative subject line. Include the generated files your change produces so `sync_toolkit.py --check` stays green.
