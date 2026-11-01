---
record_type: investor_person
id: PER-jane-doe
name: Jane Doe
role: "General Partner"           # GP / Partner / Group Partner (YC) / Solo GP / Angel / Scout
firm: Example Ventures            # "independent" for super-angels
firm_id: INV-example-ventures     # or null
person_class: seed_partner        # yc_partner | seed_partner | solo_gp | super_angel | operator_angel | scout
home_market: US
pitchbook_profile: https://my.pitchbook.com/profile/XXXXX-XX/person/profile
status: template                  # template | candidate | approved | retired
version: 1
last_refreshed: 2026-10-08
footprint:                        # what THIS person personally did (lead partner / board seat / personal angel cheque)
  window: "2025-10..2026-10"
  deals_total_12m: null
  deals_as_lead_partner_12m: null
  personal_angel_deals_12m: null
  board_seats_current: null
  claims: []
metrics:                          # same definitions as config/rubrics.md, computed on this person's deals
  E1_activity_12m: {value: null, n: null, claims: []}
  E2_earliness: {value: null, n: null, claims: []}              # share where the person backed the first institutional round
  E3_graduation_shrunk: {value: null, raw_k: null, raw_n: null, prior_p0: null, interval_80: null, vintages: "2020-2023", status: INSUFFICIENT, claims: []}
  E4_conviction: {value: null, n: null, claims: []}             # share of deals where the person is lead partner / led personally
  E7_stealth_share: {value: null, n: null, claims: []}          # share of recent deals with no press coverage at round date (early-signal value)
  E5_specialism: {top_sector: null, share: null, n: null, claims: []}
rank: null
weakest_metric: null
evidence_quality: L
recent_deals:                     # newest first, ≤ deals_per_person_max, non-European HQ only
  - {company: "", pitchbook_company_url: "", date: null, stage: pre_seed, role: lead_partner, hq_country: US, website: "", one_line_from_pitchbook: "", press_found: null, claims: []}
claims: []
---
# Jane Doe (Example Ventures)

## Why this person is a signal (3–5 lines, cited, no fame arguments)
## Recent personal footprint
## Open questions
