import importlib.util
import sys
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee'
sys.path.insert(0, WT + '/scripts')
spec = importlib.util.spec_from_file_location('carbon_junction', sys.argv[1] if len(sys.argv) > 1 else
                                              '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/impl/carbon_junction.py')
m = importlib.util.module_from_spec(spec)
sys.modules['carbon_junction'] = m
spec.loader.exec_module(m)
sys.argv = ['x']
import runpy
T = runpy.run_path(WT + '/scripts/test_carbon_junction.py', run_name='tcj')
import step3_sigma as S3
T['S3'] = S3
T['CJ'] = m
g = T
for k in ('S3', 'CJ'):
    g['t_kink'].__globals__[k] = g[k]
P = g['rows']([g['SFR']])
sid, _ = g['bed'](P, g['SFR_N'])
reg = g['registry'](sid, P, s_min_um=g['S_MIN'])
I = reg['instances']
for q in range(len(I['fi'])):
    print(q, 'self', bool(I['self'][q]), 's', I['s'][q], 'd0', I['d0'][q], 'Lc', I['Lc'][q], 'ports', g['_pcells'](reg, q, 'i'),
          g['_pcells'](reg, q, 'j'), 'seg_i', I['seg_i'][q][:3], '...', 'seg_j', I['seg_j'][q][:3], 'reason', I['reason'][q])
print({k: reg['census'].get(k) for k in ('n_self_candidates', 'n_self_kept', 'n_self_filtered', 'self_s_um')})
Pd = g['rows']([g['SFR'][:4], g['SFR'][6:]])
sidd, _ = g['bed'](Pd, g['SFR_N'])
rd = g['registry'](sidd, Pd, s_min_um=g['S_MIN'])
Id = rd['instances']
for q in range(len(Id['fi'])):
    print('split', q, 'Lc', Id['Lc'][q], 'ports', g['_pcells'](rd, q, 'i'), g['_pcells'](rd, q, 'j'), 'd0', Id['d0'][q])
print('sub split', g['_sub_cells'](rd))
print('sub same', g['_sub_cells'](reg))
