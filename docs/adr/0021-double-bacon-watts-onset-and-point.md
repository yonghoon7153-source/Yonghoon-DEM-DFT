# ADR 0021 — Double Bacon-Watts 로 knee-onset 과 knee-point 를 함께 구한다

- 상태: 채택 (2026-08-25)
- 관련: ADR 0005, `packages/wrdkit/knee.py`,
  Fermín-Cueto et al., *Energy and AI* 1 (2020) 100006

## 맥락

ADR 0005 의 네 기준은 전부 **꺾임 하나**를 찾는다. 그런데 사용자가 실제 곡선을
보며 가리키는 지점은 그보다 이르다 — 급감이 완성된 곳이 아니라 **시작되는 곳**
이다. 문헌은 이 둘을 구별한다 (Fermín-Cueto 2020):

- **knee-onset** — 완만한 열화가 처음 벗어나기 시작하는 사이클
- **knee-point** — 급감 국면이 자리 잡은 사이클

둘은 같은 사건의 앞끝과 뒷끝이고, 하나만 보고하면 나머지 반은 사용자가 눈으로
다시 찾아야 한다. 기존 `segmented`(정확 조각선형)는 knee-point 쪽 답이다.

## 결정

**Double Bacon-Watts (DBW) 를 다섯 번째 기준으로 넣고, 검출되면 primary 로
쓴다.** 모델 (Fermín-Cueto 2020 정의):

```
Q(x) = α0 + α1(x−x1) + α2(x−x1)·tanh((x−x1)/γ1) + α3(x−x2)·tanh((x−x2)/γ2)
```

x1 이 knee-onset, x2 가 knee-point 다 (γ 는 전환의 급격도). 한 번의 적합이
두 지점을 **같은 곡선의 매개변수로** 추정하므로, 서로 다른 기준 둘을 나란히
놓고 "이쪽이 onset 이겠지" 하는 것보다 정합적이다.

primary 우선순위는 `dbw` → `segmented` → `slope_ratio` (ADR 0005 의 나머지는
그대로). `segmented` 는 DBW 가 수렴하지 않거나 게이트에 걸릴 때의 대답으로
남는다.

### 적합 방법

DBW 는 초기값에 민감하다 — 한 번의 `curve_fit` 은 지역 최소에 잘 빠진다.
(x1, x2) 초기값을 격자로 훑되, 격자마다 비선형 적합을 돌리는 대신 **변수 분리**
를 쓴다: (x1, x2, γ) 를 고정하면 모델은 α 에 대해 선형이므로, 격자점마다
최소제곱을 닫힌 식으로 풀어 SSE 를 재고, 가장 좋은 씨앗 몇 개에서만
`scipy.optimize.curve_fit` (TRF, 경계 포함) 을 돌린다. 같은 격자 탐색을 수백
번의 비선형 적합 없이 하는 것뿐이고, 결과는 전 격자 p0 방식과 같은 것을 더
확실하게 준다 (선형 부분문제는 정확히 풀리므로).

경계는 제공된 절차 그대로: α 는 자유, x1·x2 ∈ [x_min, x_max], γ ∈ [0.1, 20].
x1 > x2 로 수렴하면 라벨을 정렬한다 — 모델이 (α2,x1,γ1)↔(α3,x2,γ2) 교환에
대칭이라 같은 곡선이다.

### 게이트 — 언제나 답이 나오는 방법이므로

`curve_fit` 은 항상 무언가에 수렴한다. `curvature` 가 panel 에만 남은 것과
같은 이유로, DBW 도 ADR 0005 의 게이트를 전부 통과해야 검출이다: 가속비
1.5배(`MIN_SLOPE_RATIO`, 점근 기울기 (α1−α2−α3) → (α1+α2+α3) 로 계산),
knee-point 이후 실측 손실 2 %p(`MIN_KNEE_DROP_PCT`), 굽은 모델의 적합 이득
(`MIN_FIT_GAIN_F`, 자유도 8 기준). 직선 열화 null sweep 200개에서 오탐 0 을
테스트가 고정한다.

### 알려진 한계 — sub-linear 궤적

가속 없이 점점 완만해지는(sub-linear) 곡선에서 DBW 는 knee-point 를 기록 끝
너머로 밀어 과대추정한다 (Zhang 2023 arXiv:2304.11671; IOPscience 2026). 그런
적합은 x2 가 탐색 경계나 기록 말단에 붙는 모양으로 나타나므로, **x2 가 마지막
`MIN_SEGMENT` 사이클 안이나 경계에 붙으면 검출로 치지 않고 이유를 적는다**
(§0.4). 가속 게이트가 대부분을 이미 걸러내지만, 이 모양은 이름을 불러 준다.

### Bootstrap 신뢰구간

Fermín-Cueto 2020 은 사례 재표집 bootstrap 으로 95 % CI 를 낸다.
`dbw_confidence_interval()` 로 제공하되 **API 경로에서는 부르지 않는다** —
재표집 하나가 적합 하나라 200회면 대시보드가 초 단위로 느려지고, CI 는 보고서
쓸 때 한 번 필요한 값이지 화면마다 필요한 값이 아니다.

## 결과

- 리포트가 onset 과 point 를 함께 말한다: "20번부터 벗어나기 시작해 24번에
  급감이 자리 잡았다".
- `KneeResult` 에 `onset_cycle` 이 생긴다 (DBW 만 채운다; 나머지 기준은 None).
- wrdkit 코어는 numpy 만 의존한다는 약속은 유지된다: scipy 는 함수 안에서
  지연 import 하고, 없으면 DBW 는 이유를 적고 빠진다 (`wrdkit[eis]` 가 설치
  경로다 — Makefile/bml/API requirements 전부 이미 깔고 있다).
- 대가: 리포트 경로가 곡선당 수십 ms 무거워진다 (격자 선형탐색 + 비선형 적합
  소수). 측정해서 상한을 테스트에 고정한다.

## 참고 문헌

- Bacon & Watts, *Biometrika* 58(3) (1971) — 원조 전환 회귀.
- Fermín-Cueto et al., *Energy and AI* 1 (2020) 100006 — DBW 를 배터리 열화에
  도입, onset/point 정의와 bootstrap CI. **이 구현의 원 출처.**
- Diao, Saxena, Pecht, *Energies* 12 (2019) 2910 — slope changing ratio.
- Satopaa et al., ICDCS Workshops (2011) — Kneedle (최대 곡률).
- Zhang et al., arXiv:2304.11671 (2023) — sub-linear 궤적에서 DBW 의
  knee-point 과대추정과 곡률 기반 보완.
