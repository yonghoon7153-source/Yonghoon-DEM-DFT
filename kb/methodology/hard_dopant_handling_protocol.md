# Hard / Compound Dopant Handling Protocol (doping cascade)

작성 2026-06-17. 계기: B2O3 cascade가 (1) 농도가 라벨만 다르고 구조 동일, (2) UMA relax에서
부피 −32% 붕괴 — 두 실패모드를 동시에 보임. 이를 "이런 경우 대응" 선례로 정리.
관련: `tools/doping/master_batch_273.sh`, `tools/doping/tier_cascade.sh`, `tools/doping/run_uma_screening.py`

---

## 사례: B2O3 (multi_category_2026_05_26_v23/B2O3_x002·x005·x010)
- 3 농도(x002/x005/x010) **actual_x 전부 0.25**, 구조/에너지 동일 → 농도시리즈 무효.
- `uma_relaxed.outlier_flag=True, volume_runaway dV=−30~32%` (4개 중 3개) → Stage 03 `--max_dv 0.25`가 걸러 **usable 2개만** → elastic/migration/σ 예측기 skip("only 2 usable rows, need ≥5").

---

## 실패모드 1 — 목표 농도가 base cell에서 실현 불가

### 원인
- master_batch가 `X_COMPOUND=<conc>`(0.02/0.05/0.10)는 넘기지만 **SUPERCELL을 `1,1,1`로 하드코딩**
  (master_batch_273.sh: `bash tier_cascade.sh <cif> <OUT> 5 1,1,1 0`).
- compound 도펀트는 **최소 1 unit**(B2O3 = 2B+3O). base `[1,1,1]` = **4 f.u.** → 1 unit = **x=0.25가 바닥**.
- run_compound_batch은 X_COMPOUND를 **라벨로만** 기록(`s.setdefault('concentration', label_conc)`), 구조는 1 unit 고정 → 3 농도 동일.

### 대응 (선례)
**supercell을 목표농도에 맞춰 스케일 + ACTUAL x를 보고**(nominal 라벨 강요 금지). 1 unit 기준:

| supercell | n_f.u. | actual x | ~원자수 |
|---|---|---|---|
| 1,1,1 | 4  | 0.250 (25%) | 56 |
| 2,1,1 | 8  | 0.125 (12.5%) | ~104 |
| 2,2,1 | 16 | 0.0625 (6.25%) | ~208 |
| 2,2,2 | 32 | 0.031 (3.1%) | ~416 |
| 3,2,2 | 48 | 0.021 (2.1%) | ~624 |

- 2/5/10%에 **가장 가까운 supercell**을 골라 돌리고, 결과엔 **actual_x(예: 6.25%)** 를 쓴다.
- sub-3%(2%)는 ~624원자 → UMA 가능하나 느림 → "dilute-limited" 플래그.
- **single-element 치환도 동일** — [1,1,1]에선 최소 ~5–25%라 2% 불가. 같은 supercell 스케일 적용.

### 영구 픽스 (cascade 담당)
master_batch가 `(compound, conc)`마다 **supercell = 가장 가까운 actual_x 주는 셀**을 계산해 tier_cascade에 넘기도록 수정. 그리고 라벨 대신 **actual_x를 ML feature로** 사용.

---

## 실패모드 2 — UMA cell-relax 부피 runaway

### 원인
- `run_uma_screening.py`: `relax_structure(..., cell_relax=True)` + **FrechetCellFilter** → 셀까지 relax.
- B(작음)@P자리 + O@S자리 조합에서 UMA가 셀을 비물리적으로 −30%+ 수축(특정 화학종, 특히 B-O, 에 대한 MLIP 한계).

### 대응 (선례)
1. **detect**: `dV/V0 < −0.25`(또는 `outlier_flag`)면 runaway로 간주.
2. **재시도 fixed-cell**: `cell_relax=False`(원자만 relax, 셀은 supercell의 baseline 부피 고정)로 다시 → 부피 정보는 별도 **isotropic EOS**(±2~3% 격자스캔 + BM3)로.
3. **DFT 검증**: UMA가 못 푸는 도펀트는 DFT relax/EOS로 확인(단 b2o3 EOS는 수렴 까다로움 — 좁은 grid + continuation 필요).
4. **플래그**: 그래도 안 되면 dopant를 **"UMA-cell-unstable"** 로 표시하고 cell 기반 물성(B0, E)은 "low-confidence".

### 영구 픽스 (cascade 담당)
`run_uma_screening.py`에 `--cell_relax {true|false}` 플래그 추가 + Stage 02에서 runaway 감지 시 자동 fixed-cell 재시도.

---

## 의사결정 트리 (hard dopant)
```
도펀트 결과 수상?
├─ 3 농도 actual_x 동일 → 실패모드1 → supercell 스케일 재실행, actual_x 보고
├─ dV < −25% / outlier 다수 → 실패모드2 → fixed-cell 재시도 → 안되면 DFT/EOS → 안되면 "UMA-unstable" 플래그
└─ usable rows < 5 (예측기 skip) → seed/구조 더 생성 or 위 둘 중 해당 모드 처리
```

## B2O3 선례 실행 (시연)
base cell이 너무 작아 못 하던 걸 **supercell 스케일**로:
```bash
# Stage 01+02만 (full cascade 17h 말고 빠른 시연), [2,2,1]=6.25%
OUT=/data/work/runs/b2o3_precedent_sc221
COMPOUND_FILTER=B2O3 bash tools/doping/run_compound_batch.sh \
    db/structures/lpscl_F43m_24G_canonical.cif "$OUT/01_structures" 5 2,2,1 0
python3 tools/doping/run_uma_screening.py \
    --summary "$OUT/01_structures/structures_summary.json" \
    --base db/structures/lpscl_F43m_24G_canonical.cif \
    --baseline "$OUT/02/baseline.json" --out "$OUT/02/uma_results.json" \
    --device cuda --steps 1500
```
기대: actual_x ≈ 0.0625(라벨이 아니라 실제) + dV가 [1,1,1]보다 완화되는지 확인.
여전히 runaway면 → 실패모드2 대응(fixed-cell/DFT)으로 넘어가 B2O3 = "UMA-cell-unstable" 선례 확정.
