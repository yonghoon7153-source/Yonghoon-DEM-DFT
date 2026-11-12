#!/usr/bin/env python3
"""make_sheet.py — 한 논문의 크롭 (그림 · 표 · 식 · 글 조각) 을 한 장에 작게 모은 검토용 그림.

쓰임
  python3 -I make_sheet.py --figdir <정본 트리>/litdb/figures/<slug> --out <scratchpad>/litcards/<slug>_sheet.png

- 순서 = figures.json 의 figures 목록 순서 (없으면 파일 이름순) · 목록에 없는 png 는 끝에 붙인다.
- 칸마다 이름표 = 파일 이름 · 쪽 · 원래 크기 · 표지 (manual_crop / recrop 이 있으면 M / R).
- 크롭이 많으면 여러 장으로 나눈다 (<out>_1.png · _2.png …) — 한 장에 --per 개까지.
- 정본 트리에는 아무것도 쓰지 않는다 (읽기만).
"""
import argparse
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = 400_000_000


def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"):
        if Path(p).is_file():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def collect(figdir: Path):
    meta = {}
    order = []
    fj = figdir / "figures.json"
    if fj.is_file():
        try:
            j = json.loads(fj.read_text(encoding="utf-8"))
            figs = j.get("figures", []) if isinstance(j, dict) else j
            for e in figs:
                f = e.get("file")
                if f and f not in meta:
                    meta[f] = e
                    order.append(f)
        except Exception as ex:                       # 읽히지 않으면 파일 이름순으로
            print(f"⚠ figures.json 을 못 읽음: {ex}", file=sys.stderr)
    on_disk = sorted(p.name for p in figdir.glob("*.png") if not p.name.startswith("_"))
    listed_missing = [f for f in order if f not in on_disk]
    order = [f for f in order if f in on_disk] + [f for f in on_disk if f not in meta]
    unlisted = [f for f in on_disk if f not in meta]
    return order, meta, listed_missing, unlisted


def tag(e):
    t = []
    if e.get("manual_crop"):
        t.append("M")
    if e.get("recrop"):
        t.append("R")
    return ("[" + "".join(t) + "] ") if t else ""


def sheet(figdir, files, meta, out, cols, cell, title):
    lab_h = 46
    pad = 10
    head_h = 54
    rows = math.ceil(len(files) / cols)
    W = pad + cols * (cell + pad)
    H = head_h + rows * (cell + lab_h + pad) + pad
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.text((pad, 12), title, fill=(0, 0, 0), font=font(24))
    f_lab = font(13)
    for i, name in enumerate(files):
        r, c = divmod(i, cols)
        x0 = pad + c * (cell + pad)
        y0 = head_h + r * (cell + lab_h + pad)
        d.rectangle([x0, y0, x0 + cell, y0 + cell], outline=(200, 200, 200))
        try:
            with Image.open(figdir / name) as src:
                w, h = src.size
                th = src.convert("RGB")
                th.thumbnail((cell - 4, cell - 4), Image.LANCZOS)
                im.paste(th, (x0 + (cell - th.width) // 2, y0 + (cell - th.height) // 2))
        except Exception as ex:
            w = h = 0
            d.text((x0 + 6, y0 + 6), f"못 엶: {ex}"[:60], fill=(200, 0, 0), font=f_lab)
        e = meta.get(name, {})
        pg = e.get("page")
        line1 = name if len(name) <= 52 else name[:49] + "..."
        line2 = f"{tag(e)}p{pg if pg is not None else '?'} · {w}x{h}" + ("" if name in meta else " · (not in figures.json)")
        d.text((x0 + 2, y0 + cell + 4), line1, fill=(0, 0, 0), font=f_lab)
        d.text((x0 + 2, y0 + cell + 22), line2, fill=(90, 90, 90), font=f_lab)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, optimize=True)
    return W, H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--figdir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--cell", type=int, default=400)
    ap.add_argument("--per", type=int, default=48, help="한 장에 넣는 크롭 수")
    a = ap.parse_args()
    figdir = Path(a.figdir).resolve()
    out = Path(a.out).resolve()
    if not figdir.is_dir():
        sys.exit(f"⛔ 폴더 없음: {figdir}")
    files, meta, listed_missing, unlisted = collect(figdir)
    if not files:
        sys.exit(f"⛔ png 없음: {figdir}")
    chunks = [files[i:i + a.per] for i in range(0, len(files), a.per)]
    outs = []
    for k, ch in enumerate(chunks, 1):
        o = out if len(chunks) == 1 else out.with_name(f"{out.stem}_{k}{out.suffix}")
        title = f"{figdir.name}  ·  {len(files)} crops" + (f"  ·  sheet {k}/{len(chunks)}" if len(chunks) > 1 else "")
        W, H = sheet(figdir, ch, meta, o, a.cols, a.cell, title)
        outs.append((o, W, H, len(ch)))
    for o, W, H, n in outs:
        print(f"SHEET {o}  {W}x{H}  {n} crops")
    print(f"TOTAL {len(files)} crops · figures.json 에 있는데 파일 없음 {len(listed_missing)} · 파일은 있는데 figures.json 에 없음 {len(unlisted)}")
    for f in listed_missing:
        print(f"  MISSING_FILE {f}")
    for f in unlisted:
        print(f"  UNLISTED {f}")


if __name__ == "__main__":
    main()
