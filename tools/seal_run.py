#!/usr/bin/env python3
"""Seal a closed run so its history can never change silently.
Usage: python3 tools/seal_run.py RUN-ID
Writes runs/RUN-ID/SEAL.json: sha256 of every file in runs/RUN-ID/ and of every data/ file written in that run
(per logs/events.jsonl, last write wins). The validator checks seals on every run: any mismatch is an ERROR.
To change sealed content, write a new version (.v2.md with supersedes:) in the current run, never edit."""
import sys, os, json, hashlib, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
run = sys.argv[1]
rdir = os.path.join(ROOT, "runs", run)
if not os.path.isdir(rdir): sys.exit(f"no such run {run}")
seal_path = os.path.join(rdir, "SEAL.json")
if os.path.exists(seal_path): sys.exit(f"{run} already sealed")
files = {}
for d, _, fs in os.walk(rdir):
    for f in fs:
        p = os.path.join(d, f)
        if f != "SEAL.json" and not f.endswith(".tmp"):
            files[os.path.relpath(p, ROOT)] = sha(p)
ev = os.path.join(ROOT, "logs", "events.jsonl")
for line in (open(ev, encoding="utf-8") if os.path.exists(ev) else []):
    try: e = json.loads(line)
    except json.JSONDecodeError: continue
    pth = e.get("path") or ""
    if e.get("run_id") == run and pth.startswith("data") and os.path.isfile(os.path.join(ROOT, pth)):
        files[os.path.normpath(pth)] = sha(os.path.join(ROOT, pth))
json.dump({"run_id": run, "sealed_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "files": files}, open(seal_path, "w"), indent=1)
print(f"sealed {run}: {len(files)} files")
