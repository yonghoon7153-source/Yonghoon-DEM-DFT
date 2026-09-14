---
title: 반쪽전지 OCP 형상 불변 가정과 그 파괴 (blend 전극)
description: "The α·β affine-rescaling premise behind every electrode-balancing diagnostic, where it breaks for Si/graphite blends, and the directional bias it leaves in LLI/LAM"
created: 2026-09-10
updated: 2026-09-14
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/schmitt2022_sic-ocp-shape-change-degradation-modes.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/dubarry2012_synthesize-degradation-modes.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/transcripts/2026-09-14-bms-handoff-width-and-wiki-candidates.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-primary
---

# 반쪽전지 OCP 형상 불변 가정과 그 파괴 (blend 전극)

## 정의

electrode balancing 계열 진단([[dubarry-mechanistic-mode-synthesis]],
[[birkl-ocv-degradation-diagnostic]], 우리 파이프라인)은 모두 다음을 깔고 있다:

> **열화한 전극의 OCP 곡선은 pristine 곡선의 아핀 변환(선형 스케일 + 평행이동)
> 으로 얻어진다.** 즉 곡선의 **모양은 불변**이고, 열화는 좌표축의 늘림·이동으로만
> 나타난다.

Schmitt et al. 2022 (JPS 532, 231296) 가 이 전제를 원문 그대로 진술한다
`[인쇄]`: "The shape of the OCP curve of the individual electrodes is
**generally regarded to be invariant** during battery aging… the OCP curve of an
aged electrode can be obtained by **linear scaling** of the OCP curve of a
pristine electrode."

이 가정이 있어야 4-파라미터 창 좌표 `(α_cat, β_cat, α_an, β_an)` 가 열화 상태를
**완전히** 기술한다고 말할 수 있다.

## 어디서 깨지는가

`[인쇄]` Schmitt 2022 의 실험적 답: **음극이 blend (Si/graphite) 일 때**.

blend 전극의 OCP 는 두 성분 곡선의 합성이다 (Schmidt et al. 2013 모델, 식 14–15):
```
Q_blend(U) = γ_Si · Q_Si(U) + (1 − γ_Si) · Q_G(U)
U_blend(Q) = f⁻¹(Q_blend(U))
```
`γ_Si` = 음극 총 용량 중 Si 가 제공하는 분율. **Si 가 graphite 보다 빨리
열화**하면 `γ_Si` 가 줄고, 위 합성의 결과로 **곡선의 모양 자체가 바뀐다**
(graphite·Si DV peak 가 낮은 전극 SOC 쪽으로 이동). 아핀 변환은 이 변형을
표현할 수 없다.

`[인쇄]` 측정된 파괴의 크기 (LG INR18650-MJ1, 25 °C, C/2 충전 / 1 C 방전):
**γ_Si = 9.52 % (pristine) → 5.55 % (488 EFC)** = **초기값의 약 58 %**.
반면 같은 셀의 **NMC-811 양극은 형상이 유지된다** (선행 논문 JPS 506, 230240).

## 왜 중요한가 — 축퇴와 구별되지 않는 편향을 만든다

★ 핵심은 `γ_Si ↓` 와 `α_an ↓` 가 **full-cell 관측에 같은 서명을 남긴다**는 것이다.
둘 다 full-cell DV 에서 **음극 feature 를 왼쪽으로 민다**. Schmitt 의 문장
`[인쇄]`: "**As both effects would lead to the same results with regard to the
full-cell OCV**, the left-shift of the anode peaks in the full-cell DV can be
**misinterpreted as resulting solely from an overall anode active material
loss**."

따라서 형상 불변을 강제하면 모드 추정이 **무작위 오차가 아니라 방향이 정해진
편향**을 받는다 `[인쇄]` (486 EFC 셀):

| 모드 | pristine 곡선 강제 | 형상 변화 고려 | 편향 |
|---|---|---|---|
| LAM_an | 15.5 % | 13.1 % | **+2.4 pp 과대** |
| LAM_cat | ≈2.3 % `[도표]` | ≈6.5 % `[도표]` | **≈3 pp 과소** |
| LLI | ≈13.2 % `[도표]` | ≈14.2 % `[도표]` | **≈1.1 pp 과소** |

그리고 **적합도는 이 선택을 거의 구별하지 못한다**: full-cell OCV 재구성 RMSE
**9.9 → 8.2 mV** (Δ 1.7 mV). 그런데 **"어느 전극이 충전 종료를 제한하는가" 라는
정성적 결론은 뒤집힌다** (음극 제한 → 음극 비제한).

`[해석]` 이것은 [[fitting-degeneracy]] 와 **같은 증상, 다른 원인**이다.
축퇴는 *데이터가 방향을 못 정하는 것*이고 이쪽은 *모델이 틀린 것*
(model misspecification)이다. 그런데 관측에서 보이는 모습 — 적합도는 그대로인데
파라미터가 크게 움직인다 — 은 구별되지 않는다. **우리 좌표 자체가 불완전할 수
있다**는 것이 이 개념 페이지가 위키에 있어야 하는 이유다.

## 처방과 그 대가

`[인쇄]` Schmitt 2022 가 비교한 세 가지:

| 처방 | 내용 | 대가 |
|---|---|---|
| ① 무시 | pristine 곡선 + α·β 만 | 위 표의 방향성 편향 |
| ② 다시 잰다 | 같은 열화 상태의 aged half-cell OCP 를 측정해 입력 | **셀을 뜯어야 한다** → 진단법이 못 된다. 분석용으로만 |
| ③ **γ_Si 를 자유 파라미터로** | pristine 순수 Si·graphite 곡선으로 blend 모델을 세우고 `γ_Si` 를 4개 정렬 파라미터와 **동시 최적화** (5-파라미터) | 자유도 4→5, **`γ_Si` ↔ `α_an` 새 축퇴 위험 (저자 미검사)**, 성분별 pristine 곡선 필요, 평형·병렬 lithiation 가정 |

③ 이 저자의 제안이며 **부수 이득**이 하나 있다: full-cell 저전류 충전 곡선만으로
`γ_Si` 를 비파괴 추정할 수 있고, 그 값이 half-cell 로 얻은 값과
**0.8 pp 이내**로 맞는다 (다만 full-cell 쪽이 7/7 점 모두 위 = **계통 편향**).

`[해석]` ②③ 어느 쪽도 **모드 추정치의 정확성을 독립적으로 검증하지 않는다**.
Schmitt 가 "validity 가 개선된다" 고 말할 때 근거는 (i) RMSE 1.7 mV 감소,
(ii) `γ_Si` 교차 일치 두 가지뿐이며, **LAM_an = 13.1 % 가 15.5 % 보다 참에
가깝다는 독립 측정은 없다**. 이것은 측정 논증이 아니라 **모델 선택 논증**이다.

## 이 위키에서의 적용

1. **우리 좌표의 유효 범위 표시.** `degradation-degeneracy` 는 합성 truth 를
   PyBaMM 으로 만들므로 형상 불변이 **정의상 참**이다 (같은 OCP 함수를 쓴다).
   즉 우리가 재는 축퇴는 **형상이 불변인 이상적 조건에서의 하한**이고, 실제
   Si/graphite 셀에서는 여기에 형상 오설정 편향이 **더해진다**.
2. **[[halfcell-window-parametrization-lineage]] 의 다섯 번째 파라미터.**
   `γ_Si` 는 여분을 **죽이는** 처방이 아니라 **늘리는** 처방이다 — 그 표의 세
   처방(등식/사전믿음/안 만들기)과 직교하는 네 번째 방향.
3. **[[np-lip-ocv-reparametrization]] 의 2 자유도 정리와의 관계.** Lin & Khoo 는
   *전극 OCP 함수가 고정일 때* 형상이 두 비(比)에만 의존함을 보였다. blend 전극은
   그 **함수 자체를 `γ_Si` 로 매개화된 족(family)** 으로 바꾼다 → 자유도가
   2 → 3 이 되고, 정리의 전제가 성립하지 않는다.
4. **검증 체크리스트**: 실셀 데이터에 electrode balancing 을 적용할 때
   (a) 음극이 blend 인가, (b) 그렇다면 `γ_Si` 를 자유롭게 뒀는가,
   (c) 뒀다면 `γ_Si` ↔ `α_NE` 상관을 뽑았는가. (c) 를 한 논문은 아직 없다.

## ★ 원전이 재지 않은 자리의 첫 숫자 (2026-09-14, `bms-balancing/` 실측)

Schmitt 2022 는 본문에서 `γ_Si` 와 `α_an` 이 **같은 서명을 남긴다**고 적어 놓고
그 폭을 **재지 않았다** (논문에 identifiability · degeneracy · confidence region
이라는 단어가 없다). 서브 브랜치가 그 자리의 첫 숫자를 냈다.

논문이 "좋은 재구성" 이라 부른 **pOCV RMSE 12 mV** 문턱 안에서:

| 유도량 | 폭 |
|---|---|
| LAM_NE | −4.38 % ~ +13.00 % → **17.4 %p** |
| LLI | **1.14 %p** |

⚠ **문턱을 떼고 인용하면 안 된다.** 그 12 mV 는 **다른 셀·다른 목적함수**에서
온 값이고, 문턱을 8 / 10 / 11 / 12 mV 로 옮기면 폭이
7.25 / 13.59 / 16.00 / 17.38 %p 로 변한다. 12 mV 가 받아들이는 점 중에는 이
연구 자신의 결합 목적함수에서 최적보다 **42.9 % 나쁜** 것이 있다.

이 폭이 어떻게 측정됐는지(그리고 왜 등방 표집이나 Hessian 으로는 못 재는지)는
[[near-optimal-set-width-measurement]]. 수치의 정본은
`bms-balancing/reviews/BML_R1_RESPONSE.md` 이고 이 줄들은 사본이다.

## 반대 해석 / 데이터 공백

- **`γ_Si` 변화가 형상 변화의 유일한 원인이라는 보장이 없다.** graphite 자체의
  변화, 전극 불균일(Schmitt 자신이 stage 2 peak 높이 감소를 inhomogeneity 탓으로
  돌린다), SEV/kinetic 효과가 `γ_Si` 로 흡수됐을 수 있다 — 검정되지 않았다.
- **Si OCP 곡선이 남의 논문(결정질 Si, Li & Dahn 2007)에서 왔다.** 대상 셀은
  SiO_x 다. `γ_Si` 의 **추세**는 강건해도 **절대값**(9.5 %, 1.08 wt.%)은 아니다.
- **aging state 당 셀 1개, 오차 막대 없음.** 같은 그림에서 LAM_cat 이 **−2.6 %**
  (물리적 불가) 까지 내려간다 → 추정 잡음이 주장하는 효과 크기(1–3 pp)와 **같은
  자릿수**다. 따라서 위 편향 표의 숫자는 **방향은 신뢰, 크기는 유보**로 읽는다.

## 관련
- [[fitting-degeneracy]] — 같은 증상(적합도 불변, 파라미터 이동)의 다른 원인
- [[halfcell-window-parametrization-lineage]] — 자유 파라미터 개수·제약의 계보표
- [[np-lip-ocv-reparametrization]] — 전극 OCP 함수 고정 시의 2 자유도 정리
- [[dubarry-mechanistic-mode-synthesis]] · [[birkl-ocv-degradation-diagnostic]] — 이 가정을 깔고 있는 원전들
