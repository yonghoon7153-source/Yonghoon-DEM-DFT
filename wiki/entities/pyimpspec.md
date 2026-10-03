---
title: pyimpspec (EIS 분석 도구 · KK · DRT)
description: "임피던스 스펙트럼의 Kramers–Kronig 검사 · DRT · 피크 · 등가회로 분석을 하는 Python 라이브러리 (GPL-3.0-or-later · Python ≥3.12). 우리에게는 운영 밖 분석 전용 후보 — 버리는 venv 에서 참값을 아는 합성 2-RC 로 설치 · 동작을 확인했다 (2026-10-03)"
created: 2026-10-03
updated: 2026-10-03
type: entity
tags: [battery, tooling, research]
sources: [raw/articles/2026-10-02-github-research-briefing.md, raw/repositories/2026-10-03-pyimpspec-5.2-smoke-synthetic-2rc.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-mixed
---

# pyimpspec (EIS 분석 도구 · KK · DRT)

## 개요

- 저장소: `https://github.com/vyrjana/pyimpspec` · DRT 안내: `https://vyrjana.github.io/pyimpspec/guide_drt.html` (브리핑이 준 링크 — 안내 문서는 열지 않았다).
- 브리핑 (2026-10-02 조사분 · 단일 출처): v5.2.0 (9 월 24 일) · 선형 Kramers–Kronig 검사 · DRT · 피크 면적 · 등가회로 분석.
  "DRT 피크는 정규화에 민감하고, 피크만으로 LLI/LAM · 미세단락 원인을 확정할 수 없다" 는 경고를 브리핑이 스스로 달았다.
- **1차 대조 (git 원문 · `raw/articles/2026-10-02-github-research-briefing.md` 하단):** `pyproject.toml` 의 판 5.2.0 ·
  `GPL-3.0-or-later` · `requires-python >=3.12` · `numpy >=2.5` · `scipy >=1.17` (주석 원문 "1.18 introduced issues with
  constrained fitting") · 선택 의존 `cvxopt` · `kvxopt`. CHANGELOG 5.2.0: Python 3.11 지원 중단 · CNLS 판 KK 검사 deprecated ·
  "constrained fitting appears to not work properly across all platforms … depend on the version of SciPy" (원인 미상이라고 저자가 적음).

## 실측 (2026-10-03 · `raw/repositories/2026-10-03-pyimpspec-5.2-smoke-synthetic-2rc.md`)

버리는 venv (스크래치패드 · Python 3.12.3 · numpy 2.5.3 · scipy 1.18.1 · cvxopt 1.3.3) · 운영 환경 · 저장소 불변. 스펙트럼은
R0 10 Ω + (R1 20 Ω ∥ C1 10 µF) + (R2 50 Ω ∥ C2 1 mF) — 참값 τ1 = 2e-4 s · τ2 = 5e-2 s · 잡음 0 · 71 점 (100 kHz – 10 mHz).

| 물음 | 결과 | 읽는 법 |
|---|---|---|
| 설치 · 실행 | 운영 Python 3.11 에는 못 깐다 · 버리는 3.12 venv 에는 깔린다 · `tr-rbf` DRT 는 선택 의존성 `cvxopt` 를 더해야 돈다 (없으면 `DRTError`) | 운영 환경 · 저장소 의존성에 넣을 길은 없다 (Python 판 + GPL) — 분석 전용 별도 venv |
| KK 검사 (real) | pseudo χ² 1.3e-18 · RC 53 개 · 약 9 s | 잡음 없는 회로 스펙트럼이니 당연한 통과 — 실측 스펙트럼에서의 판정력은 안 봤다 |
| DRT 피크 **위치** τ | `tr-nnls` λ 1e-3 · 1e-1 모두 2.00e-4 / 5.03e-2 s · `tr-rbf` (자동 λ 3.4e-5) 1.97e-4 / 4.98e-2 s | 250 배 떨어진 두 시정수는 위치가 정확하다 |
| DRT 피크 **높이** γ | λ 1e-3 → 84 / 169 Ω · λ 1e-1 → 11 / 26 Ω (약 7 배) · `tr-rbf` → 40 / 102 Ω | **높이는 정칙화 강도의 함수다** — 브리핑의 "정규화에 민감" 이 가장 쉬운 스펙트럼에서도 재현된다. 높이로 열화를 비교하면 안 된다 |
| DRT 피크 **넓이** ∫γ d ln τ (참값 20 / 50 Ω) | λ 1e-3: 19.97 / 50.03 · λ 1e-1: 19.53 / 50.67 · `tr-rbf`: 19.99 / 50.27 Ω | 넓이 (= 그 과정의 저항 몫) 는 λ 를 100 배 바꿔도 2.5 % 안 — 단 **잡음 없고 잘 떨어진** 경우에 한해서다 |
| 라이브러리 피크 분석 (`analyze_peaks` · `tr-rbf`) | 참 피크 둘 (R_peak 19.97 / 50.11 Ω) + **가짜 피크 둘** (τ 1.3e-5 s · 73 s · 각 0.1 Ω) | 기본값 그대로면 피크 **개수**가 늘어난다 — [[drt-peak-count-nonidentifiability]] 의 가장 쉬운 판. 개수는 문턱 · 끝 처리 규칙과 함께 적어야 한다 |

한계: 잡음 0 · 시정수 간격 250 배 · 조건마다 한 번. 겹치는 시정수 · 잡음 · 확산 꼬리 · 인덕턴스는 안 봤다. 이 표가 말하는 것은
"설치되고 돌며, 쉬운 경우 위치 · 넓이는 맞고 높이 · 개수는 설정에 끌려간다" 까지다.

## 판정 — 우리가 쓸 수 있는가

- **쓸 수 있다 — 분석 전용 · 운영 밖.** (1) Python ≥3.12 라 운영 3.11 과 같은 환경에 못 둔다. (2) GPL-3.0-or-later — 우리 코드에
  넣거나 (복사 · import 해서 배포) 하지 않는다. 별도 venv 의 독립 스크립트로 돌리고 **숫자만** 가져온다. (3) RUN_SCOPE 와 무관
  (degradation-degeneracy 파이프라인은 EIS 를 안 쓴다) — 게이트 대상이 아니다.
- **닿는 곳:** 우리 주 연구 (OCV · 저율 곡선의 LLI/LAM 피팅 degeneracy) 에는 직접 닿지 않는다. 닿는 곳은 ASSB 축의
  [[drt-peak-count-nonidentifiability]] (봉우리 개수 · 정칙화) 와, EIS 열화 진단 논문을 읽을 때의 재현 도구 (예: 공개 EIS 노화
  자료 [[zhang2020-eis-aging-dataset]]).
- **경고 (브리핑 그대로 유지):** 피크만으로 LLI/LAM · 미세단락을 확정할 수 없다 — ISC 판별 도구가 아니다
  ([[isc-detection-vs-balancing-masking]] 의 근거로 쓰지 않는다). 제약 적합을 쓰게 되면 SciPy 판을 고정하고 그 판을 결과와 함께 적는다
  (CHANGELOG 원문이 플랫폼 · SciPy 판 의존을 인정한다).

## 제안 실험 (후보 · 미착수)

- **P1 — DRT 넓이 · 개수의 강건성 (참값을 아는 합성):** 두 시정수 간격 (10–250 배) × 잡음 (0 · 0.1 · 1 %) × λ (자동 · 1e-4–1e-1)
  격자에서 넓이 오차와 봉우리 개수를 잰다. [[drt-peak-count-nonidentifiability]] 가 논문들에서 모은 "봉우리 개수는 정칙화의 함수"
  를 우리 손으로 수량화한다 — 어느 간격 · 잡음에서 넓이마저 무너지는가. 버리는 venv · 저장소 밖 · 수 분 급.
- **P2 — 브리핑 제안 (초기 ↔ 열화 EIS 의 저항 몫이 정규화를 바꿔도 유지되는가):** 실측 자료가 필요하다. 공개 EIS 노화 자료에서
  같은 SOC · 온도 쌍을 골라 λ · 방법 (`tr-nnls` ↔ `tr-rbf`) 을 바꿔 넓이 변화의 부호 · 크기가 유지되는지 본다. 우리 주 질문 축
  (OCV 곡선) 밖이라 우선순위는 낮다.
- 둘 다 사용자 승인 뒤. 운영 · RUN_SCOPE 무관이라 게이트 리뷰 대상은 아니다.

## 이 위키와의 관계

- EIS 축: [[drt-peak-count-nonidentifiability]] · [[zhang2020-eis-aging-dataset]]
- 같은 브리핑: [[pybamm]] (#5813) · [[isu-uconn-lfp-gr-emulated-degradation]] · 처리 기준: [[daily-github-briefing-triage]]

## 관련
- [[drt-peak-count-nonidentifiability]]
- [[zhang2020-eis-aging-dataset]]
- [[daily-github-briefing-triage]]
- [[isc-detection-vs-balancing-masking]]
- [[isu-uconn-lfp-gr-emulated-degradation]]
