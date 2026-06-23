# Personal Automations Kit

A portable, version-controlled kit of scheduled agentic **automations**, packaged as a Claude
Code plugin. Inspired by the idea of giving an agent a *standing brief* — "tell it what to care
about, how to think, and when to run" — then letting it run every day without you remembering to ask.

## The portability model (read this first)

This kit is built so you can pick it up and drop it onto **any** Claude account (e.g. moving
from a personal to a work account) in minutes:

- **Logic lives in Skills → Git.** Every automation is a `SKILL.md` under `skills/`. The skill
  holds *all* the logic. Schedules never contain logic.
- **Schedules are thin triggers.** Each scheduled task is one line — *"Run the `meeting-prep`
  skill and post the digest."* Recreating your schedules on a new account is a 30-second,
  copy-paste job (see the table below).
- **Connectors are per-account wiring.** Gmail, Calendar, Drive, GitHub, etc. are reconnected
  on each account. No credentials, tokens, or IDs ever live in this repo.
- **Personalization lives in one file: [`CONFIG.md`](./CONFIG.md).** Skills reference your
  details *by name* (e.g. "the running wins doc named in CONFIG.md"), never by embedding them.

Fill in `CONFIG.md`, reconnect your connectors, recreate the thin-trigger schedules — done.

## Transfer checklist (personal → work account)

1. **Push this repo** to your own GitHub (or keep using the existing one).
2. **Add the marketplace:** `/plugin marketplace add << github-user >>/Automations-`
3. **Install the plugin:** `/plugin install personal-automations@claude-automations`
4. **Reconnect connectors** on the new account: Gmail, Google Calendar, Google Drive, GitHub —
   plus any swapped ones (Slack/Linear/Firecrawl) you noted in `CONFIG.md`.
5. **Fill in [`CONFIG.md`](./CONFIG.md)** with the new account's name, role, repos, reports,
   doc names, topics, voice, etc. (See "What to fill in" at the bottom.)
6. **Recreate the thin-trigger schedules** you want, using the exact prompts in the table below.
   Put must-arrive jobs on **Cloud**, local-file jobs on **Cowork** (explained below).

## Start with one (don't automate everything at once)

The fastest path to value is **one** automation that removes your biggest daily friction —
then add more once you feel the relief.

- **Recommended first skill:** `meeting-prep`. It collapses "open twelve tabs and pretend you
  read the agenda" into one morning summary.
- **Recommended discovery step:** run `automation-auditor`. It looks across your connected
  surfaces and *suggests* which automations you actually need — this is how a kit like this
  tends to grow in the first place. It only suggests; it never creates skills on its own.

## Cloud tasks vs. Cowork tasks

| | **Cloud task** (claude.ai/code/scheduled) | **Cowork task** (desktop app) |
|---|---|---|
| Runs | Server-side | On your Mac |
| Needs laptop awake? | **No** | **Yes** (desktop app open) |
| Best for | Must-arrive jobs (morning brief), cloud connectors | Jobs needing local files, `gh` CLI, local repos |

**Rule of thumb:** put anything that *must* arrive on time (the morning brief, daily wins) on
**Cloud** so a sleeping laptop never makes you miss it. Use **Cowork** for skills that read local
files or shell out to `gh` against your local checkouts.

## Schedule setup table

Cadences are suggestions — adjust to taste. "Thin-trigger prompt" is the entire contents of the
scheduled task: it just invokes the skill, which holds the logic.

| Skill | Default on? | Recommended cadence | Run surface | Connectors | Thin-trigger prompt to paste |
|---|---|---|---|---|---|
| `meeting-prep` | ✅ on | Daily, ~7:00 | Cloud | Calendar, Drive, Gmail | Run the meeting-prep skill and post the digest. |
| `pre-meeting-access-check` | ✅ on | Daily, ~7:00 | Cloud | Calendar, Drive | Run the pre-meeting-access-check skill and post the results. |
| `daily-triage-digest` | ✅ on | Daily, ~8:00 | Cloud | Gmail (Slack/Linear opt.) | Run the daily-triage-digest skill and post the digest. |
| `calendar-sanity-scan` | optional | Daily, ~7:00 | Cloud | Calendar | Run the calendar-sanity-scan skill and post any conflicts. |
| `ship-decoder` | ✅ on | Daily, ~8:00 | Cloud (GitHub MCP) or Cowork (gh) | GitHub or web | Run the ship-decoder skill and post the summary. |
| `launch-radar` | optional | Weekly, Mon ~8:00 | Cloud | web search | Run the launch-radar skill and post the radar. |
| `industry-digest` | optional | Daily, ~7:00 | Cloud | web / Firecrawl | Run the industry-digest skill and post the 5 bullets. |
| `competitor-watch` | optional | Weekly, Mon ~8:00 | Cloud | web / Firecrawl | Run the competitor-watch skill and post any changes. |
| `daily-wins-recap` | ✅ on | Daily, ~18:00 | Cloud | Gmail, Calendar, Drive | Run the daily-wins-recap skill and append to the wins doc. |
| `weekly-impact-summary` | optional | Weekly, Fri ~16:00 | Cloud | Drive (reads wins doc) | Run the weekly-impact-summary skill and post the narrative. |
| `brag-doc-builder` | optional | Quarterly | Cloud | Drive (reads wins doc) | Run the brag-doc-builder skill and draft the brag doc. |
| `commitments-tracker` | ✅ on | Daily, ~8:00 | Cloud | Gmail (Slack opt.) | Run the commitments-tracker skill and post open commitments. |
| `follow-up-tracker` | optional | Daily (weekdays) | Cloud | Gmail | Run the follow-up-tracker skill and post threads awaiting my reply. |
| `one-on-one-prep` | optional | Daily, ~7:00 (or before each 1:1) | Cloud | Calendar, Drive, Gmail | Run the one-on-one-prep skill and post prep blocks for today's 1:1s. |
| `kudos-radar` | optional | Weekly, Thu ~15:00 | Cloud | Gmail/Calendar (+Slack opt.) | Run the kudos-radar skill and draft recognition (do not send). |
| `stale-work-finder` | optional | Weekly, Mon ~9:00 | Cowork (gh) or Cloud (MCP) | GitHub | Run the stale-work-finder skill and post my stale work. |
| `pr-review-queue` | optional | Daily (weekdays), ~9:00 | Cowork (gh) or Cloud (MCP) | GitHub | Run the pr-review-queue skill and post my review queue. |
| `dependabot-triage` | optional | Daily, ~9:00 | Cowork (gh) or Cloud (MCP) | GitHub | Run the dependabot-triage skill; merge safe updates, list the rest. |
| `ci-failure-watch` | optional | Daily, ~7:00 | Cloud (GitHub MCP) or Cowork (gh) | GitHub | Run the ci-failure-watch skill and post overnight failures. |
| `travel-logistics-tracker` | optional | Daily, ~7:00 | Cloud | Gmail, Calendar | Run the travel-logistics-tracker skill and post any trip briefs. |
| `inbox-triage-drafts` | optional | Daily, ~8:00 | Cloud | Gmail | Run the inbox-triage-drafts skill; categorize unread and draft routine replies (do not send). |
| `receipts-and-expenses` | optional | Weekly, Fri ~16:00 | Cloud | Gmail, Drive | Run the receipts-and-expenses skill and post receipts to file. |
| `automation-auditor` | ✅ on | Monthly, 1st ~9:00 | Cloud | all available | Run the automation-auditor skill and suggest new automations (do not create them). |

## How each skill is built (so you can edit safely)

Every `SKILL.md` follows the same shape:

- **Frontmatter** — `name` + a `description` written to trigger auto-discovery (what it does,
  when to use it, trigger phrases, required connectors).
- **Purpose / Instructions / Output format / Guardrails** — instructions are numbered and fully
  specified because scheduled runs are **unattended**: a skill can never pause to ask you a
  question mid-run.
- **Drafts, not actions.** Anything outward-facing or hard to undo (emails, messages, posts) is
  **drafted, never sent**. Only low-stakes, reversible work auto-acts, and each skill says so.
- **Timing guardrails.** Time-sensitive skills check the clock first — if a scheduled run fired
  late (laptop was asleep), they skip the now-useless prep and just summarize what was missed.
- **Idempotent.** Safe to run repeatedly; re-running won't duplicate appends or drafts.

## Swapping connectors (for your work account)

The kit defaults to Google Workspace + GitHub. Where a non-Google tool fits, the skill's
frontmatter and `CONFIG.md` mark the connector as swappable:

- **Messaging:** Gmail → add/replace with **Slack** (triage, commitments, kudos).
- **Issues/PRs:** GitHub → **Linear/Jira** (dev maintenance skills).
- **Web monitoring:** generic web search → **Firecrawl** (industry-digest, competitor-watch).

Set your choices in the **Connector choices** section of `CONFIG.md`.

## What to fill in (`CONFIG.md`)

Before scheduling anything, replace the `<< ... >>` placeholders in [`CONFIG.md`](./CONFIG.md):
name & role, voice & tone, industry topics, GitHub username/org/repos, direct reports,
competitor URLs, launch sources, your running "wins" doc name, brag-doc name, receipts folder,
follow-up threshold `N`, and your connector choices. **No secrets** — credentials stay in the
connectors you reconnect per account.

> Replace `<< github-user >>` in the install command above and in
> `.claude-plugin/plugin.json` with your GitHub username.
