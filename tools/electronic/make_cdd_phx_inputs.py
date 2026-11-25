#!/usr/bin/env python3
"""Generate ready-to-run QE inputs for CDD (deformation density) + ph.x (eps_inf/Z*)
from a P1 .cif (cell + fractional coords).

Writes into <outdir>/:
  scf.in           full SCF (insulator, occupations=fixed)
  scf_atomic.in    atomic-superposition density (mixing_beta=0 -> no SCF update)
  pp_rho.in        pp.x plot_num=0 -> <prefix>_rho_scf.cube
  pp_atomic.in     pp.x plot_num=0 -> <prefix>_rho_atomic.cube
  ph.in            ph.x epsil=.true. trans=.false.  (eps_inf + Born Z*)
  run_all.sh       runs everything in order

Usage:
  python3 make_cdd_phx_inputs.py --cif db/structures/comp1_V0_k444.cif \
      --prefix comp1 --outdir runs/comp1_cdd_phx \
      --pseudo_dir /data/work/pseudo --ecutwfc 60 --ecutrho 480

EDIT the pseudo filenames in PSEUDO below to match your gabia pseudo_dir
(defaults = the USPP set referenced in this repo; USPP works for ph.x epsil.
If you used ONCV-NC for ELF, swap names + use --ecutwfc 80 --ecutrho 320).
"""
import argparse, math, os
from pathlib import Path

# EDIT to match your gabia pseudo_dir -------------------------------------
PSEUDO = {
    "Li": ("6.941",  "li_pbe_v1.4.uspp.F.UPF"),
    "P":  ("30.974", "P.pbe-n-rrkjus_psl.1.0.0.UPF"),
    "S":  ("32.06",  "s_pbe_v1.4.uspp.F.UPF"),
    "Cl": ("35.45",  "cl_pbe_v1.4.uspp.F.UPF"),
}
# ------------------------------------------------------------------------


def read_cif(path):
    """Robust to column order: uses the _atom_site_ header positions."""
    a=b=c=al=be=ga=None; atoms=[]
    lines=open(path).read().splitlines(); i=0
    while i<len(lines):
        ln=lines[i]; s=ln.split()
        if ln.startswith("_cell_length_a"): a=float(s[1])
        elif ln.startswith("_cell_length_b"): b=float(s[1])
        elif ln.startswith("_cell_length_c"): c=float(s[1])
        elif ln.startswith("_cell_angle_alpha"): al=float(s[1])
        elif ln.startswith("_cell_angle_beta"): be=float(s[1])
        elif ln.startswith("_cell_angle_gamma"): ga=float(s[1])
        elif ln.strip()=="loop_":
            j=i+1; cols=[]
            while j<len(lines) and lines[j].strip().startswith("_"):
                cols.append(lines[j].strip()); j+=1
            if any("_atom_site_fract_x" in cc for cc in cols):
                isym=next((k for k,cc in enumerate(cols) if cc=="_atom_site_type_symbol"),None)
                ilab=next((k for k,cc in enumerate(cols) if cc=="_atom_site_label"),None)
                ix=cols.index("_atom_site_fract_x"); iy=cols.index("_atom_site_fract_y"); iz=cols.index("_atom_site_fract_z")
                while j<len(lines):
                    t=lines[j].split()
                    if not t or lines[j].startswith("_") or lines[j].strip()=="loop_": break
                    if len(t)>max(ix,iy,iz):
                        sym=t[isym] if isym is not None else ''.join(ch for ch in t[ilab] if ch.isalpha())
                        atoms.append((sym,float(t[ix]),float(t[iy]),float(t[iz])))
                    j+=1
                i=j; continue
        i+=1
    return (a,b,c,al,be,ga), atoms


def cell_matrix(a,b,c,al,be,ga):
    al,be,ga=[math.radians(x) for x in (al,be,ga)]
    ax=a; ay=0.0; az=0.0
    bx=b*math.cos(ga); by=b*math.sin(ga); bz=0.0
    cx=c*math.cos(be)
    cy=c*(math.cos(al)-math.cos(be)*math.cos(ga))/math.sin(ga)
    cz=c*math.sqrt(max(0.0,1-math.cos(al)**2-math.cos(be)**2-math.cos(ga)**2
                       +2*math.cos(al)*math.cos(be)*math.cos(ga)))/math.sin(ga)
    return [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]


def species_block(syms):
    out=["ATOMIC_SPECIES"]
    for e in syms:
        m,p=PSEUDO[e]; out.append(f"  {e:<3} {m:>8}  {p}")
    return "\n".join(out)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cif", required=True)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--ecutwfc", type=float, default=60.0)
    ap.add_argument("--ecutrho", type=float, default=480.0)
    ap.add_argument("--kgrid", type=int, nargs=3, default=[4,4,4])
    a=ap.parse_args()

    (la,lb,lc,al,be,ga),atoms=read_cif(a.cif)
    cell=cell_matrix(la,lb,lc,al,be,ga)
    syms=sorted({e for e,*_ in atoms}, key="Li P S Cl".split().index)
    nat=len(atoms); ntyp=len(syms)
    out=Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

    cellblk="CELL_PARAMETERS angstrom\n"+"\n".join(
        f"  {r[0]:18.12f} {r[1]:18.12f} {r[2]:18.12f}" for r in cell)
    posblk="ATOMIC_POSITIONS crystal\n"+"\n".join(
        f"  {e:<3} {x:18.12f} {y:18.12f} {z:18.12f}" for e,x,y,z in atoms)
    spec=species_block(syms)
    kblk=f"K_POINTS automatic\n  {a.kgrid[0]} {a.kgrid[1]} {a.kgrid[2]} 0 0 0"

    def sysblk(extra=""):
        return (f"  ibrav=0, nat={nat}, ntyp={ntyp}, ecutwfc={a.ecutwfc}, "
                f"ecutrho={a.ecutrho}, occupations='fixed'{extra}")

    scf=f"""&control
  calculation='scf', prefix='{a.prefix}', outdir='./out',
  pseudo_dir='{a.pseudo_dir}', tprnfor=.true., tstress=.false., verbosity='high'
/
&system
{sysblk()}
/
&electrons
  conv_thr=1d-10, mixing_beta=0.3, electron_maxstep=200
/
{spec}
{cellblk}
{posblk}
{kblk}
"""
    scf_at=f"""&control
  calculation='scf', prefix='{a.prefix}_at', outdir='./out_at',
  pseudo_dir='{a.pseudo_dir}'
/
&system
{sysblk()}
/
&electrons
  electron_maxstep=1, conv_thr=1d20, startingpot='atomic', mixing_beta=0.0
/
{spec}
{cellblk}
{posblk}
{kblk}
"""
    pp_rho=f"""&inputpp  prefix='{a.prefix}', outdir='./out', plot_num=0 /
&plot iflag=3, output_format=6, fileout='{a.prefix}_rho_scf.cube' /
"""
    pp_at=f"""&inputpp  prefix='{a.prefix}_at', outdir='./out_at', plot_num=0 /
&plot iflag=3, output_format=6, fileout='{a.prefix}_rho_atomic.cube' /
"""
    ph=f"""&inputph
  prefix='{a.prefix}', outdir='./out',
  epsil=.true., trans=.false., tr2_ph=1d-14, fildyn='{a.prefix}.dyn'
/
0.0 0.0 0.0
"""
    run=f"""#!/bin/bash
set -e
# ph.x exists in the CPU build; the GPU build (qe-7.4.1-gpu) crashes 'libgomp: TODO'.
# Use the CPU build. Override QE_BIN / NP / RUN as needed.
QE_BIN="${{QE_BIN:-/data/apps/qe-7.4.1-cpu/bin}}"
NP="${{NP:-8}}"
RUN="${{RUN:-mpirun -np $NP}}"        # if mpirun PMIx-segfaults, run: RUN='' NP=1 OMP_NUM_THREADS=8 bash run_all.sh
export OMP_NUM_THREADS="${{OMP_NUM_THREADS:-1}}"
PW="$RUN $QE_BIN/pw.x"; PP="$RUN $QE_BIN/pp.x"; PH="$RUN $QE_BIN/ph.x"
echo "QE_BIN=$QE_BIN  RUN='$RUN'  OMP=$OMP_NUM_THREADS"
echo '== SCF =='        ; $PW -in scf.in        > scf.out
grep -q 'convergence has been achieved' scf.out || {{ echo 'SCF FAILED — see scf.out'; tail -20 scf.out; exit 1; }}
echo '== ph.x eps =='   ; $PH -in ph.in         > ph.out
echo '== rho_scf =='    ; $PP -in pp_rho.in     > pp_rho.out
echo '== atomic SCF ==' ; $PW -in scf_atomic.in > scf_atomic.out
echo '== rho_atomic ==' ; $PP -in pp_atomic.in  > pp_atomic.out
echo 'DONE -> ph.out , {a.prefix}_rho_scf.cube , {a.prefix}_rho_atomic.cube'
"""
    for fn,txt in [("scf.in",scf),("scf_atomic.in",scf_at),("pp_rho.in",pp_rho),
                   ("pp_atomic.in",pp_at),("ph.in",ph),("run_all.sh",run)]:
        (out/fn).write_text(txt)
    os.chmod(out/"run_all.sh",0o755)
    print(f"wrote {out}/ : nat={nat} ntyp={ntyp} ({'/'.join(syms)})  cell {la:.3f}x{lb:.3f}x{lc:.3f}")
    print("EDIT pseudo names (PSEUDO dict) + --pseudo_dir for your gabia, then:  NP=8 bash run_all.sh")


if __name__=="__main__":
    main()
