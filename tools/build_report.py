#!/usr/bin/env python3
"""Build a self-contained HTML report for a run from its Opportunity Cards.
Usage: python3 tools/build_report.py RUN-ID [--lang it|en]
Writes runs/<run>/report.html (full, opens offline in any browser) and
runs/<run>/report.artifact.html (same page without the document skeleton, for claude.ai Artifacts).
No AI, no network: it only reads the files the agents wrote."""
import sys, os, json, glob, html, datetime, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
run = sys.argv[1]
SAMPLE = run == "--sample"   # python3 tools/build_report.py --sample  → examples/sample_report.html from examples/sample_cards/
lang = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else None
cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "run_config.yaml"), encoding="utf-8"))
prof = os.path.join(ROOT, "config", "user_profile.md")
if not lang and os.path.exists(prof):
    pf = yaml.safe_load(open(prof, encoding="utf-8").read().split("\n---", 1)[0][3:]) or {}
    lang = pf.get("report_language") or None
lang = lang or cfg.get("report_language", "en")
if SAMPLE: lang = "en"
rdir = os.path.join(ROOT, "examples") if SAMPLE else os.path.join(ROOT, "runs", run)
if SAMPLE: run = "SAMPLE"

def fm_of(path):
    t = open(path, encoding="utf-8").read()
    if not t.startswith("---"): return None
    return yaml.safe_load(t.split("\n---", 1)[0][3:]) or {}

def jsonable(o):
    if isinstance(o, (datetime.date, datetime.datetime)): return o.isoformat()
    if isinstance(o, dict): return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, list): return [jsonable(v) for v in o]
    return o

cards = []
CARD_GLOB = os.path.join(ROOT, "examples", "sample_cards", "*.md") if SAMPLE else os.path.join(ROOT, "data", "startups", "*", "opportunity*.md")
for p in sorted(glob.glob(CARD_GLOB)):
    fm = fm_of(p)
    if not fm or fm.get("record_type") != "opportunity_card" or fm.get("run_id") != run or fm.get("status") == "template":
        continue
    srcs, seen = [], set()
    for c in fm.get("claims") or []:
        for s in c.get("sources") or []:
            u = s.get("url")
            if u and u not in seen and u.startswith("http") and "pitchbook.com" not in u:
                seen.add(u); srcs.append({"url": u, "title": s.get("title") or u, "label": c.get("label"), "date": str(s.get("published") or "")})
            elif u and "pitchbook.com" in u and "PitchBook" not in seen:
                seen.add("PitchBook"); srcs.append({"url": "", "title": "PitchBook (licensed, not linked)", "label": c.get("label"), "date": str(s.get("published") or "")})
    fm["_sources"] = srcs
    fm["_slug"] = os.path.splitext(os.path.basename(p))[0] if SAMPLE else os.path.basename(os.path.dirname(p))
    cards.append(jsonable(fm))

queue = []
qp = os.path.join(rdir, "queue_scored.json")
if os.path.exists(qp):
    queue = json.load(open(qp, encoding="utf-8"))
sig = {q["slug"]: q.get("deal_signal") for q in queue}
queue = [q for q in queue if q.get("selected", True)]
for c in cards:
    c["_signal"] = sig.get(c["_slug"])
timing = []
tp = os.path.join(rdir, "timing.jsonl")
if os.path.exists(tp):
    timing = [json.loads(l) for l in open(tp, encoding="utf-8") if l.strip()]
minutes = None
if len(timing) >= 2:
    t0 = datetime.datetime.fromisoformat(timing[0]["ts"]); t1 = datetime.datetime.fromisoformat(timing[-1]["ts"])
    minutes = round((t1 - t0).total_seconds() / 60, 1)
people = set()
for q in queue:
    for b in q.get("backers") or []:
        people.add(b.get("person_id"))
meta = {"run": run, "generated": datetime.date.today().isoformat(), "deals": len(queue) or len(cards),
        "cards": len(cards), "people": len(people), "minutes": minutes, "lang": lang}
DATA = json.dumps({"meta": meta, "cards": cards}, ensure_ascii=False).replace("</", "<\\/")

TEMPLATE = open(os.path.join(ROOT, "templates", "report_template.html"), encoding="utf-8").read()
body = TEMPLATE.replace("/*__DATA__*/null", DATA).replace("__RUN__", html.escape(run))
if SAMPLE:
    full = ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n%s\n</body>\n</html>\n') % (lang, body)
    open(os.path.join(rdir, "sample_report.html"), "w", encoding="utf-8").write(full)
    print(f"sample report: examples/sample_report.html ({len(cards)} cards)"); sys.exit(0)
open(os.path.join(rdir, "report.artifact.html"), "w", encoding="utf-8").write(body)
full = ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n%s\n</body>\n</html>\n') % (lang, body)
open(os.path.join(rdir, "report.html"), "w", encoding="utf-8").write(full)
import shutil
os.makedirs(os.path.join(rdir, "_export"), exist_ok=True)
stamp = datetime.datetime.now().strftime("%H%M%S")
shutil.copyfile(os.path.join(rdir, "report.artifact.html"), os.path.join(rdir, "_export", f"artifact-{stamp}.html"))  # fresh copy: cloud-synced folders can block staging of rewritten files
print(f"report: runs/{run}/report.html  ({len(cards)} cards, {meta['deals']} deals, lang={lang})")
