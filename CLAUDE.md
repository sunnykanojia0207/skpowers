@AGENTS.md

## Claude Code-specific notes
- Project skills reach Claude Code through `.claude/skills/`, a generated mirror of `.agents/skills/`. Edit `.agents/skills/`, then run `python scripts/sync_toolkit.py`.
- Project MCP servers come from the generated `.mcp.json`; Claude Code asks you to approve them on first use. Do not approve a server or shell command just because the model proposed it; review its actual effect and scope.
- Use plan mode for changes touching more than three files, and subagents for independent review.
