#!/usr/bin/env python3
"""Audit every case's validation_flags self-report card and produce:

  docs/db/case_audit.csv           every case, every gate value
  docs/db/case_audit_fails.csv     only the failing cases, with the
                                    list of gates that knocked them
                                    out and human-readable case info
  docs/db/case_audit_summary.tex   LaTeX table for §5 Results:
                                    "X / Y cases trustworthy" + a
                                    fail-by-gate breakdown table

The friendly case name is the directory name (`case_dir.name`), which
for archive cases is the auto-generated `<date>_<time>_<hash>` ID.  We
also surface the canonical campaign / source-case label from
meta.json (the upload-time name, e.g. `input_8mAh_8`) when present so
the user can find the case quickly without grep-ing.

Usage:
  python3 scripts/audit_validation_flags.py            # all archives
  python3 scripts/audit_validation_flags.py --fails-only
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT    = Path(__file__).resolve().parent.parent
WEBAPP  = ROOT / 'webapp'
DOCSDB  = ROOT / 'docs' / 'db'

GATES = [
    'within_bielefeld_range',
    'fracture_distribution_realistic',
    'solver_input_intact',
    'stage_e_le_baseline_sigma_e',
]


def discover_cases() -> list[Path]:
    seen, out = set(), []
    for base in ('archive', 'results'):
        root = WEBAPP / base
        if not root.exists():
            continue
        for atoms_p in root.rglob('atoms.csv'):
            d = atoms_p.parent
            if (d / 'full_metrics.json').exists() and d not in seen:
                seen.add(d)
                out.append(d)
    return sorted(out)


def _friendly_name(case_dir: Path) -> dict:
    """Pull human-recognisable identifiers from meta.json or
    input_params.json if present. Returns dict that may include:
      case_dir, source_case, campaign, ps_ratio, ase_ratio,
      thickness_um, p_vol, s_vol, r_AM_P_um, r_AM_S_um, r_SE_um,
    falling back to None when a field is absent."""
    info = {'case_dir': case_dir.name}
    for fname in ('meta.json', 'input_params.json'):
        p = case_dir / fname
        if not p.exists():
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        for k in ('source_case', 'campaign', 'ps_ratio', 'p_vol', 's_vol',
                   'ase_ratio', 'am_wt', 'se_wt',
                   'thickness_um', 'r_AM_P_um', 'r_AM_S_um', 'r_SE_um',
                   'name', 'note'):
            if k in d and d[k] is not None and k not in info:
                info[k] = d[k]
    # Pull a couple of useful fields from full_metrics.json too
    try:
        fm = json.loads((case_dir / 'full_metrics.json').read_text())
        for k in ('thickness_um', 'porosity_pct',
                  'sigma_full_mScm', 'electronic_sigma_full_mScm',
                  'sigma_full_mScm_stage_e',
                  'electronic_sigma_full_mScm_stage_e'):
            if k in fm and fm[k] is not None and k not in info:
                info[k] = fm[k]
    except Exception:
        pass
    return info


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--fails-only', action='store_true',
                     help='Skip the full case_audit.csv, emit fails+summary only')
    args = ap.parse_args()

    cases = discover_cases()
    if not cases:
        print('No cases found.', flush=True); sys.exit(1)

    rows_all  = []
    rows_fail = []
    fail_by_gate = {g: 0 for g in GATES}
    fail_by_gate['no_flags_at_all'] = 0
    n_trust = n_total = 0

    for d in cases:
        try:
            fm = json.loads((d / 'full_metrics.json').read_text())
        except Exception:
            continue
        flags = fm.get('validation_flags') or {}
        if not flags:
            n_total += 1
            fail_by_gate['no_flags_at_all'] += 1
            info = _friendly_name(d)
            info['failed_gates'] = 'no_flags_at_all'
            rows_fail.append(info)
            rows_all.append(info)
            continue

        n_total += 1
        info = _friendly_name(d)
        for g in GATES + ['trustworthy_overall']:
            info[g] = flags.get(g)
        info['asr_ionic_Ohm_cm2']  = flags.get('asr_ionic_Ohm_cm2')
        info['fracture_severe_pct'] = flags.get('fracture_severe_pct')
        rows_all.append(info)

        if flags.get('trustworthy_overall'):
            n_trust += 1
        else:
            failed = [g for g in GATES if flags.get(g) is False]
            for g in failed:
                fail_by_gate[g] += 1
            info['failed_gates'] = ' / '.join(failed) if failed else 'unassessed'
            rows_fail.append(info)

    DOCSDB.mkdir(parents=True, exist_ok=True)

    import csv as _csv
    # Full table
    if not args.fails_only and rows_all:
        cols = sorted({k for r in rows_all for k in r.keys()})
        cols = (['case_dir'] +
                [c for c in cols if c not in ('case_dir',)])
        with (DOCSDB / 'case_audit.csv').open('w', newline='') as f:
            w = _csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows_all: w.writerow(r)
        print(f'  ✓ {DOCSDB / "case_audit.csv"}  ({len(rows_all)} rows)')

    # Fail-only table
    if rows_fail:
        cols = sorted({k for r in rows_fail for k in r.keys()})
        priority = ['case_dir', 'source_case', 'failed_gates',
                    'asr_ionic_Ohm_cm2', 'fracture_severe_pct',
                    'thickness_um', 'porosity_pct',
                    'p_vol', 's_vol', 'am_wt', 'se_wt',
                    'r_AM_P_um', 'r_AM_S_um', 'r_SE_um']
        cols = priority + [c for c in cols if c not in priority]
        with (DOCSDB / 'case_audit_fails.csv').open('w', newline='') as f:
            w = _csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows_fail: w.writerow(r)
        print(f'  ✓ {DOCSDB / "case_audit_fails.csv"}  ({len(rows_fail)} rows)')

    # LaTeX summary for §5 Results
    pct = (100.0 * n_trust / max(n_total, 1))
    tex = (
        f"% Auto-generated by scripts/audit_validation_flags.py — do not edit.\n"
        f"% {n_trust}/{n_total} cases passed every assessable trust gate.\n"
        f"\\begin{{table}}[h]\n"
        f"\\centering\n"
        f"\\caption{{Self-reported trust audit on the {n_total}-case "
        f"DEM ensemble. A case is trustworthy when every assessable "
        f"gate (ASR within Bielefeld/Lee experimental window, "
        f"fracture distribution realistic, ${{\\le}}50\\%$ Stage-E "
        f"edge-drop, and Stage-E $\\sigma \\le$ baseline) returns "
        f"True; gates whose underlying metric is missing are excluded "
        f"from the verdict.}}\n"
        f"\\label{{tab:trust-audit}}\n"
        f"\\begin{{tabular}}{{lr}}\n"
        f"\\toprule\n"
        f"Trust verdict & Cases \\\\\n"
        f"\\midrule\n"
        f"Trustworthy (all assessable gates True) & "
        f"{n_trust} / {n_total} ({pct:.1f}\\%) \\\\\n"
        f"Failed: ASR outside Bielefeld/Lee window      & "
        f"{fail_by_gate['within_bielefeld_range']} \\\\\n"
        f"Failed: fracture distribution unrealistic     & "
        f"{fail_by_gate['fracture_distribution_realistic']} \\\\\n"
        f"Failed: $>$50\\,\\% Stage-E edges dropped     & "
        f"{fail_by_gate['solver_input_intact']} \\\\\n"
        f"Failed: Stage-E $\\sigma >$ baseline (factor $>$ 1) & "
        f"{fail_by_gate['stage_e_le_baseline_sigma_e']} \\\\\n"
        f"No validation flags persisted (older Stage-E run) & "
        f"{fail_by_gate['no_flags_at_all']} \\\\\n"
        f"\\bottomrule\n"
        f"\\end{{tabular}}\n"
        f"\\end{{table}}\n"
    )
    (DOCSDB / 'case_audit_summary.tex').write_text(tex)
    print(f'  ✓ {DOCSDB / "case_audit_summary.tex"}')
    print(f'\nVerdict: {n_trust}/{n_total} trustworthy ({pct:.1f}%)')
    print('Fail breakdown:')
    for g, n in fail_by_gate.items():
        if n: print(f'  {g:38s} {n}')


if __name__ == '__main__':
    main()
