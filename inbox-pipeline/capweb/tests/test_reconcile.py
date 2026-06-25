#!/usr/bin/env python3
"""Unit tests for reconcile.py and propose_payments.py.

Run:  python inbox-pipeline/capweb/tests/test_reconcile.py
No network, no external deps — plain asserts so it runs anywhere Python does.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reconcile import reconcile  # noqa: E402
from propose_payments import propose_payments  # noqa: E402


def _ts(id, client, period, hours, amount=None):
    return {"id": id, "client": client, "period": period, "hours": hours, "amount": amount}


def _inv(id, client, period, hours, amount, due_date=None, payee=None):
    return {"id": id, "client": client, "period": period, "hours": hours,
            "amount": amount, "due_date": due_date, "payee": payee}


def test_matched():
    r = reconcile(
        [_ts("t1", "Acme", "2026-05", 40, "4000.00")],
        [_inv("i1", "Acme", "2026-05", 40, "4000.00", due_date="2026-06-15")],
    )
    assert len(r["matched"]) == 1, r
    m = r["matched"][0]
    assert m["amount"] == "4000.00" and m["hours"] == "40"
    assert m["invoice_id"] == "i1" and m["timesheet_id"] == "t1"
    assert all(len(r[b]) == 0 for b in r if b != "matched"), r


def test_amount_mismatch():
    # hours agree, amount differs -> amount_mismatch (and money compared exactly)
    r = reconcile(
        [_ts("t1", "Acme", "2026-05", 40, "4000.00")],
        [_inv("i1", "Acme", "2026-05", 40, "4000.01")],
    )
    assert len(r["amount_mismatch"]) == 1 and not r["matched"], r
    am = r["amount_mismatch"][0]
    assert am["timesheet_amount"] == "4000.00" and am["invoice_amount"] == "4000.01"


def test_no_float_tolerance():
    # 0.1 + 0.2 != 0.3 territory: exact Decimal compare must NOT silently match.
    r = reconcile(
        [_ts("t1", "Acme", "2026-05", 40, "0.30")],
        [_inv("i1", "Acme", "2026-05", 40, "0.3")],
    )
    # 0.30 and 0.3 are numerically equal Decimals -> matched (exact, not fuzzy).
    assert len(r["matched"]) == 1, r
    r2 = reconcile(
        [_ts("t1", "Acme", "2026-05", 40, "0.30")],
        [_inv("i1", "Acme", "2026-05", 40, "0.31")],
    )
    assert len(r2["amount_mismatch"]) == 1 and not r2["matched"], r2


def test_hours_mismatch():
    r = reconcile(
        [_ts("t1", "Acme", "2026-05", 38, "3800.00")],
        [_inv("i1", "Acme", "2026-05", 40, "4000.00")],
    )
    assert len(r["hours_mismatch"]) == 1 and not r["matched"], r


def test_missing_invoice():
    r = reconcile([_ts("t1", "Acme", "2026-05", 40, "4000.00")], [])
    assert len(r["missing_invoice"]) == 1 and not r["orphan_invoice"], r
    assert r["missing_invoice"][0]["timesheet_id"] == "t1"


def test_orphan_invoice():
    r = reconcile([], [_inv("i1", "Acme", "2026-05", 40, "4000.00", payee="Acme LLC")])
    assert len(r["orphan_invoice"]) == 1 and not r["missing_invoice"], r
    assert r["orphan_invoice"][0]["payee"] == "Acme LLC"


def test_duplicate():
    # two invoices for the same key -> duplicate, and NOT matched.
    r = reconcile(
        [_ts("t1", "Acme", "2026-05", 40, "4000.00")],
        [_inv("i1", "Acme", "2026-05", 40, "4000.00"),
         _inv("i2", "Acme", "2026-05", 40, "4000.00")],
    )
    assert len(r["duplicate"]) == 1 and not r["matched"], r
    assert r["duplicate"][0]["invoice_ids"] == ["i1", "i2"]


def test_missing_timesheet_amount_flags_not_matches():
    # timesheet has no amount -> cannot confirm equal -> amount_mismatch, never matched.
    r = reconcile(
        [_ts("t1", "Acme", "2026-05", 40, None)],
        [_inv("i1", "Acme", "2026-05", 40, "4000.00")],
    )
    assert len(r["amount_mismatch"]) == 1 and not r["matched"], r


def test_propose_payments_only_due_matched():
    r = reconcile(
        [_ts("t1", "Acme", "2026-05", 40, "4000.00"),
         _ts("t2", "Beta", "2026-05", 10, "1000.00")],
        [_inv("i1", "Acme", "2026-05", 40, "4000.00", due_date="2026-06-15", payee="Acme LLC"),
         _inv("i2", "Beta", "2026-05", 10, "1000.00")],  # matched but no due_date
    )
    sched = propose_payments(r)
    assert len(sched) == 1, sched  # only the dated match is schedulable
    assert sched[0] == {"payee": "Acme LLC", "amount": "4000.00",
                        "due_date": "2026-06-15", "source_invoice_id": "i1"}


def test_propose_payments_as_of_filter_and_order():
    report = {"matched": [
        {"client": "B", "period": "p", "invoice_id": "i2", "amount": "200.00",
         "due_date": "2026-07-01", "payee": "B"},
        {"client": "A", "period": "p", "invoice_id": "i1", "amount": "100.00",
         "due_date": "2026-06-01", "payee": "A"},
    ]}
    sched = propose_payments(report, as_of="2026-06-30")
    assert [s["source_invoice_id"] for s in sched] == ["i1"], sched  # i2 filtered out, i1 kept


def run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run())
