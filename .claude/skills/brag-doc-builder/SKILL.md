---
name: brag-doc-builder
description: >-
  Quarterly, compiles your wins log into a structured brag doc for performance reviews — organized
  by competency/impact area with evidence. Use when asked "build my brag doc", "compile my wins for
  review", "brag doc", or run on a quarterly schedule. Requires Google Drive (reads the wins doc,
  drafts the brag doc). Reads doc names and your voice from CONFIG.md.
---

# Brag Doc Builder

## Purpose
Compile a quarter (or more) of wins into a structured, review-ready brag doc so self-reviews and
promo packets write themselves from evidence you already captured.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Default scope is the last quarter. Not time-of-day sensitive.
2. Read the **wins doc** named in `CONFIG.md` across the scope period. If sparse, note the gap but
   proceed with what exists.
3. Organize accomplishments into a brag-doc structure:
   - **Impact areas / competencies** (e.g. Delivery, Leadership/Influence, Technical, Growth of
     others, Strategy). Adapt to the role in `CONFIG.md`.
   - Under each: outcome-focused bullets with concrete evidence (what, the impact, who benefited),
     including links from the wins log where available.
   - A short headline "impact summary" at top.
4. **Draft** into the brag doc named in `CONFIG.md`:
   - If a brag-doc id/name is configured and exists, **append a new dated section** (don't
     overwrite prior quarters).
   - If none exists, create a clearly-named draft doc and report its location.
5. Write in the voice from `CONFIG.md` — confident but factual.

## Output format
A structured section written to the brag doc:
```
# Brag Doc — <Quarter, Year>
## Impact summary
…
## Delivery
- <outcome + evidence + link>
## Leadership / Influence
- …
```
Then post a chat confirmation with the doc location and a 3-line highlight reel.

## Guardrails
- **Auto-action limited to your private brag doc.** Appends/creates only the brag doc named in
  `CONFIG.md`; never shares it, never sends anything, never touches other docs. Appends rather than
  overwrites so prior quarters are preserved (reversible, idempotent per quarter).
- Evidence-based — every claim ties to a real win-log entry; no invented impact.
- Doc names/ids and voice come from `CONFIG.md`.
