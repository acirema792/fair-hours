# Validation plan

What has been checked before NAS access, and what the finalist testing day will check on a real UGREEN AI NAS.

## Before NAS access

- The package passes the official static checker from the UGREEN Skill Developer Package (uliya-skill-kit 0.7.3, catalog 2.0.0) with no errors and no warnings.
- The matching rules were replayed on a synthetic case library: stand-in experts return fixed camera events and bills, a model follows this Skill, and a scorer compares each row's result with the result written down before the run. The case list and scores are in the entrant's public test bench, outside this package.

## Setup on the testing day

1. Register a team member as a known face named "Test Helper" in the surveillance app, and pick one entry camera.
2. Walk past the entry camera at planned times over the testing day, writing down the true times.
3. Put a one-page test invoice (PDF) in a test folder, with lines written to produce each result below.

## Core test 1: Check mode with a PDF bill

Say: "Check Test Helper's invoice in the test folder against the front door camera for today."
Expected: the bill is found and read; four lines give `Confirmed`, `Billed more than seen`, `Seen more than billed` and `Inconclusive` (one walk-past only); totals in both directions; the save asks for approval and returns a verified file.

## Core test 2: Draft mode

Say: "How long was Test Helper here today? Make a draft timesheet."
Expected: one draft line per sighting window with first seen, last seen and time between, labelled as a draft for both sides to confirm; no hours on single sightings.

## Edge test: camera offline during a billed visit

Unplug or disable the entry camera for 30 minutes and add an invoice line inside that window.
Expected: that line is `Inconclusive` with "recording not confirmed", never `Not seen`; the other lines are unchanged.

## Also checked

- A helper name that is not a known identity stops the run before any comparison.
- Saying the helper does not know about the cameras stops the run before any camera query.
- Declining the save leaves no file; the report stays in the chat.
