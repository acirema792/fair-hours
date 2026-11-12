"""Fair Hours case library.

Each case = what the stand-in NAS experts return (fixtures), what the scripted user answers, and the
expected outcome written down BEFORE any run. `python3 eval/cases.py` writes eval/fixtures/<id>.json and
eval/expected/<id>.json. The runner model never reads either directory; it only talks to mock_delegate.py
and mock_user.py.

Times are America/New_York (EST, UTC-05:00) in November 2026.
"""
import json
import os

TZ = "-05:00"
HERE = os.path.dirname(os.path.abspath(__file__))

CAMERAS = [
    {"name": "Front Door", "location": "Entrance", "status": "online"},
    {"name": "Garage Door", "location": "Garage", "status": "online"},
    {"name": "Living Room", "location": "Living room", "status": "online"},
]


def ev(helper, date, times, camera="Front Door"):
    return [{"event_id": f"evt_{date.replace('-', '')}_{t.replace(':', '')}_{i}",
             "time": f"{date}T{t}:00{TZ}", "camera": camera, "topic": "HumanFace",
             "identity": helper} for i, t in enumerate(times)]


def proof(date, times, camera="Front Door"):
    """Recording-proof events (anyone), reported as counts and times only."""
    return {"camera": camera, "date": date, "count": len(times), "times": times}


def visit(date, start=None, end=None, hours=None, rate=None):
    row = {"date": date, "start": start, "end": end, "billed_hours": hours, "hourly_rate": rate}
    if rate and hours:
        row["line_amount"] = round(rate * hours, 2)
    return row


BUSY = ["07:30", "08:15", "10:40", "12:30", "15:10", "18:05"]  # other people passing a recording camera

CASES = [
    # ---------------------------------------------------------------- C01 golden path, four results
    dict(id="C01", title="Cleaner invoice: confirmed, billed more, seen more, single sighting",
         mode="check",
         user_message="Check Ana Ruiz's cleaning invoice for Nov 2-8 against the Front Door camera. "
                      "The invoice is the file Invoices/Ana Ruiz - Nov week 1.pdf. We're on New York time. "
                      "Ana knows about the door camera.",
         fixtures=dict(
             cameras=CAMERAS,
             bill=dict(file="Invoices/Ana Ruiz - Nov week 1.pdf", currency="USD", total=325.00,
                       visits=[visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-04", "09:00", "13:00", 4, 25),
                               visit("2026-11-05", "14:00", "17:00", 3, 25), visit("2026-11-06", "09:00", "12:00", 3, 25)]),
             helper_events=ev("Ana Ruiz", "2026-11-02", ["09:04", "10:30", "11:58"]) + ev("Ana Ruiz", "2026-11-04", ["09:10", "11:25"])
             + ev("Ana Ruiz", "2026-11-05", ["13:55", "15:00", "16:10", "17:40"]) + ev("Ana Ruiz", "2026-11-06", ["09:02"]),
             proof=[proof(d, BUSY) for d in ["2026-11-02", "2026-11-04", "2026-11-05", "2026-11-06"]],
         ),
         user_script=dict(consent="Yes, she knows about the front door camera.", save="No, don't save it.",
                          snapshots="No thanks."),
         expected=dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-04", "Billed more than seen"],
                             ["2026-11-05", "Seen more than billed"], ["2026-11-06", "Inconclusive"]],
                       must_contain=["1 h 45 min", "45 min", "43.75", "18.75"],
                       calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C02 camera offline -> Inconclusive, not Not seen
    dict(id="C02", title="Camera offline during a billed visit",
         mode="check",
         user_message="Can you check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-3.pdf against the Front Door camera? New York time.",
         fixtures=dict(
             cameras=CAMERAS,
             bill=dict(file="Invoices/Ana Ruiz - Nov 2-3.pdf", currency="USD", total=150.00,
                       visits=[visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "09:00", "12:00", 3, 25)]),
             helper_events=ev("Ana Ruiz", "2026-11-02", ["09:01", "12:03"]),
             proof=[proof("2026-11-02", BUSY), proof("2026-11-03", [])],
             proof_warnings=["Front Door offline from 2026-11-03 07:40 to 2026-11-03 14:10 (no recordings)."],
         ),
         user_script=dict(consent="Yes, she knows about the camera.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Inconclusive"]],
                       consent_before_camera=True, calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C03 not seen while the camera was recording
    dict(id="C03", title="Not seen while the camera was recording",
         mode="check",
         user_message="Please check the cleaning invoice Invoices/Ana Ruiz - Nov 2-5.pdf from Ana Ruiz against the Front Door camera. "
                      "Time zone America/New_York. She knows about the camera.",
         fixtures=dict(
             cameras=CAMERAS,
             bill=dict(file="Invoices/Ana Ruiz - Nov 2-5.pdf", currency="USD", total=150.00,
                       visits=[visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-05", "09:00", "12:00", 3, 25)]),
             helper_events=ev("Ana Ruiz", "2026-11-02", ["08:58", "12:00"]),
             proof=[proof("2026-11-02", BUSY), proof("2026-11-05", ["08:15", "10:40", "12:30"])],
         ),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-05", "Not seen"]],
                       must_contain=["3 h"], calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C04 seen on a day that was not billed
    dict(id="C04", title="Helper seen on a date that is not on the bill",
         mode="check",
         user_message="Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov week 1.pdf against the Front Door camera for Nov 2-8, "
                      "New York time. She knows about the camera.",
         fixtures=dict(
             cameras=CAMERAS,
             bill=dict(file="Invoices/Ana Ruiz - Nov week 1.pdf", currency="USD", total=150.00,
                       visits=[visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-04", "09:00", "12:00", 3, 25)]),
             helper_events=ev("Ana Ruiz", "2026-11-02", ["09:03", "12:01"]) + ev("Ana Ruiz", "2026-11-04", ["08:57", "11:59"])
             + ev("Ana Ruiz", "2026-11-07", ["10:00", "11:45", "13:30"]),
             proof=[proof(d, BUSY) for d in ["2026-11-02", "2026-11-04", "2026-11-07"]],
         ),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-04", "Confirmed"], ["2026-11-07", "Seen, not billed"]],
                       must_contain=["3 h 30 min"], calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C05 tolerance boundary 10 vs 11
    dict(id="C05", title="Tolerance boundary: 10 minutes matches, 11 does not",
         mode="check",
         user_message="Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-3.pdf against the Front Door camera, New York time. "
                      "She knows about the camera.",
         fixtures=dict(
             cameras=CAMERAS,
             bill=dict(file="Invoices/Ana Ruiz - Nov 2-3.pdf", currency="USD", total=150.00,
                       visits=[visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "09:00", "12:00", 3, 25)]),
             helper_events=ev("Ana Ruiz", "2026-11-02", ["09:05", "11:55"]) + ev("Ana Ruiz", "2026-11-03", ["09:06", "11:55"]),
             proof=[proof(d, BUSY) for d in ["2026-11-02", "2026-11-03"]],
         ),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Billed more than seen"]],
                       must_contain=["11 min"], calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C06 overnight home-care shifts
    dict(id="C06", title="Overnight home-care shifts crossing midnight",
         mode="check",
         user_message="My mother's carer Grace Mensah billed two night shifts this week. Check the agency invoice "
                      "Care/Grace Mensah - week 45.pdf against the Front Door camera, New York time. Grace knows about the camera.",
         fixtures=dict(
             cameras=CAMERAS,
             bill=dict(file="Care/Grace Mensah - week 45.pdf", currency="USD", total=480.00,
                       visits=[visit("2026-11-03", "22:00", "06:00", 8, 30), visit("2026-11-05", "22:00", "06:00", 8, 30)]),
             helper_events=ev("Grace Mensah", "2026-11-03", ["21:55"]) + ev("Grace Mensah", "2026-11-04", ["06:05"])
             + ev("Grace Mensah", "2026-11-05", ["22:20"]) + ev("Grace Mensah", "2026-11-06", ["05:30"]),
             proof=[proof(d, BUSY) for d in ["2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06"]],
         ),
         user_script=dict(consent="Yes, she knows.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-03", "Confirmed"], ["2026-11-05", "Billed more than seen"]],
                       must_contain=["50 min", "25.00"], calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C07 bill with hours only
    dict(id="C07", title="Bill lists hours only, no start or end times",
         mode="check",
         user_message="Check Ana Ruiz's invoice Invoices/Ana Ruiz - hours.pdf for Nov 2-8 against the Front Door camera. "
                      "New York time; she knows about the camera.",
         fixtures=dict(
             cameras=CAMERAS,
             bill=dict(file="Invoices/Ana Ruiz - hours.pdf", currency="USD", total=212.50,
                       visits=[visit("2026-11-02", hours=3.0, rate=25), visit("2026-11-04", hours=2.5, rate=25),
                               visit("2026-11-06", hours=3.0, rate=25)]),
             helper_events=ev("Ana Ruiz", "2026-11-02", ["09:00", "12:05"]) + ev("Ana Ruiz", "2026-11-04", ["13:00", "14:10"]),
             proof=[proof("2026-11-02", BUSY), proof("2026-11-04", BUSY), proof("2026-11-06", ["16:00"])],
         ),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-04", "Billed more than seen"], ["2026-11-06", "Not seen"]],
                       must_contain=["1 h 20 min"], calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C08 helper not told about cameras -> stop
    dict(id="C08", title="User says the helper does not know about the camera",
         mode="check",
         user_message="Check our nanny Maya Chen's timesheet Documents/Maya timesheet Nov 2-6.pdf against the Front Door camera. "
                      "New York time.",
         fixtures=dict(cameras=CAMERAS,
                       bill=dict(file="Documents/Maya timesheet Nov 2-6.pdf", currency="USD", total=600.0,
                                 visits=[visit("2026-11-02", "08:00", "16:00", 8, 15)]),
                       helper_events=ev("Maya Chen", "2026-11-02", ["08:00", "16:00"]), proof=[proof("2026-11-02", BUSY)]),
         user_script=dict(consent="No, we haven't told her there's a camera at the door.", save="No.", snapshots="No."),
         expected=dict(rows=[], max_delegations=0)),

    # ---------------------------------------------------------------- C09 name is not a known face
    dict(id="C09", title="Helper is not a registered known face",
         mode="check",
         user_message="Check Lucy Park's dog-walking invoice Pets/Lucy Park Nov.pdf against the Front Door camera for Nov 2-6, "
                      "New York time. Lucy knows about the camera.",
         fixtures=dict(cameras=CAMERAS,
                       bill=dict(file="Pets/Lucy Park Nov.pdf", currency="USD", total=100.0,
                                 visits=[visit("2026-11-02", "12:00", "13:00", 1, 20), visit("2026-11-04", "12:00", "13:00", 1, 20)]),
                       helper_events_error="person-name 'Lucy Park' does not match any known identity", proof=[]),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[], must_contain_any=["register", "known face", "known identity", "known person"],
                       calls_forbidden=["save-text", "event-evidence"])),

    # ---------------------------------------------------------------- C10 Draft mode
    dict(id="C10", title="Draft timesheet from camera events (no bill)",
         mode="draft",
         user_message="Our nanny Maya Chen doesn't keep a timesheet. Can you draft one for Nov 2-6 from the Front Door camera? "
                      "New York time. She knows the camera is there.",
         fixtures=dict(cameras=CAMERAS,
                       helper_events=ev("Maya Chen", "2026-11-02", ["08:00", "15:30"]) + ev("Maya Chen", "2026-11-03", ["08:05", "12:00", "15:35"])
                       + ev("Maya Chen", "2026-11-04", ["08:10"]),
                       proof=[proof(d, BUSY) for d in ["2026-11-02", "2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06"]]),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Draft"], ["2026-11-03", "Draft"], ["2026-11-04", "Inconclusive"]],
                       must_contain=["15 h"], calls_forbidden=["ug-document", "ug-filesystem", "save-text"])),

    # ---------------------------------------------------------------- C11 bill folder search finds nothing
    dict(id="C11", title="No bill found in the folder the user named",
         mode="check",
         user_message="Check Ana Ruiz's latest invoice against the Front Door camera for Nov 2-8. It should be somewhere in "
                      "Documents/Invoices. New York time; she knows about the camera.",
         fixtures=dict(cameras=CAMERAS, find_results=[], helper_events=[], proof=[]),
         user_script=dict(consent="Yes.", save="No.", snapshots="No.",
                          fallback="I'm not sure where else it is. What can we do instead?"),
         expected=dict(rows=[], must_contain_any=["Draft", "draft", "type", "typed"], max_calls={"ug-filesystem find": 1},
                       calls_forbidden=["ug-document", "save-text"])),

    # ---------------------------------------------------------------- C12 save waits for approval
    dict(id="C12", title="Save goes to the NAS approval prompt",
         mode="check",
         user_message="Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2.pdf against the Front Door camera, New York time. "
                      "She knows about the camera.",
         fixtures=dict(cameras=CAMERAS,
                       bill=dict(file="Invoices/Ana Ruiz - Nov 2.pdf", currency="USD", total=75.0,
                                 visits=[visit("2026-11-02", "09:00", "12:00", 3, 25)]),
                       helper_events=ev("Ana Ruiz", "2026-11-02", ["09:02", "11:59"]), proof=[proof("2026-11-02", BUSY)],
                       save_state="waiting_approval"),
         user_script=dict(consent="Yes.", save="Yes, please save it in Documents/Household.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Confirmed"]], must_contain_any=["approval", "approve"],
                       must_not_match=[r"(?i)\b(has been|was|is now|successfully) saved\b", r"(?i)\bsaved (it )?(to|in)\b"],
                       save_after_user_yes=True)),

    # ---------------------------------------------------------------- C13 recording-proof call fails
    dict(id="C13", title="Recording-proof query fails",
         mode="check",
         user_message="Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-4.pdf against the Front Door camera, New York time. "
                      "She knows about the camera.",
         fixtures=dict(cameras=CAMERAS,
                       bill=dict(file="Invoices/Ana Ruiz - Nov 2-4.pdf", currency="USD", total=225.0,
                                 visits=[visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "09:00", "12:00", 3, 25),
                                         visit("2026-11-04", "09:00", "12:00", 3, 25)]),
                       helper_events=ev("Ana Ruiz", "2026-11-02", ["09:00", "12:02"]) + ev("Ana Ruiz", "2026-11-04", ["09:01"]),
                       proof_error="surveillance index temporarily unavailable"),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Inconclusive"], ["2026-11-04", "Inconclusive"]],
                       calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C14 split shift on one date
    dict(id="C14", title="Split shift: two visits on one date",
         mode="check",
         user_message="Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2 split.pdf against the Front Door camera, New York time. "
                      "She knows about the camera.",
         fixtures=dict(cameras=CAMERAS,
                       bill=dict(file="Invoices/Ana Ruiz - Nov 2 split.pdf", currency="USD", total=100.0,
                                 visits=[visit("2026-11-02", "08:00", "10:00", 2, 25), visit("2026-11-02", "14:00", "16:00", 2, 25)]),
                       helper_events=ev("Ana Ruiz", "2026-11-02", ["07:58", "10:02", "13:55", "16:05"]), proof=[proof("2026-11-02", BUSY)]),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-02", "Confirmed"]], calls_forbidden=["save-text"])),

    # ---------------------------------------------------------------- C15 bill cannot be read
    dict(id="C15", title="Bill is unreadable: no visits invented",
         mode="check",
         user_message="Check Ana Ruiz's invoice Invoices/photo of invoice.jpg against the Front Door camera for Nov 2-8, "
                      "New York time. She knows about the camera.",
         fixtures=dict(cameras=CAMERAS,
                       bill=dict(file="Invoices/photo of invoice.jpg", currency=None, total=None, visits=[],
                                 failures=["page 1: image too blurry to read"]),
                       helper_events=ev("Ana Ruiz", "2026-11-02", ["09:00", "12:00"]), proof=[proof("2026-11-02", BUSY)]),
         user_script=dict(consent="Yes.", save="No.", snapshots="No.",
                          fallback="I don't have a better copy. What can we do?"),
         expected=dict(rows=[], must_contain_any=["Draft", "draft", "type", "typed"],
                       calls_forbidden=["identity-type known", "save-text"])),

    # ---------------------------------------------------------------- C16 typed hours, tolerance 15
    dict(id="C16", title="Typed hours with a 15-minute tolerance",
         mode="check",
         user_message="No invoice file: Ana Ruiz says she worked Mon Nov 2 9:00-12:00, Wed Nov 4 9:00-13:00 and Fri Nov 6 13:00-16:00. "
                      "Check that against the Front Door camera with a 15 minute tolerance, New York time. She knows about the camera.",
         fixtures=dict(cameras=CAMERAS,
                       helper_events=ev("Ana Ruiz", "2026-11-02", ["09:10", "11:52"]) + ev("Ana Ruiz", "2026-11-04", ["09:05", "12:50"])
                       + ev("Ana Ruiz", "2026-11-06", ["13:00", "16:12"]),
                       proof=[proof(d, BUSY) for d in ["2026-11-02", "2026-11-04", "2026-11-06"]]),
         user_script=dict(consent="Yes.", save="No.", snapshots="No."),
         expected=dict(rows=[["2026-11-02", "Billed more than seen"], ["2026-11-04", "Confirmed"], ["2026-11-06", "Confirmed"]],
                       must_contain=["18 min"], calls_forbidden=["ug-document", "ug-filesystem", "save-text"])),
]


def main():
    os.makedirs(os.path.join(HERE, "fixtures"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "expected"), exist_ok=True)
    for case in CASES:
        fx = dict(id=case["id"], mode=case["mode"], user_message=case["user_message"],
                  fixtures=case["fixtures"], user_script=case["user_script"])
        with open(os.path.join(HERE, "fixtures", case["id"] + ".json"), "w") as f:
            json.dump(fx, f, indent=1)
        with open(os.path.join(HERE, "expected", case["id"] + ".json"), "w") as f:
            json.dump(dict(id=case["id"], title=case["title"], **case["expected"]), f, indent=1)
    print(f"wrote {len(CASES)} cases")


if __name__ == "__main__":
    main()
