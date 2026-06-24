---
name: receipts-and-expenses
description: >-
  Flags emails containing receipts/invoices that need filing, extracts the key details, and
  optionally files copies into your receipts Drive folder. Use when asked "find my receipts",
  "expenses to file", "receipts and expenses", or run on a weekly schedule. Requires Gmail and
  Google Drive connectors. Receipts folder named in CONFIG.md.
---

# Receipts & Expenses

## Purpose
Stop receipts from getting buried. Surface emails with receipts/invoices, pull out the details you
need for an expense report, and (optionally) tuck copies into your receipts folder so filing is a
formality.

## Instructions
These run unattended — never pause to ask a question.

1. **Timing guardrail.** Scope is since the last run (default ~7 days). Not time-of-day sensitive.
2. Scan Gmail for receipt/invoice signals: "receipt", "invoice", "your order", "payment
   confirmation", "tax invoice", attachments that look like receipts (PDF), known vendors
   (airlines, hotels, SaaS, rideshare).
3. For each, extract: vendor, date, amount + currency, category guess (travel / software / meals /
   other), and whether it has an attachment.
4. **Filing (optional auto-action):** if a receipts Drive folder is named in `CONFIG.md`, save a
   copy of the receipt (attachment or a PDF of the email) into that folder, named
   `<date>_<vendor>_<amount>`. If no folder is configured, skip filing and just list.
5. Total the amounts and flag anything that looks reimbursable or unusually large.

## Output format
```
🧾 Receipts & Expenses — <date>

Filed to <folder> (N):
  • <date> · <vendor> · <amount> · <category>  [email]
Found but not filed (no folder set / no attachment):
  • …
Total surfaced: <currency amount>   |   ⚠️ Review: <large/odd items>
```
If none found, say "No new receipts since last run."

## Guardrails
- **Auto-action limited to filing copies** into the one receipts folder named in `CONFIG.md`
  (copying a receipt is low-stakes and reversible). It **never** deletes mail, never submits an
  expense report, never pays or replies.
- Treat amounts and any payment details as sensitive — keep them in your brief/folder only.
- Idempotent: don't re-file a receipt already in the folder (match by vendor+date+amount).
- Receipts folder name/id comes from `CONFIG.md`.
