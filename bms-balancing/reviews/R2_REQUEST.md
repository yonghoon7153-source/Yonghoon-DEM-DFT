# 적대적 리뷰 요청 — 2차 라운드 · α·β 검증 하네스 (`bms-balancing/`)

1차(대상 `a4bea42`, 2026-09-10)는 **NO-GO**. 결론 넷 중 셋이 무너졌고 반례는 전부 재현됐다.
이 판은 그 정정 + 그 뒤 닫은 것 + **우리 자체 리뷰 결과**를 싣는다. 리뷰어는 자체 리뷰가 놓친 것 위에서 시작하면 된다.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | `abfed8b371c08b4c358f2c2b7e0853056dad838c` |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 은 이 브랜치가 소유. 본체 `claude/14-gate-code-review-9qkx05` 의 사본은 뒤처져 있다 |
| 범위 | `bms-balancing/` 만. `degradation-degeneracy/` 게이트와 무관 (`source_digest` 밖) |
| 정본 | `FINDINGS.md` + `out/*.json`·`out/*.csv` (+ `.meta.json`). 이 요청문의 숫자는 사본 |
| 저장소에 없는 것 | 규진팀 원본 MATLAB(`electrode_balancing_blend` 계열) · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 우리 환경에서만 되는 것 | `dd_verify`/`dd_eval` MATLAB 실행(§1-7·§1-8), `fixed_hc.py check`, `ne_shape.py` — 원자료가 필요. 그 출력은 §8 에 첨부 |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout abfed8b
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                      # 원자료 불필요
bash matlab/tests/run_all.sh                     # Octave 있으면 4종, 없으면 Python 2종
python3 scripts/compare_states.py pouch=out fixedhc=out/cells_pouch_fixedhc c168=out/cells_c168 c171=out/cells_c171
```

물음은 1차와 같다: **"코드가 내놓는 α·β(LAM/LLI)가 데이터에서 나온 것이냐, 분석자가 고른 설정에서 나온 것이냐"** 에 우리가 낸 답이 근거를 갖는가.

## 1. 검증 — 2026-09-11, `abfed8b`, 작업트리 clean (`git status --porcelain` 빈 출력), dirty 완화 없음

| 검사 | 출력 |
|---|---|
| `python3 -m pytest tests/ -q` | `39 passed in 7.37s` |
| `bash matlab/tests/run_all.sh` (Octave 8.4 있음) | `PASS — 실패 0: []` … `전부 통과` |
| `scripts/compare_states.py` 4 루트 | §8-1 에 전문. 헤드라인: LLI 반폭 pouch 0.29/0.43/0.54 · fixedhc 0.49/0.46/0.58 · c168 4.12/6.07/4.82 · c171 5.25/4.68/2.77 (%p) |

## 2. 1차 발견별 대응

| 1차 발견 | 판정 | 어디서 고쳤나 | 회귀 테스트 |
|---|---|---|---|
| A2 [P0] "한 점 대조는 같은 forward function 을 증명하지 않는다" / "독립 재적합이 아니다(보고값이 시작점)" | 닫힘 | `verify.py` `port --blind`(보고값 배제) · MATLAB 대조를 **점 1 → 4 조합 192 값** (§1-0 104 값 → §1-8 192 값, 최대 상대차 4.04e-12) · 툴박스↔shim §1-7 · 절차 §1-9 (자유 조합 최대 0.17 %p, 갈린 2 점은 그들이 이김) | `test_port_offers_blind_mode`, `test_compare_uses_full_precision_when_file_has_it`, `test_compare_does_not_cry_wolf_on_printed_precision` |
| A3 [P1] 실패한 optimizer 결과를 fit 으로 채택 | 닫힘 — **실제로 답을 바꿨다** (§3, v1→v2 재생성) | `verify.multistart` success 필터 | `test_multistart_rejects_failed_optimizer`, `test_multistart_keeps_successful_results` |
| B1 [P0] "1 % 안 폭 0.87 %p" 는 무작위 구름의 관측 하한 | 철회 → 재측정 LAM_NE 3.60 %p (4.1배) | `verify.near_optimal_extrema` + `verify.mode_profile_extrema` 합집합, `span_method` 를 JSON 에 명시, **여전히 하한**이라고 적음 | `test_degeneracy_recovers_ridge_with_volume`, `test_degeneracy_beats_random_cloud_on_measure_zero_ridge`, `test_committed_profile_contradicts_no_documented_span` |
| B1 [P0] 커밋된 두 산출이 서로 모순 | 닫힘 | 문서 숫자를 artifact 에서 재계산하는 테스트 군 | `test_quoted_spreads_match_artifact`, `test_dump_table_in_matlab_readme_matches_artifact`, `test_compare_states_reads_the_latest_version` |
| B4 [P1] "LLI 문헌곡선 강건 0.53 %p" 는 사후선택 분모 / "dQ/dV +2 %p" 는 미대응쌍 | 정정 (전체 축 1.0248 %p; 완전 대응쌍 3개 +1.34/+2.01/+2.17, 16쌍 중 음수 4) | `verify.cmd_matrix` `_span`·`matched` — 분모를 제목에 | `test_lli_robustness_number_is_the_full_literature_axis`, `test_dqdv_shift_is_reported_from_matched_pairs`, `test_matrix_summary_reports_matched_pairs` |
| B4-4 [P1] 기준(pristine)의 이동과 대상의 이동을 못 가른다 | 부분 — matrix 행이 기준 적합을 같이 실음 (`ref_*` 9 필드); **분리는 아직** (§7) | `verify.cmd_matrix` 행 스키마 | `test_matrix_row_carries_reference_fit` |
| "강한 음수 LAM_NE 는 전부 경계" — 원표 없이 주장 | 닫힘 — 원표 97행 커밋(`out/bms97/`), 인과를 **산술로** (§2-1) | `scripts/audit97.py` | `test_findings_section2_numbers_come_from_the_committed_table`, `test_negative_lam_ne_is_arithmetic_not_correlation` |
| "γ 프로파일 = 실질 오차막대" | 정정 — 결정론적 민감도 곡선, 잡음 모델 없음. σ 는 쟀다(`verify noise`, 0.0285 mV, 부적합/σ = 267) 그러나 원자료/필터본을 한 곡선으로 못 가름 (§7-3·§7-4) | `verify.rice_sigma`, `verify.noise_diagnosis` | `test_rice_sigma_recovers_known_noise`, `test_rice_sigma_collapses_on_presmoothed_signal_and_is_detectable` |

1차 ①~⑥ 자기 의심: ① (1 % ≠ 통계) 유지·문서화 §7-3 · ② (12 mV 문턱 전용) 유지, 대안 없음 · ③ (전역 최적) §1-9 로 절차 차이 상한 0.17 %p, γ≥0.45 점프는 §1-4 · ④ 유지 · ⑤ B4-4 · ⑥ → §1-10·§1-12.

## 3. 1차 이후 새로 닫은 것

| 절 | 주장 | 근거(artifact) |
|---|---|---|
| §1-7·§1-8 | MATLAB 툴박스↔shim: `quantile` 0, `findpeaks` 0, `sgolayfilt` 1.33e-13, `rmse_dqdv` 1.78e-12. MATLAB↔Python 192 값 최대 4.04e-12 — "앵커는 fp 한계에서 같고 rmse 는 1e-12 구현차" | 사용자 기계 CSV(§8-3) |
| §1-9 | 적합 절차(N1·N2·N3) 차이 상한 0.17 %p; blind 재적합 = 비-blind | `out/matrix_300_0009_v2.csv`, `out/profile_gamma_300_0009_Li.csv` |
| §1-11 | 포팅 버그: `np.interp` 는 내림차순 x 를 못 받음(`E_PE(0.5)=29.96 V`). 파우치는 no-op 실측 | `model._interp_lin_extrap`, `test_interp_handles_descending_x_like_matlab` |
| §1-10 | 파우치 4 상태에서 LAM_NE 최광·LLI 최협 (4/4, 100 은 LLI/LAM_PE 0.002 %p 동률). **절대 폭으로만**; 100 GITT 의 순위 뒤집힘은 경계 산물(자유 0/8) | `out/degeneracy_*.json`, `test_section_1_10_ranking_comes_from_artifacts` |
| **§1-12** | 원통형(#168·#171) 띠 확대는 **반쪽전지 대체 탓이 아님** — 파우치를 pristine 반쪽전지로 고정해도 LLI 반폭 이동 +0.03~+0.20 %p vs 격차 2.23~5.64 %p (0.5~5.2 %). 남는 것: **순위 반전** — 파우치는 LAM_NE·LLI 로 사이클을 가르고 LAM_PE 로 못 가름, 원통형은 반대. LLI 반폭 10.5x (raw) / **8.0x (best_obj 정규화)** | `out/cells_pouch_fixedhc/`, `out/cells_c168/`, `out/cells_c171/`; `test_section_1_12_*` 4종 |
| §5-2 | γ 가 만드는 음극 모양 변화는 측정 변화의 3~16 % (0.64/5.76/18.17 vs 23.94/35.77/119.34 mV). 남는 모양은 `a_NE`·`b_NE` 로 → LAM_NE. (c) 블렌드 vs 측정: max 70.5~136.0 mV, rms 19.3~24.1, max 위치 전부 x→0 끝단 | `out/ne_shape_GITT_Li.csv`, `test_section_1_12_and_5_2_ne_shape_tables_match_the_csv` |
| 산술 고정 | `LLI = f(a_PE, b_PE, b_NE)` — 반쪽전지 대체는 LAM_PE **와 LLI** 에 들어가고 LAM_NE 만 절연 (전 판의 "LAM_NE·LLI 영향 적다" 는 틀렸음) | `test_half_cell_substitution_reaches_lli_not_just_lam_pe` |

## 4. 자체 리뷰 (2026-09-11, §1-12·§5-2 대상, 렌즈별 실측)

### 4-1. CONFIRMED — 전부 반영됨

| # | 주장 | 실측 | 심각도 | 조치 | 테스트 |
|---|---|---|---|---|---|
| S1 | 띠는 `obj ≤ best·(1+1 %)` → best 가 크면 절대폭 확대. 원통형 best_obj 0.53~0.76 vs 파우치 0.29~0.51 (1.5x) | 반폭/best_obj: LLI 파우치 0.99~1.30, 원통형 3.65~10.37 → **8.0x** (raw 10.5x); LAM_NE 2.4x; LAM_PE 0.7x | 숫자가_바뀜 | §1-12 에 정규화 표 병기, "둘 다 정확한 폭 아님" 명시 | `test_section_1_12_obj_normalized_table_comes_from_artifacts` |
| S2 | 파우치 100·200·300_0009 산출에 meta 없음, starts/seed 가 JSON 에도 없음 → 나머지 10 행과 같은 설정임을 artifact 로 증명 불가 | `git diff 2965d04..9053b21 -- bms_balancing/`: dd_eval 대조·`verify noise`·§1-11 만, degeneracy 경로 무변경; 이후 `bms_balancing/` 무변경. 4 루트 커밋: `2965d04`/`9053b21`/`d471e62`/`1d671ce`(→`3fdeaa2`) | 서술만_바뀜 | §1-12 조건 7; `cmd_degeneracy` 가 `n_starts`·`seed` 를 JSON 에 기록 | `test_degeneracy_json_records_its_settings` |
| S3 | 폭이 하한이면 "겹침" 은 안전, "분리" 는 아님 — 뒤집힐 수 있는 쪽은 "파우치가 가른다" | 정의상 | 서술만_바뀜 | §1-12 겹침 표 아래 명시 | — |
| S4 | "13 행" 이 독립 관측처럼 읽힘 — 셀 3, fixedhc 3 적합은 같은 풀셀 자료 | — | 서술만_바뀜 | "13 적합" 으로, 문장 추가 | — |

### 4-2. 반증됨 (제외 사유)

| 가설 | 실측 | 결론 |
|---|---|---|
| 프로파일 격자가 관측 구름 힌트라 파우치 폭이 격자 끝에서 잘림 | 39 mode-행 중 격자 끝 = 1 (pouch 300_0147 LAM_PE HI). 격자는 constrained-extrema 힌트보다 넓고 최종 폭은 격자 안쪽 | 기각. LLI 헤드라인 무관 |
| 탐색 예산 불공정 (n_accepted 원통형 3x) | ext.n_points 28~81 로 같은 자릿수, 프로파일 격자 22·n_starts 3·tol 1 %·w_dqdv 0 전 루트 동일. n_accepted 172~210 vs 47~71 은 넓은 분지의 결과 | 기각 |

### 4-3. 이 세션에서 잡은 자체 결함 (재발 방지 테스트 포함)

`git_dirty` 가 31 meta 전부 true(untracked 산출물 때문 → 정보 0) → `scripts/provenance.py`, `--untracked-files=no` · `test_git_state_ignores_untracked_artifacts` / 문서 6 개가 "한 상태 300_0009" 를 §1-10 뒤에도 들고 있었음 → `test_docs_do_not_claim_a_narrower_state_scope_than_out` / 1차 요청문 clone 브랜치가 본체였음 → `test_review_request_clones_the_branch_that_owns_bms_balancing` / `_bands` 가 `_v2` 를 건너뛰고 옛 판을 읽음 → `compare_states.load_degeneracy` 재사용 / 문서 숫자 검사가 `"0.46" in txt` 여서 표 칸을 바꿔도 통과 → 표 파싱·칸별 대조 / `fixed_hc.py scan` 이 `st[:-0]` 로 상태 이름을 뭉갬 → `test_fixed_hc_scan_parses_state_names_in_both_sources`.

## 5. 닫지 않은 것 — 신뢰 경계

| # | 무엇 | 왜 못 닫나 | 닫는 길 |
|---|---|---|---|
| U1 | dQ/dV 항의 `compute_dqdv_rmse_blend`·`build_peak_weights_local` 은 **전사** — 그 항만 「우리 전사 ↔ 우리 포팅」 대조 | 원본 파일 안 로컬 함수, 밖에서 호출 불가 | 규진팀이 눈으로 대조 (`FOR_BMS_TEAM.md` §8) |
| U2 | pOCV export 가 원자료인지 필터본인지 | 한 곡선으로는 원리적으로 못 가름 (§7-4, 4 회 시도) | 규진팀 export 하나 |
| U3 | §1-12 의 남은 차이가 셀 물성인지 원통형 pOCV 자료 품질(잡음·분해능)인지 | 대조가 배제한 것은 반쪽전지 대체 **하나** | 원통형 계측 조건(전류·샘플 간격·필터) |
| U4 | 파우치 100·200·300_0009 의 starts/seed provenance (S2) | 코드 등가는 diff 로만 | `STATES='100 200 300_0009' ./scripts/run_states.sh` 재실행 ~2 h — 제안, 미실행 |
| U5 | fixedhc 의 B축(`matrix`)은 대조 아님 — `step_005C` 미고정 (`fixed_hc.py check` 가 잡음, fixedhc step_005C 행 = pouch 행 숫자까지 동일) | A축은 GITT 로 돌아 유효 | `fixed_hc.py make` 는 전 소스를 누름; 재실행 시 자동 해소 |
| U6 | 모든 폭은 **하한** (`is_lower_bound: true`); 1 % 띠는 신뢰구간이 아님 (부적합/σ = 267, χ² 기반 구간이 거짓으로 좁아짐) | 방법의 성질 | 반복 측정 또는 원자료 σ |
| U7 | 기준(pristine) 이동과 대상 이동의 분리 (B4-4) | 미착수 | — |
| U8 | held-out 예측 없음; 원통형 300_0147 없음; 원통형 3 행 `a_NE=ub` 경계 | 자료 | — |
| U9 | §5-2 (a)·(b) 는 크기 비교 — 방향 일치 미검. (a) 는 정규화 뒤 값 (300_0009 는 용량 −27 % 와 섞임; 깨끗한 행은 200: 용량 −0.79 %, 35.77 mV) | — | 방향 검사 추가 가능 |

## 6. 리뷰어에게 — 세게 칠 자리와 질문

1. **S1 의 정규화가 맞는 정규화인가.** 반폭/best_obj 로 나눴다. 대안은 절대 tol 로 4 루트를 재실행하는 것(수 시간). 8.0x 가 서는가, 아니면 다른 정규화에서 무너지는가.
2. **§1-12 대조의 강도.** 용량 −0.79 % 인 상태 200 에서 음극 모양 35.77 mV 를 pristine 으로 눌렀을 때 LLI 반폭 +0.03 %p. 이것으로 "대체는 원인이 아니다" 가 서는가. 반례가 있다면 어떤 조작이 더 강한가.
3. **S3 의 비대칭을 문서가 충분히 지고 있는가.** "파우치가 사이클을 가른다" 가 하한 위의 주장임을 §1-12 밖(§7-3, FOR_BMS_TEAM)에서도 지키고 있는지.
4. **U3 을 "셀 차이" 로 읽히게 쓴 문장이 남아 있는가** — `FINDINGS.md`·`INTRO.md`·`FOR_BMS_TEAM.md`·`HANDOFF_TO_GATE.md`.
5. **§5-2 의 인과 서술** — "γ 표현력 부족 → 차이가 a_NE·b_NE 로 → 그것이 LAM_NE" 는 산술(`LAM_NE` 정의)과 크기 비교뿐. 실제로 그 경로로 새는지 보이려면 무엇이 필요한가.
6. 결정이 갈릴 수 있는 선택(되돌릴 수 있음): `fixed_hc.py check` 는 판정만 하고 exit 2 — 실행을 막지 않는다 / `compare_states` 는 소스 혼합을 **경고**만 한다 / drift 테스트는 취소선·인용을 검사에서 뺀다.

## 7. 결론 문장 — 이대로 서는가 (현재 판, 원문은 `FINDINGS.md`)

1. §0-1: 포팅의 forward model 은 원본과 같다 (192 값 ≤ 4.04e-12, `w_dqdv` 항은 전사 조건). 최적화 절차 차이의 상한 0.17 %p. 그 위에서 "이 경계·seed·목적함수로 적합하면 Si 곡선·반쪽전지·미분항 선택에 따라 LAM/LLI 가 움직인다" — 통계적 정확도·전역 최적성·신뢰구간은 확립하지 않음.
2. §2-1: 97 행의 강한 음수 LAM_NE 는 **산술적으로** 「대상만 상한, 기준은 자유」에서 나온다 — 상관이 아니라 인과.
3. §1-10: 파우치 4 상태에서 LAM_NE 최광 · LLI 최협 (절대 폭 %p 로만; 상대값은 100 에서 뒤집힘).
4. §1-12: 이 순위는 **파우치의 성질이지 일반 명제가 아니다.** 원통형에서는 LAM_PE 만 사이클을 가르고 LAM_NE·LLI 는 이웃 상태 구간이 겹친다. 반쪽전지 대체는 원인이 아니다(0.5~5.2 %). 13 적합 전부에서 LAM_NE 는 최협인 적 없고 LAM_PE 는 최광인 적 없다.
5. §5-2: γ 는 측정된 음극 모양 변화의 3~16 % 만 표현한다.

## 8. 실측 첨부

### 8-1. `compare_states.py` (여기서 실행, `abfed8b`) — A축

```
[pouch] out                       LAM_PE          LAM_NE            LLI
  100       GITT          5.99±0.29      -0.04±1.06       3.98±0.29   대상 b_PE=ub
  200       GITT          6.42±1.21       4.09±1.80       8.13±0.43
  300_0009  GITT          6.36±1.43       7.90±1.80      15.70±0.54   (_v2)
  300_0147  step_005C     8.03±1.12       5.11±1.32       9.88±0.50   기준 a_NE=lb
[fixedhc] out/cells_pouch_fixedhc
  100       GITT          3.33±1.32      -0.41±1.54       4.90±0.49
  200       GITT          6.90±1.29       4.09±1.64       8.49±0.46
  300_0009  GITT          7.42±1.54       7.96±1.78      16.20±0.58
[c168] out/cells_c168
  100       GITT          0.59±1.30       3.25±3.96       3.95±4.12
  200       GITT          5.46±1.31       7.30±6.89       8.01±6.07
  300_0009  GITT         11.98±1.15       2.30±4.35       5.72±4.82   대상 a_NE=ub
[c171] out/cells_c171
  100       GITT          1.90±1.48       8.05±5.66       6.62±5.25
  200       GITT          9.33±1.34       6.55±4.08       7.70±4.68   대상 a_NE=ub
  300_0009  GITT         15.92±1.23      12.11±1.92      13.84±2.77   대상 a_NE=ub
```
겹침/분리(이웃 상태 쌍 4+4, 근최적 구간 [min,max]): pouch·fixedhc — LAM_NE 분리 4/4 · LLI 분리 4/4 · LAM_PE 겹침 3/4; c168·c171 — LAM_PE 분리 4/4 · LAM_NE 겹침 4/4 · LLI 겹침 4/4. 재현: `test_section_1_12_ranking_and_overlap_come_from_artifacts`.

### 8-2. `fixed_hc.py check` (사용자 기계, 2026-09-11) — sha256 앞 16자리

```
pouch_fixedhc  GITT: 100 200 300_0009 pristine 전부 2c4a5b692041ee86  → 고정됨
pouch_fixedhc  step_005C: 5 상태 5 해시 (e8bf303c… 8dd25df7… 5dfeb9ed… ce3b5f72… 445f164c…) → 상태마다 다름  ⇒ U5
원본          GITT: 5a397e69… e81325a8… 65570dc9… 2c4a5b69…(pristine) → 상태마다 다름  (판정기 생존 확인)
```

### 8-3. MATLAB 대조 (사용자 기계, 2026-09-10, 툴박스 설치 후) — `FINDINGS.md` §1-7·§1-8

앵커 14: ≤ 3.62e-16 · `dv_PE_0p5` 1.36e-13 · `dv_NE_0p5_0p25` 6.03e-14 · `rmse_pocv` 4.35e-15 · `rmse_dvdq` 2.84e-14 · `rmse_dqdv` 2.90e-12 · `rmse_dqdv_w` 4.04e-12 (각 32 값). 툴박스↔shim: `quantile` 0 · `findpeaks` 0 · `sgolayfilt` 1.33e-13 · `rmse_dqdv` 1.78e-12.

### 8-4. `ne_shape.py` (사용자 기계, 2026-09-11) → `out/ne_shape_GITT_Li.csv`

```
state      cap_delta%   γ       (a)측정 mV  (b)γ mV  (b)/(a)  (c)max  (c)rms  max@x  |Δ|>50mV
100          -7.53   0.2935     23.94      0.64    0.03    136.0   24.1   0.020   4.0 %
200          -0.79   0.3124     35.77      5.76    0.16    112.1   19.3   0.020   3.2 %
300_0009    -27.29   0.2397    119.34     18.17    0.15     70.5   21.7   0.063   4.2 %
```

## 9. GO 이후 / NO-GO 이후

GO: `FOR_BMS_TEAM.md` 를 규진팀에 전달 (질문 2 개 포함: pOCV 원자료 여부, 전사 함수 2 개 대조). 보존: `abfed8b` 의 `out/` 전체 + `.meta.json`, 이 요청문, 리뷰 응답.
NO-GO: 발견마다 `/finding` — 반례를 RED 테스트로 먼저 고정하고 고친다. 반례는 `tests/test_review_findings.py` 에 그대로 들어간다.
