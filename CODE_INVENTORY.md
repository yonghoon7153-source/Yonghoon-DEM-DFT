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

### B1. `mlip_snapshot_elastic_comp2v2.py` ❓ UNKNOWN
- **위치**: gabia (확인 필요)
- **목적**: MD 600K → 5 snapshot → quench → relaxed-ion Cij
- **검증 필요**: ==**사용자 우려 — 이것도 잘못됐을 수 있음**==
- **검증 방법**:
  - comp1 v1 600K MLIP → 29.1 GPa (db값) 재현되는지
  - comp2 v2 600K → 34.7 GPa (db값) 재현되는지
- **TODO**: 검증 전까지 ==사용 보류==

### B2. `comp1v2_mlip_elastic.py` ❓ UNKNOWN
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_mlip_elastic.py`
- **목적**: comp1 v2 MLIP elastic
- **검증 필요**

### B3. `comp1v2_uma_elastic.py` ❓ UNKNOWN
- **위치**: KISTI `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_uma_elastic.py`
- **목적**: UMA model elastic
- **검증 필요**

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

### F1. v5 surface MQA scripts ❓ UNKNOWN
- **위치**: 확인 필요
- **목적**: SE/NCM 계면 work of adhesion, surface MQA protocol
- **검증**: db에 결과 있음 (Wad_aJ_r10nm 등) but script 검증 필요

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
