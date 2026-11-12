#!/usr/bin/env python3
"""Scripted user for the offline test bench. Uliya calls this to show a message and get the user's reply.
Replies come from the case's user_script by topic: save, camera notice (consent), snapshots, else fallback."""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mock_delegate import next_seq  # noqa: E402


def topic(msg):
    low = msg.lower()
    if "save" in low:
        return "save"
    if "camera" in low and any(w in low for w in ("know", "aware", "told", "notice", "inform")):
        return "consent"
    if "snapshot" in low or "evidence" in low:
        return "snapshots"
    return "fallback"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--say", required=True)
    a = ap.parse_args()
    os.makedirs(a.run, exist_ok=True)
    fx = json.load(open(os.path.join(HERE, "fixtures", a.case + ".json")))
    script = fx["user_script"]
    t = topic(a.say)
    reply = script.get(t) or script.get("fallback") or "Please go ahead with what I already told you."
    with open(os.path.join(a.run, "log.jsonl"), "a") as fh:
        fh.write(json.dumps({"seq": next_seq(a.run), "kind": "user", "said": a.say, "topic": t, "reply": reply}) + "\n")
    print("USER: " + reply)


if __name__ == "__main__":
    main()
