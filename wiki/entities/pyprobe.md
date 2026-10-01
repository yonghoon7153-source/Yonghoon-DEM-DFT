---
title: PyProBE (OCV/DVA 피팅 도구)
description: "Imperial College 의 배터리 데이터 처리 도구 — 전극 OCP 로 셀 OCV·ICA·DVA 를 맞춰 전극 용량과 리튬 재고를 추정한다. 우리에게는 경쟁 도구이자, 우리 degeneracy 질문을 적용할 '판정 대상' 후보"
created: 2026-10-01
updated: 2026-10-01
type: entity
tags: [degradation, tooling, research]
sources: [raw/articles/2026-10-01-github-research-briefing.md]
confidence: low
explored: false
verificationStatus: unverified
model: claude-opus-5-5
effort: medium
claimType: mixed
evidenceScope: single-source
---

# PyProBE (OCV/DVA 피팅 도구)

## 개요

- 저장소: `https://github.com/ImperialCollegeLondon/PyProBE` · 예제: `https://pyprobe.readthedocs.io/en/latest/examples/ocv-fitting.html`
- 브리핑 요약 (2026-10-01 · 단일 출처): 전극 OCP 와 셀 OCV · ICA · DVA 를 맞춰 **전극 용량과 리튬 재고**를 추정한다.
  예제와 합성 데이터 복원 시험이 있다. 허용적 라이선스.
- **우리가 확인하지 않은 것:** 저장소 · 예제를 직접 읽거나 돌리지 않았다 (브리핑 작성자도 실행하지 않았다고 적었다).
  자유 파라미터 개수, 용량 스케일을 쓰는지, 불확실성 · 식별성 진단을 내는지 모른다.
  `confidence: low` 는 그래서다.

## 핵심 사실 — 우리 질문과의 관계

이 도구는 [[birkl-ocv-degradation-diagnostic]] 계열의 **electrode balancing 피팅**을 구현한 것으로 보인다. 우리
연구는 바로 그 피팅이 **유일한 답을 주는가**를 묻는다 ([[fitting-degeneracy]] · [[22p-physics-or-degeneracy]]).
그래서 두 갈래로 쓸 수 있다.

| 쓰임 | 내용 | 주의 |
|---|---|---|
| 경쟁 · 비교 도구 | 같은 곡선에 PyProBE 와 우리 파이프라인을 각각 적용해 LLI · LAM 추정을 비교 | 둘 다 같은 형상 정보를 쓰면 같은 축퇴를 공유할 수 있다 — 일치가 정답의 증거는 아니다 |
| **판정 대상** | 우리 PyBaMM 합성 truth (참값을 아는 곡선) 를 PyProBE 에 넣어 참값을 되찾는지, 초기값 · 피팅 범위에 따라 답이 갈리는지 본다 | [[np-lip-ocv-reparametrization]] 의 2 자유도 정리 — SOC 정규화 OCV **형상**만으로는 세 모드 비율이 다 정해지지 않는다. PyProBE 가 절대 용량을 함께 쓰는지 먼저 확인해야 한다 |

- **미세단락:** 브리핑도 "적합도가 좋다고 미세단락까지 입증되는 건 아니다" 라고 적었다. ISC 판별 도구가 아니다 —
  [[isc-detection-vs-balancing-masking]] 의 근거로 쓰지 않는다.

### 브리핑의 제안 실험 (후보 · 미착수)

"초기 · 열화 저율 곡선 한 쌍을 OCV 와 DVA 방식으로 각각 피팅하고, 평활화 · 피팅 범위를 바꿔도 LLI/LAM 결론이
유지되는지" — 우리 [[fitting-degeneracy]] 의 flat valley 판정과 같은 축이다. 우리 쪽에서 하면 **참값을 아는**
합성 곡선으로 할 수 있다는 점이 다르다 (실측 곡선으로는 "안정적" 이 "정확함" 을 뜻하지 않는다). 착수는 사용자
승인 뒤, 운영 환경 밖 별도 가상환경에서.

## 이 위키와의 관계

- 방법 축: [[fitting-degeneracy]] · 원전: [[birkl-ocv-degradation-diagnostic]] · 자유도: [[np-lip-ocv-reparametrization]]
- 같은 브리핑: [[pybamm]] · 처리 기준: [[daily-github-briefing-triage]]

## 관련
- [[fitting-degeneracy]]
- [[birkl-ocv-degradation-diagnostic]]
- [[22p-physics-or-degeneracy]]
- [[daily-github-briefing-triage]]
