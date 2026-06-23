---
name: industry-digest
description: >-
  Daily external-news digest on your topics — exactly 5 bullets, low-stakes, time-windowed to the
  last 24h. Use when asked "industry news", "what's happening in <my space>", "daily digest of my
  topics", or run on a daily schedule. Reads topics from CONFIG.md. Requires a web-search connector
  (or Firecrawl); swap per CONFIG.md.
---

# Industry Digest

## Purpose
A tight, daily pulse on the outside world for your topics — five things worth knowing, no more.
Deliberately low-stakes: skim it with coffee and move on.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Window is the last 24h. If it runs late, keep the 24h window (it's a
   rolling digest); don't expand into a giant backlog.
2. Read **industry-digest topics** from `CONFIG.md`.
3. Use the web-search/Firecrawl connector, time-windowed to ~24h, to find the most significant
   developments across those topics.
4. Select the **top 5** by significance and relevance — favor breadth across topics over five
   items on one story. Each must be genuinely newsworthy, not filler.
5. Write each as **one bullet**: the development + a half-line of why it matters, with a source link.

## Output format
```
🗞️ Industry Digest — <date>

1. <headline insight> — why it matters. [source]
2. …
3. …
4. …
5. …
```
Exactly 5 bullets. If a slow news day yields fewer than 5 worthy items, list what there is and say
"slow news day".

## Guardrails
- **Read-only, low-stakes.** Research and report only; never acts on anything.
- Always include a source link; never present rumor as fact — mark "(rumor)" if unverified.
- Hard cap at 5 — resist scope creep.
- Idempotent; topics come from `CONFIG.md`.
