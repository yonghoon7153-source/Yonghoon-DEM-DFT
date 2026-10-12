#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T2 — 네 단계 porosity (구 부피 합 · 정확 union MC) + ps45 union 요약 재현 검사.

리포 함수 (읽기 전용 import · 고치지 않는다):
  ε_sphere = scripts/dem_analysis_core.calc_porosity(atoms, plate_z, box_xy, box_y)      — 1 − ΣV_구 / (Lx·Ly·plate_z) (웹앱 기본)
  ε_union  = scripts/dem_analysis_core.calc_porosity_union_exact(..., mc_n, seed)         — 상자 [0,Lx)×[0,Ly)×[0,plate_z) 무작위 점 MC
             (lhs_union_webapp.coverage 를 그대로 쓴다 · x·y 주기 · 벽 밖 부피는 고체로 안 셈)
             mc_n = 4,000,000 (lhs_union_webapp --mc-n 기본 = dem_analysis_core.UNION_MC_N_DEFAULT) ·
             seed = zlib.crc32(b'ps_7_3_r45') (lhs_union_webapp.run 이 케이스 이름으로 주는 시드 — ps45 요약표와 같은 규칙)
  재현 검사 = scripts/lhs_union_webapp.one(atom, contact, mesh, 3, 4e6, 같은 시드) — ps45 요약표 (r45_union_summary.tsv) 를 만든 함수 그대로.
판 높이 = curve/plate.csv (= 그 step 판 메시 STL · prepare.py 대조) · 상자 = 덤프 BOX BOUNDS (0–0.05 덱 = 50 µm).

  cd OUT && python3 -I -B code/t2_porosity.py
"""
import csv
import json
import math
import sys
import time
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

import numpy as np  # noqa: E402

MC_N = 4_000_000
SEED = zlib.crc32(C.CASE.encode())
ODIR = C.OUT / 't2_porosity'


def cap(r, h):
    """lhs_union_webapp._cap 과 같은 식을 그 모듈에서 부른다 (구 cap 부피)."""
    import lhs_union_webapp as U
    return U._cap(r, h)


def boundary_counts(A, plate_z):
    """판 · 바닥 밖 입자 수 — 규칙 = plane_load_share (n_center_above_plate: z > plate_z · n_center_below_floor: z < 0) ·
    lhs_descriptor_harvest._wall_contact (닿음: 겹침 깊이 > 0 · 통째로 밖: z − r > plate_z)."""
    z, r, t = A['z'], A['r'], A['type']
    above_c = z > plate_z
    out = {
        'n_center_above_plate': int(above_c.sum()),
        'n_fully_above_plate': int((z - r > plate_z).sum()),
        'n_touch_plate': int((z + r > plate_z).sum()),
        'n_center_below_floor': int((z < 0).sum()),
        'n_touch_floor': int((z - r < 0).sum()),
        'center_above_plate_by_phase': {C.TYPE_MAP[k]: int((above_c & (t == k)).sum()) for k in C.TYPE_MAP if (above_c & (t == k)).any()},
        'center_above_plate_ids': [int(i) for i in A['id'][above_c]],
        'center_above_plate_max_um': float((z[above_c] - plate_z).max() * C.SCALE) if above_c.any() else None,
    }
    lx = ly = 0.05
    vb = lx * ly * plate_z
    v_plate = float(np.where(z + r > plate_z, cap(r, z + r - plate_z), 0.0).sum())
    v_floor = float(np.where(z - r < 0, cap(r, r - z), 0.0).sum())
    out['overhang_plate_over_Vbox_pct'] = 100.0 * v_plate / vb
    out['overhang_floor_over_Vbox_pct'] = 100.0 * v_floor / vb
    out['atom_top_um'] = float((z + r).max() * C.SCALE)            # 모든 원자의 max(z + r) — make_fig_ms '원자 기준 두께'
    return out


def stage_row(step, label, key):
    import dem_analysis_core as WEB
    atoms, A, info = C.read_atoms(step)
    (x0, x1), (y0, y1), _ = info['box_deck']
    lx, ly = x1 - x0, y1 - y0
    if not (x0 == 0.0 and y0 == 0.0 and math.isclose(lx, 0.05) and math.isclose(ly, 0.05)):
        raise SystemExit(f'⛔ 상자 {info["box_deck"]} — 0–0.05 덱 (50 µm) 이 아니다')
    plate_z = C.plate_table()[step][0]
    t0 = time.time()
    eps_s = float(WEB.calc_porosity(atoms, plate_z, box_xy=lx, box_y=ly))
    un = WEB.calc_porosity_union_exact(atoms, plate_z, box_xy=lx, box_y=ly, mc_n=MC_N, seed=SEED)
    if un['union_exact_status'] != 'OK':
        raise SystemExit(f'⛔ union 상태 {un["union_exact_status"]} @ {step}')
    bc = boundary_counts(A, plate_z)
    v_sum = float((4.0 / 3.0 * np.pi * A['r'] ** 3).sum())
    rec = {'stage_key': key, 'stage': label, 'step': step, 'time_ms': step * C.STEP_MS, 'plate_um': plate_z * C.SCALE,
           'plate_z_deck': plate_z, 'box_deck': [lx, ly], 'n_atoms': info['n_header'],
           'n_by_phase': {C.TYPE_MAP[k]: int((A['type'] == k).sum()) for k in C.TYPE_MAP},
           'eps_sphere_pct': eps_s, 'eps_union_pct': un['porosity_union_exact_pct'], 'union_mc_std_pct': un['porosity_union_exact_se_pct'],
           'union_mc_n': un['union_exact_mc_n'], 'union_mc_seed': un['union_exact_mc_seed'],
           'wall_overhang_over_Vbox_pct': un['wall_overhang_over_Vbox_pct'],
           'V_sphere_sum_deck': v_sum, 'atom_top_eps_sphere_pct_INFO': 100.0 * (1.0 - v_sum / (lx * ly * bc['atom_top_um'] / C.SCALE)),
           **bc, 'seconds': round(time.time() - t0, 1)}
    print(f'  {key:8s} step {step:>8d}  판 {rec["plate_um"]:.3f} µm  ε_sphere {eps_s:.4f} %  ε_union {rec["eps_union_pct"]:.4f} ± '
          f'{rec["union_mc_std_pct"]:.4f} %  판 위 중심 {bc["n_center_above_plate"]}  판 닿음 {bc["n_touch_plate"]}  ({rec["seconds"]} s)', flush=True)
    return rec, atoms, A


def reproduce_ps45(atoms_3220):
    """ps45 union 요약표 (r45_union_summary.tsv · 7:3 행) 재현 — 그 표를 만든 lhs_union_webapp.one() 을 같은 입력 · 같은 시드로."""
    import lhs_union_webapp as U
    import dem_analysis_core as WEB
    row = None
    with open(C.UNION_TSV, newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh, delimiter='\t'):
            if r['case'] == C.CASE:
                row = r
    s = C.STRESS_STEP
    if row is None or int(row['atom_step']) != s or row['webapp_case_id'] != C.WEBAPP_CASE:
        raise SystemExit(f'⛔ 요약표 행 {row}')
    t0 = time.time()
    rec = U.one(C.atom_path(s), C.contact_path(s), C.mesh_path(s), 3, MC_N, SEED)
    t_one = round(time.time() - t0, 1)
    plate_z = C.plate_table()[s][0]
    alt = WEB.calc_porosity_union_exact(atoms_3220, plate_z, box_xy=0.05, box_y=0.05, mc_n=MC_N)   # 웹앱 기본 시드 (다른 점) — MC 잡음 확인
    same_seed = WEB.calc_porosity_union_exact(atoms_3220, plate_z, box_xy=0.05, box_y=0.05, mc_n=MC_N, seed=SEED)
    ref = {k: float(row[k]) for k in ('porosity_union_exact_pct', 'porosity_union_exact_se_pct', 'porosity_union_pair_web_pct',
                                     'porosity_sphere_web_pct', 'thickness_um')}
    chk = {
        'union_exact_vs_tsv': {'ours': rec['mc_void_pct'], 'tsv': ref['porosity_union_exact_pct'],
                               'diff_pct_point': rec['mc_void_pct'] - ref['porosity_union_exact_pct'],
                               'tsv_4dp_equal': f'{rec["mc_void_pct"]:.4f}' == row['porosity_union_exact_pct'],
                               'within_2sigma': abs(rec['mc_void_pct'] - ref['porosity_union_exact_pct']) <= 2 * ref['porosity_union_exact_se_pct']},
        'union_se_vs_tsv': {'ours': rec['mc_void_se_pct'], 'tsv': ref['porosity_union_exact_se_pct'],
                            'tsv_4dp_equal': f'{rec["mc_void_se_pct"]:.4f}' == row['porosity_union_exact_se_pct']},
        'sphere_vs_tsv': {'ours': rec['eps_sphere_web'], 'tsv': ref['porosity_sphere_web_pct'],
                          'tsv_4dp_equal': f'{rec["eps_sphere_web"]:.4f}' == row['porosity_sphere_web_pct']},
        'pair_union_vs_tsv': {'ours': rec['eps_union_web'], 'tsv': ref['porosity_union_pair_web_pct'],
                              'tsv_2dp_equal': f'{rec["eps_union_web"]:.2f}' == row['porosity_union_pair_web_pct']},
        'thickness_vs_tsv': {'ours': rec['thickness_um'], 'tsv': ref['thickness_um'],
                             'tsv_3dp_equal': f'{rec["thickness_um"]:.3f}' == row['thickness_um']},
        'am_counts_vs_tsv': {'tsv': row['AM_P_AM_S_count']},
        'one_vs_calc_union_exact_same_seed_identical': rec['mc_void_pct'] == same_seed['porosity_union_exact_pct'],
        'webapp_default_seed': {'seed': alt['union_exact_mc_seed'], 'eps_union_pct': alt['porosity_union_exact_pct'],
                                'std_pct': alt['porosity_union_exact_se_pct'],
                                'diff_vs_tsv_pct_point': alt['porosity_union_exact_pct'] - ref['porosity_union_exact_pct'],
                                'within_2sigma_of_diff': abs(alt['porosity_union_exact_pct'] - ref['porosity_union_exact_pct'])
                                <= 2 * math.sqrt(2) * ref['porosity_union_exact_se_pct']},
        'delta_col_vs_geom_max_rel': rec['delta_col_vs_geom_max_rel'], 'n_contact_id_missing': rec['n_contact_id_missing'],
        'pair_upper_bound_ok': rec.get('pair_upper_bound_ok'), 'sphere_web_minus_dual': rec['sphere_web_minus_dual'],
        'seconds_one': t_one,
    }
    ok = (chk['union_exact_vs_tsv']['within_2sigma'] and chk['sphere_vs_tsv']['tsv_4dp_equal'] and chk['thickness_vs_tsv']['tsv_3dp_equal']
          and chk['one_vs_calc_union_exact_same_seed_identical'] and chk['webapp_default_seed']['within_2sigma_of_diff']
          and (rec['delta_col_vs_geom_max_rel'] or 0) <= U.DELTA_TOL and not rec['n_contact_id_missing'])
    chk['status'] = 'PASS' if ok else 'FAIL'
    keep = {k: v for k, v in rec.items() if not isinstance(v, (list, dict))}
    return chk, keep, row


def draw(rows, path_stem):
    """make_fig_ms.draw_preview 의 글꼴 · 크기 · 색 · 단계 점선 · 단계 이름을 그대로 쓰고, 두 계열 + 범례 (축 밖) 를 더한다."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator
    if str(C.CURVE_DIR) not in sys.path:
        sys.path.append(str(C.CURVE_DIR))
    import make_fig_ms as MF                                   # 리포 · 읽기 전용 import (상수 X0 · X1 · XLABEL)
    key = json.loads((C.CURVE_DIR / 'key_numbers.json').read_text(encoding='utf-8'))
    b = {k: int(v) for k, v in key['phase_bounds'].items()}
    bounds_ms = [b['3'] * MF.STEP_MS, b['4'] * MF.STEP_MS]     # 압축 시작 400.002 · 이완 시작 3125 ms (make_fig_ms.main 과 같은 식)
    gray, light = '#404040', '#9AA0A8'
    plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11, 'axes.edgecolor': gray, 'axes.labelcolor': gray,
                         'xtick.color': gray, 'ytick.color': gray, 'axes.linewidth': 1.0, 'xtick.direction': 'out',
                         'ytick.direction': 'out', 'xtick.major.size': 5, 'ytick.major.size': 5, 'xtick.minor.size': 2.5,
                         'ytick.minor.size': 2.5, 'xtick.minor.visible': True, 'ytick.minor.visible': True,
                         'axes.labelsize': 12.5, 'svg.hashsalt': 'ps73porosity', 'svg.fonttype': 'none'})
    W_AX, H_AX = 4.3, 3.35                                     # draw_preview 와 같은 그림 크기 → 오른쪽에 범례 자리를 더한다
    fig = plt.figure(figsize=(W_AX + 1.75, H_AX))
    ax = fig.add_axes([0.62 / (W_AX + 1.75), 0.52 / H_AX, (W_AX - 0.82) / (W_AX + 1.75), (H_AX - 0.70) / H_AX])
    ax.tick_params(top=False, right=False, which='both')
    t = [r['time_ms'] for r in rows]
    ser = [('eps_sphere_pct', None, '#2C7BB6', 'o', 'Sphere-sum'), ('eps_union_pct', 'union_mc_std_pct', '#D7191C', 's', 'Exact union (MC)')]
    for k, ek, col, mk, lab in ser:
        y = [r[k] for r in rows]
        ax.plot(t, y, '-', color=col, lw=1.6, marker=mk, ms=5.5, mew=0, label=lab, zorder=3, clip_on=False)
        if ek:
            eb = ax.errorbar(t, y, yerr=[r[ek] for r in rows], fmt='none', ecolor=col, elinewidth=1.0, capsize=0, zorder=2)
            for a in eb.lines[2]:
                a.set_clip_on(False)
    for x in bounds_ms:
        ax.axvline(x, color=light, lw=0.9, ls=':')
    ylim = (10, 35)
    y_top = ylim[1] - 0.04 * (ylim[1] - ylim[0])
    b3, b4 = bounds_ms
    ax.text(b3 / 2, y_top, 'Settling', rotation=90, fontsize=8.5, color=light, ha='center', va='top')
    ax.text((b3 + b4) / 2, y_top, 'Compression', fontsize=9, color=light, ha='center', va='top')
    ax.text(min((b4 + MF.X1) / 2, MF.X1 - 30), y_top, 'Relaxation', rotation=90, fontsize=8.5, color=light, ha='center', va='top')
    ax.set_xlim(MF.X0, MF.X1)
    ax.set_ylim(*ylim)
    ax.xaxis.set_major_locator(MultipleLocator(1000))
    ax.xaxis.set_minor_locator(MultipleLocator(500))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    ax.set_xlabel(MF.XLABEL)
    ax.set_ylabel('Porosity (%)')
    ax.legend(loc='upper left', bbox_to_anchor=(1.03, 1.0), frameon=False, fontsize=10, handlelength=1.8, borderaxespad=0.0,
              labelcolor=gray)
    fig.savefig(f'{path_stem}.png', dpi=300)
    fig.savefig(f'{path_stem}.svg', metadata={'Date': None})
    plt.close(fig)
    return bounds_ms


def write_csvs(allrows):
    """평문 CSV (요청 열 이름 · 검사 행 포함 · role 열) + Origin CSV (네 단계만 · A = X 시간 · B · C = Y · D = C 의 오차 · 머리 세 줄)."""
    with open(ODIR / 'ps73_stage_porosity.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['stage', 'step', 'time_ms', 'plate_um', 'eps_sphere_pct', 'eps_union_pct', 'union_mc_std_pct',
                    'n_center_above_plate', 'n_touch_plate', 'n_fully_above_plate', 'overhang_plate_over_box_pct', 'atom_top_um', 'role'])
        for r in allrows:
            w.writerow([r['stage'], r['step'], f'{r["time_ms"]:.3f}', f'{r["plate_um"]:.3f}', f'{r["eps_sphere_pct"]:.4f}',
                        f'{r["eps_union_pct"]:.4f}', f'{r["union_mc_std_pct"]:.4f}', r['n_center_above_plate'], r['n_touch_plate'],
                        r['n_fully_above_plate'], f'{r["overhang_plate_over_Vbox_pct"]:.5f}', f'{r["atom_top_um"]:.3f}',
                        'stage' if r['stage_key'] != 'check3220' else 'check (ps45 union summary frame · stress frame)'])
    head = ['Simulation time', 'Porosity (sphere-sum)', 'Porosity (exact union)', 'Union MC std', 'Plate height', 'Step', 'Stage',
            'Centers above plate', 'Particles touching plate']
    units = ['ms', '%', '%', '%', 'µm', '', '', '', '']
    comm = ['step × 1e-3', '1 − ΣV_sphere/(A·H)', 'MC 4e6 points · seed crc32(ps_7_3_r45)', 'binomial 1σ (yErr of C)',
            'H = plate.csv = mesh STL', '', '', 'z > H', 'z + r > H']
    rows = [(f'{r["time_ms"]:.3f}', f'{r["eps_sphere_pct"]:.4f}', f'{r["eps_union_pct"]:.4f}', f'{r["union_mc_std_pct"]:.4f}',
             f'{r["plate_um"]:.3f}', r['step'], r['stage'], r['n_center_above_plate'], r['n_touch_plate'])
            for r in allrows if r['stage_key'] != 'check3220']
    C.write_origin_csv(ODIR / 'ps73_stage_porosity_origin.csv', head, units, rows, comm)


def main():
    ODIR.mkdir(parents=True, exist_ok=True)
    if '--plot-only' in sys.argv[1:]:                          # 계산 없이 JSON 의 값으로 그림만 다시
        S = json.loads((ODIR / 'ps73_stage_porosity.json').read_text(encoding='utf-8'))
        write_csvs(S['stages'])
        draw([r for r in S['stages'] if r['stage_key'] != 'check3220'], str(ODIR / 'ps73_stage_porosity'))
        return 0
    rows = []
    for key, label, step in C.STAGES:
        rec, atoms, A = stage_row(step, label, key)
        rows.append(rec)
    chk_rec, atoms_3220, _ = stage_row(C.STRESS_STEP, 'After relaxation — stress frame (union check)', 'check3220')
    chk, one_rec, tsv_row = reproduce_ps45(atoms_3220)
    print(f'  재현 검사: one() union {one_rec["mc_void_pct"]:.4f} ± {one_rec["mc_void_se_pct"]:.4f} ↔ 요약표 '
          f'{tsv_row["porosity_union_exact_pct"]} ± {tsv_row["porosity_union_exact_se_pct"]} · sphere {one_rec["eps_sphere_web"]:.4f} ↔ '
          f'{tsv_row["porosity_sphere_web_pct"]} · 웹앱 기본 시드 {chk["webapp_default_seed"]["eps_union_pct"]:.4f} → {chk["status"]}')
    allrows = rows + [chk_rec]
    write_csvs(allrows)
    bounds = draw(rows, str(ODIR / 'ps73_stage_porosity'))
    summ = {'tool': 't2_porosity', 'mc_n': MC_N, 'seed': SEED, 'seed_rule': "zlib.crc32(b'ps_7_3_r45') — lhs_union_webapp.run 의 케이스 시드",
            'functions': {'eps_sphere': 'scripts/dem_analysis_core.calc_porosity', 'eps_union': 'scripts/dem_analysis_core.calc_porosity_union_exact '
                          '(→ scripts/lhs_union_webapp.coverage)', 'check': 'scripts/lhs_union_webapp.one'},
            'phase_bounds_ms': bounds, 'stages': allrows, 'ps45_check': chk, 'ps45_check_one_record': one_rec,
            'ps45_tsv_row': tsv_row}
    C.write_json(ODIR / 'ps73_stage_porosity.json', summ)
    print('→', ODIR, '· 재현 검사', chk['status'])
    return 0 if chk['status'] == 'PASS' else 2


if __name__ == '__main__':
    sys.exit(main())
