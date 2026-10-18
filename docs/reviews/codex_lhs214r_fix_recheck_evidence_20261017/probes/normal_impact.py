"""Independent normal-case regression using earlier reviewed fixture constructors.
All actual solver/getter implementations remain unchanged; N compares entire JSON.
"""
from pathlib import Path
import contextlib,csv,hashlib,importlib.util,io,json,os,sys,tarfile,tempfile,time
R=Path(__file__).resolve().parents[1];S=R/'source';B=R/'base';E=R/'evidence'
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',TMP=str(R/'tmp'),TEMP=str(R/'tmp'))
deps=[R.parent/'lhs_coverage_review_20260930/deps',R.parent/'gen2_network_reverify3_20261007/deps']
sys.path[:0]=list(map(str,[S/'scripts',S/'webapp',*deps]));os.environ['PYTHONPATH']=os.pathsep.join(map(str,deps))
sys.dont_write_bytecode=True;tempfile.tempdir=str(R/'tmp')
def load(path,name):
    sp=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(sp)
    with contextlib.redirect_stdout(io.StringIO()):sp.loader.exec_module(mod)
    return mod
a4=load(S/'docs/reviews/lhs214_fix_evidence_20261015/a4_no_impact.py','review_fixture')
import network_conductivity as nn, tau_flux as tn,lhs_release_build as rn
no=load(B/'scripts/network_conductivity.py','nc_old_normal');to=load(B/'scripts/tau_flux.py','tf_old_normal');ro=load(B/'scripts/lhs_release_build.py','rb_old_normal')
to._nc_mod=lambda:no
a4.L214_ADDED=() # No fields removed: exact whole-JSON equality for this revision.
out={'base':'6cb2569569ec74b7f5a96e0ef19494e872da5272','source':'60ba39e224aff48a030dccfe750342f3bf9db61f','rows':[],'method':'Earlier fixture constructors only; no claimed 10-16 A4 script available. N whole JSON, T old columns, R declared flag policy, W pre-final transform.'}
start=time.monotonic()
def add(x):
    out['rows'].append(x);(E/'normal_impact.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('N actual producer fixtures started',flush=True)
N,_,beds=a4.section_n(nn,no,False)
for x in N:add(x)
print('N',sum(x['identical'] for x in N),len(N),flush=True)
flags=['full_model_limit_hertz','full_model_limit_physics']
def without(d):return {k:v for k,v in d.items() if k not in flags}
with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='normal_tau_') as td:
    archive=S/'docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz'
    with tarfile.open(archive) as t:
        for m in t.getmembers():
            assert not m.issym() and not m.islnk() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts
        t.extractall(td,filter='data')
    bad=[];fs=[];cases=sorted((Path(td)/'cases').iterdir())
    for c in cases:
        cd=c/'work/results'/c.name;n,o=tn.case_row(cd),to.case_row(cd)
        if without(n)!=o:bad.append(c.name)
        fs.append([n.get(k) for k in flags])
    add({'section':'T','case':'194 historical cases all old cells','identical':not bad and len(cases)==194 and all(x==[False,False] for x in fs),'bad':bad,'flags_unique':list(map(list,set(map(tuple,fs))))})
for lab in ['합성 SE + AM (이온 · 전자 · 열 · H12)','real_14 (세 채널 · 커밋된 기준 덤프)','합성 진짜 비관통','합성 CF 모형 과전도 (상자 1 × 1)']:
    dual={m:beds[(lab,m)] for m in ('hertzian','physics')};pz=20.0 if lab.startswith('합성') else 30.2845
    ledger={'thickness_um':pz,'thickness_mass_conserving_um':pz*.97,'phi_se_mass_conserving':.5};perc=0. if '비관통' in lab else 100.
    def val(t):return {'cols':without(t.ion_columns(dual,ledger,perc)),'gen':t.network_generation_contract(dual),'problems':{m:t.ion_record_problem(t.mode_record(dual,m)) for m in t.MODES},'binding':{m:t.certificate_binding_problems(m,t.mode_record(dual,m)) for m in t.MODES}}
    n,o=val(tn),val(to);add({'section':'T','case':lab,'identical':n==o,'diff':a4.first_diff(n,o)})
with tarfile.open(S/'docs/reviews/codex_lhs214_failures_review_evidence_20261014/submitted/lhs214_run_evidence_1014_1520.tgz') as t:
    dual={m:json.load(t.extractfile(f'lhs214_run_evidence_1014_1520/diag_lhsx054/network_conductivity_{m}.json')) for m in ('hertzian','physics')}
ledger={'thickness_um':20.,'thickness_mass_conserving_um':19.,'phi_se_mass_conserving':.5}
n,o=without(tn.ion_columns(dual,ledger,100.)),to.ion_columns(dual,ledger,100.)
add({'section':'T','case':'lhsx_054 old diagnosed record','identical':n==o,'diff':a4.first_diff(n,o)})
for ds in ('lhs','lhsx'):
    p=S/f'docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/{ds}_handover_v12_20261006.csv'
    rr=list(csv.DictReader(p.open(encoding='utf8',newline='')));bad=[]
    for r in rr:
        for k in r:
            if rn.v13_blank_reason(r,k)!=ro.v13_blank_reason(r,k):bad.append((r['case_id'],k))
    for k in rr[0]:
        if k.startswith('ion_net_status_') and not k.startswith('ion_net_status_reason_'):
            if rn._v13_status_counts(rr,k)!=ro._v13_status_counts(rr,k):bad.append(('status',k))
    for r in rr:
        if rn._v13_class(r)!=ro._v13_class(r):bad.append(('class',r['case_id']))
    add({'section':'R','case':ds+' blank/class/status','identical':not bad,'bad':bad})
    n,o=rn.v13_primary_model_limit_problems(rr),ro.v13_primary_model_limit_problems(rr)
    add({'section':'R','case':ds+' historical missing flags refused','identical':bool(n) and not o,'new':n,'old':o,'intentional_change':True})
    rich=[dict(r,full_model_limit_hertz='False',full_model_limit_physics='False') for r in rr]
    pr=rn.v13_primary_model_limit_problems(rich)
    add({'section':'R','case':ds+' synthetic explicit flags admitted','identical':not pr,'problems':pr,'qualification':'synthetic gate test, not historical data upgrade'})
print('W pre-final transformation',flush=True)
nw,ow=a4.run_probe(str(S)),a4.run_probe(str(B))
for k in nw:add({'section':'W','case':k,'identical':nw[k]==ow[k],'diff':a4.first_diff(nw[k],ow[k])})
out['producer_errors']=[{'case':str(k),'error':v['__error__']} for k,v in beds.items() if '__error__' in v]
out['seconds']=time.monotonic()-start;out['pass']=sum(x['identical'] for x in out['rows']);out['total']=len(out['rows'])
(E/'normal_impact.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:out[k] for k in ('pass','total','seconds','producer_errors')},ensure_ascii=False),flush=True)
