#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ps_7_3_r45 (이종기술 6 mAh/cm² · P:S 7:3 · AM_P r 4.5 µm) 압밀 곡선 — 시간–두께 · 시간–압력 (Origin CSV · .ogs · 미리보기 PNG/SVG).

    python3 docs/data/ps73_compaction_curve_20261006/make_fig.py

입력 = 이 폴더 raw/ 의 ibb 원본 두 개 (1저자 10-06 밤 · ibb 에서 만든 그대로 · sha256 은 README):
  raw/ps73_logs.tgz   — SLURM 화면 출력 9 개 (r1 … r8) · 덱 9 · 러너 · log.liggghts
  raw/ps73_curve_1.tgz — 판 메시 덤프 post_ps_7_3_r45/mesh_<step>.stl 605 장 (205,000 → 3,225,000 · 5,000 step 간격)
과정: 임시 폴더에 풀고 (경로 검사) `scripts/compaction_curve.py` 로 r1 → r3 → r6 → r7 → r8 을 잇는다 (r2 · r4 · r5 는 쓰지 않는다 — README §2).
산출: curve/ (pressure.csv · plate.csv · curve_summary.json — 임시 경로는 tgz 안 경로로 바꿔 적는다 · step 그대로) · origin/ · previews/.
슬라이드판 (1저자 10-06 밤): origin/ps73_time_pressure_slide.csv · previews/ps73_time_pressure_slide.* — 압축 끝 (판 정지) 까지 원값,
  그 뒤 이완 구간 = 끝 값으로 가는 모식 지수 감쇠 (실선 · 끝 값만 계산값 · README §5).  원값 판은 그대로 둔다.
x 축 = 시뮬레이션 시간 (s) = step × Δt (1저자 10-07 *"물리적인 의미는 없어도 그게 더 직관적이니까 그걸로 바꾸자"* · 앞 판 = step · 10-06 밤) —
  Δt = 1e-6 s 를 덱 9 개 모두에서 확인한다 (다르면 거부) · 축척 덱 (r×1000 · E×0.001) 의 시간이라 실제 압착 시간이 아니다 (README §5) ·
  범위 = 판을 놓은 때 (200,002 step = 0.200002 s) 부터 끝 (3,225,000 step = 3.225 s) · 단계 경계 점선 · 목표 300 MPa 점선 (1저자 비준 · 권고대로).
"""
import csv
import json
import math
import os
import re
import sys
import tarfile
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import compaction_curve as CC     # noqa: E402

LOGS_TGZ, MESH_TGZ = HERE / 'raw' / 'ps73_logs.tgz', HERE / 'raw' / 'ps73_curve_1.tgz'
LOG_DIR = 'home/yonghoon/dem_test/ps45/logs'
#: 궤적 순서 (README §2) — r2 (판 7.18 µm 재부양) · r4 (정착 직후 재시작) · r5 ×2 (옛 판 높이 = 2 µm 재부양) 는 뺀다
KEEP = ['output_ps_7_3_r45_181338.out', 'output_ps_7_3_r45_r3_198258.out', 'output_ps_7_3_r45_r6_198529.out',
        'output_ps_7_3_r45_r7_216115.out', 'output_ps_7_3_r45_r8_220537.out']
DT_S = 1.0e-6               # 덱 timestep (s) — main() 이 덱 9 개 · log.liggghts 에서 확인 (다르면 거부)
X0, X1 = 0.2, 3.25          # s (= step × DT_S) — 판 놓은 때 (200,002 step) ~ 끝 (3,225,000 step)
XLABEL = 'Simulation time (s)'
TARGET_MPA = 300.0
SLIDE_TAU_STEP = 15000      # 슬라이드판 이완 모식의 시간 상수 (step) — 그림용 · 자료에서 정한 값이 아니다 (README §5)

CURVE, ORIGIN, PREV = HERE / 'curve', HERE / 'origin', HERE / 'previews'


def safe_extract(tgz, dest):
    """ibb 원본 — 절대 경로 · '..' · 링크 · 장치 파일이 있으면 거부 (받은 압축은 신뢰하지 않는다)."""
    with tarfile.open(tgz) as t:
        mem = t.getmembers()
        for m in mem:
            if m.name.startswith('/') or '..' in Path(m.name).parts or not (m.isfile() or m.isdir()):
                raise SystemExit(f'⛔ {tgz.name}: 위험한 항목 {m.name!r}')
        t.extractall(dest, members=mem)


def deck_dt_check(run_dir):
    """x 축 시간 = step × DT_S 가 맞는지 — 덱 9 개 (원 덱 · .orig15000 · r2–r8) 의 `variable dt` · `timestep` 과 log.liggghts 의 `timestep` 줄이
    모두 DT_S 여야 한다 (조각마다 Δt 가 다르면 step → 시간이 한 직선이 아니다 → 거부)."""
    decks = sorted(run_dir.glob('input_ps_7_3_r45*.liggghts*'))
    if len(decks) != 9:
        raise SystemExit(f'⛔ Δt 확인: 덱 9 개를 기대했는데 {len(decks)} 개 — {[d.name for d in decks]}')
    for d in decks:
        txt = d.read_text(encoding='utf-8', errors='replace')
        dts = [float(v) for v in re.findall(r'^\s*variable\s+dt\s+equal\s+(\S+)', txt, re.M)]
        ts = re.findall(r'^\s*timestep\s+(\S+)', txt, re.M)
        if dts != [DT_S] or not ts or any(t not in ('${dt}',) and float(t) != DT_S for t in ts):
            raise SystemExit(f'⛔ Δt 확인: {d.name} — variable dt {dts} · timestep {ts} (기대 {DT_S:g} s)')
    log_ts = re.findall(r'^\s*timestep\s+(\S+)', (run_dir / 'log.liggghts').read_text(encoding='utf-8', errors='replace'), re.M)
    log_num = [float(t) for t in log_ts if t != '${dt}']
    if not log_num or any(v != DT_S for v in log_num):
        raise SystemExit(f'⛔ Δt 확인: log.liggghts timestep {log_ts} (기대 {DT_S:g} s)')
    return {'dt_s': DT_S, 'decks_checked': len(decks), 'log_timestep_numeric': len(log_num)}


def main():
    for p in (CURVE, ORIGIN, PREV):
        p.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ps73_') as tmp:
        tmp = Path(tmp)
        safe_extract(LOGS_TGZ, tmp / 'logs')
        safe_extract(MESH_TGZ, tmp / 'mesh')
        dt_info = deck_dt_check(tmp / 'logs' / 'home/yonghoon/dem_test/ps45/ps_7_3_r45')
        segs = [str(tmp / 'logs' / LOG_DIR / n) for n in KEEP]
        mdir = str(tmp / 'mesh' / 'post_ps_7_3_r45')
        summary, prow, zrow = CC.build(segs, mdir)
    if summary['status'] != 'OK':
        raise SystemExit('⛔ compaction_curve REFUSED — ' + ' | '.join(summary['why']))
    for s in summary['segments']:                                        # 임시 경로 → tgz 안 경로 (결정적 산출)
        s['path'] = f'raw/ps73_logs.tgz:{LOG_DIR}/{s["label"]}'
    summary['mesh']['dir'] = 'raw/ps73_curve_1.tgz:post_ps_7_3_r45'
    CC._write_csv(CURVE / 'pressure.csv', prow, ['step', 'phase', 'segment', 'pressure_mpa'])
    CC._write_csv(CURVE / 'plate.csv', zrow, ['step', 'phase', 'plate_z_deck', 'thickness_um'])
    (CURVE / 'curve_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    b = {k: v['step'] for k, v in summary['phase_bounds'].items()}
    px = [(int(r['step']), float(r['pressure_mpa'])) for r in prow if r['pressure_mpa'] != '' and int(r['phase']) >= 2]
    zx = [(int(r['step']), float(r['thickness_um'])) for r in zrow]

    # ── Origin 워크시트 (1 줄 Long Name · 2 줄 Units · 3 줄부터 값 — 10-21 덱 make_figs.py 와 같은 꼴) ──
    def wcsv(name, head, units, rows):
        with open(ORIGIN / f'{name}.csv', 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f, lineterminator='\n')   # LF 고정 (.gitattributes — CSV eol=lf · 저장소 바이트 = SHA256SUMS)
            w.writerow(head)
            w.writerow(units)
            w.writerows(rows)
    wcsv('ps73_time_thickness', ['Simulation time', 'Thickness'], ['s', 'µm'], [(f'{s * DT_S:.6f}', f'{t:.3f}') for s, t in zx])
    wcsv('ps73_time_pressure', ['Simulation time', 'Pressure'], ['s', 'MPa'], [(f'{s * DT_S:.6f}', f'{p:.4f}') for s, p in px])

    AX = ('layer.unit = 3; layer.width = 10; layer.height = 8;\n'
          'layer.x.color = color(64,64,64); layer.x.thickness = 1; layer.x.ticks = 10;\n'
          'layer.x.ticklength = 6; layer.x.tickthickness = 1; layer.x.mticklength = 3; layer.x.mtickthickness = 1;\n'
          'layer.x.label.font = font(Aptos); layer.x.label.pt = 28; layer.x.label.color = color(64,64,64);\n'
          'layer.y.color = color(64,64,64); layer.y.thickness = 1; layer.y.ticks = 10;\n'
          'layer.y.ticklength = 6; layer.y.tickthickness = 1; layer.y.mticklength = 3; layer.y.mtickthickness = 1;\n'
          'layer.y.label.font = font(Aptos); layer.y.label.pt = 28; layer.y.label.color = color(64,64,64);\n'
          'layer.x2.showAxes = 3; layer.x2.color = color(64,64,64); layer.x2.thickness = 1; layer.x2.ticks = 0; layer.x2.showLabels = 0;\n'
          'layer.y2.showAxes = 3; layer.y2.color = color(64,64,64); layer.y2.thickness = 1; layer.y2.ticks = 0; layer.y2.showLabels = 0;\n'
          f'layer.x.from = {X0}; layer.x.to = {X1}; layer.x.inc = 1; layer.x.minor = 1;\n'
          f'page.margincontrol = 1;\nlabel -xb {XLABEL};\n')
    vb = (f'draw -n b3 -l -v {b["3"] * DT_S:.6f}; b3.linetype = 3; b3.color = color(154,160,168);\n'
          f'draw -n b4 -l -v {b["4"] * DT_S:.6f}; b4.linetype = 3; b4.color = color(154,160,168);\n')
    head = ('// {n}.ogs — ps_7_3_r45 압밀 곡선 ({what})\n// 사용: {n}.csv 를 가져온 워크북을 활성으로 두고 Script Window 에 붙여 넣기 → Enter.\n'
            '// 결과: 새 그래프 + BML 서식 · 단계 경계 점선 둘 (압축 시작 · 이완 시작).  축 제목 글꼴 · 단계 이름 글은 GUIDE.md 의 GUI 단계.\n'
            'string bk$ = %H;\n')
    (ORIGIN / 'ps73_time_thickness.ogs').write_text(
        head.format(n='ps73_time_thickness', what='시뮬레이션 시간–두께') +
        'plotxy iy:=[%(bk$)]1!(1,2) plot:=200 ogl:=<new>;\nset %C -c color(79,189,255); set %C -w 1500;\n' + AX +
        'layer.y.from = 108; layer.y.to = 142; layer.y.inc = 10; layer.y.minor = 1;\nlabel -yl Thickness (\\g(m)m);\n' + vb,
        encoding='utf-8')
    (ORIGIN / 'ps73_time_pressure.ogs').write_text(
        head.format(n='ps73_time_pressure', what='시뮬레이션 시간–압력') +
        'plotxy iy:=[%(bk$)]1!(1,2) plot:=200 ogl:=<new>;\nset %C -c color(241,64,64); set %C -w 1500;\n' + AX +
        'layer.y.from = 0; layer.y.to = 330; layer.y.inc = 100; layer.y.minor = 1;\nlabel -yl Pressure (MPa);\n' + vb +
        f'draw -n tgt -l -h {TARGET_MPA:g}; tgt.linetype = 2; tgt.color = color(64,64,64);\n',
        encoding='utf-8')

    # ── 미리보기 (BML 모양 · 이 기계에 Aptos 가 없어 Liberation Sans — Origin 결과로 바꿔 끼운다) ──
    GRAY, RED, SKY, LIGHT = '#404040', '#F14040', '#4FBDFF', '#9AA0A8'
    plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11, 'axes.edgecolor': GRAY, 'axes.labelcolor': GRAY,
                         'xtick.color': GRAY, 'ytick.color': GRAY, 'axes.linewidth': 1.0, 'xtick.direction': 'out',
                         'ytick.direction': 'out', 'xtick.major.size': 5, 'ytick.major.size': 5, 'xtick.minor.size': 2.5,
                         'ytick.minor.size': 2.5, 'xtick.minor.visible': True, 'ytick.minor.visible': True,
                         'axes.labelsize': 12.5, 'svg.hashsalt': 'ps73'})

    def panel(xy, color, ylabel, ylim, ystep, name, target=None, stab_at='top'):
        fig, ax = plt.subplots(figsize=(4.3, 3.35))
        ax.tick_params(top=False, right=False, which='both')
        ax.plot([x * DT_S for x, _ in xy], [y for _, y in xy], '-', color=color, lw=1.6)
        for k in ('3', '4'):
            ax.axvline(b[k] * DT_S, color=LIGHT, lw=0.9, ls=':')
        if target is not None:
            ax.axhline(target, color=GRAY, lw=0.9, ls='--')
            ax.text(b['3'] * DT_S + 0.06, target + 5, 'Target 300 MPa', fontsize=9, color=GRAY, va='bottom')   # 안정화 띠 오른쪽 (글 겹침 방지)
        y_top = ylim[1] - 0.04 * (ylim[1] - ylim[0])
        y_bot = ylim[0] + 0.04 * (ylim[1] - ylim[0])
        ax.text((b['2'] + b['3']) * DT_S / 2, y_top if stab_at == 'top' else y_bot, 'Stabilization', rotation=90, fontsize=8.5,
                color=LIGHT, ha='center', va='top' if stab_at == 'top' else 'bottom')   # 두께 그림은 판 높이 선 아래로
        ax.text((b['3'] + b['4']) * DT_S / 2, y_top, 'Compression', fontsize=9, color=LIGHT, ha='center', va='top')
        ax.text(min((b['4'] * DT_S + X1) / 2, X1 - 0.03), y_top, 'Relaxation', rotation=90, fontsize=8.5, color=LIGHT, ha='center', va='top')
        ax.set_xlim(X0, X1)
        ax.set_ylim(*ylim)
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.xaxis.set_minor_locator(MultipleLocator(0.5))
        ax.yaxis.set_major_locator(MultipleLocator(ystep))
        ax.yaxis.set_minor_locator(MultipleLocator(ystep / 2))
        ax.set_xlabel(XLABEL)
        ax.set_ylabel(ylabel)
        fig.tight_layout(pad=0.4)
        fig.savefig(PREV / f'{name}.png', dpi=300)
        fig.savefig(PREV / f'{name}.svg', metadata={'Date': None})
        plt.close(fig)

    panel(zx, SKY, 'Thickness (µm)', (108, 142), 10, 'ps73_time_thickness', stab_at='bottom')
    panel(px, RED, 'Pressure (MPa)', (0, 330), 100, 'ps73_time_pressure', target=TARGET_MPA)

    # ── 슬라이드판 — 압축 끝 (b['4'] = 판 정지) 까지 원값 · 그 뒤 p(s) = p_end + (p_c − p_end)·exp(−(s − b['4'])/τ) 를 1,000 step 간격으로.
    #    τ = SLIDE_TAU_STEP 은 그림용 (실제 계산은 1,000 step 안에 떨어지고 진동한다) · 끝 값 p_end (런 마지막 줄) 만 계산값.
    comp = [(s, p) for s, p in px if s <= b['4']]
    if not comp or comp[-1][0] != b['4']:
        raise SystemExit('⛔ 슬라이드판: 판 정지 step 의 압력 줄이 없다 — 모식의 출발점을 정할 수 없다')
    p_c, (s_end, p_end) = comp[-1][1], px[-1]
    sch = [(s, p_end + (p_c - p_end) * math.exp(-(s - b['4']) / SLIDE_TAU_STEP)) for s in range(b['4'] + 1000, s_end + 1, 1000)]
    slide = comp + sch
    wcsv('ps73_time_pressure_slide', ['Simulation time', 'Pressure'], ['s', 'MPa'], [(f'{s * DT_S:.6f}', f'{p:.4f}') for s, p in slide])
    panel(slide, RED, 'Pressure (MPa)', (0, 330), 100, 'ps73_time_pressure_slide', target=TARGET_MPA)

    on = {thr: next((s for s, p in px if b['3'] < s and p >= thr), None) for thr in (0.1, 1.0, 10.0, 100.0, 300.0)}
    ph4 = [(s, p) for s, p in px if s > b['4']]
    key = {'x_axis': {'label': XLABEL, 'time_s': 'step × dt_s', **dt_info,
                      'note': 'scaled deck time (r×1000 · E×0.001) — not the real pressing time (README §5)'},
           'phase_bounds': b, 'phase_bounds_s': {k: round(v * DT_S, 6) for k, v in b.items()}, 'thickness_first_um': summary['thickness_first_um'], 'thickness_last_um': summary['thickness_last_um'],
           'max_pressure_mpa': summary['max_pressure_mpa'], 'last_pressure_mpa': summary['last_pressure_mpa'],
           'first_step_pressure_ge_mpa': {f'{k:g}': v for k, v in on.items()},
           'relax_first': ph4[0] if ph4 else None, 'relax_min': min(ph4, key=lambda t: t[1]) if ph4 else None,
           'n_pressure_rows': summary['n_pressure_rows'], 'n_mesh': summary['mesh']['n'], 'n_judge_lines': summary['n_judge_lines'],
           'plate_speed_um_per_1000step': summary['plate_speed_um_per_1000step'], 'splices': summary['splices'],
           'slide_schematic': {'tau_step': SLIDE_TAU_STEP, 'start': [b['4'], p_c], 'end_value_mpa': p_end,
                               'value_at_last_step_mpa': round(sch[-1][1], 4) if sch else None, 'n_points': len(slide),
                               'note': 'relaxation segment is schematic (figure only); only end_value_mpa is computed'}}
    (HERE / 'key_numbers.json').write_text(json.dumps(key, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(key, ensure_ascii=False))


if __name__ == '__main__':
    main()
