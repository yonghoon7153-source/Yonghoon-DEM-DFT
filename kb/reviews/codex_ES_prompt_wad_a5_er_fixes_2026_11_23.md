---
title: "ES 프롬프트 — W_ad a5 묶음 Codex ER (NO-GO) 고침 확인: 같은 트리 관문 위에 — 준비 폴더의 실행 기록 보존 · 끝 기록 · WAVECAR 지우기 전 관문 · 0 스텝은 0 행으로 설명될 때만 · 이력 줄 벽시계 = 끝 기록 · 기록 명령 · 포장 배타 잠금 · 중간 반송본 대비 관측 사실 후퇴 거부 · 끝 기록 잡 · 변형 · stage · POTCAR 해시 — 업체 발송 GO 여부"
date: 2026-11-23
updated: 2026-11-24
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, prompt, letter]
letter: ES
track: wad
channel: codex
kind: prompt
status: 발송 · 회신 수령 2026-11-24 — NO-GO (P0 2 · P1 2 · P2 1 · 회신 codex_ES_reply_wad_a5_er_fixes_2026_11_24.md) · 기준 1da64d0be · MANIFEST 50beb026…
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). Codex ER (NO-GO · Q-ER-6 GO · 나머지 범위 안) 다음 편지다. ER 원문 `codex_ER_reply_wad_a5_eq_fixes_2026_11_23.md` · 첨부 `codex_ER_evidence_2026_11_23/` · 빌드 기록 ⑭ (회신 요약) · ⑮ (고침).
> 고침은 EQ 때 세운 트리 관문 하나 위에 같은 규칙으로 얹었다 (러너 = 검사기 · 같은 낱말). §1b 위협 범위는 EQ · ER 편지 그대로 싣는다.
> ⛔ 점착 W 값은 싣지 않는다 (문턱 · 상태 · 종료 코드만). ⬇ 아래 **보내는 글** (영어) 만 발송한다. 회신이 오면 `codex_ES_reply_wad_a5_er_fixes_2026_11_2x.md` 로 원문 보존.
> ⚠ GO 가 와도 업체 발송은 사용자가 정한다 · DEM 편지 10 은 a5 가 끝난 뒤 (사용자 11-20).

---

**[W_ad · a5] Fixes for your ER findings — on the same tree gate, same rules on both sides — please confirm before we send the package to the operator**

## 0. What we are asking

Your ER review (package `cc3873047`, MANIFEST `8e295bae…`) returned **NO-GO**; Q-ER-6 (blank fields · UTF-8 · ledger order) was GO, the rest in scope.
You confirmed the EQ counter-examples closed and found seven new ways to lose evidence or lift the cap: a killed c1 moved under its own `.prep_…_c1`
name and deleted by the prep cleanup · the final stage's junk file caught only after `final.json` was written and A5's `WAVECAR` deleted · a first row
whose colon became `;` (or a bare `SDA`) accepted as 0 steps · c1's end record and history row disagreeing (48,001 vs 648,001 s) · two recording
commands overlapping so the second receipt replaced the first · an intermediate return's 7 rows (or a filled receipt) silently rolled back · and an end
record whose job, or a `POTCAR.sha256`, no longer matched while the runner carried on.

We kept the structure of the EQ fix — **one fail-closed tree gate, the same rules and reason tokens in the runner and the checker** — and closed each
finding inside it or in front of it: the gate now also runs **before every irreversible step** (deleting A5's `WAVECAR`, writing `final.json`), reads
**prep folders**, **end-record identity and the POTCAR hash**, **history wall times**, and compares the tree with an existing return for **observed
facts that went backwards**; the 0-step test accepts only content that 0 rows explain; and computing, recording commands and repacking share **one
exclusive lock**. We reproduced your seven scenarios in the selftest **before** fixing — **10 new checks, all red on the ER package (266/276)** — and
rebuilt the package (**MANIFEST `50beb026f9e463a247f2c4da6452e7a048c31fb9e9ca72e39db98bc94ebf2e74`**). Please review **only these fixes**: is each finding closed (GO / conditional / NO-GO)? Did a fix open a new
hole? May this package go to the operator? Physics settings, the ladder, thresholds, the secondary rule and the G4/G5 arithmetic are unchanged.

## 1. Scope

- Base = `cc3873047` (what ER reviewed). Records-only commits after it (the main-session check, your reply verbatim, attachments, build-log key `⑭`)
  do not touch tools or package. Fixes: `19ddec83c` (tools · tests), `a6b34ffa6` (one more test, `er_packgate`, §4 Q-ER-1②) and `1da64d0be`
  (package rebuilt · build log `⑮`). This letter is a records-only commit after them.
- `git diff cc3873047 1da64d0be -- tools/wad/build_a5_vasp_package.py tools/wad/build_v5_vasp_package.py` — a5 tool sha256 `41a486faf764663e…`;
  the V5 collector file is **unchanged** (`90065ed5c4f7d052…`).
- Package `db/inputs/wad_a5_vasp_2026_11_20/` — changed files: `run_a5.sh` · `README.md` · `jobs.json` (tool sha · rule strings, new `zero_step_rule` ·
  `lock_rule`) · `MANIFEST.sha256`. Job inputs and `SEALED_ENV.tsv` are byte-identical. Two fresh builds are byte-identical.
- Line numbers below: runner = `db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh`; checker = `tools/wad/build_a5_vasp_package.py`; both at `1da64d0be`.

## 1b. Threat model — unchanged from EQ / ER (accepted in Q-EQ-7; please judge against this)

The operator is a contracted, cooperating party. The runner and the return checker exist to catch **honest failures**, not forgery.

- **In scope (a hole here is blocking):** anything an honest operator, a crashed node or a careless manual recovery can produce without intent —
  truncated or garbled output, a killed or interrupted run, a stale file left behind by a partial restore, a file copied into the wrong folder
  (including a receipt from another attempt), missing or duplicated records, wrong or empty fields typed into a recording command, encoding accidents,
  and clock or scheduler quirks.
- **Out of scope (please report as a note, not as a blocker):** a return deliberately edited so that two or more records agree with each other —
  for example replacing a field with another syntactically valid value and adjusting the matching ledger row, folder number or final record to fit.
  A return in which ledger, receipts, history, attempt folders and the final record were all edited consistently cannot be detected from the return
  alone; we accept that limit.
- **Rule of thumb:** if the scenario needs one accidental action, it is in scope; if it needs coordinated edits of two or more records chosen to stay
  consistent, it is out of scope. When unsure, say which and why.
- The fixes for your EP findings stay in place whichever side of this line they fall on.

## 2. Rules (sealed — not up for review)

Same as EQ §2: Amendment 5 v2 ladder A5 → c1 → c2; Interpretation 1 (next stage only after a confirmed SCF_NOT_CONVERGED or a run failure /
killed attempt with ≥ 1 electronic row; 0 rows → exit 7; RESTART_NOT_HONOURED · SCF_UNVERIFIED · settings-echo mismatch → exit 8);
c1's secondary value only after c2 itself ended in a confirmed state.

## 3. What changed in the gate (summary)

- **Entry points.** In addition to restart, every stage launch, `PACK_ONLY`, `pack()` and the four recording commands, the gate now runs at the
  start of `drop5` (before A5's `WAVECAR` is deleted, run_a5.sh:1172) and of `fin5` (before `final.json` is written, :992).
- **Lock.** `lock_take` (:768) is the one exclusive lock for computing (:927), the recording commands (:797) and
  `PACK_ONLY` (:917); it is held from the first check to the last write (released by the exit trap). A second, overlapping command is
  refused (exit 2) and the first record stays.
- **New checks inside the gate** (runner = checker, same tokens): prep-folder contents (`prep_<path>`); end-record job · attempt · stage
  (`end_job` · `end_attempt` · `end_stage`) and the POTCAR hash (`end_potcar_sha`); history wall time (`status_row_<i>_elapsed`); and, runner only,
  observed facts that went backwards against an existing return (`tgz_rows_lost_<path>` · `tgz_receipt_wall_<path>`).
- **0-step reading** (row rule, runner = checker): with 0 complete rows, every other line must be blank or the OSZICAR column title (a cut tail may be
  its beginning); anything else is `unexplained_line` → review.
- **Same rules on both sides.** As at ER, runner functions are cut verbatim from the generated script into the selftest harness: tree tokens
  (39 probes — the new ones: prep folder, end job / attempt / stage, POTCAR hash), the ledger harness (29 variants — new: history wall
  time), `row_scan` = `row_gate` (51 OSZICAR probes × 3 stages — new: the 0-step cases).
- **One gate, one mutation.** Switching the runner gate off (m141) turns **53 of the 279** selftest checks red; switching the checker
  gate off (m169) turns **21** red.

## 4. Your findings one by one

Each block: **fix** (where) · **your scenario → now** (selftest case, fake VASP; "was" = the ER package, reproduced red first) · **mutants** · **still
not caught**.

### Q-ER-1① · prep cleanup deleted run evidence (P1)

- **Fix.** A prep folder (`run/.prep_<job>_<stage>`) may only hold what the runner writes before launch — INCAR, POSCAR, KPOINTS, POTCAR,
  POTCAR.species.sha256, POTCAR.titel, POTCAR.sha256, WAVECAR, attempt.start (`PREP_ALLOW` build_a5_vasp_package.py:144). Anything else
  (OSZICAR, OUTCAR, stdout.log …) is run evidence: the gate stops with `prep_<path>` before the cleanup at :970 or the per-launch reset can
  delete it. Runner `files5` :541 = checker `files_problem` :2856.
- **Your scenario → now.** A killed c1 with 7 complete rows renamed to `.prep_…_c1`: was deleted, new c1, return OK, `a5_c2` adopted → now **exit 8,
  tree byte-identical, the folder (with its OSZICAR) kept, no new c1** (`er_prep`).
- **Mutants.** m192 (runner) · m193 (checker).
- **Still not caught.** A prep folder holding only the allowed names is treated as prep (it never ran — VASP is launched only after the atomic rename).

### Q-ER-1② · the final step's checks came after irreversible steps (P1)

- **Fix.** `drop5` and `fin5` start with the gate, so a junk file from the last stage stops the runner before A5's `WAVECAR` is deleted and before
  `final.json` is written; `pack()` keeps its own gate. Policy unchanged: non-standard MPI logs or core files stop the runner (exit 8, contact).
  The new gates in front of `pack()` hide its own gate from the old tests, so one more test holds `PACK_ONLY` after its gate and before `pack()`
  (at its `$(utc)` call), drops an unknown file into A5's folder and expects **exit 8 from the packing gate, no return, no temporary files**
  (`er_packgate`).
- **Your scenario → now.** The fake c1 leaves `core.1`: was `final.json` OK, A5 `WAVECAR` deleted, exit 8 only at packing → now **exit 8, no
  `final.json`, A5 `WAVECAR` kept, no return** (`er_end`); the review path that writes `final.json` without `drop5` behaves the same (`er_end_rev`);
  the EQ test `eq_junkc1` now expects the earlier stop.
- **Mutants.** m194 (`fin5` gate) · m195 (`drop5` gate) · m158 (`pack()`'s own gate — it survived the final full run because the new gates hid
  it; red once `er_packgate` was added).
- **Still not caught.** The full list of file names the operator's VASP wrapper creates is unknown (as you noted) — an unknown name stops the runner.

### Q-ER-2 · 0-step classification (P0)

- **Fix.** With 0 complete rows the OSZICAR must be explained by 0 rows: every non-row line blank, or the column title (`N E dE d eps ncg rms
  [rms(c)]` after collapsing blanks, blank-led — `OSZ_TITLE` :145); an unterminated tail may be the beginning of the title. Anything else is
  `unexplained_line` → `--infra-abort` refuses (exit 2) and the resume stops for review (exit 8). With ≥ 1 complete row other lines (e.g. `1 F= …`)
  are untouched. Runner `row_scan` :658 = checker `row_gate` :231 (`_unexplained` :236).
- **Your scenario → now.** c2's OSZICAR `SDA; 1 0 0 0 12 0` (colon → semicolon) and a bare `SDA`: was `--infra-abort` 0, new c2, `a5_c2` adopted → now
  **`--infra-abort` 2 (nothing preserved), resume exit 8 (review), nothing adopted** (`er_zero0` · `er_zero1`). Pure cases: title only, title + blank
  lines, a cut title, blank-led `N` → 0 steps; title at column 1, an `F=` line without rows, `SDA x` → `unexplained_line`.
- **Correction to our ER letter.** The longest token in real 5.4.4 rows is **19 characters** (your count: 20 V5 outputs, 2,733 DAV/RMM rows), not 16;
  the 24-character bound (`ROW_TOK_MAX` :177) keeps a margin. The vendor's c2 output format is still unverified.
- **Mutants.** m196 (runner) · m197 (checker).
- **Still not caught.** An unknown 0-row layout of a real c2 (ALGO=All) stops for review rather than counting as 0 steps.

### Q-ER-3① · end record and history row disagree (P0)

- **Fix.** For every history row the wall time (`status.tsv` column 10) must equal `elapsed_s` of that attempt's end record, before anything is summed
  (`status_row_<i>_elapsed`). Runner `hist5` :386 = checker `history_problems` :2586. An end record without its row (the runner stopped
  between the two writes) is still accepted.
- **Your scenario → now.** c1 at 648,001 s in both records (control: exit 5, c2 not launched); `attempt.json` alone loses its first digit (48,001):
  was c2 launched, return OK, `a5_c2` → now **exit 8, c2 not launched, tree unchanged, checker LADDER_VIOLATION** (`er_el`). Two older fixtures that
  had edited `elapsed_s` alone (S15 · `eq_kc`) now edit both records, as a real runner would.
- **Mutants.** m198 (runner) · m199 (checker).
- **Still not caught.** Both records edited to the same smaller value (two coordinated edits — out of scope, §1b).

### Q-ER-3② · overlapping recording commands (P0)

- **Fix.** The recording commands take the same exclusive lock as a computing run before their checks and hold it to the last write (§3 "Lock").
- **Your scenario → now.** The first `--killed` (648,001 s) is paused after its checks and before its write (the selftest holds it at its first
  `date` call); a second `--killed` (0 s) runs meanwhile: was both exit 0 → now **second refused (exit 2, the lock is live), first completes (exit 0),
  `killed.json` = 648,001 s from the first** (`er_lock`).
- **Mutants.** m200 (lock removed from the recording commands) · m20 (re-targeted: a live lock no longer refuses).
- **Still not caught.** `PACK_ONLY` takes the same lock but has no concurrency test of its own.

### Q-ER-4 · observed facts rolled back against an intermediate return (P0)

- **Fix.** The existing-return comparison now also extracts each attempt's OSZICAR and receipt: the current folder of that attempt must have at
  least as many complete rows as the return had (`tgz_rows_lost_<path>`), and a receipt's wall time may only go from `UNKNOWN` to a value — a value that
  changed or went back to `UNKNOWN` stops (`tgz_receipt_wall_<path>`). Runner `tgz5_in` :600 · :604. The return is not pinned
  byte for byte; growth (new rows, a filled receipt, new attempts) stays allowed.
- **Your scenario → now.** Intermediate return with c1's 7 rows, then c1 restored to its pre-output checkpoint: was `--infra-abort` 0, new c1, return
  overwritten → now **`--infra-abort` 8 and resume 8, tree and return byte-identical** (`er_rows`). A receipt filled to 648,001 s in an intermediate
  return, then receipt and ledger restored to their `UNKNOWN` versions: was `PACK_ONLY` 0 (return overwritten) → now **`PACK_ONLY` 8, return unchanged**
  (`er_rcpt`).
- **Mutants.** m201 (rows) · m202 (receipt wall time).
- **Still not caught.** A rollback with no earlier return on disk (nothing to compare with).

### Q-ER-5 · end-record identity and POTCAR hash before launch (P1 · conditional)

- **Fix.** The runner's end-record check (`att_ok5` :472) now also requires `job`, `attempt` and `stage` to equal the start record (which is
  bound to the folder), and the POTCAR hash recorded in the end record to equal the on-site `POTCAR.sha256` byte for byte (:481); checker
  `att_problem` does the same (:2749 · :2761). No POTCAR body is returned.
- **Your scenario → now.** One character of A5's `attempt.json` job, or one digit of `POTCAR.sha256`: was runner exit 0 (c1 launched), rejected only by
  the checker → now **exit 8 before c1, tree unchanged; the checker does not adopt** (`er_endrec0` · `er_endrec1`); tree-token probes for job,
  attempt, stage and POTCAR hash on both sides.
- **Mutants.** m203 m204 m205 m206 (runner) · m207 m208 m209 m210 (checker).

## 5. Tests

- Selftests: a5 **279/279** (276 when the 10 new counter-example checks were added, all 10 red on the ER package: 266/276; then `er_packgate`) ·
  V5 **313/313** (unchanged file) · round2 **194/194** (unchanged file) — python 3.11 · `dftd3` 1.6.0 venv, re-run on the `a6b34ffa6` tree.
  The a5 selftest also passes with **gawk 5.2.1** as `awk` and under `LC_ALL=C.UTF-8` (default awk = mawk 1.3.4).
- Existing tests adjusted: S15 and `eq_kc` now set the wall time in both the end record and the history row; `eq_junkc1` expects the stop before
  `final.json`. Two fixtures were corrected while fixing: the overlapping-command case pauses the first command at its first `date` call (after its
  checks, before its write — your description); the receipt case uses a killed 0-step attempt, whose receipt starts as `UNKNOWN`.
- Mutants (`build_a5_vasp_package.py --mutants`): **210/210** — one full run at the end (fail-fast, `--jobs 4`, 141 min) on tool `592b812d87df3706…`
  (`19ddec83c`): 209/210 red. The one survivor, m158 (`pack()`'s own gate), was hidden by the new gates in front of it (`fin5`, `drop5`, `PACK_ONLY`);
  `er_packgate` was added, and m158 on its own on the final tool `41a486faf764663e…` is red. The final tool differs from `592b812d87df3706…` only by
  that test (14 added lines inside the selftest; no runner, checker or mutant line; all 210 mutant anchors occur as before), and an added check cannot
  turn a red mutant green, so the other 209 results stand. Before the full run, the 22 new or re-targeted mutants (m20 m113 m128 re-targeted to the
  lock and gate lines that moved · m192–m210, one per new rule on each side) were run on their own: 22/22 red.
- EN / EO / EP / EQ reproductions and positive controls still pass (selftest).
- Collector regression: the recorded G5 command (V5 return unpacked in scratch) on the `a6b34ffa6` tree gives rc 3, the same JSON `afecfa08…` and
  the same console output, byte for byte.

## 6. Please look especially at

1. **0-step rule.** Only blank lines and the column title (its beginning, if cut) count as 0 rows. Is that the right reading of a 5.4.4 OSZICAR that
   ended before its first row?
2. **Lock.** One lock for computing, recording commands and `PACK_ONLY`, held from the first check to the last write; a stale lock on the same host is
   cleared, a live or foreign one refuses (exit 2). Agree?
3. **Facts that may only grow** against an intermediate return: complete rows per attempt and receipt wall time (`UNKNOWN` → value). Is anything
   else in an intermediate return a fact we should hold?
4. **What still cannot be caught** (per §1b): coordinated edits of two or more records; a rollback with no earlier return; the wall seconds typed
   into `--killed`; the node clock.

## 7. Questions

- **Q-ES-1** (Q-ER-1): prep folders with run evidence are kept and stop the runner; the gate runs before `drop5` and `fin5` — closed?
- **Q-ES-2** (Q-ER-2): 0 steps only when 0 rows explain the file — closed?
- **Q-ES-3** (Q-ER-3): history wall time = end record before summing; recording commands under the one lock — closed?
- **Q-ES-4** (Q-ER-4): complete rows and receipt wall time may not go backwards against an existing return — closed?
- **Q-ES-5** (Q-ER-5): end-record job · attempt · stage and the POTCAR hash checked by the runner before launch — closed?
- **Q-ES-6**: any new hole introduced by these fixes?
- **Q-ES-7**: Send approval — may package MANIFEST `50beb026f9e463a247f2c4da6452e7a048c31fb9e9ca72e39db98bc94ebf2e74` go to the operator?

## 8. How to reproduce

- `python3 -I tools/wad/build_a5_vasp_package.py --selftest` · `… --mutants --jobs 4` (or `--mutants m192 m193 …`; run it with a python that has
  `dftd3` so the V5 mutants are judged by the V5 selftest) · `python3 -I tools/wad/build_v5_vasp_package.py --selftest` (needs `dftd3` 1.6.0).
- `python3 -I tools/wad/build_a5_vasp_package.py --build --out <new folder>` → `diff -r` with `db/inputs/wad_a5_vasp_2026_11_20` · MANIFEST sha.
- `A5_SELFTEST_FAILFAST=1` stops the selftest at the first red check (the mutant runner sets it).

## 9. Reply format

Per question: verdict (GO / conditional / NO-GO) · evidence (file:line or test) · minimal fix if not GO · for every new finding, **in scope** (blocking) or
**out of scope** (note) per §1b. Please do not print W values.
