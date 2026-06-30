# B₂O₃-doped 챔피언의 Li-metal anode 계면 안정성 — 도핑이 anode를 **악화**시킴

**날짜** 2026-06-30 · **계기** 외부 peer-review #1(결정적 미계산) · **방법** open-Li 환원 profile (`get_element_profile`, esw와 동일 기구)
**도구** `tools/oxidation/anode_interface_stability.py` · **데이터** `db/properties/anode_interface_b2o3.json` · **그림** `docs/figures/oxidation/b2o3_anode_interface.png`

> **한 줄.** Li metal(V=0)에 닿으면 b2o3는 **LiB + Li₂O + Li₃P + LiCl + S** 로 환원되는데, **B 도펀트가 금속성 LiB(gap 0)를 추가** → reduction 계면 min gap **0.0**(무도핑 Li₃P 0.7보다 나쁨). **도핑이 Li-metal 계면 전자안정성을 악화**시킨다(수송↑의 대가). 둘 다 anode interlayer 필요(황화물 숙명)이나 **b2o3가 더 절실**.

---

## 1. 방법
- 외부리뷰가 "positive 추천 전 필수"라 지적한 anode 계면 계산. **닫힌 InterfacialReactivity(SE, Li)는 부적합**(SE가 MP 상이 아니라 hull 투영 → 반응 ~0으로 오판). 대신 **open-Li `PhaseDiagram.get_element_profile(Li, SE)`**(esw_grand_potential과 동일) 로 Li chempot sweep → **V≈0(μ_Li=metal=Li metal 접촉)** 의 환원 반응 + 산물.
- 산물별 **MP band gap** 으로 leaky(<2 eV, 전자전도성 → 비passivating) 판정. b2o3 vs 무도핑 LPSCl1.6 비교.

## 2. 결과
| 계 | Li metal 환원 반응 | 산물 gap (eV) | **min gap** | leaky |
|---|---|---|---|---|
| **b2o3** | Li₅₈B₂P₈S₄₁Cl₁₆O₃ → 2 LiB + 3 Li₂O + 8 Li₃P + 16 LiCl + 41 S | LiB **0.0**, Li₃P 0.7, S 2.61, Li₂O 4.9, LiCl 6.65 | **0.0** | **LiB(0.0)**, Li₃P(0.7) |
| LPSCl1.6 | Li₅.₄PS₄.₄Cl₁.₆ → Li₃P + 1.6 LiCl + 4.4 S | Li₃P 0.7, S 2.61, LiCl 6.65 | 0.7 | Li₃P(0.7) |

## 3. 해석 — 핵심 trade-off
1. **둘 다 Li-metal 불안정** — Li₃P(0.7 eV, leaky) 생성 = **황화물 SE 공통**(Li metal에 환원되는 잘 알려진 현상). 이것만 보면 도핑 무관.
2. **그러나 b2o3가 더 나쁨** — **B 도펀트가 금속성 LiB(gap 0)를 추가** → 계면에 **전자전도 경로** → Li metal에서 환원이 계속됨(self-limiting 안 됨). min gap 0.0 < 무도핑 0.7.
3. **즉 도핑이 anode 계면을 악화** — bulk 수송(D₀↑)을 얻는 대가로 **Li-metal 계면 전자안정성을 잃음.** (앞선 "악화 안 함" 추측은 틀렸고, 계산이 정반대를 보임 — 외부리뷰+실계산의 가치.)
4. b2o3는 Li₂O(4.9, passivating)도 추가하나 **금속성 LiB가 min gap을 지배** → 순효과는 악화.
5. **실용 함의**: 황화물 SE는 보통 Li-In 등 합금 anode 또는 interlayer를 씀. b2o3는 그 필요가 **무도핑보다 더 큼.**

## 4. 정직한 한계
- **열역학 산물만** — 형태(morphology)·연속성·동역학·실제 SEI 두께 미모델. "LiB 생성"은 가능성이지 percolating 금속막 확정은 아님.
- MP GGA/GGA+U gap(LiB metallic은 견고하나 절댓값엔 한계). 단일 조성·평형 가정.
- **다음**: Li-In(V≈0.62)·Li-Al 등 합금 anode에서의 계면(완화되는지) + cathode(양극) 산화 계면(아래 §5).

## 5. smart factory 모듈로의 확장 (interface-stability)
이 계산은 factory의 **`anode_interface_stability` 섹션**(report card)에 done으로 들어감. 일반화하면 강력한 모듈:
- **Anode reservoirs**: Li metal(0 V)✅ · **Li-In(0.62 V)** · Li-Al · Li-Sn → 각 μ_Li에서 계면 산물·leaky. (Li-In은 덜 환원적이라 보통 완화 — 정량 확인 가치.)
- **Cathode(양극) 산화 계면**: SE vs LiCoO₂/NMC811 등 충전 전압에서 — `interface_reactivity_v2.py`(이미 존재) 로 산화 interphase.
- → report card에 **anode + cathode 양면 interface 안정성** 표준 섹션.

## 참고
- `db/properties/anode_interface_b2o3.json`, `docs/figures/oxidation/b2o3_anode_interface.png`
- 도구: `tools/oxidation/anode_interface_stability.py`(open-Li), `interface_reactivity_v2.py`(cathode)
- 관련: `kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md`(ESW), `factory/cards/b2o3_report_card.md`, 외부리뷰 `factory/REVIEW.md`
