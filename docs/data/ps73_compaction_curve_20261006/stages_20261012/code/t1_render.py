#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1 — 네 단계 3D 그림 (상별 색 · 웹앱 색) · 같은 카메라 · 같은 축척 · 투명 배경 · 글자 없음.

리포 함수 (읽기 전용 import): docs/data/ps73_damping_branch_20261007/snap_moments_20261008/render3d.py 의
  render (웹앱 three.js 0.160 카메라 · 조명 · Phong 재질 · 색 관리를 옮긴 z-버퍼 · 2 배 초표본) · webapp_camera · bbox · save_png.
색 = webapp/static/js/viewer3d.js 의 COL.AM_P · COL.AM_S · COL.SE (파일에서 읽는다 — 값을 여기 적지 않는다).
카메라 = 첫 단계 (Initial compression · 405,000) 의 상자 (0–50 × 0–50 µm × 0–판 높이 138.252 µm) 로 맞춘 웹앱 기본 시점 — 네 장 같다.
자르기 = 네 장 알파의 합집합 테두리 (render3d.run 과 같은 규칙) — 나란히 놓으면 자리가 맞는다.

  cd OUT && python3 -I -B code/t1_render.py [--px 1400] [--only initial]
"""
import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

import numpy as np  # noqa: E402

ODIR = C.OUT / 't1_geometry'


def webapp_phase_colours():
    """viewer3d.js `const COL = { AM_P: 0x…, AM_S: 0x…, SE: 0x… }` → {상: (hex 문자열, sRGB 0–1)}."""
    js = C.VIEWER_JS.read_text(encoding='utf-8')
    m = re.search(r'const COL = \{(.*?)\};', js, re.S)
    if not m:
        raise SystemExit('⛔ viewer3d.js 에 const COL 없음')
    out = {}
    for ph in ('AM_P', 'AM_S', 'SE'):
        mm = re.search(rf'\b{ph}:\s*0x([0-9a-fA-F]{{6}})', m.group(1))
        if not mm:
            raise SystemExit(f'⛔ COL.{ph} 없음')
        h = int(mm.group(1), 16)
        out[ph] = ('#' + mm.group(1).lower(), (((h >> 16) & 255) / 255.0, ((h >> 8) & 255) / 255.0, (h & 255) / 255.0))
    return out


def camera_bounds():
    """첫 단계 상자 (판 높이 포함) — µm."""
    z0 = C.plate_table()[C.STAGES[0][2]][1]
    return np.array([0.0, 0.0, 0.0]), np.array([50.0, 50.0, z0])


def stage_arrays(step, cols):
    atoms, A, info = C.read_atoms(step)
    xyz = np.stack([A['x'], A['y'], A['z']], 1) * C.SCALE
    r = A['r'] * C.SCALE
    rgb = np.array([cols[C.TYPE_MAP[int(t)]][1] for t in A['type']])
    return xyz, r, rgb, A


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--px', type=int, default=1400)
    ap.add_argument('--only', help='시험용 — 이 단계 하나만 (자르기 없이 · 결과 파일 이름에 _test)')
    a = ap.parse_args(argv)
    import render3d as R                                       # 리포 · 읽기 전용 import
    ODIR.mkdir(parents=True, exist_ok=True)
    cols = webapp_phase_colours()
    lo, hi = camera_bounds()
    pos, c, right, up, fwd = R.webapp_camera(lo, hi)
    stages = [s for s in C.STAGES if (a.only is None or s[0] == a.only)]
    full, meta = [], []
    for key, label, step in stages:
        t0 = time.time()
        xyz, r, rgb, A = stage_arrays(step, cols)
        rgba = R.render(xyz, r, rgb, a.px, 2, (lo, hi))
        full.append(rgba)
        meta.append({'key': key, 'label': label, 'step': step, 'n_particles': int(len(r)),
                     'n_by_phase': {C.TYPE_MAP[k]: int((A['type'] == k).sum()) for k in C.TYPE_MAP},
                     'plate_um': C.plate_table()[step][1], 'seconds': round(time.time() - t0, 1)})
        print(f'  {key:8s} step {step:>8d}  입자 {len(r)}  ({meta[-1]["seconds"]} s)', flush=True)
    if a.only:
        R.save_png(ODIR / f'ps73_geom3d_{a.only}_test.png', full[0])
        return 0
    boxes = [R.bbox(x) for x in full]
    ya, yb = min(b[0][0] for b in boxes), max(b[0][1] for b in boxes)
    xa, xb = min(b[1][0] for b in boxes), max(b[1][1] for b in boxes)
    crop = ((int(ya), int(yb)), (int(xa), int(xb)))
    imgs = [x[ya:yb, xa:xb] for x in full]
    files = []
    for m, img in zip(meta, imgs):
        fn = ODIR / f'ps73_geom3d_{m["step"]}_{m["key"]}.png'
        R.save_png(fn, img)
        files.append(fn.name)
        m['file'] = fn.name
        m['sha256'] = C.sha256(fn)
    # 미리보기 — 흰 바탕 · 왼쪽 → 오른쪽 = Initial compression · 50 MPa · 300 MPa · After relaxation · 글자 없음 (이름은 그림 밖 · REPORT)
    from PIL import Image
    tiles = []
    for img in imgs:
        im = Image.fromarray(np.clip(np.round(img * 255), 0, 255).astype(np.uint8), 'RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        tiles.append(bg.convert('RGB'))
    gap = 40
    canvas = Image.new('RGB', (sum(t.size[0] for t in tiles) + gap * (len(tiles) - 1), tiles[0].size[1]), (255, 255, 255))
    x = 0
    for t in tiles:
        canvas.paste(t, (x, 0))
        x += t.size[0] + gap
    canvas.save(ODIR / 'ps73_geom3d_4panel_preview.png')
    cam = {'tool': 't1_render', 'renderer': 'render3d.render (snap_moments_20261008) · ss 2', 'px': a.px,
           'camera_bounds_um': [lo.tolist(), hi.tolist()], 'camera_rule': 'render3d.webapp_camera — 상자 중심 + (1.2, 0.8, 1.2) × 최대 변 · '
           '원근 50° · THREE 좌표 (x, z, y)', 'camera_pos_three': pos.tolist(), 'camera_target_three': c.tolist(),
           'crop_rows_cols': crop, 'image_size_px': [int(yb - ya), int(xb - xa)],
           'um_per_px_at_target_depth': float(np.linalg.norm(pos - c) * np.tan(np.radians(25.0)) / (a.px * 2 / 2.0) * 2),
           'colours': {k: v[0] for k, v in cols.items()}, 'colour_source': 'webapp/static/js/viewer3d.js const COL',
           'opacity_note': '웹앱은 SE 를 opacity 0.85 (OPA.SE) 로 그리지만 render3d 는 불투명 z-버퍼 — 여기 SE 는 불투명',
           'stages': meta, 'preview': 'ps73_geom3d_4panel_preview.png'}
    C.write_json(C.OUT / 'logs' / 't1_camera.json', cam)
    print('→', ODIR, files)
    return 0


if __name__ == '__main__':
    sys.exit(main())
