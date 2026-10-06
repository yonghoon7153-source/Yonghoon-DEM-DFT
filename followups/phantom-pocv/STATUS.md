# 논문 후속 — Phantom LAM/LLI (pOCV 비평형 성분) · 독립 흐름 상태판

> **흐름 이름:** 논문 후속 (Phantom pOCV) · **시작:** 2026-10-06 · 사용자 지시 "논문 후속도 REIL랑 병렬로 진행해보고" · "p2 부터 진행하고 하나의 병렬 섹션으로 구분을 해놔요"
> 게이트 루프 · REIL · COMSOL 과 **섞지 않는다.** RUN_SCOPE (`degradation-degeneracy/` 의 `src/ tools/ configs/ scripts/ run.sh requirements*.txt`) 를 바꾸지
> 않는다 — 실행은 저장소 밖 사본 (git archive) · 스크래치패드에서만. 연구 수치의 정본은 이 흐름의 결과 파일이며, 위키에는 옮겨 적지 않는다.

## 근거

| 항목 | 위치 |
|---|---|
| 원 논문 | Asheruddin N et al., "Phantom LAM and LLI: Resistance and Hysteresis Bias in Voltage-Curve Degradation Mode Analysis", arXiv 2512.19773v1 (Imperial College London) — PDF 미커밋 · sha256 `222dcd2d…` |
| raw digest | `wiki/raw/papers/asheruddin2025_phantom-lam-lli-ir-hysteresis-dma.md` |
| 개념 페이지 (P1–P5 정의 · P1 결과) | `wiki/concepts/pocv-nonequilibrium-mode-bias.md` |
| 우리 쪽 비교 대상 | `degradation-degeneracy/docs/09_22P_GAP.md` §7.10 (ocpbias PE 균일 오프셋 다리 · 정본 수치) |

## 진행표

| # | 내용 | 상태 | 근거 / 커밋 | 다음 |
|---|---|---|---|---|
| P1 | §7.10 격차 bias 부호 대조 (재집계 · 실행 0) | **완료** — 원점 건강 PE 오프셋 다리 5 개 모두 0 mV 대비 + (논문 IR 방향과 반대) · 성분별 부호는 원 fit 부재로 미확인 | 개념 페이지 "P1 결과" · `a11e6d27a` · `cfb6216aa` · `143e9f444` | — |
| P2 | 꼭대기 무거운 SOC 의존 PE 오프셋 다리 (같은 평균의 균일 다리와 비교) | **설계 조사 중** (명령 · 입력 · 비용) → 승인 요청문 → 실행 | — | 승인 요청문 (범위 · 예산 · 중단 조건) |
| P3 | `φ_Si` 자유 5 매개 적합 | 대기 (P2 뒤) | — | — |
| P4 | 충전 가지 + 탈리튬화 기준 (가지 불일치) 적합 | 대기 | — | REIL 해석 제한과 연결 |
| P5 | 적합 R 오프셋 열의 각도 (PyDMA · ampworks 방식) | 대기 | — | REIL §24 의 PyDMA 비교와 연결 |

## 규칙

- 설계 (다리 목록 · 오프셋 식 · 비교 지표 · 중단 조건) 는 **실행 전에** 이 파일 또는 승인 요청문에 고정하고, 결과를 본 뒤 바꾸지 않는다.
- 옛 §7.10 수치와는 code identity 가 달라 **같은 실행 묶음 안에서만** 비교한다.
- 실행 기록: 시작 / 종료 HEAD · 작업 트리 · 사본 sha · 환경 · 자원 관측 · stdout / stderr · 외부 rc (REIL §22 의 교훈).
