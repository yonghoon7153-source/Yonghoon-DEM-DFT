# Codex 재검증 요청 (3차) — RGLR-01 ~ 03 · WEB-03 · LHS-33 수정 + 194 인계 LW 제외 (2026-10-05)

- 기준 판정: `docs/reviews/codex_review_rgl_reverify_20261005.md` (핀 `bf4fb6aee` · **HOLD** · 새 P1 없음 · §9 최소 잔여 해제조건 = RGLR-01 · 02 · 03).
- 이번에 고친 것: §9 의 셋 + 판정문 Q1 · Q2 의 `WEB-03` (1저자 비준 = Q1 + Q2 최소) + Q7 의 `LHS-33` 좁은 amendment + Q5 의 194 인계 LW 제외.
- 핀 = `dbe0f076d7b948b8ebcfa85a02a391125b104fe2` (브랜치 `claude/sdcp-dem-manuscript-si-pqwtv8` · 수정 전부와 이 요청서를 담은 커밋 — 그 뒤 커밋은 이 줄에 SHA 를 적은 것과 믹서 작업뿐 · 망 · 입자 응력 코드 변경 없음).  사이의 `a6f950227` (믹서 보조 판독기) 은 이 검토 범위 밖이다.
- 1저자 비준: *"비준이야"* (10-05 밤 · 수정안 1–4 전부 — `LHS-33` 은 제안문의 "무효 입력만 빈칸 · 사유" 안).

## 1. 패치 (오래된 순)

| 커밋 | 원장 | 내용 | 파일 |
|---|---|---|---|
| `af9e6b15f` | RGLR-03 · RGL-06 잔여 · LHS-33 | 파서 `load_atoms_raw` 가 c_strs 세 열의 **존재 · 파싱 실패를 보존** (세 열 전무 = unavailable 그대로 · 일부 열 · 빈칸/NaN · 문자열 · Inf · 반경 무효 = 그 입자 세 키 NaN + `c_strs_invalid` 사유 · 옛 파서는 일부 열이면 KeyError) · LW = 어느 키든 있음 ↔ 전부 완전을 따로 → `FAILED (invalid_input)` · 옛 σ_VM `calc_von_mises_stress` 계약 `v2-invalid-null` (정상 입력 = 정의 · 수 · 키 불변 + `stress_cv_status: computed` · 무효/미정의 = None + `stress_cv_status` (`unavailable_no_c_strs` · `invalid_input` · `undefined_zero_mean`) + `stress_cv_reason`) · 등급 `__sigma_vm_cv_pct` 가 상태를 따른다 · 그림 · CSV · 표 재생성 · 감사 · 웹앱 사례 · 그룹 · 보고 · 툴팁 같은 묶음 · 계약 상수 = `scripts/metrics_json.py` 한 곳 | `scripts/analyze_contacts.py` · `dem_analysis_core.py` · `metrics_json.py` · `grade_engine.py` · `generate_comparison_plots.py` · `rebuild_tables_from_metrics.py` · `lhs_stress_constriction_audit.py` · `test_love_weber_stress.py` · 웹앱 `app.py` · `single.html` · `group.html` · `test_stress_lw_labels.py` |
| `9fe8ba0bf` | Q5 (LHS-29 · RGL-06) | 194 인계에서 LW 열 **명시 제외** — `WA_EXCLUDED` 패턴 `stress_lw_.+|stress_cv_lw(_nowall)?|stress_ratio_.+_lw(_nowall)?` · 사유 `frame_unverified` (parse_liggghts 가 TIMESTEP 을 버리고 atom · contact 를 따로 고른다) · CLI 가 `<인계>_excluded.tsv` 를 쓴다 · 옛 σ_VM 열은 패턴에 안 걸림 · 같은 입력 130 · 64 인계표 · 열 사전 **바이트 동일** (묶음 `contact,percolation` · 다섯 묶음 둘 다) | `scripts/lhs_design_dataset.py` |
| `e03c0a84b` | RGLR-01 · 02 · RGL-08 잔여 · WEB-03 | 공용 기술 검사 `tau_flux.ion_record_problem` (정지 계약 ③ · τ 인계 소비자가 **같은 함수** · 띠 · 퍼콜 · 연속체 게이트 앞) · 두 σ 표현 항등식 `tau_flux.sigma_identity_tol` · 생산자: 관통인데 못 푼 채널 (이온 · 전자 · 열) = **failed** (`_channel_solve_failure` · 상태 필드만) → 게시 게이트가 일반 · 정지 경로 모두에서 막는다 · 승격 한 거래 `publish_network_candidate` (동기 예외 = 되돌림 · failed 반환) · 실패 어휘 하나 (network_attempt.json v2) · 웹앱 τ 상태 행 (기술적 실패 ↔ 과학적 HOLD) · "최근 재계산 실패" 행 | `scripts/tau_flux.py` · `network_conductivity.py` (상태 필드만) · 웹앱 `pipeline_service.py` · `app.py` · `single.html` · 시험 넷 |
| `dbe0f076d` (핀) | 원장 · 탐침 재실행 기록 | RGLR-01 ~ 03 · RGL-06 · 08 · WEB-03 · LHS-33 → claimed_fixed · 탐침 재실행 기록 `docs/reviews/codex_rglr_fix_probe_rerun_20261005/` (전 · 후 JSON · 기록된 단언 · 실행기) | `docs/reviews/findings.json` · 위 폴더 · CLAUDE.md · 진행 기록 |

## 2. 판정문 해제조건 · Q 대응

| 항목 | 무엇을 했나 | 우리 시험 (수정 전 생산 코드 → 수정 뒤) |
|---|---|---|
| §9-1 RGLR-01 | 기술적 입력 검사를 **띠 판정 앞**에: computed = σ_ratio · σ_dim 유한 양수 · 관통 분율 (0, 1] · σ₀ 있음 · valid_zero = RGL-02 의 증명된 비관통 조합만 · not_computed = solver_guard · 그 밖 = `invalid_input` (NOT_COMPUTED) · L1/L2 도 건너뛰지 않는다 · 정상 L1 · L2 · 비관통은 그대로 수용 | `test_tau_flux` 37/51 → **51/51** (A6 · C3 · G2 · K6 · K7 · L1 · L2 · L2b · L4 · L4c · L5–L8) · `test_pipeline_provenance` 251/265 → **265/265** (실 생산자 `_CLIRunner` · 모드 파일 · legacy · dual 함께 변조) · `test_tau_handover_status` 22/32 → **32/32** |
| §9-2 RGLR-02 | `|σ_dim − 1000·σ₀·σ_ratio| ≤ 5e-7 + 1000·σ₀·5e-9 + 16ε(|σ_dim| + 1000·σ₀·|σ_ratio|)` — 생산자가 같은 미반올림 q* 에서 q = round(q*, 8) · σ_dim = round(q*·σ₀·1000, 6) 을 만든다 (두 반폭) · ε 항 = 생산자 곱의 이중 반올림 · numpy round · 소비자 곱셈.  σ₀ 는 반올림 없이 실린다 (`d66fd1448` 부터 · `git log -S` 확인) · 온도 런도 생산자 자신의 σ₀ → σ₀ 반올림 항 없음 · 두 모드 · 두 τ 를 같게 강제하지 않는다 | 생산자 형식 표본 20,000 (σ_ratio 1e-6 – 1.5 · 25 °C 와 −30 – 120 °C · Ea 띠 · numpy · Python 반올림) · 작은 σ 침대 · 60 °C 런 = 수용 / 비만 ×4 · 차원값만 ×4 · 허용폭 1.001 배 = 거부 |
| §9-3 RGLR-03 | 위 `af9e6b15f` (파서 보존 · 함수 any ↔ all) | `test_love_weber_stress` 87/118 → **118/118** (실 CSV → `load_atoms_raw` → LW: 정상 · 세 열 전무 · 일부 열 · NaN · 문자열 · Inf · 틀린 virial · NaN 이 가린 틀린 virial · 직접 dict `sigma_xx` 만 없음) · `test_stress_lw_labels` 51/70 → **70/70** |
| Q1 WEB-03 | 관통 풀이 실패 채널 = failed → 일반 경로도 Stage E 앞에서 거부 · 비관통 · 상 부재 = 유효 null 그대로 · 정지 경로의 실패 단계는 정지 계약 → 망 솔버 내용 검증으로 한 단계 앞당겨짐 | provenance: 채널별 spsolve 주입 (이온 · 전자 · 열 · `_CLIRunner(break_channel=…)` · 기존 서명 불변) · 사슬 시험 두 단언 갱신 (8/10 → **10/10**) · 원시 해 불변 = `test_network_boundary_rule` ⑨ (eedada5d3 와 float.hex 동일 · 9/9) |
| Q2 WEB-03 (최소) | (a) 승격 = 한 거래 (full_metrics 사본 copy2 → 도장 → full_metrics (`atomic_write_json`) → 최근 시도 success) · 도중 동기 예외 = 사본을 `os.replace` 로 되돌리고 후보를 치운다 (실패한 쓰기 함수를 다시 쓰지 않는다) · 옛 세대 6/6 · 첫 실행 = 활성 세대 없음 · 최근 시도 failed (`publish_exception` · 예외 종류 · 입력 id) · 필수 단계 **failed 반환** (KeyboardInterrupt · SystemExit 는 되돌린 뒤 다시 던짐).  (b) 실패 어휘 하나: 솔버 · lock 실패도 full_metrics 를 **안 건드린다** (옛: `network_solver_status=failed` · `stale_after_failed_retry`) → `network_solver_status` = 활성 세대 상태만 · `network_attempt.json` v2 (`latest_attempt_status` · `failure_kind` solver/lock/candidate_rejected/publish_exception · `active_network_run_id` · `active_status` · `previous_generation_kept` · `input_digests` · 옛 키 유지) · v1 기록은 단계로 종류 추정 (`network_status_view`).  (c) 웹앱: "최근 재계산 실패 (사유) · 실패 종류 · 활성 세대 … 의 값" (활성 없으면 "활성 세대 없음") | provenance OSError 주입 → 옛 세대 6 파일 SHA-256 동일 · 첫 실행 · 배치 상태식 = failed (T12h) · 실패 기록 쓰기 실패 (T19b) |
| Q3 | 변경 없음 — 영 · 비유한 소산은 지금처럼 fail-closed | — |
| Q5 | LW 를 194 인계에서 명시 제외 (위 `9fe8ba0bf`) · LW 프레임 대응 미인증은 그대로 둔다 | `lhs_design_dataset --selftest` 278/281 → **281/281** · 130 · 64 인계표 바이트 동일 + `_excluded.tsv` |
| Q7 LHS-33 | 좁은 amendment (위 `af9e6b15f`) — 정상 zero CV (균일 양의 VM) 0.0 유지 · 0/0 · NaN · 결손은 None + 상태 · 등급 소비자가 상태를 따른다 · 원본 역사 파일 무변경 | 옛 함수와 정상 입력 비트 동일 (91 입자 합성 · real_14) · `lhs_stress_constriction_audit --selftest` 10/12 → **12/12** · 웹앱 등급 · 표 · 그룹 · 툴팁 (`test_stress_lw_labels`) |

수정 전 실패 수 = 최종 시험 파일을 수정 전 생산 코드 (`fde4a812c`) 에 돌린 수 (반례 먼저 · 규율 ②).

## 3. 판정문 탐침 재실행 — 우리 트리 (Linux · Python 3.11)

판정 묶음의 `docs/reviews/codex_rgl_reverify_review_evidence_20261005/probes/network_adversarial.py` · `docs/reviews/codex_rgl_reverify_review_evidence_20261005/probes/lw_replay.py` 를 **무변경**으로 돌렸다 — 끝의 결함 단언 (`assert`) 만 기록으로 바꿨다 (`docs/reviews/codex_rglr_fix_probe_rerun_20261005/rglr_after.py`).
전 (`fde4a812c`) · 후 (통합 트리) JSON 과 기록된 단언은 그 폴더에 있다.

| 경우 | 전 | 후 |
|---|---|---|
| positive · no_through · legitimate_band | done · done · done | done · done · done (τ² 10.984918916215547 그대로) |
| solver_failed_stop | failed | failed (한 단계 앞) |
| **solver_failed_general** | done | **failed** |
| **ratio_times4** | done (τ² 2.746…) | **failed** |
| **band_ratio_missing · nan · negative · band_fraction_above1** | done ×4 | **failed ×4** |
| rejected_retry_preserves_generation | failed · 옛 세대 동일 | failed · 옛 세대 동일 |
| **write_failure_after_stamp** | EXCEPTION · 옛 세대 다름 | **failed · 옛 세대 동일** |
| LW normal · two_dimers ×2 · finite_cstr · all_cstr_absent | OK | OK |
| LW nan_plate · isolated_nan_radius · inf_cstr_first · finite_wrong_virial · false_zero_force | FAILED | FAILED |
| LW true_zero_load | UNDEFINED | UNDEFINED |
| **LW nan_cstr_first · text_cstr_first · nan_hides_wrong_virial · partial_cstr_tuple** | OK ×4 | **FAILED (invalid_input) ×4** |

기록된 단언: 망 7/7 → 4/7 (안 서는 셋 = 결함 단언 75 · 76 · 77) · LW 8/8 → 6/8 (46 · 48).

## 4. 스키마 · 소비자 변화 (요지)

- τ: 사유 코드 `invalid_input` (NOT_COMPUTED · 사유 칸 `invalid_input: 세부` · `reason_code()`) · L1/L2 무효 입력 → NOT_COMPUTED (옛 BAND_FALLBACK) · L0 computed 의 무효 σ → `invalid_input` (옛 `solver_guard`) · `not_computed` 인데 σ 가 있음 → `solver_guard` (옛 OK · TAU-22 의 C3 를 대체).  RGL-02 이전 어휘 (`not_computed` + 분율 0) 를 쓰던 시험 고정구는 valid_zero 형식으로 옮겼다.
- 생산자 (`network_conductivity.py` · S3 봉인 모듈): 관통 FULL 풀이 실패 채널 = `failed` (옛 `valid_null`) — **상태 필드만**, 해 · σ 숫자 불변 → amendment 재봉인 대상.
- `network_solver_status` = 활성 세대 상태만 · `network_attempt.json` v2 · 목록 (`list_cases`) 덧붙임 필드 `network_active_status` · `network_latest_attempt_status` · `network_latest_attempt_failure_kind` · `network_stale_after_failed_attempt` · 투영에서 `last_network_attempt_run_id` 를 걷어냄 (grep 상 독자 없음).
- LW: 파서 `c_strs_invalid` · LW `invalid_input`.  옛 σ_VM: `stress_cv_contract` · `stress_cv_status` · `stress_cv_reason` · None.  인계: `WA_EXCLUDED` LW 패턴 · `_excluded.tsv`.

## 5. 남긴 것 · 한정

- **WEB-03**: 비동기 중단 (kill -9 · 정전) 의 원자성은 **없다** — 세대별 후보 디렉터리 + 단일 활성 포인터는 미구현 · 남는 `.publish_backup_*` 청소 없음 · 실패 기록 쓰기 자체가 실패하면 단계 로그에만 · 사전 검사 구간의 예상 밖 예외는 거래 밖 (fail-closed 로 썼고 관찰되지 않음).
- 일반 경로는 RGLR-01 · 02 검사를 다시 돌리지 않는다 — 생산자의 새 출력을 게시한다 (변조 반례는 정지 경로 · τ 소비자가 막는다).
- 저장 정밀도에서 0 으로 반올림되는 σ (σ_dim < 5e-7 ≈ σ_ratio < 1.7e-7 @25 °C) · 관통 분율 (≈ 30 만 노드 이상) = `invalid_input` — 현 코퍼스에 없다.
- 10-04 ~ 10-05 창의 옛 어휘 세대 (띠 규칙 있음 · RGL-02 이전) 는 이제 NOT_COMPUTED → 재풀이 필요 · WEB-03 창에 승격된 활성 세대는 `valid_null` 표지 그대로 (보존 경로).
- **LHS-33**: 표지 없는 옛 full_metrics 의 저장된 0 은 참 0 과 구별 불가 (커밋된 코퍼스 lhs130 · lhsx64 · case_master 163 에 `stress_cv` 0 없음 · 최소 ≈ 49–57 %) · 거의 정수압 입자의 VM 근호가 음수로 반올림되면 VM 0 (의도된 이탈 — 옛 코드 = 그 입자 NaN → 침대 전체 거짓 CV 0 · 옛 코드가 유한값을 내던 입력은 전부 비트 동일) · 층별 0/0 은 0 그대로 (비트 동일).
- **LW** 프레임 대응 (TIMESTEP · 파일 선택 · 타입 대응 · 벽 기하) 은 봉인하지 않았다 → 194 인계에서 제외만 했다 (Q5).
- 범위 밖: 실 Stage E 수치 · WSL 소형 통합 · real14 fixture 회귀 · 재봉인 · 194 실행 (Q6 순서 1 이후).

## 6. 질문

1. 일반 경로 (생산자의 새 출력 게시) 에 RGLR-01 · 02 검사를 다시 두지 않은 판단 — 생산자가 같은 해에서 두 표현을 만든다 — 에 동의하는가, 아니면 일반 경로 게시 앞에도 같은 검사를 요구하는가?
2. WEB-03 Q2 최소 (동기 예외 되돌림 + 한 실패 어휘) 로 Q6 순서 1–4 (WSL 소형 통합 → 범위 명시 → amendment 재봉인 → 194 배치) 에 들어가도 되는가, 아니면 세대별 후보 디렉터리 + 단일 포인터를 194 배치 **앞**에 요구하는가?
3. 항등식 허용폭의 `16ε(|σ_dim| + 1000·σ₀·|σ_ratio|)` 여유가 생산자 산술 (곱 · numpy round · 소비자 곱) 의 경계로 적절한가?
4. LHS-33 의 "VM 근호 음수 반올림 → VM 0" 이 좁은 amendment 범위 안인가?
5. 194 인계의 승인 범위를 ⑤⑥⑦ · 망 τ (LW 제외) 로 두고 Q6 순서 1 로 넘어가도 되는가?

## 7. 재현 (Linux · 리포 뿌리)

```bash
python3 scripts/test_tau_flux.py                     # 51/51
python3 webapp/test_pipeline_provenance.py           # 265/265
python3 webapp/test_tau_handover_status.py           # 32/32
python3 webapp/test_network_handover_chain.py        # 10/10
python3 scripts/network_conductivity.py --selftest   # 30/30
python3 scripts/test_network_boundary_rule.py        # 9/9 (⑨ 는 .git 필요)
python3 scripts/test_love_weber_stress.py            # 118/118 (real14 fixture 묶음 포함)
python3 webapp/test_stress_lw_labels.py              # 70/70
python3 scripts/lhs_design_dataset.py --selftest     # 281/281
python3 scripts/lhs_stress_constriction_audit.py --selftest   # 12/12
python3 webapp/test_closed_param_groupview.py        # 44/44
python3 webapp/test_tau_grade_unify.py               # 19/19
python3 scripts/test_rint_receipts.py                # 102/102
# 판정 묶음 탐침 (zip 을 푼 폴더):
CODEX_RGLR_PKG=<풀린 폴더> python3 docs/reviews/codex_rglr_fix_probe_rerun_20261005/rglr_after.py . <출력 폴더> new_network independent_lw
```
