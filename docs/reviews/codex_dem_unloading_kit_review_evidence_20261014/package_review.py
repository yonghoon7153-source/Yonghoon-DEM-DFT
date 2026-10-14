"""Package review deliverables without mutating source or existing evidence."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile
from reproduce import verify_sources

ROOT = Path(__file__).resolve().parent
DEST = ROOT.parent / 'codex_dem_unloading_kit_review_2783061ea_20261014.zip'

def main():
    source_checks = verify_sources()
    latest = {}
    for key, name in [('reader_cases', 'reader_adversarial.json'), ('reader_continuation', 'reader_continuation.json')]:
        obj = json.loads((ROOT / 'evidence' / name).read_text(encoding='utf-8'))
        latest[key] = Path(obj['fixture_root']).name
    files = []
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if '__pycache__' in rel.parts or rel.parts[0] == 'tmp_baseline' or rel.name in ('PACKAGE_MANIFEST.json',):
            continue
        if len(rel.parts)>2 and rel.parts[0]=='evidence' and rel.parts[1].startswith('history_runner_'):
            continue
        if len(rel.parts)>2 and rel.parts[0]=='evidence' and rel.parts[1] in latest and rel.parts[2] != latest[rel.parts[1]]:
            continue
        files.append(p)
    entries = [{'path':p.relative_to(ROOT).as_posix(), 'bytes':p.stat().st_size,
                'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    manifest = {'schema':'review_package/v1', 'pin':'2783061ead9f192ab742a2f0b14b0182a98a4966',
                'verdict':'HOLD', 'source_checks':source_checks, 'files':entries,
                'exclusions':['temporary baseline/mocked-shell folders', 'superseded duplicate synthetic runs', '__pycache__'],
                'note':'Native DEM/SLURM not executed. Shell mocks environment-blocked; see report.'}
    mp = ROOT / 'PACKAGE_MANIFEST.json'
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    with zipfile.ZipFile(DEST, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files+[mp]:
            z.write(p, p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(DEST) as z:
        assert z.testzip() is None
        names=z.namelist()
        assert len(names)==len(set(n.casefold() for n in names))
        assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and ':' not in n and '\\' not in n for n in names)
        for entry in entries:
            assert hashlib.sha256(z.read(entry['path'])).hexdigest()==entry['sha256']
    receipt = {'zip':str(DEST), 'bytes':DEST.stat().st_size, 'sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
               'files_in_zip':len(files)+1, 'crc_and_entry_hashes':'PASS', 'source_unchanged':True}
    DEST.with_suffix('.receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))

if __name__=='__main__':
    main()
