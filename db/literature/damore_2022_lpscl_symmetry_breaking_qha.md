# D'Amore et al. 2022 — LPSCl 대칭 깨짐 (phonon + QHA)

**제목**: From symmetry breaking in the bulk to phase transitions at the
surface: a quantum-mechanical exploration of Li6PS5Cl argyrodite superionic
conductor
**저자**: M. D'Amore*, L. E. Daga, R. Rocca, **M. F. Sgroi** (FIAT CRF),
N. L. Marana, S. M. Casassa, L. Maschio*, **A. M. Ferrari*** (U. Torino)
**저널**: *Phys. Chem. Chem. Phys.* **2022**, *24*, 22978–22986
**DOI**: [10.1039/d2cp03599e](https://pubs.rsc.org/en/content/articlelanding/2022/cp/d2cp03599e)
**라이선스**: CC-BY-NC 3.0 (open access, 재인용 자유)
**관련 PDF (로컬)**: `/root/.claude/uploads/.../bfeaf71f-From_symmeductor.pdf`

---

## 1. 우리에게 왜 중요한가 (TL;DR)

> **F-43m cubic LPSCl (mp-985592 등 Materials Project 디폴트)에는
> imaginary phonon mode가 두 개 있다 (−146, −115 cm⁻¹) — 즉 0K에서
> dynamic instability.** 진짜 ground state는 monoclinic Pm (Model 4)이고,
> Model 2 pseudo-cubic 대비 −0.310 eV/f.u. 더 안정.

### Pustorino 2025와의 정합성
- Pustorino: 정적 DFT relaxation으로 48HR 확인 (ΔE = −0.80 eV/f.u. vs 24G)
- D'Amore: 동적 phonon 분석으로 imaginary mode → 24 pseudo-cubic + 1 monoclinic 확인
- **두 논문이 다른 방법으로 같은 메시지** → 단일 cubic relax는 잘못된 baseline

### 추가 핵심 정보 (Pustorino에는 없는 것)
1. **PBE0 hybrid functional + TZVP** — VASP/PBE 대비 더 정확한 reference
2. **B0(T) 직접 계산 (QHA)** — 100~400 K, 0/0.093 GPa 둘 다
3. **monoclinic이 pseudo-cubic보다 stiffer** (B0 ~26 vs ~18 GPa @ 298K)
4. **열팽창계수 α(298K) = 6.55×10⁻⁵ K⁻¹** — perovskite/garnet의 ~2배 (battery
   thermal cycling 시 실측 변동의 1차 reference)
5. **Surface energy (111)/(001)/(110) = 0.297/0.344/0.291 J/m²** — Pustorino의
   (100)-Li2S-def 0.20 J/m²와 다른 cleavage 비교

---

## 2. Methods 요약

### CRYSTAL (≠ VASP) — local Gaussian basis
| 항목 | 값 |
|------|-----|
| Code | CRYSTAL (Dovesi 그룹) |
| XC | **PBE0 hybrid** (25% exact exchange) |
| Basis | TZVP (Ahlrichs split-valence triple-ζ + polarization), Li/P/S/Cl 모두 |
| Coulomb/Exchange truncation T1–T5 | 8, 8, 8, 16, 20 |
| SCF conv. (relax) | 10⁻⁸ Hartree |
| SCF conv. (phonon) | 10⁻¹⁰ Hartree |
| DFT integration | Becke grid, 75 radial × 974 angular |
| Bulk supercell (thermal) | **2×2×2 = 104 atoms** |
| K-points (high-sym) | 8 along each vector → 29 irreducible |
| K-points (low-sym P1) | 260 |
| Phonon | Direct space, harmonic Hessian, 2×2×2 supercell |
| QHA | 6 volumes (V0 ± 8%), Helmholtz F(V,T) minimize |
| Pressure points | 0 GPa, 0.093 GPa (battery operation) |
| Temperature range | 100–400 K |
| Elastic | Stress-strain, Voigt-Reuss-Hill averaging |

### Surface energy 식
$$E_{\text{Surf}}^{(n)} = \frac{E_n^S - n E^b}{2A}$$

n-layer slab, 2A 분모는 양면 대칭 — Pustorino의 fracture energy γ = 2 × E_surf 와
factor 2 차이. Pustorino도 동일 정의.

---

## 3. ⭐ Bulk Models — 4가지 (Table 2)

| Model | 공간군 | a (Å) | b (Å) | c (Å) | α | β | γ | Li 위치 | 안정성 |
|-------|--------|-------|-------|-------|---|---|---|---------|--------|
| **1** | F-43m | 10.254 | 10.254 | 10.254 | 90 | 90 | 90 | (1/4, 1/4, 1/4) all 24g | ⚠ **metastable, imag phonons** |
| **2** | P1 | 9.963 | 10.051 | 10.013 | 87.9 | 89.0 | 86.8 | (3/4, 3/4, 3/4) ≈ 48h | stable (24 degenerate) |
| 3 | P1_8h | 10.043 | 10.013 | 9.957 | 90.9 | 93.1 | 87.9 | (1/2, 1/2, 1/2) | stable, ≈ Model 2 |
| **4** | **Pm** | 9.777 | 9.777 | 10.698 | 90 | 90 | 92.4 | (0.316, 0.316, −0.023) | ⭐ **GROUND STATE** |

### 핵심 결과
1. **Model 1 (Materials Project 디폴트 = F-43m)에 imaginary phonon mode 2개**:
   - F1 symmetry: −146 cm⁻¹ (3-fold degenerate)
   - F2 symmetry: −115 cm⁻¹ (3-fold degenerate)
2. F1, F2 mode 따라 normal coordinate scan → double-well potential 확인
3. 24개의 pseudo-cubic structure (P1, ΔE 차이 10⁻⁵ eV/f.u. 미만)이 등장
4. 이들은 평균하면 cubic 복구 (= 실험 X-ray cubic은 dynamic average)
5. **Model 2 (pseudo-cubic)는 Model 1보다 −0.831 eV/f.u. 더 안정** (≈64 meV/atom)
6. **Model 4 (monoclinic)는 Model 2보다 −0.310 eV/f.u. 더 안정** → Carrasco et al.
   (ref 26)이 이미 보고했던 monoclinic 변종과 일치
7. PSȢ 사면체는 모든 모델에서 보존 (rigid building block)

### Pustorino 2025와 Model 매핑
| D'Amore | Pustorino | 메모 |
|---------|-----------|------|
| Model 1 (F-43m, 24g) | 24G_super | 둘 다 metastable |
| Model 2 (P1 pseudo-cubic, ~48h) | 48H 또는 48H_low | 둘 다 안정 |
| Model 4 (Pm monoclinic) | (없음) | Pustorino는 monoclinic은 안 다룸 |
| (없음) | 48HR^inv | D'Amore는 S/Cl inversion 미고려 |

→ 두 논문 합치면 **(monoclinic + 48HR + S/Cl 50% inv) 모두 고려한 ensemble**이
완성됨. 우리는 이 cross-product를 baseline ensemble로 만들 수 있음.

---

## 4. ⭐ Elastic Moduli (Table 3)

### Pseudo-cubic Model 2 (PBE0/TZVP, 0K)

| Quantity | Reuss | Voigt | **Hill** |
|----------|-------|-------|----------|
| B (GPa)  | 16.05 | 21.36 | **18.71** |
| G (GPa)  | 11.29 | 13.69 | **12.49** |
| E (GPa)  | — | — | **30.65** |
| ν        | — | — | **0.227** |
| G/B      | — | — | **0.667** (brittle, anti-perovskite-like) |

### B0(T) 그래프 (Fig 4)
- **Pseudo-cubic Model 2 @ 0 GPa**: 18.5 GPa (100K) → 17.5 GPa (400K)
- **Pseudo-cubic Model 2 @ 0.093 GPa**: ≈ 동일 (압력 미세 영향)
- **Monoclinic Model 4 @ 0 GPa**: ≈ **26 GPa (100K) → 23.5 GPa (400K)** ⭐

### 메시지
- **monoclinic이 pseudo-cubic보다 ~5–7 GPa stiffer** (~30% 차이)
- 즉 "어느 polymorph를 baseline으로 쓰느냐"에 따라 B0가 달라짐
- 사이클링 중 monoclinic ↔ pseudo-cubic 전이 가능성 → 균열 유발 가능 추정
- G/B = 0.667 → "antiperovskite (~0.7)에 가까움" → **intrinsically brittle**
- Compared to Li3PS4 (PBE0sol): B=23.3, G=11.4, E=29.5 GPa → **LPSCl ≈ Li3PS4 with
  slightly lower B, similar G/E** (LPS는 LPSCl의 부모 구조)

### 우리 작업 함의
- 같은 LPSCl인데 Pustorino 24G vs 48H vs 48HR^inv = B0 14~30 GPa 분산
- 거기에 D'Amore monoclinic vs pseudo-cubic = +5~7 GPa 추가 분산
- → **단일 baseline 구조의 B0 절댓값에 의존하지 말고, 같은 polymorph 내 상대
  비교에 집중하자** (dopant A vs B, halogen Cl vs Br 등)

---

## 5. Thermal Expansion (Fig 3)

### 298 K 값
- **α(298K, 0 GPa) = 6.5481×10⁻⁵ K⁻¹** (pseudo-cubic Model 2)
- α(400K, 0 GPa) = 7.39×10⁻⁵ K⁻¹
- α(400K, 0.093 GPa) = 7.24×10⁻⁵ K⁻¹

### 비교
| Material | α (10⁻⁵ K⁻¹) |
|----------|---------------|
| LPSCl (Model 2, 298K) | **6.55** |
| Perovskite (typical) | 3.6 |
| Fluorite (typical) | 3.1 |
| LSGM (oxide ion conductor) | 3.1 |

→ **LPSCl은 oxide 대비 ~2× 큰 열팽창** (PSȢ tetrahedron 회전 + Li hopping
결합 효과). Battery cycling 시 thermal mismatch에 취약.

→ 우리 SE/NCM coating work에서 **CTE mismatch가 adhesion 손상의 주요 origin**일 수
있다는 점 추가 시사.

### 격자 상수 비율
- V(400K) / V(298.3K) = 1.007 (battery 작동 범위 내, 7‰ expansion)
- 작은 monoclinic 격자 변동도 보고됨 (Fig 3 magenta)

---

## 6. Surface Properties (Table 4 + Fig 6,7,8)

### Average surface energy (E_S, Eq. 2 정의)
| Surface | E_S (J/m²) | Wulff 점유 |
|---------|------------|-----------|
| (1 1 1) | **0.297** | 10.8% |
| (0 0 1) | **0.344** | 8.1% |
| (1 1 0) | **0.291** | **81.1%** ⭐ |

### 메시지
- **(110)이 가장 안정 + Wulff에서 81% 점유** (dominant facet)
- Bulk 1차 정의: fracture energy = 2 × E_S → (110): **0.58 J/m²**
- **(111), (001)은 비대칭 termination**: top은 PSȢ, bottom은 Li2S/LiCl mixed layer
- 실험 XPS 160.5 eV doublet → Li2S 잔존 일치 (Janek 그룹 ref 53)
- (110)은 β-Li3PS4 (110) facet과 local arrangement 동일
- Surface 비대칭 (top/bottom 다름) → electric field at electrode interface

### Pustorino 2025와 비교
| Surface | D'Amore (J/m²) γ=E_S | Pustorino (J/m²) γ=2E_S |
|---------|----------------------|--------------------------|
| (111) | 0.297 (E_S), 2γ ≈ 0.594 | — |
| (001)/(100) Li2S-rich | 0.344 (E_S), 2γ ≈ 0.69 | 0.74–0.78 (fracture) |
| (001)/(100) Li2S-def | (없음) | **0.20** (fracture) ⭐ |
| (110) | 0.291 (E_S), 2γ ≈ 0.58 | 0.37 (fracture) |

→ **Pustorino가 (100)-Li2S-deficient = 0.20 J/m²로 D'Amore 대비 1/3** 보고. 차이는
대칭 vs 비대칭 cleavage 정의 + Li 분포 (48HR vs Model 2). Pustorino 본문에서 직접
지적: D'Amore 값이 자기네보다 큼은 PSȢ 보존 cleavage를 안 했기 때문.

### Electrostatic potential (Fig 7)
- (111), (001) top: PSȢ → 음전위 (적색)
- (111), (001) bottom: Li⁺/Cl⁻ → 양전위/orange
- (110): 양면 모두 PSȢ + Li2S — 비교적 대칭
- → **(111)/(001) interface가 electrode와 electric polarization 큼**

---

## 7. 핵심 인사이트 (논문 결론 직접 인용 요약)

1. **F-43m cubic LPSCl은 metastable** — phonon 분석이 가장 직접적 증거
2. Pseudo-cubic Model 2 (24개의 P1) 또는 monoclinic Model 4 (Pm)가 진짜 안정상
3. Static lattice modeling은 polycrystalline 실측과 잘 부합 (PBE0)
4. **G/B ≈ 0.67 → 본질적으로 brittle** (anti-perovskite와 유사)
5. (111), (001), (110) 세 facet이 dominant; (110)이 81% Wulff 점유
6. (111), (001)에서 Li2S/LiCl 표면 분리 → **incipient phase separation = SEI 전구체**
7. 사이클링 중 monoclinic ↔ cubic 전이가 fracture 유발 가능성

---

## 8. 우리 워크플로우 액션 아이템

### A. Pustorino DB와 합쳐서 통합 baseline ensemble 만들기
다음 6개 baseline 후보 (cross-product):
1. F-43m (24G) — Pustorino 정의, 비교용 (의도적 metastable)
2. Pseudo-cubic P1 (Model 2 = D'Amore) — 24개 평균
3. Monoclinic Pm (Model 4 = D'Amore) — true ground state
4. 48H (Pustorino) — 48h 우세, no inversion
5. 48HR (Pustorino, 50% 점유) — Pustorino 정의 ground state
6. 48HR^inv (Pustorino, S/Cl 50% inv) — 실험 NMR 일치

→ **각 baseline에서 같은 dopant/concentration으로 EOS 돌려보면 dopant 효과 vs
   polymorph 효과 분리 가능**. 처음엔 비싸지만 한 번만 하면 됨.

### B. 열팽창 효과 반영
- 우리 EOS sweep은 0 K static. 실제 cell 작동 (~298 K, 사이클링 ~330 K)
  보정에 α(298K) = 6.55×10⁻⁵ K⁻¹ 사용 가능
- ΔV/V0 결과를 0K → 298K 변환: ΔV ≈ 3α·ΔT × V0 ≈ 5.9×10⁻³ (0.6%)
  → 우리 ±6% volume sweep 대비 작음, 보정 무시 가능 수준
- 그러나 NCM 캐소드 (α ~ 1×10⁻⁵)와의 mismatch는 **6× 차이** → adhesion crack의
  중요 driver

### C. Surface energy 모델 검증
- 우리가 Cl-coherent termination 사용했던 v2 paper의 surface energy를
  D'Amore (110) E_S = 0.291 J/m²와 sanity check
- (110)이 dominant이므로 우리 슬랩도 (110) 우선이어야 함
  (현재 (001)/(100) 위주면 비대칭 termination artifact 있을 수 있음)

### D. PBE0 vs PBE 비교 데이터
- D'Amore PBE0 (정확): B(Hill) = 18.7 GPa, G = 12.5 GPa
- Pustorino PBE 24G: B = 29.6 GPa, G = 10.3 GPa
- → **PBE0이 PBE 대비 더 soft하게 예측** (PBE0의 일반적 경향)
- 우리 UMA-s-1p1 (PBE 학습)이 24~30 GPa 정도 나오면 OK; 18~20 GPa는 polymorph
  차이까지 포함한 것

### E. Citation pool — 향후 paper에서
- "F-43m LPSCl is dynamically unstable (imaginary phonons at −146, −115 cm⁻¹)" —
  D'Amore PCCP 2022 ref
- "Monoclinic Pm is true ground state, 0.310 eV/f.u. below pseudo-cubic" — same ref
- "α_LPSCl = 6.55×10⁻⁵ K⁻¹ at 298K, ~2× larger than oxide conductors" — same ref
- "(110) facet dominates Wulff (81%)" — same ref
- "G/B = 0.667 indicates anti-perovskite-like brittleness" — same ref

---

## 9. Literature 핵심 (D'Amore 본문에서 우리한테 유용한 reference)

| Ref # | 저자 / 저널 | 내용 | 우리 용도 |
|-------|-------------|------|-----------|
| 17 | Adv. Appl. Energy 2021 (Sgroi 공저) | Sulfide SE 종합 리뷰 | reference |
| 26 | Schlenker Chem Mater 2020 | NMR + neutron monoclinic 변종 | 실험 reference |
| 47 | Wang, Shao J Mater Chem A 2017 | USPEX로 LPSCl P1 stable 확인 | independent confirmation |
| 48 | Carrasco ACS AMI 2021 | Cubic LPSCl metastable 언급 | sister work |
| 50 | (lit ref in Table 3) | LPSCl B=28.7, G=8.1, E=22.1 (PBE) | PBE 비교값 |
| 51 | Pugh 1954 | Pugh ratio brittleness 정의 | 인용 |
| 56 | Lepley PRB 2013 | β-Li3PS4 surface (100), γ=0.32 J/m² | parent material |

---

## 10. Pustorino 2025 ↔ D'Amore 2022 통합 메시지 (우리 paper 주장에 그대로 사용 가능)

> "LPSCl의 elastic property는 두 종류의 분산을 갖는다:
> (1) **Polymorph 분산** (D'Amore): F-43m metastable vs P1 pseudo-cubic vs Pm
>     monoclinic — B0가 18.5 ~ 26 GPa 사이 변동
> (2) **Li site disorder + S/Cl inversion 분산** (Pustorino): 같은 polymorph 내에서도
>     B0가 13.7 ~ 29.6 GPa 변동
> 따라서 dopant 효과를 정량 평가하려면 (i) baseline polymorph 고정, (ii) 같은 Li
> ordering ensemble 내에서 비교, (iii) ensemble 평균 ± 표준편차 보고가 필수다."

---

**작성일**: 2026-05-15
**관련 문서**:
- `kb/literature_db/pustorino_2025_lpscl_li_ordering_mechanical.md` (Brown sister work)
- `kb/literature_db/sundar_2025_lpscl_coating.md` (Argonne coating screening)
- `kb/descriptors/coating_descriptor_catalog.md` §7.7 (mechanical descriptors)
