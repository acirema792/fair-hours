# Matching rules

Read this in step 6. These rules decide every result. The model only applies them and explains the outcome; it does not weigh evidence by feel. When two rules could apply, the one that protects the helper from a wrong negative result wins.

## Terms

- **Billed visit**: one line from the bill (step 3) or typed by the user, with a date and either a start and end time or a number of hours. Lines for HELPER_NAME, or lines with no worker name, are compared. A line naming another worker (for example an agency substitute) still gets a row, with result `Inconclusive` and the reason "billed for another worker; only HELPER_NAME is checked", so every billed hour appears in the report. When a line is for a crew of several people, B is per person and the row notes the crew size.
- **Billed minutes (B)**: end minus start in whole minutes. If the end is earlier than the start, the visit ends the next day (add 24 hours). If only hours are printed, B = hours × 60, rounded to the nearest minute.
- **Visit events**: for a visit with times, the helper events (step 4) from 2 hours before the billed start to 2 hours after the billed end. An event inside the windows of two visits belongs to the visit whose start or end time is nearer. Each event belongs to one visit at most, so the morning departure after a night shift is never reused by the next shift. For a visit with only hours, the visit events are the helper events on the billed date not already used by another visit.
- **First seen (F)**, **last seen (L)**, **seen minutes (S)**: the earliest and latest visit events, and L minus F in whole minutes.
- **Single sighting**: one visit event, or all visit events within 5 minutes of each other.
- **Billed window**: billed start to billed end; for a visit with only hours, the whole billed date.
- **Passages** (step 5): events of other people on the entry cameras, each with a time, a camera and whether the platform recognised the person (yes or no), never a name.
- **Unrecognised passage**: a passage whose person the platform did not recognise. It may be the helper (face turned away, hood, mask), so it can never count against the helper.
- **Recording proof**: at least one passage on the entry cameras inside the billed window, and no warning of an outage, a missing recording or a truncated list for that window.
- **Tolerance (T)**: the user's tolerance in minutes, default 10.
- **Agreed terms** (optional, from the user): a minimum visit length and a rounding unit, such as "3 hours minimum" or "rounded up to 15 minutes".

## Results for a billed visit

Apply the first rule that fits. D = B − S.

| # | Situation | Result | Reason to show |
|---|---|---|---|
| 1 | The step 4 or step 5 list for that date was cut at its limit | `Inconclusive` | "event list truncated" |
| 2 | No helper events in the whole period, and the bill has two or more visits | `Inconclusive` for every visit | "the helper was never recognised in the period; check the registered name" |
| 3 | Single sighting | `Inconclusive` | "arrival or departure not recorded" |
| 4 | Visit events exist and D is from −T to +T, both ends included | `Confirmed` | B, S and D |
| 5 | Visit events exist, D is greater than T, and agreed terms explain it: B equals S rounded up to the agreed unit, or B equals the agreed minimum and S is not longer | `Confirmed` | "matches the agreed rounding" or "agreed minimum visit" |
| 6 | Visit events exist, D is greater than T, and there is an unrecognised passage between billed start − T and F, or between L and billed end + T (for a visit with only hours: any unrecognised passage that date before F or after L) | `Inconclusive` | "arrival or departure may not have been recognised" |
| 7 | Visit events exist and D is greater than T | `Billed more than seen` | "billed D min more than the cameras saw" |
| 8 | Visit events exist and D is less than −T | `Seen more than billed` | "seen −D min longer than billed" |
| 9 | No visit events and an unrecognised passage inside the billed window | `Inconclusive` | "someone unrecognised passed the entry during the billed time" |
| 10 | No visit events, recording proof, and every passage in the billed window was a recognised person | `Not seen` | "not seen while the entry cameras recognised other people"; B minutes |
| 11 | No visit events and no recording proof | `Inconclusive` | "recording not confirmed" |

Notes, which never change the result:

- When the bill has times and F or L differs from them by more than T, add a note such as "arrived 35 min after the billed start".
- Helper events on a billed date that belong to no visit window are noted on that date's row as "also seen outside the billed times".
- Helper events on a date with no billed visit are listed as `Seen, not billed`, with F, L and S, as possible unbilled time; single sightings on such dates are listed with no minutes.

## Bill arithmetic

Using only printed values from step 3, check each line: hours × rate = line amount (to the cent), and the sum of line amounts = the printed total. List every mismatch in a "Bill arithmetic" block. These checks never change a visit result.

## Totals

- **Billed**: sum of B over checked visits.
- **Confirmed**: sum of B over `Confirmed` visits.
- **Billed more than seen**: sum of D over those visits.
- **Seen more than billed**: sum of −D over those visits, plus S over `Seen, not billed` dates.
- **Not seen**: sum of B over `Not seen` visits.
- **Inconclusive**: sum of B over `Inconclusive` visits, with each reason.

Show each total in hours and minutes. Show money only when the bill prints a rate: for each visit, minutes × that line's rate ÷ 60, rounded to the cent, then summed, labelled "at the printed rates". Never net the two directions into one number; show them side by side.

## Draft rules

In Draft mode there is no bill. Group helper events by date, with one exception: when the last sighting of a date is after 18:00 and the first sighting of the next date is before 10:00 with nothing in between, they form one overnight line. A line with a single sighting is `Inconclusive` with no hours; otherwise it shows F, L and S. The draft total is the sum of S, labelled "time between first and last sighting at the entry cameras", not working time.

## Things the rules never do

- Name, count against, or identify anyone other than the named helper; passages are used only as anonymous recording proof.
- Treat an unrecognised passage as the helper, or as proof that the helper was absent.
- Treat an event whose identity the platform did not record as the helper, even if the user suggests it.
- Deduct or add breaks, travel or overtime; the cameras show passages through the entry, not work.
- Turn `Inconclusive` into `Not seen`, or any result into a judgement about honesty.
