---
title: "ET 프롬프트 — W_ad a5 묶음 Codex ES (NO-GO) 네 건 + P2 고침 확인만 (좁은 확인 한 번): 잠금 회수 한 명령만 · 중간 반송본 증거 보존 · 끝 기록 POTCAR 는 잰 값 · 이력 벽시계 원문 대조 · 잘린 열 제목 — 업체 발송 GO 여부"
date: 2026-11-24
updated: 2026-11-24
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, prompt, letter]
letter: ET
track: wad
channel: codex
kind: prompt
status: 발송 · 회신 수령 2026-11-24 — GO (codex_ET_reply_wad_a5_es_fixes_2026_11_24.md · 업체 발송은 사용자)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). Codex ES (NO-GO · P0 2 · P1 2 · P2 1) 다음 편지다. ES 원문 `kb/reviews/codex_ES_reply_wad_a5_er_fixes_2026_11_24.md` · 빌드 기록 `db/properties/wad_a5_build_log_2026_11_20.json` ⑯ (회신 요약) · ⑰ (고침).
> ⭐ 사용자 결정 (2026-11-24): 이 네 건 (+ P2) 만 고치고 **좁은 확인 한 번** ('네 건이 닫혔나') 으로 끝낸다 — 새 구멍 찾기는 하지 않는다. 그래서 이 편지는 범위를 ES 반례 재현으로 좁히고, 새 지적은 **정상 운영 경로에서 틀린 값이 채택되거나 업체 자료가 지워지는 경우에만** 막는 것으로 적는다 (§1c).
> ⛔ 점착 W 값은 싣지 않는다 (종료 코드 · 상태 · 문턱만). ⬇ 아래 **보내는 글** (영어) 만 발송한다. 회신이 오면 `codex_ET_reply_wad_a5_es_fixes_2026_11_2x.md` 로 원문 보존.
> ⚠ GO 가 와도 업체 발송은 사용자가 정한다 · DEM 편지 10 은 a5 가 끝난 뒤 (사용자 11-20).

---

**[W_ad · a5] Your four ES findings (and the P2) — fixed; please confirm only that each ES reproduction is now closed on the rebuilt package**

## 0. What we are asking

Your ES review (package `1da64d0be`, MANIFEST `50beb026…`) returned **NO-GO** with two P0, two P1 and one P2. We fixed those five and nothing else.
This round is a **narrow confirmation**: for each ES reproduction, is it closed on the rebuilt package (GO / NO-GO)? May the package go to the operator?
We are not asking for a new review of the runner or the checker (§1c says what still counts as blocking).

## 1. Scope

- Base = `1da64d0be` (what ES reviewed). The commits after it up to the fix (your reply verbatim, build-log key `⑯`, other campaigns' records) do not touch
  `tools/wad/` or the package (`git diff --stat 1da64d0be 0ff264066~1 -- tools/wad db/inputs/wad_a5_vasp_2026_11_20` is empty).
- Fix: **`0ff264066`** (tools · tests · mutants — the only tool change). The next commit, which adds this letter, holds the package rebuilt from that tool and
  build-log key `⑰` (records and package only).
- `git diff 1da64d0be 0ff264066 -- tools/wad/build_a5_vasp_package.py tools/wad/build_v5_vasp_package.py` — a5 tool sha256 `6482901e9d9b746d42fbc28d36d53e23af68ba77c7b2b3a95cec0771226f6e4f`;
  the V5 collector file is **unchanged** (`90065ed5c4f7d052…`).
- Package `db/inputs/wad_a5_vasp_2026_11_20/` — changed files: `run_a5.sh` · `README.md` · `jobs.json` (tool sha · `lock_rule` · `tree_gate_rule` · `complete_row_rule` text) · `MANIFEST.sha256`.
  Job inputs and `SEALED_ENV.tsv` are byte-identical. Two fresh builds are byte-identical. **MANIFEST `01e39753d014f25e28efae63804500c36b0358aa3281e98eab84219c6e13d392`**.
- Line numbers below: runner = the rebuilt `db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh` (MANIFEST `01e39753…`); checker = `tools/wad/build_a5_vasp_package.py` at `0ff264066`.

## 1b. Threat model — unchanged from EQ / ER / ES

Judge the four ES findings against the same §1b as before: honest failures are in scope (a crashed node, a killed run, overlapping commands, a careless
partial restore of one file, a one-character accident in one record); two or more records edited to agree with each other are out of scope (note only).

## 1c. What counts as blocking in this round (user decision)

- **Closing the ES findings:** each of your five ES reproductions (§2) should now be stopped as described. Please check those.
- **Anything new is blocking only if, on a normal operator path, it makes the checker adopt a wrong value or destroys operator data** (deletes or
  overwrites run evidence, a recorded receipt or an existing return). A normal operator path = the documented commands (README §1 run, §5 recording
  commands, `PACK_ONLY=1`, `--unlock`) used as documented, including a node crash or a scheduler kill between them.
- Everything else — a conservative false stop, message wording, a scenario that needs a manual edit, partial restore or corruption of a run file that
  §1b did not already list as an ES reproduction — please report as a **note**, not as a blocker.

## 2. Your findings one by one

Each block: **your repro → was / now** (selftest case on the fake-VASP harness; "was" = the ES package, reproduced red first) · **fix** (where) · **mutants**.
The 13 new negative checks and the 2 extended probe tables were red on the ES tool (278/293), the new positive control was green, and all are green now (293/293).

### ES-1 · P0 · stale-lock reclaim race

- **Your repro → now.** A runner killed during c1 (7 complete rows) leaves its lock (dead PID). Two `--killed c1` commands both judge it stale; each is held
  at its first lock write; the 648,001 s command takes over and is held after its checks, then the 0 s command continues. **Was:** both exit 0, receipt
  648,001 s → 0 s, resume exit 0, c2 launched. **Now:** the second exits 2 ("taken over by another command first"), the first exits 0, `killed.json` =
  648,001 s (`sched-1`), resume exit 5 (cap), no c2 (`es_lock`).
  Live owner's record cut (PID cut after the host name, or emptied): **was** second exit 0 (or a foreign-lock message) and the first command's exit removed
  the lock → **now** second exit 2 "owner record unreadable", the first command leaves the lock in place at exit (not its token), `--unlock - -` clears it,
  record 648,001 s, resume 5 (`es_lockcut0` · `es_lockcut1`). A two-field (token-less) record with a dead PID → exit 2, lock kept, A5 not launched (`s9g`).
- **Fix.** The owner record is one line `host PID token` (token = 32 hex chars from `/dev/urandom`, newline-terminated; a cut record loses the token and
  newline first). `lock_rec` (run_a5.sh:776) parses it strictly; anything else is state `bad` → stop, never stale (`lock_state` :784).
  A stale lock is taken over only by **moving its owner record with `mv`** (rename — only one command can move it) and checking that the moved record is
  the one judged stale, token included; otherwise it is moved back and the command refuses (`lock_grab` :802, used by `lock_take` :811).
  At exit the lock is removed only if the owner record is still this run's token (`lock_rel` :807). `--unlock` removes a stale or foreign lock only
  after moving that same record, and an unreadable one only if it is still unreadable (:850–857).
- **Mutants.** m211 (take-over check) · m212 (unreadable → stale) · m213 (release without token check) · re-targeted m20 · m32.

### ES-2 · P0 · interim-return evidence lost by restoring one file

- **Your repro → now.** One A5 attempt, killed; the only "not 0 steps" evidence is ① a damaged first OSZICAR row, ② one OUTCAR `Iteration` line, or
  ③ one stdout electronic-row line. Interim return packed; `--infra-abort A5` exit 2; that one file restored to its pre-output state. **Was:**
  `--infra-abort` exit 0, A5 re-run. **Now:** `--infra-abort` exit 8 and resume exit 8, tree and return byte-identical, no `run_aborted/` (`es_ev0` ·
  `es_ev1` · `es_ev2`). Separately, after an interim return: one number changed in one of c1's 7 rows (7 → 7), or `status.tsv` cut to its header —
  **was** `PACK_ONLY` 0 (return overwritten) → **now** `PACK_ONLY` 8, return unchanged (`es_keep0` · `es_keep1`). Positive control: an 8th row appended to
  the same c1 (OSZICAR, OUTCAR `Iteration`, stdout row) → `PACK_ONLY` 0, `--killed` 0 (8 rows), resume 0, checker OK (`es_grow`).
- **Fix.** The existing-return comparison (`tgz5_in` :592 (helpers `pfx5` :581 · `lines5` :585 · `ev5in` :586; checks :617 · :619–620 · :626), runner only) now requires, for every attempt in the return (matched by run_id): the
  returned OSZICAR bytes are a prefix of the current OSZICAR (`tgz_osz_changed_<path>`); the returned OUTCAR `Iteration` lines and stdout electronic-row
  lines (newline-terminated lines only; the same patterns `--infra-abort` uses, `OI_RX` · `SO_RX` :209–210) are a prefix of the current file's
  (`tgz_iter_lost_<path>` · `tgz_stdout_lost_<path>`; OUTCAR and stdout are streamed with `tar -O`, not extracted); and the returned `run/status.tsv` is
  a prefix of the current one (`tgz_history_changed`). VASP and the runner only append to these, so growth passes and any change or loss stops.
- **Mutants.** m214 (OSZICAR) · m215 (OUTCAR) · m216 (stdout) · m217 (history).

### ES-3 · P1 · POTCAR hash copied into the end record

- **Your repro → now.** One digit of `POTCAR.sha256` changed while A5 ran, body unchanged. **Was:** copied into `attempt.json`, c1 run, checker OK,
  `a5_c1` adopted. **Now:** `attempt.json` carries the hash of the body measured just before it is written; it differs from the edited file, so the gate
  before c1 stops (exit 8, `end_potcar_sha`), no c1, checker not OK, nothing adopted (`es_pot0`). Body changed while A5 ran: **was** c1 run and adopted →
  **now** exit 8 right after A5 (measured hash in the end record, POTCAR body kept), no c1, nothing adopted (`es_pot1`).
- **Fix.** `run_one5` keeps the prep-time body hash (`psh` :1106), re-hashes the body still present right before the end record (`pz` :1146),
  writes `pz` (not a copy of the file) and stops with exit 8 if `pz ≠ psh` (:1152). The checker side is unchanged (`end_potcar_sha`).
- **Mutants.** m218 (copy the file again) · m219 (no re-hash stop).

### ES-4 · P1 · `0` vs `00` in the history wall time

- **Your repro → now.** In a finished tree, `status.tsv`'s wall time `0` → `00` (the existing return removed first, so only the history rule decides).
  **Was:** `PACK_ONLY` exit 0, checker LADDER_VIOLATION. **Now:** `PACK_ONLY` exit 8, checker LADDER_VIOLATION, same token `status_row_1_elapsed`
  (`es_00`; the ledger harness also has the variant `hist_00`, runner = checker).
- **Fix.** `hist5` compares the history cell with the end record's `elapsed_s` as raw strings (`($10 "") != (have[k] "")` :388 — awk's numeric
  comparison read `00` = `0`). The end-record side is already the strict integer form (decimal, no leading zero, ≤ 16 digits — `tpl5` = `tpl_parse`), so
  string equality also enforces that form. The checker (`history_problems` :2658) already compared strings.
- **Mutants.** m220 (numeric comparison again) · re-targeted m198.

### ES-5 · P2 · cut column title `' N E'` with spaces vs tabs

- **Now.** A blank-led tail whose collapsed text is a prefix of the column title counts as 0 steps before the generic header-fragment test — `' N E'`,
  `'\tN\tE'`, `' N\tE'`, `'  N  E'` → 0 steps on both sides; `' NE'` stays a header fragment (`incomplete_row`). Runner `row_scan` :677 =
  checker `row_gate` :233 (pure table + runner = checker harness, 3 stages).
- **Mutants.** m221 (runner) · m222 (checker) · re-targeted m115 · m131 · m166 · m185.

## 3. Tests

- Selftests: a5 **293/293** (293 checks: 279 + 14 new; the 13 new negative checks and the 2 extended tables were red on the ES tool: 278/293) ·
  V5 **313/313** (unchanged file) · round2 **194/194** (unchanged file) — python 3.13 · `dftd3` 1.6.0 venv. The a5 selftest also passes under `LC_ALL=C.UTF-8`
  (awk = mawk 1.3.4; gawk was not available in this container).
- Existing tests adjusted: the three lock fixtures (live · stale · foreign) now write the three-field owner record; nothing else changed.
- Mutants (`build_a5_vasp_package.py --mutants`): the 19 new or re-targeted ones first on their own (19/19 red), then **one full run at the end: 221/222 red — the one survivor, m201 (drops the older complete-row regression check in `tgz5_in`), we read as safety-equivalent: the next line, the byte-prefix check on the same OSZICAR (`pfx5`, guarded by m214), stops the same cases with the same exit 8, and only the stop word changes from `tgz_rows_lost` to `tgz_osz_changed` (complete rows are counted from those same bytes, so while the returned bytes stay a prefix no complete row can disappear). The older check stays because its stop word is the more precise one. If you find a case that only the older check stops, that is a real gap and we will fix it**
  (fail-fast, `--jobs 4`, the same tool sha as §1).
- Collector: the V5 file is unchanged, so the 11-20 G5 collect is not affected.

## 4. Questions

- **Q-ET-1** (ES-1): stale-lock take-over by one command only · unreadable owner → stop · release only with this run's token — closed?
- **Q-ET-2** (ES-2): evidence of the same attempt in an interim return (OSZICAR bytes · OUTCAR `Iteration` · stdout rows · history) may only grow — closed?
- **Q-ET-3** (ES-3): end-record POTCAR hash = body measured just before writing; mismatch with the prep hash stops — closed?
- **Q-ET-4** (ES-4): history wall time compared as raw strings on both sides — closed?
- **Q-ET-5** (ES P2): cut title judged the same with spaces or tabs — closed?
- **Q-ET-6**: Send approval — may package MANIFEST `01e39753d014f25e28efae63804500c36b0358aa3281e98eab84219c6e13d392` go to the operator?

## 5. How to reproduce

- `python3 -I tools/wad/build_a5_vasp_package.py --selftest` · `… --mutants m211 m212 …` (`--jobs 4`) · `python3 -I tools/wad/build_v5_vasp_package.py --selftest`
  · `python3 -I tools/wad/build_round2_vasp_package.py --selftest` (the last two, and the V5 mutants, need `dftd3` 1.6.0).
- `python3 -I tools/wad/build_a5_vasp_package.py --build --out <new folder>` → `diff -r` with `db/inputs/wad_a5_vasp_2026_11_20` · MANIFEST sha.
- The ES cases are in `_selftest` right after the ER Q-ER-5 block (the comment line starting `# ── Codex ES`): `es_lock` · `es_lockcut0/1` · `s9g` ·
  `es_ev0/1/2` · `es_keep0/1` · `es_grow` · `es_pot0/1` · `es_00`.

## 6. Reply format

Per question: verdict (GO / NO-GO) · evidence (file:line or test) · for a NO-GO, the reproduction. For anything new, say whether it meets §1c
(wrong adopted value or destroyed operator data on a normal operator path → blocking) or not (note). Please do not print W values.
