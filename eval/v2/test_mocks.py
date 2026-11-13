#!/usr/bin/env python3
"""Routing test for the v2 mock experts: every delegate template in SKILL.md, with slots filled for C01,
must reach the intended action. Run before any bench run (added after a routing bug invalidated a run set)."""
import json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, "..", "..", "skill", "fair-hours", "SKILL.md")
FILL = {"HELPER_NAME": "Ana Ruiz", "PERIOD_START": "2026-11-02", "PERIOD_END": "2026-11-08", 
        "DATES": "2026-11-04", "TIMEZONE": "America/New_York", "ENTRY_CAMERAS": "Front Door", "BILL_FILE": "Invoices/Ana Ruiz - Nov week 1.pdf",
        "BILL_FOLDER": "Invoices", "NAME_HINT": "Ana", "SAVE_FOLDER": "Documents", "REPORT_TEXT": "report", "EVENT_IDS": "evt_20261104_0910"}
EXPECT = [("identity-type known, person-name", "items"), ("identity-type all", "items"), ("event-evidence", "evidence"),
          ("vision-ocr", None), ("save-text", "verified"), ("extract", "visits"), ("ug-filesystem find", "items"),
          ("ug-surveillance faces", "match"), ("ug-surveillance cameras", "cameras")]
tmpl = re.findall(r"`delegate --target (\S+) --instruction '([^']*)'`", open(SKILL).read())
assert len(tmpl) >= 9, len(tmpl)
run = tempfile.mkdtemp()
bad = 0
for target, inst in tmpl:
    for k, v in FILL.items():
        inst = inst.replace(k, v)
    out = json.loads(subprocess.run([sys.executable, os.path.join(HERE, "mock_delegate.py"), "--run", run, "--case", "C01", "--target", target, "--instruction", inst], capture_output=True, text=True).stdout)
    key = next(k for marker, k in EXPECT if marker in inst)
    data = (out.get("result") or {}).get("data") or {}
    ok = (key is None and out["state"] == "failed") or (key in data)
    if "person-name" in inst:
        ok = ok and data["count"] == 10  # all ten C01 helper events fall in the window
        import mock_delegate as M
        ok = ok and M.window(inst) == ("2026-11-02 00:00", "2026-11-09 12:00")  # 12:00 on the day after PERIOD_END
    if "identity-type all" in inst:
        ok = ok and data["count"] == 8 and all(i["time"].startswith("2026-11-04") for i in data["items"]) and not any("identity" in i for i in data["items"])  # DATES only: 6 household passages + 2 helper events (round 2, G1), no names when the instruction forbids them
    bad += not ok
    print("OK  " if ok else "BAD ", target, "|", inst[:70], "->", out["state"], list(data)[:3])
print("FAILED" if bad else "ALL ROUTES OK"); sys.exit(1 if bad else 0)
