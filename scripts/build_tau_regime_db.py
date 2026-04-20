"""
Build comprehensive tortuosity-regime database from all analyzed cases.

For each case extracts:
  - Identity (name, mode, ps_ratio, CAM vol%)
  - Geometry (phi_SE, thickness, porosity)
  - Topology (SE-SE CN mean, percolation %, top_reachable %, n_large_components)
  - Three tortuosities (tau_Dij, tau_Lap_geom, tau_Lap_eff) — derived if missing
  - Conductivities (sigma_full, sigma_bulk_net — Hertzian + physics)
  - Constriction fraction
  - Regime classification:
      * normal           : 1.3 <= Le/D <= 2.3
      * bottleneck       : Le/D > 2.3  (Dijkstra misses flux bottleneck)
      * surrogate_clean  : Le/D < 1.3  (Dijkstra ≈ Laplace, ideal packing)
      * near_threshold   : SE-SE CN < 3.5 OR percolation < 95%

Outputs:
  /tmp/tau_regime_db.json   (per-case full records)
  /tmp/tau_regime_db.csv    (flat table for plotting / spreadsheet)

Usage:
  python3 scripts/build_tau_regime_db.py
"""
from __future__ import annotations
import os, json, math, csv


SIGMA_GRAIN_MS = 3.0  # mS/cm, LPSCl bulk (MLIP-MD [S4])


def _find_meta(cid: str) -> dict:
    """Find meta.json in results/ or uploads/."""
    for base in ('webapp/results', 'webapp/uploads'):
        p = f'{base}/{cid}/meta.json'
        if os.path.exists(p):
            try:
                return json.load(open(p))
            except Exception:
                pass
    return {}


def _tau_from_sigma(phi_SE, sigma_mScm):
    """τ = √(φ_SE × σ_grain / σ_mScm), None if invalid."""
    if not (phi_SE and sigma_mScm and phi_SE > 0 and sigma_mScm > 0):
        return None
    try:
        return math.sqrt(phi_SE * SIGMA_GRAIN_MS / sigma_mScm)
    except Exception:
        return None


def _safe_div(a, b):
    try:
        if a is None or b is None or b == 0:
            return None
        return a / b
    except Exception:
        return None


def _regime(le_over_d, se_cn, perc_pct):
    flags = []
    if se_cn is not None and se_cn < 3.5:
        flags.append('near_threshold_CN')
    if perc_pct is not None and perc_pct < 95:
        flags.append('marginal_percolation')
    if le_over_d is not None:
        if le_over_d > 2.3:
            flags.append('bottleneck')
        elif le_over_d < 1.3:
            flags.append('surrogate_clean')
        else:
            flags.append('normal')
    return ','.join(flags) if flags else 'unknown'


def load_case(root: str) -> dict | None:
    fm_path = f'{root}/full_metrics.json'
    if not os.path.exists(fm_path):
        return None
    try:
        m = json.load(open(fm_path))
    except Exception:
        return None
    cid = os.path.basename(root)
    meta = _find_meta(cid)

    phi_SE = m.get('phi_se')
    sig_full = m.get('sigma_full_mScm')
    sig_bulk = m.get('sigma_bulk_net_mScm')

    tau_Dij = m.get('tortuosity_mean')
    tau_Lap_geom = _tau_from_sigma(phi_SE, sig_bulk)
    tau_Lap_eff = _tau_from_sigma(phi_SE, sig_full)

    le_over_d = _safe_div(tau_Lap_eff, tau_Dij)
    le_over_lg = _safe_div(tau_Lap_eff, tau_Lap_geom)
    lg_over_d = _safe_div(tau_Lap_geom, tau_Dij)

    # SE-SE CN key name: analyze_contacts writes as flat 'se_se_cn' (scalar mean)
    # Fallback variants for robustness across versions.
    se_cn = (m.get('se_se_cn')
             or m.get('se_se_cn_mean')
             or m.get('SE_SE_CN_mean'))
    # Handle case where it's stored as dict {'mean': X}
    if isinstance(se_cn, dict):
        se_cn = se_cn.get('mean')
    perc = m.get('percolation_pct', 0)
    bulk_frac = m.get('bulk_resistance_fraction')
    constr_frac = (1 - bulk_frac) if bulk_frac is not None else None

    cam_vol_pct = None
    if phi_SE is not None and m.get('porosity') is not None:
        cam_vol_pct = 100.0 * (1.0 - phi_SE - m['porosity']/100.0)

    return {
        'case_id':         cid,
        'name':            meta.get('name', cid),
        'mode':            meta.get('mode', '?'),
        'ps_ratio':        meta.get('ps_ratio', ''),
        'type_map':        meta.get('type_map', ''),
        # Geometry
        'phi_SE':          round(phi_SE, 4) if phi_SE else None,
        'CAM_vol_pct':     round(cam_vol_pct, 1) if cam_vol_pct else None,
        'porosity_pct':    round(m.get('porosity', 0), 2) if m.get('porosity') else None,
        'thickness_um':    round(m.get('thickness_um', 0), 1),
        # Topology
        'SE_SE_CN_mean':   round(se_cn, 2) if se_cn else None,
        'percolation_pct': round(perc, 1),
        'top_reach_pct':   round(m.get('top_reachable_pct', 0), 1),
        'n_large_clusters': m.get('n_large_components'),
        # Tortuosities (our 3)
        'tau_Dij':         round(tau_Dij, 3) if tau_Dij else None,
        'tau_Lap_geom':    round(tau_Lap_geom, 3) if tau_Lap_geom else None,
        'tau_Lap_eff':     round(tau_Lap_eff, 3) if tau_Lap_eff else None,
        'tau_sq_Lap_eff':  round(tau_Lap_eff**2, 2) if tau_Lap_eff else None,
        # Ratios
        'Le_over_Lg':      round(le_over_lg, 3) if le_over_lg else None,
        'Lg_over_D':       round(lg_over_d, 3) if lg_over_d else None,
        'Le_over_D':       round(le_over_d, 3) if le_over_d else None,
        # Conductivities
        'sigma_full_mScm':     sig_full,
        'sigma_full_physics':  m.get('sigma_full_mScm_physics'),
        'sigma_bulk_net_mScm': sig_bulk,
        # Constriction
        'bulk_R_frac':         round(bulk_frac, 3) if bulk_frac else None,
        'constriction_frac':   round(constr_frac, 3) if constr_frac else None,
        # Classification
        'regime':              _regime(le_over_d, se_cn, perc),
    }


def main():
    records = []
    for root, _, files in os.walk('webapp'):
        if 'full_metrics.json' in files:
            rec = load_case(root)
            if rec:
                records.append(rec)
    records.sort(key=lambda r: (r.get('phi_SE') or 0))

    print(f"Collected {len(records)} cases\n")

    # JSON out
    with open('/tmp/tau_regime_db.json', 'w') as f:
        json.dump(records, f, indent=2, default=str)
    print(f"Wrote /tmp/tau_regime_db.json ({len(records)} records)")

    # CSV out (flat)
    if records:
        fields = list(records[0].keys())
        with open('/tmp/tau_regime_db.csv', 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            w.writeheader()
            w.writerows(records)
        print(f"Wrote /tmp/tau_regime_db.csv")

    # Inline summary
    print("\n=== REGIME DISTRIBUTION ===")
    from collections import Counter
    tags = Counter()
    for r in records:
        for tag in (r.get('regime') or '').split(','):
            tags[tag] += 1
    for t, c in tags.most_common():
        print(f"  {t:25s} {c}")

    print("\n=== BOTTLENECK CASES (Le/D > 2.3) ===")
    bn = [r for r in records if (r.get('Le_over_D') or 0) > 2.3]
    print(f"{'name':30s} {'φ_SE':>6s} {'CN':>5s} {'τ_Dij':>6s} "
          f"{'τ_Le':>6s} {'Le/D':>6s} {'τ²_Le':>6s}")
    for r in bn:
        print(f"  {r['name'][:28]:30s} {r['phi_SE']:>6.3f} "
              f"{(r['SE_SE_CN_mean'] or 0):>5.2f} {(r['tau_Dij'] or 0):>6.2f} "
              f"{(r['tau_Lap_eff'] or 0):>6.2f} {(r['Le_over_D'] or 0):>6.2f} "
              f"{(r['tau_sq_Lap_eff'] or 0):>6.1f}")

    print("\n=== LITERATURE COMPARISON (φ_SE match, dedup by name) ===")
    # Dedup: keep one record per unique 'name' (prefer archive over results if duplicate)
    seen_names = {}
    for r in records:
        n = r.get('name')
        if not n or not r.get('phi_SE') or not r.get('tau_sq_Lap_eff'):
            continue
        if n not in seen_names:
            seen_names[n] = r
    dedup_records = list(seen_names.values())
    print(f"  (deduplicated to {len(dedup_records)} unique case names)")

    print(f"\n{'ref':28s} {'φ_SE_ref':>9s} {'τ²_ref':>7s}  "
          f"{'closest case':>25s} {'φ_SE':>6s} {'τ²':>6s} {'Δφ':>6s} {'err%':>6s}")
    print('-' * 98)
    anchors = [
        ('Minnmann 2021 42% CAM', 42, 0.44, 4.3),
        ('Wang 2023 70% CAM',     70, 0.26, 7.78),
        ('Wang 2023 80% CAM',     80, 0.16, 17.24),
        ('Dewald 2021 25% NCM',   25, 0.65, 2.4),
    ]
    for name, cam, phi_ref, tau2_ref in anchors:
        with_tau2 = [(r, abs(r['phi_SE'] - phi_ref)) for r in dedup_records]
        if not with_tau2:
            continue
        # Show top-3 closest by φ_SE
        with_tau2.sort(key=lambda x: x[1])
        closest3 = with_tau2[:3]
        for i, (r, dphi) in enumerate(closest3):
            err = 100 * (r['tau_sq_Lap_eff'] - tau2_ref) / tau2_ref
            prefix = f"  {name:26s} {phi_ref:>9.3f} {tau2_ref:>7.2f}  " if i == 0 else " " * 46
            print(f"{prefix}{r['name'][:24]:>25s} {r['phi_SE']:>6.3f} "
                  f"{r['tau_sq_Lap_eff']:>6.1f} {dphi:>6.3f} {err:>+6.0f}")


if __name__ == '__main__':
    main()
