# Pre-trip Planning — v1.0

## Purpose and routing
Use for destination exploration, itinerary architecture, resource feasibility, bookings, or route optimization even when a trip is already partially booked. Read `SKILL.md`, `references/data-model.md`, `references/stage-gates.md`, then the canonical templates in `references/pre-trip-templates.md`. Read `travel-data/USER-preferences.md` only if available and authorized; read existing trip files from the resolved workspace if present. Give a useful answer immediately; do not demand a completed intake form.

## Five planning passes (skip completed passes)
1. **Explore:** extract dates, party-specific constraints, budget band, departure point, priorities and deal-breakers. Distinguish explicit preferences from inferred ones. Offer a bounded shortlist with seasonal and logistical trade-offs; do not fabricate prices or availability.
2. **Architecture:** define 3–5 core experiences before day-by-day scheduling. Generate 2–3 *meaningfully different* route structures; show what each gains, sacrifices, and whom it suits. Expose the costs and benefits of hotel changes; avoid route sprawl unless its experience benefit is clear.
3. **Feasibility:** build a dependency chain (rare lodging, long-haul flights, transfers, entry rules, fixed-time experiences). Check real-time inventory only using actual authorized sources. Label every item `proposed` or `confirmed-booking`; never promote a suggestion to a reservation.
4. **Execution design:** after architecture is chosen, allocate nights and daily windows. Distinguish fixed commitments from weather-flexible slots; include realistic travel buffers, meal/parking needs and optional fallback activities.
5. **Departure readiness:** verify current rules, reservations, transit, contact details, and cancellation constraints; issue a concise remaining-actions list with check-by times.

## Exploration vs convergence
- **Divergent:** broaden destinations/route options only while the user is still choosing. Compare against explicit weighted or qualitative criteria; do not force numerical scores.
- **Convergent:** once the user selects an architecture, preserve it as baseline. Reopen only under `stage-gates.md`, not for a new attractive sight.
- **Jump-in:** if flights/hotels are booked, start from locked constraints and optimize the remaining free variables; do not rerun destination discovery.

## Decision record (append to decisions.md)
Use the **canonical decision schema** in `data-model.md`; do not duplicate field definitions. Only record documented rejected-option reasons.

## Five reusable decision heuristics
- Rank scarce resources by **non-substitutability × lead time**, not by itinerary order; identify dependency impacts before booking.
- Reverse-plan hard closing/last-entry deadlines and return-flight chains; distinguish closing from last entry.
- Preserve interchangeable weather windows when the destination and stay length allow; do not prescribe a fixed 2–3 nights everywhere.
- Select season based on must-have experiences first, then compare weather and regional trade-offs.
- Disclose hotel-change cost for each architecture; do not presume fewer hotels always wins.

## Five passes ↔ three user milestones
Explore + Architecture → **route architecture locked**; Feasibility + Execution design + Departure readiness → **departure readiness**; post-trip publication (later module) → **publication frozen**. Gates can be reopened only under `stage-gates.md`.

## Dependency and uncertainty protocol
For each critical item record `resource | dependent choices | status | source/as-of | last decision time | fallback`. Distinguish Blocking / Carry Forward / Accept Uncertainty. If a key dependency fails, reopen only the affected branch. Weather-sensitive activities are not locked as fixed dates unless unavoidable.

## Pre-trip output contract
Default concise response: (a) recommendation and trade-off, (b) what is already locked, (c) next decision, (d) any blocking verification, (e) conditional alternatives. If filesystem is available, write and read back updated trip-state/decisions/sources; otherwise give copy-ready entries and state that no file was persisted.

## Anti-patterns
Do not generate 14 detailed days before destination and core experiences are selected; confuse party preference with user's lifelong preference; invent live fares or rooms; claim future weather; assume driving time equals navigation ETA; keep adding stops after the route is frozen.
