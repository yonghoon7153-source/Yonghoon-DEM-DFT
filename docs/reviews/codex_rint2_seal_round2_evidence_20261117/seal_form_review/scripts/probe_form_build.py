"""Small synthetic seal-form checks; all four filled values are test fixtures only."""
from pathlib import Path
import argparse, contextlib, copy, hashlib, importlib.util, io, json, os, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
INP = ROOT / 'input'
X = INP / 'extra/seal_candidate_v2_1'
WORK = ROOT / 'seal_form_review/work'
CHAIN = WORK / 'scripts/rint_r_chain.py'
sys.dont_write_bytecode = True
sys.path.insert(0,str(WORK/'deps'))
spec = importlib.util.spec_from_file_location('seal_maker', X / 'make_sealed_copy.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
ORIG_RUN = subprocess.run
def run_lf(cmd, *args, **kw):
    # A Windows host prints CRLF; the target operational host is Linux.
    # Alter only the stdout newline convention, never the returned plan bytes.
    if isinstance(cmd, list) and '--stage' in cmd and 'plan-doc' in cmd:
        idx = cmd.index(str(CHAIN.resolve()))
        shim = "import runpy,sys;sys.stdout.reconfigure(newline='\\n');sys.argv=sys.argv[1:];runpy.run_path(sys.argv[0],run_name='__main__')"
        cmd = cmd[:idx] + ['-B', '-c', shim] + cmd[idx:]
    return ORIG_RUN(cmd, *args, **kw)
M.subprocess.run = run_lf
BASE = argparse.Namespace(
    pin_reg=str(INP/'repo'/M.REG_REL), pin_cmd=str(INP/'repo'/M.CMD_REL),
    reg_insert=str(X/'registration_R_insert.md'),cmd_insert=str(X/'commands_doc_insert.md'),
    plan=str(X/'plan_candidate.json'),
    s0_plan=str(INP/'repo/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json'),
    chain=str(CHAIN),seal_date='20261120',seal_branch=None,out=None,final=False)
logs={'test_only':True,'scope':'No engine, kit, result JSON, live host, or real seal. Input/source immutable.',
      'platform_note':'Windows stdout is forced to LF only for the unmodified chain plan-doc subprocess; synthetic calls otherwise use shipped code.', 'cases':[]}
import numpy, scipy
logs['local_test_versions']={'python':sys.version.split()[0],'numpy':numpy.__version__,'scipy':scipy.__version__}
def record(name, want, fn):
    try:
        value = fn()
        got = value if isinstance(value, str) else 'PASS'
    except (M.Fail, Exception) as e:
        got = type(e).__name__ + ': ' + str(e)
    ok = got == want if want == 'PASS' else want in got
    logs['cases'].append({'case':name,'expected':want,'actual':got,'pass':ok})
    return got
def a(**kw):
    b=copy.copy(BASE)
    for k,v in kw.items(): setattr(b,k,v)
    return b
def build_matches():
    one,man=M.build(a()); two,man2=M.build(a())
    assert one==two and man==man2
    for p,b in one.items(): assert b==(X/'build_20261120'/p).read_bytes(),p
    logs['candidate_output_sha256']={p:hashlib.sha256(b).hexdigest() for p,b in one.items()}
    return 'PASS'
record('candidate same inputs => exact supplied output bytes, twice','PASS',build_matches)
record('--final with four null fields','PLAN_NUMBER_UNREGISTERED',lambda:M.build(a(final=True)))
plan=json.loads((X/'plan_candidate.json').read_bytes())
FIXTURE={'max_ladder_points':12,'calib_rj_ratio_max':'none','sv_cf_threshold':2.0,'sv_cf_scope':'all3'}
logs['fixture_values_NOT_registration_decision']=FIXTURE
plan.update(FIXTURE)
def wplan(tag,obj):
    p=WORK/(tag+'.json');p.write_bytes(json.dumps(obj,indent=1,sort_keys=True).encode('ascii'));return str(p)
fp=wplan('TEST_ONLY_final_plan',plan)
def fixture():
    outputs,man=M.build(a(plan=fp,final=True))
    target=WORK/'TEST_ONLY_final_output'
    if target.exists():
        assert all((target/p).read_bytes()==b for p,b in outputs.items())
    else:
        M.write_out(str(target),outputs,man)
    R=M.load_chain(str(CHAIN))
    sealed=target/man['sealed_rel']
    assert R.registration_plan_hash(sealed)[0] == hashlib.sha256(Path(fp).read_bytes()).hexdigest()
    assert R.plan_doc_problem(sealed,plan) is None
    R.require_plan_numbers(plan)
    return 'PASS'
record('four fixture values + --final build and parser match','PASS',fixture)
R=M.load_chain(str(CHAIN))
def stop_code(fn):
    try:fn()
    except R.Stop as e:return e.code
    return 'ACCEPTED'
record('marked original plan hash remains unregistered','PLAN_HASH_UNREGISTERED',lambda:stop_code(lambda:R.registration_plan_hash(X/'build_20261120'/M.REG_REL)))
record('marked original S0 hash remains unregistered','S0_PLAN_HASH_UNREGISTERED',lambda:stop_code(lambda:R.registration_s0_hash(X/'build_20261120'/M.REG_REL)))
record('wrong tolerance plan rejected before output','두 계획 대조',lambda:M.build(a(plan=wplan('TEST_ONLY_wrong_tol',dict(plan,tol_ff_um=0.07)),final=True)))
record('unknown length-law rejected before output','두 계획 대조',lambda:M.build(a(plan=wplan('TEST_ONLY_wrong_law',dict(plan,len_law='len_scaled_v9')),final=True)))
record('SV threshold below one rejected','PLAN_INVALID',lambda:M.build(a(plan=wplan('TEST_ONLY_wrong_sv',dict(plan,sv_cf_threshold=0.5)),final=True)))
record('calendar-invalid seal date rejected','달력 날짜',lambda:M.build(a(seal_date='20260230')))
record('Git-invalid branch rejected','git 가지 이름',lambda:M.build(a(seal_branch='bad//ref')))
record('final copied plan to another path => byte-identical files','PASS',lambda: 'PASS' if M.build(a(plan=wplan('TEST_ONLY_copy_plan',plan),final=True))[0] == M.build(a(plan=fp,final=True))[0] else 'DIFFERENT')
logs['overall']='PASS' if all(e['pass'] for e in logs['cases']) else 'FAIL'
print(json.dumps(logs,ensure_ascii=False,indent=2))
sys.exit(0 if logs['overall']=='PASS' else 1)
