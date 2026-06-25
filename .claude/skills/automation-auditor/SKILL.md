---
name: automation-auditor
description: >-
  Monthly meta-review: looks across your connected surfaces, identifies where you're dropping balls
  or repeating manual work, and SUGGESTS new skills to add to this repo — it does not create them.
  Use when asked "audit my work surfaces", "what should I automate", "automation auditor", "where am
  I dropping balls", or run on a monthly schedule. Uses all available connectors (Gmail, Calendar,
  Drive, GitHub, and any others connected).
---

# Automation Auditor

## Purpose
The meta-skill that grows the kit. Look across everything you've connected, find the patterns —
recurring manual work, repeated questions, balls dropped, things you keep meaning to do — and
*suggest* new automations worth adding. This is how a kit like this tends to start and keep
growing. It only proposes; you decide and build.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Monthly review over roughly the last 30 days. Not time-of-day sensitive.
2. Survey the surfaces available to you (only what's connected): Gmail, Calendar, Drive, GitHub,
   and any others. Look for:
   - **Dropped balls:** threads that went stale on your side, commitments not closed, late
     replies, missed prep.
   - **Repeated manual work:** the same kind of email/summary/report you produce by hand
     repeatedly; recurring searches; copy-paste rituals.
   - **Coverage gaps:** important surfaces or routines none of the existing 23 skills cover.
3. Cross-check against the **existing skills** in this repo (`skills/*/`). Don't re-suggest
   something already covered; instead note if an existing skill should be *tuned* (cadence,
   thresholds in `CONFIG.md`).
4. Produce 3–6 **concrete suggestions**. For each: the problem observed (with evidence), the
   proposed skill (name + one-line purpose + connectors), suggested cadence/run-surface, and
   whether it should default to drafts or auto-action.
5. Note any existing skill that looks unused or mis-tuned.

## Output format
```
🔎 Automation Audit — <month>

Patterns observed:
  • <dropped ball / repeated work> — evidence: …

💡 Suggested new skills (NOT created):
  1. <proposed-skill-name> — <purpose>. Connectors: … · Cadence: … · Surface: … · Drafts/auto: …
     Why: <the pattern it addresses>
  2. …

🔧 Tune existing:
  • <skill> — suggest <change> in CONFIG.md.
```
End with: "These are suggestions only — say the word and I'll scaffold any of them as a new SKILL.md."

## Guardrails
- **Suggestions only — never creates, edits, or schedules skills automatically.** It proposes;
  building stays a deliberate human choice.
- **Read-only** across all surfaces; never sends, posts, merges, or changes anything.
- Evidence-based: tie each suggestion to something actually observed, not generic best-practice.
- Respect privacy — summarize signals, don't dump raw sensitive content.
- Idempotent; honors whatever connectors happen to be available.
