# Stage Gates, Risk and Stop Rules

## Risk classes
- **Blocking:** safety, legality, route feasibility, key reservation/transport. Resolve or adopt a verified safe alternative before dependent action. If neither is possible, explicitly mark unverified and defer the dependent action.
- **Carry Forward:** weather, seasonal bloom, day-of operations. Set owner/trigger/check-by time and backup.
- **Accept Uncertainty:** noncritical details. Search up to two focused rounds by default, then reduce precision or omit; never invent.

## User-facing milestones
1. Route architecture locked: core experiences, constraints, critical dependencies and alternatives identified.
2. Departure readiness: bookings/status, key routes, operating restrictions, contacts, and contingencies distinguished.
3. Publication frozen: source-to-text reconciliation, content review, privacy tier, and rendered file QA passed.

## Reopen
Reopen frozen decisions only when critical evidence changes, external conditions materially change, or the user changes a core requirement. A newly discovered attractive stop is not sufficient alone.

## Exit criteria
- The next decision is actionable; no unresolved Blocking issue for that action.
- Carry Forward items have check times/conditions and fallbacks.
- Nonessential unknowns have been accepted and labeled.
- The user need not complete every possible field to advance.

## Publication QA (use the included smoke-check script plus visual review)
- Source-to-manuscript reconciliation: every `include` item present; every omission deliberate.
- Verify rankings with category and year; distinguish first-person experience and external rules.
- Check style/typography, table cell font sizes, pagination, mixed Chinese-English line breaks, and mobile readability.
- PDF text layer: test Chinese search/copy, detect suspicious Unicode compatibility/radical characters, inspect fonts per page.
- Privacy: friend version versus public version; remove private room numbers, personal phone numbers, booking references when appropriate.
- Content Gate and File Gate are separate; neither substitutes for the other.
