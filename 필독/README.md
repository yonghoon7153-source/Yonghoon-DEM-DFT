# 🚨 필독 — Verified Production Code 모음

> **검증된 production code + literature reference 의 local mirror.**
> KISTI/gabia 의 production folder가 cleanup 되어도, 채팅 방이 터져 새 브랜치로 가도 ==**여기에 남음**==.

---

## ⛔ 새 브랜치 / 새 session 에서의 절대 규칙

1. ==**코드 생성 금지**==. 사용자에게 "이 작업의 verified script 어디 있나요?" 먼저 묻기.
2. 사용자가 "없음"이라고 답할 때만 ==**그제야 생성 허용**==. 즉시 CODE_INVENTORY.md 갱신.
3. 같은 작업의 새 .py "비슷한 거 짜드릴게요" ==**금지**== — `compute_cij` factor 2 누락, ntyp 하드코딩, safe wrapper false-positive 같은 hidden bug가 반복됨.
4. `필독/literature/` 의 paper 노트는 method 결정 전 ==**참고 필수**==.

---

## 사용 규칙

1. ==이 폴더의 .py 가 **paper-quality verified**==. 새로 작성 금지.
2. ==CODE_INVENTORY.md 와 cross-reference== — 검증 status, bug history, 결정 사유.
3. 변경 시 ==**KISTI/gabia 양쪽 update**== (diverge 금지).
4. 새 파일 추가 시 ==**검증 후 README + CODE_INVENTORY 양쪽 갱신**==.

---

## Pipeline 흐름 (paper #1)

```
champion CIF 만들기            B0 결정              post-processing
──────────────────────         ────────────────     ──────────────
[1] halogen enum + Li         [4] BM3 fit         [5] tight SCF
    screen + anneal               + V0 select         NSCF / DOS
    ↓                             ↓                   PDOS / Bader
    champion.xyz/.cif         V0 cell + coords       elastic Cij
    ↓                             ↓                   adhesion
[2] MLIP EOS scan
    (V0 grid 추천)
    ↓
[3] DFT EOS 11 vol
    (각 vol relax)
```

---

## 폴더 구조

```
필독/
├── README.md                   ← 이 파일
├── step1_halogen_li_anneal/    ← halogen enum + Li screen + 500K anneal
│   ├── comp1_lpscl/            (TODO: step1_v2.py + anneal_top1/top2to5)
│   ├── comp2_lpscbr/
│   │   ├── step1_v2.py         (Stage 1 halogen 420 cfg + Stage 2 Li 20 + Stage 3 100ps anneal)
│   │   └── anneal_champion.py  (best 하드코딩 + 100ps anneal — 실제 production)
│   └── modelC_lpsc16/          (TODO scp from KISTI)
│
├── step2_mlip_eos/             ← MLIP volume scan + BM3 fit
│   ├── comp1_lpscl/            (TODO scp)
│   ├── comp2_lpscbr/
│   │   └── step2_mlip_eos.py   (96-108% × 13 vol, BM3 fit, V0 grid 추천)
│   └── modelC_lpsc16/          (TODO scp)
│
├── step3_dft_eos/              ← DFT 11 volume QE input 생성
│   ├── comp1_lpscl/
│   │   └── step3_dft_eos.py    (Li6PS5Cl, ntyp=4 fixed)
│   ├── comp2_lpscbr/
│   │   └── step3_dft_eos_comp2.py (Li6PS5Cl0.5Br0.5, auto N_TYP=5)
│   └── modelC_lpsc16/          (TODO scp)
│
├── step4_bm3_v0/               ← DFT EOS BM3 fit + V0 closest grid
│   └── bm3_fit_eos.py          (generic utility, 모든 comp 공용)
│
└── step5_postproc/             ← V0 structure에서 SCF/NSCF/DOS/PDOS/Bader/elastic
    ├── comp1_lpscl/            (TODO)
    ├── comp2_lpscbr/           (TODO: run_full_pp.sh, run_comp2_v2_bader.sh, scf/nscf/dos/projwfc.in)
    └── modelC_lpsc16/          (TODO)

literature/                     ← Paper reference DB (mirror of db/literature + kb/papers literature notes)
├── README.md                   ← index of papers + add-paper procedure
├── refs.json                   ← 37 references machine-readable DB
├── camacho_forero_2020.md      ← ⭐ paper #2 sandwich Wadh SLAB method anchor
├── komatsu2022.md              ← ⭐ paper #2 BULK thermo anchor LPSCl/LiNiO2 (-424 meV/atom)
├── verified_refs_2026_05.md    ← 8 user-verified paper #1 refs (komatsu attribution corrected)
├── adhesion_literature_review.md ← adhesion DFT method review (entry 6 corrected)
├── narrative_with_literature_steps.md ← paper #1 Section 2-4 writing scaffold
├── origin_adhesion_guide.md    ← Origin bar chart settings
├── reviewer_qa_methods.md      ← Q1-Q7 reviewer 답변 template
├── choi2025_adoption_guide.md  ← Choi 2025 adoption (figure style, ack format)
└── zhao2025_critique.md        ← Zhao 2025 critical analysis (Park 답변용)

adhesion/                       ← Paper #2 SE/NCM Wad production code (mirror of KISTI)
├── README.md                   ← v10 method + run instructions + time estimates
├── phase2a_v10_sandwich.py     ⭐ Camacho-Forero sandwich + NCM middle FixAtoms hybrid
└── watchdog_phase2a_v10.sh     ← KISTI auto-restart wrapper
```

---

## Step 별 상세

### Step 1 — Halogen + Li enum + 500K Anneal

> **목적**: random Cl/Br/Li 배치 → MLIP screen 으로 ==champion 구조== 찾기.
> **모델**: UMA-s-1p1 (fairchem)
> **출력**: `comp{X}_v2_champion.xyz` + `.cif` + `pipeline_v2_results.json`

#### `step1_v2.py` (comp2 verified)
- **Stage 1**: halogen enum
  - comp2: 2 Cl + 2 Br + 4 S in 8 free sites = ==C(8,2)×C(6,2)=420 raw configs==
  - 각 config × ==1 rep Li config== (Li_configs[0], seed 42) → MLIP relax (LBFGS fmax=0.01, 200 steps)
  - Top 5 halogen 선택
- **Stage 2**: Li screen
  - best halogen × ==20 random Li configs== (seed 42, choice(48,24)) → MLIP relax
  - Top 1 Li 선택
- **Stage 3**: anneal
  - best halogen + best Li → MaxwellBoltzmann 500K → ==Langevin 500K 100ps (friction 0.01, dt=1fs)== → ==Langevin 300K 10ps quench (friction 0.05)== → LBFGS final relax (fmax=0.005, 300 steps)
  - 결과: champion.xyz/.cif

#### `anneal_champion.py` (comp2 verified)
- step1_v2.py 결과의 ==best_cl/br/li 하드코딩== + 100ps anneal 재실행
- ⚠️ ==KISTI 원본은 50ps 표기, 실제 log는 100ps== — local 본은 100ps로 통일
- comp2 production champion.xyz는 ==이 파일이 만든 것== (Apr 27 21:24)

#### Top 1 selection 검증 (comp1 evidence)
- comp1 anneal_top2to5.log: rank 2-5 best E = -217.042
- comp1 rank 1 anneal E = ==**-217.533**== (Top 1)
- ==**ΔE = 491 meV**== — Top 1 명백 winner ✓
- comp2 Top 2-5 미검증 (시간되면 nd 후 확인 가능)

---

### Step 2 — MLIP EOS

> **목적**: champion에서 ==13 volume MLIP scan== → BM3 fit → ==**DFT scan용 V0 grid 추천**==
> **모델**: UMA-s-1p1
> **출력**: 콘솔에 V0_pct ± 5 grid

#### `step2_mlip_eos.py` (comp2 verified)
- 입력: `comp2_v2_champion.xyz`
- LBFGS refine (fmax=0.005)
- Volume scan: ==96~108% × scale_atoms=True× LBFGS (fmax=0.01)==
- BM3 fit: scipy.curve_fit, initial guess (E_min, V_at_min, B0=20 GPa, B0'=4)
- 출력: B0(GPa) = B_fit × 160.2, V0, B0', R²
- 다음 step 추천: `v{round(V0_scale*100)} ± 5` (11 grid)
- ==v1 reference 25.8 GPa (comp2 v1)== 표기 ✓ fixed

---

### Step 3 — DFT EOS input 생성

> **목적**: champion fractional coords + scaled cell → ==QE relax input 11개 .in==
> **다음**: KISTI GPU에서 11 SCF relax 실행

#### `step3_dft_eos_comp2.py` (comp2 verified)
- 입력: `comp2_v2_champion.xyz`
- ==N_TYP = len(set(species))== auto count (Li/P/S/Cl/Br = 5)
- 11 volume × scale = (v_pct/100)^(1/3)
- 출력: `comp2_v2_eos_v{098-108}.in` + `tmp_v###/` 폴더
- ATOMIC_POSITIONS (crystal) — fractional coords 보존 (cell만 scale)

#### `step3_dft_eos.py` (comp1 fixed)
- 입력: `comp1_v2_rank1_annealed.xyz`
- ⚠️ ==KISTI 원본은 ntyp=3 하드코딩 bug== (실제 4종) — sed로 4 정정 (2026-05-01)
- ATOMIC_SPECIES: Li/P/S/Cl (4종)
- pseudo: SSSP_1.3.0_PBE_efficiency

#### DFT 공통 settings (실제 production)
| 설정 | 값 |
|---|---|
| ecutwfc / ecutrho | ==52 / 520 Ry== (CLAUDE.md 60/480와 다름) |
| K-grid | ==2×2×2== (EOS coarse) |
| conv_thr | 1e-8 |
| forc_conv_thr | 1e-4 |
| mixing_beta | 0.2 |
| nosym | .true. (BFGS 안정) |
| smearing | mv 0.01 Ry |

---

### Step 4 — BM3 fit + V0 closest grid

> **목적**: DFT 11 EOS 결과로 BM3 fit → V0 결정 → ==closest grid의 cell + coords를 V0 structure로 사용==
> **출력**: `BM3_fit.json` (V0, B0, B0', R², closest_grid, raw_data)

#### `bm3_fit_eos.py` (이 repo에서 새로 작성, generic)
- 입력 glob (예: `comp2_v2_eos_v*.out`) → ase.io.read espresso-out
- BM3 fit + closest grid 자동 선택
- ⚠️ ==KISTI에 .py 없음== (hand-done) — 이건 ==자동화 utility== (재현 가능하게)
- 사용 예:
  ```bash
  python bm3_fit_eos.py --pattern 'comp2_v2_eos_v*.out' \
                        --label comp2_v2 --out comp2_v2_BM3_fit.json
  ```

#### 검증 — comp2 v2 production 결과
- V0_fit = 983.578 Å³, B0 = 25.74 GPa (db 25.8 매칭 ✓)
- closest = v103 (V=984.94, ==Δ=0.14%==)
- v103의 cell + relaxed coords → `v2_postproc/comp2_v2_V0.xyz` ✓

---

### Step 5 — Post-processing

> **목적**: V0 structure에서 ==tight SCF / NSCF / DOS / PDOS / Bader / elastic==
> **출력**: paper-quality observables (band gap, charge, bond, Cij)

#### TODO — production scripts scp 필요
- `run_full_pp.sh` — SCF → NSCF → DOS → projwfc 자동화
- `run_comp2_v2_bader.sh` — pp.x → bader_lnx_64
- `scf.in`, `nscf.in`, `dos.in`, `projwfc.in` (V0 cell + coords)
- ==Post-processing 은 K-grid 더 dense (6×6×6 cubic / 6×6×3 rhombo)==

---

## 검증 status (2026-05-01 기준)

| step | comp1 | comp2 | modelC |
|---|:-:|:-:|:-:|
| 1 enum + anneal | ⏳ TODO | ✅ | ⏳ TODO |
| 2 MLIP EOS | ⏳ TODO | ✅ | ⏳ TODO |
| 3 DFT EOS | ✅ (fixed) | ✅ | ⏳ TODO |
| 4 BM3 + V0 | ✅ generic | ✅ generic | ✅ generic |
| 5 post-proc | ⏳ TODO | ⏳ TODO | ⏳ TODO |

✅ = local 저장 + 검증 끝
⏳ TODO = KISTI에서 cat/scp 필요

---

## KISTI 원본 위치 reference

| comp | path |
|---|---|
| comp1 | `kisti:/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp1_lpscl/` |
| comp2 | `kisti:/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/` |
| modelC | `kisti:/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/modelC_lpsc16/` |
| post_relax (comp1 0K elastic) | `kisti:/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/` |

## gabia 위치 (comp2 v2 0K Cij 작업용)

| 작업 | path |
|---|---|
| comp2 v2 0K Cij scan | `gabia:/data/work/bml/manuscript_support/comp2v2_dft_0K/` |
| 600K MLIP elastic | `gabia:/data/work/bml/manuscript_support/comp2v2_mlip_elastic*.py` |

---

## 변경 history

| 날짜 | 변경 |
|---|---|
| 2026-05-01 | 초기 mirror 생성 (comp2 step 1-3 + comp1 step 3 + bm3_fit_eos) |
| 2026-05-01 | comp1 step3 ntyp=3→4 sed fix |
| 2026-05-01 | comp2 step2 v1 ref 26.2→25.8 sed fix |
| 2026-05-01 | step1/step2/.../step5 폴더 구조로 재정렬 |
