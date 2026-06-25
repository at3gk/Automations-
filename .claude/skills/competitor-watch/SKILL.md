---
name: competitor-watch
description: >-
  Monitors specific competitor URLs/feeds from CONFIG.md for meaningful changes (pricing, product,
  positioning, launches) and reports only what actually changed. Use when asked "watch competitors",
  "what changed on <competitor>", "competitor watch", or run on a weekly/daily schedule. Requires a
  web-search/monitoring connector (or Firecrawl); swap per CONFIG.md.
---

# Competitor Watch

## Purpose
Keep an eye on a defined set of competitor pages/feeds and surface *meaningful* changes — new
features, pricing moves, messaging shifts, launches — while filtering out cosmetic noise.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Compare against the last run's state. If this is the first run, establish
   a baseline and say so (no "changes" on a first run).
2. Read **competitor URLs / feeds** from `CONFIG.md`.
3. For each URL/feed, fetch current content via the web/Firecrawl/monitor connector.
4. Identify **meaningful** changes only:
   - pricing/plan changes, new or removed products/features, positioning/headline changes,
     launch or shutdown announcements, notable hiring/funding signals if on the page.
   - Ignore cosmetic churn (timestamps, rotating testimonials, minor copy edits).
5. For each meaningful change: what changed, old → new where visible, and why it might matter.

## Output format
```
🛰️ Competitor Watch — <date>

<Competitor> (<url>)
  • CHANGED: <what> — <old> → <new> — why it matters: …
<Competitor 2>
  • No meaningful change.
```
If nothing meaningful changed anywhere, say "No meaningful competitor changes since last run."

## Guardrails
- **Read-only.** Observation only — never contacts competitors, signs up, or submits forms.
- Only fetch the URLs/feeds listed in `CONFIG.md`; don't crawl beyond them.
- Distinguish "changed" from "couldn't fetch" — report fetch failures separately, don't call them
  changes.
- Idempotent; watch list comes from `CONFIG.md`.
