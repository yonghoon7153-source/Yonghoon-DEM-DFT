"""Reviewer-owned text/hash/AST audit. Never imports or executes submitted code."""
import ast
import difflib
import fnmatch
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
P = 'degradation-degeneracy/'
HEAD = '24f499ba6a5e45a75613e9842ce99a679b5ce863'
records = json.loads((ROOT / 'REFERENCE_TEXT.json').read_text(encoding='utf-8'))['records']
by_key = {(r['ref'], r['path']): r for r in records}
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def get(path, ref=HEAD): return by_key[(ref, P + path)]['content']
def one(path): return get(path).encode('utf-8')
def scope(path):
    if not path.startswith(P): return False
    s = path[len(P):]
    return s.startswith(('src/', 'tools/', 'configs/', 'scripts/')) or s == 'run.sh' or ('/' not in s and fnmatch.fnmatchcase(s, 'requirements*.txt'))

identities = []
for r in records:
    b = r['content'].encode('utf-8')
    identities.append({'path': r['path'], 'ref': r['ref'], 'bytes': len(b), 'sha256': sha(b), 'blob_match': blob(b) == r['sha']})
assert all(x['blob_match'] for x in identities)
log_entries = json.loads((ROOT / 'EXPECTED_LOG_HASHES.json').read_text())
log_checks = []
for e in log_entries:
    r = next(x for x in identities if x['path'] == P + 'docs/22p_gap/gate90_evidence/' + e['file'])
    log_checks.append(dict(e, bytes_match=r['bytes'] == e['bytes'], sha_match=r['sha256'] == e['sha256']))
assert all(x['bytes_match'] and x['sha_match'] for x in log_checks)

comparisons = json.loads((ROOT / 'GIT_COMPARISONS.json').read_text())
changed_scope = [x['filename'] for x in comparisons['base_to_request']['files'] if scope(x['filename'])]
post_scope = [x['filename'] for x in comparisons['code_to_request']['files'] if scope(x['filename'])]
assert sorted(changed_scope) == sorted(P+x for x in ['requirements-validation-C.lock.txt','requirements.txt','scripts/smoke_e2e.sh','tools/env_profile.py'])
assert post_scope == []

# Reuse the earlier recipient snapshot only after every byte is checked against the new fixed Git tree.
prior_dir = ROOT / 'prior_review_data'
oldscope = json.loads((prior_dir / 'PRIOR_RUN_SCOPE_SNAPSHOT.json').read_text())
old89 = json.loads((prior_dir / 'RECEIVED_SNAPSHOT.json').read_text())
available = dict(oldscope['files'])
available.update(old89['files'])
available.update({r['path']: r for r in records if r['ref'] == HEAD})
tree = json.loads((ROOT / 'REQUEST_TREE.json').read_text())
while 'content' in tree: tree = json.loads(tree['content'])
assert tree.get('truncated') is False
scope_entries = [e for e in tree['tree'] if e['type'] == 'blob' and scope(e['path']) and not any(k in e['path'].split('/') for k in ('__pycache__','.ipynb_checkpoints')) and not e['path'].endswith(('.pyc','.pyo'))]
digest = hashlib.sha256()
scope_ids = []
for e in sorted(scope_entries, key=lambda x:x['path']):
    b = available[e['path']]['content'].encode('utf-8')
    assert blob(b) == e['sha'], e['path']
    digest.update(e['path'][len(P):].encode('utf-8')); digest.update(b)
    scope_ids.append({'path':e['path'],'blob':e['sha'],'sha256':sha(b)})
assert digest.hexdigest()[:16] == '3f84c0db52d2b9ac'

ep = get('tools/env_profile.py')
ep_ast = ast.parse(ep)
assigns = {n.targets[0].id:n.value for n in ep_ast.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
header = ast.literal_eval(assigns['HEADER'])
directives = ast.literal_eval(assigns['DIRECTIVES'])
raw_lock = one('requirements-validation-C.lock.txt'); lock = raw_lock.decode('utf-8')
assert '\r' not in lock and lock.endswith('\n')
lock_directives = {}; dists = []; shadows = []
for line in lock.splitlines():
    if line.startswith('#@ shadowed '):
        m = re.fullmatch(r'#@ shadowed ([a-z0-9]+(?:-[a-z0-9]+)*)==([^\s#]+) record-sha256 ([a-f0-9]{64}|none)',line); assert m
        shadows.append(m.groups())
    elif line.startswith('#@ '):
        m = re.fullmatch(r'#@ ([a-z]+) (.+)',line); assert m and m[1] in directives and m[1] not in lock_directives
        lock_directives[m[1]] = json.loads(m[2]); assert isinstance(lock_directives[m[1]],str)
    elif line and not line.startswith('#'):
        m = re.fullmatch(r'([a-z0-9]+(?:-[a-z0-9]+)*)==([^\s#]+)  # record-sha256 ([a-f0-9]{64}|none)',line); assert m
        dists.append(m.groups())
assert set(lock_directives) == set(directives) and lock_directives['profile'] == 'C'
assert len(dists) == 170 and [x[0] for x in dists] == sorted(set(x[0] for x in dists))
assert len(shadows) == 2 and shadows == sorted(shadows)
canon = list(header) + ['#@ '+k+' '+json.dumps(lock_directives[k], ensure_ascii=False) for k in directives] + ['']
canon += [f'{n}=={v}  # record-sha256 {h}' for n,v,h in dists]
canon += [''] + [f'#@ shadowed {n}=={v} record-sha256 {h}' for n,v,h in shadows]
assert ('\n'.join(canon)+'\n').encode() == raw_lock

# YAML is treated as text: exact scalar blocks and raw content differences, not a general YAML parser.
btext = get('docs/22p_gap/env_profile_B_v4.yaml')
sources = re.findall(r'^- path: (.+)\n  bytes: (\d+)\n  sha256: ([a-f0-9]{64})', btext,re.M)
expected_env = re.search(r'^env:\n(.*?)^solver:',btext,re.M|re.S)[1]
def simple_scalars(block):
    pairs = re.findall(r'^\s+([a-zA-Z_]+): (.+)$',block,re.M)
    assert len(pairs) == 13 and len(dict(pairs)) == 13
    return dict(pairs)
env = simple_scalars(expected_env)
bchecks = []
for path,size,h in sources:
    s = get(path); raw = s.encode()
    assert len(raw)==int(size) and sha(raw)==h
    lines=s.splitlines(); blocks=[]; anchors={}
    for i,l in enumerate(lines):
        marker = re.fullmatch(r'\s*env:(?: ([&*]id\d+))?',l)
        if marker:
            if marker[1] and marker[1].startswith('*'):
                assert anchors[marker[1][1:]] == env
                blocks.append(i+1)
                continue
            indent=len(l)-len(l.lstrip()); block=[]
            for l2 in lines[i+1:]:
                if l2.strip() and len(l2)-len(l2.lstrip())<=indent: break
                block.append(l2)
            parsed_env = simple_scalars('\n'.join(block))
            assert parsed_env==env
            if marker[1]: anchors[marker[1][1:]] = parsed_env
            blocks.append(i+1)
    assert len(blocks)==2
    bchecks.append({'path':path,'bytes':len(raw),'sha256':sha(raw),'env_lines':blocks,'all_13_values_match':True})

oldref = '26c11d6fc7feeb92bd68fce4c3972d849ada2774'
def req_lines(s): return [x for x in s.splitlines(keepends=True) if x.strip() and not x.lstrip().startswith('#')]
assert req_lines(get('requirements.txt'))==req_lines(get('requirements.txt',oldref))
diffs = {}
for p in ['requirements.txt','scripts/smoke_e2e.sh','docs/22p_gap/make_receipt.py']:
    diffs[p] = '\n'.join(difflib.unified_diff(get(p,oldref).splitlines(),get(p).splitlines(),fromfile='gate89/'+p,tofile='gate90/'+p,lineterm=''))
receipt_checks=[]
for leg in ['paired_fixed5_v4','grid_fit_v5']:
    p = f'docs/22p_gap/receipts/{leg}.validate.yaml'
    old = get(p,'8113f12bd8f3e457670117ceef53501967e8594c')
    history = get(f'docs/22p_gap/receipts/history/{leg}.validate.803e2b7781cbc9cd.yaml')
    assert old==history
    new = get(p)
    old_core=old.split('\ncore:\n',1)[1].split('\nstamp:\n',1)[0]
    new_core=new.split('\ncore:\n',1)[1].split('\nstamp:\n',1)[0]
    def normalized_core(s):
        return re.sub(r'(?m)^(    (?:validator_source_digest|make_receipt_sha256): ).*',r'\1<generation>',s)
    assert normalized_core(old_core)==normalized_core(new_core)
    assert f'lock_sha256: {sha(raw_lock)}' in new
    core_sha = re.search(r'^core_sha256: ([a-f0-9]{64})$',new,re.M)[1]
    assert core_sha in get('docs/22p_gap/LEG_PRESERVATION.yaml')
    receipt_checks.append({'leg':leg,'history_byte_identical':True,'core_changes_only':['validator_source_digest','make_receipt_sha256'],'core_sha_recorded_not_recomputed':core_sha,'stamp_match_record_present':True,'anchor_present':True})

full = get('docs/22p_gap/gate90_evidence/12_full_replay_257d4cc1c_410_of_410_rc0.log')
replay={'killed':len(re.findall(r'^물었다',full,re.M)),'survived':len(re.findall(r'^★ 안 물었다',full,re.M)),'errors':len(re.findall(r'^★ 실행오류',full,re.M))}
assert replay=={'killed':410,'survived':0,'errors':0}
out={'method':'Text/hash/AST only; no submitted module import/function call, no suites, no solver, no installation.',
     'git_blob_checks':identities,'log_checks':log_checks,'run_scope':{'changed_files':changed_scope,'post_code_changes':post_scope,'file_count':len(scope_ids),'recomputed_source_digest':digest.hexdigest()[:16],'files':scope_ids},
     'lock':{'sha256':sha(raw_lock),'canonical':True,'directives':lock_directives,'dists':len(dists),'shadowed':shadows,'record_absent':sum(x[2]=='none' for x in dists)},
     'B_manifest_checks':bchecks,'B_total_env_locations':8,'requirements_lines_unchanged':True,'receipt_checks':receipt_checks,'replay_log_line_counts':replay,'small_diffs':diffs,
     'limitations':['Submitted logs were read, not independently rerun.','No environment measurement on producer host.','Receipt core hashes are recorded values checked against anchors; no YAML reserialization or restore/rescore was performed.']}
print(json.dumps(out,ensure_ascii=False,indent=2))
