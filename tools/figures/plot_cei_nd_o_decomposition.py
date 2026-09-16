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
# ══ 2026-09-16 추가 — §D(생성에너지·균형반응) · §B kinks(x-스캔) ══════════════
FJ = Path("db/properties/cei_formation_2026_09_16.json")


def _counts(f):
    """간단 화학식 → {원소: 수}. 괄호 1겹까지 (LiNd(PO3)4). 소수 계수 지원.

    ⛔ 못 하는 것: 중첩 괄호·수화물 점표기·전하. 이 그림이 쓰는 화학식만 본다.
       아래 assert 가 틀어지면 **그림을 그리지 않고 죽는다** — 축이 조용히 틀리는 게 최악이다.
    """
    def flat(s):
        out = {}
        for el, n in re.findall(r"([A-Z][a-z]?)([0-9]*\.?[0-9]*)", s):
            if not el:
                continue
            out[el] = out.get(el, 0.0) + (float(n) if n else 1.0)
        return out
    out, rest = {}, f
    for grp, mult in re.findall(r"\(([^()]*)\)([0-9]*\.?[0-9]*)", f):
        m = float(mult) if mult else 1.0
        for el, n in flat(grp).items():
            out[el] = out.get(el, 0.0) + n * m
        rest = rest.replace(f"({grp}){mult}", "")
    for el, n in flat(rest).items():
        out[el] = out.get(el, 0.0) + n
    return out


assert _counts("Li3PO4") == {"Li": 3.0, "P": 1.0, "O": 4.0}, _counts("Li3PO4")
assert _counts("Li4P2O7") == {"Li": 4.0, "P": 2.0, "O": 7.0}, _counts("Li4P2O7")
assert _counts("LiNd(PO3)4") == {"Li": 1.0, "Nd": 1.0, "P": 4.0, "O": 12.0}, \
    _counts("LiNd(PO3)4")
assert _counts("P2S7") == {"P": 2.0, "S": 7.0}, _counts("P2S7")

if FJ.exists():
    F = json.load(open(FJ))
    # ── Fig 4a: Li 예산 사다리 — 같은 형식 반응에서 Li/P 만 바꾼다 ──────────
    #   spec 꼴: "<donor>,Nd2O3 > NdPO4,Li2O"  (P 쪽은 동일, Li/P 만 다르다)
    LAD = []
    for spec, r in F.get("reactions", {}).items():
        if not (spec.endswith("Nd2O3 > NdPO4,Li2O") and r.get("ok")):
            continue
        donor = spec.split(",")[0].strip()
        c = _counts(donor)
        if c.get("P", 0) <= 0:
            continue
        LAD.append({"donor": donor, "li_per_p": c.get("Li", 0.0) / c["P"],
                    "nd_in_donor": c.get("Nd", 0.0) > 0,
                    "dE": r["E_eV_per_P"], "reaction": r["reaction"]})
    LAD.sort(key=lambda d: d["li_per_p"])
    pure = [d for d in LAD if not d["nd_in_donor"]]          # Li↔Nd 치환 (같은 축)

    # 영점 — **인접 두 점 선형보간만** 쓴다 (전역 피팅은 3점에 과하다)
    cross = None
    for a, b in zip(pure, pure[1:]):
        if a["dE"] < 0 <= b["dE"]:
            t = -a["dE"] / (b["dE"] - a["dE"])
            cross = a["li_per_p"] + t * (b["li_per_p"] - a["li_per_p"])
            break

    fig, (b1, b2) = plt.subplots(1, 2, figsize=(11.0, 4.1),
                                 gridspec_kw={"width_ratios": [1, 1.5]})
    xs_ = [d["li_per_p"] for d in pure]; ys_ = [d["dE"] for d in pure]
    b1.axhspan(min(ys_ + [-1.4]) - 0.15, 0, color="#ede9fe", zorder=0)
    b1.text(0.06, 0.08, "Nd wins the P", transform=b1.transAxes,
            fontsize=9, color=ND, weight="bold")
    b1.text(0.60, 0.90, "Li wins the P", transform=b1.transAxes,
            fontsize=9, color=MUT, weight="bold")
    b1.plot(xs_, ys_, marker="o", ms=7, lw=2.0, color=ND, zorder=3)
    for d in pure:
        b1.annotate(d["donor"], (d["li_per_p"], d["dE"]), textcoords="offset points",
                    xytext=(6, 7), fontsize=8, color=INK)
    for d in LAD:
        if d["nd_in_donor"]:
            b1.plot([d["li_per_p"]], [d["dE"]], marker="s", ms=7, mfc="white",
                    mec=ND, mew=1.6, zorder=3)
            b1.annotate(d["donor"] + "\n(Nd$\\rightarrow$Nd, off-axis)",
                        (d["li_per_p"], d["dE"]), textcoords="offset points",
                        xytext=(8, -16), fontsize=7.5, color=MUT)
    b1.axhline(0, color=MUT, lw=0.9, ls="--")
    if cross is not None:
        b1.axvline(cross, color="#92400e", lw=1.2, ls=":")
        b1.annotate(f"crossover\nLi/P $\\approx$ {cross:.2f}", (cross, 0),
                    textcoords="offset points", xytext=(6, 42), fontsize=8.5,
                    color="#92400e")
    apply_axes(b1, "Li per P in the donor phosphate",
               "$\\Delta E$ of Nd$\\leftarrow$Li exchange (eV per P)")
    b1.set_title("Nd takes the P only when Li is scarce", fontsize=10, color=INK, pad=8)

    # ── Fig 4b: 상별 생성에너지 — P2S7 이 얼마나 얕은가 ─────────────────────
    GRP = [("Nd phosphate", ["NdPO4", "Nd(PO3)3", "NdP5O14", "LiNd(PO3)4"], ND),
           ("Li phosphate", ["Li3PO4", "Li4P2O7", "LiPO3", "P2O5"], ELEM["O"]),
           ("thiophosphate", ["Li3PS4", "P2S7", "P2S5"], ELEM["S"]),
           ("Nd non-phosphate", ["Nd2O3", "NdCl3", "Nd2S3", "NdOCl"], "#a78bfa")]
    labels, vals, cols, seps = [], [], [], []
    for gname, fs, col in GRP:
        for fm in fs:
            r = F.get("formation", {}).get(fm)
            if not (r and r.get("found")):
                continue
            labels.append(fm); vals.append(r["E_f_eV_per_atom"]); cols.append(col)
        seps.append(len(labels) - 0.5)
    b2.bar(range(len(vals)), vals, color=cols, edgecolor="white", lw=0.6)
    for s in seps[:-1]:
        b2.axvline(s, color="#e5e7eb", lw=1.0)
    for gname, s0, s1 in zip([g[0] for g in GRP], [-0.5] + seps[:-1], seps):
        b2.text((s0 + s1) / 2, 0.12, gname, ha="center", fontsize=8, color=MUT)
    b2.set_xticks(range(len(labels)))
    b2.set_xticklabels(labels, rotation=55, ha="right", fontsize=7.5)
    apply_axes(b2, None, "Formation energy (eV/atom)")
    b2.set_ylim(min(vals) - 0.35, 0.45)
    if "P2S7" in labels:
        i = labels.index("P2S7")
        b2.annotate("P$_2$S$_7$ is the shallowest sink\nin the whole set",
                    (i, vals[i]), textcoords="offset points", xytext=(-4, -46),
                    ha="center", fontsize=8, color="#92400e",
                    arrowprops=dict(arrowstyle="->", color="#92400e", lw=1.0))
    fig.tight_layout(); fig.savefig(OUT / "cei_li_budget_ladder.png", dpi=300)
    plt.close(fig)

    with open(OUT / "cei_li_budget_ladder.csv", "w", newline="") as f:
        w4 = csv.writer(f)
        w4.writerow(["donor_phosphate", "li_per_P", "donor_contains_Nd",
                     "dE_eV_per_P", "balanced_reaction"])
        for d in LAD:
            w4.writerow([d["donor"], round(d["li_per_p"], 4),
                         int(d["nd_in_donor"]), d["dE"], d["reaction"]])
        w4.writerow([]); w4.writerow(["crossover_li_per_P_linear_interp_between_adjacent_points",
                                      "" if cross is None else round(cross, 4)])
    with open(OUT / "cei_formation_energies.csv", "w", newline="") as f:
        w5 = csv.writer(f)
        w5.writerow(["formula", "group", "E_f_eV_per_atom", "E_f_eV_per_P",
                     "n_P", "e_above_hull_eV_per_atom", "entry_id"])
        for gname, fs, _ in GRP:
            for fm in fs:
                r = F.get("formation", {}).get(fm)
                if not (r and r.get("found")):
                    continue
                w5.writerow([fm, gname, r["E_f_eV_per_atom"], r.get("E_f_eV_per_P"),
                             r.get("n_P"), r["e_above_hull_eV_per_atom"], r["entry_id"]])

# ── Fig 5: x-스캔 (Richards/Ong 식 — LiPOF Fig. 1b–f 형태) ─────────────────
#   ⚠ 전압은 원소가 아니라 **순차량**이라 원소 팔레트를 안 쓴다. 명도 단조 앰버→적갈 램프.
VRAMP = ["#fcd34d", "#fbbf24", "#f59e0b", "#ea580c", "#c2410c", "#7f1d1d"]
ELECS = ["comp1", "modelc", "lpsocl", "o_only_03", "nd_only", "modelc_nd"]
CAT_X = "NMC811" if "NMC811" in CATS else CATS[0]
have_kinks = bool(D["results"][CAT_X].get("kinks"))

if have_kinks:
    fig, axs = plt.subplots(2, 3, figsize=(13.0, 7.0), sharex=True, sharey=True)
    for ax, e in zip(axs.ravel(), ELECS):
        for V, col in zip(VS, VRAMP):
            ks = D["results"][CAT_X]["kinks"][f"{V:.2f}"].get(e) or []
            if not ks:
                continue
            ks = sorted(ks, key=lambda k: k["x_atomic_frac"])
            x = [k["x_atomic_frac"] for k in ks]
            y = [k["reaction_energy_eV_per_atom"] for k in ks]
            ax.plot(x, y, lw=1.7, color=col, label=f"{V:g} V", zorder=2)
            j = min(range(len(y)), key=lambda i: y[i])
            ax.plot([x[j]], [y[j]], marker="v", ms=5, color=col, zorder=3)
            # 기전 표지 — Nd 인산염이 나오는 kink 를 점으로 찍는다
            sx = [k["x_atomic_frac"] for k in ks if prods(k["reaction"]) & SINK]
            sy = [k["reaction_energy_eV_per_atom"] for k in ks
                  if prods(k["reaction"]) & SINK]
            if sx:
                ax.plot(sx, sy, ls="none", marker="o", ms=3.6, mfc="none",
                        mec=ND, mew=1.1, zorder=4)
        apply_axes(ax, None, None)
        ax.axhline(0, color=MUT, lw=0.8, ls="--")
        ax.set_title(LAB.get(e, e), fontsize=10, color=INK)
    for ax in axs[1]:
        ax.set_xlabel("$x$  (atomic fraction of electrolyte)", fontsize=10, color=INK)
    for ax in axs[:, 0]:
        ax.set_ylabel("Reaction energy (eV/atom)", fontsize=10, color=INK)
    axs[0, 0].legend(frameon=False, fontsize=8, ncol=2, title="vs Li/Li$^+$",
                     title_fontsize=8, loc="lower left")
    axs[0, 2].plot([], [], ls="none", marker="o", ms=4, mfc="none", mec=ND, mew=1.1,
                   label="kink forms an Nd-phosphate")
    axs[0, 2].plot([], [], ls="none", marker="v", ms=5, color=MUT, label="minimum")
    axs[0, 2].legend(frameon=False, fontsize=8, loc="lower left")
    fig.suptitle(f"Interfacial reaction energy across the mixing range  "
                 f"(cathode {CAT_X})", fontsize=11, color=INK, y=0.995)
    fig.tight_layout(); fig.savefig(OUT / "cei_x_scan_panels.png", dpi=300)
    plt.close(fig)

    with open(OUT / "cei_x_scan_panels.csv", "w", newline="") as f:
        w6 = csv.writer(f)
        w6.writerow(["cathode", "electrolyte", "voltage_V", "x_atomic_frac",
                     "reaction_energy_eV_per_atom", "is_minimum",
                     "forms_Nd_phosphate", "reaction"])
        for c in CATS:
            for e in ELECS:
                for V in VS:
                    ks = D["results"][c]["kinks"][f"{V:.2f}"].get(e) or []
                    ks = sorted(ks, key=lambda k: k["x_atomic_frac"])
                    if not ks:
                        continue
                    jm = min(range(len(ks)),
                             key=lambda i: ks[i]["reaction_energy_eV_per_atom"])
                    for i, k in enumerate(ks):
                        w6.writerow([c, e, V, k["x_atomic_frac"],
                                     k["reaction_energy_eV_per_atom"], int(i == jm),
                                     int(bool(prods(k["reaction"]) & SINK)),
                                     k["reaction"]])
else:
    print("  ⚠ kinks 가 없다 — §B 를 want_kinks 판으로 다시 돌려야 Fig 5 가 나온다.")

print("PNG/CSV →", OUT)
for p in sorted(OUT.glob("*")): print("  ", p.name, p.stat().st_size, "B")
