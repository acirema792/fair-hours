# Validation plan

What has been checked before NAS access, and what the finalist testing day will check on a real UGREEN AI NAS.

## Before NAS access

- The package passes the official static checker from the UGREEN Skill Developer Package (uliya-skill-kit 0.7.3, catalog 2.0.0) with no errors and no warnings.
- The matching rules were replayed on a synthetic case library, including cases written blind by a separate author: stand-in experts return fixed camera events and bills, a model follows this Skill, and a scorer compares each row's result with the result written down before the run. A baseline run with the same model and tools but without these rules is scored the same way. The cases, runs and scores are kept in the entrant's test bench outside this package.

## Assumptions the testing day must confirm

1. `ug-surveillance event-timeline` accepts `person-name`, `identity-type known` and `all`, and `limit`, and says when a list is cut.
2. What event-timeline returns for a name that is not a known identity, and whether it reports offline cameras or missing recordings.
3. How often the test helper shows up as unrecognised on departures.
4. `ug-knowledge save-text` goes through `waiting_approval` and returns verified with an output file.

## Setup on the testing day

The day is remote. Before November 22, ask UGREEN through the Community whether the assigned NAS has a camera and a face library. Then:

- **If the NAS has a camera:** register a team member (or a UGREEN contact who agrees) as a known face named "Test Helper", and agree planned walk-past times. Write the true times down.
- **If not, and adding a camera is allowed:** add a team-owned camera that the NAS can reach, pointed at a team member, and register that face.
- **If no camera can be used:** run the document, OCR, bill arithmetic, empty-result and save steps for real, and the camera steps against the NAS's real "no cameras" response, and say so in the video.

Put a one-page test invoice (PDF) and a phone photo of a handwritten timesheet in a test folder, with lines written to produce each result below.

## Core test 1: Check mode with a PDF bill

Say: "Check Test Helper's invoice in the test folder against the front door camera for today."
Expected: the bill is read; lines give `Confirmed`, `Billed more than seen`, `Seen more than billed`, `Not seen` (a billed hour in which other recognised people passed but the helper did not) and `Inconclusive` (one walk-past only); a deliberate arithmetic error is listed; totals in both directions; the save asks for approval and returns a verified file.

## Core test 2: Draft mode from a photographed timesheet day

Say: "How long was Test Helper here today? Make a draft timesheet." Then repeat Check mode with the photographed timesheet.
Expected: one draft line per sighting window, labelled as a draft for both sides to confirm; no hours on single sightings; the photographed sheet is read through vision-ocr and its lines shown before comparing.

## Edge test: camera offline or person unrecognised during a billed visit

Disable the entry camera for 30 minutes and add an invoice line inside that window; in a second line, walk past with the face turned away.
Expected: both lines are `Inconclusive` ("recording not confirmed" and "someone unrecognised passed the entry"), never `Not seen`; the other lines are unchanged.

## Also checked

- A helper name that is not a known identity stops the run before any event query.
- Saying the helper has not been told about the face-recognising cameras stops the run before any camera query.
- Declining the save leaves no file; the report stays in the chat.
