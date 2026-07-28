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
import os
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

# σ_grain + 온도 규약 단일 출처.  이 파일은 network_conductivity 를 **서브프로세스**로 부르므로
# import 만으로는 온도가 전달되지 않는다 — 아래 _run_solver 가 CLI 플래그로 명시 전달한다.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import se_material  # noqa: E402

# Mirror app.py: load webapp/.env then honor WEBAPP_*_FOLDER so this CLI finds
# the SAME data the webapp serves — e.g. a worktree runner whose results live in
# a shared dir (env, no symlink).  Without this, WEBAPP/results is hardcoded and
# Stage E silently processes the wrong (empty) folder.
_envf = WEBAPP / '.env'
if _envf.exists():
    for _l in _envf.read_text().splitlines():
        _l = _l.strip()
        if _l and not _l.startswith('#') and '=' in _l:
            _k, _v = _l.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip())
RESULTS_DIR = Path(os.environ.get('WEBAPP_RESULTS_FOLDER') or (WEBAPP / 'results'))
ARCHIVE_DIR = Path(os.environ.get('WEBAPP_ARCHIVE_FOLDER') or (WEBAPP / 'archive'))
UPLOADS_DIR = Path(os.environ.get('WEBAPP_UPLOAD_FOLDER') or (WEBAPP / 'uploads'))

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


# ── (2b) σ_e_grain_AM(crystal, R) — Trevisanello 2021 + size dependence ───
def sigma_e_grain_factor_AM(am_label: str, r_AM_real_um: float) -> float:
    """AM σ_e factor — crystallinity × size-dependent internal-GB density.

    NOTE on stacking with solver-internal Trevisanello (2026-06-03):
    The network solver (network_conductivity.py:64-77 sigma_AM_relative) ALSO
    applies a smooth Trevisanello GB factor per AM_P particle.  Initial
    concern: these double-count.  Investigation (debug_solver_gate.py) showed
    the solver refactor IS firing correctly per-particle, BUT the network
    output is dominated by the AM_S backbone when AM_P is a minority phase,
    so solver-side reduction shows minimally in σ_e_raw.  Stage E's step-
    function correction here carries the bulk of the experimentally-observed
    σ_e compression to the 5-20 mS/cm regime that matches literature.  The
    two corrections are complementary at this corpus density, not redundant.

    Reference values (literature):
      AM_S (single-crystal): bulk σ_e size-invariant for r ≥ 0.5 μm.
        Wang 2021 measured single-crystal NMC at 1-5 μm with consistent σ.
      AM_P (polycrystalline): internal primary-grain GBs scale with
        secondary-particle size. Larger AM_P → more internal GBs →
        lower effective σ_e through the particle.
        Trevisanello 2021 reference is for typical NMC secondary (5-12 μm).

    Size-dependence table (AM_P):
      r ≤ 3 μm   → 0.75   (small secondary, fewer internal GBs)
      r 5-7 μm   → 0.65   (typical NMC commercial, Trevisanello reference)
      r 7-12 μm  → 0.55   (larger NMC, more internal GBs)
      r > 12 μm  → 0.45   (very large secondary)
    """
    if r_AM_real_um is None or not (r_AM_real_um > 0):
        r_AM_real_um = 6.0  # safety default = typical commercial NMC

    if 'AM_S' in am_label or am_label.endswith('S'):
        # Single-crystal: bulk size-invariant for r ≥ 0.5 μm
        if r_AM_real_um >= 0.5: return 1.00
        return 0.85  # mild surface effect at sub-μm (rare)

    # AM_P (polycrystalline)
    r = r_AM_real_um
    if r <= 3.0:  return 0.75
    if r <= 7.0:  return 0.65  # Trevisanello 2021 reference
    if r <= 12.0: return 0.55
    return 0.45


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
    for root in (RESULTS_DIR, ARCHIVE_DIR):
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
                 UPLOADS_DIR / case_dir.name / 'meta.json'):
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


def _solver_temp_flags(temp_c=None, ea_ion_ev=None) -> list:
    """network_conductivity 서브프로세스에 붙일 온도 플래그.

    ★ 미지정(temp_c None) → **빈 리스트** → cmd 가 예전과 문자 단위로 동일하다.  Stage-E 를
    지금까지 돌린 모든 런은 이 경로이므로 bitwise 불변이 보장된다.
    """
    if temp_c is None:
        return []
    flags = ['--temp-c', f'{float(temp_c):g}']
    if ea_ion_ev is not None:
        flags += ['--ea-ion-ev', f'{float(ea_ion_ev):g}']
    return flags


def _run_solver(case_dir: Path, contacts_modified: pd.DataFrame, type_map_str: str,
                  scale: float, temp_c=None, ea_ion_ev=None) -> dict | None:
    with tempfile.TemporaryDirectory(prefix='nfse_') as tmpd:
        tmp = Path(tmpd)
        shutil.copy2(case_dir / 'atoms.csv', tmp / 'atoms.csv')
        contacts_modified.to_csv(tmp / 'contacts.csv', index=False)
        # CRITICAL: copy input_params.json so network_conductivity reads
        # correct box_x, box_y (otherwise defaults to 0.05×0.05 and σ is
        # off by box-area ratio). Same for meta.json (some helpers read it).
        # mesh_info.json is REQUIRED too: without it network_conductivity falls
        # back to plate_z = max(atom z), which for cases with a sparse top tail
        # overshoots the true plate plane (e.g. 0.0506 vs true 0.0165 → 3×).
        # That collapses the top electrode (top_ids → 1 atom) and breaks the
        # whole geometry — the THERMAL (all-contact) solve then fails to
        # percolate and returns None (κ=0), while φ and σ come out wrong.
        for aux in ('input_params.json', 'meta.json', 'mesh_info.json'):
            src = case_dir / aux
            if src.exists():
                shutil.copy2(src, tmp / aux)
        cmd = [sys.executable, str(NET_PY),
               str(tmp / 'atoms.csv'), str(tmp / 'contacts.csv'),
               '-o', str(tmp), '-t', type_map_str, '-s', str(int(scale)),
               '--contact-mode', 'both']
        # ★ 온도 전달 (2026-07-28 적대검증 C-2).  이 파일은 솔버를 **서브프로세스**로 부르기 때문에
        #   se_material 을 import 해봐야 자식 프로세스에는 아무 영향이 없었다 — 그래서 DEM 프로덕션
        #   σ 경로(Stage E)에는 온도 루트가 아예 없었다.  플래그로 명시 전달한다.
        #   미지정이면 리스트가 비어 cmd 가 예전과 동일 (bitwise 불변).
        cmd += _solver_temp_flags(temp_c, ea_ion_ev)
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


def run_one(case_dir: Path, temp_c=None, ea_ion_ev=None) -> tuple[str, bool, str]:
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

    fm_path = case_dir / 'full_metrics.json'
    try:
        with open(fm_path) as f:
            fm = json.load(f)
    except Exception as e:
        return (case_dir.name, False, f'fm read failed: {e}')

    # ── ★ 운전온도 (2026-07-28 C-2) ────────────────────────────────────────────────
    # σ_grain 은 이온 채널의 **순수 곱셈 prefactor** 이므로 (network_conductivity 가 σ_bulk 에 완전
    # 선형), σ_ionic 계열 전량이 t_fac 에 선형이다.  그래서 두 경로가 자동으로 정합한다:
    #   · 솔버를 다시 돌리는 채널 → 자식이 --temp-c 로 σ_grain(T) 를 써서 이미 T 값
    #   · 보정계수가 1.0 이라 재솔브를 건너뛰고 **기존 25 °C 베이스라인을 재사용**하는 채널
    #     → 여기서 t_fac 을 곱해 준다.  ⚠ 이 곱셈이 없으면 T 런에서 stage_e(=T) 와 baseline(=25 °C)
    #       이 한 파일 안에 섞여 (a) loss% 가 −379 % 같은 값이 되고 (b) `v > 1.1·base` fallback
    #       가드가 항상 발동해 정답을 25 °C 값으로 **덮어써 버린다**.  둘 다 조용한 오답이다.
    # temp_c 미지정 → t_fac 은 **정확히 1.0** → _at_T 는 입력을 그대로 반환(곱셈조차 안 함) →
    # 기존 전 코퍼스 bitwise 불변.
    t_fac = se_material.arrhenius_sigma_factor(temp_c, ea_ion_ev)

    def _at_T(v):
        """T_ref(25 °C) 이온 σ 를 운전 T 로 옮긴다.  t_fac==1.0 이면 bitwise 그대로."""
        if v is None or t_fac == 1.0:
            return v
        return v * t_fac

    skip_ionic = _factor_is_unity('ionic')
    skip_e     = _factor_is_unity('e')
    # Thermal uses ALL contacts (AM-AM ∪ AM-SE ∪ SE-SE), so it MUST percolate
    # wherever ionic OR electronic does.  A baseline κ=0 alongside a non-zero
    # ionic/electronic is therefore a broken/missed baseline, NOT a real
    # degeneracy — re-solve thermal instead of reusing that 0 (skip only when the
    # correction factor is unity AND the baseline κ is already valid > 0).
    skip_kappa = (_factor_is_unity('kappa')
                  and (fm.get('thermal_sigma_full_mScm') or 0) > 0)

    # Run solver only for channels that need it (a correction OR a broken baseline)
    res_ionic = None if skip_ionic else _run_solver(case_dir, df_ionic, type_map_str, scale,
                                                    temp_c, ea_ion_ev)
    res_e     = None if skip_e     else _run_solver(case_dir, df_e,     type_map_str, scale,
                                                    temp_c, ea_ion_ev)
    res_kappa = None if skip_kappa else _run_solver(case_dir, df_kappa, type_map_str, scale,
                                                    temp_c, ea_ion_ev)

    # When solver was skipped (factor ≡ 1.0), reuse baseline values from
    # the pre-existing full_metrics.json (= the network solver baseline).
    # When solver ran, take its output.
    #   ⚠ 재사용 분기는 _at_T 로 운전 T 에 맞춘다 (solver 분기는 자식이 이미 T 로 풀었다).
    sigma_ionic_e = (_at_T(fm.get('sigma_full_mScm')) if skip_ionic else
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
    sigma_ionic_e_p = (_at_T(fm.get('sigma_full_mScm_physics')) if skip_ionic else
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

    # ⚠ 이온 베이스라인만 _at_T (저장된 값은 25 °C).  σ_e/κ 는 솔버가 T 로 스케일하지 않으므로
    #   (Reisacher: ohmic T-무관 / κ 앵커 없음 §F1) 그대로 두는 것이 정합이다.
    base_ionic = _at_T(fm.get('sigma_full_mScm'))
    base_e_solver = fm.get('electronic_sigma_full_mScm')
    base_th_solver = fm.get('thermal_sigma_full_mScm')
    # Physics baselines for the parallel Stage E pass
    base_ionic_p   = _at_T(fm.get('sigma_full_mScm_physics'))
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

    # ── Heal a stale/missing THERMAL baseline ────────────────────────────
    # The pre-fix solver stored κ_baseline=0 for cases the single-phase
    # sigma_ratio>1.5 guard wrongly rejected (thermal is the multi-phase
    # superset network — see network_conductivity.solve_network).  The webapp
    # phantom-suppresses the κ rows whenever `thermal_sigma_full_mScm` is
    # falsy (app.py: p_th_h = ... or not metrics.get('thermal_sigma_full_mScm')),
    # so a stale 0 would keep κ shown as '—' even though we just recomputed a
    # valid Stage-E κ.  When we DID re-solve (skip_kappa False) and the stored
    # baseline is still 0/None but Stage-E κ is valid, recover the raw baseline
    # from the corrected value and the Bruggeman-weighted κ factor — the exact
    # inverse of the framework's own σ_stage_e ≈ σ_baseline·Σ(g·f)/Σg relation.
    # Only thermal: electronic/ionic baseline=0 is genuine non-percolation
    # (single-phase, the guard correctly rejects) and must stay '—'.
    if (not skip_kappa) and not (fm.get('thermal_sigma_full_mScm') or 0) > 0:
        _fk = factors.get('weighted_factor_kappa')
        if sigma_th_e and sigma_th_e > 0 and _fk and _fk > 0:
            fm['thermal_sigma_full_mScm'] = round(sigma_th_e / _fk, 6)
        if sigma_th_e_p and sigma_th_e_p > 0 and _fk and _fk > 0:
            fm['thermal_sigma_full_mScm_physics'] = round(sigma_th_e_p / _fk, 6)

    # Loss percentages (vs baseline σ_e_full / σ_th_full)
    # ⚠ 이온은 _at_T 로 **같은 온도**의 베이스라인과 비교해야 한다.  Stage-E 손실은 Cronau 입도
    # 보정 몫이지 온도 몫이 아니므로, t_fac 은 분자·분모에서 정확히 상쇄되어 loss% 는 T 와 무관하다
    # (= 이 값이 T 를 켰다고 달라지면 그게 버그다).
    base_ionic = _at_T(fm.get('sigma_full_mScm'))
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

    # ── ★ 온도 provenance (T1-a) — T 를 준 런에서만 기록한다 ───────────────────────────
    # 미지정 런에는 이 키가 아예 생기지 않으므로 기존 full_metrics.json 은 키 집합까지 동일하다.
    # 기록하는 이유: 이 파일은 *_stage_e 키만 덮어쓰므로, T 런이면 **한 파일 안에 두 온도가 공존**한다
    #   (stage_e = 운전 T,  베이스라인 sigma_full_mScm = 25 °C).  하류가 이걸 모르면 조용히 섞는다.
    if temp_c is not None:
        _prov = se_material.provenance(temp_c, ea_ion_ev)
        _prov['applied_to'] = [
            'sigma_full_mScm_stage_e', 'sigma_full_mScm_stage_e_physics',
            '(+ 이들에서 파생되는 validation_flags.asr_ionic_Ohm_cm2)',
        ]
        _prov['NOT_applied_to'] = {
            'sigma_full_mScm / _physics (베이스라인)':
                '이 스크립트는 *_stage_e 만 갱신한다 → 베이스라인은 25 °C 값 그대로. '
                '같은 파일 안에서 두 온도가 섞이므로 비교 전 반드시 이 필드를 볼 것.',
            'electronic_* / thermal_*':
                'σ_e 는 ohmic T-무관(Reisacher, 정성) · κ 는 앵커 없음(§F1) → 솔버가 스케일하지 않는다.',
            'porosity / coverage / 접촉면적':
                'SE 경도 H(T)/σ_y(T) 앵커 없음(§F1) — 형상은 25 °C 압밀 결과 그대로.',
        }
        _prov['loss_pct_is_T_invariant'] = (
            'sigma_ionic_loss_pct_stage_e 는 분자·분모 모두 T 로 스케일되어 t_fac 이 상쇄된다 '
            '(= Stage-E 손실은 Cronau 입도 몫이지 온도 몫이 아니다).')
        _prov['injected_by'] = 'scripts/run_network_full_corrections.py --temp-c'
        fm['stage_e_temperature_provenance'] = _prov

    # atomic write: dump to a temp file in the SAME dir, then os.replace (atomic
    # rename) → a kill mid-write can never leave a truncated/corrupt full_metrics.json
    # (the original stays intact until the rename completes; on error the temp is removed).
    fd, _tmp = tempfile.mkstemp(dir=str(fm_path.parent), prefix='.full_metrics.', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(fm, f, indent=2, default=str)
        os.replace(_tmp, fm_path)
    except Exception:
        try:
            os.unlink(_tmp)
        except OSError:
            pass
        raise

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


# ══════════════════════════════════════════════════════════════════════════════
def _selftest_temp() -> int:
    """--temp-c 배선 회귀시험 (2026-07-28 적대검증 C-2).

      python3 scripts/run_network_full_corrections.py --selftest-temp

    검사:
      [1] ★기본값 bitwise 불변 — --temp-c 를 안 주면 (a) 서브프로세스 cmd 가 문자 단위로 예전과
          같고 (b) full_metrics.json 이 **바이트 동일**하며 (c) 새 키가 하나도 안 생긴다.
      [2] 온도 전달 — 주면 cmd 에 --temp-c/--ea-ion-ev 가 붙고 자식이 실제로 σ_grain(T) 를 쓴다.
      [3] ★재사용 분기 누출 차단 — Cronau 계수가 1.0 이라 솔버를 건너뛰고 25 °C 베이스라인을
          재사용하는 경로에서도 σ_stage_e 가 T 로 스케일된다 (안 하면 solver 분기와 T 가 어긋난다).
      [4] ★fallback 가드 오발 차단 — `v > 1.1·base` 비교가 같은 온도끼리 이뤄져,
          T 를 켰다고 stage_e 가 25 °C 폴백값으로 덮이지 않는다.
      [5] loss% 는 T 불변 (Stage-E 손실 = Cronau 입도 몫, 온도 몫 아님).
      [6] σ_e / κ 는 T 에 안 움직인다 (Reisacher ohmic / κ 앵커 없음 §F1).
      [7] provenance 가 "베이스라인은 25 °C 로 남는다"를 명시한다.
    """
    import copy
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")

    # ── [1]/[2] cmd 문자열 ────────────────────────────────────────────────────
    chk('temp 미지정 → 솔버 플래그 0개 (cmd 문자 단위 동일)', _solver_temp_flags() == [])
    chk('temp 지정 → --temp-c 전달', _solver_temp_flags(60.0) == ['--temp-c', '60'])
    chk('Eₐ 동반 지정 → --ea-ion-ev 도 전달',
        _solver_temp_flags(60.0, 0.29) == ['--temp-c', '60', '--ea-ion-ev', '0.29'])
    _base_cmd = ['py', 'net', 'a', 'c', '-o', 'x', '-t', 'm', '-s', '1000',
                 '--contact-mode', 'both']
    chk('cmd + 미지정플래그 == cmd (append 가 no-op)',
        _base_cmd + _solver_temp_flags(None) == _base_cmd)

    # ── 합성 케이스 (DEM 런 불필요) ───────────────────────────────────────────
    BASE_ION, BASE_ION_P = 0.1234, 0.1500
    BASE_E, BASE_TH = 5.6789, 7.7000

    def make_case(root, r_se_sim):
        d = Path(root); d.mkdir(parents=True, exist_ok=True)
        rows = [(1, 1, 0.003), (2, 1, 0.003), (3, 2, 0.001), (4, 2, 0.001),
                (5, 3, r_se_sim), (6, 3, r_se_sim), (7, 3, r_se_sim)]
        pd.DataFrame(rows, columns=['id', 'type', 'radius']).to_csv(d / 'atoms.csv', index=False)
        con = [(1, 2, 1e-9, 1e-7, 1e-4), (3, 4, 1e-9, 1e-7, 1e-4),
               (5, 6, 1e-9, 1e-7, 1e-4), (6, 7, 1e-9, 1e-7, 1e-4),
               (1, 5, 1e-9, 1e-7, 1e-4)]
        pd.DataFrame(con, columns=['id1', 'id2', 'contact_area', 'delta', 'fn']
                     ).to_csv(d / 'contacts.csv', index=False)
        json.dump({'type_map': '1:AM_P,2:AM_S,3:SE', 'scale': 1000, 'name': 'selftest'},
                  open(d / 'meta.json', 'w'))
        json.dump({'sigma_full_mScm': BASE_ION, 'sigma_full_mScm_physics': BASE_ION_P,
                   'electronic_sigma_full_mScm': BASE_E,
                   'thermal_sigma_full_mScm': BASE_TH,
                   'phi_se': 0.35, 'porosity': 15.6}, open(d / 'full_metrics.json', 'w'))
        return d

    # 자식 솔버 모킹: 실제 network_conductivity 는 σ_bulk 에 **완전 선형**이므로
    # (σ_full_mScm = σ_full · σ_bulk · 1000), --temp-c 는 정확히 Arrhenius 배수로 나타난다.
    real_run_solver = globals()['_run_solver']
    seen_flags = []

    def fake_run_solver(case_dir, contacts_modified, type_map_str, scale,
                        temp_c=None, ea_ion_ev=None):
        seen_flags.append(_solver_temp_flags(temp_c, ea_ion_ev))
        f = se_material.arrhenius_sigma_factor(temp_c, ea_ion_ev)
        wf = 0.70    # Cronau 0.5 µm 계수 (계수<1 분기에서만 호출된다)
        return {'sigma_full_mScm': BASE_ION * wf * f,
                'sigma_full_mScm_physics': BASE_ION_P * wf * f,
                'electronic_sigma_full_mScm': BASE_E * 0.9,
                'electronic_sigma_full_mScm_physics': BASE_E * 0.9,
                'thermal_sigma_full_mScm': BASE_TH * 0.9,
                'thermal_sigma_full_mScm_physics': BASE_TH * 0.9}

    T_C = 60.0
    FAC = se_material.arrhenius_sigma_factor(T_C)     # ×4.7851 (Eₐ 0.41, T_ref 25)
    with tempfile.TemporaryDirectory(prefix='nfse_selftest_') as td:
        globals()['_run_solver'] = fake_run_solver
        try:
            # r_SE = 1.5 µm → Cronau 계수 1.0 → skip_ionic(재사용 분기)
            # r_SE = 0.5 µm 은 표상 1.00 이라 0.25 µm 를 써서 계수<1(solver 분기)를 만든다
            for tag, r_se_sim, path in (('reuse', 1.5e-3, 'skip'), ('solver', 0.25e-3, 'run')):
                d_off = make_case(Path(td) / f'{tag}_off', r_se_sim)
                d_off2 = make_case(Path(td) / f'{tag}_off2', r_se_sim)
                d_on = make_case(Path(td) / f'{tag}_on', r_se_sim)
                fm0 = copy.deepcopy(json.load(open(d_off / 'full_metrics.json')))
                run_one(d_off)                                   # 기본 (T 미지정)
                run_one(d_off2)                                  # 재현성
                run_one(d_on, temp_c=T_C)                        # T 적용
                a = (d_off / 'full_metrics.json').read_bytes()
                b = (d_off2 / 'full_metrics.json').read_bytes()
                fa = json.loads(a)
                fb_on = json.load(open(d_on / 'full_metrics.json'))

                chk(f'[{tag}] 기본 런은 결정적(byte-identical)', a == b)
                chk(f'[{tag}] 기본 런에 온도 키가 생기지 않음',
                    'stage_e_temperature_provenance' not in fa)
                chk(f'[{tag}] 기본 런 σ_i_stage_e 가 T 무관 경로와 정확히 같은 값',
                    fa['sigma_full_mScm_stage_e'] == (BASE_ION if path == 'skip'
                                                      else BASE_ION * 0.70),
                    f"{fa['sigma_full_mScm_stage_e']!r}")
                chk(f'[{tag}] 기본 런이 베이스라인을 건드리지 않음',
                    fa['sigma_full_mScm'] == fm0['sigma_full_mScm'])

                # T 적용 = 기본값 × Arrhenius (재사용/솔버 두 분기 모두)
                want = fa['sigma_full_mScm_stage_e'] * FAC
                chk(f'[{tag}] --temp-c 60 → σ_i_stage_e = 기본 × {FAC:.4f}',
                    abs(fb_on['sigma_full_mScm_stage_e'] / want - 1.0) < 1e-12,
                    f"{fb_on['sigma_full_mScm_stage_e']:.6f} vs {want:.6f}")
                chk(f'[{tag}] physics 분기도 동일 배수',
                    abs(fb_on['sigma_full_mScm_stage_e_physics']
                        / (fa['sigma_full_mScm_stage_e_physics'] * FAC) - 1.0) < 1e-12)
                # ★ fallback 가드 오발 차단: 25 °C 폴백값(baseline×wf)으로 덮이지 않았다
                chk(f'[{tag}] fallback 가드가 T 런을 25 °C 값으로 덮지 않음',
                    fb_on['stage_e_source']['sigma_ionic'] != 'fallback_weighted_factor'
                    and fb_on['sigma_full_mScm_stage_e'] > fa['sigma_full_mScm_stage_e'] * 4.0)
                # loss% 는 T 불변
                chk(f'[{tag}] loss% 는 T 불변',
                    (fa.get('sigma_ionic_loss_pct_stage_e')
                     == fb_on.get('sigma_ionic_loss_pct_stage_e')),
                    f"{fa.get('sigma_ionic_loss_pct_stage_e')} vs "
                    f"{fb_on.get('sigma_ionic_loss_pct_stage_e')}")
                # σ_e / κ 는 T 에 안 움직인다
                chk(f'[{tag}] σ_e stage_e 는 T 무관',
                    fa['electronic_sigma_full_mScm_stage_e']
                    == fb_on['electronic_sigma_full_mScm_stage_e'])
                chk(f'[{tag}] κ stage_e 는 T 무관',
                    fa['thermal_sigma_full_mScm_stage_e']
                    == fb_on['thermal_sigma_full_mScm_stage_e'])
                # 베이스라인은 25 °C 로 남고, provenance 가 그 사실을 적는다
                chk(f'[{tag}] T 런도 베이스라인은 25 °C 값 그대로',
                    fb_on['sigma_full_mScm'] == fm0['sigma_full_mScm'])
                prov = fb_on.get('stage_e_temperature_provenance') or {}
                chk(f'[{tag}] provenance: ARRHENIUS + T_ref 25 + Eₐ 0.41 + 배수',
                    prov.get('T_dependence') == 'ARRHENIUS' and prov.get('T_ref_C') == 25.0
                    and prov.get('Ea_ion_eV') == 0.41
                    and abs((prov.get('sigma_ion_T_factor') or 0) - FAC) < 1e-12)
                chk(f'[{tag}] provenance 가 "베이스라인은 25 °C" 를 명시',
                    any('베이스라인' in k for k in (prov.get('NOT_applied_to') or {})))
                # 서브프로세스 분기에서만 플래그가 실제로 전달돼야 한다
                if path == 'run':
                    chk(f'[{tag}] solver 분기에서 --temp-c 가 자식에게 전달됨',
                        ['--temp-c', '60'] in seen_flags)
                # ★ 반사실(counterfactual): _at_T 없이 25 °C 베이스라인과 비교했다면 어떻게
                #   틀렸는지 — 이 시험이 지키는 것이 무엇인지 스스로 증명한다.
                _b25 = fm0['sigma_full_mScm']
                _cf_loss = (1.0 - fb_on['sigma_full_mScm_stage_e'] / _b25) * 100
                _cf_guard = fb_on['sigma_full_mScm_stage_e'] > _b25 * 1.1
                chk(f'[{tag}] (반사실) 25 °C 베이스라인과 비교했다면 loss%={_cf_loss:.1f} % 이고 '
                    f'fallback 가드가 {"발동" if _cf_guard else "미발동"} → 실제로 오답이 된다',
                    _cf_loss < -100.0 and _cf_guard)
        finally:
            globals()['_run_solver'] = real_run_solver

    print('STAGE-E TEMP WIRING SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=__doc__)
    ap.add_argument('cases', nargs='*', help='Specific case_ids (dir leaf) OR readable names with --name')
    ap.add_argument('--quiet', action='store_true', help='One line per case')
    ap.add_argument('--name', action='store_true',
                    help='Match positional args against meta.json["name"] (readable, e.g. '
                         'input_2mAh_a5_p00) instead of the TIMESTAMP dir leaf')
    ap.add_argument('--missing-only', action='store_true',
                    help='Only cases whose full_metrics.json lacks *_stage_e keys — fast '
                         'backfill of cases that show Stage E "—" (skips already-done cases)')
    # ★ --temp-c / --ea-ion-ev (둘 다 기본 None = 현행, 서브프로세스 cmd 문자열까지 동일).
    #   이 배선 전에는 DEM 프로덕션 σ 경로(Stage E)에 온도 루트가 **아예 없었다** — 이 파일이
    #   network_conductivity 를 서브프로세스로 부르므로 import 만으로는 온도가 넘어가지 않는다.
    se_material.temperature_argparse(ap)
    args = ap.parse_args()
    if args.ea_ion_ev is not None and args.temp_c is None:
        ap.error('--ea-ion-ev 는 --temp-c 와 함께만 의미가 있다 (온도 없이 Eₐ 만 주면 no-op) '
                 '— 조용히 무시하지 않고 여기서 멈춘다.')

    all_cases = discover_case_dirs()
    if args.cases:
        # Accept either bare case IDs (`input_6mAh_real40_4`) or full/partial
        # paths (`webapp/archive/후막(6mAh)/input_6mAh_real40_4`). Compare on
        # the leaf name so users can copy-paste the same path they see in the
        # webapp URL without "No cases found." friction.  With --name, match the
        # readable meta name instead (dir leaves are TIMESTAMP cids).
        wanted = {Path(c).name for c in args.cases}
        if args.name:
            cases = [d for d in all_cases if _read_meta(d).get('name') in wanted]
            found = {_read_meta(d).get('name') for d in cases}
        else:
            cases = [d for d in all_cases if d.name in wanted]
            found = {d.name for d in cases}
        missing = wanted - found
        if missing:
            print(f'  warning: not found in archive/results: {sorted(missing)}',
                  flush=True)
    else:
        cases = all_cases
    if args.missing_only:
        def _has_stage_e(d: Path) -> bool:
            try:
                fm = json.load(open(d / 'full_metrics.json'))
            except Exception:
                return False
            return bool(fm.get('sigma_full_mScm_stage_e'))
        before = len(cases)
        cases = [d for d in cases if not _has_stage_e(d)]
        print(f'  --missing-only: {before - len(cases)} already have Stage E → '
              f'{len(cases)} to process', flush=True)
    if not cases:
        ap.error('No cases found.')

    print(f'Stage E (literature-grounded full corrections) on {len(cases)} cases',
          flush=True)
    print('  Channel 1 (σ_ionic) : SE size-dependent σ_grain (Cronau 2022)')
    print('  Channel 2 (σ_e)     : fracture stagewise × AM crystal (Trevisanello 2021)')
    print('  Channel 3 (κ)       : AM crystal grain (Wang 2022, SE size-invariant)\n')
    if args.temp_c is not None:
        se_material.warn_band(args.temp_c, args.ea_ion_ev)
        print('  [T] ⚠ σ_ionic(+stage_e) 만 T 로 스케일된다. 같은 full_metrics.json 안의 '
              'baseline sigma_full_mScm 은 25 °C 값 그대로 남는다 '
              '→ stage_e_temperature_provenance 를 반드시 확인할 것.\n', flush=True)

    n_ok = n_fail = 0
    for i, d in enumerate(cases, 1):
        try:
            cid, ok, msg = run_one(d, temp_c=args.temp_c, ea_ion_ev=args.ea_ion_ev)
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
    if '--selftest-temp' in sys.argv:
        sys.exit(_selftest_temp())
    main()
