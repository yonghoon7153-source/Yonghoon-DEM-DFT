#!/usr/bin/env python3
"""50kg 4차년도 DEM 보고 2쪽 보조 그림 (초안) — 기공도–판 압력 (가압 가지) · 고정 높이 이완 가지 (따로).

    python3 -P docs/50kg/report_y4/figs/make_fig_p2_aux.py --log D3=<D3 log.liggghts> --log D2=<D2 log.liggghts> [--out docs/50kg/report_y4/figs]

- 로그 = 리포 밖 사본 (메인 세션이 따로 반입한다) — 이 스크립트는 글로 읽기만 한다 (실행 · 복사 없음) · sha256 은 meta 에 기록.
- 판 높이 z(step) = 로그의 `PLATE HEIGHT` − press_speed × dt × (step − 압축 시작 step) — press_speed · dt = 덱 실행 줄 · 압축 시작 step =
  PHASE 3 첫 run 의 첫 step · 끝 = PHASE 4 직전 run 의 마지막 step.  끝 mesh 의 z (끝 상태 묶음 · 6 유효숫자) 와 대조 (반올림 폭 안이어야 한다).
- 기공도 ε = 1 − ΣV_구 / (50 × 50 µm² × z) — ΣV_구 = 끝 atom 덤프의 구 부피 합 (입자 수 · 반지름 = 런 내내 같다 · ε_sphere 규약) · 바닥 벽 z = 0.
- 판 압력 = 로그 thermo `pressMPa` × 1000 (덱 P×0.001 규약) — run 마다 첫 줄 (setup 줄) 은 빼고 쓴다 (그 줄의 메시 압력은 기준이 못 된다 ·
  CLAUDE.md 재개 체크리스트 ⑤).  가압 가지 = 판 이동 중 · 판 압력 > 1 MPa (판 접촉 뒤) · 이완 가지 = 판 고정 (PHASE 4) 의 압력–step.
- 자료 없는 침대 (D1 · D0.7) = 그림에 없음 — 상태 글은 덱이 그림 밖에 쓴다.  그림 안 글 = 영어 (보고 원칙 §4).
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import kg50_y4_sources as src  # noqa: E402
import make_figs_p1 as p1  # noqa: E402

#: 크기 순서 = 한 색상 계열 밝음 → 어두움 (SE 입도 = 순서 있는 양 · 주황 = 1쪽 SE 상 색이라 피함)
SIZE_COLORS = {'D0.7': '#9EC5F0', 'D1': '#5A9BE0', 'D2': '#2A78D6', 'D3': '#174A8C'}
FIG_W, FIG_H = 4.30, 2.62
P_CONTACT_MPA = 1.0
_THERMO = re.compile(r'^\s*(\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$')


def parse_log(text, case):
    """로그 글 → (판 시작 높이 · PHASE 3 run 들 · PHASE 4 run 들).  run = [(step, pressMPa_sim)] (setup 줄 뺌)."""
    tag = case.upper()
    src.need(f'====== Simulation Finished! ({tag}:' in text, f'log: {case} 끝 줄이 없다 (다른 침대 로그?)')
    ph = re.findall(r'^====== PLATE HEIGHT: ([0-9.eE+-]+) ======$', text, flags=re.M)
    src.need(len(ph) == 1, f'log {case}: PLATE HEIGHT 출력 줄 {len(ph)} 개')
    lines = text.split('\n')
    i3 = lines.index('====== PHASE 3: COMPRESSION (Speed 0.01) ======')
    i4 = lines.index('====== PHASE 4: RELAXATION ======')
    src.need(i3 < i4, f'log {case}: 단계 순서')

    def runs(seg):
        """run 마다 (setup 줄 step, [(step, pressMPa)] 정규 줄) — setup 줄 = 머리 바로 다음 줄 (압력은 쓰지 않는다)."""
        out, cur, in_run = [], None, False
        for l in seg:
            if l.lstrip().startswith('Step') and 'pressMPa' in l:
                cur, in_run = dict(setup=None, rows=[]), True
                out.append(cur)
                continue
            if l.startswith('Loop time of'):
                in_run = False
                continue
            m = _THERMO.match(l) if in_run else None
            if m:
                if cur['setup'] is None:
                    cur['setup'] = int(m.group(1))
                else:
                    cur['rows'].append((int(m.group(1)), float(m.group(5))))
        return [r for r in out if r['rows']]

    r3 = runs(lines[i3:i4])
    r4 = runs(lines[i4:])
    cp = [float(v) for v in re.findall(r'^Current Pressure: ([0-9.eE+-]+) MPa', '\n'.join(lines[i3:i4]), flags=re.M)]
    return dict(plate_z0_sim=float(ph[0]), runs3=r3, runs4=r4, current_press=cp)


def branches(beds_by_label, logs, common):
    out = {}
    v = common['press_speed_sim']
    dt = common['dt']
    area_um2 = common['box_x_um'] * common['box_y_um']
    for label, path in logs.items():
        b = beds_by_label[label]
        es = b['endstate']
        src.need(es is not None, f'{label}: 끝 상태 묶음이 없다 (V_solid · 끝 mesh 대조 불가)')
        raw = Path(path).read_bytes()
        L = parse_log(raw.decode('utf-8', errors='strict'), b['case'])
        a = es['atoms']
        v_solid = float(np.sum(4.0 / 3.0 * np.pi * (a['r'] * src.LEN_SIM_TO_UM) ** 3))
        r3 = L['runs3']
        s0 = r3[0]['setup']                                   # 압축 시작 = PHASE 3 첫 run 의 시작 step (판이 여기서 움직이기 시작)
        s_end = r3[-1]['rows'][-1][0]                         # 압축 끝 = 마지막 run 의 마지막 step (판 정지)
        n_runs = len(r3)
        cont = all(r3[k]['setup'] == r3[k - 1]['rows'][-1][0] for k in range(1, n_runs))
        src.need(cont and s_end - s0 == 5000 * n_runs, f'{label}: 압축 run 이음 · step 수 {s_end - s0} ≠ 5000 × run {n_runs}')
        src.need(len(L['current_press']) == n_runs and L['current_press'][-1] >= common['target_MPa'] / src.P_SIM_TO_MPA
                 and all(c < common['target_MPa'] / src.P_SIM_TO_MPA for c in L['current_press'][:-1]),
                 f'{label}: Current Pressure 줄 ↔ run 수 · 목표 도달 대조 실패')
        z_end_pred = L['plate_z0_sim'] - v * dt * (s_end - s0)
        src.need(abs(z_end_pred - es['plate_z_sim']) <= 5e-7 * 1.0001, f'{label}: 예측 끝 판 높이 {z_end_pred} ↔ 끝 mesh {es["plate_z_sim"]}')
        r4 = L['runs4']
        src.need(r4 and r4[0]['setup'] == s_end, f'{label}: 이완 run 이 압축 끝 step 에서 시작하지 않는다')
        relax = [p for r in r4 for p in r['rows']]
        src.need(relax and relax[-1][0] == es['step'] and relax[-1][0] - s_end == 100000,
                 f'{label}: 이완 끝 step {relax[-1][0] if relax else None} ↔ 끝 덤프 {es["step"]}')
        load = sorted({st: p for r in r3 for st, p in r['rows']}.items())
        rows_load, rows_relax = [], []
        for st, p_sim in load:
            z_um = (L['plate_z0_sim'] - v * dt * (st - s0)) * src.LEN_SIM_TO_UM
            rows_load.append((st, p_sim * src.P_SIM_TO_MPA, z_um, 100.0 * (1.0 - v_solid / (area_um2 * z_um))))
        z_fix = es['plate_z_um']
        for st, p_sim in relax:
            rows_relax.append((st, p_sim * src.P_SIM_TO_MPA, z_fix, 100.0 * (1.0 - v_solid / (area_um2 * z_fix))))
        out[label] = dict(case=b['case'], log=str(path), log_sha256=hashlib.sha256(raw).hexdigest(), log_bytes=len(raw),
                          plate_z0_um=L['plate_z0_sim'] * src.LEN_SIM_TO_UM, s0=s0, s_end=s_end, n_runs=n_runs,
                          z_end_pred_um=z_end_pred * src.LEN_SIM_TO_UM, z_end_mesh_um=es['plate_z_um'], v_solid_um3=v_solid,
                          load=rows_load, relax=rows_relax, end_step=es['step'])
    return out


def draw(br, out):
    p1.setup_fonts()
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    ax1 = fig.add_axes([0.42 / FIG_W, 0.40 / FIG_H, 1.62 / FIG_W, (FIG_H - 0.62) / FIG_H])
    ax2 = fig.add_axes([2.55 / FIG_W, 0.40 / FIG_H, 1.62 / FIG_W, (FIG_H - 0.62) / FIG_H])
    for lab in sorted(br, key=lambda k: src.BEDS.index(next(b for b in src.BEDS if b['case'] == br[k]['case']))):
        d = br[lab]
        col = SIZE_COLORS[lab]
        L = np.array([(p, e) for _, p, _, e in d['load'] if p > P_CONTACT_MPA])
        ax1.plot(L[:, 0], L[:, 1], color=col, lw=1.4)
        R = np.array([((st - d['s_end']) / 1e3, p) for st, p, _, _ in d['relax']])
        ax2.plot(R[:, 0], R[:, 1], color=col, lw=1.4)
    ax1.set_xlim(0, 320)
    ax1.set_xticks([0, 100, 200, 300])
    ax1.set_xlabel('Plate pressure (MPa)', labelpad=1)
    ax1.set_ylabel('Porosity (%)', labelpad=2)
    ax1.set_title('(a) Loading (plate moving)', fontsize=p1.TITLE_PT, pad=3)
    ax2.set_xlim(0, 100)
    ax2.set_xticks([0, 50, 100])
    ax2.set_xlabel('Steps after plate stop (×10³)', labelpad=1)
    ax2.set_ylabel('Plate pressure (MPa)', labelpad=2)
    ax2.set_title('(b) Fixed-height relaxation', fontsize=p1.TITLE_PT, pad=3)
    for ax in (ax1, ax2):
        ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(4))
    shas = p1.save(fig, out, 'p2_aux_compaction')
    with open(out / 'p2_aux_compaction.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['bed', 'branch', 'step', 'plate_pressure_MPa', 'plate_gap_um', 'porosity_sphere_pct'])
        for lab, d in br.items():
            for name, rows in (('loading', d['load']), ('fixed_height_relaxation', d['relax'])):
                for st, p, z, e in rows:
                    w.writerow([lab, name, st, f'{p:.6f}', f'{z:.6f}', f'{e:.6f}'])
    return shas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--log', action='append', required=True, help='침대=로그 경로 (예: D3=/path/log.liggghts)')
    ap.add_argument('--out', default=str(HERE))
    a = ap.parse_args()
    out = Path(a.out)
    beds, common = src.load_all()
    by_label = {src.bed_label(b): b for b in beds}
    logs = dict(x.split('=', 1) for x in a.log)
    src.need(set(logs) <= set(by_label), f'모르는 침대 {set(logs) - set(by_label)}')
    br = branches(by_label, logs, common)
    shas = draw(br, out)
    meta = dict(generator='docs/50kg/report_y4/figs/make_fig_p2_aux.py', size_in=[FIG_W, FIG_H], dpi=p1.DPI, files=shas,
                p_contact_MPa=P_CONTACT_MPA, colors=SIZE_COLORS,
                beds={lab: {**{k: v for k, v in d.items() if k not in ('load', 'relax', 'log')}, **dict(
                    log_name=Path(d['log']).name, n_load_points=len(d['load']), n_relax_points=len(d['relax']),
                    porosity_fixed_height_pct=round(d['relax'][-1][3], 4), p_relax_end_MPa=round(d['relax'][-1][1], 4),
                    p_load_end_MPa=round(d['load'][-1][1], 4))} for lab, d in br.items()},
                missing=[src.bed_label(b) for b in beds if src.bed_label(b) not in br])
    (out / 'p2_aux_meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for lab, m in meta['beds'].items():
        print(lab, 'log sha256', m['log_sha256'][:12], '· z0', round(m['plate_z0_um'], 3), '· z_end pred/mesh', round(m['z_end_pred_um'], 4),
              round(m['z_end_mesh_um'], 4), '· ε fixed', m['porosity_fixed_height_pct'], '· P relax end', m['p_relax_end_MPa'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
