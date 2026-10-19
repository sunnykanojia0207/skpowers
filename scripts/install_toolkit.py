#!/usr/bin/env python3
"""Copy the universal toolkit into another project, then generate its tool configs.

Never overwrites: any file that already exists in the target is skipped and
listed so you can merge it by hand.

Usage:
  python scripts/install_toolkit.py <target-project-dir> [--dry-run]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# What a project needs to run the toolkit. Research docs stay in the toolkit repo.
MANIFEST = [
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "toolkit.config.json",
    ".agents/skills",
    "skills-library",
    "scripts/sync_toolkit.py",
    "scripts/vendor_skills.py",
    "docs/GETTING-STARTED.md",
    "docs/PROJECT_BRIEF.md",
    "docs/QUALITY-GATES.md",
    ".github/workflows/ci-node.example.yml",
]


def source_files() -> list[Path]:
    files: list[Path] = []
    for rel in MANIFEST:
        path = ROOT / rel
        if path.is_dir():
            # Generated skill copies are rebuilt by the target's own sync from skills-library/.
            files += sorted(
                p for p in path.rglob("*")
                if p.is_file() and "__pycache__" not in p.parts
                and not any((parent / ".toolkit-generated").exists() for parent in p.parents)
            )
        elif path.is_file():
            files.append(path)
        else:
            raise SystemExit(f"install_toolkit: toolkit file missing: {rel}")
    return files


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", type=Path, help="root directory of the project to set up")
    parser.add_argument("--dry-run", action="store_true", help="show what would be copied without writing")
    args = parser.parse_args(argv)

    target = args.target.resolve()
    if not target.is_dir():
        print(f"install_toolkit: {target} is not a directory", file=sys.stderr)
        return 2
    if target == ROOT:
        print("install_toolkit: target is the toolkit itself; run scripts/sync_toolkit.py instead", file=sys.stderr)
        return 2

    copied: list[str] = []
    skipped: list[str] = []
    for source in source_files():
        rel = source.relative_to(ROOT)
        destination = target / rel
        if destination.exists():
            skipped.append(rel.as_posix())
            continue
        copied.append(rel.as_posix())
        if not args.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    verb = "Would copy" if args.dry_run else "Copied"
    print(f"{verb} {len(copied)} file(s) into {target}")
    for rel in copied:
        print(f"  + {rel}")
    if skipped:
        print(f"Skipped {len(skipped)} existing file(s); merge these by hand:")
        for rel in skipped:
            print(f"  = {rel}")
        if "AGENTS.md" in skipped:
            print("  AGENTS.md already exists: merge the toolkit's rules into it rather than keeping two rule sets.")
        if "CLAUDE.md" in skipped:
            print("  CLAUDE.md already exists: add a line '@AGENTS.md' so Claude Code loads the shared rules.")

    if args.dry_run:
        return 0
    print("\nGenerating tool configs in the target project:")
    result = subprocess.run([sys.executable, "-I", str(target / "scripts" / "sync_toolkit.py")], cwd=target)
    if result.returncode == 0:
        print("\nNext: edit toolkit.config.json ('tools' and MCP 'enabled' flags), then rerun scripts/sync_toolkit.py.")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
