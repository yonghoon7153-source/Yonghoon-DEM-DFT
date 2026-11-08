"""Independent narrow RR2/PC9/PC10 review. Synthetic regular files only.
Windows lacks O_NONBLOCK; set it to 0 solely for ordinary-file reads.
No POSIX FIFO, process, lock, host, or simulation qualification is claimed.
"""
import hashlib
import ast
import importlib.util
import json
import os
import platform
import re
import subprocess
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
REPO = Path(os.environ.get('RINT_REVIEW_REPO', str(ROOT / 'package' / 'repo'))).resolve()
OUT = ROOT / 'contracts_probe_results.json'
if not hasattr(os, 'O_NONBLOCK'):
    os.O_NONBLOCK = 0
spec = importlib.util.spec_from_file_location('rr3_contract_source', REPO/'scripts/rint_r_chain.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
rows = []
def ck(name, got, expected):
    rows.append({'name':name,'got':got,'expected':expected,'pass':got == expected})
def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(json.dumps(obj, allow_nan=False).encode())

# Expectations derived from int-only policy, not copied implementation tests.
for rc, kind in [(0,'ok'),(1,'fail'),(-9,'fail'),(False,'bad'),(True,'bad'),
                 (0.0,'bad'),(-0.0,'bad'),('0','bad'),(None,'none'),([], 'bad'),({},'bad')]:
    ck('rc_kind_'+repr(rc), m.rc_kind(rc), kind)
    ck('rc_success_'+repr(rc), m.rc_success(rc), kind == 'ok')

with tempfile.TemporaryDirectory(prefix='rr3_contract_',dir=ROOT) as td:
    base=Path(td)
    # actual orphan consumer: paired records + log + first-result marker.
    token='a'*32
    for i, rc in enumerate([0,1,False,0.0,-0.0,'0',None,True]):
        p=base/f'rc_{i}'
        write(p/m.GROUPS_DIR/'L01.launch.json',{'name':'L01','token':token})
        write(p/m.GROUPS_DIR/'L01.end.json',{'name':'L01','token':token,'by':'chain','cause':None,'rc':rc,'confirmed':True})
        write(p/'first.first_result.json',{})
        (p/'logs').mkdir()
        (p/'logs'/'L01.log').write_text('Traceback\nKeyError: sigma',encoding='utf8')
        got=m.result_fields(p,None)
        ck('orphan_'+repr(rc), [got['cause'],got['resume_ok']], ['parent_dead',True] if type(rc) is int and rc==0 else ['runner_rc',False])

    # Null-cause vs null rc -- same returned eligibility via recover wrapper.
    p=base/'recover'; p.mkdir()
    write(p/m.GROUPS_DIR/'L01.launch.json',{'name':'L01','token':token})
    write(p/'first.first_result.json',{})
    (p/'logs').mkdir(); (p/'logs'/'L01.log').write_text('Traceback',encoding='utf8')
    for rc in [1,False,0.0,'0',None]:
        write(p/m.GROUPS_DIR/'L01.end.json',{'name':'L01','token':token,'by':'recover','cause':'parent_dead','rc':None,'confirmed':True,'chain_end':{'cause':None,'rc':rc}})
        g=m.result_fields(p,None)
        ck('recover_'+repr(rc), [g['cause'],g['resume_ok']], ['runner_rc',False])

    for i,cause in enumerate(['not_a_cause',False,0,'',[],{}]):
        for by in ['chain','recover']:
            p=base/f'unknown_cause_{i}_{by}'; p.mkdir()
            write(p/m.GROUPS_DIR/'L01.launch.json',{'name':'L01','token':token})
            end={'name':'L01','token':token,'by':by,'confirmed':True,'cause':cause,'rc':1}
            if by=='recover': end.update(cause='parent_dead',rc=None,chain_end={'cause':cause,'rc':1})
            write(p/m.GROUPS_DIR/'L01.end.json',end)
            write(p/'first.first_result.json',{})
            (p/'logs').mkdir(); (p/'logs'/'L01.log').write_text('MemoryError',encoding='utf8')
            ck('unknown_cause_resume_'+str(i)+'_'+by,m.result_fields(p,None)['resume_ok'],False)

    # Canonical producer tuples, independently enumerated from Runner._execute.
    shapes=[(None,0,'exit_ok'),(None,1,'exit_fail'),('timeout',None,'killed:timeout'),
            ('signal',None,'killed:signal'),('signal_after',None,'killed:signal_after')]
    for cause,rc,expected in shapes:
        ck('shape_'+repr((cause,rc)),m.run_record_shape({'group_cause':cause,'rc':rc}),expected)
    for cause,rc in [(None,None),(None,False),(None,0.0),('timeout',1),('signal',0),('signal_after',False),('unknown',None)]:
        ck('shape_reject_'+repr((cause,rc)),m.run_record_shape({'group_cause':cause,'rc':rc}),'bad')

    texts={'plain':'','python':'Traceback\nKeyError: sigma','oom':'CUDARuntimeError: cudaErrorMemoryAllocation',
           'host':'MemoryError','disk':'No space left on device','gpu':'CUDA_ERROR_OUT_OF_MEMORY','cupy_oom':'OutOfMemoryError'}
    for label,text in texts.items():
        p=base/f'summary_{label}'; p.mkdir(); write(p/'first.first_result.json',{})
        (p/'logs').mkdir(); (p/'logs'/'L01.log').write_text(text,encoding='utf8')
        s={'status':'STOPPED','stop':{'code':'TIME_LIMIT','run':'L01'},'runs':[{'name':'L01','outdir':'L01','rc':None,'group_cause':None,'arms_read':[]}]}
        g=m.result_fields(p,s)
        ck('old_TIME_LIMIT_None_'+label,[g['cause'],g['resume_ok']],['runner_rc' if label in ('plain','python') else 'resource',False])

    # Registered missing-log defect, and real producer positive twin.
    p=base/'log_status'; p.mkdir(); write(p/'first.first_result.json',{})
    s={'status':'STOPPED','stop':{'code':'TIME_LIMIT','run':'L01'},'runs':[{'name':'L01','outdir':'L01','rc':None,'group_cause':'timeout','arms_read':[]}]}
    ck('missing_log_resume',m.result_fields(p,s)['resume_ok'],False)
    (p/'logs').mkdir(); (p/'logs'/'L01.log').write_text('',encoding='utf8')
    ck('readable_log_producer_timeout',m.result_fields(p,s)['resume_ok'],True)
    (p/'logs'/'L01.log').unlink(); (p/'logs'/'L01.log').mkdir()
    ck('directory_log_resume',m.result_fields(p,s)['resume_ok'],False)

    for kind in ['none','end','log','output']:
        p=base/f'prerun_{kind}'; p.mkdir(); write(p/'prior.first_result.json',{})
        s={'status':'STOPPED','stop':{'code':'TIME_LIMIT','run':'L02'},'runs':[]}
        if kind=='end': write(p/m.GROUPS_DIR/'L02.end.json',{})
        elif kind=='log': (p/'logs').mkdir(); (p/'logs'/'L02.log').write_text('',encoding='utf8')
        elif kind=='output': (p/'L02_arm1').mkdir()
        ck('prerun_exception_'+kind,m.result_fields(p,s)['resume_ok'],kind=='none')

    # Missing summary is distinct from present-but-unreadable. Verdict early gate.
    p=base/'summary_read'; p.mkdir()
    for name,raw in [('truncated',b'{'),('list',b'[]'),('boolean',b'true'),('duplicate',b'{"status":"OK","status":"STOPPED"}'),('nan',b'{"status":"STOPPED","x":NaN}')]:
        (p/'ladder_summary.json').write_bytes(raw)
        ck('summary_state_'+name,m.read_summary_state(p,'ladder_summary.json')[2],'unreadable')
        try:
            m._verdict_compute([p],None,None,None,lambda:None)
            outcome='RETURNED'
        except m.Stop as ex:
            outcome=ex.code
        ck('verdict_reject_'+name,outcome,'INPUT_NOT_STAGE')
    (p/'ladder_summary.json').unlink()
    ck('summary_absent',m.stage_summary_read(p), (None,'absent'))

    # recover parser rejects non-object rejected bytes without AttributeError.
    for i,raw in enumerate([b'[]',b'null',b'true',b'1',b'{',b'{"code":"X","code":"Y"}']):
        f=base/f'rejected_{i}.json'; f.write_bytes(raw)
        try: m.rejected_record(f,'independent'); outcome='RETURNED'
        except m.Stop as ex: outcome=ex.code
        ck('rejected_'+str(i),outcome,'ATTEMPT_LEDGER_MISMATCH')

# Execute only the scanner definition extracted from the pinned test source;
# independent expressions, no full selftest/environment initialization.
src=(REPO/'scripts/test_rint_r_chain.py').read_text(encoding='utf8')
tree=ast.parse(src)
names={'RC_READERS','RC_MSG_CALLS','RC_QUOTED'}
nodes=[n for n in tree.body if (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets)) or (isinstance(n,ast.FunctionDef) and n.name=='rc_scan')]
ns={'ast':ast,'re':re}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(REPO/'scripts/test_rint_r_chain.py'),'exec'),ns)
for name,code in {
    'false_eq':"def f(x):\n return x.get('rc') == 0\n",
    'bool_alias':"def f(x):\n q=x['rc']\n return not q\n",
    'dict_get':"def f(x):\n return dict.get(x,'rc') == 0\n",
    'pop':"def f(x):\n return x.pop('rc') == 0\n",
    'closure':"def f(x):\n q=x.get('rc')\n def inner():\n  return q == 0\n return inner()\n",
    'formatted_compare':"def f(x):\n return f\"{x.get('rc')}\" == '0'\n",
}.items():
    ck('scanner_independent_bad_'+name, bool(ns['rc_scan'](code)),True)
ck('scanner_reader_positive',ns['rc_scan']("def f(x):\n return rc_success(x.get('rc'))\n"),[])
ck('scanner_pinned_source',ns['rc_scan']((REPO/'scripts/rint_r_chain.py').read_text(encoding='utf8')),[])

# Document changes: recompute budget without writing source, compare semantic JSON
# and normalized stdout bytes (Windows stdout LF conversion is not source mutation).
budget=subprocess.run([sys.executable,'-I','-B','-X','utf8',str(REPO/'docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.py')],capture_output=True,check=True).stdout.replace(b'\r\n',b'\n')
before=(REPO/'docs/reviews/rint2_rr2_fix_evidence_20261105/logs/q9_time_budget_before.out').read_bytes().replace(b'\r\n',b'\n')
ck('q9_budget_stdout_normalized_bytes',budget==before,True)
ck('q9_budget_stored_json',json.loads(budget),json.loads((REPO/'docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json').read_text(encoding='utf8')))
reg=(REPO/'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md').read_text(encoding='utf8')
code=(REPO/'scripts/carbon_junction.py').read_text(encoding='utf8')
fix=next(x for x in reg.splitlines() if x.startswith('필수 한정어:')).split('→ 11-05 정정 (RR2-03',1)[1].split('⑬',1)[0]
quote=re.findall(r'\*"(.+?)"\*',fix)
qualifiers=next(ast.literal_eval(n.value) for n in ast.parse(code).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CJUNC_QUALIFIERS' for t in n.targets))
ck('ban8_quote_exact_source_constant',len(quote)==1 and quote[0] in qualifiers[3],True)
for word in ['Δ/λ 0.02 – 0.63','q 0.4 – 19','긴 접촉 포화 = 축저항 몫을 뺀 접합 기여분','임의 교차 · 비스듬한 접합은 식 검증되지 않았다']:
    ck('ban8_document_'+word,word in fix,True)

result={'environment':{'python':sys.version,'platform':platform.platform(),
        'limitation':'Windows regular-file synthetic checks; O_NONBLOCK=0 shim only; no FIFO/process/lock/host execution'},
        'source_sha256':hashlib.sha256((REPO/'scripts/rint_r_chain.py').read_bytes()).hexdigest(),
        'passed':sum(r['pass'] for r in rows),'total':len(rows),'rows':rows}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:result[k] for k in ['source_sha256','passed','total']}))
sys.exit(0 if all(r['pass'] for r in rows) else 1)
