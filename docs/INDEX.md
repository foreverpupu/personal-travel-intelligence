# Start here

One page to find the right document without reading the repository.

## What this is

Personal Travel Intelligence (PTI) is a Markdown skill for trip planning, on-trip decisions and post-trip routebooks. It is deliberately boring: rules in files, personal data in a separate workspace, every claim about quality backed by a command you can rerun.

## Three editions, one source

| Edition | Where | Format | Updated by |
|---|---|---|---|
| Workspace / Codex | `personal-travel-intelligence/` | `references/*.md` | editing here first |
| ChatGPT Project | `project-edition/` (mirror) | flat `*.md` | manual upload |
| Public | GitHub `main` | workspace edition | squash release |

They are not copies of each other. See [EDITION-PARITY.md](EDITION-PARITY.md) for what differs and how drift is measured.

## Pick your task

**I want to use it**
→ [QUICKSTART.md](QUICKSTART.md). Copy `travel-workspace-template/` into a workspace, keep `travel-data/` private.

**I want to change a rule**
→ [CHANGE-PROTOCOL.md](CHANGE-PROTOCOL.md). Eight steps, one of which is a mutation test.

**I want to publish**
→ [RELEASE-PIPELINE.md](RELEASE-PIPELINE.md). Gates G0–G3, squash-only, explicit tag ref.

**I want to verify someone else's claim**
→ [validation/VALIDATION-PROMPT.md](validation/VALIDATION-PROMPT.md), then `python3 scripts/pack_review.py`.

**I want to know whether the skill actually helps**
→ `evaluation/REV2-PROTOCOL.md` and `RUNBOOK.md`. This is the only question the repository cannot answer yet.

## Commands

```bash
python3 scripts/check_all.py          # structure + rule parity
python3 scripts/check_all.py --strict # project drift becomes fatal
python3 scripts/mutation_test.py      # every rule must die when deleted
python3 scripts/release.py            # dirty-tree, version, privacy, release sheet
python3 scripts/pack_review.py        # publishable-only bundle for external review
```

## What the numbers mean

- `19/19` rules killed by mutation: the checker enforces them, not just mentions them.
- `ABSENT` in the parity table: the file is not on this disk; it is not a pass and not a failure.
- A release sheet with hashes: the only proof that what you published is what you tested.

## Honest status

- Consistency, traceability and privacy: measured and enforced.
- Usefulness versus a well-prompted model: **not demonstrated**. No experiment has been run yet.
