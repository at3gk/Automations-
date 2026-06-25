# ADDING_A_BRIEF.md — add a new lens in < 10 minutes

A light brief is just slot values over `../brief-engine.md`. Adding one touches **no Python and no
engine code** — that's the proof the engine works.

## Steps

1. **Pick a label to read.** It must already exist in `config/taxonomy.yml` (and usually be fed by
   `config/sender-map.yml`). If it's a brand-new category, add it to the config first and re-run
   `generate/validate_config.py` + `generate/build_filters.py`.
2. **Copy a sibling skill.** `cp -r .claude/skills/brief-career .claude/skills/brief-<name>` (from the repo root) is the
   fastest start (career is the simplest single-label lens).
3. **Fill the slot table** in the new `SKILL.md` (see the template below) and rewrite the
   frontmatter `name`/`description` so the kit auto-discovers it.
4. **Register it** the kit way: add a row to the root `README.md` skills table and a block to
   `SCHEDULES.md`; add an entry to `pipeline.json` (`kind: consumer`, its `reads`/`writes`,
   `section_prefix`) and to `run_order` (after `inbox-triage`). Stagger its schedule a few minutes
   off the other lenses so they don't race to create the day's Daily Briefs event.
5. Done. The new ledger `ledger-<slug>.json` is created on first `apply` run in Drive — nothing to
   set up.

## Slot table to fill (copy)

```
{{BRIEF_NAME}}          # e.g. "Health"
{{SLUG}}                # e.g. health   -> owns ledger-health.json
{{TARGET_LABEL_QUERY}}  # e.g. label:"Health"
{{WINDOW}}              # fallback window when triage is stale, e.g. 14d
{{ITEM_DEFINITION}}     # what counts as an item; what to exclude
{{OUTPUT_FIELDS}}       # per-item fields, e.g. what / date / action
{{PRIORITY_RUBRIC}}     # ordering, e.g. soonest date first
{{FOCUS}}               # optional emphasis
{{DRAFT_PREFIX}}        # e.g. Brief: Health   -> section "### Brief: Health" in the Daily Briefs event
{{MAX_ITEMS}}           # cap, e.g. 10
```

The engine body (`brief-engine.md`) handles state/staleness/idempotency/pagination and delivery
(upserting your section into the consolidated Daily Briefs event) — you only describe *what* this
lens looks for.
