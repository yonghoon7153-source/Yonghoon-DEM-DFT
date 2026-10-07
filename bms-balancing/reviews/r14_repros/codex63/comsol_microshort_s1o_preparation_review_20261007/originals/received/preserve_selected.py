"""New static file-identity/copy script. Does not import selected programs."""
import json, pathlib, hashlib, datetime
ROOT=pathlib.Path(__file__).resolve().parent
WORK=ROOT.parent.parent
N=WORK/'outputs/normal480_offline_preparation_20261001'
paths=[N/p for p in ['CODE_MANIFEST.json','CONTRACT.json','COMMAND_MAP.json','NATIVE_APPROVAL_FIELD_SPEC.json','PARENT_COMMAND.ps1','src/Normal480Candidate.java','src/diagnostic_consumer.py','src/candidate_entry.py']]
paths += [WORK/'outputs/b020_profile_unit_stages_20260927/src'/p for p in ['launcher.py','winjob.py']]
def identity(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
manifest=json.loads((N/'CODE_MANIFEST.json').read_bytes())
assert identity(N/'CODE_MANIFEST.json')['sha256']=='7a5cc2f1717ae7a80cd7e423861965ad51c5f639272eab7f3a3c7680499ae22c'
for f in manifest['files']:
    got=identity(N/f['file']); assert (got['bytes'],got['sha256'])==(f['bytes'],f['sha256'])
identities=[identity(p) for p in paths]
for p in paths:
    rel=p.relative_to(WORK/'outputs'); dest=ROOT/'reference/legacy'/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as out: out.write(p.read_bytes())
record=dict(kind='SELECTED_LEGACY_ORIGINAL_IDENTITIES_BEFORE_AUTHORING_CHANGES',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=identities,scope='selected code/contracts only; no MPH/prefs/process inspection',originals_modified=False)
with (ROOT/'SELECTED_ORIGINALS_BEFORE.json').open('x',encoding='utf-8') as f: json.dump(record,f,indent=2)
print(json.dumps(dict(files=len(paths),normal480_manifest_verified=True,source_originals_modified=False)))
