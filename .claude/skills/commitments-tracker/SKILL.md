---
name: commitments-tracker
description: >-
  Scans your SENT messages for things you said you'd do ("I'll look into…", "I'll send…", "let me
  follow up") and flags what's still open, so you never quietly break a promise. Use when asked
  "what did I promise", "open commitments", "things I said I'd do", or run on a daily schedule.
  Requires Gmail; optionally Slack (set messaging connector in CONFIG.md).
---

# Commitments Tracker

## Purpose
Protect trust. When you tell someone "I'll look into this" and then forget, that's a trust
problem. This skill finds commitments *you* made in your own outgoing messages and flags the ones
you haven't visibly closed out.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Look back over a rolling window (default ~14 days of sent messages).
   Not time-of-day sensitive.
2. Scan **sent** Gmail (and sent Slack messages if the messaging connector is set in `CONFIG.md`)
   for commitment language from you: "I'll …", "I will …", "let me …", "I'll get you …", "I'll
   follow up", "I'll look into", "by <day>", "next week I'll", etc.
3. For each detected commitment, capture: who you promised, what you promised, when, and any
   deadline you stated.
4. **Determine if it's still open:** check whether you later sent the deliverable / a follow-up on
   that thread, or whether the thread shows it was completed. If you can't find evidence of
   completion, treat it as **open**.
5. Rank by: stated deadline (overdue first), then age, then importance of the recipient.

## Output format
```
🤝 Open Commitments — <date>

⏰ Overdue / dated:
  • To <person> (<date>): "<what you said>" — <how overdue>  [thread]
🔸 Still open (no deadline):
  • To <person>: "<what you said>" — said <N>d ago  [thread]
✅ Looks done (FYI): <count> — not listed.
```
If nothing is open, say "No open commitments detected — you're square."

## Guardrails
- **Read-only.** Never replies, sends, or marks anything done — it only surfaces what you owe.
  Closing the loop stays your action.
- Be conservative: if there's evidence you already delivered, don't nag — move it to "looks done".
- Don't expose sensitive message contents beyond the short quote needed to jog your memory.
- Idempotent; messaging connector comes from `CONFIG.md`.
