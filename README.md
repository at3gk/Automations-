# Personal Automations Kit

A portable, version-controlled kit of scheduled agentic **automations**, vendored directly into the
repo as **project skills** (`.claude/skills/`). Inspired by the idea of giving an agent a *standing
brief* — "tell it what to care about, how to think, and when to run" — then letting it run every day
without you remembering to ask.

## The deployment model (read this first)

The kit is built to run as **Claude Code routines** — most importantly in **cloud sessions**
([claude.ai/code](https://claude.ai/code) scheduled tasks), which clone this repo into a fresh VM
and run server-side. The design follows from that:

- **Logic lives in Skills, vendored into the repo.** Every automation is a `SKILL.md` under
  **`.claude/skills/`**. Because that directory is *part of the clone*, a cloud session
  auto-discovers every skill with **no install step, no marketplace, no network fetch** — you just
  connect the repo. (See [Claude Code on the web → what's available in cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web).)
- **Schedules are thin triggers.** Each scheduled task is one line — *"Run the `meeting-prep`
  skill and post the digest."* The skill holds all the logic; the schedule never does.
- **Connectors are per-account wiring.** Gmail, Calendar, Drive, GitHub are connected per account on
  claude.ai and inherited by its cloud sessions. No credentials, tokens, or IDs ever live in this repo.
- **Personalization lives in one file: [`CONFIG.md`](./CONFIG.md).** Skills reference your details
  *by name* (e.g. "the running wins doc named in CONFIG.md"), never by embedding them. (The
  `inbox-pipeline` subsystem keeps its structured config in `inbox-pipeline/config/*.yml`; CONFIG.md
  points at it.)

> **Why project skills, not a plugin/marketplace.** A `/plugin install` writes to user-scoped
> `~/.claude/` config that does **not** exist in a fresh cloud clone, so plugin skills don't load in
> cloud sessions. Skills committed to the repo's `.claude/skills/` do. This kit therefore vendors
> everything into the repo and uses no marketplace.

## Setup checklist (new account or new repo)

1. **Push this repo** to your own GitHub (or keep using the existing one).
2. **Connect the repo** in [claude.ai/code](https://claude.ai/code) (or open it locally with Claude
   Code) — skills under `.claude/skills/` load automatically; there is nothing to install.
3. **Connect connectors** on the account: Gmail, Google Calendar, Google Drive, GitHub — plus any
   swapped ones (Slack/Linear/Firecrawl) you noted in `CONFIG.md`.
4. **Fill in [`CONFIG.md`](./CONFIG.md)** with the account's name, role, repos, reports, doc names,
   topics, voice, etc. (See "What to fill in" at the bottom.)
5. **Create the thin-trigger schedules** you want, using the exact prompts in the table below. Put
   must-arrive jobs on **Cloud**, local-file jobs on **Cowork** (explained below).

## Start with one (don't automate everything at once)

The fastest path to value is **one** automation that removes your biggest daily friction —
then add more once you feel the relief.

- **Recommended first skill:** `meeting-prep`. It collapses "open twelve tabs and pretend you
  read the agenda" into one morning summary.
- **Recommended discovery step:** run `automation-auditor`. It looks across your connected
  surfaces and *suggests* which automations you actually need — this is how a kit like this
  tends to grow in the first place. It only suggests; it never creates skills on its own.

## Cloud routines vs. Cowork tasks

| | **Cloud routine** (claude.ai/code/routines) | **Cowork task** (desktop app) |
|---|---|---|
| Runs | Server-side (autonomous, no permission prompts) | On your Mac |
| Needs laptop awake? | **No** | **Yes** (desktop app open) |
| Best for | Must-arrive jobs (morning brief), cloud connectors | Jobs needing local files, `gh` CLI, local repos |

**Rule of thumb:** put anything that *must* arrive on time (the morning brief, daily wins) on a
**Cloud routine** so a sleeping laptop never makes you miss it. Use **Cowork** for skills that read
local files or shell out to `gh` against your local checkouts.

## Schedule setup table

Cadences are suggestions — adjust to taste. "Thin-trigger prompt" is the entire **routine prompt**:
it just invokes the skill, which holds the logic.

> 📋 For **copy-paste-ready task blocks** (one per skill, with cadence, surface, the exact prompt,
> and what each needs in `CONFIG.md`), see **[`SCHEDULES.md`](./SCHEDULES.md)** — that's the
> 30-second setup scaffolding for creating or rebuilding your schedules.

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
| `inbox-triage` | optional | Daily, ~6:30 | Cloud | Gmail, Drive | Run the inbox-triage skill in propose mode and post the [Triage] draft. _(Say "apply" to label/archive.)_ |
| `brief-ai-learning` | optional | Daily, ~6:45 (after triage) | Cloud | Gmail, Drive, Calendar | Run the brief-ai-learning skill and add the AI Learning brief to today's Daily Briefs event. |
| `brief-finance` | optional | Weekly, Mon ~6:50 (after triage) | Cloud | Gmail, Drive, Calendar | Run the brief-finance skill and add the Finance brief to today's Daily Briefs event. |
| `brief-career` | optional | Weekly, Mon ~6:55 (after triage) | Cloud | Gmail, Drive, Calendar | Run the brief-career skill and add the Career brief to today's Daily Briefs event. |
| `brief-travel` | optional | Daily, ~6:40 (after triage) | Cloud | Gmail, Drive, Calendar | Run the brief-travel skill and add the Travel brief to today's Daily Briefs event. |
| `capweb-reconcile` | optional | Weekly, Fri ~16:00 (after triage) | Cloud | Gmail, Drive | Run the capweb-reconcile skill and draft the [Brief: Capweb] payment proposal. |

## The `inbox-pipeline` subsystem (producer → consumers)

Six of the skills above form a small **pipeline** rather than standing alone, with their shared
machinery in [`inbox-pipeline/`](./inbox-pipeline/):

- **Producer — `inbox-triage`** labels/archives the unlabeled tail of your inbox from
  `inbox-pipeline/config/*.yml` (the single source of truth) and writes the Drive manifest
  `inbox-state.json`. It also generates importable **Gmail filters** so the server does the bulk
  (`python inbox-pipeline/generate/build_filters.py`).
- **Consumers — `brief-*` and `capweb-reconcile`** read that manifest and query Gmail **by label**.
  The light `brief-*` lenses **consolidate into one "Daily Briefs" calendar event per day** (each
  owns a section, with a reminder you set in `CONFIG.md → Brief delivery`); `capweb-reconcile`
  delivers a private Gmail draft. Run the producer first (the manifest must be fresh).
  `capweb-reconcile` is deterministic and human-in-the-loop: it reconciles timesheets↔invoices with
  exact-dollar matching and only ever **proposes** payments — it never pays.

This subsystem follows the same kit rules (logic in skills, state in Drive, no secrets in git). The
extensions to "drafts not actions": `inbox-triage` may **label and archive** mail (explicit **apply**
mode only, within `taxonomy.yml` policy, anomaly-capped, never deleting), and the `brief-*` lenses
**upsert a self-owned Daily Briefs event** on your own calendar (reversible, self-only — a
notification, not an outward action). See [`inbox-pipeline/docs/CONVENTIONS.md`](./inbox-pipeline/docs/CONVENTIONS.md) for the
full run contract and [`inbox-pipeline/README.md`](./inbox-pipeline/README.md) for the layout.

## How each skill is built (so you can edit safely)

Every skill is a directory `.claude/skills/<name>/SKILL.md`, and every `SKILL.md` follows the same
shape:

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

> **Running these as cloud routines:** at [claude.ai/code/routines](https://claude.ai/code/routines)
> click **New routine**, select this repo, attach the connectors the skill needs, and use the
> thin-trigger prompt from the table above as the routine prompt (e.g. *"Run the inbox-triage skill
> in propose mode and post the [Triage] draft."*). The skills load from `.claude/skills/`
> automatically — there is no plugin to install. See [`SCHEDULES.md`](./SCHEDULES.md) for
> ready-to-paste routine blocks (including a single chained **daily-briefs-pipeline**) and
> `CLAUDE.md` for how the repo is laid out.
