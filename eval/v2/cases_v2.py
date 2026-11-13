"""Fair Hours case library v2 (written after audit round 1, before any v2 run).

Changes from v1 (eval/cases.py, left untouched as history):
- Fixtures now say, for every passage of another person, whether the platform recognised them (F1, F20).
- C03 corrected: an unrecognised passer inside the billed window may be the helper -> Inconclusive (audit F1;
  escalated because the v1 expected outcome encoded the defect). C03B keeps the `Not seen` path with only
  recognised passers.
- New regression cases C17-C24 for audit findings F3, F5, F6, F7, F9, F11, F12.
Blind cases written by a separate author who never saw the matching rules live in eval/v2/blind_cases.json.
`python3 eval/v2/cases_v2.py` writes eval/v2/fixtures/*.json and eval/v2/expected/*.json.
"""
import json
import os

TZ = "-05:00"
HERE = os.path.dirname(os.path.abspath(__file__))
CAMERAS = [{"name": "Front Door", "location": "Entrance", "status": "online"},
           {"name": "Garage Door", "location": "Garage entrance", "status": "online"},
           {"name": "Living Room", "location": "Living room", "status": "online"}]
KNOWN = ["Ana Ruiz", "Anabel Costa", "Grace Mensah", "Maya Chen", "Sam Okafor", "Jordan Okafor"]  # last two: household


def ev(helper, date, times, camera="Front Door"):
    return [{"event_id": f"evt_{date.replace('-', '')}_{t.replace(':', '')}", "time": f"{date}T{t}:00{TZ}",
             "camera": camera, "topic": "HumanFace", "identity": helper} for t in times]


def pas(date, times, recognised=True, camera="Front Door"):
    return [{"time": f"{date}T{t}:00{TZ}", "camera": camera, "recognised": "yes" if recognised else "no"} for t in times]


BUSY = ["07:30", "08:15", "10:40", "12:30", "15:10", "18:05"]  # household members, recognised


def busy(*dates):
    return [p for d in dates for p in pas(d, BUSY)]


def visit(date, start=None, end=None, hours=None, rate=None, amount=None, worker=None):
    row = {"date": date, "start": start, "end": end, "billed_hours": hours, "hourly_rate": rate,
           "line_amount": amount if amount is not None else (round(rate * hours, 2) if rate and hours else None)}
    if worker:
        row["worker_name"] = worker
    return row


def bill(file, visits, total=None, currency="USD", failures=None):
    return dict(file=file, visits=visits, currency=currency,
                total=total if total is not None else round(sum(v["line_amount"] or 0 for v in visits), 2),
                failures=failures or [])


YES = dict(consent="Yes, she knows the door camera recognises faces and that we may use it to check hours.",
           save="No, don't save it.", snapshots="No thanks.")


def case(id, title, mode, msg, fx, exp, script=None):
    fx.setdefault("cameras", CAMERAS)
    fx.setdefault("known_faces", KNOWN)
    return dict(id=id, title=title, mode=mode, user_message=msg, fixtures=fx, user_script=script or dict(YES), expected=exp)


A = "Ana Ruiz"
CASES = [
    case("C01", "Cleaner invoice: confirmed, billed more, seen more, single sighting", "check",
         "Check Ana Ruiz's cleaning invoice for Nov 2-8 against the Front Door camera. The invoice is the file "
         "Invoices/Ana Ruiz - Nov week 1.pdf. We're on New York time. Ana knows the door camera recognises faces and that we may check hours with it.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov week 1.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-04", "09:00", "13:00", 4, 25),
                                                                             visit("2026-11-05", "14:00", "17:00", 3, 25), visit("2026-11-06", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:04", "10:30", "11:58"]) + ev(A, "2026-11-04", ["09:10", "11:25"]) + ev(A, "2026-11-05", ["13:55", "15:00", "16:10", "17:40"]) + ev(A, "2026-11-06", ["09:02"]),
              passages=busy("2026-11-02", "2026-11-04", "2026-11-05", "2026-11-06")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-04", "Billed more than seen"], ["2026-11-05", "Seen more than billed"], ["2026-11-06", "Inconclusive"]],
              must_contain=["1 h 45 min", "45 min", "43.75", "18.75"], calls_forbidden=["save-text"])),
    case("C02", "Camera offline during a billed visit", "check",
         "Can you check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-3.pdf against the Front Door camera? New York time.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-3.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:01", "12:03"]), passages=busy("2026-11-02"),
              warnings=[{"date": "2026-11-03", "text": "Front Door offline from 2026-11-03 07:40 to 2026-11-03 14:10 (no recordings)."}]),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Inconclusive"]], consent_before_camera=True, calls_forbidden=["save-text"])),
    case("C03", "No helper events; an unrecognised person passed during the billed time", "check",
         "Please check the cleaning invoice Invoices/Ana Ruiz - Nov 2-5.pdf from Ana Ruiz against the Front Door camera. Time zone America/New_York. "
         "She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-5.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-05", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["08:58", "12:00"]),
              passages=busy("2026-11-02") + pas("2026-11-05", ["08:15", "12:30"]) + pas("2026-11-05", ["10:40"], recognised=False)),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-05", "Inconclusive"]], calls_forbidden=["save-text"])),
    case("C03B", "Not seen while the camera recognised other people", "check",
         "Please check the cleaning invoice Invoices/Ana Ruiz - Nov 2-5.pdf from Ana Ruiz against the Front Door camera. Time zone America/New_York. "
         "She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-5.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-05", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["08:58", "12:00"]), passages=busy("2026-11-02", "2026-11-05")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-05", "Not seen"]], must_contain=["3 h"], calls_forbidden=["save-text"])),
    case("C04", "Helper seen on a date that is not on the bill", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov week 1.pdf against the Front Door camera for Nov 2-8, New York time. "
         "She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov week 1.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-04", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:03", "12:01"]) + ev(A, "2026-11-04", ["08:57", "11:59"]) + ev(A, "2026-11-07", ["10:00", "11:45", "13:30"]),
              passages=busy("2026-11-02", "2026-11-04", "2026-11-07")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-04", "Confirmed"], ["2026-11-07", "Seen, not billed"]], must_contain=["3 h 30 min"], calls_forbidden=["save-text"])),
    case("C05", "Tolerance boundary: 10 minutes matches, 11 does not", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-3.pdf against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-3.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:05", "11:55"]) + ev(A, "2026-11-03", ["09:06", "11:55"]), passages=busy("2026-11-02", "2026-11-03")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Billed more than seen"]], must_contain=["11 min"], calls_forbidden=["save-text"])),
    case("C06", "Overnight home-care shifts crossing midnight", "check",
         "My mother's carer Grace Mensah billed two night shifts this week. Check the agency invoice Care/Grace Mensah - week 45.pdf against the Front Door camera, "
         "New York time. Grace knows the camera recognises faces and may be used to check hours.",
         dict(helper_name="Grace Mensah", bill=bill("Care/Grace Mensah - week 45.pdf", [visit("2026-11-03", "22:00", "06:00", 8, 30), visit("2026-11-05", "22:00", "06:00", 8, 30)]),
              helper_events=ev("Grace Mensah", "2026-11-03", ["21:55"]) + ev("Grace Mensah", "2026-11-04", ["06:05"]) + ev("Grace Mensah", "2026-11-05", ["22:20"]) + ev("Grace Mensah", "2026-11-06", ["05:30"]),
              passages=busy("2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06")),
         dict(rows=[["2026-11-03", "Confirmed"], ["2026-11-05", "Billed more than seen"]], must_contain=["50 min", "25.00"], calls_forbidden=["save-text"])),
    case("C07", "Bill lists hours only, no start or end times", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - hours.pdf for Nov 2-8 against the Front Door camera. New York time; she knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - hours.pdf", [visit("2026-11-02", hours=3.0, rate=25), visit("2026-11-04", hours=2.5, rate=25), visit("2026-11-06", hours=3.0, rate=25)]),
              helper_events=ev(A, "2026-11-02", ["09:00", "12:05"]) + ev(A, "2026-11-04", ["13:00", "14:10"]),
              passages=busy("2026-11-02", "2026-11-04") + pas("2026-11-06", ["16:00"])),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-04", "Billed more than seen"], ["2026-11-06", "Not seen"]], must_contain=["1 h 20 min"], calls_forbidden=["save-text"])),
    case("C08", "Helper has not been told about the face-recognising camera", "check",
         "Check our nanny Maya Chen's timesheet Documents/Maya timesheet Nov 2-6.pdf against the Front Door camera. New York time.",
         dict(helper_name="Maya Chen", bill=bill("Documents/Maya timesheet Nov 2-6.pdf", [visit("2026-11-02", "08:00", "16:00", 8, 15)]),
              helper_events=ev("Maya Chen", "2026-11-02", ["08:00", "16:00"]), passages=busy("2026-11-02")),
         dict(rows=[], max_delegations=0),
         script=dict(YES, consent="No, we haven't told her there's a camera at the door.")),
    case("C09", "Helper is not a registered known face", "check",
         "Check Lucy Park's dog-walking invoice Pets/Lucy Park Nov.pdf against the Front Door camera for Nov 2-6, New York time. Lucy knows the camera recognises faces and may be used to check hours.",
         dict(helper_name="Lucy Park", bill=bill("Pets/Lucy Park Nov.pdf", [visit("2026-11-02", "12:00", "13:00", 1, 20), visit("2026-11-04", "12:00", "13:00", 1, 20)]),
              helper_events_error="person-name 'Lucy Park' does not match any known identity", passages=busy("2026-11-02", "2026-11-04")),
         dict(rows=[], must_contain_any=["register", "known face", "known identity", "known person"], calls_forbidden=["save-text", "event-evidence", "event-timeline"])),
    case("C10", "Draft timesheet from camera events (no bill)", "draft",
         "Our nanny Maya Chen doesn't keep a timesheet. Can you draft one for Nov 2-6 from the Front Door camera? New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name="Maya Chen", helper_events=ev("Maya Chen", "2026-11-02", ["08:00", "15:30"]) + ev("Maya Chen", "2026-11-03", ["08:05", "12:00", "15:35"]) + ev("Maya Chen", "2026-11-04", ["08:10"]),
              passages=busy("2026-11-02", "2026-11-03", "2026-11-04", "2026-11-05", "2026-11-06")),
         dict(rows=[["2026-11-02", "Draft"], ["2026-11-03", "Draft"], ["2026-11-04", "Inconclusive"]], must_contain=["15 h"], calls_forbidden=["ug-document", "ug-filesystem", "save-text"])),
    case("C11", "No bill found in the folder the user named", "check",
         "Check Ana Ruiz's latest invoice against the Front Door camera for Nov 2-8. It should be somewhere in Documents/Invoices. New York time; she knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, find_results=[], helper_events=[], passages=[]),
         dict(rows=[], must_contain_any=["Draft", "draft", "type", "typed"], max_calls={"ug-filesystem find": 1}, calls_forbidden=["ug-document", "save-text"])),
    case("C12", "Save goes to the NAS approval prompt (period taken from the bill)", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2.pdf against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:02", "11:59"]), passages=busy("2026-11-02"), save_state="waiting_approval"),
         dict(rows=[["2026-11-02", "Confirmed"]], must_contain_any=["approval", "approve"],
              must_not_match=[r"(?i)\b(has been|was|is now|successfully) saved\b", r"(?i)\bsaved (it )?(to|in)\b"], save_after_user_yes=True),
         script=dict(YES, save="Yes, please save it in Documents/Household.", other="Yes, please also save the report in Documents/Household.")),
    case("C13", "Passages query fails", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-4.pdf against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-4.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "09:00", "12:00", 3, 25), visit("2026-11-04", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:00", "12:02"]) + ev(A, "2026-11-04", ["09:01"]), passages_error="surveillance index temporarily unavailable"),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Inconclusive"], ["2026-11-04", "Inconclusive"]], calls_forbidden=["save-text"])),
    case("C14", "Split shift: two visits on one date", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2 split.pdf against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2 split.pdf", [visit("2026-11-02", "08:00", "10:00", 2, 25), visit("2026-11-02", "14:00", "16:00", 2, 25)]),
              helper_events=ev(A, "2026-11-02", ["07:58", "10:02", "13:55", "16:05"]), passages=busy("2026-11-02")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-02", "Confirmed"]], calls_forbidden=["save-text"])),
    case("C15", "Bill is unreadable even by OCR: no visits invented", "check",
         "Check Ana Ruiz's invoice Invoices/photo of invoice.jpg against the Front Door camera for Nov 2-8, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/photo of invoice.jpg", [], total=None, currency=None, failures=["page 1: image too blurry to read"]),
              ocr_text="", helper_events=ev(A, "2026-11-02", ["09:00", "12:00"]), passages=busy("2026-11-02")),
         dict(rows=[], must_contain_any=["Draft", "draft", "type", "typed"], calls_forbidden=["identity-type known", "save-text"]),
         script=dict(YES, other="I don't have a better copy. What can we do?")),
    case("C16", "Typed hours with a 15-minute tolerance", "check",
         "No invoice file: Ana Ruiz says she worked Mon Nov 2 9:00-12:00, Wed Nov 4 9:00-13:00 and Fri Nov 6 13:00-16:00. Check that against the Front Door camera with a 15 minute tolerance, "
         "New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, helper_events=ev(A, "2026-11-02", ["09:10", "11:52"]) + ev(A, "2026-11-04", ["09:05", "12:50"]) + ev(A, "2026-11-06", ["13:00", "16:12"]),
              passages=busy("2026-11-02", "2026-11-04", "2026-11-06")),
         dict(rows=[["2026-11-02", "Billed more than seen"], ["2026-11-04", "Confirmed"], ["2026-11-06", "Confirmed"]], must_contain=["18 min"], calls_forbidden=["ug-document", "ug-filesystem", "save-text"])),
    # ---------------- regression cases for audit round 1
    case("C17", "Consecutive night shifts share no events (F5)", "check",
         "Check Grace Mensah's agency invoice Care/Grace Mensah - nights.pdf against the Front Door camera, New York time. Grace knows the camera recognises faces and may be used to check hours.",
         dict(helper_name="Grace Mensah", bill=bill("Care/Grace Mensah - nights.pdf", [visit("2026-11-03", "22:00", "06:00", 8, 30), visit("2026-11-04", "22:00", "06:00", 8, 30)]),
              helper_events=ev("Grace Mensah", "2026-11-03", ["21:58"]) + ev("Grace Mensah", "2026-11-04", ["06:03", "21:57"]) + ev("Grace Mensah", "2026-11-05", ["06:04"]),
              passages=busy("2026-11-03", "2026-11-04", "2026-11-05")),
         dict(rows=[["2026-11-03", "Confirmed"], ["2026-11-04", "Confirmed"]], calls_forbidden=["save-text"])),
    case("C18", "Departure not recognised: an unrecognised person left near the billed end (F6)", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 3.pdf against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 3.pdf", [visit("2026-11-03", "09:00", "13:00", 4, 25)]),
              helper_events=ev(A, "2026-11-03", ["09:02", "11:00"]), passages=busy("2026-11-03") + pas("2026-11-03", ["12:58"], recognised=False)),
         dict(rows=[["2026-11-03", "Inconclusive"]], calls_forbidden=["save-text"])),
    case("C19", "Agreed minimum visit and rounding explain the differences (F7)", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - terms.pdf against the Front Door camera, New York time. Our agreement is a 3-hour minimum per visit, "
         "and time is rounded up to the half hour. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - terms.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-03", "09:00", "11:30", 2.5, 25), visit("2026-11-04", "13:00", "16:30", 3.5, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:00", "11:20"]) + ev(A, "2026-11-03", ["09:05", "11:10"]) + ev(A, "2026-11-04", ["13:00", "15:10"]),
              passages=busy("2026-11-02", "2026-11-03", "2026-11-04")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Confirmed"], ["2026-11-04", "Billed more than seen"]], must_contain=["1 h 20 min"], calls_forbidden=["save-text"])),
    case("C20", "Bill arithmetic errors are listed (F7)", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-3 v2.pdf against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-3 v2.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25, amount=80.0), visit("2026-11-03", "09:00", "12:00", 3, 25)], total=165.0),
              helper_events=ev(A, "2026-11-02", ["09:01", "12:00"]) + ev(A, "2026-11-03", ["08:59", "12:02"]), passages=busy("2026-11-02", "2026-11-03")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Confirmed"]], must_contain=["80", "165", "155"], calls_forbidden=["save-text"])),
    case("C21", "Photographed handwritten timesheet read by OCR (F12)", "check",
         "Check our nanny Maya Chen's timesheet Timesheets/maya-week.jpg against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name="Maya Chen", bill=bill("Timesheets/maya-week.jpg", [], total=None, currency=None, failures=["handwriting could not be read"]),
              ocr_text="TIMESHEET Maya Chen\nMon 11/2  8:00 - 4:00  8 h\nTue 11/3  8:00 - 4:00  8 h\nTotal 16 h",
              helper_events=ev("Maya Chen", "2026-11-02", ["07:58", "16:03"]) + ev("Maya Chen", "2026-11-03", ["08:00", "14:00"]),
              passages=busy("2026-11-02", "2026-11-03")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-03", "Billed more than seen"]], must_contain=["2 h"], calls_required=["vision-ocr"], calls_forbidden=["save-text"])),
    case("C22", "Helper event list cut at the limit (F11)", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2-5.pdf against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2-5.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25), visit("2026-11-05", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:00", "12:00"]) + ev(A, "2026-11-05", ["09:00", "12:00"]), helper_cut_after="2026-11-03 18:00",
              passages=busy("2026-11-02", "2026-11-05")),
         dict(rows=[["2026-11-02", "Confirmed"], ["2026-11-05", "Inconclusive"]], calls_forbidden=["save-text"])),
    case("C23", "User gives a short name; the registered name is confirmed first (F3)", "check",
         "Check Ana's cleaning invoice Invoices/Ana Ruiz - Nov 2.pdf against the Front Door camera, New York time. She knows the camera recognises faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:02", "11:59"]), passages=busy("2026-11-02")),
         dict(rows=[["2026-11-02", "Confirmed"]], calls_forbidden=["save-text"]),
         script=dict(YES, name="Yes, Ana Ruiz is the one I mean.", other="I mean Ana Ruiz.")),
    case("C24", "A chosen camera is not at an entrance (F9)", "check",
         "Check Ana Ruiz's invoice Invoices/Ana Ruiz - Nov 2.pdf against the Living Room camera, New York time. She knows the cameras recognise faces and may be used to check hours.",
         dict(helper_name=A, bill=bill("Invoices/Ana Ruiz - Nov 2.pdf", [visit("2026-11-02", "09:00", "12:00", 3, 25)]),
              helper_events=ev(A, "2026-11-02", ["09:02", "11:59"]), passages=busy("2026-11-02")),
         dict(rows=[["2026-11-02", "Confirmed"]], calls_forbidden=["save-text"], event_cameras_forbidden=["Living Room"]),
         script=dict(YES, camera_choice="Oh, the living room camera doesn't cover a door. Use the Front Door camera instead.",
                     other="Use the Front Door camera instead.")),
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
