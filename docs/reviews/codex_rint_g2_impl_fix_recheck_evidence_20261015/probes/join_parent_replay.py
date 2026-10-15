"""Second reviewer replay of the retained parser counterexample bytes."""
from pathlib import Path
import sys,json,contextlib,io,warnings
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'source/scripts'),str(R.parent/'lhs_coverage_review_20260930/deps')]
import numpy as np
import rint_iface_join as J
import step3_sigma as S
D=R/'tmp/join_independent'
if not D.exists():
    D=R/'evidence/join_fixtures'
rows=[]
for name in ('baseline','malformed_numeric_contact_row_inside_block',
             'malformed_numeric_atom_row_inside_block','duplicate_radius_column',
             'step_extra_token','count_extra_token','wellshaped_duplicate_contact_control',
             'scaffold_fixed_decimal_radius_overflow'):
    paths=[D/(name+'_'+s) for s in ('sc.csv','atom.dump','contact.dump')]
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        j=J.am_iface_join(*paths,type_map={1:'AM_P',2:'SE'})
    out={'case':name,'status':j['status'],'codes':[x['code'] for x in j['rejections']],
         'reported_nonfinite':j['entrance'].get('n_nonfinite'),
         'finite_particles':bool(np.isfinite(j['particles']['c_um']).all() and np.isfinite(j['particles']['r_um']).all())}
    if j['status']=='PASS':
        c,r,t=(j['particles'][k] for k in ('c_um','r_um','t'))
        # For the deliberately overflowing particle do not rasterize it.
        if out['finite_particles']:
            with contextlib.redirect_stdout(io.StringIO()):
                sid,_=S.rasterize(c,r,t,None,None,(0,0,0),(6,4,4),.25,bridge_um=.24)
            led=S.am_iface_ledger(c,r,t,sid,sid,(0,0,0),.25,
                                  delta_bound_um=j['g_geo']['delta_bound_um'],bridge_um=.24)
            p=S.am_iface_plan(led,{'AM_P|AM_P':.001},join=j,gap_law='cut',unreg_law='cut',ambiguous_arm='cut')
            try:S.iface_require_quantitative(p,sid,vox=.25);out['quantitative_guard']='ACCEPT'
            except Exception as e:out['quantitative_guard']=type(e).__name__+': '+str(e)
        else:out['quantitative_guard']='NOT_RUN; invalid geometry independently rejected by ledger in join_independent.json'
    rows.append(out)
(R/'evidence/join_parent_replay.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
