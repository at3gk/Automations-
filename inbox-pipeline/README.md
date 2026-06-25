# inbox-pipeline

A Gmail + Google Drive **producer→consumer pipeline** that lives inside the Personal Automations
Kit. It is the home for the *shared, non-skill machinery* (config, generators, the brief engine,
JSON schemas, deterministic CapWeb code, docs). The runnable routines are **project skills** under
`.claude/skills/`, so any Claude Code session that clones this repo (including cloud sessions)
auto-discovers and schedules them with no install step.

## Mental model

- **Producer — `.claude/skills/inbox-triage`.** Labels/archives the unlabeled tail of the inbox from
  `config/*.yml` and writes the Drive manifest `inbox-state.json`. Everything else depends on it.
- **Consumers — `.claude/skills/brief-*` + `.claude/skills/capweb-reconcile`.** Read the manifest,
  query Gmail **by label**, and deliver a Gmail **draft**. Light briefs are thin lenses over
  `brief-engine.md`; CapWeb is the heavy, deterministic exception.

Three conventions chain them into a pipeline: **consistent labels** (`config/taxonomy.yml`), the
**Drive manifest** (`inbox-state.json`), and **Gmail drafts** as the review surface. The full run
contract is in [`docs/CONVENTIONS.md`](./docs/CONVENTIONS.md).

## What's here

```
config/        taxonomy.yml, sender-map.yml, ambiguous.yml   — SINGLE SOURCE OF TRUTH
generate/      validate_config.py (drift guard), build_filters.py (-> dist/gmail-filters.xml)
brief-engine.md  parameterized engine every light brief instantiates
capweb/        reconcile.py, propose_payments.py, extract_schema.md, schemas/, tests/
docs/          CONVENTIONS.md, DRIVE_LAYOUT.md, ADDING_A_BRIEF.md
pipeline.json  producer/consumer manifest + run_order
dist/, state/  generated/scratch — gitignored
```

The skills themselves: `.claude/skills/inbox-triage`, `.claude/skills/brief-ai-learning`,
`.claude/skills/brief-finance`, `.claude/skills/brief-career`, `.claude/skills/brief-travel`,
`.claude/skills/capweb-reconcile`.

## Regenerate filters / validate config

```bash
python inbox-pipeline/generate/validate_config.py     # lint config; exits non-zero on error
python inbox-pipeline/generate/build_filters.py       # -> inbox-pipeline/dist/gmail-filters.xml
python inbox-pipeline/capweb/tests/test_reconcile.py  # deterministic reconciliation tests
```

## Data / secrets split (same as the kit)

**Code/config in git; data/state in Drive; secrets in env.** Ledgers, `inbox-state.json`, the
generated XML, and any extracted/financial data are **never** committed (see root `.gitignore`).
State lives in Drive `/AutomationState/` — shapes documented in
[`docs/DRIVE_LAYOUT.md`](./docs/DRIVE_LAYOUT.md).

## Security note

No credentials, tokens, or message/financial data ever touch this repo. CapWeb is deterministic and
human-in-the-loop: it reconciles with exact-dollar matching, halts on any mismatch, and only ever
**proposes** payments for your approval — it has no network access and executes nothing. Triage's
only mutations (label/archive) are reversible, gated behind an explicit "apply", and capped by an
anomaly guard.

## Add a new brief

See [`docs/ADDING_A_BRIEF.md`](./docs/ADDING_A_BRIEF.md) — it's a slot table over `brief-engine.md`,
no Python and no engine changes.
