# Personal Travel Intelligence (PTI)

**Plan better. Travel smarter. Remember what really happened.**

[中文说明](README.zh-CN.md) · [Start here](docs/INDEX.md) · [Quick start](docs/QUICKSTART.md) · [Limitations](docs/LIMITATIONS.md) · [Evaluation](evaluation/README.md)

PTI is a **file-based AI travel Skill** for trip planning, on-trip decisions and post-trip storytelling. It adds reusable workflows and explicit, user-controlled travel records to a general-purpose AI assistant. **It does not make the underlying model smarter.**

### What it helps with

- **Plan:** Compare destinations and routes without quietly overwriting existing bookings or ignoring constraints.
- **Adapt:** Respond to delays, fatigue and changes while distinguishing recommendations from executed actions.
- **Remember:** Separate intended plans, confirmed facts, firsthand experiences and uncertainty; export records to user-owned Markdown files.
- **Publish:** Draft factual, human-readable travel guides and Chinese-language DOCX/PDF deliverables, with explicit QA checks.

### Boundaries

- No built-in live inventory, booking, refunds, cancellations or autonomous changes to real reservations.
- Chat history is **not automatically persisted** into files; ChatGPT Project sources are not auto-writable.
- Cross-host migration copies rules, **not** your private files or conversations.
- PDF QA depends on tools available in the host; human editorial review remains necessary.
- **Language scope:** Designed primarily for Chinese-language travel writing. Itinerary/planning workflows can be used in other languages; publishing rules and CJK checks currently assume Chinese. Other-language outputs are **not validated**.

### Quick start

**Codex / compatible agent with project skills:** copy `personal-travel-intelligence/` to `<workspace>/.agents/skills/`; copy the *contents* of `travel-workspace-template/` to your workspace root; reopen the workspace / refresh skills. Invoke `$personal-travel-intelligence` where supported. The QA script checks existing DOCX/PDF files; it does not generate them. See [quick start](docs/QUICKSTART.md) for an optional conversion toolchain. These are installation instructions, **not a claim of a successful Codex desktop test**.

**ChatGPT Project:** upload the eight generic rules (`SKILL.md` plus 7 `references/*.md`) as Project sources and paste the [Project instructions](docs/PROJECT-INSTRUCTIONS.md); manually add/update your own travel records. See [setup](docs/QUICKSTART.md).

**Tencent WorkBuddy:** compatibility and importer format **not yet verified**; no ZIP-install guarantee.

### Example: why state labels matter

- Plan: “We hoped to visit the lighthouse.”
- Actual: “The viewpoint was closed when we arrived.”
- Uncertain: “We don't know why the gate closed.”

PTI should never rewrite the experience as “We toured the lighthouse,” or invent an explanation. [Read the design rationale](docs/WHY-THE-RULES.md).

### Evidence and current status

**Limited v1.0 validation:** personal ChatGPT Project scenarios and document production from one personal trip history; observed issues in earlier output included a US Letter PDF inaccurately described as A4, and internal Project filenames leaking into a friends edition. Additional QA and publishing rules have been added, **but these rules do not guarantee compliance**. No controlled comparison vs a well-prompted general-purpose model; no independent Codex or WorkBuddy installation tests. See [known limitations](docs/LIMITATIONS.md).

### Privacy and license

The public Skill and bundled examples use **fictional or generic illustrations**, not personal travel records or booking data. Inspect all files yourself before publishing; automated scans are partial. Released under the [MIT License](LICENSE). Copyright (c) 2026 Amy Wei.

[中文 README](README.zh-CN.md) · [Experimental evaluation plan](evaluation/README.md) · [Privacy and contribution guidance](CONTRIBUTING.md)
