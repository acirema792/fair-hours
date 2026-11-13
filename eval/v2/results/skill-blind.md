**4/6 cases fully correct** · result rows 15/20 · false `Not seen` 0 · false `Confirmed` 0 · saves without a yes 0 · accusatory words 0

| Case | What it tests | Rows | Result | Why it failed |
|---|---|---|---|---|
| B01 | Nanny split shift, late evening and an unbilled Saturday | 5/5 | PASS |  |
| B02 | Agency carer: side door, storm outage, hooded arrival in the rain, a missed visit | 3/4 | FAIL | rows: expected [('2026-11-02', 'Confirmed'), ('2026-11-03', 'Inconclusive'), ('2026-11-04', 'Inconclusive'), ('2026-11-05', 'Not seen')], got [('2026-11-02', 'Confirmed'), ('2026-11-03', 'Inconclusive'), ('2026-11-04', 'Inconclusive'), ('2026-11-05', 'Inconclusive')] |
| B03 | Dog walker from typed hours with an agreed 1-hour minimum | 4/4 | PASS |  |
| B04 | Draft for cleaner with an ambiguous first name and a single-sighting day | 3/3 | PASS |  |
| B05 | Agency bill with a substitute worker and one short day | 0/4 | FAIL | rows: expected [('2026-11-09', 'Confirmed'), ('2026-11-10', 'Billed more than seen'), ('2026-11-11', 'Inconclusive'), ('2026-11-12', 'Confirmed')], got []; missing text: '1 h 45 min' |
| B06 | Tutor who has not been told about face recognition | 0/0 | PASS |  |
