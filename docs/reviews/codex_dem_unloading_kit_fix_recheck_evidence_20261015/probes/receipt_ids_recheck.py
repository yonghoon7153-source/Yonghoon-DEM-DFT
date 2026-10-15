"""Independent Q2/Q3 probes against the pinned snapshot; no simulation.

The included copy of the old independent fixture builder is loaded as a
definition via AST, so its old probes are not executed. New cases/assertions and
all outputs belong to this review. Arm input serialization uses _mk_arm only;
the verdict, selection, and gate functions are actual production functions.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import copy
import hashlib
import inspect
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'source/docs/data/ps45_unload_20261009'
sys.path.insert(0, str(KIT))
import ul_lib as L
import ul_reader as R
import ul_gates as G
import ul_s3 as S

P = L.load_params()
BED = R.B73
B = P['beds'][BED]
S0 = B['s0']
END = S0 + P['windows']['R_steps']
E = ROOT / 'evidence' / ('receipt_ids_cases_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
E.mkdir(parents=True)
OUT = {'pin': 'eaecfba2a2dfbff6f13222f6afeb01d8ebeb5a84', 'fixture_root': str(E), 'cases': {},
       'sources': {n: hashlib.sha256((KIT/n).read_bytes()).hexdigest() for n in ('ul_lib.py','ul_reader.py','ul_gates.py','ul_s3.py','run_unload.sh')}}
OUT['functions'] = {n: {'file': Path(inspect.getsourcefile(f)).name, 'line': inspect.getsourcelines(f)[1]}
                    for n, f in [('_job_receipt',R._job_receipt),('_job_restored',R._job_restored),('gate',R.gate),
                                 ('exact_id',L.exact_id),('_contacts',G._contacts),('restore_verdict',R.restore_verdict)]}

def put(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def js(path, obj):
    put(path, json.dumps(obj, ensure_ascii=False, indent=2))

def record(name, data, expected=None, matches=None):
    OUT['cases'][name] = {'actual': data, 'expected': expected, 'matches': matches}

def attempt(fn):
    try:
        return {'returned': fn()}
    except Exception as ex:
        return {'exception': type(ex).__name__, 'message': str(ex)}

def replace(path, old, new):
    txt = path.read_text(encoding='utf-8')
    assert old in txt, (path, old)
    put(path, txt.replace(old, new))

def edit_token(path, col, value, row=0):
    lines = path.read_text(encoding='utf-8').splitlines()
    hi = next(i for i, ln in enumerate(lines) if ln.startswith(('ITEM: ATOMS ', 'ITEM: ENTRIES ')))
    ci = lines[hi].split()[2:].index(col)
    tokens = lines[hi + 1 + row].split()
    tokens[ci] = str(value)
    lines[hi + 1 + row] = ' '.join(tokens)
    put(path, '\n'.join(lines) + '\n')

# Reuse only the previous review's independent baseline constructor, not its
# verdicts, calls, mutations, or any production selftest assertions.
old_path = ROOT / 'support/previous_restore_baseline.py'
old_tree = ast.parse(old_path.read_text(encoding='utf-8'))
builder = next(n for n in old_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'baseline')
exec(compile(ast.Module(body=[builder], type_ignores=[]), str(old_path), 'exec'), globals())
OUT['fixture_builder'] = {'source': str(old_path), 'sha256': hashlib.sha256(old_path.read_bytes()).hexdigest(),
                          'original_source': 'dem_unloading_kit_reverify_20261014/probes/runner_recheck.py',
                          'original_sha256': '61662b0f662473d67cf2024e32bc79aec8a4b647772ac39747e2563b4b5db3bb',
                          'scope': 'baseline function only; new grammar prerequisite line added for current protocol'}
GOOD = json.loads((ROOT/'evidence/history_reread.json').read_text(encoding='utf-8'))
TEMPLATE = E / 'restore_template'
baseline(TEMPLATE)
man = TEMPLATE/BED/'RJ/run_manifest.txt'
replace(man, 'resume=0\n', 'resume=0\ngrammar_prereq=PASS\n')
js(TEMPLATE/'history.json', GOOD)

def restored_case(name, mutate=None):
    root = E/name
    shutil.copytree(TEMPLATE, root)
    j = root/BED/'RJ'
    if mutate:
        mutate(root,j)
    result = attempt(lambda: R.restore_verdict(str(root),BED,'RJ',str(root/'history.json'),P))
    if 'returned' in result:
        js(j/'restore_verdict.json',result['returned'])
        result['next_UB'] = R.gate(str(root),BED,'UB',P)
    return root,j,result

root,j,v = restored_case('restore_positive')
record('restore_positive',v,'RESTORED and UB allowed',v['returned']['status']=='RESTORED' and v['next_UB'][0])
assert OUT['cases']['restore_positive']['matches'],v

receipts = {
    'reader_nonzero':'end=x fails=0 reader_rc=120\n',
    'fails_nonzero':'end=x fails=1 reader_rc=0\n',
    'missing_reader':'end=x fails=0\n',
    'missing_fails':'end=x reader_rc=0\n',
    'reader_text':'end=x fails=0 reader_rc=x\n',
    'reader_fraction':'end=x fails=0 reader_rc=0.0\n',
    'reader_negative':'end=x fails=0 reader_rc=-1\n',
    'reader_duplicate':'end=x fails=0 reader_rc=0 reader_rc=0\n',
    'fails_duplicate':'end=x fails=0 fails=0 reader_rc=0\n',
    'no_end':'',
    'latest_failure':'end=old fails=0 reader_rc=0\nend=new fails=0 reader_rc=1\n',
    'positive':'end=x fails=0 reader_rc=0\n',
}
for name,end in receipts.items():
    root,j,v = restored_case('receipt_'+name,lambda r,j,end=end: replace(j/'run_manifest.txt','end=x fails=0 reader_rc=0\n',end))
    expect = name == 'positive'
    record('receipt_'+name,v,'UB allowed' if expect else 'UB refused',v['next_UB'][0] is expect and v['returned']['status']=='RESTORED')
root,j,v = restored_case('receipt_no_grammar',lambda r,j: replace(j/'run_manifest.txt','grammar_prereq=PASS\n',''))
record('receipt_no_grammar',v,'UB refused',not v['next_UB'][0])

for name,end in receipts.items():
    root = E/('rj2_'+name)
    js(root/R.B100/'s0_decision.json',{'status':'PASS','s0':3660000})
    put(root/R.B100/'EXT/run_manifest.txt',f'bed={R.B100}\njob=EXT\ngrammar_prereq=PASS\n'+end)
    gate = R.gate(str(root),R.B100,'RJ2',P)
    record('rj2_'+name,gate,'RJ2 allowed' if name=='positive' else 'RJ2 refused',gate[0] is (name=='positive'))

# Actual unchanged command exits after publishing its certificate/base file.
root,j,_ = restored_case('actual_restore_stdout_failure')
(j/'restore_verdict.json').unlink()
(root/BED/'ul_base.in').unlink()
rcs = {}
for cmd,args in [('restore',[str(root),BED,'--hist',str(root/'history.json')]),('kebase',[str(root),BED])]:
    argv=[sys.executable,'-X','utf8','-B','-I',str(KIT/'ul_reader.py'),cmd,*args]
    with (root/(cmd+'_stderr.txt')).open('wb') as err:
        proc=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=err)
        proc.stdout.close()
        rcs[cmd]=proc.wait(timeout=30)
    replace(j/'run_manifest.txt',f'reader_{cmd}_rc=0',f'reader_{cmd}_rc={rcs[cmd]}')
aggregate = 2 if rcs['kebase'] else rcs['restore']
replace(j/'run_manifest.txt','end=x fails=0 reader_rc=0',f'end=x fails=0 reader_rc={aggregate}')
rv=json.loads((j/'restore_verdict.json').read_text(encoding='utf-8'))
gt=R.gate(str(root),BED,'UB',P)
record('actual_restore_stdout_failure',{'rcs':rcs,'restore_status':rv['status'],'base_exists':(root/BED/'ul_base.in').exists(),'gate':gt,
       'scope':'Real CLI commands; aggregate manifest constructed exactly as runner reader()/kebase branch. No Bash or LMP.'},
       'Nonzero command exits after files; UB refused',all(rcs.values()) and rv['status']=='RESTORED' and not gt[0])

# All restoration observation paths and original S0 reject malformed IDs.
obs = {'PRE':('R/obs/pre_bot.dump',S0),'POST':(f'R/obs/post_atom_{S0}.dump',S0),
       'R_END':('R/obs/end_pre_bot.dump',END),'UN':('UN/obs/un_pre_bot.dump',END)}
for obs_name,(rel,step) in obs.items():
    for tag,tok in [('fraction','1.5'),('zero','0'),('negative','-1'),('nan','nan'),('inf','inf')]:
        root,j,v=restored_case(f'id_{obs_name}_{tag}',lambda r,j,rel=rel,tok=tok:edit_token(j/rel,'id',tok))
        record(f'id_{obs_name}_{tag}',v,'Non-RESTORED, UB refused, no exception',
               'returned' in v and v['returned']['status']!='RESTORED' and not v['next_UB'][0])
    root,j,v=restored_case(f'id_{obs_name}_missing',lambda r,j,rel=rel:replace(j/rel,'ITEM: ATOMS id ','ITEM: ATOMS wrong_id '))
    record(f'id_{obs_name}_missing',v,'Non-RESTORED, UB refused, no exception','returned' in v and v['returned']['status']!='RESTORED' and not v['next_UB'][0])
for tag,tok in [('fraction','1.5'),('zero','0'),('negative','-1'),('missing',None)]:
    def s0mut(r,j,tok=tok):
        path=r/BED/'in'/f'atom_{S0}.liggghts'
        if tok is None: replace(path,'ITEM: ATOMS id ','ITEM: ATOMS wrong_id ')
        else: edit_token(path,'id',tok)
    root,j,v=restored_case('id_S0_'+tag,s0mut)
    record('id_S0_'+tag,v,'Non-RESTORED, UB refused, no exception','returned' in v and v['returned']['status']!='RESTORED' and not v['next_UB'][0])

# G2c both reference slots, malformed required columns, and actual restore.
for col in ('c_cpl[7]','c_cpl[8]'):
    for tag,tok in [('fraction','1.5'),('zero','0'),('negative','-1'),('missing',None)]:
        def cmut(r,j,col=col,tok=tok):
            path=j/'R/g2'/f'contact_{S0}.liggghts'
            if tok is None: replace(path,col,'not_'+col)
            else: edit_token(path,col,tok)
        name='g2c_'+col.replace('[','').replace(']','')+'_'+tag
        root,j,v=restored_case(name,cmut)
        direct=attempt(lambda:G.g2c_compare(str(j/'R/g2'/f'contact_{S0}.liggghts'),str(root/BED/'in'/f'contact_{S0}.liggghts')))
        record(name,{'restore':v,'G2c':direct},'Structured non-PASS, no exception',
               'returned' in v and v['returned']['status']!='RESTORED' and 'returned' in direct and direct['returned']['status']!='PASS')

# Real CLI propagation of the missing-column defect: no stale certificate is
# installed, and the next gate remains fail-closed despite the unhandled error.
root=E/'g2c_c_cpl7_missing'
j=root/BED/'RJ'
argv=[sys.executable,'-X','utf8','-B','-I',str(KIT/'ul_reader.py'),'restore',str(root),BED,'--hist',str(root/'history.json')]
proc=subprocess.run(argv,capture_output=True,text=True,encoding='utf-8',timeout=30)
put(root/'restore_cli_stderr.txt',proc.stderr)
record('g2c_missing_column_actual_cli',{'rc':proc.returncode,'stderr':proc.stderr,
       'certificate_exists':(j/'restore_verdict.json').exists(),'next_UB':R.gate(str(root),BED,'UB',P)},
       'Defect scope: unhandled KeyError, not a false RESTORED certificate',proc.returncode!=0 and not (j/'restore_verdict.json').exists() and not R.gate(str(root),BED,'UB',P)[0])

atoms,contacts,_=S._chain()
s0ids={a['id'] for a in atoms}
positive=S.s3_residual(atoms,contacts,s0ids,.005,atom_step=1,contact_step=1)
record('s3_direct_positive',positive,'PASS',positive['status']=='PASS')
assert positive['status']=='PASS'
for slot in ('atom_id','pair_id1','pair_id2'):
    for tag,value in [('fraction',1.5),('zero',0),('negative',-1),('bool',True),('text','1'),('over_max',2**53+1)]:
        aa,cc=copy.deepcopy(atoms),copy.deepcopy(contacts)
        if slot=='atom_id':aa[0]['id']=value
        else:cc[0][slot.removeprefix('pair_')]=value
        v=attempt(lambda:S.s3_residual(aa,cc,s0ids,.005,atom_step=1,contact_step=1))
        record('s3_direct_'+slot+'_'+tag,v,'NOT_COMPUTED, no exception','returned' in v and v['returned']['status']=='NOT_COMPUTED')

def arm(root,job):
    steps=R._ladder([.2,.25,.3,.35],[1.2,.8,.6,.4])
    for i,row in enumerate(steps[1:],1):
        row['kind']='A' if i==1 else 'B'
        row.pop('n_move',None)
    spec={'W':10000 if job in ('UT','UVb') else 5000,'dt':5e-7 if job in ('UT','UVb') else 1e-6,
          'steps':steps,'full_frames':True,'events':[('CROSS',2,'first'),('RM',4,'ncross2')],
          'summary':'RM_STOP' if job=='UT' else 'TIMEOUT'}
    d=Path(R._mk_arm(str(root),BED,job,spec,P))
    put(d/'run_check.txt',f'{job} screen.txt PASS rc=0 procs=6\n')
    put(d/'run_manifest.txt',f'bed={BED}\njob={job}\nresume=0\ngate=ALLOW\nreader_arm_rc=0\nend=x fails=0 reader_rc=0\n')
    return d

def arm_root(name,jobs=('UB','UT')):
    root=E/name
    for job in jobs: arm(root,job)
    R._fake_restored(str(root),BED)
    put(root/BED/'ul_base.in','variable ul_S2max equal 1e-5\n')
    return root

root=arm_root('arm_positive')
v=R.arm_verdict(str(root/BED/'UT'),BED,'UT',P,root=str(root))
gt=R.gate(str(root),BED,'UVa',P)
record('arm_positive',{'verdict':v,'selection':R.selection_state(str(root),P),'gate':gt},'Primary OK, UVa allowed',v['primary_status']=='OK' and gt[0])
assert OUT['cases']['arm_positive']['matches']
for tag,tok in [('fraction','2.5'),('zero','0'),('negative','-2'),('missing',None)]:
    root=arm_root('arm_id_'+tag)
    d=root/BED/'UT'
    step=R.read_run(str(d),P)['steps'][2]['step']
    path=d/'dump'/f'atom_{step}.dump'
    if tok is None:replace(path,'ITEM: ATOMS id ','ITEM: ATOMS wrong_id ')
    else:edit_token(path,'id',tok,row=1)
    v=attempt(lambda:R.arm_verdict(str(d),BED,'UT',P,root=str(root)))
    gate=R.gate(str(root),BED,'UVa',P)
    record('arm_id_'+tag,{'arm':v,'gate':gate},'UNIDENTIFIED, UVa refused, no exception','returned' in v and v['returned']['primary_status']=='UNIDENTIFIED' and not gate[0])
for col in ('c_cpl[7]','c_cpl[8]'):
    for tag,tok in [('fraction','2.5'),('missing',None)]:
        root=arm_root('arm_contact_'+col.replace('[','').replace(']','')+'_'+tag)
        d=root/BED/'UT'
        step=R.read_run(str(d),P)['steps'][2]['step']
        path=d/'dump'/f'contact_{step}.dump'
        if tok is None:replace(path,col,'wrong_'+col)
        else:edit_token(path,col,tok)
        v=attempt(lambda:R.arm_verdict(str(d),BED,'UT',P,root=str(root)))
        gate=R.gate(str(root),BED,'UVa',P)
        record(root.name,{'arm':v,'gate':gate},'UNIDENTIFIED, UVa refused, no exception','returned' in v and v['returned']['primary_status']=='UNIDENTIFIED' and not gate[0])

# Q2 deliberately recomputes arms. Capture the exact scope, without asserting
# that a stdout error changes valid physics or that late failure spoils earlier
# valid primary observations. Both unchanged readers and gate are exercised.
for mode in ('reader_stdout','stage_error','running_no_end'):
    root=arm_root('arm_failure_'+mode)
    d=root/BED/'UT'
    if mode=='reader_stdout':
        with (d/'cli_stderr.txt').open('wb') as err:
            proc=subprocess.Popen([sys.executable,'-X','utf8','-B','-I',str(KIT/'ul_reader.py'),'arm',str(root),BED,'UT'],stdout=subprocess.PIPE,stderr=err)
            proc.stdout.close();rc=proc.wait(timeout=30)
        replace(d/'run_manifest.txt','reader_arm_rc=0',f'reader_arm_rc={rc}')
        replace(d/'run_manifest.txt','end=x fails=0 reader_rc=0',f'end=x fails=0 reader_rc={rc}')
    elif mode=='stage_error':
        put(d/'screen.txt',(d/'screen.txt').read_text(encoding='utf-8')+'ERROR: synthetic late process failure\n')
        put(d/'run_check.txt','UT screen.txt FAIL ERROR rc=1\n')
        replace(d/'run_manifest.txt','end=x fails=0 reader_rc=0','stage=UT screen=screen.txt rc=1 check=ERROR\nend=x fails=1 reader_rc=0')
    else:
        replace(d/'run_manifest.txt','end=x fails=0 reader_rc=0\n','')
    v=R.arm_verdict(str(d),BED,'UT',P,root=str(root))
    record('arm_failure_'+mode,{'receipt':R._job_receipt(str(root),BED,'UT')[:2],
           'arm_primary':v['primary_status'],'trajectory':v['trajectory_status'],'selection':R.selection_state(str(root),P),
           'gate_UVa':R.gate(str(root),BED,'UVa',P),'cli_rc':rc if mode=='reader_stdout' else None},
           'Scope observation: arm receipt/stage errors not enforced by re-evaluation',None)

root=arm_root('uv_failure_final_gravity',('UB','UT','UVa'))
d=root/BED/'UVa'
replace(d/'run_manifest.txt','end=x fails=0 reader_rc=0','end=x fails=1 reader_rc=120')
other=R.BEDS[0]
R._fake_restored(str(root),other)
put(root/other/'ul_base.in','variable ul_S2max equal 1e-5\n')
record('uv_failure_final_gravity',{'receipt':R._job_receipt(str(root),BED,'UVa')[:2],
       'selection':R.selection_state(str(root),P),'other_bed_UB':R.gate(str(root),other,'UB',P),
       'gravity_UB':R.gate(str(root),BED,'G_UB',P),'report':R.report(str(root),P)},
       'Scope observation: final selection uses re-read values despite failed UV receipt',None)

# Precision-boundary evidence only. No realistic LIGGGHTS ID corruption claim:
# parser float conversion precedes exact_id, so lexical exactness is not proven.
precision=[]
for tok in ('1','1.5','1.0000000000000001','9007199254740991','9007199254740992','9007199254740993','9007199254740994'):
    path=E/'precision'/('id_'+tok.replace('.','_')+'.dump')
    put(path,'ITEM: TIMESTEP\n1\nITEM: NUMBER OF ATOMS\n1\nITEM: BOX BOUNDS pp pp ff\n0 1\n0 1\n0 1\nITEM: ATOMS id\n'+tok+'\n')
    dump=L.read_dump(str(path),'custom',['id'])
    precision.append({'token':tok,'parsed':dump['rows'][0]['id'],'accepted_id':L.exact_id(dump['rows'][0]['id'])})
record('lexical_precision_boundary',precision,'Boundary limitation; no current production-scale consequence demonstrated',None)

OUT['summary']={'checked':sum(x['matches'] is not None for x in OUT['cases'].values()),
                'failed_expectations':[k for k,v in OUT['cases'].items() if v['matches'] is False],
                'observations':[k for k,v in OUT['cases'].items() if v['matches'] is None]}
OUT['source_unchanged']={n: hashlib.sha256((KIT/n).read_bytes()).hexdigest()==sha for n,sha in OUT['sources'].items()}
js(ROOT/'evidence/receipt_ids_recheck.json',OUT)
print(json.dumps(OUT['summary'],ensure_ascii=False,indent=2))
