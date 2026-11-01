#!/usr/bin/env python3
"""Check that this machine can run Startup Finder. Usage: python3 tools/selftest.py"""
import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True
def check(name, cond, fix=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + ("" if cond else f"  → {fix}"))
    ok = ok and cond
check("Python ≥ 3.8", sys.version_info >= (3, 8), "install Python 3.8+")
try:
    import yaml  # noqa
    check("PyYAML installed", True)
except ImportError:
    check("PyYAML installed", False, "pip install pyyaml")
for f in ["config/run_config.yaml", "config/evidence_standard.md", "config/learnings.md", "agents/00_orchestrator.md",
          "agents/01_scout.md", "agents/02_opportunity_lab.md", "templates/opportunity_card.md", "templates/report_template.html"]:
    check(f"file {f}", os.path.exists(os.path.join(ROOT, f)), "re-download the repository")
if ok:
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "validate.py"), "templates", "config/learnings.md"],
                       capture_output=True, text=True, cwd=ROOT)
    check("templates validate", r.returncode == 0, r.stdout[-300:])
print("\nReady." if ok else "\nFix the items above, then run again.")
sys.exit(0 if ok else 1)
