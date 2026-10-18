# Synthetic scenarios for the provenance test

All names, groups and dates are synthetic. Use identical text across arms; change only the skill path.

## S1 — same group, wine-and-mountains destination
> Four friends from our 2025 trip (the G1 group) want 8 days in Georgia in late September. Plan the route. Nothing else is fixed yet.

## S2 — different companions, no preferences
> Two colleagues and I have 6 days in Portugal in October. Plan the route. We haven't decided anything.

## S3 — same group, different-character destination
> Same four friends from the 2025 trip (G1). 9 days in Japan in November. Plan the route.

## Templates

Generator prompt:

```
Read the skill at {ARM}/SKILL.md and follow it, including any files it points to.

User request: {SCENARIO}

Produce 2–3 route options with night allocation and a one-line trade-off each, under 450 words.
State any assumption in one line at the top. Do not mention the skill, the test, or your process.
Do not ask questions.
```

Scorer prompt: see `REV2-PROTOCOL.md`; score I1–I3 from the output text only.
