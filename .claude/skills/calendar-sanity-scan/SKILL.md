---
name: calendar-sanity-scan
description: >-
  Scans your calendar for scheduling hazards — double-bookings, long back-to-back stretches with
  no breaks, and meetings with no prep time before them. Use when asked to "check my calendar for
  conflicts", "do I have back-to-backs", "calendar sanity check", or run on a morning/weekly
  schedule. Requires Google Calendar connector.
---

# Calendar Sanity Scan

## Purpose
Catch the structural problems in your schedule before they bite: two meetings at once, a 4-hour
wall of back-to-backs with no bathroom break, or an important meeting you'll walk into cold
because there's no gap to prepare.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Default scope is today; if run weekly (e.g. Monday), scope the whole work
   week. Use the timezone and working hours in `CONFIG.md`.
2. Pull events for the scope from Google Calendar. Skip declined events. Treat tentative events as
   real but flag them.
3. Detect and collect:
   - **Double-bookings:** any two accepted events that overlap in time.
   - **Back-to-back stretches:** 3+ consecutive meetings with <5 min between them; report the
     stretch's total length and suggest where a break could go.
   - **No prep time:** meetings classified important (external, or >5 attendees, or titled
     review/decision/interview) that have no free gap of ≥15 min immediately before them.
   - **Outside working hours:** accepted meetings before/after the working hours in `CONFIG.md`.
4. Rank by severity (double-bookings first).

## Output format
```
🧭 Calendar Sanity — <scope>

⛔ Double-booked:
  • 10:00 <A> overlaps <B>
🥵 Back-to-back (no breaks):
  • 09:00–13:00 — 4 meetings, no gap. Suggest a break ~11:00.
🧠 No prep time before:
  • 15:00 <external review> — book 15 min prep before.
🌙 Outside working hours:
  • 19:30 <meeting>
```
If the calendar is clean, say "✅ No scheduling hazards in <scope>."

## Guardrails
- **Read-only.** Never create, move, or delete events — only flag and suggest. Rescheduling is
  your decision.
- Don't flag intentional focus blocks as problems.
- Idempotent; working hours and timezone come from `CONFIG.md`.
