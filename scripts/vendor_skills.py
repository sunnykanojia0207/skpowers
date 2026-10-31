#!/usr/bin/env python3
"""Download the third-party skills listed in skills-library/library.json.

Each source repository is fetched with git (shallow, sparse: only the listed
skill folders and the license), at its pinned commit, or at the latest commit
with --update. Every skill must carry a license; unlicensed skills are refused.
Nothing from the downloaded repositories is executed.

Writes:
  skills-library/<source>/<skill>/        the vendored skill (with its license)
  skills-library/library.json             pinned commit per source
  skills-library/THIRD_PARTY_NOTICES.md   source, commit, license and review flags

Review the git diff of skills-library/ before committing an update.

Usage:
  python scripts/vendor_skills.py                  fetch pinned commits (latest for unpinned sources)
  python scripts/vendor_skills.py --update         move every source to its latest commit
  python scripts/vendor_skills.py --source expo    limit to one source
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "skills-library"
CATALOG = LIBRARY / "library.json"
NOTICES = LIBRARY / "THIRD_PARTY_NOTICES.md"
LICENSE_FILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE.rst", "COPYING")
SPDX_RE = re.compile(r"^license:\s*['\"]?([A-Za-z0-9.+-]+)['\"]?\s*$", re.MULTILINE)
SCRIPT_SUFFIXES = {".sh", ".bash", ".py", ".js", ".mjs", ".cjs", ".ts", ".ps1", ".rb"}
RISKS = [
    (re.compile(r"curl[^\n|]*\|\s*(?:ba|z)?sh\b"), "pipes a download into a shell"),
    (re.compile(r"npx\s+(?:-y\s+)?skills(?:@\S+)?\s+add"), "installs other skills"),
    (re.compile(r"\bsudo\s"), "uses sudo"),
    (re.compile(r"rm\s+-rf\s+[/~$]"), "recursive delete outside the project"),
    (re.compile(r"npm\s+(?:i|install)\s+(?:-g|--global)\b"), "global npm install"),
    (re.compile(r"^allowed-tools:.*\bBash\b", re.MULTILINE), "pre-approves shell commands (allowed-tools)"),
    (re.compile(r"^\s*!`", re.MULTILINE), "runs a command when the skill loads"),
    (re.compile(r"settings(?:\.local)?\.json|hooks\.json"), "mentions agent settings or hooks files"),
]


class VendorError(Exception):
    pass


def git(*args: str, cwd: Path) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise VendorError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def fetch(repo: str, ref: str, paths: list[str], workdir: Path) -> str:
    """Sparse, shallow fetch of `paths` plus root license files; returns the commit SHA."""
    git("init", "-q", cwd=workdir)
    git("config", "core.autocrlf", "false", cwd=workdir)  # keep upstream line endings byte-for-byte
    git("remote", "add", "origin", f"https://github.com/{repo}.git", cwd=workdir)
    # "." means the skill is the repository root; otherwise a folder, or a single file when the name has a dot.
    patterns = ["/*" if p in (".", "") else f"/{p.strip('/')}" + ("" if "." in p.rsplit("/", 1)[-1] else "/") for p in paths]
    patterns += [f"/{name}" for name in LICENSE_FILES]
    git("sparse-checkout", "set", "--no-cone", *patterns, cwd=workdir)
    git("fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", ref, cwd=workdir)
    git("-c", "core.symlinks=false", "checkout", "-q", "FETCH_HEAD", cwd=workdir)
    return git("rev-parse", "HEAD", cwd=workdir)


def frontmatter_name(skill_md: Path) -> str | None:
    text = skill_md.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None
    header = text[4:text.find("\n---", 4)]
    match = re.search(r"^name:\s*['\"]?([^'\"\n#]+?)['\"]?\s*$", header, re.MULTILINE)
    return match.group(1).strip() if match else None


def resolve_license(skill_dir: Path, repo_root: Path) -> str:
    """Make sure the vendored skill carries license terms; return a description."""
    for name in LICENSE_FILES:
        if (skill_dir / name).is_file():
            return f"{name} in skill"
    for name in LICENSE_FILES:
        if (repo_root / name).is_file():
            shutil.copy2(repo_root / name, skill_dir / "LICENSE")
            return "repository LICENSE (copied)"
    match = SPDX_RE.search((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    if match and not match.group(1).lower().startswith("complete"):
        return f"{match.group(1)} (SKILL.md frontmatter)"
    raise VendorError("no license file or SPDX license in SKILL.md")


def review(skill_dir: Path) -> tuple[list[str], list[str]]:
    scripts, flags = [], set()
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in SCRIPT_SUFFIXES:
            scripts.append(path.relative_to(skill_dir).as_posix())
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern, label in RISKS:
            if pattern.search(text):
                flags.add(f"{label} ({path.relative_to(skill_dir).as_posix()})")
    return scripts, sorted(flags)


def vendor_source(name: str, source: dict, update: bool) -> list[dict]:
    ref = "HEAD" if update or not source.get("commit") else source["commit"]
    with tempfile.TemporaryDirectory(prefix="vendor-") as tmp:
        workdir = Path(tmp)
        shared = source.get("sharedFiles", [])
        commit = fetch(source["repo"], ref, list(source["skills"].values()) + shared, workdir)
        target_root = LIBRARY / name
        rows = []
        for skill, rel in source["skills"].items():
            src = workdir / rel
            if not (src / "SKILL.md").is_file():
                raise VendorError(f"{source['repo']}: {rel}/SKILL.md not found at {commit[:12]}")
            if frontmatter_name(src / "SKILL.md") != skill:
                raise VendorError(f"{source['repo']}: {rel}/SKILL.md is not named {skill!r}")
            dest = target_root / skill
            if dest.exists():
                shutil.rmtree(dest)
            excluded = set(source.get("exclude", []))
            shutil.copytree(src, dest, ignore=lambda d, names: [n for n in names if n == ".git" or (Path(d) == src and n in excluded)])
            # Repository-level files (e.g. shared checklists) that a skill links to by the same
            # relative path are copied in unmodified, as upstream recommends for per-skill installs.
            skill_text = (dest / "SKILL.md").read_text(encoding="utf-8", errors="replace")
            for rel_file in shared:
                if rel_file in skill_text and not (dest / rel_file).exists() and (workdir / rel_file).is_file():
                    (dest / rel_file).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(workdir / rel_file, dest / rel_file)
            try:
                license_note = resolve_license(dest, workdir)
            except VendorError as exc:
                shutil.rmtree(dest)
                raise VendorError(f"{source['repo']}: {skill}: {exc}") from exc
            scripts, flags = review(dest)
            rows.append({"skill": skill, "repo": source["repo"], "path": rel, "commit": commit,
                         "license": license_note, "scripts": scripts, "flags": flags})
        for stale in target_root.iterdir():
            if stale.is_dir() and stale.name not in source["skills"]:
                shutil.rmtree(stale)
        source["commit"] = commit
        return rows


def write_notices(rows: list[dict]) -> None:
    lines = [
        "# Third-Party Skills",
        "",
        "Generated by `scripts/vendor_skills.py`. Each skill is copied unmodified from the listed",
        "commit and keeps its upstream license. Review flags are heuristics for human review,",
        "not verdicts.",
        "",
        "| Skill | Source | Commit | License | Scripts | Review flags |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda r: r["skill"]):
        url = f"https://github.com/{r['repo']}/tree/{r['commit']}/{r['path']}"
        scripts = "<br>".join(r["scripts"][:6]) + (" …" if len(r["scripts"]) > 6 else "") or "none"
        flags = "<br>".join(r["flags"]) or "none"
        lines.append(f"| `{r['skill']}` | [{r['repo']}]({url}) | `{r['commit'][:12]}` | {r['license']} | {scripts} | {flags} |")
    NOTICES.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--update", action="store_true", help="fetch the latest commit of each source")
    parser.add_argument("--source", help="only vendor this source")
    args = parser.parse_args(argv)

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    sources = catalog["sources"]
    if args.source and args.source not in sources:
        print(f"vendor_skills: unknown source {args.source!r}", file=sys.stderr)
        return 2

    # A single-source run keeps the other sources' notice rows.
    state = LIBRARY / ".notices.json"
    rows = {}
    if args.source and state.exists():
        rows = {r["skill"]: r for r in json.loads(state.read_text(encoding="utf-8"))}
    failures = []
    all_skills = {skill for source in sources.values() for skill in source["skills"]}
    for name, source in sources.items():
        if args.source and name != args.source:
            continue
        print(f"- {name} ({source['repo']})", flush=True)
        # Forget this source's previous rows so skills removed from the catalog leave the notices.
        rows = {skill: row for skill, row in rows.items() if row["skill"] not in source["skills"]
                and not (row["repo"] == source["repo"] and row["skill"] not in all_skills)}
        try:
            for row in vendor_source(name, source, args.update):
                rows[row["skill"]] = row
                for flag in row["flags"]:
                    print(f"    review: {row['skill']}: {flag}")
        except VendorError as exc:
            failures.append(str(exc))
            print(f"    FAILED: {exc}", file=sys.stderr)

    if not args.source:
        for stale in LIBRARY.iterdir():
            if stale.is_dir() and stale.name not in sources:
                shutil.rmtree(stale)

    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8", newline="\n")
    state.write_text(json.dumps(list(rows.values()), indent=2) + "\n", encoding="utf-8", newline="\n")
    write_notices(list(rows.values()))
    print(f"Vendored {len(rows)} skills. Review `git diff skills-library/`, then run scripts/sync_toolkit.py.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
