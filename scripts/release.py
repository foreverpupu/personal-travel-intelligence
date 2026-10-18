#!/usr/bin/env python3
"""Release gate for the PTI skill.

Runs the local checks, a privacy scan over files that would be published, and
writes a release sheet (dist/release-<version>.md) listing what to push and
what to upload, with hashes for after-the-fact verification.

Usage:
  python3 scripts/release.py            # check + write sheet
  python3 scripts/release.py --check    # check only, no file written

Exit codes: 0 = ready, 1 = blocking problem, 2 = missing input.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
PRIVACY = [
    ("email", re.compile(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}")),
    ("cn-mobile", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("long-digit-id", re.compile(r"(?<!\d)\d{15,18}(?!\d)")),
]
# Attribution in LICENSE/README is intentional; everything else is scanned.
PRIVACY_ALLOW = {"LICENSE", "README.md", "README.zh-CN.md", "CHANGELOG.md", "privacy-terms.txt"}


def run(args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def tracked_files():
    out = run(["git", "ls-files"]).stdout.splitlines()
    return [p for p in out if os.path.isfile(os.path.join(ROOT, p))]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def privacy_scan(files):
    hits = []
    for rel in files:
        if os.path.basename(rel) in PRIVACY_ALLOW:
            continue
        try:
            text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for kind, rx in PRIVACY:
                if rx.search(line):
                    hits.append((rel, lineno, kind))
    return hits


def term_scan(files):
    path = os.path.join(ROOT, "travel-data", "privacy-terms.txt")
    if not os.path.isfile(path):
        path = os.path.join(ROOT, "docs", "privacy-terms.txt")
    if not os.path.isfile(path):
        return None
    terms = [t.strip() for t in open(path, encoding="utf-8") if t.strip() and not t.startswith("#")]
    hits = []
    for rel in files:
        if os.path.basename(rel) in PRIVACY_ALLOW:
            continue
        try:
            text = open(os.path.join(ROOT, rel), encoding="utf-8").read().lower()
        except (UnicodeDecodeError, OSError):
            continue
        for term in terms:
            if term.lower() in text:
                hits.append((rel, term))
    return hits


def main():
    check_only = "--check" in sys.argv
    allow_missing_terms = "--allow-missing-terms" in sys.argv
    blocks, warns = [], []
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()

    # A ref name is not a guarantee: a squash commit on main must not descend
    # from the private branch, or the redacted text ships anyway.
    if branch in ("main", "master"):
        if run(["git", "merge-base", "--is-ancestor", "b6e63e5", "HEAD"]).returncode == 0:
            blocks.append("HEAD on main descends from b6e63e5 — history predates the privacy redaction")

    dirty = run(["git", "status", "--porcelain"]).stdout.strip()
    if dirty:
        blocks.append("working tree is dirty — commit or stash before releasing")

    version = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
    changelog = open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read()
    if f"## {version}" not in changelog:
        blocks.append(f"CHANGELOG.md has no section for {version}")

    proc = run([sys.executable, os.path.join(ROOT, "scripts", "check_all.py")])
    if proc.returncode != 0:
        blocks.append("check_all.py failed:\n" + proc.stdout.strip())
    drift = [line.strip() for line in proc.stdout.splitlines() if line.strip().startswith("- R")]
    if drift:
        warns.append(f"project edition drift: {len(drift)} rule(s) not mirrored")

    files = tracked_files()
    term_hits = term_scan(files)
    if term_hits is None:
        message = "privacy term scan DISABLED: no travel-data/privacy-terms.txt on this machine"
        if branch in ("main", "master") and not allow_missing_terms:
            blocks.append(message + " (release from main requires the list; --allow-missing-terms overrides)")
        else:
            warns.append(message)
    elif term_hits:
        blocks.append(f"privacy terms: {len(term_hits)} hit(s) in files that would be published")
        for rel, term in term_hits[:10]:
            blocks.append(f"  {rel}: contains {term!r}")
    hits = privacy_scan(files)
    if hits:
        warns.append(f"privacy scan: {len(hits)} hit(s) in files that would be published")
        for rel, lineno, kind in hits[:20]:
            warns.append(f"  {rel}:{lineno} ({kind})")

    print(f"version      : {version}")
    print(f"commit       : {run(['git', 'rev-parse', '--short', 'HEAD']).stdout.strip()}")
    print(f"tracked files: {len(files)}")
    for item in blocks:
        print(f"BLOCK  {item}")
    for item in warns:
        print(f"WARN   {item}")
    if not blocks:
        print("GATE   : ready to publish (model review and behaviour test are separate gates)")

    if blocks:
        return 1
    if check_only:
        return 0

    os.makedirs(DIST, exist_ok=True)
    sheet = os.path.join(DIST, f"release-{version}.md")
    with open(sheet, "w", encoding="utf-8") as fh:
        fh.write(f"# Release sheet — {version}\n\n")
        fh.write(f"- generated: {time.strftime('%Y-%m-%d %H:%M')}\n")
        fh.write(f"- commit: `{run(['git', 'rev-parse', 'HEAD']).stdout.strip()}`\n")
        fh.write(f"- branch: `{run(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).stdout.strip()}`\n\n")
        fh.write("## Gates before publishing\n\n")
        fh.write("- [x] working tree clean\n")
        fh.write("- [x] structure checks (`scripts/check_all.py`)\n")
        fh.write("- [ ] model review (`docs/validation/VALIDATION-PROMPT.md`)\n")
        fh.write("- [ ] behaviour test, if this release changes a rule (`evaluation/REV2-PROTOCOL.md`)\n")
        fh.write("- [ ] Project edition regenerated and diffed\n\n")
        fh.write("## Files in this release\n\n| path | sha256 (16) | lines |\n|---|---|---|\n")
        for rel in files:
            path = os.path.join(ROOT, rel)
            lines = sum(1 for _ in open(path, encoding="utf-8", errors="replace"))
            fh.write(f"| `{rel}` | `{sha(path)}` | {lines} |\n")
        fh.write("\n## After publishing\n\n")
        fh.write("1. `git tag v" + version + "` and push the tag.\n")
        fh.write("2. Upload the Project edition files; re-download one and compare its hash above.\n")
        fh.write("3. Record the result in CHANGELOG.md; do not edit this sheet.\n")
    print(f"sheet        : {os.path.relpath(sheet, ROOT)}")
    if branch not in ("main", "master"):
        print(f"NOTE         : on '{branch}'. Publish by squash onto main; never push this branch "
              "(its history predates the privacy redaction).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
