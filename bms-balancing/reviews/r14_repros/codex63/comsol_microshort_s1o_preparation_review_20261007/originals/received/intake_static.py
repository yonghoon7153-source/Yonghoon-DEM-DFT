"""New S1-O data-only archive/identity reader; never imports received code."""
import hashlib, json, pathlib, stat, zipfile, datetime
ROOT = pathlib.Path(__file__).resolve().parent
INPUTS = [pathlib.Path('C:/Users/BML/Desktop') / n for n in [
    'COMSOL_MICROSHORT_S0_DEEP_HANDOFF_20261007.zip',
    'COMSOL_MICROSHORT_S1O_EXEC_COVER_20261007 (1).md',
    'COMSOL_MICROSHORT_S1O_SEND_TO_CODEX_v2_20261007 (1).md']]
def ident(p):
    b=p.read_bytes(); return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
out=ROOT/'reference'
out.mkdir(exist_ok=False)
ids=[ident(p) for p in INPUTS]
assert ids[0]['sha256']=='e8c386913338198c9b1535a9131667f23c8a144232ae8fbf548acfd3748ea12e'
assert ids[2]['sha256']=='16797cc16cf5b95bcef6e55d7f342b288300859c8d68df55bb7860a6a5e1b967'
with zipfile.ZipFile(INPUTS[0]) as z:
    names=z.namelist()
    assert len(names)==len(set(n.casefold() for n in names))
    for i in z.infolist():
        p=pathlib.PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename
        assert not stat.S_ISLNK(i.external_attr >> 16)
    m=json.loads(z.read('MANIFEST.json'))
    assert set(names)=={f['path'] for f in m['files']}|{'MANIFEST.json'}
    for f in m['files']:
        b=z.read(f['path'])
        assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
    for n in names:
        p=out/'s0'/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(z.read(n))
    for p in INPUTS[1:]: (out/p.name).write_bytes(p.read_bytes())
result=dict(kind='READ_ONLY_INTAKE_AND_RAW_REFERENCE_COPY',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=ids,payload_count=len(m['files']),entry_count=len(names),sha_crc_path_exact_set=True,received_code_executed=False)
(ROOT/'INPUTS_BEFORE.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
