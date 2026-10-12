#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""최종 판 (aligned_ckpt) 미리보기 — ① SE 응력 3D 를 **벽 SE 없이** (회색 없앰) ② 3D · SE 응력 네 장 묶음에 porosity 글자.

1저자 10-12: *"저 회색 없애줘"* · *"이건 porosity로 해줘야지"* (3D 네 단계 이름 = porosity) · *"log 말고 선형으로 범례"* ·
*"300 이상인거 다 같은색으로 한것처럼 잘 차이나는 mpa로"* → **선형 0–200 MPa** (200 이상 = 맨 위 색 · 네 단계 공통) —
벽 아닌 SE 분포: 296 MPa · 이완 단계 p90 ≈ 195–197 MPa (200 넘는 SE 9.3–9.7 %) · 47 MPa · 처음 p90 ≈ 47–49 MPa.
① 벽 SE (바닥 · 판에 닿은 SE) 는 판 · 바닥 힘이 덤프에 없어 σ_VM 이 불완전하다 → 칠하면 윗면이 거짓으로 낮게 (파랗게) 보이고 회색으로 두면 회색이 보인다.
   여기서는 **그리지 않는다** (그 아래 층이 보인다) · 색 범위 · 카메라 · 자르기 = aligned_figs.py 와 같다 (재계산 없음 — SE 별 CSV.gz 를 읽는다).
② 글자 = 그림 **밖** 아래 (보고자료 원칙 — 범례 · 주석은 그림 밖) · porosity = exact union (`ps73_ckpt_porosity.json`).

  cd OUT && python3 -I -B code/aligned_previews.py [--out aligned_ckpt]
"""
import argparse
import csv
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

import numpy as np  # noqa: E402

KEYS = [(400000, 'initial'), (1650000, 'p47'), (3100000, 'p296'), (3220000, 'relaxed')]
FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'


def read_se(path):
    rows = []
    with gzip.open(path, 'rt', encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            rows.append((float(r['x_um']), float(r['y_um']), float(r['z_um']), float(r['r_um']), float(r['vm_MPa']), int(r['wall_flag'])))
    return np.array(rows)


def white(img_rgba):
    from PIL import Image
    im = Image.fromarray(np.clip(np.round(img_rgba * 255), 0, 255).astype(np.uint8), 'RGBA') if not hasattr(img_rgba, 'mode') else img_rgba.convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return bg.convert('RGB')


def strip(tiles, labels, colorbar=None):
    from PIL import Image, ImageDraw, ImageFont
    h = tiles[0].size[1]
    fs = max(20, min(h // 18, int(min(t.size[0] for t in tiles) / 9)))
    font = ImageFont.truetype(FONT, fs)
    gap, band = 40, int(fs * 1.9)
    cbw = 0
    if colorbar is not None:
        sc = h * 0.8 / colorbar.size[1]
        colorbar = colorbar.resize((max(1, int(colorbar.size[0] * sc)), int(colorbar.size[1] * sc)))
        cbw = colorbar.size[0] + gap
    W = sum(t.size[0] for t in tiles) + gap * (len(tiles) - 1) + cbw
    canvas = Image.new('RGB', (W, h + band), (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    x = 0
    for t, lab in zip(tiles, labels):
        canvas.paste(t, (x, 0))
        tw = d.textlength(lab, font=font)
        d.text((x + (t.size[0] - tw) / 2, h + int(fs * 0.35)), lab, fill=(64, 64, 64), font=font)
        x += t.size[0] + gap
    if colorbar is not None:
        canvas.paste(white(colorbar), (x, int(h * 0.1)))
    return canvas


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(C.OUT / 'aligned_ckpt'))
    ap.add_argument('--vmax', type=float, default=200.0, help='선형 색 위쪽 (MPa) — 이 값 이상은 맨 위 색 · 아래쪽 = 0')
    a = ap.parse_args(argv)
    out = Path(a.out)
    src = C.OUT / 'aligned_ckpt'
    import render3d as R
    from PIL import Image
    cam = json.loads((src / 'logs' / 't1_camera.json').read_text(encoding='utf-8'))
    rec = json.loads((src / 't3_vm_se' / 'ps73_se_vm_aligned.json').read_text(encoding='utf-8'))
    por = {r['step']: r['eps_union_pct'] for r in json.loads((src / 'ps73_ckpt_porosity.json').read_text(encoding='utf-8'))['rows']}
    lo, hi = 0.0, float(a.vmax)
    tag = f'linear_0_{int(round(hi))}'
    b = cam['camera_bounds_um']
    (ya, yb), (xa, xb) = cam['crop_rows_cols']
    (out / 't3_vm_se').mkdir(parents=True, exist_ok=True)
    (out / 't1_geometry').mkdir(parents=True, exist_ok=True)
    labels = [f'Porosity {por[s]:.1f} %' for s, _ in KEYS]
    se_tiles, info = [], {}
    for step, key in KEYS:
        A = read_se(src / 't3_vm_se' / f'ps73_se_vm_{step}.csv.gz')
        keep = A[:, 5] == 0
        xyz, r, vm = A[keep, 0:3], A[keep, 3], A[keep, 4]
        rgb = R.colours(vm, np.zeros(vm.size, dtype=bool), lo, hi, grey_wall=False, scale='linear')
        rgba = R.render(xyz, r, rgb, int(cam['px']), 2, (np.array(b[0]), np.array(b[1])))
        img = rgba[ya:yb, xa:xb]
        fn = out / 't3_vm_se' / f'ps73_se_vm3d_{step}_{key}_nowall_{tag}.png'
        R.save_png(fn, img)
        se_tiles.append(white(img))
        info[str(step)] = {'n_drawn': int(keep.sum()), 'n_wall_not_drawn': int((~keep).sum()), 'file': fn.name,
                           'pct_at_or_above_vmax': float(100.0 * (vm >= hi).mean())}
        print(f'  SE 3D {step:>8d} 벽 빼고 {int(keep.sum())} 개 그림 (벽 {int((~keep).sum())} 안 그림)', flush=True)
    R.colorbar_png(out / 't3_vm_se' / f'ps73_se_vm3d_colorbar_{tag}.png', lo, hi, 'linear')
    R.colorbar_png(out / 't3_vm_se' / f'ps73_se_vm3d_colorbar_{tag}_bare.png', lo, hi, 'linear', labels=False)
    cb = Image.open(out / 't3_vm_se' / f'ps73_se_vm3d_colorbar_{tag}.png')
    strip(se_tiles, labels, cb).save(out / 't3_vm_se' / f'ps73_se_vm3d_4panel_nowall_{tag}_preview.png')
    geo = [white(Image.open(src / 't1_geometry' / f'ps73_geom3d_{s}_{k}.png')) for s, k in KEYS]
    strip(geo, labels).save(out / 't1_geometry' / 'ps73_geom3d_4panel_porosity_preview.png')
    C.write_json(out / 't3_vm_se' / f'ps73_se_vm3d_nowall_{tag}.json',
                 {'tool': 'aligned_previews', 'rule': 'wall SE (z−r<0 or z+r>plate) not drawn — their LW σ_VM lacks wall forces',
                  'scale': 'linear', 'vmin_MPa': lo, 'vmax_MPa': hi, 'above_vmax': 'top colour (jet8 t = 1)', 'labels': labels, 'porosity_source': 'ps73_ckpt_porosity.json eps_union_pct (exact union)',
                  'per_stage': info})
    print('→', out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
