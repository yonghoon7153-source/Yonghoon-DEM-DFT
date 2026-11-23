---
title: "EP 프롬프트 — W_ad a5 묶음 Codex EO (NO-GO) 재승인 조건 ①–④ 고침 확인: 완전한 전자행 계수 · 영수증 · 시작 기록 일치 판독 · 중단 시간 · 상한 · 장부 ↔ 보존 폴더 (+ P2 끝 기록 시도 ID) — 업체 발송 GO 여부"
date: 2026-11-23
updated: 2026-11-23
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, prompt, letter]
letter: EP
track: wad
channel: codex
kind: prompt
status: 발송 대기 (사용자) · 기준 8fd051a22 (EO 가 본 묶음) → 고침 df5ea438b (도구 · 시험) · 0fbc49760 (묶음 · 빌드 기록 ⑧) · 묶음 MANIFEST f10dedef… · selftest a5 211/211 · 돌연변이 113/113
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). Codex EO (NO-GO · 재승인 조건 ①–④) 다음 편지다. EO 원문 `codex_EO_reply_wad_a5_en_fixes_2026_11_23.md` (첨부 없음).
> ⛔ 점착 W 값은 싣지 않는다 (문턱 · 상태 · 종료 코드만). ⬇ 아래 **보내는 글** (영어) 만 발송한다. 회신이 오면 `codex_EP_reply_wad_a5_eo_fixes_2026_11_2x.md` 로 원문 보존.
> ⚠ GO 가 와도 업체 발송은 사용자가 정한다 · DEM 편지 10 은 a5 가 끝난 뒤 (사용자 11-20). 빌드 기록 `db/properties/wad_a5_build_log_2026_11_20.json` ⑧.

---

**[W_ad · a5] Fixes for your EO re-approval conditions ①–④ — please confirm before we send the package to the operator**

## 0. What we are asking

Your EO review (package `8fd051a22`, MANIFEST `b01d0861…`) returned **NO-GO** with four re-approval conditions (Q-EO-6):
① complete electronic-row counting · ② receipts and the start record read the same way on both sides · ③ abort wall time checked
against the 180 h cap · ④ abort ledger ↔ preserved folders; plus a conditional P2 on run identity (Q-EO-4). The EN counter-examples you
confirmed closed stay closed. We fixed each item and rebuilt the package (**MANIFEST `f10dedefe8165f64999a0dca9897ef39e951a6c3085a1baa6ee9b0106a1b169c`**).
Please review **only these fixes**: for each condition — closed (GO / conditional / NO-GO)? Did a fix open a new hole? May this package go to the
operator? Physics settings, the ladder, thresholds, the secondary rule and the G4/G5 arithmetic are unchanged.

## 1. Scope

- Base = `8fd051a22` (what EO reviewed). Records-only commits after it (your EO letter · your reply verbatim · build-log key `⑦`) do not touch tools or package.
  Fixes: `df5ea438b` (tools · tests) and `0fbc49760` (package rebuilt · build log `⑧`). This letter is a records-only commit after them.
  Commits from other tracks merged in between (b2o3 · literature extractor · governance ledger) do not touch `tools/wad/` or the package —
  `git diff 8fd051a22 HEAD -- tools/wad db/inputs/wad_a5_vasp_2026_11_20` shows only the a5 tool and the four package files.
- `git diff 8fd051a22 0fbc49760 -- tools/wad/build_a5_vasp_package.py tools/wad/build_v5_vasp_package.py` — a5 tool sha256 `35592b07ed0f0fd8…`;
  the V5 collector file is **unchanged** (`90065ed5c4f7d052…`, your EO verdict GO); the a5 selftest now binds it to the complete-row count.
- Package `db/inputs/wad_a5_vasp_2026_11_20/` — changed files: `run_a5.sh` · `README.md` · `jobs.json` (tool sha + five new rule strings
  `complete_row_rule` · `record_grammar` · `time_source_rule` · `ledger_rule` · `final_attempts_rule`) · `MANIFEST.sha256`. Job inputs (INCAR ×4 · POSCAR · KPOINTS · POTCAR spec)
  and `SEALED_ENV.tsv` are byte-identical.
- Line numbers below: runner = `db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh` (generated from `RUN_A5_ENV/CLI/BODY` in the tool file);
  checker = `tools/wad/build_a5_vasp_package.py`; both at `0fbc49760`.

## 2. Rules (sealed — not up for review)

Same as EO §2: Amendment 5 v2 ladder A5 → c1 → c2; Interpretation 1 (next stage only after a confirmed SCF_NOT_CONVERGED or a run failure /
killed attempt with ≥ 1 electronic row; 0 rows → exit 7; RESTART_NOT_HONOURED · SCF_UNVERIFIED · settings-echo mismatch → exit 8);
c1's secondary value only after c2 itself ended in a confirmed state.

## 3. Your conditions one by one

Each block: **fix** (where) · **your scenario → now** (selftest case, fake VASP) · **mutants** that must turn the selftest red · **still not caught**.

### ① Complete electronic-row counting (Q-EO-1 · P0)

- **Fix.** One definition on both sides. A **complete row** is a **newline-terminated** row-like line (1–4 letters + `:` at line start, as before)
  whose header is the stage's own header verbatim (A5 / c1 `DAV:` `RMM:`, c2 `SDA:` `CGA:`; no inner spaces), followed by whitespace and **≥ 6 fields**
  (N E dE d-eps ncg rms — the operator's round-2 return has 6- and 7-field DAV rows) with N an integer. Only complete rows are counted
  (`osz_rows`, `--killed`, the judge-contract input). The bytes after the last newline (**tail fragment**) are never counted: after ≥ 1 complete row a
  row-like tail is the normal scheduler cut and is ignored; with **0 complete rows** it is **damage**. A newline-terminated incomplete row-like line
  anywhere is damage (truncation cannot produce it). Foreign headers keep priority (`row_header_X`); NUL bytes → `nul_bytes`.
  **Any damage → review, finished or not, before the zero-row (exit 7) branch**: runner exit 8 even without killed.json; checker SCF_UNVERIFIED →
  `a5_class` REVIEW → STOPPED_FOR_REVIEW. `--killed` refuses damage and needs ≥ 1 complete row; `--infra-abort` needs "0 complete rows and no damage".
  The judge contract gets only complete rows (newline-terminated lines, own headers rewritten to `DAV:`), so a crash with complete rows + a cut tail is
  RUN_FAILED with the complete count. The collector is unchanged and now receives the complete count.
  Where: runner `row_scan` run_a5.sh:360 · `osz_feed` :379 · `judge5` :384 · `gate5` :848 (damage → REVIEW before the zero-row branch) ·
  `--infra-abort` :529 · `--killed` :603; checker `_complete_row` / `row_gate` build_a5_vasp_package.py:144 / :152 · `feed5` :188 · `judge5` :195 ·
  `osz_rows` :206 · `check_attempt5` :1818 (row scan → SCF_UNVERIFIED) · `a5_class` :2056 · aborted-folder damage in `check_return` :2322.
- **Your scenario → now.** c2 first row cut at `SDA:` (killed): was `--killed` 0 · resume 1 · NO_PRIMARY_VALUE · c1 secondary →
  now **`--killed` 2 · `--infra-abort` 2 · resume exit 8 · STOPPED_FOR_REVIEW (c2 0 rows, `incomplete_row`, class REVIEW) · no adoption** (`eo_sda`);
  with a killed.json written by the old runner (`osz_rows "1"`) → **exit 8 · c2 SCF_UNVERIFIED (0 rows) · STOPPED_FOR_REVIEW** (`eo_sda_old`).
  One complete row + `SDA:` tail: was 2 rows → now **1 row · `--killed` records `osz_rows "1"` · exit 1 · NO_PRIMARY_VALUE · c1 secondary** (`eo_tail` —
  a legitimate confirmed end); the same with `SDA:\n` (newline-terminated) → **`--killed` 2 · exit 8 · STOPPED_FOR_REVIEW** (`eo_tailnl`).
  A **finished** c2 (final record written) with 5 complete rows, a newline-terminated incomplete row and `ISTART = 0` in OUTCAR → damage is reported
  before the restart / settings checks on both sides: **runner `status.tsv` and checker both SCF_UNVERIFIED (`incomplete_row`) · exit 8 · STOPPED_FOR_REVIEW**
  (`eo_findmg`). A preserved 0-step abort folder whose OSZICAR holds an incomplete row → checker **LADDER_VIOLATION**.
  **Positive controls kept**: c2 cut after 7 valid rows → exit 1 · c1 secondary (`kill2b`); `ISTART=0/ICHARG=2` and `XYZ:` after 7 rows → exit 8 ·
  no adoption (`ken1`, `ken2` — for `XYZ:` `--killed` now refuses with `row_header_XYZ`; the resume still ends 8).
  Pure cases (11): `SDA:` cut · tail after 1 row · full-looking tail without newline · `SDA:\n` and a 2-field row with newline · damage in the middle ·
  no space after `:` and `DA V:` · foreign header before damage and NUL · 30 rows / 29 without the last newline · real 6/7-field rows · crash with a
  cut tail → RUN_FAILED 7 · secondary row list. Runner = checker on **21 OSZICAR probes × 3 stages** (count and reason) and on the judge contract
  (**14 probes × 3 stages**, 6 new).
- **Mutants.** m85 m86 m87 m88 m96 m97 (runner: field rule · tail as a line · zero-row tail not damage · damage stop on finished attempts ·
  `--infra-abort` / `--killed` accept damage) · m99 m100 m101 m112 (checker: field rule · REVIEW class · damage before zero rows · aborted-folder damage).
- **Still not caught.** The ≥ 6-field rule for `SDA:` / `CGA:` rows comes from the DAV rows we have; we hold no real 5.4.4 c2 (ALGO=All) output.
  If a real c2 row had fewer fields it would stop for review (exit 8) — never an adoption. A newline-terminated short row is damage, not a cut tail
  (§5 item 1).

### ② Receipts and the start record read the same way (Q-EO-2, first two bullets · P1)

- **Fix.** One line-record grammar **REC1** for `killed.json` · `infra_abort.json` · `attempt.start` · `final.json`, implemented twice and compared probe
  by probe: runner `rec5` (awk, `LC_ALL=C`, byte-level; NUL rejected by `tr`/`cmp` before awk) = checker `rec_parse` (bytes). REC1 = one line
  (+ one optional final newline) · `{` member (`,` member)* `}` · spaces/tabs allowed around every token (as JSON) · key `"[a-z][a-z0-9_]*"` · value =
  JSON string (raw control bytes 0x00–0x1F rejected · escapes `\" \\ \/ \b \f \n \r \t \uXXXX` only) or a non-negative integer (no leading zero ·
  ≤ 16 digits) · no duplicate key · anything else (arrays, objects, floats, true/false/null, negatives, trailing bytes) rejected. String values are
  compared **raw** on both sides — the runner writes those fields as plain ASCII. **Writing**: operator text (`--killed` / `--infra-abort` job id ·
  cancel time · reason) is JSON-escaped by `jstr` (`od` + awk — quote, backslash, 0x01–0x1F, 0x7F) instead of stripped. Both sides read the **whole**
  record (all required fields with types) before the next stage. **Start record**: before linking `killed.json.run_id`, both sides check
  `attempt.start` against the current folder — REC1 · `job` = this job · `stage` = `a5` · `attempt` ∈ the folder's stage variants · run_id format
  (ASCII) · integer `t_start` (same order on both sides). Runner mismatch → exit 2 (nothing launched, no final record, "contact") from `gate5`,
  `--killed` and `--infra-abort`; checker ATTEMPT_MISMATCH (blocking). Aborted folders get the same check inside the receipt check, and the receipt
  now carries that attempt's `run_id`. No new dependency: only `od tr cmp tail wc` (coreutils, now listed in the README / header) and awk.
  Where: runner `rec5` run_a5.sh:209 · `rget` :262 · `jstr` :263 · `start_id` :269 · `receipt5` :280 · `killed5` :821 · `gate5` :848; checker
  `rec_parse` build_a5_vasp_package.py:1616 · `rec_read` :1691 · `start_problem` :1721 · `killed_problems` :1754 · `check_attempt5` :1822 · `load_final` :2010 ·
  `abort_receipt_problem` :2081.
- **Your scenario → now.** ESC in the `--killed` reason: was runner continued to c2 (exit 0) but checker KILLED_RECORD_MISMATCH · LADDER_VIOLATION →
  now **valid one-line JSON that decodes back to the original text (ESC, quote, backslash, Korean) · c2 runs · exit 0 · OK · c2 adopted** (`eo_esc`;
  the same reason in an `--infra-abort` receipt in `eo_unk`). One comma removed: was runner continued · checker refused → now **runner exit 8
  (KILLED_RECORD_MISMATCH) · checker STOPPED_FOR_REVIEW** (`eo_kj0`). No space after `:` (valid JSON): was checker accepted · runner exit 8 → now
  **both accept: exit 1 · NO_PRIMARY_VALUE · c1 secondary** (`eo_kj1`; tabs / extra spaces `eo_kj2`). c2 `attempt.start.job` changed, run_id kept:
  was both passed · c1 secondary → now **runner exit 2 (no final record) · checker c2 ATTEMPT_MISMATCH · status ATTEMPT_MISMATCH · no adoption**
  (`eo_st0`; `attempt` → `c1` and `stage` → `a4`: `eo_st1`, `eo_st2`); `--infra-abort` on a 0-step A5 whose `attempt.start` names another job →
  **exit 2 · folder not moved · no receipt · no ledger** (`eo_st_iab`). Pure REC1 cases (5). Runner = checker on **32 byte-level REC1 probes**
  including the parsed raw values (canonical · no space · tabs · comma loss · duplicate · two lines · trailing byte · raw ESC · escaped ESC/quote/backslash/slash ·
  bad escape · leading zero · negative · float · 17 / 16 digits · empty · `{}` · UTF-8 · invalid UTF-8 · DEL · unterminated string · CRLF · NUL ·
  upper-case key · nested · two newlines · newline only · short `\u` · trailing backslash · `true` · key with space · BOM); `jstr` output decodes back for
  9 probes; **10 `attempt.start` probes**.
- **Mutants.** m89 m90 m94 m104 m113 (runner: no escaping · no job check · receipt run_id · `gate5` / `--infra-abort` start check) · m102 m103 m111
  (checker: job check · folder check · receipt run_id).
- **Still not caught.** String values are compared raw, so a non-UTF-8 byte inside a string is accepted by both sides (the runner never writes one).
  `attempt.json` is not REC1 (it carries a sha table): its `elapsed_s` is read by `grep` in the runner and `json` in the checker, which agree for the
  runner's own `%d` output only. An `attempt.start` + `killed.json` pair forged consistently for the folder is not detectable.

### ③ Abort wall time and the 180 h cap (Q-EO-2, third bullet · P1)

- **Fix.** One time source on both sides: abort receipt `wall_s` (the scheduler's value) **before** that folder's `attempt.json` `elapsed_s` →
  `killed.json` `wall_s` → `attempt.json` `elapsed_s` → UNKNOWN. The runner sums it at every launch (as before, now in this order). The **checker
  re-derives the runner's launch decisions** over the launched attempts in ladder order: for each attempt, the sum of all earlier attempts' wall times
  must be known and ≤ 180 h, else LADDER_VIOLATION. UNKNOWN stays a legitimate receipt **only while nothing was launched after it**. `--infra-wall`
  is now an a5 command: it reads the receipt with REC1, requires `wall_s` = UNKNOWN and a consistent ledger, rewrites the receipt field by field and
  adds `wall_s_filled_utc` · `wall_s_filled_s`; the checker requires the fill time ≤ the next attempt's start (both fill fields or neither, fill ≥ recorded).
  Where: runner `wall_of` run_a5.sh:327 · `wall5` :690 · `--infra-wall` :583; checker `wall_of` build_a5_vasp_package.py:2117 · cap / UNKNOWN / fill
  loop in `check_return` :2344.
- **Your scenario → now.** A5 0 steps (`elapsed_s` ≈ 0) + `WALL_S=648001`: was A5 relaunched · OK → now **resume exit 5 (cap) · A5 not relaunched ·
  LADDER_INCOMPLETE · no adoption** (`eo_cap`); an old-runner return with that receipt followed by a relaunched A5 → **LADDER_VIOLATION (cap)**.
  UNKNOWN receipt (killed A5, 0 rows, no attempt.json) → resume exit 5 → `--infra-wall … 300` (records the fill time; a second fill is refused) →
  resume → OK (`eo_unk`). Completed return with receipt **and** ledger reverted to UNKNOWN (fill fields removed): was OK → now **LADDER_VIOLATION**
  ("unknown … but launched"); fill time later than the next A5 start → **LADDER_VIOLATION**.
- **Mutants.** m91 m98 (runner: old time order · no fill record) · m105 m106 m107 m108 (checker: old time order · no cap re-derivation · UNKNOWN before a
  launch · fill after the next start).
- **Still not caught.** Clocks and `WALL_S` are the operator's (node `date +%s`, the scheduler's ledger value); a wrong `WALL_S` typed by the operator is
  taken as given. Clock skew between nodes can give a false order violation (review), not a false pass.

### ④ Abort ledger ↔ preserved folders (Q-EO-3 · P1)

- **Fix.** Runner `ledger5` (at the top of every ladder run — before the start point can be written or any stage (re)launched — and inside
  `--infra-abort` / `--infra-wall`) = checker `ledger_problems` + `abort_receipt_problem`: no ledger ⇒ no aborted folder · ledger NUL-free,
  newline-terminated, exact header · each row 8 tab fields · job · rung · `dir` = `<job>_<rung>_<row number>` · `wall_s` seconds or UNKNOWN · rows ≤ 2 ·
  **set of ledger dirs = set of `run_aborted/<job>_<rung>_<k>` folders** · every receipt valid (②, incl. `run_id` = that folder's `attempt.start`) ·
  ledger `wall_s` = receipt `wall_s`. Runner: any mismatch → REVIEW exit 8 (start point not written, nothing launched); checker: LADDER_VIOLATION.
  Where: runner `ledger5` run_a5.sh:298 · ladder top :937 · `--infra-abort` :538 · `--infra-wall` :588 / :598; checker `ledger_problems`
  build_a5_vasp_package.py:2139, called from `check_return` :2332.
- **Your scenario → now.** Your partial restore (ledger keeps the first c1 abort; its folder and `start_point.json` missing): was a start point re-written
  4 s after the first c1 · c1 relaunched · OK · new c1 adopted → now **exit 8 · start point not written · c1 not launched · checker LADDER_VIOLATION ·
  no adoption** (`eo_led0`); folder present but ledger row missing (`eo_led1`) and receipt `run_id` ≠ `attempt.start` (`eo_led2`) → the same.
  Checker on an OK return: ledger row removed · folder removed · ledger wall ≠ receipt → LADDER_VIOLATION. Runner = checker on **19 return variants**
  (problem / no problem identical).
- **Mutants.** m92 m93 (runner: no check at the ladder top · no set equality) · m109 (checker: no ledger check).
- **Still not caught.** A ledger, folders and receipts forged consistently with each other; at most 2 rows (`INFRA_MAX`).

### P2 Run identity in the final record (Q-EO-4 · conditional)

- **Fix.** `final.json` now also carries `attempts` = `path=run_id` for every attempt folder (`run/<job>_{A5,c1,c2}`, `run_aborted/<job>_<rung>_<k>`),
  in byte order, `-` when a run_id cannot be read. The re-run bundle check still compares the bundle's `final.json` with the current one byte for byte —
  two separate runs on the same mock second now differ there. The checker also requires `attempts` = the return's own folders / run_ids (else
  STOPPED_FOR_REVIEW). `final.json` is read with REC1 on both sides.
  Where: runner `att5` run_a5.sh:343 · `fin5` :708 · `ret_has_final` :646; checker `attempts_of` build_a5_vasp_package.py:2194 · `check_return` :2411.
- **Your scenario → now.** Two runs on the same mock second (`FAKE_NOW`): final records identical except `attempts`; the other run's tgz + sha moved in:
  was re-run exit 0 · OK → now **re-run exit 4 (repack hint) · after `PACK_ONLY=1` exit 0 · OK** (`eo_sw1` / `eo_sw2`); edited `attempts` →
  **STOPPED_FOR_REVIEW**.
- **Mutants.** m95 (runner: no `attempts`) · m110 (checker: no `attempts` check).
- **Still not caught.** `attempts` binds folder paths and run_ids, not file contents (those stay with the existing sha / record checks).

## 4. Tests

- Selftests: a5 **211/211** (was 163) · V5 **313/313** (unchanged file) · round2 **194/194** (unchanged file) — python 3.11 · `dftd3` 1.6.0 venv.
  The a5 selftest also passes on the final tool with **gawk 5.2.1** as `awk` and under `LC_ALL=C.UTF-8` (the runner's own awk code runs in both; default awk = mawk 1.3.4).
- Mutants: `build_a5_vasp_package.py --mutants --jobs 4` (venv python, one pass of all 113) — **113/113** on tool `35592b07ed0f0fd8…`: the 84 earlier ones
  (15 re-targeted to the new code because the lines they mutated were replaced — m25 m41 m52 m57 m59 m61 m63 m69 m73–m79) + **29 new (m85–m113)**,
  per condition as listed in §3 (① 10 · ② 8 · ③ 6 · ④ 3 · P2 2). In our first pass three of the new mutants survived — m101 (checker: damage on a finished attempt reported before the restart / settings checks), m112 (checker: damage in a preserved abort folder) and m113 (runner: the `--infra-abort` start check) — because no test went down those paths. We added `eo_findmg`, the aborted-folder damage case and `eo_st_iab` (§3; selftest 208 → 211), saw all three turn red, and re-ran all 113 on the final tool (0 invalid).
- EN reproductions (`ken1` ISTART 0, `ken2` `XYZ:`) and the positive controls (`kill2b`, `rcpt`, `spok`, `stale`) still pass.
- EM probes p1–p9 (10 files incl. p3b) re-run on the EO-reviewed tool and on the new tool, compared after normalising times, hashes and run ids:
  **9 identical** (p1, p2, p4 and p9 end in the same `FileNotFoundError` in both versions — the probe scripts expect a file the runner does not create on
  that branch; their verdict lines are identical). **p7 (prep failure) changed label**: LADDER_INCOMPLETE → **STOPPED_FOR_REVIEW**, adoption none in both.
  Cause: the probe deletes and re-creates the c2 (then c1) folder in a finished return, so the final record's `attempts` no longer matches the tree — the
  P2 check catches that edit. With `attempts` refitted to the edited tree (the list a runner would have written for it; scratch probe p7b) the label is
  LADDER_INCOMPLETE again with the same note.
- Collector regression: the 11-20 G5 aggregate re-run → rc 3 · JSON byte-identical (sha `afecfa08…`) · console output byte-identical (compared only, never displayed).

## 5. Please look especially at

1. **Complete row = newline-terminated.** An unterminated last line is never counted, even when it looks complete (its last field may be cut).
   A newline-terminated short row is treated as damage (exit 8), not as a cut tail. Is that the right side to err on for a scheduler kill on Lustre / NFS?
2. **REC1 is a strict subset of JSON**, compared on raw (undecoded) string values on both sides. Valid JSON outside the subset (e.g. `1e3`, `null`,
   nested objects, an escaped `_` in `job`) is refused by **both** sides. Any input where the two implementations still disagree?
3. **Exit codes**: an `attempt.start` that does not belong to its folder ends in exit 2 (no final record, "contact"), not exit 8; a ledger / folder /
   receipt mismatch ends in exit 8 (final record). Agree with this split?
4. **Cap re-derivation** uses ladder order (A5 aborts, A5, c1 aborts, c1, c2 aborts, c2) — order violations are reported separately, as before.
5. **What still cannot be caught**: a return in which ledger, receipts, attempt folders and the final record were all forged consistently (the checker
   only cross-checks what is in the return); `attempt.json` is not REC1 (see ②).

## 6. Questions

- **Q-EP-1** (①): complete-row counting closed — same rule on both sides · 0 complete rows + damage → review · cut tail not counted · 7-row control kept?
- **Q-EP-2** (②): receipts and the start record closed — escaping on write · whole-record REC1 read on both sides (ESC / comma loss / no space) ·
  `attempt.start` checked against its folder before the run_id link?
- **Q-EP-3** (③): abort wall time and the cap closed — receipt time first on both sides · checker re-derives the cap · UNKNOWN only before any later launch · fill time?
- **Q-EP-4** (④ + P2): ledger ↔ preserved folders closed (runner before the start point / any launch, checker on return)? Run identity in `final.json` closed?
- **Q-EP-5**: Any new hole introduced by these fixes?
- **Q-EP-6**: Send approval — may package MANIFEST `f10dedefe8165f64999a0dca9897ef39e951a6c3085a1baa6ee9b0106a1b169c` go to the operator?

## 7. How to reproduce

- `python3 -I tools/wad/build_a5_vasp_package.py --selftest` · `… --mutants --jobs 3` (or `--mutants m85 m86 …` for the new ones; run it with a python that
  has `dftd3` so the V5 mutants are judged by the V5 selftest, not by an import error) · `python3 -I tools/wad/build_v5_vasp_package.py --selftest`
  (needs `dftd3` 1.6.0 — PyPI name `dftd3`).
- `python3 -I tools/wad/build_a5_vasp_package.py --build --out <new folder>` → `diff -r` with `db/inputs/wad_a5_vasp_2026_11_20` · MANIFEST sha.
- The fake VASP now also accepts `behaviour@N|fragment` (write N rows, then `fragment` without a newline; `\n` inside the fragment is a newline) — that is
  how `SDA:` cuts are made; a `date` wrapper honours `FAKE_NOW` (same-second runs).

## 8. Reply format

Per question: verdict (GO / conditional / NO-GO) · evidence (file:line or test) · minimal fix if not GO. Please do not print W values.
