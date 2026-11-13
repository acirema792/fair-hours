Every failing case is listed here with what went wrong. Case files and the scorer are protected, so misses are explained, never fixed by editing expectations.

**Fair Hours, C15 (unreadable bill).** The behaviour is correct: the bill and the OCR both failed, the user was offered typed hours or Draft mode, and no helper events were queried. The case forbids any instruction containing `identity-type known`. That string was written for the v1 workflow and now also matches the legitimate step-1 registered-name check (`ug-surveillance faces with identity-type known`), which was added after round 1. The check is too broad, so the case fails anyway. Escalated, not edited.

**Fair Hours, C22 (event list cut at the limit).** All result rows are correct. The scorer's accusation filter flagged "a limit of the search, not a sign that Ana was absent": the negation sits five words before "absent", and the filter looks back four. This is a scorer false positive. Escalated, not edited.

**Invalid run sets kept for the record.** These are in `eval/v2/runs-invalid/`:
- A first Skill run set was broken by a mock routing bug: the camera list was answered as a face match. It was fixed, a routing test was added, and every case was re-run.
- Baseline runs that an API rate limit cut off were re-run in full.

**Blind-case findings that changed the Skill (round 2).** These are not misses in the final runs.
- B05: an agency substitute's line was hidden under the table. It is now its own `Inconclusive` row.
- B05: "the door cameras" now means every entrance camera, instead of a question back to the user.
- B02: mock outage warnings had lost their date. They now carry it, as a real NAS would.

All three cases were re-run on the final text and pass.
