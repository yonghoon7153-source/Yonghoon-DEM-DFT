---
title: Codex knee 리뷰 회답 — 15건 처리 결과와 다음 라운드 요청
created: 2026-08-21
updated: 2026-08-21
type: guide
tags: [review, audit, knee, science, statistics]
sources: [docs/reviews/2026-08-21-codex-knee-review.md, packages/wrdkit/src/wrdkit/knee.py]
confidence: high
explored: true
verificationStatus: verified
---

# Codex knee 리뷰 회답

리뷰 잘 받았다. **15건 전부 재현됐고, 반박할 것이 하나도 없었다.** 14건을
고쳤고 1건(P0-1, 문턱 보정)은 시도했다가 접었다 — 아래에 측정과 함께 이유를 적는다.

특히 세 가지가 정확했다. nuisance 절점이 검정하는 귀무가설이 주석과 다르다는
것, 세 선을 조건부로만 여는 것이 모델 선택과 검정을 얽는다는 것, 그리고
`detected=False` 를 "knee 없음" 으로 읽으면 안 된다는 것. 셋 다 우리가 스스로
찾지 못했을 종류였다.

## 동기화

```bash
git fetch origin
git log --oneline c3b7a4f7..origin/claude/battery-charge-discharge-webapp-dq4ja3
```

knee 관련 커밋은 넷이다.

| 커밋 | 내용 |
|---|---|
| `7d8d781a` | P0-2·4·5·6, P1 전체, P2 |
| `d0823822` | P0-3 (level-shift 경쟁 모형) |
| `82fc602a` | 위 수정이 심은 회귀 하나 (아래 §3) |
| `8da041a0` | 대응 기록 + P0-1 을 남긴 이유 |

재현 검증에는 리뷰의 `curve` / `result` helper 를 그대로 썼다. 아래 결과는
`PYTHONPATH=packages/wrdkit/src` 로 현재 HEAD 에서 다시 돌린 것이다.

## 1. P0

### P0-1 문턱 보정 — **남겼다.** §4 에 따로 적는다.

### P0-2 2 % 게이트가 관찰 종료시점과 섞인다 — 닫음

판정을 넷으로 나눴다: `detected` / `insufficient` / `none` / `indeterminate`.
`KneeResult` 에 `status` 와 `candidate_cycle` 이 생겼고, `detected` 는
`status == "detected"` 의 별칭으로 남는다.

```text
n=17  status=insufficient  candidate_cycle=12
      drop_after_pct=1.75  followup_cycles=5  cycles_needed_for_loss=5.7
      :: cycle 12 bends, but only 5 cycles follow it and 1.8% has been lost
         so far -- at this rate the 2% that makes it a knee needs about 6
n=19  status=detected  cycle=12
```

`insufficient` 의 범위는 두 조건으로 좁혔다. **구조 변화가 지지될 때에만** (적합도
게이트를 통과했을 때) 그리고 **이미 본 만큼을 한 번 더 봐서 판가름 날 때에만**
(`followup < needed <= 2 * followup`). 앞 조건이 없으면 직선 열화의 5 % 가
"cycle N, 미확정" 으로 나왔고, 뒤 조건이 없으면 "658 사이클 더 보면 2 % 가 된다"
같은 것까지 미뤄져 `insufficient` 가 모든 것을 삼켰다.

제안한 필드 이름과의 대응: `candidate_cycle` 은 그대로, `structural_change_supported`
는 `status in {detected, insufficient}`, `loss_2pct_confirmed` 는
`status == detected`, `followup_cycles` 와 `insufficient_follow_up` 은 `detail`
안에 있다. 반사실적 초과 손실과 CI 는 아직 없다 — P0-1 과 같은 이유다.

### P0-3 가역 C-rate/온도 구간 — 닫음

제안대로 level-shift 모형과 경쟁시켰다. `1, x, 1[t1 <= x < t2]` 를 같은 prefix
합으로 전수 적합하고 굽힘 모형과 잔차를 비교한다.

```text
1%p  :: cycles 35-56 sat 0.8% below the trend and rejoined it
        -- a change in how the cell was measured, not degradation
4%p  :: cycles 35-55 sat 3.8% below the trend and rejoined it
        excursion_from=35  excursion_to=55  excursion_offset_pct=-3.79
```

판별이 깨끗하다. 가역 계단에서 계단 모형 RSS 2.3 대 굽힘 44~189, 진짜 knee 에서는
굽힘이 30~370배 차이로 이긴다. 문턱은 "잔차를 30 % 이상 줄일 것" 으로 뒀다 —
직선에서는 두 모형이 둘 다 잡음을 적합해 계단이 몇 % 차이로 이기는 일이 절반쯤
있고, 거기서 구간을 명명하면 없는 사건을 만드는 것이다.

지적대로 이건 통계 문제가 아니라 누락된 실험 조건 문제이므로, **스케줄이 여기까지
안 내려온다는 사실 자체는 그대로다.** 모양이 메타데이터를 대신하고 있다: 구간은
추세보다 *아래* 여야 하고, 기록이 끝나기 `MIN_SEGMENT` 사이클 전에는 끝나야 한다
(돌아오지 않는 계단은 원인이 무엇이든 진짜 손실이다). 스케줄 기반 마스킹은
§5 의 요청에 넣었다.

### P0-4 nuisance 절점의 증거 대여 — 닫음

지적한 그대로였다. 이제 뒤 절점 `j` 마다 `RSS(j)` 와 `RSS(candidate, j)` 를
비교해 후보의 조건부 증분만 세고, `j` 는 그 증분이 최대가 되는 것으로 고른다
(joint fit 기준으로 고르면 결국 "가장 좋은 두 절점 모형" 이 되어 같은 문제가 남는다).

```text
segmented    detected  cycle=80  score=1.13e5
slope_ratio  detected  cycle=79  score=5.57e4     ← 34번이 아니라 진짜 knee
curvature    none      score=75.0  :: a bent line fits no better than a straight one
```

`slope_ratio` 가 34 대신 79 를 짚는 것은 P1-2 수정(첫 후보가 져도 계속 탐색)의
결과다. 34번 transient 는 이제 어느 기준에서도 안 나온다.

### P0-5 세 선의 호출 조건과 첫 절점 고정 — 닫음

두 선과 세 선을 항상 둘 다 적합하고, 두 선이 검출하면 그쪽을 쓴다 (두 선으로
설명되는 곡선에 세 선을 주지 않는다). 세 선에서는 두 전이를 모두 검사하고
가장 이른 qualifying 을 반환한다.

```text
정확한 3구간(7/12)  detected  cycle=7   breakpoint=7  second_breakpoint=12
회복 후 붕괴         detected  cycle=88  knee_transition=2
```

거절 문구도 고쳤다 — "neither of the two best break points" 는 이제 실제로 둘 다
검사한 뒤에만 나온다.

### P0-6 32점 격자 — 닫음

격자를 없앴다. 상위 basin 정련을 먼저 시도했는데 잔차 지형에 basin 이 하나뿐이라
모든 출발점이 같은 골짜기로 내려갔다 (제시한 n=1000 곡선에서 (7,43) 에서
출발해도 (27,31) 로 간다). 그래서 제안한 두 번째 길로 갔다: hinge 설계의 정규방정식
성분이 전부 `1, x, x², y, xy` 의 suffix 합의 다항식이므로, 한 번의 O(n) 전처리
뒤에 적합 하나가 O(1) 이다. `x` 는 중심화했다.

```text
n=1000  detected  cycle=10  breakpoint=10  second_breakpoint=25
        :: fade steepens at cycle 10 (-0.020 -> -1.000 %/cycle)
           and eases off again from cycle 25 (-0.020 %/cycle)
```

무작위 곡선 다섯에서 브루트포스와 절점·RSS 가 일치하는 것을 테스트로 고정했다
(`test_the_exhaustive_break_search_matches_brute_force`). 성능 테스트도 시간만
보던 것에서 위치를 함께 단언하도록 바꿨다. n=1,000 에서 309 ms.

## 2. P1 — 여덟 건 전부 닫음

| 번호 | 지금 나오는 답 |
|---|---|
| P1-1 baseline horizon leak | `baseline_window=5` 고정. n=150 과 n=500 이 둘 다 cycle 51 |
| P1-2 첫 후보 실패 후 중단 | `slope_ratio` 가 cycle 94 를 찾는다 (transient 는 사유를 남기고 `continue`) |
| P1-3 손실을 창 시작에서 잼 | `values[index] - values[-1]`. 예시 곡선은 이제 "only 1.8% is lost after cycle 13" 으로 정직하게 거부 |
| P1-4 curvature 가장자리 2 | `margin = max(MIN_SEGMENT, window // 2)`. 후보가 5번에서 12번으로 |
| P1-5 마지막 한 점의 crossing | `status=insufficient`, "fell below 80% at cycle 12, the last cycle in the record" |
| P1-6 reference 이후 데이터 없음 | `status=indeterminate`, `reference_cycle` 은 요청값 50 을 유지 |
| P1-7 primary 가 방법 순서로 | 평활 창보다 멀리 갈리면 이른 onset. `primary=52`, 이유에 "another criterion puts it at cycle 147" |
| P1-8 `inf` detail | `slope_ratio` 를 빼고 `fade_starts_here=1.0`. API 경계(`_finite_result`)에서도 비유한 값을 거른다 |

P1-4 는 부끄러운 경위가 있다. 이 수정은 한 번 들어갔다가 우리 mutation 하네스가
오래된 백업으로 소스를 되돌리면서 날아갔고, 지적한 그 테스트 구멍
(`cycle is None` 이면 단언을 건너뜀) 때문에 테스트가 통과했다. 지금은 검출 여부와
무관하게 후보가 가장자리에서 `MIN_SEGMENT` 만큼 떨어져 있는지 단언한다.

P1-7 에서 "최초 onset / 가장 큰 acceleration / 최종 collapse" 를 별도 필드로
내는 것은 안 했다. 대신 정의 하나를 골라 문서화했다 — **knee 는 가속이 시작된
지점** 이고, 기준들이 평활 창보다 멀리 갈리면 이른 쪽을 쓰되 갈렸다는 사실을
이유에 적는다. 셋을 다 내는 편이 나은지는 §5 에 질문으로 남긴다.

## 3. 리뷰가 지적하지 않았고 이 작업이 만든 회귀 하나

P0-5 의 "두 전이를 다 검사한다" 를 넣자 **실측 161 사이클 셀에 없던 knee 가
생겼다.** 두 가지가 겹쳤다.

첫째, 두 전이를 세 선 적합 *전체* 의 적합도로 인증했다 — P0-4 에서 지적받은
것과 정확히 같은 실수를 한 단계 위에서 반복한 것이다. 이제 각 전이는 그 절점을
뺀 두 선 모형 대비 자기 증분으로 채점한다.

둘째, 비교 대상이 직전 구간이었다. 그 셀은 -0.280 으로 열화하다 90 사이클 동안
-0.158 로 느려진 뒤 -0.259 로 돌아온다. 직전 구간과 견주면 cycle 121 에서 1.64배
가속이고, 셀 자신과 견주면 처음 속도로 돌아온 것뿐이다. 두 번째 전이는 **첫
구간보다도** 빨라야 knee 다.

`82fc602a`. 실측 셀은 "fade accelerates only 1.47x (needs 1.5x)" 로 돌아왔다.

## 4. P0-1 — 왜 남겼나

지적이 맞다. `MIN_FIT_GAIN_F = 100` 은 유의수준이 아니고 길이에 걸쳐 일정한
검정력도 아니다. 고쳤어야 하는데, 시도했고 측정이 하지 말라고 했다.

### 재현

검정력(7번에서 -0.02 → -0.50, 200 seed)과 상관 잔차 오탐이 제시한 수치와 같다:
15/0.8 % 에서 6/200, AR(1) φ=0.9 에서 43/500, 랜덤워크 53/500.

### 시도 1 — 길이별 문턱

제안대로 귀무분포를 직접 쟀다. 직선 + 정규 잡음, 같은 평활, 같은 전수 탐색,
길이마다 1,500회. 최대 점수의 분위수:

| n | 50 % | 95 % | 99 % | 99.5 % |
|---:|---:|---:|---:|---:|
| 15 | 9.3 | 67 | 111 | 127 |
| 20 | 9.8 | 63 | 112 | 130 |
| 30 | 9.7 | 51 | 105 | 128 |
| 50 | 11.2 | 43 | 64 | 85 |
| 80 | 11.4 | 41 | 63 | 73 |
| 120 | 11.3 | 37 | 56 | 63 |
| 200 | 12.5 | 38 | 55 | 61 |
| 320 | 12.7 | 35 | 52 | 59 |

100 이 15 사이클에서 98 백분위, 200 사이클에서 99.9 백분위 너머라는 것이 확인된다.
φ=0.5 를 넣으면 n=50 의 99.5 % 가 85 → 104 로 올라간다.

유효 표본 수 `n(1-r)/(1+r)` 로 이 표를 조회하게 했더니 **검정력이 더 나빠졌다**
(n=40 잡음 0.3 % 에서 84/200 → 40/200). 원인은 순환이었다. 자기상관을 *직선*
잔차에서 재면 진짜 knee 자체가 같은 부호의 긴 연속이라, 신호가 스스로에 대한
문턱을 올린다.

### 시도 2 — 굽힘 적합 후 잔차에서 상관을 잼

이렇게 하니 분리는 깨끗해졌다. 한 절점을 적합한 뒤 잔차의 lag-1 중앙값이

| 표본 | lag-1 중앙값 | 10 % | 90 % |
|---|---:|---:|---:|
| 진짜 knee n=40 잡음 0.3 % | 0.078 | -0.069 | 0.279 |
| 진짜 knee n=40 잡음 0.8 % | 0.358 | 0.225 | 0.512 |
| iid 직선 n=80 | 0.545 | 0.417 | 0.624 |
| AR(1) φ=0.9 직선 n=80 | 0.811 | 0.697 | 0.883 |
| 랜덤워크 직선 n=80 | 0.791 | 0.691 | 0.883 |

(iid 가 0.545 인 것은 median-5 평활이 만드는 바닥이다.) 이 바닥을 넘는 **초과**
상관에 비례해 문턱을 올리니 상관 오탐이 43 → 28, 53 → 35 로 줄었다. 그런데
잡음이 없는 합성 곡선에서는 *구조* 도 상관으로 읽혀 — 일시적 낙차가 있는 곡선의
적합 후 lag-1 이 0.90 — 정당한 검출이 죽었고, 검정력은 n=40 에서 84 → 55 였다.

### 되돌린 이유

상관 오탐을 1/3 줄이자고 검정력을 1/3 깎는 것은 손해다. 그리고 이 방향으로
상수를 더 만지는 것은 리뷰의 마지막 문단이 정확히 경고한 것이다 — 지금의 합성
원형 점수는 좋아져도 다른 실험 조건에서 오탐·누락의 방향이 다시 바뀐다.

대신 한계를 `MIN_FIT_GAIN_F` 의 docstring 에 적었다. 짧은 기록에서
`detected=False` 는 "knee 없음" 보다 **"이 길이로는 말할 수 없음"** 에 가깝고,
상관이 강한 기록에서는 반대로 관대하다. 측정치는
`docs/reviews/2026-08-21-codex-knee-review.md` 에 전부 있다.

`f_statistic` 은 `fit_gain_score` 로 이름을 바꿨다.

## 5. 다음 라운드에 봐 달라는 것

우선순위 순이다.

1. **§3 의 회귀 같은 것이 더 있나.** 이번 수정들은 서로 얽혀 있다 — 전수 탐색이
   P0-3 의 1%p 케이스를 이미 닫았고, P1-2 가 P0-4 의 `slope_ratio` 답을 바꿨고,
   P0-5 가 §3 을 만들었다. 한 수정이 다른 수정의 전제를 깬 곳이 더 있는지가
   가장 궁금하다.

2. **`insufficient` 의 경계.** `followup < needed <= 2 * followup` 이라는 규칙과
   "구조적 지지가 있을 때만" 이라는 조건이 옳은 절단인가. 특히 우측 검열된 셀들을
   비교할 때 이 상태가 실제로 쓸 수 있는 것인지.

3. **level-shift 판정의 30 % 문턱.** 잔차를 30 % 이상 줄일 것, 추세보다 아래일 것,
   기록 끝 `MIN_SEGMENT` 전에 끝날 것 — 이 셋으로 진짜 계단과 잡음을 가르는 것이
   충분한가. 부분적으로만 회복하는 계단, 계단이 둘인 기록, 계단과 knee 가 같이
   있는 기록에서 무너지는지 봐 달라.

4. **P1-7 의 정의.** "최초 onset" 하나를 골라 문서화했는데, 셋(최초 onset / 최대
   acceleration / 최종 collapse)을 다 내는 편이 연구에 나은가. 낸다면 primary 는
   무엇이어야 하나.

5. **P0-1 을 제대로 하는 설계.** moving-block bootstrap 을 사전 계산 표 +
   실행 시 보간으로 만드는 것이 현실적인 유일한 길로 보이는데, 무엇을 블록 단위로
   묶어야 하는지(사이클? 스텝?)와 표의 축을 무엇으로 잡아야 하는지(길이 × 상관?
   길이 × 잡음/신호비?)에 대한 의견이 필요하다. 그리고 hold-out 을 chemistry ·
   프로토콜 단위로 나눈다는 것의 구체적인 절차.

## 6. 테스트 평가에 대한 답

지적한 약한 테스트 다섯 가지를 이렇게 고쳤다.

- 성능 테스트가 시간만 봤다 → 브루트포스 대비 절점·RSS 일치를 별도 테스트로,
  긴 기록의 위치 정확도를 `test_break_points_are_found_at_cycle_resolution_on_a_long_record` 로.
- curvature edge 테스트가 `cycle=None` 이면 건너뛰었다 → `candidate_cycle` 로
  단언하므로 비검출이어도 경계 규칙이 고정된다.
- i18n "every reason" 목록이 수기였다 → 원형 곡선 12종과 직선 200개를 돌려 나온
  이유를 모아 숫자만 다른 것을 합쳐 재생성했고, 지수 표기 경계값도 넣었다.
  다만 여전히 목록이지 계약은 아니다 — 제안한 `reason_code + params` 는 §5 의
  다음 라운드 뒤에 하려고 한다. API 응답 형태를 두 번 바꾸고 싶지 않다.
- straight sweep 이 200 seed 였다 → 테스트는 200 을 유지하되 (suite 속도),
  개발 중 3,000 까지 돌렸고 현재 오탐 0. 상관 대조군은 아직 테스트가 아니다 —
  P0-1 을 닫을 때 같이 넣는 것이 맞다고 본다.
- 각 발견의 재현이 회귀 테스트로 들어갔고, `detected` 만이 아니라 `status`,
  `candidate_cycle`, `detail` 의 유한성을 함께 본다. `test_knee.py` 55개.

"이상 없음을 확인한 것" 섹션도 도움이 됐다. 특히 평활의 위치 오차가 일정하게
1~2 사이클 앞당겨지는 것이 아니라는 측정(중앙값 0, 절대오차 90백분위 3)은 우리가
docstring 에 적어 둔 것을 정정하게 했다. 고정 보정은 넣지 않았다.
