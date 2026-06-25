---
name: brief-ai-learning
description: >-
  An inbox-pipeline CONSUMER lens. Reads the AI & Dev labels triaged into your inbox and drafts a
  prioritized [Brief: AI Learning] of genuinely NEW, learnable things (model releases, methods,
  tools, notable papers) — skipping generic news/funding/marketing. Use when asked for an "AI
  learning brief", "what's new in AI for my stack", or on a schedule. Requires Gmail + Drive
  (reads inbox-state.json). Instantiates inbox-pipeline/brief-engine.md.
---

# Brief: AI Learning (consumer lens)

> **Contract:** obeys `inbox-pipeline/docs/CONVENTIONS.md`. This is a thin lens — the procedure is
> `inbox-pipeline/brief-engine.md`; this file only supplies the slots below. Queries Gmail **by
> label**, never the raw inbox. Owns `ledger-ai-learning.json`. Default mode propose.

## Slot values (fed to brief-engine.md)
- **{{BRIEF_NAME}}** = AI Learning
- **{{SLUG}}** = `ai-learning`
- **{{TARGET_LABEL_QUERY}}** = `(label:"AI & Dev/Newsletters" OR label:"AI & Dev/Learning")`
- **{{WINDOW}}** = `3d`
- **{{ITEM_DEFINITION}}** = genuinely NEW / learnable: model releases, methods, techniques, tools,
  notable papers. **Exclude** generic industry news, funding rounds, and marketing.
- **{{OUTPUT_FIELDS}}** = *what it is* / *why it matters to my stack* / *one concrete next step*
- **{{PRIORITY_RUBRIC}}** = relevance to my stack × actionability
- **{{FOCUS}}** = agentic orchestration, harness engineering, integration/tooling
- **{{DRAFT_PREFIX}}** = `Brief: AI Learning`  → draft `[Brief: AI Learning] {date}`
- **{{MAX_ITEMS}}** = 12

## Guardrails
- Read-only except its own draft + (in apply) `ledger-ai-learning.json`. Never labels, archives,
  writes `inbox-state.json`, or touches another routine's ledger.
- Skips items already in its ledger (no re-briefing). Notes overflow past 12.
- Complements the kit's `industry-digest` (broad web scan): this lens is label-scoped to mail
  already triaged and filtered for *learnable* signal relevant to your stack.
