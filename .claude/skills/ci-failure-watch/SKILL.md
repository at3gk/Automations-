---
name: ci-failure-watch
description: >-
  Summarizes overnight CI failures across your repos with likely causes, so you start the day
  knowing what's red and why. Use when asked "what CI broke overnight", "ci failures", "ci failure
  watch", or run on a morning schedule. Requires GitHub (GitHub MCP on Cloud, or gh CLI on Cowork).
  Repos from CONFIG.md.
---

# CI Failure Watch

## Purpose
Walk into the morning already knowing which pipelines went red overnight and the probable reason —
so you triage instead of discover.

## Instructions
These run unattended — never pause to ask a question. Use repos/org from `CONFIG.md`.

Inline live data on Cowork, or gather via GitHub MCP on Cloud:
- Recent failed runs: !`gh run list --status failure -L 30`

1. **Timing guardrail.** Window is overnight → now (roughly since end of yesterday). If run later,
   widen to "since the last check" and say so.
2. Across repos in `CONFIG.md`, find workflow runs that **failed** in the window (default branch and
   open PRs). Group by repo + workflow.
3. For each failure, pull the failing job's log tail and infer a **likely cause**: which step
   failed and the category — test failure, lint, build/compile, flaky/timeout/network, infra, or
   dependency. Quote the key error line.
4. Distinguish **persistent** failures (failing repeatedly) from **one-off/likely-flaky** (passed
   before, isolated). Flag anything blocking the default branch as urgent.

## Output format
```
🚨 CI Failures — overnight (<date>)

🔴 Blocking main:
  • <repo>/<workflow> — <step> — likely <cause>: "<error line>"  [run]
🟡 PR / branch failures:
  • …
💨 Likely flaky (passed before, isolated):
  • …
```
If everything's green, say "✅ All pipelines green overnight."

## Guardrails
- **Read-only.** Summarizes; never re-runs jobs, edits workflows, or pushes fixes. (You decide what
  to re-run or fix.)
- Be explicit about confidence — "likely cause" is a hypothesis from logs, not a verdict.
- Idempotent; repos/org come from `CONFIG.md`.
