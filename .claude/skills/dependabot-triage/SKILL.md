---
name: dependabot-triage
description: >-
  Finds Dependabot/dependency-update PRs across your repos and safely merges the low-risk ones
  (passing CI, patch/minor, dev-deps), while listing anything that needs a human. Use when asked
  "triage dependabot", "merge safe dependency updates", "dependabot triage", or run on a daily
  schedule. Requires GitHub (gh CLI on Cowork, or GitHub MCP on Cloud). Repos from CONFIG.md.
---

# Dependabot Triage

## Purpose
Clear the steady drip of dependency-update PRs: auto-merge the genuinely safe ones so they stop
piling up, and surface the risky ones for a human decision. This is the one dev skill that *acts* —
under strict safety rules, because dependency churn is high-volume and low-stakes when bounded.

## Instructions
These run unattended — never pause to ask a question. Use repos/org from `CONFIG.md`.

Inline live data on Cowork, or gather via GitHub MCP on Cloud:
- Open Dependabot PRs: !`gh search prs --author "app/dependabot" --state open --sort updated -L 50`

1. **Timing guardrail.** Daily; not time-of-day sensitive.
2. Across repos in `CONFIG.md`, list open dependency-update PRs (Dependabot/Renovate).
3. Classify each as **SAFE to auto-merge** only if ALL hold:
   - CI is **green** (all required checks passing),
   - it's a **patch or minor** bump (never a major),
   - no merge conflicts,
   - it's a dev/build dependency OR a patch on a runtime dep with passing tests,
   - the repo isn't flagged "manual-only" in `CONFIG.md`.
   Otherwise → **NEEDS HUMAN**.
4. For SAFE PRs: merge them (respecting each repo's required checks/branch protection — never
   bypass). Prefer the repo's standard merge method.
5. For NEEDS-HUMAN PRs: do nothing but explain *why* (major bump / failing CI / conflict / runtime
   dep without coverage) so the human can act fast.

## Output format
```
📦 Dependabot Triage — <date>

✅ Merged (safe): <N>
  • <repo> — <dep> <old>→<new> (patch, CI green)
🟠 Needs human: <N>
  • <repo> — <dep> <old>→<new> — reason: major version bump
  • <repo> — <dep> — reason: CI failing
```

## Guardrails
- **Auto-action is bounded and reversible.** Only merges PRs meeting EVERY safe-criterion above;
  a dependency merge is revertable. When in doubt, route to NEEDS-HUMAN — never merge a major bump,
  a red build, or anything in a manual-only repo.
- **Never bypasses branch protection or required reviews**, never force-merges, never edits code.
- Major versions, failing CI, and conflicts are always human decisions.
- Idempotent (already-merged PRs are skipped); repos and manual-only flags come from `CONFIG.md`.
