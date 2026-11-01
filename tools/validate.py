#!/usr/bin/env python3
"""Startup Finder validator: schema + evidence + banned-pattern checks.
Usage: python3 tools/validate.py [path ...]   (default: data templates)
Exit code 1 if any ERROR. Run from the 'startup finder' folder."""
import sys, os, re, json, hashlib, datetime
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = {
    "investor": ["id", "name", "investor_class", "hq_country", "website", "status", "last_refreshed", "metrics", "weakest_metric", "claims"],
    "startup_source": ["id", "name", "website", "domain", "hq_country", "status", "found_via", "round", "first_signal_date", "signal_type", "one_line", "claims"],
    "triage": ["id", "startup_id", "status", "what_it_does", "customer", "secret_hypothesis", "pan_eu_tam", "eu_knockout", "outcome", "outcome_reason", "upside", "diagnostic", "red_flag", "claims"],
    "analysis": ["id", "startup_id", "status", "classification", "secret", "lenses", "observable_before_round", "bear_case", "traction_signals", "claims"],
    "europe": ["id", "startup_id", "status", "sector_lens", "scores", "floors", "weakest", "competitors", "queries_log", "white_space", "country_ranking", "recommended_country", "claims"],
    "country": ["id", "country", "sector", "status", "valid_until", "moat_drivers", "buyer_count", "claims"],
    "proposal": ["id", "startup_id", "status", "country", "proposal_type", "wedge", "icp", "pricing_hypothesis", "sizing", "team_fit", "gtm_90d", "first_10_customers", "two_week_test", "kill_criteria", "assumptions_ranked", "ip_check", "rubric_summary", "claims"],
    "redteam": ["id", "idea_id", "status", "verdict", "kill_arguments", "graveyard", "original_eu_expansion_check", "rescore", "what_would_change_my_mind", "searches_run", "claims"],
    "memo": ["id", "idea_id", "status", "verdict", "verdict_source", "based_on"],
    "opportunity_card": ["id", "startup_id", "run_id", "status", "company", "one_liner", "label", "label_reason", "secret", "europe_queries", "europe_today", "angles", "transfers", "risks", "questions", "one_week_test", "scores", "claims"],
    "investor_person": ["id", "name", "role", "firm", "firm_id", "person_class", "home_market", "pitchbook_profile", "status", "last_refreshed", "footprint", "metrics", "weakest_metric", "recent_deals", "claims"],
    "team_profile": ["status"],
    "learnings": ["version", "last_updated", "max_active_entries"],
}
LENSES = ["insight", "wedge", "distribution", "timing", "team", "unfair_advantage"]
BANNED = ["strong team", "huge market", "massive market", "ai-powered", "first-mover advantage", "first mover advantage",
          "great product", "passionate founders", "disruptive", "game-changer", "game changer", "seamless", "revolutionary",
          "best-in-class", "world-class", "currently leading", "recently raised"]
TOPDOWN = [re.compile(r"\b\d+(\.\d+)?\s?%\s+of\s+(an?|the)\s+[^.\n]{0,40}\bmarket", re.I),
           re.compile(r"\bcapture\s+(just\s+|only\s+)?\d+(\.\d+)?\s?%", re.I)]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<![\w/.-])\+?\d[\d \-]{8,}\d(?![\w/.-])")
CLAIM_REF = re.compile(r"\[(C\d+)\]")
LABELS = {"FACT", "ESTIMATE", "HYPOTHESIS"}
SRC_TYPES = {"primary", "secondary", "pitchbook", "aggregator"}
SCORE_KEYS = {"R1","R2","R3","R4","R5","A1","A2","A3","A4","A5","C1","C2","C3","C4","T1","T2","T3","T4","T5"}

def load_cfg():
    try:
        return yaml.safe_load(open(os.path.join(ROOT, "config", "run_config.yaml"), encoding="utf-8"))
    except Exception:
        return {}

def split_fm(text):
    if not text.startswith("---"):
        return None, text
    parts = text.split("\n---", 2)
    if len(parts) < 2:
        return None, text
    fm = parts[0][3:]
    body = parts[1].split("\n", 1)[1] if "\n" in parts[1] else ""
    return fm, body

def parse_date(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v if isinstance(v, datetime.date) else v.date()
    if isinstance(v, str):
        for fmt in ("%Y-%m-%d", "%Y-%m"):
            try:
                return datetime.datetime.strptime(v, fmt).date()
            except ValueError:
                pass
    return None

def logged_hashes():
    h = {}
    p = os.path.join(ROOT, "logs", "events.jsonl")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            try:
                e = json.loads(line)
                if e.get("path") and e.get("sha256"):
                    h[os.path.normpath(e["path"])] = e["sha256"]
            except json.JSONDecodeError:
                pass
    return h

def walk_scores(obj):
    """yield (key, scoredict) for any R/A/C/T score dicts anywhere in front-matter"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in SCORE_KEYS and isinstance(v, dict) and "score" in v:
                yield k, v
            else:
                yield from walk_scores(v)
    elif isinstance(obj, list):
        for x in obj:
            yield from walk_scores(x)

def check_learnings(rel, fm, body):
    errs, warns = [], []
    for h in ("## Agent Rules & Self-Corrections", "## User Preferences & Feedback", "## Kill Patterns (Red Team)"):
        if h not in body:
            errs.append(f"{rel}: missing section '{h}'")
    if "## Agent Rules & Self-Corrections" in body:
        body = body[body.index("## Agent Rules & Self-Corrections"):]  # skip the format example in the preamble
    ids = re.findall(r"^### (L-(?:RULE|PREF|KILL)-\d{3}) · ", body, re.M)
    for d in {i for i in ids if ids.count(i) > 1}:
        errs.append(f"{rel}: duplicate entry id {d}")
    blocks = re.split(r"(?=^### L-)", body, flags=re.M)[1:]
    for b in blocks:
        eid = b.split(" ")[1]
        for f in ("Rule", "Why", "Evidence", "Applies to", "Seen", "Status"):
            if f"- **{f}:**" not in b:
                errs.append(f"{rel}: {eid} missing '{f}'")
        m = re.search(r"- \*\*Status:\*\* (\w+)", b)
        if m and m.group(1) not in ("candidate", "active", "retired"):
            errs.append(f"{rel}: {eid} invalid status '{m.group(1)}'")
    active = len(re.findall(r"- \*\*Status:\*\* active", body))
    if active > int(fm.get("max_active_entries", 40)):
        errs.append(f"{rel}: {active} active entries exceed max_active_entries")
    return errs, warns

def check_file(path, cfg, hashes, today):
    errs, warns = [], []
    rel = os.path.relpath(path, ROOT)
    text = open(path, encoding="utf-8").read()
    fm_txt, body = split_fm(text)
    base = os.path.basename(path)
    if fm_txt is None:
        if base.startswith("_") or base in ("README.md", "FAILED.md") or "/runs/" in path.replace("\\", "/"):
            return errs, warns
        return [f"{rel}: no YAML front-matter"], warns
    try:
        fm = yaml.safe_load(fm_txt) or {}
    except yaml.YAMLError as e:
        return [f"{rel}: YAML error: {e}"], warns
    rt = fm.get("record_type")
    if rt not in REQUIRED:
        return [f"{rel}: unknown or missing record_type '{rt}'"], warns
    for k in REQUIRED[rt]:
        if k not in fm:
            errs.append(f"{rel}: missing field '{k}'")
    if rt == "learnings":
        return check_learnings(rel, fm, body)
    status = fm.get("status")
    if status == "template" or rt == "team_profile":
        return errs, warns  # schema-only for templates

    # immutability
    if status == "final":
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        logged = hashes.get(os.path.normpath(rel))
        if logged is None:
            warns.append(f"{rel}: final but never logged in logs/events.jsonl")
        elif logged != sha:
            errs.append(f"{rel}: FINAL FILE MODIFIED after logging (hash mismatch) — create a .v2 instead")

    # claims
    claims = fm.get("claims") or []
    ids = set()
    stale_months = (cfg.get("freshness") or {}).get("funding_stale_months", 12)
    for c in claims:
        cid = c.get("id")
        if not cid:
            errs.append(f"{rel}: claim without id"); continue
        if cid in ids:
            errs.append(f"{rel}: duplicate claim id {cid}")
        ids.add(cid)
        lab = c.get("label")
        if lab not in LABELS:
            errs.append(f"{rel}: {cid} invalid label '{lab}'")
        srcs = c.get("sources") or []
        for s in srcs:
            if not s.get("url"):
                errs.append(f"{rel}: {cid} source without url")
            if not parse_date(s.get("published")):
                (errs if lab == "FACT" else warns).append(f"{rel}: {cid} source without valid 'published' date")
            if s.get("source_type") not in SRC_TYPES:
                warns.append(f"{rel}: {cid} source_type should be one of {sorted(SRC_TYPES)}")
        if c.get("key_number") and srcs and all(s.get("source_type") == "aggregator" for s in srcs):
            errs.append(f"{rel}: {cid} key number/metric supported only by aggregators (any label) — discovery only")
        if lab == "FACT" and not srcs:
            errs.append(f"{rel}: {cid} FACT without source")
        if lab == "ESTIMATE" and not c.get("method"):
            errs.append(f"{rel}: {cid} ESTIMATE without method")
        if lab == "HYPOTHESIS" and not c.get("falsifier"):
            errs.append(f"{rel}: {cid} HYPOTHESIS without falsifier")
        if c.get("key_number") and lab == "FACT":
            if len(srcs) < 2 and not c.get("single_source"):
                errs.append(f"{rel}: {cid} key number with <2 sources must set single_source: true")

            dates = [parse_date(s.get("published")) for s in srcs if parse_date(s.get("published"))]
            if dates and (today - max(dates)).days > stale_months * 30.5 and not c.get("stale"):
                warns.append(f"{rel}: {cid} key number older than {stale_months} months — set stale: true")

    # references
    refs = set(CLAIM_REF.findall(body))
    def collect(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("claims", "evidence", "count_claims", "rationale_claims", "observable_before_round", "observed_after_round") and isinstance(v, list):
                    for x in v:
                        if isinstance(x, str) and re.fullmatch(r"C\d+", x):
                            refs.add(x)
                else:
                    collect(v)
        elif isinstance(o, list):
            for x in o: collect(x)
    collect({k: v for k, v in fm.items() if k != "claims"})
    for r in sorted(refs - ids):
        errs.append(f"{rel}: reference to undefined claim {r}")

    # scores
    for k, v in walk_scores(fm):
        s = v.get("score")
        if s is None:
            continue
        if not isinstance(s, int) or not 1 <= s <= 5:
            errs.append(f"{rel}: {k} score must be integer 1–5 or null")
        elif not v.get("evidence") and s > 2:
            errs.append(f"{rel}: {k} score {s} without evidence (cap is 2)")

    # record-specific
    if rt == "analysis":
        lz = fm.get("lenses") or {}
        for l in LENSES:
            if l not in lz:
                errs.append(f"{rel}: lens '{l}' missing")
        if len([b for b in (fm.get("bear_case") or []) if b]) < 3:
            errs.append(f"{rel}: bear_case needs 3 items")
    if rt == "investor_person":
        if not str(fm.get("pitchbook_profile", "")).startswith("http") and status not in ("template",):
            errs.append(f"{rel}: investor_person needs a pitchbook_profile URL (people-first records are PitchBook-based)")
        for i, d in enumerate(fm.get("recent_deals") or []):
            for k in ("company", "date", "stage", "role", "hq_country", "claims"):
                if k not in (d or {}):
                    errs.append(f"{rel}: recent_deals[{i}] missing '{k}'")
            if (d or {}).get("hq_country") in ("DE","FR","ES","IT","NL","SE","DK","FI","AT","BE","PT","IE","PL","GB","UK","CH","NO"):
                warns.append(f"{rel}: recent_deals[{i}] is European-HQ — outside Phase 1 sourcing geography")
    if rt == "startup_source":
        w = str(fm.get("website", ""))
        if not (w.startswith("http") or w.lower() == "stealth"):
            errs.append(f"{rel}: website must be a URL or 'stealth' (with a claim), not '{w}'")
    if rt == "opportunity_card":
        if status != "template" and fm.get("maturity") is not None or fm.get("business_model") is not None:
            if not fm.get("business_model"):
                errs.append(f"{rel}: business_model is required (v3.1)")
            if fm.get("maturity") not in ("angel", "pre_seed", "accelerator", "seed_young", "seed", None):
                errs.append(f"{rel}: maturity must be angel/pre_seed/accelerator/seed_young/seed")
            if fm.get("evidence_level") not in ("solid", "partial", "thin", None):
                errs.append(f"{rel}: evidence_level must be solid/partial/thin")
        if fm.get("label") not in ("OPEN_SPACE", "DIFFERENTIABLE", "TRANSFERABLE", "WATCH", "BLOCKED",
                                   "SPAZIO_LIBERO", "DIFFERENZIABILE", "TRASFERIBILE", "DA_OSSERVARE", "BLOCCATO"):  # Italian = legacy v3.0
            errs.append(f"{rel}: label must be OPEN_SPACE/DIFFERENTIABLE/TRANSFERABLE/WATCH/BLOCKED")
        ang = [a for a in (fm.get("angles") or []) if isinstance(a, dict) and a.get("title")]
        if not 3 <= len(ang) <= 5:
            errs.append(f"{rel}: need 3-5 angles (got {len(ang)})")
        for i, a in enumerate(ang):
            if not a.get("for_whom") or not a.get("why_gap"):
                errs.append(f"{rel}: angle #{i+1} needs for_whom and why_gap")
            if re.search(r"\b(better ux|ai[- ]powered|cheaper|migliore ux|pi[uù] economico)\b", (a.get("title","")+" "+a.get("why_gap","")).lower()) and len(a.get("why_gap","")) < 80:
                errs.append(f"{rel}: angle #{i+1} looks generic: name the segment/workflow and why incumbents miss it")
        if len([t for t in (fm.get("transfers") or []) if isinstance(t, dict) and t.get("sector")]) < 2:
            errs.append(f"{rel}: need >=2 transfers")
        rk = [r for r in (fm.get("risks") or []) if isinstance(r, dict) and r.get("risk")]
        if not 1 <= len(rk) <= 3:
            errs.append(f"{rel}: need 1-3 risks")
        if len([q for q in (fm.get("questions") or []) if q]) < 3:
            errs.append(f"{rel}: need >=3 questions")
        if len(fm.get("europe_queries") or []) < 2:
            errs.append(f"{rel}: need >=2 europe_queries")
        for e in fm.get("europe_today") or []:
            if isinstance(e, dict) and e.get("name") and not e.get("what_they_miss"):
                errs.append(f"{rel}: europe_today '{e.get('name')}' needs what_they_miss")
        sc = fm.get("scores") or {}
        for k in ("insight", "transferability", "space", "differentiation", "feasibility"):
            v = (sc.get(k) or {}).get("score")
            if not isinstance(v, int) or not 1 <= v <= 5:
                errs.append(f"{rel}: scores.{k} must be 1-5")
        t = fm.get("one_week_test") or {}
        if not t.get("what") or not re.search(r"\d", str(t.get("signal", ""))):
            errs.append(f"{rel}: one_week_test needs what + a numeric signal")
    if rt == "triage":
        if fm.get("outcome") not in ("PASS", "PIVOT", "KILL"):
            errs.append(f"{rel}: outcome must be PASS/PIVOT/KILL")
        if fm.get("outcome") == "PIVOT" and not fm.get("pivot_vector"):
            errs.append(f"{rel}: PIVOT needs a pivot_vector")
        t = (fm.get("pan_eu_tam") or {})
        bc = t.get("buyer_count") or {}
        ko = fm.get("eu_knockout") or {}
        reason = str(fm.get("outcome_reason", "")).lower()
        early_kill = fm.get("outcome") == "KILL" and (ko.get("knocked_out") is True or "team-fit" in reason or "team fit" in reason)
        # early kills (team-fit or EU knockout) skip TAM sizing: no time spent sizing a dead idea
        if not early_kill and sum(1 for k in ("ES", "IT", "FR", "DACH") if bc.get(k) not in (None, "")) < 3:
            errs.append(f"{rel}: pan-EU TAM must count buyers in >=3 of ES/IT/FR/DACH (never one country alone)")
        min_q = 2 if early_kill else 4
        if not ("team-fit" in reason or "team fit" in reason) and len(ko.get("queries") or []) < min_q:
            errs.append(f"{rel}: eu_knockout needs >={min_q} queries")
        floor = float((cfg.get("triage") or {}).get("tam_min_eur_per_year", 10_000_000))
        hi = (t.get("tam_eur_per_year") or {}).get("high")
        if fm.get("outcome") == "PASS" and isinstance(hi, (int, float)) and hi < floor:
            errs.append(f"{rel}: PASS but pan-EU TAM high {hi:,.0f} < floor {floor:,.0f}")
        if fm.get("outcome") == "PASS" and (fm.get("eu_knockout") or {}).get("knocked_out") is True:
            errs.append(f"{rel}: PASS but eu_knockout.knocked_out is true")
    if rt == "memo":
        if fm.get("verdict") not in ("GO", "PIVOT", "KILL"):
            errs.append(f"{rel}: memo verdict must be GO/PIVOT/KILL")
        for h in ("## 1. Upside", "## 2. Kill / pivot diagnostic", "## 3. Kill criteria", "## 4. Adaptation / pivot vectors"):
            if h not in body:
                errs.append(f"{rel}: memo missing section '{h}' (balanced memo rule)")
    if rt == "europe":
        if len(fm.get("queries_log") or []) < 12:
            errs.append(f"{rel}: queries_log has <12 queries")
        langs = {q.get("lang") for q in (fm.get("queries_log") or []) if isinstance(q, dict)}
        if len(langs) < 3:
            warns.append(f"{rel}: queries in <3 languages")
        allowed = set((cfg.get("scope") or {}).get("countries") or [])
        rc = fm.get("recommended_country")
        if allowed and rc and rc not in allowed and rc not in ("DE", "AT", "CH", "SE", "DK", "NO", "FI"):
            errs.append(f"{rel}: recommended_country {rc} not in run_config countries")
    if rt == "proposal":
        cust = fm.get("first_10_customers") or []
        if len(cust) < 10:
            warns.append(f"{rel}: first_10_customers has {len(cust)} entries")
        for i, c in enumerate(cust):
            if not (c or {}).get("source_url"):
                errs.append(f"{rel}: customer #{i+1} without source_url")
        t = fm.get("two_week_test") or {}
        if not t.get("pass_threshold") or not re.search(r"\d", str(t.get("pass_threshold"))):
            errs.append(f"{rel}: two_week_test.pass_threshold must be numeric")
        if len([k for k in (fm.get("kill_criteria") or []) if k]) < 3:
            errs.append(f"{rel}: need ≥3 kill_criteria")
        for g in fm.get("gtm_90d") or []:
            if not (g or {}).get("url"):
                warns.append(f"{rel}: GTM row without url: {g.get('action','')[:40]}")
    if rt == "redteam":
        if fm.get("verdict") not in ("KILL", "REVISE", "SURVIVE"):
            errs.append(f"{rel}: verdict must be KILL/REVISE/SURVIVE")
        if len(fm.get("searches_run") or []) < 6:
            errs.append(f"{rel}: Red Team ran <6 searches")
        if fm.get("version", 1) >= 2 and fm.get("verdict") == "REVISE":
            errs.append(f"{rel}: REVISE not allowed in v2")
        sev = [a.get("severity") for a in fm.get("kill_arguments") or [] if isinstance(a, dict)]
        if fm.get("verdict") == "SURVIVE" and any(s in ("fatal",) for s in sev):
            errs.append(f"{rel}: SURVIVE with a fatal argument")

    # text checks (body + claim text)
    alltext = body + "\n" + "\n".join(str(c.get("text", "")) for c in claims) + "\n" + fm_txt
    low = alltext.lower()
    for b in BANNED:
        if b in low:
            warns.append(f"{rel}: banned/generic phrase '{b}' — make it specific or remove")
    for rx in TOPDOWN:
        m = rx.search(alltext)
        if m:
            errs.append(f"{rel}: top-down sizing pattern: '{m.group(0)}'")
    for m in EMAIL.finditer(alltext):
        errs.append(f"{rel}: email address found ({m.group(0)}) — organisations and roles only")
    for m in PHONE.finditer(body):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", m.group(0).strip()) or re.fullmatch(r"\d{5,7}-\d{2}", m.group(0).strip()) or sum(ch.isdigit() for ch in m.group(0)) < 9:
            continue
        warns.append(f"{rel}: possible phone number '{m.group(0)}'")
    if rt not in ("memo",) and "## Open questions" not in body:
        warns.append(f"{rel}: missing '## Open questions' section")
    return errs, warns

def normalise(msg):
    """error message -> rule pattern (no path, no claim ids, no numbers) for grouping by A8"""
    m = msg.split(": ", 1)[1] if ": " in msg else msg
    m = re.sub(r"\bC\d+\b", "C#", m)
    m = re.sub(r"'[^']*'", "'…'", m)
    return re.sub(r"\d+", "N", m)

def main():
    os.chdir(ROOT)
    args = sys.argv[1:]
    log_run = log_agent = None
    if "--log" in args:
        args.remove("--log")
        try:
            log_run = args.pop(args.index("--run") + 1); args.remove("--run")
            log_agent = args.pop(args.index("--agent") + 1); args.remove("--agent")
        except ValueError:
            sys.exit("--log needs --run RUN-ID and --agent A#")
    targets = args or ["data", "templates", "config/learnings.md"]
    cfg, hashes, today = load_cfg(), logged_hashes(), datetime.date.today()
    files = []
    for t in targets:
        if os.path.isfile(t):
            files.append(t)
        else:
            for d, dirs, fs in os.walk(t):
                dirs[:] = [x for x in dirs if not x.startswith("_archive")]
                files += [os.path.join(d, f) for f in fs if f.endswith(".md") and not f.endswith(".tmp")]
    E, W = [], []
    for f in sorted(files):
        e, w = check_file(os.path.abspath(f), cfg, hashes, today)
        E += e; W += w
    for w in W: print("WARN ", w)
    # history seals: closed runs must never change
    rroot = os.path.join(ROOT, "runs")  # seals
    for rn in sorted(os.listdir(rroot)) if os.path.isdir(rroot) else []:
        sp = os.path.join(rroot, rn, "SEAL.json")
        if not os.path.isfile(sp):
            continue
        seal = json.load(open(sp, encoding="utf-8"))
        for rp, h in seal["files"].items():
            ap = os.path.join(ROOT, rp)
            if not os.path.isfile(ap):
                E.append(f"{rp}: sealed by {rn} but missing (history deleted or moved)")
            elif hashlib.sha256(open(ap, "rb").read()).hexdigest() != h:
                E.append(f"{rp}: sealed by {rn} but MODIFIED: write a new version in the current run instead")
    for e in E: print("ERROR", e)
    if log_run:
        ts = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        os.makedirs(os.path.join(ROOT, "logs"), exist_ok=True)
        with open(os.path.join(ROOT, "logs", "validation.jsonl"), "a", encoding="utf-8") as f:
            for lvl, items in (("ERROR", E), ("WARN", W)):
                for msg in items:
                    f.write(json.dumps({"ts": ts, "run_id": log_run, "agent": log_agent, "level": lvl,
                                        "path": msg.split(": ", 1)[0], "pattern": normalise(msg), "message": msg},
                                       ensure_ascii=False) + "\n")
            f.write(json.dumps({"ts": ts, "run_id": log_run, "agent": log_agent, "level": "SUMMARY",
                                "files": len(files), "errors": len(E), "warnings": len(W)}) + "\n")
    print(f"\nChecked {len(files)} files: {len(E)} errors, {len(W)} warnings")
    sys.exit(1 if E else 0)

if __name__ == "__main__":
    main()
