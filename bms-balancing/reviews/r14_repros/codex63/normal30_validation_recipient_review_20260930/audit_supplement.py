"""Read-only source archive and data validation; submitted code is not executed."""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile
R=Path(__file__).resolve().parent
p=Path('C:/Users/Administrator/Downloads/COMSOL63_NORMAL30_DELIVERY_SUPPLEMENT_20260930.zip')
b=p.read_bytes()
def sha(x):return hashlib.sha256(x).hexdigest()
with zipfile.ZipFile(io.BytesIO(b)) as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len(set(n.casefold() for n in names))
    for e in z.infolist():
        path=PurePosixPath(e.filename)
        assert not path.is_absolute() and '..' not in path.parts and '\\' not in e.filename and ':' not in e.filename
        assert not stat.S_ISLNK(e.external_attr>>16) and not e.is_dir()
    assert z.testzip() is None
    data={n:z.read(n) for n in names}
m=json.loads(data['MANIFEST.json'])
assert set(names)=={v['file'] for v in m['files']}|{'MANIFEST.json'}
for v in m['files']:
    assert len(data[v['file']])==v['bytes'] and sha(data[v['file']])==v['sha256']
out=R/'supplement'
assert not out.exists()
out.mkdir()
for n,v in data.items():(out/n).write_bytes(v)
receipt=json.loads(data['DELIVERY_RECEIPT.json'])
tr=json.loads(data['FINAL_PACKAGE_TOOL_RETURN_TRANSCRIPTION.json'])
main=json.loads((R/'PACKAGE_AUDIT.json').read_bytes())
assert receipt['zip']['bytes']==main['bytes'] and receipt['zip']['sha256']==main['sha256']
assert receipt['manifest']['sha256']==main['manifest_sha256'] and receipt['payloads']==102 and receipt['entries']==103
assert json.loads(tr['result']['output'])==receipt and tr['result']['exit_code']==0
assert receipt['recipient'] is None and receipt['native_executed'] is False
report=dict(bytes=len(b),sha256=sha(b),payloads=5,entries=6,manifest_sha256=sha(data['MANIFEST.json']),size_sha_crc_exact_set_path_link_checks=True,
    main_archive_and_manifest_match=True,receipt_sha256=sha(data['DELIVERY_RECEIPT.json']),transcribed_output_semantically_equals_receipt=True,
    return_provenance=tr['provenance'],transcribed_chunk_id=tr['result']['chunk_id'],transcribed_host_rc=tr['result']['exit_code'],
    reported_overall_snapshot_s=receipt['overall_elapsed_s'],reported_successful_closeout_snapshot_s=receipt['packaging_elapsed_s'],
    final_receipt_write_and_final_return_elapsed_measured=False,complete_packaging_phase_elapsed_measured=False,
    limitations='Snapshots precede final receipt write; successful closeout timer omits earlier failed packaging attempt. No retrospective clock fabrication or source rerun.')
(R/'SUPPLEMENT_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
