"""Reviewer-owned Git/byte checks; no subject imports or executions."""
from pathlib import Path
import hashlib,json,subprocess
O=Path(__file__).resolve().parent
WT=Path('C:/Users/Administrator/Documents/Codex/g73_20260925'); DD=WT/'degradation-degeneracy'
HEAD='b0c0b9ca10743d83950c29322d30f581fecf884d'
CODE='7a7945564e6a94803b4d3bc72e8202534189ccdb'
OLD='c4b77ccf71d736dec9162cd5a5377f60f66c0782'
TEST='cfacfe6b44a27ee34af536cc84f29806d916f392'
def git(*a):return subprocess.check_output(['git','-c',f'safe.directory={WT.as_posix()}','-C',str(WT),*a])
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v):
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
assert git('rev-parse','HEAD').decode().strip()==HEAD
status=git('status','--porcelain=v1','-uall').decode();assert not status
paths=[p for p in git('ls-files','-z','--','degradation-degeneracy').decode().split('\0') if p]
save('SOURCE_BEFORE.json',{p:ident((WT/p).read_bytes()) for p in paths})
entries=[]
for folder in ('src','tools','configs','scripts'):
    for p in (DD/folder).rglob('*'):
        if p.is_file() and not any(c in ('__pycache__','.ipynb_checkpoints') for c in p.relative_to(DD).parts) and p.suffix not in ('.pyc','.pyo'):
            entries.append((p.relative_to(DD).as_posix().encode(),p))
for pattern in ('run.sh','requirements*.txt'):
    entries.extend((p.relative_to(DD).as_posix().encode(),p) for p in DD.glob(pattern) if p.is_file())
h=hashlib.sha256()
for name,p in sorted(entries):h.update(name);h.update(p.read_bytes())
digest=h.hexdigest()[:16];assert digest=='c2ef1a811e70bb4c',digest
scope=['degradation-degeneracy/'+n for n in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
for name,start,end,ps in (
    ('CODE_TO_HEAD_SCOPE.diff',CODE,HEAD,scope),
    ('G72_TO_G73_SCOPE.diff',OLD,CODE,scope),
    ('TEST_REPORT_TO_HEAD.diff',TEST,HEAD,['degradation-degeneracy']),
    ('TESTS_AND_MUTATION.diff',OLD,HEAD,['degradation-degeneracy/tests','degradation-degeneracy/docs/22p_gap/mutation_replay.py']),
    ('LEDGER_AND_RECEIPT.diff',OLD,HEAD,['degradation-degeneracy/docs/22p_gap/LEG_PRESERVATION.yaml','degradation-degeneracy/docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml']),
): (O/name).write_bytes(git('diff','--no-ext-diff',start,end,'--',*ps))
assert (O/'CODE_TO_HEAD_SCOPE.diff').stat().st_size==0
request=git('show',HEAD+':degradation-degeneracy/docs/22p_gap/GATE73_REQUEST.md')
assert request==(DD/'docs/22p_gap/GATE73_REQUEST.md').read_bytes()
(O/'GATE73_REQUEST_GIT_BLOB.md').write_bytes(request)
ref=O/'reference';ref.mkdir(exist_ok=False)
refs=['tools/preserve.py','tests/test_gate72_defensive.py','tests/test_gate71_defensive.py','tests/test_gate70_defensive.py','tests/test_issuance_authority_60.py','tests/conftest.py','docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml','docs/22p_gap/LEG_PRESERVATION.yaml','docs/22p_gap/GATE71_REQUEST.md','docs/22p_gap/GATE72_REQUEST.md','docs/22p_gap/GATE73_REQUEST.md','docs/22p_gap/mutation_replay.py','docs/22p_gap/registry_impact.md','run.sh']
for n in refs:
    p=ref/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((DD/n).read_bytes())
result={'head':HEAD,'code_target':CODE,'source_digest_independent':digest,'scope_files':len(entries),
    'status_before':status,'tracked_DD_files':len(paths),'request':ident(request),'request_blob_equals_checkout':True,
    'code_to_head_scope_diff_bytes':0,'test_report_head':TEST,
    'test_report_to_head_names':git('diff','--name-only',TEST,HEAD,'--','degradation-degeneracy').decode().splitlines(),
    'code_to_head_commits':git('log','--format=%H %s',CODE+'..'+HEAD).decode().splitlines(),
    'project_module_imports':0,'main_runs_restore_class_changes':0}
save('IDENTITY.json',result);print(json.dumps(result,ensure_ascii=False))
