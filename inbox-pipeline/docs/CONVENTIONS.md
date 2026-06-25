# CONVENTIONS.md — the inbox-pipeline run contract

Every inbox-pipeline routine (the `inbox-triage` producer, the `brief-*` lenses, and
`capweb-reconcile`) obeys this contract. Each routine's `SKILL.md` references this file rather than
restating it. This contract sits *on top of* the kit's global rules in the repo `README.md`
("drafts not actions", "no state/secrets in git", "logic in skills").

## The mental model: producer → consumers

- **Producer — `inbox-triage`.** Classifies/organizes the inbox by label and writes the handoff
  manifest `inbox-state.json` to Drive. Everything else depends on it having run.
- **Consumers — `brief-*` and `capweb-reconcile`.** Each reads the manifest, queries Gmail **by
  label** (never the raw inbox), extracts what matters, and **delivers** it. The light `brief-*`
  lenses deliver into one shared **Daily Briefs calendar event** (see **Delivery** below); CapWeb is
  the heavy exception (deterministic reconciliation, delivered as a private Gmail draft; see
  `.claude/skills/capweb-reconcile`).

Three shared conventions make these chain into a pipeline, not a pile of scripts: **consistent
labels** (from `config/taxonomy.yml`), the **Drive state manifest** (`inbox-state.json`), and a
single **review surface** per run (the consolidated brief event, or a draft) stated below.

## Modes — propose (default) / apply

There are no shell flags here; a routine's mode comes from how it's invoked (the thin-trigger
prompt).

- **`propose` (default).** Read-only except for writing its own **delivery artifact** — its section
  of the consolidated Daily Briefs event (or a report draft). Performs **no** Gmail label/archive or
  Drive state mutations. This is the kit's "draft, don't act" default.
- **`apply`.** Performs its writes — for `inbox-triage` that means label/archive + writing
  `inbox-state.json` and appending to its ledger; for a brief it means appending briefed IDs to its
  own ledger. **`apply` for a brief still only ever writes its delivery artifact + its ledger —
  never acts on the world** (no payments, no sends, no deletes).

**State the mode in the delivery artifact** (the event header and each section heading, or the draft top).

## Delivery — the consolidated Daily Briefs event

The light `brief-*` lenses don't each drop a separate draft. They **upsert one calendar event per
day** so you get a single thing to read, with a reminder, instead of N drafts:

- **One event, many sections.** The first lens to run on `{date}` creates a `📋 Daily Briefs —
  {date}` event (on the calendar/time/color/reminder from `CONFIG.md → Brief delivery`, carrying the
  marker `[auto:daily-briefs]`). Every later lens **finds that same event** and writes only its own
  block, delimited by `<!-- <slug>:start -->` … `<!-- <slug>:end -->`, leaving the others untouched.
- **Idempotent.** A re-run **replaces** the lens's own delimited block rather than appending, so
  re-briefing never duplicates a section. (Item-level de-dup against the ledger still applies first.)
- **Reversible & self-only.** The event lives on your own calendar; it's a notification, not an
  outward action — so it's written in both modes, just like the old draft was.
- **Channel override.** `CONFIG.md` `channel` can be `calendar` (default), `draft` (legacy
  Gmail-draft behavior), or `both`. CapWeb ignores this and always uses its private draft.
- **Race/overflow guards** are in `brief-engine.md` step 8 (write the earliest event if two raced;
  trim + note overflow past the ~8 KB description limit).

## Section / draft prefixes

Each brief's prefix titles its **section** in the Daily Briefs event (and, under `draft`/`both`, the
draft title) with a stable prefix + ISO date: `[Triage] YYYY-MM-DD`, `[Brief: AI Learning]
YYYY-MM-DD`, `[Brief: Finance] YYYY-MM-DD`, `[Brief: Career] YYYY-MM-DD`, `[Brief: Travel]
YYYY-MM-DD`, `[Brief: Capweb] YYYY-MM-DD`.

## Ledger ownership

Each routine owns exactly **one** Drive ledger `ledger-<slug>.json` and writes only that. Any
routine may **read** `inbox-state.json`, but **only `inbox-triage` writes it.** Never write another
routine's ledger or state. See `DRIVE_LAYOUT.md` for shapes.

## Idempotency

Before acting on a thread/item, check the owning ledger by Gmail thread/message ID; **skip if
present**. After acting (in `apply`), append the ID + run timestamp. Re-running must never duplicate
labels, re-archive, or re-brief.

## Anomaly guard

If a run would exceed a configured cap, **stop and report instead of acting**. `inbox-triage`
defaults: archive > **50** threads, or > **25** unknown senders in one run → halt and surface the
counts for a human, rather than mass-acting on a misconfiguration.

## Staleness guard (consumers)

Read `inbox-state.json.last_triage`. If it is missing or older than `max_staleness` (default
**36h**), the brief still runs but falls back to `newer_than:<window>` and **prominently notes**:
"triage stale/missing — results may include unlabeled mail."

## Least privilege

A routine does its job and nothing more: it never modifies labels outside its scope, never writes
another routine's ledger, never archives outside its category's policy, and **never deletes mail**.

## Gmail query hygiene

- **`resultCountEstimate` is unreliable — always paginate to exhaustion. Never trust the count.**
- **Check-before-create for labels** — never create a label that already exists; never touch
  `preserved_labels` from `taxonomy.yml`.
