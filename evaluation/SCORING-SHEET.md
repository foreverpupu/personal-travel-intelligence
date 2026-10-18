# Scoring sheet — rev2 protocol

Copy this file per experiment run and rename it `RUN-<date>.md`. Keep the anonymisation key in a separate file until scoring is finished.

## Session facts (fill before scoring)

| Field | Value |
|---|---|
| Date | |
| Model / version | |
| Interface (Project / local / other) | |
| Temperature / tools | |
| Scorer | |
| Second scorer (spot-check) | |
| Randomisation seed | |

## Per-run scores

`I1–I4` are 1 = pass, 0 = fail. Rubric scores 1–5 follow `RUBRIC.md`. Leave a cell empty if the indicator does not apply to that scenario.

| Run | Arm | Scenario | Output ID | I1 | I2 | I3 | I4 | Factual | Constraint | Usefulness | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A | S1 | | | | | | | | | |
| 2 | B | S1 | | | | | | | | | |
| 3 | A | S1 | | | | | | | | | |
| 4 | B | S1 | | | | | | | | | |
| 5 | A | S1 | | | | | | | | | |
| 6 | B | S1 | | | | | | | | | |
| 7 | A | S2 | | | | | | | | | |
| 8 | B | S2 | | | | | | | | | |
| 9 | A | S2 | | | | | | | | | |
| 10 | B | S2 | | | | | | | | | |
| 11 | A | S2 | | | | | | | | | |
| 12 | B | S2 | | | | | | | | | |
| 13 | A | S3 | | | | | | | | | |
| 14 | B | S3 | | | | | | | | | |
| 15 | A | S3 | | | | | | | | | |
| 16 | B | S3 | | | | | | | | | |
| 17 | A | S3 | | | | | | | | | |
| 18 | B | S3 | | | | | | | | | |

## Indicator summary

| Scenario | Arm A passes | Arm B passes | Difference | Verdict |
|---|---|---|---|---|
| S1 / I1 | /3 | /3 | | |
| S2 / I2 | /3 | /3 | | |
| S3 / I3 | /3 | /3 | | |
| All / I4 | /9 | /9 | | regression guard |

## Disagreements between scorers

| Run | Indicator | Scorer 1 | Scorer 2 | Resolution |
|---|---|---|---|---|
| | | | | |

## Verdict

- [ ] Supported
- [ ] No measurable effect (ceiling)
- [ ] Harmful
- [ ] Inconclusive — reason:

## Free-text failure notes

Quote the exact sentence that failed an indicator. A failed indicator without a quote cannot be reviewed later.
