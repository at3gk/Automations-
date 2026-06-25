---
name: capweb-reconcile
description: >-
  The inbox-pipeline HEAVY consumer for CapWeb business mail. Extracts timesheets/invoices from the
  Arjun Capweb labels, runs DETERMINISTIC Python reconciliation (exact money compare, halt on any
  mismatch), and drafts a [Brief: Capweb] proposing payments to schedule — for your approval only.
  Use when asked to "reconcile CapWeb", "capweb invoices/timesheets", "capweb payments", or on a
  schedule. NEVER pays, schedules, or moves money. Requires Gmail + Drive (reads inbox-state.json).
---

# Brief: Capweb (heavy consumer)

> **Contract:** obeys `inbox-pipeline/docs/CONVENTIONS.md`. Unlike the light briefs, this does NOT
> use the generic `brief-engine.md` for matching — the money logic is deterministic Python in
> `inbox-pipeline/capweb/`. Queries Gmail **by label**. Owns `ledger-capweb.json`. Default mode
> propose. Target labels: `(label:"Arjun Capweb" OR label:"Arjun Capweb/Accounting CapWeb")`.

## Purpose
Turn scattered CapWeb timesheet/invoice mail into a deterministic reconciliation and a payment
**proposal you approve** — with exact-dollar matching and a hard stop on anything that doesn't line
up. The LLM only extracts structure and writes the brief; it never "approximately" matches money.

## Instructions
These run unattended — never pause to ask a question.

1. **Mode + state.** Default **propose**. Read `inbox-state.json` from Drive `/AutomationState/`
   (staleness guard: if `last_triage` missing or > 36h old, note it and fall back to
   `newer_than:7d`). Query the CapWeb labels `after:{last_triage}` (fallback `newer_than:7d`).
   **Paginate to exhaustion; ignore `resultCountEstimate`.** De-dup against `ledger-capweb.json`.
2. **Extract (LLM step).** Following `inbox-pipeline/capweb/extract_schema.md`, produce `timesheet`
   and `invoice` records conforming to `inbox-pipeline/capweb/schemas/*.json`. **Leave a field
   `null` rather than guess.** If a record's `confidence` < **0.7**, route it to "needs human
   review" — do **not** feed it into reconciliation. Persist extracted data only to Drive
   `/AutomationState/scratch/` or transient memory — **never into the repo.**
3. **Reconcile (deterministic).** Pipe `{"timesheets": [...], "invoices": [...]}` into
   `python inbox-pipeline/capweb/reconcile.py`. It matches on `{client, period}`, compares hours and
   amount **exactly** (no tolerance), and returns a `reconciliation_report` with buckets: `matched`,
   `amount_mismatch`, `hours_mismatch`, `missing_invoice`, `orphan_invoice`, `duplicate`. **Every
   non-matched item is a halt-and-flag for a human — never auto-resolve.**
4. **Propose payments (deterministic).** Pipe the report into
   `python inbox-pipeline/capweb/propose_payments.py`. From **matched, due** invoices it builds a
   schedule `[{payee, amount, due_date, source_invoice_id}]`. **Output only — it calls no payment
   API and moves no money.**
5. **Deliver** the `[Brief: Capweb] {date}` draft (see Output format).
6. **Apply mode only.** The ONLY apply-mode writes are: create the draft + append reconciled/briefed
   message IDs to `ledger-capweb.json`. **It never schedules or pays.**

## Output format
```
💼 Brief: Capweb — <date>   (mode: propose | apply)
<staleness note, only if triage stale/missing>

(a) Payments to schedule — for your approval (N):
  • <payee> · <amount> · due <date> · invoice <id>
(b) Reconciliation flags needing a human decision:
  • amount_mismatch: <client>/<period> — timesheet <x> vs invoice <y>
  • hours_mismatch / missing_invoice / orphan_invoice / duplicate: …
(c) Extracted but unmatched / low-confidence (needs human review):
  • <item> — <why>
```

## Guardrails
- **No payment execution, ever.** Steps 3–4 are deterministic Python with no network; this skill
  proposes and flags only.
- **Halt on mismatch.** Any non-`matched` bucket is surfaced for a human; nothing is auto-resolved.
- **Never commit financial/extracted data.** It lives in Drive scratch/transient memory only;
  `.gitignore` also blocks `*.financial.json` and `extracted/`.
- **Money compares exactly** — handled in `reconcile.py` via Decimal; the LLM must not infer or
  compute amounts.
- Low-confidence extraction → human-review bucket, not reconciliation.
- Owns `ledger-capweb.json` only; never writes `inbox-state.json` or another routine's ledger.
