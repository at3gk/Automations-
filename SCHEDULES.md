# SCHEDULES.md — copy-paste scaffolding for your routines

This is the "30-second job" part of the portability model. Every block below is a **ready-to-paste
routine**: a prompt (the *thin trigger* — it just runs a skill; all logic lives in that skill's
`SKILL.md`), a cadence, and the connectors it needs. To set up (or rebuild on a new account):

1. Go to **claude.ai/code/routines → New routine** (or run `/schedule` in any Claude Code session).
   Routines run autonomously on Anthropic's cloud, so your laptop can be closed.
2. **Name** it, paste the block's **Prompt** as the routine prompt, and pick a model.
3. **Repository:** select this repo — the skills are auto-discovered from the cloned `.claude/`.
4. **Connectors:** attach only the ones the block lists under **Connectors** (remove the rest; the
   routine can use any included connector's tools, including writes, with no prompt).
5. **Schedule trigger:** set the **Cadence** shown (presets hourly/daily/weekdays/weekly; **minimum
   1 hour** — custom intervals via `/schedule update`). Times are entered in your local zone.
6. Fill the skill's `CONFIG.md` values (see each block's **Needs in CONFIG.md**).

> Routines run with **no permission prompts** and connectors can write unattended — the "draft,
> don't act" safety lives entirely in each skill, not the routine. A few jobs that read local files
> or shell out to `gh` still suit **Cowork** (desktop app → Automations) instead; those are marked.

> Tip: start with `meeting-prep` only, feel the relief, then add more. Run `automation-auditor`
> first if you want the kit to suggest which of these you actually need.

---

## ✅ Default-on (recommended starting set)

### meeting-prep — Daily ~07:00 — Cloud
- **Prompt:** `Run the meeting-prep skill and post the digest.`
- **Needs in CONFIG.md:** name, timezone, working hours, company domain.

### pre-meeting-access-check — Daily ~07:00 — Cloud
- **Prompt:** `Run the pre-meeting-access-check skill and post the results.`
- **Needs in CONFIG.md:** timezone, company domain.

### daily-triage-digest — Daily ~08:00 — Cloud
- **Prompt:** `Run the daily-triage-digest skill and post the digest.`
- **Needs in CONFIG.md:** urgency window; messaging connector (optional).

### ship-decoder — Daily ~08:00 — Cloud (GitHub MCP) or Cowork (gh)
- **Prompt:** `Run the ship-decoder skill and post the summary.`
- **Needs in CONFIG.md:** ship-decoder sources (repos / changelog / channels), GitHub org.

### daily-wins-recap — Daily ~18:00 — Cloud
- **Prompt:** `Run the daily-wins-recap skill and append to the wins doc.`
- **Needs in CONFIG.md:** wins doc name/id, voice & tone.

### commitments-tracker — Daily ~08:00 — Cloud
- **Prompt:** `Run the commitments-tracker skill and post open commitments.`
- **Needs in CONFIG.md:** messaging connector (optional).

### automation-auditor — Monthly (1st ~09:00) — Cloud
- **Prompt:** `Run the automation-auditor skill and suggest new automations (do not create them).`
- **Needs in CONFIG.md:** nothing required; uses whatever is connected.

---

## ◻️ Optional (add as needed)

### calendar-sanity-scan — Daily ~07:00 or Weekly Mon — Cloud
- **Prompt:** `Run the calendar-sanity-scan skill and post any conflicts.`
- **Needs in CONFIG.md:** working hours, timezone.

### launch-radar — Weekly Mon ~08:00 — Cloud
- **Prompt:** `Run the launch-radar skill and post the radar.`
- **Needs in CONFIG.md:** launch sources, topics; web-search connector.

### industry-digest — Daily ~07:00 — Cloud
- **Prompt:** `Run the industry-digest skill and post the 5 bullets.`
- **Needs in CONFIG.md:** industry-digest topics; web-search connector.

### competitor-watch — Weekly Mon ~08:00 — Cloud
- **Prompt:** `Run the competitor-watch skill and post any changes.`
- **Needs in CONFIG.md:** competitor URLs/feeds; web-search connector.

### weekly-impact-summary — Weekly Fri ~16:00 — Cloud
- **Prompt:** `Run the weekly-impact-summary skill and post the narrative.`
- **Needs in CONFIG.md:** wins doc name/id, voice & tone.

### brag-doc-builder — Quarterly — Cloud
- **Prompt:** `Run the brag-doc-builder skill and draft the brag doc.`
- **Needs in CONFIG.md:** wins doc + brag doc names/ids, role, voice & tone.

### follow-up-tracker — Daily (weekdays) — Cloud
- **Prompt:** `Run the follow-up-tracker skill and post threads awaiting my reply.`
- **Needs in CONFIG.md:** follow-up staleness N.

### one-on-one-prep — Daily ~07:00 (or before each 1:1) — Cloud
- **Prompt:** `Run the one-on-one-prep skill and post prep blocks for today's 1:1s.`
- **Needs in CONFIG.md:** direct reports.

### kudos-radar — Weekly Thu ~15:00 — Cloud
- **Prompt:** `Run the kudos-radar skill and draft recognition (do not send).`
- **Needs in CONFIG.md:** direct reports / collaborators, voice & tone.

### stale-work-finder — Weekly Mon ~09:00 — Cowork (gh) or Cloud (MCP)
- **Prompt:** `Run the stale-work-finder skill and post my stale work.`
- **Needs in CONFIG.md:** GitHub username, repos/org.

### pr-review-queue — Daily (weekdays) ~09:00 — Cowork (gh) or Cloud (MCP)
- **Prompt:** `Run the pr-review-queue skill and post my review queue.`
- **Needs in CONFIG.md:** GitHub username, repos/org.

### dependabot-triage — Daily ~09:00 — Cowork (gh) or Cloud (MCP)
- **Prompt:** `Run the dependabot-triage skill; merge safe updates, list the rest.`
- **Needs in CONFIG.md:** repos/org, any manual-only repo flags.

### ci-failure-watch — Daily ~07:00 — Cloud (GitHub MCP) or Cowork (gh)
- **Prompt:** `Run the ci-failure-watch skill and post overnight failures.`
- **Needs in CONFIG.md:** repos/org.

### travel-logistics-tracker — Daily ~07:00 — Cloud
- **Prompt:** `Run the travel-logistics-tracker skill and post any trip briefs.`
- **Needs in CONFIG.md:** nothing required (reads Gmail/Calendar).

### inbox-triage-drafts — Daily ~08:00 — Cloud
- **Prompt:** `Run the inbox-triage-drafts skill; categorize unread and draft routine replies (do not send).`
- **Needs in CONFIG.md:** voice & tone.

### receipts-and-expenses — Weekly Fri ~16:00 — Cloud
- **Prompt:** `Run the receipts-and-expenses skill and post receipts to file.`
- **Needs in CONFIG.md:** receipts Drive folder name/id.

---

## 🔁 Inbox pipeline (producer → consumers)

These form a producer→consumer pipeline: **`inbox-triage` (producer) must run and leave a fresh
`inbox-state.json` before any `brief-*` consumer**, and the light `brief-*` lenses all deliver into
**one shared "Daily Briefs" calendar event** whose reminder fires at the `CONFIG.md → Brief delivery`
reading time (default **07:00**). Because each routine run is an **isolated cloud session with its
own clone**, separate brief routines coordinate only through that event + the Drive ledgers.

**Recommended: run the whole morning brief as ONE chained routine.** A single session runs the
skills in order, so the ordering is guaranteed, there's no cross-session race on the event, and it
costs one daily run instead of five. Use the pipeline block below. (Prefer separate cadences/models
per brief? Use the individual blocks further down instead — just keep them staggered and earlier
than the 07:00 reading time.)

### 🌅 daily-briefs-pipeline (RECOMMENDED) — Daily ~06:30 — Cloud
- **Connectors:** Gmail, Google Calendar, Google Drive.
- **Prompt:**
  ```
  Run my morning inbox-brief pipeline using this repo's committed skills, in this exact order, as one chained run. Do not send email or move money — deliver only the calendar event sections, the [Triage] draft, and the ledger writes.

  1. PRODUCER — run the inbox-triage skill in APPLY mode: label and archive the unlabeled inbox tail per inbox-pipeline/config, write inbox-state.json to Drive, and post the [Triage] draft. This must finish before any brief.
  2. CONSUMERS — then, reading the fresh inbox-state.json, run these brief lenses in APPLY mode (apply so each appends to its ledger and won't re-brief the same items tomorrow). Each one upserts its own section into the single shared "Daily Briefs" calendar event per CONFIG.md → Brief delivery:
     a. brief-travel
     b. brief-ai-learning
  3. ONLY IF today is Monday, also run brief-finance and brief-career in APPLY mode (they are weekly), appending their sections to the same Daily Briefs event.

  Follow each skill's SKILL.md exactly. If inbox-state.json is missing or stale, let each brief use its documented fallback and note that in its section.
  ```
- **Needs in CONFIG.md:** Drive state folder; Brief delivery (calendar/time/reminder — defaults work).

---

**Or, separate routines** (one per skill — only if you want different cadences/models). Keep each
earlier than 07:00 and staggered so two lenses don't race to create the event.

### inbox-triage (PRODUCER) — Daily ~06:30 — Cloud
- **Connectors:** Gmail, Google Drive.
- **Prompt (apply / label+archive):** `Run the inbox-triage skill in apply mode: label and archive per taxonomy, write inbox-state.json, and post the [Triage] draft.`
- **Prompt (propose / read-only):** `Run the inbox-triage skill in propose mode and post the [Triage] draft.`
- **Needs in CONFIG.md:** Drive state folder name; config lives in `inbox-pipeline/config/*.yml`.

### brief-travel — Daily ~06:40 (after triage) — Cloud
- **Connectors:** Gmail, Google Calendar, Google Drive.
- **Prompt:** `Run the brief-travel skill in apply mode and add the Travel brief to today's Daily Briefs event.`
- **Needs in CONFIG.md:** Brief delivery (confirmation codes masked in the event).

### brief-ai-learning — Daily ~06:45 (after triage) — Cloud
- **Connectors:** Gmail, Google Calendar, Google Drive.
- **Prompt:** `Run the brief-ai-learning skill in apply mode and add the AI Learning brief to today's Daily Briefs event.`
- **Needs in CONFIG.md:** Brief delivery (calendar/time/reminder) — defaults work if left as-is.

### brief-finance — Weekly Mon ~06:50 (after triage) — Cloud
- **Connectors:** Gmail, Google Calendar, Google Drive.
- **Prompt:** `Run the brief-finance skill in apply mode and add the Finance brief to today's Daily Briefs event.`
- **Needs in CONFIG.md:** Brief delivery (read-only; never pays; account numbers masked in the event).

### brief-career — Weekly Mon ~06:55 (after triage) — Cloud
- **Connectors:** Gmail, Google Calendar, Google Drive.
- **Prompt:** `Run the brief-career skill in apply mode and add the Career brief to today's Daily Briefs event.`
- **Needs in CONFIG.md:** Brief delivery.

### capweb-reconcile (SEPARATE — not in the daily pipeline) — Weekly Fri ~16:00 — Cloud
- **Connectors:** Gmail, Google Drive.
- **Prompt:** `Run the capweb-reconcile skill in propose mode and draft the [Brief: Capweb] payment proposal (propose only — never pay; relies on triage having run earlier today, within 36h).`
- **Needs in CONFIG.md:** CapWeb confidence floor (optional); Drive state folder.

---

### Rebuilding on a new account
Reconnect connectors, fill `CONFIG.md`, then paste the blocks above for whichever skills you want.
Nothing here contains account-specific data, so this file transfers as-is.
