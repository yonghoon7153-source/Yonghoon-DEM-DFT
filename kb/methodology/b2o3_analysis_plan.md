# B₂O₃-doped champion — 추가 분석 plan (배위·결합·testable)

**목표** 챔피언 구조(`db/structures/b2o3_relaxV0.cif`)의 **삼각 BS₃ + free-S²⁻ + phosphate P–O** 서사를 전하·결합세기·전자국재·실험검증으로 다중 확증.
**상태표시** ☐ 대기 · ▶ 실행중 · ✅ 완료

| # | 분석 | 도구 | SCF재활용 | 확증하는 것 | 위치 |
|---|---|---|---|---|---|
| 1 | **ELF** | pp.x plot_num=8 | ✓ | free-S²⁻ lone pair, B–S/P–O 공유 | KISTI |
| 2 | **Bader** | pp.x plot_num=0 + bader | ✓ | B³⁺/free-S²⁻ 전하, +4Li 보상 | KISTI |
| 3 | **Voronoi+bond** | pymatgen | ✗(기하) | BS₃(3) vs PS₄(4), 결합길이 | KISTI/local |
| 4 | **CDD** | pp.x + 원자밀도 | 부분 | 도핑 전하 재분배 | KISTI(보조) |
| 5 | **ICOHP** | LOBSTER (nscf+lobster) | 새 nscf | B–S/P–S/P–O 결합세기 순위 | KISTI+LOBSTER |
| 6 | **NMR** | QE-GIPAW | 새 scf(gipaw pseudo) | ¹¹B(BS₃)/³¹P(PS₄₋ₓOₓ) shift = testable | KISTI+gipaw |
| 7 | **UMA phonon** | phonopy+UMA | ✗ | 동역학 안정성(허수모드 X)+Raman/IR | gabia ✅ |
| **8** | **dielectric/polarizability (ε∞)** | **ph.x epsil-only** | ✓(scf) | **전자 분극률 ε∞ → Li⁺ 차폐·전도 연결, anion 무름↔elastic** | **KISTI** |

**실행 batch**: ① ELF+Bader+Voronoi/bond(빠름,지금) → ② ICOHP(LOBSTER) → ③ NMR+phonon(testable) → ④ CDD(보조).

---

## Batch 1 — ELF·Bader·Voronoi (DOS용 SCF `./tmp/b2o3.save` 재활용)

### ① ② pp.x: ELF + 전하밀도 cube (KISTI sbatch)
```bash
cd /scratch/x3430a02/kgy/b2o3_eos
printf "&INPUTPP\n prefix='b2o3', outdir='./tmp', plot_num=8\n/\n&PLOT\n iflag=3, output_format=6, fileout='b2o3_elf.cube'\n/\n" > pp_elf.in
printf "&INPUTPP\n prefix='b2o3', outdir='./tmp', plot_num=0\n/\n&PLOT\n iflag=3, output_format=6, fileout='b2o3_chg.cube'\n/\n" > pp_chg.in
cat > run_pp.sh <<'EOF'
#!/bin/bash
#SBATCH -J llm_finetuning_v08 -p amd_a100nv_8 -N 1
#SBATCH --ntasks-per-node=2 --cpus-per-task=8 --gres=gpu:2 --time=01:00:00
#SBATCH -o logs/pp_%j.out --comment pytorch
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null||true
conda activate uma 2>/dev/null||true
cd "$SLURM_SUBMIT_DIR"; mkdir -p logs; B=/scratch/x3430a02/kgy/apps/qe-gpu/bin
mpirun -np 1 $B/pp.x < pp_elf.in > pp_elf.out 2>&1
mpirun -np 1 $B/pp.x < pp_chg.in > pp_chg.out 2>&1
echo PP_DONE
EOF
sbatch run_pp.sh
```
→ `b2o3_elf.cube`(VESTA: free-S lone pair), `b2o3_chg.cube`.

### ② Bader (전하 cube 후)
```bash
cd /scratch/x3430a02/kgy/b2o3_eos
bader -p all_atom b2o3_chg.cube && head -30 ACF.dat   # 원자별 charge (USPP valence=근사, 상대비교)
```

### ③ Voronoi + bond length (pymatgen, DFT불필요)
```bash
python3 - <<'PY'
from pymatgen.core import Structure
s=Structure.from_file("/scratch/x3430a02/kgy/Yonghoon-DEM-DFT/db/structures/b2o3_relaxV0.cif")
for sym in ("B","P"):
  for i,a in enumerate(s):
    if a.specie.symbol!=sym: continue
    nb=sorted([(n.specie.symbol,round(n.nn_distance,3)) for n in s.get_neighbors(a,3.2)],key=lambda x:x[1])
    print(sym,i,nb[:5])
PY
```

## Batch 2 — ICOHP (LOBSTER)
```bash
# 1) LOBSTER용 nscf (wf_collect, 대칭끄기) — 기존 nscf_dos 복제해 수정
#    (repo의 analyze_per_bond_icohp.py / 이전 Nd LOBSTER 워크플로 재사용)
cd /scratch/x3430a02/kgy/b2o3_eos
cat > lobsterin <<'EOF'
COHPstartEnergy -12
COHPendEnergy 6
basisSet pbeVaspFit2015
cohpGenerator from 1.4 to 2.0 type B type S
cohpGenerator from 1.4 to 1.9 type P type O
cohpGenerator from 1.9 to 2.4 type P type S
cohpGenerator from 3.4 to 4.2 type B type S
EOF
# 2) lobster 실행 → ICOHPLIST.lobster (B-S/P-O/P-S/free-S ICOHP)
#    lobster   (PATH에 LOBSTER 바이너리 필요)
```
→ **결합세기**: |ICOHP| 클수록 강결합. 예상: P–O ≫ B–S(BS₃) > P–S > free-S(약) → "free-S 먼저 산화"의 결합론적 근거.

## Batch 3 — testable

### ⑥ NMR (QE-GIPAW) — **gipaw pseudo 필요**(USPP 아님)
```bash
# scf (gipaw-호환 pseudo로 재SCF) → gipaw.x job='nmr'
cat > b2o3_nmr.in <<'EOF'
&inputgipaw
  job='nmr', prefix='b2o3', tmp_dir='./tmp'
  q_gipaw=0.01
/
EOF
# mpirun gipaw.x < b2o3_nmr.in > b2o3_nmr.out   (gipaw.x + GIPAW pseudo 필요)
```
→ ¹¹B(삼각 BS₃ 시그널)·³¹P(PS₄/PS₄₋ₓOₓ)·⁷Li shift → **실험 NMR과 직접 대조**.

### ⑦ UMA phonon (gabia, phonopy+UMA)
```bash
cd /data/work/b2o3md
phonopy --qe -d --dim="1 1 1" -c POSCAR_b2o3   # 변위 생성 (또는 ASE+phonopy)
# 각 변위에 UMA force 계산 → phonopy -f → band.conf → 허수모드 체크 + Raman/IR
```
→ **허수모드 없음 = 챔피언이 진짜 국소최소**(metastable 보강) + BS₃·free-S·P–O **진동모드(Raman/IR testable)**.

## Batch 4 (보조) — CDD
전하밀도차 ρ(doped)−ρ(ref): fragment/promolecule 밀도 필요(추가 SCF). ELF가 lone pair를 직접 보여주므로 우선순위 낮음 — Batch1·2 후 필요시.

---
## Batch 5 — 유전율/분극률 (ε∞) — **elastic과 짝**

> **왜.** 고체전해질에서 "polarizability"는 사실상 **유전텐서 ε**(전자분극 ε∞ + 이온분극 → 정적 ε₀). ε는 **Li⁺를 차폐**해 이동장벽·전도에 직결되고, **무른·분극성 큰 음이온(S²⁻)** 이 곧 **낮은 전단탄성 G** 의 원인과 같은 물리(음이온 전자구름의 변형성) → **elastic과 한 짝으로 보는 게 맞음**. Born charge Z*는 역학(phonon)↔전기(유전)를 잇는 다리.

**정직한 비용 등급 (USPP SSSP scf 재활용 기준):**
| 등급 | 양 | 방법 | 비용 | 비고 |
|---|---|---|---|---|
| **무료(지금)** | ε∞ 대략값 | Clausius–Mossotti(조성+V+이온 α) | 0 | **ε∞~3.9–5.7**(S²⁻ α의존). 분극의 **78% S²⁻+19% Cl⁻**, 양이온~0.7%. O²⁻ 작음(hard) → **O 도핑이 ε∞ 소폭↓**. 절대값 아닌 경향용 |
| **★ 권장(중저비용)** | **ε∞ 텐서(전자)** | **ph.x `epsil=.true., trans=.false.`** @Γ | E-field 3섭동(~3×SCF) | **Raman/Born보다 훨씬 쌈**(3N 아님). USPP scf 재활용 |
| 고비용(보류) | Born Z* + 정적 ε₀ | ph.x `epsil+trans`(또는 zeu) | 3N 섭동 = 전체 Γ DFPT = Raman급 | 우리가 이미 보류한 Raman 비용군. reviewer 요구시 |

### ⑧ ε∞ (전자 유전텐서) — ph.x epsil-only (KISTI, scf 재활용)
```bash
cd /scratch/x3430a02/kgy/b2o3_eos
ls apps_bin=/scratch/x3430a02/kgy/apps/qe-gpu/bin/ph.x   # 0) ph.x 빌드 존재 확인(GPU 빌드에 없을 수 있음)
# scf save 필요(DOS용 scf). nscf로 덮였으면 quick scf 재실행 후 진행.
cat > eps.in <<'EOF'
&inputph
  prefix='b2o3', outdir='./tmp'
  fildyn='b2o3_eps.dyn'
  epsil=.true.      ! 전자 유전텐서 ε∞ (clamped-ion)
  trans=.false.     ! phonon/Born 안함 → 싸게(E-field 3섭동만)
  tr2_ph=1.0d-14
/
EOF
# sbatch 래퍼에서: mpirun ph.x < eps.in > eps.out  → eps.out 의 "Dielectric constant in cartesian axis" 3x3
```
- **결과**: ε∞ 3×3 텐서(이방성 포함). trace/3 = 등방 평균. → CM 추정과 대조 + DFPT 정량값.
- **pseudo 주의**: 현 QE(≥6.x)는 USPP로 epsil 지원. 만약 빌드가 거부하면 **NC-pseudo 1회 재SCF**(ONCV) 후 epsil.
- **GPU 주의**: QE-GPU에 `ph.x`가 없을 수 있음 → 있으면 그걸로, 없으면 **CPU QE ph.x** 또는 **pw.x `lelfield`(유한장 Berry-phase)** 대안(작동하는 pw.x GPU 사용, 단 field방향 k조밀 필요).
- **elastic 연결**: ε∞(음이온 분극) ↔ relaxed-ion G(음이온 무름) 같은 기원 → "도핑이 S²⁻ 일부를 hard O로 → ε∞ 소폭↓ & 골격 강성↑" 한 서사로 묶임.

## 결과 종합 목표
Bader(전하)+ICOHP(결합세기)+ELF(국재) → **BS₃/free-S/phosphate 3중 확증 그림·표** 1세트 → NMR/phonon으로 **testable**까지. 각 결과 붙여주시면 figure+표+kb 정리.
