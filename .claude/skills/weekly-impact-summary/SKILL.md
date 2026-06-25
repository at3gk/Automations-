---
name: weekly-impact-summary
description: >-
  Weekly, rolls the running wins log into a short, review-ready impact narrative grouped by theme.
  Use when asked "weekly impact summary", "summarize my week", "what did I accomplish this week",
  or run on a weekly (Friday) schedule. Requires Google Drive (reads the wins doc). Reads the wins
  doc name and your voice from CONFIG.md.
---

# Weekly Impact Summary

## Purpose
Turn a week of raw wins-log bullets into a concise narrative you could paste into a status update
or a manager 1:1 — organized by impact, not chronology.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Default scope is the current week (Mon–today). Not time-of-day sensitive;
   if it runs late, still summarize the intended week.
2. Open the **wins doc** named in `CONFIG.md` and read this week's dated entries (the ones
   `daily-wins-recap` appended). If there are no entries, say so and stop.
3. Synthesize across the week:
   - Group accomplishments into 2–4 **themes** (e.g. "Shipped", "Unblocked others", "Strategy").
   - Lead with outcomes and any measurable impact.
   - Note momentum into next week (what's set up to land).
4. Write in the voice from `CONFIG.md` — review-ready, factual, no inflation.

## Output format
```
📈 Weekly Impact — week of <date>

<Theme 1>
  • <outcome-focused line>
<Theme 2>
  • …

Momentum into next week: <1–2 lines>
```
Post in chat. Do **not** modify the wins doc (this skill only reads it).

## Guardrails
- **Read-only** with respect to the wins doc and everything else — drafts a summary in chat only,
  never sends or shares it.
- If the week's wins log is empty/sparse, report that honestly instead of inventing impact.
- Idempotent; wins doc name/id and voice come from `CONFIG.md`.
