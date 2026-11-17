"""Actual S0 commitment gate on tiny synthetic git history; no census/engine execution."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[2];WORK=ROOT/'seal_form_review/work'
sys.dont_write_bytecode=True
sys.path[:0]=[str(WORK/'deps'),str(WORK/'scripts')]
import ca_s0_census as S, rint_r_chain as R
ORIG_RUN=subprocess.run
def safe_run(cmd,*args,**kw):
    if isinstance(cmd,list) and cmd and cmd[0]=='git':
        directory=cmd[cmd.index('-C')+1] if '-C' in cmd else kw.get('cwd',str(WORK))
        cmd=['git','-c','safe.directory='+str(directory)]+cmd[1:]
        env=dict(kw.get('env',os.environ));env.update(GIT_NO_LAZY_FETCH='1',GIT_OPTIONAL_LOCKS='0');kw['env']=env
    return ORIG_RUN(cmd,*args,**kw)
subprocess.run=safe_run
X=ROOT/'input/extra/seal_candidate_v2_1'
sealed='docs/reviews/rint2_seal_20261120/registration_R_sealed.md'
original='docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md'
plan='docs/data/rint2_r_plan_20261120/ca1_plan.json'
s0='docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json'
logs={'test_only':True,'note':'Tiny synthetic Git history, not an R seal. Four final values are test fixtures from probe_form_build.py.', 'cases':[]}
with tempfile.TemporaryDirectory(prefix='s0_gate_TEST_ONLY_',dir=WORK) as td:
    repo=Path(td)
    def git(*args):
        return subprocess.run(['git','-C',str(repo),'-c','user.name=synthetic-review','-c','user.email=synthetic@invalid','-c','commit.gpgsign=false',*args],capture_output=True,check=True).stdout.decode().strip()
    def write(rel,data):
        p=repo/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    git('init','-q');git('config','core.autocrlf','false')
    for rel in (sealed,original,plan):write(rel,(X/'build_20261120'/rel).read_bytes())
    write(s0,(ROOT/'input/repo'/s0).read_bytes())
    git('add','.');git('commit','-qm','TEST ONLY candidate, four null');cand=git('rev-parse','HEAD')
    def gate(label,commit,doc,want):
        try:
            result=S.verify_plan_commit(str(repo),commit,s0,doc,r_plan_path=plan)
            actual='PASS'
            info={'plan_hash':result[1],'commit':result[2],'R_plan_hash':result[3]['sha256']}
        except S.S0Error as e:actual='REJECT: '+str(e);info=None
        logs['cases'].append({'case':label,'expected':want,'actual':actual,'pass':(actual==want if want=='PASS' else want in actual),'info':info})
    gate('candidate + sealed r_doc rejects four null',cand,sealed,'PLAN_NUMBER_UNREGISTERED')
    gate('candidate + original default rejects blank S0 hash',cand,original,'끝 칸 ≠ 계획 sha256')
    for rel in (sealed,plan):write(rel,(WORK/'TEST_ONLY_final_output'/rel).read_bytes())
    git('add','.');git('commit','-qm','TEST ONLY filled fixture, not registered values');final=git('rev-parse','HEAD')
    gate('fixture final + sealed r_doc accepted',final,sealed,'PASS')
    gate('fixture final + original default rejects blank S0 hash',final,original,'끝 칸 ≠ 계획 sha256')
    gate('candidate ancestor still rejects when HEAD is fixture final',cand,sealed,'PLAN_NUMBER_UNREGISTERED')
    bad=json.loads((repo/plan).read_bytes());bad['sv_cf_threshold']=3.0
    write(plan,json.dumps(bad,indent=1,sort_keys=True).encode('ascii'));git('add','.');git('commit','-qm','TEST ONLY mismatching plan bytes');mismatch=git('rev-parse','HEAD')
    gate('different plan committed without rehash rejects',mismatch,sealed,'≠ 등록 "| 계획 해시 |"')
logs['overall']='PASS' if all(c['pass'] for c in logs['cases']) else 'FAIL'
print(json.dumps(logs,ensure_ascii=False,indent=2))
sys.exit(0 if logs['overall']=='PASS' else 1)
