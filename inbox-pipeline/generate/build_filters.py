#!/usr/bin/env python3
"""build_filters.py — config -> dist/gmail-filters.xml (Gmail Atom export format).

Generates the deterministic, high-volume server-side filters from the SAME config the
`inbox-triage` skill reads, so "filters do the bulk; triage does the tail." Import the
output via Gmail → Settings → Filters and Blocked Addresses → Import filters.

Behavior:
  * One filter entry per category's `from` list, joined `a OR b OR ...`.
  * A separate entry per category that has `subject:` matchers (so subject filters match
    regardless of sender — combining from+subject in one filter would AND them).
  * `shouldArchive=true` for categories with `archive: true`.
  * Label values XML-escaped (e.g. `AI &amp; Dev/Newsletters`).
  * Deterministic ordering (taxonomy order, then sender-map-only labels) → idempotent output.

Usage:  python inbox-pipeline/generate/build_filters.py
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
DIST = ROOT / "dist"
OUT = DIST / "gmail-filters.xml"


def _load(name: str):
    with (CONFIG_DIR / name).open() as fh:
        return yaml.safe_load(fh) or {}


def _attr(value: str) -> str:
    """Escape a value for a single-quoted XML attribute."""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("'", "&#39;")
    )


def _entry(properties: list[tuple[str, str]]) -> str:
    lines = [
        "  <entry>",
        "    <category term='filter'></category>",
        "    <title>Mail Filter</title>",
        "    <content></content>",
    ]
    for name, value in properties:
        lines.append(f"    <apps:property name='{name}' value='{_attr(value)}'/>")
    lines.append("  </entry>")
    return "\n".join(lines)


def main() -> int:
    taxonomy = _load("taxonomy.yml")
    sender_map = _load("sender-map.yml")

    # label -> archive policy (default False for labels absent from taxonomy, e.g. Arjun Capweb)
    archive_by_label = {
        e["label"]: bool(e.get("archive", False))
        for e in (taxonomy.get("categories") or [])
        if isinstance(e, dict) and "label" in e
    }

    sm = sender_map.get("categories") or {}

    # Deterministic order: taxonomy category order first, then any sender-map-only labels.
    ordered = [e["label"] for e in (taxonomy.get("categories") or []) if e.get("label") in sm]
    ordered += [label for label in sm if label not in ordered]

    entries: list[str] = []
    n_from = n_subject = n_archive = 0
    for label in ordered:
        spec = sm[label] or {}
        archive = archive_by_label.get(label, False)
        froms = spec.get("from") or []
        subjects = spec.get("subject") or []

        if froms:
            props = [("from", " OR ".join(str(f) for f in froms)), ("label", label)]
            if archive:
                props.append(("shouldArchive", "true"))
                n_archive += 1
            entries.append(_entry(props))
            n_from += 1
        if subjects:
            props = [("subject", " OR ".join(str(s) for s in subjects)), ("label", label)]
            if archive:
                props.append(("shouldArchive", "true"))
            entries.append(_entry(props))
            n_subject += 1

    feed = (
        "<?xml version='1.0' encoding='UTF-8'?>\n"
        "<feed xmlns='http://www.w3.org/2005/Atom' "
        "xmlns:apps='http://schemas.google.com/apps/2006'>\n"
        "  <title>Mail Filters</title>\n"
        + "\n".join(entries)
        + "\n</feed>\n"
    )

    DIST.mkdir(parents=True, exist_ok=True)
    OUT.write_text(feed)

    print(
        f"build_filters: wrote {OUT.relative_to(ROOT.parent)} — "
        f"{len(entries)} filters ({n_from} from-based, {n_subject} subject-based), "
        f"{n_archive} archived categories."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
