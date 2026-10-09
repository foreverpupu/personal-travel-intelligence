# Travel Knowledge Base — minimal file-backed model

A trip directory contains:
- `trip-state.md`: current summary, dates, party, constraints, locked resources, next action, last updated.
- `decisions.md`: append-oriented material decisions, including rejected options and expected vs actual outcome.
- `events.md`: timestamped observations and changes; record approximate timestamps as approximate.
- `sources.md`: source IDs, type, location/path/link, capture date, validity date, reliability notes.

**Canonical decision schema (only source of truth):** `id | date | topic | options | constraints | choice | rejected_reasons | expected | actual | lesson | source_ids | status | reopen_trigger | updated`. Other modules and templates MUST reference this schema; do not introduce alternative field sets.

Recommended event fields: ID, trip node, planned, actual, deviation, cause (confirmed/inferred/unknown), evaluation, evidence IDs, event time precision.

Claim status: `proposed`, `confirmed-booking`, `executed`, `canceled`, `official-rule`, `disputed`, `unknown`. Evidence status: `original-record`, `firsthand-user`, `compiled-summary`, `external-source`, `inference`. Do not treat the compiled routebook as independent corroboration of its own facts.

## Update and conflict rules
1. Keep raw source references; don't overwrite originals.
2. Append new evidence, then update the current state with an explicit supersession note.
3. User firsthand correction supersedes an earlier assistant proposal about what occurred; an official rule needs current authoritative verification.
4. For conflicts without resolution, mark `disputed` and avoid definitive published wording.
5. Claim file persistence only after the updated file exists and was read back/verified.
6. Use an `editorial disposition`: `include`, `omit-intentionally`, `carry-forward`, `needs-verification` for claims considered for a publication.

## Minimal example
Fictional example: Decision `DEMO-TRAIL-NIGHTS`: options 1/2 nights; preferred 2; an existing reservation permitted only 1 night; actual stay was 1 night; lesson applies only where opening hours and availability are independently confirmed. Do not generalize one trip into a permanent preference.
