"""Q4 isolated, synthetic review: no solver/runner/GPU imports or real outputs.

Uses exact AST bodies for narrowly selected control guards. Git receive commands
are copied from the sealed candidate document. This does NOT emulate Linux flock
or constitute an end-to-end production recovery test.
"""
import ast
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
SOURCE = ROOT / 'candidate_source'
SCRIPT = SOURCE / 'scripts/rint_r_chain.py'
DOC = SOURCE / 'docs/reviews/rint2_kgy_commands_20261020.md'
WORK = BASE / ('work_' + str(time.time_ns()))
assert not WORK.exists(), 'Use a new output directory; existing work is preserved.'
WORK.mkdir()
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
           GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1')
records = []

def record(case, expected, actual, ok, kind='exact_guard'):
    row = dict(case=case, expected=expected, actual=actual, passed=bool(ok), kind=kind)
    records.append(row)
    print(json.dumps(row, ensure_ascii=False))

def git(repo, *args, check=True):
    return subprocess.run(['git', '-c', 'safe.directory='+str(Path(repo).resolve()).replace('\\','/'),
                           '-c', 'core.autocrlf=false', '-c', 'user.name=synthetic-review',
                           '-c', 'user.email=review@example.invalid', '-C', str(repo), *args],
                          env=ENV, capture_output=True, check=check)

blob = hashlib.sha1(b'blob ' + str(SCRIPT.stat().st_size).encode() + b'\0' + SCRIPT.read_bytes()).hexdigest()
assert blob == '4c52a8f9c2740ccc3874d0fcb7f9acb97a477829', blob
tree = ast.parse(SCRIPT.read_text(encoding='utf-8'))
names = {'Stop', 'host_seen', 'start_chain_problem', 'folder_digest', '_ledger_now', 'recover_ledger',
         'env_unit', 'env_seal_problem', 'code_key'}
nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
assert {n.name for n in nodes} == names
G = dict(Path=Path, os=os, hashlib=hashlib, json=json, ENV_UNIT_KEYS=('python_minor','numpy','scipy'))
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SCRIPT), 'exec'), G)
G['sha256_file'] = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
record('source_pin', 'exact supplied blob', blob, True, 'provenance')

# Known Q2 boundary: version equality is NOT runtime equality. No numerical
# calculation or claim that changing a runtime knob changes a result is made.
unit = dict(python_minor='3.8', numpy='1.24.4', scipy='1.10.1')
ca = dict(env=dict(unit=unit, record_only=dict(openblas_coretype='synthetic-A',numpy_simd={'features':['A']})))
cb = dict(env=dict(unit=unit, record_only=dict(openblas_coretype='synthetic-B',numpy_simd={'features':['B']})))
plan = dict(exec_policy=dict(env_unit=unit))
same_key = G['code_key'](ca) == G['code_key'](cb)
record('known_Q2_runtime_outside_code_key','runtime-only change does not alter code key',same_key,same_key,'known_boundary_not_new_defect')
accepted = G['env_seal_problem'](ca,plan) is None and G['env_seal_problem'](cb,plan) is None
record('known_Q2_runtime_outside_env_seal','same registered versions pass for both runtime records',accepted,accepted,'known_boundary_not_new_defect')

host = dict(machine_id='synthetic-A', boot_id='boot-1', pidns='pidns-1')
start = dict(chain_pid=99, chain_start=10, host=host)
for alive in [False, True, None]:
    G['chain_parent_alive'] = lambda s, val=alive: val
    why, used = G['start_chain_problem'](start, host, {'why': 'synthetic operator'})
    record('same_boot_parent_' + str(alive), 'allow only confirmed dead; operator cannot bypass live/unknown',
           dict(held=why is not None, operator_used=used), (why is None) == (alive is False) and not used)
other = dict(host, boot_id='boot-2')
for op in [None, {'why': 'synthetic reboot confirmation'}]:
    why, used = G['start_chain_problem'](start, other, op)
    record('reboot_' + ('unconfirmed' if op is None else 'confirmed'),
           'hold without operator; allow only after scoped operator confirmation',
           dict(held=why is not None, operator_used=used), (why is None) == (op is not None) and used == (op is not None))
why, used = G['start_chain_problem'](start, dict(host, machine_id='synthetic-B'))
record('different_machine', 'hold', dict(held=why is not None, operator_used=used), why is not None and not used)

# Exact recover_ledger's early folder binding branch, with synthetic upstream
# parsed state and capture-only append. No stage_summary or scientific file is read.
original = WORK / 'original' / 'attempt_1'
original.mkdir(parents=True)
(original / 'attempt.json').write_text('{"synthetic":true}\n', encoding='ascii')
moved = WORK / 'moved' / 'attempt_1'
moved.parent.mkdir()
shutil.copytree(original, moved)
ad = dict(n=1, target='unit:P0_c0_R_j0', ledger_commit='1'*40)
st = dict(entries={1: dict(target=ad['target'])}, results={}, starts={1:dict(start, base=str(original.parent.resolve()))})
writes = []
G.update(read_attempt=lambda p: ad if Path(p).name == 'attempt_1' else None,
         host_ident=lambda: host, ledger_repo_problem=lambda p: None,
         ledger_now=lambda p: ('2'*40, b'synthetic'), ledger_parse=lambda raw: st,
         ledger_is_ancestor=lambda *args: True,
         ledger_append=lambda *args, **kwargs: writes.append(args),
         print_stop=lambda e: print(str(e)))
capture = io.StringIO()
with contextlib.redirect_stdout(capture):
    bad, used = G['recover_ledger'](moved, WORK / 'fake_ledger')
record('moved_attempt_guard', 'one rejection and no ledger append',
       dict(bad=bad, operator_used=used, append_calls=len(writes), diagnostic=capture.getvalue().strip()), bad == 1 and not writes)
dg1, dg2 = G['folder_digest'](original), G['folder_digest'](moved)
record('moved_digest', 'same bytes keep same evidence digest; recovery still rejects new base',
       dict(original=dg1, moved=dg2), dg1 == dg2)

# Independently count the 12 documented assignments rather than trusting checker.
doc = DOC.read_text(encoding='utf-8')
assignment = '\n'.join(x for x in doc.splitlines() if x.startswith('| kgy (7)') or x.startswith('| gabia (5)'))
got = re.findall(r'`(P[01]_c[01]_R_j(?:0|_lo|_hi))`', assignment)
expected = {f'{p}_c{c}_{r}' for p in ('P0','P1') for c in ('0','1') for r in ('R_j0','R_j_lo','R_j_hi')}
record('twelve_units', 'all 12 units exactly once', dict(count=len(got), unique=len(set(got)), missing=sorted(expected-set(got))),
       len(got) == 12 and set(got) == expected, 'document')

# Actual git operations with the receive block's control flow translated to
# Python. Git Bash is unavailable in this Windows host (exit 0xc0000142).
# No claim of exact shell execution or flock execution is made.
lines = doc.splitlines()
a = next(i for i,x in enumerate(lines) if x.startswith('### (5) 원장 넘김'))
o = next(i for i in range(a,len(lines)) if lines[i].strip() == '```sh')
c = next(i for i in range(o+1,len(lines)) if lines[i].strip() == '```')
blk = lines[o+1:c]
r = next(i for i,x in enumerate(blk) if x.startswith('# 받는 쪽'))
recv = '\n'.join(x for x in blk[r+1:] if not x.startswith('#'))
(BASE / 'receive_block_from_candidate.sh').write_text(recv+'\n', encoding='utf-8')
homes = {x: WORK/x for x in ('A','B','C')}
for h in homes.values():
    (h/'sdcp/ca1_relay').mkdir(parents=True)
def led(x): return homes[x]/'sdcp/ca1_ledger'
def parked(x): return homes[x]/'sdcp/ca1_ledger.parked'
def head(p): return git(p,'rev-parse','HEAD').stdout.decode().strip()
def append(x, text):
    with (led(x)/'rint_r_attempts.jsonl').open('a', encoding='ascii', newline='\n') as f: f.write(text+'\n')
    git(led(x),'add','rint_r_attempts.jsonl')
    git(led(x),'commit','-q','-m',text)
def bundle_and_park(frm,to,label):
    h = head(led(frm))
    bundle = homes[frm]/f'sdcp/ca1_relay/{label}_{frm}_to_{to}.bundle'
    git(led(frm),'bundle','create',str(bundle),'--all')
    # Serial synthetic equivalent only; no claim that Linux flock was executed.
    led(frm).rename(parked(frm))
    dest = homes[to]/'sdcp/ca1_relay'/bundle.name
    shutil.copy2(bundle,dest)
    return h,dest
def receiving(x,frm,label,h):
    script = (recv.replace('<넘김 기록 시각>',label).replace('<원장 가지>','main')
              .replace('<넘김 기록의 원장 끝 커밋>',h).replace('FROM=kgy; TO=gabia',f'FROM={frm}; TO={x}'))
    rb=homes[x]/f'sdcp/ca1_relay/{label}_{frm}_to_{x}.bundle'
    git(homes[x]/'sdcp','bundle','list-heads',str(rb))
    if parked(x).is_dir():
        p=git(parked(x),'-c','pull.rebase=false','pull','-q','--ff-only',str(rb),'main',check=False)
        if p.returncode == 0: parked(x).rename(led(x))
    else:
        p=git(homes[x]/'sdcp','clone','-q','-b','main',str(rb),str(led(x)),check=False)
    q=git(led(x),'rev-parse','HEAD',check=False)
    ok=q.returncode == 0 and q.stdout.decode().strip() == h
    out=dict(rc=0 if ok else 1,recv_ok=ok,command_rc=p.returncode,
             stderr=(p.stderr+q.stderr).decode('utf-8',errors='replace').strip(),
             method='native Git; document control-flow translation; no Bash or flock')
    (BASE / ('receive_'+x+'_'+label+'_'+str(time.time_ns())+'.json')).write_text(
        json.dumps(dict(script=script,result=out),ensure_ascii=False,indent=2),encoding='utf-8')
    return out
led('A').mkdir()
git(led('A'),'init','-q','-b','main')
append('A','synthetic header')
h1,b1=bundle_and_park('A','B','20261117T000001Z')
v=receiving('B','A','20261117T000001Z',h1)
record('receive_first_clone','RECV_OK and exact HEAD',dict(v,head_same=head(led('B'))==h1),v['recv_ok'] and head(led('B'))==h1,'git_doc_block')
append('B','synthetic entry')
h2,b2=bundle_and_park('B','A','20261117T000002Z')
v=receiving('A','B','20261117T000002Z',h2)
record('receive_return_ff','RECV_OK after pull in parked directory',dict(v,head_same=head(led('A'))==h2),v['recv_ok'] and head(led('A'))==h2,'git_doc_block')
v=receiving('A','B','20261117T000002Z',h2)
record('repeat_completed_receive','same fully received HEAD may re-confirm despite clone failure',v,v['recv_ok'] and 'already exists' in v['stderr'],'git_doc_block')

# Reconstruct the honest interrupted clone state: clone has refs/objects but
# checkout has not happened. --no-checkout reaches precisely that state without
# racing or modifying ledger records; then retry the documented receive block.
c_bundle=homes['C']/f'sdcp/ca1_relay/20261117T000003Z_A_to_C.bundle'
shutil.copy2(b2,c_bundle)
git(homes['C']/'sdcp','clone','-q','--no-checkout','-b','main',str(c_bundle),str(led('C')))
v=receiving('C','A','20261117T000003Z',h2)
G.update(LEDGER_FILE='rint_r_attempts.jsonl',ledger_head=head,
         ledger_blob=lambda repo,h:git(repo,'show',h+':rint_r_attempts.jsonl').stdout)
try:
    G['_ledger_now'](led('C'))
    rejection=None
except G['Stop'] as e:
    rejection=e.code
record('interrupted_clone_receive','HEAD receipt can pass; actual ledger read must stop',
       dict(v,ledger_guard=rejection),v['recv_ok'] and rejection=='ATTEMPT_LEDGER_MISMATCH','git_doc_block_plus_exact_guard')

# Divergence is a manual control; explicitly not an honest-flow new defect.
git(parked('B'),'commit','-q','--allow-empty','-m','synthetic divergent control')
append('A','synthetic second entry')
h3,b3=bundle_and_park('A','B','20261117T000004Z')
v=receiving('B','A','20261117T000004Z',h3)
record('divergent_parked_control','no RECV_OK; parked retained; active absent',
       dict(v,parked=parked('B').exists(),active=led('B').exists()),
       not v['recv_ok'] and parked('B').exists() and not led('B').exists(),'manual_control_not_new_defect')

summary=dict(source_blob=blob, cases=len(records), passed=sum(x['passed'] for x in records),
             records=records, scope='synthetic only; no engine/MPI/GPU/real result loading; flock not executed')
(BASE/'output.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.exit(0 if all(x['passed'] for x in records) else 1)
