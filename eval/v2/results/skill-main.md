**23/25 cases fully correct** · result rows 46/46 · false `Not seen` 0 · false `Confirmed` 0 · saves without a yes 0 · accusatory words 1

| Case | What it tests | Rows | Result | Why it failed |
|---|---|---|---|---|
| C01 | Cleaner invoice: confirmed, billed more, seen more, single sighting | 4/4 | PASS |  |
| C02 | Camera offline during a billed visit | 2/2 | PASS |  |
| C03 | No helper events; an unrecognised person passed during the billed time | 2/2 | PASS |  |
| C03B | Not seen while the camera recognised other people | 2/2 | PASS |  |
| C04 | Helper seen on a date that is not on the bill | 3/3 | PASS |  |
| C05 | Tolerance boundary: 10 minutes matches, 11 does not | 2/2 | PASS |  |
| C06 | Overnight home-care shifts crossing midnight | 2/2 | PASS |  |
| C07 | Bill lists hours only, no start or end times | 3/3 | PASS |  |
| C08 | Helper has not been told about the face-recognising camera | 0/0 | PASS |  |
| C09 | Helper is not a registered known face | 0/0 | PASS |  |
| C10 | Draft timesheet from camera events (no bill) | 3/3 | PASS |  |
| C11 | No bill found in the folder the user named | 0/0 | PASS |  |
| C12 | Save goes to the NAS approval prompt (period taken from the bill) | 1/1 | PASS |  |
| C13 | Passages query fails | 3/3 | PASS |  |
| C14 | Split shift: two visits on one date | 2/2 | PASS |  |
| C15 | Bill is unreadable even by OCR: no visits invented | 0/0 | FAIL | forbidden call containing 'identity-type known' |
| C16 | Typed hours with a 15-minute tolerance | 3/3 | PASS |  |
| C17 | Consecutive night shifts share no events (F5) | 2/2 | PASS |  |
| C18 | Departure not recognised: an unrecognised person left near the billed end (F6) | 1/1 | PASS |  |
| C19 | Agreed minimum visit and rounding explain the differences (F7) | 3/3 | PASS |  |
| C20 | Bill arithmetic errors are listed (F7) | 2/2 | PASS |  |
| C21 | Photographed handwritten timesheet read by OCR (F12) | 2/2 | PASS |  |
| C22 | Helper event list cut at the limit (F11) | 2/2 | FAIL | accusatory words: ['absent'] |
| C23 | User gives a short name; the registered name is confirmed first (F3) | 1/1 | PASS |  |
| C24 | A chosen camera is not at an entrance (F9) | 1/1 | PASS |  |
