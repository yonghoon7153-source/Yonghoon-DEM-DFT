# B2O3 Doping in LPSCl1.6 (BO-LPSC) — Chemistry Framework

**작성일**: 2026-05-19
**상태**: pre-enumeration design doc, awaiting lpscl16_verify champion
**대상**: paper #2 (BO-LPSC1.6, follow-up to paper #1 modelC family)

---

## 1. Question — B-at-P substitution은 정당한가?

User paper #2 Figure 1b는 "BO incorporation into the argyrodite framework"로
**B at 4b (P site) + O at 16e (PS4 corner S site)** 명시.

이 doping mechanism이 literature-supportable한지 확인.

---

## 2. Literature evidence — B-at-P substitution

### 2.1 Direct precedent: β-Li3PS4-B (sulfide system, 가장 가까운 analog)

US Patent 9142861 (Lithium ionic conductor, Li-P-B-S):
- Composition: **Li_{3+3/4x} B_x P_{1-3/4x} S4** (0.2 ≤ x ≤ 1.0)
- Crystal structure: β-Li3PS4 (orthorhombic Pnma)
- BS4 and PS4 tetrahedra coexist at 4b positions
- Charge compensation: 0.75 Li interstitial per B substitution
  (B³⁺ at P⁵⁺ → -2 acceptor; partial substitution averages to 0.75)

### 2.2 Si-analog argyrodite (Morscher 2024, 2022)

**Sulfide**: Li6+xP1-xSixS5Br ([PMC10911230](https://pmc.ncbi.nlm.nih.gov/articles/PMC10911230/))
- Si⁴⁺ at P⁵⁺ 4b site (confirmed XRD/NMR Rietveld)
- 1 Li interstitial per Si (acceptor +1)
- σ_Li enhanced by Li disorder

**Oxide**: Li6+xP1-xSixO5Cl ([JACS 2022](https://pubs.acs.org/doi/10.1021/jacs.2c09863))
- Full oxide argyrodite (all S → O)
- Si at P + O at S simultaneously
- σ_Li = 1.82×10⁻⁶ S/cm at x=0.75 (3 orders better than prior oxide argyrodites)
- 4 Li site disorder unlocked (T5, T5a, T3, T4 all partially occupied)

### 2.3 NASICON-type B@P (oxide phosphates, less direct but supportive)

**LATP + B2O3** ([RJIC 2024](https://link.springer.com/article/10.1134/S0036023624603271)):
- Li1.2Al0.2Zr0.1Ti1.7(PO4)3 + 2% B2O3 → σ = 2.9×10⁻⁴ S/cm (highest)
- **B2O3 precursor → P substitution** (direct relevance to user's chemistry)

**Na-V phosphate** ([PMC5157167](https://pmc.ncbi.nlm.nih.gov/articles/PMC5157167/)):
- Na3V2(P1-xBxO4)3 — B at P site with charge compensation
- Demonstrates aliovalent B substitution at P in phosphate framework

### 2.4 BS4 tetrahedral unit in Li2S-B2S3 glass (chemistry support)

- Raman 495 cm⁻¹ peak assigned to BS4 ([Sakai 1994](https://www.sciencedirect.com/science/article/abs/pii/0022309394900345))
- B prefers tetrahedral (sp³) coordination in sulfide environment
- B-S bond length 1.93 Å (typical)
- → B at tetrahedral P site (4b, PS4 framework) chemically natural

### 2.5 Control: B at Cl site (alternative mechanism, also literature-confirmed)

- LiBH4 (borohydride) doping: BH4⁻ at Cl⁻ 4d site
- [Wang 2025 Adv Mater](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202506095) — anion substitution mechanism
- [Hu 2022 ACS AEM](https://pubs.acs.org/doi/10.1021/acsaem.1c02892) — Li6PS5Cl1-x(BH4)x
- σ_Li 0.12 mS/cm at x=0.1

**Note**: BH4 ≠ B³⁺. BH4 is molecular anion (B-H bonded unit), behaves as halide
analog. Our B2O3 precursor releases **bare B³⁺**, which prefers cation site.

---

## 3. Conclusion — B-at-P for argyrodite-Cl

| Question | Answer | Evidence strength |
|---|---|---|
| B³⁺ can substitute P⁵⁺ tetrahedrally? | **YES** | β-Li3PS4-B + Si-analog + NASICON + BS4 glass |
| In argyrodite framework specifically? | **PLAUSIBLE, novel for Cl-argyrodite** | Si-analog (S5Br + O5Cl) but no B-specific Cl-argyrodite paper |
| Charge compensation mechanism? | **Li interstitial OR vacancy-fill** (LPSCl1.6 has 0.6 vac/fu pre-existing) | β-Li3PS4-B + Morscher Si analog |
| Alternative B at Cl site? | Possible (BH4-style) but for B2O3 precursor unlikely (bare B³⁺ ≠ BH4⁻ molecular) | Wang 2025 LiBH4 paper |

**Verdict**: B-at-P in argyrodite-Cl is chemistry-supportable, novel mechanism
building on solid analog precedents. Paper #2의 핵심 claim으로 promotable.

---

## 4. Key insight — pre-existing vacancy advantage

**LPSCl1.6's Li5.4 stoichiometry (0.6 Li vacancy per fu) is advantageous for
B2O3 doping** vs Si@P Morscher (Li6 base, no vacancy).

### 4.1 Charge accounting per 1 B2O3 unit (10 fu cell, 124 atoms)

Pre-doping modelC × 1×1×2: Li54 P10 S44 Cl16
- Stoichiometric Li6PS5Cl × 10 fu = Li60 P10 S50 Cl10
- LPSCl1.6 has 6 S → 6 Cl (halogen-rich) + 6 Li vacancies (charge balance)

Add 1 B2O3 unit:
- 2 P → 2 B at 4b: -4 charge (acceptor)
- 3 S → 3 O at 16e: 0 charge (isovalent)
- **Need +4 → fill 4 of 6 existing Li vacancies**
- No true Li interstitial needed!

Post-doping: **Li58 P8 B2 S41 O3 Cl16** (2 Li vacancies remaining)
- Per fu: Li5.8 P0.8 B0.2 S4.1 O0.3 Cl1.6

### 4.2 Why this is better than Morscher Si@P (Li6 base)

Morscher Li6+xP1-xSixS5Br must create true Li interstitials at non-host positions
(T5, T3, T4 sites — generally higher-energy positions). This raises:
- Synthesis difficulty (kinetic barrier for Li insertion)
- Reviewer concern about structural validity (where exactly is interstitial Li?)

LPSCl1.6 avoids this entirely: existing 4a/4d/24g vacancies absorb the extra Li.

**Paper #2 selling point**:
> "The Cl-rich Li5.4 stoichiometry of modelC provides natural sites for charge
> compensation under aliovalent acceptor doping, removing the need for
> high-energy Li interstitial positions required in Li6 baseline materials."

---

## 5. Doping site enumeration — physically-ordered hierarchical strategy

**Design principle**: enumerate the most-perturbing site first, let downstream
sites adapt. Ordering: **B (largest perturbation) → halogen (medium) → O (local)
→ Li (smallest, charge-comp)**.

User's insight (2026-05-19): B 박은 후 주변 S/Cl 재배치가 physically natural
— lpscl16 champion의 halogen 그대로 쓰는 것보다 정확. 단점은 enumeration scope
가 커짐 → pymatgen + enumlib symmetry reduction으로 해결.

### 5.1 Per-axis combinatorial scope (10 fu cell, no symmetry)

| Site | Sites | Choose | C(n,k) |
|---|---|---|---|
| B at P (4b) | 10 | 2 | **45** |
| Halogen (4a/4d free) — 4 S + 16 Cl among 20 sites | 20 | 4 | **4,845** |
| O at S (PS4 corner 16e or free) | 44 | 3 | **13,244** |
| Li fill (existing vacancies) | 6 | 4 | **15** |
| **Full product** | | | **~43 billion** |

### 5.2 Symmetry reduction (pymatgen + enumlib)

modelC R-3 (rhombohedral) symmetry + 1×1×2 supercell:
- Point ops: 6 (E, 2C3, i, 2S6)
- Translation: 2 (z-axis)
- Combined: ~12-18 operations

Expected reduction (orbit-averaged, conservative):
| Axis | Full | Sym-reduced | Reduction |
|---|---|---|---|
| B pair | 45 | ~8 | ~5× |
| Halogen (4 S / 16 Cl) | 4,845 | ~400-600 | ~10× |
| **B + halogen co-enumerate** | 218,025 | **~5,000** | ~40× |
| O placement (after B/halogen fixed; local sym lower) | 13,244 | ~3,000-4,000 | ~3-4× |
| Li fill (after B/halogen/O fixed; very low sym) | 15 | ~5-8 | ~2-3× |

Engine: `pymatgen.transformations.advanced_transformations.EnumerateStructureTransformation`
(uses enumlib's Hart-Forcade algorithm). Requires `enumlib` install (pip).

### 5.3 Hierarchical stages (with pymatgen sym reduction)

| Stage | Logic | Configs (sym-reduced) | Time (1 GPU) |
|---|---|---|---|
| **1a — B + halogen co-enumerate** | enumerate 2 B at P + 4 S among 20 free sites simultaneously | ~5,000 unique | ~1.5h SCF |
| **1b — Top 10 × O enumerate (1 representative Li each)** | for each of top 10 (B, halogen), enumerate 3 O at C(44,3) positions, sym-reduced | 10 × 3,500 ≈ 35,000 | ~10h SCF |
| **1c — Top 100 × all Li fills** | enumerate C(6,4) = 15 Li patterns, sym-reduced (~7 per) | 100 × 7 ≈ 700 | ~12 min SCF |
| **2 — Top 30 LBFGS relax** | fmax 0.05, cell + atoms free | 30 | ~2.5h |
| **3 — Top 5 MD anneal** | Langevin 500 K × 100 ps + 300 K cool × 10 ps + LBFGS final | 5 | ~3h |
| **Total** | | | **~17h on 1× A100** |

**Choice of "top 10" for Stage 1b** (paper-grade safe): if energy spread among
top 5 B-halogen patterns is small (~kT), top 5 might miss the true ground state.
Top 10 covers ~2× more of the favorable manifold.

### 5.4 Stage 1c "1 representative Li" choice rule (for Stage 1b)

To avoid 15× cost in Stage 1b, pick 1 Li fill pattern. Rule:
- Compute Bader basin centers for B, O atoms (after substitution)
- 4 closest Li vacancies (= largest electrostatic attractor) → fill these
- Heuristic, but biased toward physically reasonable starting point
- Stage 1c then enumerates all 15 patterns to identify true champion Li fill

### 5.5 Stage 3 anneal — captures halogen secondary redistribution

MD anneal at 500 K for 100 ps allows Li hops (barrier ~0.2 eV) and Cl/S free-site
hops (barrier ~0.3-0.5 eV). At 500 K kT = 43 meV → Boltzmann factor ~10⁻⁵ per
hop attempt → ~1-10 successful hops per 100 ps per atom → halogen rearrangement
captured even if Stage 1a missed the optimal pattern.

### 5.6 pymatgen implementation sketch

```python
from pymatgen.core import Structure
from pymatgen.transformations.advanced_transformations import (
    EnumerateStructureTransformation,
)
from pymatgen.transformations.site_transformations import (
    ReplaceSiteSpeciesTransformation,
)

# Load lpscl16_verify champion (62-atom primitive)
struct = Structure.from_file("lpscl16_champion.cif")
struct = struct * (1, 1, 2)  # 124 atoms, 10 fu

# Identify site groups
p_sites = [i for i, s in enumerate(struct) if s.specie.symbol == "P"]  # 10
free_anion_sites = identify_free_4a4d(struct)  # 20 sites (currently 4 S + 16 Cl in modelC)
ps4_corner_S_sites = identify_ps4_corners(struct)  # 40 sites

# === Stage 1a: B + halogen co-enumerate ===
# Set fractional occupancy on disorder sites
struct_1a = struct.copy()
for i in p_sites:
    struct_1a[i] = {"P": 0.8, "B": 0.2}  # 2 B / 10 P
for i in free_anion_sites:
    struct_1a[i] = {"Cl": 0.8, "S": 0.2}  # 4 S / 20 free sites

enum_1a = EnumerateStructureTransformation(
    min_cell_size=1, max_cell_size=1,
    enum_precision_parameter=1e-3,
)
unique_1a = enum_1a.apply_transformation(struct_1a, return_ranked_list=10_000)
# Expected: ~3,000-6,000 unique configs

# SCF each → rank → top 10
# ...

# === Stage 1b: top 10 × O enumerate ===
for top_struct in unique_1a[:10]:
    # Add representative Li fill (Bader proximity heuristic)
    top_with_Li = add_representative_Li(top_struct)
    # Disorder O at PS4 corner S
    for i in find_ps4_corners(top_with_Li):
        top_with_Li[i] = {"S": 41/44, "O": 3/44}

    enum_1b = EnumerateStructureTransformation(...)
    o_configs = enum_1b.apply_transformation(top_with_Li, return_ranked_list=5_000)
    # Expected: ~3,000-4,000 unique per top-pattern
    # SCF each

# === Stage 1c, 2, 3: as above ===
```

### 5.7 ★ UPGRADED protocol (2026-06-05) — Ewald joint pre-rank

§5.3의 sequential hierarchical(B→halogen→O→Li, 각 단계 "대표 Li 1개")은 작동하지만
**두 가지 정확도 risk**가 있어 paper-grade ground-state 탐색엔 부족:

1. **Li-ordering noise 오염**: Li spread = **1162 meV**(본 그룹 측정) ≫ B/halogen/O config 간
   에너지차(수십~수백 meV) → "대표 Li 1개" 고정 시 ranking이 Li noise에 묻혀 top-N 컷에서
   진짜 ground state 누락 위험.
2. **Sequential greedy → coupled minimum 누락**: B 위치를 O·Li 모르고 1a에서 확정하나,
   **B-O coupling**(BO₄ 형성) + **acceptor-vacancy association**(채울 Li⁺ 공공이 B³⁺ 음전하
   근처로 끌림)이 강하게 coupled → greedy가 미리 자르면 정보 손실.
3. (부차) **UMA가 B/O 화학에 약함**: oc20/omat 학습엔 mixed BOₓS₄₋ₓ 사면체·B-S 결합 희소
   → ranking systematic bias 가능 → top-5만 DFT 검증은 위험.

**해결 = Ewald 정전기 joint pre-rank** (이온 site-ordering은 장거리 정전기 지배 → point-charge
Ewald가 ms/config로 coupling을 rigorous하게 잡음, 표준 기법):

| 단계 | 방법 | 목적 |
|---|---|---|
| **Stage 0 (신규)** | B@P + halogen(S/Cl) + O@S + Li-fill을 **joint**로 구성 → **Ewald 에너지 전체 ranking** → top ~300 | greedy·Li-noise·B-O coupling·acceptor-vacancy를 한 번에 (cheap) |
| Stage 1 | Ewald top-300 → **UMA relax** → top-30 | MLIP은 정전기-검증된 상위만 (config 폭발 회피, UMA 시간 ↓) |
| Stage 2 | UMA top-30 → **DFT SCF** (top-5 아님!) | UMA의 B/O 부정확 방어 — 넓게 검증 |
| Stage 3 | DFT top-5 → relax + 500K anneal | 최종 ground state |
| **별도** | **BO₄ vs O-distributed를 motif family로 명시 구성·비교** | 핵심 물리(O 군집 여부)를 enumeration 운에 안 맡기고 직접 결론 |

**구현 메모** (`tools/doping/b2o3_enumerate.py`):
- Ewald는 **전하 다른 DOF만** ranking (B@P +3/+5, halogen S²⁻/Cl⁻, Li-fill +1). **O는 isovalent
  (O²⁻=S²⁻ 전하 동일) → Ewald-blind** → O는 BO₄/distributed/free_s **motif로 생성**해 UMA/DFT가
  공유결합성으로 판가름.
- random sampling은 joint 공간(~1e14)에 부족 → **B(C(10,2)=45) × halogen(C(20,4)=4845) 전수
  enumerate + Li는 greedy 정전기 최적배치**(acceptor-vacancy association + Li-Li 반발 정확 반영).
  218k base config, 각 Ewald = q·M·q (geometric kernel M 1회 precompute).
- **Li-vacancy 후보 = spglib 대칭완성** (깨끗한 ~66 자리). spglib 없으면 void-finder fallback(과생성,
  부정확) → **v100에선 spglib 필수**.
- 모든 config 중립(B −4 ↔ +4 Li) → Ewald 배경항 불필요. config-key 정확 dedup.

**비용**: Ewald pre-rank 수만 config = 분 단위. UMA를 5000개 다 도는 대신 top-300만 → UMA 시간
오히려 ↓. DFT를 top-30으로 넓힌 게 유일한 순증(~3-5h). **정확도/robustness ↑↑, reviewer
방어(greedy/Li-ordering 질문) 차단.**

**Charge accounting (중립성, 10 fu / 124-atom 1×1×2 cell)**:
- base modelC×(1,1,2) = Li54 P10 S44 Cl16 (중립 ✓)
- 2 P→2 B: −4 (acceptor) / 3 S→3 O: 0 (isovalent) / free-site S↔Cl 재배열: 0 (개수 보존)
- → **+4 Li**(공공 6개 중 4개 채움) → **Li58 P8 B2 S41 O3 Cl16** (중립 ✓, 공공 2개 잔존)

---

## 6. Computational checklist before script generation

- [x] Literature confirms B-at-P chemistry
- [x] Si-analog precedent (Morscher 2024) verified
- [x] Charge balance accounting (vacancy-fill mode) derived
- [x] Enumeration scope (43B configs full → ~5K via pymatgen sym reduction at Stage 1a)
- [x] Hierarchical stages 1a/1b/1c/2/3 designed (~17h on 1× A100)
- [x] B (largest perturbation) → halogen (medium) → O (local) → Li ordering
- [x] **UPGRADED protocol (§5.7)**: Ewald joint pre-rank → UMA top-300 → DFT top-30 → anneal
- [x] **lpscl16 champion ready** = `db/structures/modelc_V0_k663.xyz` (62-atom, k663 V0, PS4 intact,
      rhombohedral a=b=7.007 c=35.036; modelc_v3 paper structure). 1×1×2 → 124 atoms.
- [x] B2O3 enumerate Stage-0 script = `tools/doping/b2o3_enumerate.py` (joint Ewald pre-rank)
- [ ] v100에 pymatgen 설치 확인 (`python3 -c "import pymatgen"`) — enumlib는 선택(stochastic+Ewald는 불필요)
- [ ] Stage 0 실행 (v100) → top-300 → Stage 1 UMA relax
- [ ] DFT settings for B-doped LPSCl (Nd-doped와 동일하나 B는 f-전자 없어 ISPIN/U 불필요)

---

## 7. References

- US Patent 9142861 — Lithium ionic conductor (Li-P-B-S, β-Li3PS4-B)
- Morscher et al., JACS 2022, 144:23, [10.1021/jacs.2c09863](https://pubs.acs.org/doi/10.1021/jacs.2c09863) — Li7SiO5Cl oxide argyrodite
- Morscher et al., Adv. Energy Mater. 2024, [PMC10911230](https://pmc.ncbi.nlm.nih.gov/articles/PMC10911230/) — Li6+xP1-xSixS5Br sulfide argyrodite
- Wang et al., Adv. Mater. 2025, [10.1002/adma.202506095](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202506095) — LiBH4-LPSCl (Cl site, not P)
- Hu et al., ACS Appl. Energy Mater. 2022, [10.1021/acsaem.1c02892](https://pubs.acs.org/doi/10.1021/acsaem.1c02892) — Li6PS5Cl1-x(BH4)x
- Sakai et al., J. Non-Cryst. Solids 1994 — Li2S-B2S3 glass BS4 Raman
- Russ. J. Inorg. Chem. 2024 — LATP + B2O3 conductivity
- PMC5157167 — Na3V2(P1-xBxO4)3 cathode

---

## 변경 이력

| 날짜 | 변경 | 출처 |
|---|---|---|
| 2026-05-19 | v1 초안 (literature search + chemistry framework) | this session |
| 2026-06-05 | §5.7 UPGRADED protocol (Ewald joint pre-rank + DFT top-30 + BO₄ motif), §6 checklist 갱신 (champion=modelc_V0_k663, script 생성), 웹검색 재확인 (B@P novel-but-supportable) | this session |
| (TODO) | Stage 0 실행 결과 후 ground-state 구조 §5 update | future |
