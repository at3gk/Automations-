---
name: brief-travel
description: >-
  An inbox-pipeline CONSUMER lens. Reads the Travel label triaged into your inbox and compiles a
  prioritized [Brief: Travel] of itineraries, confirmations, schedule changes, and check-in windows.
  Use when asked for a "travel brief" from labeled mail, or on a schedule. Requires Gmail + Drive +
  Calendar (delivers into the shared Daily Briefs event, codes masked; reads inbox-state.json).
  Instantiates inbox-pipeline/brief-engine.md.
---

# Brief: Travel (consumer lens)

> **Contract:** obeys `inbox-pipeline/docs/CONVENTIONS.md`. Thin lens over
> `inbox-pipeline/brief-engine.md`. Queries Gmail **by label**, never the raw inbox. Owns
> `ledger-travel.json`. Default mode propose.

## Slot values (fed to brief-engine.md)
- **{{BRIEF_NAME}}** = Travel
- **{{SLUG}}** = `travel`
- **{{TARGET_LABEL_QUERY}}** = `label:"Travel"`
- **{{WINDOW}}** = `14d`
- **{{ITEM_DEFINITION}}** = itineraries, confirmations, schedule changes, check-in windows
- **{{OUTPUT_FIELDS}}** = *what* / *dates* / *confirmation #* / *action*
- **{{PRIORITY_RUBRIC}}** = soonest travel date first
- **{{FOCUS}}** = imminent trips and time-critical check-in/gate windows first
- **{{DRAFT_PREFIX}}** = `Brief: Travel`  → section `### Brief: Travel` in the Daily Briefs event
- **{{MAX_ITEMS}}** = 10

## Guardrails
- Read-only except its own section of the Daily Briefs event + (in apply) `ledger-travel.json`.
  Never books, cancels, or changes other calendar events.
- Treat confirmation codes/PNRs as sensitive. The Daily Briefs event is `private`, but its reminder
  can show on a lock screen — so in the event **mask the code** (show last 3 only) while keeping
  dates and what you need to act. To keep travel fully out of the calendar, set `channel: draft` in
  CONFIG → Brief delivery.
- Skips items already in its ledger. Notes overflow past 10.
- Complements the kit's `travel-logistics-tracker` (clusters trips across Gmail **and** Calendar):
  this lens is the label-scoped, manifest-driven view of already-triaged Travel mail.
