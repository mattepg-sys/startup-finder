# Scoring rubrics

All criteria are scored 1–5, where **5 is best for us**. There is **no weighted total**.
Every score is recorded as:
```yaml
R1: {score: 4, confidence: M, evidence: [C3, C7], rationale: "Spanish notarial e-filing (SIGNO) has no English API; incumbents are desktop-only"}
```
A score without evidence claim IDs is capped at 2 and gets confidence L.

## Aggregation (used by A5, A6, A7 and the orchestrator)
1. Per rubric: show the vector, the **floor** (min) and the **weakest criterion** by name.
2. Any criterion = 1 → `KILL_CANDIDATE: <criterion>`. The Red Team must attack it first.
3. Ordering of survivors: (a) fewest criteria ≤2 across all 19 → (b) highest floor → (c) the user at CP3.

---

## Investor metrics (A1). These are not 1–5 scores: raw values plus percentile within class
| Metric | Computation | Min n | Window |
|---|---|---|---|
| E1 Activity | count of pre-seed/seed/A rounds participated | 6 | last 12 months |
| E2 Earliness | share where round = company's first institutional round | 6 | last 24 months |
| E3 Graduation (shrunk) | (k + α)/(n + α + β); α = 10·p0, β = 10·(1−p0); p0 = vintage base rate (≈0.25 for 2020–21, ≈0.15 for 2022–23; verify) | 12 | seed deals in 2020–2023, next priced round within 24 months |
| E4 Conviction | share of rounds led or co-led | 6 | last 24 months |
| E5 Specialism | share of the top sector | 6 | last 24 months |
| E6 Independence | 1 − share of deals with any of the 3 most frequent co-investors | 6 | last 24 months |

**Rank within class** = median of the E1–E4 and E6 percentiles. E5 is descriptive only. Report the 80% interval for E3 (Beta posterior) and name the weakest metric.

---

## Replicability (A4)
| | 1 | 3 | 5 |
|---|---|---|---|
| **R1 Localisation moat** | Product is language- and regulation-agnostic; a US product works as-is | Some localisation (language, invoicing) but easy for the original to add | Local regulation, official integrations, language-heavy workflows or payment rails (Bizum, SEPA-specific, SDI e-invoicing in IT, DATEV in DE) make a local player structurally better |
| **R2 Original's EU entry threat** (inverse) | Original already in the EU or hiring there (job posts) | Has raised enough to expand; no EU signals yet | Original is US-regulated or US-workflow-locked; no EU signals; small round |
| **R3 Insight transfers** | The "secret" depends on US-specific structure (US healthcare billing, 401k, US tort system) | Partially transfers; needs a different buyer or channel | Same underlying pain exists in the target country, with evidence |
| **R4 Build feasibility (≤12 weeks, our team)** | Needs hardware, deep science or regulated core | MVP feasible with heavy integrations | Thin MVP feasible in ≤8 weeks with our stack |
| **R5 Regulatory cost to first revenue** (inverse) | Licence needed before any revenue (EMI, medical device class IIa+) | Compliance work (GDPR DPIA, sector certification) but can sell pilots | No licence; standard GDPR |

## Attractiveness (A4 drafts, A5 refines)
| | 1 | 3 | 5 |
|---|---|---|---|
| **A1 Bottom-up market** (count × ACV in the chosen country) | < €5M/yr serviceable | €5–50M | > €50M, with an evidenced count of target organisations |
| **A2 Pain urgency** | No evidence of spend or workaround | Workarounds visible (Excel, consultants) | Mandated deadline, fines, or visible spend on a worse solution |
| **A3 Willingness to pay** | No comparable pricing | Comparable tools priced, buyer budget unclear | Public prices of comparable local tools and a budget owner identified |
| **A4 Unit-economics proxy** | Services-heavy; gross margin < 40%; long onboarding | Mixed | Software margin; self-serve or short onboarding; ACV supports the sales motion |
| **A5 Expansion path** | Moat is country-only, with no adjacent market | 1 adjacent market with similar rules | ≥2 EU markets reachable with the same product + localisation |

## Competition intensity (A4; high = less intense)
| | 1 | 3 | 5 |
|---|---|---|---|
| **C1 Funded players in the exact wedge** (in the target country) | ≥4 | 1–3 | 0 (searched in the local language, query log attached) |
| **C2 Max funding of a local/EU player in the wedge** (inverse) | > €20M | €2–20M | < €2M or none |
| **C3 Incumbent strength** (inverse) | Incumbent with a modern product and distribution actively shipping in this wedge | Incumbent with a legacy product | Fragmented, or no incumbent |
| **C4 White-space clarity** | Can't state what we'd do differently | Differentiation on price or UX only | A specific segment, workflow or channel nobody serves, with evidence |

## Team fit (A5, from config/user_profile.md)
| | 1 | 3 | 5 |
|---|---|---|---|
| **T1 10 conversations in 2 weeks** | No network in the segment | Cold outreach with a clear list | Warm intros available (named network) |
| **T2 Tech fit** | Outside the co-founder's stack | Learnable in ≤4 weeks | Core stack |
| **T3 Language/presence** | No team member speaks the language | B2 level; remote | Native speaker, present in the country |
| **T4 Sales motion fit** | Enterprise field sales / public tenders | Inside sales to SMBs | Self-serve or founder-led to a reachable niche |
| **T5 Credentials** | Missing a licence or credential that is required to sell | Partner can provide it | None needed |

## Country selection (A4): ranks only the countries in run_config
For each allowed country:
- the moat drivers present (regulation, language, workflow, payments, incumbents)
- a bottom-up buyer count
- competitor density (C1/C2 for that country)
- our team presence (T3)
- cost to test (language, distance)

Recommend **one** country, with the runner-up and why it lost.
