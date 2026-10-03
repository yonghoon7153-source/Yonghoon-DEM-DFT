---
title: ISU-UConn LFP/흑연 모사 열화 자료 + REIL 다목적 피팅 코드
description: "전극 원판 지름 (LAM 모사) 과 리튬화 상태 (LLI 모사) 를 설계해 만든 LFP/흑연 11 셀의 반쪽 · 완전지 곡선 (CC BY 4.0) 과, 반쪽전지 곡선의 질량 배율 · 용량 오프셋을 GA/NSGA 로 맞추는 MIT 코드. 우리에게는 α·β 창 맞춤과 같은 계열의 방법을 실측 '설계 참값' 에 대 보는 외부 검증 후보"
created: 2026-10-03
updated: 2026-10-03
type: entity
tags: [degradation, tooling, research]
sources: [raw/articles/2026-10-02-github-research-briefing.md, raw/repositories/2026-10-03-reil-uconn-moo-known-truth-table.md]
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
- 논문 (README 인용 — **미열람**): T. Li 외, "Benchmarking half-cell model fitting approaches for lithium-ion battery degradation
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
| Fresh · LAM_NE-1 · LAM_PE,LLI-1 | **경계** (LII = m_P) — ±0.02 안에서 양립 · LII 위쪽 폭은 제약이 자른다 | 우리 대조 |
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
