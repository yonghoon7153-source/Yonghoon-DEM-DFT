import ast
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys
import types
from pathlib import Path

ROOT = Path(os.environ.get('REPO_ROOT', Path(__file__).resolve().parents[4])).expanduser().resolve()
OUT = Path(os.environ.get('EVIDENCE_OUT', Path.cwd() / 'lhs214-reproduction')).expanduser().resolve()
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'scripts'))
import run_network_194_parallel as N
import supp20_input_receipt as S

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def sha(b):
    return hashlib.sha256(b).hexdigest()

def put(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

base = '34713ac9650ece7c8d59b7c4d9a2aefccee693ea'
code = 'fe23f2b839f0a49adb077348fec6d4c85443b62a'
rat = 'f82929b0644be39b44e9fba9ea04cf9d60de9146'
head = git('rev-parse', 'HEAD').decode().strip()
tool = 'scripts/supp20_input_receipt.py'
regs = ['docs/reviews/lhs_network_batch_registration_20261007_g2.md',
        'docs/reviews/lhs_network_batch_registration_20261012_supp20.md']
tools = list(N.HANDOVER_FILES) + ['scripts/lhs_release_build.py', 'scripts/run_network_194_parallel.py', 'scripts/wsl_network_smoke.py']
files = sorted(set(N.CODE_FILES) | set(tools) | set(regs) | {tool})
hashes = {}
for f in files:
    current = (ROOT / f).read_bytes()
    hashes[f] = {'working':sha(current), 'HEAD':sha(git('show', head + ':' + f)),
                 'baseline':sha(git('show', base + ':' + f)), 'ratified':sha(git('show', rat + ':' + f))}
scope = {'head':head, 'baseline':base, 'ratified':rat, 'hashes':hashes,
         'sealed32_equal_baseline':all(hashes[f]['working']==hashes[f]['baseline'] for f in N.CODE_FILES),
         'other_tools_equal_baseline':all(hashes[f]['working']==hashes[f]['baseline'] for f in tools),
         'receipt_equal_code_commit':sha((ROOT/tool).read_bytes())==sha(git('show',code+':'+tool)),
         'all_working_equal_HEAD':all(v['working']==v['HEAD'] for v in hashes.values())}
oldast = ast.parse(git('show',code+'^:'+tool).decode())
newast = ast.parse((ROOT/tool).read_text())
scope['top_level_nodes'] = [len(oldast.body), len(newast.body)]
scope['changed_ast'] = [getattr(b,'name',type(b).__name__) for a,b in zip(oldast.body,newast.body) if ast.dump(a)!=ast.dump(b)]
scope['ratification_to_head_diff'] = git('diff',rat,head,'--',*regs).decode()
put('scope.json', scope)

h = N.code_hashes()
fp = N.code_fp(h)
values = {}
for f in regs:
    v,p = S.registration_values(reg_doc=f)
    values[f] = {'values':v, 'problems':p, 'fp_problems':[x for x in p if x.startswith('등록 문서 code_fp')]}
t = (ROOT/regs[0]).read_text()
s3, why = S._md_section(t,3,strip_code=True)
historical = dict(re.findall(r'^\| `([^`]+\.py)` \| `([0-9a-f]{64})` \|',s3,re.M))
inline = dict(re.findall(r'`([^`]+\.py)` `([0-9a-f]{64})`',s3))
merged = dict(historical,**inline)
reg_hash_mismatch = {f:[merged.get(f),h[f]] for f in N.CODE_FILES if merged.get(f)!=h[f]}
receipt = S.receipt()
put('container_receipt.json',receipt)
ns=types.SimpleNamespace(**{f'{a}_{b}':'' for a in N.COHORT_SPECS for b in ('harvest','cohort')})
digests={}
for cs in (['lhs','lhsx'], ['lhss']):
    p=N.build_plan(cs,N.cohort_specs(ns),(),'cost')
    digests[N.registered_production_set(p)]=N.plan_input_digest(p)
gen=N.derive_generation(N.ROOT)
closure=N.code_dependency_closure()
lazy=N.lazy_import_census()
measure={'code_fp':fp,'registrations':values,'historical_rows':len(historical),
         'active_rows_cover_sealed':all(f in merged for f in N.CODE_FILES),'active_row_mismatch':reg_hash_mismatch,
         'other_tool_hashes':{f:N.sha256_file(ROOT/f) for f in tools+[tool]},
         'input_digests':digests,'generation':gen,'closure_files':closure['files'],
         'closure_outside_sealed':[f for f in closure['files'] if f not in N.CODE_FILES],
         'lazy_count':len(lazy['lazy']),'lazy_unclassified':lazy['unclassified'],'lazy_stale':lazy['stale'],'fork_census':N.fork_census()}
put('measurements.json',measure)

# The changed functions are nested in the selftest. Extract their original AST,
# preserving implementation, and provide the same immutable code fingerprint.
selftest=next(n for n in newast.body if isinstance(n,ast.FunctionDef) and n.name=='_selftest')
nodes=[n for n in selftest.body if isinstance(n,ast.FunctionDef) and n.name in ('fp_state','s0b_fp')]
assert len(nodes)==2
mini=ast.Module(body=nodes,type_ignores=[])
env={'fp_now':fp}
exec(compile(mini,str(ROOT/tool),'exec'),env)
other='f'*64
tail=fp[:-1]+('0' if fp[-1]!='0' else '1')
choices=[None,fp,other,tail]
cases=[]
for r,p,br,bp in itertools.product(choices,repeat=4):
    for errs in ([],['등록 문서 code_fp_pending — conflicting values']):
        reg={'code_fp':r,'code_fp_pending':p}
        basev={'code_fp':br,'code_fp_pending':bp}
        # Independent truth table: registered now with no pending, or a
        # different active fingerprint explicitly pending this exact now.
        # Both documents must agree and the base parser must have no fp error.
        expected=(not errs and (r,p)==(br,bp) and
                  ((r==fp and p is None) or (r in (other,tail) and p==fp)))
        got,why=env['s0b_fp'](reg,basev,errs)
        cases.append({'reg':reg,'base':basev,'errors':errs,'expected':expected,'actual':got,'why':why})
put('s0b_truth_table.json',{'n':len(cases),'mismatch':[c for c in cases if c['actual']!=c['expected']],
                         'accepted':sum(c['actual'] for c in cases),'cases':cases})

# The promise of 64-digit equality must reject a fingerprint differing only
# in the last digit; exercise actual document parsing and receipt D1 as well.
doc=(ROOT/regs[1]).read_text()
section,why=S._md_section(doc,3,strip_code=True)
assert why=='' and section and fp in section
variants={}
replacements={'same_prefix_wrong_tail':tail,'short_63':fp[:-1],'uppercase':fp.upper(),
              'unicode_digit':fp.replace('2','２',1),'space_inside':fp[:32]+' '+fp[32:],
              'nan':'NaN','infinity':'Infinity'}
for label,val in replacements.items():
    changed=doc.replace(section,section.replace('`code_fp '+fp+'`','`code_fp '+val+'`'))
    path=OUT/('document_'+label+'.md')
    path.write_text(changed)
    rec=S.receipt(reg_doc=str(path))
    variants[label]={'rc':rec['rc'],'bad':[c['id'] for c in rec['checks'] if not c['ok']],
                     'code_fp':rec['registration']['values'].get('code_fp')}
put('document_counterexamples.json',variants)
print(json.dumps({'head':head,'sealed32_equal':scope['sealed32_equal_baseline'],
                  'tools_equal':scope['other_tools_equal_baseline'],'AST':scope['changed_ast'],
                  'code_fp':fp,'active_row_mismatch':reg_hash_mismatch,'receipt_rc':receipt['rc'],
                  'truth_table_n':len(cases),'truth_table_mismatch':sum(c['actual']!=c['expected'] for c in cases),
                  'counterexamples':variants},indent=2,ensure_ascii=False))
