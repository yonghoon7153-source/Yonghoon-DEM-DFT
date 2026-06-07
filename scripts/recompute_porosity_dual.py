#!/usr/bin/env python3
"""Walk all cases, compute dual porosity (sphere-sum + union + overlap%),
update full_metrics.json, and dump CSV for cross-case comparison.

Adds these fields per case (preserves existing 'porosity' field):
  porosity_spheresum    : same as 'porosity' (sphere-sum, current production)
  porosity_union        : 1 - V_union/V_box  (overlap-corrected, literature-comparable)
  overlap_fraction_pct  : V_lens/V_sphere_sum × 100  (plastic deformation indicator)

Why:
  - Legacy 'porosity' (sphere-sum) is current calibration target.  Keep unchanged.
  - 'porosity_union' added for clean literature comparison + critic defense.
  - 'overlap_fraction_pct' quantifies plastic deformation (DEM intent).
  - Stage 22 σ_e form remains using existing 'phi_am' (sphere-sum derived).
    No fit refit needed.  This is REPORTING augmentation only.

Run on WSL:
    python3 scripts/recompute_porosity_dual.py --dry-run    # preview
    python3 scripts/recompute_porosity_dual.py              # apply + write CSV

Output:
    /tmp/porosity_dual_comparison.csv   — all cases, all metrics
    For each case: full_metrics.json gets 3 new fields (porosity_union,
    porosity_spheresum, overlap_fraction_pct).  Original 'porosity' kept.
"""
from __future__ import annotations
import sys, json, csv, argparse, shutil
from pathlib import Path
import numpy as np


def read_atoms(atoms_path):
    """Parse LIGGGHTS atom dump or atoms.csv.  Returns dict {id: {x,y,z,radius,type}}.
    Also extracts box bounds from header (LIGGGHTS dump) → returns tuple (atoms, box_xy)."""
    atoms = {}
    box_xy = None
    suffix = atoms_path.suffix
    with open(atoms_path) as f:
        if suffix == '.csv':
            import csv as _csv
            r = _csv.DictReader(f)
            for row in r:
                aid = int(row.get('id', row.get('ID', 0)))
                atoms[aid] = {
                    'x': float(row.get('x', 0)),
                    'y': float(row.get('y', 0)),
                    'z': float(row.get('z', 0)),
                    'radius': float(row.get('radius', row.get('r', 0))),
                    'type': int(row.get('type', 0)),
                }
        else:
            # LIGGGHTS dump format
            lines = f.readlines()
            data_start = None
            # Parse box bounds — usually lines after "ITEM: BOX BOUNDS"
            for i, line in enumerate(lines):
                if line.startswith('ITEM: BOX BOUNDS'):
                    # next 3 lines are x_lo x_hi, y_lo y_hi, z_lo z_hi
                    try:
                        xbounds = lines[i+1].split()
                        ybounds = lines[i+2].split()
                        x_lo, x_hi = float(xbounds[0]), float(xbounds[1])
                        y_lo, y_hi = float(ybounds[0]), float(ybounds[1])
                        # Use mean of x/y range for box_xy (square box assumed)
                        box_xy_x = x_hi - x_lo
                        box_xy_y = y_hi - y_lo
                        box_xy = (box_xy_x + box_xy_y) / 2.0  # average
                    except (ValueError, IndexError):
                        pass
                if line.startswith('ITEM: ATOMS'):
                    data_start = i + 1; break
            if data_start is None:
                return None, box_xy
            for line in lines[data_start:]:
                parts = line.split()
                if len(parts) < 6: continue
                try:
                    aid = int(parts[0])
                    atoms[aid] = {
                        'type': int(parts[1]),
                        'x': float(parts[2]), 'y': float(parts[3]), 'z': float(parts[4]),
                        'radius': float(parts[5]),
                    }
                except (ValueError, IndexError):
                    continue
    return atoms, box_xy


def read_contacts(contacts_path):
    """Parse LIGGGHTS contact dump or contacts.csv.  Returns list of dicts with delta + ids."""
    contacts = []
    suffix = contacts_path.suffix
    with open(contacts_path) as f:
        if suffix == '.csv':
            import csv as _csv
            r = _csv.DictReader(f)
            for row in r:
                try:
                    contacts.append({
                        'id1': int(row.get('id1', 0)),
                        'id2': int(row.get('id2', 0)),
                        'delta': float(row.get('delta', 0)),
                    })
                except (ValueError, IndexError):
                    continue
        else:
            # LIGGGHTS dump: columns c_cpl[1..26]
            # delta is c_cpl[23] = index 22 (0-indexed)
            # id1 c_cpl[7] = index 6, id2 c_cpl[8] = index 7
            lines = f.readlines()
            data_start = None
            for i, line in enumerate(lines):
                if line.startswith('ITEM: ENTRIES'):
                    data_start = i + 1; break
            if data_start is None:
                return None
            for line in lines[data_start:]:
                parts = line.split()
                if len(parts) < 26: continue
                try:
                    contacts.append({
                        'id1': int(parts[6]),
                        'id2': int(parts[7]),
                        'delta': float(parts[22]),
                    })
                except (ValueError, IndexError):
                    continue
    return contacts


def compute_dual(atoms, contacts, plate_z, box_xy=0.05):
    """Return (porosity_spheresum, porosity_union, overlap_pct) all in %."""
    if not atoms:
        return None, None, None
    V_sphere_sum = sum(4/3 * np.pi * a['radius']**3 for a in atoms.values())
    V_box = box_xy * box_xy * plate_z
    eps_sphere = (1 - V_sphere_sum / V_box) * 100 if V_box > 0 else None

    V_lens_total = 0.0
    for c in contacts or []:
        delta = c.get('delta', 0)
        if delta <= 0: continue
        id1, id2 = c.get('id1'), c.get('id2')
        if id1 in atoms and id2 in atoms:
            r1, r2 = atoms[id1]['radius'], atoms[id2]['radius']
        else:
            # Fallback: assume monodisperse with mean radius
            r1 = r2 = next(iter(atoms.values()))['radius']
        d = r1 + r2 - delta
        if d <= 0: continue
        V_lens = (np.pi * delta**2 / (12 * d)) * (
            d**2 + 2*d*(r1 + r2) - 3*(r1 - r2)**2
        )
        if V_lens > 0:
            V_lens_total += V_lens
    V_union = V_sphere_sum - V_lens_total
    eps_union = (1 - V_union / V_box) * 100 if V_box > 0 else None
    overlap_pct = (V_lens_total / V_sphere_sum * 100) if V_sphere_sum > 0 else None
    return eps_sphere, eps_union, overlap_pct


def find_input_files(case_dir):
    """Locate atoms + contacts file in case dir.  Returns (atoms_path, contacts_path) or None."""
    case = Path(case_dir)
    # Standard names
    for atname in ('atoms.csv', 'atom.csv', 'atoms_final.csv'):
        ap = case / atname
        if ap.exists():
            for ctname in ('contacts.csv', 'contact.csv', 'contacts_final.csv'):
                cp = case / ctname
                if cp.exists():
                    return ap, cp
    # LIGGGHTS dumps in post_* dirs
    post_dirs = list(case.glob('post_*'))
    for pd in post_dirs:
        atoms_files = sorted(pd.glob('atom_*.liggghts'),
                             key=lambda p: int(p.stem.split('_')[-1]))
        contact_files = sorted(pd.glob('contact_*.liggghts'),
                               key=lambda p: int(p.stem.split('_')[-1]))
        if atoms_files and contact_files:
            return atoms_files[-1], contact_files[-1]
    return None


def get_plate_z(case_dir, atoms=None):
    """Read plate_z from mesh_info.json or most recent mesh STL.
    If atoms provided, validates against particle distribution and uses
    max(particle z + radius) when STL value is implausibly small.

    Some old sims have mesh_info.json with INITIAL plate position (before
    compaction) which gives ridiculous porosity.  We sanity-check by comparing
    against the actual particle bed extent."""
    stl_plate_z = None
    info_plate_z = None

    mesh_info = Path(case_dir) / 'mesh_info.json'
    if mesh_info.exists():
        try:
            info_plate_z = float(json.load(open(mesh_info)).get('plate_z', 0))
        except: pass

    # Try STL files (latest timestep)
    case = Path(case_dir)
    post_dirs = list(case.glob('post_*'))
    for pd in post_dirs:
        stls = sorted(pd.glob('mesh_*.stl'),
                      key=lambda p: int(p.stem.split('_')[-1]))
        if stls:
            with open(stls[-1]) as f:
                txt = f.read()
            zs = [float(line.split()[3]) for line in txt.split('\n')
                  if 'vertex' in line]
            if zs:
                stl_plate_z = max(zs)
                break

    # Best candidate from files
    file_plate_z = stl_plate_z if stl_plate_z and stl_plate_z > 0 else info_plate_z

    # Sanity check against particles (if provided)
    if atoms:
        particle_top = max(a['z'] + a['radius'] for a in atoms.values())
        # Add tiny margin (r/10 typical) to account for plate sitting on top
        particle_bed_z = particle_top * 1.005  # 0.5% margin
        # If STL plate_z is way smaller than particle bed → STL wrong, use particle bed
        if file_plate_z is None or file_plate_z < particle_top * 0.95:
            return particle_bed_z
        # If STL plate_z reasonable, use it
        return file_plate_z

    return file_plate_z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='Preview without writing')
    ap.add_argument('--roots', nargs='+',
                    default=['webapp/archive', 'webapp/results', 'webapp/uploads'])
    ap.add_argument('--dir', default=None,
                    help='Process ONLY this one case dir (bypasses the input_ name '
                         'filter; used by the upload pipeline for auto-compute)')
    ap.add_argument('--csv-out', default='/tmp/porosity_dual_comparison.csv')
    args = ap.parse_args()
    if args.dir:
        args.roots = [args.dir]

    cases_data = []
    for root in args.roots:
        rp = Path(root)
        if not rp.is_dir(): continue
        for metrics_path in rp.rglob('full_metrics.json'):
            case_dir = metrics_path.parent
            meta = case_dir / 'meta.json'
            nm = case_dir.name
            if meta.exists():
                try:
                    mn = json.load(open(meta)).get('name', '') or ''
                    if mn: nm = mn
                except: pass
            # uploads/<timestamp>/ dirs aren't input_-prefixed (the real name
            # lives in meta.json); the webapp SERVES from there, so process them
            # regardless of dir name.  archive/results stay input_-filtered.
            if (not args.dir
                    and 'uploads' not in str(metrics_path)
                    and not nm.startswith('input_')):
                continue

            try:
                d = json.load(open(metrics_path))
            except: continue
            old_poro = d.get('porosity')

            # Find atoms + contacts
            files = find_input_files(case_dir)
            if not files:
                cases_data.append({
                    'name': nm, 'status': 'no_input_files',
                    'porosity_old': old_poro,
                    'porosity_spheresum': None,
                    'porosity_union': None,
                    'overlap_pct': None,
                })
                continue
            atoms_path, contacts_path = files

            # Read atoms FIRST (needed for plate_z sanity check)
            try:
                atoms_result = read_atoms(atoms_path)
                if isinstance(atoms_result, tuple):
                    atoms, box_xy_from_dump = atoms_result
                else:
                    atoms = atoms_result
                    box_xy_from_dump = None
                contacts = read_contacts(contacts_path)
            except Exception as e:
                cases_data.append({
                    'name': nm, 'status': f'parse_err: {e}',
                    'porosity_old': old_poro,
                    'porosity_spheresum': None,
                    'porosity_union': None,
                    'overlap_pct': None,
                })
                continue

            if not atoms:
                cases_data.append({
                    'name': nm, 'status': 'empty_atoms',
                    'porosity_old': old_poro,
                    'porosity_spheresum': None,
                    'porosity_union': None,
                    'overlap_pct': None,
                })
                continue

            # plate_z with atoms-based sanity check (fixes 1mAh_100_X anomaly)
            plate_z = get_plate_z(case_dir, atoms=atoms)
            if plate_z is None or plate_z <= 0:
                cases_data.append({
                    'name': nm, 'status': 'no_plate_z',
                    'porosity_old': old_poro,
                    'porosity_spheresum': None,
                    'porosity_union': None,
                    'overlap_pct': None,
                })
                continue

            # Use box_xy from atoms dump (more accurate per-case), fallback to 0.05
            box_xy_use = box_xy_from_dump if box_xy_from_dump and box_xy_from_dump > 0 else 0.05
            eps_s, eps_u, ov_pct = compute_dual(atoms, contacts, plate_z, box_xy=box_xy_use)

            # Sanity check — physically plausible porosity range
            # Sphere-sum: -50% (severe plastic compaction) to +85% (loose packing)
            # Outside this range usually means plate_z or box_xy is mis-read
            status = 'OK'
            if eps_s is None or not (-50.0 < eps_s < 85.0):
                status = f'implausible (ε_sphere={eps_s:.1f}%)'
            row = {
                'name': nm,
                'status': status,
                'plate_z_um': plate_z * 1000,
                'box_xy_mm': box_xy_use * 1000,
                'N_atoms': len(atoms),
                'N_contacts': len(contacts) if contacts else 0,
                'porosity_old': old_poro,
                'porosity_spheresum': eps_s,
                'porosity_union': eps_u,
                'overlap_pct': ov_pct,
                'delta_old_vs_new': (eps_s - old_poro) if (eps_s is not None and old_poro is not None) else None,
                'delta_union_vs_sphere': (eps_u - eps_s) if (eps_u is not None and eps_s is not None) else None,
            }
            cases_data.append(row)

            if not args.dry_run:
                # Only update DB if porosity is plausible (avoid corrupting)
                if status == 'OK':
                    # Backup once
                    bak = metrics_path.with_suffix('.json.poro_bak')
                    if not bak.exists():
                        shutil.copy(metrics_path, bak)
                    d['porosity_spheresum'] = eps_s
                    d['porosity_union'] = eps_u
                    d['overlap_fraction_pct'] = ov_pct
                    # Keep legacy 'porosity' UNCHANGED
                    with open(metrics_path, 'w') as f:
                        json.dump(d, f, indent=2, ensure_ascii=False)

    # Write CSV summary
    if cases_data:
        keys = ['name', 'status', 'plate_z_um', 'box_xy_mm', 'N_atoms', 'N_contacts',
                'porosity_old', 'porosity_spheresum', 'porosity_union',
                'overlap_pct', 'delta_old_vs_new', 'delta_union_vs_sphere']
        with open(args.csv_out, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            for r in cases_data:
                w.writerow({k: r.get(k, '') for k in keys})
        print(f"CSV written: {args.csv_out}")

    # Summary
    print()
    print("=" * 80)
    n_total = len(cases_data)
    n_ok = sum(1 for r in cases_data if r['status'] == 'OK')
    print(f" Cases processed: {n_total}  (OK: {n_ok})")
    print("=" * 80)

    ok_cases = [r for r in cases_data if r['status'] == 'OK']
    if ok_cases:
        eps_s = [r['porosity_spheresum'] for r in ok_cases]
        eps_u = [r['porosity_union'] for r in ok_cases]
        ov = [r['overlap_pct'] for r in ok_cases]
        print(f"\n  porosity_spheresum   range:  {min(eps_s):+6.1f}% ~ {max(eps_s):+6.1f}%  mean {np.mean(eps_s):+5.1f}%")
        print(f"  porosity_union       range:  {min(eps_u):+6.1f}% ~ {max(eps_u):+6.1f}%  mean {np.mean(eps_u):+5.1f}%")
        print(f"  overlap_fraction_pct range:  {min(ov):5.1f}% ~ {max(ov):5.1f}%  mean {np.mean(ov):5.1f}%")
        print()
        # Show worst sphere-sum vs union divergence
        ok_cases.sort(key=lambda r: -abs((r['porosity_union'] or 0) - (r['porosity_spheresum'] or 0)))
        print(f"  Top 10 cases by |union - sphere-sum| divergence:")
        print(f"    {'name':40s}  sphere   union   overlap%")
        for r in ok_cases[:10]:
            print(f"    {r['name'][:40]:40s}  {r['porosity_spheresum']:+6.2f}%  {r['porosity_union']:+6.2f}%  {r['overlap_pct']:5.2f}%")

    if args.dry_run:
        print(f"\n  DRY-RUN — no full_metrics.json modified.  CSV still written to {args.csv_out}")


if __name__ == '__main__':
    main()
