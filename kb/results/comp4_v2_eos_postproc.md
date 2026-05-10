# comp4 v2 DFT EOS — BM3 fit + V0 결정 (2026-05-10)

> Pipeline v2 (anneal champion → DFT EOS 11 vol → BM3 fit → V0 closest grid → post-processing)의
> Step 4-7 완료. comp4 (Li5.4PS4.4Cl0.8Br0.8) 의 v2 결과를 v1과 비교.

---

## 1. Inputs

### Champion (Step 3 anneal output, GABIA)

- 파일: `/data/work/comp4_v2/1_step1to3/comp4_v2_rank2_anneal_3.xyz`
- 동의어: `comp4_v2_rank2_champion.xyz`
- E_anneal = **-255.65961830869279 eV** (cross-rank 🏆, ranks 1-4 anneal 중 최저)
- V_ref = 1204.220 Å³, 62 atoms, a=b=6.9837 Å, c=34.9183 Å (rhombohedral 5 fu stack)
- anneal_gain (vs h_E_lbfgs=-255.4138) = **+246 meV** — Li ordering optimization
- Stage1b ranks 0-4 cross-rank table:
  | row | h_E_lbfgs | champ_E_anneal | gain (meV) | best_Li |
  |---|---|---|---|---|
  | 2   | -255.4138 | **-255.6596** | -246 | rank3 Li11 🏆 |
  | 0   | -255.4665 | -255.6206 | -154 | rank3 Li10 |
  | 3   | -255.4091 | -255.6099 | -201 | rank4 Li10 |
  | 1   | -255.4149 | -255.5655 | -151 | rank0 Li9 |
  | 4   | -255.3993 | -255.5325 | -133 | rank1 Li7 |

⚠ 주의: gabia 디렉토리에 `comp4_v2_champion.xyz` 라는 별도 파일이 존재 (E=-255.6206) — **이건 글로벌 챔피언 아님**. paper / post-proc는 위에 명시된 `rank2_anneal_3.xyz` (E=-255.6596) 사용.

### DFT EOS 11 vol (Step 5-6, KISTI)

- 위치: `kisti:/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp4_lpscbrbr/dft_eos/v{098..108}/relax.out`
- protocol: champion fractional coords + scaled cell (v_pct/100)^(1/3), `calculation='relax'` (cell-fixed atom relax)
- pseudo: SSSP_1.3.0_PBE_efficiency
- DFT settings (CODE_INVENTORY 기준): ecutwfc=52, ecutrho=520, K=2x2x2, conv_thr=1e-8, mixing_beta=0.2

---

## 2. BM3 fit (Step 6)

verified `필독/step4_bm3_v0/bm3_fit_eos.py` 그대로 실행 (KISTI uma env, numpy 2.2.6, scipy 1.15.2, ase 3.27.0).

### 결과

| Quantity | Value |
|---|---|
| **B0** | **20.77 GPa** |
| **B0'** | 6.027 |
| **V0** | 1253.10 Å³ |
| E0 | -17918.5134 eV |
| n_points | 11 (v098-v108) |
| R² | 0.999983 |
| **closest grid** | **v104** (V=1252.39 Å³, Δ=-0.057%) |

### Per-volume table (eV)

| vol | V (Å³) | E (eV) | dE vs E_min (meV) |
|---|---|---|---|
| v098 | 1180.14 | -17918.1963 | +316.6 |
| v099 | 1192.18 | -17918.2976 | +215.3 |
| v100 | 1204.22 | -17918.3781 | +134.8 |
| v101 | 1216.26 | -17918.4385 | +74.4 |
| v102 | 1228.30 | -17918.4801 | +32.8 |
| v103 | 1240.35 | -17918.5042 | +8.7 |
| **v104** | **1252.39** | **-17918.5129** | **0** ⭐ |
| v105 | 1264.43 | -17918.5070 | +5.9 |
| v106 | 1276.47 | -17918.4869 | +25.9 |
| v107 | 1288.52 | -17918.4531 | +59.8 |
| v108 | 1300.56 | -17918.4061 | +106.8 |

V_ref (champion, V_v100) = 1204.22 Å³ → V0_fit = 1253.10 Å³ → V0/V_ref = 1.0406 → 챔피언이 +4% 압축 상태.

---

## 3. v1 vs v2 비교

| Quantity | comp4 v1 (paper) | **comp4 v2 (new)** | Δ |
|---|---|---|---|
| B0 (GPa) | 20.8 | **20.77** | -0.03 |
| B0' | 6.33 | 6.03 | -0.30 |
| n_points | 10 | 11 | +1 |
| R² | 0.999996 | 0.999983 | -1e-5 |

### 해석 (Li6 v2 vs Li5.4 v2 차이)

- comp1 (Li6): Δ(v1→v2) = +0.3 GPa (annealing gain 65 meV → B0 변화 측정 가능)
- comp4 (Li5.4+Br=Cl): Δ(v1→v2) = **-0.03 GPa** (annealing gain **246 meV** 더 큰데 B0 변화 거의 0)
- modelC (Li5.4 pure): Δ(v1→v2_MLIP) = -1.7 GPa (annealing 필수, flat Li landscape)

→ **comp4 의 Li ordering 민감도가 modelC 보다 작음**: anneal로 Li 재배열에서 246 meV 안정화 얻었지만 그게 cell 강성에는 거의 영향 없음. Cl=Br=0.8 frustration 환경에서 Li ordering 변화가 PS4 framework 강도에 weak coupling.

→ ==**within-family Br trend (comp3 = comp4 = 20.8 ≈ comp4_v2 = 20.77)** 이 v2 pipeline에서도 보존==. paper #1 narrative 변경 불필요.

---

## 4. closest grid → V0 structure

V0 structure = `v104/relax.out` 의 last frame:
- cell: V_v104 = 1252.39 Å³ (V0_fit 1253.10 보다 -0.057% 작음 — 거의 일치)
- atoms: 62 (Li 27 + P 5 + S 22 + Cl 4 + Br 4)
- BFGS converged (SCF 100 iter, BFGS 99 iter, force ≤ 0.0006 Ry/au, walltime 61.1 min)

post-processing 흐름 (Step 7-8):
1. v104 final cell + ATOMIC_POSITIONS → tight SCF (conv_thr=1e-10) for charge density
2. NSCF dense K-grid (6×6×3 rhombo) → DOS / PDOS via dos.x + projwfc.x
3. pp.x plot_num=21 → Bader charge analysis (Henkelman bader_lnx_64)
4. ±0.005 finite strain × 12 SCF (clamped-ion) → C_ij Voigt 6×6 → K/G/E/ν

---

## 5. Reproducibility

### Verified scripts used
- `필독/step4_bm3_v0/bm3_fit_eos.py` ✅ VERIFIED (CODE_INVENTORY E3 → 이 fit으로 status 갱신)
- BM3 함수: `E(V) = E0 + 9 V0 B0/16 × ((eta-1)^3 B0' + (eta-1)^2 (6-4 eta))`, `eta = (V0/V)^(2/3)`
- pseudo, K-grid, cutoff: comp4 pipeline_v2 step3 input과 동일

### One-liner (재현)
```bash
cd /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp4_lpscbrbr/dft_eos/
source activate uma
python3 ~/bin/bm3_fit_eos.py --pattern 'v*/relax.out' --label comp4_v2 --out comp4_v2_BM3_fit.json
```

### 다음 단계 (Step 8 post-processing)
1. v104 final cell + coords → V0.xyz 추출 (verified `필독/step5_postproc/01_dos_pdos/scf.in` template 참조해 comp4_v2 specific scf.in 채우기)
2. nscf.in / dos.in / projwfc.in / pp.in 생성 (comp4 prefix, K=6×6×3, ntyp=5)
3. KISTI에서 `필독/step5_postproc/01_dos_pdos/run_full_pp.sh` + `02_bader/run_bader.sh` 패턴 따라 실행
4. comp4 v2 elastic constants는 별도 — `phase2a_v31_mlip_elastic_v2_3comp.py` (B0 = MLIP 600K snapshot champion)와는 다른 작업 (DFT 0K finite strain 12 .in)

---

## 6. 변경된 db / inventory

| File | 변경 |
|---|---|
| `db/properties/eos.json` | `comp4_v2` entry 추가, `v1_vs_v2_comparison.comp4` 추가 |
| `db/compositions/comp4.json` | `eos_v2` 블록 추가 (B0=20.77, V0=1253.10, closest=v104) |
| `output/comp4_v2_BM3_fit.json` | full fit JSON (raw_data 11 points + provenance) |
| `kb/results/comp4_v2_eos_postproc.md` | 이 파일 |
| `CODE_INVENTORY.md` | E3 BM3 fitting → ✅ VERIFIED (comp4_v2 reproduction success) |

---

#comp4 #v2 #eos #bm3 #pipeline-v2 #post-processing #step4 #step5
