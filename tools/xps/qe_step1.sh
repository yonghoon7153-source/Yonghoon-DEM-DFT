#!/bin/bash
# qe_step1.sh — XPS periodic core-hole, iteration 1: ground-state SCF validation
# of Li3PO4 / Li3PS4 + locate QE binaries & pslibrary P input (for the core-hole PP).
# Run as a SCRIPT (not pasted) so the '!' in grep patterns is not history-expanded.
set +H                                   # belt-and-suspenders: disable history expansion
cd /data/work/runs/xps_qe || { echo "no /data/work/runs/xps_qe dir (run the MP-fetch first)"; exit 1; }

echo "=== QE binaries ==="
PW=$(command -v pw.x 2>/dev/null || find /data/apps -name pw.x -type f 2>/dev/null | head -1)
LD1=$(command -v ld1.x 2>/dev/null || find /data/apps -name ld1.x -type f 2>/dev/null | head -1)
echo "pw.x  = ${PW:-NOTFOUND}"
echo "ld1.x = ${LD1:-NOTFOUND}"
if [ -z "$LD1" ]; then
  echo "  ld1.x not found as a binary. atomic source dir(s) for building it:"
  find /data/apps -type d -name atomic 2>/dev/null | head
fi

echo "=== write QE scf inputs (pymatgen) ==="
python3 - <<'PY'
from pymatgen.core import Structure
import math
PSE="/data/work/pseudo"
PP={"Li":("li_pbe_v1.4.uspp.F.UPF",6.94),"O":("O.pbe-n-kjpaw_psl.0.1.UPF",16.00),
    "S":("s_pbe_v1.4.uspp.F.UPF",32.06),"P":("P.pbe-n-rrkjus_psl.1.0.0.UPF",30.974)}
for fn in ["li3po4","li3ps4"]:
    st=Structure.from_file(f"{fn}_mp.cif")
    els=sorted({s.symbol for s in st.species})
    ks=[max(1,math.ceil((2*math.pi/a)/0.35)) for a in st.lattice.abc]
    L=["&control","  calculation='scf'",f"  prefix='{fn}'","  outdir='./out'",
       f"  pseudo_dir='{PSE}'","  tprnfor=.true. tstress=.true.","/","&system",
       f"  ibrav=0 nat={len(st)} ntyp={len(els)}","  ecutwfc=60 ecutrho=600","  occupations='fixed'","/",
       "&electrons","  conv_thr=1.0d-8 mixing_beta=0.3","/","CELL_PARAMETERS angstrom"]
    for v in st.lattice.matrix: L.append(f"  {v[0]:.10f} {v[1]:.10f} {v[2]:.10f}")
    L.append("ATOMIC_SPECIES")
    for e in els: L.append(f"  {e} {PP[e][1]} {PP[e][0]}")
    L.append("ATOMIC_POSITIONS angstrom")
    for s in st: L.append(f"  {s.specie.symbol} {s.coords[0]:.10f} {s.coords[1]:.10f} {s.coords[2]:.10f}")
    L+=["K_POINTS automatic",f"  {ks[0]} {ks[1]} {ks[2]} 0 0 0"]
    open(f"{fn}_scf.in","w").write("\n".join(L)+"\n")
    print(f"  {fn}: nat={len(st)} ntyp={len(els)} kpts={ks}")
PY

mkdir -p out
for fn in li3po4 li3ps4; do
  echo "=== $fn ground SCF (serial; minutes) ==="
  "$PW" -in ${fn}_scf.in > ${fn}_scf.out 2>&1
  grep '^!' ${fn}_scf.out | tail -1
  grep -i "convergence has been achieved" ${fn}_scf.out | tail -1
  grep -iE "Error|stopping|cannot|not.converg" ${fn}_scf.out | head -3
done

echo "=== pslibrary P generation input (for core-hole PP step) ==="
find /data/apps -path "*pseudo_library*" -iname "P*" 2>/dev/null | head
find /data/apps -path "*pseudo_library*" -iname "*.in" 2>/dev/null | head
echo "=== DONE ==="
