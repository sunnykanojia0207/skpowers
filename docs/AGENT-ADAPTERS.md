# Per-Tool File Locations

Checked against each tool's official documentation on 2026-10-19. Tools change these paths; re-check the linked docs when something stops loading.

| Tool | Rules | Project skills | Project MCP config (generated) | Docs |
|---|---|---|---|---|
| Claude Code | `CLAUDE.md` (imports `AGENTS.md`) | `.claude/skills/` (generated mirror) | `.mcp.json` | https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/mcp |
| Codex | `AGENTS.md` | `.agents/skills/` | `.codex/config.toml` (trusted projects only) | https://learn.chatgpt.com/docs/build-skills, https://learn.chatgpt.com/docs/extend/mcp |
| Cursor | `AGENTS.md` (root and nested) | `.agents/skills/` (also reads `.cursor/`, `.claude/`, `.codex/skills/`) | `.cursor/mcp.json` | https://cursor.com/docs/context/rules, https://cursor.com/docs/context/skills, https://cursor.com/docs/context/mcp |
| OpenCode | `AGENTS.md` (falls back to `CLAUDE.md` if absent) | `.agents/skills/` (also reads `.opencode/`, `.claude/skills/`) | `opencode.json`, `mcp` key | https://opencode.ai/docs/rules/, https://opencode.ai/docs/skills/, https://opencode.ai/docs/mcp-servers/ |
| Gemini CLI | `GEMINI.md` (imports `AGENTS.md`) | `.agents/skills/` (alias of `.gemini/skills/`) | `.gemini/settings.json` | https://geminicli.com/docs/cli/skills/, https://geminicli.com/docs/tools/mcp-server/ |
| Antigravity | `AGENTS.md` (also `GEMINI.md`, `.agents/rules/*.md`) | `.agents/skills/` | `.agents/mcp_config.json` (`serverUrl` for remote) | https://antigravity.google/docs/rules, https://antigravity.google/docs/skills, https://antigravity.google/docs/mcp |
| GitHub Copilot (VS Code) | `AGENTS.md` (nearest wins), `.github/copilot-instructions.md` | `.agents/skills/` (also `.github/skills/`, `.claude/skills/`) | `.mcp.json` (`.vscode/mcp.json` is legacy) | https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions, https://code.visualstudio.com/docs/copilot/customization/mcp-servers |

## Subagents (generated)

Checked against each tool's official documentation on 2026-11-04. `sync_toolkit.py` writes every enabled library agent in each tool's format and marks it `skpowers-generated`; hand-written agents with the same name are kept.

| Tool | Folder | Read-only expressed as | Docs |
|---|---|---|---|
| Claude Code | `.claude/agents/<name>.md` | `tools` allowlist without Edit/Write | https://code.claude.com/docs/en/sub-agents |
| Cursor | `.cursor/agents/<name>.md` (also reads `.claude/agents/`, `.codex/agents/`; `.cursor/` wins) | `readonly: true` | https://cursor.com/docs/context/subagents |
| OpenCode | `.opencode/agents/<name>.md`, `mode: subagent` | `permission: {edit: deny}`; shell is `ask` or `deny` | https://opencode.ai/docs/agents/ |
| Codex | `.codex/agents/<name>.toml` (`name`, `description`, `developer_instructions`) | no per-agent sandbox: stated in the instructions; `[features] shell_tool = false` when upstream has no shell | https://learn.chatgpt.com/docs/agent-configuration/subagents |
| GitHub Copilot | `.github/agents/<name>.agent.md` (shows up once merged to the default branch) | `tools: ["read", "search"]`; agents that use MCP tools keep all tools | https://docs.github.com/en/copilot/reference/custom-agents-configuration |
| Gemini CLI | `.gemini/agents/<name>.md` | `tools: [read_file, grep_search]` (+ `run_shell_command`, `mcp_*`); editing agents inherit all tools because the edit tool names aren't documented | https://geminicli.com/docs/core/subagents/ |
| Antigravity | `.agents/agents/<name>.md` | `tools: [view_file, grep_search]` (+ `run_command`, `replace_file_content`); runs in its default `sandbox` command policy | https://antigravity.google/docs/subagents |

No model is set in any tool, so each uses its default (Claude-only names like `sonnet` don't work elsewhere). Unverified: how Cursor treats Claude's `tools` field in files it reads from `.claude/agents/` (the generated `.cursor/agents/` copy takes precedence), and whether Antigravity's write agents need more than `replace_file_content` to create new files.

## Known quirks

- **Duplicate skills in Cursor, OpenCode and Copilot.** They read both `.agents/skills/` and `.claude/skills/`, so with `claude-code` in `tools` they see each toolkit skill twice (identical content). If nobody on the team uses Claude Code, remove `claude-code` from `tools` and the sync deletes the mirror.
- **Gemini CLI vs Antigravity CLI.** Google's Gemini CLI docs say it was replaced by Antigravity CLI on 2026-06-18. Keep `gemini-cli` in `tools` only if you still use it; Antigravity reads `GEMINI.md` too, where the `@./AGENTS.md` import line is harmless.
- **Antigravity secrets.** Its MCP docs describe no environment-variable expansion, so the generated file omits `env` and stdio servers inherit variables from the shell that launched Antigravity. Verify this with your version before relying on the `github` server there.
- **Codex trust.** Codex ignores `.codex/config.toml` until you mark the project as trusted.
- **Claude Code approvals.** Servers from `.mcp.json` need a one-time approval in each interactive session's project.
- **Tool-specific skill features.** A skill can be portable in format yet depend on one tool's hooks, subagents or slash commands. Read a skill before relying on it in every tool.
