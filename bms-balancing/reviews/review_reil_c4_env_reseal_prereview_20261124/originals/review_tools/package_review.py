"""Reviewer-only file/hash/ZIP processing. Does not load submitted programs."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile, zlib

R = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def ident(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": digest(data)}

def write_json(path, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(data)
    assert path.read_bytes() == data
    return ident(path)

before = json.loads((R / 'SELECTED_LOCAL_SOURCES_BEFORE_PACKAGE.json').read_text(encoding='utf-8'))
assert all(ident(Path(x['path'])) == x for x in before['files'])
for record_file in ['INTAKE_IDENTITIES.json', 'SOURCE_BATCH_IDENTITIES.json', 'BASIS_IDENTITIES.json']:
    rows = json.loads((R / record_file).read_text(encoding='utf-8'))
    if isinstance(rows, dict):
        rows = rows['files']
    for row in rows:
        p = Path(row['path'])
        if not p.is_absolute():
            p = R / 'source' / p
        data = p.read_bytes()
        assert len(data) == row['bytes'] and digest(data) == row['sha256'], str(p)

refs = {
    "kind": "OFFICIAL_SOURCE_REFERENCES_FOR_STATIC_REVIEW",
    "scope": "Read-only official documentation and pip 24.0 source; not a measurement of the remote installation",
    "items": [
        {"url": "https://github.com/pypa/pip/blob/24.0/src/pip/_internal/cli/req_command.py", "capture": "official/pip24_0.capture.txt", "supports": "options.cert is assigned to session.verify"},
        {"url": "https://github.com/pypa/pip/blob/24.0/src/pip/_internal/network/session.py", "capture": "official/pip24_1.capture.txt", "supports": "PipSession.request defaults timeout and proxies but does not supply a per-request verify override"},
        {"url": "https://github.com/pypa/pip/blob/24.0/src/pip/_vendor/requests/sessions.py", "capture": "official/pip24_2.capture.txt", "supports": "REQUESTS_CA_BUNDLE/CURL_CA_BUNDLE merge precedence"},
        {"url": "https://github.com/pypa/pip/blob/24.0/src/pip/_internal/network/download.py", "capture": "official/pip24_3.capture.txt", "supports": "Downloading formatting uses link.netloc, not the final response host"},
        {"url": "https://pip.pypa.io/en/stable/topics/https-certificates/", "supports": "CA configuration options; version-specific reasoning uses the 24.0 sources above"},
        {"url": "https://pip.pypa.io/en/stable/topics/configuration/", "supports": "PIP_CONFIG_FILE=os.devnull disables configuration files"},
        {"url": "https://docs.python.org/3.11/library/site.html", "supports": "Executable lines in .pth and sitecustomize may affect startup"}
    ]
}
write_json(R / 'OFFICIAL_REFERENCES.json', refs)

root_files = [
    'README_KO.txt', 'REVIEW_KO.txt', 'CODEX_REPLY_KO.txt', 'REVIEW_DECISION.json',
    'INTAKE_IDENTITIES.json', 'SOURCE_BATCH_IDENTITIES.json', 'BASIS_IDENTITIES.json',
    'STATIC_EVIDENCE_AUDIT.json', 'SELFTEST_STATIC_DIFF.txt',
    'SELECTED_LOCAL_SOURCES_BEFORE_PACKAGE.json', 'OFFICIAL_REFERENCES.json'
]
payload = {name: (R / name).read_bytes() for name in root_files}
for dirname in ['source', 'basis', 'capture', 'official']:
    for path in sorted((R / dirname).rglob('*')):
        if path.is_file():
            assert not path.is_symlink()
            payload[path.relative_to(R).as_posix()] = path.read_bytes()
for name in ['intake.py', 'decode_batch.py', 'decode_basis.py', 'audit_metadata.py', 'package_review.py']:
    payload['review_tools/' + name] = (R / name).read_bytes()

assert len(payload) == len({name.casefold() for name in payload})
for name in payload:
    p = PurePosixPath(name)
    assert not p.is_absolute() and all(x not in ('', '.', '..') and ':' not in x and '\\' not in x for x in p.parts)

manifest = {
    'kind': 'STATIC_PREREVIEW_PACKAGE_MANIFEST',
    'commit': '781f357200259f24ac04a95da8aa13dfd2761524',
    'payload_count': len(payload),
    'self_excluded': True,
    'files': [{'path': name, 'bytes': len(data), 'sha256': digest(data)} for name, data in sorted(payload.items())]
}
manifest_ident = write_json(R / 'PACKAGE_MANIFEST.json', manifest)
members = dict(payload)
members['PACKAGE_MANIFEST.json'] = (R / 'PACKAGE_MANIFEST.json').read_bytes()
archive = R / 'REIL_C4_ENV_RESEAL_PREREVIEW_20261124.zip'
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, data in sorted(members.items()):
        z.writestr(name, data)
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist()) == set(members)
    assert len(z.namelist()) == len(members)
    for info in z.infolist():
        data = z.read(info)
        expected = members[info.filename]
        assert data == expected and info.file_size == len(expected)
        assert digest(data) == digest(expected)
        assert info.CRC == zlib.crc32(data) & 0xffffffff
        assert (info.external_attr >> 16) & 0o170000 != 0o120000

after = [ident(Path(x['path'])) for x in before['files']]
assert after == before['files']
post_ident = write_json(R / 'SELECTED_LOCAL_SOURCES_POST_PACKAGE.json', {
    'kind': 'REVIEW_POST_PACKAGE_SELECTED_SOURCE_IDENTITIES',
    'files': after,
    'matches_before_package': True,
    'scope': 'Four selected local prior-review source files only; the before record was made after review reads, not at turn start. No remote all-filesystem audit.'
})
archive_ident = ident(archive)
receipt_ident = write_json(R / 'DELIVERY_RECEIPT.json', {
    'kind': 'REIL_C4_ENV_RESEAL_PREREVIEW_DELIVERY_RECEIPT',
    'recipient': None,
    'archive': archive_ident,
    'manifest': manifest_ident,
    'payload_count': len(payload),
    'entries': len(members),
    'verification': 'Exact member set, safe case-unique paths, decompressed bytes/size/SHA256, non-link metadata and independently recomputed CRC32 matched.',
    'source_files_at_fixed_ref': sum(p.is_file() for p in (R / 'source').rglob('*')),
    'selected_local_originals_preserved': len(after),
    'decision': 'REVISION_REQUIRED_BEFORE_RESEAL_EXECUTION_APPROVAL',
    'required_document_corrections': ['ENV18-N1', 'ENV18-N2'],
    'execution_prerequisite': 'Freeze and statically review runner and outer harness before execution approval',
    'supplied_program_execution': 0,
    'tests': 0, 'installations': 0, 'venv_creation': 0, 'pip': 0, 'emit_check': 0, 'COMSOL': 0,
    'reseal_execution_authorized_by_review': False,
    'numeric_review_budget_seconds': None,
    'whole_review_elapsed_claim': None,
    'boundary': 'After new review ZIP readback and selected original rehash; before this receipt write/readback and actual tool return. Source submission was not repackaged or modified.'
})
print(json.dumps({
    'kind': 'REIL_C4_ENV_RESEAL_PREREVIEW_PACKAGE_RETURN',
    'archive': archive_ident, 'manifest': manifest_ident,
    'receipt': receipt_ident, 'post_package': post_ident,
    'payload_count': len(payload), 'entries': len(members),
    'decision': 'REVISION_REQUIRED_BEFORE_RESEAL_EXECUTION_APPROVAL',
    'supplied_program_execution': 0, 'tests': 0, 'COMSOL': 0,
    'whole_review_elapsed_claim': None,
    'boundary': 'After review archive and receipt write/readback; before actual tool return and subsequent serialization of that result.'
}, ensure_ascii=False, indent=2))
