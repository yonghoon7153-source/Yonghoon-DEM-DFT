# Codex 발송 프롬프트 — REIL C4-0b1 결과 검토 (배열 · 규칙 봉인 + H 핵심) · 2026-10-13

> 근거: 상태 문서 §46 (사용자 "b로 진행" — C4-0b 를 둘로 · 0b1 착수) · §47 (결과).
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-0b1 을 승인 범위대로 한 번 실행했습니다. 검토해 주세요. 브랜치 `claude/14-gate-code-review-9qkx05` 의 최신 HEAD (이 발송문이 든 커밋) 를
기준으로 보시면 됩니다. 실행 기록 커밋은 `0039b96b` 이고, 착수 HEAD 는 `d800acaf` 입니다.

## 1. 범위와 승인

- 확인 요청 `bms-balancing/docs/REIL_C4_0B_CONFIRMATION_REQUEST_20261013.md` 의 안 B. 사용자 원문 "b로 진행" (상태 §46).
- **C4-0b1** = 봉인 넷 (profile Sobol 2 · 동시 Sobol 16 · label → seed 표 · 규칙 / label 형식) + H 핵심 (목적 J_V · J_D · ρ · J_V^s · Phase A · 결합 ρ ·
  증인 분류 · 정확 잔차 · 문턱 · 공통 갱신).
- 배정: identity 60 · RED 600 · GREEN 600 · 배열 240 · 건조 300 = 계산 1,800 s · 작업 4 h · 자동 재시험 0.
- C4-0b2 (Phase B · H4 대조 · ray · 표지) 는 이 결과 뒤 사용자 확인. 자료 실행 (C4-E / A / B) 은 별도 승인.

## 2. 실행 (원문 `bms-balancing/evidence/reil_c4_0b1_20261013/`)

| 단계 | 배정 | 실측 | rc | 결과 |
|---|---|---|---|---|
| 01 identity (C4-0a 와 같은 스크립트 · 인자) | 60 s | 5.950 s | 0 | ok · problems [] |
| 02 RED (새 시험 · 골격) | 600 s | 3.884 s | 1 | 51 실패 · 0 통과 — 51 건 모두 골격 `scripts/reil_c4_h.py:24` 의 NotImplementedError |
| 03 GREEN (새 시험 · `-rP`) | 600 s | 17.304 s | 0 | 51 통과 · stderr 0 B |
| 04 배열 봉인 | 240 s | 5.597 s | 0 | `bms-balancing/reil_c4_arrays_0b1_20261013/` · MANIFEST `d122117f4b9dc70988b8636be7f2de91fa8e285dfff7c5340dcebac2e1f24b33` |
| 05 무자료 건조 | 300 s | 13.043 s | 0 | `05_dryrun/PLAN.json` · `05_dryrun/SYNTHETIC_SAMPLE.json` |

- 계산 합 45.778 s / 1,800 s. 끝 기록 1,776.9 s / 14,400 s 는 커밋 · push · 문서 작성 전 snapshot 입니다 (`06_end.json`).
- 시험 `tests/test_reil_c4_0b1.py` (`6afd6d98…`) 는 RED · GREEN · 끝에서 바이트 같습니다. 구현은 골격 `e2295942…` → `676b0847…`.
  e3a · monitor · c5 · p0 · c6_profile 은 고치지 않았습니다 (세 시점 sha 동일 — `02_red` · `03_green` · `06_source_sha256` 파일).
- RED 와 GREEN 사이 정적 검토만 했습니다 (ast · symtable · 모듈 속성 대조 — 대상 코드 실행 0). 실행기 `00_step_runner.py` 는 C4-0a 보완 실행기에서
  증거 경로 · scratch · env 두 이름만 바꿨습니다.
- porcelain 시작 · 끝 기록은 그대로 둡니다 (새 증거 · 배열이 untracked 로 보임). clean tree 라고 부르지 않습니다.

## 3. 봉인 (부속 B §2-1 첫 행)

| 묶음 | 수 | 파일 | 정의 |
|---|---|---|---|
| profile Sobol 2 | 10,332 label | `profile/<단위>.npy` × 77 (행 = label × 2 · 열 3) | 단위 77 × 좌표 {m_P, m_N, LII} × 격자 41–45 점 · 자유 변수 상자 (A §3-3 소거) |
| 동시 Sobol 16 | 134 label | `simultaneous/<단위>.npy` × 71 (행 = label × 16 · 열 4) | τ ∈ {0.02, 0.05} · 상자 P × N × d_P × d_N (A §3-4) · PRIOR_INCOMPATIBLE 20 (단위 · τ) 제외 · 앞 12 사용 |
| label → seed 표 | 10,466 | `LABEL_SEED_TABLE.json` (`64c69603…`) | seed = `int(sha256(label)[:8], 16)` (A §3-6) |
| 규칙 · label 형식 | 1 | `RULES.json` (`8c1d0632…`) | label 형식 · 토큰 표 · 격자 · Sobol 호출 · 부속 A · B 의 순회 · 동률 · 대체 · 중복 · 부족 · 동시 · seed 원문 (줄 범위 + 문서 sha256) |
| 색인 | — | `INDEX.json` (`b0fd41a0…`) | label · seed · 단위 · 행 범위 · 블록 raw float64 sha · t (분수 · float) · 상자 · P0 격자 제외 기록 |

- 생성 호출 = C6 봉인 `sobol` 과 같음: `qmc.Sobol(d, scramble=True, rng=<seed>).random_base2(m)` → `qmc.scale`. 시험이 Phase A 봉인 배열과 바이트 대조합니다.
  생성 경고는 봉인 중단입니다.
- `check_h_arrays`: MANIFEST 를 명시 sha 로 인증 → 파일 목록 · 바이트 → P0 sha → 99 칸 사전표 재계산 대조 → **배열 전부 재생성 대조** → INDEX · 표 · 규칙 기록 재생성 대조.
- 봉인하지 않은 것: 적응적 시작점 (profile s1 · s2 · 동시 상위 증인) — 쓰는 실행 직전에 봉인합니다 (B §2-1 둘째 행 · C4-0b2).

## 4. H 핵심 — 등록 절과의 대응 (`bms-balancing/scripts/reil_c4_h.py`)

| 함수 | 등록 | 시험 |
|---|---|---|
| `label` · `seed_of` · `units` | A §3-6 · 확인 요청 토큰 · 단위 77 | test_01 · 02 |
| `t_range` · `profile_grid` · `free_box` · `sim_box` · `array_plan` | A §2-5 · §3-3 · §3-4 · P0 대조 | test_03 · 04 · 05 |
| `jv_jd` · `rho` · `jd_gate` | v2 J_V · J_D (f4 의 그들 마스크) · A §1-3 | test_06 |
| `crossings` · `endpoint_gate` · `v_full` · `j_vs` | B §3 · A §4-2 · §4-3 · v2 §5 | test_06 |
| `exact_residuals` · `feasibility_class` · `witness` · `termination` · `active_set` · `classify` | A §2-1–§2-3 · B §1-2 · §2-5 | test_07 · 08 |
| `load_phase_a_arrays` · `phase_a_tasks` · `run_phase_a` · `phase_a_summary` · `rho_denominators` | A §3-1 · §3-2 · §2-3 · §2-4 | test_08 |
| `thresholds` · `reading` · `common_update` | A §1-1 · §1-2 · §2-2 마지막 행 | test_09 |
| `seal_h_arrays` · `check_h_arrays` · `rules_record` · `dryrun` · `main` | B §2-1 · C4 v2 §4-3 | test_05 · 10 |

`run_phase_a` 는 `reil_c4_monitor.supervise` 의 task_fn 계약 (task · ctx · notify · progress) 입니다. 지역 오류는 행 · 우리 코드의 예외는 `mon.Structural` 입니다.

## 5. 건조 결과

- Phase A 계획 9,856 = 1 파 66 단위 × 128 (8,448) + 결합 ρ 2 파 11 × 128 (1,408) · run_id 0–63 seed 0 · 64–127 seed 1.
- **P0 끝점 게이트: 11 셀 모두 H4 끝점 수용 실패.** P0 기록의 V_first − 2.0 V = 0.3365–0.6097 V (ν = 0.01 V). V_last 쪽은 #4 · #6 · #7 · #8 만 ν 안입니다.
  A §4-3 대로 그 셀의 H4 = UNFIT → H4 22 단위 전부 UNFIT · 게이트 뒤 Phase A 7,040. ν 는 P0 전에 정한 폭이고 끝점을 본 뒤 바꾸지 않으므로 (A §4-3)
  고치지 않았습니다. 이 귀결은 P0 기록 (2026-10-06) 만으로 계산할 수 있었으나 이번 건조가 첫 계산입니다.
- σ̂_v 11 셀 모두 유한한 양수 · J_D 빈 마스크는 자료 쪽이라 C4-A 에서 판정.
- 합성 표본 20 실행 (해석식 곡선 · maxfev 50 · 합성 σ̂_v 0.001 — 증거 · 비용 근거 아님): 목적 넷 + 결합 ρ 경로 통과 · J_V A2 2 실행은 util 오류 →
  SOLVER_ERROR (지역 분류) · 나머지 유효 · 공통 갱신 · 문턱 계산.

## 6. 밝힐 것 — 해석 · 구현 선택

1. **RED 는 골격 대상**이라 51 건이 모두 NotImplementedError 입니다. 이름은 있고 동작은 없는 상태의 실패라, 각 시험이 틀린 구현을 잡는지는 이 RED 가 보이지 않습니다.
2. "label-seed 배열" = label → seed 표 (§46 · 다시 묻습니다). "41 등분점" = 양 끝 포함 41 점 (확인 요청의 상한 46 = 41 + 5). 격자점은 정확 유리수 →
   float · 범위 밖은 정확 비교 · 중복은 float 비교 (41 등분점이 먼저).
3. J_V^s: 실험 쪽 V_exp(s_k) = `V_exp_interp[k]` (Q_exp_interp = linspace(0, Q_exp_max, 100) 이 곧 s 격자 · 보간 없음). 모델 쪽 V_sim(s_k) =
   V_full(Q_a + s_k·span) 직접 평가 (격자 보간 아님). V_full 은 objective_fun 173–189 와 같은 구성을 다시 쓴 것이고 합성에서 그들 `Vf_sim` 과 비트 동일입니다.
   그 슬라이스가 2 점 미만이면 예외 대신 비유한 (사유 기록).
4. 재평가 중 util 예외 → `invalid:NONFINITE` + `reeval_error` 기록 (등록 이유는 셋 · C5 의 REEVAL_ERROR 는 C5 한정).
5. termination: 성공 · MAX_EVAL · MAX_ITER 밖 status (INFEASIBLE_ERROR · LINALG_ERROR) → `solver_error` + 원 status. 증인은 따로 판정합니다.
6. 끝점 게이트 동률 (V_first = 2.8 V) 은 c_a = 2.0 — 등록에 없는 규칙이나 그 점은 어차피 수용 실패입니다. 비교는 float 의 정확 유리수로 합니다.
7. 오류 분류는 C5 규칙에 '우리' 파일 집합만 넓혔습니다 (이 파일 · e3a · monitor · c5).
8. ρ 는 성분 하나라도 비유한이면 nan (Python `max` 가 nan 을 숨기는 것을 막음). 공통 갱신은 최종 > 갱신 전이면 중지합니다.
9. RED / GREEN 은 C4-0 전체로 각 3 회가 됩니다 (0a · 0b1 · 0b2).

## 7. 검토 질문

- Q1. 봉인 넷의 형식 · 개수 · 대조 (§3) 가 B §2-1 의 "맞춤 전 봉인" 으로 충분한가. label → seed 표 해석 · 토큰 표를 수용하는가.
- Q2. "41 등분점" 읽기와 격자 생성 규칙 (§6-2) 을 수용하는가.
- Q3. J_V^s 의 구현 선택 (§6-3) 이 v2 §5 · A §4 · B §3 과 맞는가.
- Q4. §6-4 · §6-5 의 분류 (재평가 예외 → NONFINITE · 비성공 status → solver_error) 를 수용하는가, 아니면 다른 이름이 필요한가.
- Q5. **H4 끝점 게이트 (§5)** — P0 기록으로 11 셀 전부 H4 UNFIT 이라는 읽기가 맞는가. 맞다면 C4-0b2 의 H4 대조 (R1–R3 · 음성) · ray 구현을 등록대로
  둘지 (적용 셀 0), 범위에서 뺄지에 대한 의견.
- Q6. 골격 대상 RED (§6-1) 를 이 단계의 RED 증거로 수용하는가.
- Q7. C4-0b1 을 종결할 수 있는가. 남는 차단이 있으면 무엇인가.

## 8. 경계

자료 (xlsx · pkl · 노트북) 개봉 0 · 실제 셀 맞춤 0 · Phase B · H4 대조 · ray · 표지 0 · 전체 suite · full C6 check · 환경 재구축 · 설치 0 · COMSOL 0.

---
