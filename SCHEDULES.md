# SCHEDULES.md — copy-paste scaffolding for your scheduled tasks

This is the "30-second job" part of the portability model. Every block below is a **ready-to-paste
scheduled task**. The task body is a *thin trigger* — it just runs a skill; all the logic lives in
that skill's `SKILL.md`. To set up (or rebuild on a new account):

1. Open the right surface:
   - **Cloud** → `claude.ai/code` → Scheduled tasks → New task. (Runs server-side; laptop can be
     asleep. Use for must-arrive jobs.)
   - **Cowork** → desktop app → Automations/Schedule. (Needs the app open. Use for jobs that read
     local files or shell out to `gh`.)
2. Paste the **Prompt** line as the task content.
3. Set the **Cadence** and **Surface** shown.
4. Make sure the skill's `CONFIG.md` values are filled in (see each block's "Needs in CONFIG.md").

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

### Rebuilding on a new account
Reconnect connectors, fill `CONFIG.md`, then paste the blocks above for whichever skills you want.
Nothing here contains account-specific data, so this file transfers as-is.
