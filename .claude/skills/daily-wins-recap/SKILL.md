---
name: daily-wins-recap
description: >-
  Each evening, reads your sent mail, calendar, and any work log to capture concrete
  accomplishments and appends them to your running "wins" doc — framed as facts, not a to-do list.
  Use when asked "log my wins", "what did I accomplish today", "daily wins recap", or run on an
  evening schedule. Requires Gmail, Google Calendar, and Google Drive connectors. Reads the wins
  doc name and your voice from CONFIG.md.
---

# Daily Wins Recap

## Purpose
Keep a running, factual record of what you actually got done so performance-review season isn't a
panic-stare at a blank doc. It counters the "what did I even do today?" spiral with real data —
and it appends, so the record compounds over time.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Intended for end-of-day. If it runs the next morning instead, recap
   *yesterday* and label the entry with yesterday's date.
2. Gather today's evidence:
   - **Sent mail (Gmail):** messages you sent — decisions made, answers given, things shipped or
     unblocked.
   - **Calendar:** meetings attended (skip declined) — what they moved forward.
   - **Work log (optional):** if a work-log doc/source is named in `CONFIG.md`, include it.
3. Distill into **concrete accomplishments** — outcomes, not activities. Frame as facts:
   "Aligned X and Y on the Q3 plan", not "had a meeting about Q3". No to-dos, no future tense.
4. Locate the running **wins doc** named in `CONFIG.md` (by id if given, else search Drive by
   name). **Idempotency check:** read the doc's tail; if today's dated heading already exists,
   update/merge rather than adding a duplicate.
5. **Append** a dated section with 3–7 bullets in the voice from `CONFIG.md`. Keep it tight and
   honest — no inflation.

## Output format
Appended to the wins doc:
```
## <YYYY-MM-DD>
- <factual accomplishment> 
- …
```
Then post a short confirmation in chat: "Logged N wins for <date> to <doc name>." and echo the
bullets so you can eyeball them.

## Guardrails
- **Auto-action allowed (low-stakes, reversible):** appending to your *private* wins doc is safe
  and reversible, so this skill writes directly. It touches **only** the wins doc named in
  `CONFIG.md` — nothing else, and it never sends mail or shares anything.
- Idempotent: never double-append the same day.
- Facts only — if the evidence is thin, write fewer bullets rather than padding.
- Wins doc name/id and voice come from `CONFIG.md`.
