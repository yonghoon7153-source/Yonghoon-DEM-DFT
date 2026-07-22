#!/usr/bin/env python3
"""cdd_build.py — CDD 3-SCF 입력 생성 (complex/host/li), relaxed .out에서.
깨끗하게 처음부터 빌드: fragment별 nat/ntyp/nspin/starting_mag 정확, outdir 절대경로.
"""
import re, sys, os
W, out, nm, pse = sys.argv[1:5]
PSEUDO = {"C": "C.pbe-n-kjpaw_psl.1.0.0.UPF", "B": "B.pbe-n-kjpaw_psl.1.0.0.UPF",
          "N": "N.pbe-n-kjpaw_psl.1.0.0.UPF", "Li": "Li.pbe-s-kjpaw_psl.1.0.0.UPF"}
MASS = {"C": 12.011, "B": 10.811, "N": 14.007, "Li": 6.941}

t = open(f"{W}/{nm}.out", errors="ignore").read()
assert "JOB DONE" in t and "Begin final coordinates" in t, f"{nm}: relaxed .out 없음"
blk = t.split("Begin final coordinates")[-1].split("End final coordinates")[0]
at = [(l.split()[0], *[float(x) for x in l.split()[1:4]])
      for l in blk.splitlines() if re.match(r"\s*[A-Z][a-z]?\s+-?\d", l)]
cell = re.search(r"CELL_PARAMETERS angstrom\n(( *-?\d[^\n]*\n){3})",
                 open(f"{W}/{nm}.in").read()).group(1).rstrip("\n")

d = f"{out}/{nm}"; os.makedirs(d, exist_ok=True)

def build(atoms, tag):
    order = []
    for e, *_ in atoms:
        if e not in order: order.append(e)
    if "Li" in order: order = [e for e in order if e != "Li"] + ["Li"]  # Li 마지막
    has_li = "Li" in order
    spin = ""
    if has_li:
        spin = f"    nspin           = 2\n    starting_magnetization({order.index('Li')+1}) = 0.4\n"
    spec = "\n".join(f"  {e:2s} {MASS[e]:8.3f}  {PSEUDO[e]}" for e in order)
    pos = "\n".join(f"  {e:2s} {x:14.8f} {y:14.8f} {z:14.8f}" for e, x, y, z in atoms)
    inp = f"""&CONTROL
    calculation     = 'scf'
    prefix          = '{tag}'
    outdir          = '{d}/tmp_{tag}'
    pseudo_dir      = '{pse}'
    tprnfor         = .false.
    disk_io         = 'low'
/
&SYSTEM
    ibrav           = 0
    nat             = {len(atoms)}
    ntyp            = {len(order)}
    ecutwfc         = 60.0
    ecutrho         = 480.0
    occupations     = 'smearing'
    smearing        = 'mv'
    degauss         = 0.01
{spin}    vdw_corr        = 'grimme-d3'
    dftd3_version   = 4
/
&ELECTRONS
    conv_thr        = 1.0d-6
    mixing_beta     = 0.3
    electron_maxstep = 200
/
CELL_PARAMETERS angstrom
{cell}
ATOMIC_SPECIES
{spec}
ATOMIC_POSITIONS angstrom
{pos}
K_POINTS automatic
  3 3 1  0 0 0
"""
    open(f"{d}/{tag}.in", "w").write(inp)
    return len(atoms), len(order)

li = [a for a in at if a[0] == "Li"]; host = [a for a in at if a[0] != "Li"]
nc, tc = build(at, "complex"); nh, th = build(host, "host"); nl, tl = build(li, "li")
print(f"[{nm}] complex(nat {nc},ntyp {tc}) / host(nat {nh},ntyp {th}) / li(nat {nl},ntyp {tl})")
