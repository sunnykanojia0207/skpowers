#!/usr/bin/env python3
"""Lightweight, offline validation for the portable vibe-engineering toolkit."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
checks: list[str] = []

required_files = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "docs/AGENT-ADAPTERS.md",
    "docs/BOOTSTRAP-PROMPT.md",
    "docs/CURATED-INSTALL.md",
    "docs/GETTING-STARTED.md",
    "docs/SKILLS-CATALOG.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "skills-library/library.json",
    "skills-library/THIRD_PARTY_NOTICES.md",
    "scripts/vendor_skills.py",
    "docs/MARKETPLACE-DECISION-SUMMARY.md",
    "docs/MARKETPLACE-RESEARCH.md",
    "docs/PROJECT_BRIEF.md",
    "docs/QUALITY-GATES.md",
    "docs/TOOLKIT-GUIDE.md",
    "toolkit.config.json",
    "scripts/install-curated-skills.ps1",
    "scripts/install_toolkit.py",
    "scripts/sync_toolkit.py",
]
for relative in required_files:
    if not (ROOT / relative).is_file():
        errors.append(f"Missing required file: {relative}")
if not errors:
    checks.append(f"required files present ({len(required_files)})")

# Generated per-tool configs must match toolkit.config.json and .agents/skills.
sync = subprocess.run(
    [sys.executable, "-I", str(ROOT / "scripts" / "sync_toolkit.py"), "--check"],
    capture_output=True, text=True,
)
if sync.returncode == 0:
    checks.append("generated tool configs are up to date")
else:
    errors.append("Generated tool configs are stale or invalid:\n  " + (sync.stdout + sync.stderr).strip().replace("\n", "\n  "))

# Validate the portable Agent Skills frontmatter without needing a YAML dependency.
skill_files = sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))
name_re = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
for path in skill_files:
    relative = path.relative_to(ROOT)
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not content.startswith("---\n"):
        errors.append(f"Missing YAML frontmatter: {relative}")
        continue
    frontmatter_end = content.find("\n---\n", 4)
    if frontmatter_end < 0:
        errors.append(f"Unterminated YAML frontmatter: {relative}")
        continue
    header = content[4:frontmatter_end]
    name_match = re.search(r"^name:\s*([^\n#]+)\s*$", header, re.MULTILINE)
    description_match = re.search(r"^description:\s*(.+?)\s*$", header, re.MULTILINE)
    if not name_match:
        errors.append(f"Missing name in frontmatter: {relative}")
        continue
    name = name_match.group(1).strip().strip("\"'")
    if not name_re.fullmatch(name):
        errors.append(f"Invalid skill name {name!r}: {relative}")
    if name != path.parent.name:
        errors.append(f"Skill name does not match directory ({name!r}): {relative}")
    if not description_match or not description_match.group(1).strip():
        errors.append(f"Missing description in frontmatter: {relative}")
if skill_files and not any("skill name" in error.lower() or "frontmatter" in error.lower() for error in errors):
    checks.append(f"Agent Skills frontmatter looks valid ({len(skill_files)} skills)")

# Validate internal Markdown links to local files when they resolve to a path.
link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# Vendored third-party skills and their generated copies are kept unmodified, so
# only the toolkit's own Markdown is checked.
def is_third_party(path: Path) -> bool:
    rel = path.relative_to(ROOT).parts
    return rel[0] in {"skills-library", ".git"} or any((p / ".toolkit-generated").exists() for p in path.parents)


for path in sorted(p for p in ROOT.rglob("*.md") if not is_third_party(p)):
    text = path.read_text(encoding="utf-8")
    for raw_target in link_pattern.findall(text):
        target = raw_target.strip().split()[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#", "data:")):
            continue
        target_path = target.split("#", 1)[0].split("?", 1)[0]
        if not target_path:
            continue
        candidate = (path.parent / target_path).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            continue
        if not candidate.exists():
            errors.append(f"Broken local Markdown link in {path.relative_to(ROOT)}: {target}")
if not any("Broken local Markdown link" in error for error in errors):
    checks.append("local Markdown links resolve")

if errors:
    print("Toolkit validation FAILED:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Toolkit validation PASSED:")
for check in checks:
    print(f"- {check}")
print(f"- {len(skill_files)} local skills")
