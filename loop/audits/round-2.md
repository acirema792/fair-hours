# Fair Hours: independent audit, round 2

Auditor: independent and read-only. This file is the only one written by hand. Date 2026-11-13 UTC.
Inputs read: event-brief.md, loop-constraints.md, gate.yaml, loop/audits/round-1.md, loop/STATE.md, skill/fair-hours/** (7 files), proposal/proposal.md and build_proposal.py, README.md, JUDGES.md, SUBMISSION.md, BENCHMARK-RESULTS.md, eval/v2/** (mocks, scorer, MISSES.md, RUNNER_v2.md, fixtures, expected files, recorded runs), tools/make_benchmark_md.py, tools/build_zip.py, the reduced catalog.

## Commands run

- `python3 eval/v2/test_mocks.py` -> `ALL ROUTES OK`. Every SKILL.md template routes to the intended mock branch. Only Skill-shaped instructions are tested; see G1.
- `python3 tools/make_benchmark_md.py` -> regenerated BENCHMARK-RESULTS.md and proposal/values.json: `{"N_CASES": 31, "SKILL_HARM": 0, "BASE_HARM": 13, "SKILL_PASS": "30/31", "BASE_PASS": "3/31"}`. Fair Hours main 24/25 (rows 46/46), blind 6/6 (20/20). Baseline main 3/25 (29/46, 7 false `Not seen`, 2 false `Confirmed`), blind 0/6 (12/20, 4 false `Not seen`).
- `python3 proposal/build_proposal.py --allow-placeholders` -> `words in the ten answers: 478 / 500`, PDF 182,971 bytes, 3 pages. An independent count gives 489 whitespace tokens, or 482 tokens that contain a letter or digit. If hyphenated CLI names are split into separate words, the count is 514. The margin is thin but acceptable.
- That command rebuilt the PDF. **The committed PDF it replaced (HEAD, created 00:29 UTC) contained unfilled placeholders**: `{{BASE_HARM}} harmful calls; with them, {{SKILL_HARM}}`, `{{N_CASES}} cases`, `{{ENTRANT_NAME}}`, `{{SIGNATURE}}, {{DATE}}` (pdftotext lines 43-44, 67, 86, 88). See G4.
- `ULIYA_SKILL_KIT=.../tools/uliya-kit-local python3 tools/build_zip.py` -> checker `static-pass` 0/0/0. 7 files, 33,357 B unzipped, largest file 12,660 B, ZIP 14,723 B. The unzipped copy re-checks as static-pass. **The ZIP and SHA256SUMS are byte-identical to the committed ones.** The description is 529 characters (limit 1,024). PASS.
- I scored each run variant separately (make_benchmark_md.score per variant), then replayed every baselinehaiku log through `mock_delegate.route` to see what the baseline was actually given.
- Working tree before the audit: `tools/make_benchmark_md.py` was modified and `eval/v2/runs/baselinehaiku/` was untracked. Neither was committed (G10). This audit's commands changed BENCHMARK-RESULTS.md, proposal/values.json and the proposal PDF and HTML.

## F1–F22 verification

| # | Status | Evidence (current files) |
|---|---|---|
| F1 unrecognised face -> `Not seen` | FIXED | Step 5 returns a recognised yes/no flag per passage (SKILL.md:77). Rule 9 gives `Inconclusive` for an unrecognised passage in the billed window (matching-rules.md:33). v2 C03 expects Inconclusive, and C03B covers the `Not seen` path (skillhaiku-final/C03 and C03B both correct). |
| F2 recording proof too weak | PARTIAL | Proof now has to fall inside the billed window (matching-rules.md:15). But a single passage, on *any* of the chosen entry cameras, still proves recording for the whole window and every camera. Outage warnings are consulted only for rules 10/11, not for the `Billed more than seen` path (G2, G3). validation-plan.md:12-13 now lists outage warnings as an assumption. |
| F3 misspelled or unregistered name | FIXED | Step 1 checks the name with `faces` (SKILL.md:46,51). Rule 2 is a global guard (matching-rules.md:26). Unlike the suggested fix, it uses `faces` and not `identity-resolve`. Neither is schema-verified. |
| F4 ordering and window bug from F0 | FIXED (new defect introduced) | With a folder and no dates, the Skill now asks (SKILL.md:20). Step 4 runs to 12:00 the day after PERIOD_END (SKILL.md:71). That extension created G5: events after the period are counted. |
| F5 overnight double count | FIXED | Each event is assigned to one visit only (matching-rules.md:9). C17 is correct (skillhaiku-final2/C17). |
| F6 departures seen from behind | FIXED | Step 5 also runs for dates with D > T (SKILL.md:75), and rule 6 applies (matching-rules.md:30). C18 is correct. |
| F7 bill arithmetic and agreed terms | PARTIAL | Arithmetic (matching-rules.md:43-45), agreed terms (SKILL.md:23, rule 5). Printed hours are never checked against printed start/end (G6). `ug-document reconcile` is still unused, which is acceptable. |
| F8 undeliverable snapshots | FIXED | SKILL.md:81, report-format.md:30, privacy-and-fairness.md:10. |
| F9 entry cameras only | PARTIAL | A non-entrance camera needs the user's confirmation (SKILL.md:49), and C24 is correct. But "hallway", an indoor location, is treated as an entrance and is used by default (SKILL.md:22,49; G12). |
| F10 notice wording | FIXED | SKILL.md:24, privacy-and-fairness.md:15. |
| F11 limit 500 / over-collection | FIXED (residual) | DATES slot (SKILL.md:75-77), week split (SKILL.md:73), rule 1 (matching-rules.md:25). Rule 1 assumes the list is returned in ascending order (G11). |
| F12 photographed timesheets | FIXED | SKILL.md:63-67. C21 is correct. |
| F13 Draft overnight | FIXED | matching-rules.md:60, report-format.md:39. |
| F14 "never sends anything off the NAS" | PARTIAL (G13) | Qualified in privacy-and-fairness.md:26 and disclosures.md:13. Still unqualified in SKILL.md:10 ("sends nothing off the NAS"), README.md:3 ("camera footage and bills never leave the NAS"), proposal.md:25 ("faces, bills and reports stay local") and proposal.md:33 ("no external services"). Bill rows and the report text pass through the orchestrating chat model. |
| F15 quoting covers every slot | FIXED | SKILL.md:26. |
| F16 several rates | FIXED | matching-rules.md:56. |
| F17 camera offline now | FIXED | SKILL.md:50. |
| F18 agency workers and crews | FIXED (residual) | matching-rules.md:7, report-format.md:17. B05 is correct. For crews, "B is per person", so the Billed total understates billed crew hours (G17). |
| F19 baseline lacked defaults; scorer bugs | FIXED | The baseline now gets the policies (RUNNER_v2.md:26). The v2 scorer parses "3 Nov" (score_v2.py:28-30) and handles negation (score_v2.py:110). New baseline-fairness problems are G1 and G9. |
| F20 mock shaped to the Skill | PARTIAL | Window and camera filtering exist (mock_delegate.py:45-55,72-100). The scripted user answers "I don't know" (mock_user.py:43). But the mock still answers only Skill-shaped queries correctly (G1). |
| F21 circular, n=1, stale, not blind | PARTIAL | 6 blind cases were added and a small stand-in model (Haiku) was used. Still n=1 per case, no repeats and no spread. Two blind cases were used to tune the Skill and then re-run (MISSES.md, SUBMISSION.md:44). The regression cases C17-C24 come from the same author as the fixes. Only failing cases were re-run on the final text (G7). |
| F22 finalist plan infeasible remotely | FIXED | validation-plan.md:17-23 (camera contingency and no-camera fallback). `Not seen` is now in core test 1 (validation-plan.md:30). |

Tally: 16 FIXED (F4, F11 and F18 with residuals; F4's fix introduced G5), 6 PARTIAL (F2, F7, F9, F14, F20, F21), 0 NOT FIXED.

## Bench evidence: is the headline (30/31, 0 harmful vs 3/31, 13 harmful, both Haiku) fair?

### What holds up
- The Skill side does not rely on a scorer loophole. Across the 31 headline cases there are 0 false `Not seen`, 0 false `Confirmed` and 0 unapproved saves. All 66 rows are correct. I read 7 logs in full (C01, C03, C03B, C17 old and new, B02 old and new, C22). Each followed the step order, sent every slot resolved, made a single step-5 query only for the needed DATES, and did not save after "No".
- The one Skill miss, C15, is a real scorer artifact. The case's `calls_forbidden: identity-type known` also matches the legitimate step-1 `faces` check, as MISSES.md says.
- Expected outcomes predate the v2 runs (commit 05b305c).

### What makes the headline misleading
1. **8 of the baseline's 13 harmful errors come from runs where the mock never gave the baseline the helper's events** (G1). Replaying every baselinehaiku log through `mock_delegate.route`:
   - `identity-type all` always returns the anonymous `passages` fixture, with no names and **without the helper's own events** (mock_delegate.py:73-89). On a real NAS, "all identities" would include the helper. The baseline asked for identities in that call in B02 seq 4 ("Return ... (date, time, camera, identity)"), C01 seq 4-6 and C17 seq 5 ("identity-type all, person-name "Grace Mensah""). It got only `recognised: yes` rows.
   - A delegation that names several actions is answered with only the first action, still with state `completed` (`action = re.search(r"ug-surveillance\s+([a-z-]+)")`, mock_delegate.py:69). In B02 seq 2, a request for cameras, faces and event-timeline returned only the camera list. In seq 3, faces plus event-timeline returned only the face match. The baseline had no way to know its timeline request was dropped.
   - Per case, the baseline's harmful rows: B02 (3), C17 (2), C01 (1), C03 (1) and C23 (1) came from runs that never received a single helper event. That is 8 of 13. The remaining 5 are genuine baseline reasoning errors: C05 (11 min treated as within a 10-min tolerance), C16, C24 (Living Room), C09 (unregistered name) and B05 (substitute line marked `Not seen`).
   - The Skill is not affected. Its step 5 runs only on dates with no helper events, or reads only the `recognised` flag, so a mock that also returned the helper under `identity-type all` would not change any Skill result.
2. **3/31 "cases fully correct" for the baseline is a format artifact for 4 cases** (G9). The baseline prompt asks it to present a camera timesheet table (RUNNER_v2.md:28), and the parser counts those rows as `Draft` rows (score_v2.py:58,69-71). After dropping the stray Draft rows, C04, C06, C07 and C21 are fully correct with no other failure. C19 fails only on the exact string "1 h 20 min". A fairer baseline figure is 7/31, or 8/31 with C19.
3. **The "final text" headline mixes texts and re-runs only the failures** (G7). skillhaiku-final ran on the text before commit 6b6d47d and scored 28/31. Then one sentence was added to SKILL.md:21, and only B02, C17 (both failures) and C01 were re-run in skillhaiku-final2. Those three are merged over the originals (make_benchmark_md.py:72, `merged()` at :38-44). The other 28 were never run on the submitted text. Failures got a second draw and passes did not. The Sonnet "6/6 blind" row works the same way: B02 and B05 failed first (4/6), then the Skill was changed and both were re-run.
4. **The blind set is no longer blind.** B02 and B05 changed the Skill (MISSES.md "Blind-case findings that changed the Skill"; SUBMISSION.md:44). The unbiased first-run blind figures were Sonnet 4/6 on 7b28266 and Haiku 5/6 (skillhaiku, earlier text). They appear nowhere in the headline.
5. **Leakage into the showcase case** (G8). report-format.md:12-15 is the worked answer to case C01, with the same dates, the same billed times (09:00-12:00, 09:00-13:00, 14:00-17:00, 09:00-12:00), the same helper event times (09:04/11:58, 09:10/11:25, 13:55/17:40, 09:02) and the same four results. The Haiku and Sonnet C01 outputs reproduce it string for string ("09:04–11:58 (2 h 54 min)", "billed 1 h 45 min more than seen"). C01 is the "sample report from a real bench run" (README.md:36-38, JUDGES.md:7) and is counted in the headline.
6. Still n=1 per case, with no spread. The proposal (proposal.md:25) gives "13 vs 0" with no denominator, model, or note that the bench is synthetic in that sentence. Q8 (proposal.md:37) only says "offline bench".

## Scores (Round 1 judge view: PDF + ZIP, bench as cited evidence)

| Criterion | Score | Evidence |
|---|---|---|
| User Value | 7.5 (was 6.5) | The flow is clear and the problem is clear (SKILL.md:8, proposal.md:7-15). The report is useful in both directions, priced per line rate and never netted (matching-rules.md:47-56, report-format.md:19-30). New: bill arithmetic, agreed minimum and rounding terms (rule 5), crews and substitutes (matching-rules.md:7), OCR for photographed sheets (SKILL.md:63-67) and overnight drafts (matching-rules.md:60). Still missing: printed hours vs printed times, the commonest padding, is never checked (G6). Next-morning events outside the period inflate "Seen more than billed" (G5). The audience is still narrow: entry cameras plus the helper registered as a known face (proposal.md:45). |
| Innovation & Differentiation | 7.5 (was 7.0) | The only entry in the field that reconciles hourly home-help bills with camera events (event-brief.md:40). Anonymous passages as recording proof, unrecognised passages counted *for* the helper (matching-rules.md:14,30,33) and two-direction totals are real interaction ideas, not a wrapper. The core is still face-recognition attendance against a timesheet, and the A/B claim of differentiation is inflated (G1). |
| Technical Quality | 7.0 (was 6.0) | Strong template discipline: nine single-action templates, a slot list and a quoting rule (SKILL.md:26). A per-step state table (states-and-recovery.md:5-14). An approval-gated single write (SKILL.md:85-87,95). Checker 0/0 and a reproducible ZIP. Haiku follows it cleanly (66/66 rows). Holes remain. An outage warning near a departure still gives `Billed more than seen`, a verdict against the helper (G2). Recording proof rests on one passage on any camera (G3). Truncation logic assumes ascending order (G11). Events after the period are counted (G5). Optional inputs make a small model stall (G14; seen in skillhaiku-final/C17 and B02). No parameter name can be checked against the reduced catalog. |
| AI NAS Fit & Validation | 6.5 (was 6.0) | Good local fit: on-device face identities, local bills, NAS OCR and an approval-gated save (README.md:53-61). A credible finalist plan with a camera contingency and a no-camera fallback (validation-plan.md:17-23) and explicit NAS-only assumptions (validation-plan.md:10-15). The validation evidence is weaker than presented. 8 of the 13 baseline harmful errors are mock artifacts (G1). The "final text" figure re-ran only the failures (G7). The blind set was used for tuning (G7). The showcase case is answered verbatim inside the Skill (G8). n=1 per case. The committed PDF shipped unfilled placeholders (G4). |

OVERALL_SCORE=7.1

## New findings

Severity: S3 = high, S2 = medium, S1 = low (same scale as round 1). Protected paths (gate.yaml): eval/cases.py, eval/expected/**, eval/fixtures/**, eval/runs/**, eval/results/**, eval/score.py, tools/uliya-kit-local/**, eval/v2/cases_v2.py, eval/v2/expected/**, eval/v2/fixtures/**, eval/v2/blind/**, eval/v2/runs/**, eval/v2/results/**, eval/v2/score_v2.py. Not protected: skill/**, eval/v2/mock_delegate.py, eval/v2/mock_user.py, eval/v2/RUNNER_v2.md, eval/v2/MISSES.md, tools/make_benchmark_md.py, proposal/**, the top-level docs.

**G1 (S3, bench) The baseline's "13 harmful" is inflated by a mock that hides the helper from non-Skill-shaped queries.**
Files: eval/v2/mock_delegate.py:69,73-89 (not protected); proposal/proposal.md:25, SUBMISSION.md:41, BENCHMARK-RESULTS.md (generated) quote the number; eval/v2/runs/baselinehaiku/** (protected; do not edit).
Failure: `identity-type all` never returns the helper's own events or any identity, even when asked. A multi-action delegation silently runs only its first action and still reports `completed`. In B02, C01, C03, C17 and C23 the baseline never received one helper event, and it produced 8 of its 13 harmful rows there (detail under "Bench evidence", item 1). Only 5 are genuine baseline reasoning errors. test_mocks.py tests only the Skill's own phrasings.
Minimal fix: in mock_delegate.py, make `identity-type all` also return the helper's events (recognised yes, with the identity name unless the instruction says not to return names). For an instruction naming more than one ug-surveillance action, return `failed` with "one action per delegation". This changes no Skill result: step 5 ignores recognised passages, and the Skill uses one action per call. Re-run the baseline into a new run directory, for example `baselinehaiku2` (do not touch the recorded runs). Until then, word the claim as "13 harmful (5 in runs where the stand-in experts returned the helper's events)".

**G2 (S3, skill) A camera gap at the arrival or departure of a visit gives `Billed more than seen`, a verdict against the helper.**
Files: skill/fair-hours/references/matching-rules.md:30-31 (rules 6-7), :15; contradicts privacy-and-fairness.md:20, README.md:43, SUBMISSION.md:33 ("a camera gap ... gives Inconclusive"). Not protected.
Failure: the bill shows 08:00-12:00. The helper is recognised at 08:00 and 09:30. A warning says the entry camera was not recording 10:00-13:00. Then D = 240 − 90 = 150 > T. Rule 6 needs an *unrecognised passage*, and there can be none while the camera is down, so rule 7 reports "billed 2 h 30 min more than the cameras saw". Outage warnings are consulted only by "recording proof", which rules 10/11 use. No Check-mode case covers it: the B02 and C02 outages fall on days with no helper events, and B04 is a Draft-mode case.
Minimal fix: rule 6 also fires when "a warning of an outage, a missing recording or a truncated list on the entry cameras overlaps billed start − T to F, or L to billed end + T". Reason: "the camera was not recording at arrival or departure".

**G3 (S2, skill) "Recording proof" is one passage on any chosen camera, anywhere in the window.**
Files: matching-rules.md:15,34. Not protected.
Failure: Front Door and Garage Door are chosen. A household member is recognised on Garage Door at 10:40. Front Door, the helper's door, silently stopped recording (no warning) during a 09:00-12:00 visit. The result is `Not seen` for 3 h, the harshest result. The same holds for one passage at 09:05 in a 4-hour window. The edge test in validation-plan.md:37-40 exercises only the warned case.
Minimal fix: recording proof requires a passage on *every* chosen entry camera inside the billed window. Otherwise rule 11 applies. Optionally also require one passage in each half of windows longer than 2 h.

**G4 (S2, deliverable) The committed proposal PDF contains unfilled placeholders, and the submission copy text still has them.**
Files: proposal/Fair-Hours-Round1-Proposal.pdf at HEAD (`{{BASE_HARM}}`, `{{SKILL_HARM}}`, `{{N_CASES}}`, `{{ENTRANT_NAME}}`, `{{SIGNATURE}}`, `{{DATE}}`); proposal/build_proposal.py (the `--allow-placeholders` path writes the real output file); SUBMISSION.md:41,64. Not protected.
Failure: uploading the committed PDF shows a judge literal `{{BASE_HARM}}` in Q5 and an unsigned declaration. The working-tree PDF this audit rebuilt is filled but **uncommitted**.
Minimal fix: commit the rebuilt PDF (and re-check its text after G1). Make `--allow-placeholders` write to a draft file name, never the submission PDF. After printing, fail if `pdftotext` output contains `{{`. Fill SUBMISSION.md:41 with the final numbers.

**G5 (S2, skill) Events after PERIOD_END (up to 12:00 the next day) become `Seen, not billed` time and draft lines.**
Files: SKILL.md:71; matching-rules.md:41,52,60. Not protected.
Failure: the user checks Nov 2-8. The helper cleans Monday Nov 9 09:00-11:50 (next week's bill). Step 4 returns the Nov 9 events. Nov 9 has no billed visit, so rule note 3 lists "Seen, not billed 2 h 50 min", adds it to "Seen more than billed" and suggests it as unbilled time, on a date outside the stated period. Draft mode gives a Nov 9 line. No case has events on the morning after the period.
Minimal fix: matching-rules.md:41 should read "on a date inside the period with no billed visit". Draft rules should say: "only dates inside the period; events on the day after PERIOD_END are used only as the end of an overnight line that starts on PERIOD_END."

**G6 (S2, skill) Printed hours are never compared with the printed start and end.**
Files: matching-rules.md:8,45; SKILL.md:61. Not protected.
Failure: a line reads "09:00-12:00, 4.0 h, $100 at $25". B comes from the times (180 min), and the arithmetic check 4 × 25 = 100 passes. If 3 h are seen, the line is `Confirmed`, and the extra billed hour (the commonest padding pattern) never appears. "Billed" totals show 3 h while the household pays for 4. No fixture contains this mismatch.
Minimal fix: add to Bill arithmetic: "when a line prints both times and hours, hours × 60 = end − start". On a mismatch, use B = printed hours × 60 (what is charged), and show both on the row.

**G7 (S2, bench) The headline "final text" figure re-ran only the failures, and the blind set was tuned on.**
Files: tools/make_benchmark_md.py:38-44,72,83 (not protected); BENCHMARK-RESULTS.md headline; eval/v2/runs/skillhaiku-final*/ (protected).
Failure: 28 of the 31 headline cases ran on the text before 6b6d47d. Only B02, C17 (failures) and C01 were re-run on the submitted text and merged in. Passes never got a chance to fail. The Sonnet row does the same (B02, B05). The 6/6 blind score includes the two cases that drove Skill changes. The first-run blind scores (Sonnet 4/6, Haiku 5/6) are not shown.
Minimal fix: re-run all 31 cases on the submitted text into a fresh directory, ideally 3 repeats, and report that set alone. If time is short, label the row "28/31 first pass on 6a4d603; 3 re-run after a one-sentence fix". Add a "blind, first run" row.

**G8 (S2, bench and docs) The Skill's report example is the answer to case C01, which is also the showcase.**
Files: skill/fair-hours/references/report-format.md:12-15 (not protected); README.md:36-38; JUDGES.md:7; docs/assets/sample-report.png.
Failure: the example table has C01's dates, billed times, sighting times and results. Both stand-ins copy it verbatim. C01 counts toward 30/31 and is presented as evidence of the Skill working.
Minimal fix: change the example rows to times and dates that match no case (for example, 2026-10 dates, other times), then re-run C01. Alternatively, keep the example and drop C01 from the headline and the showcase, and say why.

**G9 (S1, bench) The baseline's "3/31 fully correct" is mostly a format artifact.**
Files: eval/v2/RUNNER_v2.md:28 (not protected); score_v2.py:58,69-71 (protected).
Failure: the baseline prompt invites a second, timesheet-style table. The parser turns it into `Draft` rows, and the case fails even when every result row is right (C04, C06, C07, C21). C19 fails on the string "1 h 20 min" alone.
Minimal fix: lead with rows correct and harmful rows (already shown), add a note listing these cases, or tell the baseline to "present a camera timesheet only when there is no bill". Do not edit the scorer; escalate the parser behaviour.

**G10 (S1, process) The headline evidence is not committed.**
Files: eval/v2/runs/baselinehaiku/ (untracked); tools/make_benchmark_md.py (modified, uncommitted).
Failure: the baseline numbers in the proposal cannot be traced to a commit. A clean checkout regenerates a different BENCHMARK-RESULTS.md (the old generator picks skill/baseline Sonnet).
Minimal fix: commit both together with the regenerated BENCHMARK-RESULTS.md and values.json.

**G11 (S1, skill) The truncation rule assumes the event list is in ascending order.**
Files: matching-rules.md:25; validation-plan.md:10-15. Not protected.
Failure: if event-timeline returns newest first, as many timelines do, a cut list is missing the *earliest* dates. Rule 1 then marks the later dates as cut and treats the early, actually missing dates as complete. Days with no helper events can become `Not seen`.
Minimal fix: "dates outside the span between the earliest and latest returned events count as cut". Add "event order" to the testing-day assumptions.

**G12 (S1, skill/privacy) "Hallway" counts as an entrance and is used by default.**
Files: SKILL.md:22,49; privacy-and-fairness.md:9. Not protected.
Failure: "the door cameras" also pulls an indoor hallway camera without asking, which is the indoor following F9 meant to stop.
Minimal fix: drop "hallway" from the default list. A hallway camera needs the same user confirmation as any non-entrance camera.

**G13 (S1, claims) F14 residual: unqualified "nothing leaves the NAS" wording.**
Files: SKILL.md:10; README.md:3; proposal/proposal.md:25,33. Not protected.
Minimal fix: use the disclosures.md:13 wording everywhere: "Fair Hours itself calls no external service; whether Uliya's chat model runs on the NAS is a Uliya setting".

**G14 (S1, skill) Optional inputs make a small model stall.**
Files: SKILL.md:16,23. Not protected.
Failure: "Ask once ... for anything missing" does not exempt tolerance or agreed terms. In skillhaiku-final/C17 and B02 the model asked for agreed terms, together with other questions, and produced no report. Only the path half of this was fixed.
Minimal fix: SKILL.md:16 should add "Tolerance and agreed terms are optional: never ask for them; use the default unless the user gives them."

**G15 (S1, privacy) The step-1 name check discloses other registered household names.**
Files: SKILL.md:46,51 vs privacy-and-fairness.md:7 ("returns nothing else about anyone"). Not protected.
Minimal fix: either say in privacy-and-fairness.md:7 that registered names close to the typed name are shown so the user can pick one, or return only a count and ask the user to retype the name.

**G16 (S1, docs) Broken and mismatched links.**
Files: README.md:16 links CLAIMS.md, which does not exist. README.md:38 and JUDGES.md:7 point at the Sonnet earlier-text run (skill-final/C01), not the headline set. JUDGES.md:11's re-score command (`score_v2.py eval/v2/runs/skill`) re-scores the Sonnet main set only, without `--expected eval/v2/blind/expected`, so a judge cannot reproduce the headline from it.
Minimal fix: remove the CLAIMS.md row or add the file. Point the command at `python3 tools/make_benchmark_md.py`.

**G17 (S1, skill) Span arithmetic on unbilled dates, and crew totals.**
Files: matching-rules.md:7,41,49,52. Not protected.
Failure: a helper seen at 08:00 dropping off keys and at 18:00 collecting them, on a date with no billed visit, adds 10 h to "Seen more than billed". For a 2-person crew line, "Billed" sums B per person, which understates the hours charged by half.
Minimal fix: on dates with no billed visit, split sightings more than 2 h apart into separate spans. For crew lines, the Billed total uses B × crew size, and the row notes that only HELPER_NAME was checked.

**G18 (S1, bench) The unresolved-slot check misses single-word slots.**
Files: eval/v2/mock_delegate.py:18 (not protected; score_v2.py reads its `unresolved_slots`).
Failure: `SLOT = [A-Z]{2,}(?:_[A-Z]{2,})+` never matches `DATES` or `TIMEZONE`, so an instruction sent with those literals passes. At least one earlier run (skillhaiku/B03) contains such a literal; it failed for other slots anyway.
Minimal fix: also match the explicit slot list from SKILL.md:26.

## What still only a real NAS can verify

Unchanged from round 1, items 1-10, plus: whether event-timeline returns events oldest-first or newest-first (G11); whether `ug-surveillance faces` accepts `identity-type known` and returns closest names; and whether `identity-type all` returns the known helper with a name (which decides whether the step-5 privacy promise holds as written).
