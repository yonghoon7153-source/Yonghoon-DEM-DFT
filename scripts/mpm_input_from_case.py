#!/usr/bin/env python3
"""DEM case → MPM input package (the webapp '[MPM input 변환]' button calls this).

From a webapp case's results dir (atoms.csv + full_metrics.json) it writes, into
<out>/ , the ready-to-run MPM input:
  • am_scaffold.csv  (type,x,y,z,r — AM_P=1/AM_S=2, the fixed skeleton)
  • se_scaffold.csv  (type,x,y,z,r — SE=3, the real seed positions)
  • run_mpm.sh       (mpm3d_compaction --se-dump … + mpm_webapp_payload …, with the
                      case's DEM porosity wired into --target-porosity)
  • mpm_input.json   (provenance: case id, n_AM, n_SE, DEM porosity/thickness)
Run run_mpm.sh on a GPU box; it produces mpm_metrics.json + mpm_payload.json, which
you upload back to the case (→ results/<case>/mpm_payload.json) for the viewer/compare.

  python3 scripts/mpm_input_from_case.py --results webapp/results/<case_id> --out /tmp/mpm_in
"""
import argparse
import csv
import json
import math
import os
import re


def _find_atom_dump(results_dir):
    """The FINAL-state raw LIGGGHTS atom dump (highest timestep) in the case dir, if present.
    The webapp keeps atom_<step>.liggghts (app.detect_mode reads it for type count); it carries the
    per-atom σ_zz virial (c_strs[3]) the analyzed atoms.csv strips → lets us get the REAL f_AM."""
    cands = []
    try:
        for f in os.listdir(results_dir):
            if f.startswith('atom') and f.endswith('.liggghts'):
                m = re.search(r'(\d+)', f)
                cands.append((int(m.group(1)) if m else -1, os.path.join(results_dir, f)))
    except OSError:
        return None
    return max(cands)[1] if cands else None      # highest timestep = the compacted 300-MPa state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', required=True, help='case results dir (has atoms.csv, full_metrics.json)')
    ap.add_argument('--case', default='', help='case id (provenance)')
    ap.add_argument('--out', required=True, help='output dir for the MPM input package')
    ap.add_argument('--type-map', default='', help='LIGGGHTS type map e.g. "1:AM_P,2:AM_S,3:SE" or '
                    '"1:AM_P,2:SE" — SE is NOT always type 3 (a no-AM_S case is type 2); parsed for SE vs AM')
    ap.add_argument('--max-points', type=float, default=90e6,
                    help='MPM point budget: auto-pick n_grid so est. points <= this (default 90M ~12GB, '
                         'fast frames).  The 209k-SE / 301M-pt case at n_grid 384 was too heavy and kept '
                         'dying — this caps it.  Raise for more SE resolution (slower/heavier).')
    ap.add_argument('--n-grid', type=int, default=0,
                    help='explicit lateral n_grid (0 = auto from RVE box + --max-points).')
    ap.add_argument('--add-recipe', default='', help='conductive-additive recipe baked into run_mpm.sh, e.g. '
                    '"AM:SE:VGCF=72:27:1" or "AM:SE:VGCF:PTFE=80:18:1:1" (Stage-1 carbon).  Empty = no carbon.')
    ap.add_argument('--add-l-cv', type=float, default=0.4, help='fibre length variation baked into run_mpm.sh.')
    ap.add_argument('--mixing', default='thinky', choices=['ballmill', 'thinky', 'handmix'],
                    help='Super P dispersion baked into run_mpm.sh (thinky = lit dry-process coating).')
    ap.add_argument('--no-dilate', action='store_true',
                    help='skip the VGCF-recipe --dilate-z auto-bake → regenerate the UN-dilated '
                         'bracket-floor zip (volume-fill/strut lower bound) without hand-editing run_mpm.sh.')
    ap.add_argument('--fibre-stiff', action='store_true',
                    help='force --fibre-stiff even for a NON-VGCF recipe.  For any VGCF recipe it is now '
                         'AUTO-baked into run_mpm.sh (VGCF as a LOAD-BEARING rigid strut = the physical model, '
                         'Cho-2024 direction), so you never need this flag for VGCF.  See mpm3d_compaction.py.')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    atoms = os.path.join(a.results, 'atoms.csv')
    if not os.path.exists(atoms):
        raise SystemExit(f'no atoms.csv in {a.results}')
    fm = {}
    fmp = os.path.join(a.results, 'full_metrics.json')
    if os.path.exists(fmp):
        fm = json.load(open(fmp))
    ip = {}
    ipp = os.path.join(a.results, 'input_params.json')
    if os.path.exists(ipp):
        ip = json.load(open(ipp))
    # per-case pressing pressure → MPM --target-gpa (material E_SE/σ_y stay the CALIBRATED
    # MPM champion, NOT read from the DEM — frame[4]: MPM is calibrated independently).
    if ip.get('target_pressure_MPa') is not None:
        press_gpa = float(ip['target_pressure_MPa']) / 1000.0
    elif ip.get('target_press_sim') is not None:
        tp = float(ip['target_press_sim'])
        press_gpa = tp if tp < 10 else tp / 1000.0          # sim 0.30 = 0.30 GPa = 300 MPa
    else:
        press_gpa = 0.30
    press_gpa = round(press_gpa, 4)

    # which atom types are SE?  from the type_map — SE is NOT always type 3 (a no-AM_S case is
    # "1:AM_P,2:SE").  Fallback to the legacy type-3 convention if no map.
    se_types = set()
    for tok in (a.type_map or '').split(','):
        if ':' in tok:
            tid, lab = tok.split(':', 1)
            if 'SE' in lab.upper():
                try:
                    se_types.add(int(tid))
                except ValueError:
                    pass
    if not se_types:
        se_types = {3}

    # split atoms.csv (id,type,x,y,z,radius; LIGGGHTS box units): SE by the type map, AM = the rest
    am_raw, se_rows = [], []
    with open(atoms) as f:
        rd = csv.DictReader(f)
        cols = {c.lower(): c for c in rd.fieldnames}
        tk = cols.get('type'); xk = cols.get('x'); yk = cols.get('y'); zk = cols.get('z')
        rk = cols.get('radius') or cols.get('r')
        for row in rd:
            t = int(float(row[tk])); rec = [t, row[xk], row[yk], row[zk], row[rk]]
            (se_rows if t in se_types else am_raw).append(rec)
    if not se_rows:
        raise SystemExit(f'no SE atoms (se_types={sorted(se_types)}, type_map={a.type_map!r}) — '
                         f'check the type map / atom types in atoms.csv')

    # AM_P (large) vs AM_S (small) by RADIUS — the physical distinction (AM_P polycrystalline
    # ~6µm / AM_S single-crystal ~2µm), robust to the type-number convention.  Bimodal → split
    # at the size-range geometric midpoint; single size → all AM_P (type 1).
    am_rows = []
    if am_raw:
        radii = [float(r[4]) for r in am_raw]
        rmin, rmax = min(radii), max(radii)
        thr = (rmin * rmax) ** 0.5 if rmax / max(rmin, 1e-12) > 1.4 else -1.0
        for rec in am_raw:
            rec[0] = 1 if (thr < 0 or float(rec[4]) >= thr) else 2          # AM_P=1 / AM_S=2 by size
            am_rows.append(rec)

    def write_csv(path, rows, note):
        with open(path, 'w', newline='') as f:
            f.write(f'# type,x,y,z,r  # {note}\n')
            w = csv.writer(f)
            for r in rows:
                w.writerow([r[0], f'{float(r[1]):.6f}', f'{float(r[2]):.6f}',
                            f'{float(r[3]):.6f}', f'{float(r[4]):.6f}'])
    write_csv(os.path.join(a.out, 'am_scaffold.csv'), am_rows,
              f'AM scaffold (AM_P=1,AM_S=2) — case {a.case}')
    write_csv(os.path.join(a.out, 'se_scaffold.csv'), se_rows,
              f'SE seed positions (col 0 = original atom type; MPM uses x,y,z,r) — case {a.case}')

    poro = fm.get('porosity')
    tgt = round(float(poro) / 100.0, 4) if poro is not None else 0.16
    # PRODUCTION = pure scaffold + hold; NO injected conditional (FINAL LOGIC, 2026-06-27).
    # The wallP conditional — --am-load-frac (Love-Weber f_AM skeleton-spring) + --floor-porosity
    # (a DEM−5 HARD porosity clamp) — was a CORNER patch that stopped the SE-poor/mono-large
    # over-compression by CLAMPING porosity at DEM−margin.  But a porosity clamp MASKS the true
    # DEM↔MPM gap, and that gap IS the validity certificate (§13/§16: regime-gate, NOT a clamp).
    # Final logic: run the MPM PURE (SE bears the load → plastic void-fill).  In-envelope cases
    # reproduce experiment (real_14 15.93 ≈ DEM 15.6 ≈ FIB-SEM 9–19 %); the out-of-envelope corner
    # (SE-sub-functional + thin = not a manufacturable cell, §16-lit) HONESTLY over-compresses, and
    # the un-clamped |DEM − MPM| gap flags it (large gap → trust DEM, not the MPM number).  The
    # conditional + --se-am-drag/--am-jam survive as OPT-IN flags in mpm3d_compaction.py for
    # experiments; production never injects them.  (Dead-patch history: troubleshooting §15/§16 + git.)
    case = a.case or os.path.basename(a.results.rstrip('/'))
    # lateral RVE box (LIGGGHTS units) → MPM scl = WIDTH/lateral_box and adaptive n_grid.  Prefer
    # input_params box_x; else the atom lateral extent (periodic box ≈ max x,y).  Thick films are
    # TALLER than this lateral, so MPM auto-extends the z grid (non-cubic) to fit — see run script.
    box_x = ip.get('box_x') or ip.get('box_x_sim')
    if not box_x:
        allxy = [float(r[1]) for r in (am_rows + se_rows)] + [float(r[2]) for r in (am_rows + se_rows)]
        box_x = max(allxy) if allxy else 0.05
    box_x = round(float(box_x), 6)
    # adaptive lateral resolution: keep SE ≈ 3.5 cells (real_14 0.05→384) so the calibration
    # transfers; but CAP by a POINT BUDGET so big-SE cases stay GPU-tractable AND finish (the
    # 209k-SE case at n_grid 384 = 301M pts kept dying/crawling).  est. points = PPC·V_SE·(n/box)³.
    V_SE = sum((4.0 / 3.0) * math.pi * float(r[4]) ** 3 for r in se_rows)   # total SE volume (box³ units)
    PPC = 8                                                     # MPM particles per cell (2×2×2)
    n_design = int(round(384 * box_x / 0.05))                  # resolution-matched to real_14
    if a.n_grid > 0:
        n_grid_mpm = max(64, a.n_grid)                         # explicit override
    elif V_SE > 0:
        n_budget = int(box_x * (a.max_points / (PPC * V_SE)) ** (1.0 / 3.0))
        n_grid_mpm = max(128, min(384, n_design, n_budget))
    else:
        n_grid_mpm = max(128, min(384, n_design))
    est_pts = int(PPC * V_SE * (n_grid_mpm / box_x) ** 3) if V_SE > 0 else 0
    # per-case SE stiffness — physically-faithful mapping (CLAUDE.md CORRECTION 1):
    # the DEM E_eff softening (1.35 GPa × the case ratio) is the GRANULAR-REARRANGEMENT
    # proxy = the SHEAR part ONLY.  So scale the MPM shear modulus μ by the case ratio
    # while HOLDING the bulk modulus K at the real-LPSC champion value (K=25.5 GPa, what
    # ν=0.49 gives at E=1.53), then back out (E, ν) for the MPM.  Normal range (×0.5–×1.5)
    # ≈ proportional-E with ν≈0.49 (×1.0 → exactly E=1.53/ν=0.49); extreme softening keeps
    # K ≫ press → no volumetric over-crush (proportional-E would let K fall toward press).
    # MPM lame(): μ=E/(2(1+ν)), K=E/(3(1-2ν)) → E=9Kμ/(3K+μ), ν=(3K-2μ)/(2(3K+μ)).
    e_se_dem = fm.get('e_se_eff_gpa')
    E_STD_DEM, E_CHAMP, NU_CHAMP = 1.35, 1.53, 0.49
    K_CHAMP = E_CHAMP / (3.0 * (1.0 - 2.0 * NU_CHAMP))      # 25.5 GPa (real LPSC bulk)
    MU_CHAMP = E_CHAMP / (2.0 * (1.0 + NU_CHAMP))           # 0.513 GPa (soft shear proxy)
    se_ratio = float(e_se_dem) / E_STD_DEM if e_se_dem else 1.0
    mu_se_mpm = MU_CHAMP * se_ratio                         # shear scales with the granular proxy
    if e_se_dem:
        e_se_mpm = round(9.0 * K_CHAMP * mu_se_mpm / (3.0 * K_CHAMP + mu_se_mpm), 4)
        nu_se_mpm = round((3.0 * K_CHAMP - 2.0 * mu_se_mpm) /
                          (2.0 * (3.0 * K_CHAMP + mu_se_mpm)), 5)  # 5 dp: K stable near ν→0.5
    else:
        e_se_mpm, nu_se_mpm = E_CHAMP, NU_CHAMP
    prov = {'case': case, 'n_AM': len(am_rows), 'n_SE': len(se_rows),
            'dem_porosity_pct': poro, 'dem_thickness_um': fm.get('thickness_um'),
            'dem_coverage_AM_P_mean': fm.get('coverage_AM_P_mean'),
            'dem_coverage_AM_S_mean': fm.get('coverage_AM_S_mean'),
            'dem_e_se_eff_gpa': e_se_dem, 'se_ratio_vs_1p35': round(se_ratio, 4),
            'mpm_e_se_gpa': e_se_mpm, 'mpm_nu_se': nu_se_mpm,
            'mpm_K_se_gpa': round(K_CHAMP, 2), 'mpm_mu_se_gpa': round(mu_se_mpm, 4),
            'press_gpa': press_gpa, 'target_porosity': tgt,
            'lateral_box': box_x, 'mpm_n_grid': n_grid_mpm, 'mpm_est_points': est_pts}
    json.dump(prov, open(os.path.join(a.out, 'mpm_input.json'), 'w'), indent=2)

    # Stage-1 carbon: append the additive flags to the compaction step if a recipe was given,
    # and carry the per-point phase into the payload (so the 도전재 3D viewer can colour the carbon)
    # A3 binder physics baked EXPLICITLY (non-monotonic PTFE cohesion: peak at --binder-opt-wt,
    # decays for over-application). These equal the mpm3d_compaction defaults, but writing them
    # makes the run self-documenting that A3 is applied. Pressure-regime propping (yield at
    # σ_y=0.05 GPa) is automatic from the PTFE material vs --target-gpa.
    # VGCF present → bake the SEM-consistent AM-position-dependent buckle morphology by default (the
    # electrode-faithful VGCF shape; fibre_rod_mpm_design §SOLUTION).  Volume/porosity-neutral, so it never
    # changes the porosity result; it just makes the seeded fibres wavy like real VGCF instead of straight.
    _buckle = '--fibre-buckle ' if 'VGCF' in a.add_recipe.upper() else ''
    # --fibre-stiff AUTO-baked for any VGCF recipe (like --fibre-buckle): real graphite VGCF (E~200 GPa,
    # σ_y ≫ 0.3 GPa press) is a LOAD-BEARING rigid strut that RESISTS compaction, NOT a passive void-
    # filler → this is the physical VGCF model (Cho-2024 conflicting-roles direction; see
    # docs/fibre_rod_mpm_design.md §COMPACTION-RESISTANCE).  So every VGCF run is strut by default (no
    # manual flag / sed needed); the --fibre-stiff CLI flag still force-enables it for a non-VGCF recipe.
    _stiff = '--fibre-stiff ' if ('VGCF' in a.add_recipe.upper() or a.fibre_stiff) else ''
    # --fibre-align AUTO for any FIBRE (VGCF or PTFE): press-induced IN-PLANE alignment.  λ_z = axial stretch
    # of the bed under the uniaxial compaction the fibres underwent WITH it = (1−ε_loose)/(1−ε_DEM),
    # ε_loose≈0.44 (random loose packing pre-press), ε_DEM = this case's compacted porosity → non-circular
    # (from the compaction ratio), morphology-faithful (real 300-MPa fibres tilt in-plane).  PTFE fibrils
    # tilt in-plane under the same uniaxial press as VGCF; SuperP (0D, no long axis) is correctly excluded.
    _eps_dem = (float(poro) / 100.0) if poro else 0.15
    _rc = a.add_recipe.upper()
    # --dilate-z AUTO for STIFF-fibre (VGCF) recipes: bed prop-open the frozen-AM MPM cannot produce
    # emergently (skeleton rearrangement = granular/DEM-class).  λ_dz = (1+φ_VGCF)·(1−ε_DEM)/(1−ε_real);
    # ε_real = ε_DEM + Δε_cho(w) interpolated from docs/data/vgcf_dilate_cho_calibrated.csv — the ONE
    # in-repo Cho-2024-anchored curve (dem_perturbation.py driver C: Balberg-percolation-gated,
    # A_cho=1.568; SUPERSEDES the first-cut linear 0.5pp/wt% which disagreed with it below 2wt% —
    # the curve is NET vs no-additive, negative below rod percolation where volume-fill dominates).
    # ⚠ anchor caveats carry over (campaign doc): Cho = 433 MPa·other composition, TWO points (0/2wt%)
    # → slope ±~50%; onset constant spans [0.7 Balberg … 5.4 Philipse]·D/L.  Soft additives (PTFE/
    # SuperP, σ_y<press) flow into pores instead of propping → EXCLUDED.  Thickness/porosity respond
    # BY CONSTRUCTION; coverage/network/SE-strain respond EMERGENTLY on the dilated bed (z-affine =
    # die-press global mode; local non-affine rearrangement stays DEM territory).  --no-dilate
    # regenerates the un-dilated bracket-floor zip (no sed needed).
    _dilate = ''; _dz = 1.0; _eps_real = _eps_dem
    _wts = {}
    if a.add_recipe:
        import sys as _sys                                              # robust regardless of caller cwd
        _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            import additives as _adds                                   # canonical recipe parser + DENS
            _parse, _awt, _DENS = _adds.parse_recipe, _adds.additive_wt, _adds.DENS
        except ImportError as _e:                                       # numpy-less env → verbatim inline
            print(f'⚠ additives import failed ({_e}) → inline parse/DENS copies (keep in sync w/ additives.py)')
            def _parse(s):                                              # = additives.parse_recipe verbatim
                keys, vals = s.split('=')
                keys = keys.split(':'); vals = [float(v) for v in vals.split(':')]
                return dict(zip(keys, vals))
            def _awt(wt):                                               # = additives.additive_wt verbatim
                return {k: float(wt[k]) for k in ('VGCF', 'SuperP', 'PTFE', 'SDCP') if wt.get(k, 0) > 0}
            _DENS = {'AM': 4.80, 'SE': 2.00, 'VGCF': 2.00}              # = additives.DENS subset
        try:
            _wts = _awt(_parse(a.add_recipe))                           # {'VGCF':1.0,...} — AM/SE ignored
        except Exception as _e:
            raise SystemExit(f'--add-recipe {a.add_recipe!r} unparseable ({_e}) — '
                             f"expected 'VGCF:PTFE=1:1' / 'PTFE=0.5' / 'AM:SE:VGCF=72:27:1'")
    _wv = float(_wts.get('VGCF', 0.0))
    if _wv > 0.0 and poro and not a.no_dilate:
        _wt_tot = sum(_wts.values())                                    # additive wt% only (AM/SE excluded)
        _r3 = lambda rows: sum(float(r[4]) ** 3 for r in rows)          # Σr³ ∝ volume (4π/3 cancels)
        _v_am, _v_se = _r3(am_rows), _r3(se_rows)
        _m_base = _v_am * _DENS['AM'] + _v_se * _DENS['SE']             # single-source densities (additives.DENS)
        _v_vgcf = (_m_base * (_wv / 100.0) / max(1.0 - _wt_tot / 100.0, 1e-6)) / _DENS['VGCF']
        _phi = _v_vgcf / max(_v_am + _v_se, 1e-12)                      # VGCF vol / base-solid vol
        _curve = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'docs', 'data', 'vgcf_dilate_cho_calibrated.csv')
        _pts = []                                                       # (wt%, Δε_pp) net-vs-no-additive
        with open(_curve) as _f:
            for _row in csv.reader(_f):
                try:
                    _pts.append((float(_row[0]), float(_row[3])))
                except (ValueError, IndexError):
                    continue                                            # header/comment lines
        _pts.sort()
        _w = min(max(_wv, _pts[0][0]), _pts[-1][0])                     # clamp to the calibrated range
        _dpp = _pts[-1][1]
        for (_w0, _d0), (_w1, _d1) in zip(_pts, _pts[1:]):
            if _w0 <= _w <= _w1:
                _dpp = _d0 + (_d1 - _d0) * (_w - _w0) / max(_w1 - _w0, 1e-9)
                break
        _eps_real = min(max(_eps_dem + _dpp / 100.0, 0.01), 0.60)
        _dz = (1.0 + _phi) * (1.0 - _eps_dem) / max(1.0 - _eps_real, 1e-6)
        if not (1.0 <= _dz <= 1.35):                                    # sanity gate: a λ outside this is a
            print(f'⚠ dilate-z λ={_dz:.4f} outside [1.0,1.35] — clamped; check recipe/porosity inputs')
            _dz = min(max(_dz, 1.0), 1.35)                              # parse/input bug, not physics
        _dz = round(_dz, 4)
        _dilate = f'--dilate-z {_dz} ' if _dz > 1.0 else ''
    # --fibre-align AUTO for any FIBRE (VGCF or PTFE): press-induced IN-PLANE alignment.  λ_z = axial
    # stretch of the bed under the uniaxial compaction the fibres underwent WITH it = (1−ε_loose)/(1−ε),
    # ε_loose≈0.44.  ε = ε_real when dilation is baked (the dilated bed's own compaction endpoint —
    # keeps the two auto-flags on ONE porosity narrative), else the case ε_DEM.  PTFE fibrils tilt
    # in-plane under the same uniaxial press as VGCF; SuperP (0D, no long axis) is correctly excluded.
    _eps_align = _eps_real if _dilate else _eps_dem
    _lam_z = round(min(1.0, (1.0 - 0.44) / max(1.0 - _eps_align, 1e-6)), 3)
    _align = f'--fibre-align {_lam_z} ' if ('VGCF' in _rc or 'PTFE' in _rc) else ''
    # strut vs dilation: λ_dz already encodes the FULL Cho prop-open; the rigid strut is a partial
    # mechanistic model of the SAME mechanism (+0.75pp @4wt% on the frozen bed) → stacking them
    # double-counts.  Dilation SUPERSEDES the auto-strut; --fibre-stiff CLI still force-enables.
    if _dilate and not a.fibre_stiff:
        _stiff = ''
    # step-2 payload must live on the SAME frame as the dilated run: pass λ_dz through (AM + seed-SE
    # rebuilt dilated in the viz) and target the dilated ε_real — else voxelize pins the void back to
    # ε_DEM exactly and the viewer/coverage compare a dilated SE cloud against un-dilated AM spheres.
    tgt_pay = round(_eps_real, 4) if _dilate else tgt
    pay_dilate = f' --dilate-z {_dz}' if _dilate else ''
    add_flags = (f' \\\n  --add-recipe "{a.add_recipe}" --add-l-cv {a.add_l_cv} --mixing {a.mixing} '
                 f'--coh-ptfe 0.10 --binder-opt-wt 1.5 {_buckle}{_stiff}{_align}{_dilate}'
                 f'--save-phase phase.npy --save-fibre fibre.npy --save-fibre-dia fibre_dia.npy'
                 if a.add_recipe else '')
    pay_phase = ' --phase phase.npy --fibre fibre.npy --fibre-dia fibre_dia.npy' if a.add_recipe else ''
    # run script: edit paths/GPU as needed, then run on a GPU box
    run = f"""#!/usr/bin/env bash
# MPM run for case {case} — generated by mpm_input_from_case.py
# SE (K-fixed): E_SE={e_se_mpm} GPa ν={nu_se_mpm}  (bulk K={prov['mpm_K_se_gpa']} GPa real-LPSC,
#   shear μ={prov['mpm_mu_se_gpa']} GPa = ×{prov['se_ratio_vs_1p35']} champion; from DEM E_eff {e_se_dem} GPa),
#   press {press_gpa} GPa.  n_grid {n_grid_mpm} → est ~{est_pts / 1e6:.0f}M points (budget {a.max_points / 1e6:.0f}M)
#   — kept tractable so the run FINISHES.  More SE resolution: regenerate with a higher
#   --max-points (heavier/slower) or edit --n-grid below.  If it OOMs, lower --n-grid / raise --gpu-mem.
set -uo pipefail
# ── one GPU = one run: refuse if an MPM compaction is already active.  Every run writes the SAME
#    se_dump.npy / phase.npy / mpm_metrics.json, so two at once CLOBBER each other (mixed outputs).
#    Checked in the foreground (before detach) so the refusal is immediate.  Override: MPM_FORCE=1 ──
if [ -z "${{MPM_DETACHED:-}}" ] && [ -z "${{MPM_FORCE:-}}" ] && pgrep -f 'scripts/mpm3d_compaction.py' >/dev/null 2>&1; then
  echo "[run_mpm] ABORT — an MPM run is already active (pgrep mpm3d_compaction).  one GPU = one run."
  echo "          wait for FINAL / 'kill <PID>' first, or 'MPM_FORCE=1 bash run_mpm.sh' to override."
  exit 1
fi
# ── self-detach: an SSH drop must NOT kill the run (the foreground run kept dying on disconnect). ──
if [ -z "${{MPM_DETACHED:-}}" ]; then
  export MPM_DETACHED=1
  log="mpm_run_$(date +%Y%m%d_%H%M%S).log"
  echo "→ detached — survives SSH drop.  log: $log"
  setsid nohup bash "$0" "$@" >"$log" 2>&1 </dev/null &
  echo "   PID $!     follow: tail -f $log     stop: kill $!"
  exit 0
fi
# ===== actual run (detached; all output → the log above) =====
echo "[run_mpm] $(hostname) start $(date)  n_grid={n_grid_mpm}  est_pts~{est_pts / 1e6:.0f}M"
# 1) plastic compaction of the REAL SE around the fixed AM scaffold (periodic x,y RVE = DEM 'boundary p p f')
python3 scripts/mpm3d_compaction.py \\
  --am-scaffold am_scaffold.csv --se-dump se_scaffold.csv --periodic \\
  --lateral-box {box_x} --n-grid {n_grid_mpm} --arch cuda --gpu-mem 28 --protocol hold --frames 150 \\
  --e-se {e_se_mpm} --nu-se {nu_se_mpm} --target-gpa {press_gpa} \\
  --save-se se_dump.npy --save-dg se_dump_dg.npy --save-eps se_dump_eps.npy --save-metrics mpm_metrics.json{add_flags} \\
  || {{ echo "[run_mpm] STEP 1 (compaction) FAILED — see the trace above.  NOT running the payload: it would"; \\
        echo "          rebuild mpm_payload.json from the STALE se_dump.npy of a PREVIOUS run and report a"; \\
        echo "          leftover porosity as if it were this run.  Fix the error and re-run."; exit 1; }}
# 2) webapp payload (AM spheres + SE surface + seed/compacted + raw metrics)
python3 scripts/mpm_webapp_payload.py \\
  --se se_dump.npy --scaffold am_scaffold.csv --se-dump se_scaffold.csv \\
  --n-vox 192 --tri-step 4 --smooth 1.5 --target-porosity {tgt_pay} --eps se_dump_eps.npy{pay_dilate} \\
  --void-max 180000 --metrics-json mpm_metrics.json --case {case}{pay_phase} --out mpm_payload.json
echo "[run_mpm] DONE $(date) → upload mpm_payload.json + mpm_metrics.json back to the case in the webapp"
"""
    rp = os.path.join(a.out, 'run_mpm.sh')
    open(rp, 'w').write(run); os.chmod(rp, 0o755)
    print(f'MPM input for case "{case}" → {a.out}/')
    print(f'  am_scaffold.csv ({len(am_rows)} AM)  se_scaffold.csv ({len(se_rows)} SE)  '
          f'run_mpm.sh  mpm_input.json  (target_porosity={tgt})')


if __name__ == '__main__':
    main()
