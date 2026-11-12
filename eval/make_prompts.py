#!/usr/bin/env python3
"""Fill eval/RUNNER.md templates for every case: eval/prompts/<variant>/<case>.txt (run dir = eval/runs/<variant>-<tag>/<case>)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
tag = sys.argv[1] if len(sys.argv) > 1 else "r0"
doc = open(os.path.join(HERE, "RUNNER.md")).read()
tmpl = {"skill": doc.split("## skill variant")[1].split("## baseline variant")[0].strip(),
        "baseline": doc.split("## baseline variant")[1].strip()}
for variant, t in tmpl.items():
    os.makedirs(os.path.join(HERE, "prompts", variant), exist_ok=True)
    for name in sorted(os.listdir(os.path.join(HERE, "fixtures"))):
        fx = json.load(open(os.path.join(HERE, "fixtures", name)))
        run = os.path.join(HERE, "runs", f"{variant}-{tag}", fx["id"])
        p = t.replace("RUN/final.md", run + "/final.md").replace("--run RUN", "--run " + run).replace("--case CASE", "--case " + fx["id"]).replace("USER_MESSAGE", fx["user_message"])
        open(os.path.join(HERE, "prompts", variant, fx["id"] + ".txt"), "w").write(p)
print("ok")
