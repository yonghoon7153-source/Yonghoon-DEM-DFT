# 사전등록 개정 A3 — **판정식을 원 사전등록의 절댓값 정의로 되돌린다** (2026-08-28, vox 0.125 공개 전)

> 대상: `sdcp_bridge_prereg_amendment_A1_20260827.md` §2·§3·§4.
> 계기: **Codex R9 Q1 [P1]** — *"원 사전등록은 grid 효과를 절댓값으로 정의하지만 A1 은
> 부호 있는 평균의 비율을 사용한다."*
> ⚠ **문턱 0.30 / 0.70 은 건드리지 않는다** (원 사전등록 §4 에서 동결).  바꾸는 것은
> **식과 이름**이다.

## 0. blind 상태 — 정확히 적는다

- **봤다**: vox 0.15 두 팔 (off R̄ = 1.123672 · on R̄ = 1.133492, 쌍대응 ΔR = +0.00982)
- **안 봤다**: vox 0.125 **어느 팔도**.  ⇒ 등록량 `A` 는 여전히 미공개.

★ Codex 가 지정한 이 개정의 정확한 지위:
> **Primary endpoint completion 전 prospectively amended, 그러나 `.15` component 를
> 일부 본 뒤의 partially unblinded amendment.**
⇒ *"완전 맹검 confirmatory preregistration"* 이라고 **부르지 않는다.**

## 1. ★ 판정식 — 절댓값 (R9 Q1 [P1])

```
x_i   = R_i(vox 0.125, off) − R_i(vox 0.15, off)
y_i   = R_i(vox 0.125, on)  − R_i(vox 0.15, on)
v     = mean(x_i)          u     = mean(y_i)
D_off = |v|                D_on  = |u|
A     = 1 − |u| / |v|
```

**왜 바꾸나** — A1 의 `A = 1 − u/v` 는 브리지가 격자 효과의 **부호만 뒤집어도** 통과한다:

| | `u = −v` 일 때 |
|---|---|
| A1 `1 − u/v` | **A = 2** → `A − 1.96q ≥ 0.70` → **h1** |
| 원등록 `1 − |u|/|v|` | **A = 0** → `A + 1.96q < 0.30` → **h0** |

부호 반전은 *"격자 의존을 없앴다"* 가 아니라 *"방향을 바꿨다"* 이고, 크기는 그대로다.
⇒ A1 은 **가설을 통과시키는 방향으로** 원 정의에서 벗어나 있었다.

**회귀시험 상주**: `scripts/bridge_grid_verdict.py --selftest` 의 `regr-sign-flip` 이
`u = −v → A = 0 → h0` 를 단언하고, **옛 식이 2.0 을 냈을 것**임도 함께 확인한다
(검사가 실제로 무는지 보이기 위해).  `check_all.sh` · CI 에 배선했다.

## 2. ★ `q` 의 이름 — 표준오차가 아니다 (R8 Q1 · R9 Q1)

`q = SD/√8` 과 `1.96q` 는 **값을 그대로 둔다** (동결된 판정선이므로).  그러나 이름을 고친다:

| 금지 | 정본 표기 |
|---|---|
| 표준오차 · SE · 95 % CI · `±` | **deterministic origin-sensitivity guard** (결정론적 origin 민감도 가드) |

근거: 8 origin 은 이 고정 침대·고정 factorial 에 대해 **완전한 유한 집합**이라 표본추출
기반 추론의 대상이 아니다.  ⚠ 그렇다고 **물리적으로 오차가 없다는 뜻도 아니다** — 이
가드는 origin 위상에 대한 민감도만 잰다.  bootstrap 은 origin 이 무작위 표본이라는 설계가
없으므로 **정당화되지 않는다** (R9 가 명시적으로 기각).

## 3. ★ 분모 gate — 이름을 고친다

```
|v| < 3·q_x  →  INDETERMINATE_OFF_GRID_CONTRAST_ORIGIN_UNSTABLE
```
옛 이름 `INDETERMINATE_NO_GRID_EFFECT` 는 **물리 주장**("격자 효과가 없다")인데 실제로
말할 수 있는 것은 **측정 한계**("off 대비가 origin 산포에 대해 불안정하다")뿐이다.

## 4. 판정표 — 구조 불변, 식만 절댓값

| 조건 | 판정 |
|---|---|
| `A − 1.96·q_A ≥ 0.70` | **h1** (브리지가 격자 의존을 없앤다 = 채널 A 지배) |
| `A + 1.96·q_A < 0.30` | **h0** (채널 B 지배 — 연결 검출로는 못 고친다) |
| 가드 구간이 `(0.30, 0.70)` 안에 온전히 | **BOTH_REJECTED** |
| 가드 구간이 문턱을 걸침 | **INDETERMINATE_PRECISION** |
| `|v| < 3·q_x` (**먼저 본다**) | **INDETERMINATE_OFF_GRID_CONTRAST_ORIGIN_UNSTABLE** |

`q_A` 는 델타법 — `A = 1 − |u|/|v|` 의 편도함수에 부호 함수가 들어간다:
`∂A/∂u = −sign(u)/|v|` · `∂A/∂v = |u|·sign(v)/v²`.

## 5. ★ 보고 의무 (R9 Q1)

판정만 적지 않는다.  **여덟 쌍을 전부 공개**한다:
- `x_i`, `y_i` 8개씩 · 각각의 **범위** · **전부 같은 부호인지**
- `v`, `u`, `|v|`, `|u|`, `q_x`, `q_y`, `q_A`
- **부호 반전 여부** (`u·v < 0`) — 반전이면 판정문에 명시한다

`bridge_grid_verdict.py` 가 이것을 전부 찍는다.

## 6. 상태 표기 (R9 최종)

```
A_PRIMARY        : HOLD
A1               : CONFIRMATORY_CANDIDATE_PENDING_A3_AND_VOX0125
A2               : EXPLORATORY_ROBUSTNESS      (독립 confirmatory replication 아님)
CALIB_VALIDATED  : NO
```

⚠ **A2 의 강등 사유** (R9 Q2): A2 를 추가하기 전에 이미 두 protocol 의 headline
(+12.37 / +30.78 %)과 PTFE-off vox 0.15 의 +0.98 %p, 재사용할 W4 대조를 알고 있었다.
`A_centerline` 자체가 미공개였다는 사실만으로 설계 전체가 다시 맹검이 되지는 않는다.
정확한 표기 = **prospectively specified, partially blinded adaptive robustness analysis**.
둘 중 하나를 골라야 한다면 **exploratory secondary analysis** 다.
★ A2 §5(두 규약이 갈리면 둘 다 보고)는 **유리한 쪽만 고르는 것을 막는다** — 그 값은
유지된다.  다만 confirmatory 지위를 복원하지는 못한다.
⇒ 두 규약이 **같은** 판정을 내도 결론은 *"시험한 두 구현에서 질적 판정이 일치했다"* 까지다.

## 7. 종료조건 — vox 0.125 를 열기 **전에**

1. ✅ 절댓값 식 · 경계 처리 · 분모 gate · `u = −v` 회귀시험을 담은 판정기 커밋
   (`scripts/bridge_grid_verdict.py`, selftest 11/11)
2. ✅ `check_all.sh` + CI 배선 (규칙 K 가 두 목록을 대조하므로 함께)
3. ✅ 이 문서 커밋
4. ⚠ **이미 vox 0.125 를 열었다면** 이 cohort 는 confirmatory 로 복구할 수 없고
   **exploratory** 로 내린다 (R9 명시).  — 2026-08-28 시점 **미개봉**.
