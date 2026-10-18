# Public validation kit — exploratory, not statistical proof

Do **not** use any anecdote already embedded in the Skill rules as an independent test. The synthetic Galicia case included here is an evaluation **starter only**; before any public claim of superiority, use new material that has not been added to the Skill, ideally supplied with participant consent. Keep factual material identical across comparison arms and do not update the Skill after seeing test results.

**Experiment 1 — Rule increment:** same model/version, tool access, fresh materials and objective; baseline uses a carefully constructed normal prompt, PTI uses the Skill. At least three independent runs per arm; anonymize outputs. Compare factual errors, constraint handling and human revisions. Do not attribute differences to the Skill when the runtime or prompt budget differs.

**Experiment 2 — End-to-end workflow:** same authorized user data; compare time and edits needed to get a satisfactory Word/PDF, including file persistence and QA. This tests system utility, not isolated rules.

**Experiment 3 — External usability:** 3a facilitated installation (tester uses a preconfigured environment, value of experience) and 3b self-installation (installation friction). Offer a completed past trip for post-trip tasks; no upcoming trip required. Record where each tester gets stuck and whether any one finishes a meaningful task. Small samples are descriptive, not statistically representative.

See `EXPERIMENT-1.md`, `EXPERIMENT-2.md`, `RUBRIC.md`, `EXPERIMENT-3.md`. No real experimental outcomes are included in this release.

## Rule-level test: preference provenance (rev2)

`REV2-PROTOCOL.md` is a pre-registered, rule-level test: three scenarios, two arms, three runs each, binary composition indicators scored blind. `SCORING-SHEET.md` is the record. `DRYRUN-2026-10-18.md` is a hand walkthrough that found four wording ambiguities and is **not** evidence of model behaviour — it exists so the next person does not repeat it.

Scope discipline: this protocol can show that one rule changed route composition. It cannot support a claim that PTI is better than a well-prompted model; that is Experiment 1.
