# DRIVE_LAYOUT.md — what lives in Drive (never in git)

All inbox-pipeline **state** lives in a single Google Drive folder, **`/AutomationState/`**. None of
it is ever committed — it is data/state, not code/config. The repo's `.gitignore` also blocks these
filenames as defense-in-depth. Create the folder once (see root `README.md` → next actions).

```
/AutomationState/
  inbox-state.json        # the handoff manifest — ONLY inbox-triage writes it
  ledger-triage.json      # owned by inbox-triage
  ledger-ai-learning.json # owned by brief-ai-learning
  ledger-finance.json     # owned by brief-finance
  ledger-career.json      # owned by brief-career
  ledger-travel.json      # owned by brief-travel
  ledger-capweb.json      # owned by capweb-reconcile
  scratch/                # transient extracted data (e.g. CapWeb financial records) — never repo
```

## `inbox-state.json` (written by `inbox-triage`)

The producer→consumer handoff manifest. Consumers read `last_triage` (staleness guard) and may use
`labeled` to scope their label queries.

```json
{
  "last_triage": "2026-06-24T08:00:00Z",
  "taxonomy_version": 1,
  "labeled": {
    "AI & Dev/Newsletters": ["<thread_id>", "<thread_id>"],
    "Finance/Banking & Cards": ["<thread_id>"],
    "Review/Unsorted": ["<thread_id>"]
  }
}
```

- `last_triage` — ISO 8601 timestamp of the last `apply` run. Missing/older than `max_staleness`
  (36h) trips the consumer staleness guard.
- `taxonomy_version` — mirrors `config/taxonomy.yml` `version`; lets a consumer notice config drift.
- `labeled` — map of label → thread IDs labeled in that run.

## `ledger-<slug>.json` (one per routine, owner-write-only)

Idempotency record. Keyed by Gmail thread/message ID so a routine never re-acts on the same item.

```json
{
  "slug": "triage",
  "entries": {
    "<thread_or_message_id>": { "run": "2026-06-24T08:00:00Z", "action": "labeled:Pets" }
  }
}
```

- `inbox-triage` records labeled/archived IDs here.
- A `brief-*` ledger records briefed IDs (so the same item isn't briefed twice).
- `capweb-reconcile` records reconciled/briefed message IDs here. **It never stores the extracted
  financial figures in git** — those live only in `/AutomationState/scratch/` or transient memory.

## Why none of this is in the repo

The kit's portability model keeps **code/config in git, data/state in Drive, secrets in env**. A new
machine/account re-points at the same `/AutomationState/` Drive folder (or starts a fresh one) and
every routine resumes idempotently — without any state having traveled through the repository.
