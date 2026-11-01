---
record_type: opportunity_card
id: OPP-magma
startup_id: STU-magma
run_id: SAMPLE
status: final
version: 1
language: en
company:
  name: Magma
  website: https://magmahq.ai
  hq: "UNKNOWN (site brand: Magma Intelligence Inc.)"
  stage: accelerator
  round_date: null
  amount_usd: null
  backers: [{name: "Y Combinator", role: accelerator}]
  eu_present: false
one_liner: "Magma packages the work traces AI agents generate inside companies (actions, corrections, completed workflows) and licenses them to AI labs, sharing revenue with the data provider [C1]."
business_model: "Two sides: a company with AI agents supplies data and gets a revenue share (percentage not published); AI labs pay for licences. HYPOTHESIS: pricing by volume or domain, not visible on the site [C1, C2]."
maturity: accelerator
evidence_level: thin
label: WATCH
label_reason: "Promising mechanism, but it needs lab demand for external work traces that is unproven, plus trust and liquidity on two sides, which a small team cannot force in three months."
secret: {text: "HYPOTHESIS: labs have exhausted useful web data and pay for real examples of completed work with human corrections; companies running agents own such flows but have no channel to sell them, so Magma acts as a licensing intermediary with revenue share [C1, C2].", claims: [C1, C2]}
europe_queries:
  - {q: "marketplace licensing AI agent work recordings training data Europe startup", lang: en}
  - {q: "dati di lavoro per addestrare agenti AI licenza dati professionisti startup Europa", lang: it}
europe_today:
  - {name: "Human Native AI", country: "UK", website: "https://www.uktech.news/ai/human-native-ai-funding-20240604", what_they_do: "Marketplace where content owners license data to companies training AI models", what_they_miss: "Content (text, images, video), not agent traces with corrections; no product seen for company workflow data", scale: "Funding round announced 2024; current size UNKNOWN", claims: [C3]}
  - {name: "Trainspot", country: "UNKNOWN", website: "https://www.businesswire.com/news/home/20241028726844/en/Introducing-Trainspot-The-AI-Data-Marketplace-That-Works-for-Everyone", what_they_do: "AI training-data marketplace presented as fair to data providers", what_they_miss: "Generic data positioning; no European vertical or agent traces stated", scale: "UNKNOWN", claims: [C4]}
angles:
  - {title: "Work traces in Italian and Spanish for regulated verticals (tax, legal, payroll)", for_whom: "Accounting and labour-consulting practices in Italy and Spain already using AI assistants on cases", why_gap: "Magma's site speaks of companies with AI agents, with no language or vertical; the European marketplaces found sell content, not completed local-language casework.", evidence: "HYPOTHESIS: multilingual models have little material on local tax procedures; falsifiable with 5 calls to model-training teams.", claims: [C1, C3]}
  - {title: "GDPR anonymisation as the product, not an obstacle", for_whom: "European companies with AI agents that cannot sell data containing personal information", why_gap: "Magma describes a read-only connection and approved scope but states no anonymisation or GDPR guarantees; the marketplaces found are not built for traces with client data.", evidence: "Site says read-only, encrypted, scoped to what you approve, handling in the data agreement [C1]. A GDPR gap is a HYPOTHESIS to check in the terms.", claims: [C1]}
  - {title: "License one trade's data in exchange for free tooling", for_whom: "Niche vertical-software vendors (dental practices, logistics) with user workflows but no data-sales channel", why_gap: "Magma targets those building agents; a vertical-software vendor with thousands of users is a different, unmentioned supplier.", evidence: "HYPOTHESIS without a source: one vendor is easier to convince than 1,000 separate SMEs.", claims: [C2]}
transfers:
  - {sector: "Field technician intervention data (HVAC, lifts, maintenance)", how: "Record checklists, photos and technician corrections to train diagnostic agents and license them to manufacturers", why_promising: "Tacit, detailed knowledge missing from public datasets; European manufacturers are natural buyers"}
  - {sector: "Administrative medical coding", how: "Corrected coding and billing traces, anonymised, for administrative agents", why_promising: "Repetitive, nationally regulated, language-dependent; the European Health Data Space pushes secondary data use"}
  - {sector: "Multilingual SME customer service", how: "Operator-resolved conversations and corrections to AI replies, licensed to builders of voice agents", why_promising: "High volume and under-served languages (Italian, Spanish) where labs have fewer examples"}
risks:
  - {risk: "Two-sided cold start: data providers must trust and labs must pay, and big labs can build their own data in-house.", severity: high, claims: [C2]}
  - {risk: "Privacy and data ownership: work traces contain client data and trade secrets; in Europe GDPR and contractual confidentiality slow every transfer.", severity: high, claims: [C1]}
  - {risk: "Thin evidence: one-page site, no named customers or buyers, no prices; everything about lab demand is HYPOTHESIS.", severity: medium, claims: [C1, C2]}
questions:
  - "Which trade you know produces daily examples of work done well that an AI lab cannot get from the web?"
  - "Who in Europe owns Italian or Spanish workflow data nobody has thought of selling?"
  - "If privacy is the problem, can anonymisation become the product itself?"
  - "Would you sell to labs or to builders of vertical agents: who actually pays?"
one_week_test: {what: "Contact 10 teams building vertical AI agents in Europe and 5 model-training teams: would you pay for local-language work traces, and at what price?", signal: ">=3 of 5 buyers describe a concrete use case and >=4 of 10 suppliers agree to discuss licensing terms", cost_eur: 0}
your_edge: null
scores:
  insight: {score: 4, why: "Selling agents' work data rather than the product is a non-obvious reading, still a HYPOTHESIS."}
  transferability: {score: 4, why: "The mechanism applies to technicians, administrative health and multilingual customer service."}
  space: {score: 4, why: "The two European marketplaces found sell content, not agent traces; search was limited, so not certain."}
  differentiation: {score: 3, why: "Language and GDPR are specific angles but need buyer proof."}
  feasibility: {score: 2, why: "A small team can build a connector, but building lab trust in three months is hard."}
  personal_fit: {score: null, why: "no profile"}
tam_hint: null
claims:
  - id: C1
    text: "Magma packages agent interaction data (traces, corrections, completed workflows) and licenses it to AI labs; connection described as read-only and encrypted, scoped to what the company approves; setup via a short form and 20-minute onboarding call; revenue share with no published percentage; no buyers or customers named; displays a 'Backed by Y Combinator' badge"
    label: FACT
    key_number: false
    sources:
      - {url: "https://magmahq.ai", title: "Magma home page", publisher: Magma, source_type: primary, published: 2026-10-31, accessed: 2026-10-31}
    single_source: true
    confidence: M
  - id: C2
    text: "AI labs have exhausted useful web data and pay for real examples of work with corrections; companies with agents have no channel today to sell such traces"
    label: HYPOTHESIS
    key_number: false
    sources: []
    single_source: false
    confidence: L
    falsifier: "5 labs or training teams say they do not buy external traces, or already have enough"
  - id: C3
    text: "Human Native AI (UK) is a marketplace for licensing data used to train AI, with a funding round reported in 2024"
    label: FACT
    key_number: false
    sources:
      - {url: "https://www.uktech.news/ai/human-native-ai-funding-20240604", title: "Human Native AI funding", publisher: UKTN, source_type: secondary, published: 2024-06-04, accessed: 2026-10-31}
    single_source: true
    confidence: M
    stale: true
  - id: C4
    text: "Trainspot was announced as an AI data marketplace on 28 October 2024"
    label: FACT
    key_number: false
    sources:
      - {url: "https://www.businesswire.com/news/home/20241028726844/en/Introducing-Trainspot-The-AI-Data-Marketplace-That-Works-for-Everyone", title: "Introducing Trainspot", publisher: Business Wire, source_type: secondary, published: 2024-10-28, accessed: 2026-10-31}
    single_source: true
    confidence: M
    stale: true
---
# Magma: Opportunity Card
WATCH: a sharp mechanism whose demand side is unproven; revisit when labs publicly buy agent-trace data or when a European vertical supplier signs.

## Open questions
- HQ, round and founders: YC company directory page.
- Actual buyers and prices: none on the site; ask at a demo or the founders.
- Other European agent-data players: two more queries.
