---
record_type: investor
id: INV-example-ventures
name: Example Ventures
investor_class: pre_seed_specialist   # seed_generalist | accelerator | pre_seed_specialist | sector_specialist | eu_seed_global
hq_country: US
website: https://example.vc
stages: [pre_seed, seed]
status: template          # template | candidate | approved | rejected | retired | final
version: 1
last_refreshed: 2026-10-06
data_basis: pitchbook     # pitchbook | public | mixed
metrics:
  E1_activity_12m: {value: 14, n: 14, window: "2025-10..2026-09", claims: [C1]}
  E2_earliness: {value: 0.64, n: 14, claims: [C1]}
  E3_graduation_shrunk: {value: 0.31, raw_k: 7, raw_n: 18, prior_p0: 0.20, interval_80: [0.21, 0.42], vintages: "2020-2023", window_months: 24, claims: [C2]}
  E4_conviction: {value: 0.50, n: 14, claims: [C1]}
  E5_specialism: {top_sector: "vertical SaaS", share: 0.43, n: 14, claims: [C1]}
  E6_independence: {value: 0.71, n: 14, claims: [C1]}
  outliers_shown_not_ranked: []
rank_in_class: null
weakest_metric: E3_graduation_shrunk
evidence_quality: M
claims:
  - id: C1
    text: "14 pre-seed/seed/A rounds Oct 2025–Sep 2026 per investments table"
    label: FACT
    key_number: true
    sources:
      - {url: "https://pitchbook.com/profiles/investor/XXXX", title: "Example Ventures investor profile", publisher: PitchBook, source_type: pitchbook, published: 2026-10-06, accessed: 2026-10-06}
    single_source: true
    confidence: M
  - id: C2
    text: "7 of 18 seed deals (2020–2023) raised a next priced round within 24 months"
    label: ESTIMATE
    key_number: true
    method: "Counted from the investments table 'last financing' column; shrinkage per config/rubrics.md"
    sources:
      - {url: "https://pitchbook.com/profiles/investor/XXXX", title: "Investments tab", publisher: PitchBook, source_type: pitchbook, published: 2026-10-06, accessed: 2026-10-06}
    single_source: true
    confidence: M
---
# Example Ventures

## Why this investor is on the list
(3–5 lines, citing [C1]… No brand-based arguments.)

## Recent deals seen (for A2)
| Company | Round | Date | Lead? | Source |
|---|---|---|---|---|

## Open questions
