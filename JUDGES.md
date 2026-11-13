# Review Fair Hours in five minutes

No account, NAS or install is needed for steps 1–4. Step 5 needs Node and Python.

| Min | Open | What to look for |
|---|---|---|
| 1 | [docs/assets/sample-report.png](docs/assets/sample-report.png) and [the run it came from](eval/v2/runs/skill-final/C01/final.md) | One sentence in, one table out. The differences go both ways (Nov 4 against the helper, Nov 5 in her favour). They are priced at the printed rate and never netted. Nov 6 is `Inconclusive` because there was only one sighting. |
| 2 | [skill/fair-hours/SKILL.md](skill/fair-hours/SKILL.md), sections *Required input* and *Workflow* | The notice gate (item 7) comes before any camera query. There are eight steps and nine delegate templates, each naming its CLI and action. Step 5 asks for other people's passages **without names**. The only write is step 8, after the user says yes and the NAS approval prompt runs. |
| 3 | [references/matching-rules.md](skill/fair-hours/references/matching-rules.md) | The 11-rule table. Read rules 6, 9, 10 and 11: an unrecognised person near the door, or a camera gap, gives `Inconclusive`. `Not seen` needs the camera to have recognised *other* people during the billed time. |
| 4 | [BENCHMARK-RESULTS.md](BENCHMARK-RESULTS.md) | Expected and actual results for every case. The expected outcomes were committed before any run, and 6 cases were written blind by an author who never saw the rules. A baseline (same model, same tools, same policies, no Fair Hours rules) is scored the same way. The misses are documented, not hidden. |
| 5 | Terminal | Run `node $ULIYA_SKILL_KIT/scripts/check-skill.mjs skill/fair-hours`, which gives `static-pass` with 0/0. Run `python3 tools/build_zip.py`, which rebuilds and re-checks the ZIP. Run `python3 eval/v2/score_v2.py eval/v2/runs/skill`, which re-scores the recorded runs. |

## Where each judging criterion is answered

| Criterion | Where |
|---|---|
| User Value | The problem and the two modes are in [SKILL.md § Goal](skill/fair-hours/SKILL.md). The report shows both directions, money at printed rates and bill arithmetic: [report-format.md](skill/fair-hours/references/report-format.md). Agreed minimum and rounding terms are in matching rule 5. |
| Innovation & Differentiation | Recording proof from anonymous passages, the rule that unrecognised passages count *for* the helper, two-direction totals and a timesheet drafted from the camera: [matching-rules.md](skill/fair-hours/references/matching-rules.md). The A/B against a generic assistant is in [BENCHMARK-RESULTS.md](BENCHMARK-RESULTS.md). |
| Technical Quality | Five experts and nine templates; the delegation states per step are in [states-and-recovery.md](skill/fair-hours/references/states-and-recovery.md). The checker passes 0/0. The independent audits are in [loop/audits/](loop/audits/). |
| AI NAS Fit & Validation | Local face identities, the camera event timeline, documents, OCR and an approval-gated save: [README § Built on UGREEN AI NAS](README.md#built-on-ugreen-ai-nas). Privacy limits are in [privacy-and-fairness.md](skill/fair-hours/references/privacy-and-fairness.md). The finalist plan, with a no-camera fallback, is in [validation-plan.md](skill/fair-hours/references/validation-plan.md). |

## What is real and what is simulated

- **Real:** the Skill package and its pass on the official checker. The checker copy in this repo matches the kit's `check-lib.mjs` line for line, apart from indentation (SHA-256 of the whitespace-normalised text: `890b3db3…078d`, for both the kit file and this copy).
- **Simulated:** the NAS experts (`eval/v2/mock_delegate.py` returns fixture data), the user (`mock_user.py`) and Uliya (a stand-in model following SKILL.md). Nothing has run on a UGREEN NAS.
