import hashlib,json,zipfile,pathlib,sys,collections
ROOT=pathlib.Path(__file__).resolve().parent
ZIP=pathlib.Path('C:/Users/Administrator/Downloads/codex_rint2_rr_round2_6917c3c9fa39.zip')
with zipfile.ZipFile(ZIP) as z:
    names=[n for n in z.namelist() if not n.endswith('/')]
    m=z.read('MANIFEST.sha256').decode('utf-8').splitlines()
    checks=[]
    for line in m:
        h,p=line.split('  ',1)
        b=z.read(p)
        checks.append({'path':p,'match':hashlib.sha256(b).hexdigest()==h,'sha256':h,'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
    expected={x['path'] for x in checks}
    remote={e['path']:e for src in ROOT.glob('remote_entries*.json') for e in json.loads(src.read_text()) if e.get('type')=='file'}
    rc=[{'path':x['path'],'match':remote[x['path'][5:]]['sha']==x['git_blob']} for x in checks if x['path'].startswith('repo/') and x['path'][5:] in remote]
    missing=sorted({str(pathlib.PurePosixPath(x['path'][5:]).parent) for x in checks if x['path'].startswith('repo/') and x['path'][5:] not in remote})
    out={'zip_sha256':hashlib.sha256(ZIP.read_bytes()).hexdigest(),'zip_bytes':ZIP.stat().st_size,'manifest_count':len(checks),'manifest_failures':[x for x in checks if not x['match']],'unmanifested':sorted(set(names)-expected-{'MANIFEST.sha256'}),'repo_count':sum(x['path'].startswith('repo/') for x in checks),'remote_checked':len(rc),'remote_failures':[x for x in rc if not x['match']],'pending_dirs':missing,'files':checks,'remote_checks':rc}
    out['extracted_original_count']=len(checks)
    out['extracted_original_changed']=[x['path'] for x in checks if not (ROOT/'received'/x['path']).is_file() or hashlib.sha256((ROOT/'received'/x['path']).read_bytes()).hexdigest()!=x['sha256']]
    (ROOT/'intake_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k not in ('files','remote_checks')},indent=2))
