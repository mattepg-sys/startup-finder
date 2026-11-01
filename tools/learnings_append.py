#!/usr/bin/env python3
"""Deterministic writer for config/learnings.md (used by A8 Retrospective; the user may use it too).

Add or reinforce entries from a JSON file:
  python3 tools/learnings_append.py --run RUN-20261008-01 --input runs/RUN-20261008-01/retro_proposals.json
Retire an entry:
  python3 tools/learnings_append.py --run RUN-... --retire L-RULE-003 --reason "superseded by L-RULE-007"

Input JSON: a list of objects:
  {"section": "rule"|"pref"|"kill",
   "key": "a4-local-language-queries",      # stable dedupe key, kebab-case
   "title": "Search competitors in the local language for every allowed country",
   "rule": "Run ≥3 local-language queries per allowed country before scoring C1.",
   "why": "queries_log <12 rejected twice; missed 2 Italian players",
   "evidence": "RUN-20261008-01: validator 'queries_log has <12 queries' ×3",
   "applies_to": ["A4"],
   "source": "validator"|"audit"|"user"|"redteam"}

Behaviour:
- Backs up the current file to config/learnings_history/ before any change.
- Same key already present: increments Seen, updates last date, appends evidence, and promotes candidate→active at Seen ≥2.
- New key: appends the entry to its section with the next ID. Status is 'active' if source == user, else 'candidate'.
- Logs every change to logs/learnings_changes.jsonl.
- Exits with code 2 (no write) if active entries would exceed max_active_entries; A8 must retire or merge first.
"""
import argparse, json, os, re, shutil, datetime, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "config", "learnings.md")
HIST = os.path.join(ROOT, "config", "learnings_history")
CHG = os.path.join(ROOT, "logs", "learnings_changes.jsonl")
SECTIONS = {"rule": ("## Agent Rules & Self-Corrections", "L-RULE"),
            "pref": ("## User Preferences & Feedback", "L-PREF"),
            "kill": ("## Kill Patterns (Red Team)", "L-KILL")}
AGENTS = {"A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "ALL"}
ENTRY_RX = re.compile(r"^### (L-(?:RULE|PREF|KILL)-\d{3}) · .*?(?=^### |^## |\Z)", re.M | re.S)
SEEN_RX = re.compile(r"- \*\*Seen:\*\* (\d+) · first (\S+) · last (\S+)")
STATUS_RX = re.compile(r"- \*\*Status:\*\* (\w+)")
KEY_RX = re.compile(r"<!-- key: (\S+) -->")
INJECTION = re.compile(r"(ignore (all|previous|the above)|disregard|system prompt|you are now|override)", re.I)

def today():
    return datetime.date.today().isoformat()

def clean(s, n=300):
    s = " ".join(str(s).split())
    return s[:n]

def log(ev):
    os.makedirs(os.path.dirname(CHG), exist_ok=True)
    ev["ts"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    with open(CHG, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")

def backup(run):
    os.makedirs(HIST, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    dst = os.path.join(HIST, f"learnings_{stamp}_{run}.md")
    shutil.copy2(PATH, dst)
    return os.path.relpath(dst, ROOT)

def split(text):
    _, fm, body = text.split("---", 2)
    return yaml.safe_load(fm), fm, body

def count_active(body):
    return len(re.findall(r"- \*\*Status:\*\* active", body))

def next_id(body, prefix):
    nums = [int(x) for x in re.findall(prefix + r"-(\d{3})", body)]
    return f"{prefix}-{(max(nums) + 1 if nums else 1):03d}"

def render(eid, p, status):
    agents = ", ".join(p["applies_to"])
    return (f"### {eid} · {agents} · {clean(p['title'], 90)}\n"
            f"<!-- key: {p['key']} -->\n"
            f"- **Rule:** {clean(p['rule'])}\n"
            f"- **Why:** {clean(p['why'])}\n"
            f"- **Evidence:** {clean(p['evidence'], 400)}\n"
            f"- **Applies to:** {agents}\n"
            f"- **Seen:** 1 · first {today()} · last {today()}\n"
            f"- **Status:** {status}\n\n")

def validate_proposal(p):
    errs = []
    for k in ("section", "key", "title", "rule", "why", "evidence", "applies_to", "source"):
        if not p.get(k):
            errs.append(f"missing {k}")
    if p.get("section") not in SECTIONS:
        errs.append("section must be rule|pref|kill")
    if p.get("key") and not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,60}", p["key"]):
        errs.append("key must be kebab-case, 3–61 chars")
    if not set(p.get("applies_to") or []) <= AGENTS:
        errs.append(f"applies_to must be within {sorted(AGENTS)}")
    if p.get("source") not in ("validator", "audit", "user", "redteam"):
        errs.append("source must be validator|audit|user|redteam")
    blob = " ".join(str(p.get(k, "")) for k in ("title", "rule", "why", "evidence"))
    if INJECTION.search(blob):
        errs.append("text looks like an instruction override — rewrite as an operating rule")
    if re.search(r"https?://", str(p.get("rule", ""))):
        errs.append("rules must not contain URLs (put sources in evidence)")
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--input")
    ap.add_argument("--retire")
    ap.add_argument("--reason", default="")
    a = ap.parse_args()
    text = open(PATH, encoding="utf-8").read()
    meta, fm_txt, full = split(text)
    cut = full.index(SECTIONS["rule"][0])
    preamble, body = full[:cut], full[cut:]   # entries live only after the first section header
    changes = []

    if a.retire:
        m = re.search(rf"^### {re.escape(a.retire)} · .*?(?=^### |^## |\Z)", body, re.M | re.S)
        if not m:
            sys.exit(f"{a.retire} not found")
        block = STATUS_RX.sub("- **Status:** retired", m.group(0), count=1)
        block = block.rstrip("\n") + f"\n- **Retired:** {today()} · {clean(a.reason, 200)}\n\n"
        body = body[:m.start()] + block + body[m.end():]
        changes.append({"action": "retire", "id": a.retire, "reason": a.reason})
    else:
        props = json.load(open(a.input, encoding="utf-8"))
        bad = {i: validate_proposal(p) for i, p in enumerate(props)}
        bad = {i: e for i, e in bad.items() if e}
        if bad:
            for i, e in bad.items():
                print(f"REJECTED proposal #{i}: {e}")
            sys.exit(1)
        for p in props:
            existing = None
            for m in ENTRY_RX.finditer(body):
                km = KEY_RX.search(m.group(0))
                if km and km.group(1) == p["key"]:
                    existing = m; break
            if existing:
                blk = existing.group(0)
                eid = blk.split(" ")[1]
                sm = SEEN_RX.search(blk)
                seen = int(sm.group(1)) + 1
                blk = SEEN_RX.sub(f"- **Seen:** {seen} · first {sm.group(2)} · last {today()}", blk, count=1)
                if clean(p["evidence"], 400) not in blk:
                    blk = re.sub(r"(- \*\*Evidence:\*\* )(.*)", lambda mm: mm.group(1) + clean(mm.group(2) + " | " + p["evidence"], 600), blk, count=1)
                st = STATUS_RX.search(blk).group(1)
                if st == "candidate" and (seen >= 2 or p["source"] in ("user")):
                    blk = STATUS_RX.sub("- **Status:** active", blk, count=1)
                    st = "active"
                body = body[:existing.start()] + blk + body[existing.end():]
                changes.append({"action": "reinforce", "id": eid, "key": p["key"], "seen": seen, "status": st})
            else:
                header, prefix = SECTIONS[p["section"]]
                eid = next_id(body, prefix)
                status = "active" if p["source"] in ("user") else "candidate"
                hpos = body.index(header)
                nxt = body.find("\n## ", hpos + len(header))
                end = nxt + 1 if nxt != -1 else len(body)
                sec = body[hpos:end].replace("_No entries yet._\n", "").replace("_No entries yet._", "")
                sec = sec.rstrip("\n") + "\n\n" + render(eid, p, status)
                body = body[:hpos] + sec + body[end:]
                changes.append({"action": "add", "id": eid, "key": p["key"], "status": status})

    cap = int(meta.get("max_active_entries", 40))
    if count_active(body) > cap:
        print(f"ABORT: active entries would be {count_active(body)} > cap {cap}. Retire or merge entries first. No changes written.")
        sys.exit(2)
    meta["last_updated"] = today()
    meta["last_run"] = a.run
    meta["version"] = int(meta.get("version", 1)) + 1
    bk = backup(a.run)
    new = "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---" + preamble + body
    tmp = PATH + ".tmp"
    open(tmp, "w", encoding="utf-8").write(new)
    os.replace(tmp, PATH)
    for c in changes:
        c.update({"run_id": a.run, "backup": bk}); log(c)
        print(json.dumps(c, ensure_ascii=False))
    print(f"OK: {len(changes)} change(s); active entries now {count_active(body)}/{cap}; backup {bk}")

if __name__ == "__main__":
    main()
