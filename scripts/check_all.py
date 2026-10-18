#!/usr/bin/env python3
"""Structural and cross-edition checks for the PTI skill.

Usage: python3 scripts/check_all.py [--quiet]

Exit codes: 0 = workspace clean (project drift is reported, not fatal);
            1 = workspace structural failure or a required rule missing;
            2 = manifest or required files missing.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "docs", "rule-manifest.json")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def find_match(paths, pattern, root=None):
    root = root or ROOT
    rx = re.compile(pattern, re.IGNORECASE)
    for rel in paths:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            continue
        for lineno, line in enumerate(read(path).splitlines(), 1):
            if rx.search(line):
                return rel, lineno, line.strip()
    return None


def rule_status(edition_root, targets, pattern, root=None):
    """Every existing target file must contain the pattern.

    Requiring all files (not any file) is what makes a single-file mutation
    fail the rule; the earlier "first match wins" version survived deletion
    whenever the phrase appeared in a second file.
    """
    root = root or ROOT
    existing, absent, lacking = [], [], []
    for rel in targets:
        path = os.path.join(root, edition_root, rel)
        if os.path.isfile(path):
            existing.append(rel)
        else:
            absent.append(rel)
    if not existing:
        return "ABSENT", None, absent, lacking
    hit = None
    for rel in existing:
        found = find_match([os.path.join(edition_root, rel)], pattern, root)
        if found is None:
            lacking.append(rel)
        elif hit is None:
            hit = found
    if lacking:
        return "MISSING", hit, absent, lacking
    if absent:
        return "PARTIAL", hit, absent, lacking
    return "OK", hit, absent, lacking


def structure_checks():
    problems, notes = [], []
    skill = os.path.join(ROOT, "personal-travel-intelligence", "SKILL.md")
    if not os.path.isfile(skill):
        problems.append("SKILL.md missing")
        return problems, notes
    text = read(skill)
    if not text.startswith("---"):
        problems.append("SKILL.md has no YAML frontmatter")
    else:
        head = text.split("---", 2)[1]
        for key in ("name:", "description:"):
            if key not in head:
                problems.append(f"frontmatter missing {key}")
    for rel in re.findall(r"`references/([\w.-]+\.md)`", text):
        if not os.path.isfile(os.path.join(ROOT, "personal-travel-intelligence", "references", rel)):
            problems.append(f"SKILL.md references missing file: references/{rel}")
    refs_dir = os.path.join(ROOT, "personal-travel-intelligence", "references")
    for name in sorted(os.listdir(refs_dir)):
        if not name.endswith(".md"):
            continue
        body = read(os.path.join(refs_dir, name))
        for rel in re.findall(r"`references/([\w.-]+\.md)`", body):
            if not os.path.isfile(os.path.join(refs_dir, rel)):
                problems.append(f"references/{name} references missing file: references/{rel}")
    for dirpath, _dirs, files in os.walk(os.path.join(ROOT, "personal-travel-intelligence")):
        for fn in files:
            if fn.endswith((".md", ".py")):
                body = read(os.path.join(dirpath, fn))
                for word in ("TODO", "FIXME"):
                    if word in body:
                        notes.append(f"{word} left in {os.path.relpath(os.path.join(dirpath, fn), ROOT)}")
    version_path = os.path.join(ROOT, "VERSION")
    title = next((line for line in text.splitlines() if line.startswith("# ")), "")
    if os.path.isfile(version_path):
        ver = read(version_path).strip()
        short = ".".join(ver.split(".")[:2])
        if f"v{short}" not in title:
            notes.append(f"VERSION {ver} does not match the SKILL.md title: {title!r}")
    else:
        notes.append("VERSION file missing")
    return problems, notes


def main():
    strict = "--strict" in sys.argv
    if not os.path.isfile(MANIFEST):
        print(f"manifest missing: {MANIFEST}")
        return 2
    manifest = json.loads(read(MANIFEST))
    editions = manifest["editions"]
    width = max(len(r["id"] + " " + r["name"]) for r in manifest["rules"]) + 2
    drift = []
    failures = []
    print(f"{'RULE'.ljust(width)}{'WORKSPACE'.ljust(34)}{'PROJECT'}")
    print("-" * (width + 34 + 12))
    for rule in manifest["rules"]:
        cells = []
        for key in ("workspace", "project"):
            root = editions[key]["root"]
            status, hit, absent, lacking = rule_status(root, rule["targets"][key], rule["pattern"])
            if status == "OK":
                rel, lineno, _ = hit
                cells.append(f"OK ({os.path.basename(rel)}:{lineno})")
            elif status == "PARTIAL":
                cells.append(f"UNVERIFIED (missing {', '.join(absent)})")
            elif status == "MISSING":
                detail = ", ".join(lacking)
                if absent:
                    detail += " · unverified: " + ", ".join(absent)
                cells.append(f"MISSING ({detail})")
            elif status == "ABSENT":
                cells.append("ABSENT (no file)")
            else:
                cells.append("MISSING")
            if key == "workspace" and status in ("MISSING", "ABSENT"):
                failures.append(f"{rule['id']} {rule['name']}: {status} in workspace")
            if key == "project" and status != "OK":
                drift.append(f"{rule['id']} {rule['name']}: {status}")
        print(f"{rule['id'] + ' ' + rule['name']: <{width}}{cells[0]: <34}{cells[1]}")

    problems, notes = structure_checks()
    print()
    if problems:
        print("STRUCTURE FAIL")
        for item in problems:
            print(f"  - {item}")
    else:
        print("STRUCTURE OK")
    for item in notes:
        print(f"  note: {item}")
    if drift:
        print()
        print(f"PROJECT DRIFT ({len(drift)} rule(s) not yet mirrored):")
        for item in drift:
            print(f"  - {item}")
        print("  → regenerate project-edition/ from the workspace edition, or record the gap in docs/EDITION-PARITY.md")
    if failures:
        print()
        print("WORKSPACE FAIL")
        for item in failures:
            print(f"  - {item}")
    if strict and drift:
        print()
        print("STRICT: project drift counts as failure in --strict mode")
    return 1 if (problems or failures or (strict and drift)) else 0


if __name__ == "__main__":
    sys.exit(main())
