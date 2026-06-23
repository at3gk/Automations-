---
name: kudos-radar
description: >-
  Surfaces team wins worth recognizing this week and DRAFTS recognition for you — never sends. The
  noticing and the words stay yours; this just makes sure your brain doesn't steal credit from
  people who earned it. Use when asked "who should I recognize", "kudos radar", "team wins to
  celebrate", or run on a weekly schedule. Requires Gmail/Calendar; optionally GitHub/Slack for
  signals. Reads direct reports and your voice from CONFIG.md.
---

# Kudos Radar

## Purpose
Help you recognize your team consistently — even in a busy week — without automating the human
part. It spots wins and drafts words *in your voice* as a starting point. You decide who to
recognize and how; you send it (or, better, say it).

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Scope is the past week. Not time-of-day sensitive.
2. Gather signals about your people (direct reports + key collaborators from `CONFIG.md`):
   - shipped/merged work (GitHub if connected), things they unblocked, help they gave others,
     wins mentioned in mail/threads you can see, milestones hit.
3. Identify 2–5 **genuinely noteworthy** wins. Favor substance over participation; skip the
   trivial. Note *who*, *what*, and *why it mattered*.
4. For each, **draft** a short, specific recognition message in the voice from `CONFIG.md` —
   concrete about the impact, not generic praise. Offer both a quick-DM version and a
   public-shoutout version.
5. Present as suggestions, clearly marked DRAFT.

## Output format
```
🌟 Kudos Radar — week of <date>   (DRAFTS — nothing sent)

<Person> — <what they did, why it mattered>
  DM draft: "<…>"
  Public draft: "<…>"
```
If nothing rises to the level, say "Quiet week — no standout wins to flag" rather than manufacturing praise.

## Guardrails
- **Drafts only — NEVER sends, posts, or DMs.** Recognition is a human act; this hands you words,
  it doesn't speak for you.
- Specific over generic; if you can't say why it mattered, don't draft it.
- Only use activity normally visible to you — no surveillance.
- Idempotent; people list and voice come from `CONFIG.md`.
