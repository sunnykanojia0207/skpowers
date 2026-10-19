"""Tests for scripts/sync_toolkit.py and scripts/install_toolkit.py (stdlib only).

Run: python -m unittest discover -s tests
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[1]
COPY = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "toolkit.config.json", ".agents/skills", "scripts", "skills-library",
        "docs/GETTING-STARTED.md", "docs/PROJECT_BRIEF.md", "docs/QUALITY-GATES.md", "templates/ci-node.yml"]


def run(script: Path, *args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", str(script), *args], cwd=cwd, capture_output=True, text=True)


class SyncToolkitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "toolkit"
        for rel in COPY:
            src, dst = TOOLKIT / rel, self.root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                # Generated library copies in .agents/skills are left out so each test starts from sources.
                shutil.copytree(src, dst, ignore=lambda d, names: [
                    n for n in names if n == "__pycache__" or (Path(d, n) / ".toolkit-generated").exists()
                ])
            else:
                shutil.copy2(src, dst)
        self.sync = self.root / "scripts" / "sync_toolkit.py"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def edit_config(self, change) -> None:
        path = self.root / "toolkit.config.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        change(config)
        path.write_text(json.dumps(config), encoding="utf-8")

    def read_json(self, rel: str) -> dict:
        return json.loads((self.root / rel).read_text(encoding="utf-8"))

    def test_generates_every_tool_and_is_idempotent(self) -> None:
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        self.assertEqual(run(self.sync, "--check", cwd=self.root).returncode, 0)
        self.assertEqual(self.read_json(".mcp.json")["mcpServers"]["context7"]["type"], "http")
        self.assertEqual(self.read_json("opencode.json")["mcp"]["playwright"]["type"], "local")
        self.assertIn("httpUrl", self.read_json(".gemini/settings.json")["mcpServers"]["context7"])
        self.assertIn("serverUrl", self.read_json(".agents/mcp_config.json")["mcpServers"]["context7"])
        codex = tomllib.loads((self.root / ".codex/config.toml").read_text(encoding="utf-8"))
        self.assertEqual(codex["mcp_servers"]["playwright"]["command"], "npx")
        self.assertTrue((self.root / ".claude/skills/production-engineering/SKILL.md").is_file())

    def test_check_reports_stale_outputs(self) -> None:
        result = run(self.sync, "--check", cwd=self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn(".mcp.json", result.stdout)

    def test_env_passthrough_uses_each_tools_syntax(self) -> None:
        self.edit_config(lambda c: c["mcpServers"]["github"].update(enabled=True))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        name = "GITHUB_PERSONAL_ACCESS_TOKEN"
        self.assertEqual(self.read_json(".mcp.json")["mcpServers"]["github"]["env"][name], "${%s}" % name)
        self.assertEqual(self.read_json(".cursor/mcp.json")["mcpServers"]["github"]["env"][name], "${env:%s}" % name)
        self.assertEqual(self.read_json("opencode.json")["mcp"]["github"]["environment"][name], "{env:%s}" % name)
        self.assertEqual(self.read_json(".gemini/settings.json")["mcpServers"]["github"]["env"][name], "${%s}" % name)
        codex = tomllib.loads((self.root / ".codex/config.toml").read_text(encoding="utf-8"))
        self.assertEqual(codex["mcp_servers"]["github"]["env_vars"], [name])

    def test_static_env_reaches_every_tool(self) -> None:
        self.edit_config(lambda c: c["mcpServers"]["mobile-mcp"].update(enabled=True))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        name, value = "MOBILEMCP_DISABLE_TELEMETRY", "1"
        self.assertEqual(self.read_json(".mcp.json")["mcpServers"]["mobile-mcp"]["env"][name], value)
        self.assertEqual(self.read_json(".cursor/mcp.json")["mcpServers"]["mobile-mcp"]["env"][name], value)
        self.assertEqual(self.read_json("opencode.json")["mcp"]["mobile-mcp"]["environment"][name], value)
        self.assertEqual(self.read_json(".gemini/settings.json")["mcpServers"]["mobile-mcp"]["env"][name], value)
        self.assertEqual(self.read_json(".agents/mcp_config.json")["mcpServers"]["mobile-mcp"]["env"][name], value)
        codex = tomllib.loads((self.root / ".codex/config.toml").read_text(encoding="utf-8"))
        self.assertEqual(codex["mcp_servers"]["mobile-mcp"]["env"][name], value)

    def test_every_configured_server_renders_for_every_tool(self) -> None:
        def enable_all(config: dict) -> None:
            for server in config["mcpServers"].values():
                if "YOUR_" not in json.dumps(server):
                    server["enabled"] = True
        self.edit_config(enable_all)
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        expected = {n for n, s in json.loads((self.root / "toolkit.config.json").read_text(encoding="utf-8"))["mcpServers"].items() if s["enabled"]}
        codex = tomllib.loads((self.root / ".codex/config.toml").read_text(encoding="utf-8"))
        self.assertEqual(set(codex["mcp_servers"]), expected)
        for rel, key in [(".mcp.json", "mcpServers"), (".cursor/mcp.json", "mcpServers"), ("opencode.json", "mcp"),
                         (".gemini/settings.json", "mcpServers"), (".agents/mcp_config.json", "mcpServers")]:
            self.assertEqual(set(self.read_json(rel)[key]), expected, rel)
        self.assertEqual(codex["mcp_servers"]["21st"]["env_vars"], ["API_KEY_21ST"])

    def test_keeps_user_servers_and_settings_and_removes_disabled(self) -> None:
        (self.root / "opencode.json").write_text(json.dumps({
            "model": "my-model",
            "mcp": {"mine": {"type": "remote", "url": "https://example.com/mcp"},
                    "github": {"type": "local", "command": ["stale"]}},
        }), encoding="utf-8")
        codex = self.root / ".codex/config.toml"
        codex.parent.mkdir()
        codex.write_text('model = "x"\n\n[mcp_servers.mine]\nurl = "https://example.com/mcp"\n', encoding="utf-8")

        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        opencode = self.read_json("opencode.json")
        self.assertEqual(opencode["model"], "my-model")
        self.assertIn("mine", opencode["mcp"])
        self.assertNotIn("github", opencode["mcp"])  # managed by the toolkit and disabled
        parsed = tomllib.loads(codex.read_text(encoding="utf-8"))
        self.assertEqual(parsed["model"], "x")
        self.assertEqual(set(parsed["mcp_servers"]), {"mine", "context7", "playwright"})

    def test_refuses_hand_written_codex_server_with_managed_name(self) -> None:
        codex = self.root / ".codex/config.toml"
        codex.parent.mkdir()
        codex.write_text('[mcp_servers.playwright]\ncommand = "x"\n', encoding="utf-8")
        result = run(self.sync, cwd=self.root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("defined by hand", result.stderr)

    def test_refuses_to_overwrite_hand_written_claude_skill(self) -> None:
        own = self.root / ".claude/skills/production-engineering"
        own.mkdir(parents=True)
        (own / "SKILL.md").write_text("mine", encoding="utf-8")
        result = run(self.sync, cwd=self.root)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((own / "SKILL.md").read_text(encoding="utf-8"), "mine")

    def test_rejects_enabled_server_with_placeholder(self) -> None:
        self.edit_config(lambda c: c["mcpServers"]["supabase"].update(enabled=True))
        result = run(self.sync, cwd=self.root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("YOUR_PROJECT_REF", result.stderr)

    def test_dropping_a_tool_removes_its_skill_mirror(self) -> None:
        run(self.sync, cwd=self.root)
        self.edit_config(lambda c: c.update(tools=["codex"]))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        self.assertEqual(list((self.root / ".claude/skills").iterdir()), [])

    def test_profiles_install_library_skills_for_every_tool(self) -> None:
        self.edit_config(lambda c: c.update(skillProfiles=["core", "ios"], skills=["mcp-builder"]))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        for name in ("systematic-debugging", "swiftui-pro", "mcp-builder"):
            self.assertTrue((self.root / ".agents/skills" / name / "SKILL.md").is_file(), name)
            self.assertTrue((self.root / ".claude/skills" / name / "SKILL.md").is_file(), name)
        self.assertFalse((self.root / ".agents/skills/security-review").exists())  # profile not enabled
        self.assertTrue((self.root / ".agents/skills/production-engineering").is_dir())  # own skill kept

    def test_disabling_a_profile_removes_only_generated_skills(self) -> None:
        self.edit_config(lambda c: c.update(skillProfiles=["ios"]))
        run(self.sync, cwd=self.root)
        self.edit_config(lambda c: c.update(skillProfiles=[]))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        self.assertFalse((self.root / ".agents/skills/swiftui-pro").exists())
        self.assertFalse((self.root / ".claude/skills/swiftui-pro").exists())
        self.assertTrue((self.root / ".agents/skills/production-engineering/SKILL.md").is_file())

    def test_rejects_unknown_profile_and_skill(self) -> None:
        self.edit_config(lambda c: c.update(skillProfiles=["nope"]))
        result = run(self.sync, cwd=self.root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown skill profile", result.stderr)
        self.edit_config(lambda c: c.update(skillProfiles=[], skills=["nope"]))
        self.assertIn("not in skills-library", run(self.sync, cwd=self.root).stderr)

    def test_library_skill_never_overwrites_a_hand_written_skill(self) -> None:
        own = self.root / ".agents/skills/swiftui-pro"
        own.mkdir(parents=True)
        (own / "SKILL.md").write_text("mine", encoding="utf-8")
        self.edit_config(lambda c: c.update(skillProfiles=["ios"]))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 2)
        self.assertEqual((own / "SKILL.md").read_text(encoding="utf-8"), "mine")

    def test_every_library_skill_is_vendored_with_license(self) -> None:
        catalog = json.loads((self.root / "skills-library/library.json").read_text(encoding="utf-8"))
        notices = (self.root / "skills-library/THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        for source_name, source in catalog["sources"].items():
            self.assertRegex(source["commit"] or "", r"^[0-9a-f]{40}$", source_name)
            for skill in source["skills"]:
                self.assertTrue((self.root / "skills-library" / source_name / skill / "SKILL.md").is_file(), skill)
                self.assertIn(f"`{skill}`", notices)
        for profile in catalog["profiles"].values():
            for skill in profile["skills"]:
                self.assertTrue(any(skill in s["skills"] for s in catalog["sources"].values()), skill)


class InstallToolkitTests(unittest.TestCase):
    def test_installs_without_overwriting_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "AGENTS.md").write_text("existing rules", encoding="utf-8")
            result = run(TOOLKIT / "scripts" / "install_toolkit.py", str(project), cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((project / "AGENTS.md").read_text(encoding="utf-8"), "existing rules")
            self.assertIn("= AGENTS.md", result.stdout)
            self.assertTrue((project / ".mcp.json").is_file())
            self.assertTrue((project / "docs/GETTING-STARTED.md").is_file())
            self.assertTrue((project / ".claude/skills/release-verification/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
