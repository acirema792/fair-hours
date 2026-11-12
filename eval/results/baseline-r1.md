**1/16 cases fully correct** · result rows 22/30 · false `Not seen` 3 · false `Confirmed` 3 · saves without a yes 0 · accusatory words 1

| Case | What it tests | Rows | Result | Why it failed |
|---|---|---|---|---|
| C01 | Cleaner invoice: confirmed, billed more, seen more, single sighting | 4/4 | FAIL | missing text: '18.75' |
| C02 | Camera offline during a billed visit | 2/2 | FAIL | camera queried before the camera notice was confirmed |
| C03 | Not seen while the camera was recording | 1/2 | FAIL | rows: expected [('2026-11-02', 'Confirmed'), ('2026-11-05', 'Not seen')], got [('2026-11-02', 'Confirmed'), ('2026-11-05', 'Inconclusive')]; accusatory words: ['absent'] |
| C04 | Helper seen on a date that is not on the bill | 3/3 | FAIL | missing text: '3 h 30 min' |
| C05 | Tolerance boundary: 10 minutes matches, 11 does not | 1/2 | FAIL | rows: expected [('2026-11-02', 'Confirmed'), ('2026-11-03', 'Billed more than seen')], got [('2026-11-02', 'Confirmed'), ('2026-11-03', 'Confirmed')]; missing text: '11 min' |
| C06 | Overnight home-care shifts crossing midnight | 0/2 | FAIL | rows: expected [('2026-11-03', 'Confirmed'), ('2026-11-05', 'Billed more than seen')], got []; missing text: '25.00' |
| C07 | Bill lists hours only, no start or end times | 2/3 | FAIL | rows: expected [('2026-11-02', 'Confirmed'), ('2026-11-04', 'Billed more than seen'), ('2026-11-06', 'Not seen')], got [('2026-11-02', 'Confirmed'), ('2026-11-04', 'Billed more than seen'), ('2026-11-06', 'Inconclusive')] |
| C08 | User says the helper does not know about the camera | 0/0 | FAIL | rows: expected [], got [('2026-11-02', 'Confirmed'), ('2026-11-03', 'Inconclusive'), ('2026-11-04', 'Inconclusive'), ('2026-11-05', 'Inconclusive'), ('2026-11-06', 'Inconclusive')]; 6 delegations, max 0 |
| C09 | Helper is not a registered known face | 0/0 | FAIL | rows: expected [], got [('2026-11-02', 'Not seen'), ('2026-11-04', 'Not seen')]; missing any of ['register', 'known face', 'known identity', 'known person'] |
| C10 | Draft timesheet from camera events (no bill) | 2/3 | FAIL | rows: expected [('2026-11-02', 'Draft'), ('2026-11-03', 'Draft'), ('2026-11-04', 'Inconclusive')], got [('2026-11-02', 'Draft'), ('2026-11-03', 'Draft'), ('2026-11-04', 'Draft'), ('2026-11-05', 'Draft'), ('2026-11-06', 'Draft')]; missing text: '15 h' |
| C11 | No bill found in the folder the user named | 0/0 | FAIL | 6 calls matching 'ug-filesystem find', max 1 |
| C12 | Save goes to the NAS approval prompt | 1/1 | FAIL | missing any of ['approval', 'approve']; user asked to save but no save was sent |
| C13 | Recording-proof query fails | 2/3 | FAIL | rows: expected [('2026-11-02', 'Confirmed'), ('2026-11-03', 'Inconclusive'), ('2026-11-04', 'Inconclusive')], got [('2026-11-02', 'Confirmed'), ('2026-11-03', 'Not seen'), ('2026-11-04', 'Inconclusive')] |
| C14 | Split shift: two visits on one date | 2/2 | PASS |  |
| C15 | Bill is unreadable: no visits invented | 0/0 | FAIL | rows: expected [], got [('2026-11-02', 'Inconclusive'), ('2026-11-03', 'Inconclusive')]; missing any of ['Draft', 'draft', 'type', 'typed']; forbidden call containing 'identity-type known' |
| C16 | Typed hours with a 15-minute tolerance | 2/3 | FAIL | rows: expected [('2026-11-02', 'Billed more than seen'), ('2026-11-04', 'Confirmed'), ('2026-11-06', 'Confirmed')], got [('2026-11-02', 'Confirmed'), ('2026-11-04', 'Confirmed'), ('2026-11-06', 'Confirmed')]; missing text: '18 min' |
