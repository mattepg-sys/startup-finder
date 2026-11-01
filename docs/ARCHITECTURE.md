# Architecture (v0.1)

```
you ──► Orchestrator (00) ── onboarding · plan + time estimate · progress · report
            │
            ├─► Scout (01) ── PitchBook (first-cheque investors) + YC / accelerator feeds
            │        └─► tools/check_queue.py ── gate: description, website, stage, already-seen
            │                                    → selects ~10 by stage tier → source → signal
            ├─► Opportunity Lab (02) × N in parallel ── one card per startup
            ├─► tools/build_report.py ── runs/<run>/report.html (no AI, no tokens)
            └─► Retrospective (08, lite) ── lessons → config/learnings.md
```

## Folders
| Path | What | In git? |
|---|---|---|
| `agents/` | prompts for each agent; `legacy/` holds the deep-dive chain | yes |
| `config/` | run settings, evidence standard, learnings, starter investors, profile example | yes (except `user_profile.md`) |
| `templates/` | card and report templates | yes |
| `tools/` | validator, queue gate, report builder, estimate, selftest, sealing | yes |
| `data/` | your startups, cards and investors | **no** |
| `runs/` | one folder per run: queue, timings, logs, report | **no** |

## Design rules
- **Early stage only:** angel, pre-seed and accelerator first; young seed to fill; never Series A+.
- **Evidence:** every key fact has a URL and a date; estimates and hypotheses are labelled. The validator enforces it.
- **Inspiration over gatekeeping:** labels guide, they don't veto.
- **History is append-only:** finished runs are sealed (`tools/seal_run.py`), and the validator fails if a sealed file changes.
- **Learning loop:** `config/learnings.md` is read by every agent at Step 0 and updated only through `tools/learnings_append.py`.
- **Budget:** about 200 web searches per Claude turn, shared by all agents, so a run caps searches per deal.
