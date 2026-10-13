"""Reviewer's data-only packaging. Does not import any submitted source."""
import hashlib
import json
import pathlib
import zipfile
from datetime import datetime, timezone

root = pathlib.Path(__file__).resolve().parent
workspace = root.parent.parent
pairs = [
    (pathlib.Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_NEXT_SCOPE_PROPOSAL_20261013.md'), 'received/NEXT_SCOPE_PROPOSAL.md', 'a7e376074cd97195e63098ccd25a921e678538ba0c6e880eaba1934dadd3b5ef'),
    (pathlib.Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OS_B_SEND_20261013.md'), 'received/OS_B_SEND_V1.md', '2181ddf1faca7b416eac709ebc7bc6f217f5c1522b7fa46089240b603a04c095'),
    (workspace / 'outputs/microshort_s1_open_connection_review_20261010/received/SEPARATE_ALLOWLIST_DRAFT_KO.md', 'basis/SEPARATE_ALLOWLIST_DRAFT_KO.md', 'da407349e62a25800236a32ef9fba0752ab5bdda0f013667f16fd52f6f0e3087'),
    (workspace / 'outputs/s1_open_r1_003_review_20261013/evidence/reference/067_RESOURCE_CONTRACT.json', 'basis/RESOURCE_CONTRACT.json', 'e45837427b1b8a69d53b10119ce7ab072bacb869bcdd53c863366c7bd04c67c1'),
    (workspace / 'outputs/microshort_s1_open_connection_r1_review_20261011/received/CODE_MANIFEST.json', 'basis/CODE_MANIFEST.json', 'feb12ef6991141aab59fd2fbc0d5f0d138bdd735255aa7123274503ce80b8ecc'),
    (workspace / 'outputs/microshort_s1_open_connection_r1_review_20261011/received/candidate/resource_connection.py.inactive.txt', 'basis/resource_connection.py.inactive.txt', 'f45e6531383d03daa2e968437c6188be0229c144c6956647b0b0f81fae795816'),
    (workspace / 'outputs/microshort_s1_open_connection_r1_review_20261011/received/OS_API_MATRIX.json', 'basis/OS_API_MATRIX.json', 'ec3ab0c209a5aab458fada593c31c63b73f6eec43b902a718823a2391d57622c'),
    (workspace / 'outputs/s1_open_r1_003_review_20261013/REVIEW_KO.md', 'basis/REVIEW_003_KO.md', 'bbc1247b38afcd965cf04034baf9bb3b90acb326ea81ced68ca48f11abe82507'),
]

def digest(b):
    return hashlib.sha256(b).hexdigest()

def write_new(name, obj):
    p = root / name
    with p.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write('\n')

source_rows = []
for source, copy, expected in pairs:
    b = source.read_bytes()
    assert digest(b) == expected, str(source)
    assert (root / copy).read_bytes() == b, copy
    blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    source_rows.append({'source': str(source), 'copy': copy, 'bytes': len(b), 'sha256': expected, 'git_blob_sha': blob, 'unchanged_from_intake': True})
remote = json.loads((root / 'REMOTE_SOURCES.json').read_text(encoding='utf-8'))
for row, repo_row in zip(source_rows[:2], remote[:2]):
    assert row['git_blob_sha'] == repo_row['git_blob_sha'], row['copy']
review_zip = workspace / 'outputs/s1_open_r1_003_review_20261013/COMSOL_MICROSHORT_S1_OPEN_R1_003_REVIEW_REPLY_20261013.zip'
prior = review_zip.read_bytes()
assert len(prior) == 38949 and digest(prior) == '879cff578dfa52a7dcf0c008cded5f42698bb3b2916570b9e4b5da0b31e10d17'
write_new('SOURCE_INDEX.json', {'kind': 'REVIEW_SOURCE_IDENTITIES', 'observed_utc': datetime.now(timezone.utc).isoformat(), 'sources': source_rows, 'attachment_git_blobs_match_fixed_ref': True, 'prior_review_zip': {'path': str(review_zip), 'bytes': len(prior), 'sha256': digest(prior)}, 'scope': 'Selected reviewer-local source bytes only; no observation of BML execution machine'})
decision = json.loads((root / 'DECISION.json').read_text(encoding='utf-8'))
assert decision['approved'] is False and decision['native_ready'] is False
assert sum(f['priority'] == 2 for f in decision['findings']) == 3
assert sum((600,1800,600,480,120)) == 3600
v2 = (root / 'OS_B_SEND_V2_INACTIVE_KO.md').read_text(encoding='utf-8')
assert '미채택' in v2 and '파일명: `null`' in v2
files = sorted(p for p in root.rglob('*') if p.is_file())
members = []
for p in files:
    assert not p.is_symlink()
    rel = p.relative_to(root).as_posix()
    if p.suffix == '.json':
        json.loads(p.read_text(encoding='utf-8'))
    b = p.read_bytes()
    members.append({'path': rel, 'bytes': len(b), 'sha256': digest(b)})
assert len({x['path'].casefold() for x in members}) == len(members)
write_new('PACKAGE_MANIFEST.json', {'kind': 'REVIEW_PACKAGE_MANIFEST', 'files': members})
archive = root / 'COMSOL_MICROSHORT_S1_OS_B_SCOPE_REVIEW_20261013.zip'
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for row in members:
        z.write(root / row['path'], row['path'])
    z.write(root / 'PACKAGE_MANIFEST.json', 'PACKAGE_MANIFEST.json')
with zipfile.ZipFile(archive, 'r') as z:
    assert z.testzip() is None
    expected = {x['path'] for x in members} | {'PACKAGE_MANIFEST.json'}
    assert len(z.infolist()) == len(expected) and set(z.namelist()) == expected
    for row in members:
        b = z.read(row['path'])
        assert len(b) == row['bytes'] and digest(b) == row['sha256']
    assert z.read('PACKAGE_MANIFEST.json') == (root / 'PACKAGE_MANIFEST.json').read_bytes()
for source, copy, expected in pairs:
    assert digest(source.read_bytes()) == expected
info = {'kind':'REVIEW_DELIVERY_RECEIPT','recipient':None,'archive':{'path':str(archive),'bytes':archive.stat().st_size,'sha256':digest(archive.read_bytes())},'payload_count':len(members),'entries':len(members)+1,'exact_set_size_sha_crc':True,'selected_originals_unchanged':True,'attachment_git_blobs_match_fixed_ref':True,'review_decision':decision['decision'],'native_ready':False,'implementation_or_execution_approved':False,'official_document_snapshot_bundle':False}
write_new('DELIVERY_RECEIPT.json', info)
print(json.dumps(info,ensure_ascii=False))
