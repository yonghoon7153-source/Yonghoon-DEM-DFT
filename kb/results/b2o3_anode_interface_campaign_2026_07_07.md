# B₂O₃ anode 계면 — 통제 campaign 확정판: **"6× 억제" 철회**, 도핑 ≈ 무도핑(악화 없음), BS₃ 강건·LiB 없음

**날짜** 2026-07-07 · **방법** UMA-s-1p1 MLIP-MD SE|Li-metal, **3 seed × 100 ps × 3 슬랩**, 600 K NVT · **동기** 예비(단일시드 50 ps) "6× 억제"의 caveat ①(통계) ②(표면종단 confound)을 정면 보완
**데이터** `db/properties/interface_campaign_summary.csv` (+ kgy per-seed `interface_decomp_{b2o3,modelc2x,modelc62}_s{2,3,4}.csv`) · **그림** `docs/figures/oxidation/interface_campaign_controlled.png` · **도구** `tools/oxidation/run_interface_campaign.sh`

> **한 줄.** **통제쌍**(b2o3 128원자 vs **modelc_2x 124원자 = b2o3를 도핑해 만든 바로 그 무도핑 프레임**, 같은 표면)에서 PS₄ 분해 **22±9% vs 26±0% = 오차 내 동등** — 예비 "6×"는 **얇은 1× 슬랩(modelc62, P 5개뿐) artifact**(같은 물질인데 48±8% = 2× 프레임의 1.9배)였다. **철회.** 유지되는 견고한 결론: ① **BS₃ thioborate 전 시드 온전(B–S 3.00→3.00)** ② **금속성 LiB 미형성**(B–Li 1–2는 B–S 온전 상태의 Li-배위 thioborate = 합금 아님) → **평형이 겁준 LiB worst-case는 동역학에서 실현 안 됨 = 도핑이 계면을 악화시키지 않음**(개선 주장도 하지 않음).

---

## 1. Campaign 결과 (3 seed × 100 ps, 600 K; mean±std)

| 지표 | b2o3 (2×,128) | modelc2x (2×,124, **통제**) | modelc62 (1×,62, 종단체크) |
|---|---|---|---|
| **PS₄ 손실 %** | **21.8 ± 9.1** | **25.6 ± 0.0** | 48.1 ± 7.8 |
| ΔP–Li (Li₃P) | 1.67 ± 0.56 | 1.63 ± 0.31 | 3.27 ± 0.25 |
| ΔS–Li (Li₂S) | 0.68 ± 0.20 | 0.96 ± 0.07 | 1.97 ± 0.12 |
| ΔLi 침투 | 7.0 ± 4.2 | 7.3 ± 0.5 | 10.3 ± 0.9 |
| B–S final | **3.00 ± 0.00 (온전)** | — | — |
| B–Li final | 1.5 ± 0.4 (B–S 온전 → LiB 아님) | — | — |

**통제 비율 (b2o3 / modelc2x):** PS₄ 85±36% · Li₃P 102±40% · Li₂S 71±22% · 침투 96±58% → **전 채널 100% 교차 = 동등** (Li₂S만 ~1.4σ 경계선 감소, 주장 안 함).

## 2. "6×"가 어디서 왔나 — artifact 해부
1. **슬랩 두께/P 개수**: P–S coord는 **전체 P 평균**. modelc62는 P가 5개뿐·슬랩이 절반 두께라 계면 반응층이 P 통계를 지배 → **같은 물질**인데 modelc2x(26%)의 **1.9배**(48%)로 부풀려짐. 예비 비교(b2o3 128 vs modelc62 62)는 이 artifact를 그대로 먹음.
2. **50 ps 타이밍 + 단일시드**: b2o3 단일시드 50 ps는 −8%였지만 100 ps에선 15–35% — **아직 self-limit 아님**, 분해 진행 중. 50 ps 시점의 "거의 무손상"은 시드 운 + 조기 스냅샷.

## 3. 유지되는 결론 (논문에 쓸 것)
- **도핑이 계면을 악화시키지 않는다**: 분해 채널 전부 무도핑과 동등. 평형 계산(`b2o3_anode_interface_2026_06_30.md`)의 "금속 LiB → 악화" worst-case는 **100 ps 동역학에서 실현 안 됨** — B는 끝까지 S 우리를 유지.
- **BS₃ 단위 자체의 강건성**: 모든 시드·모든 시점에서 B–S 3.00. (LPSC-MF의 MgS₄-온전 모티프와 동형이나, 우리 데이터는 "**단위 강건**"까지고 "**전체 골격 보호**"는 아님 — 그 구분을 지켜서 쓸 것.)
- 챔피언 서사: 이온 **보존**(O-penalty를 채널 개방이 상쇄) · 기계 **+13%** · 계면 **중립(악화 없음, LiB 없음)** · B–S 공유결합망.

## 4. 남은 한계 (정직)
- **100 ps에서 미수렴**: 양쪽 다 분해 진행 중 — 절대 분해량은 시간 하한, 비교(동등)만 인용.
- **종단 1개/프레임**: c-면 cleave 한 종류. 종단 다양화는 미탐색 (modelc62↔modelc2x 차이가 이미 종단·두께 민감성을 보여줌 → 절대값 인용 금지).
- **MLIP 반응상 정확도**(caveat ③): Li₃P/Li₂S/thioborate에서 UMA 검증용 DFT 단발 스냅샷 비교는 미실시 — 결론이 "동등"이라 부담은 낮아졌지만 선택적 보강 가능.

## 참고
- 예비(철회된 6×): `kb/results/b2o3_anode_interface_MD_dynamics_2026_07_06.md` (SUPERSEDED 배너)
- 평형 열역학: `kb/results/b2o3_anode_interface_2026_06_30.md` (Li-metal LiB worst-case / Li-In 완화)
- 이온 최종: `db/properties/b2o3_vs_lpscl16_conductivity.csv` (3-seed×3-T, Ea 0.199±0.034 vs 0.197±0.032, σ 동등)
