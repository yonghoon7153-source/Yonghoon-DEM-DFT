# Phase C — Static figures (Summary)

Phase plan에서 Phase C는 "Static figures" — DEM corpus 분석으로 paper 부록
또는 본문에 들어갈 figure 생성.  C1 + C2 완료 시점 결과 요약.

## C1 — Percolation 2D scaling fit

세미나 피드백 #3 (φc 계산) + #6 (조성 → percolation 일반화) 직접 시도.

### 결과
**핵심 발견**: 우리 86-case corpus는 commercial composition 중심 (φ_SE
∈ [0.27, 0.45]) → percolation **saturated regime**.  Threshold (~0.18-
0.33) 영역에는 데이터 없어 φc 직접 추출 불가능.

대신 σ_ionic 사용해 4가지 model 비교:

| Model | Form | R²(log) | 핵심 fit param |
|---|---|---|---|
| Kirkpatrick (add. λ) | σ₀·(φ−φc(λ))^t,  φc=φc_∞−A·λ^(−α) | 0.70 | A=0 (λ 못 잡음) |
| Kirkpatrick (mul. λ) | σ₀·(φ−φc(λ))^t,  φc=φc_∞·(1−B/λ) | 0.70 | B=0 (λ 못 잡음) |
| Bruggeman | σ_grain·φ^n | 0.70 | **n = 4.38** |
| Per-class bimodal | 위와 같은 Kirkpatrick | **0.77** | φc=0.05, t=3.4 |

→ 단순 power law `σ = σ_grain · φ^n` 으로도 동일 정확도.
   φc, λ-dependence는 본 데이터 범위에서 추출 어려움.

### Honest interpretation
- ✅ **Bimodal-class 내 강한 power-law 일관성** (R²=0.77, n=4-5 type)
- ❌ **Threshold φc 직접 추출은 불가** — 우리 데이터가 너무 SE-rich
- ⚠️ **t=3.5+ 는 Kirkpatrick 이론 t=2와 다름** — 좁은 φ 범위에서 local slope
- 📖 **문헌 인용 권장**: φc ≈ 0.18-0.33 (sphere RCP percolation)을 baseline으로,
  우리 데이터는 above-threshold confirmation 역할.

### Paper figure
- `docs/figures/percolation_2d_fit.png` (v1, sigmoid attempt)
- `docs/figures/percolation_2d_fit_v2.png` ★ (4-model comparison, paper-grade)

### 생성 명령
```bash
python3 scripts/fit_percolation_2d_v2.py
```

---

## C2 — XY-projection severe% heatmap

세미나 피드백 #4 (microstructure 어디서 어떤 형상) 부분 대응.
3D contact-level fracture를 XY 평면으로 collapse → "cathode 어느 위치가
잘 깨지는가" 시각화.

### 결과 (86 case ensemble)

| Composition | n | median severe% | max | 결론 |
|---|---|---|---|---|
| **mono AM_P** | 8 | **45%** | 64% | catastrophic — 산업 부적합 |
| bimodal | 44 | **6%** | 30% | workable |
| **mono AM_S** | 28 | **0%** | 0% | 안 깨짐 (소입자 load 분산) |

**Tier별 (capacity)**:
- 1mAh 박막: median 13%, 가장 노이지함 (얇아서 비율 큼)
- 6mAh: median 5%, outlier 2 (real_10 AMP-only 64%, real_5 36%)
- **8mAh 후막: median 1%, 가장 안정** (contact 많아 분산)
- particulate/S: 0% (AM_S only)

**Finite-size 효과 없음**: composition이 RVE 크기보다 dominant.

### 생성물
- `docs/figures/xy_heatmap/<case>.png` (86 per-case 3-panel)
- `docs/figures/xy_heatmap_ensemble.png` ★ 4-panel paper figure
- `docs/data/xy_heatmap_summary.csv` per-case scalar metrics

### 생성 명령
```bash
python3 scripts/extract_xy_fracture_heatmap.py --all
python3 scripts/xy_heatmap_ensemble.py
```

---

## Phase C 결론 (paper 인용 가능 statements)

1. **"Bimodal cathode 안정성 정량"**: 86 case ensemble에서 bimodal
   composition median severe% = 6%, mono AM_P = 45% (catastrophic).
   설계 rule "bimodal preferred" 정량 검증.

2. **"SE-rich saturated regime의 σ_ionic scaling"**: 우리 corpus는
   commercial composition 영역 (φ_SE 0.27-0.45)에서 power law
   `σ_ionic ∝ φ_SE^n`, n ≈ 4.4 (Bruggeman fit).  Bimodal-class 안에서는
   R² = 0.77로 strong dependence.  *Threshold 영역 (φ_SE < 0.2)은 본
   데이터에 미포함 → φc 직접 추출은 future work.*

3. **"Compaction fracture 위치 무관성"**: XY heatmap에서 fracture
   spatial clustering 없음 — RVE 내 uniform distribution.  Edge effect
   / 한쪽 약점 없음 — 압축이 균일하게 작동.

## Phase plan 갱신

| Phase | Step | 상태 |
|---|---|---|
| A | A1-A7 | ✅ 모두 완료 |
| B | B1-B5 | ✅ 모두 완료 |
| C | **C1 percolation 2D fit** | **✅ 완료** (limitation acknowledged) |
| C | **C2 XY-heatmap PNG** | **✅ 완료** |
| D | D1-D4 (2D microstructure 전극 생성) | ❌ 다음 트랙 |
| E | E1 schematic / E2 용어 | ❌ 수동 |

Phase A/B/C 완료.  Phase D (2D microstructure → FEM 전극)이 다음 핵심 트랙.
