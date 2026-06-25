#!/usr/bin/env python3
"""plot_cascade_v23.py — outlier check + classified plots for the 141-compound
doping cascade (v23, UMA-s-1p1). Source: db/properties/cascade_v23_champions.csv
(rank_combined==1 champions, aggregated from gabia FINAL/dataset).

NOTE the data realities baked in:
  * concentration is 0.25 for ALL rows -> the dir x002/x005/x010 are PLACEMENT
    REPLICATES at x=0.25, NOT a concentration sweep. We treat them as replicates.
  * sigma / Ea / wad columns are EMPTY in dataset.csv -> mobility/adhesion not
    plotted. Metrics available: stability (de), B0, E_young, B/G_hill, nu, pugh.
  * UMA elastic runs HIGH vs experiment -> within-cascade (UMA-vs-UMA) comparison
    only; absolute GPa not physical.
Outliers flagged: EOS fit fail, incomplete champion, unphysical elastic (nu<0,
G>B, E-B-G inconsistency), and per-metric statistical (|z|>2.5).
"""
import csv, re, math, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

CSV = "db/properties/cascade_v23_champions.csv"
OUT = "docs/figures/cascade"; os.makedirs(OUT, exist_ok=True)

LANTH = {"La", "Nd", "Sm", "Gd"}; ALKALI = {"Li", "Na"}
AE = {"Mg", "Ca", "Sr", "Ba"}; MAIN = {"B", "Al", "Ga", "In", "Si", "Ge", "Sn", "Sb"}

def fnum(s):
    try: return float(s)
    except: return math.nan

def parse_dopant(d):
    base = d.split("+")[0]                       # strip +Clrich
    clrich = "Clrich" in d
    toks = re.findall(r"([A-Z][a-z]?)(\d*)", base)
    toks = [(e, int(n) if n else 1) for e, n in toks if e]
    anion = "O" if any(e == "O" for e, _ in toks) else ("F" if any(e == "F" for e, _ in toks) else "?")
    cat = [(e, n) for e, n in toks if e not in ("O", "F")][0]
    av = 2 if anion == "O" else 1
    bn = [n for e, n in toks if e == anion][0]
    val = round(av * bn / cat[1])
    if cat[0] in LANTH: grp = "lanthanide"
    elif cat[0] in ALKALI: grp = "alkali"
    elif cat[0] in AE: grp = "alk.earth"
    elif cat[0] in MAIN: grp = "main-group"
    else: grp = "TM"
    return dict(cation=cat[0], anion=anion, valence=val, group=grp, clrich=clrich)

# ---- load ----
rows = []
for r in csv.DictReader(open(CSV)):
    p = parse_dopant(r["dopant"])
    rows.append(dict(
        dir=r["_dir"], dopant=r["dopant"].split("+")[0], **p,
        de=fnum(r["rerank_de_post_anneal"]), dV=fnum(r["anneal_dV_pct"]),
        B0=fnum(r["eos_B0_GPa"]), eos_ok=(r["eos_fit_quality_ok"] == "True"),
        E=fnum(r["elastic_E_young_GPa"]), B=fnum(r["elastic_B_hill_GPa"]),
        G=fnum(r["elastic_G_hill_GPa"]), nu=fnum(r["elastic_poisson_nu"]),
        pugh=fnum(r["elastic_pugh_GoverB"]), score=fnum(r["combined_score"])))

# ---- outlier detection ----
def zscore(vals):
    v = np.array(vals, float); m = np.nanmean(v); s = np.nanstd(v)
    return (v - m) / s if s else v * 0

flags = {r["dir"]: [] for r in rows}
for r in rows:
    if math.isnan(r["de"]) and math.isnan(r["E"]):
        flags[r["dir"]].append("INCOMPLETE(blank champion)"); continue
    if math.isnan(r["B0"]) or not r["eos_ok"]:
        flags[r["dir"]].append("EOS-fit-fail")
    if not math.isnan(r["nu"]) and r["nu"] < 0:
        flags[r["dir"]].append(f"unphysical nu={r['nu']:.2f}(<0)")
    if not math.isnan(r["G"]) and not math.isnan(r["B"]) and r["G"] > 1.4 * r["B"]:
        flags[r["dir"]].append(f"G>1.4B (pugh={r['pugh']:.2f})")
    if not any(math.isnan(x) for x in (r["E"], r["B"], r["G"])) and r["E"] > 0:
        Epred = 9 * r["B"] * r["G"] / (3 * r["B"] + r["G"])
        if abs(Epred - r["E"]) / r["E"] > 0.10:
            flags[r["dir"]].append("E!=9BG/(3B+G)")
for key, lab in [("de", "de"), ("E", "E_young"), ("B0", "B0")]:
    z = zscore([r[key] for r in rows])
    for r, zz in zip(rows, z):
        if not math.isnan(zz) and abs(zz) > 2.5:
            flags[r["dir"]].append(f"{lab} z={zz:+.1f}")
flagged = {k: v for k, v in flags.items() if v}

# ---- per-dopant aggregate (3 replicates) ----
dops = sorted(set(r["dopant"] for r in rows))
agg = {}
for d in dops:
    rs = [r for r in rows if r["dopant"] == d]
    des = [r["de"] for r in rs if not math.isnan(r["de"])]
    Es = [r["E"] for r in rs if not math.isnan(r["E"]) and (r["nu"] != r["nu"] or r["nu"] >= 0)]  # drop nu<0 elastic
    agg[d] = dict(group=rs[0]["group"], anion=rs[0]["anion"], valence=rs[0]["valence"],
                  de_mean=np.mean(des) if des else math.nan, de_min=min(des) if des else math.nan,
                  de_max=max(des) if des else math.nan,
                  E_mean=np.mean(Es) if Es else math.nan)

ANC = {"O": "#2a6fb0", "F": "#e08a1e"}            # anion colors
VALC = {1: "#9e9e9e", 2: "#7cb342", 3: "#26a69a", 4: "#5c6bc0", 5: "#ab47bc", 6: "#ec407a"}

# ================= FIGURE: 4 panels =================
fig = plt.figure(figsize=(17, 11))

# (A) stability ranking (de) — sorted, colored by anion, replicate spread
ax = fig.add_subplot(2, 2, 1)
order = sorted([d for d in dops if not math.isnan(agg[d]["de_mean"])], key=lambda d: agg[d]["de_mean"])
y = np.arange(len(order))
means = [agg[d]["de_mean"] for d in order]
lo = [agg[d]["de_mean"] - agg[d]["de_min"] for d in order]
hi = [agg[d]["de_max"] - agg[d]["de_mean"] for d in order]   # note de negative; min is most negative
cols = [ANC[agg[d]["anion"]] for d in order]
ax.barh(y, means, color=cols, edgecolor="k", lw=0.3, zorder=3)
ax.errorbar(means, y, xerr=[lo, hi], fmt="none", ecolor="0.3", elinewidth=0.7, capsize=2, zorder=4)
ax.set_yticks(y); ax.set_yticklabels(order, fontsize=6.5)
ax.set_xlabel("formation Δe vs baseline (eV/atom, more negative = more stabilizing)")
ax.set_title("(A) Stability ranking — Gd₂O₃/Ta₂O₅/Nb₂O₅ lead; alkali/late-TM oxides weakest", fontsize=10)
ax.legend(handles=[Patch(fc=ANC["O"], label="oxide"), Patch(fc=ANC["F"], label="fluoride")],
          fontsize=8, loc="lower right"); ax.grid(axis="x", alpha=.3)
ax.axvline(np.nanmean(means), ls="--", color="0.5", lw=1)

# (B) coating map: E_young vs de (valid only), colored by valence
ax = fig.add_subplot(2, 2, 2)
for r in rows:
    if math.isnan(r["E"]) or math.isnan(r["de"]) or (not math.isnan(r["nu"]) and r["nu"] < 0): continue
    ax.scatter(r["de"], r["E"], c=VALC.get(r["valence"], "k"), s=34, edgecolor="white", lw=.5, zorder=3)
# label champions of interest
for d in ["Gd2O3", "Ta2O5", "Sc2O3", "Nd2O3", "WO3", "B2O3", "Al2O3", "Cr2O3"]:
    rs = [r for r in rows if r["dopant"] == d and not math.isnan(r["E"]) and (math.isnan(r["nu"]) or r["nu"] >= 0)]
    if rs:
        r = min(rs, key=lambda r: r["de"])
        ax.annotate(d, (r["de"], r["E"]), fontsize=7, ha="center", va="bottom", xytext=(0, 3), textcoords="offset points")
ax.set_xlabel("formation Δe (eV/atom)"); ax.set_ylabel("E_young (GPa, UMA — relative)")
ax.set_title("(B) Coating map: stable + soft = lower-left = best candidate", fontsize=10)
ax.legend(handles=[Patch(fc=VALC[v], label=f"M{v}+") for v in sorted(VALC) if any(r["valence"] == v for r in rows)],
          fontsize=8, ncol=3, loc="upper left", title="cation valence"); ax.grid(alpha=.3)

# (C) de by valence (strip + mean)
ax = fig.add_subplot(2, 2, 3)
vals = sorted(set(r["valence"] for r in rows))
for i, v in enumerate(vals):
    de = [r["de"] for r in rows if r["valence"] == v and not math.isnan(r["de"])]
    x = np.random.default_rng(v).normal(i, 0.07, len(de))
    ax.scatter(x, de, c=VALC[v], s=26, alpha=.8, edgecolor="white", lw=.4)
    ax.plot([i - 0.25, i + 0.25], [np.mean(de)] * 2, color="k", lw=2, zorder=5)
ax.set_xticks(range(len(vals))); ax.set_xticklabels([f"M{v}+" for v in vals])
ax.set_xlabel("cation valence"); ax.set_ylabel("formation Δe (eV/atom)")
ax.set_title("(C) Stability vs valence — higher charge cation stabilizes more", fontsize=10); ax.grid(axis="y", alpha=.3)

# (D) B0 vs E_young consistency, anion-colored; flag elastic/eos outliers
ax = fig.add_subplot(2, 2, 4)
for r in rows:
    if math.isnan(r["E"]): continue
    bad = (r["dir"] in flagged) and any("nu" in f or "G>" in f or "9BG" in f for f in flagged[r["dir"]])
    if math.isnan(r["B0"]):
        ax.scatter(0, r["E"], marker="x", c="red", s=40, zorder=4)   # eos-fail on B0=NaN -> put at 0
    else:
        ax.scatter(r["B0"], r["E"], c=ANC[r["anion"]], s=34, edgecolor=("red" if bad else "white"),
                   lw=(1.6 if bad else .5), zorder=3)
    if bad:
        ax.annotate(r["dopant"], (r["B0"] if not math.isnan(r["B0"]) else 0, r["E"]),
                    fontsize=7, color="red", xytext=(3, 0), textcoords="offset points")
ax.set_xlabel("EOS B0 (GPa, UMA)  [x=0 → EOS fit FAILED]"); ax.set_ylabel("E_young (GPa, UMA)")
ax.set_title("(D) B0 vs E_young — red ring = elastic outlier, red × = EOS-fit fail", fontsize=10); ax.grid(alpha=.3)

plt.suptitle(f"Doping cascade v23 (UMA-s-1p1) — {len(rows)} champions @ x=0.25  ·  "
             f"{len(flagged)} flagged  ·  classify by anion/valence", fontsize=13, y=1.00)
plt.tight_layout()
plt.savefig(f"{OUT}/cascade_v23_overview.png", dpi=150, bbox_inches="tight")
plt.savefig(f"{OUT}/cascade_v23_overview.pdf", bbox_inches="tight")
print(f"saved {OUT}/cascade_v23_overview.png")

# ---- outlier report (md) ----
with open(f"{OUT}/cascade_v23_outliers.md", "w") as f:
    f.write(f"# Cascade v23 outlier report — {len(rows)} champions, {len(flagged)} flagged\n\n")
    f.write("data: `db/properties/cascade_v23_champions.csv` (UMA-s-1p1, x=0.25, rank-1 champions).\n")
    f.write("ALL concentration=0.25 (x002/05/10 = placement replicates). sigma/Ea/wad empty in dataset.\n\n")
    cats = {"INCOMPLETE": [], "EOS-fit-fail": [], "elastic-unphysical": [], "statistical": []}
    for k, v in flagged.items():
        s = " ; ".join(v)
        if any("INCOMPLETE" in x for x in v): cats["INCOMPLETE"].append((k, s))
        elif any(("nu" in x or "G>" in x or "9BG" in x) for x in v): cats["elastic-unphysical"].append((k, s))
        elif any("EOS" in x for x in v): cats["EOS-fit-fail"].append((k, s))
        else: cats["statistical"].append((k, s))
    for cat, items in cats.items():
        if not items: continue
        f.write(f"## {cat} ({len(items)})\n")
        for k, s in sorted(items): f.write(f"- **{k}** — {s}\n")
        f.write("\n")
print(f"saved {OUT}/cascade_v23_outliers.md  ({len(flagged)} flagged)")

# console summary
print("\n=== FLAGGED ===")
for k in sorted(flagged): print(f"  {k:16s} {' ; '.join(flagged[k])}")
print("\n=== TOP-8 stability (mean de) ===")
for d in sorted(dops, key=lambda d: agg[d]["de_mean"] if not math.isnan(agg[d]["de_mean"]) else 9)[:8]:
    print(f"  {d:8s} de={agg[d]['de_mean']:+.3f}  E={agg[d]['E_mean']:.1f}  M{agg[d]['valence']}+ {agg[d]['anion']} {agg[d]['group']}")
