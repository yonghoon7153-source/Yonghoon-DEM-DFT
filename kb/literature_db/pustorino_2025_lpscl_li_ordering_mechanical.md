# Pustorino et al. 2025 — LPSCl Li ordering → 기계적/전자 물성

**제목**: Mechanical and Electronic Properties of Bulk and Surface Li6PS5Cl
Argyrodite: First-Principles Insights on Li-Filament Resistance
**저자**: G. Pustorino, H. Jagad, W. Li, M. Feng, M. Poma, J. Ko (SK On),
P. Johari, **Y. Qi*** (Brown Univ.)
**저널**: *Chem. Mater.* **2025**, *37*, 313–321 (online Dec 20, 2024)
**DOI**: [10.1021/acs.chemmater.4c02577](https://pubs.acs.org/doi/10.1021/acs.chemmater.4c02577)
**관련 PDF (로컬)**:
- 본문: `/root/.claude/uploads/.../9c0aba00-...pdf`
- SI: `/root/.claude/uploads/.../2f7eb4cd-cm4c02577_si_001.pdf`

---

## 1. 우리에게 왜 중요한가 (TL;DR)

> **Li ordering 하나만 바뀌어도 B0가 13.7 → 29.6 GPa로 ±50% 흔들린다.**
> 단일 random 구조로 EOS fit하면 B0/E를 잘못 보고할 위험이 큼 →
> **anneal + 다중 relaxation으로 ground state 잡고 ensemble 평균 내야 함**
> (= 우리가 UMA EOS pre-screening 단계에서 anneal·relax를 도입한 이유의
> 1차 reference)

이 논문이 우리 워크플로우에 주는 4가지:
1. **B0/E 분산의 정량 reference** — 그 어떤 dopant보다도 Li ordering이 더 큰 변동 요인일 수 있다
2. **Strain 한계 = 1%** — elastic constants 계산 시 그 이상이면 Li가 24g→48h hop해서
   "shear instability"로 잘못 측정됨
3. **Ground state는 48HR (no inv) 또는 48HR^inv** — `data/lpscl_bulk.cif`에 무엇을 쓸지
   가이드라인. mp-985592 그대로 쓰면 사실 metastable 상태
4. **(100)-Li2S-deficient surface fracture energy = 0.20 J/m²** —
   우리 adhesion work (sundar/우리 v2 paper)에서 surface energy reference

---

## 2. Methods 요약

### DFT 세팅 (재현용)
| 항목 | 값 |
|------|-----|
| Code | VASP |
| XC | PBE-GGA |
| Cutoff | 650 eV |
| Electronic conv. | 1×10⁻⁶ eV |
| Force conv. | 0.01 eV/Å |
| Smearing | Gaussian, 0.1 eV |
| Bulk supercell | 52 atoms |
| K-points (bulk) | 3×3×3 Monkhorst-Pack |
| Slab K-points | 3×3×1 |
| Vacuum | 10 Å (양쪽) |
| Elastic constants | Finite difference, **max strain = 1%** |
| S/Cl inversion | ATAT (SQS), 4 unit cells along (100), (011), (022̄) |

### Chemical potentials (Li/LPSCl interface 평형, 기준 = Li, Li2S, Li3P, LiCl)
| Element | μᵢ (eV/atom) |
|---------|--------------|
| Li | **−1.905** |
| P | **−8.251** |
| Cl | **−5.532** |
| S | **−8.186** |

→ 우리도 fracture/surface energy 계산 시 이 값 그대로 차용 가능
(γ = (E_slab − n·E_bulk − Σnᵢμᵢ) / A 식에서 fracture energy = 2γ).

---

## 3. ⭐ Bulk 구조 13개 ensemble (Table 2)

명명규칙:
- **24G / 48H / Rand**: Li 초기 위치 (24g 만 / 48h 만 / 무작위)
- **subscript "super"**: 96 Li 슈퍼셀, 없으면 24 Li
- **subscript "rand"**: 무작위 채움
- **superscript "inv"**: 50% S²⁻/Cl⁻ inversion 적용
- **48HR**: 48h 50% 점유 (24개 무작위, 1 Li per trigonal bipyramid 강제)

| Initial | S/Cl inv | After relax (24g % / 48h %) | V (Å³/f.u.) | ΔE (eV/f.u.) |
|---------|----------|-----------------------------|-------------|--------------|
| 24G_super^rand | no | 30 / 70 | 283.06 | +0.05 |
| 24G | no | 100 / 0 | 269.34 | 0.00 (ref) |
| 24G_super | no | 100 / 0 | 269.25 | 0.00 |
| 24G^inv | 50% | 17 / 83 | 257.66 | −0.32 |
| 48H_super^rand | no | 12 / 88 | 253.19 | −0.42 |
| 48H^inv | 50% | 0 / 100 | 247.47 | −0.62 |
| 24G^inv_super | 50% | 17 / 83 | 246.25 | −0.63 |
| 48H^inv_super | 50% | 8 / 92 | 247.80 | −0.69 |
| 48H | no | 33 / 67 | 248.41 | −0.72 |
| 48HR^inv | 50% | 0 / 100 | 241.77 | −0.73 |
| 48H_super | no | 17 / 83 | 249.57 | −0.77 |
| Rand_super | no | 33 / 67 | 269.31 | −0.77 |
| **48HR** | **no** | **17 / 83** | **254.11** | **−0.80** ⭐ |

### 주요 관찰
1. **All-24G로 시작 → relax 후에도 100% 24g (cubic cell 1×1×1에서)** — 단순 relax는
   metastable trap에 갇힘. 슈퍼셀(super) 또는 random 초기화가 있어야 24g→48h 호핑이 일어남
2. **Final ground state는 48HR (no inversion)**, ΔE = −0.80 eV/f.u. — 24g 100%
   대비 약 0.8 eV/f.u. 더 안정. 1 f.u. = 13 atoms 기준 60 meV/atom
3. **S²⁻/Cl⁻ inversion 50% 패널티 ≈ +0.07 eV/f.u.** (48HR vs 48HR^inv 비교) — 작아서
   엔트로피로 충분히 mixing 가능 → NMR 실험 50% inversion과 일치
4. **48h 우세 ground state는 실험과 부합** (Schlenker 2020 Chem Mater, refs 30/31)

---

## 4. ⭐ Elastic Properties (Table 3) — Li ordering의 영향

| Structure | C11 | C12 | C44 | **B0 (GPa)** | G (GPa) | **E (GPa)** | ν |
|-----------|-----|-----|-----|--------------|---------|-------------|----|
| 24G       | 42.5 | 23.2 | 10.8/10.9 | **29.6** | 10.3 | **27.8** | 0.34 |
| 48H       | 44.0 | 21.9/20.6 | 13.2/7.9 | **29.5** | 10.8 | **29.0** | 0.33 |
| 48H^inv   | 21.9 | 8.5/8.3 | 7.2/9.5  | **13.7** | 8.8  | **21.7** | 0.23 |
| 48HR      | 31.7 | 17.2/15.6 | 12.3/15.2 | **19.9** | 12.0 | **29.9** | 0.25 |
| 48HR^inv  | 47.0 | 17.3/14.8 | 14.5/14.2 | **27.2** | 14.9 | **37.9** | 0.27 |

### 메시지
- **B0 range: 13.7 ~ 29.6 GPa = ±50% spread** — 같은 LPSCl인데도!
- **Young's modulus: 21.7 ~ 37.9 GPa = 75% spread**
- 24G ↔ 48HR (Li 분포만 다르고 inversion 없음): B0/E/G 거의 같음 (29.6 vs 19.9 GPa, 27.8 vs 29.9 GPa) →
  **"Li site (24g vs 48h) 자체는 elastic에 큰 영향 없다"**
- 48H ↔ 48H^inv (S/Cl inversion만 추가): **inversion이 modulus 감소시킴**
  (29.5 → 13.7 GPa B0)
- 48HR ↔ 48HR^inv: **반대로 inversion이 modulus 증가시킴** (19.9 → 27.2 GPa)
  → **inversion 효과는 Li 분포에 따라 부호가 바뀌는 비선형 결합 효과**
- 따라서 "S/Cl inversion이 항상 stiffening/softening한다"고 단정 못 함 — coupled
- Voigt-Reuss-Hill averaging 사용

### 우리 작업 함의
- **dopant 효과 (예: Nd→Li, Mg→Li)를 modulus로 평가하려면** Li ordering 분산
  (~16 GPa)을 먼저 컨트롤해야 함 → 같은 ordering ensemble 내 비교 또는 ensemble 평균
- 우리 EOS sweep에서 V0 변화 1~2%는 ordering 영향과 구분 안 갈 수도 있음 →
  **상대 비교 (pair01 vs pair02)는 같은 Li 배열 유지가 필수**
- **strain ≤ 1% 룰** 우리 EOS prep에도 반영 필요 — 현재 7-volume EOS (94~106%)는
  cell volume 기준 ±6%이므로 hop 가능. strain 큰 케이스는 "shear instability"
  artifact 가능성 있음을 디스카운트해야 함

---

## 5. Surface / Fracture (Table 4)

(100) plane 5개 termination + (110) 1개 비교:

| Surface | Layers | Stoichiometry | S/Cl inv | **γ_fracture (J/m²)** |
|---------|--------|---------------|----------|------------------------|
| (100)-Li2S-rich (sym)        | 6 | Li76P12S62Cl12 | no | 0.74 |
| (100)-Li2S-rich (sym)        | 3 | Li40P6S31Cl6   | no | 0.78 |
| **(100)-Li2S-deficient (sym)** | 6 | Li68P12S58Cl12 | no | **0.20** ⭐ |
| (100)-Li2S-deficient (sym)   | 3 | Li32P6S28Cl6   | no | 0.22 |
| (100)-LiCl-rich              | 6 | Li74P12S60Cl14 | yes (50%) | 0.78 |
| (100)-LiCl-rich              | 6 | Li74P12S60Cl14 | no  | 0.75 |
| **(100)-LiCl-deficient**     | 6 | Li70P12S60Cl10 | yes (50%) | **0.44** |
| (110)-stoichiometric         | 6 | Li64P14S70Cl14 | no  | 0.37 |

### 메시지
- **Crack은 (100)-Li2S-deficient surface에서 진행 (γ = 0.20 J/m²)** —
  가장 약한 cleavage plane
- 이 값은 LLZO (γ = 1.72 J/m²)의 1/9 — 그래서 LPSC가 mechanical crack에 약함
- **Cl-rich vs Cl-deficient: Cl-deficient가 더 약함** (0.44 vs 0.78 J/m²) →
  Cl 결손이 crack의 약점이 되는 점은 우리 halogen 작업 (Cl-coherent termination)에도 시사점

### Reference for our adhesion work
- D'Amore et al. (PCCP 2022, ref 50): (111)/(001)/(110) 평균 surface energy
  0.297/0.344/0.291 J/m² → **fracture = 2γ = 0.60–0.69 J/m²**
- Pustorino 본인 결과는 "더 낮음 (0.20)" — symmetry 깨면서 [PS4]³⁻ 보존한
  cleavage가 더 현실적이라는 주장
- D'Amore PCCP 2022는 우리가 이미 인용한 Sgroi 그룹 후속 paper —
  cross-reference 가능

---

## 6. Electronic (Table 5, Figure 3)

| Slab termination | Bulk gap (eV) | Surface gap (eV) | 메시지 |
|------------------|---------------|------------------|--------|
| Li2S-rich        | 2.33 | 1.76 | mild reduction |
| Li2S-deficient   | 2.33 | 2.31 | bulk-like (insulating) |
| **LiCl-rich**    | 2.16 | **0.58** | ⚠ 큰 폭 감소 — surface metallic 가능성 |
| LiCl-deficient   | 2.16 | 1.99 | mild reduction |

- **LiCl-rich surface bandgap = 0.58 eV** — undercoordinated Cl⁻ 3p가 CBM에 들어옴
- 그러나 excess electrons는 [PS4]³⁻ bulk에 분포, Cl⁻ 주변에 모이지 않음
- → **Li⁰ 환원 일으키지 못함** → "dry crack" 메커니즘 (mechanical 우선)
- LLZO와의 대조: LLZO는 La 주변에 excess e⁻ 모여 Li⁰ 환원 가능 → "wet crack"

### 비교 표 (Table 5)
| SE | G (GPa) | γ (J/m²) | E_red (V) | E_g_bulk (eV) | E_g_surf (eV) |
|----|---------|----------|-----------|---------------|---------------|
| Li2PO2N (LiPON) | 30 | 0.92 | 0.87 | 5.98 | 4.35 |
| β-Li3PS4 | 6 | 0.38 | 1.71 | 2.82 | 2.67 |
| LATP | 58 | 0.88 | 2.16 | 2.36 | 2.20 |
| LLZO | 59 | 1.72 | 0.05 | 4.30 | 2.24 |
| **LPSC (Li2S-def)** | **3.4** | **0.20** | 1.48 | 2.33 | 2.31 |

→ LPSC는 모든 SE 중 G/γ 모두 가장 낮음 = 기계적으로 가장 취약

---

## 7. Filament 메커니즘 분류

### "Dry crack" (LPSC, LPS, this work)
1. Mechanical crack 먼저 열림 (γ 낮음, G 낮음)
2. Crack tip이 anode 직전까지 도달
3. Li⁺가 crack tip 뒤쪽 (anode 쪽) 에서 reduce되어 metal로 채움
4. Li-metal이 crack 뒤를 따라가는 형상 → 실험 (Porz Adv. Energy Mater. 2017,
   Ning Nat. Mater. 2021) 일치

### "Wet crack" (LLZO)
1. γ_LLZO = 1.72 J/m² 높아 mechanical crack 안 일어남
2. 대신 grain boundary / pore surface의 reduced bandgap (2.24 eV) →
   excess e⁻가 La 주변 모임 → Li⁰ 핵형성
3. Li-filament가 anode와 분리된 채로 internal에서 자라남

---

## 8. SI에서 가져온 데이터 (relaxed POSCAR)

SI에 5개 구조의 fully relaxed POSCAR 제공됨 (재사용 가능):
- **24G** (no inv): a=10.249 Å (cubic), V/f.u. = 269.3 Å³
- **24G^inv**: a=10.487, b=9.915, c=9.912 Å (broken cubic), V/f.u. = 257.7 Å³
- **48H** (no inv): a=c=10.065, b=9.808 Å (tetragonal), V/f.u. = 248.4 Å³
- **48H^inv**: a=b=c=10.252 Å (cubic), V/f.u. = 247.5 Å³
- **48H_low**: a=9.948, b=10.274, c=9.951 Å (이름 기준 가장 낮은 E의 48H 변종)

→ **이 5개 POSCAR를 우리 `data/lpscl_baseline_ensemble/`에 보관해두면**
  baseline 구조로 reuse 가능 (안정 ground state 확보)

---

## 9. 우리 워크플로우 액션 아이템

### A. Phase 1 doping pipeline에 반영
1. **`substitute_struct.py`**: `--li_ordering` 옵션 추가 (24G / 48H / 48HR 선택,
   기본 = 48HR — 이 논문의 ground state)
2. **`run_uma_screening.py`**: ensemble 평균 모드 추가
   - 같은 (dopant, conc, comp_label) 조합에서 N=3~5 Li ordering seed로 relax
   - B0/E mean ± std 보고
3. **EOS sweep strain 한계**: 현재 6% (94~106%) → 1% 이내 sub-sweep 추가하거나
   ±6% 결과의 hop artifact 체크

### B. Baseline 정합성
- `data/lpscl_bulk.cif` (mp-985592) 그대로 쓰면 24G_super 상태 = metastable
- **권장**: SI relaxed POSCAR (48HR 또는 48H_low)을 baseline으로 다시 정의
- baseline 변경 시 ΔE/atom 비교 기준 바뀌므로 모든 결과 재계산 필요 (early가 좋음)

### C. Nd-EOS 결과 해석 가이드
- pair01 (rank1) vs pair02 (rank2) B0 차이가 ±50% 안에 들어오면 → **Li ordering
  artifact 가능성 우선 의심**
- 같은 Li ordering에서 두 pair 비교했는지 prep step 검토 필요
- `prepare_dft_eos_nd.py`가 UMA pre-relaxed 구조 이어받으면 Li 위치는 일관됨

### D. Citation pool
이 논문이 우리 향후 paper에서 인용할 핵심 reference:
- "Li ordering can vary B0 by ±50%" — Pustorino 2025 ref
- "(100)-Li2S-deficient surface γ = 0.20 J/m²" — fracture/adhesion benchmark
- "S/Cl inversion 50%, NMR 일치" — disorder treatment 정당화
- "Dry crack vs wet crack" — LPSC vs LLZO 비교 논의

---

## 10. 핵심 인용 (References from this paper 우리한테 유용한 것)

| Ref # | 저자 / 저널 | 내용 | 우리 용도 |
|-------|-------------|------|-----------|
| 17 | Tian PCCP 2019 | LLZO grain boundary excess electrons | LLZO 비교 reference |
| 23 | Morgan Chem Mater 2021 | Mechanistic origin of superionic Li in argyrodite | Li disorder fundamentals |
| 28 | Jeon J Mater Chem A 2024 | Anion disorder governing Li distribution | 최신 LPSCl 시뮬 |
| 30 | Schlenker Chem Mater 2020 | Neutron + PDF + NMR LPSCl structure | 실험 reference |
| 50 | D'Amore PCCP 2022 | Sgroi 그룹 (우리가 이미 알고 있는 paper) | bulk symmetry breaking |
| 51 | Lepley PRB 2013 | LPS structures + interface | LPS parent material |

---

**작성일**: 2026-05-15
**관련 문서**:
- `kb/literature_db/sundar_2025_lpscl_coating.md` (Argonne sibling work)
- `kb/descriptors/coating_descriptor_catalog.md` §7.7 (mechanical descriptors)
- `scripts/doping/run_uma_screening.py` (ensemble 모드 TODO)
