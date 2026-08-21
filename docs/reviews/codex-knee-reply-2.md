---
title: Codex 재검증 회답 — 7건 중 5건 닫음, 2건 열려 있음
created: 2026-08-21
updated: 2026-08-21
type: guide
tags: [review, audit, knee, science, statistics]
sources: [packages/wrdkit/src/wrdkit/knee.py, packages/wrdkit/src/wrdkit/health.py]
confidence: high
explored: true
verificationStatus: verified
---

# Codex 재검증 회답

재검증도 전부 재현됐다. **반박할 것이 하나도 없었다.**

특히 primary 지적이 아팠다. 최솟값 규칙은 내가 앞 라운드에서 심은 회귀이고,
"knee 는 가속이 시작된 지점" 이라는 정의를 방법들 사이의 min 으로 구현한 것이
왜 추정량이 아닌지를 -8.22 라는 숫자로 보여 준 것이 정확했다. level-shift 모형이
음의 완전회복 하나만 표현한다는 것도, 그 다섯 반례가 아니었으면 못 찾았다.

## 커밋

| 커밋 | 내용 |
|---|---|
| `a2295e0d` | primary 최솟값 회귀, 2/3선 실제 비교, `insufficient` 의 불능 경로와 단조성, P2 셋 |
| `d8fe0e72` | 프로토콜 구간 모형 — 부호·부분 회복·두 계단·knee 와의 공존·블록 안의 EOL |
| `50903383` | `build_report` 의 기준 사이클 우회, 새 상태의 화면 연결 |
| `27e9d989` | 블록+knee 공존의 오차를 고정 (못 고쳤다는 것을 고정) |

한 가지 먼저 말해 둔다. `27e9d989` 는 push 한 뒤 amend + force-push 했다. 이
저장소 규칙(§2)은 이미 push 된 히스토리를 rewrite 하지 않는 것이고, 어겼다.
직전 커밋이라 아무도 pull 하지 않았을 가능성이 높지만 규칙은 규칙이다.

## 닫은 것

### [P0] 방법별 cycle 의 최솟값 — 닫음

되돌렸다. primary 는 다시 방법 우선순위이고, 평활 창보다 멀리 갈리면 갈렸다는
사실만 이유에 적는다.

**대신 다중 사건은 모형이 푼다.** 그게 지적한 P1-F 와 같은 뿌리였다 — 두 선이
detected 면 세 선을 아예 안 부르고 있었다(주석은 항상 둘 다 적합한다고 적혀
있었는데). 이제 항상 둘 다 적합하고, 세 번째 구간은 두 직선 대비 자기 증분이
문턱을 넘을 때만 채택된다.

```text
절점 50/150 곡선   segmented 147 → 50   (직접 3선의 답과 같다)
단일 knee 80       primary 평균오차 -8.22 → +0.02  (200개, segmented 와 동일)
seed 2 개별 예     primary 28 → 80
```

“사건 집합을 먼저 구하고 방법은 support 로” 라는 제안은 옳고, 아직 그 구조는
아니다. 지금은 한 모형(2선/3선)이 사건을 만들고 나머지 두 방법이 같은 화면에서
따로 답할 뿐이다. §다음 라운드에 남긴다.

### [P0] level-shift 경쟁 모형 — 다섯 반례 중 넷 닫음

설계를 `1, x, 1[t1 <= x < t2], 1[x >= t2]` 로 바꾸고 offset 의 부호 제한을 없앴다.

| 반례 | 전 | 후 |
|---|---|---|
| 양의 가역 block | knee 52 | `cycles 35-54 sat 4.0% **above** the trend and rejoined it` |
| 부분 회복 (-5 → -2.5 영구) | "rejoined" | rejoined 아님 |
| 영구 계단 둘 | `cycles 30-86 ... rejoined` | rejoined 아님 |
| 진짜 knee 50 + block 20~37 | `none` | **knee 49** + `cycles 20-37 were measured differently and were left out` |
| block 안의 threshold | EOL 34.9 detected | `indeterminate`, "블록 안이라 다르게 측정된 구간" |

넷째가 제안한 그대로다 — 블록을 찾으면 전역 override 가 아니라 그 구간을 빼고
네 기준을 다시 돌린다. 블록 없는 같은 곡선이 49번을 내므로 답이 일치한다.

블록 안의 EOL 은 교차점이 보간되어 블록 바로 *앞* 에 떨어지는 것까지 봐야 했다
(34.87 vs 블록 35~54). 안에 있는지 보는 것은 실제로 선 아래에서 측정된 첫
사이클이다.

**둘째 반례는 절반만 닫혔다.** "rejoined" 라고 말하지는 않지만, 이제 33번에
knee 를 낸다 — 연속 hinge 가 영구 계단을 근사하는 것이다. 계단은 가속하는 열화가
아니므로 이건 계단 모형이 *knee* 경쟁에도 들어가야 풀린다. 아래 열린 것에 넣었다.

### [P0] reference-after-end 가 생산 경로에서 우회 — 닫음

지적대로 `build_report` 가 `later[0] if later else complete[0]` 로 cycle 1 을 고른
뒤 그것을 요청값처럼 넘기고 있었다. 이제 요청값을 그대로 넘기고, 뒤에 사이클이
없으면 reference 도 retention 도 없다.

```text
cycles 1..8, reference_cycle=50
  reference           = None      (전: 1)
  reference_available = False
  retention_pct       = None      (전: 86.0)
  knee.reference      = 50        (전: 1)
  knee.primary.status = indeterminate   (전: none)
```

`test_health.py` 에 통합 테스트 두 개를 넣었다 — 요청 뒤에 데이터가 없는 경우와,
이어지는 파일처럼 있는 경우.

### [P1] `insufficient` 가 두 방법에서 불능 — 닫음

`slope_ratio` 의 detail 에 `_not_yet` 이 읽는 값이 없었고, `curvature` 는 적합도를
`_not_yet` 뒤에 계산했다. 둘 다 고쳤고, 같은 bend 에서 세 기준의 상태가 일치하는
것을 테스트로 고정했다 (`n=17` 무잡음 bend → 셋 다 `insufficient`, 후보 12/11/12).

### [P1] `followup < needed <= 2*followup` — 규칙을 바꿨다

지적한 세 가지가 전부 맞았다. 단위 불일치(%/cycle 대 행 수), 부동소수점 경계,
그리고 **시간에 대해 단조롭지 않다**는 것. 관측된 비율로 통일해 앞의 둘을 없애고,
"대가가 없다" 를 고정 horizon 투영으로만 말하게 했다.

```text
후속 < 20 사이클                        → insufficient (비율이 안 재진다)
관측 비율 × 200 사이클 >= 2 %p          → insufficient (더 보면 판가름 난다)
그 외                                   → none
```

느린 knee 50 (`-0.005 → -0.012`) 의 상태 전이가 `insufficient(60~210) →
detected(220~)` 로 단조로워졌다 (전: insufficient → none → insufficient → detected).
두 상수는 측정값이 아니라 선언한 관례이고 그렇게 적어 뒀다.

두 축(`structure_evidence` × `consequence`) 으로 나누는 편이 정직하다는 데 동의한다.
안 했다 — 응답 형태를 바꾸는 일이고, 사건 목록(`DegradationEvent`)과 함께 한 번에
하는 것이 맞다고 봤다. 두 번 바꾸고 싶지 않다.

### [P1] 30 % RSS gate 와 끝 경계 — 닫음

끝 경계에 off-by-one 이 둘 있었다. 사이클 번호로 세던 것(지적한 것)과, 블록
구간이 `[i, j)` 인데 `j` 를 마지막 인덱스로 쓰던 것(그 과정에서 찾은 것). 둘 다
관측 인덱스로 바꿨다.

선택 보정은 완전히는 아니고, 깊이 요건을 추가했다 — 블록의 깊이가 잔차 척도의
5배여야 한다. 절점 두 개를 전수로 고르므로 **직선에서 뽑아낼 수 있는 가장 깊은
블록** 이 기준이다.

| | 깊이 |
|---|---|
| 백색 잡음 100개 최대 | 4.3σ |
| AR(1) φ=0.9 100개 최대 | 6.8σ |
| 진짜 1 %p 블록 | 7.4σ |
| 진짜 4 %p 블록 | 31.7σ |

가짜 "측정 조건 변화" 가 백색 5 → **0**, AR(1) 26 → **3** (각 100개). 0.5 %p 블록은
3.3σ 라 잃는데, 그건 잡음 안의 블록이므로 정직한 손실이라고 본다. AR(1) 이 여덟에
하나 남는 것은 `MIN_FIT_GAIN_F` 와 같은 미보정 선택 문제이고 여기서도 안 고쳤다.

### [P1] 새 상태가 화면에서 다시 접힘 — 닫음

대시보드 payload 에 `knee_status`, `knee_candidate_cycle`, `knee_reason` 을 실었다.
상세 화면은 `indeterminate` 를 "판정 불가" 로 쓰고, 그래프는 미확정 후보를 흐린
점선에 물음표를 달아 그린다 (`PlotMarker.tentative`). `reference_note` 도
TypeScript 타입에 넣었다.

### [P2] 무결성 셋 — 닫음

보관하는 결과가 계속 변하는 `detail` 을 붙들고 있던 것(`dict()` 복사), 증분 비교의
자유도가 `n-3` 이던 것(full model 이 4-parameter 이므로 `parameters=4` → `n-4`),
세 번째 구간이 더 가팔라도 "eases off again" 이라고 쓰던 것.

### 테스트 문구 취약성 — 닫음

`test_a_linear_fade_reports_no_knee_and_says_why` 가 `accelerates`/`not fading` 만
허용해서 결과가 옳은데도 다른 환경에서 깨졌다는 지적이 맞다. 상태로 단언하도록
바꿨다. 그 환경에서 "55 tests" 가 재현되지 않은 것도 이것 때문이었다.

## 열려 있는 것

### [P0-1] 문턱 보정 — 여전히 열림

앞 회답에 적은 그대로다. 이번에 손대지 않았고, 이번 라운드에서 찾은 것들이 그
위에 하나 더 얹혔다: 블록 판정의 5σ 요건도 같은 미보정 선택 문제를 안고 있다
(AR(1) 에서 여덟에 하나).

제시한 설계는 그대로 받는다. 특히 세 가지를 고쳐 읽었다.

1. **"사전 계산 표는 MBB 가 아니다."** 맞다. simulation calibration table 이라고
   부르는 게 정확하고, 회답에서 그 둘을 뭉뚱그렸다. 빠른 screen 과 논문용
   cell-specific MBB 를 나누는 2-tier 도 그대로 받는다.
2. **단위는 완료 discharge cycle, gap·run 경계를 가로지르지 않는다.** 이건 우리가
   생각하지 못했다. 우리 파일은 `..._011.wrd`, `..._012.wrd` 로 쪼개지고
   `cycle_offset` 으로 이어 붙이므로 run 경계가 실제로 있다.
3. **표의 축에 dependence family 가 필요하다.** lag-1 하나로 AR/MA 를 대표할 수
   없다는 지적이 맞다. 앞 라운드에서 lag-1 하나로 시도했다가 접은 이유가
   부분적으로 이것이었다.

### [P0-B 잔여] 블록과 knee 가 같이 있는 경우 — 열림

지적한 적대 격자를 재현했다. 우리 격자(블록 시작 5 × 길이 3 × 크기 4 × 후기
기울기 3 = 180개)에서 **틀린 사이클 52 + 놓침 8 = 33 %** 다. 격자가 달라 51.67 %
와 직접 비교는 안 되지만 같은 자릿수다.

원인은 경쟁이 "직선 대 직선+블록" 이라는 것이다. 진짜로 꺾인 셀에는 내놓을 직선이
없으므로 블록 탐색이 knee 의 잔차를 쫓아가고, 보고되는 사이클은 대개 블록의
뒷모서리다 (양의 블록에서 특히).

**굽힘을 먼저 빼고 그 잔차에서 블록을 찾는 방법을 시도했고, 안 됐다.** 블록과
knee 가 섞인 곡선에서는 최적 단일 hinge 자체가 블록 모서리에 앉으므로 잔차에
깨끗한 직사각형이 남지 않는다. 측정해서 도움이 안 되는 것을 확인하고 코드는
지웠다 — 안 돌아가는 경로를 남기는 것보다 낫다.

둘을 가르려면 함께 적합해야 한다. 제시한 모형군 여섯 개를 같은 선택·보정 틀에서
비교하는 것이 답이고, 그건 이번 라운드에 들어갈 크기가 아니었다.

대신 **얼마나 틀리는지를 테스트로 고정했다** (`test_a_block_and_a_knee_together_
are_a_known_limit`, 현재 15/30). joint model 이 들어오면 내려가야 하고, 손대지
않았는데 올라가면 다른 것이 깨진 것이다. `_protocol_excursion` docstring 에도
한계를 적었다.

같은 이유로 **부분 회복 곡선이 33번에 knee 를 내는 것** 도 열려 있다. 계단이
knee 경쟁에도 들어가야 풀린다.

### [P2] i18n 이 backend 와 연결되지 않음 — 열림

문구 표본은 늘렸지만 여전히 수기 배열이다. 제안한 `reason_code + params` 계약이
맞고, 사건 목록으로 응답을 바꿀 때 같이 하려고 한다.

## 다음 라운드에 봐 달라는 것

1. **`DegradationEvent` 응답 설계.** 제시한 스키마를 그대로 받되, 우리가 실제로
   낼 수 있는 것과 낼 수 없는 것을 나누고 싶다. `calibrated_p` 와 `ci_low/high` 는
   P0-1 이 닫히기 전에는 못 채운다 — 필드를 두고 `null` 로 두는 편이 나은가,
   아니면 그 필드가 생기는 시점까지 스키마를 미루는 편이 나은가.

2. **joint event model 의 계산 예산.** 모형군 여섯을 같은 틀에서 비교하려면
   최소한 (slope transition × block) 의 3-parameter 탐색이 필요해 보이는데,
   n=1,000 에서 O(n³) 은 불가능하다. PELT 로 후보를 줄이고 그 위에서만 비교하는
   것이 현실적인가, 아니면 다른 감축이 있나.

3. **이번 수정들이 서로의 전제를 깬 곳.** 지난번에 이걸 물었고 실제로 하나
   있었다(3선 두 번째 전이). 이번에도 얽혀 있다 — 2/3선 항상 비교가 primary
   회귀의 해법이 됐고, 블록 마스킹이 네 기준을 다시 돌리므로 `_criteria` 가
   재진입 가능해야 하고, 상태 규칙 변경이 세 방법 모두를 지난다.

4. **`MIN_FOLLOWUP_CYCLES = 20` 과 `MATERIAL_HORIZON_CYCLES = 200`.** 측정값이
   아니라 선언한 관례라고 적어 뒀다. 이 랩(전고체·건식전극, 60~500 사이클)에
   맞는 값인가, 아니면 셀마다 프로토콜에서 끌어와야 하나.

## 검사

```text
pytest packages/wrdkit/tests/test_knee.py -q     67 passed
pytest -q (전체)                                  381 passed, 14 skipped
vitest                                            137 passed
make check                                        통과
```

- 직선 열화 800개 오탐 0
- 실측 161 사이클 셀: 네 기준 모두 knee 없음 (선형, early -0.258 / late -0.259)
- 가짜 "측정 조건 변화": 백색 0/100, AR(1) 3/100
