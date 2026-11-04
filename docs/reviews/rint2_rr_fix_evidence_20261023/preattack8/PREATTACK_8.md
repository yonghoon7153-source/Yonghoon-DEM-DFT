# Pre-attack round 8 — independent review of `80095a7f0..7b51e591e` (PC7-01..05 fixes · BAN8 · RINT2-E01 · E18)

Reviewer: independent agent, 2026-11-04. Scope = `git diff 80095a7f0 7b51e591e -- scripts/rint_r_chain.py scripts/carbon_junction.py
scripts/test_rint_r_chain.py scripts/test_rint_r_chain_e2e.py scripts/test_carbon_junction.py`. Tracked files were not modified; nothing was
committed or pushed. I wrote my own findings (`notes_before_pc7.md`) before opening `preattack7/PREATTACK_7.md`; I did not open
`pc7_fix/`, `ban8_20261103/`, `e2e_verdict_20261103/` or `codex_rint2_rr_round2_request_20261103.md`.

Environment: the worktree I was given was empty (commit `bf0dd1a32 Initial commit`), so I built a sparse checkout of `7b51e591e` in the
scratchpad (`git init` + objects/info/alternates → the shared object store · `update-ref HEAD 7b51e591e` · sparse paths = `scripts/ webapp/
config/ tools/ pipeline/ .github/ .gitignore` + the five docs the tests read + `docs/data/w4b_ptfe_off_20260827/`). Commands below use
`TREE=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/preattack8/tree` and
`PROBES=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/preattack8/probes`.
Python 3.11.15 (numpy 2.4.6 · scipy 1.17.1) and Python 3.8.20 (numpy 1.24.4 · scipy 1.10.1, the uv interpreter `setup_kgy_py38.sh` installs).
The machine was shared with other agents (load average 6–7 on 4 cores) — timings are slow but no test failed for timing reasons.

**Result: P1 candidate 1 · P2 2 · P3 6.** PC7-01, 03, 05 are closed in the form round 7 described; PC7-02 and PC7-04 are closed only in the
narrow form that was tested — the same class survives one step away (P8-01, P8-02). The P1 candidate (P8-05) is not introduced by this diff,
but it is the PC7-01 class (a second actor closes an attempt that is still alive) on the `--stage recover` side, and the new start record is
where the missing information would go. On its own the verdict still stops (folder sha); with one more hand — deleting the files the live
chain produced — the verdict ledger check passes and the attempt that ran to CALIBRATED is counted as pre-result (P8-05d).

## 1. Findings

Line numbers are at `7b51e591e`.

| ID | Sev | File:line | Counterexample | Reproduction | Expected vs actual |
|---|---|---|---|---|---|
| **P8-05** | **P1 (candidate · main reviewer decides)** · PC7-01 class · window pre-dates this diff | `rint_r_chain.py` `recover_ledger` :6822–6838 (writes the result line as soon as no group record is unconfirmed) · `stage_recover` :6759 (only missing/unconfirmed end records reach `recover_group`, the only place that calls `chain_parent_alive`) · start record :3467 (holds base · host, no chain pid) · `attempt_presolve_problem` :3520–3529 (a new, non-resume attempt does not re-count earlier attempts' folders) | Operator runs `--stage recover --out <attempt> --ledger <L>` while the chain is alive but has no unconfirmed group: **(a)** after the start record, before the first runner launch (presolve · S0 checks · bed re-hash); **(b)** between two runs (run 1 end record confirmed, run 2 not launched) | (a) `python3 -I $PROBES/probe_p805_recover_live_nogroup.py $TREE` (presolve wrapped with a 20 s sleep) · (b) `python3 -I $PROBES/probe_p805b_recover_live_between_runs.py $TREE` (first `read_run` wrapped with a 15 s sleep) · follow-ups `probe_p805c_then_verdict.py` · `probe_p805d_pre_then_cut.py` | Expected: recover refuses a live chain, as `recover_group` does (PC5-03 "사슬 부모가 살아 있으면 건드리지 않는다"). Actual (a): chain alive · attempt folder = `attempt.json` only · recover **rc 0** · result line `interrupted · pre · parent_dead · resume_ok False` · the live chain then runs **14** runner calls to **CALIBRATED** (folder side now `post`) and its own result line is refused (chain rc 3) · `--add` for the same target **rc 0**. Actual (b): recover **rc 0** · `interrupted · post · parent_dead · resume_ok True` · `--add --resume 1` **rc 0** while the original chain is alive (it finishes CALIBRATED, 14 calls, rc 3). Downstream: (b)+resume → the resume attempt is refused (rc 3) and the verdict stops `attempt_1: 폴더 요약 sha ≠ 원장 결과 줄 1` (P8-05c). (a)+new attempt 2 → attempt 2 runs **CALIBRATED**; verdict stops on attempt 1's sha; after deleting the files the live chain produced (keep `attempt.json`, one hand) the verdict ledger check **passes** (INPUT_MISSING) with `ladder:P0` adopted = 2, attempts [1, 2] — attempt 1, which ran to CALIBRATED, is counted as a pre-result interruption and skipped (P8-05d). Without the cut, the verdict is protected; the premature line is what makes the cut consistent. |
| **P8-01** | **P2** · PC7-02 class | `rint_r_chain.py` `found_attempts_problem` :3910 (AL07 exception = result line `rejected` **and** any file named `attempt_<k>.rejected.json` in that base — the result line's `folder`, the side file's digest and its content are not checked) | PE02's own threat model (ledger clone reset before entry 1 · entry 1 re-appended with target `ladder:P0:FIBRE`) but result line 1 re-appended as a form-valid **rejected** line (folder `attempt_1.rejected.json` or `attempt_1`, any sha) · `attempt_1/attempt.json` deleted (same one hand as PE02) · `echo '{}' > attempt_1.rejected.json` next to the folder | `python3 -I $PROBES/probe_p801_al07_exception.py $TREE` | Expected: ATTEMPT_LEDGER_MISMATCH (attempt_1 still holds a post-result run: stopped · side post). Actual: control (`as_is` = PE02 shape) = ATTEMPT_LEDGER_MISMATCH; `rej_side` and `rej_infolder` = verdict ledger check **passes** (stop INPUT_MISSING, the same code PE02x uses for "ledger check passed") · predict input check passes · predict runs **24** runner calls · PREDICTED. For a non-input target nothing else re-reads that result line (the PC5-01 recount and the folder/sha checks run only in `target_ledger_problem` for input targets), so the exception sits exactly where no other check looks. |
| **P8-02** | **P2** · PC7-04 class | `attempt_groups_problem` :3641 (`confirmed is True` only) · `orphan_cause` :3767–3803 (never compares end-record token/name with the launch record) · `stage_recover` :6759 (confirmed end records skip `recover_group`, so the new PC7-04 check :6665–6670 never runs) · `ResumeRunner._src_done` :4336–4344 (same missing binding — by code reading; the resume attempt itself was not run) | Ladder attempt, chain parent SIGKILL after the mark (runner group alive · PE01 shape) → `groups/L01_floor.end.json` replaced by another completed attempt's end record (by chain · rc 0 · **confirmed True** · its own token) — the "partial copy" PC7-04 names | `python3 -I $PROBES/probe_p802_foreign_confirmed_end.py $TREE` | Expected: same as the control (end token ≠ launch token → group unconfirmed · rc 3 · no result line). Actual: control (same record, `confirmed False`) = rc 3 · no result line · group killed (PC7-04 works). Foreign confirmed = `attempt_groups_problem` None · `orphan_cause` (`parent_dead`, True) · recover **rc 0** ("그룹 기록 0 개 정리 · 미확인 0") · result line `interrupted · post · parent_dead · resume_ok True` · **runner group still alive after recover** · `--add --resume 1` **rc 0**. |
| P8-03 | P3 · RINT2-E01 | `byte_diff_view` :6461 (`v0 != v1` = Python equality) · `reverify_report` :6510–6519 (`results_differ` · `results_keys_differ` · `grade_differ` · `public_keys_differ` same equality) | Stored JSON value changes JSON type: number ↔ boolean (`true` vs `1`, `true` vs `1.0`) · duplicated key whose first copy differs (`"b": 999, "b": 1`) | `python3 -I $PROBES/probe_p803_byte_diff.py $TREE` · real path: `python3 -I $PROBES/probe_p803b_reverify_type.py $TREE` | Expected (docstring: "value = 파싱한 값이 다름"): `value`, and the changed key in `results_keys_differ` / `grade_differ True`. Actual: `kinds ['format']` for all three type changes and for the duplicate key. Real path: results JSON `in_E` false→0 → REVERIFY_DIFF (correct) but `results_differ False · results_keys_differ [] · results_bytes ['format']`; verdict JSON `sentence_allowed` false→0 → `grade_differ False · public_keys_differ [] · public_bytes ['format']`. Verdict behaviour is right (byte compare); the report says "only serialisation form" for a value whose JSON type changed. |
| P8-04 | P3 · RINT2-E01 | `byte_diff_view` :6461–6463 (`value` returns at once) · test E18i (`test_rint_r_chain_e2e.py` :1700 writes with `json.dump` · :1710 asserts `['value']`) | Value change together with another byte difference | `python3 -I $PROBES/probe_p803_byte_diff.py $TREE` (rows `value_and_no_nl`, `value_order_crlf`) | Docstring: kinds "BYTE_DIFF_KINDS 차례 · 여럿 가능". Actual: `['value']` only for value + missing final newline and for value + key order + CRLF. E18i writes the mutated file with `json.dump` (no final newline) and asserts exactly `['value']` — the test pins the incomplete list. Either document "value hides the other kinds" or keep collecting. |
| P8-06 | P3 · test gap | RV05/RV06 vs `byte_diff_view` :6486 · BAN8 vs `carbon_junction._divide_runs_idx` :1620 | Mutant M26 (drop `canon_bytes(v0) != new` → format) and B01 (port at `(j+0.25)` instead of the part centre) | `python3 -I $PROBES/mutate8.py /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/preattack8/mut_tree /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/preattack8/logs/m26_b01.json M26,B01` (mut_tree = plain copy of `$TREE` without `.git`) | M26 survives RV05/RV06 (the "no kind → format" fallback hides it unless another kind co-occurs; no case has number-form + another kind). B01 survives BAN8 (27/27) because part centres sit at x.7 inside cells and a quarter shift picks the same port cell; the full carbon-junction suite catches B01 with 8 other checks (KINK U ×2 · RCA05 CX ×2 · RCA05 (다) · SIDE · NEAR · MUT-RCA; 481/491 vs base 489/491 on the non-git copy, where C0 · LEN-BIT fail for lack of git history). |
| P8-07 | P3 · wording | `carbon_junction.py` :145 (`CJUNC_QUALIFIERS` "전달 길이 = 해석 시험 통과 (분산판 = 전송선 · 식 검증)") | BAN8 covers one geometry: two identical, axis-aligned, single-voxel rails in adjacent cells (R̄sh2 = 1), L_c an exact multiple of L_par. Eq. 8 with R̄sh2 ≠ 1 (e.g. a staircase / tilted fibre with larger r′) is checked only between the module-external hand ladder and the formula (BAN8 ①), never through production | reading `test_carbon_junction.py` :2287–2445 | Narrow the qualifier to "identical straight parallel rails" or add one production case with R̄sh2 ≠ 1. Note: the qualifier is part of the evidence contract (`ca_ext_cjunc.py` :466 compares it exactly) — any arm produced before this text change now fails the contract (intended re-pin, worth one line in the request). |
| P8-08 | P3 · seal wording | `byte_diff_view` :6452–6454 · report keys `first_diff_offset` · `len_delta` | Two results JSONs that differ only in a sealed σ | `python3 -I $PROBES/probe_p808_offset.py $TREE` | "값 · 글 없음 (봉인)" holds for values and text, but the offset is a function of the sealed bytes: σ 1.2345678 vs 1.2345679 → offset shows **8** agreeing leading characters, vs 1.2399999 → **4**, vs 9.9 → **0**. Low impact (reverify runs after the verdict), but the seal claim should say "offsets are derived from sealed bytes". E18k's leak check (`\d\.\d{6,}` tokens) cannot see this by design. |
| P8-09 | P3 · robustness · pre-existing | `byte_diff_view` :6456 · `reverify_report` :6506–6508 · `reverify` :6590–6594 (except lists = OSError · UnicodeDecodeError · ValueError) | Stored JSON nested 200 000 deep | `python3 -I $PROBES/probe_p803_byte_diff.py $TREE` (row `deep_nesting`) | Measured: `RecursionError` escapes `byte_diff_view`. By code reading: the older `r0` parse in `reverify_report` and the `pub0` parse in `reverify` have the same except list, so reverify ends in a traceback instead of a REVERIFY_DIFF report (exit status 1 either way, so no false SAME). |

Severity notes. P8-01 and P8-02 need a deliberate hand (ledger rewrite as in PE02; a copied end record as PC7-04 names) — rated P2 on the
round-7 scale ("시도 폴더 쓰기 권한 = 운영 규칙"). P8-05 needs only an operator mistake that PC5-03 claims to guard against (recover while
the chain is alive); it changes an R-run decision by itself (next attempt or resume accepted while the original runs) and ends in a
passing verdict after one more hand, hence the P1 candidate.

Not findings (checked):
- `_start_problem` / `ledger_parse` start rows (`python3 -I $PROBES/probe_start_parse.py $TREE`, same answers under 3.11 and 3.8): duplicate key · NaN · Infinity · non-canonical spacing · string / float / 10³⁰ `n` · NUL in base · CRLF line · BOM · NBSP or Arabic-Indic digit in the folder name — all refused; bool `n`, relative / empty base, host type, folder of another `n` — refused (PE01p; mutants M03–M07 killed). Accepted: a non-normalised absolute base (`/srv/x/../runs`, `/srv/runs/`) — the chain never writes one (`resolve()`), and recover then always refuses (`s0['base'] != fb`), i.e. a hand-edited row blocks the attempt instead of opening it. Start records do not change adoption · limit · order · next number (PE01p "same" rows).
- PC7-01 second entrance: same `--out` after `rm -rf attempt_1` → rc 3 · 0 runner calls · ledger unchanged; different `--out` → rc 3 (closure probe A).
- `CHAIN_END_FIXED`: both paths give `chain_exception · resume_ok False`, also when the log has an OOM word (closure probe B).
- `recover_group` with an *unconfirmed* foreign end record → no end written · file bytes unchanged (closure probe D).
- Python 3.8: the new code uses nothing newer than 3.8 (all three suites pass under 3.8.20, §4).

## 2. Guarantees claimed by the change

| Guarantee (where) | Counterexample tried | Result |
|---|---|---|
| Start record before the runner; a second entrance for the same `n` without a result line = screen only, "regardless of base and machine" (`START_KEYS` comment :2758, `attempt_open` docstring :3399–3403, registration ⑦ PC7-01) | same `--out` after deleting the folder · different `--out` · other host identity (PE01h) · **stale clone of the ledger made before the start record** | **Narrower.** Holds when every entrance uses the same ledger repository (closure probe A: rc 3 · 0 calls). A stale clone has no start record → rc 0 · 14 runner calls · CALIBRATED in the clone (Q-D "shadow run" — the guard is per ledger repo, not per campaign). |
| `ledger_parse`: start after its entry · one per number · results after the start · exact fields; result lines without a start still accepted; starts not counted (:3026–3029) | NaN · dup keys · bool n · relative/empty/NUL base · host str/number/missing key · start after result · twice · extra key · `start_after_other_entry` | **Held** (PE01p · `probe_start_parse.py`; M03–M07 killed). |
| "못 쓰면 러너 없이 rc 3 · 폴더 = attempt.json 만 · recover 뒤 다음 시도" (:3402–3403) | start append fails | **Held** (PE01f; M10 killed). |
| recover: result line present but folder name / sha differ, or start base ≠ this folder's base → rc 3, ledger unchanged (:6786–6788) | copied folder in another base · edited file in the original base · symlinked base | **Held** (PE01 · PE01c · PE01s; M08 · M09 · M11 killed). |
| Result line only after group exit is confirmed (Codex ② · `attempt_groups_problem`, `stage_recover`, PC5-03 "live chain = untouched") | live chain before the first launch · live chain between runs · foreign confirmed end record | **Broken** (P8-05 a · b, P8-02). Downstream: resume refused + verdict stops on folder sha (P8-05c); folder cut-back → verdict passes (P8-05d). |
| "막는 것: 멈춘 시도 폴더 지우기" (Q9 design §3-5, ledger purpose) | P8-05 (a) premature `pre` line + delete the produced files | **Broken in combination** (P8-05d). Alone, deleting files from a correctly closed attempt is still caught (folder sha). |
| `found_attempts_problem`: every found `attempt_<n>` with a ledger entry needs a well-formed attempt.json; one exception = result rejected + side record (:3893–3899) | delete / extra key / symlink (PE02) · forged rejected result line + touched side file | **Narrower.** The literal rule holds; the exception is not bound to evidence and opens the hole the rule was meant to close (P8-01). |
| `CHAIN_END_FIXED`: chain end-record table shared by the by-chain and by-recover paths (:3696–3702) | recover chain_end exception (± OOM log) · by-chain exception unconfirmed | **Held** (closure probe B; PE03 · PE03u; M15 · M16 killed). |
| PC7-04: chain_end carried only when the old end record's token and name match the launch record, else unconfirmed (:6646–6648) | other token (chain · recover) · other name · same (PE04) · **confirmed** foreign record | **Narrower.** Holds for missing/unconfirmed old records (the only ones `recover_group` sees); a confirmed foreign record bypasses it (P8-02). |
| PC7-05 wording: summary-less path cannot tell the cleanup signal → runner_rc (registration ⑦) | chain end cause None · rc 1 · unconfirmed → recover; summary path GROUP_UNCONFIRMED rc None | **Held** (closure probe C: `runner_rc` vs `group_unconfirmed`). |
| Reverify verdict = byte compare, unchanged; report v2 only adds reasons (:6397–6399, `byte_diff_view` docstring) | E18c–E18k · RV06 · M29 | **Held** (byte compare computed before the report; M29 killed). |
| Byte reasons: closed list, order, offsets and length delta exact, several kinds possible, no values (:6401–6404, :6444–6446) | CRLF · trailing space · key order · indent · escapes · 1↔1.0 · bool↔number · dup key · BOM · NaN · value+newline · deep nesting | **Narrower.** Offsets/lengths exact (RV05); bool↔number and dup key → `format` (P8-03); `value` hides the others (P8-04); offsets derived from sealed bytes (P8-08); RecursionError (P8-09). |
| BAN8: production distributed plate = discrete transmission line (1e-11) and matches Banerjee Eq. 8 within the leading discretisation error × 1.5; 2nd order; saturation; naive rejected; lumped mutation fails all six (:2287–2445) | B01 · B02 · B03 · built-in ⑧ | **Held for the tested geometry** (B02 · B03 killed; ③ is an exact pin). Port placement within a cell is not pinned by BAN8 (B01 equivalent there). |
| Qualifier "전달 길이 = 해석 시험 통과" (`carbon_junction.py` :145) | scope reading | **Narrower** (P8-07). |
| E18: real producer → verdict → reverify SAME (same / separate process) · one input changed → refused or REVERIFY_DIFF · revert → SAME · seal | E01 · E02 (see §3) | **Held** (51/51 under 3.11). |

## 3. Mutations (scratch copy `mut_tree`, one at a time, original bytes restored after each; tool `$PROBES/mutate8.py`)

Baseline on the unmutated copy: `--only PE01,PE02,PD12u,PE02x,PE03,PE04,PD13g,RV05,RV06` = 16/16 PASS; BAN8 = 27/27 PASS.

| Test | Mutation | Result |
|---|---|---|
| PE01 · PE01h · PE01r | M01 `attempt_open` ignores `st['starts']` | killed (PE01 · PE01h · PE01r) |
| PE01 · PE01f · PE01s | M02 start record not appended | killed (PE01 · PE01f · PE01h · PE01r · PE01s) |
| PE01p | M03 two starts accepted · M04 start after result accepted · M05 relative base accepted · M06 host check removed · M07 folder check removed | all killed (PE01p) |
| PE01 | M08 recover base check removed | killed (PE01) |
| PE01 · PE01c | M09 recover result-line folder/sha check removed | killed (PE01 · PE01c) |
| PE01f | M10 start-append failure → continue | killed (PE01f) |
| PE01s | M11 start base `absolute()` instead of `resolve()` | killed (PE01s) |
| PE02 · PD12u · PE02x | M12 `found_attempts_problem` back to `continue` | killed (PD12u · PE02 · PE02x) |
| PD12u · PE02x | M13 exception without the side-file condition | killed (PD12u · PE02x) |
| PD12u | M14 exception without the `rejected` condition | killed (PD12u) |
| PE03 · PE03u | M15 recover path ignores `chain_end_fixed` · M16 table maps exception → parent_dead | killed (PE03 · PE03u) both |
| PE04 | M17 token/name compare removed · M18 name compare removed · M19 still writes the end record | killed (PE04) all three |
| RV05 · RV06 | M20 no key_order · M21 no CR handling · M30 no newline-count check | killed (RV05 · RV06) |
| RV05 | M22 offset +1 · M25 whitespace/format swapped · M27 value → format · M28 no tail trailing-whitespace | killed (RV05) |
| RV06 | M23 `public_bytes` None · M24 no screen line · M29 `same` = verdict bytes only | killed (RV06) |
| RV05 | **M26** canon-format check removed | **survived** (P8-06) |
| BAN8 | **B01** port at `(j+0.25)` of each part | **survived BAN8** · killed by the full carbon-junction suite (KINK U …) |
| BAN8 | B02 `k = ceil + 1` · B03 length law `r → r**0.9` | killed (BAN8) both |
| E18 | E01 `same` = verdict bytes only · E02 no tail trailing-whitespace | E01_RESULT · E02_RESULT |

## 4. Test pass counts (my runs, sparse checkout of `7b51e591e`, `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`)

| Suite | Python 3.11.15 | Python 3.8.20 (numpy 1.24.4 · scipy 1.10.1) |
|---|---|---|
| `python3 scripts/test_rint_r_chain.py` | **442/442 PASS (691.3 s)** | **442/442 PASS (934.0 s)** |
| `python3 scripts/test_rint_r_chain_e2e.py` | **51 PASS · 0 FAIL (1193.1 s)** | PY38_E2E |
| `python3 scripts/test_carbon_junction.py` | **493/493 PASS** | **493/493 PASS** |

3.8 commands: `export PATH=/root/.local/share/uv/python/cpython-3.8.20-linux-x86_64-gnu/bin:$PATH; unset VIRTUAL_ENV;` then the same three
lines (this is what `scripts/check_kgy_py38.sh` does; I did not run the whole 11-suite script). Environment notes: before adding
`docs/data/w4b_ptfe_off_20260827/` to the sparse checkout CAX-SUB failed (cohort manifests missing); before making the tree a git repo C0 and
LEN-BIT failed (`git show <old commit>`) — both are checkout artefacts, not code faults. kgy itself runs 3.8.10, not 3.8.20.

## 5. PC7-01..05

| ID | Verdict | Evidence |
|---|---|---|
| PC7-01 | **Closed for the reported path; same class open on the recover side** | Closure probe A (`probe_pc7_closure.py`): different `--out` → rc 3 · 0 calls; same `--out` after deleting the folder → rc 3; PE01 · PE01h · PE01r pass and are mutation-sensitive (M01 · M02 · M08 · M09). Limits: one ledger repo only (stale clone → rc 0 · CALIBRATED); recover can still close a live attempt when no group is unconfirmed (P8-05 · P8-05d ends in a passing verdict after a folder cut-back). |
| PC7-02 | **Partly** | The one-hand forms (delete · extra key · symlink) are refused (PE02, M12 killed). One more cheap step under the same threat model — re-append result 1 as `rejected` and touch `attempt_1.rejected.json` — passes verdict and predict input (P8-01). The fix proposed in round 7 also asked for `folder = attempt_<n>.rejected.json`; the implementation checks only that some side file exists. |
| PC7-03 | **Closed** | Closure probe B: recover chain_end exception (± OOM log) and by-chain exception both → `chain_exception · resume_ok False`; PE03 · PE03u mutation-sensitive (M15 · M16). |
| PC7-04 | **Partly** | Unconfirmed foreign end record → held, bytes unchanged (closure probe D, PE04, M17–M19). A confirmed foreign end record never reaches the check: result line written with the group alive and a resume accepted (P8-02). |
| PC7-05 | **Closed** (wording) | Registration ⑦ now states the summary-less path → runner_rc; closure probe C confirms (`runner_rc` vs summary path `group_unconfirmed`). |

## 6. Suggested direction (short)

- P8-05: store the chain pid + start ticks in the start record and have `recover_ledger` refuse while that chain is alive (reuse `chain_parent_alive`); same rule when every group is confirmed.
- P8-02: bind every end record to its launch record (token · name) in one helper used by `attempt_groups_problem`, `orphan_cause`, `stage_recover` (todo) and `ResumeRunner._src_done`; mismatch = unconfirmed.
- P8-01: let the AL07 exception require `r['folder'] == attempt_<k>.rejected.json`, `folder_digest(side) == r['folder_sha256']`, a well-formed rejected record (n = k) and a folder with no chain artefacts (no `groups/`, `folder_side == 'pre'`); or drop the exception (AL07 is rare) and ask the operator to move the foreign folder.
- P8-03/04: compare with a type-strict equality (bool vs int vs float) and keep collecting kinds after `value`, or document both.

## 7. Files

Probes: `$PROBES/probe_common.py` · `probe_p801_al07_exception.py` · `probe_p802_foreign_confirmed_end.py` · `probe_p803_byte_diff.py` ·
`probe_p803b_reverify_type.py` · `probe_p805_recover_live_nogroup.py` · `probe_p805b_recover_live_between_runs.py` · `probe_p805c_then_verdict.py` ·
`probe_p805d_pre_then_cut.py` · `probe_pc7_closure.py` (closure probe A–D) · `probe_start_parse.py` · `probe_p808_offset.py` · `mutate8.py`.
Outputs: `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/preattack8/logs/` (`probe_p80*.out`,
`mutants.json`, `mutants.out`, `mutants_e2e.out`, `*_py311.log`, `*_py38.log`). Own pre-read notes: `.../preattack8/notes_before_pc7.md`.
