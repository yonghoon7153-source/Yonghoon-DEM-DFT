"""Richards 2016 (Chem. Mater. 28, 266-273) SI -- Figures S1-S7 vector-exact readout.

Why this is exact, not a pixel estimate
---------------------------------------
The SI figures are matplotlib *vector* drawings embedded in the PDF, so every bar
is a rectangle with analytic coordinates.  Per (electrolyte, cathode) slot the PDF
holds up to two rects:
  * type 'f'  with a PASTEL fill  -> "with mixing"        (eq 4 ; full length)
  * type 'fs' with a SATURATED fill -> "at cathode mu_Li" (eq 5 ; drawn on top)
A series whose value is 0 is simply not drawn.

Calibration: the dotted horizontal gridlines of each axes are extracted from the
same drawing list.  The topmost gridline is the 0 eV line (every bar's top edge
coincides with it); the bottom gridline is the axes floor whose value was read
from a 4x render of each panel (EV_PER_INTERVAL below).

Result: reaction energies in eV per non-Li atom, resolution ~0.001 eV (the read
error is the PDF's own rounding, not our eyes).  Reported to 0.01 in the digest.

Usage:  python tools/litdb/richards2016_si_figs.py [--csv out.csv]
"""
import sys
import fitz

PDF = r"litdb/inbox/39. Sup) Interface Stability in Solid-State Batteries.pdf"

CATHODES = ["LiCoO2", "LiFePO4", "LiMnO2", "LiNiO2", "LiTiS2", "LiVS2", "Li2S"]

SAT = {(0.0, 0.0, 1.0): 0, (0.0, 0.5, 0.0): 1, (0.75, 0.75, 0.0): 2,
       (0.75, 0.0, 0.75): 3, (1.0, 0.0, 0.0): 4, (1.0, 0.647, 0.0): 5,
       (0.0, 0.75, 0.75): 6}
PAS = {(0.408, 0.408, 0.952): 0, (0.204, 0.476, 0.204): 1, (0.714, 0.714, 0.306): 2,
       (0.714, 0.306, 0.714): 3, (0.952, 0.408, 0.408): 4, (0.952, 0.76, 0.408): 5,
       (0.306, 0.714, 0.714): 6}

# (page0, fig, axes inner rect, eV per gridline interval, electrolyte groups L->R)
PANELS = [
    (5, "S1", (222.48, 67.89, 417.87, 264.54), 2.0,
     ["Li3N", "Li3BN2", "Li4NCl"]),
    (6, "S2", (224.14, 461.09, 418.56, 659.21), 0.5,
     ["LiH", "LiBH4"]),
    (7, "S3", (208.76, 455.44, 433.14, 648.93), 0.5,
     ["Li2S", "Li3PS4", "Li10GeP2S12", "Li4SnS4", "Li6PS5Cl"]),
    (9, "S4a", (198.03, 178.78, 441.33, 355.54), 0.2,
     ["Li2O", "LiAlO2", "Li4Ti5O12", "Li2ZrO3", "Li7La3Zr2O12", "Li4GeO4"]),
    (9, "S4b", (198.03, 395.78, 441.33, 572.53), 0.2,
     ["LiNbO3", "Li3.2PO3.8N0.2", "Li3PO4", "LiGe2(PO4)3", "LiTi2(PO4)3", "Li3OCl"]),
    (13, "S5", (198.03, 114.29, 441.33, 291.04), 0.1,
     ["LiBr", "Li2MgBr4", "LiAlBr4", "Li2ZnBr4", "Li2MnBr4", "Li3InBr6"]),
    (13, "S6", (208.80, 452.35, 433.14, 645.84), 0.1,
     ["LiCl", "Li2MgCl4", "Li2ZnCl4", "LiAlCl4", "Li2CdCl4"]),
    (15, "S7", (228.33, 454.52, 418.13, 652.90), 0.05,
     ["LiF", "LiYF4", "Li3AlF6", "Li2ZrF6"]),
]


def panel_gridlines(page, ax):
    x0, y0, x1, y1 = ax
    ys = set()
    for it in page.get_drawings():
        if it["type"] != "s":
            continue
        for i in it["items"]:
            if i[0] == "l":
                a, b = i[1], i[2]
                if abs(a.y - b.y) < 0.1 and (b.x - a.x) > 100 and y0 - 1 <= a.y <= y1 + 1:
                    ys.add(round(a.y, 3))
    return sorted(ys)


def panel_bars(page, ax):
    x0, y0, x1, y1 = ax
    out = []
    for it in page.get_drawings():
        fill = it.get("fill")
        if not fill:
            continue
        key = tuple(round(c, 3) for c in fill)
        if it["type"] == "fs" and key in SAT:
            series, ci = "nomix", SAT[key]
        elif it["type"] == "f" and key in PAS:
            series, ci = "mix", PAS[key]
        else:
            continue
        for i in it["items"]:
            if i[0] != "re":
                continue
            r = i[1]
            # a data bar: inside the axes, narrower than one cathode slot of the
            # widest possible grouping, and not the legend swatch (legend sits
            # inside the axes too, so require the top edge to be near the 0 line)
            if r.width > (x1 - x0) / 7.0 or r.width < 1.0:
                continue
            if x0 - 1 <= r.x0 <= x1 and y0 - 1 <= r.y0 <= y1 + 1:
                out.append((r.x0, r.y0, r.y1, series, ci))
    return out


def read_panel(page, fig, ax, ev_per_int, groups):
    gl = panel_gridlines(page, ax)
    bars = panel_bars(page, ax)
    zero = min(b[1] for b in bars)
    # every data bar hangs from the 0 eV line; anything else with a series colour
    # inside the axes is a legend swatch -> drop it
    bars = [b for b in bars if abs(b[1] - zero) < 0.15]
    gl = [g for g in gl if g >= zero - 0.05]        # drop the axes top spine
    step = (gl[-1] - gl[0]) / (len(gl) - 1)
    scale = ev_per_int / step                       # eV per point
    # bar width = smallest positive spacing between distinct bar left edges
    xs = sorted(set(round(b[0], 2) for b in bars))
    bw = min((b - a for a, b in zip(xs, xs[1:]) if b - a > 0.5), default=1.0)
    x0 = ax[0]
    pitch = (ax[2] - ax[0]) / len(groups)
    table = {g: {c: [0.0, 0.0] for c in CATHODES} for g in groups}
    for bx0, by0, by1, series, ci in bars:
        origin = bx0 - bw * ci
        gi = int((origin - x0) / pitch)
        gi = max(0, min(len(groups) - 1, gi))
        val = -(by1 - by0) * scale
        table[groups[gi]][CATHODES[ci]][0 if series == "nomix" else 1] = val
    meta = dict(fig=fig, gridlines=len(gl), step_pt=round(step, 3),
                ev_per_int=ev_per_int, zero_y=round(zero, 2), bar_w=bw,
                floor=round(-(gl[-1] - gl[0]) * scale, 3))
    return meta, table


def main():
    doc = fitz.open(PDF)
    csv_rows = [("figure", "electrolyte", "cathode", "dPhi_no_mixing_eV_per_nonLi_atom",
                 "dPhi_with_mixing_eV_per_nonLi_atom")]
    for pi, fig, ax, evi, groups in PANELS:
        meta, table = read_panel(doc[pi], fig, ax, evi, groups)
        print(f"\n### Fig {fig} (p{pi+1})  axis floor = {meta['floor']:+.2f} eV  "
              f"({meta['gridlines']} gridlines x {evi} eV)")
        print("| electrolyte | " + " | ".join(CATHODES) + " |")
        print("|" + "---|" * (len(CATHODES) + 1))
        for g in groups:
            cells = []
            for c in CATHODES:
                n, m = table[g][c]
                cells.append(f"{n:.2f}/{m:.2f}")
                csv_rows.append((fig, g, c, f"{n:.3f}", f"{m:.3f}"))
            print(f"| {g} | " + " | ".join(cells) + " |")
            # integrity check of the eq-5 inequality
            for c in CATHODES:
                n, m = table[g][c]
                if m > n + 2e-3:
                    print(f"   !! |dPhi| < |dPhi_nomix| violated at {g}|{c}: {n} {m}")
    if "--csv" in sys.argv:
        path = sys.argv[sys.argv.index("--csv") + 1]
        with open(path, "w", encoding="utf-8", newline="") as fh:
            for r in csv_rows:
                fh.write(",".join(str(v) for v in r) + "\n")
        print("\nwrote", path, len(csv_rows) - 1, "rows")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
