---
title: "`reduction_limit_V` 는 환원한계가 아닌 것 같다 — breakpoint 하나 아래를 가리킨다"
date: 2026-08-28
updated: 2026-08-28
tags: [esw, oxidation, grand-potential, cascade, convention, question]
status: 미해결
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

# `reduction_limit_V` 가 가리키는 것이 문헌의 reduction potential 이 맞나

> 발단: `wang2026_interface_stability_kinetics_sulfide_assb` digest (2026-08-28).
> Wang 이 LPSCl 환원한계 **1.78 V**, Zhu 2015 가 **1.71 V** 인데
> 우리 `reduction_limit_V` 는 **1.242 V** 다. 0.5 V 어긋난다.
> 그런데 우리 **다른 필드** `ocv_self_decomposition_V` 가 **1.717 V** 다.

## 1. 우리 코드가 하는 일

`tools/oxidation/esw_grand_potential.py:104-110` —

```python
pos = [s for s in s_byV if s["evolution_Li"] > 1e-6]     # Li 를 흡수 = 환원
neutral = [s for s in s_byV if abs(s["evolution_Li"]) <= 1e-6]
reduction_limit = max(s["V_vs_Li"] for s in pos)          # ← 1.24
v_neutral      = min(s["V_vs_Li"] for s in neutral)       # ← 1.72
```

## 2. 🔑 breakpoint 를 보면 둘 사이가 비어 있다 (comp1)

| V | 반응 | Li 증감 |
|---:|---|---|
| 0.00 | `Li6PS5Cl + 8 Li → Li3P + 5 Li2S + LiCl` | +8 |
| **1.24** | `Li6PS5Cl + 5 Li → 5 Li2S + LiCl + P` | **+5** |
| **1.72** | `Li6PS5Cl → Li3PS4 + Li2S + LiCl` **(neutral)** | **0** |
| 2.14 | `→ … + LiS4 + …` (첫 산화) | −1.75 |

**1.24 와 1.72 사이에 breakpoint 가 없다.** 즉 1.24 에서 시작한 Li-흡수 평형이
**1.72 까지 유지**되고, 거기서 중성 평형으로 넘어간다.

⇒ *"이 아래로는 환원된다"* 는 경계는 **1.72** 다. 1.24 는 **마지막 환원 평형이 시작되는**
전압이지 환원이 끝나는 전압이 아니다. 우리는 경계의 **아래쪽 breakpoint** 를 집고 있다.

## 3. 문헌 두 편이 1.72 쪽에 있다

| 출처 | 환원한계 [V] | 산화한계 [V] |
|---|---:|---:|
| Zhu 2015 | 1.71 | 2.31 |
| Wang 2026 (`fig_S2` figure-read ≈) | 1.78 | 2.30 |
| **우리 `ocv_self_decomposition_V`** | **1.717** | — |
| 우리 `reduction_limit_V` | 1.242 | — |
| 우리 `oxidation_limit_V` | — | 2.14 |

**1.24 근처에 아무도 없다.**

## 4. 무엇이 걸려 있나

- **ESW 폭**: 지금 `2.14 − 1.24 = 0.90 V` 로 낸다. 1.72 를 쓰면 **0.42 V**.
  문헌은 0.52–0.60 V 다 ⇒ 지금 값은 환원 쪽으로 **0.5 V 과대**다.
- **cascade 입력**: `tools/cascade/rebuild_pool_inputs.py:131` 이 `red_V` 로 이 필드를 쓴다.
- **nd_doped**: `red=1.52 · ocv=1.72`. 같은 구조다.

## 5. ⛔ 그런데 단정 못 하는 이유

- **우리 데이터가 스스로 1.52 를 "reduction limit" 이라 부른다.** `nd_doped` breakpoint
  주석에 `(reduction limit)` 이 손으로 적혀 있다 — 누군가 이 규약을 **의도적으로** 골랐다는
  뜻이다. 그 판단의 근거를 못 찾았다.
- `ocv_self_decomposition_V` 는 **이름값도 한다.** 1.72 의 반응이 실제로 Li 교환 없는
  자기분해(`→ Li3PS4 + Li2S + LiCl`)다. 한 전압이 두 역할을 겸하는 것이라
  *"필드가 틀렸다"* 가 아니라 *"필드가 하나 부족하다"* 일 수 있다.
- pymatgen `get_element_profile` 이 각 항목의 `chempot` 을 그 평형의 **시작**으로 주는지
  **끝**으로 주는지 원문 확인을 안 했다. §2 의 읽기는 breakpoint 배열에서 **추론**한 것이다.
- 문헌 두 편의 계산 조건(MP hull 세대·무질서 처리)이 우리와 다르다. 수치 일치가
  **정의 일치를 증명하지 않는다.**

## 6. 닫는 방법 (제안)

1. pymatgen `get_element_profile` 의 chempot 규약을 **원문/소스에서** 확인 — 30분.
2. 확인되면 필드를 **셋으로** 분리: `reduction_onset_V`(경계, 문헌 대응) ·
   `last_reduction_step_V`(현재의 1.24) · `ocv_self_decomposition_V`(현행 유지).
   이름 하나에 두 뜻을 담지 않는다.
3. `rebuild_pool_inputs.py` 의 `red_V` 가 어느 것을 써야 하는지 같이 정한다.
4. `nd_doped` 주석의 `(reduction limit)` 표기를 그 결정에 맞춘다.

⚠ **정본 수치를 건드리는 일이라 사람 확인 없이 바꾸지 않았다.** 지금은 질문으로만 남긴다.

## 7. 연결

- `tools/oxidation/esw_grand_potential.py` — 정의 원본
- `db/properties/oxidation_stability.json` — 위 breakpoint 표
- `litdb/papers/wang2026_interface_stability_kinetics_sulfide_assb.md` §14-B — 발단
- `litdb/papers/zhu2015_*` — 1.71 의 출처
