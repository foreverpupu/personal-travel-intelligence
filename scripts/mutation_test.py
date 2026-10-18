#!/usr/bin/env python3
"""Mutation test: delete each rule's marker line and prove the gate notices.

A rule that survives deletion is a rule the checker does not actually enforce.
Works on a throwaway copy; the repository is never touched.

Usage: python3 scripts/mutation_test.py [--keep]
Exit: 0 = every mutable rule was killed, 1 = at least one survived.
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import check_all  # noqa: E402

IGNORE = shutil.ignore_patterns(".git", "dist", "_inbox", "__pycache__", ".DS_Store")


def main():
    manifest = json.load(open(os.path.join(ROOT, "docs", "rule-manifest.json"), encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="pti-mut-")
    work = os.path.join(tmp, "repo")
    shutil.copytree(ROOT, work, ignore=IGNORE)

    rows, survivors = [], 0
    try:
        for rule in manifest["rules"]:
            for edition, cfg in manifest["editions"].items():
                root = cfg["root"]
                status, hit, _absent, _lacking = check_all.rule_status(
                    root, rule["targets"][edition], rule["pattern"], root=work)
                if status not in ("OK", "PARTIAL") or not hit:
                    rows.append((rule["id"], edition, "SKIP", "not present to mutate"))
                    continue
                rel, lineno, _text = hit
                path = os.path.join(work, rel)
                lines = open(path, encoding="utf-8").read().splitlines(keepends=True)
                removed = lines.pop(lineno - 1)
                open(path, "w", encoding="utf-8").write("".join(lines))
                after, _h, _a, _l = check_all.rule_status(
                    root, rule["targets"][edition], rule["pattern"], root=work)
                open(path, "w", encoding="utf-8").write("".join(
                    lines[:lineno - 1] + [removed] + lines[lineno - 1:]))
                killed = after in ("MISSING", "ABSENT")
                survivors += 0 if killed else 1
                rows.append((rule["id"], edition, "KILLED" if killed else "SURVIVED",
                             f"deleted {os.path.basename(rel)}:{lineno} → {after}"))
    finally:
        if "--keep" in sys.argv:
            print(f"copy kept: {work}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    width = max(len(r[0]) for r in rows) + 2
    print(f"{'RULE'.ljust(width)}{'EDITION'.ljust(12)}{'RESULT'.ljust(10)}DETAIL")
    for rid, edition, result, detail in rows:
        print(f"{rid.ljust(width)}{edition.ljust(12)}{result.ljust(10)}{detail}")
    mutable = [r for r in rows if r[2] != "SKIP"]
    killed = [r for r in mutable if r[2] == "KILLED"]
    print()
    print(f"kill rate: {len(killed)}/{len(mutable)} mutable rules")
    if survivors:
        print("SURVIVED rules are not enforced: tighten the pattern or the target files.")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
