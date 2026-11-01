# Evidence standard (shared by all agents; prepended to every subagent prompt)

## 1. Every substantive statement is a claim with a label
Claims live in the record's YAML front-matter under `claims:`. In the body, reference them as [C1], [C2]…
```yaml
- id: C1
  text: "Raised $4.2M seed led by Example Ventures"
  label: FACT            # FACT | ESTIMATE | HYPOTHESIS
  key_number: true       # funding, valuation, revenue, users, headcount, market counts, prices
  sources:
    - url: https://...
      title: "..."
      publisher: "..."
      source_type: primary   # primary | secondary | pitchbook | aggregator
      published: 2026-08-14  # date of the source (YYYY-MM-DD; YYYY-MM if only month known)
      accessed: 2026-10-06
  single_source: false
  confidence: H          # H | M | L
  method: ""             # required for ESTIMATE: how computed, inputs referenced by claim id
  falsifier: ""          # required for HYPOTHESIS: what observation would prove it wrong
```
- **FACT**: directly stated by a cited source. Needs ≥1 source with URL + published date.
- **ESTIMATE**: derived by you from facts; must show `method` and its inputs. Round honestly; give a range.
- **HYPOTHESIS**: your interpretation (e.g., why it works). Must have a `falsifier`. Most "why it works" content is HYPOTHESIS—say so.
- No source → not a FACT. Don't know → write `UNKNOWN` and how to verify. Never fill gaps with plausible guesses.

## 2. Source hierarchy
1. **Primary**: company's own site/blog/press release/job posts, founder posts, investor's own announcement, regulatory filings (SEC Form D, Companies House, Handelsregister, BORME, BODACC), court/patent/trademark registers, official statistics (Eurostat, INE, ISTAT, Destatis).
2. **PitchBook** (`source_type: pitchbook`, URL = the profile URL, `accessed` = view date): curated, strong for deal data. Not a primary source for traction claims.
3. **Secondary**: reputable press (FT, Sifted, TechCrunch, Expansión, Il Sole 24 Ore, Handelsblatt, Les Echos).
4. **Aggregator**: Crunchbase, Dealroom, Tracxn, Seedtable, Nordic9, Wikipedia — **discovery only**: use to find names and primaries; never sole support for a key number, a metric, a round stage or a website, whatever the label (FACT or ESTIMATE).

## 3. Key numbers need two independent sources
- `key_number: true` requires ≥2 sources that are **independent** (not one quoting the other; an aggregator restating a press release is NOT independent of it). PitchBook + one public primary/secondary counts.
- If only one exists: keep it, set `single_source: true`, confidence ≤ M. Memos must show "(single source)".
- Conflicting numbers: report both with sources; don't average.

## 4. Freshness
- Always record `published`. Funding data older than 12 months, traction older than 6 months → add `stale: true`.
- Event date ≠ article date: a 2026 article about a 2024 round is a 2024 round.
- "Recently", "currently", "leading" without a date are banned.

## 5. Banned patterns (validator rejects them)
- Top-down sizing: "X% of a €Nbn market", "if we capture 1%". Use bottom-up: (named count of target organisations, with source) × (ACV estimate, with method).
- Generic praise without a specific, sourced mechanism: "strong team", "huge market", "AI-powered", "first-mover advantage", "great product", "passionate founders", "disruptive", "game-changer", "seamless".
- Invented people or customers. Every named person/organisation must come from a source in this record.
- Personal contact details (emails, phone numbers) of private individuals. Organisations + roles only.

## 6. The "swap test" for analysis
Before finalising any "why it works" or "wedge" text: mentally replace the company name with a competitor's. If the sentence is still true, it's generic—rewrite with the specific mechanism, number, or evidence.

## 7. Honesty about uncertainty
End every record body with `## Open questions` listing what you couldn't verify and the cheapest way to verify it (a URL to check, a person-role to ask, a registry to search).

## 8. PitchBook lane (only agents explicitly allowed: A1, A2, and A3/A4 for ≤8 single company lookups)
- the user logs in; you never handle credentials, captchas or 2FA.
- ≥ `min_seconds_between_views` between page loads; never exceed `max_views_per_session`; never click Export/Download; ≤3 table pages per profile.
- Log each view in the run's `pitchbook_log.md`: `| time | page_type | entity | purpose |`.
- Page approvals (`pitchbook.mode: live_browser`): before each PitchBook page load, if the browser asks for site access, call `request_access` with scope "once" and wait for the user's approval, then load. A denied or unanswered approval → pause and report. Do not switch to public sources.
- On captcha / rate-limit / "unusual activity" / logout: stop PitchBook immediately, log it (`--action pitchbook_stop`), **halt the PitchBook stage** (`on_unavailable: halt`) and return to the orchestrator. Never fall back to aggregators silently.
- **Load browser tools by exact name only**: `select:mcp__remote-devices__Claude_Browser__navigate,…__get_page_text,…__read_page,…__find,…__computer,…__request_access,…__tabs_context`. Never load the whole Claude_Browser namespace, and never load `javascript_tool`.
- Read PitchBook with navigate, get_page_text, read_page, find and screenshots only. **Never run JavaScript on PitchBook pages** (no javascript_tool, no injected hooks, no calls to its internal APIs). That is automated extraction, whatever the pace.
- Only one agent uses PitchBook at a time; the orchestrator grants the lane explicitly in your task prompt ("PITCHBOOK_LANE: granted, budget N views"). No grant → don't open PitchBook.

## 9. File discipline
- Write only the paths your task prompt assigns you. Write to `<file>.tmp` then rename.
- Never edit a file with `status: final`; create `<name>.v2.md` with `supersedes:` and `change_reason:`.
- After writing, validate **every** attempt with logging on, so first-pass failures are captured for the retrospective: `python3 tools/validate.py <your files> --log --run <run_id> --agent <A#>`. Fix the errors and re-run. Never delete or edit `logs/validation.jsonl`.
- After the file passes, append one line to `logs/events.jsonl` (the orchestrator gives you the helper command).
- Don't game the validator: a fake or non-independent second source is a worse violation than a flagged `single_source`.
- If you cannot complete: write `FAILED.md` in your target folder with the reason and what you got.
