#!/usr/bin/env python3
"""(A) Re-run network_conductivity.py on cases with raw σ_e but missing
form-array metrics (coverage_AM_mean / f_perc_x_AM).

This is the proper fix for cases shown as hollow gray squares on σ_e
per-config plots — they had Kirchhoff solver run originally but the
analysis pipeline didn't compute coverage_AM / f_perc.  Re-running the
network solver computes these metrics and updates full_metrics.json.

What this script does:
  1. Walks webapp/archive + webapp/results
  2. Finds cases that satisfy ALL of:
       - raw σ_e exists (network solver ran originally)
       - coverage_AM_mean OR f_perc_x_AM is None/missing
       - atoms.csv exists in case dir (input data available)
       - contacts.csv exists (Hertzian contacts data)
  3. For each such case, runs:
       python3 scripts/network_conductivity.py atoms.csv contacts.csv \\
              -o <case_dir>/network_output \\
              --contact-mode hertzian
  4. Then re-merges new network results into full_metrics.json
     (calls merge_network_to_metrics.py if available, else parses output)

Run on WSL:
  python3 scripts/rerun_network_for_missing.py --dry-run   # preview
  python3 scripts/rerun_network_for_missing.py --max 5     # do 5 first to test
  python3 scripts/rerun_network_for_missing.py             # do all

Expected duration: ~30s–2min per case (Kirchhoff solver on N×N system).
For 31 cases: ~15–60 min total.

After completion: re-run the form fit verification CLI command to see
if LOOCV / R² improved.
"""
from __future__ import annotations
import sys, json, argparse, subprocess, time
from pathlib import Path
import shutil

SCRIPTS_DIR = Path(__file__).parent
NETWORK_SCRIPT = SCRIPTS_DIR / 'network_conductivity.py'
MERGE_SCRIPT = SCRIPTS_DIR / 'merge_network_to_metrics.py'


def find_target_cases(roots, require_inputs=True):
    """Return list of (case_dir, case_name, missing_list)."""
    out = []
    for root in roots:
        rp = Path(root)
        if not rp.is_dir(): continue
        for mp in rp.rglob('full_metrics.json'):
            try:
                d = json.load(open(mp))
            except: continue
            # Has raw σ_e?
            sig = d.get('electronic_sigma_full_mScm') or \
                  d.get('electronic_sigma_full_mScm_stage_e')
            if not (sig and sig > 0): continue
            # Missing target metrics?
            missing = []
            if not d.get('coverage_AM_mean'): missing.append('coverage_AM_mean')
            if not d.get('f_perc_x_AM'): missing.append('f_perc_x_AM')
            if not missing: continue
            case_dir = mp.parent
            # Has input data for re-run?
            if require_inputs:
                atoms = case_dir / 'atoms.csv'
                contacts = case_dir / 'contacts.csv'
                if not (atoms.exists() and contacts.exists()): continue
            # Friendly name from meta.json
            meta = case_dir / 'meta.json'
            nm = case_dir.name
            if meta.exists():
                try:
                    mn = json.load(open(meta)).get('name', '') or ''
                    if mn: nm = mn
                except: pass
            # Skip nameless temp case_ids
            if not nm.startswith('input_'): continue
            out.append((case_dir, nm, missing))
    return out


def run_network_solver(case_dir, dry=False, verbose=False):
    """Re-run network_conductivity.py on a single case dir.
    Output: <case_dir>/network_output/network_results.json
    Returns True on success."""
    atoms = case_dir / 'atoms.csv'
    contacts = case_dir / 'contacts.csv'
    if not atoms.exists() or not contacts.exists():
        return False, "atoms.csv or contacts.csv missing"
    out_dir = case_dir / 'network_output'
    cmd = ['python3', str(NETWORK_SCRIPT), str(atoms), str(contacts),
           '-o', str(out_dir), '--contact-mode', 'hertzian']
    if dry:
        return True, f"[DRY] {' '.join(cmd)}"
    out_dir.mkdir(exist_ok=True)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            err_lines = (result.stderr or '').strip().split('\n')[-3:]
            return False, f"solver failed: {'; '.join(err_lines)}"
        if verbose and result.stdout:
            print(result.stdout[-500:])
        return True, "OK"
    except subprocess.TimeoutExpired:
        return False, "timeout (>10min)"
    except Exception as e:
        return False, f"exception: {e}"


def merge_to_metrics(case_dir, dry=False):
    """Merge network_output into full_metrics.json."""
    src = case_dir / 'network_output' / 'network_results.json'
    if not src.exists():
        # Try other possible filenames
        for alt in ('network_conductivity.json', 'results.json', 'output.json'):
            ap = case_dir / 'network_output' / alt
            if ap.exists(): src = ap; break
    if not src.exists():
        return False, "no network output file found"
    metrics = case_dir / 'full_metrics.json'
    if dry:
        return True, f"[DRY] would merge {src.name} into {metrics.name}"
    try:
        with open(metrics) as f: m = json.load(f)
        with open(src) as f: n = json.load(f)
        # Backup if not yet
        bak = case_dir / 'full_metrics.json.bak'
        if not bak.exists():
            shutil.copy(metrics, bak)
        # Merge keys (prefer existing non-null, fill nulls from network output)
        updated_keys = []
        for k, v in n.items():
            if v is None: continue
            if m.get(k) in (None, 0, 0.0, ''):
                m[k] = v
                updated_keys.append(k)
        with open(metrics, 'w') as f:
            json.dump(m, f, indent=2, ensure_ascii=False)
        return True, f"merged {len(updated_keys)} keys: {updated_keys[:5]}"
    except Exception as e:
        return False, f"merge failed: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help="Preview only, no execution")
    ap.add_argument('--max', type=int, default=None, help="Process first N cases (for testing)")
    ap.add_argument('--verbose', action='store_true', help="Print solver stdout")
    ap.add_argument('--roots', nargs='+', default=['webapp/archive', 'webapp/results'])
    ap.add_argument('--no-input-check', action='store_true',
                    help="List even cases without atoms.csv (for inspection)")
    args = ap.parse_args()

    if not NETWORK_SCRIPT.exists():
        print(f"[ERROR] network solver script not found: {NETWORK_SCRIPT}")
        return

    cases = find_target_cases(args.roots, require_inputs=not args.no_input_check)
    if args.max: cases = cases[:args.max]

    print(f"Found {len(cases)} cases to process:")
    for case_dir, nm, missing in cases:
        print(f"  {nm:35s}  missing: {','.join(missing)}")
    print()

    if args.dry_run:
        print("DRY-RUN — no execution.  Re-run without --dry-run to apply.")
        return

    print("=" * 80)
    print(f" Re-running network solver on {len(cases)} cases")
    print("=" * 80)
    succ = 0; fail = 0; t0 = time.time()
    for i, (case_dir, nm, missing) in enumerate(cases, 1):
        elapsed = time.time() - t0
        eta = (elapsed / i) * (len(cases) - i) if i > 0 else 0
        print(f"\n[{i}/{len(cases)}]  {nm}   (elapsed {elapsed:.0f}s, eta {eta:.0f}s)")
        ok, msg = run_network_solver(case_dir, verbose=args.verbose)
        print(f"  solver: {'✓' if ok else '✗'}  {msg}")
        if not ok:
            fail += 1; continue
        ok2, msg2 = merge_to_metrics(case_dir)
        print(f"  merge:  {'✓' if ok2 else '✗'}  {msg2}")
        if ok2: succ += 1
        else: fail += 1

    print()
    print("=" * 80)
    print(f" SUMMARY: {succ} succeeded, {fail} failed   (total {time.time()-t0:.0f}s)")
    print("=" * 80)
    if succ > 0:
        print(f"\nNext: re-verify σ_e LOOCV (corpus should expand)")
        print(f"  python3 -c 'see Round 4 verify command'")


if __name__ == '__main__':
    main()
