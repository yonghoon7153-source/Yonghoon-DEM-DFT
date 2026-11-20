---
title: "EM 회신 — a5 묶음 독립 리뷰 (NO-GO · P0 2 · P1 4)"
tags: [review, internal, wad, vasp, a5]
status: 회신 수령 2026-11-20 · NO-GO · 고침 진행
letter: EM
date: 2026-11-20
kind: internal independent review (reply)
track: W_ad (DEM 협업) — 1저자 = 사용자
subject: 은 e70 far 재시도 a5 묶음 발송 전 독립 리뷰 (HEAD 28ef1ea3)
verdict: NO-GO (P0 2 · P1 4) — 아직 보내지 않는다
---

# EM 회신 — a5 묶음 발송 전 독립 리뷰 (원문 · 영어 · 리뷰어 보고 그대로 옮김)

Independent review of the a5 VASP retry package (HEAD 28ef1ea3). I ran probes against the generated run_a5.sh with the module's fake VASP, plus the real 5.4.4 a4 outputs. The package should not go out yet. Two paths adopt a value the amendment forbids, and four more are likely to hurt in normal operator use. Most share one root cause: the runner works out the start point again on every run from whether the A5 WAVECAR file is still on disk, it moves on after any non-OK stage, and the checker never confirms that c2 actually ran or that the stages ran in order.

## Findings, most severe first

**P0-1 — c1's secondary value is auto-adopted when c2 never ran**
- Where: build_v5_vasp_package.py:1091-1139 (adopt_a5) and build_a5_vasp_package.py:1092-1120 (check_return). The checker only flags a c2 that exists when it shouldn't; it never flags a missing c2, and the resulting NO_PRIMARY_VALUE is in A5_OK_STATES.
- Scenario (reproduced): c1 stalls (SCF_NOT_CONVERGED, small stall width) and c2 never runs. Three ways reproduced: the 180 h cap stops the ladder (runner exit 5, "1저자 결정을 기다려"); c2 prep fails, e.g. disk full while copying the 6.8 GB WAVECAR, leaving a folder with input copies only (simulated); a c2 0-step is recorded with --infra-abort and not re-run.
- Result: checker NO_PRIMARY_VALUE with no violation; collector adopts c1 by the secondary rule. Skips "c2 primary" in the c1 primary → c2 primary → c1 secondary order and overrides the spec's "cap stop → 1저자".
- Fix: if c1 is not OK and c2 is missing, or incomplete without killed.json, or only under run_aborted/, return a status outside A5_OK_STATES (e.g. LADDER_INCOMPLETE). Don't consider c1 secondary unless c2 was actually used up. Add selftest negatives for all three triggers.

**P0-2 — stages run out of order, and c2's secondary value displaces a c1 that converged**
- Where: checker has no time-order check (check_return); runner re-derives the start point each run from the current A5 WAVECAR (build_a5:595-597); drop5 deletes that WAVECAR in final states (build_a5:570-573); --infra-abort accepts a stage even when later stages exist (build_a5:374-419).
- Route (i), reproduced: c1 dies with 0 rows but the runner survives, so c2 runs, stalls and ends with exit 1; drop5 deletes the A5 WAVECAR → operator records --infra-abort c1 as the README says and re-runs → c1 runs again from W0 and converges ("✅" exit 0) → checker relabels c1 RESTART_NOT_HONOURED and adopts c2's secondary value.
- Route (ii), reproduced: A5 has 0 rows, so c1 runs from W0 and converges (start correct at the time) → operator records a late --infra-abort A5 → on re-run the start flips to A5: c1 becomes RESTART_NOT_HONOURED, c2 runs from A5 and stalls, c2's secondary value is adopted with no violation flagged.
- Fix: checker: require A5 end ≤ c1 start ≤ c1 end ≤ c2 start (attempt.json t_start/t_end) and every aborted attempt older than the next stage; else LADDER_VIOLATION · collector: no auto-adoption if any c-stage is RESTART_NOT_HONOURED · runner: persist the start point once (e.g. run/start_point.json at c1 launch); --infra-abort <st> refuses when a later stage exists.

**P1-1 — re-running after a converged c1 launches c2 and blocks the valid result**
- Where: run_a5.sh lines 464-467, 489-491, 500-508.
- Scenario (reproduced): after a clean exit 0 the operator runs `bash run_a5.sh` again (the README invites it: "다시 돌리면 기록을 다시 판정해…"; also plausible instead of PACK_ONLY after exit 4). Runner logs "A5 자격 미달 — ⓐ WAVECAR 없음" and judges c1 against the W0 sha, so c1 shows RESTART_NOT_HONOURED; c2 starts from W0 (up to 400 steps, ~44-88 h); ends "✅ 끝" and overwrites a5_return.tgz; checker returns LADDER_VIOLATION; nothing adopted.
- Fix: persist the start point; if c1 is done and OK, finish 0 before deriving anything; refuse to launch when the ladder is complete. README: after exit 0/1/6 only re-pack with PACK_ONLY=1.

**P1-2 — a stage with 0 electronic steps moves the ladder on; one launch failure uses up all three stages**
- Where: run_a5.sh 489-491, 500-508 move on after any non-OK result. Round-2 (build_round2:837,842) and amendment 4 "다음_단_자격" only move on after SCF_NOT_CONVERGED or RUN_FAILED.
- Scenario (reproduced): a VASP_CMD typo (rc 127, no output) runs A5 → c1 from W0 → c2 within seconds and exits 1 "그대로 반송". c1 and c2 are labelled RESTART_NOT_HONOURED although VASP never started. --infra-abort can restore only 2 of 3 stages (limit 2); the third is lost to an infra event, and a5 is the last attempt.
- Fix: 0 rows → stop with a message pointing to --infra-abort or to us. Move on only after SCF_NOT_CONVERGED, RUN_FAILED (≥1 row), or a killed attempt with rows.
- Decision for the user: should c1 RESTART_NOT_HONOURED move on to c2? Amendment 5 says "c1 이 주 기준 OK 가 아니면 자동"; amendment 4's rule says no. Recommendation: stop and go to 1저자.

**P1-3 — a relative or mistyped W0 path is silently treated as `none`, then pinned**
- Where: run_a5.sh:20 (`cd "$HERE"` before reading any paths) and 380-399.
- Scenario (reproduced): operator runs from the parent folder with a W0 path relative to it. Runner can't find the file, records "파일이 없거나 읽을 수 없다" (verified 0). A5 starts fresh, the W0 fallback is gone; if A5 then fails, the job closes with no value. Correcting the path and re-running → exit 2 ("첫 기록과 다르다"), no documented recovery.
- Fix: resolve paths before the cd or require absolute paths. Exit 2 if a non-`none` path is missing/unreadable. Start A5 fresh only on sha/size/header mismatch.

**P1-4 — fact check before sending: W0 is probably already deleted**
- Evidence: the round-2 runner the operator used (db/inputs/wad_round2_vasp_v5_2026_10_22/run_all.sh:516-518,524-525) ends the a4 ladder with drop_wav, which deletes stageA/WAVECAR when the final state is SCF_NOT_CONVERGED — exactly the pilot status. The returned env.txt has no "남긴다" (keeping) line.
- Conflict: contradicts RETURN_NOTES "stage-ⓐ WAVECAR 포함", which amendment 5 ⓪ relies on.
- Ask the operator first: `ls -l` and `sha256sum` of that path before shipping. Warn them not to re-run the round-2 runner's stage P (if the file exists, that run would delete it).

**P2 items**
- Records missing from the adopted value: adopt_a5 and rec["a5_adoption"] don't carry the start point; the spec asks for "시작점 = 보존 ⓐ" when A5 is ineligible. total_w_labels / total_w_citable (build_v5:1440-1453) get no a5 label when G4 PASS came through a5, so a sample W can be marked citable without "G5 원시 결과를 본 뒤 정한 재시도".
- Prep failure blocks the stage permanently: run_one5 creates the folder before the 6.8 GB copy (run_a5.sh 406-421). Every later run exits 1, the message says "값 없음 — 그대로 반송", and the collector notes "a5 값 없음 (최종 — 이 잡은 닫는다)" (reproduced). Fix: prepare in a temp folder and rename on success, or remove it on failure.
- Lock only checks the local PID (kill -0): under SGE, a login-node command or a second submission on another node sees a live lock as stale — can pack mid-run, write killed.json into a live attempt, or delete the live run's lock. Fix: store hostname with the PID; refuse when the host differs.
- Runner and checker can disagree on whether A5 qualifies (runner: SCF result only; checker: also a clean settings audit). If A5 fails the audit, the runner starts c1/c2 from A5, the checker expects W0, and the whole a5 is labelled RESTART_NOT_HONOURED. Should get its own status.
- 0-row attempts get the wrong label: RESTART_NOT_HONOURED instead of SCF_UNVERIFIED (no_rows), because the restart check runs first (run_a5.sh 200-203; build_a5 963-975).
- Unpacking into the round-2 folder (reproduced): cap ledger counts round-2 attempts → immediate exit 5 "누적 257 h > 180 h — 1저자 결정을 기다려"; return rejected as UNREGISTERED_ATTEMPT; round-2's MANIFEST, README and jobs.json overwritten. Runner should refuse when run/ contains anything else.

**P3 — README and usability gaps**
- No parallel-layout instruction: W0 has 872 bands only with 64 ranks, KPAR 2, NCORE 4; without the perf file the default becomes 896 bands and steps are slower than the cap assumes. Nothing checks that c1/c2 use the start WAVECAR's band count.
- No walltime guidance: the whole ladder can take ~165 h and a stage cut by the scheduler is lost. Give per-stage worst cases (A5 ~33 h, c1 ~44 h, c2 ~88 h).
- Missing: absolute paths; unpack into an empty folder; ~14-21 GB extra disk on top of W0; keep W0 until a5 finishes; how to clear the pinned W0 record.
- Exit codes: 5 also means "interrupted attempt, record --killed"; the exit-1 message after a prep failure wrongly says "그대로 반송".

## Checked and found sound
- INCARs: the four files differ from the sealed INCAR exactly by the spec's changes; no LMAXMIX or BMIX. MANIFEST and README sha agree, shipped run_a5.sh equals the builder output, tool shas in jobs.json match. SEALED_ENV (W0 sha/size/header, registry, restart phrase, 180 h, limit 2) matches the amendment and the a4 record.
- Operator data: W0 never modified, moved or deleted in any probe (only copies removed). Attempt folders use atomic mkdir and are never overwritten. Return packing never includes WAVECAR/CHGCAR/POTCAR bodies and includes w0_check.json. Cap checked before each stage, including infra-abort and killed time; unknown wall clock stops the ladder.
- Restart check: c1/c2 require source = copy = end = expected sha, ISTART 1, ICHARG 0, no "WAVECAR not read", and the positive phrase. A5's end sha not used.
- Parsing: SCF contract ①-⑤ and row-header gate agree between bash and Python on the selftest probes and on the real 5.4.4 a4 OSZICAR/OUTCAR. Settings checks read all needed OUTCAR values from real output. Restart phrase found in the real stdout.log. Broyden history length reads 44 on the real a4 files, matching the amendment's diagnosis.
- Secondary rule and G4: c1/c2 only, confirmed non-convergence only, ≥100 steps, both windows, max(range, mean shift), area from the bound job, ≤0.002 threshold, both-secondary mismatch check, primary beats secondary, A5 and old attempts refused. G4 adds u_W correctly. Labels attached to the adopted record, the G4 e70 entry and G5; adoption history covers all four attempts.
- Collector reproduction: without a5 input the current collector reproduces the 11-20 G5 aggregate byte-for-byte (output only cmp'd, never displayed).
- Selftests: a5 67/67 and V5 279/279 pass.

No repository file was changed (git status clean); no W values printed or written. Probe scripts (run with the venv python and -B) are in the session scratchpad a5indep/probes/: harness.py, p1_rerun_after_ok.py, p2_launch_failure.py, p3_cap_then_adopt.py, p3b_c2_aborted.py, p4_w0_path.py, p5_real_parse.py, bash_real.sh, p6_c1_zero_then_abort.py, p7_prep_fail.py, p8_a5_zero_late_abort.py, p9_colocated.py.

---

## 주 세션 처리 (2026-11-20)

- 사용자 결정 (P1-2 의 질문): AskUserQuestion '멈추고 1저자에게 (Recommended)' — 다음 단은 앞 단이 확인된 미수렴 · 실행 실패 (전자 스텝 ≥ 1) 로 끝났을 때만 · 스텝 0 은 멈추고 0 스텝 기록 뒤 같은 단 다시 · 재시작 미이행 · 미확인 · 설정 위반은 멈추고 1저자 → 결정 `D-2026-11-20-wad-aprime-v5-e70-a5-interp1` (개정 5 해석 1 · 개정 파일은 봉인 그대로)
- P1-4 사실 확인: 외주 2차 러너 drop_wav 는 FINAL 이 SCF_NOT_CONVERGED 면 `rm -f` (INCOMPLETE_ATTEMPT · RESTART_NOT_HONOURED · SCF_UNVERIFIED · PREP_FAILED 일 때만 남긴다) · 반송 env.txt 마지막 a4 줄은 '✗ … 값 없음 (SCF_NOT_CONVERGED)' 이고 '남긴다' 줄 없음 → W0 는 지워졌을 가능성이 높다 (RETURN_NOTES 문장과 어긋남) · 개정 5 는 이 경우를 이미 정했다 (A5 새로)
- 주 세션 구현 해석 (보수 · 개정 '순서' 규칙에서 따름): c1 보조 채택은 c2 가 확인된 결과 (확인된 미수렴 · 실행 실패/끊김 ≥ 1 행) 로 끝났을 때만 — c2 가 없거나 미확인 · 재시작 미이행 · 설정 위반이면 c2 주 기준이 미정이라 자동 채택 없음 → 1저자
- 고침: 도구를 만든 갈래 에이전트에게 위 전부 (P0 · P1 · P2 · P3) 를 넘김 — 고침 뒤 다시 검토 · 필요하면 두 번째 독립 리뷰
