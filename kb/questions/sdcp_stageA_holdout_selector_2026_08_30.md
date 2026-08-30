---
title: "estimand 카드 — Stage A 홀드아웃: UMA 선택기가 DFT 순위를 맞히나"
date: 2026-08-30
updated: 2026-08-30
tags: [estimand, sdcp, stage-a, holdout, uma, selector, prereg]
status: open
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: single-source
feedsInto: db/properties/sdcp_stageA_closure_conditions_2026_08_29.json
---

# estimand 카드 — Stage A 홀드아웃 (**결과 0잡, 던지기 전**)

> 왜 이 카드가 있나: **새 물리량을 재기 전에는 카드를 채운다** (CLAUDE.md 2026-08-28).
> D3-off 16잡을 버려서 예산이 났고, 그 예산으로 **새 질문**을 하려는 것이므로
> 예산 전용은 자동 승인이 아니다.

## 왜 중요한가

primary estimand `ΔΔE_lowE = min_p A(SDCP,p) − min_q A(c10,q)` 의 `min` 은
**UMA 가 고른 4자세 안의 최저**다. 그 4개 안에 DFT 최저가 없으면 primary 는
원하는 양이 아니라 **선택기의 산물**이 된다. Stage B(전수 자세)는 금지돼 있으므로
이 가정을 시험하는 경로는 **홀드아웃 하나뿐**이다.

## 1. 무엇을 원하는가 (한 문장)

**UMA-s-1p1 이 매긴 자세 순위가 DFT 순위를 맞히는가** — 즉 UMA 상위 4자세만 DFT 로
채점하는 현행 규약이 "그 4개 안에 DFT 최저가 있다" 를 실제로 보장하는가.

⚠ 이것은 primary estimand(ΔΔE_lowE)가 **아니다.** primary 를 대체하지도, 평균되지도
않는다. 이것은 primary 가 기대는 **가정 하나**를 시험하는 별도 질문이다.

## 2. 그것을 재는 양 (식으로)

```
A(f,p)   = E_complex(f,p) − E_mol(f)          [기존 정의 그대로]
S(f,p)   = UMA E_bind(f,p)                     [선택기가 매긴 점수]

H1 (이항)  : min_{p ∈ holdout} A(f,p)  <  min_{q ∈ calibration} A(f,q)  ?
H2 (연속)  : ρ_f = Spearman[ rank_p S(f,p) , rank_p A(f,p) ]
             p ∈ calibration ∪ holdout  (조각당 4 + 8 = 12자세)
```

- `E_mol(f)` 는 조각 안에서 **정확히 소거**되므로 A 로 순위를 매기는 것은
  E_complex 로 매기는 것과 같다 ⇒ 기준계 문제에 안 걸린다.
- ⚠ **조각 간 비교가 아니다.** ρ 는 조각별로 따로 낸다. 두 조각의 ρ 를 평균하지 않는다.

## 3. 🔴 이 계에서 잘 정의되는가

| 물음 | 답 | 근거 |
|---|---|---|
| SCF 해가 하나인가 | **아니다 — 여럿이다** | AFM 슬랩. pm1 / net4 두 branch, net4 는 realized basin A(≈4 μB)/B(≈6 μB) |
| 열린 껍질이 있는가 | 분자 쪽은 **없다** (중성 닫힌껍질 두 조각) · 슬랩은 있다 | `sdcp_neutral` C₁₁H₁₆O₆S₂ · `ptfe_c10` C₁₀F₂₂ 둘 다 짝수 전자 |
| 기판이 자성인가 | **그렇다** | 위와 같음 |
| 기판이 산화환원 활성인가 | **그렇다** (LiNiO₂) | wave1 에서 복합체 자화가 −0.31 / 3.72 μB 로 흩어진 전례 |
| 참조와 대상이 같은 전자 상태인가 | **A 는 슬랩이 안 들어가서 이 문제를 피한다** | A = E_complex − E_mol. 조각 안 순위라 슬랩 basin 이 **공통모드**로 빠진다 — **단 12자세가 전부 같은 basin 일 때만** |
| 보존 가정 | 자세가 달라도 **같은 슬랩·같은 basin**, 분자 무결(결합 절단·양성자 이동 없음) | §4 게이트 |

**선택·집계 규칙 (선언)**
- branch 는 **pm1 하나로 고정**한다. 홀드아웃 잡은 pm1 D3-on 만 돈다.
- 12자세 중 **realized basin 이 다른 자세는 ρ 에서 제외**하고, 제외 수를 함께 보고한다.
  제외가 3자세를 넘으면 그 조각의 ρ 는 **unresolved**.
- H1 은 basin 이 맞는 자세들 안에서만 판정한다.

⇒ 판정 규칙(회신 N)에 걸리지 않는다: admissible state 가 여럿이지만 **선택 규칙
(pm1 고정 + basin 일치 자세만)** 을 여기서 미리 적었다.

## 3-1. 홀드아웃 자세를 **어떻게 고르나** (결과 보기 전 동결)

조각당 8자세. **2축 층화**:

| 축 | 층 | 왜 |
|---|---|---|
| UMA 사분위 | Q1·Q2·Q3·Q4 (UMA E_bind 오름차순 후보풀을 4등분) | 상위만 보면 "상위 안에 최저가 있다" 를 시험할 수 없다 |
| 접촉 motif | 조각별 2종 (아래) | 순위 실패가 에너지축이 아니라 **기하 유형**에서 날 수 있다 |

**접촉 motif 정의** (조각마다 다르다 — 같은 이름을 쓰면 안 된다):

- `sdcp_neutral`: **`sulfonate`** = 최근접 분자-표면 원자쌍이 SO₃ 의 O 또는 산성 H
  · **`backbone`** = 그 외 (티오펜 고리 · 에틸렌다이옥시 · C–H)
- `ptfe_c10`: **`terminus`** = 최근접 원자가 사슬 말단 3원자 이내의 F
  · **`midchain`** = 그 외

⇒ 4사분위 × 2 motif = **8칸, 칸당 1자세.** 칸이 비면 **같은 사분위의 다른 motif** 에서
채우고 그 사실을 manifest 에 적는다. 두 칸 이상 비면 그 조각 홀드아웃은
**층화 실패**로 기록하고 ρ 만 쓴다 (H1 은 유지).

⛔ **동결이 먼저다.** 후보 선정은 결과가 하나도 없는 상태에서 돌리고,
`freeze_sha256` 를 manifest 에 박은 뒤에만 잡을 만든다.

## 4. 검증 게이트 — 결과 보기 전에

| 게이트 | 기대 | 위반 시 |
|---|---|---|
| POSCAR 원자수·조성 | calibration 자세와 동일 | 그 잡 폐기 |
| INCAR | calibration pm1 잡과 **IVDW·LREAL·NUPDOWN 포함 전건 동일** | 그 잡 폐기 |
| realized basin | pm1 | ρ 에서 제외 (§3) |
| 분자 무결성 | 결합 절단 · 양성자 이동 · 탈착 없음 | 그 잡 폐기 + prereg 재개조건 발동 |
| `Edisp (eV)` 존재 | 1회 | C3 unresolved (이 카드 범위 밖) |

## 4-1. 판정 문턱 — **지금 박는다**

| | 문턱 | 뜻 |
|---|---|---|
| **H1** | 홀드아웃 최저 < calibration 최저 **− 30 meV** | 선택기 **실패**. prereg 재개조건 발동 (이미 등록돼 있다) |
| | 차가 ±30 meV 안 | **미해결** — "맞혔다" 라고 쓰지 않는다 |
| | 홀드아웃 최저 > calibration 최저 + 30 meV | 그 조각에서 선택기가 **버텼다** |
| **H2** | ρ_f ≥ 0.70 | 순위가 대체로 보존됨 |
| | 0.30 ≤ ρ_f < 0.70 | **미해결** |
| | ρ_f < 0.30 | 선택기의 순위가 DFT 순위와 **무관** |

⚠ 30 meV 는 사전등록 규약(`kb/questions/sdcp_site_preference.md`)의 판정바닥을
그대로 쓴 것이다 — 새로 정한 수가 아니다.
⚠ n=12 에서 ρ=0.70 은 p≈0.01 수준이지만 **가설검정으로 쓰지 않는다** (값 서술).

## 5. 무엇을 주장할 것인가 / 무엇은 주장하지 않는가

**나오면 말할 수 있는 것**
- *"이 조각의 12 표본 자세에서 UMA 순위와 DFT 순위의 Spearman ρ 가 X 였다"*
- *"층화 홀드아웃 8자세 중 어느 것도 calibration 최저를 30 meV 이상 밑돌지 않았다"*

**나와도 말하지 않을 것**
- ⛔ *"UMA 가 전역 최소를 찾는다"* — 후보풀 밖은 안 봤다
- ⛔ *"선택기가 검증됐다"* — 두 조각·한 표면·한 branch 다
- ⛔ ρ 를 두 조각에 걸쳐 평균하거나 pooled ρ 를 내는 것
- ⛔ 홀드아웃 값을 primary estimand(ΔΔE_lowE)의 min 후보에 **넣는 것**
  — primary 는 사전등록된 calibration 집합으로만 계산한다. 홀드아웃이 더 낮으면
  그것은 **primary 를 고치는 사유가 아니라 재개 사유**다

**한 표에 놓으면 안 되는 것**
- legacy(wave1) 값. clean slab 이 다르다 (`daf71160` vs `d5f18feb`)
- `motif_probe` 번들의 값

## 6. 규약 대조 (30초)

```bash
grep -rl "holdout\|selector\|Spearman" kb/ | head
grep -rl "판정바닥\|30 meV" kb/questions/ | head
```

기존 판정: `kb/questions/sdcp_site_preference.md` 의 판정바닥 max(30 meV, 쌍 편차) ·
n<3 NO_VERDICT — **그것이 이긴다.** 위 30 meV 는 그것을 승계한 것이다.

## Evidence For

- 후보풀 생성이 이미 동결 manifest(`from_basins`)로 강제돼 있어, 홀드아웃을
  **결과 없이** 뽑는 절차가 코드에 존재한다 (새로 만들 것이 없다).
- prereg 가 이미 재개조건으로 *"holdout/cutoff 후보가 DFT 최저가 되어 MLIP rank
  가정이 실패"* 를 등록해 두었다 — H1 은 **새 판정이 아니라 등록된 판정의 측정**이다.
- `A(f,p) = E_complex − E_mol` 은 조각 안에서 `E_mol` 이 정확히 소거되므로,
  wave1 을 물린 reference-equivalence 결함(NUPDOWN·LREAL 비대칭)에 **원리적으로 안 걸린다**.
- 예산이 실제로 났다: D3-off 16잡이 `Edisp` 로 대체 가능함을 실물 OUTCAR 로 확인했다
  (phaseB `IVDW=11` 세 잡에 `Edisp (eV)` 존재, δ = −0.37323 eV 산출).

## Evidence Against

- **n=12, 반복 없음.** ρ 에 불확도를 못 준다. ρ=0.55 같은 값이 나오면 아무 말도 못 한다.
- 후보풀 자체가 UMA 이완 기하 위의 UMA 점수다 — "UMA 순위" 가 어느 기하에서의
  순위인지 한 겹 더 있고 이 카드는 그것을 안 푼다.
- 층화 칸(4사분위 × 2 motif)이 **빌 수 있다.** 특히 `ptfe_c10` 은 대칭이 높아
  Q4 × terminus 같은 칸에 후보가 없을 수 있다.
- 홀드아웃이 이기면(H1 실패) primary 를 **못 고친다** — 재개 사유일 뿐이라,
  이 16잡은 "원고 숫자" 를 하나도 안 만든다. 예산의 40 % 다.
- ⚠ 반론 유지: *"차라리 그 16잡으로 자세를 늘려 min 을 더 낮추는 게 원고에 낫다"* —
  이 반론은 **틀리지 않았다**. 다만 그렇게 하면 min 이 표본크기에 따라 움직이는
  양이 되고(champion pool size bias, `kb/results/champion_pool_size_bias_2026_08_18.md`),
  사전등록된 집합이 사라진다. 그 대가로 선택기 가정은 여전히 미검증으로 남는다.

## 결정 실험

조각당 8자세(4사분위 × 2 motif), **pm1 D3-on 단일점 1잡씩**, 총 16잡.
결과 보기 전 `freeze_sha256` 동결. 판정은 §4-1 의 H1·H2 문턱 그대로.

- **H1 실패**(홀드아웃 최저가 calibration 최저를 30 meV 이상 밑돎) ⇒ prereg 재개조건 발동,
  primary 는 **그대로 두고** 재개 절차로 간다.
- **H1 통과 + H2 ρ ≥ 0.70** ⇒ 이 두 조각·이 표면·이 branch 에서 선택기가 버텼다고 적는다.
- 그 사이 ⇒ **미해결**로 적고 원고에는 안 쓴다.

## Status Log

| 날짜 | 무엇 |
|---|---|
| 2026-08-30 | 카드 작성. **DFT 결과 0잡.** 회신 AB 의 Q6 예산 재설계에서 1저자가 옵션 A 채택 |

## 열린 채로 두는 것

- 후보풀이 **UMA 이완 위 단일점**이라 "UMA 순위" 자체가 어떤 기하에서의 순위인지
  한 겹 더 있다. 이 카드는 그것을 안 푼다.
- 조각당 8자세로 ρ 의 불확도를 못 준다 (n=12, 반복 없음).
