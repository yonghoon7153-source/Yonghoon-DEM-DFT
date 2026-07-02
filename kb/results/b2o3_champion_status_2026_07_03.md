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
| 이온 | MD σ₃₀₀ | ✅ | **18.5 mS/cm** (Ea 0.223) | 13.9 (0.224) → **1.33×, D0-driven** |
| 기계 | EOS B0 | ✅ | **24.48 GPa** | 21.7 (**+13%**) |
| 기계 | **DFT Cij** | ▶ **824692 (8/12)** | 지금까지 UMA만(E~41) → DFT Cij 채우는 중 | comp1 22.06 / modelc 27.66 (E_VRH) |
| 전자 | **ICOHP** | ▶ **824939 (PAW SCF)** | 지금까지 ELF만, LOBSTER 없음 → 채우는 중 | P–S −6.00, Li–Cl −2.10, Li–S −1.72 |
| 전자 | gap/Bader/ELF/CDD | ✅ | gap ~2.0 eV, B+3/P+5/O−1.9, **B–S ELF 0.959(최공유)**, P–O 0.930 | — |
| 안정성 | phonon/hull | ✅ | 0 허수모드, lowest 13.7 cm⁻¹, +37.5 meV/at | — |
| 안정성 | 산화창 ESW | ✅ | **0.31 V** (ox 2.03 / red 1.72) | 0.90 V |
| 구조 | 결합길이/배위 | ✅ | **B–S 1.83Å(삼각 BS3)**, P–O 1.56Å(phosphate PS2O2/PS3O), **B–O 없음**; Voronoi disorder ×1.3–4 | — |
| 광학 | ε∞ (ph.x epsil) | ▶ 대기 | SCF 수렴, ph.x epsil 대기 (ph.x hang 이력 → epsilon.x 우회 가능) | — |
| 이온 | Li density (MD 궤적) | ☐ 대기 | | |

## 지금 돌아가는 잡 (KISTI, /scratch/x3430a02/kgy/b2o3_eos)

- **824939 ICOHP** — all-PAW(kjpaw) SCF → nscf(nosym, nbnd460, wf_collect) → LOBSTER.
  볼 것: **charge spilling (<3%)**, **B–O / B–S −ICOHP** (기존 nd/comp1/modelc 스키마에 맞춰 비교).
  ⚠ 챔피언 cutoff(ecut 60/480) + 기본 basis 사용. 기존 `tools/comp1_v3/build_lobster_paw_inputs.py`는
  **ecut 70/560 + 확장 basis(Li 1s2s2p, P/S/Cl 3s3p3d)**로 spilling<5% 맞췄음
  → spilling 높으면 그 세팅으로 재실행.
- **824692_8 elastic** — relaxed-ion 12 strain (11/22/33/23/13/12 ×±). 8/12 완료, strain_13_p 이완 중.
  → b2o3 DFT Cij → K, G, E, ν (comp1/modelc paper-grade와 동일 프로토콜).

## 남은 것
- ε∞: ph.x epsil 실행 (또는 hang 시 epsilon.x 우회)
- Li density: MD 궤적에서 추출
- paper/슬라이드 조립 상태 및 TODO — kb 서사 정독(3/3) 후 갱신
