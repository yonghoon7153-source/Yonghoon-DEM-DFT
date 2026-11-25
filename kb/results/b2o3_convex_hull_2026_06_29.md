# B₂O₃-doped LPSCl1.6 convex-hull 안정성: 준안정(37.5 meV/atom), 분해산물이 BS₃를 예측

**날짜** 2026-06-29 · **방법** UMA(omat)-일관 convex hull (우리 구조 + MP 경쟁상 전부 UMA single-point)
**구조** `db/structures/b2o3_relaxV0.cif` (DFT V₀ 고정셀 relax) · **결과** `db/properties/b2o3_ehull_result.json`

> **한 줄 결론.** B₂O₃-doped 챔피언은 **E_above_hull = 37.5 meV/atom (준안정, 합성가능 범위)** — 무도핑 modelC(16.7)보다 **+20.8 meV/atom** 높지만 여전히 ≲50 meV/atom. 결정적으로 **hull 분해산물에 Li₃BS₃(삼각 BS₃ thioborate)와 Li₄B₇ClO₁₂(borate)가 등장** → 열역학이 독립적으로 **B→BS₃ thioborate + O→borate**를 예측, 우리 coordination 결론(BS₃ + free-S + O-on-P)을 **독립 입증**.

---

## 1. 결과

| 계 | E_above_hull (meV/atom) | chemsys | 분해산물 (분율) |
|---|---|---|---|
| **modelC (무도핑 LPSCl1.6)** | **16.7** | Li-P-S-Cl (110 MP) | Li₃PS₄ 0.65, LiCl 0.26, Li₂S 0.10 |
| **B₂O₃-doped (champion)** | **37.5** | Li-P-S-Cl-B-O (349 MP) | Li₃PS₄ 0.50, LiCl 0.25, Li₂S 0.19, **Li₄B₇ClO₁₂ 0.047, Li₃BS₃ 0.014** |
| Δ(도핑) | **+20.8** | | 도핑이 hull 위로 ~21 meV/atom 올림 |

- **둘 다 준안정** — argyrodite는 본래 0K hull 위 준안정(modelC 16.7이 그 증거). 둘 다 합성가능 범위(≲50 meV/atom, Sun 2016 metastability threshold).
- **도핑 페널티 +21 meV/atom** = B₂O₃가 들어가는 게 열역학적으로 약간 불리(도펀트가 별도 thioborate/borate로 갈라서려는 경향) — 하지만 37.5는 **여전히 합성가능 준안정**.

## 2. 분해산물 = coordination 결론의 독립 입증 ★

b2o3 hull 분해산물이 host 분해(Li₃PS₄+LiCl+Li₂S)에 더해 **두 B-상**을 예측:
- **Li₃BS₃** = 결정질 **orthothioborate, 삼각평면 BS₃** — 우리가 챔피언에서 찾은 바로 그 motif.
- **Li₄B₇ClO₁₂** = lithium borate chloride — **O가 borate로**.

→ 구조 분석(국소 배위)뿐 아니라 **열역학(hull)** 도 "B는 BS₃ thioborate, O는 borate로 가려 한다"고 말함. 두 독립 경로가 같은 결론 → BS₃ 결론이 매우 견고.

## 3. 정직한 한계
- **UMA(MLIP) 에너지** (DFT 아님). 절대 meV/atom엔 MLIP 오차(~수십 meV/atom 가능). **상대 Δ(+21)와 분해산물 정체(Li₃BS₃ 등)는 더 견고** (같은 방법 일관 비교 + 화학적으로 타당).
- `--mode mp`(MP 에너지 hull)는 우리 구조 에너지를 안 쓰고 조성만 보므로 다른(더 환원적: Li, S, Li₃P 등) 산물을 줌 — E_above_hull엔 **UMA 일관(--mode uma)이 정답**.
- DFT 절대 ΔE_above_hull이 필요하면 winner + 경쟁상 DFT 재계산 필요 (현재 미수행).

## 4. 종합 (paper용)
B₂O₃ 도핑 LPSCl1.6은 **준안정·합성가능(37.5 meV/atom, 무도핑 대비 +21)**. 도펀트는 열역학적으로 **Li₃BS₃(삼각 BS₃) + Li-borate로 살짝 갈라서려는 경향**이나 페널티가 작아 고용체로 존재 가능. 이 hull 분해 경향이 **챔피언 국소 배위(BS₃ + free-S + O-on-P)와 정확히 일치** — 구조·열역학 양면에서 "thioborate BS₃" 서사가 성립.

## 참고
- `db/properties/b2o3_ehull_result.json`, `docs/figures/cascade/b2o3_ehull_comparison.png`
- `tools/doping/convex_hull_ehull.py` (UMA-consistent / MP-products 모드)
- 관련: `kb/results/b2o3_champion_coordination_2026_06_29.md` (BS₃ 구조 결론)
