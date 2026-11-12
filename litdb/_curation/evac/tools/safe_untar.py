#!/usr/bin/env python3
"""safe_untar.py — tgz 를 빈 새 폴더에 푼다 (보통 파일만 · 경로 이탈 · 링크 · 장치 파일은 건너뜀).
python3 -I safe_untar.py <tgz> <빈 폴더>"""
import sys
import tarfile
from pathlib import Path, PurePosixPath

src, dest = Path(sys.argv[1]), Path(sys.argv[2])
if dest.exists() and any(dest.iterdir()):
    sys.exit(f"⛔ 빈 폴더가 아니다: {dest}")
dest.mkdir(parents=True, exist_ok=True)
n = skipped = total = 0
with tarfile.open(src, "r:*") as t:
    for m in t:
        p = PurePosixPath(m.name)
        if not m.isreg() or p.is_absolute() or ".." in p.parts or m.size > 400 * 1024 * 1024:
            if not m.isdir():
                skipped += 1
                print("  건너뜀:", m.name[:100], "(보통 파일 아님 / 경로 / 크기)")
            continue
        out = dest.joinpath(*p.parts)
        out.parent.mkdir(parents=True, exist_ok=True)
        f = t.extractfile(m)
        with open(out, "wb") as o:
            while True:
                b = f.read(1 << 20)
                if not b:
                    break
                o.write(b)
        n += 1
        total += m.size
print(f"{src.name}: {n} 파일 · {total / 1e6:.1f} MB · 건너뜀 {skipped} → {dest}")
