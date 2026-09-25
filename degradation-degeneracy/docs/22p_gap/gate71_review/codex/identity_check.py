"""Receiver-owned data-only identity/snapshot checks. Imports no project module."""
from pathlib import Path
import hashlib, json, subprocess, zipfile, io

OUT = Path(__file__).resolve().parent
WT = Path('C:/Users/Administrator/Documents/Codex/g71_20260925')
DD = WT / 'degradation-degeneracy'
HEAD = '4505b70c6e63453e0424239cac7d48488fee022a'
CODE = '876429562f6a69b59793c70700cb5b375391ab67'
OLD = 'f0dfaff3bea1e1caedcd7a34275e908284cc2d4f'
def git(*args):
    return subprocess.check_output(['git','-c',f'safe.directory={WT.as_posix()}','-C',str(WT),*args])
def h(raw): return hashlib.sha256(raw).hexdigest()
def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert git('rev-parse','HEAD').decode().strip() == HEAD
state = git('status','--porcelain=v1','-uall').decode()
tracked = git('ls-files','-z','--','degradation-degeneracy').decode().split('\0')
snapshot = {}
for name in filter(None, tracked):
    raw = (WT/name).read_bytes()
    snapshot[name] = {'bytes':len(raw),'sha256':h(raw)}
dump('SOURCE_BEFORE.json',snapshot)
entries=[]
for folder in ('src','tools','configs','scripts'):
    for path in (DD/folder).rglob('*'):
        if path.is_file() and not any(p in ('__pycache__','.ipynb_checkpoints') for p in path.relative_to(DD).parts) and path.suffix not in ('.pyc','.pyo'):
            entries.append((path.relative_to(DD).as_posix().encode(),path))
for glob in ('run.sh','requirements*.txt'):
    entries.extend((p.relative_to(DD).as_posix().encode(),p) for p in DD.glob(glob) if p.is_file())
digest=hashlib.sha256()
for key,path in sorted(entries): digest.update(key);digest.update(path.read_bytes())
scope=['degradation-degeneracy/'+p for p in ('src','tools','configs','scripts','run.sh','requirements*.txt')]
for name,start,end,paths in (
    ('CODE_TO_HEAD_SCOPE.diff',CODE,HEAD,scope),
    ('RUN_SCOPE_DIFF.diff',OLD,CODE,scope),
    ('TESTS_AND_DOCS.diff','8568f782db3acbf00d872ce5527147258c00bec7',HEAD,['degradation-degeneracy/tests','degradation-degeneracy/docs/22p_gap/plan_leg.py','degradation-degeneracy/docs/22p_gap/registry_impact.md']),
    ('E10_TO_HEAD.diff','0e6348be9ec80919e0f84ae246294cb6336e9545',HEAD,['degradation-degeneracy']),
):
    (OUT/name).write_bytes(git('diff','--no-ext-diff',start,end,'--',*paths))
request=git('show',HEAD+':degradation-degeneracy/docs/22p_gap/GATE71_REQUEST.md')
(OUT/'GATE71_REQUEST_GIT_BLOB.md').write_bytes(request)
assert request == (DD/'docs/22p_gap/GATE71_REQUEST.md').read_bytes()
registries=sorted((DD/'docs/22p_gap/_exec_class').glob('*.json'))
census={k:0 for k in ('legacy','rekey','fixture','leg_L','other')}
variants={'modern':0,'legacy':0,'other':0}
for path in registries:
    rec=json.loads(path.read_bytes());ev=rec.get('evidence','')
    kind='legacy' if ev.startswith('legacy 분류') else 'rekey' if 're-key' in ev else 'fixture' if '_complete_artifact' in ev else 'leg_L' if 'leg=L ' in ev else 'other'
    census[kind]+=1
    keys=set(rec);legacy={'content_id','execution_class','evidence','recorded_at'}
    variants['modern' if keys==legacy|{'sealed'} else 'legacy' if keys==legacy else 'other']+=1
result={'head':HEAD,'code_target':CODE,'status_before':state,'tracked_DD_files':len(snapshot),
        'source_digest_independent_byte_calculation':digest.hexdigest()[:16],
        'source_digest_declared':'b705a21a1237ec73','scope_files':len(entries),
        'code_to_head_scope_diff_bytes':(OUT/'CODE_TO_HEAD_SCOPE.diff').stat().st_size,
        'request_sha256':h(request),'request_blob_equals_checkout':True,
        'registry_disk_top_level_json':len(registries),'registry_evidence_text_census':census,'registry_keyset_census':variants,
        'registry_tracked_paths':len(git('ls-files','--','degradation-degeneracy/docs/22p_gap/_exec_class/*.json').decode().splitlines()),
        'limits':'Registry census is a text/keyset classification, not independent verification of the historical scientific runs.',
        'project_modules_imported':0,'main_runs_restores_class_changes':0}
assert result['source_digest_independent_byte_calculation']==result['source_digest_declared']
assert result['code_to_head_scope_diff_bytes']==0
dump('IDENTITY.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
