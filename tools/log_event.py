#!/usr/bin/env python3
"""Append one event to logs/events.jsonl (append-only).
Usage: python3 tools/log_event.py --run RUN-20261006-01 --agent A3 --action write --path data/startups/acme-ai/02_analysis.md [--note "..."]"""
import argparse, json, hashlib, os, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--run", required=True); ap.add_argument("--agent", required=True)
ap.add_argument("--action", required=True, choices=["write", "revise", "checkpoint", "decision", "fail", "pitchbook_stop", "note"])
ap.add_argument("--path", default=""); ap.add_argument("--note", default="")
a = ap.parse_args()
sha = ""
if a.path:
    p = os.path.join(ROOT, a.path)
    if os.path.isfile(p):
        sha = hashlib.sha256(open(p, encoding="utf-8").read().encode("utf-8")).hexdigest()
ev = {"ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "run_id": a.run, "agent": a.agent,
      "action": a.action, "path": os.path.normpath(a.path) if a.path else "", "sha256": sha, "note": a.note}
os.makedirs(os.path.join(ROOT, "logs"), exist_ok=True)
with open(os.path.join(ROOT, "logs", "events.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps(ev, ensure_ascii=False) + "\n")
print(json.dumps(ev))
