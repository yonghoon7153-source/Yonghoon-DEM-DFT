#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T3 — 3,220,000 (이완 단계 · 접촉 덤프 프레임) SE 입자의 Love–Weber von Mises · 접촉 상대 상으로 분류.

입력 = 리포 웹앱 파서 (scripts/parse_liggghts.py) 출력 OUT/ana_3220000 (atoms.csv · contacts.csv · mesh_info.json) + input_params.json
(box 0.05 — snap_moments README §5 명령과 같은 꼴) + OUT/ana_3220000_meta.json (type_map_resolved · scale 1000).
계산 = snap_moments_20261008/vm_moments.py 의 moment() 를 **그대로** 부른다 —
  봉인 scripts/dem_analysis_core.calc_love_weber_stress(atoms_raw, contacts_raw, tmap, plate_z, box_x, box_y,
  plate_z_source='mesh', return_arrays=True) (입력 = scripts/plane_load_share.load_raw_for_lw = 봉인 analyze_contacts 로더) ·
  σ_VM = arrays_vm × scale / 1e6 (MPa) · 벽 = (z − r < 0) | (z + r > plate_z).
LW 반환 전체 (상태 · 검사 · 벽 표지) 는 같은 호출의 반환값을 가로채 기록만 한다 (값 · 인자 불변).
분류 = 같은 contacts_raw (LW 가 쓴 접촉 목록) 의 접촉 상대 상: PC (AM_P) · SC (AM_S) · SE.

  cd OUT && python3 -I -B code/t3_vm_se.py            # 계산 + 표 + 그림 (3D 는 T1 의 카메라 · 자르기 — logs/t1_camera.json 필요)
  cd OUT && python3 -I -B code/t3_vm_se.py --plots-only
"""
import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

import numpy as np  # noqa: E402

ANA = C.OUT / 'ana_3220000'
META = C.OUT / 'ana_3220000_meta.json'
ODIR = C.OUT / 't3_vm_se'
CLASSES = [('SE_only', 'SE only'), ('PC_only', 'PC only'), ('SC_only', 'SC only'), ('PC_and_SC', 'PC + SC'), ('no_contact', 'No contact')]
#: 그림 축 이름 (x = SE 가 닿은 AM 의 종류) — 분류 정의는 CSV · REPORT 와 같다 (SE 이웃은 어느 칸에서나 허용)
AXIS_LABEL = {'SE_only': 'None', 'PC_only': 'PC', 'SC_only': 'SC', 'PC_and_SC': 'PC + SC'}


def compute():
    import vm_moments as VM                                    # 리포 · 읽기 전용 import (snap_moments_20261008)
    pls = VM.pls
    core = pls._sealed('dem_analysis_core')
    meta = json.loads(META.read_text(encoding='utf-8'))
    tmap = pls.parse_type_map(meta['type_map_resolved'])
    scale = float(meta['scale'])
    orig = core.calc_love_weber_stress
    cap = {}

    def spy(*a, **k):                                          # 같은 호출 · 같은 반환 — 기록만
        out = orig(*a, **k)
        cap['lw'], cap['atoms_raw'], cap['contacts_raw'] = out, a[0], a[1]
        cap['args'] = {'type_map': a[2], 'plate_z': a[3], **{kk: vv for kk, vv in k.items()}}
        return out
    core.calc_love_weber_stress = spy
    try:
        t0 = time.time()
        rec, P = VM.moment(C.STRESS_STEP, ANA, tmap, scale)
        t_lw = round(time.time() - t0, 1)
    finally:
        core.calc_love_weber_stress = orig
    lw = cap['lw']
    plate_z_used = float(cap['args']['plate_z'])
    plate_csv = C.plate_table()[C.STRESS_STEP][0]
    flags = {k: v for k, v in lw.items() if k not in ('ids', 'tensor', 'arrays_vm')}
    if rec['lw_status'] != 'OK' or P is None:
        C.write_json(ODIR / 'lw_status.json', {'status': rec['lw_status'], 'flags': flags})
        raise SystemExit(f'⛔ LW 상태 {rec["lw_status"]} — 값을 내지 않는다')
    atoms_raw, contacts_raw = cap['atoms_raw'], cap['contacts_raw']
    # ── 접촉 상대 상 · 중복 검사 ──
    ids_sorted = np.array(sorted(atoms_raw), dtype=np.int64)
    typ = np.array([atoms_raw[i]['type'] for i in ids_sorted], dtype=np.int64)
    c1 = np.array([c['id1'] for c in contacts_raw], dtype=np.int64)
    c2 = np.array([c['id2'] for c in contacts_raw], dtype=np.int64)
    dl = np.array([c['delta'] for c in contacts_raw], dtype=float)
    j1, j2 = np.searchsorted(ids_sorted, c1), np.searchsorted(ids_sorted, c2)
    if not (np.array_equal(ids_sorted[j1], c1) and np.array_equal(ids_sorted[j2], c2)):
        raise SystemExit('⛔ 접촉 id 가 원자에 없다')
    lo_, hi_ = np.minimum(c1, c2), np.maximum(c1, c2)
    key = lo_ * (int(ids_sorted.max()) + 1) + hi_
    n_dup = int(key.size - np.unique(key).size)
    n_self = int((c1 == c2).sum())
    t1, t2 = typ[j1], typ[j2]
    n = ids_sorted.size
    cnt = {}
    for nm, tv in (('SE', 3), ('PC', 1), ('SC', 2)):
        cnt[nm] = (np.bincount(j1[t2 == tv], minlength=n) + np.bincount(j2[t1 == tv], minlength=n)).astype(np.int64)
    # ── SE 입자 표 (vm_moments.moment 의 P 순서 = atoms_raw 키 순서) ──
    pid = np.asarray(P['ids'], dtype=np.int64)
    row_of = np.searchsorted(ids_sorted, pid)
    is_se = P['name'] == 'SE'
    z, r = P['z'], P['r']
    zd = np.array([float(atoms_raw[a]['z']) for a in pid])        # 덱 단위 — vm_moments.moment 와 같은 비교 (µm 로 곱하지 않고)
    rd = np.array([float(atoms_raw[a]['radius']) for a in pid])
    floor = (zd - rd) < 0.0
    plate = (zd + rd) > plate_z_used
    if not np.array_equal(floor | plate, P['wall']):
        raise SystemExit('⛔ 벽 표지 재현 불일치 (바닥 · 판 ↔ vm_moments wall)')
    rows = []
    for i in np.where(is_se)[0]:
        k = row_of[i]
        nse, npc, nsc = int(cnt['SE'][k]), int(cnt['PC'][k]), int(cnt['SC'][k])
        if npc and nsc:
            cl = 'PC_and_SC'
        elif npc:
            cl = 'PC_only'
        elif nsc:
            cl = 'SC_only'
        elif nse:
            cl = 'SE_only'
        else:
            cl = 'no_contact'
        rows.append((int(pid[i]), float(P['x'][i]), float(P['y'][i]), float(z[i]), float(r[i]), float(P['vm'][i]),
                     nse, npc, nsc, cl, int(P['wall'][i]), int(floor[i]), int(plate[i])))
    # 접촉 0 인 SE 의 σ_VM = 0 이어야 한다 (정의상) · 접촉 있는 SE 는 대부분 > 0
    zero_bad = [rw[0] for rw in rows if rw[9] == 'no_contact' and rw[5] != 0.0]
    info = {'lw_status': rec['lw_status'], 'lw_flags': flags, 'lw_call_args': {k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()})
                                                                              for k, v in cap['args'].items()},
            'plate_z_used_deck': plate_z_used, 'plate_z_plate_csv_deck': plate_csv, 'plate_z_equal': plate_z_used == plate_csv,
            'vm_moments_record': {k: v for k, v in rec.items()}, 'seconds_lw': t_lw,
            'contacts': {'n': int(c1.size), 'n_duplicate_unordered_pairs': n_dup, 'n_self_pairs': n_self,
                         'n_delta_nonpositive': int((dl <= 0).sum())},
            'no_contact_with_nonzero_vm': zero_bad[:20], 'n_no_contact_with_nonzero_vm': len(zero_bad)}
    return rows, info


def stats(v):
    if v.size == 0:
        return dict(n=0, mean=None, median=None, p25=None, p75=None, p90=None)
    return dict(n=int(v.size), mean=float(v.mean()), median=float(np.median(v)), p25=float(np.percentile(v, 25)),
                p75=float(np.percentile(v, 75)), p90=float(np.percentile(v, 90)))


def write_tables(rows, info):
    with open(ODIR / 'ps73_se_vm_3220000.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['id', 'x_um', 'y_um', 'z_um', 'r_um', 'vm_MPa', 'n_SE', 'n_PC', 'n_SC', 'class', 'wall_flag', 'wall_floor', 'wall_plate'])
        for rw in rows:
            w.writerow([rw[0], f'{rw[1]:.4f}', f'{rw[2]:.4f}', f'{rw[3]:.4f}', f'{rw[4]:.4f}', f'{rw[5]:.9g}', rw[6], rw[7], rw[8], rw[9],
                        rw[10], rw[11], rw[12]])
    vm = np.array([rw[5] for rw in rows])
    cl = np.array([rw[9] for rw in rows])
    wall = np.array([rw[10] for rw in rows], dtype=bool)
    summ = {}
    for k, lab in CLASSES:
        m = cl == k
        s_nw = stats(vm[m & ~wall])
        s_all = stats(vm[m])
        summ[k] = {'label': lab, 'n_all': int(m.sum()), 'n_wall': int((m & wall).sum()), 'n_nonwall': int((m & ~wall).sum()),
                   'n_zero_vm_nonwall': int((m & ~wall & (vm == 0)).sum()), 'nonwall': s_nw, 'all_incl_wall': s_all}
    tot_nw = stats(vm[~wall])
    summ['ALL_SE'] = {'label': 'All SE', 'n_all': int(vm.size), 'n_wall': int(wall.sum()), 'n_nonwall': int((~wall).sum()),
                      'n_zero_vm_nonwall': int((~wall & (vm == 0)).sum()), 'nonwall': tot_nw, 'all_incl_wall': stats(vm)}
    head = ['class', 'label', 'n_all', 'n_wall', 'n_nonwall', 'mean_MPa', 'median_MPa', 'p25_MPa', 'p75_MPa', 'p90_MPa',
            'mean_incl_wall_MPa', 'median_incl_wall_MPa']
    f = lambda v: '' if v is None else f'{v:.4g}'
    with open(ODIR / 'ps73_se_vm_class_summary.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(head)
        for k in [c[0] for c in CLASSES] + ['ALL_SE']:
            s = summ[k]
            w.writerow([k, s['label'], s['n_all'], s['n_wall'], s['n_nonwall'], f(s['nonwall']['mean']), f(s['nonwall']['median']),
                        f(s['nonwall']['p25']), f(s['nonwall']['p75']), f(s['nonwall']['p90']), f(s['all_incl_wall']['mean']),
                        f(s['all_incl_wall']['median'])])
    # Origin 꼴 (머리 세 줄)
    C.write_origin_csv(ODIR / 'ps73_se_vm_class_summary_origin.csv',
                       ['SE contact class', 'n (non-wall)', 'Mean', 'Median', 'p25', 'p75', 'p90'],
                       ['', '', 'MPa', 'MPa', 'MPa', 'MPa', 'MPa'],
                       [(summ[k]['label'], summ[k]['n_nonwall'], f(summ[k]['nonwall']['mean']), f(summ[k]['nonwall']['median']),
                         f(summ[k]['nonwall']['p25']), f(summ[k]['nonwall']['p75']), f(summ[k]['nonwall']['p90']))
                        for k in [c[0] for c in CLASSES] + ['ALL_SE']],
                       ['Love–Weber σ_VM · step 3220000 · walls excluded', '', '', '', '', '', ''])
    return summ


def load_rows():
    rows = []
    with open(ODIR / 'ps73_se_vm_3220000.csv', newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            rows.append((int(r['id']), float(r['x_um']), float(r['y_um']), float(r['z_um']), float(r['r_um']), float(r['vm_MPa']),
                         int(r['n_SE']), int(r['n_PC']), int(r['n_SC']), r['class'], int(r['wall_flag']), int(r['wall_floor']),
                         int(r['wall_plate'])))
    return rows


def draw_box(rows, stem):
    """σ_VM 분포 (벽 아님) — 상자 = p25–p75 · 가운데 선 = 중앙값 · 수염 = p5–p95 · ◆ = 평균 · 이상점 안 그림 · log y.
    글꼴 · 크기 · 색 = make_fig_ms.draw_preview 와 같다 · 범례 = 축 밖."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    gray = '#404040'
    plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11, 'axes.edgecolor': gray, 'axes.labelcolor': gray,
                         'xtick.color': gray, 'ytick.color': gray, 'axes.linewidth': 1.0, 'xtick.direction': 'out',
                         'ytick.direction': 'out', 'xtick.major.size': 5, 'ytick.major.size': 5, 'xtick.minor.size': 2.5,
                         'ytick.minor.size': 2.5, 'axes.labelsize': 12.5, 'svg.hashsalt': 'ps73sevm', 'svg.fonttype': 'none'})
    keys = [k for k, _ in CLASSES if k != 'no_contact']
    labs = [AXIS_LABEL[k] for k in keys]                     # 축 = 'AM contact partner' — None (SE 만) · PC · SC · PC + SC
    vm = np.array([rw[5] for rw in rows])
    cl = np.array([rw[9] for rw in rows])
    wall = np.array([rw[10] for rw in rows], dtype=bool)
    data = [vm[(cl == k) & ~wall & (vm > 0)] for k in keys]
    W_AX, H_AX = 4.3, 3.35
    fig = plt.figure(figsize=(W_AX + 1.75, H_AX))
    ax = fig.add_axes([0.72 / (W_AX + 1.75), 0.52 / H_AX, (W_AX - 0.92) / (W_AX + 1.75), (H_AX - 0.70) / H_AX])
    ax.tick_params(top=False, right=False, which='both')
    face = '#2C7BB6'
    ax.boxplot(data, whis=(5, 95), showfliers=False, patch_artist=True, widths=0.55,
                    medianprops=dict(color='#D7191C', lw=1.6), boxprops=dict(facecolor=face + '40', edgecolor=gray, lw=1.0),
                    whiskerprops=dict(color=gray, lw=1.0), capprops=dict(color=gray, lw=1.0))
    ax.plot(range(1, len(data) + 1), [d.mean() for d in data], 'D', color=gray, ms=4.5, mew=0, zorder=4)
    ax.set_yscale('log')
    ax.set_xticks(range(1, len(labs) + 1))
    ax.set_xticklabels(labs)
    ax.set_ylabel('SE von Mises stress (MPa)')
    ax.set_xlabel('AM contact partner')
    lo = min(np.percentile(d, 5) for d in data)
    hi = max(np.percentile(d, 95) for d in data)
    ax.set_ylim(10 ** math.floor(math.log10(lo)), 10 ** math.ceil(math.log10(hi)))
    handles = [Patch(facecolor=face + '40', edgecolor=gray, label='p25–p75'), Line2D([], [], color='#D7191C', lw=1.6, label='Median'),
               Line2D([], [], color=gray, marker='D', ls='none', ms=4.5, mew=0, label='Mean'),
               Line2D([], [], color=gray, lw=1.0, label='p5–p95')]
    ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.03, 1.0), frameon=False, fontsize=10, handlelength=1.6,
              borderaxespad=0.0, labelcolor=gray)
    fig.savefig(f'{stem}.png', dpi=300)
    fig.savefig(f'{stem}.svg', metadata={'Date': None})
    plt.close(fig)
    return {'whiskers': 'p5–p95', 'box': 'p25–p75', 'fliers': 'not drawn', 'population': 'non-wall SE with σ_VM > 0'}


def render_se(rows, info_cam):
    """SE 만 3D — 색 = σ_VM (jet · log · render3d.colours) · 범위 = 벽 아닌 SE (σ_VM > 0) 의 p5–p95 (vm_moments.common_range 규칙을 SE 에) ·
    카메라 · 자르기 = T1 과 같음 (logs/t1_camera.json) · 벽 입자도 칠한다 (render3d 기본 · 벽 힘 빠진 값)."""
    import render3d as R
    xyz = np.array([[rw[1], rw[2], rw[3]] for rw in rows])
    r = np.array([rw[4] for rw in rows])
    vm = np.array([rw[5] for rw in rows])
    wall = np.array([rw[10] for rw in rows], dtype=bool)
    ok = (~wall) & (vm > 0)
    lo, hi = float(np.percentile(vm[ok], 5)), float(np.percentile(vm[ok], 95))
    b = info_cam['camera_bounds_um']
    (ya, yb), (xa, xb) = info_cam['crop_rows_cols']
    from PIL import Image
    inside = True
    #  기본 = 벽 입자도 칠함 (render3d 기본 · README §7 1저자 요청) · 보조 = 벽 입자 회색 (render3d.colours grey_wall=True · WALL_RGB)
    for grey, suffix in ((False, ''), (True, '_wallgrey')):
        rgb = R.colours(vm, wall, lo, hi, grey_wall=grey, scale='log')
        rgba = R.render(xyz, r, rgb, int(info_cam['px']), 2, (np.array(b[0]), np.array(b[1])))
        full_bbox = R.bbox(rgba)
        inside = inside and (full_bbox[0][0] >= ya and full_bbox[0][1] <= yb and full_bbox[1][0] >= xa and full_bbox[1][1] <= xb)
        img = rgba[ya:yb, xa:xb]
        R.save_png(ODIR / f'ps73_se_vm3d_3220000{suffix}.png', img)
        im = Image.fromarray(np.clip(np.round(img * 255), 0, 255).astype(np.uint8), 'RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        bg.convert('RGB').save(ODIR / f'ps73_se_vm3d_3220000{suffix}_preview_white.png')
    mid = R.colorbar_png(ODIR / 'ps73_se_vm3d_colorbar.png', lo, hi, 'log')
    R.colorbar_png(ODIR / 'ps73_se_vm3d_colorbar_bare.png', lo, hi, 'log', labels=False)
    return {'colour_rule': 'p5–p95 of non-wall SE with σ_VM > 0 (vm_moments.common_range p5p95 rule applied to SE · this step)',
            'vmin_MPa': lo, 'vmax_MPa': hi, 'colorbar_mid_MPa': mid, 'scale': 'log', 'cmap': 'render3d.jet8 = viewer3d.js jetColor',
            'n_below_vmin': int((vm < lo).sum()), 'n_above_vmax': int((vm > hi).sum()), 'n_zero': int((vm == 0).sum()),
            'n_wall': int(wall.sum()), 'wall_painting': {'ps73_se_vm3d_3220000.png': 'wall SE painted with incomplete LW value (render3d default)',
                                                         'ps73_se_vm3d_3220000_wallgrey.png': 'wall SE grey (render3d.WALL_RGB 0.72)'},
            'silhouette_inside_t1_crop': bool(inside), 'crop_rows_cols': info_cam['crop_rows_cols']}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--plots-only', action='store_true')
    ap.add_argument('--no-3d', action='store_true')
    a = ap.parse_args(argv)
    ODIR.mkdir(parents=True, exist_ok=True)
    if a.plots_only:
        rows = load_rows()
        info = json.loads((ODIR / 'ps73_se_vm_3220000.json').read_text(encoding='utf-8'))
    else:
        rows, info = compute()
        info['class_summary'] = write_tables(rows, info)
        info['inputs_sha256'] = {nm: C.sha256(ANA / nm) for nm in ('atoms.csv', 'contacts.csv', 'mesh_info.json', 'input_params.json')}
        info['meta_sha256'] = C.sha256(META)
        pl = json.loads(C.PLANE_JSON.read_text(encoding='utf-8'))['cases']['7:3']['inputs_sha256']
        info['webapp_case_sha256_match'] = {nm: info['inputs_sha256'][nm] == pl.get(nm) for nm in ('atoms.csv', 'contacts.csv', 'mesh_info.json')}
    info['box_plot'] = draw_box(rows, str(ODIR / 'ps73_se_vm_by_class'))
    if not a.no_3d:
        cam_p = C.OUT / 'logs' / 't1_camera.json'
        if cam_p.is_file():
            info['render3d'] = render_se(rows, json.loads(cam_p.read_text(encoding='utf-8')))
        else:
            print('⏸ logs/t1_camera.json 없음 — 3D 는 T1 뒤에 --plots-only 로')
    C.write_json(ODIR / 'ps73_se_vm_3220000.json', info)
    s = info['class_summary']
    print('LW', info['lw_status'], '· 판', info['plate_z_used_deck'], '= plate.csv', info['plate_z_equal'], '· 접촉', info['contacts'])
    for k, _ in CLASSES + [('ALL_SE', '')]:
        nw = s[k]['nonwall']
        fm = lambda v: '—' if v is None else f'{v:.4g}'
        print(f'  {k:10s} n {s[k]["n_all"]:>6d} (벽 {s[k]["n_wall"]:>5d})  평균 {fm(nw["mean"])}  중앙 {fm(nw["median"])}  '
              f'p25 {fm(nw["p25"])}  p75 {fm(nw["p75"])}  p90 {fm(nw["p90"])} MPa')
    return 0


if __name__ == '__main__':
    sys.exit(main())
