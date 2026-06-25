---
name: launch-radar
description: >-
  Weekly scan that surfaces upcoming launches touching your space so you're never blindsided. Use
  when asked "what's launching soon", "launch radar", "upcoming releases in my area", or run on a
  weekly schedule. Reads launch sources and topics from CONFIG.md. Requires a web-search connector
  (or Firecrawl); swap per CONFIG.md.
---

# Launch Radar

## Purpose
Look *forward*, not back: surface launches, releases, and announcements coming up that touch your
team's space, so you can prepare instead of reacting.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Horizon is the next ~2–4 weeks. This is weekly and not time-of-day
   sensitive; if it runs late, just run it.
2. Read **launch sources** and **topics / beats** from `CONFIG.md` (roadmaps, release pages,
   newsletters, competitor blogs).
3. Using the web-search/Firecrawl connector, find signals of *upcoming* (not yet shipped) launches
   in those areas: dated roadmap items, "coming soon", betas, pre-announcements, conference talks.
4. For each, capture: what's launching, who's behind it, expected date/window, and why it matters
   to you. Rank by relevance to your beats and how soon it lands.
5. Note anything that could affect your own team's plans or messaging.

## Output format
```
🔭 Launch Radar — week of <date>

⏰ Imminent (this week/next):
  • <what> — <who> — ~<date> — why it matters: …  [source]
🗓️ On the horizon (2–4 weeks):
  • …
⚠️ Could affect us:
  • …
```
If nothing relevant is upcoming, say "Radar clear — no relevant launches on the horizon."

## Guardrails
- **Read-only.** External research only — never posts, contacts anyone, or acts.
- Cite a source link for every item; if you can't source it, mark it "(unconfirmed)".
- Stay within configured topics/sources to avoid noise.
- Idempotent; sources and topics come from `CONFIG.md`.
