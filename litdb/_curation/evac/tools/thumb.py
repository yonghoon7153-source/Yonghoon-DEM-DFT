#!/usr/bin/env python3
"""thumb.py — 모음 그림을 메인 세션이 훑어볼 작은 그림으로 줄인다 (1저자에게는 원본을 보낸다).
python3 -I thumb.py <slug>   → litcards/<slug>_sheet*_thumb.png (너비 1100)"""
import sys
from pathlib import Path
from PIL import Image
SCR = Path(__file__).resolve().parents[1]
for p in sorted((SCR / "litcards").glob(f"{sys.argv[1]}_sheet*.png")):
    if p.stem.endswith("_thumb"):
        continue
    im = Image.open(p)
    w = 1100
    im = im.convert("RGB").resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
    out = p.with_name(p.stem + "_thumb.png")
    im.save(out, optimize=True)
    print(out, im.size)
