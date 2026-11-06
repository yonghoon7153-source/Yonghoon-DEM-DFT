"""폴더의 SHA256SUMS 만들기 — 그 폴더 아래 모든 일반 파일 (이름이 SHA256SUMS 인 파일 뺌 · 링크 없음) 을 상대 경로 (POSIX) 바이트 차례로 `sha256sum` 꼴 줄로.
  python3 -I make_sums.py <폴더>   (그 폴더에서 sha256sum -c SHA256SUMS 로 대조)"""
import hashlib
import os
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
rows = []
for dp, dns, fns in os.walk(root):
    dns.sort()
    for nm in fns:
        p = Path(dp) / nm
        if nm == 'SHA256SUMS':
            continue
        if p.is_symlink() or not p.is_file():
            sys.exit(f'일반 파일이 아님: {p}')
        rows.append((p.relative_to(root).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest()))
rows.sort(key=lambda x: x[0].encode('utf-8'))
(root / 'SHA256SUMS').write_text(''.join(f'{h}  {r}\n' for r, h in rows), encoding='utf-8')
print(f'{root / "SHA256SUMS"} · 파일 {len(rows)}')
