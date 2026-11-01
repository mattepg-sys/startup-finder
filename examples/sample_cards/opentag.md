---
record_type: opportunity_card
id: OPP-opentag
startup_id: STU-opentag
run_id: SAMPLE
status: final
version: 1
language: en
company:
  name: OpenTag
  website: https://tryopentag.com
  hq: "UNKNOWN (site names only the copyright holder Open Curiosity, Inc.)"
  stage: accelerator
  round_date: null
  amount_usd: null
  backers: [{name: "Y Combinator", role: accelerator}]
  eu_present: false
one_liner: "OpenTag is an AI teammate inside Slack that answers from company knowledge, runs tasks across 50+ integrations and automates recurring work [C1]."
business_model: "HYPOTHESIS: subscription per workspace or seat plus model usage; the site links to a pricing page but shows no figures, and offers free sign-up [C1, C2]."
maturity: accelerator
evidence_level: partial
label: DIFFERENTIABLE
label_reason: "European players exist (Dust, Langdock) and are GDPR-positioned, but they leave open Microsoft Teams shops, regulated small firms and local back-office tools."
secret: {text: "HYPOTHESIS: it lives where the work already happens (the Slack channel), inherits the requester's permissions, asks for human approval on consequential actions, and routes across 40+ models to cut cost per task, so margins hold even with many small tasks [C1, C2].", claims: [C1, C2]}
europe_queries:
  - {q: "Dust Langdock AI agents Slack Europe enterprise assistant", lang: en}
  - {q: "assistente AI aziendale Slack Teams agenti PMI italiane", lang: it}
europe_today:
  - {name: "Dust", country: "FR", website: "https://dust.tt", what_they_do: "Custom AI assistants connected to Notion, Drive, Intercom and Slack, mentionable in Slack; TechCrunch names Alan, Qonto, Pennylane, PayFit as customers", what_they_miss: "Aimed at mid-size French tech scale-ups; no sign of an offer for small Italian or Spanish firms with local invoicing or payroll tools", scale: "Series A led by Sequoia (2024)", claims: [C3]}
  - {name: "Langdock", country: "DE", website: "https://www.langdock.com", what_they_do: "Company-wide AI platform: chat, agents, workflows, integrations and API; claims GDPR compliance, EU deployment, ISO 27001 and SOC 2 Type II", what_they_miss: "Sold as an organisation-wide rollout with its own chat interface, not as a teammate living in the Slack channel with delegated tasks", scale: "UNKNOWN", claims: [C4]}
  - {name: "Slack native agents (Agentforce)", country: "US", website: "https://slack.com/intl/it-it/ai-agents", what_they_do: "Slack itself offers AI agents, with Italian-language pages", what_they_miss: "Tied to the Salesforce ecosystem; not neutral across models and third-party tools", scale: "UNKNOWN", claims: [C5]}
angles:
  - {title: "AI teammate for Italian accounting and payroll practices", for_whom: "Practices of 5-30 people that talk to clients over messaging channels and live by Italian tax deadlines", why_gap: "Dust and Langdock are horizontal; no player found knows F24 deadlines or e-invoicing.", evidence: "Dust cites tech scale-ups as customers, not professional practices [C3]. That nobody serves practices is a HYPOTHESIS to test with 10 calls.", claims: [C3]}
  - {title: "Microsoft Teams version with EU data handling", for_whom: "SMEs and public bodies in Italy, Spain and Germany that run Teams, not Slack", why_gap: "OpenTag lists Teams only as coming soon, and works only in Slack today.", evidence: "Teams support marked coming soon [C1].", claims: [C1]}
  - {title: "Audit-ready approvals for regulated small firms (health, law, local banks)", for_whom: "Compliance teams that cannot delegate actions without an audit trail", why_gap: "OpenTag has approvals and SOC 2 Type I, but data residency and GDPR logging are not stated for European regulated buyers.", evidence: "SOC 2 Type I completed, Type II in progress; no residency statement on the page [C1].", claims: [C1]}
  - {title: "Pricing per solved task instead of per seat", for_whom: "Very small firms with few users but many repetitive requests", why_gap: "Per-seat pricing penalises tiny teams; OpenTag's 70% saving is a stated target, not a customer average.", evidence: "Page presents the cost reduction as a target [C1].", claims: [C1]}
transfers:
  - {sector: "Medical practices on WhatsApp Business", how: "A teammate in the channel staff already use, with role-based permissions and approval before anything goes to a patient", why_promising: "Staff live in messaging and lose time on repetitive tasks; health-data rules favour a local deployment"}
  - {sector: "Construction firms with WhatsApp groups", how: "An assistant in the group that fills daily reports, material orders and progress updates from photos and voice notes", why_promising: "Work flows through photos and voice notes with no archive; a wiki built from conversations fixes handovers"}
  - {sector: "Real-estate agencies on Teams or WhatsApp", how: "A teammate that updates the CRM, prepares listing sheets and schedules viewings", why_promising: "Many repeated steps between portals and local CRMs"}
risks:
  - {risk: "Slack and large vendors (Salesforce, Microsoft) ship native agents, which can squeeze room for a neutral third party.", severity: high, claims: [C5]}
  - {risk: "Thin evidence on pricing, revenue and retention; the named customers are largely startups from the same ecosystem and were not measured here.", severity: medium, claims: [C1]}
questions:
  - "Which repetitive chat-based task does someone you know in a small firm or practice still do by hand every week?"
  - "Who around you runs Teams or WhatsApp rather than Slack, and what would make them delegate a task to an AI?"
  - "What action should an AI teammate never take without approval inside a regulated Italian company?"
  - "Which local back-office tool (invoicing, payroll, CRM) does no AI assistant connect to yet?"
one_week_test: {what: "10 interviews with owners of professional practices or SMEs in one city: show 3 recurring tasks and ask which they would hand to an AI teammate in the channel they already use", signal: ">=4 of 10 name a weekly repeated task and say they would pay 50 EUR per month", cost_eur: 0}
your_edge: null
scores:
  insight: {score: 2, why: "An AI teammate in Slack is a common pattern; the less obvious part is inherited permissions plus approval."}
  transferability: {score: 4, why: "The pattern fits any messaging channel and any sector with repetitive tasks."}
  space: {score: 3, why: "Dust and Langdock hold the horizontal European space; channels and local sectors remain."}
  differentiation: {score: 3, why: "The practices and Teams angles are concrete but unvalidated."}
  feasibility: {score: 3, why: "One channel and one sector is doable in 3 months on third-party APIs; broad integration is not."}
  personal_fit: {score: null, why: "no profile"}
tam_hint: null
claims:
  - id: C1
    text: "OpenTag is an AI teammate for Slack: answers from company knowledge, runs tasks from chat, schedules automations, limits each request to the requester's permissions, asks approval for consequential actions, builds a company wiki; 50+ integrations; routes across 40+ models with a stated target of up to 70% lower cost per task; Teams support coming soon; SOC 2 Type I completed, Type II in progress; no prices shown; named customers include Thunder Compute, Audun, Conifer, Rovi Health, Hi Energy AI, Context.dev, Reclaim Protocol, 28 ROW, cfo.ai; says it is backed by Y Combinator; HQ not stated"
    label: FACT
    key_number: false
    sources:
      - {url: "https://tryopentag.com", title: "OpenTag home page", publisher: OpenTag, source_type: primary, published: 2026-10-31, accessed: 2026-10-31}
    single_source: true
    confidence: M
  - id: C2
    text: "The edge is living in the channel where work happens, with inherited permissions and human approval, and lower average cost per task through model routing"
    label: HYPOTHESIS
    key_number: false
    sources: []
    single_source: false
    confidence: L
    falsifier: "Customers renew without routing or permissions mattering to the decision, or renewals depend only on model quality"
  - id: C3
    text: "Dust is a French startup: AI assistants over internal data (Notion, Drive, Intercom, Slack), mentionable in Slack; Series A led by Sequoia; customers named by TechCrunch include Watershed, Alan, Qonto, Pennylane, PayFit"
    label: FACT
    key_number: false
    sources:
      - {url: "https://techcrunch.com/2024/06/27/dust-grabs-another-16-million-for-its-enterprise-ai-assistants-connected-to-internal-data", title: "Dust grabs another $16M for its enterprise AI assistants", publisher: TechCrunch, source_type: secondary, published: 2024-06-27, accessed: 2026-10-31}
    single_source: true
    confidence: M
    stale: true
  - id: C4
    text: "Langdock offers an organisation-wide AI platform (Chat, Workflows, Agents, Integrations, API, multiple models); site claims GDPR compliance, EU deployment, ISO 27001 and SOC 2 Type II, and lists a Berlin address for Langdock GmbH"
    label: FACT
    key_number: false
    sources:
      - {url: "https://www.langdock.com", title: "Langdock home page", publisher: Langdock, source_type: primary, published: 2026-10-31, accessed: 2026-10-31}
    single_source: true
    confidence: M
  - id: C5
    text: "Slack offers native AI agents (Agentforce) with Italian-language pages"
    label: FACT
    key_number: false
    sources:
      - {url: "https://slack.com/intl/it-it/ai-agents", title: "Slack AI agents", publisher: Slack, source_type: primary, published: 2026-10-31, accessed: 2026-10-31}
    single_source: true
    confidence: M
---
# OpenTag: Opportunity Card
DIFFERENTIABLE: the pattern is known and Dust/Langdock serve it in Europe; the open roads are regulated Italian practices, Teams and per-task pricing.

## Open questions
- OpenTag HQ, pricing and data residency: check the pricing page and trust center.
- Slack share among SMEs in ES/IT/DACH: Eurostat or sector surveys.
- Langdock's current scale: company announcement or press.
