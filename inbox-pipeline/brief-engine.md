# brief-engine.md — the parameterized brief engine

Every light `brief-*` lens is an instance of this one procedure. A lens supplies the slot values
below; the engine is the shared body. (CapWeb does **not** use this engine for its reconciliation —
it delegates to `.claude/skills/capweb-reconcile`.) This keeps "adding a brief" to filling a slot table —
see `docs/ADDING_A_BRIEF.md`.

## Slots a lens must fill

| Slot | Meaning |
|---|---|
| `{{BRIEF_NAME}}` | human name, e.g. "AI Learning" |
| `{{SLUG}}` | ledger slug, e.g. `ai-learning` → owns `ledger-ai-learning.json` |
| `{{TARGET_LABEL_QUERY}}` | Gmail label query, e.g. `(label:"AI & Dev/Newsletters" OR label:"AI & Dev/Learning")` |
| `{{WINDOW}}` | fallback recency window when triage is stale/missing, e.g. `3d` |
| `{{ITEM_DEFINITION}}` | what counts as an item (and what to exclude) |
| `{{OUTPUT_FIELDS}}` | the per-item fields to emit |
| `{{PRIORITY_RUBRIC}}` | how to order items |
| `{{FOCUS}}` | lens on what matters (optional emphasis) |
| `{{DRAFT_PREFIX}}` | section heading in the Daily Briefs event (and, if a draft is also kept, the draft title prefix), e.g. `Brief: AI Learning` |
| `{{MAX_ITEMS}}` | cap; note overflow if exceeded |

## Procedure (engine body)

These run unattended — never pause to ask a question. Obeys `docs/CONVENTIONS.md` (modes,
idempotency, staleness, least privilege).

1. **Read state.** Load `inbox-state.json` from Drive `/AutomationState/`. Read `last_triage`.
2. **Staleness guard.** If `last_triage` is missing or older than `max_staleness` (36h), set
   `STALE = true`.
3. **Query.**
   - Fresh: `{{TARGET_LABEL_QUERY}} after:{last_triage}`.
   - Stale/missing: fall back to `{{TARGET_LABEL_QUERY}} newer_than:{{WINDOW}}` and, if even the
     label may be unapplied, widen to `newer_than:{{WINDOW}}`. **Prominently note** "triage
     stale/missing — results may include unlabeled mail."
   - **Paginate to exhaustion. Ignore `resultCountEstimate`.**
4. **De-dup.** Drop any thread/message whose ID is already in `ledger-{{SLUG}}.json`.
5. **Extract.** Keep only items matching `{{ITEM_DEFINITION}}`; discard the rest (count them).
6. **Emit.** For each kept item, produce `{{OUTPUT_FIELDS}}`.
7. **Prioritize.** Order by `{{PRIORITY_RUBRIC}}`, applying `{{FOCUS}}`. Cap at `{{MAX_ITEMS}}`;
   if more remain, keep the top `{{MAX_ITEMS}}` and **note the overflow count**.
8. **Deliver — upsert the consolidated Daily Briefs event.** Read the **Brief delivery** settings
   from `CONFIG.md` (`channel`, calendar, title, reading time, reminder lead, color, timezone).
   All lenses share **one event per day**; each owns one section of it. Unless `channel` is `draft`
   only:
   1. **Find today's event.** `list_events` on the brief calendar for `{date}` (local
      midnight→midnight); match the event whose description contains the marker `[auto:daily-briefs]`
      and whose title starts with the configured title (`fullText:"[auto:daily-briefs]"` narrows it).
   2. **Create if missing.** `create_event`: `summary = "{title} — {date}"`; `startTime` at the
      configured reading time on `{date}` in your CONFIG timezone (omit `timeZone` to inherit the
      primary calendar's zone); 30-minute block; `availability = AVAILABILITY_FREE` (don't show as
      busy); `colorId` = configured color; `visibility = private`;
      `overrideReminders = [{method:"popup", minutes:<reminder lead>}]`. Seed `description` with the
      header `📋 {title} — {date}   (mode: …)`, a one-line note, and the marker `[auto:daily-briefs]`.
   3. **Upsert THIS lens's section.** The lens owns the block delimited by
      `<!-- {{SLUG}}:start -->` … `<!-- {{SLUG}}:end -->`. Build the section (skeleton below).
      **Replace** that block if present (idempotent re-run); else **insert** it just before the
      trailing marker. Preserve every other lens's block **byte-for-byte**, and don't change the
      event's start time or reminders. `update_event` with the full new `description` (refresh only
      the header's mode tag).
   4. **Concurrency guard.** If more than one matching event exists for `{date}` (two lenses raced
      the create), write to the **earliest-created** one and note "duplicate Daily Briefs event —
      merge manually." Staggering lenses a few minutes apart (see `SCHEDULES.md`) avoids this.
   5. **Overflow.** Calendar descriptions hold ~8 KB; the `{{MAX_ITEMS}}` cap keeps a section small.
      If the combined description would exceed that, keep this lens's top items, note the overflow,
      and (when `channel` includes `draft`) rely on the draft for the full list.
   - If `channel` is `draft` or `both`: also create the Gmail **draft** titled `[{{DRAFT_PREFIX}}]
     {date}` with the full brief (legacy behavior). `draft`-only skips the calendar entirely.
   - **Delivery runs in BOTH propose and apply modes** — the event/draft is the brief's output, not
     a world-action (it's on your own calendar and reversible). Only step 9's ledger write is
     apply-gated. State the mode in both the event header and the section heading.
9. **Apply mode only.** Append the briefed IDs (+ run timestamp) to `ledger-{{SLUG}}.json`. Never
   modify labels/archive, never write `inbox-state.json`, never touch another routine's ledger.

## Output skeleton

The event wraps all lenses; each lens writes only its own delimited section:

```
📋 Daily Briefs — {date}   (mode: propose|apply)
Your daily briefs, consolidated. Each lens fills its section as it runs.
[auto:daily-briefs]

<!-- {{SLUG}}:start -->
### {{DRAFT_PREFIX}}   (N items · mode: propose|apply)
<staleness note, only if triage stale/missing>
1. <highest-priority item> — {{OUTPUT_FIELDS}}
2. ...
(+N more not shown — raise {{MAX_ITEMS}} or narrow the window)
Skipped ~N off-topic items.
<!-- {{SLUG}}:end -->
```
