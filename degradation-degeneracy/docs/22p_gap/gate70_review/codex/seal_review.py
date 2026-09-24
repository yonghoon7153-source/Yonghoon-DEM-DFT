"""Reviewer-owned evidence collection and delivery; never invokes product code."""
import hashlib, json, pathlib, subprocess, sys, zipfile

OUT=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('C:/Users/Administrator/Documents/Codex/g70_20260924')
DD=REPO/'degradation-degeneracy'
def sha(b): return hashlib.sha256(b).hexdigest()
def save(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args): return subprocess.check_output(['git',*args],cwd=REPO)

if sys.argv[1]=='collect':
    ranges={
      'run.sh':[(15,65),(161,235),(249,322),(343,381),(404,419),(509,565)],
      'src/io.py':[(37,80),(81,178),(194,230),(1670,1720)],
      'tools/preserve.py':[(2979,3017),(3245,3268),(4335,4356),(4873,4888),(4950,5012),(5076,5112),(5380,5394),(5580,5599),(5750,5819),(5883,5927),(6380,6410),(7248,7293),(7380,7398),(7464,7524),(7770,7786),(7946,7962)],
      'tests/conftest.py':[(40,58),(145,194)],
      'tests/test_runner.py':[(51,110)],
      'tests/test_docs_lint.py':[(9185,9228)],
      'tests/test_compare.py':[(930,954)],
      'scripts/smoke_e2e.sh':[(118,134),(214,255)],
      'scripts/archive_results.sh':[(135,166)],
      'docs/22p_gap/LEG_PRESERVATION.yaml':[(620,644),(654,768)],
      'docs/22p_gap/GATE63_REQUEST.md':[(40,68)],
      'docs/22p_gap/GATE49_REQUEST.md':[(8,26)],
      'docs/08_REVIEW_RESPONSE.md':[(7080,7110)],
      'docs/22p_gap/STAGE3_CONTRACT.md':[(433,443),(483,490),(753,767),(1222,1277),(1500,1525)],
      'docs/22p_gap/row_projection.py':[(2395,2414),(2480,2499),(3525,3578)],
      'docs/22p_gap/mutation_replay.py':[(6830,6883),(6960,6986),(7106,7202)],
      'tools/archive_bundle.py':[(288,307),(362,395)],
      'docs/22p_gap/make_receipt.py':[(135,168),(193,239)],
    }
    dest=OUT/'source_excerpts';dest.mkdir(exist_ok=False)
    index={}
    for name,spans in ranges.items():
        p=DD/name;raw=p.read_bytes();lines=raw.decode('utf-8').splitlines()
        content=['# '+name,'# Entire source SHA-256: '+sha(raw),'# Fixed HEAD: 8568f782db3acbf00d872ce5527147258c00bec7']
        for lo,hi in spans:
            content.append('\n# Lines '+str(lo)+'-'+str(hi))
            content.extend(f'{i}: {lines[i-1]}' for i in range(lo,min(hi,len(lines))+1))
        target=dest/(name.replace('/','__')+'.txt')
        target.write_text('\n'.join(content)+'\n',encoding='utf-8')
        index[name]={'source_bytes':len(raw),'source_sha256':sha(raw),'ranges':spans,'excerpt':target.name}
    save(dest/'INDEX.json',index)
    before=json.loads((OUT/'SOURCE_BEFORE.json').read_text(encoding='utf-8'))
    after={};changed=[]
    for name,old in before.items():
        p=REPO/name
        now={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} if p.is_file() else None
        after[name]=now
        if now!=old:changed.append(name)
    save(OUT/'SOURCE_AFTER.json',after)
    registry=DD/'docs/22p_gap/_exec_class'
    tracked=[x.decode() for x in git('ls-files','-z','degradation-degeneracy/docs/22p_gap/_exec_class/*.json').split(b'\0') if x]
    disk=list(registry.glob('*.json'))
    claims=DD/'docs/22p_gap/_claims'
    row={'head':git('rev-parse','HEAD').decode().strip(),'tracked_files_compared':len(before),'changed':changed,
      'git_status_porcelain':git('status','--porcelain=v1').decode(),
      'registry_top_level_disk_json_count':len(disk),'registry_tracked_matching_path_count':len(tracked),
      'original_checkout_side_effect':{'path':str(claims),'exists':claims.exists(),'members':[p.name for p in claims.iterdir()] if claims.exists() else [],
        'cause':'Subagent precheck created lifecycle root before Windows mount check failed. No claim files; directory retained.'},
      'scope':'Tracked DD file bytes and registry observation, not all OS writes or all processes. Review worktree/git administrative creation excluded from unchanged claim.',
      'main_science_runs':0,'comsol_calls':0,'product_edits':0,'restorations':0,'historical_class_changes':0}
    save(OUT/'PRESERVATION_REVIEW.json',row)
    assert not changed and not row['git_status_porcelain']
    print(json.dumps(row,ensure_ascii=False))

elif sys.argv[1]=='package':
    target=OUT/'GATE70_REVIEW_20260924.zip'
    assert not target.exists()
    files=[]
    for p in sorted(OUT.rglob('*')):
        if p.is_file() and p.name not in {'MANIFEST.json','GENERATION_RECEIPT.json'} and p.suffix!='.zip' and '__pycache__' not in p.parts:
            files.append(p)
    manifest={'format':'review-payload-manifest/v1','files':[{'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]}
    save(OUT/'MANIFEST.json',manifest)
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files+[OUT/'MANIFEST.json']:z.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(target) as z:
        names=z.namelist();expected=[r['path'] for r in manifest['files']]+['MANIFEST.json']
        assert len(names)==len(set(names))==len(set(n.casefold() for n in names))
        assert set(names)==set(expected) and z.testzip() is None
        for info in z.infolist():
            assert not info.filename.startswith(('/','\\')) and '..' not in pathlib.PurePosixPath(info.filename).parts
            assert not ((info.external_attr>>16)&0o170000)==0o120000
        for row in manifest['files']:
            raw=z.read(row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
        assert z.read('MANIFEST.json')==(OUT/'MANIFEST.json').read_bytes()
    raw=target.read_bytes()
    receipt={'scope':'Receiver review package; no product execution authorization','file':target.name,'bytes':len(raw),'sha256':sha(raw),'payload_count':len(files),'entries_including_manifest':len(files)+1,'manifest_sha256':sha((OUT/'MANIFEST.json').read_bytes()),'exact_set_size_sha_crc_names_paths_links_verified':True,'recipient':None,'verdict':'NO-GO_CURRENT_MAIN_RUN'}
    save(OUT/'GENERATION_RECEIPT.json',receipt);print(json.dumps(receipt,ensure_ascii=False))
