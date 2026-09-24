"""Read-only identity/preservation checks and selected source snapshots."""
import hashlib,json,pathlib,subprocess,zipfile
from review_checks import HERE,REPO,DD,HEAD,BASE,git,dump,sha

source_paths=['tests/phase_witness.py','tests/test_gate66_defensive.py','tests/test_gate68_defensive.py',
              'docs/22p_gap/mutation_replay.py','tests/interpreter_fixture.py','tests/test_gate65_defensive.py',
              'tests/test_gate67_defensive.py','tests/conftest.py']
source=[]
for rel in source_paths:
    blob=git('show',f'{HEAD}:degradation-degeneracy/{rel}')
    dst=HERE/'target_source'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(blob)
    source.append(dict(path=rel,bytes=len(blob),sha256=sha(blob),working_bytes_same=(DD/rel).read_bytes()==blob))
dump(HERE/'SOURCE_SNAPSHOT_MANIFEST.json',source)

archive_checks=[]
prior=json.loads((HERE/'GIT_BLOB_MANIFEST_CHECKS.json').read_text(encoding='utf-8'))
for g in (66,67,68):
    folder=DD/'docs/22p_gap'/f'gate{g}_review';archive=next(folder.glob('*.zip'))
    mn='REVIEW_MANIFEST.json' if g==67 else 'MANIFEST.json'
    with zipfile.ZipFile(archive) as z:
        m=json.loads(z.read(mn));es=m.get('files') or next(x for x in m.values() if isinstance(x,list))
        names=[x.filename for x in z.infolist()];wanted={mn}|{e.get('path') or e.get('file') for e in es}
        issues=[]
        for i in z.infolist():
            p=pathlib.PurePosixPath(i.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in i.filename or ':' in i.filename:issues.append(i.filename)
            if (i.external_attr>>16)&0o170000==0o120000:issues.append(i.filename+':symlink')
        size_wrong=[]
        for e in es:
            p=e.get('path') or e.get('file');expected=e.get('bytes',e.get('size'))
            actual=z.getinfo(p).file_size
            if expected is not None and actual!=expected:size_wrong.append(p)
        archive_checks.append(dict(gate=g,raw_sha256=sha(archive.read_bytes()),entries=len(names),
            exact_set=set(names)==wanted,duplicate_names=len(names)!=len(set(names)),
            case_collision=len(names)!=len({n.casefold() for n in names}),unsafe_paths_or_links=issues,
            manifest_size_errors=size_wrong,CRC_bad=z.testzip(),
            git_blob_size_errors=[e['path'] for e in prior[str(g)]['rows'] if e['size']!=z.getinfo(e['path']).file_size]))
dump(HERE/'ARCHIVE_SET_AND_SIZE_CHECKS.json',archive_checks)

registry='degradation-degeneracy/docs/22p_gap/_exec_class'
tracked=git('ls-files','--',registry).decode().splitlines()
files=sorted((REPO/registry).glob('*.json'));bad=[]
for p in files:
    rel=p.relative_to(REPO).as_posix()
    if rel not in tracked or sha(p.read_bytes())!=sha(git('show',f'{HEAD}:{rel}')):bad.append(rel)
row=dict(head=git('rev-parse','HEAD').decode().strip(),status_after=git('status','--porcelain=v1').decode(),
    scope_last_commit=git('-C',str(DD),'log','-1','--format=%H','--','src','tools','configs','scripts','run.sh','requirements*.txt').decode().strip(),
    registry_tracked=len(tracked),registry_disk_json=len(files),registry_byte_mismatches=bad,
    registry_delta_from_prior=git('diff','--name-status',BASE,HEAD,'--',registry).decode(),
    selected_source_equal=all(x['working_bytes_same'] for x in source))
dump(HERE/'FINAL_PRESERVATION.json',row)

docs={}
for key,argv in {
    'D1_old_fixed_commit_difference':['diff','--numstat','a31be7a9',BASE,'--','degradation-degeneracy'],
    'D1_old_code_excluding_request':['diff','--name-only','a31be7a9',BASE,'--','degradation-degeneracy',':!degradation-degeneracy/docs/22p_gap/GATE68_REQUEST.md'],
    'attributes_before_readdition':['log','--reverse','--format=%H %s','90c766f^..afab648','--','degradation-degeneracy/.gitattributes',
        'degradation-degeneracy/docs/22p_gap/gate66_review','degradation-degeneracy/docs/22p_gap/gate67_review','degradation-degeneracy/docs/22p_gap/gate68_review'],
}.items():
    b=git(*argv);(HERE/(key+'.txt')).write_bytes(b);docs[key]=b.decode('utf-8')
dump(HERE/'DOCUMENT_IDENTITIES.json',docs)
print(json.dumps(row,ensure_ascii=True),flush=True)
