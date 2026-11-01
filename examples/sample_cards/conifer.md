---
record_type: opportunity_card
id: OPP-conifer
startup_id: STU-conifer
run_id: SAMPLE
status: final
version: 1
language: en
company:
  name: Conifer
  website: https://conifer.build
  hq: "San Francisco, US"
  stage: accelerator
  round_date: null
  amount_usd: null
  backers: [{name: "Y Combinator", role: accelerator}]
  eu_present: false
one_liner: "Conifer is an inference gateway that routes each LLM request to the cheapest model that can still do the job, across 200+ models [C1]."
business_model: "Cloud tokens are billed at each model's own rate with no markup; own keys or local hardware are free. HYPOTHESIS: future revenue from team plans or a share of savings [C1, C2]."
maturity: accelerator
evidence_level: partial
label: TRANSFERABLE
label_reason: "A straight copy is weak in a crowded gateway market with European players already present, but least-cost routing as a mechanism is strong in other cost-opaque markets."
secret: {text: "HYPOTHESIS: choosing per request not only the model but also provider and caching turns token price into an optimisation variable; with no markup the gateway earns trust and gathers cost/quality data that improves routing [C1, C2].", claims: [C1, C2]}
europe_queries:
  - {q: "LLM router gateway Europe startup Eden AI Portkey OpenRouter alternative GDPR EU hosting", lang: en}
  - {q: "passerelle LLM routage modeles souveraine europeenne startup reduire couts IA", lang: fr}
europe_today:
  - {name: "Opper", country: "SE", website: "https://opper.ai/blog/best-european-ai-gateways", what_they_do: "One API for 700+ models with OpenAI-, Anthropic- and Gemini-compatible endpoints and EU routes; mentions an LLM Router feature", what_they_miss: "The article does not describe per-request cost optimisation or harness and cache selection", scale: "UNKNOWN", claims: [C3]}
  - {name: "Cortecs", country: "AT", website: "https://opper.ai/blog/best-european-ai-gateways", what_they_do: "Pay-per-use access to about 150 endpoints from 10+ providers on European infrastructure (vendor claims)", what_they_miss: "Focus is European residency, not dynamic cost routing", scale: "UNKNOWN", claims: [C3]}
  - {name: "Requesty", country: "GB", website: "https://opper.ai/blog/best-european-ai-gateways", what_they_do: "Routes to 600+ models from 30+ providers with EU endpoints on AWS Frankfurt; 5% markup on model cost (vendor claims)", what_they_miss: "A percentage markup grows with usage; cost-selection logic is not described", scale: "UNKNOWN", claims: [C3]}
  - {name: "Eden AI", country: "FR", website: "https://opper.ai/blog/best-european-ai-gateways", what_they_do: "Aggregator of LLMs plus speech, OCR and translation APIs, 500+ models (vendor claims)", what_they_miss: "Breadth across APIs; automatic per-request cost optimisation is not described", scale: "UNKNOWN", claims: [C3]}
angles:
  - {title: "Cost router with a GDPR-readable request log for SMEs and firms", for_whom: "Software houses and professional firms in Italy and Spain that send client data to LLMs and must document where it goes", why_gap: "European gateways sell EU residency; none found combines per-request savings with a log a non-technical privacy officer can read.", evidence: "Opper, Cortecs and Requesty are presented for EU residency, not cost optimisation [C3]. The gap is a HYPOTHESIS to verify.", claims: [C3]}
  - {title: "Savings-share billing for non-technical product teams", for_whom: "Agencies and SMEs using LLMs via no-code tools who only see the invoice", why_gap: "Conifer targets developers (Claude Desktop, Cursor, VS Code); the gateways found charge markups, not a share of savings.", evidence: "Conifer integrations are developer tools [C1]; Requesty applies a 5% markup [C3].", claims: [C1, C3]}
  - {title: "Local-hardware fallback for firms with sensitive data (health, legal)", for_whom: "Firms that cannot send data off-site but could use the cloud for non-sensitive tasks", why_gap: "Conifer allows local models through a llama-compatible endpoint but describes no rules for sensitive data in an EU context.", evidence: "Page lists local hardware as an option [C1].", claims: [C1]}
  - {title: "Task-specific router (invoice OCR, call transcription) in European languages", for_whom: "Products doing a single task in Italian, Spanish, German or French", why_gap: "Generic routers pick by price; quality per task in smaller languages needs local benchmarks no gateway describes.", evidence: "HYPOTHESIS: no per-language benchmark appears in the sources found [C2].", claims: [C2]}
transfers:
  - {sector: "Cloud services routing (compute, storage, CDN) by cost", how: "Same mechanism: pick on the fly the cheapest provider meeting a quality requirement", why_promising: "Cloud costs are variable and opaque, and small teams lack time to compare"}
  - {sector: "Payment and SMS API routing in Europe", how: "Choose the cheapest provider per country and channel across many aggregators", why_promising: "Tariffs differ per country and national rules apply; savings are measurable per message"}
  - {sector: "Energy purchasing for SMEs", how: "Route flexible consumption to the cheapest supplier or time band", why_promising: "Prices vary over time and small firms have no visibility"}
risks:
  - {risk: "The gateway market is crowded (OpenRouter, Portkey, European gateways) and providers can add their own routing or pricing; the edge may be easy to copy.", severity: high, claims: [C3]}
  - {risk: "No named customers on the site and no markup model: thin evidence on traction and on how it earns revenue.", severity: medium, claims: [C1]}
questions:
  - "Who around you pays a monthly LLM bill and does not know which requests cost the most?"
  - "What would an Italian privacy officer want to see in a log of requests sent to an LLM?"
  - "If the router earned a share of savings instead of a markup, who would trust it more?"
  - "In which Italian-language task does a small model suffice, and how would you prove it in a day?"
one_week_test: {what: "10 interviews with developers or founders in Italy/Spain whose products use LLMs: ask for the monthly bill and whether they know cost per feature", signal: ">=4 of 10 pay over 500 EUR per month without knowing cost per feature; >=3 would accept a one-week log test", cost_eur: 0}
your_edge: null
scores:
  insight: {score: 3, why: "Routing harness and cache as well as model is less obvious than model-only routing; the effect remains a HYPOTHESIS."}
  transferability: {score: 4, why: "Best-provider-on-the-fly applies to cloud, payments and energy."}
  space: {score: 2, why: "Four European gateways already exist, plus global OpenRouter and Portkey."}
  differentiation: {score: 3, why: "Readable compliance and per-task routing in a language are specific but unvalidated."}
  feasibility: {score: 3, why: "A proxy with rules for one task is doable in 3 months; covering 200 models is not."}
  personal_fit: {score: null, why: "no profile"}
tam_hint: null
claims:
  - id: C1
    text: "Conifer is an inference gateway: 200+ models behind one endpoint, own provider keys or local models through a llama-compatible endpoint, routes each query to the cheapest model that can handle it; cloud tokens at each model's rate with no markup; integrations with Claude Desktop, Codex Desktop, Cursor, VS Code, Zed and others; no customers named on the site. The YC directory lists Conifer (San Francisco, 4 employees) as 'least cost routing system to reduce 70%+ token spend'"
    label: FACT
    key_number: false
    sources:
      - {url: "https://conifer.build", title: "Conifer home page", publisher: Conifer, source_type: primary, published: 2026-10-31, accessed: 2026-10-31}
      - {url: "https://www.ycombinator.com/companies/conifer", title: "Conifer at Y Combinator", publisher: Y Combinator, source_type: primary, published: 2026-10-31, accessed: 2026-10-31}
    single_source: false
    confidence: M
  - id: C2
    text: "The edge is joint optimisation of harness, model, provider and cache per request, with cost/quality data that improves routing over time"
    label: HYPOTHESIS
    key_number: false
    sources: []
    single_source: false
    confidence: L
    falsifier: "A public benchmark shows a single-model router reaches the same cost per task, or customers do not lower their bill with Conifer"
  - id: C3
    text: "Opper article (5 Aug 2026) on European AI gateways: Opper (SE, 700+ models, LLM Router feature), Cortecs (AT, about 150 endpoints, European infrastructure), Requesty (GB, 600+ models, EU endpoints on AWS Frankfurt, 5% markup), Orq.ai (NL), Eden AI (FR, 500+ models); figures are vendor-stated; the article does not describe per-request cost optimisation"
    label: FACT
    key_number: false
    sources:
      - {url: "https://opper.ai/blog/best-european-ai-gateways", title: "The 5 best European AI gateways in 2026", publisher: Opper, source_type: primary, published: 2026-08-05, accessed: 2026-10-31}
    single_source: true
    confidence: M
---
# Conifer: Opportunity Card
TRANSFERABLE: the mechanism is strong but the gateway market is crowded; the roads are readable compliance, per-task routing in a language, savings-share billing, and the same idea in other cost-opaque markets.

## Open questions
- Conifer team and revenue model: contact page and founder posts.
- Whether Opper's LLM Router optimises for cost: Opper documentation.
- Real pricing and usage of European gateways: demos or pricing pages.
