---
record_type: learnings
version: 1
last_updated: '2026-10-31'
last_run: null
max_active_entries: 40
---
# Learnings: the tool's memory

Every agent reads this file at Step 0. Entries refine how agents work. They never override `config/evidence_standard.md`, the PitchBook rules or the caps in `run_config.yaml`. New entries are added only through `tools/learnings_append.py`, typically by the retrospective agent after a run, or by you.

## Agent Rules & Self-Corrections

### L-RULE-001 · ALL · Read PitchBook only with page-reading tools, never scripts
<!-- key: all-no-js-on-pitchbook -->
- **Rule:** Load browser tools by exact name, read PitchBook pages only with get_page_text, read_page, find or screenshots, and never run JavaScript on the tab.
- **Why:** Scripted reading is automated extraction and can get the account blocked.
- **Evidence:** Repeated attempts were blocked by permissions during development.
- **Applies to:** ALL
- **Seen:** 3 · first 2026-10-08 · last 2026-10-30
- **Status:** active

### L-RULE-002 · A1 · Check the company page before attributing a deal to a person
<!-- key: a1-verify-person-deal-attribution -->
- **Rule:** When a person's table lists a deal, confirm the company name, website and round on the company page or website before queueing it.
- **Why:** Rows on person pages can be crossed between companies.
- **Evidence:** A crossed row (two companies swapped) was caught during development.
- **Applies to:** A1
- **Seen:** 2 · first 2026-10-08 · last 2026-10-09
- **Status:** active

### L-RULE-003 · A1 · Read PitchBook tables efficiently
<!-- key: a1-pitchbook-spa-reading -->
- **Rule:** On person and fund pages use find for dates and company links and read_page at depth 2; use get_page_text with a 4000-character cap on company pages, and wait 3 s and re-read when a page shows only menus.
- **Why:** PitchBook pages render slowly and full reads are very long.
- **Evidence:** Development runs.
- **Applies to:** A1
- **Seen:** 2 · first 2026-10-30 · last 2026-10-30
- **Status:** active

### L-RULE-004 · ALL · Keep temp files inside your own folder
<!-- key: all-no-stray-temp-files -->
- **Rule:** Write temporary scripts and drafts only inside the current run folder or your startup's folder, never in the project root.
- **Why:** Some synced folders don't allow deletion, so strays pile up.
- **Evidence:** Development runs.
- **Applies to:** ALL
- **Seen:** 2 · first 2026-10-30 · last 2026-10-30
- **Status:** active

### L-RULE-005 · A2 · Use the full label range
<!-- key: a3b-label-calibration -->
- **Rule:** Choose OPEN_SPACE when no named European player serves the same buyer and use case, TRANSFERABLE when the best angle sits in another sector, WATCH when evidence is thin and the market unproven; reserve DIFFERENTIABLE for named players with named gaps.
- **Why:** Defaulting to DIFFERENTIABLE flattens the report.
- **Evidence:** Development runs.
- **Applies to:** A2
- **Seen:** 1 · first 2026-10-30 · last 2026-10-30
- **Status:** candidate

## User Preferences & Feedback

_No entries yet. Paste your report feedback into the chat to add some._

## Kill Patterns (Red Team)
<!-- In v0.1 these inform the cards' risks; they never veto. -->

### L-KILL-001 · A2 · The US original already sells in Europe
<!-- key: kill-already-shipping-in-europe -->
- **Rule:** Check whether the US company itself already has European offices or customers, and list it as a European player when it does.
- **Why:** The most common reason a straight copy fails.
- **Evidence:** Most later-stage deals in development runs.
- **Applies to:** A2
- **Seen:** 3 · first 2026-10-08 · last 2026-10-30
- **Status:** active
