# Matching rules

Read this in step 6. These rules decide every result. The model only applies them and explains the outcome; it does not weigh evidence by feel.

## Terms

- **Billed visit**: one line from the bill (step 3) or one line typed by the user, with a date, and either a start and end time or a number of hours.
- **Billed minutes (B)**: end minus start in whole minutes. If the end is earlier than the start, the visit ends the next day (add 24 hours). If only hours are printed, B = hours × 60, rounded to the nearest minute.
- **Helper events**: step 4 events for the named helper on the entry cameras, in TIMEZONE.
- **Visit day events**: helper events on the billed date. For a visit that crosses midnight, also include events on the next day up to the billed end time plus 2 hours.
- **First seen (F)** and **last seen (L)**: the earliest and latest visit day events.
- **Seen minutes (S)**: L minus F in whole minutes.
- **Single sighting**: one visit day event, or all visit day events within 5 minutes of each other.
- **Recording proof**: step 5 shows at least one event, from anyone, on any of the entry cameras on the billed date between 2 hours before the billed start and 2 hours after the billed end (or anywhere on that date when the bill has no times), and no warning reports those cameras offline or missing recordings in that window.
- **Tolerance (T)**: the user's tolerance in minutes, default 10.

## Results for a billed visit

Apply the first rule that fits.

| # | Situation | Result | What to show |
|---|---|---|---|
| 1 | Helper has visit day events, not a single sighting, and the difference D = B − S is from −T to +T, both ends included | `Confirmed` | B, S and D |
| 2 | Same as 1 but D is greater than T | `Billed more than seen` | D minutes, as "billed D minutes more than the cameras saw" |
| 3 | Same as 1 but D is less than −T | `Seen more than billed` | −D minutes, as "seen −D minutes longer than billed" |
| 4 | Single sighting | `Inconclusive` | "arrival or departure not recorded"; no minutes |
| 5 | No visit day events and recording proof exists | `Not seen` | "not seen on the entry cameras while they were recording"; B minutes |
| 6 | No visit day events and no recording proof | `Inconclusive` | "recording not confirmed"; no minutes |

Extra notes, which never change the result:

- When the bill has start and end times and F or L differs from them by more than T, add a note such as "arrived 35 min after the billed start, left 40 min after the billed end".
- Helper events on a date with no billed visit are listed as `Seen, not billed`, with F, L and S, as possible unbilled time. Single sightings on such dates are listed with no minutes. An event already used for a billed visit, such as the morning departure after an overnight visit, is never counted again.
- Two billed visits on the same date with start and end times (a split shift) are compared one by one: split that date's helper events at the time halfway between the first visit's end and the second visit's start, and apply the rules to each part with its own visit. When the bill gives only hours, compare the date as one visit: B is the sum of the hours and S runs from the first to the last event of that date.

## Totals

- **Billed**: sum of B over all billed visits.
- **Confirmed**: sum of B over `Confirmed` visits.
- **Billed more than seen**: sum of D over `Billed more than seen` visits.
- **Seen more than billed**: sum of −D over `Seen more than billed` visits, plus S over `Seen, not billed` dates.
- **Not seen**: sum of B over `Not seen` visits.
- **Inconclusive**: sum of B over `Inconclusive` visits, with each reason.

Show each total in hours and minutes. Show money only when the bill prints an hourly rate: minutes × rate ÷ 60, rounded to the cent, labelled "at the printed rate". Never net the two directions into one number; show them side by side.

## Draft rules

In Draft mode there is no bill. For each date with helper events: a single sighting gives a line marked `Inconclusive` with no hours; otherwise the line shows F, L and S. The draft total is the sum of S. Label it "time between first and last sighting at the entry cameras", not working time.

## Things the rules never do

- Use events of anyone other than the named helper, except as recording proof counts.
- Treat an event whose identity the platform did not record as the helper, even if the user suggests it.
- Deduct or add breaks, travel or overtime; the cameras show passages through the entry, not work.
- Turn `Inconclusive` into `Not seen`, or any result into a judgement about honesty.
