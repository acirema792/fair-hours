# Claims and evidence

Each public claim, with how strong its evidence is.

- **REPRODUCIBLE:** a command in this repo produces it.
- **RECORDED:** the run files are committed and can be re-scored, but re-running them needs a model.
- **NOT CLAIMED:** we say so explicitly so nobody reads it in.

| Claim | Tier | Evidence |
|---|---|---|
| The Skill passes the official checker with 0 errors and 0 warnings. | REPRODUCIBLE | `node $ULIYA_SKILL_KIT/scripts/check-skill.mjs skill/fair-hours`. `python3 tools/build_zip.py` refuses to build otherwise and re-checks the unzipped copy. |
| The ZIP is Markdown only and within the size and file limits. | REPRODUCIBLE | `tools/build_zip.py` and `dist/SHA256SUMS.txt` |
| The ten proposal answers total 500 words or fewer. | REPRODUCIBLE | `python3 proposal/build_proposal.py` prints the count and refuses to build over 500. |
| Across 35 bench cases, the same small model made 0 harmful calls with Fair Hours and 8 without it. It got 31/35 cases fully right with Fair Hours and 13/35 without. | RECORDED | Runs: `eval/v2/runs/skillhaiku-r3`, `eval/v2/runs/baselinehaiku-r3`. Tables: `python3 tools/make_benchmark_md.py`, which writes [BENCHMARK-RESULTS.md](BENCHMARK-RESULTS.md). |
| Expected outcomes were fixed before the runs. | RECORDED | Git history of `eval/v2/expected`, `eval/v2/blind/expected` and `eval/v2/round2/expected`. These paths are protected in `gate.yaml`. |
| 6 cases were written blind by a separate author who never saw the rules. | RECORDED | `eval/v2/blind/README.md`. The first-contact blind score is disclosed in the History table of BENCHMARK-RESULTS.md. |
| The baseline had the same tools, policies and labels. | RECORDED | `eval/v2/RUNNER_v2.md` and `eval/v2/make_prompts_v2.py` |
| Every miss is explained. | RECORDED | [eval/v2/MISSES.md](eval/v2/MISSES.md) |
| Independent audits scored the entry, and the fixes were verified. | RECORDED | [loop/audits/](loop/audits/), `loop/ledger.json` |
| Fair Hours itself calls no external service. | REPRODUCIBLE | Every delegation in SKILL.md targets a NAS expert. Run `grep -n "delegate" skill/fair-hours/SKILL.md`. |
| It works on a real UGREEN AI NAS. | NOT CLAIMED | Nothing has run on a NAS. [validation-plan.md](skill/fair-hours/references/validation-plan.md) lists what finalist day must confirm. |
| The bench measures camera or face-recognition accuracy. | NOT CLAIMED | The experts are mocks returning fixture data. The bench measures whether the rules are followed. |
| Uliya's own model behaves like the stand-in. | NOT CLAIMED | Claude Haiku stands in for a small local orchestrator. |
