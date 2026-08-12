"""corrected 5킷 재실행 + OLD(6f689062 이전) ↔ NEW segment 셀집합 차분.

목적 두 개:
  (a) `segment_cells` 재수정 후의 corrected CSV 를 확정 → CL-05/CL-08 hold 해제 근거
  (b) 그 수정이 집계에서 왜 안 보이는지를 **측정**한다 (추론 금지)
"""
import sys, os, json, importlib.util, subprocess, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import fibre_segment_raster as NEW                       # noqa: E402
from sr01_realbed_ab import seed_carbon_on_kit           # noqa: E402

# 수정 **이전** 판(70183ddd)을 git 에서 꺼내 같은 입력에 나란히 돌린다.
OLD_REV = os.environ.get('RASTER_OLD_REV', '70183ddd')
_tmp = tempfile.mkdtemp()
_old_path = os.path.join(_tmp, 'raster_old.py')
with open(_old_path, 'w', encoding='utf-8') as fh:
    fh.write(subprocess.check_output(
        ['git', 'show', f'{OLD_REV}:scripts/fibre_segment_raster.py'],
        cwd=os.path.dirname(HERE)).decode())
spec = importlib.util.spec_from_file_location('raster_old', _old_path)
OLD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OLD)

KITS = ['kit_ps_0_10', 'kit_ps_3_7', 'kit_ps_5_5', 'kit_ps_7_3', 'kit_ps_10_0']
VOX, GAP_TOL = 0.4, 2.0

out = []
for kit in KITS:
    S = seed_carbon_on_kit(kit, 288, 1.0, 0, max_fibres=0)
    pts, fid, step = S['pts'], S['fid'], S['step']
    old_all, new_all = [], []
    n_seg = 0
    n_seg_diff = 0
    for f in np.unique(fid):
        P = pts[fid == f]
        if len(P) < 2:
            continue
        d = np.linalg.norm(np.diff(P, axis=0), axis=1)
        brk = np.nonzero(d > GAP_TOL * step)[0] + 1
        runs = np.split(P, brk) if len(brk) else [P]
        for R in runs:
            if len(R) < 1:
                continue
            n_seg += 1
            a = OLD.polyline_cells(R, VOX)
            b = NEW.polyline_cells(R, VOX)
            old_all.append(a)
            new_all.append(b)
            if a.shape != b.shape or not np.array_equal(a, b):
                n_seg_diff += 1
    oc = np.unique(np.vstack(old_all), axis=0)
    nc = np.unique(np.vstack(new_all), axis=0)
    so = set(map(tuple, oc.tolist()))
    sn = set(map(tuple, nc.tolist()))
    rec = dict(kit=kit, step_um=float(step), vox_um=VOX,
               step_over_vox=float(step / VOX),
               n_polylines=n_seg, n_polylines_differing=n_seg_diff,
               old_cells=len(so), new_cells=len(sn),
               only_old=len(so - sn), only_new=len(sn - so))
    out.append(rec)
    print(json.dumps(rec, ensure_ascii=False), flush=True)

json.dump(out, open(os.path.join(os.path.dirname(HERE), 'docs', 'data',
                                'sr01_raster_fix_impact.json'), 'w'), ensure_ascii=False, indent=2)
print('done')
