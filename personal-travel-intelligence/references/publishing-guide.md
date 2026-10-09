# Publishing guide — Friends edition & personal archive v1.0

## Editorial promise
Not a generic destination introduction. Tell the traveler what it *felt like*, what was worth the trade-off, what actually happened, and how a friend can make a better decision.

## Two editions
- **Friends / 分享版**: 1 opening hook, actual sequence, decision points, trade-offs, practical navigation names, safety/time-window notes. Cut weak restaurant catalogues and exaggerated adjectives.
- **Personal archive / 收藏版**: add detailed daily memories, companion feedback (with permission), meal details, notes, price and reservations from evidence, contextual images with accurate caption/date. Do not leak confirmation numbers, IDs, phone numbers of companions or personal location traces.

## Language and structure
- Chinese city / place name + searchable English at first appearance, e.g. 京都（Kyoto）、格拉纳达（Granada）、皇后镇（Queenstown）.
- Wineries and restaurants by their actual official name; explain unfamiliar terms once, e.g. Wine Tram（葡萄酒电车）、Game Drive（野生动物追踪车游）.
- No '百分百能看到鲸鱼', fake reservations, unnamed 'experts say', or invented service quality.
- Prefer lived observations over stale listicles; don't mistake a later award for how the traveler made a decision on the day.

## Evidence boundaries in narrative prose
- Vivid writing is welcome, but do not invent **actions, departure times, transport modes, purchases, food/drinks, weather intensity or progression, specific visual details, or causal explanations** absent from the user's record. For example, “it rained” does not establish “the rain did not stop” or “we canceled because of rain.”
- Preserve a traveler's actual feelings when supported; avoid putting new emotions or scenic impressions in their voice. When the facts are thin, write concisely or request more recollections rather than filling gaps with atmosphere.
- This is an editorial rule, not proof the model will follow it. The PDF QA script only checks technical output fidelity and cannot certify factual truth.

## Page design
- A4; heading hierarchy; 10–11 pt Chinese body; reasonable line spacing; no split tables; section breaks only as needed.
- Keep real photographs optional unless their location/date are sufficiently grounded.
- Word editable first, then searchable PDF; PDF and Word must match.
- Include compact as-of note for hours, contacts, prices, timetables.

## QA checklist (must actually run)
1. Content check against provided source and discrepancy list.
2. Internal date/route/order consistency.
3. No cross-trip or synthetic test details.
4. Render Word to page images, inspect page boundaries, headers, line breaks and any tables.
5. Render PDF to images; extract/search Chinese place names and check replacement glyphs/compatibility radicals.
6. Compare **full normalized Word and PDF Chinese text**, not only a handful of keywords; any missing Chinese character fails publication; check for missing English words too. Log extra PDF text separately (e.g., repeated headers/footers), and investigate every missing visible character.
7. Check word/page geometry (A4 expected), detect visible text outside pages (fail). Text within 20 pt of a left/right margin is an advisory flag requiring visual review, not an automatic failure. Unexpected extra PDF text is also advisory until compared with legitimate headers/footers; visually inspect each page at >=150 dpi.
8. Mark any check not performed as NOT TESTED, never 'PASS'.
