#!/usr/bin/env python3
"""Fill eval/v2/RUNNER_v2.md for every v2, blind and round-2 case.
usage: python3 eval/v2/make_prompts_v2.py VARIANT RUN_TAG OUT_DIR   (VARIANT = skill | baseline)"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
variant, tag, out = sys.argv[1], sys.argv[2], sys.argv[3]
doc = open(os.path.join(HERE, "RUNNER_v2.md")).read()
t = doc.split("## skill variant")[1].split("## baseline variant")[0].strip() if variant == "skill" else doc.split("## baseline variant")[1].strip()
os.makedirs(out, exist_ok=True)
paths = sorted(glob.glob(os.path.join(HERE, "fixtures", "*.json"))) + sorted(glob.glob(os.path.join(HERE, "blind", "fixtures", "*.json"))) + sorted(glob.glob(os.path.join(HERE, "round2", "fixtures", "*.json")))
for fp in paths:
    fx = json.load(open(fp)); cid = fx["id"]; run = os.path.join(HERE, "runs", tag, cid)
    p = t.replace("RUN/final.md", run + "/final.md").replace("--run RUN", "--run " + run).replace("--case CASE", "--case " + cid).replace("USER_MESSAGE", fx["user_message"])
    open(os.path.join(out, cid + ".txt"), "w").write(p)
print(len(paths), "prompts ->", out)
