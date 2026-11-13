# Loop state
Round: 1 complete (fixes applied, awaiting bench v2 + round-2 audit)
Scores: round-1 audit 6.4
Open findings: none unaddressed from round 1 (all 22 actioned; verification pending in round 2)
## Escalations (for the person)
- E1: v1 case C03 expected `Not seen` encodes audit finding F1 (an unrecognised passer may be the helper). v1 left untouched; v2 corrects it (C03 -> Inconclusive) and adds C03B for the `Not seen` path. Please confirm.
- E2: v1 scorer could not parse dates like "3 Nov", under-counting the baseline (22/30 -> 24/30 rows). v1 scorer untouched; corrected numbers come from eval/v2/score_v2.py --expected eval/expected. Published claims will use corrected numbers.
