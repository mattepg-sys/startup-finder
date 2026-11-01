---
record_type: triage
id: TRI-acme-ai
startup_id: STU-acme-ai
status: template           # template | final
version: 2
what_it_does: "One factual sentence (from the company page)"
customer: "Buyer role + organisation type"
secret_hypothesis: "They bet that X, which most miss because Y"   # HYPOTHESIS; passes the swap test
pan_eu_tam:                 # Western Europe combined: never one country alone
  markets: [ES, IT, FR, DACH]
  buyer_count: {ES: null, IT: null, FR: null, DACH: null, total: null, unit: "organisations", claims: []}
  acv_eur: {low: null, high: null, method: "", claims: []}
  tam_eur_per_year: {low: null, high: null}   # = total buyers x ACV, at full ICP adoption
  passes_floor: null        # tam high >= triage.tam_min_eur_per_year AND tam low >= 50% of floor
eu_knockout:
  queries: []               # >=4, >=2 languages: [{q, lang, hits_used}]
  closest_match: {name: "", country: "", website: "", raised_eur: null, customers_or_staff: "", same_wedge: null, claims: []}
  us_original_in_eu: {finding: "", claims: []}
  knocked_out: null         # true if an exact localised match exists at scale (see run_config triage.eu_knockout)
outcome: PASS               # PASS | PIVOT | KILL
outcome_reason: "one line naming the gate"
pivot_vector: ""            # required if PIVOT: the adaptation that clears both gates, with evidence
upside: "2–3 lines: why it works in the US: wedge, innovation, unfair advantage (cite claims)"
diagnostic: "2–3 lines: European barrier: market size, competitor or regulation (cite claims)"
red_flag: "The single most serious concern"
claims: []
---
# Acme AI: triage card (1 page)

## Upside (why it works in the US)
## Diagnostic (why it may fail in Europe)
## Gates: pan-EU TAM and EU knockout
## Open questions
