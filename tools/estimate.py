#!/usr/bin/env python3
"""Print a time estimate for the next run, before it starts.
Usage: python3 tools/estimate.py [--profile quick|standard]
Uses the median of this user's own past runs (runs/*/timing.jsonl) when available, else defaults."""
import os, sys, json, glob, datetime, statistics
import yaml
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "run_config.yaml"), encoding="utf-8"))
prof = sys.argv[sys.argv.index("--profile") + 1] if "--profile" in sys.argv else cfg.get("active_profile", "quick")
deals = ((cfg.get("run_profiles") or {}).get(prof) or {}).get("deals_max", 10)
DEFAULT = {"onboarding": (1, 2), "preflight": (1, 3), "scouting": (8, 12), "lab": (4, 7), "report": (0.5, 1)}
YOU = {"onboarding", "preflight"}  # stages that may need the user (questions, PitchBook sign-in)
seen = {k: [] for k in DEFAULT}
for f in glob.glob(os.path.join(ROOT, "runs", "*", "timing.jsonl")):
    rows = []
    for l in open(f, encoding="utf-8"):
        try: rows.append(json.loads(l))
        except json.JSONDecodeError: pass
    ts = {r["stage"]: datetime.datetime.fromisoformat(r["ts"]) for r in rows if "ts" in r}
    def span(a, b, key):
        if a in ts and b in ts and ts[b] > ts[a]:
            seen[key].append((ts[b] - ts[a]).total_seconds() / 60)
    span("preflight_done", "scouting_done", "scouting")
    span("scouting_done", "lab_done", "lab")
    span("lab_done", "report_done", "report")
first_run = not os.path.exists(os.path.join(ROOT, "config", "user_profile.md"))
lo = hi = you = 0.0
print(f"Plan · profile '{prof}' · about {deals} startups")
for stage, (dlo, dhi) in DEFAULT.items():
    if stage == "onboarding" and not first_run:
        continue
    vals = seen.get(stage) or []
    if len(vals) >= 3:
        m = statistics.median(vals); a, b = m * 0.8, m * 1.25; src = f"your last {len(vals)} runs"
    else:
        a, b = dlo, dhi; src = "default"
    scale = deals / 10 if stage == "lab" else 1
    a, b = a * scale, b * scale
    lo += a; hi += b
    if stage in YOU: you += b
    a, b = max(a, 0.5), max(b, 1)
    print(f"  {stage:<11} {a:4.0f}–{b:<4.0f} min  ({src}){'  ← may need you' if stage in YOU else ''}")
print(f"Total ≈ {lo:.0f}–{hi:.0f} min · your time ≤ {you:.0f} min · you can leave it running after the start")
