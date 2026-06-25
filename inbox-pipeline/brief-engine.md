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
   **Read-newest rule:** if more than one file shares a state/ledger name (this connector can't update
   in place, so copies accumulate), use the **most-recently-modified** one and ignore the rest — never
   fail or branch because duplicates exist.
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
      header `📋 {title} · {Weekday, Mon D}   ({mode})` and, on the **last** line, the quiet marker
      `— briefs auto-update here daily · [auto:daily-briefs]` (the literal token is how step 1 finds
      the event again; keep it but tuck it at the bottom).
   3. **Upsert THIS lens's section.** A lens's section **begins at its heading line**
      `## {EMOJI} {{BRIEF_NAME}}` and runs until the next `## ` heading or the trailing marker line.
      (Pick a fitting emoji: 🧠 AI Learning · ✈️ Travel · 💳 Finance · 💼 Career · 📋 default.) Build
      the section per the skeleton below. **Replace** that span if the heading already exists
      (idempotent re-run); else **insert** a fresh section just above the trailing marker, keeping
      lenses in a stable order. Preserve every other lens's section **verbatim**; don't change the
      event's start time or reminders. `update_event` with the full new `description`. **Do not use
      HTML-comment delimiters** (`<!-- … -->`) — they render as literal text in a calendar
      description; the heading line is the section key.
   4. **Concurrency guard.** If more than one matching event exists for `{date}` (two lenses raced
      the create), write to the **earliest-created** one and note "duplicate Daily Briefs event —
      merge manually." Staggering lenses a few minutes apart (see `SCHEDULES.md`) avoids this.
   5. **Overflow.** Calendar descriptions hold ~8 KB; the `{{MAX_ITEMS}}` cap keeps a section small.
      If the combined description would exceed that, keep this lens's top items, note the overflow,
      and (when `channel` includes `draft`) rely on the draft for the full list.
   6. **Links for deep dives.** Every item ends with a links line so you can dig in:
      `🔗` the **primary external URL** pulled from the email body when there is one (the article /
      release / paper link), and `✉️` the **source email** at
      `https://mail.google.com/mail/u/0/#all/<thread_id>`. Always include `✉️`; omit `🔗` only when the
      email has no meaningful external link. Never invent a URL — use what's in the message.
   - If `channel` is `draft` or `both`: also create the Gmail **draft** titled `[{{DRAFT_PREFIX}}]
     {date}` with the full brief (legacy behavior). `draft`-only skips the calendar entirely.
   - **Delivery runs in BOTH propose and apply modes** — the event/draft is the brief's output, not
     a world-action (it's on your own calendar and reversible). Only step 9's ledger write is
     apply-gated. State the mode in both the event header and the section heading.
9. **Apply mode only.** Append the briefed IDs (+ run timestamp) to `ledger-{{SLUG}}.json` under that
   **canonical name** in `/AutomationState/`. This connector has no in-place update, so writing
   produces a fresh copy — that's expected and fine (step 1's read-newest rule handles it). **Do not
   emit a "delete the old file" instruction** in the brief; older copies are harmless and superseded.
   Never modify labels/archive, never write `inbox-state.json`, never touch another routine's ledger.

## Output skeleton

The event wraps all lenses. Each lens owns one `## ` section (its heading is the upsert key). Write
like a person would — plain headlines and a sentence of "why," not `What:/Why:/Next:` labels:

```
📋 Daily Briefs · Thu, Jun 25   (apply)

## 🧠 AI Learning
• Gemini 3.5 Flash adds computer-use (cheaper/faster agent tier)
  Opens cheap agentic UI-automation, and lands as a direct competitor to your Claude harness —
  worth a real comparison before you commit a stack.
  → Next: prototype a Flash computer-use run against your agent harness.
  🔗 https://example.com/the-actual-article  ·  ✉️ https://mail.google.com/mail/u/0/#all/19ef9d2fbb2cbdf2
• <next item, same shape…>
(+2 more — narrow the window or raise {{MAX_ITEMS}})
~3 off-topic skipped (2 DataCamp marketing, 1 startup-idea pitch)

## ✈️ Travel — nothing new today.

— briefs auto-update here daily · [auto:daily-briefs]
```

- A lens with **zero items** collapses to a single line: `## {EMOJI} {{BRIEF_NAME}} — nothing new today.`
  (no empty body, no boilerplate).
- If triage is stale/missing, add one quiet line under the heading: `(triage stale — may include
  unlabeled mail)`.
- Item body renders `{{OUTPUT_FIELDS}}` as natural prose; always end with the `🔗 · ✉️` links line.
