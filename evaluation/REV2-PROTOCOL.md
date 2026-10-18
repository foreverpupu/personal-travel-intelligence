# rev2 protocol — does preference provenance change route composition?

Pre-register before running. Fill the prediction column first; do not edit it afterwards.

## Claim under test

> Adding the preference-provenance rule changes route composition: a confirmed group preference stops being the default template, without being silently dropped.

This is a **narrow, testable** claim. It is not "PTI is better than a plain prompt" — that is Experiment 1 in `evaluation/README.md`.

## Design

| Item | Value |
|---|---|
| Arms | A = v1.0.0 skill (no provenance), B = rev2 skill |
| Scenarios | S1, S2, S3 below |
| Runs | 3 per scenario per arm = 18 |
| Context | fresh conversation each run; no prior scenario in context |
| Materials | identical per scenario across arms; fixed dates, party, constraints |
| Order | randomised, interleaved (A,S1 / B,S2 / …), not arm-by-arm |
| Blinding | outputs renamed to random IDs before scoring |
| Scorer | one primary scorer + one spot-check of 6 random runs |

## Scenarios

- **S1.** Same companions as a prior group trip (label G1); a wine-and-mountains destination; 7–9 days; nothing else stated.
- **S2.** Different companions; no stated preferences; destination and dates fixed by the brief.
- **S3.** Same friends; a destination with a strong but different character (recommended: Japan, 8–10 days).

Use synthetic companion briefs. Do not paste real booking references or the real trip ledger into the test.

## Primary indicators (binary, scored from the output only)

| ID | Scenario | Question | Pass |
|---|---|---|---|
| I1 | S1 | Does at least one of the 2–3 options foreground a non-wine, non-nature experience (history, culture, city life)? | yes |
| I2 | S2 | Does the output avoid asserting wine/nature/relaxation as this group's preference? | yes |
| I3 | S3 | Does the output avoid presenting the previous trip's mix as the frame (no "like the last trip", no wine-first default)? | yes |
| I4 | all | Does the output avoid inventing bookings, prices, or opening hours? | yes |

I4 is a regression guard: a provenance win must not cost factual discipline.

## Decision rule

- **Supported** if B passes I1–I3 in ≥2 of 3 runs per scenario, A fails at least one of I1–I3 in ≥2 of 3, and I4 holds in both arms.
- **No measurable effect** if A also passes — likely a ceiling effect; the rule may still be worth keeping for consistency, but it is not evidence of improvement.
- **Harmful** if B drops a confirmed group preference that A kept, or fails I4 more often than A.

Do not pool scenarios into a single score. Three scenarios × three runs is descriptive, not statistical.

## Threats to validity

1. **Self-generated baseline.** If the baseline prompt is weaker than the skill, the comparison flatters B. Keep prompt length and structure matched.
2. **Prompt sensitivity.** Rewrite each scenario twice with different wording; note if results flip.
3. **Model version drift.** Record model, version, date, temperature/tool settings. A rerun on a new model is a new experiment.
4. **Scorer bias.** The scorer knows the hypothesis. Blind the labels and report disagreements rather than averaging them.
5. **Ceiling effect.** Current models may already diversify; then the rule cannot show an effect and the honest conclusion is "not demonstrated".
6. **Internal rule.** The rule is allowed to stay silent, so absence of provenance talk in the output proves nothing.

## Cost and stopping

About 18 generations plus 30 minutes of scoring. Stop early only if I4 fails in either arm (correctness regression) — fix that before continuing.

## What would falsify the claim

- A passes I1–I3 as often as B → no effect.
- B omits the confirmed group preference → the rule over-corrected.
- B's diversity comes from invented attractions → the indicator is gameable; redesign I1 to require named, real places.

## Record

Fill `SCORING-SHEET.md`. Keep raw outputs and the anonymisation key for 6 months. Report the result in `CHANGELOG.md`, not by editing this file.
