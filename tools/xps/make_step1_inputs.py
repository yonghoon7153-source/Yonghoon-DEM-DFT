#!/usr/bin/env python3
"""make_step1_inputs.py — ORCA dSCF XPS calibration, STEP 1: P 1s chemical shift
between phosphate (Li3PO4 cluster) and thiophosphate (Li3PS4 cluster).

Why P 1s (not 2p): the P 2p chemical SHIFT == P 1s shift (both track the P-site
potential), and 1s is a single non-degenerate core MO -> no spin-orbit, no
localization needed (P is the unique heaviest-but-one atom). Clean calibration.
Target: experiment P 2p thiophosphate 131.7 -> phosphate 133.3 = +1.6 eV.

Builds two neutral closed-shell clusters (PX4^3- + 3 Li+, net 0), writes the
geometry-opt ORCA inputs, and a gabia submit script that: opt -> neutral SP ->
dSCF core-hole (IonizeAlpha at the P 1s index) -> prints BE and the shift.
Run: python3 tools/xps/make_step1_inputs.py   (emits into runs/xps_step1/)
"""
import numpy as np, os

OUT = "runs/xps_step1"; os.makedirs(OUT, exist_ok=True)
# tetrahedral unit directions
D = np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]], float)
D /= np.linalg.norm(D, axis=1, keepdims=True)

def build(Xel, dPX, rLi):
    """P at origin; 4 X (Xel) tetrahedral at dPX; 3 Li+ bridging 3 X-pairs at radius rLi."""
    lines = [("P", np.zeros(3))]
    for d in D: lines.append((Xel, d * dPX))
    for a, b in [(0, 1), (2, 3), (0, 2)]:
        v = D[a] + D[b]; v /= np.linalg.norm(v)
        lines.append(("Li", v * rLi))
    return lines

SYS = {
    "li3po4": dict(geom=build("O", 1.54, 1.99), note="phosphate PO4^3- + 3Li (P-O 1.54 A)"),
    "li3ps4": dict(geom=build("S", 2.05, 2.45), note="thiophosphate PS4^3- + 3Li (P-S 2.05 A)"),
}

def xyzblock(geom):
    return "\n".join(f"{el:2s} {p[0]:12.6f} {p[1]:12.6f} {p[2]:12.6f}" for el, p in geom)

OPT_HEAD = ("! PBE0 def2-TZVP D4 RIJCOSX def2/J OPT TightSCF\n"
            "%maxcore 3000\n")
for name, s in SYS.items():
    with open(f"{OUT}/{name}_opt.inp", "w") as f:
        f.write(f"# {s['note']} — geometry opt (neutral closed shell)\n")
        f.write(OPT_HEAD)
        f.write(f"* xyz 0 1\n{xyzblock(s['geom'])}\n*\n")
    # sanity: print first-shell bond lengths
    g = s["geom"]; P = g[0][1]
    bl = [np.linalg.norm(p - P) for el, p in g[1:5]]
    print(f"{name}: P-X = {np.mean(bl):.3f} A (x4) ; {s['note']}")

# ---- gabia submit script (raw string: no python interpolation; $... and {} are literal bash/py) ----
SUB = r"""#!/bin/bash
# run_xps_step1.sh — ORCA 6.1.1 dSCF P 1s chemical shift (XPS calibration).
# phosphate (Li3PO4) vs thiophosphate (Li3PS4); target experimental P2p shift = +1.6 eV.
# full path required for ORCA MPI. Run from this dir on gabia.
ORCA=/data/apps/orca-6.1.1/orca
cd "$(dirname "$0")"

for sys in li3po4 li3ps4; do
  echo "=== $sys : geometry opt ==="
  $ORCA ${sys}_opt.inp > ${sys}_opt.out
  ( grep -q "HURRAY" ${sys}_opt.out || grep -q "OPTIMIZATION RUN DONE" ${sys}_opt.out ) \
     && echo "  opt done -> ${sys}_opt.xyz" || echo "  WARN: opt may not have converged"
done

# P 1s orbital index: Li3PO4 -> 0 (P is heaviest atom). Li3PS4 -> 4 (4 S 1s sit BELOW P 1s, S Z=16 > P Z=15).
declare -A PIDX=( [li3po4]=0 [li3ps4]=4 )

for sys in li3po4 li3ps4; do
  idx=${PIDX[$sys]}
  # neutral SP (identical settings to dSCF, minus DELTASCF) at optimized geometry -> E_N
  cat > ${sys}_neutral.inp <<EOF
! PBE0 def2-TZVP RIJCOSX def2/J TightSCF
%maxcore 3000
*xyzfile 0 1 ${sys}_opt.xyz
EOF
  $ORCA ${sys}_neutral.inp > ${sys}_neutral.out
  # dSCF P 1s core hole (ORCA auto-makes the +1/doublet core-ionized state)
  cat > ${sys}_P1s.inp <<EOF
! PBE0 def2-TZVP RIJCOSX def2/J DELTASCF NODIIS UKS TightSCF
%maxcore 3000
%scf
  IonizeAlpha $idx
end
*xyzfile 0 1 ${sys}_opt.xyz
EOF
  echo "=== $sys : dSCF P 1s core hole (IonizeAlpha $idx) ==="
  $ORCA ${sys}_P1s.inp > ${sys}_P1s.out
done

echo ""; echo "=== RESULTS ==="
python3 - <<'PY'
def E(f):
    v=None
    for l in open(f):
        if "FINAL SINGLE POINT ENERGY" in l: v=float(l.split()[-1])
    return v
Ha=27.2113845
res={}
for sys in ("li3po4","li3ps4"):
    en=E(f"{sys}_neutral.out"); ei=E(f"{sys}_P1s.out")
    if en is None or ei is None: print(f"{sys}: MISSING energy (check .out)"); continue
    be=(ei-en)*Ha; res[sys]=be
    print(f"{sys:7s}: E_N={en:.6f}  E_ion={ei:.6f}  BE(P1s)={be:.1f} eV")
if len(res)==2:
    sh=res["li3po4"]-res["li3ps4"]
    print(f"\ndSCF P1s shift (phosphate - thiophosphate) = {sh:+.2f} eV")
    print("experiment (P 2p 131.7 -> 133.3)            = +1.60 eV")
    ok = 1.2 <= sh <= 2.1
    print("=> METHOD VALIDATED" if ok else "=> off target — check P1s orbital index (BE ~2140-2160 eV expected, NOT ~2470=S1s)")
PY
"""
with open(f"{OUT}/run_xps_step1.sh", "w") as f:
    f.write(SUB)
os.chmod(f"{OUT}/run_xps_step1.sh", 0o755)
print(f"\nwrote {OUT}/  (li3po4_opt.inp, li3ps4_opt.inp, run_xps_step1.sh)")
