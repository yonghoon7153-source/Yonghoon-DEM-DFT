# DOS / PDOS — 무엇을 보는가 (modelC vs Nd₂O₃-doped)

작성 2026-06-24. DOS = 에너지별 상태밀도(E_F=0), PDOS = 원소별 분해. Gaussian **0.15 eV** 평활, gap = **eigenvalue gap**(`electronic.json` v100).

## modelC (LPSCl1.6) — gap **2.10 eV**
- **VBM = S 3p** : VB 최상단(≈−1.3 eV)이 **S 지배 ~90%** (PDOS: S 27 / total 30; Li 2 / Cl 0.4 / P 0.07).
- Cl 3p : −4 eV 큰 peak(보라).
- CB 바닥(+1.2~) = **S + P + Li**(PS₄ antibonding + Li). 깊은 VB는 P/Li 혼합.
- **clean insulator** : N(E_F)=0, E_F mid-gap.

## Nd₂O₃-doped modelC — gap **1.63 eV** (−0.47 vs modelC)
PDOS가 **통합노트 결론을 한눈에 시각 확정**(`kb/physics/nd_4f_doping_consolidated_corrected_2026_06_24.md` §2·C6·C7):
1. **VBM = S 3p 그대로** (host 불변) : VB 상단(−1.0 eV) S=11.5 ≫ Nd 0.7 / O 0.04.
2. **O 2p (빨강) DEEP, peak ≈ −3.9 eV = spectator** : gap edge(±0.7) 근처 아님 → **O는 전자구조에 무해**(갭 좁힘의 원인 아님). [C6]
3. **Nd (cyan)가 CBM 바닥에서 솟음 (peak ≈ +1.8 eV)** : Nd 5d/6s가 **CBM을 끌어내림 → gap 2.10→1.63 narrowing**. 단 **Nd 4f는 gap 밖**(채워진 4f 깊이, 빈 4f는 CB 위) → **gap 안에 4f 없음 → host는 clean insulator 유지**. = 순수 Nd 화합물의 "4f→metal" 실패와 **다름**. [C7]

| | VBM | gap 좁힘 주체 | O 위치 | 4f |
|---|---|---|---|---|
| **무엇이 보이나** | S 3p (host, 불변) | **Nd 5d @CBM** | −3.9 eV (deep, 무해) | gap 밖 (clean) |

## 한 줄
**VBM=S 3p(host 불변) · O 2p deep spectator(무해) · 갭 narrowing = Nd 5d@CBM (4f-in-gap 아님).**
→ "갭 좁힘 단점은 **Nd 몫**, O는 전자구조 **무해**"의 **직접 시각 근거**. (전자차단 σ_e↓는 bulk 갭이 아니라 interphase O-phosphate 효과 — `nd2o3_O_effect_transfer` §②.)

## ⚠ 주의
- gap = **eigenvalue gap**(modelc 2.099 / nd 1.632). **PBE라 절대값 ~1 eV 과소** → "wide-gap insulator"·trend만.
- DFT+U(Nd 4f, **U=8**). **Nd 4f 위치는 U 민감** → trend robust, 절대위치 주의. on-Nd 4f 정량은 **spin density** 권장(ELF/PDOS 4f는 신뢰 낮음).

## 파일
- **CSV(깔끔, 0.15 eV, valence 창 −8~5)** : `modelc_dos_pdos_0.15.csv` (E−EF, total, S, P, Cl, Li) · `nd_dos_pdos_0.15.csv` (+ O, Nd, **Nd_4f**).
- figure : modelC/nd DOS·PDOS(사용자 보유), `../nd_dos/nd_dos_pdos_v2.png`, `nd_{DOS,PDOS}.png`, `nd_4f_excluded_gap.png`.
- source : `../{modelc,comp1}_pdos_compact.csv`, `../nd_dos/nd_pdos_compact.csv`. 도구 : `tools/figures/export_dos_pdos_csv.py`.
> ⚠ 기존 `modelc_smooth0.15.csv`는 Li 1s semicore(−46 eV) 포함 깨진 파일 — **대신 `modelc_dos_pdos_0.15.csv` 사용**.
