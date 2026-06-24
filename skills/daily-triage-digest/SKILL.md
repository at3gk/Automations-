---
name: daily-triage-digest
description: >-
  Sweeps Gmail (and Slack/Linear if connected) for the things that genuinely need your attention
  today, groups them by urgency, and ignores the rest. Use when asked to "triage my inbox", "what
  needs me today", "daily digest", or run on a morning schedule. Requires Gmail; optionally Slack
  and/or Linear (set messaging/issue connectors in CONFIG.md).
---

# Daily Triage Digest

## Purpose
Replace inbox-scrolling with one prioritized digest of what actually needs you today. The goal is
*signal* — surface the few things that matter and explicitly drop the noise.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Read the urgency window from `CONFIG.md` (default: today + tomorrow).
   If the run fired late in the day, still produce the digest but label it "afternoon catch-up".
2. **Gmail:** scan unread + recently received mail from roughly the last 24h (and anything still
   unread from the urgency window). Identify items that need *you specifically*: direct asks,
   questions awaiting your answer, deadlines, approvals, things where you're the blocker.
3. **Messaging connector (optional):** if `CONFIG.md` sets Slack/Linear, include DMs/mentions and
   assigned issues that need action. If not connected, skip silently.
4. Aggressively **ignore**: newsletters, automated notifications, FYI cc's, marketing, anything
   already handled. Do not list these individually — just a count.
5. **Group by urgency:**
   - 🔴 **Today / blocking** — needs a response or action today.
   - 🟡 **This week** — important but not same-day.
   - 🟢 **FYI worth knowing** — no action, but you'd want to know.
6. For each item: one line — who, the ask, and the suggested next step (e.g. "reply", "approve",
   "delegate"). Link the source.

## Output format
```
📬 Daily Triage — <date>

🔴 Today / blocking (N)
  • <sender>: <the ask> → <next step>  [link]
🟡 This week (N)
  • …
🟢 FYI (N)
  • …

Ignored ~<N> low-signal items (newsletters, notifications, cc's).
```

## Guardrails
- **Read-only / drafts-never-sent.** This skill does NOT reply, archive, or change anything — it
  only surfaces and recommends. (Drafting replies is `inbox-triage-drafts`'s job.)
- Bias toward fewer, higher-confidence items; when unsure, put it in 🟢 rather than 🔴.
- Never expose full message bodies of sensitive mail — summarize.
- Idempotent; connector choices and urgency window come from `CONFIG.md`.
