---
title: "EQ 프롬프트 — W_ad a5 묶음 Codex EP (NO-GO) 재승인 조건 ①–④ 고침 확인: 숫자로 읽히는 행 · 콜론 앞 머리 절단 · 시간 출처는 보존 폴더 영수증만 · 시도 이력 (status.tsv) 대조 · 시작 · 끝 · 최종 목록 실행 ID (+ 조건부 영수증 칸 · UTF-8 · P2 장부 순서) — 업체 발송 GO 여부"
date: 2026-11-23
updated: 2026-11-23
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, prompt, letter]
letter: EQ
track: wad
channel: codex
kind: prompt
status: 발송 대기 (사용자) · 기준 0fbc49760 (EP 가 본 묶음 · MANIFEST f10dedef…) → 고침 a97eba79f (도구 · 시험) · 891e106e5 (묶음 · 빌드 기록 ⑩) · 묶음 MANIFEST 679d7050… · selftest a5 236/236 · 돌연변이 140/140
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). Codex EP (NO-GO · 재승인 조건 ①–④) 다음 편지다. EP 원문 `codex_EP_reply_wad_a5_eo_fixes_2026_11_23.md` · 첨부 `codex_EP_evidence_2026_11_23/extra.json` (반례 꼴 목록) · 빌드 기록 ⑨ (회신 요약) · ⑩ (고침).
> ⛔ 점착 W 값은 싣지 않는다 (문턱 · 상태 · 종료 코드만). ⬇ 아래 **보내는 글** (영어) 만 발송한다. 회신이 오면 `codex_EQ_reply_wad_a5_ep_fixes_2026_11_2x.md` 로 원문 보존.
> ⚠ GO 가 와도 업체 발송은 사용자가 정한다 · DEM 편지 10 은 a5 가 끝난 뒤 (사용자 11-20).

---

**[W_ad · a5] Fixes for your EP re-approval conditions ①–④ (and the conditional items) — please confirm before we send the package to the operator**

## 0. What we are asking

Your EP review (package `0fbc49760`, MANIFEST `f10dedef…`) returned **NO-GO**. Your four re-approval conditions (Q-EP-6): ① no stage may be
consumed by a row whose numbers cannot be read · ② only receipts bound to the current attempt count toward the wall-time sum · ③ c-stage traces
left after a partial restore must be cross-checked · ④ run IDs must agree across start record, end record and final list. Also the two conditional
items (Q-EP-2: empty receipt fields, non-UTF-8 operator text) and the P2 (Q-EP-5: ledger order). The EO counter-examples you confirmed closed
stay closed. We reproduced every scenario of `extra.json` in the selftest **before** fixing (23 new checks red on the EP package: 211/234),
fixed both sides with one rule each, and rebuilt the package (**MANIFEST `679d705024b1c573e5a2861fbc3caa557d9f6ef016fb3d39bb2e8d4c829df278`**).
Please review **only these fixes**: per condition — closed (GO / conditional / NO-GO)? Did a fix open a new hole? May this package go to the
operator? Physics settings, the ladder, thresholds, the secondary rule and the G4/G5 arithmetic are unchanged.

## 1. Scope

- Base = `0fbc49760` (what EP reviewed). Records-only commits after it (your EP letter · your reply verbatim · attachments · build-log key `⑨`) do not touch
  tools or package. Fixes: `a97eba79f` (tools · tests) and `891e106e5` (package rebuilt · build log `⑩`). This letter is a records-only commit after them.
- `git diff 0fbc49760 891e106e5 -- tools/wad/build_a5_vasp_package.py tools/wad/build_v5_vasp_package.py` — a5 tool sha256 `af7848e1fc9ede11…`;
  the V5 collector file is **unchanged** (`90065ed5c4f7d052…`).
- Package `db/inputs/wad_a5_vasp_2026_11_20/` — changed files: `run_a5.sh` · `README.md` · `jobs.json` (tool sha · rule strings, new `history_rule`) ·
  `MANIFEST.sha256`. Job inputs (INCAR ×4 · POSCAR · KPOINTS · POTCAR spec) and `SEALED_ENV.tsv` are byte-identical.
- Line numbers below: runner = `db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh` (generated from `RUN_A5_ENV/CLI/BODY` in the tool file);
  checker = `tools/wad/build_a5_vasp_package.py`; both at `891e106e5`.

## 2. Rules (sealed — not up for review)

Same as EP §2: Amendment 5 v2 ladder A5 → c1 → c2; Interpretation 1 (next stage only after a confirmed SCF_NOT_CONVERGED or a run failure /
killed attempt with ≥ 1 electronic row; 0 rows → exit 7; RESTART_NOT_HONOURED · SCF_UNVERIFIED · settings-echo mismatch → exit 8);
c1's secondary value only after c2 itself ended in a confirmed state.

## 3. Your conditions one by one

Each block: **fix** (where) · **your scenario → now** (selftest case, fake VASP; "was" = the EP package, reproduced red first) · **mutants** that must
turn the selftest red · **still not caught**.

### ① No stage consumed by a row whose numbers cannot be read (Q-EP-1 · P0)

- **Fix.** The complete-row rule (one rule, runner `row_scan` = checker `row_gate`) now also requires the row to **read as numbers**: **6 or 7 fields**
  (N E dE d-eps ncg rms [rms(c)]), N a positive integer (`[1-9][0-9]*`), ncg an integer, every other field a real number
  (`[+-]?(digits[.digits] | .digits)` with an optional `E`/`e` exponent of at most two digits — so `NaN`, `inf`, `***`, words and |x| ≥ 1E+100 are not numbers).
  A row-like line that fails this is **damage** (`incomplete_row`), finished or not — so `--killed` refuses it, a finished run failure with such a row
  ends in REVIEW (exit 8) before the zero-row and RUN_FAILED branches, and the judge contract never sees it. **Header cut before the colon**: an
  unterminated tail made of 1–4 letters/spaces at column 1 (`S`, `SD`, `SDA`, `D` …) is a row-like tail — with 0 complete rows it is damage, so
  `--infra-abort` refuses it and the resume stops for review; after ≥ 1 complete row it is the normal cut and is ignored. Normal 6- and 7-field rows are accepted.
  Where: runner `row_scan` run_a5.sh:429 (header cut :446) · `gate5` :925 · `--infra-abort` :599 · `--killed` :674; checker `REAL_TOK` / `HDR_CUT`
  build_a5_vasp_package.py:150 / :151 · `_complete_row` :155 · `row_gate` :166 (header cut :195).
- **Your scenario → now.** c2's only row `SDA: 1 none missing missing abc bad` (killed): was `--killed` 0 · resume 1 · NO_PRIMARY_VALUE · c1 secondary →
  now **`--killed` 2 · resume exit 8 · STOPPED_FOR_REVIEW (c2 0 complete rows, `incomplete_row`) · no adoption** (`ep_garb`). The same row in a finished
  run failure (rc 1): was RUN_FAILED · 1 row · c1 secondary → now **exit 8 · `status.tsv` and checker c2 SCF_UNVERIFIED (`incomplete_row`) · no adoption**
  (`ep_garb_rf`). First row cut at `SDA` (before the colon): was `--infra-abort` 0 · resume 0 · OK · c2 adopted → now **`--infra-abort` 2 · resume exit 8 ·
  STOPPED_FOR_REVIEW · nothing preserved** (`ep_hcut`). Positive controls unchanged (`eo_tail` 1 row + `SDA:` tail → exit 1 · c1 secondary; `kill2b` 7 rows; real
  6- and 7-field DAV rows). Pure cases (4 new): the garbage row (alone and after a valid row) · NaN / non-integer ncg / N 0 / N −1 / 8 fields / 3-digit exponent /
  `***` / `inf` · signs and leading/trailing decimal points accepted · header cuts (`SDA`, `D`, `SD A`) vs a cut column-header line and a blank-led fragment.
  Runner = checker on **35 OSZICAR probes × 3 stages** (14 new) and on the judge contract (14 probes × 3 stages).
- **Mutants.** m114 m115 (runner: number reading · header cut) · m130 m131 (checker: the same) · m85 m99 re-targeted (old field rule on the new line).
- **Still not caught.** The 6/7-field rule for `SDA:` / `CGA:` rows comes from real DAV rows; we hold no real 5.4.4 c2 (ALGO=All) output — a different
  layout would stop for review (exit 8), never adopt. The header-cut rule assumes VASP rows start at column 1: a blank-led letter fragment cannot be told
  from a cut column-header line and is treated as 0 steps.

### ② Only receipts bound to the current attempt count toward the wall-time sum (Q-EP-3 · P1)

- **Fix.** One time source on both sides, now location-bound: a **preserved folder** (`run_aborted/<job>_<rung>_<k>`) takes the wall time **only from its
  own receipt** (`infra_abort.json`, itself bound to the ledger row, the folder and the folder's `attempt.start` run_id by ②–④ of the ledger check); a
  **progress folder** (`run/<job>_<stage>`) never reads a receipt (killed.json → attempt.json → UNKNOWN). In addition, **an abort receipt (or `.part`) inside a
  progress folder is rejected**: runner `ledger5` at the top of every ladder run (before the start point or any launch) and in `--infra-abort` / `--infra-wall`
  → REVIEW exit 8; checker `ledger_problems` → LADDER_VIOLATION.
  Where: runner `wall_of` run_a5.sh:335 · `ledger5` stray check :303 · `wall5` :766; checker `wall_of` build_a5_vasp_package.py:2251 · `ledger_problems` :2322.
- **Your scenario → now.** c1 killed and recorded with 648,001 s, plus another attempt's 0-step receipt copied into `run/<job>_c1/`: was c2 launched ·
  exit 0 · OK · c2 adopted → now **resume exit 8 · c2 not launched** (`ep_stray`); checker on an OK return with a receipt copied into `run/<job>_c1/` →
  **LADDER_VIOLATION**. Runner = checker on 5 `wall_of` probes (progress folder with receipt + killed.json → the killed.json value · with receipt +
  attempt.json → the attempt.json value · empty → UNKNOWN · preserved folder with receipt + attempt.json → the receipt · preserved folder without receipt → unreadable).
- **Mutants.** m116 m117 (runner: old time source · no stray check) · m132 m133 (checker: the same) · m91 m105 re-targeted (receipt not first).
- **Still not caught.** The scheduler wall time is taken as given (`WALL_S` and the node clock are the operator's).

### ③ c-stage traces left after a partial restore are cross-checked (Q-EP-4a · P1)

- **Fix.** `run/status.tsv` rows now carry the attempt's **run_id** (last column; header `…\twall_s\trun_id`). Before the start point is written or any stage
  (re)launched — and in the record commands — runner `hist5` (called from `ledger5`, also when there is no ledger) requires **every history row to be
  explained by a finished attempt folder** (`attempt.json` present) **in `run/` or `run_aborted/` with the same run_id and variant**, each row once; checker
  `history_problems` applies the same rule on return. Mismatch → REVIEW exit 8 · LADDER_VIOLATION.
  Where: runner `hist5` run_a5.sh:373 · history row :890 · ladder top :1015; checker `STATUS_HEAD` / `history_problems` build_a5_vasp_package.py:2273 / :2276.
- **Your scenario → now.** Partial restore (ledger, preserved c1 folder and `start_point.json` removed together, the first c1's history row left): was start
  point re-written · c1 relaunched · OK · new c1 adopted → now **exit 8 · start point not written · c1 not launched** (`ep_hist`); the checker on an
  old-runner-style return (ledger and preserved folder removed, final record refitted to the tree) → **LADDER_VIOLATION** (the history row has no attempt).
  Ledger cross-check harness: 23 return variants, runner = checker (new: history row without attempt · stray receipt · empty receipt field · preserved
  attempt.json with another run_id; the "no ledger, no folder" variant now also drops that attempt's history row, i.e. a consistent restore).
- **Mutants.** m119 m120 (runner: no history check · not called when there is no ledger) · m135 (checker).
- **Still not caught.** A restore that also removes or rewrites the matching history rows (consistent forgery); a finished attempt **without** a history row is
  not flagged (the runner can be killed between the end record and the history row — we did not want a false stop there).

### ④ Run IDs agree across start record, end record and final list (Q-EP-4c · conditional)

- **Fix.** (a) A **finished** attempt's end record (`attempt.json`) must carry the **same run_id and t_start as its `attempt.start`** — runner `end_id`
  (in `gate5` → BAD2 exit 2, nothing launched; in `receipt5` for preserved folders) = checker `end_problem` (in `check_attempt5` → ATTEMPT_MISMATCH, blocking;
  in `abort_receipt_problem`). (b) The final record must exist for an adoptable return: the checker turns OK / NO_PRIMARY_VALUE into
  **STOPPED_FOR_REVIEW** when `run/final.json` is missing. (c) Before **`PACK_ONLY=1`** and before a **normal re-run** of a finished ladder, the runner
  reads the whole final record (`fin_ok`: REC1 · code 0/1/5/6/8 · state · why · `attempts` present and equal to the current attempt list) → otherwise exit 2
  (nothing packed or run).
  Where: runner `end_id` run_a5.sh:364 · `gate5` :938 · `receipt5` :280 · `fin_ok` :414 · `PACK_ONLY` guard :698 · re-run guard :727; checker `end_problem`
  build_a5_vasp_package.py:1847 · `check_attempt5` :1976 · `abort_receipt_problem` :2233 · final-record rule in `check_return` :2639.
- **Your scenario → now.** A normal c1 whose `attempt.json.run_id` (or `t_start`) alone is changed: was OK · a5_c1 → now **c1 ATTEMPT_MISMATCH · no adoption**;
  runner on a finished A5 with a changed `attempt.json.run_id`: was exit 7 → now **exit 2 (BAD2 `end_run_id`)** (`ep_eid`). OK return without `final.json`:
  was OK · adopted → now **STOPPED_FOR_REVIEW**. `final.json` without `attempts` / with an edited list: was `PACK_ONLY` 0 · re-run 0 → now **both exit 2,
  bundle untouched** (`ep_fin0`, `ep_fin1`).
- **Mutants.** m121 m122 m127 m128 m129 (runner: `gate5` / `receipt5` end identity · re-run / `PACK_ONLY` guard · list comparison) · m136 m137 m140 (checker:
  end identity · preserved folder · missing final record) · m25 m46 re-targeted.
- **Still not caught.** `attempt.json` is not REC1 (it carries a sha table): run_id / t_start / elapsed_s are read by `grep` in the runner and `json` in the
  checker, which agree for the runner's own output (with duplicated keys the checker is the stricter side).

### Conditional Q-EP-2 — receipt fields and non-UTF-8 text

- **Fix.** `sched_job_id`, `cancel_utc` and `reason` must be **non-empty on read** in `killed.json` and `infra_abort.json` (runner `killed5` / `receipt5` =
  checker `killed_problems` / `abort_receipt_problem`, right after the field-type checks). Operator text is **refused at write time if it is not valid UTF-8**
  (runner `u8ok` in `--killed` and `--infra-abort` → exit 2, nothing written). We chose refusal over replacement: replacing bytes would silently change what
  the operator typed, and a refusal costs one re-typed command. `u8ok` follows RFC 3629 (overlong forms, surrogates, > U+10FFFF and truncated sequences
  refused) and matches Python's strict decoder on 18 probes. The limit text is corrected: the runner no longer writes non-UTF-8 bytes; on **read**, REC1
  still compares raw bytes and accepts non-UTF-8 inside strings on both sides alike (only a hand-edited record could carry them; a strict UTF-8 JSON reader
  would refuse such a record).
  Where: runner `receipt5` run_a5.sh:280 · `killed5` :897 · `u8ok` :393 · `--infra-abort` :620 · `--killed` :689; checker `killed_problems` build_a5_vasp_package.py:1906 ·
  `abort_receipt_problem` :2225.
- **Your scenario → now.** `sched_job_id` emptied in killed.json: was both accepted · c1 secondary → now **runner exit 8 (KILLED_RECORD_MISMATCH) · checker
  STOPPED_FOR_REVIEW** (`ep_kjempty`); an emptied receipt `reason` → **LADDER_VIOLATION**. Reason with byte 0xE9: was written as is → now **`--killed` 2 and
  `--infra-abort` 2, nothing written** (`ep_u8`, `ep_u8b`).
- **Mutants.** m123 m124 m125 m126 (runner) · m138 m139 (checker).

### P2 Q-EP-5 — ledger order

- **Fix.** Before the ladder re-sorts anything, the ledger rows (= global abort numbers) must be in occurrence order: for consecutive rows the receipt's
  `recorded_s` and the folder's `attempt.start` `t_start` must not decrease (runner `ledger5` = checker `_ledger_core`). A separate rung-order check was
  tried and dropped: it is implied by this time order plus the existing ladder-order check, and could not be tested on its own.
  Where: runner run_a5.sh:330; checker build_a5_vasp_package.py:2385.
- **Your scenario → now.** Real order A5 → c1, ledger rows and folder numbers swapped to c1#1 → A5#2: was resume 0 · checker OK · a5_c1 → now **resume exit 8 ·
  c1 not launched · checker LADDER_VIOLATION**; the unswapped twin still ends OK (`ep_rev`).
- **Mutants.** m118 (runner) · m134 (checker).
- **Still not caught.** The order check trusts the operator node's `date +%s` (both times come from the same login node).

## 4. Tests

- Selftests: a5 **236/236** (was 211; 23 new checks were red on the EP package before the fixes, plus two more: `--infra-abort` UTF-8 and a
  checker-only empty `killed.json` field) · V5 **313/313**
  (unchanged file) · round2 **194/194** (unchanged file; both re-run on the `a97eba79f` tree) — python 3.11 · `dftd3` 1.6.0 venv. The a5 selftest also passes with **gawk 5.2.1** as `awk` and
  under `LC_ALL=C.UTF-8` (default awk = mawk 1.3.4).
- Existing tests adjusted: the `c2` state variants built by deleting or truncating a finished c2 now also drop that attempt's history row (a real return
  where c2 never finished has no such row) · the two EN P1 runner guard tests (`ga5`: A5 missing with a preserved c1; `gc1`: c1 missing with a
  preserved c2) now also drop the removed stage's history row, so the history check does not pre-empt the guard they test · the ledger harness's
  "no ledger, no folder" variant drops the matching history row · the runner prints the code
  and state of `final.json` instead of a byte-cut line (a cut inside a multibyte character produced invalid UTF-8 on the console).
- Mutants: `build_a5_vasp_package.py --mutants` (venv python, two prefix batches, `--jobs 2` each) — **140/140** on tool `af7848e1fc9ede11…`: the 113 earlier ones
  (6 re-targeted to the changed lines — m25 m46 m85 m91 m99 m105) + **27 new (m114–m140)**, at least one per new guard on each side (§3). In our first full pass three survived — m65 and m66
  (EN P1 runner guards, now shadowed in their tests by the new history check) and m139 (checker empty `killed.json` field, shadowed by the final-record
  code check); we isolated the tests (above) and added the checker-only case, saw all three turn red, and re-ran all 140 on the final tool. The two batches reported 69/69 and 71/71, and each of the 140 names has exactly one red line in the logs.
- EN / EO reproductions and positive controls (`ken1`, `ken2`, `eo_sda`, `eo_tail`, `eo_esc`, `eo_kj*`, `eo_st*`, `eo_cap`, `eo_unk`, `eo_led*`, `eo_sw*`, `kill2b`,
  `rcpt`, `spok`, `stale`) still pass.
- EM probes p1–p9 (10 files incl. p3b) re-run on the EP-reviewed tool and on the new tool, compared after normalising times, hashes and
  run ids: **9 identical** (p1, p2, p4 and p9 end in the same `FileNotFoundError` in both versions — the probe scripts expect a file the runner does not
  create on that branch; their verdict lines are identical). **p7 (prep failure) changed label again**: STOPPED_FOR_REVIEW → **LADDER_VIOLATION**,
  adoption none in both. The probe deletes the finished c2 (then c1) folder of a completed return while its `status.tsv` row stays — a partial restore,
  now caught by ③. With the final record refitted **and** the orphaned history rows dropped (what a runner that really failed in preparation leaves;
  scratch probe p7c) the label is LADDER_INCOMPLETE with the same note as in EO / EP.
- Collector regression: the V5 collector file is unchanged since the 11-20 G5 aggregate. Re-running the recorded G5 command (V5 return unpacked in
  scratch) on the `a97eba79f` tree gives rc 3, the same JSON `afecfa08…` and the same console output, byte for byte — as at the EO and EP rounds.

## 5. Please look especially at

1. **Number reading** is purely lexical (sign · digits · one decimal point · E/e exponent ≤ 2 digits). Fortran prints `0.1+101` for |x| ≥ 1E+100 (no `E`);
   such a row is damage (review). Is a two-digit exponent the right bound for a 5.4.4 OSZICAR?
2. **Header cut** = unterminated 1–4 letters/spaces at column 1. A blank-led fragment is treated as a cut column-header line (0 steps). Agree?
3. **History direction**: rows must be explained by attempts; attempts without rows are not flagged (kill window). Agree with the one-way rule?
4. **Exit codes**: an `attempt.json` that does not belong to its `attempt.start` ends in exit 2 (no final record, "contact"), like a foreign `attempt.start`;
   history / ledger / stray-receipt mismatches end in exit 8 (final record). A final record that does not match the tree blocks both repack and re-run (exit 2).
5. **What still cannot be caught**: a return in which ledger, receipts, history, attempt folders and the final record were all edited consistently.

## 6. Questions

- **Q-EQ-1** (①): numbers-readable rows and header cuts closed (both sides · finished and killed · `--killed` / `--infra-abort` refusals · 6/7-field rows kept)?
- **Q-EQ-2** (②): time source bound to the preserved folder's own receipt, and receipts in progress folders rejected before any launch and on return — closed?
- **Q-EQ-3** (③): partial restore cross-checked through the run_id in `status.tsv` (runner before the start point / any launch, checker on return) — closed?
- **Q-EQ-4** (④): start / end / final run IDs (`end_id` = `end_problem`, final record required, `fin_ok` before repack and re-run) — closed?
- **Q-EQ-5**: conditional items (empty receipt fields · UTF-8 refusal at write) and the P2 ledger order — closed? Any new hole introduced by these fixes?
- **Q-EQ-6**: Send approval — may package MANIFEST `679d705024b1c573e5a2861fbc3caa557d9f6ef016fb3d39bb2e8d4c829df278` go to the operator?

## 7. How to reproduce

- `python3 -I tools/wad/build_a5_vasp_package.py --selftest` · `… --mutants --jobs 2` (or `--mutants m114 m115 …`; run it with a python that has `dftd3` so the
  V5 mutants are judged by the V5 selftest, not by an import error) · `python3 -I tools/wad/build_v5_vasp_package.py --selftest` (needs `dftd3` 1.6.0).
- `python3 -I tools/wad/build_a5_vasp_package.py --build --out <new folder>` → `diff -r` with `db/inputs/wad_a5_vasp_2026_11_20` · MANIFEST sha.
- Fake VASP plans used here: `plateau@0|SDA: 1 none missing missing abc bad\n` (killed) · `crash@0|…` (finished run failure) · `plateau@0|SDA` (cut before the colon).

## 8. Reply format

Per question: verdict (GO / conditional / NO-GO) · evidence (file:line or test) · minimal fix if not GO. Please do not print W values.
