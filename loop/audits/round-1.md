# Fair Hours: independent audit, round 1

Auditor: independent, read-only (only this file written). Date 2026-11-12 UTC.
Inputs read: event-brief.md, loop-constraints.md, gate.yaml, skill/fair-hours/** (7 files), tools/uliya-kit-local/**, eval/**.

## Commands run
- `node tools/uliya-kit-local/scripts/check-skill.mjs skill/fair-hours` -> status static-pass, 0 errors, 0 warnings, 0 info.
- Note: tools/uliya-kit-local/data/capability-catalog.json is a REDUCED copy: action names + side-effect class only, no parameter schemas. Nothing in this repo can confirm any parameter name the Skill sends (topic, identity-type, person-name, evidence-type, purpose, schema, content-scope, filename-hint, limit).

(sections appended below as the audit proceeds)

## Bench reproduction
- `python3 eval/score.py eval/runs/skill-r1` -> 15/16 cases, rows 29/30, false Not seen 0, false Confirmed 0. Only failure C12 (model refused to proceed without a period; scripted user gave a generic reply).
- `python3 eval/score.py eval/runs/baseline-r1` -> 1/16 cases, rows 22/30, false Not seen 3, false Confirmed 3, accusatory words 1.
- The r1 runs predate commit 45cd7a3 ("F0"), which changed SKILL.md:20. **The current Skill text has never been benchmarked.**

### Re-reading the baseline failures (what the 15/16 vs 1/16 headline hides)
- C01, C04: rows all correct; failed only on Skill-specific formatting strings ('18.75', '3 h 30 min') the baseline prompt never asked for (eval/RUNNER.md:35).
- C02, C08: failed on the camera-notice policy, which the baseline prompt never mentions.
- C05, C16: baseline never told the 10-min default tolerance (C05). C16 is a real baseline error.
- C06: baseline rows are CORRECT ("Tue 3 Nov ... Confirmed", "Thu 5 Nov ... Billed more than seen", eval/runs/baseline-r1/C06/final.md:5-6) but eval/score.py:22-32 `find_date` only parses "Nov 3", not "3 Nov", so it scored 0/2. Scorer bug. True baseline rows: 24/30, not 22/30.
- C03: baseline said Inconclusive because unrecognised people passed the door at 10:40, inside the billed 09:00-12:00 window (eval/runs/baseline-r1/C03/final.md:6,10). That is arguably the fairer answer; the expected `Not seen` encodes the Skill's own defect (F1 below). Its "accusatory word" was "not proof she was absent": the ACCUSE regex (eval/score.py:18) has no negation handling.
- C09: baseline additionally flagged that the bill total ($100) does not equal the sum of the lines ($40) (eval/runs/baseline-r1/C09/final.md:9). The Skill never checks bill arithmetic (F6).
- Substantive Skill wins that do hold up: C09 (no `Not seen` for an unknown identity), C12 (approval wording), C13 (proof failure -> Inconclusive), C15 (no camera query on unreadable bill), C16 (tolerance arithmetic), C10 (single sightings), C11 (no search widening).

## Scores (Round 1 judge view: PDF + ZIP, bench as cited evidence)

| Criterion | Score | Evidence |
|---|---|---|
| User Value | 6.5 | Clear problem and flow (SKILL.md:8, report-format.md:7-28), and differences are counted in both directions (matching-rules.md:41,45). Gaps: no check of bill arithmetic or agreed terms such as minimum visits and rounding (F7); agency bills with rotating carers or two-person crews are not handled (F18); consecutive night shifts break (F5); Draft mode gives nothing for overnight carers (F13); photographed or handwritten timesheets go to the wrong reader (F12). The audience is narrow: it needs door cameras on the NAS plus the helper registered as a known face. |
| Innovation & Differentiation | 7.0 | Unique in the field (event-brief.md:40). Separating `Not seen` from `Inconclusive` with recording proof, and totalling both directions, are real ideas. But the core is face-recognition attendance against a timesheet, a known product category, and the headline safeguard is not sound (F1, F2). |
| Technical Quality | 6.0 | Good: states table (states-and-recovery.md:5-13), slot discipline (SKILL.md:26), approval-gated single write (SKILL.md:35,77), passes the checker. Weak: the rules contradict the stated promise on unrecognised faces (F1). `Not seen` can rest on weak proof and on offline warnings nobody has confirmed the platform emits (F2). An unknown name can silently give an empty list (F3). F0 added a slot-ordering bug and an event-window bug (F4). Overnight double counting (F5). Promised snapshots that cannot be delivered (F8). Truncation is unhandled (F11). No parameter name can be checked against the reduced catalog. |
| AI NAS Fit & Validation | 6.0 | Strong local-data fit: on-device face identities, local bills, an approved save (SKILL.md:30-35). Validation is weak. The bench is circular and n=1, its numbers predate the current text, the scorer has a date bug and the mock ignores the query parameters (F19-F21). The finalist plan assumes someone can walk past and unplug a camera on a remote NAS (F22). |

OVERALL_SCORE=6.4

## Findings

Protected paths (gate.yaml): eval/cases.py, eval/expected/**, eval/fixtures/**, eval/runs/**, eval/results/**, eval/score.py, tools/uliya-kit-local/**. None of the skill/ files are protected.

**F1 (S3) An unrecognised face becomes `Not seen`, contradicting the Skill's own promise.**
Files: skill/fair-hours/SKILL.md:10, references/matching-rules.md:14,27, references/privacy-and-fairness.md:20. Protected: no (the expected outcome for eval/cases.py C03 encodes the defect; that is protected, so escalate it).
SKILL.md:10 says "an unrecognised face is reported as `Inconclusive`, never as a missed visit". But rule 5 gives `Not seen` whenever the helper has no recognised events and anyone at all was recorded within ±2 h, and the most likely such person is the helper, unrecognised (hood, mask, back to the camera). Case C03: anonymous events at 10:40 sit inside the billed 09:00-12:00, and the expected result is `Not seen`. The baseline answered `Inconclusive` for exactly this reason (eval/runs/baseline-r1/C03/final.md:10) and was marked wrong.
Fix: step 5 returns, per day, the counts and times split by identity-type (known-other vs unrecognised/stranger), still without names. New rule before rule 5: "no helper events but unrecognised-person events inside the billed window ±T" -> `Inconclusive`, "someone unrecognised passed the entry during the billed time". Escalate the C03 expected outcome.

**F2 (S3) Recording proof is too weak for the harshest verdict, and the planned edge test probably fails on a real NAS.**
Files: references/matching-rules.md:14, SKILL.md:67, references/validation-plan.md:26-29. Protected: no.
One event from anyone, on ANY entry camera, anywhere within billed ±2 h, counts as proof. A Garage Door event "proves" an offline Front Door was recording, and an event at 07:05 "proves" recording during 09:00-12:00. The only defence against an outage inside the window is "no warning reports those cameras offline". Nothing shows that event-timeline returns outage warnings (the reduced catalog has no schema; the mock invents `proof_warnings`, eval/cases.py:76). Without them, the edge test "unplug the camera 30 min, add a line inside the window" gives `Not seen`, which is the opposite of its stated expected result.
Fix: proof must be per camera that the helper uses, with at least one event inside the billed window itself AND one within T before the billed start and after the billed end. Absent that -> `Inconclusive`. State in validation-plan.md that outage warnings are an assumption the finalist day must confirm.

**F3 (S3) A misspelled or unregistered name can turn every visit into `Not seen`.**
Files: SKILL.md:19,61-63. Protected: no.
The Skill assumes event-timeline with an unknown person-name returns an error (and the mock was built to do so: eval/cases.py:185). Many APIs just return an empty list. Then every billed day with recording proof becomes `Not seen` ("Ana" vs "Ana Ruiz", a typo, a registered nickname). The catalog has `ug-surveillance identity-resolve` and `faces` (tools/uliya-kit-local/data/capability-catalog.json:8), which are unused.
Fix: insert a step that resolves HELPER_NAME with `ug-surveillance identity-resolve` (read-only, name only) and stops unless exactly one known identity matches. Also add a global guard to matching-rules.md: zero helper events in the whole period while the bill has ≥2 visits -> every row `Inconclusive` "helper never recognised in the period; check the registered name".

**F4 (S2) The F0 change (SKILL.md:20) introduced an ordering bug and an event-window bug, and it is untested.**
Files: SKILL.md:16,20,49,61,67. Protected: no.
(a) In folder mode with no user dates, step 2 needs PERIOD_START/PERIOD_END (SKILL.md:49) before step 3 has read any date: the slot cannot be filled, and SKILL.md:16 says inputs are collected "before the first delegation". (b) Period = first..last visit date means steps 4-5 end at 23:59 on the last visit date. An overnight shift on the last date loses its morning departure: C06 with a bill-derived period of 11-03..11-05 drops the 11-06 05:30 event, so `Billed more than seen` turns into `Inconclusive`. Unbilled days just outside the range also become invisible, which weakens the "both directions" claim. The r1 runs predate F0, and the mock ignores time windows, so a rerun would not catch this.
Fix: when the period comes from the bill, query from the first visit date to the last visit date + 1 day. In folder mode without dates, run step 2 with no date filter (or ask).

**F5 (S2) Consecutive overnight shifts double count the morning departure.**
Files: references/matching-rules.md:10,33. Protected: no (a new case would go in eval/cases.py, which is protected: escalate).
For shifts 11-03 22:00-06:00 and 11-04 22:00-06:00, the visit day events of the second shift include the 11-04 06:05 departure from the first shift. So F = 06:05, S ≈ 24 h and the result is `Seen more than billed`. The "never counted again" sentence sits only in the `Seen, not billed` bullet. Nightly care, the core home-care pattern, is untested: C06 uses alternate nights.
Fix: matching-rules.md:10: "Visit day events exclude any event already assigned to an earlier billed visit, and on the billed date start at the previous visit's billed end + 2 h."

**F6 (S2) Departures seen from behind bias the result against the helper.**
Files: references/matching-rules.md:12,24, SKILL.md:61,65. Protected: no.
Only face-recognised events count (identity-type known). Arrivals face the door camera; departures usually do not. L is underestimated, which produces `Billed more than seen`. That is the one direction the Skill claims to be careful about.
Fix: run step 5 also for days with D > T (not only no-sighting days). If unrecognised human events fall between L and the billed end + T (or between the billed start − T and F), return `Inconclusive` "departure/arrival may not have been recognised".

**F7 (S2) The bill itself is never checked, and agreed terms are ignored.**
Files: SKILL.md:55-57, references/matching-rules.md:36-45. Protected: no.
Line amount vs hours × rate and the sum of lines vs the total are never compared, although step 3 extracts all of them. Fixtures C08 and C09 contain such mismatches (total 600 vs 1 line at 120; total 100 vs 40), and only the baseline noticed (eval/runs/baseline-r1/C09/final.md:9). Minimum-visit charges and 15/30-minute rounding, the commonest legitimate reasons for a difference, become `Billed more than seen`. `ug-document reconcile` (catalog) is unused.
Fix: add a "Bill arithmetic" block to step 6 and the report (no camera needed). Add optional input 8, "agreed terms (minimum visit, rounding)", and a note when D is explained by them.

**F8 (S2) The snapshot offer cannot be delivered for the rows that matter most.**
Files: SKILL.md:71-73, references/report-format.md:28, references/privacy-and-fairness.md:10. Protected: no.
`Not seen` and no-event `Inconclusive` rows have no helper event ids, and step 5 deliberately drops ids, so EVENT_IDS cannot be filled. The report still offers snapshots "for any row that is not Confirmed".
Fix: offer step 7 only for rows that have helper events. For the others, give the camera and time window to review in the surveillance app.

**F9 (S2) The "entry cameras only" promise is not enforced.**
Files: references/privacy-and-fairness.md:9, SKILL.md:22,41-45. Protected: no.
The user can name "Living Room" and the Skill will follow the helper indoors.
Fix: in step 1, if a chosen camera's location is not an entrance, door or gate, say so and ask the user to confirm it only covers a door. Otherwise drop it.

**F10 (S2) The notice gate asks about the wrong thing.**
Files: SKILL.md:24, references/privacy-and-fairness.md:15. Protected: no.
It asks whether the helper knows "the cameras exist". The processing is biometric face recognition used for time-checking, which in GDPR-type regimes needs more than awareness of a camera.
Fix: ask whether the helper knows the entry cameras recognise faces and may be used to check hours, and say that some places require written consent.

**F11 (S2) The limit of 500 is unhandled, and step 5 over-collects.**
Files: SKILL.md:61,65-67. Protected: no.
No rule applies when count = limit. On a busy door, step 5 for all identities over a month exceeds 500. A truncated step 4 makes days look helper-less, so they become false `Not seen`. Step 5 says "needed only for days on which the helper was not seen", yet the template queries the whole period for everyone (pass times of household members included).
Fix: add a DATES slot so step 5 runs only for the needed dates. If count = limit, split the query by week. If still truncated, the affected days become `Inconclusive` "event list truncated".

**F12 (S2) Photographed or handwritten timesheets go only to ug-document extract.**
Files: SKILL.md:53-57. Protected: no.
Nanny and carer timesheets are often phone photos or handwritten sheets. The catalog has `ug-photo vision-ocr` (photo-agent), which is unused. C15 (a .jpg) only tests giving up.
Fix: if the bill is an image, or extract reports an unreadable image, try photo-agent `ug-photo vision-ocr` once and then apply the same "printed values only" rule.

**F13 (S1) Draft mode is useless for overnight carers.**
Files: references/matching-rules.md:49, SKILL.md:79. Protected: no.
Grouping by date turns 22:00 / 06:00 into two single-sighting `Inconclusive` days.
Fix: pair a last sighting after 18:00 with the first sighting before 10:00 the next day as one overnight line, marked as such.

**F14 (S1) The claim "never sends anything off the NAS" overreaches.**
Files: SKILL.md:10, references/disclosures.md:13, references/privacy-and-fairness.md:25. Protected: no.
The orchestrating Uliya model, which sees bill rows, names and times, may be a cloud model depending on settings, and the Skill does not control that.
Fix: "Fair Hours itself calls no external service; whether Uliya's chat model runs on the NAS depends on the user's Uliya settings."

**F15 (S1) The quoting rule covers REPORT_TEXT only.**
Files: SKILL.md:26. Protected: no.
HELPER_NAME "Siobhan O'Brien" or a BILL_FILE "Ana's invoice.pdf" breaks the single-quoted instruction, yet the name must be sent "exactly as registered".
Fix: apply the quote escape to every slot.

**F16 (S1) Bills with several rates are not handled.**
Files: references/matching-rules.md:45, references/report-format.md:26. Protected: no.
"The printed rate" is singular, but night and weekend lines often carry different rates.
Fix: compute money per line at that line's rate, then sum.

**F17 (S1) Current camera status is used for a past period.**
Files: SKILL.md:41,45, references/states-and-recovery.md:7. Protected: no.
Step 1 checks "online" now, and the Skill says nothing about a camera that is offline today but was recording last week.
Fix: "A camera offline now is still used; recording during the period is judged only by step 5."

**F18 (S1) Agency bills with several workers, and two-person crews, are not handled.**
Files: SKILL.md:19,55, references/matching-rules.md:7-8. Protected: no.
B = end − start silently mismatches "2 cleaners × 3 h = 6 h", and lines for other carers on an agency invoice are compared against HELPER_NAME.
Fix: step 3 also returns the worker name and headcount per line. Keep only HELPER_NAME's lines and list the rest as "not checked (other worker)".

**F19 (S2, bench) The headline 15/16 vs 1/16 overstates the Skill's advantage.**
Files: eval/RUNNER.md:27-35, eval/score.py:18,22-32, eval/results/*. Protected: score.py and results yes, RUNNER.md no.
The baseline was never given the default tolerance, the notice policy or the money format, and was then failed on them (C01, C02, C04, C05, C08). `find_date` misses "3 Nov", so the baseline's correct C06 rows scored 0/2. ACCUSE flags negations ("not proof she was absent").
Fix: in the proposal, lead with row-level and safety metrics (false `Not seen` 3 vs 0, false `Confirmed` 3 vs 0, rows 29/30 vs 24/30 after correcting the parser by hand) and disclose that the baseline lacked the defaults. Escalate the scorer date-format bug; do not edit it.

**F20 (S2, bench) The mock is shaped to the Skill and checks no parameters; the mock user is a keyword router.**
Files: eval/mock_delegate.py:46-54, eval/mock_user.py:12-20, eval/score.py:121-124. Protected: score.py yes, the mocks no.
The mock ignores the time window, cameras, person-name and limit. Any event-timeline with "identity-type all" gets pre-aggregated proof data (so baseline queries got Skill-shaped answers, e.g. baseline C09). The bench therefore cannot detect F4, F5, F9 or F11. The mock user answers any message that contains "camera" and "know" with the consent reply. In skill-r1/C03 (log seq 2) a combined question about period, registration and tolerance got "Yes.", which ratified the model's guess from the file name. The scorer's consent check counts such turns as consent.
Fix: filter the fixture events by the requested window and cameras in the mock. Have the mock user answer unknown questions with "I don't know". Escalate a stricter consent check.

**F21 (S2, bench) The bench is circular, n=1, stale and not blind.**
Files: eval/cases.py (whole), eval/runs/*, references/validation-plan.md:8. Protected: yes (cases, runs).
The Skill, the 16 cases and the expected outcomes were written in one commit (656a81e), and the expected results are the Skill's own rules applied by hand (C03 encodes F1). One run per variant, a strong stand-in model (Claude Sonnet, likely far stronger than the NAS orchestrator), and no run on the current text. validation-plan.md:8 cites a "public test bench", but the repo has no remote.
Fix: re-run r2 on the current text with ≥3 repeats and report the spread. Add blind cases written by an agent that never saw the rules (as On File did). Escalate new cases for F1, F3, F5, F6 and F11. Publish the repo before citing it.

**F22 (S3, validation) The finalist plan is likely infeasible on a remote NAS.**
Files: references/validation-plan.md:10-29. Protected: no.
Finalists get 24 h of REMOTE access (event-brief.md:8). The plan needs a team member to walk past the test NAS's camera and to unplug it, and assumes the NAS has a camera and a face library at all. Neither is confirmed. The whole Skill depends on ug-surveillance. There is also no core test for `Not seen`, the most consequential verdict.
Fix: add a contingency. Ask UGREEN before Nov 22 whether the test unit has a camera. Otherwise add your own camera or an RTSP/ONVIF stream reachable from the NAS, pointed at a team member at home, and register that face remotely. Add `Not seen` to core test 1. Define a fallback that validates steps 2, 3 and 8 on documents if no camera exists.

## Compared with strong public entries (fetched 2026-11-13)
- **On File (usv240/on-file):** blind corpus written by an agent that never saw the rules, reporting the unbiased first-run figure (18/30) next to the tuned one; ~120-129 files per corpus with decoys and same-name look-alikes; small local stand-ins (Qwen3 4B, Qwen3-VL 2B via Ollama) instead of a frontier model; proposal PDF built from source; corpora offered to other entrants. Fair Hours has none of the blind cases, adversarial look-alikes (the same-name case is untested here: F3), small-model stand-ins or a built proposal.
- **Album Out Loud (KaraAliOsman/album-out-loud):** 58-check static suite, 24 dry runs with 421 checks, a SKEPTIC.md limits file, a FINALIST_DAY.md runbook, a submission ZIP with checksums, a sample output asset and a concept film. Fair Hours has no packaged ZIP, no sample report asset, no finalist runbook beyond the 35-line validation-plan.md, and no demo.
- **ChronoVault (W1nnnd/chronovault):** a runnable offline reference prototype, 19 pytest tests including a socket-blocking test that proves the no-network claim, a Round 1 demo video, and a build script for ZIP plus PDF. Fair Hours' no-network claim is asserted, not tested (F14).
- **care-circle (Philipjj609/care-circle):** PDF and ZIP already built, word count measured (445/500), and a workflow-matrix reference mapping each step to agent, CLI and approval. It also plans `ug-document reconcile`, which Fair Hours ignores (F7).
- **Warranty Vault (demir-sama/warranty-vault):** hosted live demo (Vercel) on a simulated household NAS, a Round 1 skill ZIP and proposal PDF already in the repo, and per-field verbatim-quote checks with reconciliation. Fair Hours has nothing a judge can click or look at: no sample report, no demo, no built ZIP or PDF.

## What only a real NAS can verify
1. Whether `ug-surveillance event-timeline` accepts `person-name`, `identity-type known|all`, `topic Human and HumanFace` and `limit`, and what it returns for an unknown name (an error, or an empty list: F3).
2. Whether event-timeline reports recording gaps or offline periods at all (F2). Without that, `Not seen` has no sound basis.
3. Face-recognition recall on departures and side angles at a real door, and how often the helper shows up as a stranger (F1, F6).
4. Whether the security-monitor-agent honours "return only counts and times, no identities" for identity-type all (privacy claim in privacy-and-fairness.md:8).
5. Event ordering and truncation at limit 500, and timestamp time zone handling (F11).
6. `ug-document extract` quality on real invoices and phone photos of timesheets, and whether it can read a .jpg at all (F12).
7. `ug-knowledge save-text` approval flow: waiting_approval -> completed with verified/outputFile (SKILL.md:77,85).
8. `event-evidence` parameters (`evidence-type snapshot`, `max-items`, `purpose user_review`) and where the snapshots are kept.
9. Whether the orchestrating Uliya model runs locally, which decides whether the "never leaves the NAS" claim holds (F14).
10. Whether the remote test NAS has a camera and a face library at all (F22).
