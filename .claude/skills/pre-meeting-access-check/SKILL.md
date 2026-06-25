---
name: pre-meeting-access-check
description: >-
  Verifies you can actually open every doc and link referenced in today's calendar invites, and
  flags anything locked along with who to ping for access. Use when asked to "check my doc access",
  "can I open today's agenda docs", or run on a morning schedule alongside meeting-prep. Requires
  Google Calendar and Google Drive connectors.
---

# Pre-Meeting Access Check

## Purpose
Eliminate the "the agenda doc is locked and the meeting starts now" panic by checking access to
every referenced document ahead of time and telling you exactly whom to ask for access.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Using the timezone in `CONFIG.md`, only check docs for meetings that
   haven't happened yet. If the run fired after 10:00, note "Ran late — checked upcoming meetings
   only."
2. Pull today's Google Calendar events (skip declined ones).
3. From each invite's description/body, extract every link: Google Drive/Docs/Sheets/Slides URLs
   first, then other links.
4. For each **Google Drive** link, check access via Drive:
   - Fetch file metadata / permissions. If you can read it → ✅ accessible.
   - If access is denied or the file isn't visible → 🔒 locked. Capture the file's **owner** (or
     the meeting organizer if the owner isn't visible) as the person to ping.
5. For **non-Drive** links, do a lightweight reachability note only ("external link — verify
   manually"); do not attempt logins or bypass anything.
6. Group results: locked items first (action needed), then accessible (reassurance).

## Output format
```
🔐 Pre-Meeting Access Check — <date>

🔒 Needs access (ping before the meeting):
  • <doc title> — for 10:00 <meeting> — ask <owner/organizer>
🌐 External links to eyeball:
  • <url> — for 14:00 <meeting>
✅ All clear (N docs): <doc>, <doc>, …
```
If everything is accessible, lead with "✅ All today's docs are accessible."

## Guardrails
- **Read-only.** Never request access, send messages, or change sharing settings — only *report*
  what's locked and who to ask. (Requesting access is your call to make.)
- Never attempt to bypass permissions or open links behind logins.
- If owner info isn't available, fall back to naming the meeting organizer.
- Idempotent; values like company domain come from `CONFIG.md`.
