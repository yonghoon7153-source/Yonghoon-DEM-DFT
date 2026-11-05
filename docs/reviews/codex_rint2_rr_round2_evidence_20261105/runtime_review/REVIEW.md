# Rint② RR round 2 — independent runtime / attempt-ledger review

Review pin: `6917c3c9fa397936d3381ba1c1785562c5232e46`; baseline `9bec6b7646374daed0d3edbb9647f9f46d302750`. Supplied files were read, not edited. The review concerns recovery, first-result markers, attempt adoption, resource classification, and the runtime portions of Q2/Q4/Q5/Q9.

## Evidence and limits

- Independent test `probe_runtime.py`: **311/311 assertions PASS**, with raw output `run.log` and individually named assertions `results.json`.
- Windows 11, CPython 3.12.14, NumPy 2.5.3, SciPy 1.16.3. No production/research inputs, actual hosts, SSH, WSL, GPU, full gate, or numerical campaign were used.
- Tests execute actual `rint_r_chain` / `rint_first_result` functions. Real files and scratch Git repositories exercise recovery commits, second-entry rejection, folder evidence, append rollback, history checking, and verdict ledger checking. Harmless Python subprocesses exercise marker success and immediate failure before returning the stand-in solver value.
- Linux `/proc` identity and process-group effects are explicit fixtures/mocks. `ledger_lock` is replaced by a no-op context **only for sequential Windows Git tests**. A command-local `safe.directory` flag is added to Git calls for scratch repository ownership; global Git configuration is unchanged. Consequently **flock concurrency, actual parent SIGKILL, group killing, Linux permission semantics, and kgy runtime behavior were not independently rerun**. Parent confirmed there is no authorized Linux surface.
- The supplied Linux PASS logs are not counted as independent executions. `report_c_raw/SHA256SUMS` was independently checked: **93/93 listed files present and matching**. This closes source availability, not runtime reproducibility.

## New adjacent defect: malformed success rc enables forbidden recovery resume

Suggested severity **P3** (record-validation gap; normal internal producer does not emit malformed rc). Suggested identifier `RR2-RT01` pending root coordination.

`scripts/rint_r_chain.py:3869` treats `rc == 0` as a successful by-chain run in `orphan_cause`. Python therefore accepts JSON `false` and `0.0`. In contrast, `runner_rc_failed` at 3771–3775 explicitly treats bool and float as malformed failures, and `ResumeRunner._src_done` at 4460–4467 requires integer zero.

Reproduction uses the same token/name-bound confirmed end record, a first-result marker, no stage summary, and a log containing `Traceback` / `KeyError`. Only the end-record `rc` changes:

| End rc | `runner_rc_failed` | Actual recover result | Next `--resume` ordering check |
|---|---|---|---|
| integer 1 | true | `interrupted / post / runner_rc / resume_ok=false` | `RESUME_NOT_ALLOWED` |
| boolean false | true | `interrupted / post / parent_dead / resume_ok=true` | accepted (`None`) |
| float 0.0 | true | `interrupted / post / parent_dead / resume_ok=true` | accepted (`None`) |

`residual_rc.json` records the actual pure/file functions. `residual_rc_integration.json` records actual Git recovery commits and `attempt_order_problem` acceptance, including scratch repo paths. The start record is present; process identity is mocked dead. `attempt_groups_problem` accepts the correctly bound end record in all cases. The discrepancy is unrelated to process-kill effectiveness.

This is a single malformed end-field before the first recovery/result commit, not an edit of all ledger/folder/result copies. No legitimate producer path emitting malformed rc was found. No full numerical rerun or final verdict false-green is claimed. A resumed failed run has no completed payload bytes to compare in this fixture; `_src_done` rejects malformed rc, then the normal remaining-payload rule permits a fresh run with determinism assumed. It does not establish preservation of an immutable numeric answer.

Minimal fix: at 3869 require `type(rc) is int and rc == 0`, matching the other consumers. In-memory application only (submitted source unchanged), `candidate_fix_results.json` confirms bool/float now produce `runner_rc / resume_ok=false`, while legitimate int zero remains unchanged. Add tests for malformed rc on the by-chain summary-less path and the recover→result→resume gate.

## Finding-by-finding assessment

“Closed” below means the original minimum behavioral defect is closed within the stated code/data boundary, not approval of the entire campaign or actual kgy process lifecycle. “Partial—runtime evidence” means the logic passed but an essential native guarantee could not be independently executed here.

| ID | Assessment | Actual function/evidence and boundary |
|---|---|---|
| RCA2-05 | Closed, scoped; campaign still HOLD | Execution policy is a plan field (`exec_policy_problems` 1149, `require_plan_numbers` 1227, `exec_check_or_stop` 1238); runner deadline 4388; attempt order/adoption 3312/3365; second-entry and recovery Git fixtures pass. Numbers must still be registered. Ledger and ordinary-process restrictions do not prevent all-copy forgery or shadow runs. |
| RCA2-07 | Closed | Current comments 4695/4773/4801/4813 state per-extension ≤100 and no total bound. Independent arithmetic reproduces old 82-solve 205.8–248.9 h and all3 220.2–318.8 h from stated historical assumptions. No real ETA or new timing observation. |
| PC5-01 | Closed | `result_line_problem` 3946 recomputes fields; `ledger_history_problem` 2930 rejects hidden ledger commits. Real `merge -s ours` fixture rejected, real Git recovery field/digest checks exercised. End-record malformed rc remains the separate new defect above. |
| PC5-02 | Closed | `words_cause` 3751: address errors first, five resource words next, CUDA errors then failure. Independent 17-log matrix including mixed illegal-address/OOM passes. |
| PC5-03 | Partial—runtime evidence | `chain_parent_alive` 2537 and `recover_group` 6875 gate visible living/unknown parents. Identity mocks and real file/Git no-result checks pass. Actual Linux live-parent protection not rerun. |
| PC5-04 | Closed, host-policy scope | `host_seen` 2557 rejects changed boot/pidns/machine; operator override confined to unseen/legacy state. Three host-field mutations, visible-unknown operator rejection, legacy handling pass. Operator assertion truth remains external. |
| PC5-05 | Closed | `adoption` 3312 skips pre-result resumed attempts: chain `[1,3]` retained when 2 stops before result. Later fresh post-result attempt rejected. |
| PC5-06 | Closed for original illegal/CUDA/exception cases | `orphan_cause` 3841, `result_fields` 3893; independent matrix covers by-chain failures, timeout, recovered failed rc, and recovered exception. New malformed-rc branch is separate; known missing-log/unknown-rc boundaries remain. |
| PC5-07 | Partial—runtime evidence | `group_members` 2465 finds a living task under Z leader and marks unreadable candidate environment unknown. Real fake-proc files exercise both. Actual Linux thread/environ lifetime and kill completion not rerun. |
| PC5-08 | Partial—runtime evidence | `ledger_lock` 2969 encloses read/check/write/commit; `ledger_append` 3173 rollback verified using actual Git with injected add failure, clean working/index bytes restored. Native flock contention and signal death cannot be established with Windows no-op lock. Known PC6-04 process-death caveat remains. |
| PC5-10 | Closed | Actual `ledger_verdict_check` 4158 using old commit ignores a later other-target folder and rejects a later same-target folder. This is a ledger-input check, not numerical reverify. |
| PC5-11 | Closed, source availability | 93 submitted raw files match manifest; SOURCE.txt explains 207 accounting, reruns, 9/9 deterministic records, 11 bundles. Does not convert submitted logs into new independent PASS. |
| PC6-01 | Partial—runtime evidence | `_run_session_ours` 2418 / `_run_kin` 2429 / `group_members` 2465 distinguish unrelated EACCES from candidate descendants; visible members retained when others unknown; `group_settle` never confirms unknown. Fake proc / mocked EACCES only. hidepid/setsid/real user remain unverified. |
| PC6-02 | Closed | One `words_cause` / `words_keep` rule is exercised across summary and orphan routes including library status errors. Bare “CUDA error: out of memory” is deliberately nonretryable under current five-word policy. |
| PC6-09 | Closed, entry logic | `attempt_open` 3457 checks own existing attempt and start record; actual second-base entry returns 3 without making directory or changing ledger. Native orphan containment itself not tested. |
| PC6-12 | Closed | `found_attempts_problem` 4012 rejects changed target even outside selected input; consumers share function. Actual file evidence checks plus real verdict-commit fixture exercised. Search scope/renamed outside folders remain declared boundary. |
| PC6-13 | **Partial—new adjacent malformed-rc gap** | Original summary/recovered-chain_end failures now nonretryable and matrix passes. By-chain summary-less `rc=false/0.0` still grants retry at 3869; integrated recovery/next eligibility reproduced above. |
| PC7-01 | Closed, start-ledger scope | `attempt_open` commits start before runner and rejects any second base; `recover_ledger` 7019 checks start base and result digest. Real Git fixtures cover live start/no result, changed folder, second base. Clone/shadow ledger remains outside scope. |
| PC7-02 | Closed | Malformed/missing attempt record is rejected by `found_attempts_problem`; only evidence-bound AL07 accepted. Actual missing/bad and changed-target fixtures pass. |
| PC7-03 | Closed | `CHAIN_END_FIXED` 3791, `chain_end_fixed` 3794, orphan route 3881 retain exception→chain_exception through recovery regardless of resource words. Independent matrix passes. SIGINT policy itself remains open as documented. |
| PC7-04 | Closed | `recover_group` uses `group_pair` 3709 before reusing old chain_end; wrong token/name returns held with no end. Independent fixture passes, while process cleanup is mocked. |
| PC7-05 | Closed, documentation distinction | Registration §10-5 explicitly limits “signal_after→group_unconfirmed” to summary-present route. Summary-less recovered cause=None/rc failure is runner_rc unless resource words. Matrix confirms that branch. |
| PC8-01 | Closed | `al07_foreign_ok` 3988 rejects bad status/name/digest/schema/n/code and attempt/summary/group/result traces; honest foreign directory accepted. Empty side record rejected by actual `found_attempts_problem`. |
| PC8-02 | Closed, binding scope | `group_pair` feeds all five consumers; wrong token/name with confirmed=true rejected by group check, orphan read, resume-copy check, and recover; stage_recover selection inspected at 6992. New malformed rc concerns semantics after successful binding, not binding itself. |
| PC8-05 | Closed, start-parent logic; native lifecycle unverified | `start_chain_problem` 2571 called before result at 7063. Actual Git living-start fixture (identity mocked) writes no result even with operator flag; dead parent permits result. All host/legacy policies pass. Actual Linux live process is not claimed verified. |
| SELF-137 | Closed, test-helper defect | Actual `test_rint_r_chain_e2e.e13_cmdlines` at 962–971 reads full bytes. Supplement `probe_self137.py` / `self137_results.json`: wrapper text beyond offset 160 survives interpreter lengths 74, 180, 1000 (3/3); old slicing would miss it. Native `/proc` bytes mocked. E13b/c/e/f explicitly require `saw_window` (1081, 1092, 1200, 1209); production containment not rerun by this helper test. |

## Answers to assigned questions

**Q2 condition② / Q4:** The control flow implements the requested recovery-before-finalization boundary: group scan/settle before end record, runner rejects unconfirmed groups before reading payload (4402), recovery rejects alive/unknown start parents before committing result, and start entry blocks another base/machine using the same ledger. It is appropriate to retain these implementation closures while stating that **this review has not independently established Linux OS containment or kgy behavior**. A global statement “all parent-death termination proven” would be too broad. PC7-07 before-start window is acceptable as a pre-result availability limitation: racing same-ledger starts use expected raw bytes so only one can pass; losing one cannot start its runner. It is not permission to silently reset starts or omit recovery. PC7-06 missing native tests remain evidence debt, not evidence that the corresponding guards fail.

**Q5:** Original CUDA/resource and exception-path inconsistencies are repaired within the declared substring policy. The table is not an all-failure semantic classifier. Fix the new malformed-rc branch before sealing: one-line fix is narrow and independently checked. Also prefer closing already-open **PC6-05** before sealing: missing/unreadable summary-route log is silently `''` (`run_log_text` 3800), so TIME_LIMIT plus marker yields `resume_ok=true` (independently reproduced `known_PC6_05_summary_missing_log_resume`). It cannot establish absence of forbidden CUDA failure evidence; smallest change is track readable/not-readable separately and deny resume if missing, aligning summary-less route. Known PC6-03 SIGINT and PC6-06 chain memory/ENOSPC are conservative availability/policy differences; they need clear text, not a new numerical verdict guard. Unknown pre-end rc/traceback is an explicit limitation, and policy must not present it as known resource failure. GPU resume prohibition remains an operational rule, not code enforcement.

**Q9:** Python 3.8.20 + NumPy/SciPy version gate is useful compatibility evidence, not sufficient runtime evidence for kgy 3.8.10/non-root/SSH/proc options. Before a real first campaign, on the authorized actual user context record: interpreter/build and full package freeze; UID and pid namespace/boot identities; /proc mount/hidepid and visibility of own child environment and stat; harmless same-user fixture with ordinary SSH/agent background present; parent death separate from runner death; post-recovery no child/late marker remains; readonly/unseen-host case remains unconfirmed; sequential and concurrent ledger append on the actual filesystem with exclusive lock; git-add failure leaves previous committed bytes. These are small lifecycle fixtures, not S0/R simulations. No such host access was performed here.

Minor documentation residual: `q9_time_budget.py:7` still calls no-op “same process” although the arithmetic and main documents use the same frozen parent environment / new runner per run. Root/science reviewer notified; no arithmetic impact.
