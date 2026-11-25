---
title: "`reduction_limit_V` 는 환원한계가 아닌 것 같다 — breakpoint 하나 아래를 가리킨다"
date: 2026-08-28
updated: 2026-09-13
tags: [esw, oxidation, grand-potential, cascade, convention, question]
status: open
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

## Evidence For — breakpoint 를 보면 둘 사이가 비어 있다 (comp1)

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

## 왜 중요한가 — 무엇이 걸려 있나

- **ESW 폭**: 지금 `2.14 − 1.24 = 0.90 V` 로 낸다. 1.72 를 쓰면 **0.42 V**.
  문헌은 0.52–0.60 V 다 ⇒ 지금 값은 환원 쪽으로 **0.5 V 과대**다.
- **cascade 입력**: `tools/cascade/rebuild_pool_inputs.py:131` 이 `red_V` 로 이 필드를 쓴다.
- **nd_doped**: `red=1.52 · ocv=1.72`. 같은 구조다.

## 4.5 🔑 pymatgen 소스 확인 — §2 추론이 맞다 (2026-08-28, gabia 실측)

`PhaseDiagram.get_element_profile` 본문의 결정적인 한 줄:

```python
for cc in self.get_critical_compositions(el_comp, gc_comp)[1:]:
    ...
    c = self.get_composition_chempots(cc + el_comp * 1e-5)[element]   # ← 여기
```

`cc` 는 **임계조성(두 facet 사이 경계)** 이다. 거기에 열린원소(Li)를 `1e-5` 만큼 **더해서**
chempot 을 잰다. Li 를 더하면 μ_Li 가 **올라가고**, `V = μ_ref − μ` 이므로 전압은 **내려간다.**

⇒ 보고되는 `chempot` 은 그 경계의 **Li-rich(저전압) 쪽 facet** 값이다.
**모든 항목이 자기 경계의 아래쪽을 가리킨다.**

그래서 우리가 `max(V where evolution>0)` 로 집은 1.24 는 *"환원이 끝나는 전압"* 이 아니라
**그 아래 facet 의 전압**이다. 실제 환원 개시는 중성 facet 의 아래 끝 = **1.72**.

**독립 검증 — 산화 쪽에서 같은 편향이 보인다:**

| | 우리 | 문헌 | 우리 다음 breakpoint |
|---|---:|---:|---:|
| 환원한계 | 1.24 | 1.71 (Zhu) · 1.78 (Wang) · **1.7 (Nolan p.2031)** | **1.72** ✓ |
| 산화한계 | 2.14 | 2.31 (Zhu) · 2.30 (Wang) · **2.4 (Nolan p.2031)** | **2.36** |

둘 다 문헌값이 **우리 값과 다음 breakpoint 사이**에 있다. 한쪽만이면 우연일 수 있는데
**양쪽이 같은 방향**이라 규약 차이로 읽는 게 자연스럽다.

**★ 2026-09-13 추가 — 세 번째 문헌 점, 그리고 산화 쪽이 나아졌다.**
계보 #7 digest(`nolan2018_computation_accelerated_design_review.md`)가 p. 2031 에서
**`Li₆PS₅Cl` 를 이름으로 들어** *"undergoing reduction at 1.7 V and oxidation at 2.4 V"* 라고 적는다
(원출처 ref 63 [Zhu15] · ref 71 [Rich16] — **2차 인용이라 우리 db 이식은 금지**, 방향 판단용).
**2.4 는 우리 2.36 쪽에 붙는다** — Wang 의 2.30 이 2.14 와 2.36 의 중간이라 애매했던 자리를 메운다.

⚠ 그래도 산화 쪽을 **닫지 않는다**: 우리 canonical 산화 onset 은 이 파일의 2.14 가 아니라
**2.256 V** 다(다른 파일, phase-set 해시 고정 + `LiS₄`·`SCl₃`·`Li₅PS₄Cl₂` 제외). 규약이 한 겹 더 있다.
**이 카드는 환원만 닫는다.**

## Evidence Against — ⛔ 그런데 단정 못 하는 이유

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

## 결정 실험 — 닫는 방법 (제안)

1. pymatgen `get_element_profile` 의 chempot 규약을 **원문/소스에서** 확인 — 30분.
2. 확인되면 필드를 **셋으로** 분리: `reduction_onset_V`(경계, 문헌 대응) ·
   `last_reduction_step_V`(현재의 1.24) · `ocv_self_decomposition_V`(현행 유지).
   이름 하나에 두 뜻을 담지 않는다.
3. `rebuild_pool_inputs.py` 의 `red_V` 가 어느 것을 써야 하는지 같이 정한다.
4. `nd_doped` 주석의 `(reduction limit)` 표기를 그 결정에 맞춘다.

⚠ **정본 수치를 건드리는 일이라 사람 확인 없이 바꾸지 않았다.** 지금은 질문으로만 남긴다.

## Status Log

- **2026-08-28** — 카드 작성 (wang2026 digest 가 발단). 같은 날 gabia 에서 pymatgen 소스를
  확인해 §2 추론이 맞음을 확인(§4.5) — 규약은 각 경계의 **아래쪽**을 취한다.
  ⛔ **사람 승인 대기**: 필드 이름/분할을 바꾸는 것은 cascade 하류 전체에 걸리므로
  1저자 판단 없이 손대지 않는다.
- **2026-09-13** — 계보 digest 충돌을 가르다가 이 카드로 되돌아왔다
  (`kb/questions/coating_lineage_sibling_conflicts_2026_09_13.md` 충돌 1).
  · 세 번째 문헌 점 확보 — Nolan 2018 p. 2031 이 **`Li₆PS₅Cl` 를 이름으로** 1.7 / 2.4 V.
    **양쪽 다 "한 칸 위" 를 지지**한다(§4.5 표 갱신).
  · `citation_hazards.json` 에 **`HZ-esw-reduction-limit-facet-convention`**(CONDITIONAL) 신설 —
    지금까지 이 카드의 경고가 **원장에 없어서** 인용 전 30초 절차에 안 걸렸다.
  · ⛔ **결속 실패를 확인했다** — 이 세 필드는 `canonical_registry.json` 에 **없다**(43항목 어디에도).
    그래서 hazard 에 `claim` 을 못 걸고 `prohibition_axis` 도 죽은 선언이 된다.
    **레지스트리 등록이 새 선결조건**이다.
  · 여전히 **정본 수치·필드명은 안 건드렸다** — 위 승인 대기는 그대로다.

## 연결

- `tools/oxidation/esw_grand_potential.py` — 정의 원본
- `db/properties/oxidation_stability.json` — 위 breakpoint 표
- `litdb/papers/wang2026_interface_stability_kinetics_sulfide_assb.md` §14-B — 발단
- `litdb/papers/zhu2015_*` — 1.71 의 출처
