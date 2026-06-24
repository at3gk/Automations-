---
name: meeting-prep
description: >-
  Builds a per-meeting prep brief from today's calendar so you walk in ready. For each event it
  classifies the meeting (1:1 / team sync / external / focus block) and assembles purpose,
  attendees, linked docs, and 2–3 things to bring. Use when asked to "prep my meetings", "morning
  brief", "what's on my calendar today", or run on a morning schedule. Requires Google Calendar,
  Google Drive, and Gmail connectors (swap Calendar/Drive/Gmail for your org's equivalents if needed).
---

# Meeting Prep

## Purpose
Turn today's calendar into a single, skimmable brief so you arrive at every meeting with context
already synthesized instead of opening twelve tabs. Reads identity, working hours, and timezone
from `CONFIG.md`.

## Instructions
These run unattended — never pause to ask a question; make the best reasonable assumption and note it.

1. **Timing guardrail.** Determine the current local time using the timezone in `CONFIG.md`.
   - If it's before the first meeting and earlier than ~10:00, do full prep for the whole day.
   - If it's already after 10:00 (e.g. the scheduled run fired late because the machine was
     asleep), skip prep for meetings that already happened and only prep meetings still ahead.
     Add a one-line note: "Ran late — prepped remaining meetings only."
2. Pull today's events from Google Calendar (00:00–23:59 local). **Skip events you've declined.**
   Skip all-day informational entries unless they look like a real meeting.
3. For each remaining event, **classify** it as one of: `1:1`, `team sync`, `external`, or
   `focus block`. Use attendee count, domains (external = attendees outside your company domain),
   and title cues.
4. Gather context per event:
   - **Purpose:** infer from title + description/agenda.
   - **Attendees:** list names; flag external attendees and their org.
   - **Linked docs:** find doc/links in the invite body; for each Google Drive link, note the
     title. (Do NOT verify access here — that's `pre-meeting-access-check`'s job.)
   - **Recent context:** if Gmail has a recent thread with the organizer/attendees on the topic,
     summarize the latest state in one line.
5. Produce **2–3 "things to bring"** per meeting — concrete prep tailored to the type:
   - `1:1`: their recent wins/blockers, anything you owe them.
   - `team sync`: status of your items, decisions needed.
   - `external`: who they are, the goal, one smart question.
   - `focus block`: the single outcome to protect the time for.
6. Format per the Output section. Keep each meeting block tight.

## Output format
```
🗓️ Meeting Prep — <weekday, date>   (<N> meetings)

09:30 · [1:1] Sync with <name>
  Purpose: …
  Attendees: …
  Docs: <title> (link)
  Bring: • … • … • …

11:00 · [external] <title>
  …
```
End with a one-line "today at a glance" (busiest stretch, any external meetings, first free block).

## Guardrails
- **Read-only.** This skill never edits calendar events, sends mail, or messages anyone. Output is
  a brief only.
- Skip declined events; never invent attendees, docs, or agenda content — if unknown, write
  "(none found)".
- Idempotent: re-running just regenerates the brief.
- All personal values (name, timezone, company domain) come from `CONFIG.md`.
