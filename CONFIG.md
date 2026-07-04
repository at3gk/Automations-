# CONFIG.md — your personalization (the ONLY file with your details)

Every skill reads its personal values from here **by name**. Skills never embed your name,
doc IDs, repos, or URLs directly — that is what keeps this kit portable. When you move to a new
account, you fill in this one file and everything else just works.

> **Rules**
> - Replace every `<< ... >>` placeholder with your real value.
> - Do **not** put secrets, tokens, or passwords here. Credentials live in the connectors you
>   reconnect per account (Gmail, Calendar, Drive, GitHub, etc.), never in this repo.
> - Leave a value as its placeholder if a skill that uses it isn't enabled — that skill just
>   won't run until you fill it in.

---

## Identity

- **Name:** << your name >>
- **Role / title:** << your role, e.g. Senior Director, Developer Relations >>
- **Company / org:** << your company >>
- **Timezone:** << e.g. America/New_York >>
- **Working hours:** << e.g. 09:00–18:00 >>  <!-- used by timing guardrails -->

## Voice & tone

Used by every skill that DRAFTS text in your name (`kudos-radar`, `inbox-triage-drafts`,
`daily-wins-recap`, `weekly-impact-summary`, `brag-doc-builder`). Describe how you sound so
drafts read like you — the words stay yours, the kit just gets the first draft close.

- **Voice descriptor:** << e.g. warm, direct, low on jargon, occasional dry humor >>
- **Sign-off you use:** << e.g. "Thanks, <name>" >>
- **Things to avoid:** << e.g. corporate filler, exclamation overload, em-dashes >>

## Topics & interests

- **Industry-digest topics:** << comma-separated, e.g. AI agents, developer tooling, OSS funding >>
- **Beats I must never be surprised by:** << e.g. anything touching my team's product area >>

## GitHub

- **GitHub username:** at3gk  <!-- prefilled (non-sensitive); change on a new account -->
- **Primary org:** << your-org >>
- **Repos to watch (ship-decoder / stale-work / CI):** << owner/repo, owner/repo2 >>
- **Ship-decoder sources:** << repos AND/OR changelog URL AND/OR Slack channels >>

## People

- **Direct reports (for one-on-one-prep):** << name (github/email), name2 (github/email) >>
- **Key collaborators:** << optional: people whose activity matters for prep >>

## Watch lists

- **Competitor URLs / feeds (competitor-watch):** << https://..., https://... >>
- **Launch sources (launch-radar):** << release pages, roadmaps, newsletters >>

## Documents (names + IDs — IDs optional, names required)

- **Running "wins" doc (daily-wins-recap, weekly-impact-summary):** name = << "My Wins Log" >>, id = << google-doc-id or leave blank to search by name >>
- **Brag doc (brag-doc-builder):** name = << "Brag Doc 2026" >>, id = << optional >>
- **Receipts / expenses Drive folder (receipts-and-expenses):** name = << "Receipts 2026" >>, id = << optional >>

## Thresholds

- **Follow-up staleness N (follow-up-tracker):** << 3 >> days
- **Daily-triage urgency window:** << today + tomorrow >>

## Inbox pipeline (the `inbox-triage` + `brief-*` + `capweb-reconcile` skills)

Unlike the rest of the kit, this subsystem's "personalization" is **structured config**, not prose,
so it lives in its own files (the single source of truth). This section is just the index/pointers:

- **Taxonomy + sender map:** `inbox-pipeline/config/taxonomy.yml`, `sender-map.yml`, `ambiguous.yml`.
  Edit those to change labels, archive policy, or sender routing — then run
  `python inbox-pipeline/generate/validate_config.py` and `…/build_filters.py`.
- **Drive state folder:** << "/AutomationState/" >>  <!-- holds inbox-state.json + ledger-*.json; create once -->
- **Triage staleness window (consumers fall back if older):** << 36 >> hours
- **CapWeb extraction confidence floor (below → human review):** << 0.7 >>

No secrets here — Gmail/Drive access comes from the connectors you reconnect per account.

### Inbox triage (backfill pacing + safety guards)

`inbox-triage` processes the inbox **newest-first, capped per run**, so a large backlog drains over
several daily runs instead of one runaway session. (Only the *first* run looks at the whole inbox;
every run after sees just the unlabeled tail + new mail.)

- **Per-run batch cap:** << 200 >> newest threads  (raise to drain a backlog faster; lower for shorter sessions)
- **Archive hard-halt cap:** << 50 >> threads  (archiving is the only semi-destructive action — the run halts and applies nothing if exceeded)
- **Unknown-sender halt fraction:** << 60 >> % of the batch
- **Unknown-sender halt floor:** << 40 >> unknown threads  (the fraction only trips the halt once at least this many threads are unknown, so a tiny high-variety batch — e.g. 7/8 — never trips it; a large batch above the fraction always does)

  When a run's unknown (Review/Unsorted) threads exceed **both** the floor **and** the fraction, the
  sender map is out of date: the run **halts, applies nothing, and downgrades to propose** (labels
  the gap in a `[Triage]` draft). This halt is **non-negotiable** — "it's just an aged backlog" is
  not a reason to proceed; that's exactly the condition the halt exists to catch. Fix the map
  (add the suggested senders) and the next run clears on its own.

### Brief delivery (how the `brief-*` lenses reach you)

The light `brief-*` lenses consolidate into **one calendar event per day** (a `📋 Daily Briefs`
event with a reminder) instead of a pile of separate Gmail drafts — first lens to run creates it,
the rest append their own section. Set how you want it delivered:

- **Channel:** << calendar >>  (`calendar` = consolidated event · `draft` = legacy Gmail draft · `both`)
- **Calendar for briefs:** << primary >>  (calendar ID, or `primary`)
- **Daily event title:** << "📋 Daily Briefs" >>  (the date is appended automatically)
- **Reading time (local):** << 07:00 >>  (when the event starts / your nudge to sit and read)
- **Reminder lead:** << 0 >> minutes before  (popup ping; `0` = exactly at the reading time)
- **Event color:** << 5 >>  (Google color ID 1–11; `5` = Banana, stands out)

> **Timing dependency:** the event/reminder fires at the reading time, so every `brief-*` lens (and
> `inbox-triage` before them) must be **scheduled to run earlier than this** — otherwise the reminder
> fires before the brief exists. Default schedule: triage ~06:30, lenses staggered 06:40–06:55,
> event 07:00 (see `SCHEDULES.md`).

Timezone is taken from **Identity → Timezone** above. Note: `capweb-reconcile` is **not** part of
this consolidation — its payment proposals stay in a private Gmail draft, never a calendar event.

## Connector choices (swap per account)

The kit assumes **Google Workspace** (Gmail, Calendar, Drive) and **GitHub**. Where a skill
could use a different tool, set your choice here and the skill adapts. Leave as-is to use the
default.

- **Messaging connector:** << Slack | Linear | none >>  (used by daily-triage-digest, commitments-tracker)
- **Web-search / monitoring connector:** << web search | Firecrawl | none >>  (industry-digest, competitor-watch, launch-radar, ship-decoder fallback)
- **Issue tracker:** << GitHub | Linear | Jira | none >>
