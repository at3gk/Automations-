---
name: pr-review-queue
description: >-
  Shows just the PRs waiting on YOUR review, ranked by age and importance, so you clear the queue
  in priority order. Use when asked "what do I need to review", "my review queue", "PRs waiting on
  me", or run on a daily (weekday) schedule. Requires GitHub (gh CLI on Cowork, or GitHub MCP on
  Cloud). Username/repos from CONFIG.md.
---

# PR Review Queue

## Purpose
A focused, ranked list of pull requests blocked on your review — so you know exactly what to
review first instead of scanning notifications. Narrower than `stale-work-finder`: this is *only*
your pending reviews, every day.

## Instructions
These run unattended — never pause to ask a question. Use the GitHub username from `CONFIG.md`.

Inline live data on Cowork (replace `<<me>>`), or gather the same via GitHub MCP on Cloud:
- Awaiting my review: !`gh search prs --review-requested "<<me>>" --state open --sort updated -L 50`

1. **Timing guardrail.** Daily snapshot; not time-of-day sensitive.
2. Collect open PRs where your review is requested (or your team's, if you're the reviewer), across
   repos/org in `CONFIG.md`. Exclude PRs you've already reviewed and drafts.
3. For each: repo, title, author, age since review requested, size (lines/files if available), and
   whether it's blocking a release/teammate.
4. **Rank** by a blend of: age (older first), blocking-impact (someone waiting / release), and
   author seniority of need (e.g. a teammate blocked vs. a draft). Put quick wins (tiny diffs) up
   top as easy clears where ties occur.

## Output format
```
🔍 PR Review Queue — <date>   (<N> waiting)

1. <repo> — <title> — @<author> — waiting <N>d — ~<size>  [link]
2. …
⚡ Quick wins (tiny diffs): <repo> #…, <repo> #…
```
If empty, say "✅ Review queue clear — nothing waiting on you."

## Guardrails
- **Read-only.** Lists and ranks; never approves, comments, or requests changes — reviewing stays
  your action.
- Don't include PRs you authored (that's stale-work-finder territory).
- Idempotent; username and repos/org come from `CONFIG.md`.
