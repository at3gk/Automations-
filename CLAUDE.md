# CLAUDE.md — repo guide for Claude Code

This repo is the **Personal Automations Kit**: a set of scheduled agentic routines that run as
**Claude Code project skills**. It is designed to run in **cloud sessions** (claude.ai/code
scheduled tasks) that clone this repo — so everything needed is committed here, with no plugin or
marketplace to install.

## How routines are run

Each automation is a skill at `.claude/skills/<name>/SKILL.md`, auto-discovered because `.claude/`
is part of the clone. A scheduled task's body is a **thin trigger** — one line that names the skill,
e.g. `Run the inbox-triage skill in propose mode and post the [Triage] draft.` All logic lives in
the skill; the schedule holds none. See `SCHEDULES.md` for ready-to-paste task blocks and `README.md`
for the full skill table.

## Layout

- `.claude/skills/<name>/SKILL.md` — the 29 routines (the runnable units).
- `inbox-pipeline/` — shared, non-skill machinery for the inbox subsystem (referenced by the
  `inbox-triage`, `brief-*`, and `capweb-reconcile` skills via repo-root-relative paths):
  - `config/*.yml` — single source of truth for the mail taxonomy + sender map.
  - `generate/` — `validate_config.py` (config linter) and `build_filters.py` (→ Gmail filter XML).
  - `brief-engine.md` — the parameterized engine the light `brief-*` lenses instantiate.
  - `capweb/` — deterministic Python (`reconcile.py`, `propose_payments.py`), JSON schemas, tests.
  - `docs/` — `CONVENTIONS.md` (the run contract), `DRIVE_LAYOUT.md`, `ADDING_A_BRIEF.md`.
- `CONFIG.md` — the only place for personal values (referenced by name, never embedded).

## The inbox-pipeline subsystem (producer → consumers)

`inbox-triage` (producer) labels/archives the unlabeled tail of Gmail from `inbox-pipeline/config/`
and writes the Drive manifest `inbox-state.json`. The `brief-*` lenses and `capweb-reconcile`
(consumers) read that manifest and query Gmail **by label**. The light `brief-*` lenses **deliver
into one shared "Daily Briefs" calendar event per day** (each owns a delimited section; reminder
configurable in `CONFIG.md → Brief delivery`); `capweb-reconcile` delivers a private Gmail draft.
Always run the producer first. Full contract: `inbox-pipeline/docs/CONVENTIONS.md`.

## Operating rules (apply to all routines)

- **Drafts, not actions.** Outward/irreversible work is drafted, never sent. The one sanctioned
  *outward* write is `inbox-triage` label/archive — and only in explicit **apply** mode, within
  `taxonomy.yml` policy, capped by an anomaly guard, never deleting. The `brief-*` lenses also
  upsert a **self-owned Daily Briefs calendar event** on your own calendar — a reversible, self-only
  notification (not an outward action), delivered in both modes just as the old draft was.
- **propose (default) / apply.** Default is read-only + a report draft; "apply" performs the
  routine's writes. State the mode at the top of every report.
- **Code/config in git; data/state in Drive; secrets in env.** Ledgers, `inbox-state.json`,
  generated XML, and any extracted/financial data are gitignored and live in Drive
  `/AutomationState/` — never commit them.
- **CapWeb never pays.** Reconciliation is deterministic with exact-dollar matching; it halts on
  mismatch and only *proposes* payments for human approval.

## Common commands

```bash
python inbox-pipeline/generate/validate_config.py     # lint config (run before build/triage)
python inbox-pipeline/generate/build_filters.py       # regenerate inbox-pipeline/dist/gmail-filters.xml
python inbox-pipeline/capweb/tests/test_reconcile.py  # CapWeb reconciliation unit tests
```
