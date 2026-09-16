"""CEI 그림 + Origin-ready CSV + **화면 절(§3·§4·§5) 생성**. house_style 준수 · 라벨 영문만.

⛔ §3·§4·§5 는 **이 파일이 유일한 소스**다. `db/properties/cei_figs/index.html` 의 그 절들을
  손으로 고치면 **다음 재생성에 지워진다** — 2026-09-16 에 실제로 그렇게 비유 박스 4 개를
  잃었다(§3 예산 · §4 물감 · §5 XRD · §5 핀홀). 그 절을 고칠 일이 있으면 **여기서** 고친다.
  나머지 절(§1·§2·§6·§7·§8)은 index.html 이 소스다.
"""
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
                        (dt, BOTH, "LPSCl$_{1.6}$@Nd$_2$O$_3$ (measured)", "^")):
    m = [st.mean(s[V]) for V in VS]
    lo = [min(s[V]) for V in VS]; hi = [max(s[V]) for V in VS]
    a1.fill_between(VS, lo, hi, color=col, alpha=0.13, lw=0)
    a1.plot(VS, m, marker=mk, color=col, lw=2.0, ms=6, label=lab)
a1.plot(VS, [st.mean(dn[V]) + st.mean(do[V]) for V in VS], ls=":", lw=1.8,
        color=MUT, label="Nd only $+$ O only (sum of parts)")
apply_axes(a1, "Voltage (V vs Li/Li$^+$)",
           "$\\Delta$ reaction energy vs LPSCl$_{1.6}$ (eV/atom)")
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
        ("modelc_nd", SINK, ND, "LPSCl$_{1.6}$@Nd$_2$O$_3$ : Nd-phosphate", None),
        ("nd_only", SINK, "#a78bfa", "Nd only : Nd-phosphate", None),
        ("modelc", BAD, "#c05621", "LPSCl$_{1.6}$ : P$_2$S$_7$ formed", "//"),
        ("modelc_nd", BAD, "#fbbf24", "LPSCl$_{1.6}$@Nd$_2$O$_3$ : P$_2$S$_7$", "//"))):
    ax.bar([x + (i - 1.5) * w for x in xs], [count(e, V, S) for V in VS],
           width=w, color=col, label=lab, hatch=hatch, edgecolor="white", lw=0.6)
apply_axes(ax, "Voltage (V vs Li/Li$^+$)", "Cathodes showing the phase (of 4)")
ax.set_xticks(xs); ax.set_xticklabels([f"{v:g}" for v in VS])
ax.set_yticks(range(5)); ax.set_ylim(0, 4.9)
ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper center")
# 이름이 길어지면서 옛 자리(3.4, 1.45)가 4.3 V 막대를 덮었다. 화살표도 뺐다 —
# 가리킬 대상이 **높이 0 인 막대**라 어디로 그어도 다른 막대를 가로지른다.
# 범례에 노랑 항목이 있고 본문이 "전부 0" 이라 말하므로 화살표가 할 일이 없다.
ax.text(1.55, 3.45, "LPSCl$_{1.6}$@Nd$_2$O$_3$ never forms P$_2$S$_7$\n"
                    "(the yellow bars are all zero)",
        fontsize=8, color="#92400e", va="top")
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
#: ⚠ **표시명만** 여기서 바꾼다 — 키(comp1·modelc·modelc_nd)는 CSV·JSON 열 이름이고
#:   기계 경로라 안 건드린다 (1저자 2026-09-16: "modelc 라 하지 말고 lpscl1.6 으로,
#:   공치환은 lpscl1.6@nd2o3 로 — 같이 보는 문서니까").
LAB = {"comp1": "LPSCl", "modelc": "LPSCl$_{1.6}$", "lpsocl": "LPSOCl$_{1.6}$",
       "o_only_03": "O 0.3 only", "nd_only": "Nd only",
       "modelc_nd": "LPSCl$_{1.6}$@Nd$_2$O$_3$"}
#: ⛔ LAB 은 **matplotlib mathtext** 다. HTML 에 그대로 쓰면 `LPSCl$_{1.6}$` 가 날것으로
#:   찍힌다 — 2026-09-16 에 §4 표·본문이 그렇게 나갔다(오류 없음·화면만 깨짐).
#:   렌더러가 둘이면 문자열도 둘이라야 한다. 파일 끝 assert 가 HTML 로 새는 `$` 를 잡는다.
LAB_HTML = {k: (v.replace("$_{1.6}$", "<sub>1.6</sub>").replace("$_2$", "<sub>2</sub>")
                 .replace("$_3$", "<sub>3</sub>")) for k, v in LAB.items()}
assert not any("$" in v for v in LAB_HTML.values()), f"LAB_HTML 에 mathtext 가 남았다: {LAB_HTML}"
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
    b1.text(0.62, 0.10, "Nd wins the P", transform=b1.transAxes,
            fontsize=9, color=ND, weight="bold")
    b1.text(0.48, 0.93, "Li wins the P", transform=b1.transAxes,
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
                        xytext=(11, -2), fontsize=7.5, color=MUT, va="center")
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
    # ⚠ 막대가 전부 음수라 **y>0 이 통째로 빈다** — 주석·군 이름을 거기 올린다.
    #   (처음엔 막대 사이에 넣었다가 P2O5·Nd2O3 막대를 덮었다.)
    for gname, s0, s1 in zip([g[0] for g in GRP], [-0.5] + seps[:-1], seps):
        b2.text((s0 + s1) / 2, 1.06, gname, ha="center", fontsize=8, color=MUT)
    b2.set_xticks(range(len(labels)))
    b2.set_xticklabels(labels, rotation=55, ha="right", fontsize=7.5)
    apply_axes(b2, None, "Formation energy (eV/atom)")
    b2.set_ylim(min(vals) - 0.35, 1.30)
    if "P2S7" in labels:
        i = labels.index("P2S7")
        b2.annotate("P$_2$S$_7$ is the shallowest sink in the whole set",
                    (i, vals[i]), xytext=(i, 0.58), ha="center",
                    fontsize=8.5, color="#92400e",
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
    # ⚠ 전압 곡선은 **모든 패널에서** label 을 달았다 — 그냥 legend() 를 부르면 그 여섯이
    #   같이 딸려 나온다(첫 판에서 실제로 그랬다). 표식 손잡이를 **명시해서** 넘긴다.
    h1, = axs[0, 2].plot([], [], ls="none", marker="o", ms=4, mfc="none", mec=ND,
                         mew=1.1, label="kink forms an Nd-phosphate")
    h2, = axs[0, 2].plot([], [], ls="none", marker="v", ms=5, color=MUT,
                         label="minimum")
    axs[0, 2].legend(handles=[h1, h2], frameon=False, fontsize=8, loc="upper right")
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

# ── HTML 절 생성 (2026-09-16) ────────────────────────────────────────────────
#   ⛔ 표의 숫자를 **손으로 치지 않는다.** 2026-09-16 에 4자리 소수 15 개를 손으로
#     쳤다가 전부 틀렸다. 여기서 JSON→HTML 로 찍고, index.html 은 이 조각을 끼운다.
def _fmt(v, n=4, sign=True):
    if v is None:
        return "—"
    return f"{v:+.{n}f}" if sign else f"{v:.{n}f}"


sec = []
if FJ.exists() and LAD:
    rows = "\n".join(
        f'<tr><td class="mono">{d["donor"]}</td><td>{d["li_per_p"]:g}</td>'
        f'<td class="{"nd" if d["dE"] < 0 else ""}">{_fmt(d["dE"])}</td>'
        f'<td class="mono" style="text-align:left;font-size:.74rem">{d["reaction"]}</td>'
        f'{"<td>Nd→Nd</td>" if d["nd_in_donor"] else "<td>Li→Nd</td>"}</tr>'
        for d in LAD)
    ch = {s: r for s, r in F["reactions"].items() if r.get("ok")}
    def rxn(key):
        for s, r in ch.items():
            if s.startswith(key):
                return r
        return None
    r_li2o = rxn("Li3PO4,Nd2O3")
    r_licl = rxn("NdCl3,Li3PO4")
    r_ps7_nd = rxn("P2S7,Nd2O3")
    r_ps7_li = rxn("P2S7,Li2O")
    frows = "\n".join(
        f'<tr><td class="mono">{fm}</td><td>{g}</td>'
        f'<td>{_fmt(F["formation"][fm]["E_f_eV_per_atom"], 4, False)}</td>'
        f'<td>{_fmt(F["formation"][fm].get("E_f_eV_per_P"), 2, False)}</td>'
        f'<td>{_fmt(F["formation"][fm]["e_above_hull_eV_per_atom"], 4, False)}</td></tr>'
        for g, fs, _ in GRP for fm in fs
        if F.get("formation", {}).get(fm, {}).get("found"))
    sec.append(f"""
<h2>3. 검증 — 그리고 가설의 절반이 틀렸다</h2>

<p>§2 의 가설을 재려고 같은 hull 에서 <strong>균형반응 10 개</strong>를 돌렸다
(<code>ComputedReaction</code>, 계수는 도구가 잡는다). 검산 고리 둘이 닫힌다 —
<span class="mono">③−④ = ⑤−⑥ = ① = {_fmt(r_li2o["E_eV_per_P"])}</span>, 소수 4 자리까지.</p>

<div class="card warn">
<p style="margin:0"><strong>⛔ 철회</strong> — "NdPO₄ 가 Li₃PO₄ 보다 깊은 P 싱크다" 는
<strong>틀렸다</strong>. <span class="mono">Li₃PO₄ + ½Nd₂O₃ → NdPO₄ + 1.5 Li₂O</span> 가
<strong>{_fmt(r_li2o["E_eV_per_P"])} eV/P</strong> 로 <strong>양수</strong>다.
생성에너지 표도 같은 말을 한다 — P 하나당 Li₃PO₄ 가 더 깊다.</p>
</div>

<h3>그런데 Li 예산을 낮추면 부호가 뒤집힌다</h3>

<p class="plain">익숙한 것에 빗대면 <b>예산 문제</b>다. 같은 P 한 개를 붙잡는 데
Li₃PO₄ 는 <b>Li 를 3 개</b> 쓰고 NdPO₄ 는 <b>0 개</b> 쓴다. Li 가 넉넉할 때는 비싼 쪽이
더 튼튼해서 그쪽으로 간다. 그런데 <b>고전압이란 Li 가 양극으로 빠져나간 상태</b>라
Li 가 희소해지고, 그때는 "3 개짜리" 를 살 수 없다. 그래서 Nd 는 <b>더 좋은 인산염을
만드는 것이 아니라, Li 를 안 쓰는 선택지를 하나 더 열어 주는 것</b>이다.</p>

<p>같은 형식(<span class="mono">&lt;공여상&gt; + ½Nd₂O₃ → NdPO₄ + Li₂O</span>)에서
<strong>P 하나당 Li 개수만</strong> 바꾸면 완전 단조다.</p>

<div class="tblwrap">
<table>
<thead><tr><th>P 공여상</th><th>Li/P</th><th>ΔE (eV/P)</th><th>균형반응</th><th>치환</th></tr></thead>
<tbody>
{rows}
</tbody></table>
</div>

<figure>
<img src="cei_li_budget_ladder.png" alt="Left: exchange energy versus Li per P, crossing zero near 1.67. Right: formation energy per atom for fifteen phases grouped into Nd phosphates, Li phosphates, thiophosphates and Nd non-phosphates.">
<figcaption><b>Fig. 4. Lithium cost of the phosphate sink.</b>
(a) Energy of the Nd&#8592;Li exchange reaction, &#60;donor&#62; + &#189;&#8201;Nd<sub>2</sub>O<sub>3</sub>
&#8594; NdPO<sub>4</sub> + Li<sub>2</sub>O, per phosphorus atom, plotted against the Li:P ratio of the
donor phosphate. The zero crossing at Li/P &#8776; {cross:.2f} is obtained by linear interpolation
between the two bracketing points, not by a global fit. LiNd(PO<sub>3</sub>)<sub>4</sub> (open square)
already contains Nd and is therefore shown on the same axis but excluded from the slope.
(b) MP2020-corrected formation energies of the fifteen phases considered, grouped by class;
P<sub>2</sub>S<sub>7</sub> is the shallowest sink of the set at
{_fmt(F["formation"]["P2S7"]["E_f_eV_per_atom"], 4, False)}&#8201;eV/atom.</figcaption>
</figure>

<div class="figexp">
<div class="figexp-h">Fig. 4 를 읽는 법</div>
<p><b>왼쪽 그림</b>의 가로축은 "P 하나를 붙잡는 데 Li 를 몇 개 쓰는 상인가" 이고,
세로축은 "그 상에서 Nd 가 P 를 뺏어 가는 것이 이로운가" 다. <b>세로축이 0 보다 아래면
Nd 가 이긴다.</b> 네 점이 <b>완전히 단조</b>라서, Li 를 적게 쓰는 상일수록 Nd 가 유리해진다는
관계가 그대로 보인다.</p>
<p>점선으로 표시한 <b>Li/P &#8776; {cross:.2f}</b> 가 부호가 뒤집히는 자리다. 이 값은
전체 네 점에 직선을 맞춘 것이 <b>아니라</b>, 부호가 갈리는 <b>바로 옆 두 점(Li/P 1 과 2)만</b>
이어서 얻었다 — 점이 셋뿐인데 전역 피팅을 하면 없는 정밀도를 만들어 낸다.</p>
<p>빈 사각형 <b>LiNd(PO₃)₄</b> 는 같은 축에 찍혀 있지만 <b>기울기 계산에서 뺐다.</b>
나머지 셋은 Li 자리를 Nd 가 대신하는 반응인데 이것만 이미 Nd 를 품고 있어 Nd&#8594;Nd 라,
같은 기울기 위에 있다고 볼 근거가 없다.</p>
<p><b>오른쪽 그림</b>은 맥락이다. 막대가 아래로 길수록 그 상이 안정하다.
왼쪽 세 묶음(Nd 인산염 · Li 인산염 · 티오인산염)을 보면
<b>P₂S₇ 만 유독 짧다</b> — 인산염들의 1/5 수준이다. "O 만 있으면 P 는 어느 쪽이든
인산염으로 간다" 가 여기서 나온다.</p>
<p>⚠ 오른쪽 그림의 <code>E_f/P</code> 열(표에만 있음)은 <b>반응에너지가 아니다.</b>
O:P 비가 다른 상을 한 줄에 놓으면 P–O 결합 수 차이를 P 하나당으로 뭉갠다 — 순위 힌트로만 읽는다.</p>
</div>

<div class="card warn">
<p style="margin:0"><b>⛔ 이 관계는 우리가 처음이 아니다 — Xiao 2019 (Joule) 이 이미 발표했다.</b>
Ceder 그룹이 코팅 후보 10 만 종을 훑어 <b>산화한계가 Li 원자분율과 음의 상관</b>을 보였고(Fig. 7A),
<b>ortho(PO₄³⁻) &lt; pyro(P₂O₇⁴⁻) &lt; meta(PO₃⁻)</b> 순으로 산화한계가 오른다는 것도 냈다
(Fig. 6, 중앙값 <span class="mono">figure-read &#8776; 4.1 &#8594; 4.5 &#8594; 5.0 V</span>).
<b>아래 사다리 Li₃PO₄ → Li₄P₂O₇ → LiPO₃ 는 정확히 그 세 계열, 같은 순서</b>다.</p>
<p style="margin:10px 0 0"><b>⇒ 이 관계를 우리 발견으로 쓰지 않는다.</b> 우리 계산은 <b>독립 확인</b>이고,
신규성은 <b>재는 양</b>(M³⁺←Li 교환에너지 · 교차점 Li/P &#8776; 1.67)과 <b>경로</b>(발라주는 코팅이 아니라
전해질 도펀트가 계면에서 <b>제자리에</b> 만든다)에 있다.
기록 <code>lit_xiao2019_li_budget_precedence_2026_09_16</code>.
⚠ Xiao 논문은 <b>Fig. 6·7 만 실제로 봤다</b> — 나머지 그림·표는 digest 텍스트로만 안다.</p>
</div>

<div class="card answer">
<p style="margin:0"><strong>고쳐 쓴 기전</strong> — Nd 는 "더 좋은 인산염을 만드는" 게 아니라
<strong>Li 를 안 쓰고 인산염을 만드는 경로를 연다</strong>. Li₃PO₄ 는 P 하나당 Li 3 개를
먹고 NdPO₄ 는 <strong>0 개</strong>다. 고전압에서 Li 가 양극으로 빠져나가면 Li 가 희소해지고,
그때 경쟁은 Li₃PO₄ 대 NdPO₄ 가 아니라 <strong>LiPO₃ 대 NdPO₄</strong> 가 된다 —
거기선 Nd 가 {_fmt(-abs(rxn("LiPO3,Nd2O3")["E_eV_per_P"]))} eV/P 로 이긴다.</p>
<p style="margin:10px 0 0">O 효과가 전압에 평평하고(인산염을 <em>가능</em>하게만 함)
Nd 효과가 6.6 배 커지는 것(Li 가 희소해질수록 값어치가 커짐)이 이 그림에 그대로 맞는다.</p>
</div>

<h3>버려지는 Li 가 어디로 가느냐도 부호를 바꾼다</h3>

<p>P 쪽이 똑같고 <strong>밀려난 Li 3 개의 행선지만</strong> 다른 두 반응:</p>

<div class="rx">Li₂O 로   {r_li2o["reaction"]}
          ΔE = {_fmt(r_li2o["E_eV_per_P"])} eV/P   <span style="color:#6b7280">(Nd 진다)</span>
LiCl 로   {r_licl["reaction"]}
          ΔE = {_fmt(r_licl["E_eV_per_P"])} eV/P   <span style="color:#6d28d9;font-weight:600">(Nd 이긴다)</span></div>

<p>{abs(r_li2o["E_eV_per_P"] - r_licl["E_eV_per_P"]):.2f} eV/P 차이가 통째로 Li₂O 대 LiCl 이다.
아지로다이트에는 f.u. 당 Cl 이 1.6 개 있고, §B 의 hull 이 고른 산물에 실제로
<span class="mono">NdPO₄ + 0.77 LiCl</span> 이 같이 나온다 — <strong>작동하는 채널은 LiCl 쪽</strong>이다.</p>

<h3>살아남은 절반 — P₂S₇ 는 형편없는 P 싱크다</h3>

<div class="rx">P₂S₇ → Nd 인산염   {r_ps7_nd["reaction"]}
                   ΔE = {_fmt(r_ps7_nd["E_eV_per_P"])} eV/P
P₂S₇ → Li 인산염   {r_ps7_li["reaction"]}
                   ΔE = {_fmt(r_ps7_li["E_eV_per_P"])} eV/P</div>

<p>둘 다 −5 eV/P 안팎으로 압도적이다. <strong>O 만 있으면 P 는 어느 쪽이든 인산염으로 간다</strong> —
이것이 O 효과가 전압에 평평한 이유고, §2 가설에서 <strong>살아남은 부분</strong>이다.</p>

<div class="tblwrap">
<table>
<thead><tr><th>상</th><th>묶음</th><th>E_f (eV/atom)</th><th>E_f (eV/P)</th><th>hull 거리</th></tr></thead>
<tbody>
{frows}
</tbody></table>
</div>

<div class="card warn">
<p style="margin:0"><strong>⚠ E_f/P 열은 반응에너지가 아니다.</strong> O:P 비가 다른 상을
한 줄에 놓으면 P–O 결합 수 차이를 P 하나당으로 뭉갠다 — <strong>순위 힌트</strong>다.
판정은 위 균형반응이 한다. 반응물·생성물 집합도 <strong>사람이 고른 것</strong>이고,
hull 이 고르는 판정은 §4 쪽이다.</p>
</div>
""")

if have_kinks:
    import statistics as _st
    srow = []
    for e in ELECS:
        mins, nsink, ntot, areas = [], 0, 0, []
        # ⚠ kink 비율은 **전 조건**(4 양극 × 6 전압)이다 — 깊이·넓이는 4.5 V 다.
        #   처음엔 셋 다 4.5 V 로 세어 놓고 본문에 "전 조건" 이라 썼다 (301 vs 1732).
        for c in CATS:
            for _V in VS:
                kk = D["results"][c]["kinks"][f"{_V:.2f}"].get(e) or []
                nsink += sum(1 for k in kk if prods(k["reaction"]) & SINK)
                ntot += len(kk)
        for c in CATS:
            ks = sorted(D["results"][c]["kinks"]["4.50"].get(e) or [],
                        key=lambda k: k["x_atomic_frac"])
            if len(ks) < 2:
                continue
            mins.append(min(k["reaction_energy_eV_per_atom"] for k in ks))
            areas.append(sum(
                0.5 * (ks[i + 1]["x_atomic_frac"] - ks[i]["x_atomic_frac"])
                * (ks[i]["reaction_energy_eV_per_atom"]
                   + ks[i + 1]["reaction_energy_eV_per_atom"])
                for i in range(len(ks) - 1)))
        srow.append((e, _st.mean(mins), _st.mean(areas), nsink, ntot))
    trs = "\n".join(
        f'<tr><td>{LAB_HTML.get(e, e)}</td><td>{m:+.4f}</td><td>{a:+.4f}</td>'
        f'<td class="{"nd" if ns else ""}">{ns}/{nt} = {100*ns/nt:.0f}%</td></tr>'
        for e, m, a, ns, nt in srow)
    best = min(srow, key=lambda r: -r[1])
    sec.append(f"""
<h2>4. 전 혼합범위 스캔 — 최소점 하나가 아니라 곡선 전체</h2>

<p class="plain">익숙한 것에 빗대면 <b>물감 두 색을 맞대고 문지른 자리</b>다.
경계가 칼로 자른 듯 한 줄이 아니라, <b>섞인 띠</b>가 생기고 그 띠 안에서 자리마다
섞인 비율이 다르다. 여기 <b>x 축이 그 비율</b>이다 — x=0 은 양극만, x=1 은 전해질만,
가운데는 반반. 비율이 달라지면 <b>거기서 생기는 물질도 달라진다</b>.</p>

<p>지금까지 쓴 값은 <strong>가장 깊은 kink 하나</strong>였다. 도구가 나머지를 계산해 놓고
버리고 있었다 — 이제 전 kink 를 남긴다(조건당 16–18 개). 그러면 Richards/Ong 식
<em>반응에너지 vs 혼합비 x</em> 곡선이 통째로 그려진다.</p>

<figure>
<img src="cei_x_scan_panels.png" alt="Six panels of interfacial reaction energy versus electrolyte mixing fraction, one per electrolyte, each with six voltage curves. The two Nd-containing panels are dense with markers showing Nd-phosphate-forming kinks; the four non-Nd panels have none.">
<figcaption><b>Fig. 5. Interfacial reaction energy across the full mixing range</b>
(after Richards <i>et al.</i>, <i>Chem. Mater.</i> <b>28</b>, 266, 2016). Each panel is one
electrolyte composition against the {CAT_X} cathode; the six curves are the applied voltages
(light yellow 2.5&#8201;V to dark red 4.5&#8201;V). <i>x</i> is the atomic fraction of electrolyte in the
mixture, so <i>x</i>&#8201;=&#8201;0 is pure cathode and <i>x</i>&#8201;=&#8201;1 pure electrolyte. Triangles mark the
minimum of each curve; open circles mark kinks whose product set contains an Nd phosphate.
Voltage is a sequential variable and is therefore mapped to a monotone lightness ramp rather
than to the element palette used elsewhere.</figcaption>
</figure>

<div class="figexp">
<div class="figexp-h">Fig. 5 를 읽는 법</div>
<p><b>곡선 하나가 전압 하나</b>다. 밝은 노랑이 2.5 V, 진한 적갈이 4.5 V. 아래로 내려갈수록
반응이 잘 일어난다는 뜻이라, <b>곡선이 얕을수록 좋은 전해질</b>이다.</p>
<p>가로축 <i>x</i> 는 섞인 비율이다 — 왼쪽 끝은 양극만, 오른쪽 끝은 전해질만, 가운데가 반반.
곡선이 <b>매끈한 곡선이 아니라 꺾은선</b>인 것이 핵심이다. 꺾이는 점마다 <b>생기는 물질 조합이
통째로 바뀐다.</b> ▽ 는 그중 제일 깊은 자리, 즉 <b>제일 심하게 반응하는 비율</b>이다 —
지금까지 우리가 인용해 온 값이 그 점 하나였다.</p>
<p><b>보라색 빈 동그라미</b>가 이 그림에서 제일 할 말이 많은 표시다. 그 자리에서 나오는
물질 중에 <b>Nd 인산염이 있다</b>는 뜻인데, 아래 줄 가운데·오른쪽(Nd 있는 계) 패널만
빼곡하고 <b>나머지 넷은 하나도 없다.</b> 특정 비율에서만 잠깐 나오는 게 아니라
<i>x</i> 축 거의 전체에 걸쳐 나온다.</p>
<p>⚠ 곡선 아래 넓이를 "총 반응성" 으로 인용하지 않는다. <i>x</i> 는 섞인 비율일 뿐,
실제 계면에서 어느 비율이 실현되는지는 이 계산이 말하지 않는다. 쓸 수 있는 것은
<b>같은 격자 위에서의 순서</b>다.</p>
</div>

<div class="tblwrap">
<table>
<thead><tr><th>전해질</th><th>최소 깊이 (4.5 V)</th><th>∫E dx (4.5 V)</th><th>Nd 인산염 kink (전 조건)</th></tr></thead>
<tbody>
{trs}
</tbody></table>
</div>

<p>양극 4 종 평균이다. <strong>세 지표가 같은 순서</strong>를 준다 —
최소 깊이·곡선 아래 넓이·(앞 절의) 최소 kink 값. 제일 얕은 것이
<strong>{LAB_HTML.get(best[0], best[0])}</strong> ({best[1]:+.4f} eV/atom).</p>

<div class="card answer">
<p style="margin:0"><strong>가장 깨끗한 신호</strong> — Nd 인산염이 나오는 kink 비율이
<strong>이분법</strong>이다. Nd 없는 넷은 <strong>0 %</strong>(전 조건 {sum(nt for e,m,a,ns,nt in srow if e in ("comp1","modelc","lpsocl","o_only_03")):,} kink 중 <strong>0 개</strong>),
Nd 있는 둘은 <strong>{min(100*ns/nt for e,m,a,ns,nt in srow if ns):.0f}–{max(100*ns/nt for e,m,a,ns,nt in srow):.0f} %</strong>. 최소점 하나만 보면 안 보이던 것이다 —
Nd 인산염은 특정 혼합비에서만 나오는 게 아니라 <strong>x 축 거의 전체에 걸쳐</strong> 나온다.</p>
</div>

<div class="card warn">
<p style="margin:0"><strong>⚠ ∫E dx 를 '총 반응성' 으로 인용하지 않는다.</strong> x 는
혼합비일 뿐 실제 계면에서 어느 x 가 실현되는지는 이 계산이 말하지 않는다. 여기서
쓸 수 있는 것은 <strong>같은 격자 위에서의 순서</strong>다.</p>
</div>
""")

if sec:
    (OUT / "sections_new.html").write_text("\n".join(sec), encoding="utf-8")
    print("  sections_new.html", (OUT / "sections_new.html").stat().st_size, "B")

# ── §5 (갭 대상 규칙) 절 생성 — 2026-09-16 개정문 비준 후 ────────────────────
#   ⛔ 종수·전압커버리지를 손으로 치지 않는다. 판별 규칙을 여기서 **다시 계산**해서
#     카드와 화면이 같은 자료를 보게 한다 (둘이 갈라지면 화면이 이긴다 — 사람은 화면을
#     인용하니까. CLAUDE.md §화면·claim 결속 규율).
TM = ("Co", "Ni", "Mn")
ND_E, NON_E = {"nd_only", "modelc_nd"}, {"comp1", "modelc", "lpsocl", "o_only_03"}


def _has_tm(f):
    return any(el in re.findall(r"[A-Z][a-z]?", f) for el in TM)


_seen = {}
for _c in CATS:
    for _V, _row in D["results"][_c]["kinks"].items():
        for _e, _ks in _row.items():
            for _k in _ks:
                for _p in prods(_k["reaction"]):
                    if _p == "Li":
                        continue
                    r = _seen.setdefault(_p, {"e": set(), "V": set()})
                    r["e"].add(_e); r["V"].add(_V)

#: 최소 kink 산물만 셌을 때의 집합 — "36 → 97" 의 앞 숫자를 **여기서 다시 센다**
#:   (앞 숫자를 손으로 치면 kinks 판이 바뀔 때 화면만 옛 숫자를 계속 말한다).
_minset = set()
for _c in CATS:
    for _V, _row in D["results"][_c]["reactions"].items():
        for _e, _rx in _row.items():
            if _rx:
                _minset |= {p for p in prods(_rx) if p != "Li"}

_all = set(_seen)
_ndonly = {p for p in _all if _seen[p]["e"] <= ND_E}
_nononly = {p for p in _all if _seen[p]["e"] <= NON_E}
_both = _all - _ndonly - _nononly
_disc = _ndonly | _nononly
_target = sorted([p for p in _disc if not _has_tm(p)],
                 key=lambda p: (-len(_seen[p]["V"]), p))
#: 이미 측정된 상 (sei_electronic.json 의 frozen-4f 정본). 화면이 자체 보관하지 않고 읽는다.
_ELEC = {}
try:
    _ej = json.load(open("db/properties/sei_electronic.json"))["results"]
    for _k, _v in _ej.items():
        if _k.endswith("_frozen4f") and (_v or {}).get("gap") is not None:
            _ELEC[_k.split("_mp-")[0]] = _v["gap"]
except (OSError, ValueError, KeyError):
    pass


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


trows = "\n".join(
    '<tr><td class="mono">{f}</td><td>{side}</td><td>{v}/6</td><td>{tm}</td></tr>'.format(
        f=p, side=("Nd 계에만" if p in _ndonly else "무Nd 계에만"),
        v=len(_seen[p]["V"]),
        tm=(f'<span class="nd">{_ELEC[_norm(p)]:.4f} eV</span>'
            if _norm(p) in _ELEC else "—"))
    for p in _target)
_done = [p for p in _target if _norm(p) in _ELEC]

sec.append(f"""
<h2>5. 갭 단계(§C)는 무엇을 재나 — 목록을 먼저 박았다</h2>

<p>§4 가 kink 를 전부 남기면서 <strong>산물 집합이 {len(_minset)} → {len(_all)} 종</strong>이 됐다.
즉 갭 단계의 대상 목록이 <strong>어제와 다른 자료 위에 서 있다</strong>. 어느 쪽을 쓸지는
<strong>갭을 한 줄도 돌리기 전에</strong> 정해야 한다.</p>

<div class="tblwrap">
<table>
<thead><tr><th>구분</th><th>종수</th><th>그중 전이금속</th></tr></thead>
<tbody>
<tr><td><strong>양쪽 다 나옴</strong> (도핑 무관)</td><td><strong>{len(_both)}</strong></td><td>{sum(_has_tm(p) for p in _both)}</td></tr>
<tr><td>Nd 계에만</td><td>{len(_ndonly)}</td><td>{sum(_has_tm(p) for p in _ndonly)}</td></tr>
<tr><td>무Nd 계에만</td><td>{len(_nononly)}</td><td>{sum(_has_tm(p) for p in _nononly)}</td></tr>
</tbody></table>
</div>

<div class="card answer">
<p style="margin:0"><strong>{len(_all)} 종 중 {len(_both)} 종이 도핑 여부와 무관하게 똑같이 나온다.</strong>
그 {len(_both)} 종의 갭은 아무리 정확히 재도 <em>"Nd/O 도핑이 부동태에 도움이 되나"</em> 에
<strong>답을 못 한다</strong> — 양쪽 표에 같은 숫자가 두 번 적힐 뿐이다.</p>
</div>

<p class="plain">익숙한 것에 빗대면 <b>XRD 패턴 두 장을 겹쳐 보는 일</b>이다.
도핑한 시료와 안 한 시료의 패턴에서 <b>공통 피크는 차이를 말해 주지 않는다</b> —
아무리 정밀하게 재도 양쪽에 똑같이 있으니까. 말해 주는 것은 <b>한쪽에만 있는 피크</b>다.
여기서도 똑같다. 그래서 다음 단계(밴드갭)는 <b>한쪽 계에만 나오는 상</b>만 잰다.</p>

<h3>그래서 대상 = 판별종 ∧ 전이금속 비포함 = {len(_target)} 종</h3>

<div class="tblwrap">
<table>
<thead><tr><th>상</th><th>어느 쪽에만</th><th>전압 커버리지</th><th>이미 측정된 갭</th></tr></thead>
<tbody>
{trows}
</tbody></table>
</div>

<p>{len(_done)} 종은 이미 있다 (<span class="mono">{', '.join(_done)}</span>, frozen-4f,
2026-08-12 마감). ⇒ <strong>신규는 {len(_target) - len(_done)} 종</strong>.
전압 6 구간 전부에 나오는 것은 <strong>{_target[0]}</strong> 하나뿐이라, 그것을
<strong>파일럿</strong>으로 먼저 완주하고 실측 벽시계로 나머지를 추정한다.</p>

<div class="card warn">
<p style="margin:0"><strong>⛔ 무엇을 왜 뺐는지는 예산이 아니라 논증이다.</strong></p>
<ul style="margin:8px 0 0">
<li><strong>{len(_both)} 종</strong> — <strong>판별력이 없어서</strong> 뺀다. 공짜로 줘도 이 질문엔 못 쓴다.</li>
<li><strong>전이금속 판별종 {len(_disc) - len(_target)} 종</strong> — ① PBE 가 모트 절연체 갭을 크게
과소평가한다 (문헌 상식, 우리 측정 아님) ② 자기 배열마다 갭이 달라
<strong>스칼라 보고량이 정의되지 않는다</strong>. 카드 판정 기준 그대로다 —
<em>"admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라 보고량은 정의되지 않는다."</em></li>
<li>⚠ 이건 <strong>해결이 아니라 회피</strong>다. 나중에 "CEI 전체가 절연이다" 를 말하고 싶어지면
이 문제를 다시 마주친다.</li>
</ul>
</div>

<p class="plain">익숙한 것에 빗대면 <b>코팅의 핀홀</b>이다. 갭이 크다는 것은
그 층이 <b>전자를 안 흘린다</b>는 뜻이고, 전자가 계면을 못 건너가면 반응이 거기서 멈춘다 —
그게 부동태다. 다만 층이 아무리 절연이어도 <b>구멍이 하나 뚫려 이어져 있으면</b> 거기로
샌다. 갭 계산은 <b>재료가 막을 성질을 갖는지</b>만 말하고 <b>실제로 구멍 없이 덮였는지</b>는
말하지 않는다.</p>

<h3>결과 보기 전에 박은 문턱</h3>
<ul>
<li><strong>G1</strong> — 차이라고 부를 최소폭 <strong>0.30 eV</strong>. 근거는 관측된 재현 폭 둘:
comp1 2.066 vs 재계산 2.0656 (같은 방법) · Nd₂O₃ 우리 3.9479 vs MP 3.8118 (다른 방법, Δ0.136).
큰 쪽의 약 2 배. ⚠ 이 계의 잡음에서 유도한 값이 <strong>아니다</strong>.</li>
<li><strong>G2</strong> — Nd 판별종의 <strong>최소 갭</strong> vs P₂O₅ 갭. 0.30 eV 이상 작으면
"Nd 는 더 새는 층을 추가한다", 반대면 "Nd 층도 절연", 그 미만이면
<strong>"구분되지 않는다"</strong> (0 이라고 하지 않는다).</li>
<li><strong>G3</strong> — 이것이 Nd/O 부동태 카드 §5-c 의 <em>"Nd 가 O 의 이득을 상쇄한다"</em>
가설에 대한 <strong>갭 축 직접 판정</strong>이다. 구동력 축에서는 §1 이 이미 가법성으로 기각했다.</li>
<li><strong>G4</strong> — frozen-4f 로 갭이 0 근처면 <strong>metal 로 선언하지 않는다</strong>.
`undetermined` 로 두고 blocker 를 적는다.</li>
<li><strong>G5 ⛔</strong> — 갭으로 <strong>부동태 결론을 내지 않는다</strong>. 연속성·두께·Li⁺ 전도가
이 계산에 없다. §C 는 "이 층이 전자를 막을 성질을 갖는가" 까지만 답한다.</li>
</ul>

<p style="color:var(--mut);font-size:.87rem">개정문
<code>cathode_cei_gap_target_amendment_2026_09_16</code> (ratified, 결과 보기 전 봉인) ·
결정 <code>D-2026-09-16-cathode-cei-gap-target</code> (active).
위 종수·전압 커버리지는 이 화면이 <strong>원자료에서 다시 계산</strong>한 것이다 —
카드와 화면이 같은 JSON 을 본다.</p>
""")
(OUT / "sections_new.html").write_text("\n".join(sec), encoding="utf-8")
print("  sections_new.html (§5 포함)", (OUT / "sections_new.html").stat().st_size, "B")

# ══ Fig 6 — 3가 도펀트 7종 x-스캔 (2026-09-16) ═══════════════════════════════
#   ⚠ 이 그림의 요점은 **곡선이 아니라 표식**이다. 곡선끼리는 M 간 폭이 0.008 eV/atom
#     (사전 봉인 ±0.010 미만)이라 눈으로 구분되지 않는다. 갈리는 것은 **어느 kink 에서
#     M-인산염이 나오느냐**다. 곡선을 겹쳐 그려 "차이가 없다" 를 보이고, 표식으로
#     "그런데 산물은 다르다" 를 보인다.
import glob as _glob, os as _os
_DF = sorted(_glob.glob("db/properties/dopant_iface_*_2026_09_16.json"))
if _DF:
    _MS = [_os.path.basename(f).split("_")[2] for f in _DF]
    _D = {m: json.load(open(f))["results"] for m, f in zip(_MS, _DF)}
    _ORDER = [m for m in ("Al", "Sc", "Y", "La", "Ce", "Gd", "Nd") if m in _D]
    _CAT = "NMC811" if "NMC811" in _D[_ORDER[0]] else list(_D[_ORDER[0]])[0]
    _VS = ["2.50", "3.50", "4.30", "4.50"]
    _RAMP = ["#fcd34d", "#f59e0b", "#c2410c", "#7f1d1d"]

    def _els(f):
        return set(re.findall(r"[A-Z][a-z]?", f))

    def _plist(r):
        return [re.sub(r"^[0-9.eE+-]+\s+", "", t.strip())
                for t in r.split("->", 1)[1].split("+") if t.strip()]

    fig, axs = plt.subplots(2, 4, figsize=(15.0, 7.2), sharex=True, sharey=True)
    for ax, m in zip(axs.ravel(), _ORDER + ["base"]):
        key = m
        for V, col in zip(_VS, _RAMP):
            row = _D[_ORDER[0] if m == "base" else m][_CAT]["kinks"][V]
            ks = sorted(row.get(key) or [], key=lambda k: k["x_atomic_frac"])
            if not ks:
                continue
            x = [k["x_atomic_frac"] for k in ks]
            y = [k["reaction_energy_eV_per_atom"] for k in ks]
            ax.plot(x, y, lw=1.6, color=col, label=f"{float(V):g} V", zorder=2)
            if m != "base":
                sx = [k["x_atomic_frac"] for k in ks
                      if any({m, "P", "O"} <= _els(p) for p in _plist(k["reaction"]))]
                sy = [k["reaction_energy_eV_per_atom"] for k in ks
                      if any({m, "P", "O"} <= _els(p) for p in _plist(k["reaction"]))]
                if sx:
                    ax.plot(sx, sy, ls="none", marker="o", ms=3.4, mfc="none",
                            mec=ND, mew=1.1, zorder=4)
        apply_axes(ax, None, None)
        ax.axhline(0, color=MUT, lw=0.8, ls="--")
        ax.set_title("undoped (base)" if m == "base" else f"{m} only",
                     fontsize=10, color=(MUT if m == "base" else INK))
    for ax in axs[1]:
        ax.set_xlabel("$x$  (atomic fraction of electrolyte)", fontsize=10, color=INK)
    for ax in axs[:, 0]:
        ax.set_ylabel("Reaction energy (eV/atom)", fontsize=10, color=INK)
    axs[0, 0].legend(frameon=False, fontsize=8, ncol=2, title="vs Li/Li$^+$",
                     title_fontsize=8, loc="lower left")
    # 표식 범례는 **표식이 하나도 없는 패널**(undoped)에 둔다 — 거기가 비어 있기도 하고,
    # "0 개인 패널" 옆에 범례가 있는 편이 대비가 읽힌다.
    _h, = axs[1, 3].plot([], [], ls="none", marker="o", ms=4, mfc="none", mec=ND,
                         mew=1.1, label="kink forms an M-phosphate")
    axs[1, 3].legend(handles=[_h], frameon=False, fontsize=8, loc="upper right")
    fig.suptitle(f"Trivalent dopants across the mixing range  (cathode {_CAT}) — "
                 f"the curves overlap; the products do not",
                 fontsize=11, color=INK, y=0.995)
    fig.tight_layout()
    fig.savefig(OUT / "cei_dopant_x_scan.png", dpi=300)
    plt.close(fig)

    with open(OUT / "cei_dopant_x_scan.csv", "w", newline="") as f:
        w7 = csv.writer(f)
        w7.writerow(["cathode", "dopant", "voltage_V", "x_atomic_frac",
                     "reaction_energy_eV_per_atom", "forms_M_phosphate", "reaction"])
        for m in _ORDER:
            for c in _D[m]:
                for V in _VS:
                    for k in sorted(_D[m][c]["kinks"][V].get(m) or [],
                                    key=lambda k: k["x_atomic_frac"]):
                        hit = any({m, "P", "O"} <= _els(p) for p in _plist(k["reaction"]))
                        w7.writerow([c, m, V, k["x_atomic_frac"],
                                     k["reaction_energy_eV_per_atom"], int(hit),
                                     k["reaction"]])
    print("  cei_dopant_x_scan.png / .csv")


# ══ §6 + Fig 7 — dual compatibility (2026-09-16) ═════════════════════════════
#   출처: cha2024 (Li₂ZrCl₆ 이 NCM·LPSCl **양쪽**과 호환) 을 읽고 찾은 "우리가 안 한 검사".
#   §B 는 전해질 vs 양극만 봤다. 사이에 생기는 CEI 상이 **전해질 쪽과도** 괜찮은지는 미검사였다.
#   ⛔ 숫자를 손으로 치지 않는다 — JSONL·사다리 JSON 에서 읽고, ρ·p 도 여기서 **다시 센다**.
DC_JL = "db/properties/dual_compat_closed_2026_09_16.jsonl"
VOX_J = "db/properties/product_vox_ladder_result_2026_09_16.json"

#: 무도핑 전해질 기준 (도핑 쪽은 hull 기준선 이동과 분리 안 돼 화면에 안 올린다 — 카드 §6)
_DCE = "LPSCl1.6"
_dc, _dcx = {}, {}
for _ln in open(DC_JL, encoding="utf-8"):
    _r = json.loads(_ln)
    if _r.get("species") != _DCE or "dE_eV_per_atom" not in _r:
        continue
    _dc[_r["cathode"]] = _r["dE_eV_per_atom"]
    _dcx[_r["cathode"]] = _r.get("mixing_x")
assert len(_dc) == 10, f"§6: 무도핑 쌍이 10 이어야 하는데 {len(_dc)} — JSONL 이 바뀌었다"

#: x-재검사 파일이 있으면 `mixing_x` 를 그쪽으로 덮는다. 본 JSONL 의 16 쌍은
#: `mixing_x` 필드를 넣기 **전** 실행이라 x 가 None 이다 — 없는 값을 숫자로 그리지 않는다.
_XJL = Path("db/properties/dual_compat_li3po4_xcheck_2026_09_16.jsonl")
if _XJL.exists():
    for _ln in _XJL.read_text(encoding="utf-8").splitlines():
        _r = json.loads(_ln)
        if _r.get("species") == _DCE and _r.get("mixing_x") is not None:
            _dcx[_r["cathode"]] = _r["mixing_x"]

#: V_ox 는 사다리 기록에서. R2 목록("LiPO3 4.980")이 **화학식과 값을 같이** 들고 있는
#: 유일한 자리라 거기서 읽고, 실측_V 의 전정밀 값으로 승격하면서 **1:1 대응을 검사**한다.
#: (대응이 깨지면 그림을 그리지 않고 죽는다 — 축이 조용히 틀리는 게 최악이다.)
_vl = json.load(open(VOX_J, encoding="utf-8"))
_vox = {}
for _k in ("통과", "미달"):
    for _s in _vl["R2_4.5V_게이트"][_k]:
        _f, _v = _s.rsplit(" ", 1)
        _vox[_f] = float(_v)
_full = [e["V_ox"] for e in _vl["실측_V"].values() if e.get("V_ox") is not None]
for _f in list(_vox):
    _m = [x for x in _full if round(x, 3) == round(_vox[_f], 3)]
    assert len(_m) == 1, f"§6: {_f} 의 V_ox {_vox[_f]} 가 실측_V 에 1:1 로 없다 ({_m})"
    _vox[_f] = _m[0]
assert len(_vox) >= 5, f"§6: V_ox 가 {len(_vox)} 개뿐 — 사다리 기록이 바뀌었다"

#: 두 축을 다 가진 상 = 트레이드오프 점. Li₃PS₄ 는 전해질 자신이라 §6 대상이 아니다
#: (dual-compat 실행에 안 넣었으므로 교집합에서 자동으로 빠진다).
_pts = sorted((f for f in _dc if f in _vox), key=lambda f: _vox[f])
assert len(_pts) == 4, f"§6: 트레이드오프 점이 4 여야 하는데 {len(_pts)} — {_pts}"


def _op(f):
    """O/P 응축도. Li₃PO₄ 4.0 · Li₄P₂O₇ 3.5 · LiPO₃ 3.0 · NdP₅O₁₄ 2.8."""
    c = _counts(f)
    return (c.get("O", 0.0) / c["P"]) if c.get("P") else None


def _lip(f):
    c = _counts(f)
    return (c.get("Li", 0.0) / c["P"]) if c.get("P") else None


def _klass(f):
    c = _counts(f)
    if c.get("S") and c.get("O"):
        return "sulfate"
    if not c.get("P"):
        return "halide"
    o = _op(f)
    return ("ortho" if o >= 3.9 else "pyro" if o >= 3.4 else
            "meta" if o >= 2.95 else "ultra")


#: ρ 와 정확순열 p 를 **여기서 다시 센다** — 카드에 적힌 값을 옮겨 적지 않는다.
from itertools import permutations as _perm
_ey = [_dc[f] for f in _pts]                       # V_ox 오름차순으로 정렬된 ΔE
_n = len(_ey)
_rx = sorted(range(_n), key=lambda i: _vox[_pts[i]])
_ry = sorted(range(_n), key=lambda i: _ey[i])
_d2 = sum((_rx.index(i) - _ry.index(i)) ** 2 for i in range(_n))
_rho = 1 - 6 * _d2 / (_n * (_n * _n - 1))
_mono = sum(1 for p in _perm(_ey) if all(p[i] > p[i + 1] for i in range(_n - 1)))
_ptot = 1
for _i in range(1, _n + 1):
    _ptot *= _i
_pval = _mono / _ptot
assert abs(_rho + 1.0) < 1e-9, f"§6: ρ 가 −1 이 아니다 ({_rho}) — 단조가 깨졌으면 §6 문구를 다시 써야 한다"

# ── Fig 7 ────────────────────────────────────────────────────────────────────
_KC = {"ortho": ELEM.get("O", "#be123c"), "pyro": "#ea580c", "meta": ELEM.get("P", "#7c3aed"),
       "ultra": "#1d4ed8", "halide": ELEM.get("Cl", "#65a30d"), "sulfate": ELEM.get("S", "#c05621")}
_TEX = {"Li3PO4": "Li$_3$PO$_4$", "Li4P2O7": "Li$_4$P$_2$O$_7$", "LiPO3": "LiPO$_3$",
        "LiNd(PO3)4": "LiNd(PO$_3$)$_4$", "NdPO4": "NdPO$_4$", "Nd(PO3)3": "Nd(PO$_3$)$_3$",
        "NdP5O14": "NdP$_5$O$_{14}$", "NdCl3": "NdCl$_3$", "Li2SO4": "Li$_2$SO$_4$",
        "Nd2(SO4)3": "Nd$_2$(SO$_4$)$_3$"}

_fig, (_a, _b) = plt.subplots(1, 2, figsize=(11.2, 4.4))

_a.plot([_vox[f] for f in _pts], _ey, color=MUT, lw=1.0, ls="--", zorder=1)
for _f in _pts:
    _a.scatter([_vox[_f]], [_dc[_f]], s=78, color=_KC[_klass(_f)], zorder=3,
               edgecolor="white", linewidth=1.0)
    # 오른쪽 끝 점은 라벨을 **왼쪽**으로 붙인다 — 안 그러면 축 밖으로 잘린다(실측).
    _far = _f == _pts[-1]
    _a.annotate(_TEX[_f], (_vox[_f], _dc[_f]), textcoords="offset points",
                xytext=((-9, -13) if _far else (8, -13)), fontsize=9, color=INK,
                ha=("right" if _far else "left"))
_a.margins(x=0.10, y=0.14)
_a.axvline(4.5, color=MUT, lw=0.8, ls=":")
_a.text(4.5, _a.get_ylim()[1], " 4.5 V gate", fontsize=8, color=MUT,
        va="top", ha="left")
_a.set_title(f"(a) Higher oxidation limit, worse toward the electrolyte\n"
             f"$\\rho$ = {_rho:.0f},  exact one-sided $p$ = {_mono}/{_ptot} = {_pval:.3f}",
             fontsize=10, color=INK, pad=8)
apply_axes(_a, "Oxidation limit $V_{ox}$ (V vs Li/Li$^+$)",
           "Reaction energy with SE (eV/atom)", fontsize=10)

_ord = sorted(_dc, key=lambda f: -_dc[f])
_b.barh(range(len(_ord)), [_dc[f] for f in _ord],
        color=[_KC[_klass(f)] for f in _ord], height=0.66)
_b.set_yticks(range(len(_ord)))
_b.set_yticklabels([_TEX[f] for f in _ord], fontsize=9, color=INK)
_b.invert_yaxis()
_b.axvline(0, color=MUT, lw=0.8)
for _i, _f in enumerate(_ord):
    _b.text(_dc[_f] - 0.003, _i, f"{_dc[_f]:.4f}", va="center", ha="right",
            fontsize=8, color=MUT)
_b.set_xlim(min(_dc.values()) * 1.35, 0.012)
_b.set_title("(b) Sulfates are worse than every phosphate", fontsize=10, color=INK, pad=8)
apply_axes(_b, "Reaction energy with SE (eV/atom)", None, fontsize=10)
_hs = [plt.Line2D([], [], marker="s", ls="none", color=_KC[k], label=k)
       for k in ("ortho", "pyro", "meta", "ultra", "halide", "sulfate")]
# 왼쪽 **위**가 비어 있다 (0 에서 왼쪽으로 자라는 막대라 위쪽 짧은 막대 옆이 빈다).
# lower left 에 두면 최하단 Nd2(SO4)3 의 값 라벨을 덮는다 — 실측 확인.
_b.legend(handles=_hs, frameon=False, fontsize=8, loc="upper left", ncol=2)

_fig.suptitle("Dual compatibility of CEI products with LPSCl$_{1.6}$ "
              "(closed system, 0 V, hull-referenced reactants)",
              fontsize=11, color=INK, y=0.995)
_fig.tight_layout()
_fig.savefig(OUT / "cei_dual_compat.png", dpi=300)
plt.close(_fig)

with open(OUT / "cei_dual_compat.csv", "w", newline="", encoding="utf-8") as _f:
    _w = csv.writer(_f)
    _w.writerow(["phase", "electrolyte", "dE_eV_per_atom", "mixing_x", "O_per_P",
                 "Li_per_P", "class", "V_ox_V"])
    for _p in _ord:
        _w.writerow([_p, _DCE, _dc[_p], _dcx.get(_p), _op(_p), _lip(_p), _klass(_p),
                     _vox.get(_p, "")])
print("  cei_dual_compat.png / .csv")


def _h(f):
    """화학식 → 아래첨자 HTML. 이 목록의 화학식엔 첨자 아닌 숫자가 없어서 전부 <sub> 다.

    ⛔ 못 하는 것: 계수(앞자리 숫자)·수화물 점표기·전하. 반응식에는 쓰면 안 된다.
    """
    return re.sub(r"([0-9]+(?:\.[0-9]+)?)", r"<sub>\1</sub>", f)


assert _h("LiNd(PO3)4") == "LiNd(PO<sub>3</sub>)<sub>4</sub>", "§6: _h 가 괄호 화학식을 망가뜨린다"
assert _h("Nd2(SO4)3") == "Nd<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub>", "§6: _h 검산 실패"
assert _h("NdCl3") == "NdCl<sub>3</sub>", "§6: _h 검산 실패"


# ── §6 절 ────────────────────────────────────────────────────────────────────
_r6 = "\n".join(
    '<tr><td class="mono">{f}</td><td>{k}</td><td>{o}</td><td class="mono">{e:+.4f}</td>'
    '<td class="mono">{v}</td></tr>'.format(
        f=_h(_p), k=_klass(_p), o=("&#8212;" if _op(_p) is None else f"{_op(_p):.1f}"),
        e=_dc[_p], v=(f"{_vox[_p]:.3f}" if _p in _vox else "&#8212;"))
    for _p in _ord)
_pmin, _pmax = _pts[0], _pts[-1]
#: x 를 실측했으면 값을, 아니면 "미측정" 이라고 **말한다** — 0 이나 빈칸으로 그리지 않는다.
_x3 = ("x&#8201;=&#8201;%.1f 로 실측했다" % _dcx["Li3PO4"]) if _dcx.get("Li3PO4") is not None \
    else ("x 는 <b>아직 실측 안 했다</b> (그 쌍은 <code>mixing_x</code> 필드를 넣기 전 실행이다) &#8212; "
          "끝점이라는 것은 반응식 좌변에 상대가 없는 데서 <b>추론</b>한 것이다")

sec.append(f"""
<h2 id="s7">7. 반대쪽 접촉 — 이 층은 전해질과도 지내야 한다</h2>

<p>§1&#8211;§6 은 전부 <strong>양극 쪽</strong>을 봤다. 그런데 CEI 는 양극과 전해질
<strong>사이</strong>에 끼어 있다 &#8212; 한쪽만 검사한 셈이다. 그래서 §2 의 산물을
<strong>전해질(LPSCl<sub>1.6</sub>)에 직접 붙여</strong> 닫힌계 0&#8201;V 로 {len(_dc)} 종을 다시 쟀다.
대조군으로 <strong>무도핑 경로의 산물(Li<sub>3</sub>PO<sub>4</sub>&#183;LiPO<sub>3</sub>)</strong>을 같이 넣었다 &#8212;
없으면 <em>"우리 산물이 전해질과 싸운다"</em> 를 해석할 수 없다.</p>

<div class="tblwrap">
<table>
<thead><tr><th>상</th><th>분류</th><th>O/P</th><th>전해질과의 &Delta;E (eV/atom)</th><th>V<sub>ox</sub> (V)</th></tr></thead>
<tbody>
{_r6}
</tbody></table>
</div>

<figure>
<img src="cei_dual_compat.png" alt="Left: reaction energy with the electrolyte plotted against oxidation limit for four lithium phosphates, falling monotonically. Right: horizontal bars ranking ten phases by reaction energy with the electrolyte, with the two sulfates at the bottom.">
<figcaption><b>Fig. 7. Dual compatibility of the interphase products.</b>
(a) Reaction energy of each product with the electrolyte LPSCl<sub>1.6</sub>
(Li<sub>5.4</sub>PS<sub>4.4</sub>Cl<sub>1.6</sub>), evaluated in a closed system at 0&#8201;V with
<i>use_hull_energy</i>&#8201;=&#8201;true, plotted against the oxidation limit V<sub>ox</sub> of the same
phase taken from the lithium-budget ladder. Only the four phases for which both quantities are
defined are shown; V<sub>ox</sub> is undefined for the lithium-free phases. The four points fall
monotonically (Spearman &rho;&#8201;=&#8201;{_rho:.0f}); with the direction registered in advance,
the exact one-sided permutation probability is {_mono}/{_ptot}&#8201;=&#8201;{_pval:.3f}.
The dotted line marks the 4.5&#8201;V design gate.
(b) All {len(_dc)} products ranked by the same quantity and coloured by class. Zero means the two
phases coexist with no driving force to react; more negative means a stronger mutual reaction.
Both sulfates lie below every phosphate.</figcaption>
</figure>

<div class="figexp">
<div class="figexp-h">Fig. 7 을 읽는 법</div>
<p><b>왼쪽 그림</b>의 가로축은 <b>"이 상이 몇 볼트까지 버티나"</b>(양극 쪽 요구),
세로축은 <b>"이 상이 전해질과 얼마나 싸우나"</b>(전해질 쪽 요구)다. 세로축이
<b>0 이면 안 싸우는 것</b>이고 아래로 내려갈수록 더 싸운다. 네 점이
<b>오른쪽 아래로 완전히 단조</b>다 &#8212; <b>전압에 강해질수록 전해질과 더 싸운다.</b>
두 요구가 같은 방향이면 좋은 상을 하나 고르면 되는데, <b>반대 방향이라 고를 수가 없다.</b></p>
<p>점선이 4.5&#8201;V 설계 문턱이다. 그 선 <b>왼쪽</b>에 있는
{_h(_pmin)} 는 전해질과 제일 잘 지내지만(&Delta;E&#8201;=&#8201;{_dc[_pmin]:+.4f})
<b>전압을 못 버틴다</b>({_vox[_pmin]:.3f}&#8201;V). 오른쪽 끝의 {_h(_pmax)} 는
전압은 제일 잘 버티는데({_vox[_pmax]:.3f}&#8201;V) 전해질과 제일 많이 싸운다
({_dc[_pmax]:+.4f}). <b>그 둘이 같은 그림의 양 끝</b>이라는 게 이 절의 요지다.</p>
<p><b>오른쪽 그림</b>은 {len(_dc)} 종 전체 순위다. 색이 분류인데, 인산염은
<b>응축될수록</b>(ortho&#8594;meta&#8594;ultra) 아래로 내려간다. 그런데 <b>황산염 둘이
모든 인산염보다 더 아래</b>에 있다 &#8212; 응축도 축으로 설명되지 않는 <b>별도 위험</b>이다.</p>
<p>⚠ 왼쪽 네 점은 <b>독립 표본이 아니라 한 화학 계열 위의 네 점</b>이다.
{_pval:.3f} 은 <b>순서에 대한 순열 확률</b>이지 "일반적으로 성립한다" 는 뜻이 아니다.
게다가 넷 다 <b>Li 를 품은 인산염</b>이라 응축도와 Li 함량이 이 계열에서는 분리되지 않는다 &#8212;
기전 문장은 "인산염 일반" 이 아니라 <b>"Li-인산염 응축 계열"</b> 로 좁혀 써야 한다.</p>
</div>

<p class="plain">익숙한 것에 빗대면 <b>양면 테이프</b>다. 한쪽 면은 양극에, 다른 쪽 면은
전해질에 붙어야 하는데, <b>한쪽에 잘 붙는 배합일수록 다른 쪽에는 잘 안 붙는</b> 상황이다.
한 면만 시험해 보고 "좋은 테이프" 라고 하면 안 되는 이유가 이것이고,
지금까지 우리가 본 것이 <b>딱 한 면</b>이었다.</p>

<div class="card warn" data-claim="dualcompat.sulfate.risk">
<p style="margin:0"><strong>🔴 우리한테 불리한 발견도 같이 나왔다.</strong>
<span class="claim-mark">[불리]</span></p>
<p style="margin:8px 0 0">Li<sub>2</sub>SO<sub>4</sub> 는 <strong>&Delta;E&#8201;=&#8201;{_dc["Li2SO4"]:+.4f}</strong> 로
전체 {len(_dc)} 종 중 아래에서 두 번째다. 그런데 이 상은 §2 산물 인구조사에서
<strong>가장 많이 나온 상(65 회)</strong>이다 &#8212; <strong>우리가 제일 많이 만든다고 예측하는 상이
전해질 쪽에서는 거의 최악</strong>이다. 제일 나쁜 Nd<sub>2</sub>(SO<sub>4</sub>)<sub>3</sub>
({_dc["Nd2(SO4)3"]:+.4f}) 도 황산염이다. 유리한 쪽만 싣는 화면은 원장이 아니라 광고다.</p>
</div>

<div class="card" data-claim="dualcompat.doping.defensive">
<p style="margin:0"><strong>도핑이 이 접촉을 <em>새로</em> 망가뜨리지는 않는다 &#8212; 그러나 우위 논거는 아니다.</strong></p>
<p style="margin:8px 0 0">무도핑 경로가 3.5&#8201;V 에서 실제로 만드는
LiPO<sub>3</sub> 가 <strong>{_dc["LiPO3"]:+.4f}</strong>, 도핑 경로의
LiNd(PO<sub>3</sub>)<sub>4</sub> 가 <strong>{_dc["LiNd(PO3)4"]:+.4f}</strong> 다.
차이 {abs(_dc["LiPO3"] - _dc["LiNd(PO3)4"]):.4f}&#8201;eV/atom 은 이 계산의 해상도 안쪽이고,
우리는 이 양에 대한 문턱을 <strong>사전에 정해 둔 적이 없다</strong>.
⇒ <strong>"둘은 구분되지 않는다"</strong> 라고만 쓴다. <em>"도핑이 더 낫다"</em> 도
<em>"더 나쁘다"</em> 도 쓰지 않는다.</p>
</div>

<div class="card warn">
<p style="margin:0"><strong>⛔ 이 절에서 철회된 것 하나</strong></p>
<p style="margin:8px 0 0">처음 {len(_dc) - 2} 종만 봤을 때 <em>"O/P 응축도 <strong>하나로</strong>
&Delta;E 가 단조 정렬된다"</em> 고 적었다. 그 뒤 <strong>결과를 보기 전에 등록한 예측</strong>대로
Li<sub>4</sub>P<sub>2</sub>O<sub>7</sub> 을 넣었더니 <strong>{_dc["Li4P2O7"]:+.4f}</strong> 로,
O/P 가 더 큰 NdPO<sub>4</sub>({_dc["NdPO4"]:+.4f}) 보다 <strong>덜</strong> 반응했다 &#8212;
단일 축이면 불가능한 순서다. <strong>철회한다.</strong> 대신 계열을 나누면
(Li 계열 / Nd 계열) 각각 단조이고 같은 O/P 에서 Nd 쪽이 더 음수인데,
이건 <strong>데이터를 보고 만든 가설(post-hoc)</strong>이라 검정이 아니다.
같은 실행에서 등록했던 <strong>다른</strong> 예측(Li<sub>2</sub>SO<sub>4</sub> &lt; &#8722;0.05)은 통과했고,
등록했던 <strong>검정</strong>(위 Fig. 7a)도 통과했다.</p>
</div>

<div class="card warn">
<p style="margin:0"><strong>⛔ 같은 명령의 열린계 실행은 무효다 &#8212; 그 산물 목록을 §6 대상으로 쓰지 않는다</strong></p>
<p style="margin:8px 0 0">같은 8 상대를 3.5/4.0/4.3&#8201;V <strong>열린계</strong>로도 돌렸는데,
<strong>여섯 상대에서 숫자가 글자 그대로 같았고</strong> 반응식 좌변에 상대가 <strong>없었다</strong>.
최소 kink 가 x&#8201;=&#8201;0 끝점에 걸려 <strong>전해질 혼자 분해되는 에너지</strong>를 여섯 번
다시 잰 것이다 &#8212; 상대는 계산에 한 번도 안 들어갔다. 오류도 안 났고 값도 그럴듯했다.
그 실행의 인구조사가 PCl<sub>5</sub>&#183;P<sub>2</sub>S<sub>7</sub>&#183;SCl 을 48 회씩
<strong>거짓 꼬리표</strong>를 달고 §6 후보로 올렸다.
파일명에 <span class="mono">_INVALID_endpoint_degenerate</span> 를 박았고, 도구는
끝점을 기록에 남기고 인구조사에서 빼도록 고쳤다.
⚠ 다만 <strong>닫힌계의 끝점은 무효가 아니라 정상 판정</strong>이다
(&ldquo;섞을 구동력 없음&rdquo;) &#8212; 위 표의 Li<sub>3</sub>PO<sub>4</sub> {_dc["Li3PO4"]:+.4f} 가 그 경우이고,
{_x3}. 한 깃발로 읽으면 멀쩡한 판정을 버린다.</p>
</div>

<p style="color:var(--mut);font-size:.87rem">원자료
<code>db/properties/dual_compat_closed_2026_09_16.jsonl</code> ({len(_dc)} 쌍 &times; 전해질 2) ·
결과 <code>dual_compat_result_2026_09_16.json</code> · 판정
<code>dual_compat_amendment_2026_09_16.json</code> · 그림 자료
<code>cei_dual_compat.csv</code>. 위 &rho;&#183;p 와 모든 수치는 이 화면이
<strong>원자료에서 다시 계산</strong>한 것이다. <code>citable: false</code> &#8212; 1저자&#183;리뷰 판정 전이다.</p>
""")
_out6 = "\n".join(sec)
#: 렌더러가 둘(matplotlib · HTML)인 데서 오는 조용한 깨짐을 여기서 막는다 —
#: 2026-09-16 에 §4 표가 `LPSCl$_{1.6}$` 를 날것으로 내보냈다(오류 없음·화면만 깨짐).
#: 쓰기 **전에** 죽는다.
_leak = re.findall(r"\$[_^][^$\n]{0,20}\$", _out6)
assert not _leak, f"생성 HTML 에 matplotlib mathtext 가 샜다: {_leak[:5]}"
(OUT / "sections_new.html").write_text(_out6, encoding="utf-8")
print("  sections_new.html (§6 포함)", (OUT / "sections_new.html").stat().st_size, "B")
