---
name: brief-finance
description: >-
  An inbox-pipeline CONSUMER lens. Reads the Finance labels triaged into your inbox and compiles a
  prioritized [Brief: Finance] of statements due, payments, balance/fraud alerts, and material
  account changes. Use when asked for a "finance brief", "what bills/alerts need me", or on a
  schedule. Requires Gmail + Drive + Calendar (delivers into the shared Daily Briefs event, account
  numbers masked; reads inbox-state.json). Instantiates inbox-pipeline/brief-engine.md. Read-only —
  never pays or moves money.
---

# Brief: Finance (consumer lens)

> **Contract:** obeys `inbox-pipeline/docs/CONVENTIONS.md`. Thin lens over
> `inbox-pipeline/brief-engine.md`. Queries Gmail **by label**, never the raw inbox. Owns
> `ledger-finance.json`. Default mode propose.

## Slot values (fed to brief-engine.md)
- **{{BRIEF_NAME}}** = Finance
- **{{SLUG}}** = `finance`
- **{{TARGET_LABEL_QUERY}}** = `(label:"Finance/Banking & Cards" OR label:"Finance/Investing")`
- **{{WINDOW}}** = `7d`
- **{{ITEM_DEFINITION}}** = statements due, payments, balance/fraud alerts, material account changes
- **{{OUTPUT_FIELDS}}** = *what* / *amount* / *due date* / *action*
- **{{PRIORITY_RUBRIC}}** = due date, then amount
- **{{FOCUS}}** = time-sensitive money items first; surface anything that looks like fraud loudly
- **{{DRAFT_PREFIX}}** = `Brief: Finance`  → section `### Brief: Finance` in the Daily Briefs event
- **{{MAX_ITEMS}}** = 12

## Guardrails
- **Read-only.** Never pays, schedules, replies, or moves money — it only surfaces and recommends.
  In apply it writes only `ledger-finance.json`.
- Treat account details as sensitive. The Daily Briefs event is `private`, but its reminder can show
  on a lock screen — so in the event **mask identifiers** (full account/card numbers → last 4) while
  keeping what you need to act (amount, due date). Never forward/send. If you'd rather keep finance
  fully out of the calendar, set `channel: draft` in CONFIG → Brief delivery.
- Skips items already in its ledger. Notes overflow past 12.
- Distinct from the kit's `receipts-and-expenses` (which files receipt copies): this lens reports
  due/alert items from already-triaged Finance mail.
