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

## K. ✅ 해결 — comp2 v2 production은 KISTI 에 있음

```
/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/
```

(gabia의 `comp2_v2_V0.xyz` 는 KISTI에서 transfer된 copy)

### Full pipeline 파일들 (KISTI)
- `step1_enumerate_halogen.py` — halogen enum (단순 버전)
- `step1_v2.py` — halogen + Li screen + Li anneal (full 버전)
- `step2_mlip_eos.py` — MLIP EOS
- `step3_dft_eos.py` + `step3_dft_eos_comp2.py` — DFT EOS scan
- `anneal_champion.py` — anneal script
- `comp2_v2_champion.cif/.xyz` — anneal output
- `v2_postproc/comp2_v2_V0.xyz` — post-EOS V0
- 12 volume EOS scan (v098 to v108) + tmp_v###/.save
- PDOS files (128 pdos_atm)
- Bader charge.dat / charge.cube / BM3_fit.json
- `run_comp2_v2_bader.sh`

### narrative 영향
==comp2 v2도 full anneal pipeline 거침== → 21% v1→v2 stiffening 정량 결과 ==paper narrative 유지 valid== ✓.

### TODO — 어느 step1을 썼는지 확인
- `step1_enumerate_halogen.py` (단순 halogen enum)
- `step1_v2.py` (full 3-stage)
둘 다 있는데 실제 production 사용된 것 추적 필요.

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
