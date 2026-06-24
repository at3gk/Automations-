# CapWeb extraction guide (LLM step)

This is the **only** judgment step in CapWeb. You read CapWeb emails/attachments and produce
structured `timesheet` and `invoice` records that conform to `schemas/timesheet.schema.json` and
`schemas/invoice.schema.json`. The deterministic Python (`reconcile.py`, `propose_payments.py`)
does everything after this — it does **not** re-interpret prose, so the records you emit are the
whole truth it works from.

## Hard rules

1. **Never guess. Leave a field `null` rather than invent it.** A wrong number here becomes a wrong
   reconciliation. Missing data is safe (it flags for a human); fabricated data is not.
2. **Do not compute amounts.** If an amount isn't stated, leave `amount: null`. Do not multiply
   hours × a rate you inferred — `reconcile.py` compares amounts exactly and will flag the gap.
3. **`period` must be a stable key that matches across the timesheet and the invoice** (e.g.
   `"2026-05"` or `"2026-W21"`). If the two documents express the period differently, normalize to
   one form and use it on both; if you can't be sure they refer to the same period, do **not**
   force them — leave them to flag as missing/orphan.
4. **`confidence` (0–1).** If your confidence in a record is below the SKILL.md threshold (default
   0.7), route the item to **"needs human review"** in the brief — do **not** feed it into
   reconciliation.
5. **Extracted financial data stays in Drive/scratch — never written into the repo.**

## Fields to pull

### timesheet (required: id, client, period, hours)
- `id` — stable id, e.g. `<gmail_message_id>:<index>`
- `client` — the client/contractor name reconciliation keys on
- `period` — normalized billing period string (see rule 3)
- `hours` — hours worked, as stated (fractions ok, e.g. `40.5`)
- `amount` — expected pay if explicitly stated, else `null`
- `source_message_id`, `confidence` — provenance + your confidence

### invoice (required: id, client, period, hours, amount)
- `id` — invoice number if present, else `<gmail_message_id>:<index>`
- `client`, `period`, `hours` — as above (must line up with the timesheet to match)
- `amount` — billed amount exactly as written (no rounding, keep cents)
- `due_date` — ISO date the invoice is due; required for it to reach the payment proposal
- `payee` — who to pay; `null` is fine (defaults to `client`)
- `source_message_id`, `confidence`

## Output shape

```json
{
  "timesheets": [ { "id": "...", "client": "...", "period": "2026-05", "hours": 40, "amount": "4000.00" } ],
  "invoices":   [ { "id": "INV-12", "client": "...", "period": "2026-05", "hours": 40, "amount": "4000.00", "due_date": "2026-06-15", "payee": "Acme LLC" } ]
}
```

Pipe this object into `reconcile.py` on stdin. Everything downstream is deterministic.
