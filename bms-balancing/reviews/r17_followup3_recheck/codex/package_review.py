"""Package existing review evidence only. Does not run attached/product code."""
import hashlib, json, pathlib, zipfile

ROOT=pathlib.Path(__file__).resolve().parent
def digest(data): return hashlib.sha256(data).hexdigest()
def tree(folder):
    for p in (ROOT/folder).rglob('*'):
        if p.is_file() and not any(x in {'venv-off','venv-on','__pycache__','.git'} for x in p.relative_to(ROOT/folder).parts):
            if p.is_symlink(): raise ValueError(str(p))
            yield p
def direct_prefixes(prefixes):
    return [p for p in ROOT.iterdir() if p.is_file() and any(p.name.startswith(x) for x in prefixes)]
shared = [ROOT/x for x in ['README_KO.md','run_checks.py','package_review.py']]
shared += direct_prefixes(['head.','head_after_','status_before.','status_after_'])
shared += [ROOT/'final_checks/ENVIRONMENT.json',ROOT/'final_checks/SOURCE_IDENTITIES.json']
send=pathlib.Path('C:/Users/Administrator/Downloads/SEND_R17_GATE68_2026-09-23.md')

r17 = shared + [ROOT/'R17_REVIEW_KO.md',ROOT/'R17_CLAUDE_REPLY.md']
r17 += direct_prefixes(['r17_','control_','gc_extra_'])
r17 += list(tree('r17_repros'))+list(tree('r17_controls'))
r17 += list(tree('final_checks/source_snapshots/bms-balancing'))

gate = shared + [ROOT/'GATE68_REVIEW_KO.md',ROOT/'GATE68_CLAUDE_REPLY.md',ROOT/'final_checks.py']
gate += direct_prefixes(['gate_','gate-','repro_boundaries.','repro_gate68_t1.','run_scope_log.','source_digest'])
gate += list(tree('gate_mutations'))+list(tree('gate-boundaries_short'))+list(tree('t1_setup_only'))
gate += [ROOT/'final_checks/COMMITTED_ENTRY_RESULTS.json']
gate += list(tree('final_checks/source_snapshots/degradation-degeneracy'))
gate += [ROOT/'final_checks/source_snapshots/CLAUDE.md']

result=[]
for kind, paths in [('R17',r17),('GATE68',gate)]:
    entries={p.relative_to(ROOT).as_posix():p.read_bytes() for p in paths}
    entries['request/SEND_R17_GATE68_2026-09-23.md']=send.read_bytes()
    assert len(entries)==len({x.casefold() for x in entries})
    assert all(not x.startswith('/') and '..' not in pathlib.PurePosixPath(x).parts for x in entries)
    rows=[dict(path=n,bytes=len(b),sha256=digest(b)) for n,b in sorted(entries.items())]
    manifest=(json.dumps(dict(scope=kind,head='a1979cdf5b9f04234b6a441150e161bd4f0a3ced',
        payload_count=len(rows),files=rows),ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    entries['MANIFEST.json']=manifest
    dest=ROOT/(kind+'_REVIEW_HANDOFF_20260924.zip')
    with zipfile.ZipFile(dest,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n,b in sorted(entries.items()):z.writestr(n,b)
    with zipfile.ZipFile(dest) as z:
        assert len(z.namelist())==len(set(z.namelist()))==len(entries)
        assert set(z.namelist())==set(entries)
        assert z.testzip() is None
        for n,b in entries.items():assert z.read(n)==b
    raw=dest.read_bytes()
    result.append(dict(kind=kind,file=dest.name,bytes=len(raw),sha256=digest(raw),
        payload_count=len(rows),entries=len(entries),manifest_sha256=digest(manifest),
        exact_set_size_sha_crc=True,recipient_verification=None))
receipt=ROOT/'REVIEW_DELIVERY_RECEIPT.json'
with receipt.open('x',encoding='utf-8',newline='\n') as f:
    json.dump(dict(scope='Reviewer-generated evidence packages; not a product execution approval',packages=result),f,ensure_ascii=False,indent=2)
    f.write('\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
