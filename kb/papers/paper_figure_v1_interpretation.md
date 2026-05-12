# Paper #1 Figures (comp4 v1 era) — Interpretation Note

> **Scope**: 이 노트는 comp4 v1 anneal champion 시절의 두 paper figure 해석에만 집중한다.
> comp4 v2 swap 이후의 변화 (R 변동, narrative pivot) 는 별도 (`kb/results/comp4_v2_adhesion_narrative_pivot.md`) 에서 다룸. 본 노트에서는 **v2 영향 일체 배제**.
>
> **다운로드**:
> - Figure 1 (binding curves) CSV: `output/paper_figures_v1/binding_curves_v1_paper_figure.csv`
> - Figure 2 (bond densities) CSV: `output/paper_figures_v1/bond_density_v1_paper_figure.csv`
> - Raw GitHub URLs:
>   - https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/debug-api-500-error-iukkt/output/paper_figures_v1/binding_curves_v1_paper_figure.csv
>   - https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/debug-api-500-error-iukkt/output/paper_figures_v1/bond_density_v1_paper_figure.csv

---

## Figure 1 — `UMA binding curves (R = +0.925)`

### 방법 (v1 paper figure)
- Rigid Z-scan, gap 0.8–4.0 Å
- UMA-s-1p1 calculator, **1L NCM** (paper figure protocol)
- 5 paper comps만 plot (modelC 제외)
- Sign convention: `E_adh = -W_ad` → **negative = binding favorable**
- **No asymptote subtraction** (raw `-W`). 자연스러운 per-comp 무한원 spread 그대로 표시.
- Cubic spline smoothing, gray band = equilibrium gap window 1.2–1.6 Å
- 데이터 source: `output/paper_figures_v1/binding_curves_v1_paper_figure.csv`

### 핵심 관찰

**1. Cross-family ordering: Li5.4 > Li6**

| comp | family   | well-depth (J/m²) | d_eq (Å) | paper Wad (mJ/m²) |
|------|----------|-------------------|----------|-------------------|
| comp3 | Li5.4   | **−0.315**         | 1.4      | **316**            |
| comp5 | Li5.4   | −0.280             | 1.6      | 249                |
| comp4 | Li5.4   | −0.265             | 1.6      | 298                |
| comp1 | Li6     | −0.200             | 1.2      | 194                |
| comp2 | Li6     | −0.180             | 1.2      | 180                |

- **Li5.4 family 셋 다 Li6 family 둘보다 깊음** (≈40–60% deeper)
- 이것이 paper #2 main message — vacancy chemical anchor 가 macroscopic Wad 증가시킴.
- Pearson R(−well depth, paper exp) = **+0.925**.

**2. Within-family Br trend (Li5.4 family)**
- comp3 (Cl-rich, Br=0.6) > comp5 (Br-rich, Br=1.0) > comp4 (balanced, Br=0.8)
- comp4 가 comp5 보다 살짝 얕은 것이 paper trend 와 정확히 일치하지는 않지만 (paper: comp4=298 > comp5=249), well-depth 자체는 거의 같음 (-0.265 vs -0.280).

**3. Within-family Br trend (Li6 family)**
- comp1 (Cl-only) ≈ comp2 (50/50) — 거의 같은 well depth ~−0.19. Br substitution 효과 미미.

**4. Asymptote (d=4 Å) 자연 분포**
- Li6 family: +0.13 (comp1), +0.12 (comp2) → 양수
- Li5.4 family: −0.18 ~ −0.19 → 음수
- 이 spread는 cell area difference 와 Madelung baseline 의 자연스러운 결과. Asymptote subtract 하지 않은 이유: 원본 paper figure 가 raw `-W` 으로 plot 했기 때문.

### 메커니즘 해석

Li5.4 family의 vacancy 가 표면 Li 를 under-coordinated 상태로 만들어 NCM O 와 chemical bonding 가능. Li6 family 는 표면 Li 가 모두 coordination saturated → NCM O 와 weak vdW only. → Li5.4 well 이 더 깊은 이유.

전체 비교는 `WHY_ADHESION.md` 의 vacancy chemical anchor mechanism 참조.

---

## Figure 2 — `Interface bond densities and experimental adhesion`

### 방법 (v1 paper figure)
- v15 protocol: `필독/adhesion/phase2a_v15_bond_robustness.py`
- 36 xy-shift registries, 평균
- Single Z-cut at equilibrium gap (≈1.4 Å)
- Bond cutoffs: Li-O 2.8 Å, Cl-O 3.4 Å, Br-O 3.6 Å (within metallic-radii sum)
- Bond density = bond count / interfacial area (Å⁻²)
- Right axis: paper experimental Wad (mJ/m²) overlay (line plot)
- 데이터 source: `output/paper_figures_v1/bond_density_v1_paper_figure.csv`

### 핵심 관찰

| comp | formula            | Li-O (Å⁻²) | Cl-O (Å⁻²) | Br-O (Å⁻²) | paper Wad (mJ/m²) |
|------|--------------------|-----------:|-----------:|-----------:|------------------:|
| comp1 | LPSC₁.₀          | 0.1147     | 0.0247     | 0.0000     | 194               |
| comp2 | LPSC₀.₅Br₀.₅     | 0.0759     | 0.0292     | 0.0000     | 180               |
| comp3 | LPSC₁.₀Br₀.₆     | **0.1372** | 0.0000     | 0.0000     | **316**           |
| comp4 | LPSC₀.₈Br₀.₈     | 0.1245     | 0.0000     | 0.1083     | 298               |
| comp5 | LPSC₀.₆Br₁.₀     | 0.1256     | 0.0000     | 0.1078     | 249               |
| modelC | LPSC₁.₆ (no Br) | 0.0853     | 0.0881     | 0.0000     | —                 |

**1. Li-O (attractive cation-anion): paper Wad 와 양의 상관**
- comp3 가장 높음 (0.137) → paper Wad 도 가장 높음 (316).
- Pearson R(Li-O, paper Wad) ≈ **+0.819** (v1 era 값).
- 메커니즘: Li5.4 family에서 vacancy 가 표면 Li 의 under-coordination 을 유도 → NCM O 와의 cation-anion bonding 증가.

**2. Cl-O (small anion, repulsive when at surface): paper Wad 와 음의 상관**
- Li6 family 만 Cl-O bond 있음 (Cl 표면 노출). Li5.4 family 는 Cl-O = 0 (Cl 이 bulk 에 갇힘).
- Pearson R(Cl-O, paper Wad) ≈ **−0.914** (v1 era 값) — 가장 강한 anti-correlation.
- 메커니즘: Cl⁻ 가 표면에 노출되면 NCM O²⁻ 와 anion-anion repulsion → Wad 감소.

**3. Br-O (large anion, repulsive but smaller magnitude than Cl-O)**
- Li5.4 mid/high-Br (comp4, comp5) 에서 Br-O 약 0.11.
- Pearson R(Br-O, paper Wad) ≈ +0.394 (약함). Br 은 크기 때문에 표면 노출에도 repulsion 약함.

**4. modelC (Cl-only Li5.4) 의 위치**
- 가장 낮은 Li-O (0.085) + 높은 Cl-O (0.088). Li5.4 family인데도 Cl-O 가 strong repulsion 유발 → paper Wad 알려지지 않았지만 작을 것으로 추정.
- Br 이 없으면 Li5.4 vacancy 의 advantage 가 Cl-O repulsion 으로 상쇄됨.

### 메커니즘 종합

1. **Li-O bonding** (attractive, cation-anion) = adhesion 의 main driver
   - Li5.4 vacancy → 표면 Li under-coordinated → Li-O bonding 증가 → Wad ↑

2. **Cl-O exposure** (repulsive, anion-anion) = adhesion killer
   - Li6 family 표면에 Cl 가 노출됨 → NCM O 와 repulsion → Wad ↓

3. **Br-O exposure** = 중성 (size 큰 anion = 약한 repulsion)
   - Li5.4 family Br-rich (comp5) 가 comp3 보다 Wad 낮음: Br 표면 노출이 약하게 negative

4. **Cl/Br balance** = trade-off
   - comp3 (Cl-rich, Br-light): Cl 은 bulk, Br=0 표면 → 최적 → Wad 가장 높음 (316)
   - comp5 (Cl-light, Br-rich): Cl=0, Br 표면 노출 ↑ → Wad 떨어짐 (249)

이 두 figure 가 paper #2 의 micro→macro bridge 핵심 증거. Wad 실험값과 microscopic geometry (bond density) 가 직접 연결됨.

---

## 데이터 재현 (단순 plot 만)

```python
import csv, matplotlib.pyplot as plt, numpy as np
from scipy.interpolate import CubicSpline

# === Figure 1 ===
rows = [r for r in csv.reader(open("output/paper_figures_v1/binding_curves_v1_paper_figure.csv"))
        if r and not r[0].startswith('#')]
header = rows[0]; data = rows[1:]
gaps = np.array([float(r[0]) for r in data])
comps = header[1:]
fig, ax = plt.subplots(figsize=(11, 7.5))
COLORS = {'comp1':'#1f77b4','comp2':'#17becf','comp3':'#d62728','comp4':'#9467bd','comp5':'#2ca02c'}
MARK   = {'comp1':'s','comp2':'o','comp3':'^','comp4':'D','comp5':'v'}
for j, c in enumerate(comps):
    y = np.array([float(r[1+j]) if r[1+j] else np.nan for r in data])
    m = ~np.isnan(y)
    cs = CubicSpline(gaps[m], y[m])
    xd = np.linspace(gaps[m].min(), gaps[m].max(), 250)
    ax.plot(xd, cs(xd), '-', color=COLORS[c], lw=3, alpha=0.95)
    ax.plot(gaps[m], y[m], MARK[c], color=COLORS[c], ms=9, mec='k', mew=0.5, label=c)
ax.axvspan(1.2, 1.6, alpha=0.13, color='gray'); ax.axhline(0, color='k', lw=0.7)
ax.set_xlabel('Interface gap, $d$ (Å)'); ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)')
ax.set_title('UMA binding curves (R = +0.925)'); ax.legend(loc='lower right')
fig.savefig('figure1_v1_reproduce.png', dpi=300, bbox_inches='tight')
```

```python
# === Figure 2 ===
import csv, matplotlib.pyplot as plt, numpy as np
rows = [r for r in csv.reader(open("output/paper_figures_v1/bond_density_v1_paper_figure.csv"))
        if r and not r[0].startswith('#')]
header = rows[0]; data = rows[1:]
comps = [r[0] for r in data]
labels = [r[1] for r in data]
li_o = [float(r[2]) for r in data]
cl_o = [float(r[3]) for r in data]
br_o = [float(r[4]) for r in data]
wad  = [float(r[5]) if r[5] else None for r in data]

fig, ax = plt.subplots(figsize=(13, 6.5))
x = np.arange(len(comps)); w = 0.27
ax.bar(x - w, li_o, w, color='#3b7dd8', label='Li-O (attractive, cation-anion)')
ax.bar(x,     cl_o, w, color='#d63838', label='Cl-O (repulsive, small anion)')
ax.bar(x + w, br_o, w, color='#3da848', label='Br-O (repulsive, large anion)')
ax.set_xticks(x); ax.set_xticklabels(labels, rotation=20)
ax.set_ylabel(r'Bond density (Å$^{-2}$)'); ax.legend(loc='upper left')

ax2 = ax.twinx()
xp = [i for i,v in enumerate(wad) if v is not None]
yp = [wad[i] for i in xp]
ax2.plot(xp, yp, 'o-', color='k', mfc='white', ms=10, mew=2, label='Paper exp W_ad (mJ/m²)')
for xi, yi in zip(xp, yp): ax2.annotate(f'{int(yi)}', (xi, yi), xytext=(0,8),
                                          textcoords='offset points', ha='center', fontweight='bold')
ax2.set_ylabel(r'Paper exp $W_{ad}$ (mJ/m²)'); ax2.legend(loc='upper right')
ax.set_title('Interface bond densities and experimental adhesion')
fig.savefig('figure2_v1_reproduce.png', dpi=300, bbox_inches='tight')
```

---

## 관련 파일

- 데이터:
  - `output/paper_figures_v1/binding_curves_v1_paper_figure.csv`
  - `output/paper_figures_v1/bond_density_v1_paper_figure.csv`
- v1 vs v2 비교 (참고만): `output/comp4_v2_adhesion/v1_v2_REDO_comparison.json`
- v15 protocol script: `필독/adhesion/phase2a_v15_bond_robustness.py`
- vacancy mechanism: `WHY_ADHESION.md`
- 본 문서: `kb/papers/paper_figure_v1_interpretation.md`

#paper #figure-v1 #adhesion #vacancy #bond-density #micro-to-macro
