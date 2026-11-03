from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent/'received_zip'
rows=[]
for line in (root/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
    expected,name=line.split('  ',1);name=name.removeprefix('./')
    actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
    rows.append((name,actual==expected))
assert all(ok for _,ok in rows)
assert len(rows)==198
print('received package: 198/198 PASS')
