# Round 4 independent docs/tests review

Pin: `1f9f3607eb2f0118d322eeff780bba6eb17b85a2`. Comparison: independently retained round-3 package, `17d45fb9cdfc7033bdfd41509527cea23ba1654c`. Paths below are relative to the current `package/repo` unless explicitly marked as reviewer evidence.

**Assigned scope: one additional P3 evidence/test-accounting issue: historical mutant M56 is distinguishable, despite the “equivalent” label repeated in the current request. Current production code correctly rejects the distinguishing input. RR3-02 and the textual SELF-158 correction are closed; PC13-04 and the four specified PC14-06 survivors are closed. Q4 fixture changes are justified.** This does not decide whether other reviewers found a remaining resume-policy counterexample. Q5 must retain the specified scope and conditions; it is not evidence of field qualification or a completed campaign gate.

## Independent work and boundary

- Read the current request, previous verdict, fix plan, current source/test diff, PA13/PA14 test and mutation logic, and raw suite/row/mutation outputs.
- `audit_docs_tests.py` performs read-only AST/diff/raw-record inspection. Results include full source/test/request diffs, `diff_inventory.json`, `row_counts.json`, `raw_log_counts.json`, `mutation_counts.json`, `survivor_coverage.json`, and `rr3_02_corrections.json`.
- `tiny_docs_tests.py`: **24/24** on Windows Python **3.12.14**, invoked with `-I -X utf8 -B`. Twelve checks cover two synthetic producer-shaped public-arm fixtures; eight compare four actual production-function branches with their exact historical mutants; three positive branch controls; one source/test/ledger hash invariant. `tiny_checks.json` contains every observation. Counts overlap conceptually with the supplied suites and must not be added to their totals.
- A separate late `probe_m56.py` invokes the real production helper and the exact historical mutant with actual tiny reviewer-owned file paths and no mocked helper. `m56_result.json` shows different outcomes and refutes the unconditional equivalence classification. This is not part of the 24/24 count.
- The mutation microchecks extract and execute the actual function bodies. `read_attempt` alone is replaced with explicit synthetic identities; their paths are nonexistent and the tested early branches return before payload provenance checks. They are not CLI, ledger, process, or field tests.
- No source or findings-ledger write. No actual research, S0/R campaign, WSL, ibb/kgy host, GPU, full gate, or full mutation sweep executed here. The parent review handles broader targeted execution and package integrity.
- Audit-tool development failures are reviewer-only: first attempt used path variable `MUT` instead of mutation list `M`; second omitted `mutation_PA13_extra.json`. Both produced tracebacks before the survivor artifact, were corrected, and the final read-only audit completed. They are not product failures. The old extra file contains M47/M54 and must be included in historical mutation accounting.

## Finding decisions and precise locations

| Item | Decision | Evidence and boundary |
|---|---|---|
| RR3-02 | Closed | `docs/reviews/codex_rint2_rr_round3_request_20261108.md:83,84,86,94,135,140,154`. Each of the six previous-verdict `rg` hits (83,84,86,94,135,154) now has an explicit `11-08 정정` / `RR3-02` marker; line 140 also corrects the former nonempty-list condition. The diff changes exactly these seven lines. Historical text is retained, chain-side end-record comparisons are stated, summary/orphan signal_after paths are separated, and STOPS membership is separated from occurrence-specific subsets. |
| SELF-158 | Closed for wording only | Round-3 request `:134` explicitly says the old GU-record-rc closure was overstated, names the originating commit/report, identifies CT06 S2's CHAIN_OK1 limitation, and narrows the old claim. This sentence was already present at the round-3 pin and is unchanged in this diff. Current request `:48` correctly asks for textual confirmation only. No historical report rewrite or new runtime closure is inferred. |
| PC13-04 | Closed for the identified duplicated expression | `scripts/rint_r_chain.py:2177–2180` defines the shared prefix; `:2273`, `:2342`, `:5462` call it from classifier, reader, and graph-source producer. The replaced expressions are semantically the same for their valid kit input. `test_rint_r_chain.py:16430–16451` scans the literal kit-slice expression; `:16454–16499` checks call sites and performs actual successful `read_run` plus patched common-validator rejection. The scanner is not a universal alias/dataflow proof, and none is needed to close these concrete copies. |
| PC14-06 | Closed for the four identified survivors | `test_rint_r_chain.py:16720–16723` has each missing negative; `:16704–16705` has valid from=resume_of=2 controls with/without source. `:16739–16753` checks cause, eligibility, and reason, and treats exceptions as failed rows. The exact four historical mutation strings match `preattack14/probes/mutate.py` and `pa14_fix/tools/mutate_pa14.py`; supplied current raw results each fail PA14D, while identity is 8/8. Independent minimal branch checks distinguish all four and preserve three valid controls. This closes a test gap, not a newly changed guard. |

The four survivor distinctions are explicit, not accidental broad-suite failures:

| Historical mutant | New row | Current micro-observation | Mutant micro-observation |
|---|---|---|---|
| M14 copied_from type | `f_m14_copied_from_true` | Reason, rejects bool | None |
| M18 precomparison compared list | `f_m18_rr_cmp_det_none` | Reason, rejects nonempty compared before rerun completion | None |
| M47 compared element type | `f_m47_cmp_elem_int` | Reason, handles integer element | AttributeError; PA14D explicitly counts an exception as failure |
| M54 lower from bound | `f_m54_from_below_resume_of` | Reason, rejects from 1 below resume_of 2 | None |

## Additional P3: M56 is a distinguishable survivor, not equivalent

Affected current claim: `docs/reviews/codex_rint2_rr_round4_request_20261109.md:103`, “51 (동치 2) 중 45/49”. The originating historical report is `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack14/REPORT.md:9`, explicitly naming M46 and M56 as equivalent. The exact M56 operator is `preattack14/probes/mutate.py:60`:

```python
if not src.is_dir():   # current production guard
if not src.exists():   # M56
```

The supplied raw outputs `preattack14/out/mutation_PA13.json` plus `mutation_PA13_extra.json` contain **51 operators, 45 killed, 6 surviving** (M14, M18, M46, M47, M54, M56). The individual M56 output is 4/4 PASS. A survivor is not equivalent merely because those tests pass.

Tiny distinguishing input (`probe_m56.py`, `m56_result.json`): create `attempt_1` as an ordinary file and a sibling `attempt_1.rejected.json`. Call the helper at `attempt_2` with `resume={from:1,copied:[],rerun:'R',compared:[],determinism:'assumed'}`, one new run `R` with valid `R_arm1`, and a later timeout stop. No actual attempt or research run is made.

- Current `scripts/rint_r_chain.py:4438–4442`: source is not a directory, sibling rejected record is present, returns the explicit rejected-source reason.
- M56: the source file exists, so the rejected-source branch is bypassed; `resume_leftovers(file/R_arm1)` (`:5283–5293`) returns no payloads, agreeing with the empty compared list, and the helper returns **None**.

This is a direct production-helper counterexample to the equivalence label. The current code is safe on this input, and this review has **not** shown a current `result_fields`, ledger, or CLI eligibility failure. The case uses malformed source-path state, which must be stated; if equivalence was intended only over source paths proven to be absent/directories, that precondition must be explicit and proved at this consumer. The current request's unqualified equivalence claim has neither restriction nor proof.

Keeping M46's JSON-value-domain equivalence classification, the historical accounting is **45/50 non-equivalent mutants killed, five distinguishable survivors**, not 45/49 with four. Do not modify raw historical outputs. Minimal remedy: correct/annotate the current claim and historical equivalence interpretation; preserve the distinguishing input as a negative regression with absent-source/directory-source controls and include this operator in a follow-up mutation check. The independent four named PC14-06 survivors remain closed, and the separate PA14-fix **23/23** count is unaffected. This finding does not by itself justify another runtime execution hold.

## Q4: accept the fixture migration

`test_rint_r_chain.py:14936` preserves CT06_ARM's three keys `{file,index,sha256}`. That is the failure-identity producer shape, not a completed read. The new `ct06_pub` at `:14944–14948` supplies the public successful-read shape and is used for the intended successful prior run at `:15002`, `:15454`, `:15467`, and `:15484`.

The test diff does not remove any existing test function. Its only changed existing function body is `t_PC12C`; it changes the intended-success fixture and supplies kit/request context, not the expected success booleans. The CT06 change is its table's `c_prev_record`. Failure-identity fixtures remain in the negative stopped-run cases (`:15040–15043`, `:15096–15106`) and new RR3 negative paths. The no-group-cause PC12C case remains negative after receiving an otherwise valid fixture. This is preserving the intended isolation of the tested defect, not deleting negative coverage.

Producer evidence for the later value correction is independent of the new validator:

- `scripts/run_contract.py:722` constructs `p3ca-` plus 16 lowercase SHA-256 hex characters.
- `scripts/step3_sigma.py:232–239` returns the 16-byte BLAKE2b hex digest, i.e. 32 lowercase characters. The reader obtains the grid fingerprint through evidence at `scripts/rint_r_chain.py:2398–2404`.
- `scripts/rint_r_chain.py:2420–2433` computes zero error as 0.0 and positive error through the certificate's target judge. `ct06_pub`'s float `1e-6` is inside the established positive tolerance; its four pass flags and convergence values have successful producer forms.
- The fixture's SHA and fingerprint are synthetic placeholders of the valid forms, not verified actual payload provenance. Q4 only needs that producer-shape property; the request explicitly excludes cross-file byte provenance at `docs/reviews/codex_rint2_rr_round4_request_20261109.md:63`.

The supplied old-tests/new-RR3-chain cross-run is **479/481**, with only CT06 and PC12C failing. Its row JSON identifies exactly CT06 `c_prev_record` and PC12C `cli_honest_tl_after_ok`, `gu_after_ok`, `rr_after_copied`, `rr_signal_after_ok`, `tl_none_after_ok`; the new classifier calls these old fixtures `file_ids`. This matches the semantic change. The new fixture repairs the positive premise; it does not bless the old failed-read record.

## Raw evidence accounting

The following counts were independently recounted from individual `PASS`/`FAIL` lines and compared with raw suite summaries. They are received author executions, **not** this reviewer's new independent runs. The historical preattack-14 equivalence denominator is the exception identified above; raw test outcomes themselves match.

| Evidence | Before | After |
|---|---:|---:|
| RR3 selected, `rr3_fix/logs/{before,after}_RR3.log` | 3 PASS + 5 FAIL | 8 PASS + 0 FAIL |
| RR3 full 3.11 | 481 PASS + 0 FAIL | 487 PASS + 0 FAIL |
| RR3 targeted | — | 15 PASS + 0 FAIL |
| RR3 old tests × fixed chain | — | 479 PASS + 2 FAIL |
| PA13 selected, `pa13_{before,after}.log` | 0 PASS + 4 FAIL | 4 PASS + 0 FAIL |
| PA13 full 3.11 | prior 487 | 491 PASS + 0 FAIL |
| PA14 selected including PA13 | 4 PASS + 4 FAIL | 8 PASS + 0 FAIL |
| PA14 full 3.11 | prior 491 | 495 PASS + 0 FAIL |
| Each supplied post-fix e2e | — | 51 PASS + 0 FAIL |
| Each supplied py38 chain | — | RR3 487; PA13 491; PA14 495, all no FAIL rows |
| Each supplied py38 e2e | — | 51 PASS + 0 FAIL |

Per-case JSON confirms PA13 A/B/C/D row totals **48/59/7/3**, failing **38/48/5/2 → 0/0/0/0**; PA14 A/B/C/D **11/3/28/18**, failing **6/2/20/9 → 0/0/0/0**. Rows retained in detailed outputs match `n` where the harness emits the full row map. CLI helper results sometimes emit only count/failures, so no absent per-row transcript is invented.

Raw mutation records have **23/23** caught RR3 mutants, **49/49** PA13, and **23/23** PA14; every caught record has named failed new/selected tests. Identity reports are 9/9, 4/4, 8/8 respectively. The four PA14 historical survivors are the exact same transformations, now each fails PA14D. The separately reported equivalent `_show` mutant remains outside 23, not silently counted as caught. This audit did not independently execute all mutation campaigns.

The supplied Python 3.8 evidence contains the named eleven suite logs. Chain/e2e counts above agree; the remaining logs support run_contract 124/124, RINT selftest PASS, ptfe_face_alpha 242/0, carbon_junction 547/547, ca_ext_b6 502/0, ca_ext_runner 151/0, target_cert 264/264, conv_cert 29/29, census 186/0. `step3_conv_cert.log` explicitly skips the K4b SciPy comparison on 1.10.1 without counting it; passing eleven scripts is not every possible field check. Actual kgy 3.8.10 is still unqualified as declared.

The tau raw log reports 383670 accepted target-judge cases (300378 boundary cases), no e>tau, max e=tau. This is consistent received evidence, not an exhaustive numeric-domain proof or a new execution here.

## Q5 scope wording

The request asks at `docs/reviews/codex_rint2_rr_round4_request_20261109.md:121`; it does not itself constitute a reviewer GO. The fix plan's `:121–122` expressly forbids a general-policy GO based on unchecked legacy exceptions and reserves actual records, field qualification, source diff, and fingerprint checking for sealing. The request's `:66–67` openly retains PC14-02 and PC14-03, and `:71` states synthetic/host limitations.

If the other code-review streams close the specified blockers, the supported wording is: **“지정된 코드·설계·문서 수정은 명시한 합성 검토 범위에서 수용한다(재개 정책 수정 포함). 선언 한정의 실제 계획·시도 기록 대조와 현장 자격, S0 단계1 채택 조건, 12단위 끝-끝, 새 계획/핀 봉인은 별도 조건으로 남는다.”**

Do not shorten this to an unrestricted “재개 정책 전체 GO” or infer that this docs/tests stream authorizes executing the campaign. New counterexamples from the parallel producer/value or resume-policy review would supersede that conditional wording.
