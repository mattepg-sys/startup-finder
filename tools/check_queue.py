#!/usr/bin/env python3
"""Gate + scorer for runs/<run>/deal_queue.jsonl (append-only; the last line per slug wins).
Usage: python3 tools/check_queue.py RUN-ID [--log]
- ERROR if a queued deal lacks a description, a website (URL or 'stealth'), a PitchBook company URL,
  or mapping verification (name + round cross-checked on the company page). Such deals cannot be triaged.
- Computes deal_signal deterministically from config/run_config.yaml signal_weights and the PER- person_class,
  and writes runs/<run>/queue_scored.json (sorted by signal; only valid deals)."""
import sys, os, json, re, datetime
import yaml
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
run = sys.argv[1]; log = "--log" in sys.argv
cfg = yaml.safe_load(open(os.path.join(ROOT, "config", "run_config.yaml"), encoding="utf-8"))
W = cfg["signal_weights"]
EU = {"DE","FR","ES","IT","NL","SE","DK","FI","AT","BE","PT","IE","PL","GB","UK","CH","NO","LU","CZ","EE","LT","LV","GR","HU","RO","SK","SI","HR","BG","CY","MT"}
def person_class(pid):
    import glob
    cands = sorted(glob.glob(os.path.join(ROOT, "runs", run, "people", pid + "*.md"))) or \
            sorted(glob.glob(os.path.join(ROOT, "data", "investors", pid + "*.md")))
    if not cands: return None
    txt = open(cands[-1], encoding="utf-8").read()   # latest version (.v2 sorts after .md? ensure)
    vers = [c for c in cands if re.search(r"\.v\d+\.md$", c)]
    if vers: txt = open(sorted(vers, key=lambda x: int(re.search(r"\.v(\d+)\.md$", x).group(1)))[-1], encoding="utf-8").read()
    m = re.search(r"^person_class:\s*(\w+)", txt, re.M)
    return m.group(1) if m else None
rows = {}
for line in open(os.path.join(ROOT, "runs", run, "deal_queue.jsonl"), encoding="utf-8"):
    line = line.strip()
    if not line: continue
    d = json.loads(line)
    key = d.get("slug") or re.sub(r"[^a-z0-9]+", "-", d.get("company", "").lower()).strip("-")
    rows[key] = {**rows.get(key, {}), **d}
EF = cfg.get("early_stage_focus") or {}
EXCL = set(EF.get("exclude_stages") or [])
RELAX = set(EF.get("relaxed_verification") or [])
TIER = {st: int(t) for t, sts in (EF.get("priority_tiers") or {}).items() for st in sts}
def stage_of(d):
    st = str(d.get("stage") or "").lower().replace("-", "_").replace(" ", "_")
    if st == "seed":
        fy = d.get("founded"); tr = d.get("total_raised_usd")
        try:
            young = fy and int(str(fy)[:4]) >= datetime.date.today().year - 2 and (tr is None or float(tr) <= 5_000_000)
        except ValueError:
            young = False
        return "seed_young" if young else "seed"
    return st
E, ok, excluded = [], [], []
# never re-analyse startups that earlier runs already covered (snapshot taken at run start)
exf = os.path.join(ROOT, "runs", run, "exclude_slugs.txt")
ALREADY = {x.strip() for x in open(exf, encoding="utf-8").read().split(",") if x.strip()} if os.path.exists(exf) else set()
for slug, d in rows.items():
    if d.get("status") in ("rejected", "rejected_misattributed", "superseded"): continue
    st = stage_of(d)
    if slug in ALREADY:
        excluded.append(f"{slug} (already analysed in an earlier run)"); continue
    if st in EXCL:
        excluded.append(f"{slug} ({st})"); continue
    relaxed = st in RELAX
    from_feed = str(d.get("source", "pitchbook")) != "pitchbook"
    errs = []
    ol = str(d.get("one_line", "")).strip()
    if not ol or ol.upper().startswith("UNKNOWN"): errs.append("missing description (100% description rule)")
    w = str(d.get("website", ""))
    if not (w.startswith("http") or w.lower() == "stealth"): errs.append("website must be URL or 'stealth'")
    if not from_feed and not str(d.get("pitchbook_company_url", "")).startswith("http"): errs.append("missing pitchbook_company_url")
    mv = d.get("mapping_verified") or {}
    if not mv.get("name_match") or (not relaxed and not mv.get("round_match")):
        errs.append("mapping not verified on company page (name" + ("" if relaxed else " + round") + ")")
    if str(d.get("hq_country", "")).upper() in EU: errs.append("European HQ: outside sourcing geography")
    backers = d.get("backers") or []
    if not backers and not from_feed: errs.append("no backers")
    if errs:
        E += [f"{slug}: {e}" for e in errs]; continue
    s = 0.0
    for b in backers:
        pc = person_class(b["person_id"]) or "seed_partner"
        s += W.get(pc, 1.0) * W["role_multiplier"].get(b.get("role", "lead_partner"), 1.0)
    s *= W["earliness_bonus"].get(d.get("stage"), 1.0)
    if d.get("press_found") is False: s *= W["no_press_bonus"]
    if d.get("eu_present") is True: s *= W.get("eu_present_multiplier", 1.0)
    if from_feed and not backers: s = 1.0
    d["deal_signal"] = round(s, 2); d["slug"] = slug
    d["stage_norm"] = st; d["priority_tier"] = TIER.get(st, 3)
    ok.append(d)
# selection priority: earliest stage tier first, then investor signal (card scores are separate)
SRC = {src: i for i, src in enumerate(EF.get("source_priority") or ["pitchbook"])}
srank = lambda d: SRC.get(str(d.get("source", "pitchbook")), 99)
ok.sort(key=lambda x: (x["priority_tier"], srank(x), -x["deal_signal"]))
target = int(EF.get("target_deals") or len(ok))
sel = ok[:target]
# PitchBook quota: swap feed deals out for PitchBook deals (tier <= 2) until the share is met
need = round(float(EF.get("target_pitchbook_share") or 0) * target)
pb_rest = [d for d in ok[target:] if srank(d) == 0 and d["priority_tier"] <= 2]
while sum(1 for d in sel if srank(d) == 0) < need and pb_rest:
    feeds = [d for d in sel if srank(d) != 0]
    if not feeds: break
    sel.remove(feeds[-1]); sel.append(pb_rest.pop(0))
ids = {id(d) for d in sel}
for d in ok: d["selected"] = id(d) in ids
ok.sort(key=lambda x: (not x["selected"], x["priority_tier"], srank(x), -x["deal_signal"]))
json.dump(ok, open(os.path.join(ROOT, "runs", run, "queue_scored.json"), "w"), indent=1)
for e in E: print("ERROR", e)
t1 = sum(1 for d in ok if d["selected"] and d["priority_tier"] == 1)
pbn = sum(1 for d in ok if d["selected"] and str(d.get("source", "pitchbook")) == "pitchbook")
print(f"valid deals: {len(ok)} | selected: {min(target, len(ok))} (tier-1: {t1}, PitchBook: {pbn}) | rejected by gate: {len({e.split(':')[0] for e in E})} | excluded stage: {len(excluded)}")
for d in ok[:40]: print(f'{"*" if d["selected"] else " "} T{d["priority_tier"]} {d["deal_signal"]:5}  {d["slug"]:26} {d["stage_norm"][:11]:11} {d.get("one_line","")[:60]}')
for x in excluded: print("EXCLUDED", x)
if log:
    with open(os.path.join(ROOT, "logs", "validation.jsonl"), "a", encoding="utf-8") as f:
        ts = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        for e in E:
            f.write(json.dumps({"ts": ts, "run_id": run, "agent": "A1", "level": "ERROR", "path": f"runs/{run}/deal_queue.jsonl",
                                "pattern": re.sub(r"^[^:]+: ", "", e), "message": e}) + "\n")
sys.exit(1 if E else 0)
