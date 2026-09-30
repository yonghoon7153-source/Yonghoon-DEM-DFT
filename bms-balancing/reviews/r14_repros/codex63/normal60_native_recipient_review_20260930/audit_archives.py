"""Reviewer-owned archive byte validation. Never executes received contents."""
import hashlib, json, stat, zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
SOURCES = [Path('C:/Users/Administrator/Downloads') / n for n in (
    'COMSOL63_NORMAL60_NATIVE_RESULT_20260930.zip',
    'NORMAL60_NATIVE_DELIVERY_SUPPLEMENT_20260930.zip')]

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

records = []
for source, folder in zip(SOURCES, ['received', 'supplement']):
    before = {'bytes': source.stat().st_size, 'sha256': sha(source)}
    destination = ROOT / folder
    assert not destination.exists(), 'Never overwrite an existing extraction'
    with zipfile.ZipFile(source) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        assert len(names) == len(set(names)) == len({n.casefold() for n in names})
        for i in infos:
            p = PurePosixPath(i.filename)
            assert not p.is_absolute() and not any(s in ('', '.', '..') for s in i.filename.split('/'))
            assert '\\' not in i.filename and ':' not in i.filename and not i.is_dir()
            assert not stat.S_ISLNK(i.external_attr >> 16)
        raw = z.read('MANIFEST.json')
        m = json.loads(raw)
        entries = m['files']
        assert len({e['file'] for e in entries}) == len(entries)
        assert set(names) == {e['file'] for e in entries} | {'MANIFEST.json'}
        identities = {}
        for e in entries:
            info = z.getinfo(e['file'])
            assert info.file_size == e['bytes']
            h = hashlib.sha256()
            # Extract only after path validation; reading to EOF validates ZIP CRC.
            target = destination / e['file']
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as stream, target.open('xb') as out:
                while chunk := stream.read(1024*1024):
                    h.update(chunk); out.write(chunk)
            assert h.hexdigest() == e['sha256'], e['file']
            identities[e['file']] = {'bytes': info.file_size, 'sha256': h.hexdigest()}
        (destination / 'MANIFEST.json').write_bytes(raw)
        records.append({'file': str(source), **before, 'payload': len(entries),
            'entries': len(infos), 'manifest_bytes': len(raw),
            'manifest_sha256': hashlib.sha256(raw).hexdigest(),
            'exact_set_size_sha_crc_path_case_link': True,
            'members': identities})
    assert before == {'bytes': source.stat().st_size, 'sha256': sha(source)}
(ROOT/'ARCHIVE_AUDIT.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k != 'members'} for r in records], indent=2))
