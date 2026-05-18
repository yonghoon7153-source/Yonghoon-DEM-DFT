# 🚨🚨🚨 최상위 규칙 — 새 브랜치 / 새 session 진입 시 ==**코드 생성 금지**==
# 🚨🚨🚨 사용자에게 "이 작업의 코드/스크립트 어디에 있나요?" ==**먼저 물어볼 것**==
# 🚨🚨🚨 사용자가 "없다"고 답할 때만 ==**그제서야 생성 허용**==
#
# 이유:
# - 방(session)이 터져서 새 브랜치로 옮길 때 사용자의 verified production code는 KISTI/gabia/예전 브랜치에 살아 있음.
# - Claude가 새로 짠 비슷한 코드는 hidden bug (compute_cij factor 2 누락, ntyp 하드코딩, safe wrapper "JOB DONE" 오판) 사례가 ==**반복**==됨.
# - "비슷한 거 짜드릴게요" / "내가 만들어드릴게요" 같은 응답 ==**금지**==.
# - inventory에 위치 모르면 사용자에게 묻고, 사용자가 없다고 확인한 뒤에만 새로 작성. 작성 후 즉시 CODE_INVENTORY.md 갱신.
#
# 위반 시: 사용자 시간/계산자원 손해 + 잘못된 결과 paper 위협.

# 🚨 필독 — **`kb/projects/MUST_READ_digital_twin_north_star.md`** ← 압축 후 첫 5분 안에 읽기
# 🚨 필독 — 이 프로젝트 = Digital Twin Platform (3-layer ML). Nd2O3 paper narrative drift 금지.
# 🚨 필독 — Argyrodite Mechanical Properties Research — Knowledge Base
# 🚨 필독 — `CODE_INVENTORY.md` 먼저 읽고 시작
# 🚨 필독 — 새 session 시작 시 위 north_star + 이 파일 + CODE_INVENTORY.md 셋 다 무조건 읽음
# 🚨 필독 — `필독/literature/` 의 paper 노트도 method 결정 전 참고

> [!error] CRITICAL — Before any code-related action, READ FIRST:
> **`CODE_INVENTORY.md`** at repo root.
> Rules:
> 1. **NEVER generate scripts** — only use entries from CODE_INVENTORY.md
> 2. If task's verified script not in inventory → **ASK user where it is**, do NOT recreate
> 3. If anomalous result → cross-check inventory `status` field before trusting
> 4. Update inventory when scripts get verified/found-buggy/relocated
>
> History of past mistakes (do not repeat):
> - compute_cij.py shear factor 2 bug → comp2 v2 wasted
> - Method 3 v2 LBFGS missing → clamped C=98 anomaly
> - safe wrapper "JOB DONE" check → premature exit on walltime
> See `CODE_INVENTORY.md` section "사용자 손해 history".

## Project Overview
PhD research (BML Lab, Hanyang University, 안용훈) on halogen-substituted argyrodite
solid electrolytes. Goal: predict mechanical properties (B0, E, Cij, Wad) via
multi-scale DFT/MLIP pipeline and understand how Cl/Br substitution affects them.

Paper: "Beyond Electrochemistry: Tailoring Mechanical Properties of Halogen-Substituted Argyrodites"

## Repository Structure
```
db/                          # Structured data (JSON) — machine-queryable
  compositions/              # Per-composition master files (comp1.json ... modelc.json)
  properties/                # Cross-composition property tables (eos.json, elastic.json, ...)
  literature/                # Reference database (refs.json)
  inputs/                    # DFT/MLIP input templates
    qe_templates/            # Quantum ESPRESSO input templates
    mlip_templates/          # MACE/UMA input templates
    adhesion_templates/      # SE/NCM adhesion calculation templates
  pipelines/                 # Pipeline definitions (v1.json, v2.json)
kb/                          # Knowledge base (Markdown) — human-readable
  methodology/               # Pipeline, methods, protocols
  physics/                   # Physical concepts, equations, interpretations
  results/                   # Per-composition and cross-composition analysis
  papers/                    # Paper drafts, notes, imported literature summaries
tools/                       # Python CLI tools
  kb_search.py               # Search across db/ and kb/ with evidence citations
  kb_index.py                # Auto-index new data, rebuild search index
  kb_export.py               # Export tables/figures for paper writing
  crop_interface.py          # VESTA z-crop of adhesion interface xyz
  plot_wad_stats.py          # Seed convergence + Wad histogram + paired (SI fig)
  plot_ncm_convergence.py    # 1L vs 5L NCM thickness (SI fig)
  plot_method_comparison.py  # v5/v8/5L method bar chart (SI fig)
  plot_gap_wad_correlation.py # Interface gap vs Wad scatter (SI fig)
  plot_br_content_trend.py   # Br content vs B0/E/Wad trend (SI fig)
  plot_master_summary.py     # 4-panel paper headline figure
  plot_coating_fom.py        # Coating figure-of-merit (E vs Wad scatter)
  analyze_halogen_bonds.py   # X-O bond count z-profile (needs xyz)
  li_layer_partition.py      # Li 1st/2nd/3rd layer classification (needs xyz)
  br_swap_test.py            # Br↔Cl substitution causal test (needs UMA)
  run_all.sh                 # Run all data-ready plots
output/                      # Generated plots and JSON summaries
tests/                       # Tests for tools
```

## Compositions
| ID     | Formula                      | Atoms | Cell    | f.u. | Family |
|--------|------------------------------|-------|---------|------|--------|
| comp1  | Li6PS5Cl                     | 52    | cubic   | 4    | Li6    |
| comp2  | Li6PS5Cl0.5Br0.5             | 52    | cubic   | 4    | Li6    |
| comp3  | Li5.4PS4.4Cl1.0Br0.6         | 62    | rhombo  | 5    | Li5.4  |
| comp4  | Li5.4PS4.4Cl0.8Br0.8         | 62    | rhombo  | 5    | Li5.4  |
| comp5  | Li5.4PS4.4Cl0.6Br1.0         | 62    | rhombo  | 5    | Li5.4  |
| modelc | Li5.4PS4.4Cl1.6              | 62    | rhombo  | 5    | Li5.4  |

## Key Results (Quick Reference)
- B0: comp1(26.2) > comp2(25.8) > comp5(22.9) > modelc(21.7) > comp3(20.8) = comp4(20.8) GPa
- E (600K snap): comp1(29.1) > comp2(28.6) > comp3(27.3) > comp4(26.4) > comp5(25.8) GPa
- Trend: Br increase -> B0/E decrease (intrinsic)
- Li ordering sensitivity: comp5 DC44 = 12.7 GPa (47%), DE = 15.6 GPa (22%)
- Band gap: 2.0-2.3 eV range, Br slightly reduces gap

## Pipeline
Two versions:
- **v1 (current paper):** Halogen enumerate -> MLIP screen -> DFT relax -> DFT EOS -> Post-processing
- **v2 (recommended):** + Li screening (20 random) + 500K MLIP MD annealing -> champion selection

## How to Use This Repo
1. **Query data:** `python tools/kb_search.py "comp5 bulk modulus"` or `python tools/kb_search.py "Br effect on elastic"`
2. **Add new data:** Edit JSON in db/, then `python tools/kb_index.py --rebuild`
3. **Export for paper:** `python tools/kb_export.py --table eos` or `--table elastic`
4. **Browse knowledge:** Read markdown files in kb/
5. **Generate SI figures:** `bash tools/run_all.sh` — outputs to `output/`

## Conventions
- Energies in eV (or Ry where QE native)
- Pressures/moduli in GPa
- Distances in Angstrom
- Charges in |e|
- Surface/adhesion energies in J/m^2
- comp IDs: comp1, comp2, comp3, comp4, comp5, modelc
- Basin labels: A (most stable), B, C...
- Pipeline versions: v1, v2

## DFT Settings (QE) — actual production values

### EOS scan (step 3)
- Functional: PBE (SSSP_1.3.0_PBE_efficiency)
- ecutwfc: **52 Ry**, ecutrho: **520 Ry**
- K-grid: **2x2x2** (cubic 52-atom; coarse OK for relative E)
- conv_thr: 1e-8, mixing_beta: 0.2, nosym: .true.
- smearing: mv, degauss: 0.01 Ry
- forc_conv_thr: 1e-4 (relax), nstep: 200

### Post-processing (V0 SCF / NSCF / elastic)
- ecutwfc: 60 Ry, ecutrho: 480 Ry (tighter)
- K-grid: 6x6x3 (rhombo), 6x6x6 (cubic) — dense for accurate band/Bader
- conv_thr: 1e-10 (tight SCF), 1e-8 (elastic relax)
- smearing: mv, degauss: 0.01 (DOS) / 0.005 (PDOS projwfc)

### Notes
- EOS uses coarser cutoff/K to scan 11 volumes economically
- Post-processing tightens for paper-quality observables

## MLIP Settings
- Model: MACE-MP-0 (screening), UMA-s-1p2 (adhesion)
- MD: Langevin thermostat, dt=2fs
- Annealing: 500K, 50-100ps
- Elastic: 600K snapshot x5, quench, FIRE relax, finite-strain Cij
