---
name: follow-up-tracker
description: >-
  Finds email threads awaiting YOUR reply for more than N days (N from CONFIG.md) so nothing
  important goes silent on your side. Use when asked "what am I ignoring", "threads waiting on me",
  "follow-up tracker", or run on a daily schedule. Requires Gmail connector.
---

# Follow-Up Tracker

## Purpose
Surface conversations that are stuck *because of you* — threads where someone is waiting on your
reply and it's been longer than your threshold. Distinct from `commitments-tracker` (explicit
promises you made); this catches implicit "your turn" replies.

## Instructions
These run unattended — never pause to ask a question.

1. Read the staleness threshold **N** from `CONFIG.md` (default 3 days).
2. **Timing guardrail.** Not time-of-day sensitive; just run with the rolling window.
3. Scan Gmail for threads where:
   - the **last message was from someone else** (i.e. the ball is in your court),
   - it was directed at you (to/cc you, or a direct ask),
   - and the last message is **older than N days**.
4. Exclude: newsletters, automated/no-reply senders, list mail, threads you've intentionally
   closed, and FYI cc's with no ask.
5. For each, capture: who's waiting, the gist of what they need, how many days it's been stale, and
   a one-word suggested action (reply / delegate / decline / archive).
6. Rank oldest-first, weighting important senders higher.

## Output format
```
⏳ Awaiting Your Reply (>=<N>d) — <date>

  • <person> — <what they need> — <D>d stale → <action>  [thread]
  • …
```
If clear, say "Inbox clear — nothing older than <N>d is waiting on you."

## Guardrails
- **Read-only.** Never replies, archives, or sends — it only lists what's waiting and suggests.
- Conservative on "needs your reply": when ambiguous whether the ball is in your court, leave it
  out rather than create false guilt.
- Don't surface sensitive content beyond a short gist.
- Idempotent; threshold N comes from `CONFIG.md`.
