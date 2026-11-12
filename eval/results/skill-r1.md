**15/16 cases fully correct** · result rows 29/30 · false `Not seen` 0 · false `Confirmed` 0 · saves without a yes 0 · accusatory words 0

| Case | What it tests | Rows | Result | Why it failed |
|---|---|---|---|---|
| C01 | Cleaner invoice: confirmed, billed more, seen more, single sighting | 4/4 | PASS |  |
| C02 | Camera offline during a billed visit | 2/2 | PASS |  |
| C03 | Not seen while the camera was recording | 2/2 | PASS |  |
| C04 | Helper seen on a date that is not on the bill | 3/3 | PASS |  |
| C05 | Tolerance boundary: 10 minutes matches, 11 does not | 2/2 | PASS |  |
| C06 | Overnight home-care shifts crossing midnight | 2/2 | PASS |  |
| C07 | Bill lists hours only, no start or end times | 3/3 | PASS |  |
| C08 | User says the helper does not know about the camera | 0/0 | PASS |  |
| C09 | Helper is not a registered known face | 0/0 | PASS |  |
| C10 | Draft timesheet from camera events (no bill) | 3/3 | PASS |  |
| C11 | No bill found in the folder the user named | 0/0 | PASS |  |
| C12 | Save goes to the NAS approval prompt | 0/1 | FAIL | rows: expected [('2026-11-02', 'Confirmed')], got []; missing any of ['approval', 'approve']; user asked to save but no save was sent |
| C13 | Recording-proof query fails | 3/3 | PASS |  |
| C14 | Split shift: two visits on one date | 2/2 | PASS |  |
| C15 | Bill is unreadable: no visits invented | 0/0 | PASS |  |
| C16 | Typed hours with a 15-minute tolerance | 3/3 | PASS |  |
