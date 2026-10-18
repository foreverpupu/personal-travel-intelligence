# Synthetic scenarios for the provenance test

Destination names are placeholders on purpose: the public repo carries the structure, and the concrete names live in a private file (`travel-data/scenarios-concrete.md`, git-ignored). Substitute before a run.

## Placeholders

| Token | Concrete value (private) | Why this kind of place |
|---|---|---|
| `{WINE_MOUNTAIN_DEST}` | see private file | a destination whose obvious draw is wine and mountains |
| `{MIXED_DEST}` | see private file | a destination with several unrelated regional characters |
| `{DIFFERENT_DEST}` | see private file | a destination with a strong but different character from the prior trip |

## S1 — same group, wine-and-mountains destination
> Four friends from our 2025 trip (the G1 group) want 8 days in {WINE_MOUNTAIN_DEST} in late September. Plan the route. Nothing else is fixed yet.

## S2 — different companions, no preferences
> Two colleagues and I have 6 days in {MIXED_DEST} in October. Plan the route. We haven't decided anything.

## S3 — same group, different-character destination
> Same four friends from the 2025 trip (G1). 9 days in {DIFFERENT_DEST} in November. Plan the route.

## Templates

Generator prompt:

```
Read the skill at {ARM}/SKILL.md and follow it, including any files it points to.

User request: {SCENARIO}

Produce 2–3 route options with night allocation and a one-line trade-off each, under 450 words.
State any assumption in one line at the top. Do not mention the skill, the test, or your process.
Do not ask questions.
```

Scorer prompt: see `REV2-PROTOCOL.md`; score I1–I5 from the output text only, plus the disk snapshot for I5.
