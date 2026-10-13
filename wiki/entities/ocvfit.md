---
title: ocvfit (OCV 맞춤 + '식별 불가' 표시 — watch)
description: "반쪽전지 OCP 로 전지 OCV 를 맞춰 LLI · LAM_PE · LAM_NE 를 내고, 잔차 자기상관으로 부풀린 프로파일 구간에 기준 곡선 섭동 예산을 더해 반폭이 1 %p 를 넘는 모드는 '식별 불가 (구간만)' 로 내놓는 Python 도구 (MIT · 0.1.0 · numpy와 scipy 만). 우리 축퇴 질문의 직접 경쟁 · 비교 도구. 2026-10-13 1차 대조는 코드 읽기만 (실행 0) · 릴리스 태그 없음 · 예제는 합성 데이터 · watch."
created: 2026-10-13
updated: 2026-10-13
type: entity
tags: [degradation, tooling, research]
sources: [raw/articles/2026-10-13-github-research-briefing.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: single-source
---

# ocvfit (OCV 맞춤 + '식별 불가' 표시 — watch)

## 개요

- 저장소: `https://github.com/catnap042/ocvfit` — MIT · 2026-10-09 공개 · HEAD `2b898cc6` · `pyproject.toml` 0.1.0 · Python ≥3.10 · 의존성 numpy · scipy 만 ·
  **릴리스 태그 없음** (`git ls-remote --tags` 빈 응답). 1차 대조 원문은 `raw/articles/2026-10-13-github-research-briefing.md`.
- 하는 일: 반쪽전지 OCP 두 곡선으로 전지 OCV (방전) 를 맞춰 양극 용량 `Q_pe` · 음극 용량 `Q_ne` · 리튬 재고 `n_li` 를 내고, BOL ↔ aged 비로 모드를 낸다
  (`MODE_PARAMETERS = {"LLI": "n_li", "LAM_PE": "Q_pe", "LAM_NE": "Q_ne"}` · 모드 = 1 − aged / BOL). 혼합 양극 (`blend.py`) · dQ/dV · dV/dQ (`ica.py`) 도 있다.
- 브리핑 (2026-10-13 · 단일 출처) 의 사실 주장 대조: MIT · 다중 Python CI **정의** (3.10 · 3.12 · 3.13) · LFP 식별 불가 시험 · 모델의 오프셋이 저항이 아닌 **전압 상수** (`v_offset`) — 원문과 맞다.
  "예제 5개" 는 스크립트 4 + CSV 3 으로 셈이 다르고 (셈 기준 미확인), CI 가 실제로 통과했는지는 확인하지 않았다.

## 핵심 — 식별 판정을 1 급 출력으로 둔다 (원문 `src/ocvfit/uncertainty.py`)

1. **잔차 상관 보정 프로파일 구간** — 매개변수 하나를 격자에 고정하고 나머지를 재적합 · Δχ² < 3.84·(1+ρ)/(1−ρ) 인 값을 받는다 (부풀림 상한 100 · ρ = 최적 잔차의 lag-1 자기상관).
   OCV 잔차는 곡선을 따라 강하게 상관돼 있어 독립 가정이면 구간이 너무 좁다는 것이 원문의 이유다.
2. **기준 곡선 섭동 예산** — 반쪽전지 곡선마다 균일 오프셋 (기본 ±3 mV) + 매끈한 형상 오차 (기본 2 mV · `sin` 세 항) 를 넣어 재적합 · 8 번 뽑은 최대 편차.
3. **판정** — 최종 구간 = 프로파일 구간 ± 예산 · 반폭 > 1 %p 면 "not identifiable" (점값 없이 구간만). 모드 구간은 BOL · aged 두 프로파일의 끝을
   엇갈려 묶는 보수적 결합 (`[1 − aged_hi/bol_lo, 1 − aged_lo/bol_hi]`).

LFP 시험 (`tests/test_lfp_identifiability.py`) 원문 요지: LFP 평탄부가 거의 평평해 **리튬화 쪽 가파른 끝이 측정 창 안에 있어야만 양극 용량이 정해진다.**
음극 제한 설계에서는 그 끝이 창 밖이라 LLI · LAM_NE 는 흑연 staging 덕에 식별되고 LAM_PE 는 섭동 예산이 지배해 식별 불가 · 양극 제한 설계에서는 식별된다 — 두 설계를 시험으로 고정했다.

## 우리 질문과의 관계 (`[해석]`)

- [[data-window-identifiability]] — LFP 시험은 "평탄부 끝이 창 안에 없으면 그 전극 용량은 정해지지 않는다" 는 창 규칙의 **제3자 구현**이다. 같은 현상의 설계 참값 실측은
  [[fitting-degeneracy]] 의 "LFP 평탄부에서 LLI 가 LAM_PE 로 읽힌다" 절 ([[isu-uconn-lfp-gr-emulated-degradation]]) — ocvfit 은 그 자리를 점값 대신 '구간만' 으로 막는다.
- [[22p-physics-or-degeneracy]] — 모드마다 매개변수 하나의 프로파일로 구간을 얻으므로, 22p 가 묻는 **두 모드의 차 (PE − NE 격차)** 의 구간은 직접 나오지 않는다.
  두 모드 구간을 독립으로 묶으면 둘 사이 공분산 (축퇴 방향) 을 잃는다 — [[near-optimal-set-width-measurement]] 가 유도량 폭을 직접 미는 이유와 같은 지점.
- [[pocv-nonequilibrium-mode-bias]] — 섭동 예산의 균일 오프셋 ±3 mV 는 그 페이지의 "기준 +δ ≡ 측정 −δ" 통로와 같은 축이다. 우리 `ocpbias` PE 다리가 그 예산의
  합성 truth 판이다 (우리는 고정 크기 · 부호별 다리, ocvfit 은 8 번 무작위의 최대).
- [[ampworks]] · [[pyprobe]] 와의 차이: 그 둘은 점 추정 (+ 대각 Hessian 불확도 등) 이고, ocvfit 은 식별 판정을 출력 단계에 둔다. 우리 실측에서 그 둘의 불확도는
  틀린 적합에서 참 오차를 덮지 못했다 — ocvfit 의 구간이 덮는지는 아직 아무도 우리 truth 로 재지 않았다.

## 한계 (원문 · 브리핑 기준)

- 0.1.0 · 릴리스 태그 없음 · 예제는 합성 데이터 · 실측 검증 없음 (브리핑 주장 · README 의 worked example 도 합성).
- 섭동 예산은 **8 번 무작위의 최대값**이지 상한 (bound) 이 아니다 (seed 고정). 1 %p 문턱 · ±3 mV · 2 mV 는 기본값 선택이다.
- OCV 만으로는 부반응으로 잃은 Li 와 고립된 활물질 속에 갇힌 Li 를 완전히 가르지 못한다 (브리핑). `v_offset` 은 전압 상수다 — 누설저항 · 미세단락으로 읽지 않는다.

## 제안 실험 (후보 · 미착수 — 사용자 승인 대상)

- **E1 (브리핑 제안의 우리 판):** 참값을 아는 우리 합성 truth 로 전 구간 ↔ 잘린 구간 · PE 오프셋 다리 (`ocpbias`) 를 넣어 — ① "not identifiable" 표시가 우리 축퇴 판정과
  같은 자리에서 켜지는가 ② 구간이 참값을 덮는가 ③ 22p 의 격차에 대해 두 모드 구간을 묶으면 무엇을 잃는가. 격리는 [[ampworks]] · [[pyprobe]] 시험과 같다
  (버리는 venv · 운영 환경 · 저장소 산출물 · RUN_SCOPE 0).
- 주의: 우리 truth 는 composite 음극 (2 상) DFN 의 방전 곡선이다 — ocvfit 의 단일 음극 · 평형 OCV 가정과 다르므로, 해석 전에 입력 정합 (저율 · 가지 · 음극 OCP) 을 먼저 정한다.

## 관련

- [[fitting-degeneracy]] · [[data-window-identifiability]] · [[near-optimal-set-width-measurement]] · [[pocv-nonequilibrium-mode-bias]]
- [[ampworks]] · [[pyprobe]] — 같은 질문의 다른 도구 (우리 truth 실측 있음)
- [[22p-physics-or-degeneracy]] — 격차 (두 모드의 차) 의 열린 질문
- [[daily-github-briefing-triage]] — ② 경쟁 도구 축 · ④ 실험 아이디어 축
