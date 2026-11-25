# B₂O₃-doped 챔피언 — anode(Li, Li-In) + cathode 계면을 **하나의 전기화학 창**으로 통합

**날짜** 2026-06-30 · **계기** "li, li-in, cathode 통합" · **그림** `docs/figures/oxidation/b2o3_interface_window_integrated.png`
**도구** `tools/oxidation/plot_interface_window_integrated.py` · **데이터** `anode_interface_b2o3.json` + `b2o3_esw.json` + `b2o3_sei_gaps.json`

> **한 줄.** 0 V(Li metal) → 0.62 V(Li-In) → … → ~4.3 V(충전 양극)까지 **하나의 전압 축**에 **계면 product의 band gap(=전자 leakiness)** 을 그리면 b2o3의 계면 이야기가 한눈에 갈린다: **anode쪽이 liability**(LiB 0.0 @ Li metal → Li₃P 0.7 @ Li-In, 둘 다 leaky<2 eV), **cathode/산화쪽은 오히려 passivated**(Li₂B₂S₅ 2.44 → B₂O₃ 8.38 → BPO₄ 7.0, 전부 wide-gap). 즉 **B/O 도펀트의 부담은 환원(anode)쪽에 몰려 있고, 산화(cathode)쪽에선 wide-gap B/O 상이 보호막**이 된다.

---

## 1. 왜 하나의 그림으로 통합되나 — 공통 지표
anode 계면과 cathode 계면은 보통 따로 본다. 그러나 **둘 다 같은 질문**을 묻는다: *"이 전압에서 생기는 interphase가 절연성(passivating)인가, 전자전도성(leaky)인가?"* → **공통 y축 = 한정 product의 MP band gap(eV)**, **공통 x축 = V vs Li/Li⁺**. <2 eV면 leaky(전자전도 → 환원/산화가 self-limiting 안 됨), ≥2 eV면 passivating. 이 한 장으로 **Li metal · Li-In · 산화/cathode** 를 같은 척도에서 비교한다.

- **anode 저장소 점**(원형, 0 V·0.62 V): 실제 Li/Li-In 접촉의 환원 interphase — `anode_interface_b2o3.json`(open-Li `get_element_profile`).
- **intrinsic 분해 점**(다이아몬드, 1.72→3.24 V): SE 자체의 전기화학 분해 product가 전압 상승(산화, 양극쪽)에 따라 어떻게 변하는지 — `b2o3_esw.json`(B-product 전압) + `b2o3_sei_gaps.json`(gap).

## 2. 통합 결과 (b2o3)
| V (vs Li⁺) | regime | 한정 product | gap (eV) | 판정 |
|---|---|---|---|---|
| **0.00** | anode — Li metal | **LiB** (금속성) | **0.00** | 🔴 leaky (최악) |
| **0.62** | anode — Li-In | **Li₃P** | **0.70** | 🔴 leaky |
| 1.72 | 환원 한계(intrinsic) | BP | 1.08 | 🔴 leaky |
| 2.03 | 산화 한계(intrinsic) | Li₂B₂S₅ | 2.44 | 🟢 passivating |
| 2.75 | 산화(intrinsic) | B₂O₃ | 8.38 | 🟢 passivating |
| 3.24 | 산화/cathode(intrinsic) | BPO₄ | 7.00 | 🟢 passivating |

비교(무도핑 anode): Li metal Li₃P **0.70**, Li-In P₂S₇ **1.89**(둘 다 무도핑이 b2o3보다 완만).

## 3. 통합 해석 — 부담은 anode, 보호는 cathode
1. **anode쪽 (V ≤ 1.7, 붉은 영역)**: b2o3의 모든 계면 product가 leaky(<2 eV). 특히 **bare Li metal에서 금속성 LiB(0.0)** = 최악 → 도핑이 **환원 안정성을 악화**. 단 **Li-In(0.62 V)이면 LiB가 안 생기고 Li₃P(0.7)** 로 완화(§ 별도 note). → **anode가 headline liability이며, 완화책은 Li-In 합금 anode.**
2. **cathode/산화쪽 (V ≥ 2.0, 초록 영역)**: 산화 product가 전부 **wide-gap passivating** — Li₂B₂S₅(2.44), 특히 **B₂O₃(8.38)·BPO₄(7.0)**. 즉 **B/O 도펀트가 산화쪽에 절연 보호막**을 만든다. 이것이 "**좁은 ESW(0.31 V)를 passivating interphase가 보상**"(sei note)한다는 말의 실체 — 보상은 **산화쪽에서** 일어난다.
3. **통합 그림의 메시지**: 같은 도펀트가 **anode에선 독(metallic LiB), cathode에선 약(wide-gap B/O)**. 전기화학 창을 가로지르며 부호가 바뀐다. 셀 설계 함의: **Li-In anode + (필요시) 양극 코팅** 조합이면 b2o3의 양면 계면이 모두 관리 범위.

## 4. 정직한 한계
- **열역학 product/평형 가정** — 형태·연속성·동역학·실제 interphase 두께 미모델. gap은 MP GGA/GGA+U(절댓값 한계, 금속성/절연성 경향은 견고).
- **"intrinsic 분해"는 SE 자체의 전기화학 분해**이지, **SE + 특정 양극(LiCoO₂/NMC811)의 화학 반응**이 아님. 후자(더 정밀한 cathode 계면)는 **`interface_reactivity_v2.py`(voltage-resolved Richards/Ong 2016)** 로 별도 계산 — **아직 미실행**. 실행하면 이 그림에 "SE/cathode 반응성" overlay로 추가, report card의 `cathode_interface_stability` 섹션이 done으로 채워짐.
- anode 점(0·0.62 V)과 intrinsic 점(≥1.72 V)은 **다른 regime**(저장소 접촉 vs 자체 분해)이라 한 곡선이지만 물리적 의미가 구간별로 다름(그림 범례·본문에서 구분).

## 5. report card 연결
- `anode_interface_stability`: **done**(Li-metal + Li-In, `li_in_min_gap_eV` 포함).
- `cathode_interface_stability`: **n.a.(pending)** — `interface_reactivity_v2.py` 실행 시 자동 done(assembler 배선 완료).
- 이 통합 그림은 두 섹션 + ESW를 잇는 **synthesis 그림**(factory `interface_stability` stage의 figure 산출).

## 참고
- 그림/도구: `docs/figures/oxidation/b2o3_interface_window_integrated.png`, `tools/oxidation/plot_interface_window_integrated.py`
- 데이터: `db/properties/anode_interface_b2o3.json`, `b2o3_esw.json`, `b2o3_sei_gaps.json`
- 관련 note: `kb/results/b2o3_anode_interface_2026_06_30.md`(Li-In 완화), `kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md`(ESW)
- cathode 정밀화: `tools/oxidation/interface_reactivity_v2.py`(미실행), 그림 `tools/oxidation/plot_cathode_interface.py`
