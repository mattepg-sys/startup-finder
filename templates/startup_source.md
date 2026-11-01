---
record_type: startup_source
id: STU-acme-ai
name: Acme AI
website: https://acme.ai
domain: acme.ai
hq_country: US
founded: 2025
status: template           # template | sourced | triaged | shortlisted | deep | dropped | final
version: 1
found_via: [INV-example-ventures]
round:
  stage: seed              # pre_seed | seed | series_a
  date: 2026-08-14         # event date, not article date
  amount_usd: 4200000      # null if undisclosed
  lead: "Example Ventures"
  investors: ["Example Ventures", "Angel X"]
  claims: [C1]
first_signal_date: 2026-07-30
signal_type: form_d        # pitchbook | form_d | registry | portfolio_page | press | programme | social
one_line: "Acme AI automates prior-authorisation paperwork for US orthopaedic clinics"   # factual, from the company's own site
sector_guess: "healthcare / vertical AI"
customer_type: B2B         # B2B | B2C | B2B2C | B2G
claims:
  - id: C1
    text: "Raised $4.2M seed led by Example Ventures on 2026-08-14"
    label: FACT
    key_number: true
    sources:
      - {url: "https://pitchbook.com/profiles/company/XXXX", title: "Acme AI profile", publisher: PitchBook, source_type: pitchbook, published: 2026-10-06, accessed: 2026-10-06}
      - {url: "https://acme.ai/blog/seed", title: "Announcing our seed", publisher: "Acme AI", source_type: primary, published: 2026-08-14, accessed: 2026-10-06}
    single_source: false
    confidence: H
---
# Acme AI — sourcing record
Earliest signal: Form D filed 2026-07-30, ahead of the 2026-08-14 announcement.

## Open questions
