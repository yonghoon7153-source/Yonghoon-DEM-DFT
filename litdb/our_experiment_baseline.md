# 우리 실험 기준값 (our_experiment_baseline) — 건식 후막 bimodal 전고체 복합양극

> 이 브랜치(실험 파트)의 **ground truth**. 모든 문헌 비교(`comparison_vs_ours.md` §)의 실험측 기준점.
> 시뮬레이션 기준값은 `our_dem_baseline.md`(DEM/MPM, stoic-knuth 연계). 원자료는 `../db/`.
> 갱신: 2026-06-26.

## 0. 소재계 / 공정 한 줄 요약
단결정 NMC811 (No.1/No.2) + 다결정 대립 NMC811 (Poly) + Li₆PS₅Cl(LPSCl, ~1 µm) catholyte +
VGCF/Super C + PTFE(MW 50만) 바인더. **무용매 건식 공정** (Thinky 믹싱 → ball-mill → PTFE 섬유화 →
hot rolling). 조성 **AM:SE:VGCF:PTFE = 80:18:1:1**.

## 1. 양극활물질 (CAM) — `../db/materials/cathode_active_materials.csv`
| 실험명 | 보고서명 | 종류 | Ni/Co/Mn(ICP) | D50 | 비용량(half, 0.1C DC) | 표면 |
|---|---|---|---|---|---|---|
| No.1 | NCM_2 | 단결정 소립 | 82.5/12.7/4.8 | 3.94 µm | **205.9 mAh/g** | 매끈 |
| No.2 | NCM_3 | 단결정 소립 | 86.9/5.7/7.4 | 3.84 µm | **213 mAh/g** | satellite 잔류물 |
| Poly | 대립 | 다결정 811 | ~Ni88 | ~10 µm(2차) | **200 mAh/g** | cauliflower |

- 진밀도 NCM = 4.8 g/cm³. ⚠ 보고서 NCM_1/2/3 ≠ 실험 No.1/No.2/Poly (NCM_1=자체구입 5µm 응집, 미사용).

## 2. 고체전해질 — `../db/materials/solid_electrolyte.csv`
LPSCl 아지로다이트, ~1 µm, **σ_ion = 2.0 mS/cm** (500 MPa 가압, 60 MPa 체결), 진밀도 2.0 g/cm³.

## 3. 건식 복합양극 전달 특성 (실측) — `../db/electrochemistry/ptfe_conductivity.csv`
| PTFE wt% | σ_electronic | σ_ionic | 비고 |
|---|---|---|---|
| 0.5 | 0.04–0.05 mS/cm | **0.062 mS/cm** | 최고 이온전도 |
| 1.0 | 0.04–0.05 mS/cm | **0.057 mS/cm** | 표준 조성 |
| 2.0 | 0.04–0.05 mS/cm | **0.019 mS/cm** | PTFE 과다 → SE-SE 접촉 차단 |

- **σ_e는 PTFE 무관(도전재 지배), σ_ion은 PTFE↑ → 급감** (Lee2025 경향과 일치).
- PTFE 최소 0.5 wt%(미만은 전극 미형성), 2.0%까지 형성 가능.

## 4. ★ Bimodal porosity (건식 펠렛, Furnas dip) — `../db/porosity/`
| P:S(대립:소립) | porosity 평균 | std |
|---|---|---|
| S only (0:10) | 23.9 % | 3.7 |
| 3:7 | 21.2 % | 3.4 |
| 5:5 | 20.2 % | 2.5 |
| **7:3 (최소)** | **19.7 %** | 3.1 |
| P only (10:0) | 25.3 % | 1.8 |
→ **bimodal dip 실험 확증, 최소 P:S=7:3 ≈ 19.7%.** DEM/McGeary/Bouvard packing의 실험 앵커.

## 5. 전기화학 성능 (실측)
- **Half-cell 코인 formation** (2.5–4.3 V, 25 ℃, 0.1C) — `../db/electrochemistry/formation_coincell.csv`:
  No.1 CC225.0/DC205.9/Eff91.5%/DCIR23.5Ω · No.2 CC237.3/DC213.0/Eff89.8%/DCIR27.5Ω.
- **건식 전고체셀 0.1C** (NCM_1, PTFE별): 0.5% 230.5/198.7 · 1% 225.9/194.2 · 2% 227.9/196.8 (충/방전 mAh/g).
- **율속** (0.5% PTFE, 1C): NCM_2(매끈) 150 mAh/g > NCM_3(잔류물) 135 mAh/g → 표면구조가 율속 지배.
- 셀 구성: SE 0.15 g 50 MPa → 전극 13 mm → 500 MPa → Li-In → 60 MPa 체결. -50℃ 노점 드라이룸, 30 ℃.

## 6. 로딩 / 면용량 — `../db/loading/loading_table.csv`
- 면용량 3 mAh/cm² 기준 CAM 로딩: No.1 14.57 · No.2 14.08 · Poly 15.0 mg/cm².
- Bimodal 블렌드 비용량(가중): P:S 7:3=201.77 · 5:5=202.95 · 3:7=204.13 mAh/g (200~205.9 사이 선형).

## 7. 설계 변수 / 모델 파라미터 — `../db/model/p2d_parameters.csv`
면용량 4/6/8 · fam 0.7/0.8/0.9 · P:S 3:7/5:5/7:3 · 제작압 450 MPa · 구동압 150 MPa.
P2D: i0=5 A/m², D_Li,NCM=1e-14 m²/s, σ_e,cathode=10 mS/cm, E_NCM=221 GPa, E_LPSCl=22.3 GPa.
⚠ 모델 σ_ion,cathode 가정값(0.25 mS/cm)이 실측(0.057–0.062)과 ~4× 차이 — `../docs/project/05_ISSUES_AND_FIXES.md`.

## 8. 핵심 trade-off (2차년도 설계 표적)
**packing 최적(P:S≈7:3, porosity 최소) ↔ 입자내 전달 최적(소립 단결정↑, grain boundary 저항↓)**.
대립↑ → packing 좋아지나 입자내 Li 확산·GB 저항↑·두께방향 이용률 편차↑. 최적점 = bimodal 비율 + fam + 면용량의 결합 최적화.
