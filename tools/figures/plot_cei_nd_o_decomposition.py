"""CEI Nd/O 분해 그림 3종 + Origin-ready CSV. house_style 준수 · 라벨은 영문만."""
import json, re, sys, csv, statistics as st
from pathlib import Path
sys.path.insert(0, ".")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tools.figures.house_style import INK, MUT, ELEM, apply_axes

OUT = Path("/tmp/claude-0/cei_fig"); OUT.mkdir(exist_ok=True)
D = json.load(open("db/properties/cei_interface_V_2026_09_16.json"))
VS = [2.5, 3.0, 3.5, 4.0, 4.3, 4.5]
CATS = list(D["results"])

def delta(key, V):
    out = []
    for c in CATS:
        r = D["results"][c]["by_voltage"][f"{V:.2f}"]
        if r.get(key) is not None and r.get("modelc") is not None:
            out.append(r[key] - r["modelc"])
    return out

dn = {V: delta("nd_only", V) for V in VS}
do = {V: delta("o_only_03", V) for V in VS}
dt = {V: delta("modelc_nd", V) for V in VS}
res = {V: [a + b - t for a, b, t in zip(dn[V], do[V], dt[V])] for V in VS}
# ⚠ house ELEM["Nd"] 는 O(#be123c)와 같은 붉은 계열이라 한 그림에서 구분이 안 된다.
#   Nd 는 CLAUDE.md 원소 팔레트에 없으므로 여기서 **보라**로 고정한다 (P #7c3aed 는 이 그림에 없다).
ND, OX, BOTH = "#6d28d9", ELEM.get("O", "#be123c"), INK

# ── Fig 1: 분해 (주 그림) ────────────────────────────────────────────────
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.2, 4.0), gridspec_kw={"width_ratios": [1.35, 1]})
for s, col, lab, mk in ((dn, ND, "Nd only (Nd$^{3+}$$\\leftrightarrow$3Li$^+$)", "o"),
                        (do, OX, "O only (O 0.3, S$\\rightarrow$O)", "s"),
                        (dt, BOTH, "Nd + O (measured)", "^")):
    m = [st.mean(s[V]) for V in VS]
    lo = [min(s[V]) for V in VS]; hi = [max(s[V]) for V in VS]
    a1.fill_between(VS, lo, hi, color=col, alpha=0.13, lw=0)
    a1.plot(VS, m, marker=mk, color=col, lw=2.0, ms=6, label=lab)
a1.plot(VS, [st.mean(dn[V]) + st.mean(do[V]) for V in VS], ls=":", lw=1.8,
        color=MUT, label="Nd + O (sum of parts)")
apply_axes(a1, "Voltage (V vs Li/Li$^+$)",
           "$\\Delta$ reaction energy vs LPSCl1.6 (eV/atom)")
a1.axhline(0, color=MUT, lw=0.8, ls="--")
a1.legend(frameon=False, fontsize=8.5, loc="upper left")
a1.text(0.03, 0.62, "higher = less reactive", transform=a1.transAxes,
        fontsize=8.5, color=MUT, style="italic")

rm = [st.mean(res[V]) for V in VS]
a2.axhspan(-0.010, 0.010, color="#fef9c3", zorder=0)
a2.plot(VS, rm, marker="D", color=INK, lw=2.0, ms=5)
a2.fill_between(VS, [min(res[V]) for V in VS], [max(res[V]) for V in VS],
                color=INK, alpha=0.12, lw=0)
a2.axhline(0, color=MUT, lw=0.8, ls="--")
apply_axes(a2, "Voltage (V vs Li/Li$^+$)", "Additivity residual (eV/atom)")
a2.text(0.04, 0.90, "pre-registered band  $\\pm$0.010", transform=a2.transAxes,
        fontsize=8.5, color="#92400e")
a2.set_ylim(-0.014, 0.014)
fig.tight_layout(); fig.savefig(OUT / "cei_nd_o_decomposition.png", dpi=300); plt.close(fig)

with open(OUT / "cei_nd_o_decomposition.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["voltage_V", "delta_nd_only_mean_eV_per_atom", "delta_nd_only_min", "delta_nd_only_max",
                "delta_o_only_mean_eV_per_atom", "delta_o_only_min", "delta_o_only_max",
                "delta_both_measured_mean_eV_per_atom", "delta_sum_of_parts_mean_eV_per_atom",
                "additivity_residual_mean_eV_per_atom", "residual_min", "residual_max", "n_cathodes"])
    for V in VS:
        w.writerow([V, round(st.mean(dn[V]), 5), round(min(dn[V]), 5), round(max(dn[V]), 5),
                    round(st.mean(do[V]), 5), round(min(do[V]), 5), round(max(do[V]), 5),
                    round(st.mean(dt[V]), 5), round(st.mean(dn[V]) + st.mean(do[V]), 5),
                    round(st.mean(res[V]), 5), round(min(res[V]), 5), round(max(res[V]), 5), len(dn[V])])

# ── Fig 2: 기전 — Nd phosphate sink vs P2S7 ─────────────────────────────
SINK = {"NdPO4", "Nd(PO3)3", "NdP5O14", "LiNd(PO3)4"}
BAD = {"P2S7"}
def prods(r):
    return {re.sub(r"^[0-9.eE+-]+\s+", "", t.strip())
            for t in r.split("->", 1)[1].split("+") if t.strip()}
def count(e, V, S):
    n = 0
    for c in CATS:
        rx = D["results"][c]["reactions"][f"{V:.2f}"].get(e)
        if rx and (prods(rx) & S): n += 1
    return n

fig, ax = plt.subplots(figsize=(7.0, 4.2))
# ⚠ 전압을 실좌표로 쓰면 4.30/4.50 이 0.2 밖에 안 떨어져 막대가 겹친다 → **범주형 위치**
xs = list(range(len(VS)))
w = 0.2
for i, (e, S, col, lab, hatch) in enumerate((
        ("modelc_nd", SINK, ND, "Nd$+$O : Nd-phosphate formed", None),
        ("nd_only", SINK, "#a78bfa", "Nd only : Nd-phosphate formed", None),
        ("modelc", BAD, "#c05621", "LPSCl1.6 : P$_2$S$_7$ formed", "//"),
        ("modelc_nd", BAD, "#fbbf24", "Nd$+$O : P$_2$S$_7$ formed", "//"))):
    ax.bar([x + (i - 1.5) * w for x in xs], [count(e, V, S) for V in VS],
           width=w, color=col, label=lab, hatch=hatch, edgecolor="white", lw=0.6)
apply_axes(ax, "Voltage (V vs Li/Li$^+$)", "Cathodes showing the phase (of 4)")
ax.set_xticks(xs); ax.set_xticklabels([f"{v:g}" for v in VS])
ax.set_yticks(range(5)); ax.set_ylim(0, 4.9)
ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper center")
ax.annotate("Nd$+$O never forms P$_2$S$_7$\n(yellow bars are all zero)",
            xy=(4.5, 0.45), xytext=(3.4, 1.45), fontsize=8.5, color="#92400e",
            arrowprops=dict(arrowstyle="->", color="#92400e", lw=1.0))
ax.set_title("P is captured as Nd-phosphate instead of P$_2$S$_7$",
             fontsize=10, color=INK, pad=8)
fig.tight_layout(); fig.savefig(OUT / "cei_nd_phosphate_sink.png", dpi=300); plt.close(fig)

with open(OUT / "cei_nd_phosphate_sink.csv", "w", newline="") as f:
    w2 = csv.writer(f)
    w2.writerow(["voltage_V", "electrolyte", "n_cathodes_with_Nd_phosphate",
                 "n_cathodes_with_P2S7", "n_cathodes_total"])
    for V in VS:
        for e in ("modelc", "lpsocl", "nd_only", "modelc_nd"):
            w2.writerow([V, e, count(e, V, SINK), count(e, V, BAD), len(CATS)])

# ── Fig 3: 양극별 절대 반응E ─────────────────────────────────────────────
fig, axs = plt.subplots(1, 4, figsize=(13.0, 3.5), sharey=True)
COL = {"comp1": "#9ca3af", "modelc": "#6b7280", "lpsocl": "#be123c",
       "o_only_03": "#f472b6", "nd_only": "#a78bfa", "modelc_nd": ND}
LAB = {"comp1": "LPSCl", "modelc": "LPSCl1.6", "lpsocl": "LPSOCl (O 0.2)",
       "o_only_03": "O 0.3", "nd_only": "Nd only", "modelc_nd": "Nd + O"}
for ax, c in zip(axs, CATS):
    for e, col in COL.items():
        y = [D["results"][c]["by_voltage"][f"{V:.2f}"].get(e) for V in VS]
        ax.plot(VS, y, marker="o", ms=4, lw=1.7, color=col, label=LAB[e])
    apply_axes(ax, "Voltage (V vs Li/Li$^+$)",
               "Reaction energy (eV/atom)" if c == CATS[0] else None)
    ax.set_title(c, fontsize=10, color=INK)
axs[0].legend(frameon=False, fontsize=7.5, loc="lower left")
fig.tight_layout(); fig.savefig(OUT / "cei_reaction_energy_by_cathode.png", dpi=300); plt.close(fig)

with open(OUT / "cei_reaction_energy_by_cathode.csv", "w", newline="") as f:
    w3 = csv.writer(f)
    w3.writerow(["cathode", "voltage_V"] + list(COL) + ["min_kink_reaction_modelc_nd"])
    for c in CATS:
        for V in VS:
            r = D["results"][c]["by_voltage"][f"{V:.2f}"]
            w3.writerow([c, V] + [r.get(e) for e in COL]
                        + [D["results"][c]["reactions"][f"{V:.2f}"].get("modelc_nd")])
print("PNG 3 · CSV 3 →", OUT)
for p in sorted(OUT.glob("*")): print("  ", p.name, p.stat().st_size, "B")
