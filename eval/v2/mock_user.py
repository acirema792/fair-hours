#!/usr/bin/env python3
"""Bench v2 scripted user. Replies by topic from the case's user_script; anything it has no answer for
gets "I don't know." (audit round 1, F20: no keyword reply may ratify a guess)."""
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
    if "camera" in low and any(w in low for w in ("know", "aware", "told", "notice", "inform", "consent")) and \
            any(w in low for w in ("recogni", "face", "check", "hours", "know about", "aware")):
        return "consent"
    if "living room" in low or ("cover" in low and "door" in low) or "entrance" in low:
        return "camera_choice"
    if "registered" in low or "closest" in low or "which name" in low or "which one" in low:
        return "name"
    if "snapshot" in low or "evidence" in low:
        return "snapshots"
    return "other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--say", required=True)
    a = ap.parse_args()
    os.makedirs(a.run, exist_ok=True)
    fp = os.path.join(HERE, "fixtures", a.case + ".json")
    for alt in ("blind", "round2"):
        if not os.path.exists(fp):
            fp = os.path.join(HERE, alt, "fixtures", a.case + ".json")
    fx = json.load(open(fp))
    script = fx["user_script"]
    t = topic(a.say)
    reply = script.get(t) or script.get("other") or "I don't know."
    with open(os.path.join(a.run, "log.jsonl"), "a") as fh:
        fh.write(json.dumps({"seq": next_seq(a.run), "kind": "user", "said": a.say, "topic": t, "reply": reply}) + "\n")
    print("USER: " + reply)


if __name__ == "__main__":
    main()
