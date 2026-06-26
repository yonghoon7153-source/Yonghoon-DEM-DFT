#!/usr/bin/env python3
"""plot_cascade_oxidation_vs_banik.py — our cascade per-dopant oxidation onset vs the
Banik 2022 "sulfur pins the oxidation onset" thesis. Banik (Mo+Zeier, our grand-potential
method's home lab): iso-structural substitution (P->Si/Ge, Cl->I) CANNOT move the
S-limited oxidation onset (VBM = non-bonding S 3p). Our heterovalent-oxide cascade mostly
agrees (S-ceiling 2.14 V), but accesses small exceptions Banik's exchange route does not.
3 categories: pinned at the S-limit / raised above (the exceptions) / lowered below (dopant
self-oxidizes first). Source: db/properties/oxidation_stability_cascade.csv (UMA cascade, MP hull).
"""
import csv, io, math
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
OUT = "docs/figures/cascade"
SLIM = 2.14  # S2--limited onset (comp1=modelc, Banik's pinned ceiling)

raw = open("db/properties/oxidation_stability_cascade.csv").read().splitlines()
h = next(i for i, l in enumerate(raw) if l.startswith("dopant,"))
rows = list(csv.DictReader(io.StringIO("\n".join(raw[h:]))))
for r in rows:
    r["ox"] = float(r["ox_V"]); r["win"] = float(r["window_V"])

def cat(r):
    if r["ox"] > SLIM + 0.01: return "raised"          # exception: onset above S-limit
    if abs(r["ox"] - SLIM) <= 0.01: return "pinned"      # at S-limit (Banik)
    if r["win"] < 0.05: return "collapsed"               # late-TM M-redox eats window
    return "lowered"                                     # dopant self-oxidizes below S-limit
COL = {"raised": "#e65100", "pinned": "#1e88e5", "lowered": "#9e9e9e", "collapsed": "#b71c1c"}
LAB = {"raised": "raised > S-limit (EXCEPTION)", "pinned": "pinned at S-limit 2.14 V (Banik)",
       "lowered": "lowered (dopant self-oxidizes first)", "collapsed": "collapsed window (late-TM)"}

rows.sort(key=lambda r: r["ox"])
y = np.arange(len(rows))
fig, ax = plt.subplots(figsize=(10, 13))
ax.axvline(SLIM, color="#1e88e5", ls="--", lw=1.6, zorder=1)
ax.text(SLIM, len(rows) + 0.5, "S²⁻-limit 2.14 V\n(Banik: substitution can't raise)",
        color="#1e88e5", fontsize=8.5, ha="center", va="bottom", fontweight="bold")
for i, r in enumerate(rows):
    c = COL[cat(r)]
    ax.plot(r["ox"], i, "o", ms=8, color=c, zorder=3)
    lab = r["dopant"]
    ax.text(r["ox"] + 0.012, i, lab, fontsize=6.0, va="center",
            color=("k" if cat(r) in ("raised", "pinned") else "0.45"),
            fontweight=("bold" if cat(r) == "raised" else "normal"))
# bracket the exceptions
exc = [i for i, r in enumerate(rows) if cat(r) == "raised"]
if exc:
    ax.annotate("6 exceptions = all trivalent (M³⁺) oxides\nSc·Cr·In·Ga·Y·B₂O₃  (+0.14–0.22 V,\nnew ox-limiting rxn; S-backbone still pinned)",
                xy=(2.30, np.mean(exc)), xytext=(2.40, np.mean(exc) - 9),
                fontsize=8, color="#e65100", ha="center",
                arrowprops=dict(arrowstyle="->", color="#e65100", lw=1.3))
ax.set_yticks([]); ax.set_xlabel("oxidation onset (V vs Li/Li⁺), grand-potential ESW")
ax.set_xlim(1.7, 2.55); ax.set_ylim(-1, len(rows) + 3)
n = {k: sum(1 for r in rows if cat(r) == k) for k in COL}
ax.set_title("Cascade oxidation onset vs the Banik S-pin thesis\n"
             f"pinned {n['pinned']} · raised {n['raised']} (M³⁺ oxides) · lowered {n['lowered']} · collapsed {n['collapsed']}  (of {len(rows)})",
             fontsize=11)
ax.legend(handles=[Patch(fc=COL[k], label=LAB[k]) for k in ["raised", "pinned", "lowered", "collapsed"]],
          fontsize=8.5, loc="lower right")
ax.grid(axis="x", alpha=.3)
plt.tight_layout()
plt.savefig(f"{OUT}/cascade_oxidation_vs_banik.png", dpi=150, bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_oxidation_vs_banik.pdf", bbox_inches="tight")
print(f"saved {OUT}/cascade_oxidation_vs_banik.png")
print("\n=== onset-RAISING exceptions (contra Banik's iso-structural claim) ===")
for r in [r for r in rows if cat(r) == "raised"]:
    print(f"  {r['dopant']:7s} ox={r['ox']:.3f}  val={r['valence']} {r['anion']} {r['group']}  (+{r['ox']-SLIM:.2f} V)")
print(f"\npinned at S-limit: {n['pinned']}  |  lowered(self-ox): {n['lowered']}  |  collapsed: {n['collapsed']}")
print("Banik holds at the S-BACKBONE level for all; the 6 exceptions are heterovalent-oxide")
print("dopants introducing a NEW ox-limiting reaction — a route Banik's P->Si/Ge, Cl->I exchange doesn't access.")
