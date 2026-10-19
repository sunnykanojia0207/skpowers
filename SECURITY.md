# Security Policy

## Scope

This toolkit ships instructions that AI coding agents follow with your permissions: `AGENTS.md`, skills in `.agents/skills/` and `skills-library/`, and MCP server configuration. A malicious or careless change to any of them can make an agent run commands, leak data or weaken checks. Treat changes to these files like changes to CI configuration.

## How third-party skills are handled

- Skills are vendored by `scripts/vendor_skills.py` from upstream Git repositories at a **pinned commit**, unmodified, with their upstream license. Unlicensed skills are refused.
- Nothing from a downloaded repository is executed during vendoring.
- Each vendored skill is scanned for review flags (remote scripts piped to a shell, installing other skills, `sudo`, destructive deletes, global installs, tool pre-approval via `allowed-tools`, commands that run when a skill loads, and references to agent settings or hooks files). Flags are listed in [`skills-library/THIRD_PARTY_NOTICES.md`](skills-library/THIRD_PARTY_NOTICES.md); they are prompts for human review, not verdicts.
- Every skill was also reviewed by hand before inclusion. Skills that download unreviewable binaries, write agent hook or settings files, or run unpinned remote packages on load are excluded. See [`docs/SKILLS-CATALOG.md`](docs/SKILLS-CATALOG.md) for the exclusions and the cautions on included skills.
- Updates (`python scripts/vendor_skills.py --update`) must be reviewed as a diff of `skills-library/` before merging.

## MCP servers

All MCP servers in `toolkit.config.json` except Context7 and Playwright are **off by default**. Prefer read-only modes, scope tokens to one project, never supply production credentials, and keep secrets in environment variables (`envPassthrough`), never in the config.

## Reporting a vulnerability

If you find a skill, script or configuration in this repository that could cause an agent to exfiltrate data, execute untrusted code, or bypass permissions, please report it privately to the repository owner instead of opening a public issue. Include the file path, the upstream commit (from `THIRD_PARTY_NOTICES.md` if it is a vendored skill) and the behaviour you observed.

Vulnerabilities in a vendored skill should also be reported to its upstream project.
