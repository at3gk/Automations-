---
name: brief-career
description: >-
  An inbox-pipeline CONSUMER lens. Reads the Career label triaged into your inbox and compiles a
  prioritized [Brief: Career] of relevant roles, deadlines, intro/networking asks, and application
  status. Use when asked for a "career brief", "job/networking roundup", or on a schedule. Requires
  Gmail + Drive + Calendar (delivers into the shared Daily Briefs event; reads inbox-state.json).
  Instantiates inbox-pipeline/brief-engine.md.
---

# Brief: Career (consumer lens)

> **Contract:** obeys `inbox-pipeline/docs/CONVENTIONS.md`. Thin lens over
> `inbox-pipeline/brief-engine.md`. Queries Gmail **by label**, never the raw inbox. Owns
> `ledger-career.json`. Default mode propose.

## Slot values (fed to brief-engine.md)
- **{{BRIEF_NAME}}** = Career
- **{{SLUG}}** = `career`
- **{{TARGET_LABEL_QUERY}}** = `label:"Career"`
- **{{WINDOW}}** = `7d`
- **{{ITEM_DEFINITION}}** = relevant roles, deadlines, intro/networking asks, application status
- **{{OUTPUT_FIELDS}}** = *what* / *who* / *deadline* / *suggested action*
- **{{PRIORITY_RUBRIC}}** = deadline, then fit
- **{{FOCUS}}** = time-bound opportunities and warm intros first
- **{{DRAFT_PREFIX}}** = `Brief: Career`  → section `### Brief: Career` in the Daily Briefs event
- **{{MAX_ITEMS}}** = 10

## Guardrails
- Read-only except its own section of the Daily Briefs event + (in apply) `ledger-career.json`.
  Never replies or applies on your behalf — surfaces only.
- Skips items already in its ledger. Notes overflow past 10.
