"""Offline, read-only integrity check. Does not fetch, repair or run simulations."""
from pathlib import Path
import hashlib, json
R=Path(__file__).resolve().parent
def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def main():
    source=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
    for row in source:
        data=(R/'source'/row['path']).read_bytes()
        assert blob(data)==row['sha'], ('git_blob', row['path'])
        assert hashlib.sha256(data).hexdigest()==row['sha256'], ('source_sha256',row['path'])
    manifest=json.loads((R/'bundle_manifest.json').read_text(encoding='utf8'))
    for row in manifest['files']:
        data=(R/row['path']).read_bytes()
        assert len(data)==row['bytes'], ('size',row['path'])
        assert hashlib.sha256(data).hexdigest()==row['sha256'], ('sha256',row['path'])
    print('PASS: pinned Git blobs',len(source),'and bundle files',len(manifest['files']))
    print('Pin:',manifest['review_pin'])
    print('Manifest integrity is not a proof of scientific validity.')
if __name__=='__main__':
    main()
