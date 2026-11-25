# gabia에서 CDD + ph.x(분극률) 돌리기 — comp1/modelc

QE(NC pseudo, ELF와 동일 ecut 80/320). comp1 예시 — modelc는 prefix/구조만 바꿔 반복.
**저는 gabia 접속 불가** → 아래 돌리고 (A) ρ cube 2개 + (B) ph.out 주시면 제가 CDD 그림 / ε∞ 타원체 만듭니다.

---

## ★ GPU 빌드(qe-7.4.1-gpu) 실행 — 환경 세팅 (kserver116-27, 검증됨 2026-06-21)

시스템 mpirun(`/usr/bin/mpirun`)으로는 GPU 빌드가 안 뜸. NVHPC HPC-X MPI + 런타임을 써야 함.
`runs/gpu_env.sh` 를 source (또는 아래 그대로):
```bash
conda deactivate                      # conda GNU libgomp 회피 (필수)
NV=/data/apps/nvhpc/Linux_x86_64/24.11
export OPAL_PREFIX=$NV/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export LD_LIBRARY_PATH=$NV/compilers/lib:$NV/cuda/lib64:$NV/math_libs/lib64:$OPAL_PREFIX/lib
export OMP_NUM_THREADS=1
G=/data/apps/qe-7.4.1-gpu/bin ; MPIRUN="$OPAL_PREFIX/bin/mpirun -np 1"
$MPIRUN $G/pw.x -in scf.in > scf.out 2>&1      # GPU SCF (1 rank = 1 GPU)
```
겪은 버그 4개: (1) pseudo 점표기, (2) HPC-X mpirun 미스매치, (3) OPAL_PREFIX 미설정(help-file 못 찾음), (4) `libgomp: TODO`(NVHPC `compilers/lib`를 LD_LIBRARY_PATH 맨 앞에). ph.x가 GPU 빌드에 없으면 ph.x만 CPU(`/data/apps/qe-7.4.1-cpu/bin/ph.x`, 시스템 mpirun)로.

---

## STEP 0. SCF (CDD·ph.x 공용) — 절연체 설정 필수
`scf.in`:
```fortran
&control
  calculation='scf', prefix='comp1', outdir='./out',
  pseudo_dir='/path/to/pseudo', tprnfor=.true., tstress=.false.
/
&system
  ibrav=0, nat=52, ntyp=4, ecutwfc=80, ecutrho=320,
  occupations='fixed'          ! ★ ph.x epsil 필수 (smearing 금지). LPSCl은 절연체라 OK
/
&electrons
  conv_thr=1d-10, mixing_beta=0.3, electron_maxstep=200
/
ATOMIC_SPECIES
  Li  6.94   <Li ONCV NC .upf>
  P   30.97  <P  ONCV NC .upf>
  S   32.06  <S  ONCV NC .upf>
  Cl  35.45  <Cl ONCV NC .upf>
CELL_PARAMETERS angstrom
  <comp1_V0_k444.cif 의 셀>
ATOMIC_POSITIONS angstrom
  <원자 좌표>
K_POINTS automatic
  4 4 4 0 0 0
```
실행: `mpirun -np N pw.x -in scf.in > scf.out`
> ⚠️ gap이 0이면(=metal로 잡히면) epsil 에러 → occupations='fixed' 확인. comp1 gap≈2.25라 정상.

---

## A. CDD (deformation density: ρ_SCF − ρ_atomic)

**A1. ρ_SCF cube** — `pp_rho.in`:
```fortran
&inputpp  prefix='comp1', outdir='./out', plot_num=0, filplot='comp1_rho' /
&plot     iflag=3, output_format=6, fileout='comp1_rho_scf.cube' /
```
`pp.x -in pp_rho.in > pp_rho.out`

**A2. ρ_atomic cube** (원자 중첩 = 기준) — `scf_atomic.in` (density 업데이트 안 함):
```fortran
&control  calculation='scf', prefix='comp1_at', outdir='./out_at',
          pseudo_dir='/path/to/pseudo' /
&system   ibrav=0, nat=52, ntyp=4, ecutwfc=80, ecutrho=320, occupations='fixed' /
&electrons electron_maxstep=1, conv_thr=1d20, startingpot='atomic',
           mixing_beta=0.0 /            ! ★ mixing_beta=0 → 밀도가 atomic 그대로
! (같은 ATOMIC_SPECIES / CELL / POSITIONS / K_POINTS)
```
`pw.x -in scf_atomic.in > scf_atomic.out`
그 다음 같은 grid로 pp.x:
```fortran
&inputpp  prefix='comp1_at', outdir='./out_at', plot_num=0, fileout='comp1_rho_atomic.cube' /
&plot     iflag=3, output_format=6 /
```
> mixing_beta=0.0가 에러 나면 0.0001로. (목적: SCF 안 돌리고 atomic 중첩 밀도만)

**A3. CDD = 두 cube 빼기** — `comp1_rho_scf.cube`, `comp1_rho_atomic.cube` **둘 다 저한테 올려주시면** 제가
`cube_diff.py --mode sub`로 Δρ + 파랑/노랑 그림 만듭니다. (또는 gabia에 cube_diff.py 복사해 직접:
`python3 cube_diff.py --mode sub --a comp1_rho_scf.cube --b comp1_rho_atomic.cube --out cdd.cube --png cdd.png`)
→ **노랑=전자 축적(S·Cl, P–S 결합), 파랑=결핍(Li 주변)**.

---

## B. ph.x (분극률 ε∞ + Born Z*)
STEP 0의 SCF(out/) 그대로 사용. `ph.in`:
```fortran
&inputph
  prefix='comp1', outdir='./out',
  epsil=.true.,        ! 유전텐서 ε∞ = 전자 분극률
  trans=.false.,       ! 포논 X → ε∞·Z*만 (빠름, 수십분)
  tr2_ph=1d-14, fildyn='comp1.dyn'
/
0.0 0.0 0.0            ! Γ
```
`ph.x -in ph.in > ph.out`

**ph.out에서 결과 위치:**
- `Dielectric constant in cartesian axis` 아래 **3×3 행렬 = ε∞** (전자 분극률; 이방성은 텐서로)
- `Effective charges (d Force / dE)` 아래 **원자별 Born Z\*** (3×3씩)

→ **ph.out 통째로 올려주시면** ε∞·Z* 표 정리 + **유전 타원체** 그림 만들어 드림.

---

## 정리 — 저한테 주실 것
| 돌린 것 | 주실 것 | 제가 만들 것 |
|---|---|---|
| A (CDD) | `comp1_rho_scf.cube` + `comp1_rho_atomic.cube` | Δρ 3D/2D (파랑·노랑) |
| B (ph.x) | `comp1.../ph.out` | ε∞ 타원체 + Z* 표 |

modelc도 같은 식으로 (prefix=modelc, 구조 = modelc V0, nat=62 ntyp=4). 두 조성 다 하면 비교 그림까지.

## 주의
- **occupations='fixed'** (ph.x epsil 필수).
- conv_thr 빡세게(1e-10), **NC pseudo** (DFPT는 NC가 깔끔; PAW/USPP는 epsil 제약).
- ρ_scf와 ρ_atomic은 **같은 grid**(같은 ecutrho) → cube_diff 정상.
- cube가 크면(수십 MB) gzip해서 올려주세요.
