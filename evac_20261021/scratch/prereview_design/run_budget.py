"""Registration R 3rd edition §10 run table -> GPU hours vs the 10-21 schedule (fix plan §5 Q1: runs 10-25..10-29, verdict 10-30..31).

Sources (repo):
  * per-arm time, LEAN=2, ARMS=1, new DBE bed, rtol 1e-8, maxiter 60000: 2,578 s  (registration v2 §7, 10-20 10:50 line)
  * per-arm time, LEAN=4, 8 arms: finish times 12:16 13:06 13:54 14:44 15:31 16:19 17:07 17:55, start ~11:28  (v2 §7, 18:59 line)
  * factor x1.7-2 for rtol 1e-12 (+ (c) re-solve) = registration §3-5 / §10 [탐침 어림]; GRID dof x1.728 = registration §9
  * run table = registration §10 (fixed part) + ladders (points per ladder from probe_registration_v3: 10-13)
All outputs are estimates (추정) - no GPU was used.

Usage: python3 -I run_budget.py
"""
import json
import os

lean2_min = 2578 / 60.0
fin = ['12:16', '13:06', '13:54', '14:44', '15:31', '16:19', '17:07', '17:55']
mins = [int(h) * 60 + int(m) for h, m in (t.split(':') for t in fin)]
lean4_min = (mins[-1] - (11 * 60 + 28)) / 8.0
L = 12                       # points per ladder (probe: 10, 12, 13)
grid = 1.728
cfg = {
    'main': {'arms': 42 + 4 + 2 * L, 'scale': 1.0},       # 42 fixed + SV counterfactual (R_j,0 only) + 2 ladders
    'FIBRE': {'arms': 42 + 2 * L, 'scale': 1.0},
    'UNREG': {'arms': 42 + 2 * L, 'scale': 1.0},
    'GRID': {'arms': 42 + 2 * L, 'scale': grid},
    'SVORDER': {'arms': 36, 'scale': 1.0},
    'GRID_current_gen_control': {'arms': 6, 'scale': grid},
}
window_runs_h = 5 * 24       # 10-25..10-29
window_all_h = 7 * 24        # 10-25..10-31
res = {'per_arm_min_LEAN2_measured': lean2_min, 'per_arm_min_LEAN4_measured': lean4_min, 'L_points_per_ladder': L,
       'configs': {}}
for f_lbl, f in (('x1.0', 1.0), ('x1.7', 1.7), ('x2.0', 2.0)):
    tot = 0.0
    for k, v in cfg.items():
        h = v['arms'] * v['scale'] * lean2_min * f / 60.0
        res['configs'].setdefault(k, {})[f_lbl + '_h'] = round(h, 1)
        tot += h
    res['total_h_' + f_lbl] = round(tot, 1)
    res['main_only_h_' + f_lbl] = res['configs']['main'][f_lbl + '_h']
res['window_runs_h_10_25_to_29'] = window_runs_h
res['window_h_10_25_to_31'] = window_all_h
res['arms_total_no_overflow'] = sum(v['arms'] for v in cfg.values())
res['overflow_worst_extra_arms'] = {'SBE_origin_8arm': 2 * 4 * 8, 'DBE_origin_8arm_per_corner_all': 4 * 5 * 3 * 8}
print(json.dumps(res, indent=1))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_budget.json'), 'w'), indent=1)
