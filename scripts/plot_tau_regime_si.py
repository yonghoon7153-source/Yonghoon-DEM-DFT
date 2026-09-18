"""
Generate SI-quality figures from /tmp/tau_regime_db.json.

Figures produced:
  /tmp/si_fig_regime_map.pdf       Main regime map (Le/D vs SE-SE CN, colored by
                                    constriction fraction)
  /tmp/si_fig_literature_match.pdf τ² vs φ_SE + Minnmann/Wang/Dewald anchors
  /tmp/si_fig_ratio_distribution.pdf 3 histograms (Le/Lg, Lg/D, Le/D) — for
                                     median non-commutativity footnote
  /tmp/si_fig_bottleneck_showcase.pdf  Annotated showcase: input_8_AMS +
                                        input_real8_40_7 as bottleneck examples

Usage:
  python3 scripts/build_tau_regime_db.py   # first, build DB
  python3 scripts/plot_tau_regime_si.py    # then, plot
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


DB_PATH = '/tmp/tau_regime_db.json'
OUT_DIR = '/tmp'


def load_db():
    with open(DB_PATH) as f:
        return json.load(f)


# ─── Figure 1: Regime map ────────────────────────────────────────────────

def fig_regime_map(records):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    xs = np.array([r['SE_SE_CN_mean'] for r in records if r.get('SE_SE_CN_mean') and r.get('Le_over_D')])
    ys = np.array([r['Le_over_D'] for r in records if r.get('SE_SE_CN_mean') and r.get('Le_over_D')])
    cs = np.array([(r['constriction_frac'] or 0.75) for r in records
                   if r.get('SE_SE_CN_mean') and r.get('Le_over_D')])
    names = [r['name'] for r in records if r.get('SE_SE_CN_mean') and r.get('Le_over_D')]

    # Regime zones
    ax.axhspan(1.3, 2.3, alpha=0.1, color='tab:green', zorder=0)
    ax.axhspan(2.3, ys.max() * 1.1 if len(ys) else 4, alpha=0.1, color='tab:red', zorder=0)
    ax.axhspan(min(ys.min() * 0.9, 0.5) if len(ys) else 0.5, 1.3, alpha=0.1, color='tab:blue', zorder=0)
    ax.axvspan(0, 3.5, alpha=0.15, color='tab:red', zorder=0)

    # Reference lines
    ax.axhline(1.76, color='k', ls='--', lw=1, alpha=0.6)
    ax.text(xs.max()*0.95 if len(xs) else 6, 1.80, 'median 1.76', fontsize=8, ha='right')
    ax.axvline(3.5, color='tab:red', ls=':', lw=1, alpha=0.8)
    ax.text(3.45, 3.5, 'SE-SE CN\nthreshold 3.5', fontsize=8, ha='right', color='tab:red')

    # Scatter
    sc = ax.scatter(xs, ys, c=cs, cmap='viridis', s=50, edgecolor='k',
                    linewidth=0.5, vmin=0.6, vmax=0.85, zorder=3)
    cbar = plt.colorbar(sc, ax=ax, label='Constriction fraction  R$_{GB}$/(R$_{GB}$+R$_{bulk}$)')

    # Annotate bottleneck outliers
    for x, y, n in zip(xs, ys, names):
        if y > 2.5:
            ax.annotate(n.replace('input_', ''), (x, y),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=7, color='tab:red', fontweight='bold')

    # Regime labels
    ax.text(xs.max()*0.98 if len(xs) else 6, 2.7, 'BOTTLENECK\n(Le/D > 2.3)',
            fontsize=9, ha='right', color='tab:red', alpha=0.8)
    ax.text(xs.max()*0.98 if len(xs) else 6, 1.7, 'NORMAL (1.3–2.3)',
            fontsize=9, ha='right', color='tab:green', alpha=0.8)
    ax.text(xs.max()*0.98 if len(xs) else 6, 1.0, 'SURROGATE CLEAN (<1.3)',
            fontsize=9, ha='right', color='tab:blue', alpha=0.8)

    ax.set_xlabel('SE–SE coordination number  ⟨CN⟩', fontsize=11)
    ax.set_ylabel(r'$\tau_{Lap,\,eff}\,/\,\tau_{Dij}$  (bottleneck indicator)',
                  fontsize=11)
    ax.set_title(f'Tortuosity regime map (n={len(xs)} DEM cases)')
    ax.grid(alpha=0.3)

    plt.tight_layout()
    out = f'{OUT_DIR}/si_fig_regime_map.pdf'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─── Figure 2: Literature match ──────────────────────────────────────────

def fig_literature_match(records):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    xs = np.array([r['phi_SE'] for r in records if r.get('phi_SE') and r.get('tau_sq_Lap_eff')])
    ys = np.array([r['tau_sq_Lap_eff'] for r in records
                   if r.get('phi_SE') and r.get('tau_sq_Lap_eff')])

    ax.scatter(xs, ys, s=45, c='steelblue', edgecolor='k', linewidth=0.5,
               alpha=0.7, label=f'This work DEM (n={len(xs)})')

    #  ── 문헌 앵커 — **하나만 남았다** (2026-09-18, 원장 `GAP3-37`) ────────────────
    #  ⛔ 뺀 것 셋.  지우지 않고 **추적 결과와 함께 보존**한다 (원문이 나오면 복원 가능).
    #
    #    ('Dewald 2021 (25% NCM)', 0.65, 2.4)   ← **Minnmann 과 같은 논문**이다.
    #        `docs/rint_anchor_db_research.md:58` 이 그것을 "Bielefeld/**Dewald**/Janek,
    #        Charge Transport Bottlenecks" 로 적고 DOI 가 `10.1149/1945-7111/abf8d7` 인데
    #        `docs/lit_minnmann2021_…:3` 의 DOI 와 **동일**하다.  값 2.4 도 Minnmann 카드의
    #        Fig 2b 표(`:168`)에 있다 ⇒ 한 논문이 **독립 앵커 2 개로 이중계상**돼 있었다.
    #        ⚠ φ 도 어긋난다 — Minnmann 가정 porosity 14 % 로는 1−0.25−0.14 = 0.61 인데
    #        0.65 를 썼다.
    #
    #    ('Wang 2023 (70% CAM)', 0.26, 7.78)  ·  ('Wang 2023 (80% CAM)', 0.16, 17.24)
    #        ⛔ **출처가 리포 전체에 0 건**이다 — litdb 정본 274 편에 `wang2023*` 카드가
    #        없고, 리포에서 "Wang 2023" 을 서지로 식별하는 유일한 줄
    #        (`build_literature_reference.py:18`) 은 **DEM overlap 규약**(δ/R 0.05–0.15)
    #        문맥이다.  tortuosity 와 무관하다.
    #        ★ 게다가 세 가지가 더 어긋난다 (전부 산술·측정):
    #          ① 두 점이 porosity 를 **정확히 4.0 %** 로 함의한다 (Minnmann 규약
    #             `φ = 1 − CAM_vol − porosity` 적용).  Minnmann 14 % 의 1/3.5 이고
    #             두 점이 **같은 수**로 떨어진다 = 측정이 아니라 구성된 수라는 신호.
    #          ② 두 점을 지나는 적합 `τ² = 0.855·φ^(−1.639)` 의 γ 가 정본
    #             `litdb/papers/bielefeld2020_…:224` 의 실측 밴드 γ∈[0.32, 0.67] **밖**이다
    #             (α=1.639 는 밴드 [1.21, 2.02] 안).
    #          ③ 그림이 그리던 `φ^(−2.36)` 점선은 이 두 별을 **3.09× · 4.38× 벗어난다**
    #             ⇒ 이름표("Wang 2023 fit")와 달리 **그 점들에 대한 적합이 아니었다**.
    #        ⚠ 다만 `τ² = φ^(−1.5)` 가 두 값을 3 %·9 % 안에서 재현한다 — 어딘가 실재하는
    #          수를 옮겨 적었을 가능성은 남는다.  그래서 값을 **여기 보존**한다.
    #
    #  ⚠ 앵커가 하나뿐이라는 사실이 그림에 **드러나야 한다** — 숨기지 않는다.
    anchors = [
        ('Minnmann 2021 (42% CAM)', 0.44, 4.3,  'tab:red'),
    ]
    for name, phi, tau2, col in anchors:
        ax.scatter(phi, tau2, marker='*', s=300, c=col, edgecolor='k',
                   linewidth=1, zorder=5, label=name)

    #  ── Bruggeman 기준선 ───────────────────────────────────────────────────────
    #  ⛔⛔ **옛 주석이 규약을 지어냈다 — 철회한다** (2026-09-18, 원장 `GAP3-37`).
    #     그 주석은 *"Bruggeman 줄 α=1.5 → −1.0 ⇒ τ² = φ^(2−2α)"* 라고 적었는데,
    #     이것은 **그려진 −1.0 을 맞다고 전제하고 거꾸로 맞춘 식**이고 `τ² = φ^(2−2α)` 는
    #     **리포 어디에도 정의돼 있지 않다**.  그 −1.0 자체가 오류였다.
    #
    #  ★ 리포의 진짜 규약은 **코드에 있다** (유도 가능, 문헌 불요):
    #        `scripts/build_tau_regime_db.py:43-48`  τ = √(φ_SE · σ_grain / σ)   ⇒ τ² = φ·σ₀/σ_eff
    #        `scripts/network_conductivity.py:1098`  Bruggeman EMT: σ_eff/σ₀ = φ^1.5
    #     둘을 합치면  **τ² = φ^(1−α)**  ⇒ α = 1.5 → **−0.5**  (α = 2.36 이었다면 −1.36).
    #     독립 확인: `docs/lit_minnmann2021_…:150` (같은 τ 정의) ·
    #     정본 `litdb/papers/bielefeld2020_…:222` — *"**표준 Bruggeman: τ²(ε) = ε^(−1/2)**"*.
    #
    #  ⛔ "Wang 2023 fit" 점선(`φ^(−2.36)`)은 **지웠다** — 출처 0 건인 데다 자기 이름표가
    #     붙은 두 앵커를 3.09×·4.38× 벗어났다 (위 anchors 주석 참조).  적합이 아닌 선에
    #     "fit" 이라 적는 것이 앵커 없음보다 나쁘다.
    #
    #  ⚠ 범례는 **그리는 지수에서 생성**한다 (원장 `GAP3-FIG` ⑥) — 곡선↔글자가 갈릴 수 없다.
    BRUG_ALPHA = 1.5                 # σ_eff/σ₀ = φ^α  (구형 입자 EMT)
    BRUG_EXP = 1.0 - BRUG_ALPHA      # τ² = φ^(1−α)  ⇒ −0.5.  ★ 손으로 적지 않는다
    phi_range = np.linspace(0.15, 0.7, 50)
    ax.plot(phi_range, phi_range**BRUG_EXP, 'k--', alpha=0.5,
            label=f'Bruggeman (α={BRUG_ALPHA:g}): τ²=φ$^{{{BRUG_EXP:g}}}$')

    ax.set_xlabel(r'$\varphi_\mathrm{SE}$', fontsize=11)
    ax.set_ylabel(r'$\tau^2_{Lap,\,eff}$', fontsize=11)
    ax.set_yscale('log')
    ax.set_title('Tortuosity² vs SE fraction — literature match')
    ax.grid(alpha=0.3, which='both')
    ax.legend(fontsize=8, loc='upper right')

    plt.tight_layout()
    out = f'{OUT_DIR}/si_fig_literature_match.pdf'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─── Figure 3: Ratio distributions (median non-commutativity) ────────────

def fig_ratio_distributions(records):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

    cols = [('Le_over_Lg', r'$\tau_{Lap,eff}\,/\,\tau_{Lap,geom}$', 2.01, 'tab:red'),
            ('Lg_over_D',  r'$\tau_{Lap,geom}\,/\,\tau_{Dij}$',    0.79, 'tab:green'),
            ('Le_over_D',  r'$\tau_{Lap,eff}\,/\,\tau_{Dij}$',     1.76, 'tab:blue')]

    for ax, (key, lbl, med, col) in zip(axes, cols):
        vals = [r[key] for r in records if r.get(key) is not None]
        ax.hist(vals, bins=20, color=col, alpha=0.7, edgecolor='k')
        ax.axvline(med, color='k', ls='--', lw=1.5, label=f'median = {med}')
        ax.set_xlabel(lbl, fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel('Count')
    fig.suptitle(f'Per-case ratio distributions (n={len(records)}) — '
                 f'medians are independent, not multiplicatively constrained')

    plt.tight_layout()
    out = f'{OUT_DIR}/si_fig_ratio_distribution.pdf'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return out


# ─── Figure 4: Bottleneck showcase ───────────────────────────────────────

def fig_bottleneck_showcase(records):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    # Main population
    xs = np.array([r['phi_SE'] for r in records if r.get('phi_SE') and r.get('Le_over_D')])
    ys = np.array([r['Le_over_D'] for r in records if r.get('phi_SE') and r.get('Le_over_D')])
    cns = np.array([(r.get('SE_SE_CN_mean') or 4.0) for r in records
                    if r.get('phi_SE') and r.get('Le_over_D')])
    names = [r['name'] for r in records if r.get('phi_SE') and r.get('Le_over_D')]

    sc = ax.scatter(xs, ys, c=cns, cmap='plasma_r', s=60, edgecolor='k',
                    linewidth=0.5, vmin=2.5, vmax=6, alpha=0.85)
    cbar = plt.colorbar(sc, ax=ax, label='SE-SE CN mean')

    # Reference lines
    ax.axhline(1.76, color='k', ls='--', lw=1, alpha=0.5,
               label='bulk median  Le/D = 1.76')
    ax.axhline(2.3, color='tab:red', ls=':', lw=1.2, alpha=0.7,
               label='bottleneck onset  (Le/D = 2.3)')

    # Highlight bottleneck outliers
    for x, y, cn, n in zip(xs, ys, cns, names):
        if y > 2.3:
            ax.annotate(f'{n.replace("input_", "")}\n(CN={cn:.1f})', (x, y),
                        xytext=(10, 5), textcoords='offset points',
                        fontsize=8, color='tab:red', fontweight='bold',
                        arrowprops=dict(arrowstyle='->', color='tab:red', alpha=0.6))

    ax.set_xlabel(r'$\varphi_\mathrm{SE}$', fontsize=11)
    ax.set_ylabel(r'$\tau_{Lap,\,eff}\,/\,\tau_{Dij}$', fontsize=11)
    ax.set_title('Bottleneck regime identification — Dijkstra underestimates flux resistance\n'
                 'when Le/D > 2.3 and SE-SE CN approaches percolation threshold')
    ax.grid(alpha=0.3)
    ax.legend(loc='upper left', fontsize=9)

    plt.tight_layout()
    out = f'{OUT_DIR}/si_fig_bottleneck_showcase.pdf'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.savefig(out.replace('.pdf', '.png'), dpi=150, bbox_inches='tight')
    plt.close()
    return out


def main():
    if not os.path.exists(DB_PATH):
        #  ⛔ **fail-open 이었다** (원장 `GAP3-39`, 2026-09-18).  여기서 그냥 `return` 하면
        #     함수가 `None` 을 돌려주고 `main()` 이 성공(rc=0)으로 끝난다 — 그림이 한 장도
        #     안 나왔는데 파이프라인에는 **초록**으로 보인다.
        #     = CLAUDE.md 규율 ⑤ 의 false-green 이 **종료코드 층**에서 재현된 것.
        print(f"ERROR: {DB_PATH} not found. Run build_tau_regime_db.py first.")
        return 1
    records = load_db()
    print(f"Loaded {len(records)} records from {DB_PATH}\n")

    out1 = fig_regime_map(records)
    print(f"  [1/4] Regime map → {out1} (+png)")

    out2 = fig_literature_match(records)
    print(f"  [2/4] Literature match → {out2} (+png)")

    out3 = fig_ratio_distributions(records)
    print(f"  [3/4] Ratio distributions → {out3} (+png)")

    out4 = fig_bottleneck_showcase(records)
    print(f"  [4/4] Bottleneck showcase → {out4} (+png)")

    print(f"\n✓ All SI figures generated in {OUT_DIR}/")
    return 0


if __name__ == '__main__':
    #  ⛔ `main()` 의 반환을 **종료코드로 흘린다** (`GAP3-39`).  전에는 `main()` 만 부르고
    #     버려서 어떤 실패도 rc=0 이 됐다.
    raise SystemExit(main())
