"""Review archive bytes as data only. Never import or execute received code."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, stat, zipfile

ROOT = Path(__file__).resolve().parent
SRC = Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_R1_004_VALIDATION_RESULT_20261009.zip')
DEST = ROOT / 'received'
def sha(b): return hashlib.sha256(b).hexdigest()
def check_zip(raw, expected_count):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) == len({n.casefold() for n in names})
        assert sum(i.file_size for i in z.infolist()) < 50 * 1024 * 1024
        for i in z.infolist():
            p = PurePosixPath(i.filename)
            assert not p.is_absolute() and '..' not in p.parts and ':' not in i.filename and '\\' not in i.filename
            assert not i.is_dir() and not stat.S_ISLNK(i.external_attr >> 16)
        data = {n: z.read(n) for n in names}
        m = json.loads(data['PACKAGE_MANIFEST.json'])
        entries = {e['path']: e for e in m['files']}
        assert len(entries) == len(m['files']) == expected_count
        assert set(data) == set(entries) | {'PACKAGE_MANIFEST.json'}
        for n, e in entries.items():
            assert len(data[n]) == e['bytes'] and sha(data[n]) == e['sha256'], n
        assert z.testzip() is None
        return data

assert not DEST.exists(), 'No overwrite'
raw = SRC.read_bytes()
assert len(raw) == 796501 and sha(raw) == 'cb85fa123395caf9ea323b0c531144bf30754322ba9b0362f1bbac3e5bc8ff2c'
data = check_zip(raw, 50)
assert len(data['PACKAGE_MANIFEST.json']) == 8399
assert sha(data['PACKAGE_MANIFEST.json']) == '83a07d177e52bb5bd9069e4267d6a731c5a0bfa7e7b490d10d1c5b8945e8311c'
oldraw = data['reference/R1_003_ORIGINAL_RESULT.zip']
assert sha(oldraw) == '11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b'
old = check_zip(oldraw, 153)
previous = ROOT.parent / 'microshort_s1o_r1_003_stop_review_20261008/received'
assert all((previous / n).read_bytes() == b for n, b in old.items())
for n, b in data.items():
    p = DEST / n
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f: f.write(b)
result = dict(kind='INDEPENDENT_ARCHIVE_BYTE_REVIEW', archive=dict(path=str(SRC), bytes=len(raw), sha256=sha(raw)),
              payload_count=50, entries=51, path_set_size_sha_crc_pass=True,
              embedded_R1_003_payload_count=153, embedded_R1_003_byte_equal_previous_review=True,
              received_code_executions=0, test_reruns=0, native_executions=0)
(ROOT / 'INPUT_CHECK.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
