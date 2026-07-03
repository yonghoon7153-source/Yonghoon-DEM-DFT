# B₂O₃ Champion — 작업 현황 (2026-07-03)

**시스템** b2o3 "champion" = **B₂O₃ 도핑 Model C** (= 도핑된 LPSCl1.6). 조성
**Li58P8S41Cl16B2O3 (128원자)**, modelc 2× 슈퍼셀 프레임. screening/anneal 승자,
동역학 안정(허수모드 0), convex hull **+37.5 meV/atom**.
**비교 대상** modelc (= LPSCl1.6, 무도핑 Cl-only).
**목표** B₂O₃ 도핑이 argyrodite를 다물성(이온·기계·전자·안정성)에서 어떻게 개선하나
→ 슬라이드("champion") + paper figure.

## 현황표

| 축 | 항목 | 상태 | b2o3 | modelc(무도핑) |
|---|---|---|---|---|
| 이온 | BVSE 채널 | ✅ | 채널부피 **+45%**; percolation onset 면내 0.50 / c축 1.99 val² (**4× 이방성 — B₂O₃층이 c축 막음**) | — |
| 이온 | MD σ / Ea | ✅ multi-seed 갱신 | **Ea = 0.21 ± 0.03 eV** (3-seed 600K; 단일-seed 0.223은 막대 안의 한 점). σ **측정구간 ~1.3×** — **not a barrier effect** (RT 절대 σ는 seed 따라 11–65로 **보고불가**; D0-vs-barrier 분해는 seed 의존이라 폐기) | Ea 0.2235 → **오차 내 동일**. **modelc 3-seed reseed 진행중**(kgy)으로 대칭 막대화 |
| 기계 | EOS B0 | ✅ | **24.48 GPa** | 21.7 (**+13%**) |
| 기계 | **DFT Cij** | ⚠ 일부 | **Bulk 27 GPa 신뢰**(relaxed-ion normal + EOS 24.5 교차검증, +13% 강화). **G/E는 relaxed-ion shear ±basin 오염으로 미보고** (C66 붕괴·고유값 음수). clamped-ion 러너 준비됨(`tools/elastic/run_b2o3_elastic_clamped_kisti.sh`)이나 보류 | comp1 22.06 / modelc 27.66 (E_VRH); clamped ≈52 |
| 전자 | **ICOHP** | ✅ 완료 | **spilling 1.57%**. **P–O −8.56·B–S −7.57 = 새 강한 공유결합**(B–S가 host P–S보다 셈), **P–S −6.11≈modelc −6.00 = host 불변**. Li–X(−0.83/−0.80)는 minimal basis라 modelc와 미비교(확장basis 재실행 시 가능). 그림/CSV/json 커밋됨 | P–S −6.00, Li–Cl −2.10, Li–S −1.72 |
| 전자 | gap/Bader/ELF/CDD | ✅ | gap ~2.0 eV, B+3/P+5/O−1.9, **B–S ELF 0.959(최공유)**, P–O 0.930 | — |
| 안정성 | phonon/hull | ✅ | 0 허수모드, lowest 13.7 cm⁻¹, +37.5 meV/at | — |
| 안정성 | 산화창 ESW | ✅ | **0.31 V** (ox 2.03 / red 1.72) | 0.90 V |
| 구조 | 결합길이/배위 | ✅ | **B–S 1.83Å(삼각 BS3)**, P–O 1.56Å(phosphate PS2O2/PS3O), **B–O 없음**; Voronoi disorder ×1.3–4 | — |
| 광학 | ε∞ (분극률) | ⛔ 접음 | **Shelved (secondary).** 3경로 모두 막힘: ph.x DFPT epsil hang(GPU 빌드 없음) · lelfield ×2 hang(826870은 ecutrho600+PAW addusdens 15GB → iter1 stall, scancel) · epsilon.x는 NC pseudo 필요. **향후 과제**: ONCV NC pseudo로 SCF/nscf 재계산 후 epsilon.x. **논문은 4축으로 진행** | — |
| 이온 | Li density (MD 궤적) | ✅ 완료 | gabia 600K MD 궤적(400프레임)→ `b2o3_T600_Li.cube` (셀 검증 2436 Å³ = V0). BVSE(정적)와 짝 = 실제 Li 점유 | — |

## 진행 상태 (2026-07-03 갱신)

- **ICOHP** ✅ 완료 — 확장 basis(Li 1s2s2p, P/S/Cl 3s3p3d) 재실행, **spilling 1.19%**, host 결합(P–S) modelc와 정합, 새 결합 B–S/P–O. 그림·CSV·json 커밋됨.
- **elastic** ✅ 마감 — **Bulk 27 GPa 신뢰**(relaxed-ion normal + EOS 24.5 교차검증). relaxed-ion shear는 ±basin 오염으로 G/E **미보고**(정직).
- **ε∞** ⛔ 접음 — job 826870(lelfield ecutrho600+PAW) iter1 stall → `scancel`. NC epsilon.x는 향후 과제.
- **modelc 600K 3-seed reseed** ▶ kgy 진행중 — LPSCl1.6 Ea 대칭 오차막대용(`tools/modelc_v3/run_modelc_600K_reseed.sh`, 62-atom V0).

## 남은 것
- **modelc reseed 완료 시**: LPSCl1.6 Ea = 0.22 ± 0.0X 산출 → conductivity/decomposition CSV를 **대칭 오차막대로 최종화**(현재 single-seed 1.33×·D0-driven 파생물은 폐기·주석 정정 완료).
- ~~ε∞~~ **접음** (secondary, NC epsilon.x는 향후).
- ~~Li density~~ ✅ 완료.
- paper/슬라이드 조립.
