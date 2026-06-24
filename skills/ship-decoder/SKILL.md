---
name: ship-decoder
description: >-
  Summarizes what your team/org shipped in the last 24 hours in plain language you can use in
  conversation. Use when asked "what did we ship", "what shipped yesterday", "ship decoder", or
  run on a daily schedule. Sources (repos / changelog / channels) come from CONFIG.md. Requires
  GitHub (MCP connector or gh CLI) and/or a web-search connector; swap per CONFIG.md.
---

# Ship Decoder

## Purpose
So you're never surprised by your own org's launches. Translate the last 24h of merged PRs,
releases, and changelog entries into plain language you could repeat in a hallway conversation —
no jargon, no raw diff-speak.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Window is the last 24h from run time. If the run fired late, widen to
   "since the last digest" so nothing is missed, and say so.
2. Read **ship-decoder sources** from `CONFIG.md` (repos, changelog URL, and/or channels).
3. Gather shipped work from the available connector:
   - **GitHub:** merged PRs and new releases/tags in the listed repos in the window. If using the
     `gh` CLI on Cowork, you may inline live data, e.g.:
     Recent merges: !`gh search prs --merged --sort updated -L 30 "org:<< org >>"`
     (Replace `<< org >>` — or rely on the GitHub MCP connector on Cloud.)
   - **Changelog/web:** if a changelog URL or channels are configured and web search is enabled,
     pull entries dated in the window.
4. For each shipped item, write **one plain-language line**: what changed and why it matters to a
   non-engineer. Group by product area / repo. Collapse trivial chores (version bumps, lint).
5. Add a short "talking points" footer: 2–3 things worth mentioning in conversation today.

## Output format
```
🚀 Shipped — last 24h

<Product area / repo>
  • <plain-language what + why it matters>  [link]

💬 Talking points:
  • …
```
If nothing notable shipped, say "Quiet 24h — nothing notable shipped."

## Guardrails
- **Read-only.** Never merges, comments, or pushes — reporting only.
- Plain language over jargon; if you can't explain why something matters, omit it rather than
  padding.
- Don't leak private repo details beyond what the digest needs.
- Idempotent; sources and connector choice come from `CONFIG.md`.
