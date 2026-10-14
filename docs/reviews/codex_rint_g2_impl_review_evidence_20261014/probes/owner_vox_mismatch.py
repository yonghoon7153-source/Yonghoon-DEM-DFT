"""Demonstrate a CNC plan/solver voxel-spacing mismatch without editing source."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE/'source/scripts'), str(HERE.parent/'lhs_coverage_review_20260930/deps'),
               str(HERE.parent/'gen2_network_reverify3_20261007/deps')]
import numpy as np
from scipy.sparse.linalg import spsolve
import step3_sigma as S3


def plan_for(c, r, sid, h):
    led = S3.am_iface_ledger(c, r, np.array([2, 2]), sid, sid, (0., 0., 0.), h,
                            delta_bound_um=0., bridge_um=1.2*h)
    return S3.am_iface_plan(led, {'AM_S|AM_S': 1e-3})


def main():
    h = 0.2
    c = np.array([[1., 1., 1.], [1., 1., 2.98]])
    r = np.ones(2)
    sid, _ = S3.rasterize(c, r, np.array([2, 2]), None, None, (0., 0., 0.), (2., 2., 4.), h, bridge_um=1.2*h)
    p = plan_for(c, r, sid, h)
    p_scaled = plan_for(c*2, r*2, sid, h*2)
    sig = S3.electronic_sigma_table(0.010, 0.005, 100., 10., 250.)
    orig = S3._solve_cg
    S3._solve_cg = lambda L, b: (spsolve(L.tocsc(), b), 0)
    rows = []
    try:
        for name, vox, plan in [('matching', h, p), ('mismatched', h*2, p), ('rebuilt_scaled', h*2, p_scaled)]:
            res = S3.solve_sigma_z(sid, sig, vox, return_field=True, z_bot_um=0., z_top_um=20*vox, iface=plan)
            physical_film_G = sum(float(np.sum(1e-8*vox*vox/a['rface'][~a['cut']]))
                                  for a in res['_iface']['axes'])
            rows.append({'case': name, 'solver_vox': vox, 'plan_vox': plan['vox'], 'rejections': plan['rejections'],
                         'sigma': res['sigma_eff'], 'cg_info': res['cg_info'], 'resid': res['resid'],
                         'reported_vox': res['iface']['iface_contact_ledger']['vox_um'],
                         'reported_A': res['iface']['iface_contact_ledger']['A_film_sum_um2'],
                         'reported_film_G': res['iface']['iface_contact_ledger']['film_G_S_total'],
                         'actual_face_film_G': physical_film_G,
                         'n_film_rows_used': res['iface']['iface_contact_ledger']['n_film_rows_used']})
    finally:
        S3._solve_cg = orig
    out = {'fixture': {'c': c.tolist(), 'r': r.tolist(), 'sid_shape': list(sid.shape), 'h': h, 'r_type': 1e-3},
           'rows': rows, 'mismatched_G_over_reported': rows[1]['actual_face_film_G']/rows[1]['reported_film_G']['remove_area'],
           'same_scaled_matrix_sigma_relative_difference': rows[1]['sigma']/rows[2]['sigma']-1}
    target = HERE/'evidence/owner_vox_mismatch.json'
    target.write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
