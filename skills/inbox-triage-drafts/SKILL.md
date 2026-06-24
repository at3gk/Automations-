---
name: inbox-triage-drafts
description: >-
  Categorizes unread mail and DRAFTS replies for the routine ones (drafts only — never sends), so
  your inbox is pre-sorted and the easy replies are 90% written. Use when asked "draft my replies",
  "triage and draft", "inbox drafts", or run on a daily schedule. Requires Gmail connector. Reads
  your voice from CONFIG.md.
---

# Inbox Triage + Drafts

## Purpose
Take the routine reply burden off your plate without taking your voice out of it. Sort unread mail
into categories and pre-write drafts for the predictable ones — you review, tweak, and send.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Scope unread mail from roughly the last 24–48h. If run late, keep the
   window (don't draft replies to stale threads that may be overtaken by events — flag those
   instead).
2. Categorize unread Gmail into:
   - **Routine / draftable:** scheduling, simple confirmations, "got it / thanks", short factual
     answers, intros, FYIs needing a one-line ack.
   - **Needs you:** judgment calls, sensitive topics, negotiations, anything high-stakes — do NOT
     draft these; just flag.
   - **Ignore:** newsletters, notifications, marketing — count only.
3. For each **routine** item, create a **Gmail draft** reply in the voice from `CONFIG.md`:
   concise, matches the thread's tone, fills in obvious details, leaves `[[brackets]]` where it
   genuinely needs your input. Save as a draft on the thread — **never send.**
4. Summarize what you drafted and what you flagged.

## Output format
```
📝 Inbox Triage + Drafts — <date>   (drafts saved, nothing sent)

✍️ Drafted replies (N) — review & send:
  • <sender>: <subject> — draft ready  [thread]
🙋 Needs you (no draft):
  • <sender>: <why it needs you>  [thread]
🔕 Ignored: <count>
```

## Guardrails
- **Drafts only — NEVER sends.** Every reply is saved as a Gmail draft for your review. This is the
  hard rule.
- Only drafts genuinely routine mail; anything sensitive, high-stakes, or ambiguous is flagged, not
  drafted.
- Leave `[[brackets]]` rather than inventing facts you don't have.
- Idempotent: if a draft already exists on a thread, update it rather than stacking duplicates.
- Voice comes from `CONFIG.md`.
