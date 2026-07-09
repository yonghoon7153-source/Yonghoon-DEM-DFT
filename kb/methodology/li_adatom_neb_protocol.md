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

## OUTCOME v3 (2026-06-06, FINAL) — proper-slab UMA dig: topology inversion confirmed

> [!important] 결정판. v2의 0.054도 **thin-slab artifact로 폐기**. 제대로 된 논문-충실 slab으로 재조사한 결과.

**셋업 (논문 Cui 2023 충실 재현)**: Li3N(001) **6층 N-노출 Li2N termination**, 3×3, 243 atoms, top 5 relax,
UMA-s-1p1. (`li3n_uma_investigate.py`, `build_li3n_001(terminate='N')`)

**① 흡착 site 에너지 (UMA, oc20 & omat 동일 순서)**:

| site | E_bind (oc20) | 순위 |
|---|---|---|
| hollow | −2.093 | 🥇 **UMA 최소** |
| bridge | −2.073 | 🥈 |
| on-N | −1.903 | 🥉 **최약** |
| *paper on-N* | *−3.44* | *DFT 최소* |

→ **Topology inversion**: UMA는 hollow 최소, on-N 최약. 논문 DFT는 on-N이 최소(우물). oc20·omat 둘 다 동일.

**② NEB (각 방법 자기 최소점끼리)**:

| 경로 | barrier | 의미 |
|---|---|---|
| hollow → hollow_adj | **0.237 eV** | UMA 정직한 장벽 (자기 최소점 hollow 기준) |
| on-N → on-N_adj | **0.025 eV ≈ 0** | on-N 끝점이 off-site로 relax → **UMA에 on-N 우물 없음 확증** |

**메커니즘 (왜 깨지나)**: Li adatom(δ+)–N³⁻ **on-top 정전기+전자전달 결합**이 DFT의 on-N 우물(0.133)을 만듦.
단거리 MLIP인 UMA는 이 전하이동 on-top 결합을 못 담아 → adatom을 generic하게 hollow로 떨굼(= LiC6식 거동).
그래서 (a) 최소 site가 틀리고(hollow), (b) 장벽이 carbon급(0.237 ≈ LiC6 0.241)으로 부풀려져 **"Li3N이
carbon보다 안 빠르다"는 가짜 결론**을 줌.

**왜 LPSCl/LiC6은 멀쩡한데 Li3N만**: LPSCl = 평형 벌크·풍부 화학(sulfide/halide)·상대비교 → in-distribution.
LiC6 = Li가 hollow 선호(약한 상호작용) → UMA가 맞춤(0.241 vs DFT 0.287). Li3N = 강한 ionic nitride·극성표면·
on-top 전하이동·0.13 eV 미세신호 → out-of-distribution. (`why-uma-fails-li3n` 분석)

**결정**:
- **Li3N 장벽은 UMA로 불가** (0.054도 0.237도 신뢰 X — topology 자체가 틀림). **UMA를 path-finder로도 쓰면 안 됨**(hollow 오도).
- **루트 = on-N → 인접 on-N** (논문 + 화학 + UMA의 "on-N 우물 없음"이 역설적 확인). 절대값은 **DFT** 필요.
- 며칠 안 날리는 확정법: **DFT static 3방**(on-N/hollow/bridge relax)으로 DFT 최소 site 재확인(몇 시간) → on-N 확정 시 **CatLearn ML-NEB**(`li3n_mlneb_gpaw.py`)로 0.133.
- 발표 수치: **Li3N 0.133(문헌) vs carbon 0.24–0.30 → ~2×** (옛 6×·10⁴배 주장은 thin-slab artifact, 폐기).

**도구**: `li3n_uma_investigate.py` (sites/neb/sweep, term/두께/task knob), `li3n_mlneb_gpaw.py` (논문 ML-NEB).


- ASE 3.23+ docs: `ase.mep.NEB`, `EspressoProfile`.
- UMA-s-1p1: FAIRChem (Meta) foundation MLIP.

---

## 2026-07-09 UPDATE — revision 캠페인: NEB 완전 폐기, PES-직접 프로파일로 대체

**배경**: 리뷰어가 reaction coordinate 상세를 요구 → 측정 기반으로 재구축 (mirrored-spline 0.054/0.102 폐기).

**확보한 것 (UMA, kserver116)**: 12×12 구속 PES(`li3n_pes_uma.py`, 점별 adatom z-이완 + 상판 이완) → 등가 최소 6개,
minimax MEP **barrier 0.156 eV**, saddle = **on-top-Li**(frac 0.750,0.250; env Li:0.54Å) — on-N이 아님.

**NEB 4연속 실패 계보 (전부 다른 병리 — 이 계에서 NEB 자체가 부적합하다는 증거)**:
| 시도 | 설정 | 실패 모드 |
|---|---|---|
| v1 (×3) | IDPP 보간 | on-top-N 위로 보간 → 폭주 |
| v2a | PES-seed | seed가 PBC를 감아 6 Å 이미지 갭 → 가짜 8.95 eV |
| v2b | +unwrap | ① linspace 중복 이미지 ② minimax 시드가 중간 최소점 관통(2-hop) ③ **자유 상판이 on-top-Li 안장 근처에서 재구성** → 8.95 eV 재폭주 + 내부 이미지가 끝점보다 0.46 eV 낮아짐 |
| v3 | 1-hop 절단 + **전 슬랩 동결**(3-DOF) | 수치 수렴(fmax 0.046)했으나 **물리 무효**: 동결 슬랩이 초기 site의 이완 기억을 보존 → **등가 끝점이 +0.73 eV 비대칭**(장벽 0.156의 4.7배), 경로 3.41→11.6 Å 미끄러짐, BARRIER 1.544 = 인용 금지 |

**교훈 (일반화)**: 무른 이온성 표면(Li₃N)에서 MLIP-NEB는 양쪽 함정 — **자유 슬랩 = 재구성 폭주, 동결 슬랩 = 초기-site 기억 편향**.
견고한 객체는 **구속 PES 스캔 그 자체** (점별 국소 이완 = 단열 프로파일, 대역폭 넓은 재구성 봉쇄).

**대체 산출물**: `li3n_mep_profile.py` — pes_grid.csv에서 minimax MEP를 따라 E(s)를 직접 추출(1-hop 절단, s = 실공간 경로길이)
→ `mep_profile.csv/png` (계산점 마커, 스플라인 없음). **리뷰어 패키지 = pes_map.png(2D) + mep_profile.png(1D) + P0 DFT 장벽.**

**DFT 중재자 (진행 중)**: `dft_p0/` p0_min(자유 이완)·p0_saddle(xy-pin 이완) — 위 §의 "UMA site topology 불신" 결론과 정합:
UMA-min이 DFT에서 다른 site로 흘러가면 그것대로 기록 (DFT가 최종 심판, UMA는 지형 정찰). 장벽 = (E_saddle−E_min)×13.6057 vs 문헌 0.133 eV.

### 2026-07-09 追記 — LiC₆에선 반대: PES-격자 실패, NEB가 정답 (방법-재료 궁합)

SI 비교군용으로 LiC₆(0001)에 같은 12×12 구속 PES를 시도 → **부적합 판정**:
- 반셀 이동점 E[6,0]=0.59 eV (Li 초격자 대칭이면 ~0이어야) — slab의 삽입-Li 배열이 4.26 Å 부분주기를 안 가짐
- 최소점들이 전부 +0.36 eV 이상 (등가 hollow 부재), E[6,6]=5.4 eV 병리점
- 원인: 매 grid점을 A0 슬랩 상태에서 시작하는 구속이완이 **무른 삽입-Li 부격자의 이완 이력(hysteresis)**을
  80 스텝 안에 못 털어냄 (Li₃N의 뻣뻣한 표면에선 문제없던 것)

**교훈 (일반화)**: 표면 확산 계산의 방법 선택은 재료-의존 —
| | Li₃N (001) | LiC₆ (0001) |
|---|---|---|
| NEB | ❌ 4연속 실패 (재구성/기억 편향) | ✅ 0.241 eV, 대칭 끝점, dip 없음 (검증됨) |
| 구속 PES-격자 | ✅ 0.156/0.171 eV (측정 MEP) | ❌ 이력 오염 (본 절) |
→ SI 패널: Li₃N = PES/dense-scan 산출물, LiC₆ = 기존 NEB 산출물 (각자 잘 듣는 방법; 둘 다 DFT 도장 예정 —
Li₃N은 P0 pair, LiC₆는 기존 "DFT SCF on UMA" 0.287 + 추후 P0-pair 업그레이드 옵션).
LiC₆ PES 산출물(/data/work/runs/lic6_pes_uma)은 인용 금지, 이 진단의 증거로만 보존.
