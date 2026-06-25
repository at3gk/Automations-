---
name: one-on-one-prep
description: >-
  Before each 1:1, pulls your last notes plus that person's recent visible activity into a focused
  prep block, so you show up present instead of scrambling. Use when asked "prep my 1:1s", "1:1
  prep for <name>", or run on a morning schedule. Direct reports are listed in CONFIG.md. Requires
  Google Calendar, Google Drive, and Gmail; optionally GitHub/Slack for activity.
---

# One-on-One Prep

## Purpose
Make 1:1s about the human, not the logistics. Walk in with last time's threads, what you owe them,
and a read on their recent work — so the time goes to connection, not catch-up.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Default: prep 1:1s scheduled for **today**. If run right before a
   specific 1:1, prep just that one. If run after a 1:1 already happened, skip it.
2. From Google Calendar, find today's events that are 1:1s — two attendees, or matching a direct
   report in `CONFIG.md`. Skip declined.
3. For each 1:1 partner:
   - **Last notes:** search Drive/Gmail for your most recent notes or thread with them; summarize
     open threads and any action items either side owes.
   - **Recent visible activity:** if connectors allow, pull lightweight recent signals — shipped
     PRs/issues (GitHub), notable sent mail, wins they mentioned. Keep it to what's genuinely
     visible to you; do not surveil.
   - **What you owe them:** cross-reference commitments you made to this person.
4. Assemble a prep block: 2–3 talking points, anything to recognize, and one open question.

## Output format
```
👥 1:1 Prep — <date>

15:00 · <name>
  Since last time: …
  They've been working on: …
  You owe them: …
  Talk about: • … • …
  Worth recognizing: …
```
If no 1:1s today, say "No 1:1s on the calendar today."

## Guardrails
- **Read-only.** Prep notes only — never messages the person or changes anything.
- Surface only activity normally visible to you; this is preparation, not monitoring. Keep it
  respectful and minimal.
- The recognition and the words stay yours — this only gathers context.
- Idempotent; direct reports come from `CONFIG.md`.
