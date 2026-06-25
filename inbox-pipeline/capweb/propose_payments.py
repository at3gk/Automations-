#!/usr/bin/env python3
"""propose_payments.py — build a payment schedule to APPROVE. Never pays.

Pure, deterministic, NO network, NO payment API. Takes a reconciliation_report (from
reconcile.py) and emits an ordered list of proposed payments built ONLY from `matched`
invoices that are due (i.e. carry a due_date). Output is a proposal for human approval
inside the CapWeb brief draft — it never schedules, calls a bank, or moves money.

  schedule item: {payee, amount, due_date, source_invoice_id}

CLI:  python propose_payments.py < report.json > schedule.json
"""
from __future__ import annotations

import json
import sys


def propose_payments(report: dict, as_of: str | None = None) -> list[dict]:
    """From matched, due invoices, build a sorted payment schedule (pure).

    A matched item is "due" when it has a non-empty due_date. If `as_of` (ISO date) is
    given, only include items due on or before it; otherwise include all dated matches.
    Ordered by (due_date, payee) for deterministic output.
    """
    schedule: list[dict] = []
    for m in report.get("matched", []):
        due = m.get("due_date")
        if not due:
            continue  # matched but no due date -> nothing to schedule yet
        if as_of is not None and str(due) > str(as_of):
            continue
        schedule.append({
            "payee": m.get("payee") or m.get("client"),
            "amount": m.get("amount"),
            "due_date": due,
            "source_invoice_id": m.get("invoice_id"),
        })

    schedule.sort(key=lambda x: (str(x.get("due_date") or ""), str(x.get("payee") or "")))
    return schedule


def main(argv: list[str]) -> int:
    as_of = argv[1] if len(argv) > 1 else None
    report = json.load(sys.stdin)
    schedule = propose_payments(report, as_of=as_of)
    json.dump({"proposed_payments": schedule}, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
