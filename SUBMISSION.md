# Devpost submission: copy-paste fields

Round 1 closes **Sun 2026-11-15 23:45 PT** (Mon 02:45 in GMT-5). Submit by Sunday afternoon PT, two or more hours early.

## Files to upload

| Field | File | Limit | Status |
|---|---|---|---|
| Project Proposal (PDF) | `proposal/Fair-Hours-Round1-Proposal.pdf` | ≤1 MB, ≤500 words over the ten answers | built by `proposal/build_proposal.py` (word count printed) |
| Pre-test Skill Package (ZIP) | `dist/fair-hours.zip` | ZIP and unzipped ≤10 MB, ≤1 MB per file, ≤100 files | built by `tools/build_zip.py` (checker static-pass, re-checked after unzip) |
| Thumbnail / gallery image | `docs/assets/cover.png` (1500×1000, 3:2) | 5 MB | rendered |

## Project name

Fair Hours

## Elevator pitch (≤200 characters)

Checks a home helper's hourly bill against when your own door camera recognised them, visit by visit, both ways, on your UGREEN AI NAS. Every doubt goes to the helper.

## Track

Explore Your Imagination (the Devpost label for the rules' Open Innovation track)

## About the project

### Inspiration
Millions of households pay a cleaner, nanny, dog walker or home-care aide by the hour, and the bill arrives every week. Families either trust it blindly or keep paper logs. Medicaid has had to verify home-care visits electronically since the 21st Century Cures Act; families who pay privately have nothing similar. Meanwhile many of those homes already have a door camera that recognises faces and stores the footage on their own NAS.

### What it does
You tell Uliya: *"Check Ana's cleaning invoice against the front door camera."* Fair Hours reads the bill, pulls only Ana's recognised arrivals and departures from your entrance cameras, and gives each billed visit one result: **Confirmed**, **Billed more than seen**, **Seen more than billed**, **Not seen**, **Inconclusive** or **Seen, not billed**. The totals for the two directions are shown side by side, priced at the printed rates and never netted. Bill arithmetic errors are flagged. With no bill, it drafts a timesheet from the camera for both sides to confirm.

**Every doubt goes to the helper.** Any of the following makes a visit Inconclusive, never Not seen: a camera gap, an arrival without a departure, an unrecognised person at the door near the billed times, or a cut-off event list. Not seen requires the camera to have recognised *other* people during the billed time while never seeing the helper.

### How we built it
- Fair Hours is a Markdown-only Uliya orchestration Skill built with the official UGOS Skill Creation Tool (uliya-skill-kit 0.7.3, catalog 2.0.0).
- It uses five registered experts: security-monitor-agent (cameras, faces, event-timeline, event-evidence), file-agent, document-agent, photo-agent (OCR for photographed timesheets) and knowledge-agent (an approval-gated save).
- An 11-rule table decides every result. The model only applies the rules and explains them.
- Other people at the door are used only as anonymous passages (time, camera, recognised yes/no), never names.
- A notice gate stops before any camera query if the helper hasn't been told the cameras recognise faces and may be used to check hours.
- To test it before NAS access, we built an offline bench: mock NAS experts, a scripted user, and expected outcomes committed before any run. It has 35 cases, 6 of them written blind by a separate author who never saw the rules. The same model following Fair Hours made 0 harmful calls and got 31/35 cases fully right. Without the rules, given the same tools and policies, it made 8 harmful calls and got 13/35.

### Challenges
The hard part was fairness. Our first rules would have called a visit "Not seen" when someone unrecognised passed the door during the billed time, but that person could have been the helper with her face turned away. An independent audit caught it. The fix runs the other way: unrecognised passages now count *for* the helper. Blind cases caught two more gaps: an agency substitute's line was hidden, and "the door cameras" led to an unnecessary question.

### Accomplishments
- The official checker passes with 0 errors and 0 warnings.
- Zero harmful calls across the bench, including the blind cases.
- Every billed hour appears in the report, in one direction or the other or as Inconclusive with a reason.

### What we learned
For a Skill that touches people's pay, "Inconclusive" is a feature. The rules have to make it hard to be wrong *against* someone, and easy to show the evidence.

### What's next
- Finalist day on a real iDX6011 Pro: confirm parameter behaviour, outage warnings and recognition on departures.
- Then a weekly scheduled check, and a shareable summary that the household and the helper can both confirm.

## Built with

uliya, ugos, ugreen-ai-nas, markdown, python (offline bench only)

## Links

- Repository: https://github.com/acirema792/fair-hours (optional for Round 1)
