# B₂O₃-doped 챔피언의 anode 계면 안정성 — Li-metal에선 **악화**, Li-In에선 **완화**

**날짜** 2026-06-30 · **계기** 외부 peer-review #1(결정적 미계산) · **방법** open-Li 환원 profile (`get_element_profile`, esw와 동일 기구)
**도구** `tools/oxidation/anode_interface_stability.py` · **데이터** `db/properties/anode_interface_b2o3.json` · **그림** `docs/figures/oxidation/b2o3_anode_interface.png`

> **한 줄.** **bare Li metal(0 V)** 에선 B 도펀트가 금속성 LiB(gap 0)를 추가 → b2o3 reduction 계면 min gap **0.0**(무도핑 Li₃P 0.7보다 나쁨) = **도핑이 Li-metal 계면을 악화**. **그러나** 황화물 ASSB가 실제로 쓰는 **Li-In anode(≈0.62 V)** 에선 금속성 LiB가 **생성되지 않아**(B → B₆P + Li₃BO₃) min gap **0.7**(Li₃P only) = **무도핑-at-Li-metal과 같은 tier → 실용적으로 관리 가능.** 즉 b2o3의 최악 anode 부담은 **bare-Li-metal 한정**이고 Li-In이 그것을 피한다.

---

## 1. 방법
- 외부리뷰가 "positive 추천 전 필수"라 지적한 anode 계면 계산. **닫힌 InterfacialReactivity(SE, Li)는 부적합**(SE가 MP 상이 아니라 hull 투영 → 반응 ~0으로 오판). 대신 **open-Li `PhaseDiagram.get_element_profile(Li, SE)`**(esw_grand_potential과 동일) 로 Li chempot sweep → 각 anode 저장소 전압(μ_Li)에서의 환원 반응 + 산물.
- **anode 저장소를 다중화**: Li metal(0 V, 가장 환원적) · **Li-In(≈0.62 V, 표준 황화물-ASSB anode)**. 각 V에서 nearest-step 분해 반응을 읽음.
- 산물별 **MP band gap** 으로 leaky(<2 eV, 전자전도성 → 비passivating) 판정. b2o3 vs 무도핑 LPSCl1.6 비교.

## 2. 결과
| 계 | anode | 환원 반응 (요지) | gap-한정 상 | **min gap** | leaky |
|---|---|---|---|---|---|
| **b2o3** | Li-metal (0 V) | → 2 LiB + 3 Li₂O + 8 Li₃P + 16 LiCl + 41 S | **LiB 0.0** (금속성) | **0.0** | LiB(0.0), Li₃P(0.7) |
| **b2o3** | **Li-In (0.62 V)** | → ⅙ B₆P + Li₃BO₃ + 7.83 Li₃P + 16 LiCl + 41 S | Li₃P 0.7 | **0.7** | Li₃P(0.7) |
| LPSCl1.6 | Li-metal (0 V) | → Li₃P + 1.6 LiCl + 4.4 S | Li₃P 0.7 | 0.7 | Li₃P(0.7) |
| LPSCl1.6 | Li-In (0.62 V) | → 0.5 P₂S₇ + 1.6 LiCl + 0.9 S | P₂S₇ 1.89 | 1.89 | P₂S₇(1.89) |

→ **핵심 대비**: b2o3는 Li-metal에서만 금속성 LiB(0.0)가 나오고, Li-In에선 B가 **B₆P + Li₃BO₃**(둘 다 비-leaky, Li₃BO₃는 5.15 eV)로 가 LiB가 사라진다. 남는 leaky는 Li₃P(0.7)뿐 = 무도핑-at-Li-metal과 동급.

## 3. 해석 — Li-metal 부담은 bare-Li-metal 한정, Li-In이 완화
1. **vs bare Li metal: 도핑이 악화.** Li₃P(0.7, leaky)는 황화물 SE 공통이나, b2o3는 거기에 **금속성 LiB(gap 0)** 를 더함 → 계면에 전자전도 경로 → 환원 self-limiting 실패. min gap 0.0 < 무도핑 0.7. (앞선 "악화 안 함" 추측은 틀렸고 계산이 정반대 — 외부리뷰+실계산의 가치.)
2. **vs Li-In: 부담이 사라짐.** Li-In은 μ_Li가 덜 환원적(0.62 V) → B가 **금속성 LiB 대신 B₆P + Li₃BO₃**(Li₃BO₃ 5.15 eV, passivating)로 감. min gap이 0.0 → **0.7**로 올라가 **무도핑-at-Li-metal과 같은 tier**. 무도핑은 Li-In에서 더 완만(1.89, P₂S₇).
3. **즉 trade-off는 anode 선택에 의존.** bulk 수송 이득(D₀↑)의 대가인 "악화된 anode"는 **bare Li metal에서만** 결정적이고, 황화물 ASSB가 어차피 쓰는 **Li-In 합금 anode면 실용적으로 관리 가능**(이게 황화물 ASSB가 Li-In을 쓰는 바로 그 이유).
4. **실용 함의**: b2o3를 Li metal 직접 접촉으로 쓰면 interlayer가 무도핑보다 더 절실하지만, **표준 Li-In 셀 구성에선 anode가 deal-breaker가 아니다.** headline 부담은 여전히 좁은 ESW·준안정성이지 Li-In-anode 계면이 아님.

## 4. 정직한 한계
- **열역학 산물만** — 형태(morphology)·연속성·동역학·실제 SEI 두께·핵생성 미모델. "LiB 생성"은 가능성이지 percolating 금속막 확정은 아니며, "Li-In에서 LiB 부재"도 평형 산물 기준.
- MP GGA/GGA+U gap(LiB metallic은 견고하나 절댓값엔 한계). Li-In 전압은 ≈0.62 V 대표값(조성·SOC에 따라 변동); nearest-step 근사.
- 단일 조성·평형 가정. cathode(양극) 산화 계면은 §5(미계산, `interface_reactivity_v2.py`).

## 5. smart factory 모듈로의 확장 (interface-stability)
이 계산은 factory의 **`anode_interface_stability` 섹션**(report card)에 done으로 들어감(`li_in_min_gap_eV` 포함). 일반화하면 강력한 모듈:
- **Anode reservoirs**: Li metal(0 V)✅ · **Li-In(0.62 V)✅** · Li-Al(0.30 V) · Li-Sn(0.85 V) → 각 μ_Li에서 계면 산물·leaky (도구는 `--anode_voltages`로 임의 확장).
- **Cathode(양극) 산화 계면**(미계산): SE vs LiCoO₂/NMC811 등 충전 전압에서 — `interface_reactivity_v2.py`(이미 존재) 로 산화 interphase → report card에 **anode + cathode 양면 interface** 표준 섹션.

## 참고
- `db/properties/anode_interface_b2o3.json`(by_anode: Li-metal + Li-In), `docs/figures/oxidation/b2o3_anode_interface.png`
- 도구: `tools/oxidation/anode_interface_stability.py`(open-Li, 다중 anode), `tools/oxidation/plot_anode_interface.py`(그림), `interface_reactivity_v2.py`(cathode)
- 관련: `kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md`(ESW), `factory/cards/b2o3_report_card.md`, 외부리뷰 `factory/REVIEW.md`
