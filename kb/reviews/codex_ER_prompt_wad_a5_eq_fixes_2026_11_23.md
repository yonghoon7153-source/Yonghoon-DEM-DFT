---
title: "ER 프롬프트 — W_ad a5 묶음 Codex EQ (NO-GO) 고침 확인: 트리 관문 하나 (러너 모든 진입점 — 다시 돌림 · 단 발사 직전 · PACK_ONLY · 포장 덮어쓰기 전 · 기록 명령 · 검사기 같은 규칙 · 같은 낱말) — 기록 문법 엄격 · 끝 기록 원자적 쓰기 · 끝 기록 + 끊김 기록 공존 거부 · 끊김 기록 결속 · 잔여 · 모르는 파일 · 기존 반송본 대조 · 끝 기록 code/state 조합 · 앞 빈칸 머리 조각 · 칸 길이 ≤ 24 · 필수 칸 빈칸 문자 · 기록 UTF-8 · 장부 단 순서 — 업체 발송 GO 여부"
date: 2026-11-23
updated: 2026-11-23
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, prompt, letter]
letter: ER
track: wad
channel: codex
kind: prompt
status: 발송 대기 (사용자) · 기준 891e106e5 (EQ 가 본 묶음 · MANIFEST 679d7050…) → 고침 c14d52abb (도구 · 시험) · cc3873047 (묶음 · 빌드 기록 ⑬) · 묶음 MANIFEST 8e295bae… · selftest a5 266/266 · 돌연변이 191 (첫 전체 판 186 · 살아남은 5 시험 떼어 5/5)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). Codex EQ (NO-GO · 위협 범위 §1b GO · 범위 안 지적 전부) 다음 편지다. EQ 원문 `codex_EQ_reply_wad_a5_ep_fixes_2026_11_23.md` · 첨부 `codex_EQ_evidence_2026_11_23/` · 빌드 기록 ⑫ (회신 요약) · ⑬ (고침).
> ⭐ 이번 고침은 항목별 땜질이 아니라 **트리 관문 하나** 로 묶었다 (다섯 번째 NO-GO · 같은 종류 — '러너는 계속하고 검사기만 나중에 거부' · '잔여 · 복사된 · 깨진 기록을 믿음' — 가 되풀이됐다). §1b 위협 범위는 EQ 편지 그대로 싣는다.
> ⛔ 점착 W 값은 싣지 않는다 (문턱 · 상태 · 종료 코드만). ⬇ 아래 **보내는 글** (영어) 만 발송한다. 회신이 오면 `codex_ER_reply_wad_a5_eq_fixes_2026_11_2x.md` 로 원문 보존.
> ⚠ GO 가 와도 업체 발송은 사용자가 정한다 · DEM 편지 10 은 a5 가 끝난 뒤 (사용자 11-20).

---

**[W_ad · a5] Fixes for your EQ findings — one fail-closed tree gate on every runner entry point, and the same gate in the return checker — please confirm before we send the package to the operator**

## 0. What we are asking

Your EQ review (package `891e106e5`, MANIFEST `679d7050…`) returned **NO-GO** and accepted the threat model of §1b (Q-EQ-7 GO). The EP counter-examples
were closed; your new findings were all in scope: a header fragment after leading blanks (`  SDA`) read as 0 steps · a 310-digit number read as a row ·
a foreign `killed.json` in a finished attempt lifting the 180 h cap · `run/` restored to an older checkpoint overwriting a valid existing return ·
a 0-byte `status.tsv` · a truncated end record (`attempt.json` without its `}`, or `t_start` with `.5`) that the runner kept going on · a repack
(`PACK_ONLY=1`) that dropped on-site errors (a leftover `*.part`, a changed end ID, `code 0` + `REVIEW`) · a scheduler ID of three blanks · a receipt byte
corrupted after saving · and, as a note (P2), a same-second ledger swap. They are one pattern that kept coming back: **the runner keeps going on a tree
that only the checker rejects later, and records that are left over, copied or broken are trusted.**

So instead of one patch per finding we put **one fail-closed tree gate** in front of everything the runner does, and the checker applies **the same rules,
with the same reason tokens,** to the return. Anything unknown, unreadable or inconsistent stops the runner with **exit 8 before it writes, launches or
packs anything**; the tree and any existing return stay as they were. We reproduced every EQ scenario in the selftest **before** fixing (20 new checks red
on the EQ package: 237/257), built the gate on both sides, and rebuilt the package (**MANIFEST `8e295baea495de906bddb172f14e30a1fe2d58cd93775ddee783c95c0ce0db5d`**). Please review **only these fixes**: is each
finding closed (GO / conditional / NO-GO)? Did the gate open a new hole? May this package go to the operator? Physics settings, the ladder, thresholds,
the secondary rule and the G4/G5 arithmetic are unchanged.

## 1. Scope

- Base = `891e106e5` (what EQ reviewed). Records-only commits after it (the §1b addition to the EQ letter, your reply verbatim, attachments, build-log
  keys `⑪` `⑫`) do not touch tools or package. Fixes: `c14d52abb` (tools · tests) and `cc3873047` (package rebuilt · build log `⑬`). This letter is a
  records-only commit after them.
- `git diff 891e106e5 cc3873047 -- tools/wad/build_a5_vasp_package.py tools/wad/build_v5_vasp_package.py` — a5 tool sha256 `edd9666cd1ade0e6…`;
  the V5 collector file is **unchanged** (`90065ed5c4f7d052…`).
- Package `db/inputs/wad_a5_vasp_2026_11_20/` — changed files: `run_a5.sh` · `README.md` · `jobs.json` (tool sha · rule strings, new `tree_gate_rule`) ·
  `MANIFEST.sha256`. Job inputs (INCAR ×4 · POSCAR · KPOINTS · POTCAR spec) and `SEALED_ENV.tsv` are byte-identical.
- Line numbers below: runner = `db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh` (generated from `RUN_A5_ENV/CLI/BODY` in the tool file);
  checker = `tools/wad/build_a5_vasp_package.py`; both at `cc3873047`.

## 1b. Threat model — unchanged from EQ (accepted in Q-EQ-7; please judge against this)

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

## 3. One tree gate (the structural fix — please read this first)

**Where it runs.** `tree_gate` (run_a5.sh:603) evaluates `tree5` (:588); on the first reason it prints it and exits **8** — nothing is
written, launched or packed, and `run/`, `run_aborted/` and `a5_return.tgz` stay as they were (the lock is removed by the exit trap). It is called at
every entry point:
1. every start or restart, right after the lock and before anything is written (env.txt, status.tsv, prep cleanup, ⓪ record, reuse of a finished
   ladder) — :901;
2. right before every stage launch (first line of `cap_gate`, before the time-cap check) — :1136;
3. `PACK_ONLY=1` — :881;
4. inside `pack()` itself, before `a5_return.tgz` is overwritten (covers the final pack and the reuse of an existing return) — :126;
5. the four recording commands `--infra-abort` · `--infra-wall` · `--killed` · `--reset-w0` — :761.

**What it checks, in this order (the first reason wins).**
1. **Names** (`files5` :511 = `files_problem` build_a5_vasp_package.py:2756). `run/` holds only the known records, the three stage
   folders, the lock and the prep folders; `run_aborted/` only `<job>_<stage>_<k>` folders; an attempt folder only regular, non-link files whose names
   are on the return allow / forbid lists or are standard VASP outputs (`CONTCAR`, `DOSCAR`, … `vaspout.h5`). Any `*.part`, unknown name, link or
   subfolder anywhere under `run/` or `run_aborted/` stops it (`run_entry_<n>` · `aborted_entry_<n>` · `file_<path>`) — so a repack can no longer drop an
   on-site error.
2. **Each attempt folder** (`rec_dir5` :491 = `rec_dir_problem` :2721; reason `<folder>:<token>`): `attempt.start` present and
   belonging to the folder · the four records (`attempt.start`, `attempt.json`, `killed.json`, `infra_abort.json`) valid UTF-8 · a finished attempt's
   `attempt.json` parses with **the exact printf template the runner writes** (`tpl5` :432 = `tpl_parse` :2617 — strings without quote,
   backslash or control bytes; integers without leading zero and ≤ 16 digits; nothing missing, nothing extra: a lost `}` or `"t_start": 1763856000.5`
   is `att_form`) and its identity and **seal** hold (`att_ok5` :463 = `att_problem` :2681 — `run_id` and `t_start` = `attempt.start`;
   the sha256 table in `attempt.json` = the files now present, POTCAR body excluded) · `killed.json` never in `run_aborted/` (`killed_in_aborted`) and
   never next to `attempt.json` (`end_and_killed`), and when alone it is **bound to that attempt before any time is used** (`killed_rec5` :478
   = `killed_rec_problem` :2696 — one-line record, fields, required fields not blank, job and rung, **`run_id` = `attempt.start`**,
   wall-seconds form, `recorded_s` ≥ `t_start`) · no `infra_abort.json` in a `run/` stage folder (`stray_receipt`).
3. **Ledger · receipts · history** (`ledger5` :302 with `receipt5` :284 and `hist5` :366 = `_ledger_core` :2538 ·
   `abort_receipt_problem` :2419 · `history_problems` :2481): as at EP, plus valid UTF-8 for `infra_aborts.tsv` and
   `status.tsv`, a **non-empty** `status.tsv` (header-only is fine — `status_empty`), its last line ending in a newline, and ledger rows in stage order
   A5 ≤ c1 ≤ c2 (P2).
4. **Final record**, if present (`fin_ok` :414 = `final_problem` :2783): UTF-8 · one-line record · fields · **allowed code/state pairs
   only** — (0, OK) (1, NO_PRIMARY) (1, CLOSED) (5, CAP) (6, ENV) (8, REVIEW) (`FINAL_COMBOS` :144) · attempts = the attempts now in the tree.
5. **Start point and ⓪ record**, if present (`sp_rec5` :537 · `w0_rec5` :545 = `sp_problem` :2802 · `w0_problem` :2813;
   `w0_check.json` by its printf template).
6. **Existing return** (runner only — `tgz5` :550, `tgz5_in` :562). If `a5_return.tgz` or its `.sha256` exists, both must exist and match
   (a pack's own temporary files are removed by the next pack and are not part of this check). The record files are extracted to a temporary folder: the tgz `final.json` must be byte-identical to the
   current one (a missing or different current `final.json` is `tgz_final_differs`); every attempt in the tgz (by its `attempt.start` run_id) must still be
   in the tree — a `run/` attempt in place or moved by `--infra-abort` into a `run_aborted/` folder of the same stage, a `run_aborted/` attempt in the same
   place — with byte-identical `attempt.json` / `killed.json` where the tgz had them (`tgz_attempt_missing_<path>` · `tgz_end_differs_<path>/<file>`).
   An intermediate pack without a final record stays allowed (the tree may only have grown since); a tree that is **older** than the return stops the
   runner with the return untouched.

**Checker.** `check_return` adds every `tree_problems` reason (:2823, wired at :3010) to the ladder violations →
`LADDER_VIOLATION`, with the token the runner prints. The existing-return comparison is runner-only (the checker receives one return).

**Writers.** End records are completed in a temporary file and then moved into place: `attempt.json` and `WAVECAR.info` now use `*.part` + `mv`
(:1057 · :1062 · :1068); a failed write or move stops the runner with exit 8 right there (no end record, no next stage) and the leftover `*.part` stops the next
start at the gate. `final.json`, `start_point.json`, `w0_check.json`, `killed.json` and `infra_abort.json` were already written this way; `status.tsv` is
append-only and a cut append is caught by the final-newline rule.

**Same rules on both sides.** The runner functions are cut verbatim from the generated script into the selftest harness and compared with the checker
on the same inputs: tree tokens (34 probes with one problem each — runner first token = checker first token = expected token), the ledger
harness (28 return variants), `rec5` = `rec_parse` (32), `start_id` = `start_problem` (12), `u8ok` = `_u8` (18), `nbj` = `_blank` (18), `nbw` (12),
`row_scan` = `row_gate` (44 OSZICAR probes × 3 stages).

**One gate, one mutation.** Switching the runner gate off (m141 — `tree_gate` returns at once) turns **44 of the 266** selftest checks red;
switching the checker gate off (m169 — `tree_problems` not consulted) turns **21** red. Every EQ scenario that concerns that side is in its set.

## 4. Your findings one by one

Each block: **fix** · **your scenario → now** (selftest case, fake VASP; "was" = the EQ package, reproduced red first) · **mutants** that must turn the
selftest red · **still not caught**.

### Q-EQ-1 · electronic rows (P0)

- **Fix — leading blanks.** The unterminated tail is read after stripping leading blanks and tabs; a 1–4 letter fragment is damage (`incomplete_row`)
  unless it is a blank-led `N` (the column-title line cut short → 0 steps). We did not limit it to prefixes of the stage's allowed headers: any short
  letter fragment with 0 complete rows stops for review. Runner :633 = checker :217.
- **Fix — finite numbers.** Every field of a complete row is at most 24 characters (`ROW_TOK_MAX` :171, `_complete_row` :175;
  runner :630); with the two-digit exponent this bounds |x| below 1e119, so a readable row is always finite. Real 5.4.4 fields are ≤ 16 characters.
- **Your scenario → now.** c2 ends in `  SDA`: was `--infra-abort` 0 · re-run 0 · OK · `a5_c2` → now **`--infra-abort` 2 (nothing preserved) · re-run
  exit 8 · STOPPED_FOR_REVIEW · not adopted** (`eq_sda2`). c2's only row with a 310-digit energy: was RUN_FAILED · c1 secondary adopted → now **exit 8 · `incomplete_row` ·
  nothing adopted** (`eq_310`). Pure cases: `  SDA`, tab + `DA`, a foreign `  DAV` → damage; blank-led `N` → 0 steps; `N` at column 1 → damage; one complete
  row then a fragment → the normal cut; 25-character energy / ncg → damage; 24 characters → accepted.
- **Mutants.** m164 m165 m166 (runner: field length · leading blanks · column-title exception) · m183 m184 m185 (checker: the same) · m85 m114 m115 m130
  m131 kept on their lines.
- **Still not caught.** SDA/CGA field counts come from real DAV rows (we hold no real 5.4.4 c2 output) — a different layout stops for review, never adopts.

### Q-EQ-2 · a foreign `killed.json` and the 180 h cap (P0)

- **Fix.** §3 item 2: `attempt.json` + `killed.json` in one folder → `end_and_killed`; a lone `killed.json` must name its folder's `attempt.start` run_id
  (`killed_run_id`) and pass the record checks before its wall time is read — on both sides, at every entry point.
- **Your scenario → now.** c1's end record at 648,001 s — control, nothing copied: exit 5, c2 not launched (`eq_kc0`). A 0-s `killed.json` issued for
  another run_id copied into that finished c1: was exit 0 · checker OK · collector `a5_c2` → now **gate exit 8 (`end_and_killed`) · c2 not launched ·
  tree unchanged · checker LADDER_VIOLATION** (`eq_kc1`). A lone `killed.json` naming another run_id in an interrupted folder → `killed_run_id`, exit 8
  (tree-token probe `k_rid`; EN P1 runner case).
- **Mutants.** m147 m148 m168 (runner: coexistence · in `run_aborted/` · record form) · m58–m62 re-targeted to `killed_rec5` · m173 m174 m179 m180
  (checker) · m75 m78 re-targeted.
- **Still not caught.** The wall seconds typed into `--killed` are the operator's figure (the scheduler's own record is not in the return).

### Q-EQ-3 · partial restore and history (P1)

- **Fix.** §3 item 6 (existing return) and item 3 (`status_empty`).
- **Your scenario → now.** Completed ladder, `run/` restored to the checkpoint right after A5, the valid `a5_return.tgz` with completed c1 · c2 next to
  it: was c1 · c2 re-run with new IDs, tgz overwritten, new return OK → now **exit 8 (`tgz_final_differs`) · tree and tgz byte-identical** (`eq_restore`).
  Each rule alone: only `final.json` removed → `tgz_final_differs` (`eq_finlost`); intermediate pack holding an interrupted c1, then the c1 folder deleted →
  `tgz_attempt_missing` (`eq_mr`); intermediate pack after c1 finished, then c1's end record and history row removed (an earlier checkpoint) →
  `tgz_end_differs` (`eq_ed`). Positive: an intermediate pack followed by a normal resume still ends OK (`eq_mid`). A 0-byte `status.tsv`: was c1 · c2
  launched → now **exit 8 before any launch** (`eq_st0`); a header-only file is accepted.
- **Mutants.** m153 m154 m155 m156 (runner: comparison · final record · attempts · end-record bytes) · m150 (runner) · m176 (checker).
- **Still not caught.** A restore when no earlier return exists, with the history rows removed consistently (out of scope, as at EQ).

### Q-EQ-4 · end records and repack (P1)

- **Fix.** Template grammar for `attempt.json` (§3 item 2), atomic writers (§3 "Writers"), names and seals at every entry point (§3 items 1–2), final-record
  pairs (§3 item 4) — repack and reuse go through the same gate.
- **Your scenario → now.** A5 `attempt.json` without its last `}`, or with `t_start` `.5`: was c1 · c2 launched, exit 0 → now **exit 8 (`att_form`) · c1 not
  launched** (`eq_trunc` brace · dot5). Write failure (a `mv` that fails like a full disk): **exit 8 right there · no end record · c1 not launched · next
  start exit 8 on the leftover `attempt.json.part`** (`eq_mvfail`). Finished ladder with `infra_abort.json.part` in c1 · with c1's end run_id changed ·
  with `final.json` `code 0` + `REVIEW`: was `PACK_ONLY` 0 · re-run 0 · return OK → now **`PACK_ONLY` exit 8 · re-run exit 8 · tree unchanged · checker
  LADDER_VIOLATION** (`eq_pack` part · eid · code0rev). Also a finished attempt's `OUTCAR` changed after its end record → `seal_OUTCAR`, exit 8 (`eq_seal`),
  and unknown files (`core.1`) or leftovers in any folder → exit 8 at the next launch, at the final pack, at restart and at a recording command
  (`eq_junkA5` · `eq_junkc1` · `eq_entry` · `eq_recgate`).
- **Mutants.** m141–m146 m157 m158 m161 m162 m163 m167 (runner) · m25 m127 m128 re-targeted (restart · `PACK_ONLY` gate lines) · m151 (runner pairs) · m129 m110 (final-record attempts — runner `fin_ok`,
  checker `final_problem`) ·
  m169–m172 m177 m181 m182 m186 m187 m188 (checker).
- **Still not caught.** Atomicity is tested by injecting a failing `mv`; a node crash between two records (e.g. after `attempt.json`, before its
  `status.tsv` row) is the one-way history gap you confirmed at EQ (resumes normally).

### Q-EQ-5 · required fields · UTF-8 · ledger order (conditional, P1 / P2)

- **Fix — blanks.** A required field (scheduler ID · cancel time · reason) must contain a character other than the six blank characters space, tab, LF,
  VT, FF and CR — when written (`nbw` :391, both recording commands :804 · :871) and when read (`nbj` :392 = `_blank` :2668, on the raw
  JSON text after removing spaces and the escapes `\t \n \r \f \u0009–\u000d  `). Anything the runner accepts at write is accepted at read.
- **Fix — UTF-8 when consumed.** Every record the gate reads (`attempt.start`, `attempt.json`, `killed.json`, `infra_abort.json`, `infra_aborts.tsv`,
  `status.tsv`, `final.json`, `start_point.json`, `w0_check.json`) must be valid UTF-8 (`u8in` :393 = `_u8` :2656).
- **Fix — P2.** Ledger rows in stage order A5 ≤ c1 ≤ c2 (`ledger_row_<i>_rung_order`, runner :318 = checker :2578), separate from the time order.
  The README / jobs.json text no longer says the time check implies the stage order.
- **Your scenario → now.** Scheduler ID of three blanks: was a receipt issued and the next stage adopted → now **`--killed` 2 · `--infra-abort` 2 · nothing
  written** (`eq_blank`); VT/FF-only cancel time or reason → exit 2 as well. A receipt or killed record whose required field holds only blank escapes
  (`\t\r\n\u000b\f `, `\u0009\u000A `) → **exit 8 / LADDER_VIOLATION**; `\u001c` or an escaped backslash + `t` are not blank (both sides). A receipt's
  reason byte changed to 0xE9 after saving: was re-run and adopted → now **exit 8 (`run_aborted/…:utf8_infra_abort.json`) · checker LADDER_VIOLATION**
  (`eq_byte`). Same-second swap c1#1 → A5#2: was exit 0 · OK → now **exit 8 · checker LADDER_VIOLATION**; the unswapped twin still ends OK (`eq_ss` ·
  `eq_ss_ok`).
- **Mutants.** m159 m160 m191 (runner write) · m123 m124 m189 (runner read) · m138 m139 m180 m190 (checker) · m149 m175 (UTF-8) · m152 m178 (stage order) · m118 m134 (time order, EP P2 — now
  tested with two same-stage rows so the stage-order rule cannot shadow it).
- **Still not caught.** Blank means those six ASCII characters only (a field of Unicode spaces such as U+3000 is accepted on both sides). The order check
  trusts the node's `date +%s`.

## 5. Tests

- Selftests: a5 **266/266** (20 checks red on the EQ package before the fixes, 237/257; 262 when the gate first went green; + the blank-character
  checks; + the tests split off for the first-pass survivors, below) · V5 **313/313** (unchanged
  file) · round2 **194/194** (unchanged file) — python 3.11 · `dftd3` 1.6.0 venv, all re-run on the `c14d52abb` tree. The a5 selftest also passes with
  **gawk 5.2.1** as `awk` and under `LC_ALL=C.UTF-8` (default awk = mawk 1.3.4).
- Existing tests adjusted because the gate now stops first: runner exits for broken records are **8** with no final record and no repack (was 2 or a final
  record 8); checker labels for those trees are **LADDER_VIOLATION** (was START_POINT_MISMATCH · KILLED_RECORD_MISMATCH · STOPPED_FOR_REVIEW in some
  variants); fixtures that built inconsistent trees by accident were made consistent (final-record attempts, `attempt.start` in a moved folder, written
  times in killed records); the EO P2 same-second foreign return now stops at `tgz_final_differs`.
- Mutants (`build_a5_vasp_package.py --mutants`): **191** — first full pass (191 mutants, fail-fast, `--jobs 4`, 109 min) on tool `ab1bd5aa87514eb6…`: 186 red. Five survived — m110 m118 m129 m134 m176 — each shadowed by a newer check (the gate's own final-record comparison, the existing-return comparison, the new stage-order rule, the checker's header rule). We split their tests (two same-stage ledger rows with reversed times; final-record attempts with no existing return; the checker's `status_empty` token) and moved m110 onto `final_problem` (the older comparison in `check_return` now sits behind the gate). No runner or checker logic changed (one checker message gained the `ledger_time_order` token). The five re-run on the final tool `edd9666cd1ade0e6…`: 5/5 red; the selftest only got stricter, so the other 186 stay red. The 191 = the 140 earlier ones (28 re-targeted to the changed lines) + 51 new (m141–m191), at least one per gate entry point and per rule on each side.
- EN / EO / EP reproductions and positive controls still pass (selftest).
- EM probes p1–p9 (12 files incl. p3b, p7b, p7c) re-run on the EQ-reviewed tool and on the new tool, compared after normalising times, hashes and run ids:
  **9 identical** (p1, p2, p4 and p9 end in the same `FileNotFoundError` in both versions — the probe scripts expect a file the runner does not create on that branch; their verdict lines are identical). p7 and p7b gain one more violation — the tree gate's `no_start`: these probes leave a stage folder holding inputs but no `attempt.start`, a state the runner never produces (it writes `attempt.start` in the prep folder before the atomic rename) — and keep the label LADDER_VIOLATION; p7c changes LADDER_INCOMPLETE → **LADDER_VIOLATION** for the same reason. No adoption in any version. (New-side probes ran on tool `ab1bd5aa…`, whose runner and checker logic is that of the final tool.)
- Collector regression: re-running the recorded G5 command (V5 return unpacked in scratch) on the `c14d52abb` tree gives rc 3, the same JSON `afecfa08…`
  and the same console output, byte for byte.

## 6. Please look especially at

1. **False stops.** A `VASP_CMD` wrapper that leaves non-standard files in an attempt folder (core dumps, MPI logs) now stops the runner (exit 8, contact).
   So does a crash in the instant between the two final `mv`s of a pack (new tgz, old `.sha256`). We prefer that to a silent pass. Is the allow list
   (return allow / forbid lists + standard VASP outputs) right for a 5.4.4 node?
2. **Existing return.** Compared only by the runner (the checker gets one return). An intermediate pack is allowed to be older than the tree; a final one
   must match it byte for byte. Agree?
3. **Exit codes.** Everything the gate finds is exit 8 with no write; refusals of typed fields in a recording command stay exit 2 (nothing written).
4. **What still cannot be caught** (per §1b): a return in which ledger, receipts, history, attempt folders and the final record were all edited consistently;
   the wall seconds typed into `--killed`; the node clock.

## 7. Questions

- **Q-ER-1** (structure): one gate at every runner entry point, the same rules and tokens in the checker — does it close the pattern "runner keeps going,
  checker rejects later" for the records in scope? Any entry point we missed?
- **Q-ER-2** (Q-EQ-1): leading-blank fragments and the field-length bound — closed?
- **Q-ER-3** (Q-EQ-2): a copied `killed.json` can no longer lift the cap — closed?
- **Q-ER-4** (Q-EQ-3): restore against an existing return, 0-byte history — closed?
- **Q-ER-5** (Q-EQ-4): truncated end records, atomic writes, repack and reuse through the gate — closed?
- **Q-ER-6** (Q-EQ-5 + P2): blank fields (write and read), UTF-8 when consumed, ledger stage order — closed? Any new hole introduced by the gate?
- **Q-ER-7**: Send approval — may package MANIFEST `8e295baea495de906bddb172f14e30a1fe2d58cd93775ddee783c95c0ce0db5d` go to the operator?

## 8. How to reproduce

- `python3 -I tools/wad/build_a5_vasp_package.py --selftest` · `… --mutants --jobs 2` (or `--mutants m141 m169 …`; run it with a python that has `dftd3` so
  the V5 mutants are judged by the V5 selftest, not by an import error) · `python3 -I tools/wad/build_v5_vasp_package.py --selftest` (needs `dftd3` 1.6.0).
- `python3 -I tools/wad/build_a5_vasp_package.py --build --out <new folder>` → `diff -r` with `db/inputs/wad_a5_vasp_2026_11_20` · MANIFEST sha.
- Set `A5_SELFTEST_FAILFAST=1` to stop the selftest at the first red check (the mutant runner sets it).

## 9. Reply format

Per question: verdict (GO / conditional / NO-GO) · evidence (file:line or test) · minimal fix if not GO · for every new finding, **in scope** (blocking) or
**out of scope** (note) per §1b. Please do not print W values.
