---
title: ISU-UConn LFP/흑연 모사 열화 자료 + REIL 다목적 피팅 코드
description: "전극 원판 지름 (LAM 모사) 과 리튬화 상태 (LLI 모사) 를 설계해 만든 LFP/흑연 11 셀의 반쪽 · 완전지 곡선 (CC BY 4.0) 과, 반쪽전지 곡선의 질량 배율 · 용량 오프셋을 GA/NSGA 로 맞추는 MIT 코드. 우리에게는 α·β 창 맞춤과 같은 계열의 방법을 실측 '설계 참값' 에 대 보는 외부 검증 후보"
created: 2026-10-03
updated: 2026-10-06
type: entity
tags: [degradation, tooling, research]
sources: [raw/articles/2026-10-02-github-research-briefing.md, raw/repositories/2026-10-03-reil-uconn-moo-known-truth-table.md, raw/papers/li2026_half-cell-fitting-multiobjective-benchmark.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-mixed
---

# ISU-UConn LFP/흑연 모사 열화 자료 + REIL 다목적 피팅 코드

## 개요

- 코드 (MIT · "Copyright (c) 2026 REIL-UConn"): `https://github.com/REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics`
  · 끝 커밋 `1188c37` (2026-07-13 UTC). 파일은 노트북 1 · `util_LFP.py` · `LFP_Data.xlsx` (19 시트) · `results/` (pdf · pkl). 자동 시험 · 잠금 파일 없음.
- 논문 (README 인용 · **2026-10-05 열람** — C1-core 기록 `bms-balancing/docs/REIL_C1_CORE_SPEC_20261005.md`): T. Li 외, "Benchmarking half-cell model fitting approaches for lithium-ion battery degradation
  diagnostics", *eTransportation* 29, 100593 (2026) · doi `10.1016/j.etran.2026.100593`.
- 자료 (README 인용 — 자료 페이지 미열람): "ISU-UConn LFP/Graphite Emulated Degradation Dataset", *REIL Datasets* 6 (2026, CC BY 4.0).
  저장소 안 `LFP_Data.xlsx` 가 그 자료와 같은지는 대조하지 않았다.
- 1차 대조 원문: `raw/articles/2026-10-02-github-research-briefing.md` 하단 · 참값 표 · 목적 함수 원문: `raw/repositories/2026-10-03-reil-uconn-moo-known-truth-table.md`.

## 설계 참값 표 (노트북 셀 8 · 9 원문에서)

열화를 노화로 만들지 않고 **제작으로 모사**했다 — 전극 원판 지름 (LFP 12 · 15 mm · 흑연 12 · 16 mm) 과 리튬화 상태 시트 (SOC-10 ·
SOC-20 등). 이름표 · 시트 · 참값은 같은 순서의 세 목록이고, 결과 그림이 이 순서로 참값을 겹쳐 그린다.

| 이름표 | 시트 | 참값 (m_P · m_N · LII) |
|---|---|---|
| Fresh | 15-LFP 16-Gr Full-cell @ C_20 | 1 · 1 · 1 |
| LLI-1 | 15-LFP 16-Gr SOC-10 | 1 · 1 · 0.9 |
| LLI-2 | 15-LFP 16-Gr SOC-20 | 1 · 1 · 0.8 |
| LAM_PE-1 | 12-LFP 16-Gr SOC-100 | 0.64 · 1 · 1 |
| LAM_NE-1 | 15-LFP 12-Gr Full-cell @ C_20 | 1 · 0.56 · 1 |
| LAM_PE,LLI-1 | Full cell after FM SOC 0 | 0.64 · 1 · 0.64 |
| LAM_PE,LLI-2 | Full cell after FM SOC 10 | 0.64 · 1 · 0.58 |
| LAM_NE,LLI-1 | 15-LFP 12-Gr SOC-10 | 1 · 0.56 · 0.9 |
| LAM_NE,LLI-2 | 15-LFP 12-Gr SOC-20 | 1 · 0.56 · 0.8 |
| All mode-1 | 12-LFP 12-Gr SOC-10 | 0.64 · 0.56 · 0.58 |
| All mode-2 | 12-LFP 12-Gr SOC-20 | 0.64 · 0.56 · 0.51 |

- `[재현]` (우리 계산 · 저자 설명은 논문 미열람이라 확인 안 함): 0.64 = (12/15)² · 0.56 ≈ (12/16)² = 0.5625 → m 은 **원판 면적비**다.
  LII 0.58 ≈ 0.64 × 0.9 · 0.51 ≈ 0.64 × 0.8 → 두 효과를 **곱**으로 합쳤다.
- 열린 물음 (저장소에 설명 없음): 'SOC-10 · SOC-20' 이 어느 전극을 어떻게 전처리했다는 뜻인가 · 'Full cell after FM' 의 FM 이 무엇인가 ·
  'SOC-100' 인 LAM_PE-1 의 LII 가 1 인 근거 · 셀마다 한 개만 쓰는가 (셀 8 `cell_idx` 가 시트 안의 한 셀을 고른다) · 원판 타발 · 장전량의
  제작 편차. **참값은 명목 설계값**이지 측정값이 아니다.

## 방법 — 우리 α·β 창 맞춤과 같은 계열

- 결정 변수 넷: 반쪽전지 곡선의 질량 배율 `m_P` · `m_N` 과 용량 오프셋 `d_P` · `d_N` — `bms-balancing/` 하네스가 검증하는 규진팀 모델의
  `[a_PE, b_PE, a_NE, b_NE, γ_Si]` 에서 Si 블렌드 항을 뺀 꼴과 같은 구조다 (배율 = a · 오프셋 = b). 원전 계보는
  [[birkl-ocv-degradation-diagnostic]] · 창 매개변수 계보는 [[halfcell-window-parametrization-lineage]].
- 건강 매개변수 셋: `m_P` · `m_N` · `LII = (m_P · max_q − (d_P − d_N)) / max_q` — 오프셋은 **차이 하나**만 들어간다.
- 목적 함수 넷 (`objective_fun` 원문): f1 끝점 전압 (최댓값 오차의 제곱 + 최솟값 오차 RMS 의 절반 — 제곱과 RMS 가 섞인 합) · f2 V–Q
  곡선 MSE · f3 dV/dQ 첫 피크 위치 + 피크 주변 16 점 크기 (피크를 못 찾으면 1) · f4 dV/dQ 곡선 MSE (dV/dQ_exp < 0.4 구간만).
  조합 여섯 (셀 3): {f2} · {f1, f2} · {f3, f4} · {f1, f2, f3} · {f1, f2, f4} · {f1–f4}. 하나면 GA, 둘–셋이면 NSGA2, 넷이면 NSGA3 (pop 50).
- Pareto 에서 하나를 고를 때 `find_balanced_solution` — 목적별 min–max 정규화 뒤 이상점 (0) 까지 거리 최소.
- **일반 부등식 (2026-10-03 사전 검토가 짚음 · 이 절의 처음 판에 빠져 있었다):** GA · NSGA2 · NSGA3 모두
  `G = d_N − d_P + 1e-4 ≤ 0` (`util_LFP.py` 613 · 634 · 655) → `d_P − d_N ≥ 1e-4` → LII 식과 합치면 **`LII < m_P`**. 상자
  (`xl = [0.6, 0.5, 0.005, 0]` · `xu = [1.1, 1.1, 0.5, 1]`) 는 거꾸로 `LII ≥ m_P − 0.5/max_q` 를 건다.
- 반쪽전지 곡선: LFP · 흑연 각 12 mm C/20 (셀 6) · 명목 장전량 LFP 13.5 · 흑연 5.77 mg cm⁻² (셀 4) — 평형 OCP 가 아니라 저율 곡선.

## 판정 — 우리가 쓸 수 있는가

- **쓸 수 있다 — 외부 검증 후보로 가장 좋은 꼴.** 우리 합성 truth (PyBaMM · 참값을 정확히 앎) 와 실측 노화 자료 (참값 모름) 사이의
  빈칸 — **실측 곡선 + 설계 참값** — 을 채운다. 같은 4 변수 구조라 우리 식별성 측정 ([[fitting-degeneracy]] ·
  [[near-optimal-set-width-measurement]]) 을 그대로 얹을 수 있다. 라이선스 (코드 MIT · 자료 CC BY 4.0) 상 분석 · 인용에 걸림이 없다.
- **한계 (브리핑과 같은 방향 · 우리 말로):** (1) LFP 는 OCV 고원이 평탄해 양극 배율 · 오프셋이 끝점에만 기대는 화학이다 — 우리 NMC
  (Chen2020) 와 축퇴 구조가 다르다. (2) 모사 열화이지 자연 노화가 아니다 (SEI · 균열 · 불균일 없음). (3) ASSB 아님 · 미세단락 판별 자료
  아님 ([[isc-detection-vs-balancing-masking]] 의 근거로 쓰지 않는다). (4) 참값은 명목 설계값 · 조건당 셀 한 개로 보인다.
- **주의 — 남의 pickle:** `results/*.pkl` 는 열지 않는다 (역직렬화 = 임의 코드 실행). 비교가 필요하면 그들의 노트북을 버리는 환경에서
  다시 돌려 숫자를 만든다.
- RUN_SCOPE 무관 (읽기 · 별도 환경). 우리 코드에 들일 일이 생기면 그때 게이트 절차.

## 제안 실험 (후보 · 미착수 · 사용자 승인 뒤)

- **E1 — 외부 설계 참값 복원 + 근최적 집합 폭:** 11 셀 각각에 같은 4 변수 맞춤을 하고 (a) 최적점이 참값 (m_P · m_N · LII) 에 얼마나 가까운지,
  (b) 근최적 집합 (RMSE 가 최적 + ε 안) 이 참값을 **포함하는지 · 얼마나 넓은지** 를 잰다. PyProBE 실측 ([[pyprobe]]) 과 같은 판정 틀을
  실측 곡선에 처음 적용하는 셈이다. 목적 함수 (V–Q ↔ dV/dQ) 를 바꿔도 결론이 유지되는지가 그들 논문의 물음과 겹친다.
- **E2 — 형상만 ↔ 절대 용량:** 그들 LII 는 절대 용량 (mAh) 을 쓴다. 용량 열을 지우고 SOC 정규화 형상만 주면 무엇이 사라지는지 —
  [[np-lip-ocv-reparametrization]] 2 자유도 정리를 **실측 곡선**에서 확인한다 (합성에서는 PyProBE 형상만 시험으로 확인됨).
- **E3 — 그들 코드 그대로 재현:** 노트북을 버리는 venv 에서 다시 돌려 (GA/NSGA 무작위성 · 시드 미고정 확인) 결과 PDF 의 건강 매개변수가
  다시 나오는지. E1 의 비교 기준선.
- 셋 다 운영 · RUN_SCOPE 밖. 다만 E1 은 **성공 기준 (허용 오차 · 근최적 ε · 어느 셀을 볼지) 을 돌리기 전에 고정**해야 "맞으면
  성공" 이 되지 않는다 — 착수 승인 시 이 기준의 사전 검토 (Codex) 를 권한다.
- → 2026-10-03: 성공 기준을 고정한 프로토콜 v1 → 사전 검토 → v2 정정본 (아래 절). E1 · E2 · E3 는 v2 에서 H1–H4 · E3a/E3b 로
  다시 나뉘었다. 여전히 미착수.

## 사전 검토 (2026-10-03) — 프로토콜 정정 필요 · 실행 0

v1 프로토콜 (`bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL.md`) 의 Codex 사전 검토 판정은
`PROTOCOL_REVISION_REQUIRED_BEFORE_CONFIRMATORY_EXECUTION` (묶음 `bms-balancing/reviews/prereview_pybamm_reil_20261003/`). 방향 (E3 재현 → 점 추정 → 집합 → 목적 →
형상) 은 타당하고, 확인적 사전 등록으로는 R1–R6 정정이 먼저다. 정정본: `bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md`.

| 명목 행 (위 표) | 원 부등식 G 아래 | 근거 |
|---|---|---|
| LAM_PE-1 (0.64 · 1 · 1) | **PRIOR_INCOMPATIBLE** — ±0.05 로도 양립 안 함 | LII − m_P = +0.36 (검토자 발견) |
| Fresh · LAM_NE-1 · LAM_PE,LLI-1 | ~~**경계** (LII = m_P) — ±0.02 안에서 양립~~ **무여유 선 (d_P = d_N) 위 = G 밖** — τ = 0 배제 · ±0.02 양립은 `max_q ≥ 1/400` 조건부 (2026-10-04 v2 재검토 정정 · 아래 절) · LII 위쪽 폭은 제약이 자른다 | 우리 대조 · 정정은 재검토 |
| LLI-2 · LAM_NE,LLI-2 (m_P − LII = 0.2) | G 아래 안 · **그들 상자에서는** `max_q > 2.5` 이면 명목점 배제 | 우리 대조 · max_q 는 자료 (맞춤 전 P0 에서 확정) |

- 이것은 **허용 영역이 명목값을 배제하는 대수적 사실**이지 데이터의 편향 · 축퇴 관측이 아니다 — 판정표의 편향 · 축퇴 칸에 넣지 않는다.
- 위 '열린 물음' 의 LAM_PE-1 LII 1 은 이 대조로 더 날카로워졌다: 명목표의 곱 구조 (0.58 ≈ 0.64 × 0.9) 는 LII 가 pristine 양극 용량
  기준임을 가리키므로, LAM_PE-1 은 작은 양극 + 흑연 쪽 리튬 재고 설계일 가능성이 크다 (가설 — 논문 확인 전). 그렇다면 원 G 는
  "양극 용량을 넘는 재고는 없다" 는 모델 가정이고 그 셀은 가정 밖이다.
- v2 의 골자: 대상은 h(x) ∈ H(S) (개별 투영 · 개별 양립 · 동시 양립 · 명목점 정확 대조) · 다중 시작 국소 최적화의 좁음 · 배제는
  UNRESOLVED (실용 선택) · J_V = √f2 [V] · J_D = √f4 [V/mAh] · 결합 = 벡터 제약 집합 · 2σ̂_v 는 경험 기준 · 허용 영역 셋 (그들
  상자 + G = E3 계약 · 넓힌 상자 + G · 넓힌 상자 · G 없음 = 다른 영역) · 외삽 의존 증인 표시 · H4 는 양쪽 각자의 cutoff 정규화와
  scale 대칭 대조 · E3 는 "코드 경로 재실행" (E3a) 과 "출판 결과 재현" (E3b · 미등록) 으로 나눔.
- 선행 조건: **논문 전문 (또는 동등 명세) 이 확인적 맞춤의 선행 조건** (검토 권고 채택 — 시트 의미 · LII 정의 · E3b 기준 수치) ·
  v2 재검토 수용 · 자료를 처음 여는 맞춤 전 단계 P0 의 승인 · 실행 승인. 공개 사본 검색 1 회 (2026-10-03) 결과 없음.
- 라이선스: 코드 MIT · 자료 CC BY 4.0 확인 (검토자) — 저자 · 제목 · 출처 · 라이선스 · 변경 사항 표기 유지 · 논문 그림 재배포는 별도.

## v2 재검토 (2026-10-04) — 설계 방향 수용 · 문서 보완 넷 · 실행 0

v2 의 Codex 재검토 판정은 `DESIGN_DIRECTION_ACCEPTED_DOCUMENT_REVISION_REQUIRED` (묶음 `bms-balancing/reviews/prereview_reil_v2_20261004/` ·
기준 커밋 `ed397bab4`). R1–R6 반영은 수용됐다 — A0/A1/A2 분리 · `UNRESOLVED` · E3a/E3b 구분 포함. 확인적 사전 등록을 확정하기 전에
남은 문서 보완 넷과 우리 처리는 정정 부속 문서 `bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md` 에 있다 (유효
프로토콜 = v2 + 부속 A · 대체한 v2 문장을 줄 번호로 적었다).

| 재검토 | 요지 | 부속 A |
|---|---|---|
| RV2-N1 (P1) | 결합 최소에 상대 δ 를 다시 곱하면 벡터 집합과 달라진다 · H4 의 문턱 T 가 없다 · 뒤에 더 낮은 최소를 찾았을 때의 처리가 없다 | 결합 = `ρ = max(J_V/Ĵ_V, J_D/Ĵ_D) ≤ 1 + δ` (벡터 집합과 같은 집합 · δ 네 값은 재판독) · `T_s = Ĵ_s + 2σ̂_v` · 모든 탐색 뒤 한 번의 공통 갱신 (문턱을 조이기만 한다) |
| RV2-N2 (P1) | Ĵ 는 유효 증인으로만 · 단위 있는 수치 허용치 · 예산 종료 ↔ 증인 분리 · P0 의 수치 실패 | 독립 재평가 + 선형 잔차 ≤ 1e-10 (단위별) · `termination` 과 `witness` 를 따로 · P0 = 닫힌 구간식을 정확한 유리수로 (`P0_UNFIT` ≠ PRIOR_INCOMPATIBLE) |
| RV2-N3 (P2) | 결정적 시작 · 순회 · seed · 격자 보고 단위 · 예산 · 비용 측정도 맞춤 | 중심에서 바깥으로 sweep 하나 · 시작 정확히 4 · seed = label 의 sha256 · "충족 / 미해결 격자점" 으로 보고 · 지역 실행 ≤ 54,901 · 목적 호출 ≤ 109,817,477 (E3a optimizer 호출 275 는 따로) · 비용 측정은 별도 승인 |
| RV2-N4 (P2) | 1000 점 교차는 고정 근사다 · 끝점 · 교차 중복 · 음성 대조 · 대칭은 반증이 아니다 | 이름 정정 · 끝점 수용 폭 ν = 0.01 V (사전 선택) · 유일 교차 · 모델 곡선끼리의 음성 대조 · ray 이탈은 먼저 구현 · 수치 · 영역 경계로 분류 (v2 의 반증 문구 철회) |

- **상자 문구 정정** (위 사전 검토 표의 '경계' 줄 포함): Fresh · LAM_NE-1 · LAM_PE,LLI-1 은 G 의 경계 위가 아니라 무여유 선 위, 곧 G 밖이다
  (±0.02 양립은 `max_q ≥ 1/400` 조건부 · P0 가 확정) · 비율은 정확한 분수로 (τ = 0 상한: All mode-2 `50/13` · LAM_PE,LLI-2 · All mode-1 `25/3`) · LLI-2 형의
  τ = 0.02 상한은 `max_q ≤ 25/8 = 3.125` — 우리가 가정한 3.0–3.3 은 그 값을 사이에 두므로 전부를 "경계" 로 부르지 않는다.
- 재검토의 산술 (예산 · 비율 · 영역별 offset 차 구간) 은 정확한 분수로 따로 대조해 같았다 — 자료 계산이 아니다.
- **C1 을 둘로:** C1-core (시트 의미 · LII 정의 · 셀/step 선택 — 확인적 맞춤의 선행 조건) · C1-E3b (출판 비교 수치 · 요약 방식 — E3b 등록만의
  선행 조건). E3b 는 미등록 그대로.
- 승인 아님: P0 · 비용 측정 · 맞춤 · 설치 · 구현. 다음은 부속 A 의 재검토 (사용자 결정).
- **2026-10-04 부속 A 재검토 요청 발송** (사용자 전달 · 요청문 `bms-balancing/docs/REIL_V2_ANNEX_A_REREVIEW_REQUEST_20261004.md` ·
  고정 커밋 `a82d7135e` · Q1–Q6) — 회신은 아래 절.

## 부속 A 재검토 (2026-10-04) — RV2-N1 종결 · 세 국소 정정 → 부속 B · 실행 0

판정 `DOCUMENT_CONDITIONALLY_ACCEPTABLE_THREE_LOCAL_CORRECTIONS_REQUIRED` (묶음 `bms-balancing/reviews/prereview_reil_v2_annexA_20261004/` ·
고정 커밋 `a82d7135e`). **RV2-N1 (결합 · H4 문턱 · 공통 갱신) 종결 수용** · N2–N4 는 핵심 수용 · 국소 정정 셋. 부속 A 는 보존하고 (재검토
요구) 정정은 부속 B `bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md` (유효 프로토콜 = v2 + A + B · B > A > v2).

| 재검토 | 요지 | 부속 B |
|---|---|---|
| RV2A-N1 (P1) | `1e-10` 안의 위반도 정확 집합 밖일 수 있다 (G 위반 5e-11 반례) — "상태 불변" 보증은 틀렸다 | 보증 삭제 · 증인 두 등급 (`exact_feasible` · `numerically_accepted`) · 수치 수용에만 기대는 양립 · 폭은 `수치 경계 의존` + UNRESOLVED · P0 의 PRIOR_INCOMPATIBLE 불변 |
| RV2A-N2 (P2) | 이웃 · Phase A 결과에 기대는 시작점은 맞춤 전에 다 봉인할 수 없다 · Phase A 증인 1–3 개의 동시 양립 | 봉인 시점 둘 (고정 배열은 맞춤 전 · 적응적 시작점은 그 실행 직전 · 근거 run · 증인 · 변환) · `min(4, n_valid)` + Sobol 12 · s2 부족 · 숨은 추가 시작 없음 |
| RV2A-N3 (P2) | 같은 격자점 교차가 반올림으로 둘이 될 수 있다 | 평탄 거부 → 끝점 정확 일치는 격자 index · `Q_j` 그대로 → 엄격한 부호 변화만 보간 |

- 재검토의 자료 무관 반례 셋을 같은 상수 산술로 재현했다 — 셋 다 맞다.
- 자체 재독으로 둘을 더: 부속 A 가 v2 205–219 를 대체하며 v2 218–219 의 **기록 항목**을 다시 적지 않아 효력이 사라져 있었다 (부속 B §2-5
  에서 되살림) · 프로파일 등식 잔차로 등급을 매기면 LII 프로파일 증인이 일괄로 수치 수용이 된다 (등급은 주장의 정확한 집합 기준 · §1-2).
- 수용 범위의 문구도 좁혔다 (부속 B §4): 공통 갱신의 "조이기만" 은 같은 최종 저장 점 집합의 비교일 때 · 최종 ρ 는 모든 저장 쌍을 다시
  비교 · 독립 풀은 방법별 발견 최소 (전역 최소 아님) · Sobol 16 중 앞 12 에 균형 성질을 주장하지 않음 · ν 는 사전 선택 폭 · 대조는 구현 진단.
- 재검토 요청문 `bms-balancing/docs/REIL_V2_ANNEX_B_REREVIEW_REQUEST_20261004.md` (발송은 사용자 결정). 승인 아님: P0 · 비용 측정 · 맞춤 ·
  설치 · 구현. 문서 조건이 닫혀도 C1-core · 판 고정 · P0 · 비용 측정 · 실행의 별도 승인과 E3b 미등록은 그대로.
- **2026-10-04 부속 B 재검토 요청 발송** (사용자 전달 · 요청문 `bms-balancing/docs/REIL_V2_ANNEX_B_REREVIEW_REQUEST_20261004.md` ·
  고정 커밋 `e64f587bc` · Q1–Q6) — 회신은 아래 절.

## 부속 B 재검토 (2026-10-04) — RV2A-N1–N3 종결 · 문서 조건 C2 종결 · 실행 0

판정 `DOCUMENT_ACCEPTED_RV2A_N1_N2_N3_CLOSED_NO_EXECUTION_AUTHORIZATION` (묶음 `bms-balancing/reviews/prereview_reil_v2_annexB_20261004/` ·
고정 커밋 `e64f587bc`). **RV2A-N1 · N2 · N3 종결 · 확인적 사전 등록의 문서 수용 조건 C2 종결** · 새 차단 0 · 추가 정정본 요구 없음 · 유효
프로토콜 = v2 + A + B (B > A > v2). RV2-N1 종결과 이미 수용한 설계는 유지. 검토자가 v2 · A blob 이 앞 검토와 같고 B blob
`b25f9c4e…` (17,210 B · SHA-256 `fe2b39b2…`) 임을 독립 재계산했다 — 저장소 전체나 RUN_SCOPE 무변경의 인증은 아니다.

수용하며 검토자가 붙인 읽기 (새 조건이 아니라 적용 범위의 명확화):

- `exact_feasible` 은 그 주장의 선형 제약 집합에 대한 등급이다 — 물리량 무오차 · 목적함수 정확 계산 · 전역 최적성 인증이 아니다.
- `COMPATIBLE` 의 근거 증인은 독립 재평가와 최종 목적 문턱 (`J ≤ T`) 도 통과해야 한다 · 근거 증인 0 개면 NOT_FOUND / UNRESOLVED ·
  `1e-9` 는 문턱 완화가 아니라 목적 경계 라벨 기준.
- 무조건 WIDE 는 실제 투영값이 2τ 넘게 떨어진 정확 증인 한 쌍이 받친다 · 수치 수용 증인에만 기대면 한정 WIDE + UNRESOLVED.
- "자료에 기대지 않는 고정 배열" 은 앞선 맞춤 결과에 비적응적이라는 뜻이다 — 슬라이스 범위 · P/N · `max_q` 는 P0 에 기댈 수 있다.
- 시작 부족은 실제 수를 줄일 뿐 (복제 · 추가 Sobol · 예산 전용 없음) → 지역 실행 54,901 · 목적 호출 109,817,477 상한은 커지지 않는다
  (독립 재평가 · E3a · ray · 기록 비용은 그 밖).
- 격자 index 교차의 대조는 검토자의 작은 상수 산술이다 — 아직 없는 H4 구현의 기능 검증이 아니다. 고정 1000 점 근사 · 유일 교차 ·
  span > 0 는 그대로.

| 남는 선행 조건 (기존 · 새 발견 아님) | 상태 |
|---|---|
| C1-core | 논문 전문 또는 저자 제공 동등 핵심 명세 (시트 의미 · 명목 LII 정의 · 셀/step 선택) — 미확보 |
| C6 | 판 · 환경 고정 · 실제 전달 옵션과 고정 배열 식별 — 미시행 |
| C3 | 자료를 처음 여는 P0 — 별도 사용자 승인 |
| C5 | 비용 측정 (= 맞춤 · 파일럿 취급) — 별도 승인 |
| C4 | 실제 E3a / H 실행 · 자원 · 시간 범위 — 별도 승인 |
| C1-E3b | E3b 미등록 그대로 — E3a / H 의 새 선행 조건으로 넓히지 않음 |

- 다음은 위 조건의 확보 상태와 별도 작업 범위를 정하는 사용자 결정 (C1-core 명세 확보 · 환경 고정 · P0 / 비용 측정 / 실행 각각의
  승인). 문서 수용은 자료 개봉 · P0 · 비용 측정 · 맞춤 · 설치 · 구현의 승인이 아니고 자동 시작하지 않는다. GATE89 · PyBaMM 고정과 무관.
- **2026-10-04 선행 조건 확보 상태 제시** — `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md`: C1-core **미확보** (논문 미열람 · 공개 여부
  미확인 — 웹 검색에서 찾지 못했고 Crossref 는 이 환경의 네트워크 정책이 막는다) · C6 미시행 (문서 쪽 옵션 표 · 배열 봉인 규칙만) · 제안 순서
  C1-core → C6 → P0 → 비용 측정 → 실행. 지금 필요한 입력은 논문 (또는 저자 명세) 하나 — 각 단계는 사용자 결정.
- **2026-10-04 N2 (C6 준비) 초안** — `bms-balancing/docs/REIL_C6_ENV_PROFILE_DRAFT_20261004.md`: 실행 환경 프로필의 축 · 부속 A §3-1 옵션
  8 개의 대조 목록 · Sobol 배열 봉인 · 실행 기계 후보 셋 (결정은 사용자). 문서만 — 설치 · 버전 실측 · 실행 0 · 판 번호를 고르지 않았다.
- **2026-10-05 실행 기계 결정 — 이 클라우드 컨테이너** (사용자 "이컨테이너에서 하고 논문 이름 자세하게 줘봐") — 프로필 · 봉인 · 실행 기록은
  저장소로 · 실행하는 세션마다 다시 대조 · 설치는 버리는 venv 에서만 (범위는 C6 승인 문서에) · C6 실행은 별도 승인 · 기본 순서는 N1 (논문) 뒤.
  기록 `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md` §6.
- **2026-10-05 서지 확인 (README 원문 · BibTeX)** — 저자 일곱: Tingkai Li · Yifan Zhang · Benjamin Nowacki · Sina Navidi · Thomas Schmitt · Shan Hu ·
  Chao Hu · 제목 · 권 · 쪽 · doi 는 위 개요와 같다 · 끝 커밋 `1188c37` 그대로. README 만 읽었다 (xlsx · pkl · 노트북 열지 않음). 논문은 여전히 미열람.
- **2026-10-05 C1-core (논문 쪽) 확보 — 논문 · 보충 자료 수신** — `bms-balancing/docs/REIL_C1_CORE_SPEC_20261005.md`: 분석 11 시트 = 논문
  Table 1 의 11 행 · 명목 = Table 1 의 모사값 (노트북 명목표 11 행과 일치) · LII 식 (14)–(16) · 맞춤 = 다섯 번째 cycle · #3 은 리튬을 흑연 쪽에 둔 설계
  (가설 (나) 확인) · 참값 불확실성 a–d (formation 손실 · 높은 N/P 의 LAM_NE · 공급사 용량 기준 · pre-formation) · step 대응 · 분석 밖 6 시트는 P0.
- **2026-10-05 C6 시행 (이 컨테이너 · 스크래치패드의 버리는 venv)** — 봉인 `bms-balancing/reil_c6_20261005/` (lock · 프로필 · COBYQA 옵션 대조 ·
  Sobol Phase A 배열 sha256 식별 · `check` · 변이 증명) · 결과 절 `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md` §10 (판 · 수치의 정본은
  봉인 파일). 부속 A §3-1 의 COBYQA 옵션 8 개는 문서화돼 있고 합성 함수로 전달이 확인됐다. **같은 정수의 옛 `seed=` 는 `rng=` 와 다른 Sobol 배열을
  낸다 (경고 없음)** — 시작점은 `rng=` 로만 만든다. 결과의 수용은 Codex 에 별도로 청하고 P0 은 그 뒤다. 위 표의 C1-core · C6 행은 2026-10-04 시점이다.

## 논문 digest (2026-10-05) — 그림에서 보이는 것

원문 해체분석: `raw/papers/li2026_half-cell-fitting-multiobjective-benchmark.md` (그림 38 장 — `raw/figures/li2026_half-cell-fitting-multiobjective-benchmark/`).
C1-core 기록과 같은 원문을 다시 읽은 것이고 그 기록 · 프로토콜은 고치지 않았다. 아래는 출판 그림의 판독 (`[도표]`) · 원문 값으로 한
산술 (`[재현]`) — **E3b 비교 기준이 아니고 판정에 쓰지 않는다.**

- 맞춤 곡선은 **충전 곡선**이다 (Fig. 7 · A.3 — ≈2.33 V → 3.6 V) — C1-core §3 의 추정을 그림이 받친다.
- `MSE_QV` 하나로 맞추면 15 mm LFP 셀 여섯과 LAM_PE-1 의 `m_PE − LII` 가 0.00–0.04 — 설계 LLI 가 LAM_PE 로 읽힌다 (digest §8-3).
- 맞춤 LII ≈ 충전 용량 ÷ 3.10–3.16 mAh (열 셀) — `LII·max_q = Q_end + d_N` 이라 LII 는 사실상 용량이다. 이 비가 함의하는 `max_q` ≈ 3.1
  (`d_N ≈ 0` 가정) 은 C1-core §4-5 의 어림 2.89 보다 크고 부속 A §5-3 의 τ = 0.02 문턱 3.125 와 판독 오차 안에서 겹친다 → P0 (digest §8-4).
- LAM_PE-1 의 출판 해는 부등식 아래 설계의 '거울' (`m_PE` 1.02–1.09 · `m_NE` 0.50–0.69) · 일부 추정값이 상자 끝 (0.5 · 0.6 · 1.1) 에 붙음 (§8-3 · §8-5).
- 15 | 12 셀 셋 (명목 N/P 0.63) 에 리튬 석출과 들어맞는 충전 끝 신호 (음의 dV/dQ ≈2.3–2.5 mAh) — 참값 불확실성 후보 (§9-3).
- ~~formation 손실의 크기 단서: Fig. 9 CE 곱 (15 | 16 · cycle 1–4) ≈0.83 · LAM_PE-1 용량 기반 ≈0.82 (가정 둘 · §8-4 · §9-2).~~ **철회 (2026-10-05 ·
  RV2C-N2)** — CE 곱은 CE 비들의 곱이라 Li 손실률로 환산하지 않는다 · U-a 크기 미정 · 두 어림 모두 크기 단서로 쓰지 않는다 (아래 "부속 C 재검토" 절).
- 공개 코드 ↔ 논문: 식 (9) ↔ f1 · 식 (11) ↔ f3 · 부등식 · 상자 · NE 상수 외삽이 논문에 없다 (E3b 등록 때 · E3a 무관) · 식 (7) 의 `δ` 부호가
  식 (15) · Fig. 5 와 반대 (§2-1 · §3-1).

## 부속 C 재검토 (2026-10-05) — C1-core 논문 쪽 수용 · 부속 C 국소 정정 셋 → 부속 D · 실행 0

판정 `ANNEX_C_CONDITIONALLY_ACCEPTABLE_THREE_LOCAL_DOCUMENT_CORRECTIONS` (고정 커밋 `4ad68af44` · 받은 바이트
`bms-balancing/reviews/prereview_reil_v2_annexC_20261005/`): C1-core 의 논문 쪽 근거는 수용 (실물 시트 · 셀 열 · step 대응은 P0) · 부속 C 는 P2 셋의
정정을 조건으로 적합 · v2 + A + B 의 C2 종결 유지 · 실행 · P0 · C6 · 맞춤 승인 아님 · E3b 미등록. 정정은
`bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_D.md` (C 의 바이트는 그대로) · C1-core 기록 §8.

- **RV2C-N1** — 명목 목표값이 Fig. 6 / A.4 의 Theoretical 표식과 대응한다는 것과, 출판 추정치의 정규화 분모가 util `max_q` 와 같다는 것은 다르다
  (후자 미확인). 식 (16) 의 상대 잔존량 = `z / z_F` · 명목 Fresh 의 `m_P = 1` · `d_P = d_N` 은 `z_F = 1` 의 충분조건이지 필요조건이 아니다.
- **RV2C-N2** — CE 곱은 CE 비들의 곱이라 Li 재고 손실률로 환산할 수 없다 (cycle 사이 용량 · 초기 재고를 잇는 결속 없이는 망원곱이 아니다) → 위 "논문
  digest" 절의 "크기 단서" 줄과 raw digest §8-4 · §9-2 · §16-1 의 "≈17 % 손실" 해석은 **철회** (raw 는 불변 — 정정 참조는 이 절) · U-a 크기는 미정.
- **RV2C-N3** — P0 의 cycle · 방향을 두 칸의 세 상태 (`일치` / `불일치` / `판정 불가`) 로 고정 · 확인된 불일치 우선으로 종합 · NaN 분절 번호나 그림으로
  cycle 을 추정하지 않음 · 완전지 충전 (PE 탈리튬 · NE 리튬화) 과 반쪽전지 기준의 방향을 나눔 · C1-core 기록의 "나머지 6 시트" 는 #15 가 아니라
  **시트 #12 · #13 · #14 · #17 · #18 · #19** (#15 · #16 = 기준 둘).
- U-e (15 | 12 셀 셋의 충전 끝 신호) 는 **미확인 · 비특이적 기전 가설로만** 수용 — 석출 확인 · 정량 손실 · 특정 오차 방향으로 쓰지 않는다.
- 다음 (회신의 순서 · 각각 사용자 결정): 정정 확인 + C6 결과의 별도 수용 → P0 의 범위 · 예산 · 중단 조건을 사용자에게 따로 요청.
- **독립 교차검토 (다른 Codex 세션 · 2026-10-05):** 같은 판정을 지지 (`PRIOR_CONDITIONAL_DOCUMENT_VERDICT_SUPPORTED_CORRECTIONS_NOT_YET_VERIFIED` —
  N1–N3 타당 · 새 P1 없음 · 부속 D 는 보지 않음). 반례 산술 (N1 `z_F = 1` 이 `m_P = 1 · d_P = d_N` 없이도 · N2 같은 CE 곱에 다른 잔존율) · 9 조합
  종합표 · 독립 검사 63 (이 컨테이너에서 다시 돌려 63/63). 묶음 `bms-balancing/reviews/prereview_reil_v2_annexC_crossreview_20261005/` · 상태 문서 §11.
- **부속 D 재확인 + C6 결과 검토 (2026-10-06):** (A) 부속 D 수용 — RV2C-N1–N3 **종결** (p3 의 PE 탈리튬 / NE 리튬화는 기대 방향의 근거 ·
  실제 기준곡선 확인은 P0). (B) C6 봉인 식별 수용 · 전체 종결은 국소 보충 둘 (C6-N1 충돌 예외 범위 · C6-N2 실행 원문 미보존 · 옵션 전달 근거)
  대기. 묶음 `bms-balancing/reviews/prereview_reil_v2_annexD_c6_20261006/` · 보충 `bms-balancing/docs/REIL_C6_SUPPLEMENT_20261006.md` · 상태 문서 §13.
- **C6 보충 검토 (2026-10-06):** C6-N1 (충돌 예외를 관측된 LICENSE 한 건으로 · 구현) · C6-N2 (실행 원문 미보존 신고 · 옵션 전달은 정적 구조까지)
  수용 → **C6 사전 준비 검토 종결**. 다음은 P0 범위 · 예산 · 중단 조건의 사용자 승인 요청 (자료 개봉 · 재구축 · 맞춤 아직 0). 묶음
  `bms-balancing/reviews/prereview_reil_v2_c6_supplement_20261006/` · 상태 문서 §15.

## 이 위키와의 관계

- 방법 축: [[fitting-degeneracy]] · [[near-optimal-set-width-measurement]] · 원전: [[birkl-ocv-degradation-diagnostic]] · 자유도: [[np-lip-ocv-reparametrization]]
- 같은 판정 틀의 앞선 실측: [[pyprobe]] · 물음: [[22p-physics-or-degeneracy]]
- 같은 브리핑: [[pybamm]] (#5813) · [[pyimpspec]] · 처리 기준: [[daily-github-briefing-triage]]

## 관련
- [[fitting-degeneracy]]
- [[near-optimal-set-width-measurement]]
- [[birkl-ocv-degradation-diagnostic]]
- [[halfcell-window-parametrization-lineage]]
- [[np-lip-ocv-reparametrization]]
- [[pyprobe]]
- [[22p-physics-or-degeneracy]]
- [[daily-github-briefing-triage]]
