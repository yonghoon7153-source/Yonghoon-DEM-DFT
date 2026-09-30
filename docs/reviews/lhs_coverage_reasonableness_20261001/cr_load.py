#!/usr/bin/env python3
"""cov5 reasonableness — loader: builds one per-case table (both cohorts) and pickles it.
READ-ONLY on the repo; writes only into the scratchpad."""
import csv, glob, json, math, os, pickle
import numpy as np

import os as _os, tempfile as _tf
HERE = _os.path.dirname(_os.path.abspath(__file__))
REPO = _os.path.abspath(_os.path.join(HERE, '..', '..', '..'))
SP = _os.environ.get('COV5_WORK') or _os.path.join(_tf.gettempdir(), 'cov5_work')   # 중간 산출 (리포 밖)
_os.makedirs(SP, exist_ok=True)
D = REPO + '/docs/data'   # 5번 원자료 (docs/data/{lhs,lhsx}_{descriptors_cov,webapp_coverage}_1e09f661d/)


def fnum(x):
    if x is None:
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if s == '':
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


def load_design():
    des = {}
    for r in csv.DictReader(open(REPO + '/docs/data/lhs_design_20260818.csv')):
        des[r['case_id']] = dict(block=r['block'], am_pct=fnum(r['am_pct']), d_se=fnum(r['d_se_um']),
                                 d_am_p=fnum(r['d_am_p_um']), d_am_s=fnum(r['d_am_s_um']), ps_frac=fnum(r['ps_frac']),
                                 loading=fnum(r['loading_mAh_cm2']))
    for r in csv.DictReader(open(REPO + '/docs/data/lhsx_design_adapted_20260929.csv')):
        des[r['case_id']] = dict(block=r['block'], am_pct=fnum(r['am_pct']), d_se=fnum(r['d_se_um']),
                                 d_am_p=fnum(r['d_am_p_um']), d_am_s=fnum(r['d_am_s_um']), ps_frac=fnum(r['ps_frac']),
                                 loading=np.nan, volfrac=fnum(r['lhsx_volfrac']))
    return des


def main():
    des = load_design()
    rows = []
    for cohort, hdir, wdir in (('LHS', 'lhs_descriptors_cov_1e09f661d', 'lhs_webapp_coverage_1e09f661d'),
                               ('lhsx', 'lhsx_descriptors_cov_1e09f661d', 'lhsx_webapp_coverage_1e09f661d')):
        W = {r['case']: r for r in csv.DictReader(open(f'{D}/{wdir}/metrics_flat.csv'))}
        ST = json.load(open(f'{D}/{wdir}/status.json'))
        stc = ST['cases']
        for p in sorted(glob.glob(f'{D}/{hdir}/*.json')):
            cid = os.path.basename(p)[:-5]
            if cid.startswith('_'):
                continue
            H = json.load(open(p))
            w = W[cid]
            d = des[cid]
            pc = H['phase_counts']
            row = dict(cohort=cohort, case=cid, **d)
            row['n_P'] = pc.get('AM_P', 0); row['n_S'] = pc.get('AM_S', 0); row['n_A'] = pc.get('AM', 0); row['n_SE'] = pc.get('SE', 0)
            row['n_AMtot'] = row['n_P'] + row['n_S'] + row['n_A']
            row['phi_se'] = H['phi_se']; row['phi_am'] = H['phi_am']
            row['se_of_solid'] = H['phi_se'] / (H['phi_se'] + H['phi_am'])
            row['porosity'] = H['porosity_sphere_pct_RECORD_ONLY']
            row['thick_um'] = H['handover_qc']['thickness_wall_gap_um']
            # --- harvester Hertz-geom + wall-excl ---
            for ph, key in (('P', 'AM_P'), ('S', 'AM_S'), ('T', 'AM_total'), ('A', 'AM_only')):
                row[f'hz_{ph}'] = fnum(H.get(f'coverage_{key}_hertz_pct'))
                row[f'we_{ph}'] = fnum(H.get(f'coverage_{key}_wallexcl_pct'))
                row[f'we_{ph}_st'] = H.get(f'coverage_{key}_wallexcl_status')
            for ph, key in (('P', 'AM_P'), ('S', 'AM_S'), ('T', 'AM_total')):
                row[f'hz_{ph}_st'] = H['status'].get(f'coverage_{key}')
            cd, wd = H['coverage_detail'], H['coverage_wallexcl_detail']
            row['hz_ncap'] = cd['n_capped']; row['hz_nbad'] = cd['n_free_surface_invalid']
            row['we_ncap'] = wd['n_capped']; row['we_nbad'] = wd['n_free_surface_invalid']
            for lab in ('AM_P', 'AM_S', 'AM'):
                row[f'hz_cnt_{lab}'] = (cd['counts'][lab]['n_particles'], cd['counts'][lab]['n_valid'])
                row[f'we_cnt_{lab}'] = (wd['counts'][lab]['n_particles'], wd['counts'][lab]['n_valid'])
            row['wall_split'] = H['coverage_wall_split']['by_phase']
            row['wall_touch'] = H.get('wall_touch')
            # --- webapp ---
            row['w_nP'] = fnum(w['n_AM_P']); row['w_nS'] = fnum(w['n_AM_S']); row['w_nSE'] = fnum(w['n_SE'])
            row['w_rP'] = fnum(w['r_AM_P']); row['w_rS'] = fnum(w['r_AM_S']); row['w_rSE'] = fnum(w['r_SE'])
            row['w_mode'] = w['meta.mode']
            for ph, key in (('P', 'AM_P'), ('S', 'AM_S')):
                row[f'wh_{ph}'] = fnum(w[f'coverage_{key}_mean']); row[f'wh_{ph}_sd'] = fnum(w[f'coverage_{key}_std'])
                row[f'lp_{ph}'] = fnum(w[f'coverage_{key}_mean_physics']); row[f'lp_{ph}_sd'] = fnum(w[f'coverage_{key}_std_physics'])
                row[f'lp_{ph}_dpct'] = fnum(w[f'coverage_{key}_delta_pct_physics'])
                row[f'lr_{ph}'] = fnum(w[f'coverage_{key}_mean_physics_rough']); row[f'lr_{ph}_sd'] = fnum(w[f'coverage_{key}_std_physics_rough'])
                row[f'lr_{ph}_dpct'] = fnum(w[f'coverage_{key}_delta_pct_rough'])
                row[f'v2_{ph}'] = fnum(w[f'coverage_{key}_mean_physics_v2']); row[f'v2_{ph}_sd'] = fnum(w[f'coverage_{key}_std_physics_v2'])
            row['lp_T'] = fnum(w['coverage_AM_mean_physics']); row['lp_T_dpct'] = fnum(w['coverage_AM_delta_pct_physics'])
            row['lr_T'] = fnum(w['coverage_AM_mean_physics_rough']); row['lr_T_dpct'] = fnum(w['coverage_AM_delta_pct_rough'])
            row['v2_T'] = fnum(w['coverage_AM_mean_physics_v2'])
            row['v2_status'] = w['coverage_status_physics_v2']
            row['v2_nam'] = fnum(w['am_denominator_physics_v2.n_am'])
            row['v2_nfree0'] = fnum(w['am_denominator_physics_v2.n_free_surface_nonpositive'])
            row['v2_nclip'] = fnum(w['am_denominator_physics_v2.n_coverage_clipped_100'])
            row['v2_nrinv'] = fnum(w['am_denominator_physics_v2.n_radius_invalid'])
            row['v2_ncont'] = fnum(w['n_contacts_physics_v2'])
            row['v2_confl'] = fnum(w['cap_conflict_frac_physics_v2'])
            for b in ('hertzian', 'liggghts', 'tabor', 'volume', 'geom', 'elastic', 'other'):
                row[f'bind_amse_{b}'] = fnum(w[f'A_binding_share_AM_SE_pct.{b}'])
            row['area_amse_h'] = fnum(w['area_AM전체_SE_total']); row['area_amse_p'] = fnum(w['area_AM전체_SE_total_physics'])
            row['area_amse_v2'] = fnum(w['area_AM전체_SE_total_physics_v2'])
            row['area_amse_dpct'] = fnum(w['area_AM전체_SE_total_delta_pct_physics'])
            row['am_se_cn_mean'] = fnum(w['am_se_cn_mean'])
            row['AM_P_se_cn_mean'] = fnum(w['AM_P_se_cn_mean']); row['AM_S_se_cn_mean'] = fnum(w['AM_S_se_cn_mean'])
            row['overlap_mean'] = fnum(w['overlap_mean']); row['overlap_max'] = fnum(w['overlap_max'])
            row['status_case'] = stc[cid]['status'] if isinstance(stc, dict) and cid in stc else None
            row['type_map_fold'] = stc[cid].get('type_map_fold') if isinstance(stc, dict) and cid in stc else None
            rows.append(row)
    pickle.dump(rows, open(SP + '/cr_rows.pkl', 'wb'))
    print('rows', len(rows), 'LHS', sum(r['cohort'] == 'LHS' for r in rows), 'lhsx', sum(r['cohort'] == 'lhsx' for r in rows))


if __name__ == '__main__':
    main()
