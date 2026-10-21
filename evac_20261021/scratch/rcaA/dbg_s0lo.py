import os
import sys
import tempfile
import shutil
import numpy as np
sys.path.insert(0, 'scripts')
import test_ca_s0_census as T
import ca_s0_census as S0
import carbon_junction as CJ

tmp = tempfile.mkdtemp(prefix='dbgs0_')
T.STATE['tmp'] = tmp
try:
    vg, pt = T._kit_rv()
    kit = T.write_kit(tmp, 'kit_RV', vgcf=vg, ptfe=pt, vol={'VGCF': 0.05, 'PTFE': 0.1})
    calls = []
    orig = CJ.cjunc_registry

    def spy(*a, **k):
        r = orig(*a, **k)
        calls.append((a, k, r))
        return r
    CJ.cjunc_registry = spy
    S0.run_stage(1, [kit], os.path.join(tmp, 'out'), vox=T.J_H, bridge_um=0.48, sdcp_sphere_d=0.30)
    CJ.cjunc_registry = orig
    a, k, r = calls[0]
    print('box_lo', repr(a[1]), 'vox', a[2], 'thr', r['thresholds'])
    c = r['census']
    print({kk: c.get(kk) for kk in ('n_revisit_pairs', 'n_revisit_cells', 'n_revisit_fibres', 'revisit_s_um', 'n_port_ties',
                                    'n_subedges', 'n_subedges_long', 'n_subedges_ptfe_cov', 'n_instances_ptfe_partial')})
    inst = r['instances']
    print('Lc', inst['Lc'], 'nsub', inst['nsub'], 'self', inst['self'])
    print('sub cov', r['subedges']['ptfe_cov'], 'sub cp', r['subedges']['cp'][:3])
finally:
    shutil.rmtree(tmp, ignore_errors=True)
