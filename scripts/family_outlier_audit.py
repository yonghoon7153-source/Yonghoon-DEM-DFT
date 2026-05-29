#!/usr/bin/env python3
"""Family-level sibling-tail outlier audit for σ_ionic and σ_e.

Scans the corpus for any case whose name matches a base+suffix pattern
(e.g. input_1mAh_8_AMS_S1..S5, input_1mAh_6_S1..S5, input_72_seed1..5),
groups them by base family, and flags members that deviate from the
family median by more than a threshold.

These are the σ_ionic / σ_electronic equivalent of the original
"sibling-tail" exclusions made in 2026-05-28 (input_1mAh_9_S5,
input_particulate_12_S2/S3 — deleted from disk for σ_ionic).

For each family-deviant case, the user can choose:
  - Add to _EXCLUDED_NAMES_EL (or σ_ionic's _EXCLUDED_NAMES) if it's a
    one-off per-seed sim anomaly (no upstream physics-side fix needed)
  - Investigate upstream if the deviation suggests a systematic issue

Run on WSL:
    python3 scripts/family_outlier_audit.py
"""
from __future__ import annotations
import re
import json
from pathlib import Path
from collections import defaultdict
import numpy as np


# Sibling-suffix patterns to strip when grouping
# (matches: _S1..S99, _seed1..seed99, _v1..v99)
_SUFFIX_RE = re.compile(r'_(S|seed|v)\d+$', re.IGNORECASE)


def _family_base(nm: str) -> str:
    """Return the base family name with sibling suffix stripped.
    'input_1mAh_8_AMS_S3' -> 'input_1mAh_8_AMS'
    'input_72_seed1'      -> 'input_72'
    'input_1mAh_6_S5'     -> 'input_1mAh_6'
    Non-sibling cases return as-is."""
    return _SUFFIX_RE.sub('', nm)


def _is_sibling(nm: str) -> bool:
    return bool(_SUFFIX_RE.search(nm))


def _stage_e_electronic_target(d):
    """Match generate_comparison_plots._stage_e_electronic_target."""
    raw = d.get('electronic_sigma_full_mScm')
    if not (isinstance(raw, (int, float)) and not isinstance(raw, bool) and raw > 0):
        return None
    src = d.get('stage_e_source') or {}
    if (src.get('sigma_e') == 'fallback_weighted_factor'
            and src.get('sigma_e_physics') == 'fallback_weighted_factor'):
        return None
    for k in ('electronic_sigma_full_mScm_stage_e',
              'electronic_sigma_full_mScm',
              'electronic_sigma_full_mScm_stage_e_physics',
              'electronic_sigma_full_mScm_physics'):
        v = d.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool) and 0 < v <= 100:
            return float(v)
    return None


def _sigma_ionic_target(d):
    """Best available σ_ionic — Stage E preferred."""
    for k in ('sigma_ionic_full_mScm_stage_e',
              'sigma_ionic_full_mScm',
              'sigma_ionic_full_mScm_physics'):
        v = d.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0:
            return float(v)
    return None


def main():
    # ───── Walk corpus ─────
    records = {}   # name → dict
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            meta_p = mp.parent / 'meta.json'
            if not meta_p.exists():
                continue
            try:
                nm = json.load(open(meta_p)).get('name', '') or ''
            except Exception:
                continue
            if not nm or nm in records:
                continue
            try:
                d = json.load(open(mp))
            except Exception:
                continue
            si = _sigma_ionic_target(d)
            se = _stage_e_electronic_target(d)
            records[nm] = {
                'name': nm,
                'sigma_ionic': si,
                'sigma_e': se,
                'phi_am': d.get('phi_am'),
                'p_amp': d.get('AM_P_n_particles', 0) / max(
                    (d.get('AM_P_n_particles', 0) or 0) + (d.get('AM_S_n_particles', 0) or 0),
                    1),
            }

    # ───── Group by family ─────
    families = defaultdict(list)
    for nm, rec in records.items():
        if _is_sibling(nm):
            base = _family_base(nm)
            families[base].append(rec)
    # ALSO include the base itself if it exists (input_1mAh_6 + input_1mAh_6_S1..S5)
    for base in list(families.keys()):
        if base in records:
            families[base].append(records[base])
    # Dedup (base might be added twice)
    for base in families:
        seen = set(); uniq = []
        for r in families[base]:
            if r['name'] in seen: continue
            seen.add(r['name']); uniq.append(r)
        families[base] = uniq

    # ───── Analyze each family ─────
    print("=" * 100)
    print(" Family-level sibling-tail outlier audit")
    print("=" * 100)
    print(f"  Total corpus cases : {len(records)}")
    print(f"  Sibling families   : {len(families)}")
    print()

    candidate_exclusions = {'sigma_ionic': [], 'sigma_e': []}

    for base in sorted(families):
        members = families[base]
        if len(members) < 2:
            continue
        # Family σ_ionic stats
        si_vals = [m['sigma_ionic'] for m in members if m['sigma_ionic'] is not None]
        se_vals = [m['sigma_e'] for m in members if m['sigma_e'] is not None]

        print("─" * 100)
        print(f" Family: {base}   (n = {len(members)} members)")
        print("─" * 100)

        # σ_ionic family stats
        if len(si_vals) >= 2:
            si_med = float(np.median(si_vals))
            si_mad = float(np.median(np.abs(np.array(si_vals) - si_med)))
            si_max_dev = max(abs(v - si_med) / si_med * 100 for v in si_vals)
            print(f"   σ_ionic family: median={si_med:.4f}  MAD={si_mad:.4f}  "
                  f"spread (n={len(si_vals)}):  {min(si_vals):.4f} ~ {max(si_vals):.4f}  "
                  f"(max dev {si_max_dev:.0f}%)")
            for m in sorted(members, key=lambda r: -((r['sigma_ionic'] or 0))):
                if m['sigma_ionic'] is None: continue
                dev_pct = (m['sigma_ionic'] - si_med) / si_med * 100
                marker = " ★ OUTLIER" if abs(dev_pct) > 50 else (
                         " ◆ FAR-TAIL" if abs(dev_pct) > 30 else "")
                print(f"     {m['name'][:42]:42s}  σ_i = {m['sigma_ionic']:8.4f}  "
                      f"({dev_pct:+6.1f}% from family median){marker}")
                if abs(dev_pct) > 50:
                    candidate_exclusions['sigma_ionic'].append(
                        (m['name'], m['sigma_ionic'], si_med, dev_pct))

        # σ_e family stats
        if len(se_vals) >= 2:
            se_med = float(np.median(se_vals))
            se_mad = float(np.median(np.abs(np.array(se_vals) - se_med)))
            se_max_dev = max(abs(v - se_med) / se_med * 100 for v in se_vals)
            print(f"   σ_e     family: median={se_med:.4f}  MAD={se_mad:.4f}  "
                  f"spread (n={len(se_vals)}):  {min(se_vals):.4f} ~ {max(se_vals):.4f}  "
                  f"(max dev {se_max_dev:.0f}%)")
            for m in sorted(members, key=lambda r: -((r['sigma_e'] or 0))):
                if m['sigma_e'] is None: continue
                dev_pct = (m['sigma_e'] - se_med) / se_med * 100
                marker = " ★ OUTLIER" if abs(dev_pct) > 50 else (
                         " ◆ FAR-TAIL" if abs(dev_pct) > 30 else "")
                print(f"     {m['name'][:42]:42s}  σ_e = {m['sigma_e']:8.4f}  "
                      f"({dev_pct:+6.1f}% from family median){marker}")
                if abs(dev_pct) > 50:
                    candidate_exclusions['sigma_e'].append(
                        (m['name'], m['sigma_e'], se_med, dev_pct))
        print()

    # ───── Summary ─────
    print("=" * 100)
    print(" CANDIDATE FAMILY-LEVEL EXCLUSIONS (>50% dev from family median)")
    print("=" * 100)
    print()
    print(f"  σ_ionic side ({len(candidate_exclusions['sigma_ionic'])} candidates):")
    for nm, v, med, dev in candidate_exclusions['sigma_ionic']:
        print(f"     {nm:42s}  σ_i={v:.4f} vs family median {med:.4f}  ({dev:+.0f}%)")
    if not candidate_exclusions['sigma_ionic']:
        print(f"     (none — all sibling families within ±50% of family median)")
    print()
    print(f"  σ_e side ({len(candidate_exclusions['sigma_e'])} candidates):")
    for nm, v, med, dev in candidate_exclusions['sigma_e']:
        print(f"     {nm:42s}  σ_e={v:.4f} vs family median {med:.4f}  ({dev:+.0f}%)")
    if not candidate_exclusions['sigma_e']:
        print(f"     (none — all sibling families within ±50% of family median)")
    print()

    # ───── Action recommendations ─────
    print("=" * 100)
    print(" RECOMMENDED ACTIONS")
    print("=" * 100)
    print()
    all_excl = (set(nm for nm, *_ in candidate_exclusions['sigma_ionic']) |
                set(nm for nm, *_ in candidate_exclusions['sigma_e']))
    if all_excl:
        print(f"  Add to _EXCLUDED_NAMES (σ_ionic) and/or _EXCLUDED_NAMES_EL (σ_e):")
        for nm in sorted(all_excl):
            ion_dev = next((d for n, _, _, d in candidate_exclusions['sigma_ionic']
                            if n == nm), None)
            ele_dev = next((d for n, _, _, d in candidate_exclusions['sigma_e']
                            if n == nm), None)
            tags = []
            if ion_dev is not None: tags.append(f"σ_i {ion_dev:+.0f}%")
            if ele_dev is not None: tags.append(f"σ_e {ele_dev:+.0f}%")
            print(f"     '{nm}',   # {' / '.join(tags)} from family median")
    else:
        print(f"  No family-level exclusions warranted (>50% threshold).")
        print(f"  All sibling families are statistically consistent.")
    print()
    print(f"  After adding these to _EXCLUDED, re-run:")
    print(f"     python3 scripts/electronic_nested_cv.py | grep -A3 'STAGE 12'")
    print(f"     python3 scripts/nested_cv_sat.py        | tail -40")


if __name__ == '__main__':
    main()
