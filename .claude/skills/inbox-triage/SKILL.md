---
name: inbox-triage
description: >-
  The inbox-pipeline PRODUCER. Labels and (where policy says) archives the unlabeled tail of your
  Gmail inbox from config/taxonomy.yml + config/sender-map.yml, discovers new recurring senders, and
  writes the inbox-state.json handoff manifest to Drive so the brief-* skills can run. Use when asked
  to "triage my inbox", "organize/label my mail", "run inbox-triage", or on a daily schedule. Default
  mode is propose (read-only + a [Triage] draft); say "apply" to actually label/archive. Requires
  Gmail and Google Drive connectors.
---

# Inbox Triage (producer)

> **Contract:** obeys `inbox-pipeline/docs/CONVENTIONS.md` (modes, ledger ownership, idempotency,
> anomaly + staleness guards, least privilege). This is the **only** routine that writes
> `inbox-state.json`. Single source of truth is `inbox-pipeline/config/*.yml` — never hardcode
> labels or senders here.

## Purpose
Sort the *unlabeled tail* of the inbox (the mail server-side filters didn't catch), discover new
recurring senders to fold back into config, and publish the `inbox-state.json` manifest the
consumer briefs depend on. Filters do the bulk; this does the tail.

## Instructions
These run unattended — never pause to ask a question.

1. **Mode.** Default **propose** (read-only; create only the `[Triage]` draft). Run **apply** only
   if explicitly told to ("apply", "label and archive"). State the mode at the top of the draft.
2. **Load config + state.** Read `inbox-pipeline/config/taxonomy.yml`, `sender-map.yml`,
   `ambiguous.yml`. Read `inbox-state.json` and `ledger-triage.json` from Drive `/AutomationState/`
   if present. **Read-newest rule:** if duplicates of either file exist (this connector can't update
   in place), use the **most-recently-modified** copy and ignore the rest.
3. **Ensure labels (apply only).** For each taxonomy `categories[].label` and the `review_label`,
   **check-before-create**: create missing nested labels; never duplicate; **never** create or
   modify anything in `preserved_labels`.
4. **Scope the query (capped, newest-first).** Order **newest-first**. First-ever run → `in:inbox`;
   otherwise → `in:inbox -has:userlabels` (optionally `+ newer_than:{since last_triage}` once the
   backlog is cleared). **Process at most `batch_cap` newest threads this run (CONFIG → Inbox triage;
   default 200) — do NOT paginate past the cap.** This drains a large backlog over several daily runs
   (≈ `batch_cap` − daily inflow per run) while keeping recent mail sorted promptly for the briefs.
   Ignore `resultCountEstimate`, but **count how many unlabeled threads remain past the cap** for the
   report so progress is visible.
5. **Classify each thread** by highest-confidence sender-map match: **exact address > domain >
   subject**. No confident match → stage to `Review/Unsorted`, keep in inbox. Any `ambiguous.yml`
   hit → `Review/Unsorted` too (**never** the guessed category).
6. **Idempotency.** Skip any thread already in `ledger-triage.json`.
7. **Apply policy.** Matched category → its label; **archive only if that category's `archive:
   true`** (currently only `Shopping & Deals`). Never archive anything else.
8. **Anomaly guard.** **Hard-halt and apply nothing** if this run would archive > `archive_cap`
   (CONFIG; default **50**) threads — archiving is the only semi-destructive action and always
   warrants a human checkpoint. Unknown senders are **report-only** during a capped run (they're
   staged to `Review/Unsorted`, never acted on destructively); halt only if unknown senders exceed
   `unknown_halt_fraction` (CONFIG; default **60%**) of the batch, which signals a broken sender map
   rather than a normal backlog. (The per-run `batch_cap` already bounds blast radius.)
9. **Discover senders.** Collect senders with **≥3 hits this run** that aren't in `sender-map.yml`
   as paste-ready suggested additions (domain + proposed category + sample subjects).
10. **Writes (apply only).** Apply the label/archive actions; append touched thread IDs (+ run
    timestamp) to `ledger-triage.json`; write `inbox-state.json` with `last_triage` (ISO now),
    `taxonomy_version` (from taxonomy.yml), and `labeled[label] = [thread_ids…]` for this run. Use
    the **canonical names** `inbox-state.json` / `ledger-triage.json` in `/AutomationState/` (never a
    dated or renamed variant). This connector has no in-place update, so a fresh copy is written each
    run — that's expected; readers take the newest. **Never tell the user to delete the old copy** and
    never put a "supersedes / please delete" note in the file or the `[Triage]` draft. Duplicates are
    harmless clutter, not an action item.
11. **Deliver** the `[Triage] {date}` draft (see Output format).

## Output format
```
🗂️ Inbox Triage — <date>   (mode: propose | apply)
Backlog: processed <N>/<batch_cap> newest · <M> unlabeled threads remain (~<R> more daily runs to clear)

Counts per label:
  • <label> — <N>
Archived (Shopping & Deals only): <N>
Review/Unsorted (need a human read): <N>
  • <sender>: <subject>  [thread]
Suggested sender-map.yml additions (≥3 hits, paste-ready):
  "<Category>":
    from: [<domain>]   # samples: "<subject>", "<subject>"
⚠️ Guard trips: <e.g. archive cap exceeded — halted, nothing applied>
```

## Guardrails
- **propose is read-only.** In propose mode the ONLY write is the `[Triage]` draft — no labels, no
  archive, no state. apply performs the writes in steps 7/10.
- **Never deletes mail. Never archives outside `archive: true` policy. Never touches
  `preserved_labels`.**
- **Single source of truth:** all labels/senders come from `inbox-pipeline/config/*.yml`. New
  senders are *suggested*, never silently added.
- **Anomaly guard halts** rather than mass-acting on a misconfiguration.
- Owns `ledger-triage.json` and `inbox-state.json` only; never writes another routine's state.
- Related read-only kit skill: `daily-triage-digest` answers "what needs me today" without changing
  mail; this skill *organizes* mail and produces the manifest. They complement, not replace.
