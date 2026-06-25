#!/usr/bin/env python3
"""reconcile.py — deterministic timesheet <-> invoice reconciliation.

Pure functions, JSON in / JSON out, NO network, NO secrets, NEVER executes payments.
Money and hours compare EXACTLY (via Decimal) — no fuzzy matching, no tolerance.

Matching key is {client, period}. Each input record lands in exactly one report bucket:
  matched          hours and amount agree
  hours_mismatch   hours disagree
  amount_mismatch  hours agree but amount disagrees
  missing_invoice  timesheet with no invoice for its key
  orphan_invoice   invoice with no timesheet for its key
  duplicate        >1 timesheet or >1 invoice for the same key (not matched; flagged)

Any non-matched bucket is a halt-and-flag item for a human. Nothing is auto-resolved.

CLI:  python reconcile.py < input.json > report.json
      input.json = {"timesheets": [...], "invoices": [...]}
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from typing import Any


def _dec(value: Any) -> Decimal | None:
    """Exact Decimal from a number/string; None if absent/uninterpretable."""
    if value is None:
        return None
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None


def _key(record: dict) -> tuple[str, str]:
    return (str(record.get("client", "")).strip(), str(record.get("period", "")).strip())


def _money_str(d: Decimal | None) -> str | None:
    return None if d is None else format(d, "f")


def reconcile(timesheets: list[dict], invoices: list[dict]) -> dict:
    """Reconcile two lists of records into a reconciliation_report dict (pure)."""
    ts_by_key: dict[tuple[str, str], list[dict]] = defaultdict(list)
    inv_by_key: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for t in timesheets:
        ts_by_key[_key(t)].append(t)
    for i in invoices:
        inv_by_key[_key(i)].append(i)

    report: dict[str, list] = {
        "matched": [],
        "amount_mismatch": [],
        "hours_mismatch": [],
        "missing_invoice": [],
        "orphan_invoice": [],
        "duplicate": [],
    }

    all_keys = sorted(set(ts_by_key) | set(inv_by_key))
    for key in all_keys:
        client, period = key
        ts_list = ts_by_key.get(key, [])
        inv_list = inv_by_key.get(key, [])

        # Duplicate guard: ambiguous matching -> halt-and-flag, do not match this key.
        if len(ts_list) > 1 or len(inv_list) > 1:
            report["duplicate"].append({
                "client": client,
                "period": period,
                "timesheet_ids": sorted(str(t.get("id", "")) for t in ts_list),
                "invoice_ids": sorted(str(i.get("id", "")) for i in inv_list),
                "reason": "more than one timesheet or invoice for this {client, period}",
            })
            continue

        if ts_list and not inv_list:
            t = ts_list[0]
            report["missing_invoice"].append({
                "client": client, "period": period,
                "timesheet_id": str(t.get("id", "")),
                "hours": _money_str(_dec(t.get("hours"))),
                "amount": _money_str(_dec(t.get("amount"))),
            })
            continue

        if inv_list and not ts_list:
            i = inv_list[0]
            report["orphan_invoice"].append({
                "client": client, "period": period,
                "invoice_id": str(i.get("id", "")),
                "hours": _money_str(_dec(i.get("hours"))),
                "amount": _money_str(_dec(i.get("amount"))),
                "due_date": i.get("due_date"),
                "payee": i.get("payee") or client,
            })
            continue

        # Exactly one of each -> compare.
        t, i = ts_list[0], inv_list[0]
        t_hours, i_hours = _dec(t.get("hours")), _dec(i.get("hours"))
        t_amount, i_amount = _dec(t.get("amount")), _dec(i.get("amount"))

        base = {
            "client": client, "period": period,
            "timesheet_id": str(t.get("id", "")),
            "invoice_id": str(i.get("id", "")),
        }

        if t_hours is None or i_hours is None or t_hours != i_hours:
            report["hours_mismatch"].append({
                **base,
                "timesheet_hours": _money_str(t_hours),
                "invoice_hours": _money_str(i_hours),
                "invoice_amount": _money_str(i_amount),
            })
            continue

        # Hours agree. Amount must match EXACTLY. A missing timesheet amount cannot be
        # confirmed equal -> flag as a mismatch for a human rather than assume.
        if t_amount is None or i_amount is None or t_amount != i_amount:
            report["amount_mismatch"].append({
                **base,
                "hours": _money_str(t_hours),
                "timesheet_amount": _money_str(t_amount),
                "invoice_amount": _money_str(i_amount),
            })
            continue

        report["matched"].append({
            **base,
            "hours": _money_str(t_hours),
            "amount": _money_str(i_amount),
            "payee": i.get("payee") or client,
            "due_date": i.get("due_date"),
        })

    return report


def main(argv: list[str]) -> int:
    data = json.load(sys.stdin)
    report = reconcile(data.get("timesheets", []), data.get("invoices", []))
    json.dump(report, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
