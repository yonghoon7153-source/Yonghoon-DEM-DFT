---
title: "EN 프롬프트 — W_ad a5 묶음 (은 쪽 G4 e70 far 재시도) 고침 확인: 내부 독립 리뷰 EM (NO-GO · P0 2 · P1 4 · P2 · P3) 대응 — 업체 발송 GO 여부"
date: 2026-11-22
updated: 2026-11-22
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, prompt, letter]
letter: EN
track: wad
channel: codex
kind: prompt
status: 발송 2026-11-22 (사용자) · 기준 커밋 68f683462 · 묶음 MANIFEST 8439e129… → 회신 수령 NO-GO (P0 1 · P1 3 · P2 1 · P3 1 — codex_EN_reply_wad_a5_em_fixes_2026_11_22.md)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). EM (내부 독립 리뷰 · NO-GO) 다음 편지다. 사용자 2026-11-20 *"codex 리뷰도 받을까"* → 권고 '받자'.
> ⛔ 점착 W 값은 싣지 않는다 (문턱 · 상태 · 벽시계만). ⬇ 아래 **보내는 글** (영어) 만 발송한다. 회신이 오면 `codex_EN_reply_wad_a5_em_fixes_2026_11_22.md` 로 원문 보존.
> ⚠ GO 가 와도 업체 발송은 사용자가 정한다 · DEM 편지 10 은 a5 가 끝난 뒤 (사용자 11-20).

---

**[W_ad · a5] Fixes for the independent review EM — please confirm before we send the package to the operator**

## 0. What we are asking

The a5 retry package (one VASP job: the Ag-side G4 ENCUT 650 far endpoint · ladder A5 → c1 → c2) went through an internal
independent review (EM) at commit `28ef1ea3`. EM returned **NO-GO** with P0 ×2, P1 ×4, P2 items and P3 README gaps (full text in
`kb/reviews/internal_EM_reply_wad_a5_package_2026_11_20.md`). We fixed every item and rebuilt the package
(**MANIFEST `8439e129bc18d595e72f94e6501469fed4109f419c827d5b98bb1cb269d24d20`**). Please review **only the fixes**:
for each EM finding — closed (GO / conditional / NO-GO)? Did a fix open a new hole? May this package go to the operator?
The physics settings (INCARs · ladder · thresholds · secondary rule · G4/G5 arithmetic) were checked sound by EM and are unchanged — no need to reopen them.

## 1. Scope

- Base = `28ef1ea3` (what EM reviewed). Later commits that touch the tools or the package: `0718bc6b1` (the fixes) · `6a3a98ff3` (two surviving mutants → tests tightened · README wording · package rebuilt) · `68f683462` (one load-dependent mutant → test tightened · package rebuilt). Everything else in between is records only (`2cecb0fb` build log · kb · an unrelated MD track).
- `git diff 28ef1ea3 68f683462 -- tools/wad/build_a5_vasp_package.py tools/wad/build_v5_vasp_package.py` (a5 builder/runner/checker · V5 collector `adopt_a5` · `collect` labels).
- Package `db/inputs/wad_a5_vasp_2026_11_20/` — changed files: `run_a5.sh` · `README.md` · `jobs.json` (tool sha) · `MANIFEST.sha256`. Job inputs (INCAR ×4 · POSCAR · KPOINTS · POTCAR spec) are byte-identical.
- Build log `db/properties/wad_a5_build_log_2026_11_20.json` keys `④` and `⑤`.

## 2. Rules the fixes implement (sealed decisions — not up for review)

- Amendment 5 v2 (ratified 11-20): A5 (LDIPOL off) → c1 (Davidson · MAXMIX 200 · AMIX 0.1 · AMIN 0.01 · NELM 400) → c2 (ALGO All · TIME 0.1 · NELM 400); adoption order c1 primary → c2 primary → c1 secondary → c2 secondary; 180 h cap; a5 is the last attempt.
- Interpretation 1 (first author, 11-20, answering EM P1-2): the next stage starts **only** after the current stage ended in a confirmed SCF_NOT_CONVERGED or a run failure with ≥ 1 electronic step (including a killed attempt with ≥ 1 row recorded via `--killed`). 0 electronic steps → stop (exit 7; operator records `--infra-abort` and re-runs the same stage, or contacts us). RESTART_NOT_HONOURED · SCF_UNVERIFIED · settings-echo mismatch → stop (exit 8; first author).
- Conservative reading (main session, user informed): c1's secondary value may be adopted only if c2 itself ended in a confirmed state (SCF_NOT_CONVERGED · RUN_FAILED with ≥ 1 row · killed with ≥ 1 row). Otherwise LADDER_INCOMPLETE / STOPPED_FOR_REVIEW → no automatic adoption.

## 3. Finding by finding — what changed, and EM's own probes before → after

We re-ran EM's probe scripts (`kb/reviews/internal_EM_probes/`, only the tool path and scratch folder changed) against the EM-reviewed tools (before) and the fixed tools (after).

| EM | Fix | Probe: before → after |
|---|---|---|
| P0-1 c1 secondary adopted when c2 never ran | Checker returns LADDER_INCOMPLETE when c1 is not OK and c2 is missing / prep-only / without an end record / only under `run_aborted/`; collector re-checks (`a5_c2_confirmed`) even if the checker says NO_PRIMARY_VALUE | cap stop (p3): adopted c1 secondary → LADDER_INCOMPLETE, none · c2 0-step abort (p3b): adopted → exit 7, LADDER_INCOMPLETE, none · c2 prep-only (p7): adopted → LADDER_INCOMPLETE, none |
| P0-2 out-of-order stages · c2 secondary displacing a converged c1 | Start point persisted once in `run/start_point.json` at the first c-stage launch and never re-derived; checker enforces A5 end ≤ c1 start ≤ c1 end ≤ c2 start and aborted attempts older than the next stage (LADDER_VIOLATION); `--infra-abort`/`--killed <st>` refuse when a later stage exists; collector: no auto-adoption if any c-stage is RESTART_NOT_HONOURED | route (i) p6: c2 ran after c1 0 rows, A5 WAVECAR deleted, c1 later from W0 → stop at exit 7, A5 WAVECAR kept, c1 re-run from the recorded A5 start → primary · route (ii) p8: c1 ran from W0, late A5 abort, c2 secondary adopted → stop at exit 7 before c1; after the abort record A5 → c1 → primary |
| P1-1 re-run after a converged c1 launches c2 | `run/final.json` written at every end (0 · 1 · 5 cap · 8 · 6 after launch); a re-run prints it and exits with the same code without launching anything; README says re-pack only with `PACK_ONLY=1` | p1: re-run launched c2 from W0 (LADDER_VIOLATION) → launches nothing, check stays OK |
| P1-2 0-step stage moves the ladder on | Interpretation 1 (above) in runner and checker | p2 (VASP_CMD typo): A5 · c1 · c2 used up in seconds → exit 7 after A5, nothing else launched |
| P1-3 relative / mistyped W0 silently `none` | Paths resolved against the caller's cwd before `cd`; a non-`none` path that is missing/unreadable → exit 2 with nothing recorded; sha/size/header mismatch → recorded 'not verified' and A5 starts fresh; `--reset-w0` clears the record before A5 launches | p4: relative path → verified · typo → exit 2, no record · corrected path → normal run (exit 0) |
| P1-4 W0 probably deleted | README §0.2: `ls -l` + `sha256sum` first; size and sha given; `W0_WAVECAR=none` if absent; do not re-run the round-2 runner | (operator step) |
| P2 records | `a5_start_point` in every adoption record ('start point = preserved ⓐ' when W0); a5 labels propagate to `total_w_labels` / `total_w_citable` when G4 PASS came through a5 | selftests (V5) |
| P2 prep failure | stage prepared in a temp folder and renamed on success; a prep failure exits 3 and does not use up the stage | p7 c1 prep-only: 'closed for good' → LADDER_INCOMPLETE (first author) |
| P2 lock | lock stores host + PID; a lock from another host is refused with an `--unlock <host> <pid>` hint | selftests |
| P2 runner/checker A5 eligibility | every stage, A5 included, passes the same settings-echo subset (`echo5`, identical keys · regexes · tolerances in runner and checker) before its verdict — a mismatch stops the ladder for review (exit 8) instead of silently starting c1/c2 from A5; the runner's `elig5` mirrors the checker's `a_eligible` record checks, and a valid A5 record whose WAVECAR later vanished or changed goes to the first author (no fallback to W0) | selftests |
| P2 0-row label | 0-row attempts are SCF_UNVERIFIED (no_rows), not RESTART_NOT_HONOURED | p2 / p6 |
| P2 unpacking into the round-2 folder | runner refuses (exit 2) when the folder holds anything that is not a5 | p9: cap ledger counted round-2 (exit 5) → exit 2, nothing launched |
| P3 README | new-empty-folder · absolute paths · parallel layout (64 ranks · NCORE 4 · KPAR 2 → NBANDS 872) · per-stage worst wall clock (A5 ≈ 33 h · c1 ≈ 44 h · c2 ≤ ≈ 88 h) · 14–21 GB disk · keep W0 until a5 ends · exit-code table (0–8) | — |

Also unchanged and re-confirmed: EM's real-output probe (p5, the 5.4.4 a4 OSZICAR/OUTCAR) gives the same SCF contract, row gate, secondary numbers, Broyden history (44) and restart evidence before and after; the only difference is that the settings echo now also carries NELM (intended).

## 4. Tests

- Selftests: a5 124/124 · V5 303/303 · round2 194/194 (python 3.11 · dftd3 1.6.0).
- Mutants: `build_a5_vasp_package.py --mutants --jobs 3` — **51/51 caught** (1032 s · tool `751dbe30`). The table grew to 51 (a mutant for every new gate). Three needed tighter tests on the way: **m09** (runner drops the end-sha condition from `honoured`) was masked because the stage verdict re-checks the end sha itself — but the returned `WAVECAR.info` would then say `honoured: 1`, so the tests now check that field; **m18** (collector drops the ≥ 100-step rule) was invisible because the only short-c2 case ended in the same adoption either way — the test now also checks that c2 is not even a secondary candidate; **m12** (checker drops 'c2 present although c1 OK') survived only under parallel CPU load: the test copies c1 into c2, and when the fake c1 took ≥ 1 s the time-order rule raised LADDER_VIOLATION first — the test now looks for that exact reason in `ladder_violations` (caught both idle and under deliberate CPU load).
- Collector regression: the 11-20 G5 aggregate re-run with the fixed V5 collector reproduces the stored JSON byte-for-byte (sha `afecfa08…`; output compared only, never displayed).

## 5. Please look especially at

1. The start-point record: is there any path where `run/start_point.json` can be written before the c-stage that it binds, or rewritten later (re-runs · `--infra-abort` · `--killed` · `PACK_ONLY`)?
2. `run/final.json`: can a stage still launch after an end (exit 0 · 1 · 5 cap · 8 · 6 after launch), e.g. via a re-run with different environment variables?
3. The checker's time-order rule (LADDER_VIOLATION) against attempts moved to `run_aborted/`.
4. Exit 7 does not pack a return (nothing to judge yet) — is that acceptable, given README §3 tells the operator to record `--infra-abort` or contact us?

## 6. Questions

- **Q-EN-1**: P0-1 closed?
- **Q-EN-2**: P0-2 (both routes and the `--infra-abort` / `--killed` refusal) closed?
- **Q-EN-3**: P1-1 · P1-2 · P1-3 closed? P1-4 README wording adequate?
- **Q-EN-4**: P2 items and P3 README — anything still missing or wrong?
- **Q-EN-5**: Any new hole introduced by the fixes?
- **Q-EN-6**: Send approval — may package MANIFEST `8439e129bc18d595e72f94e6501469fed4109f419c827d5b98bb1cb269d24d20` go to the operator?

## 7. How to reproduce

- `python3 -I tools/wad/build_a5_vasp_package.py --selftest` · `… --mutants --jobs 3` · `python3 -I tools/wad/build_v5_vasp_package.py --selftest` (needs `dftd3` 1.6.0 — PyPI name `dftd3`).
- `python3 -I tools/wad/build_a5_vasp_package.py --build --out <new folder>` → `diff -r` with `db/inputs/wad_a5_vasp_2026_11_20` · MANIFEST sha.
- EM probes: copy `kb/reviews/internal_EM_probes/` to scratch, point `harness.py`'s `sys.path` at the tools to test, run each `p*.py` with `-B`.

## 8. Reply format

Per question: verdict (GO / conditional / NO-GO) · evidence (file:line or probe) · minimal fix if not GO. Please do not print W values.
