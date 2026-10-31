#!/usr/bin/env python3
"""Set up the toolkit in a project in one step, then pick its skills automatically.

Copies only what a project needs (rules, config, the toolkit's own skills, the sync
script, a few docs). The skills library stays in this toolkit checkout and is shared
by every project; the sync copies just the skills the project needs. Existing files
are never overwritten; they are listed so you can merge them by hand.

Usage (from the project folder):
  python ~/.skpowers/scripts/install_toolkit.py              set up the current folder
  python ~/.skpowers/scripts/install_toolkit.py <dir>        set up another folder
  python ~/.skpowers/scripts/install_toolkit.py --update     refresh the sync script and toolkit skills
  python ~/.skpowers/scripts/install_toolkit.py --dry-run    show what would change
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME_FILE = Path(".agents") / ".toolkit-home"

# Copied once; never overwritten because projects customise them.
PROJECT_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "toolkit.config.json",
    "docs/GETTING-STARTED.md",
    "docs/PROJECT_BRIEF.md",
    "docs/QUALITY-GATES.md",
    "templates/ci-node.yml",
    "templates/docs",
]
# Toolkit path -> project path, for templates that land somewhere else in the project.
RENAMES = {"templates/docs/README.md": "docs/DOCS-INDEX.md", "templates/docs/": "docs/"}


def destination_for(rel: str) -> str:
    if rel in RENAMES:
        return RENAMES[rel]
    for prefix, target in RENAMES.items():
        if prefix.endswith("/") and rel.startswith(prefix):
            return target + rel[len(prefix):]
    return rel
# Owned by the toolkit; refreshed by --update.
TOOLKIT_FILES = ["scripts/sync_toolkit.py", ".agents/skills"]


def expand(rels: list[str]) -> list[Path]:
    files: list[Path] = []
    for rel in rels:
        path = ROOT / rel
        if path.is_dir():
            # Library skills (marked .toolkit-generated) come from the shared library at sync time.
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
    parser.add_argument("target", type=Path, nargs="?", default=Path.cwd(), help="project folder (default: current folder)")
    parser.add_argument("--update", action="store_true", help="also refresh toolkit-owned files that already exist")
    parser.add_argument("--dry-run", action="store_true", help="show what would change without writing")
    args = parser.parse_args(argv)

    target = args.target.resolve()
    if not target.is_dir():
        print(f"install_toolkit: {target} is not a directory", file=sys.stderr)
        return 2
    if target == ROOT:
        print("install_toolkit: this is the toolkit itself; run scripts/sync_toolkit.py instead", file=sys.stderr)
        return 2

    copied, refreshed, skipped = [], [], []
    plan = [(p, False) for p in expand(PROJECT_FILES)] + [(p, True) for p in expand(TOOLKIT_FILES)]
    for source, toolkit_owned in plan:
        rel = Path(destination_for(source.relative_to(ROOT).as_posix()))
        destination = target / rel
        if destination.exists():
            if not (toolkit_owned and args.update):
                skipped.append(rel.as_posix())
                continue
            if destination.read_bytes() == source.read_bytes():
                continue
            refreshed.append(rel.as_posix())
        else:
            copied.append(rel.as_posix())
        if not args.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    verb = "Would" if args.dry_run else "Did"
    print(f"{verb} copy {len(copied)} file(s)" + (f", refresh {len(refreshed)}" if refreshed else "") + f" into {target}",
          flush=True)
    project_skips = [s for s in skipped if not s.startswith((".agents/", "scripts/"))]
    if project_skips:
        print("Kept your existing files (merge by hand if needed): " + ", ".join(project_skips))
        if "AGENTS.md" in project_skips:
            print("  AGENTS.md exists: merge the toolkit's rules into it rather than keeping two rule sets.")
        if "CLAUDE.md" in project_skips:
            print("  CLAUDE.md exists: add a line '@AGENTS.md' so Claude Code loads the shared rules.")
    if args.dry_run:
        return 0

    # Remember where the shared library lives; machine-specific, so kept out of git.
    (target / HOME_FILE).parent.mkdir(parents=True, exist_ok=True)
    (target / HOME_FILE).write_text(str(ROOT) + "\n", encoding="utf-8")
    ignore = target / ".agents" / ".gitignore"
    if not ignore.exists():
        ignore.write_text(".toolkit-home\n", encoding="utf-8")

    print("Picking skills for this project:", flush=True)
    env = {**os.environ, "SKPOWERS_HOME": str(ROOT)}
    result = subprocess.run([sys.executable, "-I", str(target / "scripts" / "sync_toolkit.py"), "--quiet"], cwd=target, env=env)
    if result.returncode == 0:
        print("\nDone. Open the project in any AI coding tool. To see why skills were picked:"
              "\n  python scripts/sync_toolkit.py --explain"
              "\nTo add skills for a task:  python scripts/sync_toolkit.py --suggest \"<what you want to build>\"")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
