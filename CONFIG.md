# CONFIG.md — your personalization (the ONLY file with your details)

Every skill reads its personal values from here **by name**. Skills never embed your name,
doc IDs, repos, or URLs directly — that is what keeps this kit portable. When you move to a new
account, you fill in this one file and everything else just works.

> **Rules**
> - Replace every `<< ... >>` placeholder with your real value.
> - Do **not** put secrets, tokens, or passwords here. Credentials live in the connectors you
>   reconnect per account (Gmail, Calendar, Drive, GitHub, etc.), never in this repo.
> - Leave a value as its placeholder if a skill that uses it isn't enabled — that skill just
>   won't run until you fill it in.

---

## Identity

- **Name:** << your name >>
- **Role / title:** << your role, e.g. Senior Director, Developer Relations >>
- **Company / org:** << your company >>
- **Timezone:** << e.g. America/New_York >>
- **Working hours:** << e.g. 09:00–18:00 >>  <!-- used by timing guardrails -->

## Voice & tone

Used by every skill that DRAFTS text in your name (`kudos-radar`, `inbox-triage-drafts`,
`daily-wins-recap`, `weekly-impact-summary`, `brag-doc-builder`). Describe how you sound so
drafts read like you — the words stay yours, the kit just gets the first draft close.

- **Voice descriptor:** << e.g. warm, direct, low on jargon, occasional dry humor >>
- **Sign-off you use:** << e.g. "Thanks, <name>" >>
- **Things to avoid:** << e.g. corporate filler, exclamation overload, em-dashes >>

## Topics & interests

- **Industry-digest topics:** << comma-separated, e.g. AI agents, developer tooling, OSS funding >>
- **Beats I must never be surprised by:** << e.g. anything touching my team's product area >>

## GitHub

- **GitHub username:** << your-github-username >>
- **Primary org:** << your-org >>
- **Repos to watch (ship-decoder / stale-work / CI):** << owner/repo, owner/repo2 >>
- **Ship-decoder sources:** << repos AND/OR changelog URL AND/OR Slack channels >>

## People

- **Direct reports (for one-on-one-prep):** << name (github/email), name2 (github/email) >>
- **Key collaborators:** << optional: people whose activity matters for prep >>

## Watch lists

- **Competitor URLs / feeds (competitor-watch):** << https://..., https://... >>
- **Launch sources (launch-radar):** << release pages, roadmaps, newsletters >>

## Documents (names + IDs — IDs optional, names required)

- **Running "wins" doc (daily-wins-recap, weekly-impact-summary):** name = << "My Wins Log" >>, id = << google-doc-id or leave blank to search by name >>
- **Brag doc (brag-doc-builder):** name = << "Brag Doc 2026" >>, id = << optional >>
- **Receipts / expenses Drive folder (receipts-and-expenses):** name = << "Receipts 2026" >>, id = << optional >>

## Thresholds

- **Follow-up staleness N (follow-up-tracker):** << 3 >> days
- **Daily-triage urgency window:** << today + tomorrow >>

## Connector choices (swap per account)

The kit assumes **Google Workspace** (Gmail, Calendar, Drive) and **GitHub**. Where a skill
could use a different tool, set your choice here and the skill adapts. Leave as-is to use the
default.

- **Messaging connector:** << Slack | Linear | none >>  (used by daily-triage-digest, commitments-tracker)
- **Web-search / monitoring connector:** << web search | Firecrawl | none >>  (industry-digest, competitor-watch, launch-radar, ship-decoder fallback)
- **Issue tracker:** << GitHub | Linear | Jira | none >>
