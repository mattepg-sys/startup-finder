---
record_type: opportunity_card
id: OPP-acme-ai
startup_id: STU-acme-ai
run_id: RUN-YYYYMMDD-HHMM
status: template          # template | final
version: 1
language: en
company:
  name: Acme AI
  website: https://acme.ai
  hq: "San Francisco, US"
  stage: seed
  round_date: 2026-08-14
  amount_usd: 4200000     # null if unknown
  backers: [{name: "Elad Gil", role: lead_partner}]
  eu_present: false       # true if the company itself already has EU offices/customers
one_liner: "One sentence: what it does, for whom."
business_model: "Who pays, for what, how (price if visible, else HYPOTHESIS)."
maturity: pre_seed          # angel | pre_seed | accelerator | seed_young | seed
evidence_level: partial     # solid | partial | thin
label: DIFFERENTIABLE     # OPEN_SPACE | DIFFERENTIABLE | TRANSFERABLE | WATCH | BLOCKED
label_reason: "One sentence on why this label."
secret: {text: "The non-obvious mechanism that makes it work in the US.", claims: [C1]}
europe_queries: [{q: "", lang: es}, {q: "", lang: en}]     # ≥2
europe_today:             # 0–5 named players; for each, what they do NOT do
  - {name: "", country: "", website: "", what_they_do: "", what_they_miss: "", scale: "", claims: []}
angles:                   # 3–5 specific differentiation angles
  - {title: "", for_whom: "", why_gap: "", evidence: "", claims: []}
transfers:                # 2–3 other sectors for the same mechanism
  - {sector: "", how: "", why_promising: ""}
risks:                    # 1–3, informative, not a veto
  - {risk: "", severity: medium, claims: []}
questions: ["", "", ""]   # 3–5 prompts for the user's creativity
your_edge: null           # filled only if config/user_profile.md has content
one_week_test: {what: "", signal: "", cost_eur: 0}
scores:                   # 1–5, no total
  insight: {score: 3, why: ""}
  transferability: {score: 3, why: ""}
  space: {score: 3, why: ""}
  differentiation: {score: 3, why: ""}
  feasibility: {score: 3, why: ""}
  personal_fit: {score: null, why: "no profile"}
tam_hint: null            # optional {low_eur, high_eur, method}, never a gate
claims: []
---
# Acme AI: Opportunity Card
(The report is built from the front-matter; the body is optional notes.)

## Open questions
