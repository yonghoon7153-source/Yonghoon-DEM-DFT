#!/usr/bin/env python3
"""네 시점 von Mises — ps73 (ps45 · PC:SC 7:3 · r45) 압축 중 → 이완 끝을 같은 색 범위로 (1저자 10-08 *"4등분으로 von mis 구한 다음에 공동 스케일로"*).

입력 (시점마다): 웹앱 파서 결과 폴더 (atoms.csv · contacts.csv · mesh_info.json · input_params.json — `scripts/parse_liggghts.py` 출력) +
공통 meta (type_map_resolved · scale).  폴더는 `--moment STEP DIR` 로 시점 순서대로 준다.
계산: 봉인 `dem_analysis_core.calc_love_weber_stress` (return_arrays) 의 `arrays_vm` 그대로 — 입자 접촉력 기반 대칭 응력의 von Mises
(웹앱 'AM 만 — 입자 응력 (LW)' 와 같은 정의) × scale / 1e6 → MPa.  읽기 전용 (봉인 함수 · 로더를 고치지 않는다 · `plane_load_share` 를 거친다).
벽 (바닥 · 판) 접촉은 덤프에 없다 → 벽에 닿은 입자 (z − r < 0 · z + r > 판 높이) 는 응력이 불완전 = 회색 · 색 범위 · 평균에서 뺀다.

그림 (영문 · Liberation Sans/Arial):
  vm_moments.{png,svg}       위 = 판 압력 곡선 + 네 시점 표지 · 아래 = 네 패널 (AM 입자 옆모습 x–z · 정사영 · 깊이 순 · 실제 반경) ·
                              색 = σ_VM (MPa · log) · 네 패널 같은 범위 (기본 = 네 시점 AM 값을 모은 p5–p95)
  vm_moments_ratio.{png,svg} 같은 그림 · 색 = σ_VM / ⟨σ_VM⟩ (그 시점 전 입자 평균 — 크기를 뺀 공간 분포만)
  vm_profile.{png,svg}       높이 (z / 판 높이 · 10 칸) 별 부피 가중 평균 σ_VM — AM · SE 두 패널 · 네 시점 선
자료: vm_moments.json (시점별 상태 · 수 · 평균 · 위 1/3 ÷ 아래 1/3 · 색 범위) · vm_am_<step>.csv (AM 입자) · vm_profile.csv.
LW 상태가 OK 가 아닌 시점이 하나라도 있으면 그림을 그리지 않고 rc 2 (공동 색 범위는 네 시점이 다 있어야 뜻이 있다 — 0 으로 채우지 않는다).

  python3 vm_moments.py --meta meta.json --moment 1000000 <dir1> --moment 2200000 <dir2> --moment 3100000 <dir3> --moment 3220000 <dir4> --out <폴더>
  python3 vm_moments.py --selftest
"""
import argparse
import csv
import importlib
import json
import math
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DT_S = 1e-6                                   # 덱 timestep (s) — ps73 압축 곡선과 같은 환산 (step × 1e-6 s)
LABELS4 = ('First plate contact', 'Mid-compression', 'Just before the stop', 'Relaxed end')
WALL_GREY, NOCONTACT_GREY = '#b8b8b8', '#e6e6e6'
N_BINS = 10
FONTS = ('Liberation Sans', 'Arial')               # 그림 글꼴 후보 (없으면 matplotlib 기본 DejaVu Sans)


def _repo():
    env = os.environ.get('DEM_REPO')
    if env and (Path(env) / 'scripts' / 'plane_load_share.py').is_file():
        return Path(env)
    for p in [HERE] + list(HERE.parents):
        if (p / 'scripts' / 'plane_load_share.py').is_file():
            return p
    raise RuntimeError('리포 scripts/plane_load_share.py 를 못 찾았다 (DEM_REPO 로 지정)')


REPO = _repo()
if str(REPO / 'scripts') not in sys.path:
    sys.path.insert(0, str(REPO / 'scripts'))
pls = importlib.import_module('plane_load_share')
PRESSURE_CSV = REPO / 'docs' / 'data' / 'ps73_compaction_curve_20261006' / 'curve' / 'pressure.csv'


def plate_pressure(path=PRESSURE_CSV):
    out = {}
    with open(path, encoding='utf-8') as fh:
        r = csv.reader(fh)
        next(r)
        for row in r:
            try:
                out[int(row[0])] = float(row[3])
            except (ValueError, IndexError):
                continue
    return out


def moment(step, res_dir, tmap, scale):
    """한 시점 — 봉인 LW → 입자 σ_VM (MPa) · σ_zz (압축 양수 MPa) · 벽 표지.  LW 가 OK 가 아니면 값 없이 상태만."""
    res_dir = Path(res_dir)
    core = pls._sealed('dem_analysis_core')
    plate_z = float(json.loads((res_dir / 'mesh_info.json').read_text(encoding='utf-8'))['plate_z'])
    ip = json.loads((res_dir / 'input_params.json').read_text(encoding='utf-8'))
    bx, by = float(ip['box_x']), float(ip['box_y'])
    atoms_raw, contacts_raw = pls.load_raw_for_lw(res_dir)
    lw = core.calc_love_weber_stress(atoms_raw, contacts_raw, tmap, plate_z, box_x=bx, box_y=by,
                                     plate_z_source='mesh', return_arrays=True)
    rec = {'step': int(step), 'dir': str(res_dir), 'lw_status': str(lw.get('status')), 'lw_definition': lw.get('definition'),
           'plate_z_um': plate_z * scale, 'box_um': [bx * scale, by * scale], 'n_atoms': len(atoms_raw), 'n_contacts': len(contacts_raw),
           'inputs_sha256': {nm: pls._sha(res_dir / nm) for nm in ('atoms.csv', 'contacts.csv', 'mesh_info.json', 'input_params.json')}}
    if rec['lw_status'] != 'OK':
        return rec, None
    ids = list(lw['ids'])
    conv = float(scale) / 1e6
    vm = np.asarray(lw['arrays_vm'], dtype=float) * conv
    szz = -np.asarray(lw['tensor'], dtype=float)[:, 2, 2] * conv
    g = lambda k: np.array([float(atoms_raw[a][k]) for a in ids])
    x, y, z, r = g('x'), g('y'), g('z'), g('radius')
    name = np.array([str(tmap.get(atoms_raw[a]['type'], '')) for a in ids], dtype=object)
    wall = ((z - r) < 0.0) | ((z + r) > plate_z)
    P = {'ids': np.array(ids), 'name': name, 'x': x * scale, 'y': y * scale, 'z': z * scale, 'r': r * scale,
         'vm': vm, 'szz': szz, 'wall': wall, 'H': plate_z * scale}
    vol = r ** 3
    rec['mean_vm_all_MPa'] = float(vm.mean())            # 전 입자 수 평균 (접촉 없는 입자 = 0 · 웹앱 lw_ratio 의 분모와 같은 정의)
    for ph, m in (('AM', np.array(['AM' in n for n in name])), ('SE', name == 'SE')):
        ok = m & ~wall
        H = plate_z
        top, bot = ok & (z > 2 * H / 3), ok & (z < H / 3)
        wmean = lambda mm: float((vol[mm] * vm[mm]).sum() / vol[mm].sum()) if mm.any() else None
        t, b = wmean(top), wmean(bot)
        rec[ph] = {'n': int(m.sum()), 'n_wall': int((m & wall).sum()), 'n_zero': int((ok & (vm == 0)).sum()),
                   'mean_vm_MPa': wmean(ok), 'median_vm_MPa': float(np.median(vm[ok])) if ok.any() else None,
                   'top_third_mean_vm_MPa': t, 'bottom_third_mean_vm_MPa': b,
                   'top_over_bottom': (t / b if (t is not None and b) else None)}
    return rec, P


def common_range(Ps, rule='p5p95', vmin=None, vmax=None, key='vm'):
    """네 시점 AM (벽 아님 · 값 > 0) 을 모은 범위 — p5p95 (기본) · minmax · fixed (vmin · vmax)."""
    vals = np.concatenate([P[key][(np.array(['AM' in n for n in P['name']])) & ~P['wall'] & (P[key] > 0)] for P in Ps])
    if rule == 'fixed':
        if not (vmin and vmax and 0 < vmin < vmax):
            raise ValueError('fixed 범위는 0 < vmin < vmax 가 필요하다')
        return float(vmin), float(vmax)
    if not vals.size:
        raise ValueError('색 범위를 낼 AM 값이 없다')
    if rule == 'minmax':
        return float(vals.min()), float(vals.max())
    return float(np.percentile(vals, 5)), float(np.percentile(vals, 95))


def _fmt_p(p):
    return f'{p:.2f}' if p < 10 else f'{p:.0f}'


def _style(plt):
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': list(FONTS) + ['DejaVu Sans'], 'font.size': 8, 'axes.linewidth': 0.8,
                         'xtick.direction': 'in', 'ytick.direction': 'in', 'svg.fonttype': 'none'})


def draw_moments(recs, Ps, labels, pres, lo, hi, out_png, key='vm', cbar_label=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import EllipseCollection
    from matplotlib.colors import LogNorm
    _style(plt)
    n = len(Ps)
    fig = plt.figure(figsize=(2.6 * n + 1.0, 6.6))
    gs = fig.add_gridspec(2, n + 1, height_ratios=[1.0, 3.2], width_ratios=[1] * n + [0.06], hspace=0.32, wspace=0.18)
    ax0 = fig.add_subplot(gs[0, :n])
    steps = sorted(pres)
    ax0.plot([s * DT_S for s in steps], [pres[s] for s in steps], '-', color='#000000', lw=1.0)
    ts = [rec['step'] * DT_S for rec in recs]
    span = (steps[-1] - steps[0]) * DT_S
    for k, t in enumerate(ts):
        ax0.axvline(t, ls=':', color='#c00000', lw=0.9)
        near_next = k + 1 < len(ts) and ts[k + 1] - t < 0.05 * span          # 가까운 두 표지 (3.10 · 3.22 s) 가 겹치지 않게
        near_prev = k > 0 and t - ts[k - 1] < 0.05 * span
        ha = 'right' if near_next else ('left' if near_prev else 'center')
        ax0.text(t, 318, f'({chr(97 + k)})', ha=ha, va='bottom', color='#c00000', fontsize=8)
    ax0.set_xlim(steps[0] * DT_S, steps[-1] * DT_S)
    ax0.set_ylim(0, 345)
    ax0.set_xlabel('Simulation time (s)')
    ax0.set_ylabel('Plate pressure (MPa)')
    norm = LogNorm(vmin=lo, vmax=hi)
    cmap = matplotlib.colormaps['jet']
    zmax = max(P['H'] for P in Ps)
    bx = max(rec['box_um'][0] for rec in recs)
    for k, (rec, P) in enumerate(zip(recs, Ps)):
        ax = fig.add_subplot(gs[1, k])
        am = np.array(['AM' in nm for nm in P['name']])
        idx = np.where(am)[0]
        idx = idx[np.argsort(-P['y'][idx])]               # 먼 쪽 (y 큰 쪽) 먼저 → 앞 (y 작은 쪽) 이 위에 그려진다
        v = P[key][idx]
        col = np.array([cmap(norm(np.clip(val, lo, hi))) if val > 0 else matplotlib.colors.to_rgba(NOCONTACT_GREY) for val in v])
        col[P['wall'][idx]] = matplotlib.colors.to_rgba(WALL_GREY)
        ec = EllipseCollection(2 * P['r'][idx], 2 * P['r'][idx], np.zeros(idx.size), units='xy',
                               offsets=np.c_[P['x'][idx], P['z'][idx]], offset_transform=ax.transData,
                               facecolors=col, edgecolors='#202020', linewidths=0.12)
        ax.add_collection(ec)
        ax.axhline(P['H'], color='#606060', lw=0.8, ls='--')
        ax.set_xlim(0, bx)
        ax.set_ylim(0, zmax * 1.02)
        ax.set_aspect('equal')
        ax.set_xlabel('x (µm)')
        if k == 0:
            ax.set_ylabel('z (µm)')
        else:
            ax.set_yticklabels([])
        p = pres.get(rec['step'])
        ax.set_title(f'({chr(97 + k)}) {labels[k]}\nt = {rec["step"] * DT_S:.2f} s · plate {_fmt_p(p) if p is not None else "—"} MPa',
                     fontsize=8)
    cax = fig.add_subplot(gs[1, n])
    sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, cax=cax)
    cb.set_label(cbar_label or 'von Mises stress σ_VM (MPa) — Love–Weber, AM particles', fontsize=8)
    fig.text(0.01, 0.005, 'AM particles only (side view x–z, depth-sorted, true radius).  Grey = touching floor or plate '
             '(wall forces are not in the contact dump — stress incomplete).  Same colour range in all panels.', fontsize=6.5, color='#404040')
    fig.savefig(out_png, dpi=220, bbox_inches='tight')
    fig.savefig(str(out_png)[:-4] + '.svg', bbox_inches='tight')
    plt.close(fig)


def profiles(recs, Ps):
    rows = []
    for rec, P in zip(recs, Ps):
        zn = P['z'] / P['H']
        vol = P['r'] ** 3
        for ph in ('AM', 'SE'):
            m = (np.array(['AM' in n for n in P['name']]) if ph == 'AM' else (P['name'] == 'SE')) & ~P['wall']
            for b in range(N_BINS):
                lo, hi = b / N_BINS, (b + 1) / N_BINS
                mm = m & (zn >= lo) & (zn < hi)
                rows.append({'step': rec['step'], 'phase': ph, 'z_over_H_lo': lo, 'z_over_H_hi': hi, 'n': int(mm.sum()),
                             'mean_vm_MPa': float((vol[mm] * P['vm'][mm]).sum() / vol[mm].sum()) if mm.any() else None})
    return rows


def draw_profile(recs, rows, labels, out_png):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    _style(plt)
    pal = ['#2c7bb6', '#7b3294', '#d7191c', '#1a9641']
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 3.4), sharey=True)
    for j, ph in enumerate(('AM', 'SE')):
        ax = axs[j]
        for k, rec in enumerate(recs):
            rr = [r for r in rows if r['step'] == rec['step'] and r['phase'] == ph and r['mean_vm_MPa']]
            ax.plot([r['mean_vm_MPa'] for r in rr], [(r['z_over_H_lo'] + r['z_over_H_hi']) / 2 for r in rr], '-o', ms=2.5, lw=1.0,
                    color=pal[k % 4], label=f'({chr(97 + k)}) {labels[k]}')
        ax.set_xscale('log')
        ax.set_xlabel(f'Mean σ_VM of {ph} (MPa, volume-weighted)')
        ax.set_ylim(0, 1)
        if j == 0:
            ax.set_ylabel('Height z / plate height')
    axs[1].legend(fontsize=6.5, frameon=False, loc='lower right')
    fig.tight_layout()
    fig.savefig(out_png, dpi=220)
    fig.savefig(str(out_png)[:-4] + '.svg')
    plt.close(fig)


def run(moments, meta_path, out_dir, labels=None, rule='p5p95', vmin=None, vmax=None, pressure_csv=PRESSURE_CSV):
    meta = json.loads(Path(meta_path).read_text(encoding='utf-8'))
    tmap = pls.parse_type_map(meta.get('type_map_resolved') or meta.get('type_map'))
    scale = float(meta['scale'])
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    labels = list(labels) if labels else (list(LABELS4) if len(moments) == 4 else [f'step {s}' for s, _ in moments])
    if len(labels) != len(moments):
        raise ValueError('라벨 수 ≠ 시점 수')
    pres = plate_pressure(pressure_csv)
    recs, Ps = [], []
    for s, d in moments:
        rec, P = moment(int(s), d, tmap, scale)
        rec['label'] = labels[len(recs)]
        rec['time_s'] = int(s) * DT_S
        rec['plate_pressure_MPa'] = pres.get(int(s))
        recs.append(rec)
        Ps.append(P)
    summary = {'tool': 'vm_moments', 'definition': 'Love–Weber 입자 응력 (봉인 calc_love_weber_stress · return_arrays · arrays_vm = 대칭부 VM) '
               '× scale / 1e6 = MPa · 벽 접촉 입자 제외 · 평균 = 부피 가중 · 위 / 아래 1/3 = 판 높이 기준', 'meta': str(meta_path),
               'moments': recs}
    bad = [r['step'] for r, P in zip(recs, Ps) if P is None]
    if bad:
        summary['status'] = f'NOT_DRAWN (LW 상태가 OK 아닌 시점 {bad})'
        (out / 'vm_moments.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')
        return 2, summary
    lo, hi = common_range(Ps, rule, vmin, vmax)
    for P in Ps:
        m = P['vm']
        P['ratio'] = m / float(m.mean()) if m.mean() > 0 else np.zeros_like(m)
    rlo, rhi = common_range(Ps, 'p5p95' if rule != 'minmax' else 'minmax', key='ratio')
    summary['colour_range_MPa'] = {'rule': rule, 'vmin': lo, 'vmax': hi, 'scale': 'log', 'pooled': 'AM 입자 (벽 아님 · σ_VM > 0) 네 시점'}
    summary['colour_range_ratio'] = {'rule': 'p5p95' if rule != 'minmax' else 'minmax', 'vmin': rlo, 'vmax': rhi, 'scale': 'log'}
    draw_moments(recs, Ps, labels, pres, lo, hi, out / 'vm_moments.png')
    draw_moments(recs, Ps, labels, pres, rlo, rhi, out / 'vm_moments_ratio.png', key='ratio',
                 cbar_label='σ_VM / ⟨σ_VM⟩ (mean of all particles at that moment)')
    rows = profiles(recs, Ps)
    draw_profile(recs, rows, labels, out / 'vm_profile.png')
    with open(out / 'vm_profile.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for rec, P in zip(recs, Ps):
        am = np.where(np.array(['AM' in n for n in P['name']]))[0]
        with open(out / f'vm_am_{rec["step"]}.csv', 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['id', 'phase', 'x_um', 'y_um', 'z_um', 'r_um', 'vm_MPa', 'szz_compressive_MPa', 'wall'])
            for i in am:
                w.writerow([int(P['ids'][i]), P['name'][i], f'{P["x"][i]:.4f}', f'{P["y"][i]:.4f}', f'{P["z"][i]:.4f}', f'{P["r"][i]:.4f}',
                            f'{P["vm"][i]:.9g}', f'{P["szz"][i]:.9g}', int(P['wall'][i])])
    summary['status'] = 'OK'
    (out / 'vm_moments.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0, summary


def print_report(summary):
    print(f'상태 {summary.get("status")}')
    for r in summary['moments']:
        am = r.get('AM') or {}
        f = lambda v: '—' if v is None else (f'{v:.3g}')
        print(f'  step {r["step"]:>8}  t {r["time_s"]:.3f} s  판 {f(r.get("plate_pressure_MPa"))} MPa  LW {r["lw_status"][:30]}  '
              f'AM σ_VM 평균 {f(am.get("mean_vm_MPa"))} MPa  위÷아래 {f(am.get("top_over_bottom"))}  (AM {am.get("n")} · 벽 {am.get("n_wall")})')
    cr = summary.get('colour_range_MPa')
    if cr:
        print(f'  색 범위 (공동) {cr["vmin"]:.3g} … {cr["vmax"]:.3g} MPa ({cr["rule"]} · log)')


# ── 시험 (합성 기둥 — 손 계산과 대조) ──────────────────────────────────────────────
def _write_case(d, parts, cons, plate_z, box=1.0):
    d.mkdir(parents=True, exist_ok=True)
    with open(d / 'atoms.csv', 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['id', 'type', 'x', 'y', 'z', 'radius'])
        for p in parts:
            w.writerow(list(p))
    with open(d / 'contacts.csv', 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['id1', 'id2', 'fx', 'fy', 'fz', 'fn_x', 'fn_y', 'fn_z', 'ft_x', 'ft_y', 'ft_z', 'contact_area', 'delta', 'cp_x', 'cp_y', 'cp_z'])
        for c in cons:
            (fx, fy, fz), (cx, cy, cz) = c[2], c[3]
            w.writerow([c[0], c[1], fx, fy, fz, fx, fy, fz, 0.0, 0.0, 0.0, 1e-3, 1e-3, cx, cy, cz])
    (d / 'mesh_info.json').write_text(json.dumps({'plate_z': plate_z}), encoding='utf-8')
    (d / 'input_params.json').write_text(json.dumps({'box_x': box, 'box_y': box}), encoding='utf-8')


def _bed(forces_fn, n_layers=6, r=0.05):
    """세로 기둥 넷 (AM_P 둘 · SE 둘) · 층 k 와 k+1 사이 접촉 힘 F_k = forces_fn(k) (아래 입자가 받는 힘 = (0, 0, −F)) · 바닥 입자는
    바닥에 살짝 묻힘 (벽) · 맨 위 입자는 판에 닿음 (벽)."""
    parts, cons, pid = [], [], 1
    for col, (x, typ) in enumerate(((0.2, 1), (0.4, 1), (0.6, 3), (0.8, 3))):
        zs = [r - 1e-4 + 2 * r * k for k in range(n_layers)]
        ids = list(range(pid, pid + n_layers))
        pid += n_layers
        for i, zz in zip(ids, zs):
            parts.append((i, typ, x, 0.5, zz, r))
        for k in range(n_layers - 1):
            F = forces_fn(k)
            cons.append((ids[k], ids[k + 1], (0.0, 0.0, -F), (x, 0.5, 0.5 * (zs[k] + zs[k + 1]))))
    plate_z = (r - 1e-4 + 2 * r * (n_layers - 1)) + r - 1e-4
    return parts, cons, plate_z


def selftest():
    ok, fail = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
            print(f'  PASS  {name}')
        else:
            fail.append(name)
            print(f'  FAIL  {name}  {extra}')

    r, scale = 0.05, 1000.0
    V = 4.0 / 3.0 * math.pi * r ** 3
    beds = {1000000: lambda k: 1e-6, 2200000: lambda k: 2.0 + 0.5 * k, 3100000: lambda k: 1.0 + 1.0 * k, 3220000: lambda k: 3.0}
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        meta = td / 'meta.json'
        meta.write_text(json.dumps({'type_map_resolved': '1:AM_P,2:AM_S,3:SE', 'scale': scale}), encoding='utf-8')
        mom = []
        for s, fn in beds.items():
            parts, cons, pz = _bed(fn)
            _write_case(td / f'c{s}', parts, cons, pz)
            mom.append((s, td / f'c{s}'))
        rc, S = run(mom, meta, td / 'out')
        chk(f'V1 네 시점 OK · rc 0 ({rc} · {S.get("status")})', rc == 0 and S.get('status') == 'OK')
        files = ['vm_moments.png', 'vm_moments.svg', 'vm_moments_ratio.png', 'vm_profile.png', 'vm_profile.csv', 'vm_moments.json'] + \
                [f'vm_am_{s}.csv' for s in beds]
        chk('V2 출력 파일 (그림 셋 · CSV · JSON)', all((td / 'out' / f).is_file() and (td / 'out' / f).stat().st_size > 0 for f in files))
        # 손 계산 — 층 k (1 ≤ k ≤ n−2) 입자: 아래 접촉 F_{k−1} · 위 접촉 F_k → σ_zz = −r (F_{k−1} + F_k) / V · VM = r (F_{k−1} + F_k) / V
        rows = list(csv.DictReader(open(td / 'out' / 'vm_am_3100000.csv')))
        z_of = lambda k: (r - 1e-4 + 2 * r * k) * scale
        hand = {round(z_of(k), 3): r * (beds[3100000](k - 1) + beds[3100000](k)) / V * scale / 1e6 for k in range(1, 5)}
        got = {round(float(rw['z_um']), 3): float(rw['vm_MPa']) for rw in rows if rw['wall'] == '0'}
        chk(f'V3 σ_VM = 손 계산 r (F_below + F_above) / V × scale / 1e6 (안쪽 층 넷 · 기둥 둘)',
            set(got) == set(hand) and all(math.isclose(got[k], hand[k], rel_tol=1e-8) for k in hand), f'{got} vs {hand}')
        chk('V4 바닥 · 판에 닿은 입자 = 벽 (AM 기둥 둘 × 2)', sum(rw['wall'] == '1' for rw in rows) == 4)
        m = {x['step']: x for x in S['moments']}
        tb = m[3100000]['AM']['top_over_bottom']
        chk(f'V5 위로 갈수록 센 시점 → 위 ÷ 아래 > 1 ({tb:.3g}) · 고른 시점 = 1 ({m[3220000]["AM"]["top_over_bottom"]:.6g})',
            tb > 1.5 and math.isclose(m[3220000]['AM']['top_over_bottom'], 1.0, rel_tol=1e-12))
        cr = S['colour_range_MPa']
        allv = np.array([float(rw['vm_MPa']) for s in beds for rw in csv.DictReader(open(td / 'out' / f'vm_am_{s}.csv')) if rw['wall'] == '0'])
        chk(f'V6 공동 색 범위 = 네 시점 AM (벽 아님) 을 모은 p5–p95 ({cr["vmin"]:.3g} … {cr["vmax"]:.3g})',
            math.isclose(cr['vmin'], float(np.percentile(allv, 5)), rel_tol=1e-6) and math.isclose(cr['vmax'], float(np.percentile(allv, 95)), rel_tol=1e-6))
        chk('V6b 입력 sha256 기록 (atoms · contacts · mesh_info · input_params)',
            all(len(x['inputs_sha256']) == 4 and all(len(h) == 64 for h in x['inputs_sha256'].values()) for x in S['moments']))
        chk('V7 판 압력 = 압축 곡선 CSV 값 (1,000,000 → 0.449 MPa · 3,220,000 → 165.3 MPa)',
            math.isclose(m[1000000]['plate_pressure_MPa'], 0.44918529, rel_tol=1e-6) and math.isclose(m[3220000]['plate_pressure_MPa'], 165.30183, rel_tol=1e-6))
        # 실패 경로 — 접촉점이 입자 밖 → 봉인 LW 가 FAILED → 그림 없음 · rc 2 (값을 지어내지 않는다)
        parts, cons, pz = _bed(beds[3100000])
        c0 = cons[0]
        cons[0] = (c0[0], c0[1], c0[2], (c0[3][0] + 0.3, c0[3][1], c0[3][2]))
        _write_case(td / 'bad', parts, cons, pz)
        rc2, S2 = run([(1000000, td / 'c1000000'), (3100000, td / 'bad')], meta, td / 'out_bad')
        chk(f'V8 LW 실패 시점 → 그림 안 그림 · rc 2 ({rc2} · {S2.get("status", "")[:40]})',
            rc2 == 2 and not (td / 'out_bad' / 'vm_moments.png').exists() and S2['moments'][1]['lw_status'] != 'OK')
        # V10 선호 글꼴 (Arial · Liberation Sans) 이 없는 기계 — 경고 없이 DejaVu Sans 로 (1저자 WSL 10-08: 글자마다 findfont 경고 · 5,140 줄)
        import logging
        global FONTS
        keep = FONTS
        FONTS = ('NoSuchFontA_vm', 'NoSuchFontB_vm')
        logs = []

        class _H(logging.Handler):
            def emit(self, rec):
                logs.append(rec.getMessage())
        h = _H()
        lg = logging.getLogger('matplotlib.font_manager')
        lg.addHandler(h)
        try:
            run(mom, meta, td / 'out_font')
        finally:
            lg.removeHandler(h)
            FONTS = keep
        nf = [m for m in logs if 'not found' in m]
        chk(f'V10 선호 글꼴이 없어도 findfont 경고 0 줄 ({len(nf)})', not nf, (nf[:1] or [''])[0])
        try:
            common_range([], 'fixed', 2.0, 1.0)
            chk('V9 fixed 범위 vmin ≥ vmax 거부', False)
        except ValueError:
            chk('V9 fixed 범위 vmin ≥ vmax 거부', True)
    print(f'\n{ok} PASS · {len(fail)} FAIL')
    return 0 if not fail else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='네 시점 von Mises (Love–Weber) — 공동 색 범위 그림 (읽기 전용)')
    ap.add_argument('--moment', nargs=2, action='append', metavar=('STEP', 'DIR'), help='시점 step 과 파서 결과 폴더 (순서대로 · 여러 번)')
    ap.add_argument('--meta', help='type_map_resolved · scale JSON (같은 침대 — 시점 공통)')
    ap.add_argument('--labels', nargs='+', help='패널 이름 (영문 · 시점 수만큼)')
    ap.add_argument('--range', dest='rule', choices=('p5p95', 'minmax', 'fixed'), default='p5p95')
    ap.add_argument('--vmin', type=float)
    ap.add_argument('--vmax', type=float)
    ap.add_argument('--out', help='출력 폴더')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.moment and a.meta and a.out):
        ap.error('--moment (여러 번) · --meta · --out 이 필요하다 (또는 --selftest)')
    rc, S = run([(int(s), d) for s, d in a.moment], a.meta, a.out, a.labels, a.rule, a.vmin, a.vmax)
    print_report(S)
    print(f'→ {a.out}  rc={rc}')
    return rc


if __name__ == '__main__':
    sys.exit(main())
