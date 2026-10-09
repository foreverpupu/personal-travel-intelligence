# Known limitations and validation status

**Tested (limited):** ChatGPT Project workflows, manual source-file handoff and a few itinerary/on-trip/post-trip cases drawing largely from one private trip history. This is not multi-user production validation.

**Observed output defects in earlier tests:** (1) a Chinese routebook PDF was US Letter despite the model claiming A4; (2) a friends-edition draft contained internal Project file names/editor notes. Fixes added: numeric page-size checks; explicit prohibition on internal names in reader-facing material; separate source notes. They are mitigation rules, not guarantees. Independently check exported files and their metadata.

**Not tested:** incremental benefit vs a well-prompted baseline, native Codex desktop client installation, Tencent WorkBuddy installation and cross-host sync, English-language publishing, live inventory or bookings. Only manual migration of rules and authorized trip data is supported.

**Operational constraints:** hosts may not provide DOCX/PDF export tools, required Python packages or fonts. The QA script reports structural signals and does not replace visual reading. Private travel records must be stored and transferred deliberately.

**Export vs QA:** This repository supplies a DOCX/PDF inspection script, not a guaranteed DOCX/PDF generator. The optional Pandoc + LibreOffice commands in the Quick Start require separately installed tools and fonts; the workflow has not been verified in every target host.

**QA interpretation:** Near-margin text and extra PDF text are warnings requiring human review; complete text outside the page, missing DOCX characters, and non-A4 pages are hard failures. English-only material can pass the generic check; add `--require-chinese` for Chinese-language routebooks. QA cannot determine semantic faithfulness or perfect visual rendering.

**Observed semantic failure in a synthetic rehearsal:** In one run with the Skill files available, an assistant added unsupported details about departure time, transportation, food and weather, and incorrectly made continuing rain an additional cause for skipping a stop. The DOCX/PDF QA script returned PASS because it checks output structure and text preservation, **not factual grounding**. This is an observed failure, not evidence about relative performance against a general-purpose model. Added editorial guidance is a mitigation attempt and has **not** been shown to prevent recurrence.
