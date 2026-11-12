#!/usr/bin/env python3
"""Stand-in for Uliya's `delegate --target <agent> --instruction '<task>'` in the offline test bench.

Routes the instruction to a fixture by the CLI/action it names, returns a delegation envelope
({"state": completed|failed|waiting_approval, ...}) and appends every call to RUN/log.jsonl.
It never decides anything about the comparison itself: it only returns what a NAS expert would.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AGENT_OF = {"ug-surveillance": "security-monitor-agent", "ug-document": "document-agent",
            "ug-filesystem": "file-agent", "ug-filemgr": "file-agent", "file-workflow": "file-agent",
            "ug-knowledge": "knowledge-agent", "ug-photo": "photo-agent", "ug-video": "media-agent", "ug-music": "media-agent"}
SLOT = re.compile(r"\b[A-Z]{2,}(?:_[A-Z]{2,})+\b")


def next_seq(run):
    path = os.path.join(run, "seq")
    n = int(open(path).read()) + 1 if os.path.exists(path) else 1
    open(path, "w").write(str(n))
    return n


def respond(state, data=None, error=None, message=None):
    out = {"state": state}
    if state == "completed":
        out["result"] = {"ok": True, "data": data}
    elif state == "failed":
        out["result"] = {"ok": False, "error": error}
    if message:
        out["message"] = message
    return out


def route(fx, target, inst):
    low = inst.lower()
    clis = [c for c in AGENT_OF if c in low]
    for c in clis:
        if AGENT_OF[c] != target:
            return respond("failed", error={"code": "WRONG_EXPERT", "message": f"{c} is owned by {AGENT_OF[c]}, not {target}"})
    f = fx["fixtures"]
    if "ug-surveillance" in low and "event-timeline" in low:
        if "identity-type all" in low or "identity-type: all" in low:
            if f.get("proof_error"):
                return respond("failed", error={"code": "SERVICE_UNAVAILABLE", "message": f["proof_error"]})
            return respond("completed", data={"per_camera_day": f.get("proof", []), "warnings": f.get("proof_warnings", [])})
        if f.get("helper_events_error"):
            return respond("failed", error={"code": "IDENTITY_NOT_FOUND", "message": f["helper_events_error"]})
        items = f.get("helper_events", [])
        return respond("completed", data={"items": items, "count": len(items), "warnings": []})
    if "ug-surveillance" in low and "event-evidence" in low:
        ids = re.findall(r"evt_[0-9_]+", inst)
        return respond("completed", data={"evidence": [{"event_id": i, "type": "snapshot", "ref": f"snapshot://{i}/1"} for i in ids]})
    if "ug-surveillance" in low and "cameras" in low:
        return respond("completed", data={"cameras": f.get("cameras", [])})
    if "ug-filesystem" in low and "find" in low:
        if "find_results" in f:
            return respond("completed", data={"items": f["find_results"]})
        bill = f.get("bill")
        return respond("completed", data={"items": [{"path": bill["file"], "size": 182344, "mtime": "2026-11-09T18:20:00-05:00"}] if bill else []})
    if "ug-document" in low and "extract" in low:
        bill = f.get("bill")
        if not bill:
            return respond("failed", error={"code": "FILE_NOT_FOUND", "message": "no such file"})
        rows = [dict(v, source_text=f"{v['date']} {v.get('start') or ''}-{v.get('end') or ''} {v.get('billed_hours')} h") for v in bill["visits"]]
        return respond("completed", data={"file": bill["file"], "visits": rows, "total": bill.get("total"),
                                          "currency": bill.get("currency"), "failures": bill.get("failures", [])})
    if "ug-knowledge" in low and "save-text" in low:
        if f.get("save_state") == "waiting_approval":
            return respond("waiting_approval", message="The save is waiting for the user's approval in the NAS approval prompt.")
        return respond("completed", data={"verified": True, "outputFile": "Documents/Household/fair-hours-report.md", "contentBytes": len(inst)})
    return respond("failed", error={"code": "UNSUPPORTED", "message": "the expert could not map this instruction to a published capability"})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--case", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--instruction", required=True)
    a = ap.parse_args()
    os.makedirs(a.run, exist_ok=True)
    fx = json.load(open(os.path.join(HERE, "fixtures", a.case + ".json")))
    out = route(fx, a.target, a.instruction)
    entry = {"seq": next_seq(a.run), "kind": "delegate", "target": a.target, "instruction": a.instruction,
             "state": out["state"], "unresolved_slots": SLOT.findall(a.instruction)}
    with open(os.path.join(a.run, "log.jsonl"), "a") as fh:
        fh.write(json.dumps(entry) + "\n")
    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
