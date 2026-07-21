#!/usr/bin/env python3
"""neb_build_kgy.py — CI-NEB inputs for Li hollow->hollow hops (run ON kgy).

Cases (1L models — the 2x2 matrix proved layer effects <20 meV on E_bind, and a
barrier is a site-energy DIFFERENCE on the same host so layer effects cancel
further; graphene-surface 1L is also the literature-standard model):
  Li_on_hbn       surface diffusion on the h-BN coating   (Shi 2017 ref: 0.10 eV)
  Li_on_graphene  surface diffusion on bare VGCF          (lit baseline ~0.3 eV)
  Li_in_gallery   in-gallery diffusion hBN|Li|VGCF        (THE new number)

Path = one hop between adjacent hollows (+a1 = +2.46 A, x). TS (bridge/atop —
and in the gallery, whatever the cap registry makes of it) is found by CI-NEB,
not assumed. Endpoints are pre-relaxed minima; neb.x keeps them fixed (default).

Two-pass & idempotent (runner calls it before AND after the endpoint relaxes):
  pass 1: neb/<case>_nebB.in = endpoint-B relax (Li +2.46 A, substrate dimple re-forms)
  pass 2: neb/<case>/neb.in  = CI-NEB 7 images (FIRST=<case>.out, LAST=<case>_nebB.out)
"""
import os
import re

WORK = os.environ.get("WORK", os.path.expanduser("~/work/vgcf_hbn"))
NEB = f"{WORK}/neb"
CASES = ["Li_on_hbn", "Li_on_graphene", "Li_in_gallery"]
HOP = 2.46  # A, one hollow-lattice vector (+x)


def final_coords(path):
    if not os.path.exists(path):
        return None
    t = open(path, errors="ignore").read()
    if "JOB DONE" not in t or "Begin final coordinates" not in t:
        return None
    blk = t.split("Begin final coordinates")[-1].split("End final coordinates")[0]
    at = [l.split() for l in blk.splitlines() if re.match(r"\s*[A-Z][a-z]?\s+-?\d", l)]
    return [(a[0], float(a[1]), float(a[2]), float(a[3])) for a in at]


def pos_block(at):
    return "\n".join(f"  {e:2s} {x:14.8f} {y:14.8f} {z:14.8f}" for e, x, y, z in at)


def grab(txt, pat):
    m = re.search(pat, txt)
    assert m, f"pattern miss: {pat}"
    return m.group(0)


def main():
    os.makedirs(NEB, exist_ok=True)
    for c in CASES:
        A = final_coords(f"{WORK}/{c}.out")
        if A is None:
            print(f"  {c}: 원본 relax 미완/없음 — skip")
            continue
        assert A[-1][0] == "Li", f"{c}: Li가 마지막 원자가 아님"
        tin = open(f"{WORK}/{c}.in").read()
        # ---- pass 1: endpoint-B relax (Li shifted one hollow along +x) ----
        e, x, y, z = A[-1]
        posB0 = pos_block(A[:-1] + [(e, x + HOP, y, z)])
        tB = re.sub(r"(ATOMIC_POSITIONS angstrom\n).*?(\n\nK_POINTS)",
                    lambda m: m.group(1) + posB0 + m.group(2), tin, flags=re.S)
        tB = tB.replace("prefix          = '", "prefix          = 'B", 1)
        pB = f"{NEB}/{c}_nebB.in"
        if not os.path.exists(pB):
            open(pB, "w").write(tB)
            print(f"  {c}: endpoint-B relax 입력 -> {pB}")
        # ---- pass 2: NEB input (needs relaxed endpoint-B) ----
        Bf = final_coords(f"{NEB}/{c}_nebB.out")
        if Bf is None:
            print(f"  {c}: endpoint-B 미완 — NEB 입력은 다음 패스에서")
            continue
        nml = tin.split("CELL_PARAMETERS")[0]
        nml = nml.replace("calculation     = 'relax'", "calculation     = 'scf'")
        nml = re.sub(r"&IONS.*?/\n", "", nml, flags=re.S)
        cell = grab(tin, r"CELL_PARAMETERS angstrom\n( *-?\d[^\n]*\n){3}")
        spec = grab(tin, r"ATOMIC_SPECIES\n( +[A-Za-z][^\n]*\n)+")
        kpts = grab(tin, r"K_POINTS automatic\n[^\n]*\n?")
        neb_in = f"""BEGIN
BEGIN_PATH_INPUT
&PATH
    string_method   = 'neb'
    restart_mode    = 'from_scratch'
    nstep_path      = 150
    opt_scheme      = 'broyden'
    num_of_images   = 7
    k_max           = 0.3
    k_min           = 0.2
    CI_scheme       = 'auto'
    path_thr        = 0.05
/
END_PATH_INPUT
BEGIN_ENGINE_INPUT
{nml}{cell}
{spec}
{kpts}BEGIN_POSITIONS
FIRST_IMAGE
ATOMIC_POSITIONS angstrom
{pos_block(A)}
LAST_IMAGE
ATOMIC_POSITIONS angstrom
{pos_block(Bf)}
END_POSITIONS
END_ENGINE_INPUT
END
"""
        d = f"{NEB}/{c}"
        os.makedirs(d, exist_ok=True)
        open(f"{d}/neb.in", "w").write(neb_in)
        print(f"  {c}: NEB 입력 -> {d}/neb.in (7 images, CI auto, hop {HOP} A)")


if __name__ == "__main__":
    main()
