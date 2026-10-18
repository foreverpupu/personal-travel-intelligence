# Change protocol — how to change this skill without creating another version mess

Use this whenever a rule, schema or template changes. It exists because three environments (public repo, local workspace, ChatGPT Project) drifted apart in October 2026, and nobody could tell which rules were live where.

## Inputs

- the change you want, stated as a behaviour ("stop copying the last trip's mix"), not as wording;
- the current `CHANGELOG.md` and `VERSION`;
- access to the workspace edition (source of truth);
- for Project changes: the affected Project sources, so the mirror can be diffed.

## Steps

1. **Classify.** Rule (changes behaviour) / schema (changes what is recorded) / text (wording only). Rules and schema need a test; text does not.
2. **Assign or reuse a rule ID.** Add it to `docs/rule-manifest.json` with a stable pattern. The pattern must match the new wording and nothing else — test it against a file that should fail.
3. **Edit the workspace edition first.** Nothing else is a source of truth. Keep the edit to one concern per commit.
4. **Decide the Project copy.** Mirror it (rewrite `references/x.md` → `x.md`, drop workspace-only sections) or consciously defer it. A deferred mirror is a recorded gap, not silence: add it to `docs/EDITION-PARITY.md`.
5. **Run `python3 scripts/check_all.py`.** Workspace must be clean. Project drift is reported and must be either fixed or justified in the parity doc.
6. **Test if step 1 said "rule".** Run `evaluation/REV2-PROTOCOL.md` (or the protocol for that rule). If the change cannot be observed in an output, redesign the change — an unobservable rule cannot be verified.
7. **Record.** `CHANGELOG.md` entry with rule IDs, what was tested, what passed, and what remains unknown. Bump `VERSION` (minor for rules, patch for text).
8. **Mirror proof.** Re-download the Project file after upload and diff it. An upload that was not re-downloaded is unverified.

## Parameters you can tune

| Parameter | Default | When to change |
|---|---|---|
| Runs per arm | 3 | raise to 5 if results flip between runs; never below 3 |
| Pass threshold | 2 of 3 | 3 of 3 when the change is safety-related |
| Scenarios | the three rev2 scenarios | add a scenario when a new failure mode appears |
| Scorer | 1 primary + 1 spot-check | 2 independent scorers if the verdict is disputed |
| Rule pattern | one phrase, case-insensitive | switch to a section anchor if the phrase appears twice |

## Quality gates

- Workspace checker clean; project drift listed with an owner and a date.
- Every rule ID appears in at least one edition with a line number you can point to.
- A rule change has either a test result or an explicit "not tested" in the changelog. No third option.
- No file claims a version it does not have. `VERSION`, the SKILL.md title, and the changelog must agree.

## When to re-judge (not just re-run)

- model or interface version changes;
- a new destination class is added to the skill (e.g. multi-country rail trips);
- the user's confirmed preferences change — the preference file is an input to the test, not a constant;
- the Project file set changes shape (renames, splits) — the mirror procedure itself must be re-checked;
- more than ~20% of rules change in one release — rerun the full protocol, not just the changed rule.

## Rollback

`git revert <commit>` on `private-rev2`. The public `main` is never the rollback target for private changes. The Project edition is rolled back by re-uploading the previous file — keep the previous Project files in `project-edition/archive/<date>/`.

## Known failure modes

- Editing the Project copy first, then the workspace: guarantees divergence.
- Adding a rule without a manifest entry: the checker cannot see it, drift returns silently.
- Treating "the file uploaded" as "the rule is live": the 2026-10 transfer of a v1.0.0 clone looked like success and changed nothing.
