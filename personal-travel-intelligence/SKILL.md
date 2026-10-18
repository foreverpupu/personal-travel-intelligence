---
name: personal-travel-intelligence
description: Personal travel intelligence for trip planning, itinerary comparison, travel changes and on-trip notes, post-trip reflection, factual travel guides and Chinese-language Word/PDF travel stories. 个人旅行：行前规划、旅中调整、行后路书。
---
# Personal Travel Intelligence v1.1 — Personal Travel Skill

Choose by actual user intent, without forcing an explicit stage:
- 行前／目的地建议／已预订酒店路线接手: use `references/pre-trip.md` and `references/stage-gates.md`.
- 旅中／现在怎么办／天气变化／刚刚去了某地: use `references/on-trip.md`.
- 行后／旅行总结／实走路书／朋友分享版／Word PDF: use `references/post-trip.md` and `references/publishing-guide.md`.
- Use `references/data-model.md` only where structured facts or explicit handoffs are needed.

Four nonnegotiable rules:
1. Do not invent facts, causality, confirmed bookings, live operating conditions, or actual visits.
2. Preserve locked bookings and legal/safety gates; AI recommendations are not executed actions.
3. Never pretend shared knowledge files auto-update; chat-only facts are not archived until a verified workspace write or explicit user upload.
4. Deliverable files must open correctly: verify rendered pages, no clipping or missing Chinese, and Word/PDF content parity before saying QA PASS.

Private preferences and trip states live in the user's authorized workspace, separate from generic Skill rules. Resolve from the current working directory's `travel-data/` when available; ask before accessing personal files outside the workspace. When asked to continue an existing trip, first inspect its uploaded trip-state; if absent, say so and distinguish any other available context. Do not treat sample routebooks or synthetic fixtures as proof of personal history. Keep answers practical and proportional to urgency.

For cross-trip planning, use preference provenance: distinguish current-trip explicit needs, confirmed preferences of the same companions, destination-specific opportunities, and inferences from past success. Do not copy a prior itinerary mix or discard relevant confirmed group preferences merely because they were expressed on a previous trip. See `references/pre-trip.md`.

## Runtime portability
Use `references/` for bundled workflows. If a writable local workspace is authorized, put trip files under `travel-data/trips/<trip-id>/` and write/verify changes there. In a read-only ChatGPT Project, provide an updated file for explicit manual upload. Do not claim that Codex/WorkBuddy workspaces and ChatGPT Project sources automatically sync. Do not treat an output file as installed or archived without checking. For pre-trip templates, use `references/pre-trip-templates.md`; for preferences, read `travel-data/USER-preferences.md` only if present and authorized.

## Publishing and workspace safety additions
- For a reader-facing friends edition, do not leak Project names, filenames, source IDs, evidence-status labels, or editorial verification commentary into the article. Keep provenance in a separate `source-notes.md`.
- Default document page size to A4. After export, inspect actual PDF page dimensions numerically (about 595 × 842 points), check Unicode Chinese extraction and visual clipping. If not verified, report NOT VERIFIED, not QA PASS.
- When migrating an authorized personal travel archive, map a preference file to `travel-data/USER-preferences.md` and each trip ledger to `travel-data/trips/<trip-id>/`. Confirm source-to-target mapping with the user; never overwrite newer records without approval.
