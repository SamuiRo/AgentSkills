#!/usr/bin/env python3
"""Heuristic version-bump consistency check for the docs-and-versioning skill.

Autodetects a project's version manifest (package.json, pyproject.toml,
Cargo.toml, composer.json, go.mod, or a bare VERSION file), then checks:

  - whether the current version appears anywhere in docs/project/CHANGELOG.md
  - whether, in the current git diff against --base, a manifest and its
    paired lockfile moved together (a manifest bump with no matching
    lockfile change is a common, easy-to-miss mistake)

This is a starting point to adapt, not a guarantee — ecosystems vary and
this only knows the common cases. Treat a clean run as "nothing obviously
wrong", not as proof the bump is correct.

Usage:
    python check_version_bump.py [--root .] [--changelog docs/project/CHANGELOG.md] [--base HEAD~1]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

MANIFEST_LOCK_PAIRS = [
    ("package.json", "package-lock.json"),
    ("package.json", "npm-shrinkwrap.json"),
    ("pyproject.toml", "poetry.lock"),
    ("pyproject.toml", "uv.lock"),
    ("Cargo.toml", "Cargo.lock"),
    ("composer.json", "composer.lock"),
]


def extract_version(manifest: Path) -> str | None:
    text = manifest.read_text(encoding="utf-8", errors="replace")
    if manifest.name in ("package.json", "composer.json"):
        try:
            return json.loads(text).get("version")
        except json.JSONDecodeError:
            return None
    if manifest.name in ("pyproject.toml", "Cargo.toml"):
        match = re.search(r'(?m)^\s*version\s*=\s*["\']([^"\']+)["\']', text)
        return match.group(1) if match else None
    if manifest.name == "VERSION":
        return text.strip() or None
    if manifest.name == "go.mod":
        return None  # go.mod versions are the module path / go directive, not a semver to track here
    return None


def find_manifests(root: Path) -> list[Path]:
    names = ["package.json", "pyproject.toml", "Cargo.toml", "composer.json", "VERSION"]
    found = []
    for name in names:
        candidate = root / name
        if candidate.exists():
            found.append(candidate)
    return found


def changed_files(root: Path, base: str) -> set[str] | None:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", base],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="project root")
    parser.add_argument("--changelog", default="docs/project/CHANGELOG.md", help="path to CHANGELOG.md")
    parser.add_argument("--base", default="HEAD~1", help="git ref to diff against for the lockfile-pairing check")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    problems: list[str] = []

    manifests = find_manifests(root)
    if not manifests:
        print("no known version manifest found (package.json, pyproject.toml, Cargo.toml, composer.json, VERSION)")
        return 0

    changelog = root / args.changelog
    changelog_text = changelog.read_text(encoding="utf-8", errors="replace") if changelog.exists() else ""

    for manifest in manifests:
        version = extract_version(manifest)
        if not version:
            continue
        print(f"{manifest.relative_to(root)}: version {version}")

        if changelog.exists():
            if version not in changelog_text:
                problems.append(f"{version} (from {manifest.name}) has no entry in {args.changelog}")
        else:
            problems.append(f"{args.changelog} does not exist")

    diff = changed_files(root, args.base)
    if diff is not None:
        for manifest_name, lock_name in MANIFEST_LOCK_PAIRS:
            manifest_changed = manifest_name in diff
            lock_exists = (root / lock_name).exists()
            lock_changed = lock_name in diff
            if manifest_changed and lock_exists and not lock_changed:
                problems.append(
                    f"{manifest_name} changed against {args.base} but {lock_name} did not — "
                    "check whether the version bump and lockfile drifted apart"
                )
    else:
        print(f"(skipped lockfile-pairing check: not a git repo, or {args.base} doesn't resolve)")

    if problems:
        print(f"\nversion bump check: {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("\nversion bump check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
