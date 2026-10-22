"""Read-only pinned implementation probes. All generated output stays beside this file."""
import contextlib, copy, hashlib, io, json, math, os, sys, traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = Path(os.environ.get('RINT_REVIEW_SOURCE') or ROOT / 'source').expanduser().resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(SOURCE / 'scripts'))
import numpy as np
import carbon_junction as CJ
import step3_sigma as S3
import ca_ext_svcf as SV
import rint_r_chain as RC
import test_carbon_junction as T
T.CJ, T.S3 = CJ, S3

def serial(x):
    if isinstance(x, dict): return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [serial(v) for v in x]
    if isinstance(x, np.ndarray): return serial(x.tolist())
    if isinstance(x, np.generic): return serial(x.item())
    if isinstance(x,float) and not math.isfinite(x): return str(x)
    return x

def check_record(raw, threshold=2.):
    rec = SV.sv_cf_record(raw)
    evidence = {'sv_counterfactual_request':{'threshold':raw['threshold']}, 'solve':{'sv_counterfactual':rec}}
    try: problem = SV.sv_cf_problem(evidence, True)
    except Exception as exc: problem = type(exc).__name__+': '+str(exc)
    flags, detail = RC.sv_assess({('1','P0','R_j0'):{'sv_cf':SV.chain_view(rec)}}, threshold,'R_j0')
    return {'problem':problem,'flags':flags,'detail':detail,'record':rec}

def run_geometry(polys, sdcp, shape, hook=None, patch=None):
    # Independent fixture construction calls actual raster/registry/plan/solve.
    rows = T.cat_rows(T.rows(polys), T.rows([[p] for p in sdcp], phase=5,kind=0,fid0=700))
    sid,_ = T.bed(rows,shape,sdcp_sphere_d_um=0.)
    reg = T.registry(sid, rows, tol_sj_um=.1, r_sdcp_um=.5)
    if hook: hook(reg)
    plan = CJ.cjunc_plan(reg,1000.,unreg_law='cut',ptfe_stamp='off',sv_counterfactual={'threshold':None})
    original = CJ.CjuncAssembler._sv_unsplit_cells
    if patch: CJ.CjuncAssembler._sv_unsplit_cells=patch(original)
    try: res = T.solve(sid,T.sig_e(),shape,plan)
    finally: CJ.CjuncAssembler._sv_unsplit_cells=original
    raw = res['cjunc']['sv_counterfactual']
    return {'G':T.I_of(res,shape),'sigma':res['sigma_eff'],'census':reg['census'],**check_record(raw)},raw

out={'source_root':str(SOURCE),
     'source_sha256':{p:hashlib.sha256((SOURCE/'scripts'/p).read_bytes()).hexdigest()
                      for p in ('carbon_junction.py','ca_ext_svcf.py','ptfe_face_alpha.py','rint_r_chain.py')},
     'runtime':{'python':sys.version,'numpy':np.__version__}}

tags={'RCA03','RCA04','RCA04-V','RCA04-EPS','RCA04-DUP','RCA05','RCA06','RCA06-H','GAP','RING','SELFD','QC','QD','QD2','KBND','CEN','S3','FA+CJ'}
test_log=io.StringIO()
with contextlib.redirect_stdout(test_log), contextlib.redirect_stderr(test_log):
    for tag, fn in T.CASES:
        if tag in tags:
            print('CASE',tag)
            try: fn()
            except Exception:
                traceback.print_exc()
                T.chk(tag+' uncaught exception',False)
(HERE/'targeted_tests.log').write_text(test_log.getvalue(),encoding='utf-8')
out['author_regression']={'passed':T._ok,'failed':T._fail,'tags':sorted(tags)}

# Two independent SDCP bridge components, each traversed by two straight fibres.
# Four symmetric complete rails have no transverse current: true bridge removal ratio is 1.
shape=(11,3,9)
polys=[[(x+.5,1.5,.5),(x+.5,1.5,8.5)] for x in (1,3,7,9)]
sdcp=[(x+.5,1.5,4.5) for x in (1,2,3,7,8,9)]
out['two_symmetric_components'],multi_raw=run_geometry(polys,sdcp,shape)
out['two_symmetric_components']['independent_expected_G']=4/(.005+6*.01+2*.007+.005)
out['two_symmetric_components']['true_bridge_removal_ratio']=1.

# Partial-removal mutation preserves labels and census, but deletes only the first component's cells.
# Its false upper endpoint is exactly 2, so threshold 2 incorrectly produces no blocker.
def first_component_only(original):
    def mutant(self):
        labels,lins=original(self)
        grid_labels,_=CJ.ndimage.label(self.sid==5)
        return labels,np.flatnonzero(np.isin(grid_labels.ravel(),labels[:1]))
    return mutant
out['first_component_only_mutation'],_=run_geometry(polys,sdcp,shape,patch=first_component_only)
before_pass,before_fail=T._ok,len(T._fail)
original=CJ.CjuncAssembler._sv_unsplit_cells
CJ.CjuncAssembler._sv_unsplit_cells=first_component_only(original)
mutation_log=io.StringIO()
try:
    with contextlib.redirect_stdout(mutation_log):T.t_sv_bracket()
finally:CJ.CjuncAssembler._sv_unsplit_cells=original
(HERE/'first_component_mutation.log').write_text(mutation_log.getvalue(),encoding='utf-8')
out['author_QD2_under_first_component_mutation']={'passed':T._ok-before_pass,'failed':T._fail[before_fail:]}

# Producer creates unsplit_census_mismatch: test through projection AND validator, not sv_assess alone.
out['census_mismatch'],_=run_geometry(polys,sdcp,shape,hook=lambda r:r['census'].__setitem__('n_unsplit_bridging_components',0))

# A genuinely finite upper endpoint: add a remote fifth complete rail.
shape=(15,3,9)
polys_f=polys+[[(13.5,1.5,.5),(13.5,1.5,8.5)]]
out['two_components_finite_upper'],finite_raw=run_geometry(polys_f,sdcp,shape)

# Existing PRE2 record-consistency counterexample class, each mutation independently applied.
mutations={
 'lower_wrong_ratio':lambda r:r.__setitem__('sv_counterfactual_ratio',1.1),
 'upper_wrong_ratio':lambda r:(r.__setitem__('sv_counterfactual_ratio_hi',1.1),r['upper'].__setitem__('sv_counterfactual_ratio',1.1)),
 'upper_removed_count_zero':lambda r:r['upper'].__setitem__('n_components_removed',0),
 'computed_without_certificates':lambda r:(r.__setitem__('conv_cert',None),r['upper'].__setitem__('conv_cert',None)),
 'arbitrary_bracket_rule':lambda r:r.__setitem__('bracket_rule','not-the-registered-rule'),
 'huge_unsplit_count':lambda r:r.__setitem__('n_unsplit_bridging_components',10**400),
 'false_certificate':lambda r:r.__setitem__('conv_cert',{'status':'POSITIVE_SOLVED','ok':False}),
}
out['record_mutations']={}
for name,fn in mutations.items():
    raw=copy.deepcopy(finite_raw);fn(raw)
    result=check_record(raw)
    out['record_mutations'][name]={k:v for k,v in result.items() if k!='record'}

# A solver perturbation within all four actual certificate tolerances produces a
# threshold crossing without tampering with any evidence fields.
from scipy.sparse.linalg import spsolve
P=T.cat_rows(T.rows(T.SVX),T.rows(T.SVX_SDCP,phase=5,kind=0,fid0=700))
sid,_=T.bed(P,T.SVX_N)
reg=T.registry(sid,P,tol_sj_um=.1,r_sdcp_um=.5)
plan=T.plan(reg,T.SVX_RJ,sv_counterfactual={'threshold':None})
exact_G,_,_=T._svx_ref(T.SVX_RJ)
exact_cut,_,_=T._svx_ref(T.SVX_RJ,with_sv=False)
actual_ratio=exact_G/exact_cut
old_solver,old_cert,old_rtol=S3._solve_cg,S3.CONV_CERT,S3.CG_RTOL
calls=[0]
def perturbed_solver(L,b,*a,**kw):
    calls[0]+=1
    phi=spsolve(L.tocsc(),b)
    if calls[0]==1: phi=phi+1.e-8
    return phi,0
S3._solve_cg,S3.CONV_CERT,S3.CG_RTOL=perturbed_solver,True,1.e-12
try: res=T.quiet(S3.solve_sigma_z,sid,T.sig_e(),T.H,z_top_um=float(T.SVX_N[2]),z_bot_um=0.,cjunc=plan)
finally:S3._solve_cg,S3.CONV_CERT,S3.CG_RTOL=old_solver,old_cert,old_rtol
raw=res['cjunc']['sv_counterfactual']
computed_ratio=raw['sv_counterfactual_ratio']
threshold=(computed_ratio+actual_ratio)/2 if computed_ratio is not None else actual_ratio
out['actual_certified_threshold_crossing']={**check_record(raw,threshold),'reference_full_G':exact_G,
    'reference_cut_G':exact_cut,'reference_true_ratio':actual_ratio,'threshold':threshold,
    'main_certificate':res.get('conv_cert'),'raw_lower_certificate':raw.get('conv_cert'),
    'solver_calls':calls[0],'perturbation':1.e-8}
mc,cc=res.get('conv_cert'),raw.get('conv_cert')
out['actual_certified_threshold_crossing']['certified_ratio_interval']=[mc['target_lo']/cc['target_hi'],mc['target_hi']/cc['target_lo']]
out['actual_certified_threshold_crossing']['computed_ratio']=computed_ratio
out['actual_certified_threshold_crossing']['certificate_ok']={'main':mc['ok'],'lower':cc['ok']}
deleted=copy.deepcopy(raw);deleted['conv_cert']=None
out['certificate_removed_from_certified_run']=check_record(deleted,threshold)

# Replay a real, successful certificate from the .44843 cut circuit alongside
# the different finite-upper fixture's legitimate end currents. Projection drops
# all the numeric fields that could expose this wrong certificate binding.
foreign=copy.deepcopy(finite_raw)
for end in (foreign,foreign['upper']):end['conv_cert']=copy.deepcopy(cc)
out['foreign_certificate_accepted']=check_record(foreign,6.)
out['foreign_certificate_accepted']['raw_certificate_I_bot']=cc['I_bot']
out['foreign_certificate_accepted']['raw_end_Gcuts']=[foreign['G_cut_code'],foreign['upper']['G_cut_code']]

# S1 original analytic false cut and nominal-volume review cases.
import test_ptfe_face_alpha as F
import ptfe_face_alpha as FA
import run_contract as CONTRACT
F.S3,F.FA,F.RC=S3,FA,CONTRACT
fa_log=io.StringIO()
with contextlib.redirect_stdout(fa_log),contextlib.redirect_stderr(fa_log):
    for fn in (F.t_f16,F.t_f17,F.t_f18,F.t_f19):
        try:fn()
        except Exception:traceback.print_exc();F.chk(fn.__name__+' uncaught',False)
(HERE/'s1_tests.log').write_text(fa_log.getvalue(),encoding='utf-8')
out['s1_regression']={'passed':F._ok,'failed':F._fail}

# Port and original branch probes are also saved numerically beyond regression pass labels.
out['port_variants']=[]
for tag,rows in [('base',T.rows_exact([T.T4_A,T.T4_B])),('reversed',T.rows_exact([T.T4_A[::-1],T.T4_B[::-1]])),
                 ('subdivided',T.rows_exact([T.T4_A,T.T4_B],step=.125)),('fid_renamed',T.rows_exact([T.T4_A,T.T4_B],fids=[20,10]))]:
    sid,reg,res=T._solve_full(rows,T.T4_N)
    out['port_variants'].append({'name':tag,'G':T.I_of(res,T.T4_N),'sigma':res['sigma_eff'],
                                  'i':T._pcells(reg,0,'i'),'j':T._pcells(reg,0,'j'),
                                  'system_digest':hashlib.sha256(b''.join(T.sys_bytes(res))).hexdigest()})

(HERE/'geometry_results.json').write_text(json.dumps(serial(out),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary={k:{kk:vv for kk,vv in v.items() if kk in ('G','sigma','problem','flags','independent_expected_G','reference_true_ratio','threshold','solver_calls','computed_ratio','certified_ratio_interval','certificate_ok')}
         for k,v in out.items() if isinstance(v,dict) and 'record' in v}
summary['regression']=out['author_regression'];summary['s1_regression']=out['s1_regression']
summary['record_mutations']={k:{'problem':v['problem'],'flags':v['flags']} for k,v in out['record_mutations'].items()}
print(json.dumps(serial(summary),ensure_ascii=False,indent=2))
