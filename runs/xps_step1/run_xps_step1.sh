#!/bin/bash
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
