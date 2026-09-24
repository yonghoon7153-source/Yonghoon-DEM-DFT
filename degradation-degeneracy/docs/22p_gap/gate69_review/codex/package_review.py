"""Package existing recipient review evidence; no product/test execution."""
import datetime,hashlib,json,pathlib,sys,zipfile
import pytest
from review_checks import HERE,dump,sha

def read(p):return json.loads((HERE/p).read_text(encoding='utf-8'))
assert read('IDENTITY.json')['request_raw_equal']
assert read('targeted.pytest.json')['summary']=={'passed':41,'total':41,'collected':41}
assert read('preimages.json')['rc']==0
assert (HERE/'source_digest.stdout.bin').read_text(encoding='utf-8').strip()=='e9ee7475dea7de1d'
rows=read('older_premise_mutations/RESULTS.json')
rows.append({'phases':read('mutation/RESULTS.json')['rows'],'original_unchanged':read('mutation/RESULTS.json')['original_unchanged']})
for r in rows:
    assert r['original_unchanged']
    assert r['phases']['baseline']['rc']==0
    m=r['phases']['mutant'];assert m['rc']==1 and m['exact_failed_set'] and m['call_only'] and all(m['witnesses'].values())
pres=read('FINAL_PRESERVATION.json')
assert pres['status_after']=='' and pres['registry_byte_mismatches']==[]
assert pres['registry_tracked']==pres['registry_disk_json']==367
for row in read('ARCHIVE_SET_AND_SIZE_CHECKS.json'):
    assert row['exact_set'] and not row['duplicate_names'] and not row['case_collision']
    assert not row['unsafe_paths_or_links'] and not row['manifest_size_errors'] and row['CRC_bad'] is None
    assert not row['git_blob_size_errors']
dump(HERE/'REVIEW_VERIFICATION_SUMMARY.json',dict(
    verdict='ACCEPT_G68_T1_AND_SCOPED_GATE69_CLOSURE_NOT_MAIN_RUN_GO',
    python=sys.version,pytest=pytest.__version__,head=pres['head'],new_blocking_findings=0,
    targeted_pass=41,real_premise_child_cases=7,recipient_record_variants=7,
    premise_registered_mutations=4,git_manifest_counts={'66':107,'67':350,'68':141},
    product_source_modified=False,full_scientific_suite_run=False,main_run_authorized=False,comsol_runs=0))

zp=HERE/'GATE69_REVIEW_HANDOFF_20260924.zip'
assert not zp.exists()
excluded={'MANIFEST.json',zp.name,'DELIVERY_RECEIPT.json'}
files=[]
for p in sorted(HERE.rglob('*')):
    if not p.is_file() or p.name in excluded or '__pycache__' in p.parts:continue
    assert not p.is_symlink()
    b=p.read_bytes();files.append(dict(path=p.relative_to(HERE).as_posix(),bytes=len(b),sha256=sha(b)))
manifest=dict(scope='Gate69 recipient review; not main-execution approval',head=pres['head'],payload_count=len(files),files=files)
dump(HERE/'MANIFEST.json',manifest)
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for f in files:z.write(HERE/f['path'],f['path'])
    z.write(HERE/'MANIFEST.json','MANIFEST.json')
with zipfile.ZipFile(zp) as z:
    names=z.namelist();assert len(names)==len(set(names))==len({n.casefold() for n in names})
    assert set(names)=={'MANIFEST.json'}|{f['path'] for f in files}
    assert z.testzip() is None
    for f in files:
        b=z.read(f['path']);assert len(b)==f['bytes'] and sha(b)==f['sha256']
    assert z.read('MANIFEST.json')==(HERE/'MANIFEST.json').read_bytes()
receipt=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    archive=zp.name,bytes=zp.stat().st_size,sha256=sha(zp.read_bytes()),payload_count=len(files),
    manifest_sha256=sha((HERE/'MANIFEST.json').read_bytes()),all_payload_size_sha_crc_verified=True,
    recipient_verification=None,verdict=read('REVIEW_VERIFICATION_SUMMARY.json')['verdict'])
dump(HERE/'DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=True))
