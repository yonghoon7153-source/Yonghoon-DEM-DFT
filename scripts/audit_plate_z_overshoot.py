#!/usr/bin/env python3
"""Quantify the mesh_info.json / plate_z overshoot across the webapp corpus.

Stage-E re-solves (run_network_full_corrections._run_solver) used to run
network_conductivity.py in a temp dir WITHOUT mesh_info.json, so the solver
fell back to plate_z = max(atom z).  When a case has a sparse top tail, that
max overshoots the true plate plane recorded in mesh_info.json — collapsing
the top electrode and corrupting the THERMAL all-contact solve (κ=0) and the
geometry-normalised σ for any re-solved channel.

This audit reports, per case, the overshoot ratio R = max(atom z) / plate_z
(mesh_info.json).  R ≈ 1 → unaffected; R ≫ 1 → its Stage-E re-solve used a
wrong plate_z and should be recomputed with the mesh_info.json fix.  Cases
with no mesh_info.json never had a 'true' plate_z to begin with (always used
the fallback) and are listed separately.

Run:  python3 scripts/audit_plate_z_overshoot.py [--results webapp/results]
                                                 [--thresh 1.15]
"""
import argparse
import csv
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def _max_z(atoms_csv):
    """Max z over all atoms — pure-csv (no pandas), streams the file."""
    with open(atoms_csv, newline='') as fh:
        rd = csv.reader(fh)
        header = next(rd, None)
        if not header:
            return None
        try:
            zi = header.index('z')
        except ValueError:
            return None
        mz = None
        for row in rd:
            if len(row) <= zi:
                continue
            try:
                z = float(row[zi])
            except ValueError:
                continue
            if mz is None or z > mz:
                mz = z
        return mz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', default=os.path.join(HERE, '..', 'webapp', 'results'))
    ap.add_argument('--thresh', type=float, default=1.15,
                    help='flag cases whose max(atom z)/plate_z exceeds this')
    a = ap.parse_args()

    rows, no_mesh = [], []
    for fm_path in sorted(glob.glob(os.path.join(a.results, '*', 'full_metrics.json'))):
        cdir = os.path.dirname(fm_path)
        cid = os.path.basename(cdir)
        atoms = os.path.join(cdir, 'atoms.csv')
        mesh = os.path.join(cdir, 'mesh_info.json')
        if not os.path.exists(atoms):
            continue
        mz = _max_z(atoms)
        if mz is None:
            continue
        try:
            fm = json.load(open(fm_path))
        except Exception:
            fm = {}
        se_k = fm.get('thermal_sigma_full_mScm_stage_e')
        if not os.path.exists(mesh):
            no_mesh.append((cid, mz, se_k))
            continue
        try:
            pz = json.load(open(mesh)).get('plate_z')
        except Exception:
            pz = None
        if not pz or pz <= 0:
            no_mesh.append((cid, mz, se_k))
            continue
        rows.append((cid, pz, mz, mz / pz, se_k))

    rows.sort(key=lambda r: r[3], reverse=True)
    flagged = [r for r in rows if r[3] > a.thresh]

    print(f"Plate-z overshoot audit  ({len(rows)} cases w/ mesh_info, "
          f"{len(no_mesh)} without)\n")
    print(f"  {'case':30s} {'plate_z':>9s} {'max_z':>9s} {'ratio':>6s} {'κ_stageE':>9s}")
    print(f"  {'-'*30} {'-'*9} {'-'*9} {'-'*6} {'-'*9}")
    for cid, pz, mz, r, sek in rows:
        mark = '  ⚠ OVERSHOOT' if r > a.thresh else ''
        sk = f'{sek:.2f}' if isinstance(sek, (int, float)) else str(sek)
        print(f"  {cid:30s} {pz:9.5f} {mz:9.5f} {r:6.2f} {sk:>9s}{mark}")
    if no_mesh:
        print(f"\n  (no mesh_info.json — always used fallback plate_z):")
        for cid, mz, sek in no_mesh:
            sk = f'{sek:.2f}' if isinstance(sek, (int, float)) else str(sek)
            print(f"    {cid:30s} max_z={mz:9.5f}  κ_stageE={sk}")

    print(f"\nSUMMARY: {len(flagged)}/{len(rows)} cases overshoot > {a.thresh}× "
          f"→ their Stage-E re-solve used a wrong plate_z and should be "
          f"recomputed with the mesh_info.json fix.")
    if flagged:
        print("Worst offenders:")
        for cid, pz, mz, r, sek in flagged[:10]:
            print(f"  {cid}  ratio={r:.2f}  (plate_z {pz:.4f} → max_z {mz:.4f})")


if __name__ == '__main__':
    main()
