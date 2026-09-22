"""Package only explicit review artifacts; never packages target/input/fixture trees."""
import hashlib, json, pathlib, zipfile
HERE=pathlib.Path(__file__).resolve().parent
NAMES=[
    'R17_REVIEW.md','CLAUDE_REPLY.md','REPRO_README.md','TEST_STATUS.md','REVIEW_IDENTITY.json',
    'repro_r17.py','science_repro.py','run_checks.py','package_review.py',
    'REPRO_RESULTS.json','SCIENCE_REPRO_RESULTS.json',
    'pytest_full.log','pytest_full.json','pytest_r15_r16.log','pytest_r15_r16.json',
    'pytest_r15_r16_local.log','pytest_r15_r16_local.json','pytest_targeted.xml',
    'pytest_width_contract.log','pytest_width_contract.json','pytest_width.xml',
    'check_u14_current.log','check_u14_current.json','check_u14_oldrev.log','check_u14_oldrev.json',
    'check_u14_legacy_archive.log','check_u14_legacy_archive.json'
]
def sha(b):return hashlib.sha256(b).hexdigest()
assert len(NAMES)==len(set(NAMES))
blobs={n:(HERE/n).read_bytes() for n in NAMES}
manifest=json.dumps({'scope':'R17 reviewer artifacts only; no input battery workbooks/MPH',
                    'target_commit':'dfc1fc78b3396c95709650860f1502c0e83ead40',
                    'entries':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in blobs.items()]},
                   ensure_ascii=False,indent=2).encode('utf-8')
out=HERE/'R17_REVIEW_PACKAGE.zip'
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in blobs.items():z.writestr(n,b)
    z.writestr('MANIFEST.json',manifest)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(NAMES)+1 and len(set(z.namelist()))==len(NAMES)+1
    assert set(z.namelist())==set(NAMES)|{'MANIFEST.json'}
    for n,b in blobs.items():assert z.read(n)==b
receipt={'zip':str(out),'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),
         'payloads':len(NAMES),'entries':len(NAMES)+1,'manifest_sha256':sha(manifest),
         'verified_exact_set_sha_crc':True}
(HERE/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))

