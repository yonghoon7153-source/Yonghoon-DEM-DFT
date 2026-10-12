#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ps73 SE σ_VM 3D — AM 접촉 상대별 네 장 (상자그림 · 중앙값 대신 · 1저자 10-13).

1저자 10-13: *"저 중앙값 그림이 필요한게 아니고 ~사이에 응력값이던 3d geometry로 해서 각각의 차이를 보고싶은거야"*
→ 같은 단계 · 같은 카메라 · 같은 선형 색 범위 (기본 0–150 MPa = 1저자 *"150이 제일 좋은듯"* · 상한 이상 = 맨 위 색) 에서 접촉 상대 분류마다 그 SE 만 그린다:
   None (AM 접촉 없음 = SE_only) · PC (PC 만 · PC_only) · SC (SC 만 · SC_only) · PC + SC (둘 다 · PC_and_SC) — 분류 = t3_vm_se 의 `class` 열 (상자그림과 같은 분류).
벽 SE (z−r<0 · z+r>판) 는 그리지 않는다 (판 · 바닥 힘이 덤프에 없어 σ_VM 불완전 — aligned_previews.py 와 같은 규칙).  AM 은 그리지 않는다.
입력 (읽기만) = aligned_ckpt/t3_vm_se/ps73_se_vm_<step>.csv.gz · aligned_ckpt/logs/t1_camera.json (재계산 없음).

  cd OUT && python3 -I -B code/aligned_class3d.py [--step 3220000] [--vmax 150] [--out aligned_ckpt]      (처음 보인 미리보기 = --vmax 200)
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import aligned_previews as AP  # noqa: E402

import numpy as np  # noqa: E402

STAGE_KEY = {400000: 'initial', 1650000: 'p47', 3100000: 'p296', 3220000: 'relaxed'}
#: (class 열 값, 파일 꼬리, 그림 글자) — 글자 = 상자그림 x 축 (`AM contact partner`) 과 같게
CLASSES = [('SE_only', 'none', 'None'), ('PC_only', 'pc', 'PC'), ('SC_only', 'sc', 'SC'), ('PC_and_SC', 'pcsc', 'PC + SC')]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--step', type=int, default=3220000, choices=sorted(STAGE_KEY))
    ap.add_argument('--vmax', type=float, default=150.0, help='선형 색 위쪽 (MPa) — 이 값 이상은 맨 위 색 · 아래쪽 = 0')
    ap.add_argument('--out', default=str(C.OUT / 'aligned_ckpt'))
    a = ap.parse_args(argv)
    import render3d as R
    from PIL import Image
    src = C.OUT / 'aligned_ckpt'
    out = Path(a.out) / 't3_vm_se'
    out.mkdir(parents=True, exist_ok=True)
    cam = json.loads((src / 'logs' / 't1_camera.json').read_text(encoding='utf-8'))
    b = cam['camera_bounds_um']
    (ya, yb), (xa, xb) = cam['crop_rows_cols']
    lo, hi = 0.0, float(a.vmax)
    tag = f'linear_0_{int(round(hi))}'
    key = STAGE_KEY[a.step]
    import csv
    import gzip
    rows = []
    with gzip.open(src / 't3_vm_se' / f'ps73_se_vm_{a.step}.csv.gz', 'rt', encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    wall = np.array([r['wall_flag'] != '0' for r in rows])
    cls = np.array([r['class'] for r in rows])
    xyz = np.array([[float(r['x_um']), float(r['y_um']), float(r['z_um'])] for r in rows])
    rad = np.array([float(r['r_um']) for r in rows])
    vm = np.array([float(r['vm_MPa']) for r in rows])
    known = {c for c, _, _ in CLASSES}
    if set(cls[~wall]) - known:
        raise SystemExit(f'⛔ 모르는 분류 {sorted(set(cls[~wall]) - known)}')
    tiles, labels, info = [], [], {}
    for c, tail, lab in CLASSES:
        keep = (~wall) & (cls == c)
        v = vm[keep]
        rgb = R.colours(v, np.zeros(v.size, dtype=bool), lo, hi, grey_wall=False, scale='linear')
        rgba = R.render(xyz[keep], rad[keep], rgb, int(cam['px']), 2, (np.array(b[0]), np.array(b[1])))
        img = rgba[ya:yb, xa:xb]
        fn = out / f'ps73_se_vm3d_{a.step}_{key}_class_{tail}_nowall_{tag}.png'
        R.save_png(fn, img)
        tiles.append(AP.white(img))
        q = np.percentile(v, [25, 50, 75, 90]) if v.size else [float('nan')] * 4
        labels.append(f'{lab} (n = {int(keep.sum())})')
        info[c] = {'label': lab, 'n_drawn': int(keep.sum()), 'file': fn.name,
                   'p25_p50_p75_p90_MPa': [round(float(x), 2) for x in q],
                   'pct_at_or_above_vmax': round(float(100.0 * (v >= hi).mean()), 2) if v.size else None}
        print(f'  {lab:8s} n {int(keep.sum()):6d}  p25/p50/p75/p90 = ' + ' / '.join(f'{x:.1f}' for x in q)
              + f' MPa  ≥{hi:g}: {info[c]["pct_at_or_above_vmax"]} %', flush=True)
    cbp = out / f'ps73_se_vm3d_colorbar_{tag}.png'
    if not cbp.exists():
        R.colorbar_png(cbp, lo, hi, 'linear')
        R.colorbar_png(out / f'ps73_se_vm3d_colorbar_{tag}_bare.png', lo, hi, 'linear', labels=False)
    AP.strip(tiles, labels, Image.open(cbp)).save(out / f'ps73_se_vm3d_{a.step}_{key}_class_4panel_nowall_{tag}_preview.png')
    C.write_json(out / f'ps73_se_vm3d_{a.step}_{key}_class_nowall_{tag}.json',
                 {'tool': 'aligned_class3d', 'step': a.step, 'stage_key': key,
                  'rule': 'per AM-contact class (t3_vm_se class column): only that class of non-wall SE drawn · wall SE (z−r<0 or z+r>plate) not drawn · AM not drawn',
                  'scale': 'linear', 'vmin_MPa': lo, 'vmax_MPa': hi, 'above_vmax': 'top colour (jet8 t = 1)',
                  'camera': 'aligned_ckpt/logs/t1_camera.json (same as the 4-stage figures)', 'per_class': info})
    print('→', out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
