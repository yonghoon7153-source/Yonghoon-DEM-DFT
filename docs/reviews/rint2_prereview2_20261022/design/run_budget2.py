"""Registration R §10-4 GPU-time basis vs repo records (no repository import).

Inputs (repo records):
  DBE arm 0 (new DBE bed, current gen, LEAN 2, rtol 1e-8) = 2,578 s   — anchor registration v2 §7 10:50 line
  SBE arm 0 (current gen, LEAN 2)                         =   879 s   — anchor registration v2 §7 C line (σ_e solve 704 s, same bed, other run)
  synthetic B1 table (docs/reviews/codex_rint2_carbon_design_review_evidence_20261021/_repro_ours_20261021/extra_step3_conv_cert_table.log):
      CG iterations, 41,472 dof, fibre σ 7,853.98 (next-gen contrast) — 'plain' (no junction) vs 'junction' (one junction edge per column)
Run:  python3 -I run_budget2.py      (writes run_budget2.json)
"""
import json
import os

it = {'plain': {1e-8: [691, 692, 731], 1e-12: [1095, 1091, 1133], 1e-14: [1283, 1286, 1326]},
      'junction': {1e-8: [2280, 2185, 2516], 1e-12: [4191, 4276, 4326], 1e-14: [5054, 5051, 5476]}}
m = {f: {r: sum(v) / len(v) for r, v in d.items()} for f, d in it.items()}
ratio = {
    'rtol_only_plain_1e-8_to_1e-12': m['plain'][1e-12] / m['plain'][1e-8],
    'rtol_only_junction_1e-8_to_1e-12': m['junction'][1e-12] / m['junction'][1e-8],
    'form_at_1e-12_junction_over_plain': m['junction'][1e-12] / m['plain'][1e-12],
    'junction_1e-12_over_plain_1e-8': m['junction'][1e-12] / m['plain'][1e-8],
    'junction_1e-14_cold_over_plain_1e-8 (upper for +resolve)': m['junction'][1e-14] / m['plain'][1e-8],
}
# registration §10-4 main judgment ① = 78 arms; split SBE / DBE (registration table rows)
sbe_arms = 24 + 8 + 4 + 2          # two ladders x12 + end origin 4 runs x2 arms + SBE origin 2 runs x2 + no-op 2
dbe_arms = 12 + 24 + 4             # corners 12 + DBE origin 12 runs x2 + SV counterfactual (R_j0, 4 arm-equivalents)
reg = {f'x{k}': 78 * 2578 * k / 3600 for k in (1, 1.7, 2)}
split1 = (sbe_arms * 879 + dbe_arms * 2578) / 3600
SBE_SOLVE, SBE_OVH = 704, 175
DBE_SOLVE_FRAC = SBE_SOLVE / 879    # assumption: same solve fraction as SBE (0.80)
DBE_SOLVE, DBE_OVH = 2578 * DBE_SOLVE_FRAC, 2578 * (1 - DBE_SOLVE_FRAC)
est = {}
for name, f in (('rtol_only_1.7', 1.7), ('rtol_only_2', 2.0), ('junction_1e-12/plain_1e-8', ratio['junction_1e-12_over_plain_1e-8']),
                ('junction_1e-14cold/plain_1e-8', ratio['junction_1e-14_cold_over_plain_1e-8 (upper for +resolve)'])):
    t = sbe_arms * (SBE_OVH + SBE_SOLVE * f) + dbe_arms * (DBE_OVH + DBE_SOLVE * f)
    est[name] = t / 3600
out = {'mean_iters': {f: {str(r): v for r, v in d.items()} for f, d in m.items()}, 'ratios': ratio,
       'main_arms': {'sbe': sbe_arms, 'dbe_incl_sv': dbe_arms, 'total': sbe_arms + dbe_arms},
       'registration_main_hours': reg, 'split_base_hours_x1': split1, 'main_hours_by_factor_on_solve': est,
       'window_hours': {'10-25..29': 120, 'to 10-31': 168},
       'overflow_one_DBE_corner_over (24 arms) hours': {'x1': 24 * 2578 / 3600, 'x1.7': 24 * 2578 * 1.7 / 3600,
                                                          'x6.05_solve': 24 * (DBE_OVH + DBE_SOLVE * ratio['junction_1e-12_over_plain_1e-8']) / 3600}}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'run_budget2.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
