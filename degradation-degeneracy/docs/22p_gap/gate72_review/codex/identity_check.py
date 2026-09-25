"""Reviewer data-only Git/byte snapshot. No project modules imported."""
from pathlib import Path
import hashlib, json, subprocess
OUT=Path(__file__).resolve().parent
WT=Path('C:/Users/Administrator/Documents/Codex/g72_20260925')
DD=WT/'degradation-degeneracy'
HEAD='c4b77ccf71d736dec9162cd5a5377f60f66c0782'
CODE='82854571d0240951c929d4a9b90260e53ca38e88'
OLD='4505b70c6e63453e0424239cac7d48488fee022a'
TEST='b921333322f17a9ac5d92153865da441dc0c9bd7'
def git(*args):
    return subprocess.check_output(['git','-c',f'safe.directory={WT.as_posix()}','-C',str(WT),*args])
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert git('rev-parse','HEAD').decode().strip()==HEAD
state=git('status','--porcelain=v1','-uall').decode()
assert not state
paths=filter(None,git('ls-files','-z','--','degradation-degeneracy').decode().split('\0'))
snap={p:ident((WT/p).read_bytes()) for p in paths}
dump('SOURCE_BEFORE.json',snap)
entries=[]
for folder in ('src','tools','configs','scripts'):
    for p in (DD/folder).rglob('*'):
        if p.is_file() and not any(c in ('__pycache__','.ipynb_checkpoints') for c in p.relative_to(DD).parts) and p.suffix not in ('.pyc','.pyo'):
            entries.append((p.relative_to(DD).as_posix().encode(),p))
for pattern in ('run.sh','requirements*.txt'):
    entries.extend((p.relative_to(DD).as_posix().encode(),p) for p in DD.glob(pattern) if p.is_file())
h=hashlib.sha256()
for name,p in sorted(entries):h.update(name);h.update(p.read_bytes())
digest=h.hexdigest()[:16]
assert digest=='518d4f63076b77e3',digest
scope=['degradation-degeneracy/'+p for p in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
for name,start,end,paths in (
    ('CODE_TO_HEAD_SCOPE.diff',CODE,HEAD,scope),
    ('G71_TO_G72_SCOPE.diff',OLD,CODE,scope),
    ('TEST_REPORT_TO_HEAD.diff',TEST,HEAD,['degradation-degeneracy']),
    ('TESTS_AND_DOCS.diff',OLD,HEAD,['degradation-degeneracy/tests','degradation-degeneracy/docs/22p_gap/GATE71_REQUEST.md','degradation-degeneracy/docs/22p_gap/GATE72_REQUEST.md','degradation-degeneracy/docs/22p_gap/mutation_replay.py']),
): (OUT/name).write_bytes(git('diff','--no-ext-diff',start,end,'--',*paths))
assert (OUT/'CODE_TO_HEAD_SCOPE.diff').stat().st_size==0
request=git('show',HEAD+':degradation-degeneracy/docs/22p_gap/GATE72_REQUEST.md')
assert request==(DD/'docs/22p_gap/GATE72_REQUEST.md').read_bytes()
(OUT/'GATE72_REQUEST_GIT_BLOB.md').write_bytes(request)
refs=['tools/preserve.py','tests/test_gate71_defensive.py','tests/test_gate70_defensive.py','tests/conftest.py','docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml','docs/22p_gap/LEG_PRESERVATION.yaml','docs/22p_gap/GATE71_REQUEST.md','docs/22p_gap/GATE72_REQUEST.md','docs/22p_gap/mutation_replay.py','run.sh']
reference=OUT/'reference'; reference.mkdir(exist_ok=False)
for name in refs:
    p=reference/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((DD/name).read_bytes())
dump('IDENTITY.json',{'head':HEAD,'code_target':CODE,'source_digest_independent':digest,'scope_files':len(entries),'status_before':state,
     'tracked_DD_files':len(snap),'request':ident(request),'request_blob_equals_checkout':True,'code_to_head_scope_diff_bytes':0,
     'test_report_head':TEST,'test_report_to_head_names':git('diff','--name-only',TEST,HEAD,'--','degradation-degeneracy').decode().splitlines(),
     'project_module_imports':0,'main_runs_restore_class_changes':0})
print((OUT/'IDENTITY.json').read_text(encoding='utf-8'))
