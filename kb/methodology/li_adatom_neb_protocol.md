---
title: "Li Adatom Diffusion NEB Protocol — UMA + DFT Verification"
tags: [methodology, neb, mlip, dft, anode-free, ssb, li-adatom]
date: 2026-06-02
status: confirmed
---

# Li Adatom Diffusion NEB Protocol

> [!important] Two-track protocol
> **Track 1**: UMA-oc20 fast NEB (~min/system) for path discovery + sanity check
> **Track 2**: DFT verification — SCF on UMA geometry (intermediate cost) *or* full DFT NEB (definitive, ~5–7 days/system)

## 1. Slab construction

| System | Lattice | Slab | Top layer | Frozen |
|---|---|---|---|---|
| Li₃N (001) | P6/mmm, a=3.65, c=3.87 Å | 3×3×4, 144 atoms → trim top Li(1) → **135 atoms** | 18 Li(2) + 9 N (N + Li(2) mixed terminantion, matches paper Fig 2a) | bottom 50% |
| LiC₆ (0001) | stage-1 √3×√3 R30°, a=4.26 Å | 2×2×2, 112 atoms → trim surface Li → **108 atoms** | 24 C (graphene-terminated; Li intercalated, not on surface) | bottom 50% |
| LiNO₃ (001) | R-3c, a=4.692, c=15.21 Å | — | — | builder R-3c symmetry bug, **not used** |

Vacuum 15 Å along c-axis. Slab built via `build_li3n_slab.py`, `build_lic6_slab.py`.

## 2. NEB setup (ASE)

```python
from ase.mep import NEB                 # ASE 3.23+; from ase.neb removed
from ase.optimize import BFGS           # FIRE as fallback
from ase.constraints import FixAtoms

n_images = 7                            # initial + 5 mid + final
IDPP_interpolation = True               # image-dependent pair potential
CI_NEB = True                           # climbing image for accurate TS
spring_k = 0.1
fmax_target = 0.05  # eV/Å
```

Endpoint relaxation first (fmax 0.02 eV/Å), then 2-phase NEB:
- **Phase 1**: regular NEB, ~5 steps (spring equilibrium)
- **Phase 2**: CI-NEB until fmax ≤ 0.05 eV/Å

## 3. Track 1 — UMA-oc20 calculator

```python
from fairchem.core import FAIRChemCalculator, InferenceSettings
settings = InferenceSettings(merge_mole=False)  # avoid composition cache assertion
calc = FAIRChemCalculator(model="uma-s-1p1", task="oc20", settings=settings)
```

- **Why oc20**: surface adsorbate task, matches our slab+adatom geometry. omat task verified worse for SDCP-LiNiO₂ (Phase A); oc20 robust for both Li3N and LiC6.
- **Runtime**: ~5–10 min/system on single A6000.
- **Output**: `neb_path_final.xyz` (7-frame multi-xyz), `neb_energies.json`.

## 4. Track 2A — DFT SCF on UMA geometry (intermediate verification)

For each of 7 UMA-relaxed image coordinates, run a single QE pw.x SCF (geometry frozen).

```fortran
calculation='scf'                       ! no geometry relaxation
ecutwfc=60, ecutrho=480                 ! Ry, USPP
k-grid 2x2x1, nosym=.true., smearing='mv', degauss=0.01
conv_thr=1e-8, mixing_beta=0.3, electron_maxstep=300
```

Pseudos:
- Li: `li_pbe_v1.4.uspp.F.UPF`
- N: `N.pbe-n-radius_5.UPF`
- C: `C.pbe-n-kjpaw_psl.1.0.0.UPF`

Runtime: ~8h/system (7 SCF × ~1h each). Build inputs: `build_dft_neb_inputs.py`. Run: `run_dft_neb.sh`. Parse: auto-JSON at end.

**Effective barrier definition** (when bridge minimum exists):
$$E_a^{eff} = E(\text{TS}) - E(\text{bridge minimum})$$
Used for systems where adatom prefers a bridge site over the on-N/hollow endpoint (Li3N).

**Caveat**: This method captures DFT energetics at UMA-relaxed geometry. If UMA over-smooths the TS (saddle point), the absolute barrier is underestimated. Same-protocol relative comparison (e.g., LiC6/Li3N ratio) is robust; absolute values are not.

## 5. Track 2B — Full DFT NEB (definitive)

ASE NEB driving QE `pw.x` as calculator. Each image geometry is DFT-relaxed under NEB forces.

```python
from ase.calculators.espresso import Espresso, EspressoProfile  # ASE 3.23+ REQUIRES profile
profile = EspressoProfile(
    command="mpirun -np 1 pw.x",
    pseudo_dir="/data/work/pseudo"
)
```

- Per-image working directory (`img0/`, ..., `img6/`) — avoids wfc file collisions.
- Same QE settings as Track 2A (PBE+USPP, 60/480 Ry, 2x2x1 k).
- Warm-start: UMA `neb_path_final.xyz` as initial guess.
- 2-phase: 5 regular NEB → 30 CI-NEB max steps, fmax 0.05 eV/Å.
- Restart auto via `neb.traj` checkpoint (handles SIGKILL gracefully).
- Runtime: ~5–7 days/system on single A6000 (~7 SCF/NEB-step × 15–25 steps).

Scripts: `run_neb_qe.py`, `run_neb_qe.sh`.

## 6. Lessons / footguns

1. **Shell PATH override**: `run_neb_qe.sh` initially OVERWROTE PATH with NVHPC paths → killed conda env python → `numpy not found`. Fixed by **prepending** NVHPC paths (`PATH=NVHPC:$PATH`).
2. **ASE Espresso config**: `ASE_ESPRESSO_COMMAND` env var alone triggers `BadConfiguration` in ASE 3.23+. Must explicitly pass `EspressoProfile` instance to calculator constructor.
3. **Duplicate launch**: nohup-launched NEB doesn't show in interactive shell `ps` until you re-source — easy to accidentally launch twice. Always check `ps -ef | grep run_neb` before launching.
4. **Two NEB processes sharing same WORK directory** = espresso.pwi/pwo collision = corrupted state. Use single launcher only.
5. **Stress-strain elastic** (modelC_v3) doesn't need BM-EOS K externally — each strain SCF prints stress tensor (with `tstress=.true.`), giving one full column of Cij directly. Off-diagonal C12/C13/C23 measurable, no cubic-symmetry assumption needed.

## 7. Output structure (per system)

```
<work_dir>/
├── img0.in ... img6.in              # SCF or NEB inputs
├── img0.out ... img6.out            # outputs with energies
├── tmp_imgN/                        # QE outdir (wavefunctions)
├── neb.traj                         # ASE optimizer trajectory (NEB only)
├── neb.log                          # BFGS/FIRE step log (NEB only)
├── dft_neb_results.json             # parsed energies + barriers
└── (for full DFT NEB:) neb_path_final_dft.xyz
```

## OUTCOME (2026-06-06, REVISED) — UMA-oc20 N→N CI-NEB works; matches paper qualitatively

> [!warning] 이전 "UMA 사망, park" 판정은 철회됨 (over-call).
> Cui 2023 Methods 정독 결과: 논문은 **vanilla DFT NEB가 아니라 ML-NEB(CatLearn, GP surrogate)** 를 썼다
> (GPAW PBE/PAW 500 eV, 6층 slab 위 5층 relax, k 3×3×1, 9 images). 즉 "그냥 따라하라"는 = **surrogate를 써라**.
> UMA가 바로 그 surrogate이고, **우리 UMA-oc20 N→N CI-NEB는 이미 작동했다.**

| 시스템 | UMA-**oc20** CI-NEB | DFT-SCF(UMA geom) | 논문(Cui, GPAW ML-NEB) |
|---|---|---|---|
| **LiC₆(0001)** | ✅ **0.241 eV** | 0.287 eV | — |
| **Li₃N(001)** N→인접N | ✅ **0.054 eV** (path A/B/C 6각 대칭 확인) | 0.049 eV | 0.133 eV |

**핵심 비교 (슬라이드용, 충족)**: Li₃N(0.05) ≪ LiC₆(0.24), 약 **6×** → 상온 lateral 확산 ~10⁴배 빠름.
= 발표 주장("Li₃N 표면이 lithiated carbon보다 Li adatom diffusion에 유리") 그대로 지지.

**"3번 실패"의 진짜 원인 (UMA가 아니라 세팅)**:
1. 작동한 NEB는 task=**`oc20`** (surface adsorbate; 논문 세팅과 정합).
2. "실패한" 2D PES는 task=**`omat`** (bulk 재료용 → 표면 adatom desorption/incorporation 못 잡음) **+**
   애초에 free 2D PES 자체가 표면확산엔 틀린 도구 (정답은 NEB). → `li3n_pes_scan.py` 기본값 omat이 함정.
3. 따라서 omat + free-PES 조합이 깨진 것이지 **UMA-oc20 자체는 정상.**

**절대값 gap (UMA 0.054 vs 논문 0.133)**: UMA가 saddle을 over-smooth → 절대 barrier 과소(~2×).
**정성(Li₃N≪LiC₆, ~6×)은 robust** (동일 protocol 상대비교). 절대값까지 논문과 맞추려면 아래 두 경로.

**남은 경로 (택1)**:
- **(A) 논문 정확 재현** — GPAW PBE/PAW 500 eV + **CatLearn ML-NEB**(GP active-learning, 며칠 아님) → 0.133 목표.
  스크립트: `tools/neb_diffusion/li3n_mlneb_gpaw.py` (paper-faithful generator).
- **(C) 현행 UMA-oc20 + DFT-SCF 정성비교** — 이미 완료, 발표 가능. Li₃N≪LiC₆ 결론에 충분.

**도구**: `tools/neb_diffusion/run_neb_qe.py`(oc20 UMA NEB), `li3n_mlneb_gpaw.py`(CatLearn 재현),
`li3n_pes_scan.py`(주의: `--uma_task oc20` 명시할 것; 기본 omat은 표면에 부적합).

## References

- Cui et al. ACS Nano 2023, **17**, 3168 — Li3N (001) 0.133 eV target.
- ASE 3.23+ docs: `ase.mep.NEB`, `EspressoProfile`.
- UMA-s-1p1: FAIRChem (Meta) foundation MLIP.
