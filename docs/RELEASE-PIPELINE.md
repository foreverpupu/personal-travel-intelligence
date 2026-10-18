# Release pipeline — local → GitHub → ChatGPT Project

One source of truth, two publication targets, three gates. The point is that publishing never depends on remembering which copy is current.

## Roles

| Location | Holds | Never holds |
|---|---|---|
| Local branch `private-rev2` | Working edition, evaluation kit, release sheets, private travel data | — |
| GitHub `main` | Public workspace edition (`references/` layout), docs, evaluation, CHANGELOG | `travel-data/`, `project-edition/`, `_inbox/`, `dist/` |
| ChatGPT Project | Flat Project edition + `USER-preferences.md` | Workspace-only sections, private ledgers |

## Flow

```
edit locally
   │
   ├─ G0  scripts/check_all.py          structure + rule parity
   ├─ G1  scripts/release.py            clean tree, version, privacy scan, sheet
   ├─ G2  model review                  docs/validation/VALIDATION-PROMPT.md
   ├─ G3  behaviour test (rule changes) evaluation/REV2-PROTOCOL.md
   │
   ├─ publish GitHub: squash → commit on main → tag → push explicit ref
   └─ publish Project: regenerate flat files → upload → re-download and hash check
```

G0, G0b and G1 are machine gates. G0b exists because a rule that survives deletion is not enforced, whatever the table says. G2 and G3 are judgement gates; skipping G3 is allowed for text-only releases, skipping G2 is not.

## Commands

```bash
# on private-rev2: gates only, never a tag
python3 scripts/check_all.py            # G0
python3 scripts/mutation_test.py        # G0b: every rule must be killed by deleting it
python3 scripts/release.py --check      # G1, no sheet yet

# publish: squash onto main, tag that commit
git checkout main
git merge --squash private-rev2
git commit -m "v<version>: <summary>"
python3 scripts/release.py              # exit 0 required; never pipe it through tail/head
test $? -eq 0 || { echo "release blocked"; exit 1; }
git tag v<version>
git push origin main refs/tags/v<version>   # explicit ref; --tags pushes every local tag

# keep the branch from diverging after a squash
git checkout private-rev2
git merge main
```

`release.py` refuses a dirty tree on purpose: a release sheet must describe a commit, not a snapshot of unsaved work.

## What goes where

- **Rule or schema change** → workspace edition → regenerate Project files → both targets, same version.
- **Wording only** → same path, patch version, G3 may be skipped and that must be written in the changelog.
- **Private preference change** → `travel-data/USER-preferences.md` and the Project upload only. Never in Git, never in a release sheet.
- **Process/docs change** → GitHub + local; Project does not need re-uploading.

## Version policy

- `VERSION` is the workspace edition's semver; the SKILL.md title carries `v<major>.<minor>`.
- GitHub tags match `VERSION` exactly (`v1.1.1`).
- The Project edition carries its own note in `project-edition/LOCAL-NOTES.md`; do not tag it.
- A public tag is only created after G1 and G2 pass. If G2 finds blockers, fix, re-run, and bump the patch again — never move an existing tag.

## Publishing rule (non-negotiable)

`private-rev2` is never pushed: its history predates the privacy redaction. Publish by squash:

```bash
git checkout main
git fetch origin
test "$(git rev-parse main)" = "$(git rev-parse origin/main)"   # main must match the remote
tree=$(git rev-parse private-rev2^{tree})
commit=$(git commit-tree "$tree" -p main -m "v<version>: <summary>")
git update-ref refs/heads/main "$commit"
git tag v<version>
git push origin main refs/tags/v<version>
```

Use `commit-tree`, not `merge --squash`. A squash merge replays a diff that `main` already contains after the previous release, so the second release conflicts on files both sides changed. `commit-tree` takes the exact tree from the private branch, gives it one parent, and cannot conflict. Never commit directly on `main`: it is a publishing pointer, not a working branch. (This paragraph exists because the 1.1.10 release hit exactly that conflict.)

`--tags` is forbidden: a tag created on `private-rev2` points at a commit whose ancestors contain the pre-redaction text, and pushing the tag publishes that history. Push the single ref instead.

A pre-push hook enforces this. Install it once per clone:

```bash
git config core.hooksPath .githooks
```

It rejects anything except `main`/`master` and tags matching `v*`, **and** rejects any commit that descends from `b6e63e5` (the first private commit). The ref name alone was not enough: `git push origin private-rev2:main` and a tag created on the private branch both look legitimate by name and would have shipped the pre-redaction history.

`release.py` repeats the ancestry check on `main` and blocks there too, because a hook can be bypassed with `--no-verify` while the release script is the step itself. Before pushing, confirm the public branch is a single commit:

```bash
git log --oneline main ^origin/main    # must print exactly one line
```

The privacy term list is mandatory when releasing from `main`: if `travel-data/privacy-terms.txt` is missing, `release.py` blocks (`--allow-missing-terms` overrides, and the override is visible in the command history).

ChatGPT Project upload is gated on `python3 scripts/check_all.py --strict` exiting 0. Without `--strict`, project drift only warns, and an upload would ship a knowingly incomplete edition.

## Verifying a publication actually landed

- GitHub: compare `dist/release-<version>.md` hashes with the files at the tag (`git show v1.1.1:path | shasum`).
- Project: re-download one uploaded file and compare its hash with the same sheet. An upload that was not re-downloaded counts as unverified — this is exactly how a v1.0.0 clone was once mistaken for an update.

## Rollback

- GitHub: `git revert <commit>`, new patch tag. Never force-push `main`.
- Project: re-upload the previous file from `project-edition/archive/<date>/`.
- Local: `git revert` on the branch; the release sheet stays as the record of what was published.

## Cadence

Release when a rule changes, not on a calendar. Batch text fixes into the next rule release. If two releases happen in a week and both change rules, the second one probably needed the behaviour test more than the first.
