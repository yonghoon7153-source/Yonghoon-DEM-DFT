#!/usr/bin/env python3
"""Dopant SITE-PREFERENCE via antisite swap (same-composition, all-UMA).

WHY this exists
---------------
The 273-cascade enumerates a dopant at different Wyckoff sites, but it uses a
*different charge-compensation* per site (e.g. B@P uses Li-interstitial comp,
B@Li uses Cl-rich chain comp).  Those configs therefore have *different
compositions and different atom counts* (56 vs 47 atoms for B2O3) -> their raw
energies are NOT comparable, so the cascade cannot answer "which site does the
dopant prefer".

This tool answers it cleanly with a controlled, SAME-COMPOSITION pair:
  start from one relaxed champion structure (fixed atom inventory) and build
    S_P  : dopant cation M sits on a framework P site   (M <-> nearest P swapped)
    S_Li : dopant cation M sits on a Li site            (M <-> nearest Li swapped)
  Both have the IDENTICAL composition (only positions are exchanged), relax both
  with the same UMA model, and compare total energy:
    dE = E(S_P) - E(S_Li)   ;   dE<0 => M prefers the framework P site.

Interpretation / honest caveat
------------------------------
Because composition is held fixed, moving M into the framework necessarily
displaces a P to M's old (often Li-region) position -> the comparison includes
that antisite penalty.  That is the intrinsic physics of a fixed-composition
comparison and is the cleanest "same atom count" statement possible.  A
*reservoir-referenced* defect-formation-energy comparison (composition allowed
to change, chemical potentials chosen) answers a slightly different question and
depends on synthesis conditions; that is intentionally NOT done here.

Only CATION dopants (M = leading element of the compound, not a host element)
are handled.  Li-/Na-led "dopants" (Li2O, Li3N, LiCl, ...) introduce an ANION on
the chalcogen sublattice -> cation P-vs-Li swap is N/A; those are skipped with a
logged reason (extend later if needed).

UMA convention matches tools/doping/b2o3_uma_relax.py (uma-s-1p1 / omat /
FrechetCellFilter + FIRE).

Modes
-----
  --xyz CHAMP --sys NAME --out DIR      : run the swap pair, write site_pref.json
  --find_champion --sys NAME --cas CAS  : print champion xyz path (for batch)
  --summary --out OUTROOT               : aggregate all site_pref.json into a table
"""
import argparse, json, os, re, sys, datetime, warnings
from pathlib import Path
import numpy as np

# FrechetCellFilter computes a matrix logarithm of the cell deformation every
# step; scipy emits a benign "logm result may be inaccurate" RuntimeWarning
# (err ~1e-13 = machine precision).  Silence it so relax logs stay readable.
warnings.filterwarnings("ignore", message="logm result may be inaccurate")

HOST = {"Li", "P", "S", "Cl"}
ANIONS = {"O", "N", "F", "Br", "I", "Se", "Te"}


# ----------------------------------------------------------------------------
def leading_element(sys_name):
    """'B2O3_x005' -> 'B' ; 'SnO2_x010' -> 'Sn' ; 'Nd2O3_x002' -> 'Nd'."""
    formula = sys_name.split("_x")[0]
    m = re.match(r"([A-Z][a-z]?)", formula)
    return m.group(1) if m else None


def git_commit():
    try:
        import subprocess
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def provenance(model, task):
    p = {"timestamp_iso": datetime.datetime.now().astimezone().isoformat(),
         "tool": "site_preference_swap.py",
         "method": "antisite swap, same-composition, all-UMA",
         "uma_model_name": model, "uma_task_name": task,
         "git_commit": git_commit()}
    try:
        import ase
        p["ase_version"] = ase.__version__
    except Exception:
        pass
    return p


# ----------------------------------------------------------------------------
def find_champion(sys_name, cas):
    """Return the cascade-chosen winner xyz (08_elastic > 07_eos > 04_anneal)."""
    base = Path(cas) / sys_name
    for stage in ("08_elastic", "07_eos"):
        f = base / stage / "postproc_summary.json"
        if f.exists():
            try:
                d = json.load(open(f))
                recs = d.get("records") or []
                if recs and recs[0].get("xyz_input") and Path(recs[0]["xyz_input"]).exists():
                    return recs[0]["xyz_input"]
                xy = (d.get("cli_args") or {}).get("xyz") or []
                for x in xy:
                    if Path(x).exists():
                        return x
            except Exception:
                pass
    # fallback: lowest-E anneal post_relax.xyz
    f = base / "04_anneal" / "anneal_results.json"
    if f.exists():
        try:
            d = json.load(open(f))
            res = d.get("results") or []
            cand = []
            for r in res:
                nm = r.get("name")
                pr = base / "04_anneal" / nm / "post_relax.xyz"
                e = r.get("E_post_anneal_per_atom") or r.get("e_per_atom") or r.get("energy")
                if nm and pr.exists():
                    cand.append((e if e is not None else 0.0, str(pr)))
            if cand:
                cand.sort(key=lambda t: t[0])
                return cand[0][1]
        except Exception:
            pass
    return ""


# ----------------------------------------------------------------------------
def build_swap(atoms, M_idx, partner_sym):
    """Return a copy with each M atom's position exchanged with its nearest
    `partner_sym` atom (antisite swap; composition unchanged). None if too few
    partner atoms."""
    a = atoms.copy()
    syms = a.get_chemical_symbols()
    partners = [i for i, s in enumerate(syms) if s == partner_sym]
    if len(partners) < len(M_idx):
        return None
    used = set()
    for m in M_idx:
        d = a.get_distances(m, partners, mic=True)
        for k in np.argsort(d):
            p = partners[k]
            if p not in used:
                pm = a.positions[m].copy()
                a.positions[m] = a.positions[p].copy()
                a.positions[p] = pm
                used.add(p)
                break
        else:
            return None
    return a


def relax(atoms, calc, fmax, steps, logf):
    from ase.optimize import FIRE
    from ase.filters import FrechetCellFilter
    atoms.calc = calc
    flt = FrechetCellFilter(atoms)          # cell + atoms free (matches cascade)
    opt = FIRE(flt, logfile=logf)
    conv = opt.run(fmax=fmax, steps=steps)
    return atoms.get_potential_energy(), bool(conv), opt.get_number_of_steps()


def make_calc(model, task, device):
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    try:
        predictor = pretrained_mlip.get_predict_unit(model, device=device)
    except Exception as e:                       # e.g. CUDA OOM / no GPU
        if device != "cpu":
            print(f"[warn] device={device} failed ({type(e).__name__}); falling back to cpu")
            predictor = pretrained_mlip.get_predict_unit(model, device="cpu")
        else:
            raise
    return FAIRChemCalculator(predictor, task_name=task)


# ----------------------------------------------------------------------------
def run_pair(args):
    from ase.io import read, write
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    res_path = out / "site_pref.json"

    M = args.dopant or leading_element(args.sys)
    rec = {"sys": args.sys, "dopant": M, "champion_xyz": args.xyz,
           "provenance": provenance(args.model, args.task)}

    if M in HOST:
        rec.update(status="skip", reason=f"leading element {M} is a host species "
                   "(anion/Li-sublattice dopant) -> cation P-vs-Li swap N/A")
        json.dump(rec, open(res_path, "w"), indent=1)
        print(f"[{args.sys}] SKIP: {rec['reason']}")
        return 0

    atoms = read(args.xyz)
    syms = atoms.get_chemical_symbols()
    M_idx = [i for i, s in enumerate(syms) if s == M]
    nP = syms.count("P")
    nLi = syms.count("Li")
    rec.update(n_atoms=len(atoms), n_dopant=len(M_idx), n_P=nP, n_Li=nLi,
               composition={s: syms.count(s) for s in sorted(set(syms))})

    if not M_idx:
        rec.update(status="error", reason=f"dopant {M} not found in {args.xyz}")
        json.dump(rec, open(res_path, "w"), indent=1)
        print(f"[{args.sys}] ERROR: {rec['reason']}")
        return 1
    if nP < len(M_idx) or nLi < len(M_idx):
        rec.update(status="skip", reason=f"not enough P({nP}) or Li({nLi}) to swap "
                   f"{len(M_idx)} {M}")
        json.dump(rec, open(res_path, "w"), indent=1)
        print(f"[{args.sys}] SKIP: {rec['reason']}")
        return 0

    S_P = build_swap(atoms, M_idx, "P")
    S_Li = build_swap(atoms, M_idx, "Li")
    if S_P is None or S_Li is None:
        rec.update(status="skip", reason="swap construction failed (partner shortage)")
        json.dump(rec, open(res_path, "w"), indent=1)
        print(f"[{args.sys}] SKIP: {rec['reason']}")
        return 0

    calc = make_calc(args.model, args.task, args.device)
    E_P, cP, sP = relax(S_P, calc, args.fmax, args.steps, str(out / "relax_P.log"))
    E_Li, cLi, sLi = relax(S_Li, calc, args.fmax, args.steps, str(out / "relax_Li.log"))
    write(str(out / "M_at_P.xyz"), S_P)
    write(str(out / "M_at_Li.xyz"), S_Li)

    dE = E_P - E_Li
    pref = "P_framework" if dE < 0 else "Li_site"
    rec.update(status="ok",
               E_M_at_P_eV=E_P, E_M_at_Li_eV=E_Li,
               converged_P=cP, converged_Li=cLi, steps_P=sP, steps_Li=sLi,
               dE_total_eV=dE, dE_per_dopant_eV=dE / len(M_idx),
               preferred_site=pref, fmax=args.fmax)
    json.dump(rec, open(res_path, "w"), indent=1)
    print(f"[{args.sys}] {M}: E(P)={E_P:.3f} E(Li)={E_Li:.3f}  "
          f"dE={dE:+.3f} eV ({dE/len(M_idx):+.3f}/dopant)  -> prefers {pref}"
          f"{'' if (cP and cLi) else '  [NOT fully converged]'}")
    return 0


def summary(args):
    root = Path(args.out)
    rows = []
    for f in sorted(root.glob("*/site_pref.json")):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        rows.append(d)
    ok = [r for r in rows if r.get("status") == "ok"]
    ok.sort(key=lambda r: r.get("dE_per_dopant_eV", 0.0))
    print(f"\n### site-preference summary: {len(ok)} ok / {len(rows)} total ###")
    print(f"{'system':<14}{'M':>4}{'dE/dop(eV)':>11}{'pref':>13}{'conv':>6}")
    print("=" * 50)
    for r in ok:
        conv = "y" if (r.get("converged_P") and r.get("converged_Li")) else "n"
        print(f"{r['sys']:<14}{r.get('dopant',''):>4}"
              f"{r.get('dE_per_dopant_eV',0):>11.3f}{r.get('preferred_site',''):>13}{conv:>6}")
    sk = [r for r in rows if r.get("status") != "ok"]
    if sk:
        print(f"\n(skipped/err {len(sk)}: " +
              ", ".join(f"{r['sys']}[{r.get('status')}]" for r in sk[:30]) +
              (" ..." if len(sk) > 30 else "") + ")")


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sys")
    ap.add_argument("--xyz")
    ap.add_argument("--out")
    ap.add_argument("--cas")
    ap.add_argument("--dopant", help="override dopant element (default = leading element of --sys)")
    ap.add_argument("--model", default="uma-s-1p1")
    ap.add_argument("--task", default="omat")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--find_champion", action="store_true")
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args()

    if args.find_champion:
        print(find_champion(args.sys, args.cas))
        return
    if args.summary:
        summary(args)
        return
    if not (args.sys and args.xyz and args.out):
        ap.error("run mode needs --sys --xyz --out")
    sys.exit(run_pair(args))


if __name__ == "__main__":
    main()
