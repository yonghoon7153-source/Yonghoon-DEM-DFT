# 적대적 리뷰 요청 — 3차 라운드 · α·β 검증 하네스 (`bms-balancing/`)

2차(대상 `abfed8b`)는 **NO-GO** (P1 9 · P2 1, `reviews/R2_CODEX.md`). 열 건 전부 우리 트리에서 재현됐고,
내부 리뷰 L2·L5(`reviews/R2_INTERNAL_*.md`)가 결론급 셋을 더했다. 이 판은 그 스무 항목의 대응이다
(`reviews/R2_LEDGER.md`). **목표가 바뀌었다**: 코드 제공자의 은퇴로 사용자가 전권을 인수했고 규진팀에
회신하지 않는다. `FOR_BMS_TEAM.md` 는 동결(배너). 그러므로 이 라운드의 GO 는 "외부에 보내도 되는가"
가 아니라 **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"** 다.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 들어 있는 커밋 (`git log -1`; 코드·문서의 마지막 변경은 `f5d9aafd2c2a3f40287f365ee37cb55753d6e36e`) |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 소유 |
| 범위 | `bms-balancing/` 만. `degradation-degeneracy/` 게이트는 본체 브랜치 일 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). 이 요청문의 숫자는 사본 |
| 저장소에 없는 것 | 원본 MATLAB(`electrode_balancing_blend.m`) · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT`. 단 §1-13 은 원본의 로컬 함수 둘을 사용자가 직접 열어 대조한 기록 |
| 우리 환경에서만 되는 것 | MATLAB `dd_eval` 재생성(§8-3), `ne_shape.py`, `fixed_hc.py check`, 원자료 `eval`. 산출과 판정은 `out/recompare/`·`out/ne_shape_GITT_Li.csv` 에 커밋 |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                                             # 원자료 불필요, 54 passed 기대
bash matlab/tests/run_all.sh
python3 reviews/r2_repros/harness_r2_replay.py --target "$PWD" --output /tmp/r.json   # R2 반례 재생
python3 scripts/compare_states.py pouch=out fixedhc=out/cells_pouch_fixedhc c168=out/cells_c168 c171=out/cells_c171
```

## 1. 검증 — 2026-09-11, `f5d9aaf`, 작업트리 clean, dirty 완화 없음

| 검사 | 출력 |
|---|---|
| `python3 -m pytest tests/ -q` | `54 passed in 6.54s` |
| `bash matlab/tests/run_all.sh` (Octave 8.4) | `PASS — 0 개 실패` · `PASS — 실패 0: []` · `전부 통과` |
| R2 반례 재생 (`harness_r2_replay.py`) | `port rc 1` — `assert all(scenarios[k]["incorrect_all_match"] …)` **AssertionError** (비교기가 미완 대조를 더 이상 "전부 일치" 로 안 찍는다) · `inference rc 1` — `assert any("2.30±4.35" …)` **AssertionError** (표시가 `best [min,max]`) · `shape rc 1` — **AttributeError** `SyntheticHalfCell` 에 `E_PE` 없음 (우리 `ne_shape` 가 PE 축을 읽게 돼 그쪽 합성 클래스가 낡음; R2-08/09/10 의 닫힘은 아래 테스트가 증명) · `consumed_axis rc 0` — **사실이므로 그대로 성립** (측정 NE 미소비) |
| 재대조 4 (`out/recompare/*_r2.txt`) | 네 조합 "앵커 16개가 전부 맞고, rmse 32개는 … 실제 수치 차이" 최대 상대차 2.68e-12 / 4.04e-12 / 2.54e-12 / 3.28e-12 |

## 2. R2 발견별 대응

| R2 | 판정 | 어디서 | 테스트 |
|---|---|---|---|
| R2-01 비교 안 한 셀도 "전부 일치" | 닫힘 | `verify._compare_dd_eval`: 기대/비교 셀 수, 행 누락·격자 불일치·NaN → "대조 미완 — 성공 아님", 구판 스키마는 "부분" 표시, dict 반환 | `test_r2_01_comparator_does_not_certify_uncompared_cells`, `matlab/tests/test_compare_bisect.py`(격자·행 누락에서 "전부 일치" 금지) |
| R2-02 짧은 토큰이 파일 atol 0.1 | 닫힘 | `verify.printed_abs_tols`: 열별, 유효 15자리 이상 토큰이 있는 열은 전정밀도(0) | `test_r2_02_short_exact_token_does_not_relax_file_tolerance`, 기존 두 정밀도 테스트 유지 |
| R2-03 profile 이 실패 결과 저장 | 닫힘 | `verify.cmd_profile`: multistart 와 같은 채택, `n_ok/n_tried` 열, 전부 실패 γ 미저장 + `summary.gamma_all_failed`. **기존 profile 산출은 수렴 미확인** (재실행 안 함) | `test_r2_03_profile_does_not_store_failed_optimizer_rows` |
| R2-04 `best±span/2` | 닫힘 | `compare_states` `best [min,max]`; §1-10 표 `best [min, max]`·폭(max−min) | `test_r2_04_*`, `test_section_1_10_table_prints_best_min_max_and_width` |
| R2-05 외곽 겹침 ≠ 공유값 | 문서 닫힘 · 증인은 새 실행부터 | §1-12 "외곽 범위" 로 한정, "겹침은 안전" 철회; `mode_profile_extrema` 가 `attainable_pct/grid_pct` 보존 (기존 JSON 에는 없음) | `test_mode_profile_keeps_the_attainable_grid_for_connectivity` |
| R2-06 /best 정규화 | 닫힘 (철회) | §1-12: /best 는 임의 재척도화; 물리 단위(`rmse_pocv`) 표 — 분모에 따라 2.9~10.5x, /rmse 에서 구간 겹침; "벗긴 값" 철회 | `test_section_1_12_physical_normalization_and_misfit_tables_match_artifacts` |
| R2-07 측정 NE 미소비 · 이전 가정 없음 | 닫힘 (철회 + 실측) | §1-12 "PE 곡선뿐" 문단; "대체는 원인이 아니다" 철회 → "파우치 PE 고정 실험은 원통형 크기의 LLI 띠를 만들지 않았다"; PE 축 개입 강도 실측(조건 7: 100 rms 24.3 mV, 200 2.7, 300 4.1 — **개입은 100 에서만 강했다**) | `test_section_1_12_pouch_pe_fixing_did_not_reproduce_the_wide_lli_band`(LAM_PE 반대 부호 단언 포함), `test_section_1_12_pe_axis_strength_table_matches_the_csv`, `test_ne_shape_measures_the_consumed_pe_axis_too` |
| R2-08 γ 표현력 | 닫힘 (철회) | §5-2 제목·해석: (b)/(a) 는 적합이 움직인 Δγ; 같은 크기를 낼 Δγ 는 상자 안; `b_NE` 만 바꾸면 LAM_NE=0; 보상은 `a_PE`·`b_PE` 로도. `ne_shape` 판정문 수정. 표현력(γ 직접 적합)은 미구현 | 판정문·CSV 스키마 테스트 |
| R2-09 `<1.20` | 닫힘 | `audit97` 행별 임계 1.177~1.196 + 고정-기준 조건; §2-1 제목·문단 정정; INTRO §6-1 | `test_r2_09_audit97_reports_per_row_thresholds_not_a_single_cutoff` |
| R2-10 `gamma_ref` 열 | 닫힘 | `ne_shape` 가 `gamma_target`·`gamma_ref` 분리, CSV 재생성(`1a133c4`) | `test_r2_10_ne_shape_csv_carries_both_gammas` |

내부 L2·L5: L5-F1(대조가 LAM_PE 패턴 재현) → §1-12 세 mode 몫 표 + 반대 부호 단언 · L5-F4(best_obj 는 auto-scale 단위, 부적합 증가) → 물리 정규화·부적합 표 · L5-F5(§1-10 반대 기전) → §1-10 정정 · L5-F6(FOR_BMS 오도 5) → 동결 배너 · L2-F1(INTRO §6-1) → 재작성 · L2-F2/F3(HANDOFF) → 정정 · L2-F4("8 중 6" → 5, 재계산 확인) · L2-F5(16/97 라벨) · L2-F7(§0-1) → R2 정정판 · L2-F8 잔존 문장 묶음 → 정리. 추가로 **C21**: §1-8 의 192 값 CSV 가 미보존이었음이 드러나 툴박스 `dd_eval` 로 재생성·재대조 (`out/recompare/`).

## 3. 철회 목록 (§0-2 에 추가된 R2 행)

"우리 대체는 원인이 아니다 (0.5~5.2 %)" · "LAM_PE 식별 가능성은 두 셀에서 똑같다 / 대조는 파우치 패턴 유지" · "정규화하면 8.0 배 — 교란을 벗긴 값" · "원통형은 못 가른다" (→ 외곽 범위 겹침) · "γ 는 3~16 % 만 표현 → 그것이 곧 LAM_NE" · "상한을 1.20 아래로 잡았으면 음수 불가 / 인과가 닫혔다" · "100 GITT 뒤집힘은 §2-1 과 같은 기전".

## 4. 지금 정본이 말하는 것 (§0-1 R2 정정판) — 이대로 서는가

1. 포팅의 forward model 은 원본과 같다 — 192 값 최대 상대차 4.04e-12 (§1-8, `out/recompare/`); dQ/dV 항의 전사 함수 둘은 원본과 줄 단위 일치 (§1-13). 절차 차이의 **관측** 상한 0.17 %p (§1-9, 전 조건의 상한 아님).
2. §2-1: 97 행의 강한 음수 LAM_NE 는 **기준 적합을 고정한 조건의 부호 산술**로 「대상 상한·기준 자유」에서 나온다 (5/5). 경계 변경 재적합의 인과는 미확립.
3. §1-10: 파우치 네 상태에서 **탐색 하한 폭**의 순위는 LAM_NE 최광·LLI 최협 (4/4, 절대 폭 %p 로만). 식별성의 확정이 아니다.
4. §1-12: 원통형 둘의 LLI 하한 폭은 raw 로 5~10 배(하한끼리, max/max; 분모에 따라 2.9~10.5). 파우치 PE 고정 실험은 그 폭을 만들지 않았으나(개입은 100 에서만 강했다: rms 24 mV) **LAM_PE 에서는 원통형 패턴을 재현**했다. "대체 배제" 도 "셀 차이" 도 아니다. 외곽 범위는 파우치에서 LAM_NE·LLI 분리, 원통형에서 LAM_PE 분리·LAM_NE·LLI 겹침 — 공유 가능값은 미확정.
5. 원통형 부적합(`rmse_pocv`)은 사이클과 함께 1.5~1.6 배 커지고 파우치는 0.77 배 — 잡음 가설과 맞지 않고, §5-2(적합이 γ 를 움직여 측정 NE 변화를 좇지 않음, 블렌드 vs 측정 rms 19~24 mV)와 함께 **모델 부적합**이라는 제3의 답을 지지한다.

## 5. 닫지 않은 것

| # | 무엇 | 상태 |
|---|---|---|
| U1' | 원본 가중 버전 `compute_dqdv_rmse_weighted_blend`(328~347)의 분모 및 `lower_half_mean_local` 대조 | **닫힘 (요청문 발송 직후)** — 분모 `sum(w)` 로 포팅과 같음; lower_half_mean 은 빈-표본 가드(0 vs eps)만 ≠ (§1-13) |
| U2 | pOCV 워크북이 원자료인지 재표본인지 | 간격 균일성 검사 대기 |
| U3 | 원통형 차이 = 셀 물성 vs 자료 품질 vs 모델 부적합 | 부적합 증가로 한 칸 좁힘; 확정 아님 |
| U4 | 파우치 100·200·300_0009 산출의 starts/seed provenance | 코드 동일성은 diff 로만; `run_states.sh` 재실행 미실행 |
| U5 | fixedhc 의 B축(`matrix`)은 대조 아님 (`step_005C` 미고정) | 그대로 |
| U6 | 폭은 전부 하한; 1 % 띠 ≠ 신뢰구간; 공통 절대 문턱 재실행 미실행 | 그대로 |
| U7 | 기준(pristine) 이동과 대상 이동의 분리 | 미착수 |
| U8 | 기존 profile 산출의 수렴 상태(R2-03 이전 코드) | "수렴 미확인" — 재실행 안 함 |
| U9 | γ 직접 적합(표현력) · 공유 가능값 증인(기존 JSON 에 격자 목록 없음) | 미구현 / 새 실행부터 |
| U10 | 테스트 사각지대 잔여: INTRO·HANDOFF 숫자 무검사, `tol_percent_of_best` ×100, 한정어 삭제 | 열림 |

## 6. 리뷰어에게 — 질문

1. §1-12 정정판이 R2-07·L5-F1 을 충분히 지고 있는가. 특히 "개입이 100 에서만 강했고 그 100 에서 LLI 는 격차의 5 %" 라는 문장이 다시 배제 논증으로 읽히지 않는가.
2. 물리 정규화 표를 "분모에 따라 2.9~10.5 배" 로 두는 것이 맞는가, 표를 빼야 하는가. 공통 절대 문턱 재실행 없이 말할 수 있는 최대치는 무엇인가.
3. §0-1 이 "제3의 답(모델 부적합)" 을 부적합 증가(1.5~1.6 배) + §5-2 로 지지된다고 적었다 — 산출물 이상으로 나간 것 아닌가. 잡음·전류·온도 등 대안이 같은 증가를 만들 수 있는가.
4. 문서를 산출물에 묶는 방식(표 파싱·칸별 대조, `tests/test_review_findings.py` 후반)의 빈틈.
5. **목표 전환 관점**: 이 정본이 새 모델의 설계 요구서로 쓰이려면 무엇이 더 있어야 하는가 — 우리가 뽑은 세 줄은 (측정 NE 를 쓰는 음극 표현, PE 기준 처리를 명시적 선택으로, 잡음 모델이 있는 목적함수)이다.

## 7. 실측 첨부

- `out/recompare/dd_eval_*_r2.{csv,txt}` — 4 조합 × (앵커 16 + rmse 32), 툴박스 본체, `%.17g`.
- `out/ne_shape_GITT_Li.csv` — (a)(b)(c) + `gamma_target/gamma_ref` + `pe_shape_max/rms_mV` (100: 35.70/24.27 · 200: 20.24/2.71 · 300_0009: 24.78/4.09 mV).
- §1-13 표 — 원본 두 로컬 함수 vs 전사 vs 포팅, 줄 단위.
- `reviews/R2_INTERNAL_L2.md`·`L5.md` — 재계산 스크립트 출력 전문.

## 8. 이후

GO: 정본의 결론 5 개 + 부적합 증거를 출발점으로 새 모델 설계 요구서(`docs/`)를 쓴다. 보존: 이 커밋의 `out/` 전체·`reviews/`.
NO-GO: 발견마다 `/finding` — 반례를 RED 테스트로 먼저.
