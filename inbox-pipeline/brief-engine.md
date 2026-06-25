# brief-engine.md — the parameterized brief engine

Every light `brief-*` lens is an instance of this one procedure. A lens supplies the slot values
below; the engine is the shared body. (CapWeb does **not** use this engine for its reconciliation —
it delegates to `.claude/skills/capweb-reconcile`.) This keeps "adding a brief" to filling a slot table —
see `docs/ADDING_A_BRIEF.md`.

## Slots a lens must fill

| Slot | Meaning |
|---|---|
| `{{BRIEF_NAME}}` | human name, e.g. "AI Learning" |
| `{{SLUG}}` | ledger slug, e.g. `ai-learning` → owns `ledger-ai-learning.json` |
| `{{TARGET_LABEL_QUERY}}` | Gmail label query, e.g. `(label:"AI & Dev/Newsletters" OR label:"AI & Dev/Learning")` |
| `{{WINDOW}}` | fallback recency window when triage is stale/missing, e.g. `3d` |
| `{{ITEM_DEFINITION}}` | what counts as an item (and what to exclude) |
| `{{OUTPUT_FIELDS}}` | the per-item fields to emit |
| `{{PRIORITY_RUBRIC}}` | how to order items |
| `{{FOCUS}}` | lens on what matters (optional emphasis) |
| `{{DRAFT_PREFIX}}` | draft title prefix, e.g. `Brief: AI Learning` |
| `{{MAX_ITEMS}}` | cap; note overflow if exceeded |

## Procedure (engine body)

These run unattended — never pause to ask a question. Obeys `docs/CONVENTIONS.md` (modes,
idempotency, staleness, least privilege).

1. **Read state.** Load `inbox-state.json` from Drive `/AutomationState/`. Read `last_triage`.
2. **Staleness guard.** If `last_triage` is missing or older than `max_staleness` (36h), set
   `STALE = true`.
3. **Query.**
   - Fresh: `{{TARGET_LABEL_QUERY}} after:{last_triage}`.
   - Stale/missing: fall back to `{{TARGET_LABEL_QUERY}} newer_than:{{WINDOW}}` and, if even the
     label may be unapplied, widen to `newer_than:{{WINDOW}}`. **Prominently note** "triage
     stale/missing — results may include unlabeled mail."
   - **Paginate to exhaustion. Ignore `resultCountEstimate`.**
4. **De-dup.** Drop any thread/message whose ID is already in `ledger-{{SLUG}}.json`.
5. **Extract.** Keep only items matching `{{ITEM_DEFINITION}}`; discard the rest (count them).
6. **Emit.** For each kept item, produce `{{OUTPUT_FIELDS}}`.
7. **Prioritize.** Order by `{{PRIORITY_RUBRIC}}`, applying `{{FOCUS}}`. Cap at `{{MAX_ITEMS}}`;
   if more remain, keep the top `{{MAX_ITEMS}}` and **note the overflow count**.
8. **Deliver.** Create a Gmail **draft** titled `[{{DRAFT_PREFIX}}] {date}`, top items first, with
   the mode (propose/apply) stated at the top and the staleness note if `STALE`.
9. **Apply mode only.** Append the briefed IDs (+ run timestamp) to `ledger-{{SLUG}}.json`. Never
   modify labels/archive, never write `inbox-state.json`, never touch another routine's ledger.

## Output skeleton

```
[{{BRIEF_NAME}}] Brief — {date}   (mode: propose|apply)
<staleness note, only if triage stale/missing>

1. <highest-priority item> — {{OUTPUT_FIELDS}}
2. ...

(+N more not shown — raise {{MAX_ITEMS}} or narrow the window)
Skipped ~N off-topic items.
```
