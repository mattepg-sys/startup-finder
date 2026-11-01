# Startup Finder: product spec v3 (2026-10-30)

## What the tool is for
**An inspiration engine, not an investment committee.** It finds what top individual investors (solo GPs, angels) have just backed in the US/global market, explains *why* it works, maps what already exists in Europe, and hands the user concrete angles to build on:
- where an existing European player leaves room to **differentiate**;
- where the user's own **domain knowledge** could become an edge (optional);
- which **other sector** the same mechanism could be transplanted to.

It does **not** promise a perfect turnkey idea. It must never discard an idea only because competitors exist: competitors are information.

## Who uses it
Mostly students and early founders. They may have **no domain expertise and no profile**. The tool must work fully without a profile; a profile only adds a "your edge" section.

## Core loop (default run, profile `quick`, target ≤ 20 machine-minutes)
1. **Scout** (PitchBook, user's own licence): 6–12 individual investors → ≤12 recent deals, each checked on its company page. Deals with obvious European presence are flagged, not dropped.
2. **Opportunity Lab** (parallel, ~2–3 min per deal): one **Opportunity Card** per deal.
3. **Report**: one HTML page per run (`runs/<run>/report.html`) built by a script, with no AI and no tokens.
4. **Optional deep dive** on the 1–2 cards the user picks: full Europe map, proposal and red team (legacy pipeline).

## Opportunity labels (replace PASS/KILL)
| Label | Meaning | Typical next step |
|---|---|---|
| **OPEN_SPACE** | No clear European equivalent for this buyer/use case | Validate demand fast |
| **DIFFERENTIABLE** | Players exist, but leave named gaps (segment, language, workflow, price, regulation) | Pick one gap and own it |
| **TRANSFERABLE** | The *mechanism* is more promising in another sector than as a copy | Explore the named sector |
| **WATCH** | Interesting, but timing, team or market isn't there yet | Revisit in 6–12 months |
| **BLOCKED** | Hard blocker for a small team: licence, hardware, deep science, illegal in EU | Only learn from the mechanism |

## Opportunity Card (one screen per deal)
1. **One-liner**: what it does and who backed it (investor signal).
2. **The secret**: the non-obvious mechanism that makes it work in the US (labelled HYPOTHESIS when inferred).
3. **Europe today**: 2–5 named players, with what each does *not* do.
4. **Differentiation angles**: 3–5 specific angles (segment, language, workflow, regulation, pricing, channel). Each has a reason and evidence.
5. **Transfers**: 2–3 other sectors where the same mechanism applies, with why.
6. **Risks to know**: the 3 strongest risks (light red team). They inform; they do not veto.
7. **Questions for you**: 3–5 prompts that open creative space.
8. **Your edge**: only if a profile exists. How the user's background fits.
9. **One-week test**: one cheap experiment with a numeric signal.
10. **Scores** (1–5, no total): Insight · Transferability · Space · Differentiation · Feasibility [· Personal fit].
11. **Sources**: clickable, every key fact labelled FACT, ESTIMATE or HYPOTHESIS.

## Language
Everything (prompts, agents, cards, report) is **English by default**. A user can write prompts in any language and set `report_language` (in `config/user_profile.md` or `run_config.yaml`) to receive cards and the report in another language. Field keys and labels always stay in English.

## What we keep from v2
- Evidence standard (labels, dated sources, no top-down sizing).
- Single-writer files, sealed runs, the validator.
- The learnings loop.
- The PitchBook rules: no scripts, pacing, user-owned login.

## What we cut from the default path
- PASS/KILL gates.
- Mandatory pan-EU TAM per deal: a TAM range only when cheap, never as a gate.
- The fund-level investor ranking.
- A separate verification agent.
- The strategist and red team run on every idea: they are now on demand only.
- The heavy retrospective: the default is now a short automatic note.

## Success metrics for the product
- Machine time ≤ 20 min per quick run.
- ≥ 70% of cards rated "useful" by the user (thumbs in the report).
- ≥ 3 specific differentiation angles per card.
- 0 fabricated sources in a 10-claim audit.
