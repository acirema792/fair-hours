#!/usr/bin/env python3
"""Bench v2 stand-in for Uliya's `delegate --target <agent> --instruction '<task>'`.

Stricter than v1 (audit round 1, F20): events are filtered by the dates, time window and cameras the
instruction names; passages carry recognised yes/no and no names; faces, vision-ocr and cut-off lists are
supported. Every call is appended to RUN/log.jsonl. It never decides anything about the comparison.
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
DATE = re.compile(r"(2026-\d\d-\d\d)(?:[ T](\d\d:\d\d))?")


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


def cameras_named(inst, cams):
    named = [c["name"] for c in cams if c["name"].lower() in inst.lower()]
    return named or [c["name"] for c in cams]


def window(inst):
    """(start, end) as 'YYYY-MM-DD HH:MM' strings from 'from X ... to Y', else None."""
    m = re.search(r"from\s+(2026-\d\d-\d\d)(?:[ T](\d\d:\d\d))?.{0,40}?\bto\s+(2026-\d\d-\d\d)(?:[ T](\d\d:\d\d))?", inst)
    if not m:
        return None
    return f"{m.group(1)} {m.group(2) or '00:00'}", f"{m.group(3)} {m.group(4) or '23:59'}"


def local(ts):  # '2026-11-02T09:04:00-05:00' -> '2026-11-02 09:04'
    return ts[:10] + " " + ts[11:16]


def route(fx, target, inst):
    low = inst.lower()
    for c in [c for c in AGENT_OF if c in low]:
        if AGENT_OF[c] != target:
            return respond("failed", error={"code": "WRONG_EXPERT", "message": f"{c} is owned by {AGENT_OF[c]}, not {target}"})
    f = fx["fixtures"]
    cams = f.get("cameras", [])
    if "ug-surveillance" in low and "event-timeline" in low:
        named = cameras_named(inst, cams)
        if "identity-type all" in low:  # passages
            if f.get("passages_error"):
                return respond("failed", error={"code": "SERVICE_UNAVAILABLE", "message": f["passages_error"]})
            dates = set(re.findall(r"2026-\d\d-\d\d", inst))
            w = window(inst)
            items = []
            for p in f.get("passages", []):
                d = p["time"][:10]
                if p["camera"] not in named:
                    continue
                if w and not (w[0] <= local(p["time"]) <= w[1]):
                    continue
                if not w and dates and d not in dates:
                    continue
                items.append({"time": p["time"], "camera": p["camera"], "recognised": p["recognised"]})
            warn = [x["text"] for x in f.get("warnings", []) if not dates or x["date"] in dates or (w and w[0][:10] <= x["date"] <= w[1][:10])]
            return respond("completed", data={"items": items, "count": len(items), "cut_at_limit": False, "warnings": warn})
        if f.get("helper_events_error"):
            return respond("failed", error={"code": "IDENTITY_NOT_FOUND", "message": f["helper_events_error"]})
        helper = f.get("helper_name", "")
        if helper and helper.lower() not in low:
            return respond("completed", data={"items": [], "count": 0, "cut_at_limit": False, "warnings": []})
        w = window(inst)
        items = [e for e in f.get("helper_events", []) if e["camera"] in named and (not w or w[0] <= local(e["time"]) <= w[1])]
        cut = f.get("helper_cut_after")
        if cut:
            items = [e for e in items if local(e["time"]) <= cut]
        warn = [x["text"] for x in f.get("warnings", []) if not w or w[0][:10] <= x["date"] <= w[1][:10]]
        return respond("completed", data={"items": items, "count": len(items), "cut_at_limit": bool(cut),
                                          "note": f"list cut at the limit after {cut}" if cut else None, "warnings": warn})
    if "ug-surveillance" in low and "event-evidence" in low:
        ids = re.findall(r"evt_[0-9_]+", inst)
        return respond("completed", data={"evidence": [{"event_id": i, "type": "snapshot", "ref": f"snapshot://{i}/1"} for i in ids]})
    if "ug-surveillance" in low and "faces" in low:
        known = f.get("known_faces", [])
        helper_asked = next((k for k in known if k.lower() in low), None)
        exact = [k for k in known if re.search(r"\b" + re.escape(k.lower()) + r"\b", low)]
        if exact:
            return respond("completed", data={"match": "yes", "name": exact[0]})
        words = set(re.findall(r"[a-z]+", low))
        close = [k for k in known if words & set(k.lower().split())]
        return respond("completed", data={"match": "no", "closest": close})
    if "ug-surveillance" in low and "cameras" in low:
        return respond("completed", data={"cameras": cams})
    if "ug-filesystem" in low and "find" in low:
        if "find_results" in f:
            return respond("completed", data={"items": f["find_results"]})
        bill = f.get("bill")
        return respond("completed", data={"items": [{"path": bill["file"], "size": 182344, "mtime": "2026-11-09T18:20:00-05:00"}] if bill else []})
    if "ug-document" in low and "extract" in low:
        bill = f.get("bill")
        if not bill or bill["file"].lower() not in low:
            return respond("failed", error={"code": "FILE_NOT_FOUND", "message": "no such file"})
        rows = [dict(v, source_text=v.get("source_text") or f"{v['date']} {v.get('start') or ''}-{v.get('end') or ''} {v.get('billed_hours')} h") for v in bill["visits"]]
        return respond("completed", data={"file": bill["file"], "visits": rows, "total": bill.get("total"),
                                          "currency": bill.get("currency"), "failures": bill.get("failures", [])})
    if "ug-photo" in low and "vision-ocr" in low:
        if "ocr_text" not in f:
            return respond("failed", error={"code": "NO_TEXT", "message": "no text recognised"})
        return respond("completed", data={"text": f["ocr_text"]})
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
    fp = os.path.join(HERE, "fixtures", a.case + ".json")
    if not os.path.exists(fp):
        fp = os.path.join(HERE, "blind", "fixtures", a.case + ".json")
    fx = json.load(open(fp))
    out = route(fx, a.target, a.instruction)
    entry = {"seq": next_seq(a.run), "kind": "delegate", "target": a.target, "instruction": a.instruction,
             "state": out["state"], "unresolved_slots": SLOT.findall(a.instruction)}
    with open(os.path.join(a.run, "log.jsonl"), "a") as fh:
        fh.write(json.dumps(entry) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
