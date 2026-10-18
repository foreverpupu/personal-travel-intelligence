# Experiment runbook — from zero to a verdict in one sitting

This is the operational companion to `REV2-PROTOCOL.md`. The protocol says what to measure; this says how to run it without accidentally proving what you hoped.

## 0. Prerequisites (10 minutes)

```bash
# freeze the arms from git, never from the working tree
git archive v1.0.0 personal-travel-intelligence | tar -x -C ../arm-a
cp -R personal-travel-intelligence ../arm-b/personal-travel-intelligence
```

Create `travel-data/USER-preferences.md` in **both** arms with the same synthetic content. If the two arms differ in anything except the skill text, the experiment measures that difference instead.

Check the only intended difference:

```bash
diff -r ../arm-a/personal-travel-intelligence ../arm-b/personal-travel-intelligence
```

## 1. Run order

18 runs: 3 scenarios × 2 arms × 3 repetitions. Interleave arms so drift in model behaviour does not favour one side:

| # | Scenario | Arm |
|---|---|---|
| 1 | S1 | A |
| 2 | S1 | B |
| 3 | S2 | A |
| 4 | S2 | B |
| 5 | S3 | A |
| 6 | S3 | B |
| 7–12 | same pattern, reversed (B first) | |
| 13–18 | randomise with a recorded seed | |

Record: model, interface, date, temperature/tools, seed.

## 2. Generate

Instantiate the placeholders in `SCENARIOS.md` from `travel-data/scenarios-concrete.md` (private, git-ignored), then use the template. One fresh conversation per run; never let a run see another scenario.

Save as `runs/<random-id>.md`. Keep the mapping `random-id → (scenario, arm)` in a separate file that the scorer never opens.

Before and after each run, snapshot the arm's `travel-data/` (`find . -type f | sort`); I5 compares the claim in the output with what actually exists.

## 3. Blind

Before scoring:

```bash
shuf -n 18 < ids.txt    # or any random order you record
```

Rename outputs to `001.md … 018.md`. Strip any sentence that names the skill, the process, or the archival state — the skill itself asks for these notes, so expect them in every output. Record how many outputs carried them as a secondary observation.

## 4. Score

Two scorers, independently, using `SCORING-SHEET.md`. Scorers see only the output text and the indicator definitions. They do not see the arm, the hypothesis, or each other's sheet.

Binary indicators, from `REV2-PROTOCOL.md`:

- I1 (S1): at least one option foregrounds history/culture/city life, not only wine and nature.
- I2 (S2): no assertion that the companions want wine/nature/relaxation.
- I3 (S3): no framing from the previous trip and no wine-first default.
- I4 (all): no invented bookings, prices or opening hours.

## 5. Agreement

```bash
python3 scripts/kappa.py scores.csv
```

`scores.csv` format:

```csv
run,scorer,indicator,value
001,1,I1,1
001,2,I1,1
```

Report κ per indicator. Below 0.6, the indicator wording is the problem; fix it before interpreting the result.

## 6. Verdict

Apply the decision rule in `REV2-PROTOCOL.md`:

- **Supported:** B passes I1–I3 in ≥2/3 per scenario, A fails at least one in ≥2/3, I4 holds in both.
- **No measurable effect:** A also passes. Report it as such; do not rebrand it as "directionally positive".
- **Harmful:** B drops a confirmed group preference or fails I4 more often.
- **Inconclusive:** κ < 0.6 or the run order was broken.

Write the result into `CHANGELOG.md` under a new version. Do not edit the protocol after seeing outputs; if the protocol was wrong, write a new one and mark the old run as exploratory.

## 7. Cost and stopping

About 18 generations and 60–90 minutes of scoring. Stop only for a broken arm (I4 failure in either arm) or κ below threshold. A pilot with one run per cell is allowed to debug the kit; label it `PILOT — not evidence` in the filename.

## 8. When to rerun

New model version, a new destination class, changed user preferences, or a change to more than one rule. A wording-only edit does not justify a rerun.
