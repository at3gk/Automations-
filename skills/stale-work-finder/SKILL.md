---
name: stale-work-finder
description: >-
  Finds all your stale GitHub work that's falling through the cracks — your PRs un-reviewed 7+
  days, PRs assigned to you to review 3+ days, issues idle 14+ days, drafts open 2+ weeks — grouped
  by how embarrassingly stale they are. Use when asked "what's falling through the cracks", "my
  stale work", "stale work finder", or run on a weekly (Monday) schedule. Requires GitHub (gh CLI
  on Cowork, or the GitHub MCP connector on Cloud). Username/repos from CONFIG.md.
---

# Stale Work Finder

## Purpose
Surface the work you opened and forgot — PRs waiting on reviews, reviews waiting on you, issues
gone quiet, drafts collecting dust — before someone else has to remind you. The results are always
a little eye-opening, but it's better to know.

## Instructions
These run unattended — never pause to ask a question. Use your GitHub username from `CONFIG.md`.

On Cowork you can inline live data with the `gh` CLI (replace `<<me>>` with the username in
`CONFIG.md`); on Cloud, gather the same via the GitHub MCP connector instead:

- My open PRs: !`gh search prs --author "<<me>>" --state open --sort updated -L 50`
- PRs awaiting my review: !`gh search prs --review-requested "<<me>>" --state open --sort updated -L 50`
- Issues assigned to me: !`gh search issues --assignee "<<me>>" --state open --sort updated -L 50`

1. **Timing guardrail.** This is a weekly snapshot; not time-of-day sensitive. If it runs late,
   just run it.
2. Collect, across your repos/org from `CONFIG.md`:
   - PRs **you opened** that haven't received a review in **7+ days**.
   - PRs **assigned to you to review** that you haven't reviewed, older than **3 days**.
   - **Issues assigned to you** with no activity in **14+ days**.
   - **Draft PRs you own** that have been drafts for **2+ weeks**.
3. For each item show: repo, title, link, how long it's been stale, and who's involved.
4. **Group by staleness:**
   - 🔴 Embarrassingly stale (3+ weeks)
   - 🟡 Getting dusty (1–3 weeks)
   - 🟢 Just needs a nudge (under a week)

## Output format
```
🧹 Stale Work — <date>

🔴 Embarrassingly stale (3+ wks)
  • <repo> — <title> — stale <N>d — <who>  [link]
🟡 Getting dusty (1–3 wks)
  • …
🟢 Just needs a nudge (<1 wk)
  • …
```
If nothing is stale, say "✅ Nothing stale — your GitHub house is in order."

## Guardrails
- **Read-only.** Lists stale work; never comments, merges, closes, or nudges anyone — that's your
  call. (Merging safe items is `dependabot-triage`'s job, under its own rules.)
- Skip bot-authored and archived-repo noise unless relevant.
- Idempotent; username and repos/org come from `CONFIG.md`.
