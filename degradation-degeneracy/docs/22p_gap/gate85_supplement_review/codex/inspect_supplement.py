"""Reviewer-owned ZIP/text inspection; never executes submitted scripts."""
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

HERE=Path(__file__).resolve().parent
REF=HERE/'reference'
E=HERE/'evidence'
OLD=HERE.parent/'gate85_review_20261001'
Z=Path('C:/Users/Administrator/Downloads/README (1).zip')
PREFIX='degradation-degeneracy/docs/22p_gap/gate85_evidence/'
COMMIT='1b49700e65fb6408caa48124df365264e32480a9'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def js(p):
    return json.loads(p.read_text(encoding='utf-8'))

def dump(n,d):
    (HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def save(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and p.read_bytes()!=b:
        raise ValueError('Reference collision '+str(p))
    p.write_bytes(b)

before={p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
zb=Z.read_bytes()
remote={}
for p in E.glob('degradation-degeneracy__*.json'):
    d=js(p)
    b=d['content'].encode('utf-8')
    assert d['requested_ref']==COMMIT and blob(b)==d['sha']
    rel=d['requested_path']
    if rel.startswith(PREFIX):
        rel=rel.removeprefix(PREFIX)
        remote[rel]=b
        save(REF/'committed'/rel,b)
    else:
        save(REF/'metadata'/Path(rel).name,b)
readme=remote['README.md'].decode('utf-8')
listed={path:{'bytes':int(size),'sha256_prefix':prefix} for path,size,prefix in re.findall(r'^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{16})` \|$',readme,re.M)}
assert len(listed)==25
for rel,b in remote.items():
    if rel=='README.md':
        continue
    assert len(b)==listed[rel]['bytes'] and sha(b).startswith(listed[rel]['sha256_prefix'])
zip_members={}
with zipfile.ZipFile(Z) as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    assert sum(x.file_size for x in z.infolist())<2000000
    assert z.testzip() is None
    for info in z.infolist():
        n=info.filename;p=PurePosixPath(n)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n
        assert stat.S_IFMT(info.external_attr>>16)!=stat.S_IFLNK and not info.is_dir()
        b=z.read(info)
        rel='README.md' if n=='README (1).md' else next(k for k in listed if PurePosixPath(k).name==n)
        assert rel not in zip_members
        if rel in remote:
            assert b==remote[rel]
        if rel in listed:
            assert len(b)==listed[rel]['bytes'] and sha(b).startswith(listed[rel]['sha256_prefix'])
        zip_members[rel]=b
        save(REF/'attached'/rel,b)
rows=[]
for rel,item in listed.items():
    b=remote.get(rel,zip_members.get(rel))
    rows.append({'path':rel,'readme':item,'in_commit':rel in remote,'in_attachment':rel in zip_members,
                 'available':b is not None,'actual_bytes':len(b) if b is not None else None,
                 'actual_sha256':sha(b) if b is not None else None})
comp=js(E/'COMMIT_COMPARE.json')
assert comp['merge_base_commit']['sha']=='b49c24fabe94be7a5986bdc54de2d4278c4ebf65'
assert comp['behind_by']==0 and len(comp['files'])<300
scope_prefixes=tuple('degradation-degeneracy/'+s+'/' for s in ['src','tools','scripts','configs'])
assert not any(x['filename'].startswith(scope_prefixes) or x['filename'].split('/')[-1] in ['run.sh','requirements.txt','requirements-gpu.txt'] for x in comp['files'])
replay=remote['full_replay/g85_replay_all.txt'].decode()
lines=replay.splitlines()
killed=[x for x in lines if re.match(r'^물었다\s',x)]
missed=[x for x in lines if '★ 안 물었다' in x]
assert len(killed)==344 and len(missed)==1
aborted=remote['full_replay_aborted/g84_replay_all.txt'].decode().splitlines()
aborted_counts={label:sum(bool(re.match(pattern,x)) for x in aborted) for label,pattern in [('killed_lines',r'^물었다\s'),('unmatched_lines',r'^★ 안 물었다\s'),('error_prefix_lines_including_partial_final_line',r'^★ 실행오류\s')]}
cmd=remote['probe/probe_g84_real_reasons.as_run.command.txt'].decode()
assert cmd.split('\n',1)[1].rsplit('\nEOF',1)[0]+'\n'==remote['probe/probe_g84_real_reasons.as_run.py'].decode()
original=remote['probe/g84_probe_real_reasons.txt'].decode().splitlines()
assert len(original)==5 and all('STARTED_AND_FINISHED fits=True' in x for x in original)
after={p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
assert after==before and sha(Z.read_bytes())==sha(zb)
dump('SUPPLEMENT_INTEGRITY.json',{'input_zip':{'path':str(Z),'bytes':len(zb),'sha256':sha(zb),'entries':len(zip_members),'CRC_path_case_link_checks':True},
 'commit':COMMIT,'listed_payload':len(listed),'committed_payload':len(remote)-1,
 'attached_payload':len(zip_members)-1,'listed_available':sum(x['available'] for x in rows),
 'attachment_readme_matches_commit':zip_members['README.md']==remote['README.md'],
 'not_available':[x['path'] for x in rows if not x['available']],
 'uncommitted_attachment_payload':[x for x in zip_members if x not in remote],'files':rows,
 'RUN_SCOPE_changed':False,'source_digest_inherited_from_verified_previous_head':'ba51cd20caa10b7b',
 'received_code_executed':False})
dump('LOG_INDEX.json',{'original_probe_lines':original,'full_replay_tail':lines[-14:],
 'complete_replay_counts':{'killed':len(killed),'unmatched':len(missed),'total_ran':345},
 'aborted_stdout_counts':aborted_counts,'aborted_readme_claim':{'killed':193,'unmatched':3,'execution_errors':1},
 'original_script_matches_command_heredoc':True,
 'lines_with_unmatched_witness':missed,'preimages':[x for x in lines if 'preimage' in x or '정확히' in x],
 'limits':'Only submitted text inspected. Runtime facts are supplied evidence, not direct reviewer remote observation or OS audit.'})
dump('SELECTED_PRESERVATION.json',{'scope':'Original local Gate85 review and input ZIP','before':before,'after':after,'pass':before==after,'input_zip_unchanged':True})
print(json.dumps({'status':'SUPPLEMENT_BYTES_VERIFIED','zip_entries':len(zip_members),'listed':len(listed),
 'committed':len(remote)-1,'available':sum(x['available'] for x in rows),'missing':[x['path'] for x in rows if not x['available']],
 'prior_files_unchanged':len(before),'received_code_executed':False},ensure_ascii=False))
