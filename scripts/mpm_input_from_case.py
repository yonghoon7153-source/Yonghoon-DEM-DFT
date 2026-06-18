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
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', required=True, help='case results dir (has atoms.csv, full_metrics.json)')
    ap.add_argument('--case', default='', help='case id (provenance)')
    ap.add_argument('--out', required=True, help='output dir for the MPM input package')
    ap.add_argument('--type-map', default='', help='LIGGGHTS type map e.g. "1:AM_P,2:AM_S,3:SE" or '
                    '"1:AM_P,2:SE" — SE is NOT always type 3 (a no-AM_S case is type 2); parsed for SE vs AM')
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
    case = a.case or os.path.basename(a.results.rstrip('/'))
    # lateral RVE box (LIGGGHTS units) → MPM scl = WIDTH/lateral_box and adaptive n_grid.  Prefer
    # input_params box_x; else the atom lateral extent (periodic box ≈ max x,y).  Thick films are
    # TALLER than this lateral, so MPM auto-extends the z grid (non-cubic) to fit — see run script.
    box_x = ip.get('box_x') or ip.get('box_x_sim')
    if not box_x:
        allxy = [float(r[1]) for r in (am_rows + se_rows)] + [float(r[2]) for r in (am_rows + se_rows)]
        box_x = max(allxy) if allxy else 0.05
    box_x = round(float(box_x), 6)
    # adaptive lateral resolution: keep SE ≈ 3.5 cells (real_14 0.05→384, unchanged) so the
    # calibration transfers; scales DOWN for smaller RVEs so the tall-nz grid fits GPU memory.
    n_grid_mpm = max(128, min(384, int(round(384 * box_x / 0.05))))
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
            'lateral_box': box_x, 'mpm_n_grid': n_grid_mpm}
    json.dump(prov, open(os.path.join(a.out, 'mpm_input.json'), 'w'), indent=2)

    # run script: edit paths/GPU as needed, then run on a GPU box
    run = f"""#!/usr/bin/env bash
# MPM run for case {case} — generated by mpm_input_from_case.py
# SE scaled to this case (K-fixed): E_SE={e_se_mpm} GPa ν={nu_se_mpm}  (bulk K={prov['mpm_K_se_gpa']} GPa
#   real-LPSC, shear μ={prov['mpm_mu_se_gpa']} GPa = ×{prov['se_ratio_vs_1p35']} of champion;
#   from DEM E_eff {e_se_dem} GPa), press {press_gpa} GPa
# 1) plastic compaction of the REAL SE around the fixed AM scaffold + raw metrics
#    --periodic: x,y periodic RVE = the DEM 'boundary p p f' (boundary AM/SE get bulk
#    compaction + coverage).  Validated on real_14: porosity 15.93->15.91% (anchor held),
#    coverage AM_P/S 26.6/28.1 -> 29.3/30.9% (boundary grains now represented).
#    --lateral-box {box_x}: real RVE width (NOT assumed 50µm).  n_grid {n_grid_mpm} keeps SE
#    resolved; MPM auto-extends nz for this thick film (158µm films no longer overflow the box).
#    If it OOMs, lower --n-grid or raise --gpu-mem.
python3 scripts/mpm3d_compaction.py \\
  --am-scaffold am_scaffold.csv --se-dump se_scaffold.csv --periodic \\
  --lateral-box {box_x} --n-grid {n_grid_mpm} --arch cuda --gpu-mem 28 --protocol hold --frames 150 \\
  --e-se {e_se_mpm} --nu-se {nu_se_mpm} --target-gpa {press_gpa} \\
  --save-se se_dump.npy --save-dg se_dump_dg.npy --save-eps se_dump_eps.npy --save-metrics mpm_metrics.json

# 2) webapp payload (AM spheres + SE surface + seed/compacted + raw metrics)
python3 scripts/mpm_webapp_payload.py \\
  --se se_dump.npy --scaffold am_scaffold.csv --se-dump se_scaffold.csv \\
  --n-vox 192 --tri-step 5 --target-porosity {tgt} --eps se_dump_eps.npy \\
  --metrics-json mpm_metrics.json --case {case} --out mpm_payload.json

echo "→ upload mpm_payload.json (and mpm_metrics.json) back to the case in the webapp"
"""
    rp = os.path.join(a.out, 'run_mpm.sh')
    open(rp, 'w').write(run); os.chmod(rp, 0o755)
    print(f'MPM input for case "{case}" → {a.out}/')
    print(f'  am_scaffold.csv ({len(am_rows)} AM)  se_scaffold.csv ({len(se_rows)} SE)  '
          f'run_mpm.sh  mpm_input.json  (target_porosity={tgt})')


if __name__ == '__main__':
    main()
