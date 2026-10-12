#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""응력과 같은 step 네 단계 — 3D (상별 색) + SE 만 von Mises (Love–Weber) · 네 단계 같은 색 범위.

1저자 10-12: *"3D porosity를 저때로 맞추면 좋을듯"* · *"AM 에서 했던것처럼 1 step 정도만 하고 contact 뽑으면"* · *"SE 응력 = am 은 없고 SE 만"*.
단계 = 체크포인트 step — 400,000 (판 닿기 전 · 0 MPa) · 1,650,000 (47.1 MPa) · 3,100,000 (296.2 MPa) · 3,220,000 (이완 · 165.3 MPa).
porosity 는 `t2b_union_ckpt.py` (exact union) — 여기는 그림만.

입력 (읽기만):
  400,000 · 1,650,000 · 3,100,000 = 1저자 WSL 스냅숏 (`make_snap_decks.py` · run 0) 파서 출력 `<snap-root>/ps73_snap_<S>/ana/`
  3,220,000 = 첫 판 T3 와 같은 파서 출력 (`--ana-3220000`) · 상 이름 표 = `--meta` (type_map_resolved · scale — 첫 판과 같은 파일)
계산 = 첫 판 코드를 **그대로** 부른다 (값 · 인자 불변):
  3D = t1_render.main (render3d · 같은 카메라 규칙 · 첫 단계 상자) — 원자만 스냅숏 atoms.csv 에서 읽게 바꾼다
  σ_VM · 분류 = t3_vm_se.compute (vm_moments.moment → 봉인 calc_love_weber_stress) — 단계마다 ANA · step 만 바꾼다
  색 범위 = 네 단계 벽 아닌 SE (σ_VM > 0) 를 **모은** p5–p95 (vm_moments.common_range 규칙 · 10-08 AM 그림과 같은 규칙) · log · jet
출력 = `<out>` (기본 OUT/aligned_ckpt) — 첫 판 (t1_geometry · t3_vm_se) 은 건드리지 않는다.

  cd OUT && python3 -I -B code/aligned_figs.py --snap-root <폴더> --ana-3220000 <폴더> --meta <ana_3220000_meta.json>
"""
import argparse
import csv
import gzip
import io
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

import numpy as np  # noqa: E402

STAGES = [
    ('initial', 'Initial (before plate contact)', 400000),
    ('p47', '47 MPa (compression)', 1650000),
    ('p296', '296 MPa (just before stop)', 3100000),
    ('relaxed', 'After relaxation', 3220000),
]
SNAP_STEPS = (400000, 1650000, 3100000)


def snap_reader(snap_root, real_read):
    """C.read_atoms 와 같은 반환꼴 — 스냅숏 step 은 파서 출력 atoms.csv, 나머지는 원래 함수."""
    def read(step):
        if step not in SNAP_STEPS:
            return real_read(step)
        p = Path(snap_root) / f'ps73_snap_{step}' / 'ana' / 'atoms.csv'
        atoms = {}
        with open(p, newline='', encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                i = int(float(r['id']))
                if i in atoms:
                    raise SystemExit(f'⛔ {p}: id 중복 {i}')
                atoms[i] = {'x': float(r['x']), 'y': float(r['y']), 'z': float(r['z']), 'radius': float(r['radius']), 'type': int(float(r['type']))}
        ids = np.array(sorted(atoms), dtype=np.int64)
        arr = {'id': ids, 'x': np.array([atoms[i]['x'] for i in ids]), 'y': np.array([atoms[i]['y'] for i in ids]),
               'z': np.array([atoms[i]['z'] for i in ids]), 'r': np.array([atoms[i]['radius'] for i in ids]),
               'type': np.array([atoms[i]['type'] for i in ids], dtype=np.int64)}
        return atoms, arr, {'timestep': step, 'n_header': len(atoms), 'source': str(p)}
    return read


def ana_dir(a, step):
    return Path(a.ana_3220000) if step == 3220000 else Path(a.snap_root) / f'ps73_snap_{step}' / 'ana'


def run_t1(a, out):
    import t1_render as T1
    real = C.read_atoms
    C.read_atoms = snap_reader(a.snap_root, real)
    C.STAGES = STAGES
    old_out, old_odir = C.OUT, T1.ODIR
    C.OUT, T1.ODIR = out, out / 't1_geometry'
    (out / 'logs').mkdir(parents=True, exist_ok=True)
    try:
        T1.main(['--px', str(a.px)])
    finally:
        C.read_atoms, C.OUT, T1.ODIR = real, old_out, old_odir
    return json.loads((out / 'logs' / 't1_camera.json').read_text(encoding='utf-8'))


def stage_vm(a, step):
    import t3_vm_se as T3
    T3.ANA, T3.META, C.STRESS_STEP = ana_dir(a, step), Path(a.meta), step
    rows, info = T3.compute()
    info['inputs_sha256'] = {nm: C.sha256(T3.ANA / nm) for nm in ('atoms.csv', 'contacts.csv', 'mesh_info.json', 'input_params.json')}
    return rows, info


def write_gz_csv(path, header, rows):
    buf = io.StringIO(newline='')
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(header)
    w.writerows(rows)
    with open(path, 'wb') as fb, gzip.GzipFile(filename='', mode='wb', fileobj=fb, mtime=0) as gz:
        gz.write(buf.getvalue().encode('utf-8'))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--snap-root', required=True)
    ap.add_argument('--ana-3220000', required=True)
    ap.add_argument('--meta', required=True)
    ap.add_argument('--out', default=str(C.OUT / 'aligned_ckpt'))
    ap.add_argument('--px', type=int, default=1400)
    a = ap.parse_args(argv)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    import t3_vm_se as T3
    import render3d as R
    # ① 3D (상별 색) — 첫 판 T1 과 같은 코드 · 같은 카메라 규칙
    cam = run_t1(a, out)
    # ② 단계마다 σ_VM · 분류
    vdir = out / 't3_vm_se'
    vdir.mkdir(parents=True, exist_ok=True)
    per, infos = {}, {}
    for key, label, step in STAGES:
        t0 = time.time()
        rows, info = stage_vm(a, step)
        per[step], infos[step] = rows, info
        print(f'  σ_VM {key:8s} {step:>8d}  LW {info["lw_status"]}  SE {len(rows)}  ({round(time.time() - t0, 1)} s)', flush=True)
        write_gz_csv(vdir / f'ps73_se_vm_{step}.csv.gz',
                     ['id', 'x_um', 'y_um', 'z_um', 'r_um', 'vm_MPa', 'n_SE', 'n_PC', 'n_SC', 'class', 'wall_flag', 'wall_floor', 'wall_plate'],
                     [[rw[0], f'{rw[1]:.4f}', f'{rw[2]:.4f}', f'{rw[3]:.4f}', f'{rw[4]:.4f}', f'{rw[5]:.9g}', rw[6], rw[7], rw[8], rw[9],
                       rw[10], rw[11], rw[12]] for rw in rows])
    # ③ 공동 색 범위 = 네 단계 벽 아닌 SE (σ_VM > 0) 를 모은 p5–p95
    pool = np.concatenate([np.array([rw[5] for rw in per[s] if not rw[10] and rw[5] > 0]) for _, _, s in STAGES])
    lo, hi = float(np.percentile(pool, 5)), float(np.percentile(pool, 95))
    b = cam['camera_bounds_um']
    (ya, yb), (xa, xb) = cam['crop_rows_cols']
    from PIL import Image
    files = {}
    for key, label, step in STAGES:
        rows = per[step]
        xyz = np.array([[rw[1], rw[2], rw[3]] for rw in rows])
        r = np.array([rw[4] for rw in rows])
        vm = np.array([rw[5] for rw in rows])
        wall = np.array([rw[10] for rw in rows], dtype=bool)
        for grey, suffix in ((False, ''), (True, '_wallgrey')):
            rgb = R.colours(vm, wall, lo, hi, grey_wall=grey, scale='log')
            rgba = R.render(xyz, r, rgb, int(cam['px']), 2, (np.array(b[0]), np.array(b[1])))
            img = rgba[ya:yb, xa:xb]
            fn = vdir / f'ps73_se_vm3d_{step}_{key}{suffix}.png'
            R.save_png(fn, img)
            files[fn.name] = C.sha256(fn)
            im = Image.fromarray(np.clip(np.round(img * 255), 0, 255).astype(np.uint8), 'RGBA')
            bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
            bg.alpha_composite(im)
            bg.convert('RGB').save(vdir / f'ps73_se_vm3d_{step}_{key}{suffix}_preview_white.png')
        print(f'  3D SE {key:8s} {step:>8d} 그림 둘', flush=True)
    mid = R.colorbar_png(vdir / 'ps73_se_vm3d_colorbar_common.png', lo, hi, 'log')
    R.colorbar_png(vdir / 'ps73_se_vm3d_colorbar_common_bare.png', lo, hi, 'log', labels=False)
    # ④ 단계 × 분류 요약 (벽 아닌 SE · MPa) — 평문 + Origin
    summ = {}
    out_rows, origin_rows = [], []
    for key, label, step in STAGES:
        rows = per[step]
        vm = np.array([rw[5] for rw in rows])
        cl = np.array([rw[9] for rw in rows])
        wall = np.array([rw[10] for rw in rows], dtype=bool)
        summ[step] = {}
        for ck, clab in T3.CLASSES + [('ALL_SE', 'All SE')]:
            m = (~wall) if ck == 'ALL_SE' else ((cl == ck) & ~wall)
            s = T3.stats(vm[m])
            summ[step][ck] = {'label': clab, 'n_nonwall': int(m.sum()), **s}
            f = lambda v: '' if v is None else f'{v:.4g}'
            out_rows.append([step, label, ck, clab, int(m.sum()), f(s['mean']), f(s['median']), f(s['p25']), f(s['p75']), f(s['p90'])])
            origin_rows.append((f'{step * C.STEP_MS:.3f}', label, clab, int(m.sum()), f(s['mean']), f(s['median']), f(s['p25']),
                                f(s['p75']), f(s['p90'])))
    with open(vdir / 'ps73_se_vm_stage_class_summary.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['step', 'stage', 'class', 'label', 'n_nonwall', 'mean_MPa', 'median_MPa', 'p25_MPa', 'p75_MPa', 'p90_MPa'])
        w.writerows(out_rows)
    C.write_origin_csv(vdir / 'ps73_se_vm_stage_class_summary_origin.csv',
                       ['Simulation time', 'Stage', 'SE contact class', 'n (non-wall)', 'Mean', 'Median', 'p25', 'p75', 'p90'],
                       ['ms', '', '', '', 'MPa', 'MPa', 'MPa', 'MPa', 'MPa'], origin_rows,
                       ['step × 1e-3', '', 'AM touched by the SE', '', 'Love–Weber σ_VM · walls excluded', '', '', '', ''])
    rec = {'tool': 'aligned_figs', 'stages': [{'key': k, 'label': l, 'step': s} for k, l, s in STAGES],
           'colour_rule': 'pooled p5–p95 of non-wall SE with σ_VM > 0 over the four stages (vm_moments.common_range rule) · log · jet',
           'vmin_MPa': lo, 'vmax_MPa': hi, 'colorbar_mid_MPa': mid, 'n_pool': int(pool.size), 'camera': cam,
           'per_stage': {str(s): {'lw_status': infos[s]['lw_status'], 'lw_flags': infos[s]['lw_flags'], 'contacts': infos[s]['contacts'],
                                  'plate_z_used_deck': infos[s]['plate_z_used_deck'], 'plate_z_equal': infos[s]['plate_z_equal'],
                                  'inputs_sha256': infos[s]['inputs_sha256'], 'n_se': len(per[s]),
                                  'n_no_contact_with_nonzero_vm': infos[s]['n_no_contact_with_nonzero_vm'],
                                  'class_summary_nonwall': summ[s]} for _, _, s in STAGES},
           'png_sha256': files}
    C.write_json(vdir / 'ps73_se_vm_aligned.json', rec)
    print(f'공동 색 범위 {lo:.4g} … {hi:.4g} MPa (모은 SE {pool.size})')
    for key, label, step in STAGES:
        s = summ[step]['ALL_SE']
        print(f'  {step:>8d} {label:34s} SE (벽 아님) {s["n_nonwall"]:>6d}  중앙 {s["median"]:.4g}  평균 {s["mean"]:.4g} MPa')
    return 0


if __name__ == '__main__':
    sys.exit(main())
