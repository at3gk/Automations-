# CONVENTIONS.md — the inbox-pipeline run contract

Every inbox-pipeline routine (the `inbox-triage` producer, the `brief-*` lenses, and
`capweb-reconcile`) obeys this contract. Each routine's `SKILL.md` references this file rather than
restating it. This contract sits *on top of* the kit's global rules in the repo `README.md`
("drafts not actions", "no state/secrets in git", "logic in skills").

## The mental model: producer → consumers

- **Producer — `inbox-triage`.** Classifies/organizes the inbox by label and writes the handoff
  manifest `inbox-state.json` to Drive. Everything else depends on it having run.
- **Consumers — `brief-*` and `capweb-reconcile`.** Each reads the manifest, queries Gmail **by
  label** (never the raw inbox), extracts what matters, and delivers a Gmail **draft**. Most briefs
  are thin lenses over the shared `brief-engine.md`. CapWeb is the heavy exception (deterministic
  reconciliation; see `.claude/skills/capweb-reconcile`).

Three shared conventions make these chain into a pipeline, not a pile of scripts: **consistent
labels** (from `config/taxonomy.yml`), the **Drive state manifest** (`inbox-state.json`), and
**Gmail drafts** as the human-review surface.

## Modes — propose (default) / apply

There are no shell flags here; a routine's mode comes from how it's invoked (the thin-trigger
prompt).

- **`propose` (default).** Read-only except for writing its own report **draft**. Performs **no**
  Gmail/Drive mutations (no labeling, archiving, or state writes). This is the kit's "draft, don't
  act" default.
- **`apply`.** Performs its writes — for `inbox-triage` that means label/archive + writing
  `inbox-state.json` and appending to its ledger; for a brief it means appending briefed IDs to its
  own ledger. **`apply` for a brief still only ever writes a draft + its ledger — never acts on the
  world** (no payments, no sends, no deletes).

**State the mode at the top of every report draft.**

## Draft prefixes

Reports/briefs are delivered as Gmail drafts titled with a stable prefix + ISO date:
`[Triage] YYYY-MM-DD`, `[Brief: AI Learning] YYYY-MM-DD`, `[Brief: Finance] YYYY-MM-DD`,
`[Brief: Career] YYYY-MM-DD`, `[Brief: Travel] YYYY-MM-DD`, `[Brief: Capweb] YYYY-MM-DD`.

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
