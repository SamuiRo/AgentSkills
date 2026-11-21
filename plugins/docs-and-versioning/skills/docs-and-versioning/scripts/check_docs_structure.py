#!/usr/bin/env python3
"""Structural checks for a docs/ tree that follows the docs-and-versioning skill.

Flags, without opinion on content:
  - a doc missing its role banner ("> **Role:** ... · **Audience:** ...")
  - a doc that exists under docs/ but isn't linked from docs/README.md
  - a relative markdown link that doesn't resolve to a real file
  - docs/project/HANDOFF.md going over its line cap

Usage:
    python check_docs_structure.py [docs_dir] [--handoff-cap N]

Exit code is non-zero if any check fails. Dependency-free (stdlib only) so
it can be dropped into any project's own test/lint/CI step.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BANNER_RE = re.compile(r"^\s*>\s*\*\*Role:\*\*.+", re.MULTILINE)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def find_md_files(docs_dir: Path) -> list[Path]:
    return sorted(p for p in docs_dir.rglob("*.md") if p.is_file())


def has_banner(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    head = "\n".join(text.splitlines()[:6])
    return bool(BANNER_RE.search(head))


def extract_local_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = HTML_COMMENT_RE.sub("", text)  # example links inside <!-- --> aren't real references
    links = []
    for match in MD_LINK_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0].strip()
        if target:
            links.append(target)
    return links


def check(docs_dir: Path, handoff_cap: int) -> list[str]:
    problems: list[str] = []
    md_files = find_md_files(docs_dir)
    if not md_files:
        return [f"no markdown files found under {docs_dir}"]

    readme = docs_dir / "README.md"

    # 1. Role banners (README.md is the index and is exempt).
    for f in md_files:
        if f == readme:
            continue
        if not has_banner(f):
            problems.append(f"missing role banner: {f}")

    # 2. Every file linked from README.md (orphan check).
    if readme.exists():
        linked_targets = set()
        for target in extract_local_links(readme):
            resolved = (readme.parent / target).resolve()
            linked_targets.add(resolved)
        for f in md_files:
            if f == readme:
                continue
            if f.resolve() not in linked_targets:
                problems.append(f"not linked from docs/README.md: {f}")
    else:
        problems.append(f"missing index: {readme}")

    # 3. Relative links resolve (a link to a directory, e.g. "decisions/", is fine).
    for f in md_files:
        for target in extract_local_links(f):
            resolved = (f.parent / target).resolve()
            if not resolved.exists():
                problems.append(f"broken relative link in {f}: -> {target}")

    # 4. HANDOFF.md line cap.
    handoff = docs_dir / "project" / "HANDOFF.md"
    if handoff.exists():
        line_count = len(handoff.read_text(encoding="utf-8", errors="replace").splitlines())
        if line_count > handoff_cap:
            problems.append(
                f"{handoff} is {line_count} lines, over the {handoff_cap}-line cap"
            )

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docs_dir", nargs="?", default="docs", help="path to the docs/ directory")
    parser.add_argument("--handoff-cap", type=int, default=100, help="max lines for project/HANDOFF.md")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    if not docs_dir.is_dir():
        print(f"error: {docs_dir} is not a directory", file=sys.stderr)
        return 2

    problems = check(docs_dir, args.handoff_cap)
    if problems:
        print(f"docs structure check: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("docs structure check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
