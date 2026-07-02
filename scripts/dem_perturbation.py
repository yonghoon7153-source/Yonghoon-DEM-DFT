#!/usr/bin/env python3
"""DEM post-compaction PERTURBATION LAYER.

Physics-driven adjustment of the REAL DEM particle geometry (positions + radii)
to represent states the single frozen 300-MPa DEM snapshot cannot.  One engine,
several drivers — reusable across the roadmap (works standalone AND after the
Phase-3 predictor / for inverse design):

  • springback  — hooke/hysteresis ELASTIC UNLOAD (press release).  In the LIGGGHTS
                  hysteretic model the UNLOAD stiffness is set by
                  coefficientMaxElasticStiffness (m6 = k₂/k₁), NOT by
                  coefficientRestitution (m3 = the VISCOUS damping, quasi-static-
                  irrelevant).  Linear hysteretic recovery on unload to F=0:
                     recovered overlap Δδ = δ·(k₁/k₂) = δ / (k₂/k₁),
                  residual (plastic) overlap = δ·(1 − k₁/k₂).  PAIR-DEPENDENT
                  (input_real_14): AM-AM k₂/k₁=1.5 → recover 67 %; AM-SE=3.0 → 33 %;
                  SE-SE=5.0 → 20 %.  So the SE matrix (stiff unload + strong adhesion
                  m7 kc=1e6 cold-weld) barely springs back and stays compacted, while
                  the AM recover more (and lose the most contact area).  This is the
                  DEM's OWN contact model run in reverse → frame[4]-consistent, NOT an
                  arbitrary expansion.  m7 (adhesion) makes it an UPPER bound (real ≤
                  this, SE-SE most suppressed); m8 (plasticity depth φf) caps the
                  plastic overlap.  Extra real springback beyond the rigid-sphere
                  contacts (SE viscoelastic / binder) is a separate quantified gap.
                                                                          [LIVE]
  • breathing   — (de)lithiation radius change r→r·(1+ΔV/3): overlaps shift, some
                  contacts are LOST (δ<0) → σ_ionic/σ_e drop → cycle degradation.
                  Driver stub below (NCM SOC-volume curve = the independent physics).
  • dilate      — VGCF rod-network jamming prop-open (Philipse φ·L/D≈5.4).  Driver
                  stub below.

ENGINE (shared): a driver returns, per contact, the NEW overlap (and, per atom,
the NEW radius).  From the overlap CHANGES the layer computes the confined-
uniaxial macroscopic strain ε_zz — the DEM box is a periodic x,y RVE with a free
z platen ('boundary p p f'), so lateral strain is ~0 and all recovery goes into
z — by best fit  ε_zz·b_z·n_z = Δ(separation)  over the contact network.  Then it
updates porosity/thickness and (optionally) writes perturbed atoms.csv +
contacts.csv so the EXISTING scripts/network_conductivity.py recomputes the
perturbed σ (transport is NOT reinvented here).

NON-CIRCULAR: every driver's magnitude comes from INDEPENDENT physics (COR, NCM
SOC-volume, rod L/D) — never tuned to match a target porosity.
SMALL-PERTURBATION validity: the position update is a first-order affine z-stretch;
large rearrangements (overlaps opening a full diameter) need a real DEM re-run.

Usage:
    python3 scripts/dem_perturbation.py --case webapp/results/<cid> --driver springback [--cor 0.3]
    python3 scripts/dem_perturbation.py --selftest
    # write perturbed CSVs for an unloaded-σ re-solve:
    python3 scripts/dem_perturbation.py --case <cid> --driver springback --write-csv <out_dir>
"""
from __future__ import annotations
import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

# LIGGGHTS production contact model — input_real_14.liggghts, 'gran model hooke/hysteresis'.
#   types 1:AM_P  2:AM_S  3:SE.  Pair matrices read straight off fixes m1..m8.
REAL14 = {
    'youngsModulus':          {1: 1.4e8, 2: 1.4e8, 3: 0.135e7},   # m1 (softened LIGGGHTS units)
    'poissonsRatio':          {1: 0.25,  2: 0.25,  3: 0.30},      # m2
    'coefficientRestitution': 0.3,                                 # m3 — VISCOUS damping (dynamic); NOT the unload
    # m6 coefficientMaxElasticStiffness = k₂/k₁ (unload/load stiffness ratio) → THIS drives springback.
    'k2_over_k1': {(1, 1): 1.5, (1, 2): 1.5, (1, 3): 3.0,
                   (2, 2): 1.5, (2, 3): 3.0, (3, 3): 5.0},
    # m7 coefficientAdhesionStiffness kc — SE-SE 1e6 (cold-weld/vdW) resists springback (→ upper-bound flag).
    'adhesion':          {(1, 1): 1.0e5, (1, 2): 1.0e5, (1, 3): 2.0e5,
                          (2, 2): 1.0e5, (2, 3): 2.0e5, (3, 3): 1.0e6},
    # m8 coefficientPlasticityDepth φf — max plastic overlap fraction (below it a contact is fully elastic).
    'plasticity_depth':  {(1, 1): 0.05, (1, 2): 0.05, (1, 3): 0.01,
                          (2, 2): 0.05, (2, 3): 0.01, (3, 3): 0.005},
}
DEFAULT_COR = REAL14['coefficientRestitution']   # kept for the CLI note only (viscous, not the unload stiffness)


def _pair(matrix, t1, t2, default=None):
    """Symmetric per-type-pair lookup (LIGGGHTS peratomtypepair)."""
    if t1 is None or t2 is None:
        return default
    return matrix.get((t1, t2), matrix.get((t2, t1), default))


# ─────────────────────────────────────────────────────────────────────────────
# Load — minimal, self-contained (columns confirmed vs analyze_contacts.py)
#   atoms.csv    : id,type,x,y,z,radius(,c_strs[*],v*)
#   contacts.csv : id1,id2,fn_x,fn_y,fn_z,ft_*,contact_area,delta
# ─────────────────────────────────────────────────────────────────────────────
class DEMState:
    def __init__(self, atoms, contacts, box_x, box_y, scale, porosity_loaded=None,
                 thickness_um_loaded=None):
        self.atoms = atoms                      # {id: {'type','x','y','z','radius'}}
        self.contacts = contacts                # [{'id1','id2','delta','contact_area',...}]
        self.box_x = box_x                      # sim units (lateral period)
        self.box_y = box_y
        self.scale = scale                      # box units per µm  (µm = sim / scale? see _um)
        self.porosity_loaded = porosity_loaded  # fraction [0,1] from full_metrics (validated)
        self.thickness_um_loaded = thickness_um_loaded

    def um(self, sim_len):
        """sim length → µm.  scale = sim units per µm (0.05 box = 50 µm → scale=0.001)."""
        return sim_len / self.scale if self.scale else sim_len


def _read_csv_dict(path):
    import csv
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def load_state(case_dir):
    case = Path(case_dir)
    a_rows = _read_csv_dict(case / 'atoms.csv')
    c_rows = _read_csv_dict(case / 'contacts.csv')
    atoms = {}
    for r in a_rows:
        atoms[int(float(r['id']))] = {
            'type': int(float(r['type'])),
            'x': float(r['x']), 'y': float(r['y']), 'z': float(r['z']),
            'radius': float(r['radius']),
        }
    contacts = []
    for r in c_rows:
        try:
            contacts.append({
                'id1': int(float(r['id1'])), 'id2': int(float(r['id2'])),
                'delta': float(r.get('delta', 0) or 0),
                'contact_area': float(r.get('contact_area', 0) or 0),
            })
        except (ValueError, KeyError):
            continue
    box_x = box_y = 0.05
    scale = 0.001                                   # default 50 µm box → 0.05 sim
    ip = case / 'input_params.json'
    if ip.exists():
        d = json.load(open(ip))
        box_x = float(d.get('box_x', box_x)); box_y = float(d.get('box_y', box_y))
        scale = float(d.get('scale', scale))
    poros, thick = _loaded_porosity_thickness(case)
    return DEMState(atoms, contacts, box_x, box_y, scale, poros, thick)


def _loaded_porosity_thickness(case):
    """Validated loaded porosity (fraction) + thickness (µm) from full_metrics.json.
    Tries several key spellings; returns (None, None) if absent (caller falls back
    to the geometric estimate)."""
    fm = Path(case) / 'full_metrics.json'
    if not fm.exists():
        return None, None
    d = json.load(open(fm))
    def _get(*keys):
        for k in keys:
            if k in d and d[k] not in (None, ''):
                return d[k]
        return None
    poros = _get('porosity', 'porosity_pct', 'porosity_percent', 'epsilon')
    thick = _get('thickness_um', 'electrode_thickness_um', 'thickness')
    if poros is not None and float(poros) > 1.0:   # stored as % → fraction
        poros = float(poros) / 100.0
    return (float(poros) if poros is not None else None,
            float(thick) if thick is not None else None)


# ─────────────────────────────────────────────────────────────────────────────
# DRIVERS — each returns (sep_change, new_radius)
#   sep_change[c]  = increase in centre-to-centre separation at contact c
#                    (= overlap REDUCTION = δ_old − δ_new).  >0 = particles part.
#   new_radius[id] = perturbed radius (springback: unchanged).
# ─────────────────────────────────────────────────────────────────────────────
def driver_springback(state: DEMState, k2k1=None, plasticity_depth=None):
    """hooke/hysteresis ELASTIC UNLOAD.  Recovered overlap per contact = δ/(k₂/k₁),
    with k₂/k₁ = coefficientMaxElasticStiffness (m6), PAIR-DEPENDENT.  (COR/m3 is
    viscous damping and does NOT enter a quasi-static unload.)

    plasticity_depth (m8, φf): if the loaded overlap δ is BELOW the plastic-depth
    onset (δ/r < φf → the contact never went plastic) it recovers FULLY (Δδ=δ);
    above it, the linear-hysteretic residual δ·(1−k₁/k₂) remains.  Adhesion (m7)
    is reported for context and makes this an UPPER bound (not applied as a fudge)."""
    k2k1 = k2k1 or REAL14['k2_over_k1']
    phi = plasticity_depth or REAL14['plasticity_depth']
    sep = np.zeros(len(state.contacts))
    for i, c in enumerate(state.contacts):
        d = c['delta']
        if d <= 0:
            continue
        a1 = state.atoms.get(c['id1']); a2 = state.atoms.get(c['id2'])
        t1 = a1.get('type') if a1 else None
        t2 = a2.get('type') if a2 else None
        ratio = _pair(k2k1, t1, t2, default=3.0)        # k₂/k₁ for this pair
        r_eff = 0.0
        if a1 and a2 and (a1['radius'] + a2['radius']) > 0:
            r_eff = a1['radius'] * a2['radius'] / (a1['radius'] + a2['radius'])   # reduced radius
        phi_f = _pair(phi, t1, t2, default=0.01)
        if r_eff > 0 and d < phi_f * r_eff:             # below plastic-depth onset → fully elastic
            sep[i] = d
        else:
            sep[i] = d / ratio                          # Δδ recovered = δ·(k₁/k₂)
    return sep, {aid: a['radius'] for aid, a in state.atoms.items()}


def driver_breathing(state: DEMState, dvol_by_type):
    """(De)lithiation radius change.  dvol_by_type = {atom_type: ΔV/V} (signed;
    delithiation/charge ≈ −0.02..−0.06 for NCM).  Δr/r = ΔV/(3V).  Contact overlap
    shifts by Δr_i+Δr_j; a contact with δ_new<0 is LOST (network topology change).
    Returns sep_change (separation INCREASE where the pair shrinks) + new radii.
    [STUB for Phase-B: wire NCM SOC-volume curve as dvol_by_type; the ENGINE below
     already handles the resulting strain + contact loss.]"""
    new_r = {}
    for aid, a in state.atoms.items():
        f = dvol_by_type.get(a['type'], 0.0)
        new_r[aid] = a['radius'] * (1.0 + f / 3.0)
    sep = np.zeros(len(state.contacts))
    for i, c in enumerate(state.contacts):
        dr = ((new_r[c['id1']] - state.atoms[c['id1']]['radius'])
              + (new_r[c['id2']] - state.atoms[c['id2']]['radius']))
        sep[i] = -dr                                    # shrink (dr<0) → separation grows
    return sep, new_r


# ─────────────────────────────────────────────────────────────────────────────
# DRIVER C — dilate: VGCF rod-network PROP-OPEN (Philipse rod jamming)
#   The packing half of the additive porosity effect (frame[5] DEM domain) that
#   --fibre-stiff (frozen AM) could not reach: the VGCF fibre network jams and
#   holds the bed open → porosity UP (Cho-2024 conflicting-roles direction).
# ─────────────────────────────────────────────────────────────────────────────
VGCF_L_UM = 10.0        # as-grown vapour-grown carbon fibre length (µm)
VGCF_D_UM = 0.15        # fibre diameter (150 nm)
PHILIPSE_C = 5.4        # Philipse 1996 random-contact rod jamming: φ_jam·(L/D) = 5.4
LOOSE_POROSITY = 0.40   # random-loose-packing cap (the bed cannot prop looser than this)


def _porosity_added_solid(p0, phi_add_bed, eps_zz):
    """Porosity after adding a solid fraction phi_add_bed (of the ORIGINAL bed volume)
    and expanding the bed uniaxially by eps_zz.  Original bed volume normalised to 1."""
    return 1.0 - ((1.0 - p0) + phi_add_bed) / (1.0 + eps_zz)


def driver_dilate(state: DEMState, vgcf_vol_pct_solid, L_um=VGCF_L_UM, D_um=VGCF_D_UM):
    """VGCF rod-network prop-open via Philipse rod jamming.  NON-CIRCULAR: the
    jamming onset comes from the fibre geometry (L/D), never from a target porosity.

      φ_jam = C_rod·D/L          (Philipse 1996; VGCF L/D≈67 → φ_jam≈8 vol% ≈ 4 wt%
                                  → low-wt% carbon has an OUTSIZED structural effect)
      φ_vgcf,bed = vol%_of_solid · (1−ε₀)
      x = φ_vgcf,bed / φ_jam      (jamming ratio; x≥1 = rods jam)
      p = 1 − exp(−x)            (prop gate: weak below jamming, →1 above)
      eps_zz = p · φ_vgcf,bed · A (bed expansion; A = excluded-volume amplification)

    A is BRACKETED and reported, NOT fudged to a target:
      • A=1  (lower)  — rods add their own volume as height (conservative prop).
      • A=1/φ_jam (upper) — full rod-network exclusion, capped at LOOSE_POROSITY.
    The exact A within the bracket = the AM/SE fillability of the open rod mesh, which
    only the DEM force balance (VGCF rods in LIGGGHTS) pins.  So this returns the
    jamming ONSET + DIRECTION + porosity BRACKET, with A=1 as the reported nominal."""
    p0 = state.porosity_loaded if state.porosity_loaded is not None else _geometric_porosity(state)
    phi_jam = PHILIPSE_C * D_um / L_um
    phi_bed = (vgcf_vol_pct_solid / 100.0) * (1.0 - p0)
    x = (phi_bed / phi_jam) if phi_jam > 0 else 0.0
    p = 1.0 - math.exp(-x)

    def _por(A):
        return _porosity_added_solid(p0, phi_bed, p * phi_bed * A)
    por_vf = _porosity_added_solid(p0, phi_bed, 0.0)          # volume-fill (no prop)
    por_lower = _por(1.0)                                     # A=1 conservative nominal
    por_upper = min(LOOSE_POROSITY, _por(1.0 / phi_jam) if phi_jam > 0 else LOOSE_POROSITY)
    return {
        'driver': f'dilate (VGCF rod-jamming, Philipse; L/D={L_um/D_um:.0f})',
        'vgcf_vol_pct_of_solid': round(vgcf_vol_pct_solid, 3),
        'phi_jam_vol_pct': round(100 * phi_jam, 2),
        'phi_vgcf_bed_vol_pct': round(100 * phi_bed, 2),
        'jamming_ratio_x': round(x, 3),
        'jammed': bool(x >= 1.0),
        'prop_gate_p': round(p, 3),
        'porosity_no_additive_pct': round(100 * p0, 3),
        'porosity_volume_fill_pct': round(100 * por_vf, 3),
        'porosity_dilate_nominal_pct': round(100 * por_lower, 3),      # A=1
        'porosity_dilate_bracket_pct': [round(100 * por_lower, 3), round(100 * por_upper, 3)],
        'eps_zz_nominal': round(p * phi_bed * 1.0, 5),
        'note': ('onset(Philipse)+direction are non-circular; the value WITHIN the bracket '
                 '= AM/SE fillability of the rod mesh → pinned only by DEM co-compaction. '
                 'porosity UP vs volume-fill; vs no-additive depends on A.'),
    }


# ─────────────────────────────────────────────────────────────────────────────
# ENGINE — confined-uniaxial macroscopic strain from contact-overlap changes
# ─────────────────────────────────────────────────────────────────────────────
def bestfit_uniaxial_ezz(state: DEMState, sep_change):
    """Least-squares axial strain ε_zz s.t.  ε_zz·b_z·n_z ≈ Δsep  over all contacts.
    DEM box = periodic x,y (fixed) + free z platen → lateral strain 0, uniaxial z.
    n = branch/|branch| (from atom centres).  ε_zz = Σ(b_z·n_z·Δsep)/Σ(b_z·n_z)²."""
    num = den = 0.0
    for i, c in enumerate(state.contacts):
        a1 = state.atoms.get(c['id1']); a2 = state.atoms.get(c['id2'])
        if a1 is None or a2 is None:
            continue
        bx, by, bz = a2['x'] - a1['x'], a2['y'] - a1['y'], a2['z'] - a1['z']
        L = math.sqrt(bx * bx + by * by + bz * bz)
        if L <= 0:
            continue
        w = bz * (bz / L)                               # b_z · n_z  = b_z²/L
        num += w * sep_change[i]
        den += w * w
    return (num / den) if den > 0 else 0.0


def porosity_after(state: DEMState, ezz):
    """Unloaded porosity from the VALIDATED loaded porosity + axial strain (solid
    conserved, thickness ×(1+ε_zz)).  Convention-consistent (reuses the case's
    reported porosity).  Falls back to a geometric estimate if unavailable."""
    p0 = state.porosity_loaded
    if p0 is None:
        p0 = _geometric_porosity(state)
    p1 = 1.0 - (1.0 - p0) / (1.0 + ezz)
    return p0, p1


def _geometric_porosity(state: DEMState):
    solid = sum((4.0 / 3.0) * math.pi * a['radius'] ** 3 for a in state.atoms.values())
    zt = [a['z'] + a['radius'] for a in state.atoms.values()]
    zb = [a['z'] - a['radius'] for a in state.atoms.values()]
    h = (max(zt) - min(zb)) if zt else 0.0
    vbox = state.box_x * state.box_y * h
    return max(0.0, 1.0 - solid / vbox) if vbox > 0 else 0.0


def contact_area_change(state: DEMState, sep_change, new_radius):
    """Report how the contact areas shrink under the perturbation, and how many
    contacts are LOST (δ_new ≤ 0).  Uses the Hertzian disc a² = R*·δ scaling so the
    ratio is model-light: A_new/A_old = δ_new/δ_old (same R*).  For a σ re-solve use
    --write-csv and rerun network_conductivity on the perturbed contacts."""
    lost = 0
    ratios = []
    for i, c in enumerate(state.contacts):
        d_old = c['delta']
        # δ_new = δ_old − Δsep   (springback: δ·(1−COR²));  breathing folds Δr into sep
        d_new = d_old - sep_change[i]
        if d_old > 0:
            if d_new <= 0:
                lost += 1
                ratios.append(0.0)
            else:
                ratios.append(d_new / d_old)
    return {
        'n_contacts': int(sum(1 for c in state.contacts if c['delta'] > 0)),
        'n_lost': int(lost),
        'mean_area_ratio': float(np.mean(ratios)) if ratios else 1.0,
    }


def apply_driver(state: DEMState, driver_name, dvol_by_type=None,
                 vgcf_vol_pct=None, vgcf_L=VGCF_L_UM, vgcf_D=VGCF_D_UM):
    if driver_name == 'dilate':                          # analytic (Philipse), not contact-based
        if vgcf_vol_pct is None:
            raise ValueError('dilate needs --vgcf-vol-pct (VGCF vol% of solid)')
        return driver_dilate(state, vgcf_vol_pct, vgcf_L, vgcf_D), None, None
    if driver_name == 'springback':
        sep, new_r = driver_springback(state)
        k = REAL14['k2_over_k1']
        drv = (f'springback (hooke/hysteresis unload; recovery δ/(k₂/k₁), m6: '
               f'AM-AM {1/k[(1,1)]:.2f}·δ / AM-SE {1/k[(1,3)]:.2f}·δ / SE-SE {1/k[(3,3)]:.2f}·δ; '
               f'adhesion m7 → upper bound)')
    elif driver_name == 'breathing':
        sep, new_r = driver_breathing(state, dvol_by_type or {})
        drv = f'breathing (ΔV/V={dvol_by_type})'
    else:
        raise ValueError(f'unknown driver: {driver_name}')
    ezz = bestfit_uniaxial_ezz(state, sep)
    p0, p1 = porosity_after(state, ezz)
    ca = contact_area_change(state, sep, new_r)
    dm = [c['delta'] for c in state.contacts if c['delta'] > 0]
    out = {
        'driver': drv,
        'n_atoms': len(state.atoms), 'n_contacts': len(state.contacts),
        'eps_zz': round(float(ezz), 6),
        'porosity_loaded_pct': round(100.0 * p0, 3),
        'porosity_perturbed_pct': round(100.0 * p1, 3),
        'delta_porosity_pp': round(100.0 * (p1 - p0), 3),
        'mean_overlap_sim': round(float(np.mean(dm)), 8) if dm else 0.0,
        'contacts': ca,
    }
    if state.thickness_um_loaded:
        out['thickness_loaded_um'] = round(state.thickness_um_loaded, 3)
        out['thickness_perturbed_um'] = round(state.thickness_um_loaded * (1 + ezz), 3)
    return out, sep, new_r


def write_perturbed_csvs(state: DEMState, sep_change, new_radius, ezz, out_dir):
    """Perturbed atoms.csv (z affine-stretched by ε_zz about the floor; radii from
    the driver) + contacts.csv (δ,contact_area rescaled) → feed network_conductivity
    for the perturbed σ.  First-order (affine z) position update — small-strain."""
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    zb = min(a['z'] - a['radius'] for a in state.atoms.values())
    import csv
    with open(out / 'atoms.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['id', 'type', 'x', 'y', 'z', 'radius'])
        for aid, a in state.atoms.items():
            z = zb + (a['z'] - zb) * (1.0 + ezz)
            w.writerow([aid, a['type'], a['x'], a['y'], z, new_radius[aid]])
    with open(out / 'contacts.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id1', 'id2', 'fn_x', 'fn_y', 'fn_z', 'ft_x', 'ft_y', 'ft_z',
                    'contact_area', 'delta'])
        for i, c in enumerate(state.contacts):
            d_new = max(0.0, c['delta'] - sep_change[i])
            a_ratio = (d_new / c['delta']) if c['delta'] > 0 else 0.0
            w.writerow([c['id1'], c['id2'], 0, 0, 0, 0, 0, 0,
                        c['contact_area'] * a_ratio, d_new])
    return str(out)


# ─────────────────────────────────────────────────────────────────────────────
# SELF-TEST — synthetic packings with analytically-known springback (no case data)
# ─────────────────────────────────────────────────────────────────────────────
def _mk_state(atoms, contacts, box=1.0, scale=1.0, poros=0.20, thick=10.0):
    return DEMState(atoms, contacts, box, box, scale, poros, thick)


def selftest():
    R, d = 1.0, 0.10
    L = 2 * R - d                                      # branch length
    r_eff = R * R / (2 * R)                            # reduced radius = R/2 = 0.5

    def chain(t):
        atoms = {1: {'type': t, 'x': 0, 'y': 0, 'z': R, 'radius': R},
                 2: {'type': t, 'x': 0, 'y': 0, 'z': 3 * R - d, 'radius': R},
                 3: {'type': t, 'x': 0, 'y': 0, 'z': 5 * R - 2 * d, 'radius': R}}
        contacts = [{'id1': 1, 'id2': 2, 'delta': d, 'contact_area': 1.0},
                    {'id1': 2, 'id2': 3, 'delta': d, 'contact_area': 1.0}]
        return _mk_state(atoms, contacts)

    # (1) AM chain (type 1): k₂/k₁=1.5 → recover δ/1.5.  d=0.10 > φf·r_eff=0.05·0.5 → plastic regime.
    st = chain(1)
    sep, new_r = driver_springback(st)
    ezz = bestfit_uniaxial_ezz(st, sep)
    assert abs(ezz - (d / 1.5) / L) < 1e-9, (ezz, (d / 1.5) / L)
    ca = contact_area_change(st, sep, new_r)
    assert ca['n_lost'] == 0 and abs(ca['mean_area_ratio'] - (1 - 1 / 1.5)) < 1e-9, ca
    print(f"  [1] AM chain (m6=1.5): ε_zz={ezz:.6f}==(δ/1.5)/L ✓  residual area {ca['mean_area_ratio']:.3f} "
          f"(=1−1/1.5, AM loses 67% overlap) ✓")

    # (2) SE chain (type 3): k₂/k₁=5.0 → recover δ/5 (SE barely springs back, stays compacted).
    st3 = chain(3)
    sep3, nr3 = driver_springback(st3)
    ezz3 = bestfit_uniaxial_ezz(st3, sep3)
    ca3 = contact_area_change(st3, sep3, nr3)
    assert abs(ezz3 - (d / 5.0) / L) < 1e-9, (ezz3, (d / 5.0) / L)
    assert ezz3 < ezz, "SE must spring back LESS than AM"
    print(f"  [2] SE chain (m6=5.0): ε_zz={ezz3:.6f}==(δ/5)/L ✓  residual area {ca3['mean_area_ratio']:.3f} "
          f"(SE retains 80%, springs back 4× less than AM) ✓")

    # (3) below plastic-depth onset (small δ) → FULLY elastic recovery (Δδ=δ).
    small = 0.02                                       # AM: φf·r_eff = 0.05·0.5 = 0.025 > 0.02 → elastic
    st_e = _mk_state({1: {'type': 1, 'x': 0, 'y': 0, 'z': R, 'radius': R},
                      2: {'type': 1, 'x': 0, 'y': 0, 'z': 3 * R - small, 'radius': R}},
                     [{'id1': 1, 'id2': 2, 'delta': small, 'contact_area': 1.0}])
    sep_e, _ = driver_springback(st_e)
    assert abs(sep_e[0] - small) < 1e-12, sep_e     # full recovery
    print("  [3] δ below φf·r_eff (m8 plasticity depth): FULL elastic recovery Δδ=δ ✓")

    # (4) horizontal contact contributes 0 to uniaxial ε_zz.
    st_h = _mk_state({1: {'type': 3, 'x': 0, 'y': 0, 'z': R, 'radius': R},
                      2: {'type': 3, 'x': 2 * R - d, 'y': 0, 'z': R, 'radius': R}},
                     [{'id1': 1, 'id2': 2, 'delta': d, 'contact_area': 1.0}])
    assert abs(bestfit_uniaxial_ezz(st_h, driver_springback(st_h)[0])) < 1e-12
    print("  [4] horizontal contact: ε_zz=0 (only z-contacts spring the platen) ✓")

    # (5) breathing: delithiation shrink (ΔV/V=−6%) parts contacts → porosity ↑.
    st5 = chain(1)
    sepb, nrb = driver_breathing(st5, {1: -0.06})
    ezzb = bestfit_uniaxial_ezz(st5, sepb)
    _, p1b = porosity_after(st5, ezzb)
    assert ezzb > 0 and p1b > st5.porosity_loaded, (ezzb, p1b)
    print(f"  [5] breathing ΔV/V=−6%: ε_zz={ezzb:.5f}>0, porosity {100*st5.porosity_loaded:.1f}→"
          f"{100*p1b:.2f}% ✓")

    # (6) dilate: VGCF rod-jamming prop (Philipse).  φ_jam=5.4·0.15/10=0.081; real_4-like ε₀=0.1428,
    #     4 wt% = 8.06 vol% of solid → x≈0.85 (just below jamming); prop lifts porosity ABOVE volume-fill.
    st6 = _mk_state({1: {'type': 1, 'x': 0, 'y': 0, 'z': 1.0, 'radius': 1.0}}, [], poros=0.1428)
    dd = driver_dilate(st6, vgcf_vol_pct_solid=8.06, L_um=10.0, D_um=0.15)
    assert abs(dd['phi_jam_vol_pct'] - 8.1) < 0.2, dd
    assert 0.80 < dd['jamming_ratio_x'] < 0.90 and not dd['jammed'], dd
    assert dd['porosity_dilate_nominal_pct'] > dd['porosity_volume_fill_pct'], dd
    lo, hi = dd['porosity_dilate_bracket_pct']
    assert lo <= dd['porosity_dilate_nominal_pct'] <= hi + 1e-9 and hi <= 100 * LOOSE_POROSITY + 1e-9, dd
    print(f"  [6] dilate VGCF 4wt% (Philipse L/D=67): φ_jam={dd['phi_jam_vol_pct']}vol% x={dd['jamming_ratio_x']} "
          f"→ vol-fill {dd['porosity_volume_fill_pct']}% → dilate {dd['porosity_dilate_nominal_pct']}% "
          f"bracket{dd['porosity_dilate_bracket_pct']} ✓")

    print("SELF-TEST PASSED ✓")
    return True


# ─────────────────────────────────────────────────────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--case', help='case dir with atoms.csv + contacts.csv (+ full_metrics.json)')
    ap.add_argument('--driver', default='springback', choices=['springback', 'breathing', 'dilate'])
    ap.add_argument('--vgcf-vol-pct', type=float, default=None,
                    help='dilate: VGCF vol%% of solid (from the campaign; e.g. 4wt%% → 8.06).')
    ap.add_argument('--vgcf-l', type=float, default=VGCF_L_UM, help='dilate: VGCF fibre length µm (10).')
    ap.add_argument('--vgcf-d', type=float, default=VGCF_D_UM, help='dilate: VGCF fibre diameter µm (0.15).')
    ap.add_argument('--cor', type=float, default=DEFAULT_COR,
                    help=f'coefficientRestitution (m3, production {DEFAULT_COR}) — the VISCOUS damping; '
                         f'informational only.  Springback uses coefficientMaxElasticStiffness (m6 = k₂/k₁), '
                         f'not COR.')
    ap.add_argument('--dvol', default='',
                    help='breathing ΔV/V per atom type, e.g. "1:-0.04,2:-0.02" (charge=shrink)')
    ap.add_argument('--write-csv', default='', help='write perturbed atoms.csv+contacts.csv here')
    ap.add_argument('--out', default='', help='write the summary JSON here')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return 0 if selftest() else 1
    if not a.case:
        ap.error('need --case (or --selftest)')

    st = load_state(a.case)
    dvol = None
    if a.dvol:
        dvol = {int(k): float(v) for k, v in (kv.split(':') for kv in a.dvol.split(','))}
    summary, sep, new_r = apply_driver(st, a.driver, dvol_by_type=dvol,
                                       vgcf_vol_pct=a.vgcf_vol_pct, vgcf_L=a.vgcf_l, vgcf_D=a.vgcf_d)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if a.write_csv and sep is not None:
        p = write_perturbed_csvs(st, sep, new_r, summary['eps_zz'], a.write_csv)
        print(f"  wrote perturbed atoms.csv + contacts.csv → {p}  "
              f"(rerun scripts/network_conductivity.py there for the perturbed σ)")
    if a.out:
        json.dump(summary, open(a.out, 'w'), indent=2, ensure_ascii=False)
        print(f"  saved summary → {a.out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
