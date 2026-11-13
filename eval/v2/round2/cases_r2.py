"""Round-2 regression cases (audit round 2: G2, G3, G5, G6). Expected outcomes written before any run.
`python3 eval/v2/round2/cases_r2.py` writes eval/v2/round2/fixtures/*.json and eval/v2/round2/expected/*.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cases_v2 import A, CAMERAS, KNOWN, YES, bill, busy, ev, pas, visit  # noqa: E402

MSG = " New York time. She knows the door cameras recognise faces and may be used to check hours."


def case(id, title, msg, fx, exp, script=None):
    fx.setdefault("cameras", CAMERAS)
    fx.setdefault("known_faces", KNOWN)
    return dict(id=id, title=title, mode="check", user_message=msg, fixtures=fx, user_script=script or dict(YES), expected=exp)


CASES = [
    case("R01", "Camera gap at the departure: never Billed more than seen (G2)",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-3 r.pdf against the Front Door camera." + MSG,
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-3 r.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "08:00", "12:00", 4, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:02", "11:58"]) + ev(A, "2026-11-03", ["08:00", "09:30"]),
              passages=busy("2026-11-02") + pas("2026-11-03", ["07:30", "08:15"]),
              warnings=[{"date": "2026-11-03", "text": "Front Door not recording from 2026-11-03 10:00 to 2026-11-03 13:00."}]),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Inconclusive"]], calls_forbidden=["save-text"])),
    case("R02", "Recording proof needed on every chosen entry camera (G3)",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-3 two doors.pdf against the Front Door and Garage Door cameras." + MSG,
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-3 two doors.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:01", "12:00"]),
              passages=busy("2026-11-02") + pas("2026-11-02", ["10:15"], camera="Garage Door")
              + pas("2026-11-03", ["07:30"]) + pas("2026-11-03", ["10:40"], camera="Garage Door")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Inconclusive"]], calls_forbidden=["save-text"])),
    case("R03", "Events after the period are not counted as unbilled time (G5)",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov week 1 r.pdf against the Front Door camera for Nov 2-8." + MSG,
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov week 1 r.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-04", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:00", "12:01"]) + ev(A, "2026-11-04", ["08:58", "11:59"]) + ev(A, "2026-11-09", ["09:00", "11:50"]),
              passages=busy("2026-11-02", "2026-11-04", "2026-11-09")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-04", "Confirmed"]], calls_forbidden=["save-text"])),
    case("R04", "Printed hours larger than the printed times (G6)",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2 hours.pdf against the Front Door camera." + MSG,
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2 hours.pdf", [visit("2026-11-02", "09:00", "12:00", 4, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:00", "12:02"]), passages=busy("2026-11-02")),
         dict(rows=[["2026-11-02", "Billed more than seen"]], must_contain=["58 min"], calls_forbidden=["save-text"])),
]


def main():
    for d in ("fixtures", "expected"):
        os.makedirs(os.path.join(HERE, d), exist_ok=True)
    for c in CASES:
        json.dump(dict(id=c["id"], mode=c["mode"], user_message=c["user_message"], fixtures=c["fixtures"], user_script=c["user_script"]),
                  open(os.path.join(HERE, "fixtures", c["id"] + ".json"), "w"), indent=1)
        json.dump(dict(id=c["id"], title=c["title"], **c["expected"]), open(os.path.join(HERE, "expected", c["id"] + ".json"), "w"), indent=1)
    print(f"wrote {len(CASES)} cases")


if __name__ == "__main__":
    main()
