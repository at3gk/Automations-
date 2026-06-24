#!/usr/bin/env python3
"""validate_config.py — lint the inbox-pipeline config (the drift guard).

Keeps taxonomy.yml, sender-map.yml, and ambiguous.yml mutually consistent so the
`inbox-triage` skill and the generated Gmail filters can never disagree. Run this
before build_filters.py and before relying on a triage run.

Checks (errors → non-zero exit):
  1. Malformed structure (missing keys, wrong types, empty matcher lists).
  2. A `from` matcher used in more than one category (ambiguous routing).
  3. A `from` matcher that also appears in ambiguous.yml (can't auto-file AND never-auto-file).
  4. A sender-map label that is not a known label (taxonomy category, preserved label,
     or the review label).
Warnings (do not fail the build):
  5. A taxonomy category with no sender-map entry (reachable only by body classification).

Usage:  python inbox-pipeline/generate/validate_config.py
Exit code 0 = clean, 1 = errors found.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def _load(name: str):
    path = CONFIG_DIR / name
    if not path.exists():
        raise SystemExit(f"ERROR: missing config file: {path}")
    with path.open() as fh:
        return yaml.safe_load(fh) or {}


def _norm(matcher: str) -> str:
    return str(matcher).strip().lower()


def main() -> int:
    taxonomy = _load("taxonomy.yml")
    sender_map = _load("sender-map.yml")
    ambiguous = _load("ambiguous.yml")

    errors: list[str] = []
    warnings: list[str] = []

    # --- known labels: taxonomy categories + preserved + review bucket -------------
    tax_categories = taxonomy.get("categories") or []
    tax_labels = []
    for i, entry in enumerate(tax_categories):
        if not isinstance(entry, dict) or "label" not in entry:
            errors.append(f"taxonomy.categories[{i}] is malformed (need a `label` key): {entry!r}")
            continue
        if "archive" in entry and not isinstance(entry["archive"], bool):
            errors.append(f"taxonomy category {entry['label']!r}: `archive` must be true/false")
        tax_labels.append(entry["label"])

    preserved = taxonomy.get("preserved_labels") or []
    review_label = taxonomy.get("review_label")
    if not review_label:
        errors.append("taxonomy.yml is missing `review_label`.")
    known_labels = set(tax_labels) | set(preserved) | ({review_label} if review_label else set())

    # --- ambiguous matchers --------------------------------------------------------
    ambiguous_matchers = set()
    for i, entry in enumerate(ambiguous.get("never_autofile") or []):
        if not isinstance(entry, dict) or "match" not in entry:
            errors.append(f"ambiguous.never_autofile[{i}] is malformed (need a `match` key): {entry!r}")
            continue
        ambiguous_matchers.add(_norm(entry["match"]))

    # --- walk sender-map -----------------------------------------------------------
    seen_from: dict[str, str] = {}  # matcher -> first category that used it
    sm_categories = sender_map.get("categories") or {}
    if not isinstance(sm_categories, dict):
        errors.append("sender-map.yml `categories` must be a mapping of label -> matchers.")
        sm_categories = {}

    for label, spec in sm_categories.items():
        if label not in known_labels:
            errors.append(
                f"sender-map label {label!r} is not in taxonomy categories, preserved_labels, "
                f"or review_label."
            )
        if not isinstance(spec, dict):
            errors.append(f"sender-map category {label!r} must be a mapping with `from`/`subject`.")
            continue
        froms = spec.get("from") or []
        subjects = spec.get("subject") or []
        if not froms and not subjects:
            errors.append(f"sender-map category {label!r} has neither `from` nor `subject` matchers.")
        if froms and not isinstance(froms, list):
            errors.append(f"sender-map category {label!r}: `from` must be a list.")
            froms = []
        if subjects and not isinstance(subjects, list):
            errors.append(f"sender-map category {label!r}: `subject` must be a list.")

        for raw in froms:
            m = _norm(raw)
            if m in seen_from:
                errors.append(
                    f"duplicate `from` matcher {m!r} in {label!r} (already used in {seen_from[m]!r})."
                )
            else:
                seen_from[m] = label
            if m in ambiguous_matchers:
                errors.append(
                    f"`from` matcher {m!r} in {label!r} also appears in ambiguous.yml "
                    f"(conflict: can't auto-file AND never-auto-file)."
                )

    # --- warning: taxonomy category with no sender-map entry -----------------------
    for label in tax_labels:
        if label not in sm_categories:
            warnings.append(f"taxonomy category {label!r} has no sender-map entry "
                            f"(reachable only by body classification).")

    # --- report --------------------------------------------------------------------
    for w in warnings:
        print(f"  warn: {w}")
    if errors:
        print()
        for e in errors:
            print(f"  ERROR: {e}")
        print(f"\nvalidate_config: FAIL — {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(
        f"validate_config: OK — {len(tax_labels)} categories, "
        f"{len(seen_from)} unique senders, {len(ambiguous_matchers)} ambiguous, "
        f"{len(warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
