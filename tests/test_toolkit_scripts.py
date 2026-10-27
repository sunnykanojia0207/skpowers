"""Tests for scripts/sync_toolkit.py and scripts/install_toolkit.py (stdlib only).

Run: python -m unittest discover -s tests
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[1]
# Test projects use the toolkit's shared library through SKPOWERS_HOME, like installed projects do.
COPY = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "toolkit.config.json", ".agents/skills", "scripts",
        "docs/GETTING-STARTED.md", "docs/PROJECT_BRIEF.md", "docs/QUALITY-GATES.md", "templates/ci-node.yml"]


def run(script: Path, *args: str, cwd: Path, library: bool = True) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k != "SKPOWERS_HOME"}
    env["HOME"] = env["USERPROFILE"] = str(cwd)  # never pick up a real ~/.skpowers
    if library:
        env["SKPOWERS_HOME"] = str(TOOLKIT)
    return subprocess.run([sys.executable, "-I", str(script), *args], cwd=cwd, capture_output=True, text=True, env=env)


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

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_auto_selects_profiles_from_a_nextjs_saas(self) -> None:
        self.write("package.json", json.dumps({"dependencies": {
            "next": "16.0.0", "react": "19.0.0", "react-dom": "19.0.0", "@prisma/client": "6.0.0",
            "stripe": "18.0.0", "openai": "5.0.0", "sonner": "2.0.0", "framer-motion": "12.0.0"}}))
        self.write("prisma/schema.prisma", 'datasource db {\n  provider = "postgresql"\n}\n')
        self.write("Dockerfile", "FROM node:22\n")
        self.edit_config(lambda c: c.update(autoSkills=True, skillProfiles=[]))

        explained = run(self.sync, "--explain", cwd=self.root)
        self.assertEqual(explained.returncode, 0, explained.stderr)
        self.assertIn("next", explained.stdout)
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        skills = self.root / ".agents/skills"
        for name in ("systematic-debugging", "vercel-react-best-practices", "playwright-best-practices",
                     "better-interface", "prisma-client-api", "supabase-postgres-best-practices",
                     "docker-compose-patterns", "eval-audit", "animate", "vibe-security", "ask-sonner"):
            self.assertTrue((skills / name / "SKILL.md").is_file(), name)
        # security pre-approves Bash, so it is only suggested
        self.assertFalse((skills / "security-review").exists())
        self.assertIn("security", explained.stdout.split("Suggested")[1])

    def test_auto_selects_react_native_not_native_ios_for_expo(self) -> None:
        self.write("package.json", json.dumps({"dependencies": {"expo": "54.0.0", "react-native": "0.81.0"}}))
        self.write("ios/Podfile", "platform :ios\n")
        self.edit_config(lambda c: c.update(autoSkills=True, skillProfiles=[]))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        self.assertTrue((self.root / ".agents/skills/expo-router/SKILL.md").is_file())
        self.assertFalse((self.root / ".agents/skills/swiftui-pro").exists())

    def test_auto_selects_from_brief_checkboxes(self) -> None:
        self.write("docs/PROJECT_BRIEF.md", "## Platforms\n- [ ] Web\n- [x] iOS\n- [x] Android\n- [x] AI/LLM features\n")
        self.edit_config(lambda c: c.update(autoSkills=True, skillProfiles=[]))
        explained = run(self.sync, "--explain", cwd=self.root).stdout
        self.assertIn("react-native", explained)
        self.assertIn("ai-apps", explained)
        self.assertNotIn("\n  web ", explained)

    def test_auto_selection_drops_profiles_when_requirements_go_away(self) -> None:
        self.write("package.json", json.dumps({"dependencies": {"@prisma/client": "6.0.0"}}))
        self.edit_config(lambda c: c.update(autoSkills=True, skillProfiles=[]))
        run(self.sync, cwd=self.root)
        self.assertTrue((self.root / ".agents/skills/prisma-cli").is_dir())
        self.write("package.json", json.dumps({"dependencies": {}}))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        self.assertFalse((self.root / ".agents/skills/prisma-cli").exists())
        self.assertTrue((self.root / ".agents/skills/systematic-debugging").is_dir())  # baseline stays

    def test_auto_selects_language_profiles_and_framework_skills(self) -> None:
        self.write("api/pyproject.toml", '[project]\nname = "svc"\ndependencies = ["fastapi>=0.115", "pandas"]\n')
        self.write("worker/go.mod", "module example.com/worker\n")
        self.write("web/package.json", json.dumps({"dependencies": {"next": "16.0.0", "ai": "5.0.0"},
                                                    "devDependencies": {"typescript": "5.9.0"}}))
        self.write("infra/main.tf", 'terraform {}\n')
        self.write("mobile/android/build.gradle", "plugins { id 'com.android.application' }\n")
        self.write("mobile/package.json", json.dumps({"dependencies": {"expo": "54.0.0"}}))
        self.edit_config(lambda c: c.update(autoSkills=True, skillProfiles=[]))
        out = run(self.sync, "--explain", cwd=self.root).stdout
        profiles = out.split("Individual skills")[0]
        for name in ("python", "go", "nextjs", "typescript", "react-native", "ai-apps"):
            self.assertIn(f"\n  {name} ", profiles, name)
        self.assertNotIn("\n  java ", profiles)  # Gradle here belongs to the mobile app
        self.assertNotIn("\n  name ", out)  # pyproject keys are not dependencies
        for skill in ("fastapi-expert", "pandas-pro", "ai-sdk", "terraform-engineer"):
            self.assertIn(f"\n  {skill} ", out, skill)
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        self.assertTrue((self.root / ".agents/skills/golang-pro/SKILL.md").is_file())

    def test_auto_selects_vendor_platform_profiles(self) -> None:
        self.write("package.json", json.dumps({"dependencies": {
            "firebase": "12.0.0", "convex": "1.20.0", "@clerk/nextjs": "6.0.0", "gsap": "3.13.0",
            "@neondatabase/serverless": "1.0.0", "fastify": "5.0.0", "@mastra/core": "0.20.0",
            "@mendable/firecrawl-js": "4.0.0"}}))
        self.write("wrangler.jsonc", "{}\n")
        self.write("turbo.json", "{}\n")
        self.edit_config(lambda c: c.update(autoSkills=True, skillProfiles=[]))
        out = run(self.sync, "--explain", cwd=self.root).stdout
        for name in ("firebase", "cloudflare", "convex", "clerk", "neon", "gsap", "firecrawl",
                     "turborepo", "fastify-best-practices", "mastra", "vibe-security"):
            self.assertIn(f"\n  {name} ", out, name)
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        for skill in ("firebase-security-rules-auditor", "wrangler", "convex-authz", "clerk-webhooks", "gsap-react"):
            self.assertTrue((self.root / ".agents/skills" / skill / "SKILL.md").is_file(), skill)

    def test_auto_selects_claude_api_for_anthropic_sdk_users(self) -> None:
        self.write("requirements.txt", "anthropic>=0.70\nfastapi\n")
        self.edit_config(lambda c: c.update(autoSkills=True, skillProfiles=[]))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        for skill in ("claude-api", "eval-audit", "python-pro", "fastapi-expert"):
            self.assertTrue((self.root / ".agents/skills" / skill / "SKILL.md").is_file(), skill)

    def test_missing_library_keeps_copied_skills(self) -> None:
        self.edit_config(lambda c: c.update(skillProfiles=["ios"]))
        run(self.sync, cwd=self.root)
        result = run(self.sync, cwd=self.root, library=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("library not found", result.stdout)
        self.assertTrue((self.root / ".agents/skills/swiftui-pro/SKILL.md").is_file())
        self.assertEqual(run(self.sync, "--check", cwd=self.root, library=False).returncode, 0)

    def test_suggest_and_enable_from_a_task(self) -> None:
        self.edit_config(lambda c: c.update(autoSkills=True, skillProfiles=["core"]))
        out = run(self.sync, "--suggest", "add clerk login to the app", cwd=self.root).stdout
        self.assertIn("profile clerk", out)
        self.assertNotIn("convex", out)  # stack-specific profiles need the request to name their stack
        result = run(self.sync, "--enable", "clerk", "landing-page-design", cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / ".agents/skills/clerk-setup/SKILL.md").is_file())
        self.assertTrue((self.root / ".agents/skills/landing-page-design/SKILL.md").is_file())
        config = json.loads((self.root / "toolkit.config.json").read_text(encoding="utf-8"))
        self.assertIn("clerk", config["skillProfiles"])
        self.assertIn("landing-page-design", config["skills"])
        run(self.sync, "--disable", "clerk", cwd=self.root)
        self.assertFalse((self.root / ".agents/skills/clerk-setup").exists())
        self.assertEqual(run(self.sync, "--enable", "no-such-thing", cwd=self.root).returncode, 2)

    def test_auto_skills_off_uses_only_explicit_profiles(self) -> None:
        self.write("package.json", json.dumps({"dependencies": {"next": "16.0.0"}}))
        self.edit_config(lambda c: c.update(autoSkills=False, skillProfiles=["ios"]))
        self.assertEqual(run(self.sync, cwd=self.root).returncode, 0)
        self.assertTrue((self.root / ".agents/skills/swiftui-pro").is_dir())
        self.assertFalse((self.root / ".agents/skills/vercel-react-best-practices").exists())

    def test_every_library_skill_is_vendored_with_license(self) -> None:
        catalog = json.loads((TOOLKIT / "skills-library/library.json").read_text(encoding="utf-8"))
        notices = (TOOLKIT / "skills-library/THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        for source_name, source in catalog["sources"].items():
            self.assertRegex(source["commit"] or "", r"^[0-9a-f]{40}$", source_name)
            for skill in source["skills"]:
                self.assertTrue((TOOLKIT / "skills-library" / source_name / skill / "SKILL.md").is_file(), skill)
                self.assertIn(f"`{skill}`", notices)
        for profile in catalog["profiles"].values():
            for skill in profile["skills"]:
                self.assertTrue(any(skill in s["skills"] for s in catalog["sources"].values()), skill)


class InstallToolkitTests(unittest.TestCase):
    def test_installs_fast_without_the_library_and_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "AGENTS.md").write_text("existing rules", encoding="utf-8")
            (project / "package.json").write_text(json.dumps({"dependencies": {"expo": "54.0.0"}}), encoding="utf-8")
            result = run(TOOLKIT / "scripts" / "install_toolkit.py", str(project), cwd=project, library=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((project / "AGENTS.md").read_text(encoding="utf-8"), "existing rules")
            self.assertIn("AGENTS.md", result.stdout)
            self.assertFalse((project / "skills-library").exists())
            self.assertFalse((project / "scripts/vendor_skills.py").exists())
            self.assertEqual((project / ".agents/.toolkit-home").read_text(encoding="utf-8").strip(), str(TOOLKIT))
            self.assertIn(".toolkit-home", (project / ".agents/.gitignore").read_text(encoding="utf-8"))
            self.assertTrue((project / ".mcp.json").is_file())
            self.assertTrue((project / ".agents/skills/expo-router/SKILL.md").is_file())  # auto-selected
            self.assertTrue((project / ".claude/skills/python-venv/SKILL.md").is_file())
            # The project syncs again on its own, finding the library through .agents/.toolkit-home.
            again = run(project / "scripts" / "sync_toolkit.py", "--check", cwd=project, library=False)
            self.assertEqual(again.returncode, 0, again.stdout + again.stderr)

    def test_update_refreshes_toolkit_owned_files_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            installer = TOOLKIT / "scripts" / "install_toolkit.py"
            run(installer, str(project), cwd=project)
            (project / "scripts/sync_toolkit.py").write_text("# stale", encoding="utf-8")
            (project / "AGENTS.md").write_text("my rules", encoding="utf-8")
            result = run(installer, str(project), "--update", cwd=project)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotEqual((project / "scripts/sync_toolkit.py").read_text(encoding="utf-8"), "# stale")
            self.assertEqual((project / "AGENTS.md").read_text(encoding="utf-8"), "my rules")


if __name__ == "__main__":
    unittest.main()
