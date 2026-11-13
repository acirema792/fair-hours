---
name: fair-hours
description: Fair Hours compares hourly home-help bills (cleaners, nannies, home-care aides, tutors, dog walkers) with the arrival and departure events that the household's own entry cameras recorded on UGREEN AI NAS for that helper, visit by visit and in both directions, and drafts a timesheet from camera events when there is no bill. Use when the user asks to check a helper's invoice or timesheet against the door camera, asks how many hours a named helper was at the home in a period, or wants a draft timesheet for a helper to confirm.
---

# Goal

Give a household a fair, visit-by-visit answer to one question: do the hours on a helper's bill match the times the household's own entry cameras recognised that helper arriving and leaving? Fair Hours counts differences in both directions, so time the helper worked but did not bill is reported as clearly as billed time the cameras did not see. It also checks the bill's own arithmetic. When there is no bill, it drafts a timesheet from the camera events for both sides to confirm.

Fair Hours compares and explains. It never accuses, never decides what anyone owes, and never identifies a person from appearance. A camera gap, an arrival without a departure, an unrecognised person at the door, or a cut-off event list is reported as `Inconclusive`, never as a missed visit. Fair Hours itself calls no external service; which chat model Uliya uses to run it is a Uliya setting.

Reply in the language the user writes in. Keep CLI names, agent names and status values unchanged.

# Required input

Collect these before the first delegation. Ask once, in one short message, for anything required that is missing. Never guess a value. Tolerance and agreed terms are optional: never ask for them; use the default unless the user gives them.

1. **Mode**: `Check` (a bill or typed hours exist) or `Draft` (build a timesheet from camera events only).
2. **Helper name**: as the household registered the helper as a known face in the surveillance app. Step 1 confirms it. Fair Hours does not register, rename or guess faces.
3. **Period**: first and last date, and the household time zone. In Check mode with a bill file and no dates from the user, do not ask: after step 3, use the first and last billed dates and state them at the top of the report. With a bill folder and no dates, ask for the period.
4. **Bill** (Check mode only): a file the user names, a folder plus a hint such as the helper name, or hours typed by the user as date, start, end. Use a file name or path exactly as the user gives it, even a short one such as Care/invoice.pdf; ask for a fuller path only if step 3 reports that the file was not found.
5. **Entry cameras**: the cameras that cover the doors the helper uses. If the user names no camera or says "the door cameras", use every camera whose location in step 1 is an entrance, door or gate, and say which ones were used. Ask only if no camera has such a location.
6. **Tolerance**: minutes of difference treated as a match. Default 10. Optional **agreed terms**: a minimum visit length or a rounding unit.
7. **Notice**: the user confirms the helper knows the entry cameras recognise faces and may be used to check hours. If the user says no, explain that Fair Hours only works when the helper has been told, mention that some places require written consent for this, and stop before any camera query.

Value slots in the delegate instructions below are written in UPPER_CASE (HELPER_NAME, PERIOD_START, PERIOD_END, DATES, TIMEZONE, ENTRY_CAMERAS, BILL_FILE, BILL_FOLDER, NAME_HINT, SAVE_FOLDER, REPORT_TEXT, EVENT_IDS). Replace every slot with the confirmed value before sending. Never send an instruction that still contains an UPPER_CASE slot. Write dates as YYYY-MM-DD and times as HH:MM in TIMEZONE. PERIOD_START and PERIOD_END are the dates the user gave or, when the period comes from the bill, the first and last billed dates read in step 3. If any value contains a single quote (a name such as O'Brien, a file name, the report), write that quote with the standard shell sequence for a quote inside single quotes.

# Generation-time capability evidence

- `ug-surveillance` → `security-monitor-agent`
- `ug-document` → `document-agent`
- `ug-photo` → `photo-agent`
- `ug-filesystem` → `file-agent`
- `ug-knowledge` → `knowledge-agent`

Read-only steps: `ug-surveillance` cameras, faces, event-timeline and event-evidence; `ug-document` extract; `ug-photo` vision-ocr; `ug-filesystem` find. The only state change is the optional `ug-knowledge` save-text, which runs the platform approval workflow and is sent only after the user says yes.

# Workflow

Run the steps in order. Pass only the real result of each upstream step downstream. Read [references/privacy-and-fairness.md](references/privacy-and-fairness.md) before step 1, and [references/states-and-recovery.md](references/states-and-recovery.md) for how to handle each delegation state.

**Step 1. Cameras and helper (security-monitor-agent).**

`delegate --target security-monitor-agent --instruction 'Use ug-surveillance cameras to list all cameras with name, location and status. Read only. Do not return faces, plates or snapshots.'`

`delegate --target security-monitor-agent --instruction 'Use ug-surveillance faces with identity-type known to check whether exactly one known identity is named HELPER_NAME. Read only. Return yes or no, and if no, only the registered names that are closest to HELPER_NAME. Do not return images or details of anyone.'`

- If none of the named entry cameras appear, show the list and ask the user to choose. If there are no cameras, say Fair Hours needs at least one entry camera and stop.
- If a chosen camera's location is not an entrance, door or gate (a hallway included), ask the user to confirm it only covers a door; otherwise leave it out.
- A camera that is offline now is still used: recording during the period is judged in step 6 from steps 4 and 5.
- If no known identity matches HELPER_NAME, show the closest registered names and ask which one is meant; if none fits, tell the user to register the helper as a known face in the surveillance app, and stop.

**Step 2. Find the bill (file-agent).** Check mode only, and only when the user gave a folder instead of an exact file.

`delegate --target file-agent --instruction 'Use ug-filesystem find in the folder BILL_FOLDER for files whose name contains NAME_HINT or invoice or timesheet, modified from PERIOD_START to 30 days after PERIOD_END. Read only. Return each path with size and modified time. If there are no results, return an empty list and do not search any other folder.'`

If there are no results, tell the user no bill was found in that folder and offer Draft mode or typed hours; do not widen the search. If there are several, ask the user to pick one.

**Step 3. Read the billed visits (document-agent, then photo-agent if needed).** Check mode with a bill file only. Typed hours go straight to step 4.

`delegate --target document-agent --instruction 'Use ug-document extract with schema auto and content-scope full on the file BILL_FILE. Return one row per billed visit with date, start time, end time, billed hours, hourly rate, line amount, worker name and number of workers, plus the exact text each value was read from. Also return the bill total, currency and the period printed on the bill. Leave a value empty when it is not printed; do not compute or infer missing values. List any page or line that could not be read.'`

If the bill is a photo or scan and extract returns no readable visits, try once:

`delegate --target photo-agent --instruction 'Use ug-photo vision-ocr on the file BILL_FILE. Read only. Return the recognised text exactly as read, line by line.'`

From OCR text, use only dates, times, hours, rates and amounts that appear in it, and list the lines used at the top of the report; continue without waiting for a confirmation unless a date or time cannot be read. Keep only visits dated inside the period. If no billed visit can be read, say so and offer typed hours or Draft mode. Never invent a visit, a time or a rate.

**Step 4. Helper events (security-monitor-agent).**

`delegate --target security-monitor-agent --instruction 'Use ug-surveillance event-timeline from PERIOD_START 00:00 to 12:00 on the day after PERIOD_END in time zone TIMEZONE, for the cameras ENTRY_CAMERAS, with topic Human and HumanFace, identity-type known, person-name HELPER_NAME and limit 500. Return every event with its event id, local time, camera and the identity name exactly as recorded, and say whether the list was cut at the limit. Read only. Do not return events of any other person. Report any warning about missing recordings or offline cameras.'`

If the list was cut at the limit, repeat step 4 one week at a time; dates still cut become `Inconclusive` under the matching rules. An empty list is a real result: continue, because it feeds the rules in step 6.

**Step 5. Passages (security-monitor-agent).** Only for DATES: billed dates with no visit events, and billed dates where the bill is longer than the time seen by more than the tolerance. It proves the cameras were recording, and finds unrecognised people who might be the helper, without naming anyone.

`delegate --target security-monitor-agent --instruction 'Use ug-surveillance event-timeline in time zone TIMEZONE for the cameras ENTRY_CAMERAS on these dates only: DATES, with topic Human and HumanFace, identity-type all and limit 500. For each event return only its local time, its camera and whether the person was recognised as a known identity (yes or no). Do not return names, faces, plates, snapshots or other details. Say whether any list was cut at the limit, and report any warning about missing recordings or offline cameras.'`

**Step 6. Compare (no delegation).** Apply [references/matching-rules.md](references/matching-rules.md) exactly, including the bill arithmetic check. Every result comes from those rules and the real results of steps 3 to 5. Do the time arithmetic in whole minutes and show it.

**Step 7. Evidence for the user (security-monitor-agent).** Optional. Only for rows that are not `Confirmed` and have helper events, and only when the user asks. For rows without helper events, give the camera and the time window so the user can review the recording in the surveillance app.

`delegate --target security-monitor-agent --instruction 'Use ug-surveillance event-evidence for the events EVENT_IDS with evidence-type snapshot, max-items 2 per event and purpose user_review. Read only. Return the snapshot references for the user to review on the NAS. Do not export or share them.'`

**Step 8. Report.** Present the report in the chat using [references/report-format.md](references/report-format.md). Then ask whether to save it on the NAS. Only after a clear yes and a folder:

`delegate --target knowledge-agent --instruction 'Use ug-knowledge save-text to save the text REPORT_TEXT in the folder SAVE_FOLDER with filename-hint fair-hours HELPER_NAME PERIOD_START to PERIOD_END. Save only this text. Return verified, outputFile and contentBytes.'`

**Draft mode** runs steps 1, 4, 6 and 8. Each day with helper events becomes a draft line (first seen, last seen, span) under the Draft rules in the matching rules; a line with a single sighting is marked `Inconclusive`, with no hours.

# Completion and failure

- A step's result is used only after the expert returns `completed`. Treat `failed` and `cancelled` as stops for every step that needs that result; report what finished and what did not.
- `waiting_user`: relay the expert's question to the user word for word, wait, then resume the same step. Do not answer for the user.
- `waiting_approval`: only step 8 can reach this. Tell the user the save is waiting for their approval in the NAS approval prompt; report the save only after `completed` returns verified true and an output file.
- Empty results: no bill found, no billed visits read, no helper events, or no cameras are reported as such, with the next options; Fair Hours never fills a gap with similar or invented data and never widens the search on its own.
- Partial results: if step 5 fails, every visit that needed it becomes `Inconclusive` with the reason "recording not confirmed"; the rest of the report stands.
- The job is complete when the report has been shown, and, if the user asked to save it, the save returned `completed`. Fair Hours never says a report was saved, a snapshot was found or a camera was checked without that real result.

Other references: [references/validation-plan.md](references/validation-plan.md) lists the finalist test cases; [references/disclosures.md](references/disclosures.md) lists authorship, AI assistance and third-party components.
