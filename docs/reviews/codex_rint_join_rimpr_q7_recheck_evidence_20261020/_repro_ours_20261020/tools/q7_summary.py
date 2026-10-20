"""Side-by-side Q7 numbers: Codex evidence vs ours (read-only).

Usage: python3 -I q7_summary.py <codex q7_independent.json> <ours q7_independent.json>
"""
import json
import sys

a = json.load(open(sys.argv[1], encoding='utf-8'), parse_constant=float)
b = json.load(open(sys.argv[2], encoding='utf-8'), parse_constant=float)


def rel(x, y):
    return abs(x - y) / abs(x) if x else abs(y)


print('env codex', a['python'].split()[0], a['numpy'], a['scipy'], '| ours', b['python'].split()[0], b['numpy'], b['scipy'])
print('bad_values', len(a['bad_values']), len(b['bad_values']),
      'all rejected (ours)', all(not r['gate']['accepted'] and not r['solve']['accepted'] and r['cg_calls'] == 0 for r in b['bad_values']))
for name in ('cnc_normal', 'cnc_registered_zero', 'cnc_doubled_all', 'rrm_normal', 'rrm_registered_zero', 'rrm_doubled_all'):
    ca, cb = a['positive_controls'][name], b['positive_controls'][name]
    sa, sb = ca['new']['sigma_eff'], cb['new']['sigma_eff']
    print(f"{name:22s} film/cut {ca['film']}/{ca['cut']} vs {cb['film']}/{cb['cut']}  sigma codex {sa!r} ours {sb!r}  rel {rel(sa, sb):.2e}"
          f"  identical old/new: codex {ca['entire_result_identical']} ours {cb['entire_result_identical']}"
          f"  ndof {cb['new']['n_dof']} resid {cb['new']['resid']:.3e}")
print('cnc_zero_equals_off', a['positive_controls']['cnc_zero_equals_off'], b['positive_controls']['cnc_zero_equals_off'])
na, nb = a['n9b']['nan_zero'], b['n9b']['nan_zero']
print('N9b nan==zero exact (ours)', nb['exact_equal'])
print('N9b sigma codex', na['old_nan']['sigma_eff'], na['old_nan']['sigma_hex'], '| ours', nb['old_nan']['sigma_eff'], nb['old_nan']['sigma_hex'])
print('N9b resid codex', na['old_nan']['resid'], '| ours', nb['old_nan']['resid'])
print('N9b phi sha codex', na['old_nan']['phi']['sha256'], '| ours', nb['old_nan']['phi']['sha256'])
print('N9b phi shape', nb['old_nan']['phi']['shape'], nb['old_nan']['phi']['dtype'])
print('N9b matrix codex', {k: na['matrix'][0][k] for k in ('shape', 'nnz')}, 'ours', {k: nb['matrix'][0][k] for k in ('shape', 'nnz')})
print('N9b matrix/rhs hashes equal codex<->ours', na['matrix'] == nb['matrix'])
ca, cb = a['n9b']['cut_deleted_k_changed'], b['n9b']['cut_deleted_k_changed']
print('cut deletion sigma codex', ca['generic_solve']['sigma_eff'], '| ours', cb['generic_solve']['sigma_eff'],
      'rel', f"{rel(ca['generic_solve']['sigma_eff'], cb['generic_solve']['sigma_eff']):.2e}",
      'wrapper accepted', cb['wrapper']['accepted'], 'cg', cb['wrapper_cg_calls'])
print('pure cut deleted independent', a['n9b']['pure_cut_deleted_independent'], b['n9b']['pure_cut_deleted_independent'])
print('off cases', len(a['off_cases']), len(b['off_cases']), all(x['entire_result_and_raster_byte_equal'] for x in b['off_cases']))
for k in ('off', 'rrm', 'rrm_zero', 'cnc'):
    x, y = a['native_cg'][k], b['native_cg'][k]
    print(f"native_cg {k:8s} identical codex {x['entire_result_identical']} ours {y['entire_result_identical']}  resid codex {x['new']['resid']:.3e} ours {y['new']['resid']:.3e}  unconv ours {y['new']['unconverged']}")
sa = [(s['name'], s['gate']['accepted'], s['solve']['accepted'], s['solve'].get('type')) for s in a['schema_boundary']]
sb = [(s['name'], s['gate']['accepted'], s['solve']['accepted'], s['solve'].get('type')) for s in b['schema_boundary']]
print('schema boundary same accept/type', sa == sb)
if sa != sb:
    for x, y in zip(sa, sb):
        if x != y:
            print('   ', x, y)
