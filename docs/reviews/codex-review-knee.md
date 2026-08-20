---
title: Codex 리뷰 과제 — knee 판정 (과학 코어)
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [review, audit, knee, science]
sources: [packages/wrdkit/src/wrdkit/knee.py, packages/wrdkit/tests/test_knee.py]
confidence: high
explored: false
verificationStatus: unverified
---

# Codex 리뷰 — knee 판정

이 저장소에서 **틀리면 논문이 틀리는** 코드가 하나 있다면 `wrdkit/knee.py` 다.
용량 급감 지점을 몇 번 사이클이라고 말하는 곳이고, 그 숫자가 셀 비교의 결론이
된다. 다른 리뷰 과제들과 달리 이번 것은 범위가 좁다 — 파일 하나와 그 테스트.
대신 **깊게** 봐 달라.

리뷰 대상 커밋: `c3b7a4f7`

```
packages/wrdkit/src/wrdkit/knee.py      +246 / -60
packages/wrdkit/tests/test_knee.py      +281 / -2
apps/web/src/lib/i18n.ts                (이유 문구 한글화)
```

## 0. 준비

```bash
git fetch origin
git checkout -b codex/knee-review origin/claude/battery-charge-discharge-webapp-dq4ja3
git log -1 --stat c3b7a4f7

# 검증 환경
make setup            # 없으면: python -m venv .venv && .venv/bin/pip install -e packages/wrdkit
.venv/bin/python -m pytest packages/wrdkit/tests/test_knee.py -q
```

작업은 **네 브랜치**에서. 이 브랜치(`claude/battery-charge-discharge-webapp-dq4ja3`)
에 직접 커밋하지 말고, 결과를 md 로 돌려주면 우리가 반영한다. 한 폴더에서 두
브랜치를 오가지 말 것 — `git worktree add` 를 쓴다 (CLAUDE.md §0.7).

## 1. 무엇을 왜 바꿨나 (맥락)

실측 4.6 V 전고체 셀에서 "두 직선 교점" 기준이 판정을 거부했다. 곡선 모양은
**평탄(3\~23) → 급감(24\~32) → 다시 완만(33\~62)** 이다. 이 랩의 고전압 셀에서
흔한 모양이다.

두 직선 모형은 꺾임을 하나만 놓을 수 있으므로, RSS 를 최소화하는 절점이
*감속* 구간(45번 부근)에 떨어진다. 거기서는 열화가 이전보다 느리므로 코드가
"절점 이후로 가속하지 않는다" 를 반환했다 — 기술적으로 맞고, 쓸모없다.

그래서:

1. 두 직선이 그 이유로 거부하면 **세 직선 적합**으로 승격하고 첫 절점을 knee 로
   본다. 두 번째 절점(다시 완만해지는 곳)도 이유 문장에 적는다.
2. **손실 게이트** `MIN_KNEE_DROP_PCT = 2.0` — knee 이후 실제로 2 %p 는 잃어야
   한다. 비율만 보면 -0.021 → -0.116 %/cycle 이 5.55 배지만 남은 사이클을 다
   합쳐도 0.5 % 인 건강한 셀에 knee 가 붙었다.
3. **굽힘 검정** `MIN_FIT_GAIN_F = 100` — 세 기준이 각자 다른 방식으로 사이클을
   제안하지만 주장은 같다("여기서 꺾인다"). 그러면 검정도 하나면 된다: 거기서
   꺾은 선이 곧은 선보다 잘 맞아야 한다.
4. **기준 기울기를 중앙값으로**, **잡음 여유 2σ**(겹치지 않는 창들의 연속
   차분으로 추정), **창의 가운데를 답으로**, **곡률의 가장자리 여유를
   MIN_SEGMENT 로**.
5. `primary` 에서 `threshold` 와 `curvature` 를 뺐다.

측정 결과 (원형 곡선 12종 + 직선 열화 400개):

| 기준 | 맞음/틀림/놓침 | 직선 400개 오탐 |
|---|---|---|
| segmented | 8/1/1 → **11/1/0** | 5 → **0** |
| slope_ratio | 5/4/1 → **9/1/2** | 68 → **0** |
| curvature | 8/2/0 → **10/1/0** | 40 → **0** |
| primary | 4/6/0 → **11/1/0** | 69 → **0** |

## 2. 봐 달라는 것 (우선순위 순)

### P0 — 상수가 데이터에 과적합됐나

가장 의심스러운 지점이다. `MIN_FIT_GAIN_F = 100`, `MIN_KNEE_DROP_PCT = 2.0`,
`SLOPE_NOISE_SIGMAS = 2.0` 은 전부 **우리가 만든 합성 곡선**으로 골랐다. 곡선을
만든 사람과 문턱을 고른 사람이 같으면 그건 검증이 아니다.

- 이 상수들이 **다른 모양**의 곡선에서 무너지는가? 직접 곡선을 만들어 보라.
  특히: 여러 번 꺾이는 곡선, 온도 사이클로 계단이 지는 곡선, C-rate 시험처럼
  용량이 뚝 떨어졌다 돌아오는 곡선, 사이클 수가 15\~25 인 짧은 기록.
- `MIN_FIT_GAIN_F` 는 F 분포를 쓰지 않는다 (평활 때문에 잔차가 상관돼 p-value 가
  정직하지 않다는 이유로 "screen" 이라고 적어 뒀다). 이 논증이 맞나? 아니면
  Davies 검정이나 부트스트랩이 실제로 적용 가능한가?
- `MIN_KNEE_DROP_PCT` 를 "기간이 아니라 총량" 으로 정의한 것이 맞나? 500 사이클
  느린 셀과 30 사이클 빠른 셀에 같은 2 % 를 요구하는 것이 옳은가?

### P0 — 세 직선 승격이 편향을 심지 않나

`_three_segment` 는 두 직선이 **감속 이유로** 거부될 때만 호출된다. 그 조건부
호출 자체가 선택 편향이다.

- 승격 조건이 맞나? 두 직선이 *다른* 이유로 거부될 때도 세 직선이 옳은
  경우가 있나?
- 격자 솎기(`THREE_SEGMENT_GRID = 32`)가 절점을 놓치는 경우가 있나? 특히 긴
  기록에서 knee 가 앞쪽에 몰려 있을 때.
- 세 직선 적합에서 **첫** 절점을 knee 로 보는 것이 맞나? 우리 측정에서
  "돌연사" 곡선은 τ1=7(잡음), τ2=55(진짜) 가 나왔다. 두 직선이 그 곡선을
  정상 처리해서 승격이 안 일어났을 뿐이다 — 승격 경로에서 같은 일이 생기면?

### P1 — 굽힘 검정이 기준들의 독립성을 죽이지 않나

`_bend_gain` 을 세 기준에 모두 걸었다. 넷을 다 보여 주는 이유가 "기준마다 강한
곳이 다르다" 인데, 마지막 관문을 공유하면 서로 독립이 아니게 된다.

- 실제로 세 기준이 이제 거의 같은 답만 내는가? 그렇다면 넷을 보여 주는 의미가
  줄어든 것이고, 화면 문구가 사실과 달라진다.
- `_bend_gain` 안에서 "제안된 절점 뒤에 자유 절점 하나를 더 허용" 하는 부분
  (`knee.py` 의 nuisance 절점) — 이것이 검정을 얼마나 무르게 만드나?

### P1 — 놓친 것들

- `slope_ratio` 가 **완만한 knee**(0.05 → 0.16 %/cycle)를 16 사이클 늦게 잡는다.
  이건 우리가 알고 남겨 둔 한계다. 더 나은 방법이 있나?
- 평활 창(중앙값 5점)이 꺾임을 1\~2 사이클 앞으로 당긴다. 보정할 수 있나,
  아니면 보정하려다 더 나빠지나?
- 기준 사이클(3번) 이전을 잘라내는 것이 `slope_ratio` 의 baseline 창과 겹쳐
  이중으로 formation 을 배제하고 있지 않나?

### P2 — 코드로서

- `_hinge_fit` 이 `np.linalg.lstsq` 를 절점마다 부른다. n=1000 에서 ~190 ms.
  더 빠른 형태(QR 갱신, 정규방정식)가 정확도를 해치지 않고 가능한가?
- 반환 `detail` 딕셔너리의 키가 경로마다 다르다 (`segments`, `second_breakpoint`
  는 3선 경로에만). API 스키마가 `dict[str, float]` 라 통과하지만, 화면이
  기대하는 키가 없을 때 조용히 빈칸이 된다.
- `MIN_FADE_RATE = 1e-6` 과 `_acceleration` 의 `inf` 처리가 서로 맞물려 있다.
  경계에서 이상한 일이 생기나?

## 3. 재현 도구

리뷰용으로 쓸 수 있는 것들 (테스트 파일 안에 있다):

```python
from packages.wrdkit.tests.test_knee import _curve, _noisy_linear
# _curve(n, 유지율함수, seed=, noise=)  → formation 2 사이클 + 잡음이 붙은 실측형 곡선
# _noisy_linear(seed)                   → 길이·속도·잡음이 무작위인 직선 열화
```

`test_straight_line_fades_never_get_a_knee` 가 200개 sweep 이다. **seed 범위를
늘려 보라** — 우리는 400까지 봤다. 더 늘리면 오탐이 나오나?

## 4. 돌려줄 형식

기존 리뷰들과 같게:

```markdown
## [P0] 제목
**파일**: packages/wrdkit/src/wrdkit/knee.py:123
**증상**: 무엇이 잘못되는가 (재현 코드 포함)
**근거**: 왜 그렇게 판단했나
**제안**: 어떻게 고칠 것인가
```

특히 **재현 코드**를 붙여 달라. 곡선을 만드는 파이썬 몇 줄이면 우리가 바로
회귀 테스트로 굳힐 수 있다.

한 가지 부탁: "이 상수가 임의적이다" 같은 지적은 우리도 안다 (docstring 에
그렇게 적어 뒀다). **그 상수로 실제로 틀린 답이 나오는 곡선**을 찾아 주는 쪽이
훨씬 값지다.
