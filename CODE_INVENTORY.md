# 🚨 필독 — CODE INVENTORY (master catalog)
# 🚨 필독 — CODE INVENTORY (master catalog)
# 🚨 필독 — CODE INVENTORY (master catalog)

> [!error] CRITICAL RULE FOR CLAUDE — ==이 파일이 모든 code 작업의 1순위 reference==
> 1. **이 파일을 가장 먼저 읽는다** — 모든 code-related 작업 전에.
> 2. **새 script 생성 금지** — 기존 verified script만 사용.
> 3. inventory에 없으면 **사용자에게 위치 묻기** — 추측/생성 금지.
> 4. 절대 "내가 짜드릴게요" / "비슷한 거 만들게요" 같은 응답 금지.
> 5. 의심되는 결과 나오면 즉시 inventory 확인하고 사용자에게 보고.
> 6. **세션 새로 시작될 때마다** 이 파일 + CLAUDE.md 둘 다 무조건 읽음.

---

## 사용자 손해 history (참고)

| 사건 | 영향 |
|---|---|
| comp2 v2 0K Cij compute_cij.py shear factor 2 누락 | C44 2x 잘못, comp2 v2 데이터 폐기 직전 |
| Method 3 v2 LBFGS 누락 → clamped C=98 anomaly | 작업 시간 손해 |
| KISTI safe wrapper "JOB DONE" check bug | rank02/03 자동 restart 안 됨, walltime 4h 낭비 |
| modelC PDOS K=12x12x6 NaN bug | nscf 다시 |

==**같은 실수 반복 막기 위해 이 파일 만듦**==.

---

## 검증 상태 분류

- ✅ **VERIFIED**: 결과가 db/실험과 일치 검증됨
- ⚠️ **SUSPECTED**: 결과 anomalous, bug 의심
- ❌ **BUGGY**: bug 확정
- ❓ **UNKNOWN**: 검증 안 됨, 사용 전 검증 필수

---

## A. DFT 0K Cij (finite-strain)

### A1. `compute_cij_check.py` ✅ VERIFIED
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/compute_cij_check.py`
- **목적**: 12 elastic_*.out에서 stress 추출 → Voigt 6x6 C → C11/C12/C44/K/G/E/ν
- **검증**: comp1 v2 → E_VRH=80.43 GPa (db 78.9, 0.6% match, 2026-05-01)
- **사용**: comp1 v2 elastic outputs (KISTI)
- **Voigt shear 처리**: 정상 (factor 2 적용됨, 추정)

### A2. `compute_cij.py` (gabia copy) ❌ BUGGY
- **위치**: gabia `/data/work/bml/manuscript_support/comp2v2_dft_0K/compute_cij.py`
- **목적**: A1과 같은 목적
- **버그**: ==Voigt shear strain factor 2 누락 추정== — comp2 v2 C44=77.6 (실제 ~38.8)
- **증거**: comp2 v2 raw / 2 = 38.80 ≈ comp1 v2 verified 38.87
- **조치**: ==**사용 금지**== 또는 ==**KISTI version (A1) 으로 교체**==
- **검증 필요**: factor 2 위치 확인하는 grep

### A3. `make_comp2_strain.py` ✅ VERIFIED (strain protocol)
- **위치**: gabia `/data/work/bml/manuscript_support/comp2v2_dft_0K/make_comp2_strain.py`
- **목적**: V0 cell + 12 strain (e1-e6, ±) cell parameters 생성
- **검증**: cell parameters 확인 결과 normal/shear strain 정확히 0.005 적용 (2026-05-01)
- **확인된 출력**:
  - e1_p: a 9.99929865 (+0.005)
  - e4_p: off-diagonal 0.04974775 (γ=0.005)

### A4. `run_comp2v2_0K_v2.sh` ✅ VERIFIED (chain runner)
- **위치**: gabia `/data/work/bml/manuscript_support/comp2v2_dft_0K/run_comp2v2_0K_v2.sh`
- **목적**: 12 strain folder 순회 → mpirun pw.x 실행
- **검증**: 12/12 JOB DONE (2026-05-01)
- **환경**: nvhpc/24.11 hpcx-2.20 ompi, qe-7.4.1-gpu, CUDA_VISIBLE_DEVICES=0

### A5. `comp1v2_elastic_*.in` ✅ VERIFIED
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_elastic_{1,2,3,4,5,6}{p,m}.in`
- **목적**: comp1 v2 12 strain QE 입력
- **검증**: 12/12 JOB DONE (Apr 14-15 2026), C44=38.87 → db 39.0 match
- **calculation**: 'scf' (clamped-ion)

---

## B. MLIP 600K snapshot elastic

### ⭐ B0. `phase2a_v31_mlip_elastic_v2_3comp.py` ✅✅✅ CHAMPION SCRIPT (2026-05-08)

> **이 항목이 MLIP 600K snapshot elastic의 SOLE CANONICAL SCRIPT**.
> Paper #1 v1 published 와 동일한 verified protocol을 사용.
> 다른 elastic 스크립트는 **검증 안 됐거나 버그 있음** (B1-B3 참조).

- **로컬 mirror**: `필독/adhesion/phase2a_v31_mlip_elastic_v2_3comp.py`
- **KISTI 위치 (실행용)**: `/scratch/x3430a02/kgy/manuscript_support/phase2a_v31_mlip_elastic_v2_3comp.py`
- **GitHub raw URL**: `https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/review-ml-migration-W29af/필독/adhesion/phase2a_v31_mlip_elastic_v2_3comp.py`
- **목적**: 600K Langevin MD 10 ps → 5 snapshots × 2 ps → 0K BFGS quench →
  per-strain LBFGS ionic relax → finite-strain Cij (delta=0.005)
- **검증된 protocol** (older `mlip_snapshot_elastic.py`에서 verbatim 복사,
  paper #1 v1 published values 재현):
  - shear strain `eps[i,j]=eps[j,i]=d/2` → ε_4_Voigt = d (correct)
  - cell transform: `cell0 @ (I+eps).T` (transposed F)
  - `set_cell(scale_atoms=False)` + `set_scaled_positions(pos0)` (frozen
    fractional)
  - **per-strain LBFGS ionic relax** (relaxed-ion, NOT clamped-ion)
  - stress sign flip + GPa convert: `s = -a.get_stress(voigt=True)*160.2176634`
- **인자**: 코드 안에 v2 anneal champion 3개 path 하드코딩 (STRUCTURE_PATHS.md
  기반):
  - comp1_v2: `post_relax_comp1_v2/comp1v2_scf.out` (espresso-out)
  - comp2_v2: `pipeline_v2/comp2_lpscbr/v2_postproc/comp2_v2_V0.xyz` (extxyz)
  - modelC_v2: `pipeline_v2/modelC_lpsc16/v2_postproc/gabia_pkg/modelc_v2_V0.xyz` (extxyz)
- **time**: ~60-90 min (3 comps × 5 snapshots × per-strain LBFGS)
- **사용**: paper #1 v2 anneal champion compositions의 elastic constants
  재계산 (2026-05-08 paper #2 link 일관성 위해)
- **출력**: `phase2a_v31_results/run.log` + `summary.json` (per-comp Cij,
  K, G, E + v1 vs v2 comparison table)

**왜 champion 인가**:
1. **2 bug** 모두 fix (v2 script은 둘 다 있음): shear factor 2 + clamped-ion
2. **Paper #1 v1 published와 동일 protocol** (older `mlip_snapshot_elastic.py`
   verbatim copy)
3. **검증 anchor**: comp1 v1 baseline (E=29.1, C44=13.1) 재현되어야 함
4. **comp2 v2 검증**: 기존 db E=34.7 재현 시 protocol 정확성 확인

### B1. `mlip_elastic_snapshot_v2.py` ❌❌ BUGGY — DO NOT USE
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/mlip_elastic_snapshot_v2.py`
- **상태**: ==**확인된 버그 2개. paper #2 작업 절대 사용 금지.**==
- **bug 1 — shear strain factor 2**:
  - 코드: `strains[3]=[[0,0,0],[0,0,1],[0,1,0]]` (full d each off-diagonal)
  - 결과: ε_4_Voigt = 2δ (should be δ) → C44 2x inflated
  - 정확한 코드 (older script): `eps[1,2]=eps[2,1]=d/2`
- **bug 2 — clamped-ion (no per-strain LBFGS)**:
  - 코드: `s.set_cell(cell0 @ eps, scale_atoms=True)` 후 바로 stress 측정
  - 결과: ions이 strain된 cell 안에서 relax 안 함 → Cij 모두 ~2x inflated
  - 정확한 protocol (older script): per-strain `LBFGS(a).run(fmax=0.01, steps=200)`
- **데이터 증거** (2026-05-08 v31 디버깅):
  - comp1_v2 v31 (이 buggy 스크립트의 함수 import 사용): C11=70, C44=58, E=98
  - v1 baseline (relaxed-ion correct): C11=33, C44=13, E=29
  - C11 ratio 2.1x (clamped-ion artifact only)
  - C44 ratio 4.5x (clamped-ion × shear factor 2)
- **이전에 이 스크립트로 만든 값 (mlip_snapshot_v2_log.txt)** comp2B C11=66
  E=93, comp5 C11=71 — 이 값들은 **paper에 사용 금지**.
- **사용해야 하면**: B0 (v31c) 사용. 이 파일은 archive 용도로만 보존.

### B2. `comp1v2_mlip_elastic.py` ❓ UNKNOWN
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_mlip_elastic.py`
- **목적**: comp1 v2 MLIP elastic
- **검증 필요** — 사용 전 B1 같은 bug 있는지 확인. 있으면 B0 (v31c) 사용.

### B3. `comp1v2_uma_elastic.py` ❓ UNKNOWN
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_uma_elastic.py`
- **목적**: UMA model elastic
- **검증 필요** — 동일.

### B_legacy. `mlip_snapshot_elastic.py` ✅ VERIFIED (older, paper #1 v1 source)
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/mlip_snapshot_elastic.py`
- **사용**: paper #1 v1 published (comp1, comp2, comp3, comp4 hardcoded
  fractional coords, no comp5/modelC)
- **상태**: ✅ verified — db/properties/elastic.json `mlip_600K_snapshot` 항목의
  comp1 (E=29.1), comp2 (E=28.6), comp3 (E=27.3), comp4 (E=26.4) 출처
- **재사용 권장 방법**: 이 함수가 B0 (v31c)의 `elastic_0K_from_snapshot` +
  `md_then_snapshot_elastic` 함수로 verbatim 복사됨. **B0 사용 = B_legacy
  사용 (다른 path / extra comp)**.

---

## C. Structure 처리

### C1. `fix_atoms_cell_v3.py` ❓ UNKNOWN
- **위치**: gabia `/data/work/bml/manuscript_support/comp2v2_dft_0K/fix_atoms_cell_v3.py`
- **목적**: ATOMIC_POSITIONS (crystal) + CELL_PARAMETERS strain (affine protocol)
- **검증 필요**: 결과물이 strain 정확히 적용된 cell parameters 만들었는지 (A3 검증 결과로 간접 OK?)

### C2. `fix_atoms_to_crystal.py` ❓ UNKNOWN
- **위치**: gabia `/data/work/bml/manuscript_support/comp2v2_dft_0K/fix_atoms_to_crystal.py`
- **목적**: ATOMIC_POSITIONS Cartesian → crystal 변환
- **검증 필요**

---

## D. Wrapper scripts (Phase 3, paper #2)

### D1. `run_rank02_safe.sh`, `run_rank03_safe.sh`, `run_rank04_safe.sh` ✅ FIXED
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/Nd_doped_phase3/phase3_inputs_top4/`
- **목적**: rank02-04 wrapper (max_seconds + restart loop)
- **이전 BUG**: "JOB DONE" 체크가 walltime hit 시 false positive → premature exit
- **FIX (2026-05-01)**: `grep -qE "bfgs converged in|End of BFGS Geometry"` 로 변경
- **검증**: 14:15 launch 후 정상 진행

### D2. `run_rank01_gabia.sh` ✅ NEW (KISTI 패턴 + gabia env)
- **위치**: gabia `/data/work/nd_doped_modelc/3_dft_verify/phase3_inputs_top4/run_rank01_gabia.sh`
- **목적**: rank01 wrapper (gabia)
- **상태**: 2026-05-01 만들어짐, 14:14 launch (PID 613607)
- **검증 필요**: BFGS convergence 도달 시 정상 exit 하는지

---

## E. Post-processing (Bader, PDOS, EOS)

### E1. Bader scripts ❓ UNKNOWN
- **위치**: 확인 필요 (KISTI / gabia 어디?)
- **목적**: Henkelman bader_lnx_64 on QE pp.x charge density
- **이전 결과**: comp1 v2, comp2 v2, modelC v2 Bader values 모두 db에
- **검증**: 결과가 합리적인지는 확인됐지만, script 자체 검증은 ❓

### E2. PDOS scripts ❓ UNKNOWN
- **위치**: 확인 필요
- **목적**: projwfc.x → PDOS analysis
- **이전 BUG**: KISTI GPU build K=12x12x6 NaN issue → K=6x6x3 + nosym으로 fix
- **검증**: comp1 v2, comp2 v2, modelC v2 PDOS 결과 db에

### E3. EOS BM3 fitting script ❓ UNKNOWN
- **위치**: 확인 필요
- **목적**: 11 volume points → BM3 fit → B0, V0, B0'
- **이전 결과**: comp2 v2 B0=25.8, modelC B0=21.7 등 db에

---

## F. Adhesion (Wad)

### F1. `phase2a_lbfgs_wad.py` ✅ VERIFIED (paper #1 v5 baseline)
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase2a_lbfgs_wad.py`
- **목적**: SE/NCM v5 — single interface + 30 Å vacuum + FixAtoms 33% bottom (both NCM and SE) + /A
- **검증**: paper #1 Section 4 published values
  - comp1: 1.277 J/m² (paper) | comp2B: 1.183 | comp3: 2.103 | comp4: 1.970 | comp5: 1.651
  - R = 0.9999 with experiment
- **NCM**: 1L conv (3 atomic layers) — known to be "broken structure" per user 2026-05-07
- **상태**: ==**baseline 보존**==. v10으로 superseded but kept for reference comparison.

### F2. `phase2a_v10_sandwich.py` ❌ INVERTED (cycle 1 result, stopped 2026-05-07 13:45)
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase2a_v10_sandwich.py` (paste from `필독/adhesion/`)
- **로컬 미러**: `필독/adhesion/phase2a_v10_sandwich.py`
- **목적**: Camacho-Forero 2020 sandwich method (LPSCl/NCM 업그레이드) — paper #2 main
- **Cycle 1 결과 (3/216)**:
  - comp1 W=+2.057 (paper 1.28, 1.6×, Camacho-Forero LPSCl/Li2S=1.44 anchor 일치)
  - comp2 W=+1.854
  - comp3 W=**-0.058** (paper 2.10, Li5.4 vacancy effect ==REVERSED==)
- **원인**: SE no FixAtoms → Li6 high Li density 23 atoms migrate → high apparent Wad (intermixing dominates). Li5.4 vacancy = fewer Li → less migration → near-zero Wad. v5 paper의 vacancy chemical anchor mechanism 사라짐.
- **상태**: ❌ STOP, supersededby v10b
- **변경점 (vs v5)**:
  - Sandwich (no vacuum at interface) → /(2A)
  - NCM 3L conv (9 atomic layers, 42.57 Å)
  - FixAtoms NCM **middle** 3 atomic layers (preserves bulk + symmetric interfaces)
  - SE no FixAtoms (Camacho-Forero standard) ⚠️ — root cause of v10 inversion
  - LBFGS fmax=0.03, steps=400

### F8. `phase2a_v16to22_full_suite.py` ❓ UNKNOWN — comprehensive validation suite (v16-v22)
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase2a_v16to22_full_suite.py`
- **로컬 미러**: `필독/adhesion/phase2a_v16to22_full_suite.py` ⭐
- **목적**: v16 cutoff + v17 gap_window + v18 per-atom + v19 phase1 crossval + v20 xyz vis + v21 composite + v22 relaxed bonds
- **시간**: ~15 min total (v16-v21 geometry only fast, v22 needs UMA LBFGS)
- **상태**: 작성 완료, 배포 대기. v15 통과 후 다음 단계.

### F7. `phase2a_v15_bond_robustness.py` ✅ ROBUST validated (CV 6.1%)
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase2a_v15_bond_robustness.py`
- **로컬 미러**: `필독/adhesion/phase2a_v15_bond_robustness.py`
- **목적**: 36 xy-shifts × 6 comps bond count statistics
- **결과**: average CV non-zero bonds = 6.1% → robust intrinsic feature
  - Li-O density v14 single R1 = +0.8325, v15 mean of 36 = +0.8190 (Δ=0.014)
  - Cl-O density v14 = -0.9131, v15 = -0.9142 (Δ=0.001)
- **시간**: 2.1 min (pure geometry, no UMA)

### F6. `phase2a_v14_full_validation.py` ✅ DIAGNOSTIC done
- **위치**: KISTI 동일
- **로컬 미러**: `필독/adhesion/phase2a_v14_full_validation.py`
- **결과**: gap_eq 1.2-1.6 Å (per comp), W_eq R(paper)=-0.7596 (anti-correlated), Li-O density R=+0.8325, Cl-O density R=-0.9131
- **결론**: Energy descriptor anti-correlated, geometric (bond density) correlated
- **시간**: 1.1 min

### F5. `phase2a_v13_validation.py` ✅ DIAGNOSTIC done
- **위치**: KISTI 동일, 로컬 `필독/adhesion/phase2a_v13_validation.py`
- **결과**: Z-scan W_max all at gap=1.5 (shortest tested), ranking OPPOSITE of v12 gap=2.5 → v12 was gap-coincidence
- **시간**: ~10 min

### F4. `phase2a_v12_rigid_haruyama.py` ✅ baseline (rigid, NO LBFGS)
- **위치**: KISTI 동일, 로컬 `필독/adhesion/phase2a_v12_rigid_haruyama.py`
- **결과 216/216 (3.7 min)**:
  - comp1=0.378, comp2=0.339, comp3=1.107, comp4=0.504, comp5=0.514, modelC=0.236
  - Cycle 1 ranking matched paper exp (coincidental, gap=2.5 dependent)
- **상태**: ⭐ baseline for v13-v22 validation suite

### F2c. `phase2a_v11_haruyama_single.py` ❌ INVERTED — LBFGS Li intermixing artifact
- 결과 cycle 1: comp1=7.85, comp3=4.22, comp4=2.60, Li_mig 7-20 atoms
- Stopped 2026-05-07 15:30

### F2c_old. `phase2a_v11_haruyama_single.py` ❓ UNKNOWN — pending pilot ⭐ ACTIVE
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase2a_v11_haruyama_single.py` (paste from `필독/adhesion/`)
- **로컬 미러**: `필독/adhesion/phase2a_v11_haruyama_single.py` ⭐
- **목적**: ==**Haruyama 2014 faithful**== — single interface + vacuum + /A (anti-sandwich for oxide/sulfide hetero)
- **Anchor**: Haruyama 2014 PRIMARY method anchor + Komatsu 2022 BULK + Camacho-Forero 2020 chemistry
- **변경점 (vs v10b sandwich)**:
  - Sandwich → ==**single interface + vacuum 30 Å**== (Haruyama §2.1 explicit)
  - /(2A) → ==**/A**== (single interface formula)
  - NCM/SE middle 1/3 fix → ==**NCM bottom 1/3 + SE top 1/3**== (vacuum-touching sides only)
  - Active interface: NCM_top (free) ↔ SE_bottom (free) — chemistry develops
- **검증 필요**: pilot 후 cross-family Li5.4 > Li6 회복 + Wad scale 0.5-1.5 J/m² 정상 범위
- **Context**: ==**v5 paper #1 results LOST (server)**==. R²=0.9999 was curated. So v11 is from-scratch validation, no v5 ground truth.
- **상태**: 작성 완료, KISTI deploy 대기

### F2b. `phase2a_v10b_sandwich_se_fixed.py` ❌ INVERTED (cycle 1, stopped 2026-05-07 14:40)
- Cycle 1 (4/216): comp1=+1.96, comp2=+1.80, comp3=+0.22, comp4=−0.28 → Cross-family INVERTED
- Root cause: Haruyama 2014 §2.1 explicit anti-sandwich for oxide/sulfide hetero
- Stopped, supersededby v11

### F2b_old. `phase2a_v10b_sandwich_se_fixed.py` ❓ UNKNOWN — pending pilot
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/phase2a_v10b_sandwich_se_fixed.py` (paste from `필독/adhesion/`)
- **로컬 미러**: `필독/adhesion/phase2a_v10b_sandwich_se_fixed.py` ⭐
- **목적**: v10b — sandwich + symmetric NCM/SE middle FixAtoms (v10 cycle 1 inversion 해결)
- **변경점 (vs v10)**:
  - **SE middle 1/3 FixAtoms 추가** (NEW) — preserve bulk SE, prevent Li intercalation, allow surface vacancy chemistry
  - LBFGS fmax 0.05 (was 0.03), steps 300 (was 400) — middle fix should converge faster
  - Iso slabs도 같은 middle 1/3 fix (consistency)
  - RESULTS_DIR: phase2a_v10b_results
- **검증 필요**: cycle 1 후 cross-family Li5.4 > Li6 회복 여부 + Wad scale 1-3 J/m² 정상 범위
- **상태**: 작성 완료, KISTI deploy 대기

### F3. `phase2a_v9_cleavage.py` ❌ INVERTED (cross-family failed, stopped 2026-05-07)
- **위치**: KISTI 동일 디렉토리
- **방식**: rigid cleavage Wad = (E_sep_no_relax - E_iface) / A
- **결과 (24/216 partial)**: comp3 v9=0.82 vs v5 paper 2.10 (-61%), Li6 > Li5.4 ==**REVERSED**==
- **원인**: rigid cleavage = bond-breaking only, vacancy strain release effect 사라짐
- **상태**: ==**폐기**==

### F4. `phase2a_v8_surface_mqa.py` ❌ INVERTED
- **위치**: KISTI 동일 디렉토리
- **방식**: 800K → 300K → 100K MQA + LBFGS
- **결과**: cross-family 같은 inversion (v9와 비슷)
- **상태**: 폐기

### F5. `phase1_rigid_binding.py` ✅ DIAGNOSTIC (binding curve only)
- **위치**: KISTI 동일 디렉토리
- **목적**: rigid Z-scan binding curve (no relax) — Method A/B 비교
- **결과**: phase1_summary.json. Method A modelC W_max=-2.18 (음수, isolated slab unphysical).
- **사용**: SI figure보강. main Wad는 F1/F2 사용.

### NCM structure files (verified inputs)
- `ncm_7x7x1_PRESERVED.xyz`: LiNiO2 588 atoms (147 Li/Ni + 294 O), c=14.19 Å (1L conv = 3 atomic layer)
- `ncm_7x7x1_3Lconv.xyz`: LiNiO2 1764 atoms, c=42.57 Å (3L conv = 9 atomic layer) — **v10 input**
- `ncm_5x5x1_PRESERVED.xyz`: 300 atoms (1L conv)
- `ncm_5x5x1_3Lconv.xyz`: 900 atoms, c=42.57 Å (3L conv) — **v10 input**
- `ncm_5x5x1_2Lconv.xyz`: 600 atoms (2L conv) — unused
- 3Lconv 생성 방법: `ase.read('*_PRESERVED.xyz') * (1,1,3)` 단순 z-repeat (verified 2026-05-07)

---

## G. 검증 우선순위 (Critical first)

> [!warning] paper #1 main figure에 영향
> 1. **B1** (`mlip_snapshot_elastic`) — paper Section 3 main → ==**최우선 검증**==
> 2. **A2** (`compute_cij.py` gabia) — already known buggy → 사용 중지
> 3. **E1** (Bader) — paper Section 2 main → 결과는 합리적이지만 script 검증
> 4. **E2** (PDOS) — paper Section 2 → 위와 동일

> [!info] paper SI / 보조
> 5. C1, C2, F1 — 결과는 있지만 script 검증

---

## H. 검증 절차 (script별)

각 script 검증 시 다음 확인:
1. **input 명세** — 어떤 파일 받는가
2. **output 명세** — 어떤 결과 내는가
3. **알려진 reference** — 다른 db값과 일치하는가 (예: comp1 v2)
4. **edge case** — shear vs normal, cubic vs rhombo, ISPIN=2 등
5. **dependency 버전** — ASE, numpy, MACE-MP-0 등

---

## I. 새 사용 규칙 (Claude algorithm fix)

> [!important] CLAUDE 행동 강제
>
> 사용자가 "compute_cij 돌려줘" / "elastic 계산하자" 같은 명령 시:
>
> 1. **이 파일 (CODE_INVENTORY.md) 먼저 읽기**
> 2. **해당 작업의 verified script 위치 확인**
> 3. **없으면 사용자에게 "어디에 있나요" 묻기**
> 4. **있으면 그 script 실행 명령만 제공**
> 5. ==**절대 새 script 생성 금지**==
> 6. ==**"비슷한 거 짜드릴게요" 답변 금지**==
>
> 결과 anomaly 발생 시:
> - 즉시 이 파일의 ✅ VERIFIED 항목과 비교
> - script 검증 상태 (status) 사용자에게 보고
> - bug 의심 시 사용자 confirm 전까지 결과 신뢰 안 함

---

## J. 변경 history

| 날짜 | 변경 |
|---|---|
| 2026-05-01 | 초기 catalog 생성 — comp2 v2 C44 anomaly bug 사건 후 |
| 2026-05-01 | step1_v2.py (comp1 v2) ✅ VERIFIED, comp2 v2 production 코드 ❌ 미확인 |

---

## Pipeline v2 — Step 별 production code

> 위치: KISTI `pipeline_v2/{comp1_lpscl, comp2_lpscbr, modelC_lpsc16}/`

### 1. Halogen enumerate ✅
- file: `step1_v2.py` (Stage 1)
- comp1: C(8,4)=70 / comp2: C(8,2)×C(6,2)=420 / modelC: (확인필요)
- output: top halogen config

### 2. Li screen ✅
- file: `step1_v2.py` (Stage 2)
- 20 random Li configs (seed=42) on best halogen
- output: top Li config

### 3. Anneal ✅
- file: `step1_v2.py` (Stage 3) + `anneal_champion.py`
- protocol: 500K 100ps Langevin + 300K 10ps quench + LBFGS
- top_for_anneal: Top 1
- output: `comp{1,2}_v2_champion.{xyz,cif}`, `pipeline_v2_results.json`

### 4. MLIP EOS ✅
- file: `step2_mlip_eos.py`
- input: `comp2_v2_champion.xyz` → LBFGS refine (fmax=0.005)
- protocol: 13 volumes (v096~v108) × cell-fixed LBFGS (fmax=0.01)
- BM3 fit → B0, V0, B0', R²
- output: V0 grid 추천 (v{round(V0_scale*100)} ± 5) for DFT EOS

### 5. DFT EOS ✅
- comp2 file: `step3_dft_eos_comp2.py`
- comp1 file: `step3_dft_eos.py`
- protocol: 11 volumes (v098~v108) × `calculation='relax'` (cell-fixed atom relax)
- pseudo: SSSP_1.3.0_PBE_efficiency
- output: `comp{1,2}_v2_eos_v{098-108}.in` + tmp_v###/

<!--
주석:
* comp1 step3_dft_eos.py에 `ntyp=3` 하드코딩 bug — 실제 4종 (Li,P,S,Cl).
  production은 manual fix 후 돌렸음 (결과 db 매칭 ✓).

* DFT settings (실제 사용값, CLAUDE.md 기본값과 다름):
  ecutwfc=52, ecutrho=520, K=2x2x2, mixing_beta=0.2, nosym=.true.
  smearing=mv, degauss=0.01, conv_thr=1e-8, forc_conv_thr=1e-4
  → CLAUDE.md (ecutwfc=60, ecutrho=480, K=6x6x6) outdated.

* K=2x2x2는 EOS 용 (relative E만 필요). post-processing은 더 dense 사용.
-->


### 6. BM3 fit + V0 selection ✅
- input: 11 v###/pw.out (DFT EOS 결과)
- BM3 fit: n=11 points → V0, E0, B0, B0'
- closest grid: argmin |V - V0|
- output: `comp2_v2_BM3_fit.json` (raw_data + fit params),
  `v2_postproc/tmp_v###/` (closest grid의 .save copy),
  `v2_postproc/comp2_v2_V0.xyz` (closest grid cell + relaxed coords)
- 검증 (comp2 v2):
  - V0_fit = 983.58 Å³, B0 = 25.74 GPa (db 25.8 매칭 ✓)
  - closest = v103 (V=984.94, Δ=0.14%)
  - V0.xyz cell a=9.9496 = v103^(1/3) ✓

<!--
주석:
* BM3 fit script .py 없음 (hand-done 또는 notebook).
  결과 json + raw_data로 재계산 가능. reproducibility 약간 미흡.
* tmp_v103/이 V0 cell의 .save 보유 → post-processing은 v103 cell+coords 사용.
-->


### 7. Post-processing ❓
- PDOS (128 pdos_atm files)
- Bader (`charge.dat`, `charge.cube`, `run_comp2_v2_bader.sh`)
- (검증 대기)

---

### v2 실행 status
| comp | step 1-3 | step 4-7 |
|---|:-:|:-:|
| comp1 | ✅ | ✅ |
| comp2 | ✅ | ✅ |
| comp3, 4, 5 | ⏳ TODO (template ready) | — |
| modelC | ✅ | ✅ |

### modelC 코드 위치 (필독 미러 안 함, reference만)
- KISTI: `/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/modelC_lpsc16/`
- 파일: `modelC_v2_step1.py`, `modelC_v2_mlip_eos.py`, `gen_dft_eos.py`, `modelC_v2_step3_continue.py`
- comp1/comp2 step1_v2.py와 ==logic 동일==, rhombohedral cell + Cl-only + Li5.4 family (vacancy) 차이만.

⚠️ ==**modelC v2 actual production은 Top 5 anneal (50ps each)**== — comp1/comp2 (Top 1 + 100ps)와 다름.
필독/ 로컬본은 Top 1 + 100ps로 unified 작성, ==modelC_v2_step3_continue.py만 historical Top 5 evidence로 보존==.

<!--
주석 (잡설):

* Apr 27 timeline (comp2 v2):
  16:05 step1_v2.py 작성 → 17:46 run → best_cl=[0,2], br=[5,7], li=Li_configs[0]
  20:25 anneal_champion.py (best 하드코딩) → 21:24 champion.xyz/cif

* anneal_champion.py 코드는 50ps 표기, log는 100ps 실행 — .py가 나중 수정.
  production은 100ps.

* Top 1 selection 검증 (comp1 evidence):
  - rank 2-5 best E = -217.042 / rank 1 anneal E = -217.533
  - ΔE = 491 meV → Top 1 명백 winner
  - comp2 Top 2-5 미검증 (nd 후 확인 가능)

* gabia comp2_v2_V0.xyz는 KISTI에서 transfer된 copy.

* step1_enumerate_halogen.py (Apr 27 15:55)는 superseded.

* paper narrative:
  - within-family Br trend (paper main) = v1 비교
  - anneal stiffening (paper sub) = comp1/comp2/modelC v1 vs v2
  - comp3-5 v2 시간 부족, comp345_v2_from_modelC.py template 준비됨
-->

---

## TODO — 사용자가 채워야 할 빈칸

다음 명령 결과 paste해 주시면 inventory 채워집니다:

```bash
# KISTI에서 — 모든 .py 스크립트 위치
find /scratch/x3430a02/kgy/manuscript_support -name "*.py" 2>/dev/null

# gabia에서 — 모든 .py 스크립트 위치
find /data/work/bml/manuscript_support -name "*.py" 2>/dev/null

# Adhesion / EOS / Bader 관련
find /scratch /data -name "*bader*" -o -name "*adhesion*" -o -name "*eos*" 2>/dev/null | head -30
```

---

#code-inventory #verified-scripts #claude-algorithm

---

## Z. 2026-05-15 unification — newly migrated files

(From `claude/configure-spawn-halogen-lithium-TjDCB`. See `MIGRATION_2026_05_15.md`.)

### Z1. Doping screening pipeline (Phase 1) — `tools/doping/`
- **`tools/doping/site_preference.py`** ✅ VERIFIED (validated against 19 documented LPSCl substitutions, 0/19 mismatch)
  - `--validate` flag cross-checks RADIUS_TOL against literature
  - `--all` runs every entry in DOPANT_DB
  - Per-site cutoffs (Li 0.60 / P 0.55 / S 0.50 / Cl 0.50 Å) calibrated from observed cases — refs in code header
- **`tools/doping/substitute_struct.py`** ✅ tested on data/lpscl_bulk.cif (217 structures generated for 29 dopants)
  - `--polymorph`, `--li_ordering`, `--method random --n_seeds N` options
  - Ensemble mode produces N independent Li-vacancy + dopant-site seeds per (dopant, conc) for B0/E mean±std
- **`tools/doping/run_uma_screening.py`** ✅ dry-run OK (3 struct in 21.8s on gabia A100 uma env)
  - UMA-s-1p1 + FrechetCellFilter + FIRE, fmax 0.05, resume-safe
- **`tools/doping/analyze_screening.py`** ✅
  - Composite ranking (energy / volume / site_pref / charge_comp) + Top-N report
- **`tools/doping/fetch_mp_structure.py`** ✅
  - MP API wrapper; warns mp-985592 is dynamically unstable cubic
- **`db/doping/dopant_candidates.json`** — 30 dopants Shannon radii + charges
- **`db/doping/site_preference_initial.json`** — Tier-1 screening result (29/30 dopants compatible)
- **`db/structures/lpscl_bulk.cif`** — UMA-relaxed LPSCl baseline (52 atom, pseudo_cubic_P1, 48H_low)

### Z2. Nd-doped LPSCl DFT EOS (paper #2) — `runs/nd_doped_modelc/`
- **`runs/nd_doped_modelc/2_uma_eos_predft/`**
  - `uma_screen_all_pairs.py`, `uma_eos_pre_dft.py`, `sbatch_uma_eos_kisti.sh`
- **`runs/nd_doped_modelc/3_dft_eos/`**
  - `prepare_dft_eos_nd.py` (UMA → DFT input prep, 7 volumes per pair)
  - `sbatch_dft_eos_nd.sh` (KISTI sbatch, 2 GPUs, --comment=qe)
  - `run_dft_eos_pair.sh` (per-pair runner with BFGS auto-restart)
  - Status: rank1 (pair_00) + rank2 (pair_02) DFT EOS in progress on KISTI

### Z3. v0 paper analysis / plotting — `필독/adhesion/`
- `alpha_sensitivity_FINAL.py` (α strain correction sensitivity, R=+0.989 derivation)
- `bond_density_36reg_FAST.py` (36 lateral registries averaging — fixes single-config artifact)
- `bond_density_LiO_cutoff_sweep.py` (Li-O cutoff sensitivity)
- `comprehensive_FINAL_analysis.py`
- `generate_stacked_deq_orthogonal.py`
- `plot_R0988_TIGHT_FIT.py` (paper Figure 5)
- `run_li_migration_FINAL_combo.py` (vacancy-driven ΔW_ad, anchor evidence)

### Z4. Knowledge base additions — `kb/methodology/`, `kb/papers/`, `db/literature/`
- `kb/methodology/argyrodite_mechanical_pipeline.md` ⭐ — canonical 8-step + 3 appendices, integrates v1 user-provided + Pustorino 2025 + D'Amore 2022 findings + per-step ref. table
- `kb/methodology/coating_descriptor_catalog.md` — 60+ descriptors, §4 has B0 baseline-dependence warning (Pustorino/D'Amore)
- `kb/methodology/doping_substitution_algorithm.md`
- `kb/methodology/PHASE1_QUICKSTART_doping.md`
- `kb/methodology/digital_twin_roadmap.md`, `platforms_literature_db_tools.md`, `platforms_ml_automation.md`
- `kb/papers/mechanism_anion_O_descriptor.md` (v0 paper mechanism, R=+0.989, 3-tier Cl-O / S-O / Li-O drivers)
- `db/literature/damore_2022_lpscl_symmetry_breaking_qha.md` (LPSCl F-43m metastable, imag phonons; B0(298K) 18.7 vs 26 GPa polymorph spread)
- `db/literature/pustorino_2025_lpscl_li_ordering_mechanical.md` (Li ordering + S/Cl inv → B0 13.7~29.6 GPa, ±50%; 48HR is ground state)
- `db/literature/sundar_2025_lpscl_coating.md` (Argonne 3-interface ΔE screening, comparison baseline)

### Z5. Tools — `tools/`
- `tools/literature_harvest.py` — OpenAlex / Semantic Scholar API client for auto-curation


### Z6. Compound-set doping (Type A/B/C from literature)
- **`tools/doping/substitute_compound.py`** ✅ tested on Nd2O3 / Li5.4PS4.4Cl1.6 / MgO / Al2O3+Cl
  - Type A: ionic compound (`--compound Nd2O3 --x_compound 0.05`)
  - Type B: halide-rich (`--halide_rich Cl --excess_per_fu 0.6`) reproduces Li6-xPS5-xCl1+x
  - Type C: chain Type A + Type B (`--also_halide_rich Cl --excess_per_fu 0.3`)
  - Charge balance auto: cation aliovalency at Li site → extra Li vacancy
  - Each test verified: Mg/Nd/Al all give expected (Li_count, Mg/Nd/Al_count, S_count, O_count, Cl_count, total_atoms)
- `tools/doping/site_preference.py` — add 6 rare-earth dopants (La, Ce, Nd, Sm, Gd, Yb)
  for Nd2O3 / La2O3 / Sm2O3 oxide-coating chemistry (Sundar 2025 + paper #2). Validation
  table unchanged (0/19 mismatches preserved).
- `db/literature/lpscl_doping_precursor_compounds_review.md` — 4-mechanism
  classification (A: compound set, B: halide-rich, C: aliovalent+halide co-doping,
  D: additive not lattice). 10 reference citations with DOIs.


### Z7. 2026-05-16 gabia migration — binding curve / EOS / elastic

**Provenance**: gabia `/data/work/v30u_ensemble/` (binding curve production for R=+0.989 paper figure), `/data/work/comp3_v2_eos/` (comp3 v2 EOS), `/data/work/modelc_v2_elastic/` (modelC v2 elastic) mirrored to repo on 2026-05-16. User-confirmed *"마지막으로 이게 나온 코드"* for the UMA binding curves figure (Cl-coherent termination, α=1.0, uniform Li5.4 dW, R=+0.989, ρ=+1.000, ⟨RMSE⟩=0.0662 J/m², strict paper rank, 5 comps).

#### Z7-A. Binding curve production — `필독/adhesion/v30u_ensemble/` (45 .py files)

**핵심 production lineage**:
- `run_v30u_1L.py` → `_correct.py` → `_correct_mlip_relax.py` → `_correct_eiso_fix.py` → `_face_flip.py` — 5-step 진화. **최종**: `_correct_eiso_fix.py` + `_face_flip.py` 조합 (eiso 보정 + face orientation flip).
- `run_v30u_ensemble.py`, `run_v30u_full_ensemble.py` — multi-comp batch driver.
- `run_comp35_v2_eiso_fix.py`, `run_comp4_v2_eiso_fix.py` — comp별 eiso rerun.

**Slab/face generators**:
- `make_comp12_stacked_orthogonal.py`, `make_comp35_v2_slab.py`, `make_comp4_v2_stacked_orthogonal.py`
- `enumerate_v1_faces.py`, `enumerate_v2_faces.py`
- `generate_stacked_xyz_at_deq.py`, `generate_stacked_deq_orthogonal.py`

**α correction (paper Figure 5)**:
- `alpha_sensitivity_FINAL.py` — α ∈ [0.0, 1.5] sweep
- `alpha_strain_fit.py` — α strain fitting
- `db/properties/alpha_sensitivity_FINAL.json` — output data

**Wad analysis**:
- `normalize_wad_by_surface_Li.py` — surface-Li normalization
- `bond_density_at_interface.py`, `_full.py`, `_36reg_FAST.py`, `_36reg_FINAL.py`, `_LiO_cutoff_sweep.py`, `_FINAL_combo.py`
- `bond_length_ensemble.py`
- `analyze_per_z_surface_all.py`, `analyze_species_z_profile.py`, `analyze_halogen_slab_positions.py`

**🎯 R=0.989 figure plotters**:
- `plot_binding_curves_morse_fullwindow.py` ⭐ — **사용자가 보낸 figure** (Cl-coherent, α=1.0, Morse fit, full window 0.5-4.2 Å)
- `plot_killer_v2_R0988_final.py`, `plot_R0988_standalone.py`, `plot_killer_v2_figure_n5.py`, `plot_killer_v2_figure.py`
- `plot_binding_curves_morse.py` (earlier window)
- `plot_v30u_1L_correct_z0_only.py`, `plot_v30u_1L_correct_eiso_fix.py`

**Li migration tests (anchor mechanism evidence)**:
- `run_li_migration_rigid_test.py`, `_rigid_36reg.py`, `_FINAL_combo.py`

**Mechanism schematics**:
- `scheme_vacancy_mechanism.py`, `render_interface_3axis.py`, `render_interface_3d.py`

**Misc**:
- `comprehensive_FINAL_analysis.py`, `exhaustive_v2_trend_analysis.py`

**검증 status**: ✅ **VERIFIED** — paper Figure 5 (R=+0.989, ρ=+1.000) 재현 source. raw z-shift directories는 gabia 보존 (`/data/work/v30u_ensemble/comp{1,2,4,5}_slab_v*_zshifts/`, `comp3_slab_v1_PRESERVED_zshifts`), 필요 시 추가 mirror.

#### Z7-B. EOS production — `필독/step2_mlip_eos/comp3_v2/`, `필독/step3_dft_eos/comp3_v2/`

- `필독/step2_mlip_eos/comp3_v2/comp3_v2_mlip_eos.py` ✅ MLIP EOS scan (UMA, comp3 v2)
- `필독/step3_dft_eos/comp3_v2/step3_dft_eos_comp3.py` ✅ DFT EOS 11 volumes (comp3 v2)
- `필독/step3_dft_eos/comp3_v2/run_comp3_v2_eos.sh` — gabia chain runner
- `필독/step3_dft_eos/comp3_v2/watch_eos.sh` — progress monitor
- `필독/step3_dft_eos/run_eos_both.sh` — basin A/B batch driver (modelC)
- `필독/step3_dft_eos/run_comp5_elastic_basinA.sh` — comp5 basinA elastic
- `필독/step3_dft_eos/run_all_elastic_v2.sh` — all-comp elastic v2 batch

**검증 status**: ✅ **production source** for db/properties/eos.json (canonical B0: comp1=26.2, comp2=25.8, comp3=20.8, comp4=20.8, comp5=22.9, modelc=21.7 GPa). BM3 fit downstream in `필독/step4_bm3_v0/bm3_fit_eos.py` (already inventoried).

#### Z7-C. modelC v2 elastic — `필독/step5_postproc/elastic_modelC_v2/` ❌ BUGGY

⚠ **factor 2 bug 재발** (CLAUDE.md history A2 `compute_cij.py` 동일 패턴):

- `modelC_mlip_elastic.py` — MLIP elastic (modelC)
- `dft_0K/make_strain.py` — strain generator
- `dft_0K/fit_cij.py` — **❌ BUGGY** — Voigt shear factor 2 누락
- `dft_0K/run_dft_elastic.sh`, `run_dft_gpu.sh`, `run_modelc_v2_0K_elastic.sh` — runners

**진단** (2026-05-16):
- `make_strain.py` shear eps matrix: `[[0,0,0],[0,0,1],[0,1,0]] * STRAIN` → ε_xy = ε_yx = STRAIN (symmetric tensor strain) → **engineering γ_xy = 2×STRAIN**.
- `fit_cij.py` line: `ds = (sig_p − sig_m) / (2*STRAIN)` — STRAIN으로만 나눔.
- σ_xy(QE) = 2·C_66·ε_xy = 2·C_66·STRAIN ⇒ ds = 2·C_66 ⇒ **reported C_44/C_55/C_66 = 2× true Voigt**.
- 영향: K_V (diagonal-only) 정확, **G_V/G_R 2× over**, E_young 2× over, Pugh ratio 잘못.
- **증거**: `db/properties/elastic.json` row 1 (comp1 C44=37.9, E=76.9, factor 2 over) → canonical row 4 (comp1 C44=13.1, E=29.1, ✅ factor 2 fixed, sign-corrected). row 1이 이 fit_cij.py pattern.

**조치**: ❌ **사용 금지**. modelC v2 elastic 결과는 다음 verified source 사용:
- **0K DFT clamped-ion**: KISTI `compute_cij_check.py` (CODE_INVENTORY A1 ✅)
- **600K MLIP snapshot relaxed-ion**: `필독/adhesion/phase2a_v31_mlip_elastic_v2_3comp.py` (B0 champion ✅, paper #1 v1 reproduction)

repo에 mirror된 이유: gabia cleanup 대비 reference 보존 + factor 2 bug 비교 anchor.

#### Z7 history note (사용자 손해 방지)
- 2026-05-01: A2 `compute_cij.py` (gabia comp2_v2) factor 2 누락 → comp2 v2 wasted
- 2026-05-16: **modelC v2 `fit_cij.py` 동일 패턴 재발견** — 같은 author가 새 디렉토리에 같은 bug 복제. 향후 elastic 신규 코드 작성 시 **make_strain의 shear ε vs γ 정의 + fit의 / (2·STRAIN) divisor 항상 한 쌍으로 검토**.

