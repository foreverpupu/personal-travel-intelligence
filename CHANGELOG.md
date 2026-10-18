# Changelog

Three artefacts share a name but not a release cadence. This file is the only place that records all three.

## 1.1.11 — 2026-10-19

- Fixes a wrong number in `docs/INDEX.md` (claimed 19/19 mutation kills; the checker reports 15/15 rule×edition checks). Documentation only, no rule or behaviour change.
- 1.1.10 and earlier remain as published; this patch exists so the public entry page does not overstate the evidence.

## 1.1.10 — 2026-10-19 · local branch `private-rev2`

Process incident and the fix that came out of it.

- **Incident:** the 1.1.9 release gate blocked on two destination names, but the push still ran because the command piped `release.py` through `tail`, which swallowed the exit code. The published tree therefore contains two country names in evaluation docs. No personal identifiers, bookings or preferences were published; the names are places, not people.
- **Decision:** do not rewrite public history — force-pushing to remove a country name costs more than it buys, and the names remain in the 1.1.9 commit regardless of later edits. Recorded here instead of hidden.
- **Fix:** concrete destinations moved to `travel-data/scenarios-concrete.md` (git-ignored); public `SCENARIOS.md` uses `{WINE_MOUNTAIN_DEST}`-style placeholders. `RUNBOOK.md` substitutes them at run time. The pilot's quotes were genericised.
- **Process fix:** `RELEASE-PIPELINE.md` now says never to pipe `release.py`, and shows an explicit exit-code check. This file exists because a pipe defeated the gate once.

## 1.1.9 — 2026-10-19 · local branch `private-rev2`

Evaluation kit and a pilot that changed the kit.

- `docs/INDEX.md`: one-page entry point (which document for which task, and what the numbers mean). README links to it.
- `evaluation/SCENARIOS.md`, `evaluation/RUNBOOK.md`: three synthetic scenarios, run order, blinding, note-stripping, disk snapshot, κ reporting.
- `scripts/kappa.py`: Cohen's κ for two scorers on binary indicators.
- `evaluation/PILOT-2026-10-19.md`: six runs (one per cell), blind-scored. κ = 1.00 on all indicators — treated as "wording is readable", not validity. S1 and S3 produced the expected direction, S2 was dead, all six outputs carried process notes, and one run **falsely claimed to have written a trip ledger**.
- `REV2-PROTOCOL.md`: **I5 added** — a persistence claim must match the disk. The pilot is labelled exploratory and is not evidence.
- No skill rule changed; no claim of usefulness is made.

## 1.1.8 — 2026-10-19 · local branch `private-rev2`

Project alignment after the upload, no behaviour change on the workspace side.

- Project `pre-trip.md` replaced with the v1.1 candidate (feasibility sanity checks). Owner-confirmed upload; not re-downloaded, so read-back remains unverified and is labelled as such.
- Parity targets corrected: project R6/R7 now point at `publishing-guide.md` only. They previously required the Project `SKILL.md` to carry A4/privacy rules that belong in the publishing guide, which produced a false MISSING.
- Parity matrix: R8/R9 OK, R6/R7/R10 ABSENT (file not on disk), replacing the misleading "MISSING".

## 1.1.7 — 2026-10-19 · local branch `private-rev2`

Fifth external review: the push guard checked ref names, not history.

- **Ancestry check in `pre-push`:** any ref whose commit descends from `b6e63e5` is rejected, which closes `private-rev2:main`, a release tag created on the private branch, and `private-rev2:refs/tags/v9`. Tested: main 0, private 1, tag-on-main 0, tag-on-private 1, private:main 1, private:tag 1.
- **Same check in `release.py` on `main`**, because a hook can be bypassed with `--no-verify` and the release script cannot.
- **Missing term list blocks releases from `main`** (`--allow-missing-terms` overrides explicitly); it stays a warning on the private branch.
- Release runbook adds `git log --oneline main ^origin/main` — exactly one commit expected before pushing.

## 1.1.6 — 2026-10-19 · local branch `private-rev2`

Fourth external review: the publish commands themselves were the risk.

- **`--tags` removed.** Pushing every local tag would publish any tag created on `private-rev2`, whose ancestors contain the pre-redaction text. Publishing now pushes `refs/tags/v<version>` only.
- **Pre-push hook** (`.githooks/pre-push`, install with `git config core.hooksPath .githooks`): blocks every ref except `main`/`master` and `v*` tags. Tested: main 0, private branch 1, `v1.1.6` 0, other tag 1.
- **Publish sequence corrected:** gates run on the branch without tagging; the squash commit on `main` is what gets tagged; the release sheet is regenerated on `main` so its commit matches the tag; `main` is merged back into `private-rev2` after each release.
- **Bundle completeness:** `pack_review.py` now includes every Project rule file (except notes and the private preference file), so the bundle can reproduce the upload gate once those files exist.
- **Privacy scan can fail loudly:** a missing term list now warns that the scan is disabled, and a hit blocks the release instead of warning.

## 1.1.5 — 2026-10-19 · local branch `private-rev2`

Privacy blocker from the second external review. All four items were reproduced.

- `DRYRUN-2026-10-18.md` described routes by real city names; replaced with "capital / wine region / mountain region". The private mapping stays in `travel-data/eval-labels.md`.
- `docs/privacy-terms.txt` was tracked, publishing the very terms it was meant to hide. Moved to `travel-data/privacy-terms.txt` (git-ignored); the release gate reads it from there and degrades gracefully when absent.
- `VALIDATION-PROMPT.md` carried a personal folder name; replaced with a generic path.
- Branch history still contains the pre-redaction text. Publishing is now squash-only, documented in `RELEASE-PIPELINE.md` and `EDITION-PARITY.md`; `release.py` prints a warning when run off `main`.
- R6/R7 in the Project edition are now labelled `MISSING` (confirmed absent in `SKILL.md`) instead of `UNVERIFIED`; the unread `publishing-guide.md` is shown as residual doubt rather than a reason to soften the label. Project upload is gated on `check_all.py --strict` exiting 0.

## 1.1.4 — 2026-10-18 · local branch `private-rev2`

Three blockers from the first external review (path mode, bundle `review-1.1.2`). Each was reproduced before fixing.

- **The checker could not be killed (M3).** `rule_status` accepted a match in *any* target file, so deleting R5 from `SKILL.md` still matched `pre-trip.md` and reported OK. Every existing target file must now contain the marker. Added `scripts/mutation_test.py`, which deletes each marker on a throwaway copy and asserts the gate fails: kill rate 15/15 after tightening the R4 and R10 patterns (each previously appeared twice in its file).
- **Schema contradiction.** The canonical field list in `data-model.md` lacked `provenance` while `decisions.md` had it. Field added to the canonical list.
- **Privacy.** Real trip names in `CHANGELOG.md` and the evaluation docs replaced with synthetic labels (Trip A / group G1); the mapping is kept in git-ignored `travel-data/eval-labels.md`; the release gate now scans `docs/privacy-terms.txt`.
- **Known limitation, unchanged:** the manifest checks presence, not meaning. Rewording a rule to its opposite still passes; only the scenario protocol can catch that.

## 1.1.3 — 2026-10-18 · local branch `private-rev2`

Triggered by the first external review run, which correctly refused to judge after the prompt's path placeholders were left unfilled.

- `pack_review.py` now writes `REVIEW-PROMPT.md` inside the bundle with `{BUNDLE}`, `{REPO}` and the version already substituted — the reviewer never sees a placeholder.
- Prompt hardened: an invalid bundle path must stop the review; `check_all.py` exit 0 is explicitly not approval while `PROJECT DRIFT` is listed.
- `check_all.py --strict` elevates project drift to a failing exit code (opt-in; releases still warn by default).

## 1.1.2 — 2026-10-18 · local branch `private-rev2`

No rule text changed.

- **Review bundle:** `scripts/pack_review.py` — copies tracked files plus the two Project rule files into `dist/review-<version>/`, writes `MANIFEST.sha256`, excludes `travel-data/` and the Project patch notes. The bundle contains its own checker, so a reviewer can verify it before judging it.
- **Validation prompt rewritten:** goal-driven instead of "assume defects"; adds normative grading (MUST/SHOULD/untestable), traceability matrix, mutation test of the checker, edition diff, counter-example search, and version audit. Three delivery modes: path, upload, blind.

## 1.1.1 — 2026-10-18 · local branch `private-rev2`

No rule text changed.

- **Release pipeline:** `docs/RELEASE-PIPELINE.md` — local → GitHub → ChatGPT Project, four gates, version policy, rollback.
- **Machine gate:** `scripts/release.py` — refuses a dirty tree, checks `VERSION` against the changelog, scans published files for emails/phone/ID patterns, writes `dist/release-<version>.md` with per-file hashes.
- **Model gate:** `docs/validation/VALIDATION-PROMPT.md` — five-gate audit prompt, blind A/B prompt, Project upload check, plus the failure modes they are designed to counter.

## 1.1.0 — 2026-10-18 · local branch `private-rev2`

Workspace/Codex edition only; not pushed to the public repository.

- **Schema:** provenance classes defined in `references/data-model.md` (`trip-explicit`, `group-confirmed`, `destination-fit`, `prior-success-inference`, `unknown`) with a precedence order; `decisions.md` template gains a `provenance` field. The rev2 rule previously had no place to record its own output.
- **Rule:** `references/pre-trip.md` gains two feasibility checks — reference class and pre-mortem — both internal, surfaced only when they change a decision.
- **Clarification:** group identity is never assumed; provenance and confidence are independent axes.
- **Verification:** `scripts/check_all.py` + `docs/rule-manifest.json` + `docs/EDITION-PARITY.md`.
- **Evaluation:** `evaluation/REV2-PROTOCOL.md`, `SCORING-SHEET.md`, `DRYRUN-2026-10-18.md`.
- **Known gap:** `project-edition/` is behind this version (R6 partial, R8/R9 missing, R10 unverifiable). Deliberate: the Project edition was received as rev2 and is left byte-identical until you decide to re-upload.

## 1.0.0+rev2 — 2026-10-10 · ChatGPT Project only

- `SKILL.md` and `pre-trip.md` gain the cross-trip preference provenance rule.
- `USER-preferences.md` gains three confirmed entries (experience diversity, holiday timing, a scoped group-specific companion note) and drops a trip-specific destination line.
- Never mirrored to the public repository or to any local workspace until 2026-10-18.

## 1.0.0 — 2026-10-09 · public repository

- Initial public release, commit `e8d5bac`, tag `v1.0.0`.
