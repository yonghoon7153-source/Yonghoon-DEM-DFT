---
title: "doped E_ads 를 '상태 선언' 으로 살릴 수 있나 — NUPDOWN 은 홀 위치를 안 묶는다"
date: 2026-08-29
updated: 2026-08-29
tags: [sdcp, doped, estimand, spin, nupdown, constrained-dft, open-question]
status: 미해결 — 2026-08-29 all-stop 으로 **보류**, 올리고머 캠페인 재개 시 여기서 이어간다
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# 질문

`sdcp_doped` 흡착에너지는 회신 M/N/O 3연속으로 **단일 스칼라가 정의되지 않음**이 확정됐다.
estimand 카드가 주는 탈출구 셋 중 **①「상태를 선언해 `X(상태)` 로 정의한다」** 를
쓰면 살릴 수 있나?

> ⚠ **이 카드는 대표성 문제(n=1 = 고리당 100 % 산화)를 논외로 두고**, 오직
> *"정의된 조건부 값을 만들 수 있는가"* 만 다룬다. 대표성은
> `kb/syntheses/why_so3h_not_deprotonated_2026_08_29.md` §0-③ 이 별도로 다룬다.

---

## 1. 왜 지금은 정의가 안 되나 (실측)

`E_ads = E_복합체 − E_슬랩 − E_분자` 에서 세 항이 **각각 특정 상태**여야 하고
셋이 **같은 규칙**으로 골라져야 한다.

중성형은 **닫힌 껍질**이라 자유 스핀으로 돌려도 매번 같은 해(m≈0)로 간다 ⇒ 자동 정의.

도핑형은 `NUPDOWN=-1`(자유)로 돌리면 **굴러떨어진 데로** 수렴한다.
`db/properties/sdcp_wave1_job_energies_2026_08_28.csv` 실측:

| 잡 | E [eV] | 총자화 [μB] |
|---|---:|---:|
| `mol__sdcp_doped__box24` | −200.3454 | **1.000** (doublet 선언됨) |
| complex Li-top **pm1** static | −1146.2963 | **−0.306** |
| complex Li-top **pm1** dense | −1146.1967 | −0.213 |
| complex Li-top **net4** static | −1146.1123 | **+3.724** |
| complex Ni-top **net4** static | −1146.1313 | +3.631 |
| `clean_slab` net4 | −944.8464 | +5.999 |

**둘 다 정당하게 수렴한 해다.** 어느 쪽도 틀리지 않았다. 그러나 **서로 다른 상태**이고,
분자 기준(1.000)에서 3.72 짜리 복합체를 빼면 **상태를 가로질러 뺀 것**이 된다.

## 2. 제안했던 해법 — 정책을 선언한다

```
슬랩    AFM 상쇄        →  0
분자    doublet         →  1
복합체  0 + 1           →  1     ← NUPDOWN = 1 로 고정
```

⇒ `E_ads(총자화 1, AFM basin X, doublet)` = **정의된 조건부 값**.
동반 보고: `carrier_retention` = OUTCAR per-ion 모멘트를 분자 원자에 대해 적분한 **연속값**.

## 3. 🔴 구멍 — `NUPDOWN` 은 총자화만 묶는다

**`NUPDOWN` 은 `N_up − N_down = 1` 만 강제한다. 그 전자가 *어디* 있는지는 안 묶는다.**

총자화 1 을 만족하는 배치가 최소 둘:

| | 배치 | 우리 선언과 |
|---|---|---|
| **(a)** | 홀이 **분자 백본 π** 에 | ✅ 선언하려는 것 |
| **(b)** | 홀이 **슬랩 Ni** 에 — 분자는 닫힌 껍질 음이온, 슬랩 AFM 부격자 재배열로 알짜 1 | ⛔ 선언 위반인데 **제약은 통과** |

⇒ **고정해도 선언이 강제되지 않는다.** 공간을 좁힐 뿐이다.

## 4. 🔴 더 껄끄러운 것 — 1 은 이 계가 원하는 상태가 아니다

자유로 두면 **−0.31 또는 +3.72** 로 간다. **1 이 아니다.**

- 분자를 1 로 고정 → 고립 doublet 의 **자연 상태**라 대가 없음
- 복합체를 1 로 고정 → 자유 최소에서 **끌어내는 것**이라 **에너지 대가**를 치른다

그 대가가 `E_ads` 에 그대로 들어간다 ⇒ `E_ads(선언)` 은 자유값보다 **덜 음수**로 나온다.

**틀린 값은 아니다** — *"홀이 분자에 남도록 붙잡았을 때의 흡착에너지"* 라는 물리적으로
의미 있는 양이다(diabatic 에 가깝다). 다만 **"그" 흡착에너지는 아니다.**

⚠ 그리고 자유 최소가 3.7 μB 라는 것 **자체가 정보**다 — 흡착하면서 전하가 슬랩으로
크게 옮겨간다는 뜻일 수 있다. **선언값만 보고하면 그것을 가린다.**

## 5. 실행하려면 (비용과 위험)

| 단계 | 비용 |
|---|---|
| 정책 선언 (문서) | 0 |
| 복합체 `NUPDOWN=1` 재실행 (자세 2 × basin 1) | **226원자 2잡** |
| `carrier_retention` 산출 (OUTCAR per-ion 모멘트) | 0 |
| **결과 보기 전에 정한 문턱**과 대조 | — |
| 통과 → `E_ads(선언 상태)` + retention 병기 | |
| 미달 → **`NO_STATE`, 값 없음** | 🔴 위험 |

계산은 싸다. **위험은 마지막 갈래**다 — 돌려 보기 전엔 통과 여부를 모르고,
전 자세가 미달이면 잡 2개 쓰고 값이 없다.

## 6. 정공법 (해본 적 없음)

홀을 **실제로** 국소화시키려면 constrained DFT 나 점유행렬 제어(`LDAUTYPE=3` 류의
occupation matrix control)가 필요하다. VASP 에서 별개 기법이고 **우리 이력에 없다.**
`NUPDOWN` 은 그 대용품이지 대체품이 아니다.

---

## 착수 전 반드시 정할 것 (사후선택 방지)

1. **`carrier_retention` 문턱을 결과 보기 전에 못박는다.** 미달 자세는 버린다.
2. **분할 방법을 미리 정한다** — per-ion 모멘트 합산은 정성적 분할이다.
   Bader / spin-density difference 와 갈리면 `PARTITION_DEPENDENT`.
3. **자유 최소를 같이 보고한다.** 선언값만 내면 전하이동 신호를 숨기게 된다.
4. **어느 AFM basin 인지 선언**하고 세 계에 동일 적용.

## 판정 이력

- 회신 M (2026-08-28): basin 혼합
- 회신 N: admissible state 다중 — estimand 미정의. *"여덟 실패의 원인은 하나가 아니라 층위"*
- 회신 O: P0 전면 반려 + 슬랩 NO-GO. **"같은 NUPDOWN 값이 아니라 같은 state-selection policy"**
- 회신 T (2026-08-29): 이 절을 **떼어 보류** — `kb/reviews/_T_doped_section_parked.txt`
- 팀 결정 (2026-08-29): **all-stop**, 중성 SO₃H 집중

## 재개 조건

`sdcp_doped_closed_2026_08_28.json` 의 `planned_upgrade_triggers` 그대로 —
회신 O 7조건 전부, **부분 재개 없음**. 이 카드는 그중 ②(주 estimand 설계)의 초안이다.
그리고 §3 의 구멍이 **먼저 닫혀야** ② 가 성립한다.
