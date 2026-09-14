# R3 라운드 원장 — 발견 통합 · 상태 · 순서 (대상 a432d23, 2026-09-11)

> **다음 세션은 이 파일부터 읽는다.** 리뷰 원문: `R3_CODEX.md` (외부, NO-GO · P1 9). 보조 보고서 셋은
> `r3_repros/reports/` (분야별 번호 — 정본 번호는 `R3_CODEX.md` 의 R3-01~09).
> Codex 반례 재생: `python3 reviews/r3_repros/harness_r3_replay.py --target <a432d23 의 bms-balancing 절대경로> --output /tmp/r3.json`
> — 대상 SHA 를 확인하므로 `git worktree add <dir> a432d23` 로 만든 트리에서 돈다. 우리 재생 기록:
> `r3_repros/replay_ours_a432d23.json` (8 단계 rc 전부 Codex 기록과 같음 — **아홉 건 전부 재현, 반박 성립 없음**).
> 수정 뒤에는 반례의 "잘못된 결과를 재현했다" assertion 이 **실패해야** 정상이다 (아래 ‘수정 뒤 재실행’).

판정: **NO-GO** (Codex) — "현재 정본의 결론 5 개를 그대로 새 모델의 설계 전제로 채택" 에 대한 것.

> **R4 재판정 (2026-09-11, `R4_LEDGER.md`)**: R3-01·03(계산)·04·09 와 05/07 원래 사례·08 순차 사례는 종결 인정. 02 는 (c) 갈래(R4-01), 05 는 중복 파싱(R4-04), 06 은 추정·반올림(R4-02·03), 08 은 공유 `.part`(R4-06) 로 다시 열렸다가 R4 에서 닫혔다.
관측을 보존하고 원인 해석을 후보 가설로 낮추면 요구서 초안은 진행해도 된다고 명시했다 (§5).

## 발견 (Codex 번호 그대로)

| ID | 무엇 | 상태 | 어디서 | 회귀 |
|---|---|---|---|---|
| R3-01 | 정확한 모델에 상태별 잡음만으로 잔차 증가 표(12 값) 재현 → "잡음 가설과 맞지 않는다 · U3 한 칸 · 제3의 답 지지" 는 산출물 밖 | **닫힘 (철회)** | §0-1 · §0-2 행 · §1-12 잔차 문단(제목 "관측이며 원인은 미확정") · §7-3 · WORKING_STATE · HANDOFF · INTRO · R2 원장 C8 | `test_r3_01_findings_keeps_the_residual_growth_as_observation_not_as_cause` |
| R3-02 | 정확히 표현 가능한 곡선(γ 0.15→0.45, 선택 쌍 0.15→0.16)에도 `ne_shape` 가 "블렌드 모양이 아니라는(모델 부적합) 쪽" 출력 | **닫힘 (코드+철회)** | `scripts/ne_shape.py` 판정문 세 갈래 — 비율까지만, 원인 판정 없음; §5-2 · §0-2 행 | `test_r3_02_ne_shape_does_not_call_a_representable_curve_model_mismatch` |
| R3-03 | "같은 크기를 낼 Δγ 는 상자 안" — secant 외삽 · 기준점 여유 무시. 300_0009: γ_ref 0.2953 → 합법 [−0.295, +0.205], ±0.365 양쪽 밖; 합성 100 mV vs 가족 최대 45.2 mV 에도 "상자 안" | **닫힘 (코드+철회+실측)** | `ne_shape.gamma_headroom` — 합법 Δγ·합법 γ 최대 변화(격자 501)·(a) 증인(가장 가까운 합법 γ, 없으면 없음) 출력 + CSV 열 6 개; §5-2 산술 정정. **실측 (fb62342, 사용자 기계)**: 100·200 증인 γ 0.221 / 0.177 (Δ −0.074 / −0.118), 300_0009 없음 — 합법 최대 86.01 (γ=0) < (a) 119.34 mV (정규화·모양 한정어 포함, §5-2 표) | `test_r3_03_ne_shape_reports_legal_gamma_headroom_and_a_witness_or_none`, `test_r3_03_committed_ne_shape_csv_and_section_5_2_carry_the_headroom_not_the_box_claim` (§5-2 (d) 표 칸별; 변이 4 종 실패 확인) |
| R3-04 | 정규화 표: "pristine 적합의 rmse" 라 했으나 계산은 대상 적합(`[0]`); "7 적합" 은 6 (GITT, 300_0147 제외). pristine 분모면 4.99x·겹침 없음 | **닫힘 (정정)** | §1-12 표: 행 이름이 분모를 말함(`/rmse_pocv (대상 적합)`, `/ref_rmse_pocv (pristine 기준 적합)` 추가), 머리글 "6 적합, GITT"; 본문 R3-04 문단; §0-2 행 | `test_section_1_12_physical_normalization_and_misfit_tables_match_artifacts` (머리글 개수·분모 역할·문장 검사) |
| R3-05 | 앵커 누락·NaN, 파라미터 NaN 이 `complete` | **닫힘 (코드)** | `verify._compare_dd_eval`: 앵커 기대 16 개를 셈(`anchors_expected/compared/missing_anchors`), 비유한 앵커·파라미터 → incomplete, 누락 앵커/열 → `partial`(성공 아님) | `test_r3_05_comparator_rejects_missing_or_nan_anchors_and_nan_parameters` |
| R3-06 | 전정밀도 열의 값이 전부 짧으면(0.125) 추론 atol 1e-3 이 1/1024 차이를 지움 | **닫힘 (코드)** | `resolve_precision`: 옵션 `--precision g17|full|fixed:N` → 파일 `# printed_format` 선언 → 추정(표시). `dd_eval.m`·`mirror_dd_eval.py`·`eval --out` 이 선언을 적음. `result["precision_source"]` | `test_r3_06_declared_or_requested_precision_is_not_inferred_from_token_length` |
| R3-07 | `--compare` 가 갈려도 process 종료 코드 0 | **닫힘 (코드)** | `cmd_eval` 이 `EXIT_BY_STATUS` (0 complete · 1 갈림 · 2 미완/빈 파일 · 3 부분, `--allow-partial` 로만 0) 반환, `main` → `sys.exit` | `test_r3_07_eval_compare_exit_code_follows_the_verdict` (별도 process) |
| R3-08 | 전부 실패한 profile 이 파일을 안 쓰고 정상 반환 → wrapper 가 옛 CSV 를 새 성공으로, `write_meta` 까지 | **닫힘 (코드)** | `cmd_profile`: `.part` 에 쓰고 `os.replace`, 행 없으면 종료 2 (옛 파일 보존, 새 결과 아님); `run_states.sh run`: 시작 도장보다 **새로 쓰인 파일**만 OK (`find -newer`, ns) | `test_r3_08_profile_all_failed_exits_nonzero_and_leaves_the_old_csv_alone`, `test_r3_08_run_states_helper_requires_a_fresh_artifact` |
| S-01 (자체) | fb62342 의 meta 가 `git_dirty: true` — 커밋에는 CSV·meta 만 있었다. 추적된 산출물을 **다시 쓰는 것 자체**가 '추적 파일 수정' 으로 잡혀 재생성 meta 의 플래그가 늘 켜진다 (정보 없음) | **닫힘 (코드)** | `provenance.git_state(exclude=…)` — 지금 쓰는 산출물과 meta 를 pathspec 으로 뺀다; `ne_shape._write_csv`·`run_states.sh write_meta` 가 넘긴다. 코드 수정은 여전히 true | `test_git_state_can_exclude_the_artifact_being_rewritten`, `test_ne_shape_meta_is_clean_when_only_the_artifact_changed` (RED 확인 뒤 GREEN) |
| R3-09 | 192 값 회귀가 TXT 판정문의 숫자를 읽음 — CSV 값을 9.0 으로 바꿔도 통과 | **닫힘 (테스트)** | `test_section_1_8_192_values_are_backed_by_committed_recompare_artifacts`: TXT 원시값 vs CSV 직접 재계산 + 같은 값으로 비교기 실행(`precision="g17"`) → 그 다음에 판정문·§1-8 숫자 대조; §1-8 R3 정정 문단 | (자기 자신) — Codex `harness_r3_artifact_repros.py` 가 수정 뒤 CSV 변조 단계에서 AssertionError (상대차 769.8) |

R2 조건별 판정(`R3_CODEX.md` §3)에서 "부분" 이던 01·02·03 은 위 05·06·07·08 로 닫혔고, "안 닫힘" 이던 08(γ 표현력)은 02·03 으로 닫혔다.
질문 Q1~Q5 의 답 중 문서에 반영한 것: Q1 "5 %" 를 원인 기여율로 읽지 않는다(§1-12 표현 유지 확인) · Q2 정규화 표는 분모·집합을 고쳐 **재척도화 민감도 기술표**로만 (§1-12) · Q3 후보 가설로 (§0-1·§1-12·§5-2) · Q4 R3-04·08·09 · Q5 요구서 표 → 새 모델 요구서 초안의 골격 (다음 단계).

## 수정 뒤 재실행 (이 커밋, 우리 트리)

| 무엇 | 결과 |
|---|---|
| `python3 -m pytest tests/ -q` | 65 passed (fb62342 의 CSV 로 `test_r3_03_committed_…` 활성; S-01 테스트 2 추가) |
| `bash matlab/tests/run_all.sh` (Octave 없음 → 4·5 단계) | 전부 통과 (`--compare` 이분 판정 0 실패, eval 스모크 PASS) |
| `reviews/r3_repros/harness_r3_port_repros.py --target $PWD` | `missing_anchor` 가 `partial` 이라 반례 assertion **실패** (= 닫힘) |
| `reviews/r3_repros/harness_r3_shape_repros.py --target $PWD` | "상자 안" 문구 없음 → 반례 assertion **실패** (= 닫힘) |
| `reviews/r3_repros/harness_r3_artifact_repros.py --target $PWD` | CSV 9.0 변조 뒤 C21 회귀가 상대차 769.8 로 **실패** (= 닫힘) |
| R3-04 변이 감사 (임시 사본의 FINDINGS 변조 4 종: 머리글 7 적합 · pristine 행에 대상 숫자 · 행 이름 맞바꿈 · 본문 'pristine 적합의') | 넷 다 회귀 **실패**, 원본은 통과 |
| `reviews/r3_repros/harness_r3_inference_repros.py --root $PWD --case denominator` | 옛 문장("pristine 적합의", "7 적합") 부재로 assertion **실패** (= 닫힘); `--case noise` 는 그대로 재현된다 — 그것이 R3-01 의 근거이고 우리가 철회한 이유다 |

## 닫는 순서 (실행 기록)

1. ~~재현~~ — worktree `a432d23` 에서 `harness_r3_replay.py` 8 단계 rc 일치 (`replay_ours_a432d23.json`)
2. ~~RED~~ — 신규 9 + 개정 2 테스트가 옛 코드·문서에서 11 실패 (이유 확인: 종료 코드 0, `anchors_compared` 없음, "모델 부적합" 출력, "7 적합" …)
3. ~~코드~~ — `verify.py`(05·06·07·08) · `run_states.sh`(08) · `ne_shape.py`(02·03) · `dd_eval.m`+`mirror_dd_eval.py`(06)
4. ~~문서~~ — FINDINGS §0-1·§0-2·§1-8·§1-12·§5-2·§7-3 · WORKING_STATE · HANDOFF · INTRO · README · matlab/README · R2 원장 C8·C9
5. ~~GREEN + 변이 감사~~ — 위 표
6. ~~사용자 기계: `python3 scripts/ne_shape.py` → CSV 재생성 커밋~~ — fb62342. §5-2 (d) 표 채움 + 칸별 회귀 + 변이 4 종. 그 meta 의 `git_dirty: true` 가 S-01 을 드러냈다 (닫힘; 다음 재실행부터 false).
7. ~~R4 요청문~~ — `R4_REQUEST.md` (이 커밋). 대상은 그 파일이 든 커밋. GO 기준은 R3 §5 의 다섯 조건. U11(ne_shape CSV) 재실행 커밋이 먼저 오면 요청문 §0·§5 의 U11 줄을 갱신한다.

## 유지되는 것 (Codex 가 인정한 긍정적 증거)

192 값의 수치적 일치(4 쌍, TXT 원시값 직접 재계산) · 12 normalization 행의 matrix/degeneracy 대상·기준 parameter 정확 일치 · R2-04/05(문서)/06/07/09/10 닫힘 · §1-12 주요 문장("파우치 PE 고정 실험은 원통형 규모의 LLI 하한 폭을 만들지 않았다") 수용 가능 · 54 → 62 passed + 1 skipped (신규 9).
