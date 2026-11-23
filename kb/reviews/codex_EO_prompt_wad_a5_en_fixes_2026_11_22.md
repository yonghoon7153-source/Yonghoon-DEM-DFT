---
title: "EO 프롬프트 — W_ad a5 묶음 Codex EN (NO-GO · P0 1 · P1 3 · P2 1 · P3 1) 고침 확인: 끊긴 단의 원문 검사 · killed.json 대조 · 중단 영수증 · 시작점 유실 · 옛 반송 묶음 — 업체 발송 GO 여부"
date: 2026-11-22
updated: 2026-11-22
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, prompt, letter]
letter: EO
track: wad
channel: codex
kind: prompt
status: 발송 2026-11-23 (사용자) · 회신 대기 · 기준 커밋 68f683462 → 고침 b84907868 (도구) · 8fd051a22 (묶음) · 묶음 MANIFEST b01d0861… · 돌연변이 84/84
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). Codex EN (NO-GO) 다음 편지다. EN 원문 `codex_EN_reply_wad_a5_em_fixes_2026_11_22.md` · 첨부 `codex_EN_evidence_2026_11_22/`.
> ⛔ 점착 W 값은 싣지 않는다 (문턱 · 상태 · 종료 코드만). ⬇ 아래 **보내는 글** (영어) 만 발송한다. 회신이 오면 `codex_EO_reply_wad_a5_en_fixes_2026_11_22.md` 로 원문 보존.
> ⚠ GO 가 와도 업체 발송은 사용자가 정한다 · DEM 편지 10 은 a5 가 끝난 뒤 (사용자 11-20).

---

**[W_ad · a5] Fixes for your EN review — please confirm before we send the package to the operator**

## 0. What we are asking

Your EN review (base `68f683462`, MANIFEST `8439e129…`) returned **NO-GO**: P0 ×1 (a killed c2 whose raw output contradicts a restart or carries
foreign row headers was still treated as a confirmed end, so c1's secondary value was adopted), P1 ×3, P2 ×1, P3 ×1. EM's earlier
counter-examples stayed closed. We fixed every EN item and rebuilt the package (**MANIFEST `b01d0861e382ab3af04278dd115e6b7d088c543af9bfbfea80a7e079c60867b0`**). Please review **only the EN fixes**:
for each EN finding — closed (GO / conditional / NO-GO)? Did a fix open a new hole? May this package go to the operator?
Physics settings, the ladder, thresholds, the secondary rule and the G4/G5 arithmetic are unchanged.

## 1. Scope

- Base = `68f683462` (what EN reviewed). Fixes: `b84907868` (tools · tests) and `8fd051a22` (package rebuilt · build log). Records-only commits in between: `609454492` (EN letter) · `2b0fc9aa8` (your reply and attachments, verbatim); commits after `8fd051a22` are records only too (this letter · build-log mutant totals · an unrelated b2o3 run-log entry and raw-output recovery).
- `git diff 68f683462 8fd051a22 -- tools/wad/build_a5_vasp_package.py tools/wad/build_v5_vasp_package.py` (tool sha256 `83695d51…` · `90065ed5…`).
- Package `db/inputs/wad_a5_vasp_2026_11_20/` — changed files: `run_a5.sh` · `README.md` · `jobs.json` (tool sha) · `MANIFEST.sha256`. Job inputs (INCAR ×4 · POSCAR · KPOINTS · POTCAR spec) are byte-identical.
- Build log `db/properties/wad_a5_build_log_2026_11_20.json` key `⑥`.

## 2. Rules (sealed — not up for review)

Same as EN §2: Amendment 5 v2 ladder A5 → c1 → c2; Interpretation 1 (next stage only after a confirmed SCF_NOT_CONVERGED or a run failure /
killed attempt with ≥ 1 electronic row; 0 rows → exit 7; RESTART_NOT_HONOURED · SCF_UNVERIFIED · settings-echo mismatch → exit 8);
c1's secondary value only after c2 itself ended in a confirmed state.

## 3. Finding by finding — what changed

| EN | Fix (runner `run_a5.sh` · checker `check_return` · collector) | Evidence: your scenario ("was" = your reported result) → now (our selftest case) |
|---|---|---|
| **P0** killed c-stage drops observed contradictions | **Runner**: new `killed5` (called from `gate5` on the killed branch, after the row count and the settings echo, in the same order as a finished attempt): ① row headers must be the stage's own (A5 · c1 = DAV/RMM, c2 = SDA/CGA) → else `SCF_UNVERIFIED`; ② for c1 · c2 the raw restart evidence — OUTCAR `ISTART 1 job` · `ICHARG 0 charge` · no `WAVECAR not read` · the registry's restart phrase · OUTCAR NKPTS/NBANDS/ENCUT = start-point header → else `RESTART_NOT_HONOURED`; ③ the killed.json record (below). Any failure → `REVIEW` → exit 8. **Checker**: `killed_problems` mirrors the same three checks in the same order; a killed attempt that fails one gets that status (killed stays true), `a5_class` maps it to REVIEW → STOPPED_FOR_REVIEW. **Collector** (`a5_c2_confirmed`) only accepts a killed c2 whose status is still INCOMPLETE_ATTEMPT. What the killed path still cannot see: the three WAVECAR sha values (no end record is written when the runner is killed; the copy's sha was checked before launch) | c2 `ISTART=0, ICHARG=2`, killed after 7 rows → `--killed` → re-run: was exit 1 · NO_PRIMARY_VALUE · c1 secondary → now **exit 8 · STOPPED_FOR_REVIEW (c2 RESTART_NOT_HONOURED) · none** (selftest `ken1`). c2 rows `XYZ:` → was the same adoption → now **exit 8 · STOPPED_FOR_REVIEW (c2 SCF_UNVERIFIED) · none** (`ken2`). Also covered: missing restart phrase (`ken3`) · NBANDS 873 vs start header 872 (`ken4`) · phrase present but OUTCAR ISTART 0 (`ken5`). **Positive control kept**: c2 cut after 7 valid SDA/CGA rows with intact restart evidence → `--killed` → exit 1 · NO_PRIMARY_VALUE · c1 secondary adopted (`kill2b`; the full-length `kill2` too) |
| **P1** killed.json not bound to the attempt · run_aborted receipt optional | **killed.json** (runner `killed5` ③ and checker): one line starting `{"job": "` · job · rung · `run_id` = attempt.start · `osz_rows` = the current row count · `wall_s` decimal seconds · `recorded_s` ≥ attempt start · no key twice (runner field readers return empty on a duplicate; checker parses with a duplicate-rejecting hook) → else `KILLED_RECORD_MISMATCH` (exit 8 / STOPPED_FOR_REVIEW). **Receipts**: every `run_aborted/<job>_<stage>_<k>` must hold a readable one-line `infra_abort.json` with job · rung = folder · `wall_s` seconds or `UNKNOWN` · integer `recorded_s` ≥ attempt start → else LADDER_VIOLATION | killed.json truncated to `{` in the return: was c1 secondary → now **STOPPED_FOR_REVIEW · none** (S2 variant `killed_trunc`); same for rows − 1 · other run_id · rung c1 · `wall_s` `0100` · duplicate key (wrong value first) · two lines · `recorded_s` < start (S2 variants; runner side: `kv0`–`kv7` → exit 8). Receipt deleted after a successful A5 0-step retry: was OK (order check fell back to `attempt.json` `t_end`) → now **LADDER_VIOLATION** (`rcpt`); also truncated · wrong rung · string or missing `recorded_s` · bad `wall_s`. Positive control: intact receipt → OK |
| **P1** lost `start_point.json` re-written after an aborted c1 | **Runner**: before the start point is first written, and before A5 or c1 may be (re)launched, it now also looks under `run_aborted/` for c-stages (A5 NEW guard · start-point branch · c1 NEW guard) → `REVIEW` exit 8, nothing launched, nothing re-derived. **Checker**: `start_point.json` `written_s` must be an integer ≤ the earliest c-stage start, `run_aborted/` included → else LADDER_VIOLATION | c1 0 rows → `--infra-abort` → delete `start_point.json` → re-run: was a re-written start point (2 s after the first c1) and c1 primary adopted → now **exit 8 · c1 not launched · START_POINT_MISSING · none** (`splost`). Old-runner record (written_s = first c1 + 2 s): **LADDER_VIOLATION** (`spw`); string / missing written_s too. Guards: A5 folder gone with an aborted c1 → exit 8 without relaunching A5 (`ga5`); c1 folder gone with an aborted c2 → exit 8 without launching c1 (`gc1`). Positive control: same history without the loss → OK (`spok`) |
| **P1** stale PACK_ONLY bundle after a failed final pack | On a re-run after an end, the runner now checks that `a5_return.tgz` matches its one-line `.sha256` (`sha256sum -c`) **and** that the bundle's `run/final.json` is byte-identical to the current one; otherwise exit 4 with "PACK_ONLY=1 bash run_a5.sh" (no stage is launched either way) | intermediate PACK_ONLY bundle → final pack fails (exit 4) → plain re-run: was exit 0 + "send the bundle" (bundle had no final.json · LADDER_INCOMPLETE) → now **exit 4** + repack hint; after `PACK_ONLY=1` → re-run exit 0 · OK (`stale`) |
| **P2** collector accepts RUN_FAILED with 0 / missing rows | `a5_c2_confirmed` requires an integer `osz_rows` ≥ 1 for every confirmed end (SCF_NOT_CONVERGED · RUN_FAILED · killed) | RUN_FAILED with rows 0 · missing · `True` · `"30"`, SCF_NOT_CONVERGED with 0, killed without rows → no c1 secondary; RUN_FAILED with 7 rows → confirmed (V5 selftest) |
| **P3** README §3 | Split into "A5 → c1 (start-point choice)" and "c1 → c2 (next-stage condition)"; the exit-8 line now names foreign row headers and a killed.json that does not match its attempt, and says killed attempts get the same raw checks; §4 adds the exit-4 case for a stale bundle | README diff |

## 4. Tests

- Selftests: a5 **163/163** (was 124) · V5 **313/313** (was 303) · round2 194/194 (unchanged file) — python 3.11 · `dftd3` 1.6.0.
- Mutants: `build_a5_vasp_package.py --mutants --jobs 3` — **84/84 caught** (the 51 earlier ones re-run on the new tool + 33 new, m52–m84 · tool `83695d51`: one for each new runner, checker and collector gate; e.g. m56 = the runner never calls `killed5` (the EN behaviour), m68 = the checker never calls `killed_problems`, m67 = the runner skips the bundle/final-record check). Two new tests were adjusted so that a single gate is the only thing that can catch its mutant: an OUTCAR with ISTART 0 **but** the restart phrase present (`istart0p`, otherwise the phrase check masks the ISTART check), and a two-line killed.json whose `recorded_s` still ends its line (otherwise the integer reader masks the one-line check).
- EM probes p1–p9: re-run on the new tools — output identical to the EN-reviewed tools (normalised for timestamps and hashes).
- Collector regression: the 11-20 G5 aggregate re-run with the patched V5 collector → rc 3 · JSON byte-identical (sha `afecfa08…`) · console output identical (compared only, never displayed).

## 5. Please look especially at

1. The runner and checker now evaluate killed attempts with the same three checks in the same order. Is there a killed-attempt record the runner accepts (exit 1 path) but the checker refuses, or the reverse, outside the cases where the checker is deliberately stricter (duplicate keys in fields the runner does not read)?
2. Is there any remaining way to re-write `run/start_point.json` after a c-stage started, now that `run_aborted/` is consulted?
3. The receipt requirement treats `wall_s: "UNKNOWN"` as a valid receipt (the runner already refuses to launch the next stage while any wall clock is unknown). Agree?
4. The stale-bundle check compares only `run/final.json` inside the bundle with the current file. After an end every record command is refused, so we think that is sufficient — agree?
5. Your Q-EN-4 note — `start_point.json` is written before c1's preparation, so it proves the **choice** of start point, not the restart itself — we agree and kept that meaning: the restart is proven per c-stage (WAVECAR.info sha triple for finished attempts · the raw checks above for killed ones). The new `written_s` rule does not fire on the prep-failure retry you tried (written before the first launch, the launch comes later).

## 6. Questions

- **Q-EO-1**: P0 (killed c-stage raw checks in runner and checker) closed? Positive controls adequate?
- **Q-EO-2**: P1 killed.json binding and run_aborted receipts closed?
- **Q-EO-3**: P1 lost start point closed (runner guards + checker `written_s`)?
- **Q-EO-4**: P1 stale bundle · P2 collector rows · P3 README closed?
- **Q-EO-5**: Any new hole introduced by these fixes?
- **Q-EO-6**: Send approval — may package MANIFEST `b01d0861e382ab3af04278dd115e6b7d088c543af9bfbfea80a7e079c60867b0` go to the operator?

## 7. How to reproduce

- `python3 -I tools/wad/build_a5_vasp_package.py --selftest` · `… --mutants --jobs 3` (or `--mutants m52 m53 …` for the new ones) · `python3 -I tools/wad/build_v5_vasp_package.py --selftest` (needs `dftd3` 1.6.0 — PyPI name `dftd3`).
- `python3 -I tools/wad/build_a5_vasp_package.py --build --out <new folder>` → `diff -r` with `db/inputs/wad_a5_vasp_2026_11_20` · MANIFEST sha.
- The fake VASP now accepts `behaviour@N` in the plan (write N electronic rows, no end record — a job cut by the scheduler) and a `FAKE_TAR_FAIL=1` wrapper fails only the final `tar czf`.

## 8. Reply format

Per question: verdict (GO / conditional / NO-GO) · evidence (file:line or test) · minimal fix if not GO. Please do not print W values.
