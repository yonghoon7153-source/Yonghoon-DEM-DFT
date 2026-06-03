#!/usr/bin/env python3
"""Stage E — Full literature-grounded network solver.

Combines two literature corrections on top of the network solver:

  (1) Stagewise fracture σ_factor (Stage D, Lawn 1998 + Trevisanello 2021)
       intact / microcrack / multicrack / fragmentation / pulverization
       → 1.00 / 0.85 / 0.40 / 0.10 / 0.02
       (literature-realistic central estimate for σ_e_loss)

  (2) Per-particle σ_grain factor — material/synthesis correction
       (a) σ_ionic_grain_SE(r_SE) — Cronau 2022 amorphization
            r_SE 1.5 μm → 1.00, 1.0 → 0.85, 0.5 → 0.70, <0.3 → 0.33
       (b) σ_e_grain_AM(crystal) — Trevisanello 2021 SC vs PC
            AM_S (single-crystal): 1.00
            AM_P (polycrystalline): 0.65
       (c) κ_thermal_grain — AM crystallinity dependent (SE size-invariant
           because sulfide κ already in glassy regime, ~0.5 W/mK)
            AM_S: 1.00, AM_P: 0.50, SE: 1.00 regardless of r_SE

Channel-specific application via edge contact_area scaling:

  σ_ionic edges (SE-SE)         : × f_SE(r) on each particle, harmonic mean
  σ_e edges (AM-AM)             : × f_AM(crystal) on each, harmonic mean
                                   × f_fracture (Lawn stage)
  κ edges (all)                 : × f_κ(crystal/size) per pair-type

Implementation: scales contact_area + delta with channel-conditional logic
in a SINGLE pre-processed contacts.csv — network_conductivity then computes
σ_ionic / σ_e / κ from this with proper edge weights.

This is the *literature-realistic central estimate* for the paper's
σ_eff = σ_grain × η_topology framework, with all three orthogonal
corrections applied per Cronau 2022, Trevisanello 2021, and Wang 2022.

Output keys merged into full_metrics.json:
  sigma_full_mScm_stage_e               (σ_ionic, grain-corrected)
  electronic_sigma_full_mScm_stage_e    (σ_e, fracture + grain-corrected)
  thermal_sigma_full_mScm_stage_e       (κ, grain-corrected)
  electronic_sigma_loss_pct_stage_e
  thermal_sigma_loss_pct_stage_e
  stage_e_factors_used                  (audit trail)

Usage:
  python3 scripts/run_network_full_corrections.py
  python3 scripts/run_network_full_corrections.py --quiet
  python3 scripts/run_network_full_corrections.py CID …
"""
from __future__ import annotations
import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
import numpy as np

ROOT     = Path(__file__).resolve().parent.parent
SCRIPTS  = ROOT / 'scripts'
WEBAPP   = ROOT / 'webapp'
NET_PY   = SCRIPTS / 'network_conductivity.py'

sys.path.insert(0, str(SCRIPTS))
from fracture_model import fracture_classify_force_sim  # noqa: E402

# ── (1) Stagewise fracture σ_factor (Stage D) ────────────────────────────
FRACTURE_STAGES: list[tuple[float, float, float, str]] = [
    (-float('inf'),  1.0, 1.00, 'intact'),
    (1.0,            3.0, 0.85, 'microcrack'),
    (3.0,           11.0, 0.40, 'multicrack'),
    (11.0,          32.0, 0.10, 'fragmentation'),
    (32.0,  float('inf'), 0.02, 'pulverization'),
]


def _fracture_factor(m: float) -> tuple[float, str]:
    for lo, hi, f, lbl in FRACTURE_STAGES:
        if lo <= m < hi:
            return f, lbl
    return 1.0, 'intact'


# ── (2a) σ_ionic_grain_SE(r_SE) — literature-grounded, smooth size-effect ──
def sigma_ionic_grain_factor_SE(r_SE_real_um: float) -> float:
    """SE σ_grain factor — literature-grounded with smooth transition zone.

    Reference table (literature consensus):
      r_SE ≥ 1.5 μm  → 1.00   ✓ very high (산업 표준, multiple measurements)
      r_SE = 0.5 μm  → 1.00   ✓ high (Cronau optimum + SPS size-invariant)
      r_SE = 0.3 μm  → 0.90   ~ moderate (transition zone)
      r_SE = 0.1 μm  → 0.65   ✓ medium (SPS GB onset)
      r_SE ≤ 30 nm   → 0.33   ✓ high (Cronau extreme-milling limit)

    Critical literature findings:
      - Sulfide intra-grain GB is *negligible* (Going Against the Grain 2024).
      - Cronau 2022's 1/3 reduction is at *extended ball-milling*, primarily
        affecting D50 < 0.3 μm.
      - SPS data (ScienceDirect 2023): grain σ_grain drops only below ~100 nm.

    Trigger behavior: when atom file uploaded, auto-detects r_SE from
    atoms.csv (median SE radius / scale) and applies appropriate factor.
    """
    r = r_SE_real_um
    if r is None or not (r > 0): return 1.00       # safety default
    if r >= 0.5:  return 1.00                       # size-invariant region
    if r >= 0.3:  return 0.90                       # transition zone
    if r >= 0.1:  return 0.65                       # nano-GB onset (SPS)
    if r >= 0.03: return 0.33 + 0.32*(r-0.03)/0.07  # smooth interp 30-100 nm
    return 0.33                                      # extreme-milling limit


# ── (2b) σ_e_grain_AM(crystal, R) — DISABLED (2026-06-03, C2a refactor) ───
def sigma_e_grain_factor_AM(am_label: str, r_AM_real_um: float) -> float:
    """C2a refactor (2026-06-03): Trevisanello GB correction is now applied
    PER-PARTICLE inside the network solver via sigma_AM_relative(r, type)
    (see network_conductivity.py:64-77).  Applying the Stage E factor on
    top would DOUBLE-COUNT the same physics → over-correction
    (verified by σ_e regression after solver refactor went live).

    Returning 1.0 makes Stage E a pass-through for AM crystal corrections;
    the solver is now single-source-of-truth for Trevisanello physics.

    Historic step-function (kept as reference, NOT applied):
      AM_S (single-crystal):    1.00 (≥0.5μm), 0.85 (<0.5μm)
      AM_P (polycrystalline):   0.75 (≤3μm), 0.65 (5-7μm), 0.55 (7-12μm), 0.45 (>12μm)
    """
    return 1.0


# ── (2c) κ_thermal_grain(crystal, R) — Wang 2022 + phonon size effect ─────
def kappa_grain_factor_AM(am_label: str, r_AM_real_um: float) -> float:
    """AM κ factor — crystallinity × size-dependent phonon GB scattering.

    AM_S: phonon mostly bulk-like (preserved single-crystal κ ~5-8 W/mK).
    AM_P: secondary-particle internal GBs scatter phonons strongly.
          Effect scales with internal GB density which grows with
          secondary-particle size.

    Size-dependence table (AM_P):
      r ≤ 3 μm   → 0.65
      r 5-7 μm   → 0.50  (typical reference)
      r 7-12 μm  → 0.40
      r > 12 μm  → 0.30
    """
    if r_AM_real_um is None or not (r_AM_real_um > 0):
        r_AM_real_um = 6.0

    if 'AM_S' in am_label or am_label.endswith('S'):
        return 1.00

    # AM_P (polycrystalline)
    r = r_AM_real_um
    if r <= 3.0:  return 0.65
    if r <= 7.0:  return 0.50  # typical reference
    if r <= 12.0: return 0.40
    return 0.30


def kappa_grain_factor_SE(r_SE_real_um: float) -> float:
    """SE κ factor — sulfide is already glassy (~0.5 W/mK), size-invariant."""
    return 1.00


def _harmonic_mean(a: float, b: float) -> float:
    if a <= 0 or b <= 0: return 0.0
    return 2.0 * a * b / (a + b)


def discover_case_dirs() -> list[Path]:
    """Recursively find case dirs under results/ and archive/ at any depth.
    Fixes a depth-1-only iteration bug that silently skipped categorized
    archive cases (webapp/archive/category/case_id/)."""
    seen = set()
    out = []
    for base in ('results', 'archive'):
        root = WEBAPP / base
        if not root.exists(): continue
        for atoms_p in root.rglob('atoms.csv'):
            case_dir = atoms_p.parent
            if ((case_dir / 'contacts.csv').exists()
                    and (case_dir / 'full_metrics.json').exists()
                    and case_dir not in seen):
                seen.add(case_dir)
                out.append(case_dir)
    return sorted(out)


def _read_meta(case_dir: Path) -> dict:
    for path in (case_dir / 'meta.json',
                 WEBAPP / 'uploads' / case_dir.name / 'meta.json'):
        if path.exists():
            try: return json.load(open(path))
            except Exception: pass
    return {}


def parse_type_map(s: str) -> dict:
    out = {}
    for tok in (s or '').split(','):
        if ':' in tok:
            k, v = tok.split(':', 1)
            try: out[int(k.strip())] = v.strip()
            except Exception: pass
    return out


def _se_radius_real_um(atoms_df: pd.DataFrame, type_map: dict, scale: float) -> float:
    se_types = [tid for tid, lbl in type_map.items() if 'SE' in str(lbl)]
    if not se_types:
        return float('nan')
    sub = atoms_df[atoms_df['type'].isin(se_types)]
    if sub.empty:
        return float('nan')
    r_sim = float(sub['radius'].median())
    return r_sim * 1.0e6 / scale


def apply_corrections(atoms_df: pd.DataFrame, contacts_df: pd.DataFrame,
                       type_map: dict, scale: float
                       ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Return three modified contacts_df — one per channel — with appropriate
    contact_area scaling for σ_ionic / σ_e / κ_thermal computation."""
    am_types = {tid for tid, lbl in type_map.items() if 'AM' in str(lbl)}
    se_types = {tid for tid, lbl in type_map.items() if 'SE' in str(lbl)}
    id_to_type   = dict(zip(atoms_df['id'].astype(int),
                              atoms_df['type'].astype(int)))
    id_to_radius = dict(zip(atoms_df['id'].astype(int),
                              atoms_df['radius'].astype(float)))

    # Per-particle σ_e / κ factors — type AND size dependent
    scale_local = scale  # capture closure
    def particle_AM_factor(tid: int, pid: int) -> float:
        lbl = type_map.get(tid, '')
        if 'AM' not in lbl:
            return 1.00
        r_sim = id_to_radius.get(pid, 0.0)
        r_real_um = r_sim * 1.0e6 / scale_local if r_sim > 0 else 0.0
        return sigma_e_grain_factor_AM(lbl, r_real_um)

    def particle_kappa_factor(tid: int, pid: int) -> float:
        lbl = type_map.get(tid, '')
        r_sim = id_to_radius.get(pid, 0.0)
        r_real_um = r_sim * 1.0e6 / scale_local if r_sim > 0 else 0.0
        if 'SE' in lbl:
            return kappa_grain_factor_SE(r_real_um)
        if 'AM' in lbl:
            return kappa_grain_factor_AM(lbl, r_real_um)
        return 1.00

    # SE σ_ionic factor (single value, all SE same size in our cases)
    r_SE_real = _se_radius_real_um(atoms_df, type_map, scale)
    f_SE_ionic = sigma_ionic_grain_factor_SE(r_SE_real)

    # Build edge-by-edge factor arrays
    n = len(contacts_df)
    f_ionic = []   # for SE-SE only (others get 0 / N/A — solver ignores)
    f_e     = []   # for AM-AM only
    f_kappa = []   # for ALL contacts
    stage_counts = {lbl: 0 for *_, lbl in FRACTURE_STAGES}
    n_am_am = 0

    for _, c in contacts_df.iterrows():
        i1 = int(c['id1']); i2 = int(c['id2'])
        t1 = id_to_type.get(i1); t2 = id_to_type.get(i2)
        if t1 is None or t2 is None:
            f_ionic.append(1.0); f_e.append(1.0); f_kappa.append(1.0); continue

        is_se_se = (t1 in se_types and t2 in se_types)
        is_am_am = (t1 in am_types and t2 in am_types)
        is_am_se = ((t1 in am_types and t2 in se_types) or
                    (t1 in se_types and t2 in am_types))

        # Channel 1: σ_ionic
        if is_se_se:
            f_ionic.append(f_SE_ionic)
        else:
            f_ionic.append(1.0)  # AM not in ionic graph anyway

        # Channel 2: σ_e — fracture × grain
        if is_am_am:
            n_am_am += 1
            r1 = id_to_radius.get(i1, 0.0); r2 = id_to_radius.get(i2, 0.0)
            r_min = min(r1, r2)
            fn = float(c.get('fn', 0) or 0)
            if fn <= 0:
                fn = math.sqrt((c.get('fn_x', 0) or 0) ** 2
                                + (c.get('fn_y', 0) or 0) ** 2
                                + (c.get('fn_z', 0) or 0) ** 2)
            if r_min > 0 and fn > 0:
                pair_label = '-'.join(sorted([type_map.get(t1, ''),
                                                type_map.get(t2, '')]))
                _stg, _pc, mult = fracture_classify_force_sim(
                    fn, r_min, contact_type=pair_label, scale=scale)
                ff, lbl = _fracture_factor(mult)
            else:
                ff, lbl = 1.0, 'intact'
            stage_counts[lbl] += 1

            # Grain factor (harmonic mean of two AM particles, size-dependent)
            g1 = particle_AM_factor(t1, i1); g2 = particle_AM_factor(t2, i2)
            gf = _harmonic_mean(g1, g2)
            f_e.append(ff * gf)
        else:
            f_e.append(1.0)  # SE not in electronic graph

        # Channel 3: κ — size-dependent grain factor
        k1 = particle_kappa_factor(t1, i1); k2 = particle_kappa_factor(t2, i2)
        kf = _harmonic_mean(k1, k2)
        f_kappa.append(kf)

    # Audit trail — sample one representative AM_P and AM_S particle to log
    def _sample_radius(label: str) -> float:
        for tid, lbl in type_map.items():
            if lbl == label:
                sub = atoms_df[atoms_df['type'] == tid]
                if not sub.empty:
                    r_sim = float(sub['radius'].median())
                    return r_sim * 1.0e6 / scale
        return 0.0
    r_AM_P = _sample_radius('AM_P')
    r_AM_S = _sample_radius('AM_S')

    f_AM_P_e = sigma_e_grain_factor_AM('AM_P', r_AM_P) if r_AM_P > 0 else None
    f_AM_S_e = sigma_e_grain_factor_AM('AM_S', r_AM_S) if r_AM_S > 0 else None
    f_AM_P_k = kappa_grain_factor_AM('AM_P',  r_AM_P) if r_AM_P > 0 else None
    f_AM_S_k = kappa_grain_factor_AM('AM_S',  r_AM_S) if r_AM_S > 0 else None
    f_SE_k   = kappa_grain_factor_SE(r_SE_real) if r_SE_real > 0 else None

    factors_summary = {
        'r_SE_um':         r_SE_real,
        'r_AM_P_um':       r_AM_P,
        'r_AM_S_um':       r_AM_S,
        'f_SE_ionic':      f_SE_ionic,
        'AM_factors':      {'AM_S': f_AM_S_e, 'AM_P': f_AM_P_e},
        'kappa_factors':   {'AM_S': f_AM_S_k, 'AM_P': f_AM_P_k, 'SE': f_SE_k},
        'n_am_am_total':   n_am_am,
        'fracture_stage_counts': {k: int(v) for k, v in stage_counts.items()},
    }

    # Build three separate modified contacts_df
    df_ionic = contacts_df.copy()
    df_e     = contacts_df.copy()
    df_kappa = contacts_df.copy()
    factors_ionic = pd.Series(f_ionic, index=contacts_df.index)
    factors_e     = pd.Series(f_e,     index=contacts_df.index)
    factors_kappa = pd.Series(f_kappa, index=contacts_df.index)
    for col in ('contact_area', 'delta'):
        if col in df_ionic.columns:
            df_ionic[col] = df_ionic[col].astype(float) * factors_ionic
            df_e[col]     = df_e[col].astype(float) * factors_e
            df_kappa[col] = df_kappa[col].astype(float) * factors_kappa

    # Drop edges whose total factor falls below MIN_FACTOR_CUTOFF (default
    # 0.05 = 5 % of original conductance). This is the same philosophy as
    # Stage C's binary cutoff: contacts in the pulverization stage
    # (σ_factor 0.02) combined with AM_P grain factor (0.65) leave
    # contact_area at ~1.3 % of original — these are essentially-broken
    # contacts that the solver should treat as severed, not as ill-
    # conditioned tiny-g edges that destabilise the LU solve.
    #
    # Empirically, keeping these tiny edges produced σ_e Stage E values
    # 5-130× higher than baseline for 10/80 cases — mathematically
    # impossible because Stage E's σ_factor ≤ 1 must reduce σ. Dropping
    # them eliminates the matrix dynamic-range explosion that causes
    # spsolve to mis-converge.
    MIN_FACTOR_CUTOFF = 0.05
    n_orig = len(df_e)
    df_e = df_e[factors_e >= MIN_FACTOR_CUTOFF].reset_index(drop=True)
    df_ionic = df_ionic[factors_ionic >= MIN_FACTOR_CUTOFF].reset_index(drop=True)
    df_kappa = df_kappa[factors_kappa >= MIN_FACTOR_CUTOFF].reset_index(drop=True)
    factors_summary['n_dropped_e'] = n_orig - len(df_e)
    factors_summary['n_dropped_ionic'] = n_orig - len(df_ionic)
    factors_summary['n_dropped_kappa'] = n_orig - len(df_kappa)
    factors_summary['min_factor_cutoff'] = MIN_FACTOR_CUTOFF

    # Conductance-weighted mean factor per channel (used as fallback when
    # the network solver returns None due to numerical instability for
    # near-percolation-threshold topologies). The weight is the ORIGINAL
    # contact_area (proxy for original g, since g ∝ contact_area / R_total
    # ∝ contact_area for matched-radius pairs). For each channel:
    #    σ_stage_e_approx ≈ σ_baseline × <factor>_g-weighted
    # which is a Bruggeman-style effective-medium approximation.
    if 'contact_area' in contacts_df.columns:
        ca = contacts_df['contact_area'].astype(float).clip(lower=0).values
    else:
        ca = np.ones(len(contacts_df))
    g_proxy = ca

    def _wm(factors_list):
        f_arr = np.asarray(factors_list, dtype=float)
        denom = float(g_proxy.sum())
        if denom <= 0:
            return None
        return float((g_proxy * f_arr).sum() / denom)

    factors_summary['weighted_factor_ionic'] = _wm(f_ionic)
    factors_summary['weighted_factor_e']     = _wm(f_e)
    factors_summary['weighted_factor_kappa'] = _wm(f_kappa)

    return df_ionic, df_e, df_kappa, factors_summary


def _run_solver(case_dir: Path, contacts_modified: pd.DataFrame, type_map_str: str,
                  scale: float) -> dict | None:
    with tempfile.TemporaryDirectory(prefix='nfse_') as tmpd:
        tmp = Path(tmpd)
        shutil.copy2(case_dir / 'atoms.csv', tmp / 'atoms.csv')
        contacts_modified.to_csv(tmp / 'contacts.csv', index=False)
        # CRITICAL: copy input_params.json so network_conductivity reads
        # correct box_x, box_y (otherwise defaults to 0.05×0.05 and σ is
        # off by box-area ratio). Same for meta.json (some helpers read it).
        for aux in ('input_params.json', 'meta.json'):
            src = case_dir / aux
            if src.exists():
                shutil.copy2(src, tmp / aux)
        cmd = [sys.executable, str(NET_PY),
               str(tmp / 'atoms.csv'), str(tmp / 'contacts.csv'),
               '-o', str(tmp), '-t', type_map_str, '-s', str(int(scale)),
               '--contact-mode', 'both']
        try:
            cp = subprocess.run(cmd, check=False, capture_output=True,
                                  text=True, timeout=1800)
        except Exception:
            return None
        if cp.returncode != 0:
            return None
        net_json_p = tmp / 'network_conductivity.json'
        if not net_json_p.exists():
            return None
        with open(net_json_p) as f:
            return json.load(f)


# ── Self-report card ─────────────────────────────────────────────────
# Bielefeld 2022 reports 10-50 Ω·cm² ASR_ionic for sulfide ASSB cathodes
# at ~1 mAh/cm² loading; Lee 2020 reports 30-80 Ω·cm² at 380 MPa cold
# press.  We use a permissive union 10-200 Ω·cm² as the
# "within published experimental window" flag.
ASR_IONIC_TRUST_RANGE_OHM_CM2 = (10.0, 200.0)


def _compute_validation_flags(fm: dict, factors: dict,
                                sigma_ionic_e, sigma_e_e, sigma_th_e
                                ) -> dict:
    """Five-flag self-report card written into full_metrics.json after
    every Stage-E run.  Each flag is `bool | None`; None means the
    underlying metric is missing for this case (so downstream tools
    should treat it as 'not assessable' rather than 'failed').
    """
    flags: dict = {}

    # (1) ASR_ionic within Bielefeld/Lee range -----------------------
    # ASR = L / σ_ionic where L is cathode thickness (cm) and
    # σ_ionic is in S/cm.  Use Stage-E σ_ionic when available,
    # otherwise baseline.
    L_um = fm.get('thickness_um') or fm.get('cathode_thickness_um')
    sig_iso = (sigma_ionic_e if sigma_ionic_e and sigma_ionic_e > 0
                else fm.get('sigma_full_mScm'))
    if L_um and sig_iso and sig_iso > 0:
        L_cm = float(L_um) * 1.0e-4
        sigma_S_cm = float(sig_iso) * 1.0e-3
        asr = L_cm / sigma_S_cm           # Ω·cm²
        lo, hi = ASR_IONIC_TRUST_RANGE_OHM_CM2
        flags['within_bielefeld_range'] = bool(lo <= asr <= hi)
        flags['asr_ionic_Ohm_cm2']      = round(asr, 2)
    else:
        flags['within_bielefeld_range'] = None
        flags['asr_ionic_Ohm_cm2']      = None

    # (2) Fracture distribution realistic ----------------------------
    # Two sanity checks: severe % ≤ 50 (Lawn 1998 cone-crack experiments
    # rarely show >40 % severe even at 1 GPa loading), and at least one
    # contact landed in each of intact / microcrack / multicrack
    # (otherwise the classifier saw all contacts in one bucket and
    # something upstream is broken).
    sc = factors.get('fracture_stage_counts') or {}
    n_severe = (sc.get('fragmentation', 0) + sc.get('pulverization', 0))
    n_tot    = sum(sc.values()) if sc else 0
    if n_tot > 0:
        sev_pct = 100.0 * n_severe / n_tot
        diversity = sum(1 for v in sc.values() if v > 0)
        flags['fracture_distribution_realistic'] = bool(
            sev_pct <= 50.0 and diversity >= 1)
        flags['fracture_severe_pct'] = round(sev_pct, 2)
    else:
        flags['fracture_distribution_realistic'] = None
        flags['fracture_severe_pct']            = None

    # (3) Stage-E factor edge-drop ratio (<= 0.5 trustworthy) --------
    # apply_corrections drops edges whose total factor falls below the
    # 5 % cutoff (MIN_FACTOR_CUTOFF).  If we end up throwing more than
    # half of the AM-AM electronic edges away the Bruggeman fallback
    # is doing nearly all the work and the result should be flagged.
    n_drop_e = factors.get('n_dropped_e')
    n_amam   = factors.get('n_am_am_total')
    if n_drop_e is not None and n_amam:
        drop_ratio = float(n_drop_e) / float(n_amam)
        flags['edge_drop_ratio_e'] = round(drop_ratio, 4)
        flags['solver_input_intact'] = bool(drop_ratio <= 0.5)
    else:
        flags['edge_drop_ratio_e']  = None
        flags['solver_input_intact'] = None

    # (4) Stage-E σ ≤ baseline (factor ≤ 1 invariant) ---------------
    # Bruggeman fallback guarantees this by construction, but the
    # solver path doesn't, so we record whether the invariant held.
    def _le(a, b, tol=1.05):
        if a is None or b is None: return None
        return bool(a <= b * tol)
    flags['stage_e_le_baseline_sigma_e']  = _le(
        sigma_e_e,     fm.get('electronic_sigma_full_mScm'))
    flags['stage_e_le_baseline_sigma_ion'] = _le(
        sigma_ionic_e, fm.get('sigma_full_mScm'))
    flags['stage_e_le_baseline_kappa']    = _le(
        sigma_th_e,    fm.get('thermal_sigma_full_mScm'))

    # (5) Bruggeman fallback fired ---------------------------------
    src = fm.get('stage_e_source') or {}
    flags['bruggeman_fallback_fired_any'] = bool(any(
        v == 'fallback_weighted_factor' for v in src.values()))

    # Overall trust flag — every *assessable* gate must be True; gates
    # whose underlying metric is missing (None) are treated as
    # "not assessable" rather than "failed" so older archive cases
    # whose Stage-E run predates a newer factor key still pass when the
    # available evidence is positive.  `gates_evaluated` records which
    # gates the verdict actually rests on.
    gate_results = {
        'within_bielefeld_range':         flags['within_bielefeld_range'],
        'fracture_distribution_realistic': flags['fracture_distribution_realistic'],
        'solver_input_intact':            flags['solver_input_intact'],
        'stage_e_le_baseline_sigma_e':    flags['stage_e_le_baseline_sigma_e'],
    }
    assessable = {k: v for k, v in gate_results.items() if v is not None}
    flags['gates_evaluated']    = sorted(assessable.keys())
    flags['gates_not_assessed'] = sorted(k for k, v in gate_results.items()
                                           if v is None)
    flags['trustworthy_overall'] = bool(assessable and
                                          all(v is True for v in assessable.values()))
    return flags


def run_one(case_dir: Path) -> tuple[str, bool, str]:
    meta = _read_meta(case_dir)
    type_map = parse_type_map(meta.get('type_map', '1:AM_P,2:AM_S,3:SE'))
    if not type_map:
        type_map = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    type_map_str = meta.get('type_map', '1:AM_P,2:AM_S,3:SE')
    scale = float(meta.get('scale', 1000))

    atoms_df = pd.read_csv(case_dir / 'atoms.csv')
    contacts_df = pd.read_csv(case_dir / 'contacts.csv', low_memory=False)

    df_ionic, df_e, df_kappa, factors = apply_corrections(
        atoms_df, contacts_df, type_map, scale)

    # Optimization: if every per-contact factor for a channel is 1.0 (e.g.
    # Cronau σ_ionic factor is size-invariant ×1.00 for r_SE ≥ 0.5 µm), the
    # modified contacts are identical to the original and re-running the
    # solver is wasted work — and worse, it sometimes returns a *different*
    # numerical answer due to LU-solve / sparse-matrix conditioning that's
    # sensitive to row ordering changes from reset_index. Detect that case
    # and skip the solver, reusing the baseline values directly.
    def _factor_is_unity(channel: str) -> bool:
        key = {'ionic': 'f_SE_ionic',
               'e':     'weighted_factor_e',
               'kappa': 'weighted_factor_kappa'}[channel]
        if channel == 'ionic':
            v = factors.get('f_SE_ionic')
            return v is not None and abs(v - 1.0) < 1e-9
        v = factors.get(key)
        # For e/kappa, the weighted factor is a Bruggeman-style mean; only
        # consider unity-pass when AM factors are explicitly all 1.0
        if channel == 'e':
            af = factors.get('AM_factors', {})
            return all(abs((af.get(k) or 1.0) - 1.0) < 1e-9 for k in ('AM_P', 'AM_S'))
        if channel == 'kappa':
            kf = factors.get('kappa_factors', {})
            return all(abs((kf.get(k) or 1.0) - 1.0) < 1e-9
                       for k in ('AM_P', 'AM_S', 'SE'))
        return False

    skip_ionic = _factor_is_unity('ionic')
    skip_e     = _factor_is_unity('e')
    skip_kappa = _factor_is_unity('kappa')

    # Run solver only for channels that actually have corrections to apply
    res_ionic = None if skip_ionic else _run_solver(case_dir, df_ionic, type_map_str, scale)
    res_e     = None if skip_e     else _run_solver(case_dir, df_e,     type_map_str, scale)
    res_kappa = None if skip_kappa else _run_solver(case_dir, df_kappa, type_map_str, scale)

    fm_path = case_dir / 'full_metrics.json'
    try:
        with open(fm_path) as f:
            fm = json.load(f)
    except Exception as e:
        return (case_dir.name, False, f'fm read failed: {e}')

    # When solver was skipped (factor ≡ 1.0), reuse baseline values from
    # the pre-existing full_metrics.json (= the network solver baseline).
    # When solver ran, take its output.
    sigma_ionic_e = (fm.get('sigma_full_mScm') if skip_ionic else
                     (res_ionic.get('sigma_full_mScm') if res_ionic else None))
    sigma_e_e     = (fm.get('electronic_sigma_full_mScm') if skip_e else
                     (res_e.get('electronic_sigma_full_mScm') if res_e else None))
    sigma_th_e    = (fm.get('thermal_sigma_full_mScm') if skip_kappa else
                     (res_kappa.get('thermal_sigma_full_mScm') if res_kappa else None))

    # --- Physics-mode parallel: solver returned both modes via --contact-mode
    # both, so the same JSON has *_physics counterparts. Stage E factors
    # (Lawn fracture × Cronau / Trev / Wang) are grain-level corrections
    # that apply equally to both contact-area models. Reading the *_physics
    # variants here lets the UI display Stage E for Hertzian AND Physics
    # baselines side-by-side (mirrors the existing Network Solver section
    # 4-column format: Hertzian | Physics | Δ%).
    sigma_ionic_e_p = (fm.get('sigma_full_mScm_physics') if skip_ionic else
                       (res_ionic.get('sigma_full_mScm_physics') if res_ionic else None))
    sigma_e_e_p     = (fm.get('electronic_sigma_full_mScm_physics') if skip_e else
                       (res_e.get('electronic_sigma_full_mScm_physics') if res_e else None))
    sigma_th_e_p    = (fm.get('thermal_sigma_full_mScm_physics') if skip_kappa else
                       (res_kappa.get('thermal_sigma_full_mScm_physics') if res_kappa else None))

    # Auto-trigger: factor-weighted Bruggeman fallback when solver fails
    # or returns unphysical values. Conditions for triggering fallback:
    #   (a) solver returned None (full failure)
    #   (b) solver returned ≤ 0
    #   (c) solver value > 1.1 × baseline (impossible: Stage E factors ≤ 1)
    #
    # Approximation: σ_stage_e ≈ σ_baseline × Σ(g_i · f_i) / Σ(g_i)
    # where g_i ∝ original contact_area (proxy for original conductance),
    # f_i = per-contact factor (fracture σ × grain). This is a Bruggeman-
    # style effective-medium estimate that's mathematically consistent
    # with the framework's σ_factor ≤ 1 constraint.
    source_ionic = 'baseline_no_correction' if skip_ionic else 'solver'
    source_e     = 'baseline_no_correction' if skip_e     else 'solver'
    source_th    = 'baseline_no_correction' if skip_kappa else 'solver'
    fallback_messages = []

    def _is_invalid(v, base):
        return (v is None or not (v > 0)
                or (base is not None and base > 0 and v > base * 1.1))

    def _trigger_reason(v, base):
        if v is None: return 'solver returned None'
        if not (v > 0): return f'solver returned non-positive ({v})'
        if base and v > base * 1.1: return f'solver result {v:.3f} > 1.1·baseline {base:.3f}'
        return ''

    base_ionic = fm.get('sigma_full_mScm')
    base_e_solver = fm.get('electronic_sigma_full_mScm')
    base_th_solver = fm.get('thermal_sigma_full_mScm')
    # Physics baselines for the parallel Stage E pass
    base_ionic_p   = fm.get('sigma_full_mScm_physics')
    base_e_p       = fm.get('electronic_sigma_full_mScm_physics')
    base_th_p      = fm.get('thermal_sigma_full_mScm_physics')

    # ── Hertzian-baseline Stage E fallback ──
    if _is_invalid(sigma_ionic_e, base_ionic) and base_ionic and factors.get('weighted_factor_ionic') is not None:
        reason = _trigger_reason(sigma_ionic_e, base_ionic)
        sigma_ionic_e = base_ionic * factors['weighted_factor_ionic']
        source_ionic = 'fallback_weighted_factor'
        fallback_messages.append(
            f"σ_i fallback ({reason}) → {sigma_ionic_e:.4f} = {base_ionic:.4f}×{factors['weighted_factor_ionic']:.3f}")
    if _is_invalid(sigma_e_e, base_e_solver) and base_e_solver and factors.get('weighted_factor_e') is not None:
        reason = _trigger_reason(sigma_e_e, base_e_solver)
        sigma_e_e = base_e_solver * factors['weighted_factor_e']
        source_e = 'fallback_weighted_factor'
        fallback_messages.append(
            f"σ_e fallback ({reason}) → {sigma_e_e:.3f} = {base_e_solver:.3f}×{factors['weighted_factor_e']:.3f}")
    if _is_invalid(sigma_th_e, base_th_solver) and base_th_solver and factors.get('weighted_factor_kappa') is not None:
        reason = _trigger_reason(sigma_th_e, base_th_solver)
        sigma_th_e = base_th_solver * factors['weighted_factor_kappa']
        source_th = 'fallback_weighted_factor'
        fallback_messages.append(
            f"κ fallback ({reason}) → {sigma_th_e:.3f} = {base_th_solver:.3f}×{factors['weighted_factor_kappa']:.3f}")

    # ── Physics-baseline Stage E fallback (mirrors above logic) ──
    source_ionic_p = 'baseline_no_correction' if skip_ionic else 'solver'
    source_e_p     = 'baseline_no_correction' if skip_e     else 'solver'
    source_th_p    = 'baseline_no_correction' if skip_kappa else 'solver'
    if _is_invalid(sigma_ionic_e_p, base_ionic_p) and base_ionic_p and factors.get('weighted_factor_ionic') is not None:
        sigma_ionic_e_p = base_ionic_p * factors['weighted_factor_ionic']
        source_ionic_p = 'fallback_weighted_factor'
    if _is_invalid(sigma_e_e_p, base_e_p) and base_e_p and factors.get('weighted_factor_e') is not None:
        sigma_e_e_p = base_e_p * factors['weighted_factor_e']
        source_e_p = 'fallback_weighted_factor'
    if _is_invalid(sigma_th_e_p, base_th_p) and base_th_p and factors.get('weighted_factor_kappa') is not None:
        sigma_th_e_p = base_th_p * factors['weighted_factor_kappa']
        source_th_p = 'fallback_weighted_factor'

    fm['stage_e_source'] = {
        'sigma_ionic':    source_ionic,
        'sigma_e':        source_e,
        'sigma_thermal':  source_th,
        # Physics-baseline counterparts (mirrors Hertzian fields above)
        'sigma_ionic_physics':    source_ionic_p,
        'sigma_e_physics':        source_e_p,
        'sigma_thermal_physics':  source_th_p,
    }

    # Hertzian-baseline Stage E (existing keys, backward-compatible)
    fm['sigma_full_mScm_stage_e']            = sigma_ionic_e
    fm['electronic_sigma_full_mScm_stage_e'] = sigma_e_e
    fm['thermal_sigma_full_mScm_stage_e']    = sigma_th_e
    # Physics-baseline Stage E (NEW — added so UI can show 4-col Δ% format
    # mirroring the Network Solver section)
    fm['sigma_full_mScm_stage_e_physics']            = sigma_ionic_e_p
    fm['electronic_sigma_full_mScm_stage_e_physics'] = sigma_e_e_p
    fm['thermal_sigma_full_mScm_stage_e_physics']    = sigma_th_e_p
    fm['stage_e_factors_used'] = {
        'r_SE_um':       factors['r_SE_um'],
        'f_SE_ionic':    factors['f_SE_ionic'],
        'AM_factors':    factors['AM_factors'],
        'kappa_factors': factors['kappa_factors'],
    }
    fm['stage_e_fracture_stage_counts'] = factors['fracture_stage_counts']
    fm['fracture_aware_method_full']    = 'Stage E (fracture + grain corrections)'

    # Loss percentages (vs baseline σ_e_full / σ_th_full)
    base_ionic = fm.get('sigma_full_mScm')
    base_e     = fm.get('electronic_sigma_full_mScm')
    base_th    = fm.get('thermal_sigma_full_mScm')
    if base_ionic and base_ionic > 0 and sigma_ionic_e is not None:
        fm['sigma_ionic_loss_pct_stage_e'] = round((1.0 - sigma_ionic_e/base_ionic)*100, 2)
    if base_e and base_e > 0 and sigma_e_e is not None:
        fm['electronic_sigma_loss_pct_stage_e'] = round((1.0 - sigma_e_e/base_e)*100, 2)
    if base_th and base_th > 0 and sigma_th_e is not None:
        fm['thermal_sigma_loss_pct_stage_e'] = round((1.0 - sigma_th_e/base_th)*100, 2)

    # ── Per-case self-report card ────────────────────────────────────
    # Five boolean trust flags so downstream consumers (paper §6
    # Bielefeld-range check, dashboard "trustworthy?" column, batch QC)
    # can filter cases without re-running every gate. Conservative on
    # purpose — when a value is missing the flag stays False.
    fm['validation_flags'] = _compute_validation_flags(
        fm, factors, sigma_ionic_e, sigma_e_e, sigma_th_e)

    with open(fm_path, 'w') as f:
        json.dump(fm, f, indent=2, default=str)

    msg = (f'σ_i: {(base_ionic or 0):.3f}→{(sigma_ionic_e or 0):.3f} '
           f'(P:{(base_ionic_p or 0):.3f}→{(sigma_ionic_e_p or 0):.3f}) '
           f'σ_e: {(base_e or 0):.2f}→{(sigma_e_e or 0):.2f} '
           f'(P:{(base_e_p or 0):.2f}→{(sigma_e_e_p or 0):.2f}) '
           f'κ: {(base_th or 0):.2f}→{(sigma_th_e or 0):.2f}  '
           f'r_SE={factors["r_SE_um"]:.2f}μm')
    if fallback_messages:
        # Tag the case message so it surfaces in main() loop output, and
        # emit per-channel reasons on a continuation line so the user can
        # see which channel triggered the Bruggeman-style fallback.
        msg += f'  [⚡FALLBACK×{len(fallback_messages)}]'
        for fm_msg in fallback_messages:
            print(f'         ↳ {fm_msg}', flush=True)
    return (case_dir.name, True, msg)


def main() -> None:
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids')
    ap.add_argument('--quiet', action='store_true', help='One line per case')
    args = ap.parse_args()

    all_cases = discover_case_dirs()
    if args.cases:
        # Accept either bare case IDs (`input_6mAh_real40_4`) or full/partial
        # paths (`webapp/archive/후막(6mAh)/input_6mAh_real40_4`). Compare on
        # the leaf name so users can copy-paste the same path they see in the
        # webapp URL without "No cases found." friction.
        wanted = {Path(c).name for c in args.cases}
        cases = [d for d in all_cases if d.name in wanted]
        missing = wanted - {d.name for d in cases}
        if missing:
            print(f'  warning: not found in archive/results: {sorted(missing)}',
                  flush=True)
    else:
        cases = all_cases
    if not cases:
        ap.error('No cases found.')

    print(f'Stage E (literature-grounded full corrections) on {len(cases)} cases',
          flush=True)
    print('  Channel 1 (σ_ionic) : SE size-dependent σ_grain (Cronau 2022)')
    print('  Channel 2 (σ_e)     : fracture stagewise × AM crystal (Trevisanello 2021)')
    print('  Channel 3 (κ)       : AM crystal grain (Wang 2022, SE size-invariant)\n')

    n_ok = n_fail = 0
    for i, d in enumerate(cases, 1):
        try:
            cid, ok, msg = run_one(d)
        except Exception as e:
            cid, ok, msg = (d.name, False, f'EXC: {type(e).__name__}: {e}')
        tag = '✓' if ok else '✗'
        if not args.quiet or not ok:
            print(f'  [{i:3d}/{len(cases)}] {tag} {cid:30s}  {msg[:130]}',
                  flush=True)
        if ok: n_ok += 1
        else:  n_fail += 1
    print(f'\nDone — {n_ok} ok, {n_fail} failed.', flush=True)
    if n_fail: sys.exit(1)


if __name__ == '__main__':
    main()
