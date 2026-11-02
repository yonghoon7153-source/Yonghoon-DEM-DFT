#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""50kg D1 (kg50_d1_b50 · SE D50 1 µm) 압밀 곡선 — 세 패널 왼쪽 열 (두께 · 판 속도 · 판 압력) · Origin CSV · .ogs · 미리보기 PNG/SVG ·
key_numbers_d1_ms.json · 오른쪽 3D 단계 프레임 표 (1저자 11-02 *"이 그림도 50Kg_D1 기준으로 만들면 좋을듯"*).

    python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py             # 산출 (결정적 — 다시 돌려도 같은 바이트)
    python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py --selftest  # 반례 시험 (합성 로그 · 리포 자료 안 읽음)

본보기 = ps73 ms 판 (`docs/data/ps73_compaction_curve_20261006/make_fig_ms.py` · `make_fig_velocity_ms.py` · 그 README §5 · §7 · §8) 의
서식 · 축 · Origin CSV (1 줄 Long Name · 2 줄 Units · C 열 Source).  로그 읽기 = ps73 생성기와 같은 `scripts/compaction_curve.py`
(`parse_log` · `resolve` · `_phase_at` — thermo 블록 · run 마다 첫 줄 (설정 줄) 버림 · 단계 표지 · 판정 줄 · 사본 금지).

입력 (리포 · 읽기만):
  docs/data/kg50_d1_end_20261031/kg50_d1_b50_log.liggghts — 본 런 로그 (덱 명령 되풀이 포함 · 20,001 → 2,785,002)
  docs/data/kg50_d1_end_20261031/README.md — 로그 · 덱 · 끝 덤프 sha256 · 끝 판 높이 기록 (mesh_end 122.596 µm)
  docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts — 리포 덱 (로그 안 덱과 설정이 같은지)
  docs/50kg/report_y4/draft2/data/D1/{metrics_D1.json, curve_D1.csv} — 초안 2 압밀 곡선 (다른 코드로 읽은 값과 대조 · 단계 표 ε_sphere 참고값)
값:
  시간 (ms) = step × dt × 1000 (dt = 로그 안 덱 `variable dt` = 모든 숫자 `timestep`) — 축척 덱의 시간 (실제 압착 시간 아님)
  두께 (µm) = 판 위치 (덱으로 계산 — 메시 덤프는 리포에 없다): 안정화 = `PLATE HEIGHT` 고정 · 압축 = press_speed 등속 하강 ·
             이완 = 고정 → 끝 값을 mesh_end (6 유효숫자) 와 대조 (반올림 반폭 안이어야 한다)
  판 속도 (µm/s) = press_speed (덱 m/s) × 1e6 / r 배율 · 압력 (MPa) = thermo `pressMPa` / P 배율 (Scale 머리 r×1000 · P×0.001)
정착 (Particle packing) 구간 두께 = 원자 위치가 필요한데 리포에 없다 → 그리지 않는다 (README §4 = 필요한 클러스터 파일 · ps73 방법).
"""
import csv
import hashlib
import itertools
import json
import math
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
import compaction_curve as CC  # noqa: E402  ps73 생성기와 같은 로그 읽기 규칙 (사본 금지)

LOG = ROOT / 'docs/data/kg50_d1_end_20261031/kg50_d1_b50_log.liggghts'
D1_README = ROOT / 'docs/data/kg50_d1_end_20261031/README.md'
DECK = ROOT / 'docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts'
METRICS = ROOT / 'docs/50kg/report_y4/draft2/data/D1/metrics_D1.json'
CURVE_D1 = ROOT / 'docs/50kg/report_y4/draft2/data/D1/curve_D1.csv'
#: D1 README §1 표 · §2 표의 기록 — 생성기가 README 글에 같은 글자가 있는지 확인한다 (README 와 상수가 갈리면 멈춘다)
LOG_SHA256 = '6a90f706da68e3d5041ff063d0ffd4f61e9d89a5823f29e0755a23ed679bc1b5'
DECK_SHA256 = '514afdb705613dab876c9c0ff5c1f2fef3fad3e029d71778875c08b89edfde91'
ATOM_END_SHA256 = 'e55bb3f44c138cf824837f9dd17775eaea5cc1148b28a8c1d4c07c57a3aec635'
MESH_END_SHA256 = 'ec99971a2e7f27e1baeedbdab72e6f3c2db52239cc318671142931d56592fe16'
MESH_END_TEXT = '판 높이 122.596 µm (mesh_end)'
#: D1 런 폴더 (리포 기록: docs/data/kg50_decks_20261027_v3_b50/README.md §3 — 삽입 런 `cd $HOME/simulation/kg50_d1_b50` · 끝 묶음 접두 `kg50_d1_b50/`)
RUN_PARENT, RUN_CASE = '$HOME/simulation', 'kg50_d1_b50'
TAR_TAG = 'kg50_d1_stage_frames_20261102'

ORIGIN, PREV = HERE / 'origin', HERE / 'previews'
KEY_JSON = HERE / 'key_numbers_d1_ms.json'
STAGE_CSV = HERE / 'stage_frames_d1.csv'
FIG_NAME = 'd1_ms_compaction_3panel'
CSV_NAMES = {'thickness': 'd1_ms_thickness_plate', 'velocity': 'd1_ms_plate_velocity', 'pressure': 'd1_ms_pressure'}

XLABEL = 'Time (ms)'          # 1저자 슬라이드 축 이름 (ps73 미리보기 = 'Simulation time (ms)' — 한정어는 README §5 · 캡션에)
X0, X1 = 0.0, 2800.0          # ms — 0 (투입) ~ 끝 2,785.002 ms + 여유
STL_HALF_ULP_DECK = 5e-7      # mesh STL 꼭짓점 = 6 유효숫자 (0.122596 덱 m) → 반올림 반폭 5e-7 덱 m = 0.0005 µm
STAGE_P_MPA = 50.0            # 오른쪽 3D 단계 "50 MPa"
SLOPE_REL = 1e-9              # 판 궤적 기울기 자기검사 (상대)
GRAY, LIGHT, RED = '#404040', '#9AA0A8', '#F14040'
COLORS = {'thickness': '#4FBDFF', 'velocity': '#7030A0', 'pressure': '#F14040'}
SRC = {'noplate': 'no plate (0 by definition)', 'thermo': 'measured (thermo pressMPa)',
       'placed': 'plate placed (log PLATE HEIGHT)', 'stab': 'plate fixed (stabilization · deck)',
       'c_start': 'compression start (deck press_speed)', 'comp': 'compression (deck press_speed · computed)',
       'stop': 'plate stop (loop exit)', 'relax': 'plate fixed (relaxation · deck)', 'end': 'end of run (= mesh_end check)'}
_NUM = r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'


# ───────────────────────────── 덱 설정 (로그 안 명령 되풀이 · 또는 덱 글) ─────────────────────────────
def _one(pattern, text, what):
    hits = re.findall(pattern, text, re.M)
    if len(hits) != 1:
        raise ValueError(f'{what}: {len(hits)} 줄 (하나여야 한다)')
    return hits[0]


def deck_settings(text):
    """로그 (LIGGGHTS 머리 · 명령 되풀이 = 변수 풀린 줄 포함) 또는 덱 글 → 설정.  어긋나면 ValueError (fail-closed).
    단위 = `units si` · Scale 머리 `# Scale: r×A, E×B, P×C` (길이 µm/덱 m = 1e6/A · 실제 MPa = 덱 MPa / C) ·
    dt = `variable dt` = 모든 숫자 `timestep` (로그면 풀린 숫자 줄이 있어야 한다) · 판 속도 = `variable press_speed` = 모든
    move/mesh linear z 성분 (옆으로 0) · 압력 면적 = `pressMPa` 식 = 판정 식 `current_press` = 상자 x·y (로그) ·
    `PLATE HEIGHT` = Z_MAX + r_AM_P + plate_margin (로그) · 압축 루프 `run N` · atom · mesh 덤프 간격 · 덤프 폴더."""
    is_log = text.startswith('LIGGGHTS (')
    body = '\n'.join(ln.split('#', 1)[0].rstrip() for ln in text.splitlines())
    units = _one(r'^\s*units\s+(\S+)\s*$', body, 'units')
    if units != 'si':
        raise ValueError(f'units {units} (si 여야 한다 — dt 초 · 길이 덱 m · 압력 Pa)')
    s_r, s_e, s_p = (float(v) for v in _one(rf'^#\s*Scale:\s*r×({_NUM}),\s*E×({_NUM}),\s*P×({_NUM})\s*$', text, 'Scale 머리'))
    if s_r <= 0 or s_p <= 0:
        raise ValueError(f'Scale 배율 r×{s_r} · P×{s_p}')
    dt = float(_one(rf'^\s*variable\s+dt\s+equal\s+({_NUM})\s*$', body, 'variable dt'))
    ts = re.findall(r'^\s*timestep\s+(\S+)\s*$', body, re.M)
    num_ts = [t for t in ts if t != '${dt}']
    if dt <= 0 or not ts or (is_log and not num_ts) or any(not re.fullmatch(_NUM, t) or float(t) != dt for t in num_ts):
        raise ValueError(f'timestep {ts} ≠ variable dt {dt}')
    speed = float(_one(rf'^\s*variable\s+press_speed\s+equal\s+({_NUM})\s*$', body, 'variable press_speed'))
    mv = re.findall(r'^\s*fix\s+\S+\s+\S+\s+move/mesh\s+mesh\s+\S+\s+linear\s+(\S+)\s+(\S+)\s+(\S+)\s*$', body, re.M)
    if not mv or (is_log and all(vz == '-${press_speed}' for _, _, vz in mv)):
        raise ValueError(f'move/mesh linear 줄 {mv} (로그면 풀린 숫자 줄이 있어야 한다)')
    speeds = set()
    for vx, vy, vz in mv:
        if float(vx) != 0.0 or float(vy) != 0.0:
            raise ValueError(f'판이 옆으로 움직인다: {vx} {vy}')
        speeds.add(speed if vz == '-${press_speed}' else -float(vz))
    if speeds != {speed} or speed <= 0:
        raise ValueError(f'판 속도 {sorted(speeds)} ≠ press_speed {speed}')
    target = float(_one(rf'^\s*variable\s+target_press\s+equal\s+({_NUM})\s*$', body, 'variable target_press'))
    area = float(_one(rf'^\s*variable\s+pressMPa\s+equal\s+abs\(f_top_mesh\[3\]\)/({_NUM})/1000000\s*$', body, 'pressMPa 식'))
    judge_areas = {float(a) for a in re.findall(
        rf'^\s*variable\s+current_press\s+equal\s+"abs\(f_top_mesh\[3\]\)\s*/\s*({_NUM})\s*/\s*1000000"\s*$', body, re.M)}
    if judge_areas != {area}:
        raise ValueError(f'판정 식 면적 {sorted(judge_areas)} ≠ pressMPa 면적 {area}')
    out = {'units': units, 'scale_r': s_r, 'scale_E': s_e, 'scale_P': s_p, 'um_per_deck_m': 1e6 / s_r, 'mpa_per_deck_mpa': 1.0 / s_p,
           'dt_s': dt, 'press_speed_deck_m_s': speed, 'target_deck': target, 'target_mpa': target / s_p, 'area_deck_m2': area,
           'r_am_p_deck': float(_one(rf'^\s*variable\s+r_AM_P\s+equal\s+({_NUM})\s*$', body, 'variable r_AM_P')),
           'plate_margin_deck': float(_one(rf'^\s*variable\s+plate_margin\s+equal\s+({_NUM})\s*$', body, 'variable plate_margin'))}
    if is_log:                                       # read_restart 출력 · 판 높이 출력 = 로그에만 (덱 글에는 region · print 명령)
        x0, y0, _, x1, y1, _ = (float(v) for v in _one(
            rf'^\s*orthogonal box = \(({_NUM}) ({_NUM}) ({_NUM})\) to \(({_NUM}) ({_NUM}) ({_NUM})\)\s*$', body, 'orthogonal box'))
        if abs((x1 - x0) * (y1 - y0) - area) > 1e-12 * max(1.0, area):
            raise ValueError(f'상자 x·y 면적 {(x1 - x0) * (y1 - y0)} ≠ pressMPa 면적 {area}')
        zmax = float(_one(rf'^\s*=+\s*Z_MAX \(center\):\s*({_NUM})\s*=+\s*$', body, 'Z_MAX 출력'))
        plate = float(_one(rf'^\s*=+\s*PLATE HEIGHT:\s*({_NUM})\s*=+\s*$', body, 'PLATE HEIGHT 출력'))
        if abs(plate - (zmax + out['r_am_p_deck'] + out['plate_margin_deck'])) > 1e-12:
            raise ValueError(f'PLATE HEIGHT {plate} ≠ Z_MAX {zmax} + r_AM_P + plate_margin')
        out.update(box_xy_deck=[x0, x1, y0, y1], zmax_center_deck=zmax, plate_z0_deck=plate)
    out['loop_run_steps'] = int(_one(r'^\s*label\s+loop_press\s*\n\s*run\s+(\d+)\s*$', body, '압축 루프 run'))
    ad = re.findall(r'^\s*dump\s+dmp_atom\s+all\s+custom\s+(\d+)\s+(\S+)/atom_\*\.liggghts\b', body, re.M)
    md = re.findall(r'^\s*dump\s+dmp_mesh\s+all\s+mesh/stl\s+(\d+)\s+(\S+)/mesh_\*\.stl\b', body, re.M)
    if len(ad) != 1 or len(md) != 1 or ad[0][1] != md[0][1]:
        raise ValueError(f'atom · mesh 덤프 줄 {ad} · {md}')
    if re.search(r'^\s*undump\s+dmp_(atom|mesh)\s*$', body, re.M):
        raise ValueError('undump dmp_atom/dmp_mesh — 덤프가 끝까지 이어진다는 가정이 깨진다')
    out.update(atom_dump_every=int(ad[0][0]), mesh_dump_every=int(md[0][0]), post_dir=ad[0][1])
    return out


# ───────────────────────────── thermo 곡선 (compaction_curve 규칙) ─────────────────────────────
def read_curve(log_path, target_deck, loop_run_steps):
    """로그 → 행 (설정 줄 뺌 · 단계) · 단계 경계 · 판정 줄 · KE 참고 (설정 줄 포함 · 처음 것).  어긋나면 ValueError.
    C1 압력 열 · 유한 · C4 판정 줄 = 같은 step thermo · 목표 = 덱 하나 · 마지막만 목표 이상 · PHASE 4 = 루프 탈출 · C6 step 엄격 증가 ·
    압축 run 이 loop_run_steps 마다 빈틈없이 이어진다 · read_restart 파일 step = 첫 thermo step (하나의 런 조각)."""
    seg = CC.resolve(CC.parse_log(str(log_path)))
    if not seg['blocks']:
        raise ValueError('thermo 블록이 없다')
    prob, bounds = [], {}
    for step, num, name in seg['marks']:
        if step is None or str(num) in bounds:
            prob.append(f'PHASE {num} 표지 (step {step}) 가 풀리지 않거나 둘')
        else:
            bounds[str(num)] = {'step': step, 'name': name}
    if sorted(bounds) != ['1', '2', '3', '4']:
        raise ValueError(f'단계 표지 1–4 가 하나씩이 아니다: {sorted(bounds)} · {prob}')
    if not bounds['1']['step'] < bounds['2']['step'] < bounds['3']['step'] < bounds['4']['step']:
        raise ValueError(f'단계 경계 순서 {bounds}')
    for b in seg['blocks']:
        if len(b['cols']) < 2 or b['cols'][1] != 'Atoms':
            prob.append(f'thermo 머리 {b["cols"]} — 둘째 열이 Atoms 가 아니다')
    rows, ke = [], {}
    for b in seg['blocks']:
        kc = b['cols'].index('KinEng') if 'KinEng' in b['cols'] else None
        for i, (step, vals) in enumerate(b['rows']):
            if kc is not None:
                ke.setdefault(step, (int(vals[1]), vals[kc]))
            if i == 0:
                continue                                   # 설정 줄 (run 마다 첫 줄) 버림 — compaction_curve 와 같은 규칙
            rows.append({'step': step, 'atoms': int(vals[1]), 'short': len(b['rows']) <= CC.SHORT_BLOCK_ROWS,
                         'p_deck': vals[b['pcol']] if b['pcol'] is not None else None})
    for r in rows:
        r['phase'] = CC._phase_at(bounds, r['step'])
    st = [r['step'] for r in rows]
    if any(s2 <= s1 for s1, s2 in zip(st, st[1:])):
        prob.append('C6 step 이 엄격히 증가하지 않는다')
    nopc = [r['step'] for r in rows if r['phase'] >= 2 and r['p_deck'] is None and not r['short']]
    if nopc:
        prob.append(f'C1 단계 ≥ 2 thermo 에 압력 열이 없다 (step {nopc[0]} 외 {len(nopc) - 1})')
    bad = [r['step'] for r in rows if r['p_deck'] is not None and not math.isfinite(r['p_deck'])]
    if bad:
        prob.append(f'C1 비유한 압력 {len(bad)} 줄 (첫 step {bad[0]})')
    b3, b4 = bounds['3']['step'], bounds['4']['step']
    judges = []
    for step, x, t, blk in seg['judges']:
        p = next((v[blk['pcol']] for s, v in blk['rows'] if s == step), None) if blk and blk['pcol'] is not None else None
        if step is None or x is None or t is None or p is None or not (math.isfinite(x) and math.isfinite(p)):
            prob.append(f'C4 판정 줄 (step {step}) 을 thermo 와 대조할 수 없다')
        elif abs(x - p) > 1e-12 + CC.JUDGE_REL * max(abs(x), abs(p)):
            prob.append(f'C4 판정 줄 {x!r} ≠ thermo {p!r} (step {step})')
        judges.append((step, x, t))
    if not judges:
        prob.append('C4 판정 줄이 없다')
    else:
        if {t for _, _, t in judges} != {target_deck}:
            prob.append(f'C4 판정 목표 {sorted({str(t) for _, _, t in judges})} ≠ 덱 target_press {target_deck}')
        if judges[-1][1] is None or judges[-1][1] < target_deck or any(x is None or x >= target_deck for _, x, _ in judges[:-1]):
            prob.append('C4 마지막 판정 줄만 목표 이상이어야 한다 (루프 탈출 규칙)')
        if judges[-1][0] != b4:
            prob.append(f'C4 PHASE 4 표지 step {b4} ≠ 루프 탈출 판정 줄 step {judges[-1][0]}')
        want = list(range(b3 + loop_run_steps, b4 + 1, loop_run_steps))
        if [s for s, _, _ in judges] != want or (b4 - b3) % loop_run_steps:
            prob.append(f'압축 run 이 {loop_run_steps} step 씩 이어지지 않는다 (판정 줄 {len(judges)} · 기대 {len(want)})')
    rs = seg['restarts']
    d = re.findall(r'(\d+)', Path(rs[0]).name) if rs else []
    if len(rs) != 1 or not d or int(d[-1]) != seg['first']:
        prob.append(f'read_restart {rs} 의 step ≠ 첫 thermo step {seg["first"]}')
    if prob:
        raise ValueError(' | '.join(prob))
    return {'rows': rows, 'bounds': bounds, 'judges': judges, 'ke': ke, 'first_step': seg['first'], 'last_step': seg['last'],
            'read_restart': rs[0], 'n_blocks': len(seg['blocks'])}


# ───────────────────────────── 판 궤적 · 속도 · 압력 ─────────────────────────────
def plate_model(b2, b3, b4, end, z0_deck, speed, dt):
    """판 높이 (덱 m) 함수 — [b2, b3] 고정 · (b3, b4] 등속 하강 · (b4, end] 고정.  판 놓기 전 · 끝 뒤 step = ValueError."""
    if not (b2 < b3 < b4 < end):
        raise ValueError(f'단계 경계 순서 {b2} {b3} {b4} {end}')

    def z(step):
        if step < b2 or step > end:
            raise ValueError(f'step {step} 은 판이 있는 구간 [{b2}, {end}] 밖')
        return z0_deck - speed * dt * (min(max(step, b3), b4) - b3)
    return z


def check_plate_end(z_end_deck, mesh_end_um, um_per_deck_m, half_ulp_deck=STL_HALF_ULP_DECK):
    """계산한 끝 판 높이 ↔ mesh_end (6 유효숫자) — (잔차 µm, 허용 µm).  반올림 반폭 밖이면 ValueError."""
    res_um = z_end_deck * um_per_deck_m - mesh_end_um
    tol_um = half_ulp_deck * um_per_deck_m * 1.0001
    if not abs(res_um) <= tol_um:
        raise ValueError(f'계산 끝 판 높이 {z_end_deck * um_per_deck_m:.6f} µm ≠ mesh_end {mesh_end_um} µm (잔차 {res_um:+.6f} > ±{tol_um:.6f})')
    return res_um, tol_um


def thickness_series(zfn, bnd, every, ms_per_step, um_per_deck_m):
    """판 위치 (ms, µm, 출처) — 메시 덤프 step (every 마다 · 클러스터 mesh_<step>.stl 과 같은 자리) + 단계 모서리 넷."""
    b2, b3, b4, end = bnd
    corner = {b2: SRC['placed'], b3: SRC['c_start'], b4: SRC['stop'], end: SRC['end']}
    grid = set(range((b2 // every + 1) * every, end + 1, every)) | set(corner)

    def src(s):
        if s in corner:
            return corner[s]
        return SRC['stab'] if s < b3 else (SRC['comp'] if s < b4 else SRC['relax'])
    return [(s * ms_per_step, zfn(s) * um_per_deck_m, src(s)) for s in sorted(grid)]


def velocity_series(bnd, v_um_s, ms_per_step):
    """계단 선 7 점 (ms, µm/s, 출처) — 판 없음 0 · 판 놓음 · 압축 시작에서 0 → v · 판 정지에서 v → 0 · 런 끝."""
    b2, b3, b4, end = (s * ms_per_step for s in bnd)
    return [(0.0, 0.0, SRC['noplate']), (b2, 0.0, SRC['placed']), (b3, 0.0, SRC['stab']), (b3, v_um_s, SRC['c_start']),
            (b4, v_um_s, SRC['stop']), (b4, 0.0, SRC['relax']), (end, 0.0, SRC['end'])]


def pressure_series(rows, mpa_per_deck, ms_per_step):
    """(step, MPa) 원값 + (ms, MPa, 출처) 그림 점 — (0 ms, 0 MPa, 판 없음) 하나 + 단계 ≥ 2 thermo 원값.
    판을 놓은 뒤 첫 압력은 0 이어야 한다 (판은 맨 위 입자 위 틈을 두고 놓인다 — 아니면 거부)."""
    px = [(r['step'], r['p_deck'] * mpa_per_deck) for r in rows if r['phase'] >= 2 and r['p_deck'] is not None]
    if not px or px[0][1] != 0.0:
        raise ValueError(f'판을 놓은 뒤 첫 압력이 0 이 아니다: {px[:1]}')
    return px, [(0.0, 0.0, SRC['noplate'])] + [(s * ms_per_step, p, SRC['thermo']) for s, p in px]


# ───────────────────────────── 3D 단계 프레임 ─────────────────────────────
def dump_steps(b3, end, every):
    """압축 시작 (b3) 뒤 atom 덤프 step — every 의 배수 (설정 줄 step 이 배수가 아니면 그 자리에는 안 쓴다) + 끝 덤프 (atom_end · 끝 step)."""
    return list(range((b3 // every + 1) * every, end + 1, every)) + ([end] if end % every else [])


def stage_table(px, bounds, dumps, end, zfn, um_per_deck_m, atoms_at, ms_per_step, p_stage=STAGE_P_MPA):
    """오른쪽 3D 네 단계 → 사건 step · 가장 가까운 atom 덤프 (같은 거리면 뒤) · 반대쪽 덤프 · 사건과 같은 단계의 가장 가까운 덤프 (권고).
    사건: Initial compression = 압축 시작 (PHASE 3 경계) · 50 MPa = 압축 중 압력이 처음 p_stage 이상인 thermo 줄 · 300 MPa = 판 정지
    (PHASE 4 경계 = 루프 탈출) · After relaxation = 런 끝.  ValueError = 압축 중 p_stage 에 닿지 않음."""
    b3, b4 = bounds['3']['step'], bounds['4']['step']
    pmap = dict(px)
    c50 = next((s for s, p in px if b3 < s <= b4 and p >= p_stage), None)
    if c50 is None:
        raise ValueError(f'압축 중 {p_stage:g} MPa 에 닿은 thermo 줄이 없다')
    events = [('initial_compression', 'Initial compression', b3, 3), ('p50', f'{p_stage:g} MPa', c50, 3),
              ('p300_stop', '300 MPa (plate stop)', b4, 3), ('after_relaxation', 'After relaxation', end, 4)]

    def info(s):
        return {'step': s, 'ms': s * ms_per_step, 'phase': CC._phase_at(bounds, s), 'pressure_mpa': pmap.get(s),
                'plate_um': zfn(s) * um_per_deck_m, 'atoms': atoms_at.get(s)}
    out = []
    for key, label, ev, ev_phase in events:
        near = min(dumps, key=lambda d: (abs(d - ev), -d))
        other = [d for d in dumps if (d - ev) * (near - ev) < 0]
        other = min(other, key=lambda d: abs(d - ev)) if other else None
        same = [d for d in dumps if CC._phase_at(bounds, d) == ev_phase]
        rec = min(same, key=lambda d: (abs(d - ev), -d)) if same else None
        out.append({'stage': key, 'label': label, 'event': info(ev), 'event_phase': ev_phase,
                    'nearest': dict(info(near), delta_steps=near - ev),
                    'other_side': None if other is None else dict(info(other), delta_steps=other - ev),
                    'recommended': None if rec is None else dict(info(rec), delta_steps=rec - ev),
                    'nearest_is_same_phase': CC._phase_at(bounds, near) == ev_phase})
    return out


def dump_names(step, end, post_dir):
    if step == end:
        return f'{post_dir}/atom_end_{end}.liggghts', f'{post_dir}/mesh_end_{end}.stl'
    return f'{post_dir}/atom_{step}.liggghts', f'{post_dir}/mesh_{step}.stl'


def cluster_command(steps, end, post_dir, atoms_at, parent=RUN_PARENT, case=RUN_CASE, tag=TAR_TAG):
    """1저자가 클러스터에서 붙여 넣을 명령 (`bash -s` · 오류면 그 자리에서 멈춤 — 로그인 셸은 닫히지 않는다 · 주소 · 포트 없음).
    ① 같은 런인지 = 끝 묶음 atom_end · mesh_end sha256 (리포 기록) ② atom 덤프마다 머리 TIMESTEP · 원자 수 = 이 로그의 thermo ③ 크기 ·
    sha256 목록 + tgz (홈 폴더에 씀 · 런 폴더는 읽기만 · 묶음 안 경로 = `<case>/post_…/…` — 끝 묶음과 같은 꼴)."""
    files = [f'{case}/{f}' for s in steps for f in dump_names(s, end, post_dir)]
    a_end, m_end = (f'{case}/{f}' for f in dump_names(end, end, post_dir))
    chk = '\n'.join(f'check {case}/{dump_names(s, end, post_dir)[0]} {s} {atoms_at[s]}' for s in steps)
    return ("bash -s <<'EOF'\nset -euo pipefail\n"
            f'cd "{parent}"   # D1 런 폴더 = {parent}/{case} (리포 기록: docs/data/kg50_decks_20261027_v3_b50/README.md §3)\n'
            f'printf "%s  %s\\n" {ATOM_END_SHA256} {a_end} {MESH_END_SHA256} {m_end} | sha256sum -c -   # 같은 런 (끝 묶음 기록)\n'
            'check() { t=$(sed -n 2p "$1"); n=$(sed -n 4p "$1"); [ "$t" = "$2" ] && [ "$n" = "$3" ] || '
            '{ echo "STOP $1: TIMESTEP $t atoms $n (expected $2 $3)"; exit 1; }; }\n'
            f'{chk}\n'
            f'F="{" ".join(files)}"\n'
            'ls -l $F\n'
            f'sha256sum $F > "$HOME/{tag}.sha256"\n'
            f'tar czf "$HOME/{tag}.tgz" $F\n'
            f'sha256sum "$HOME/{tag}.tgz" "$HOME/{tag}.sha256"\n'
            'EOF')


# ───────────────────────────── 대조 (초안 2) ─────────────────────────────
def crosscheck_draft2(metrics, curve_rows, ours):
    """초안 2 (make_fig_p2_aux.branches 경로) ↔ 이 생성기 — 같은 로그를 다른 코드로 읽은 값이 같아야 한다.  (문제 목록, 통계)."""
    prob, c = [], metrics.get('compaction', {})
    pairs = [('compress_start_step', ours['b3']), ('stop_step', ours['b4']), ('n_compress_runs', ours['n_runs']),
             ('plate_z0_um', ours['z0_um']), ('z_end_pred_um', ours['z_end_um']), ('z_end_mesh_um', ours['mesh_end_um']),
             ('p_t0minus_MPa', ours['p_stop']), ('p_relax_first_MPa', ours['p_relax_first']), ('p_end_MPa', ours['p_end']),
             ('n_load_rows', ours['n_load']), ('n_relax_rows', ours['n_relax'])]
    for k, v in pairs:
        if k not in c or not abs(float(c[k]) - float(v)) <= 1e-9 * max(1.0, abs(float(v))):
            prob.append(f'metrics {k} {c.get(k)} ≠ {v}')
    pz = dict(ours['px'])
    dz = dp = 0.0
    n = 0
    for r in curve_rows:
        s = int(r['step'])
        if s not in pz:
            prob.append(f'curve_D1 step {s} 이 이 곡선에 없다')
            continue
        n += 1
        d_p = abs(float(r['plate_pressure_MPa']) - pz[s])
        d_z = abs(float(r['plate_gap_um']) - ours['zfn_um'](s)) if r['branch'] == 'loading' else 0.0
        if not (math.isfinite(d_p) and math.isfinite(d_z)):          # max(0.0, nan) = 0.0 — NaN 이 조용히 사라지지 않게 줄마다 본다
            prob.append(f'curve_D1 step {s} 비유한 값')
            continue
        dp, dz = max(dp, d_p), max(dz, d_z)
    if n != ours['n_load'] + ours['n_relax']:
        prob.append(f'curve_D1 행 {n} ≠ 압축 + 이완 {ours["n_load"] + ours["n_relax"]}')
    if not (dz <= 1e-6 and dp <= 1e-6):
        prob.append(f'curve_D1 판 높이 최대 차 {dz:.3g} µm · 압력 최대 차 {dp:.3g} MPa')
    return prob, {'n_rows_compared': n, 'max_abs_plate_um': dz, 'max_abs_pressure_mpa': dp}


# ───────────────────────────── 산출 ─────────────────────────────
def write_origin_csv(path, head, units, rows):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, lineterminator='\n')    # LF 고정 (.gitattributes)
        w.writerow(head)
        w.writerow(units)
        w.writerows(rows)


def ogs_text(name, what, color, y_from, y_to, y_inc, ylabel, bounds_ms, target=None):
    """ps73 .ogs 와 같은 BML 서식 (바깥 틱 · 위/오른쪽 축선 · #404040 · 10 × 8 cm · Aptos 28 pt) — 단계 경계 점선 셋."""
    ax = ('layer.unit = 3; layer.width = 10; layer.height = 8;\n'
          'layer.x.color = color(64,64,64); layer.x.thickness = 1; layer.x.ticks = 10;\n'
          'layer.x.ticklength = 6; layer.x.tickthickness = 1; layer.x.mticklength = 3; layer.x.mtickthickness = 1;\n'
          'layer.x.label.font = font(Aptos); layer.x.label.pt = 28; layer.x.label.color = color(64,64,64);\n'
          'layer.y.color = color(64,64,64); layer.y.thickness = 1; layer.y.ticks = 10;\n'
          'layer.y.ticklength = 6; layer.y.tickthickness = 1; layer.y.mticklength = 3; layer.y.mtickthickness = 1;\n'
          'layer.y.label.font = font(Aptos); layer.y.label.pt = 28; layer.y.label.color = color(64,64,64);\n'
          'layer.x2.showAxes = 3; layer.x2.color = color(64,64,64); layer.x2.thickness = 1; layer.x2.ticks = 0; layer.x2.showLabels = 0;\n'
          'layer.y2.showAxes = 3; layer.y2.color = color(64,64,64); layer.y2.thickness = 1; layer.y2.ticks = 0; layer.y2.showLabels = 0;\n'
          f'layer.x.from = {X0:g}; layer.x.to = {X1:g}; layer.x.inc = 1000; layer.x.minor = 1;\n'
          f'page.margincontrol = 1;\nlabel -xb {XLABEL};\n')
    vb = ''.join(f'draw -n b{i} -l -v {t:.3f}; b{i}.linetype = 3; b{i}.color = color(154,160,168);\n'
                 for i, t in enumerate(bounds_ms, start=2))
    tgt = f'draw -n tgt -l -h {target:g}; tgt.linetype = 2; tgt.color = color(64,64,64);\n' if target is not None else ''
    marks = ' · '.join(f'{t:.3f}' for t in bounds_ms)
    return (f'// {name}.ogs — 50kg D1 (kg50_d1_b50 · SE D50 1 µm) 압밀 곡선 ({what})\n'
            f'// 사용: {name}.csv 를 가져온 워크북을 활성으로 두고 Script Window 에 붙여 넣기 → Enter.\n'
            f'// 결과: 새 그래프 + BML 서식 · 단계 경계 점선 셋 ({marks} ms = 판 놓음 · 압축 시작 · 판 정지).  C 열 (Source) 은 그리지 않는다.\n'
            'string bk$ = %H;\n'
            'plotxy iy:=[%(bk$)]1!(1,2) plot:=200 ogl:=<new>;\n'
            f'set %C -c color({color}); set %C -w 1500;\n' + ax +
            f'layer.y.from = {y_from:g}; layer.y.to = {y_to:g}; layer.y.inc = {y_inc:g}; layer.y.minor = 1;\nlabel -yl {ylabel};\n' + vb + tgt)


def draw_preview(tser, vser, pser, bounds_ms, target_mpa, arrows, stem):
    """세 패널 왼쪽 열 미리보기 (ps73 서식 · 이 기계에 Aptos 가 없어 Liberation Sans — Origin 결과로 바꿔 끼운다).
    arrows = [(x, y, dx_pt, dy_pt)] 두께 패널의 작은 빨간 화살표 (자료가 있는 점만 가리킨다)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter, MultipleLocator
    plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11, 'axes.edgecolor': GRAY, 'axes.labelcolor': GRAY,
                         'xtick.color': GRAY, 'ytick.color': GRAY, 'axes.linewidth': 1.0, 'xtick.direction': 'out',
                         'ytick.direction': 'out', 'xtick.major.size': 5, 'ytick.major.size': 5, 'xtick.minor.size': 2.5,
                         'ytick.minor.size': 2.5, 'xtick.minor.visible': True, 'ytick.minor.visible': True,
                         'axes.labelsize': 12, 'svg.hashsalt': 'd1ms', 'mathtext.fontset': 'custom',   # s⁻¹ (U+207B 없는 글꼴)
                         'mathtext.rm': 'Liberation Sans', 'mathtext.it': 'Liberation Sans:italic', 'mathtext.bf': 'Liberation Sans:bold',
                         'mathtext.sf': 'Liberation Sans', 'mathtext.cal': 'Liberation Sans', 'mathtext.tt': 'Liberation Mono'})
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(4.3, 7.2))
    b2, b3, b4 = bounds_ms
    spec = [(tser, 'thickness', 'Thickness (µm)', (115, 150), 10),
            (vser, 'velocity', r'Plate velocity (µm s$^{-1}$)', (0, 15), 5),
            (pser, 'pressure', 'Measured pressure (MPa)', (0, 330), 100)]
    for ax, (ser, key, ylabel, ylim, ystep) in zip(axs, spec):
        ax.tick_params(top=False, right=False, which='both')
        ax.plot([t for t, _, _ in ser], [y for _, y, _ in ser], '-', color=COLORS[key], lw=1.6)
        for t in bounds_ms:
            ax.axvline(t, color=LIGHT, lw=0.9, ls=':')
        ax.set_ylim(*ylim)
        ax.yaxis.set_major_locator(MultipleLocator(ystep))
        ax.yaxis.set_minor_locator(MultipleLocator(ystep / 2))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _p: '0' if abs(y) < 1e-12 else f'{y:g}'))   # 보고 원칙 "0.0 → 0"
        ax.set_ylabel(ylabel)
    ax = axs[0]                                           # 단계 이름 · 화살표 = 두께 패널만
    lo, hi = ax.get_ylim()
    y_top, y_bot = hi - 0.04 * (hi - lo), lo + 0.04 * (hi - lo)
    ax.text(b2 / 2, y_top, 'Particle packing', rotation=90, fontsize=8.5, color=LIGHT, ha='center', va='top')
    ax.text((b2 + b3) / 2, y_bot, 'Stabilization', rotation=90, fontsize=8.5, color=LIGHT, ha='center', va='bottom')  # 판 높이 선 아래
    ax.text((b3 + b4) / 2, y_top, 'Compression', fontsize=9, color=LIGHT, ha='center', va='top')
    ax.text(min((b4 + X1) / 2, X1 - 30), y_top, 'Relaxation', rotation=90, fontsize=8.5, color=LIGHT, ha='center', va='top')
    for x, y, dx, dy in arrows:
        ax.annotate('', xy=(x, y), xytext=(dx, dy), textcoords='offset points',
                    arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.2, shrinkA=0, shrinkB=1.5, mutation_scale=8))
    pa = axs[2]
    pa.axhline(target_mpa, color=GRAY, lw=0.9, ls='--')
    pa.text(b3 + 60, target_mpa + 5, f'Target {target_mpa:g} MPa', fontsize=9, color=GRAY, va='bottom')
    axs[-1].set_xlim(X0, X1)
    axs[-1].xaxis.set_major_locator(MultipleLocator(1000))
    axs[-1].xaxis.set_minor_locator(MultipleLocator(500))
    axs[-1].set_xlabel(XLABEL)
    fig.align_ylabels(axs)
    fig.tight_layout(pad=0.4, h_pad=0.6)
    fig.savefig(PREV / f'{stem}.png', dpi=300)
    fig.savefig(PREV / f'{stem}.svg', metadata={'Date': None})
    plt.close(fig)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rel(p):
    return Path(p).resolve().relative_to(ROOT).as_posix()


def main():
    if sha256_file(LOG) != LOG_SHA256 or sha256_file(DECK) != DECK_SHA256:
        raise SystemExit(f'⛔ 로그 · 리포 덱 sha256 ≠ D1 README 기록 ({rel(LOG)} · {rel(DECK)})')
    readme = D1_README.read_text(encoding='utf-8')
    if not all(x in readme for x in (LOG_SHA256, DECK_SHA256, ATOM_END_SHA256, MESH_END_SHA256, MESH_END_TEXT)):
        raise SystemExit('⛔ D1 README 기록 (로그 · 덱 · atom_end · mesh_end sha256 · 끝 판 높이) 이 이 생성기의 상수와 다르다')
    try:
        dk = deck_settings(LOG.read_text(encoding='utf-8'))
        repo_dk = deck_settings(DECK.read_text(encoding='utf-8'))
        same = ('units', 'scale_r', 'scale_E', 'scale_P', 'dt_s', 'press_speed_deck_m_s', 'target_deck', 'area_deck_m2', 'r_am_p_deck',
                'plate_margin_deck', 'loop_run_steps', 'atom_dump_every', 'mesh_dump_every', 'post_dir')
        diff = [k for k in same if dk[k] != repo_dk[k]]
        if diff:
            raise ValueError(f'로그 안 덱 ↔ 리포 덱 설정 다름: {diff}')
        cv = read_curve(LOG, dk['target_deck'], dk['loop_run_steps'])
        ms_per_step, um, mpa = dk['dt_s'] * 1e3, dk['um_per_deck_m'], dk['mpa_per_deck_mpa']
        b = {k: v['step'] for k, v in cv['bounds'].items()}
        end = cv['last_step']
        bnd = (b['2'], b['3'], b['4'], end)
        meta = json.loads(METRICS.read_text(encoding='utf-8'))
        mesh_end_um = float(meta['compaction']['z_end_mesh_um'])
        if f'{mesh_end_um:.3f}' not in MESH_END_TEXT:
            raise ValueError(f'metrics_D1.json mesh_end {mesh_end_um} µm ≠ D1 README ({MESH_END_TEXT})')
        zfn = plate_model(*bnd, dk['plate_z0_deck'], dk['press_speed_deck_m_s'], dk['dt_s'])
        z_end = zfn(end)
        res_um, tol_um = check_plate_end(z_end, mesh_end_um, um)
        slope = (zfn(b['4']) - zfn(b['3'])) / ((b['4'] - b['3']) * dk['dt_s'])
        if not abs(-slope - dk['press_speed_deck_m_s']) <= SLOPE_REL * dk['press_speed_deck_m_s']:
            raise ValueError(f'판 궤적 기울기 {-slope} ≠ press_speed')
        tser = thickness_series(zfn, bnd, dk['mesh_dump_every'], ms_per_step, um)
        v_um_s = dk['press_speed_deck_m_s'] * um
        vser = velocity_series(bnd, v_um_s, ms_per_step)
        px, pser = pressure_series(cv['rows'], mpa, ms_per_step)
        atoms_at = {r['step']: r['atoms'] for r in cv['rows']}
        pmap = dict(px)
        load = [(s, p) for s, p in px if b['3'] < s <= b['4']]
        relax = [(s, p) for s, p in px if s > b['4']]
        ours = {'b3': b['3'], 'b4': b['4'], 'n_runs': len(cv['judges']), 'z0_um': dk['plate_z0_deck'] * um, 'z_end_um': z_end * um,
                'mesh_end_um': mesh_end_um, 'p_stop': pmap[b['4']], 'p_relax_first': relax[0][1], 'p_end': relax[-1][1],
                'n_load': len(load), 'n_relax': len(relax), 'px': px, 'zfn_um': lambda s: zfn(s) * um}
        with open(CURVE_D1, newline='', encoding='utf-8') as f:
            crow = list(csv.DictReader(f))
        xprob, xstat = crosscheck_draft2(meta, crow, ours)
        if xprob:
            raise ValueError('초안 2 대조 실패 — ' + ' | '.join(xprob[:6]))
        dumps = dump_steps(b['3'], end, dk['atom_dump_every'])
        stages = stage_table(px, cv['bounds'], dumps, end, zfn, um, atoms_at, ms_per_step)
    except ValueError as e:
        raise SystemExit(f'⛔ {e}')
    eps_d2 = {int(r['step']): float(r['eps_sphere_pct']) for r in crow}
    for st in stages:
        for role in ('event', 'nearest', 'other_side', 'recommended'):
            if st[role] is not None:
                st[role]['eps_sphere_pct_draft2'] = eps_d2.get(st[role]['step'])
                if role != 'event':
                    st[role]['atom_file'], st[role]['mesh_file'] = dump_names(st[role]['step'], end, dk['post_dir'])
    tar_steps = sorted({st[r]['step'] for st in stages for r in ('nearest', 'recommended') if st[r] is not None})
    cmd = cluster_command(tar_steps, end, dk['post_dir'], atoms_at)
    bounds_ms = [b['2'] * ms_per_step, b['3'] * ms_per_step, b['4'] * ms_per_step]
    arrows = [(b['4'] * ms_per_step, zfn(b['4']) * um, -26, 20)]   # 판 정지 (이완 시작) — 두께 곡선 위 점 · 투입 시작은 자료 없음

    for p in (ORIGIN, PREV):
        p.mkdir(exist_ok=True)
    write_origin_csv(ORIGIN / f'{CSV_NAMES["thickness"]}.csv', ['Time', 'Thickness', 'Source'], ['ms', 'µm', ''],
                     [(f'{t:.3f}', f'{z:.4f}', s) for t, z, s in tser])
    write_origin_csv(ORIGIN / f'{CSV_NAMES["velocity"]}.csv', ['Time', 'Plate velocity', 'Source'], ['ms', 'µm/s', ''],
                     [(f'{t:.3f}', f'{v:g}', s) for t, v, s in vser])
    write_origin_csv(ORIGIN / f'{CSV_NAMES["pressure"]}.csv', ['Time', 'Measured pressure', 'Source'], ['ms', 'MPa', ''],
                     [(f'{t:.3f}', f'{p:.8g}', s) for t, p, s in pser])
    ogs = [('thickness', '시간 (ms)–두께 (판 위치 · 덱으로 계산)', '79,189,255', 115, 150, 10, 'Thickness (\\g(m)m)', None),
           ('velocity', '시간 (ms)–판 속도 · 덱 press_speed', '112,48,160', 0, 15, 5, 'Plate velocity (\\g(m)m s\\+(-1))', None),
           ('pressure', '시간 (ms)–판 압력 (thermo 원값)', '241,64,64', 0, 330, 100, 'Measured pressure (MPa)', dk['target_mpa'])]
    for key, what, color, y0, y1, yi, ylab, tgt in ogs:
        (ORIGIN / f'{CSV_NAMES[key]}.ogs').write_text(ogs_text(CSV_NAMES[key], what, color, y0, y1, yi, ylab, bounds_ms, tgt),
                                                      encoding='utf-8')
    draw_preview(tser, vser, pser, bounds_ms, dk['target_mpa'], arrows, FIG_NAME)
    with open(STAGE_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['stage', 'event_step', 'event_pressure_MPa', 'role', 'dump_step', 'delta_steps', 'dump_phase', 'pressure_MPa',
                    'plate_um', 'atoms', 'eps_sphere_pct_draft2', 'atom_file', 'mesh_file'])
        for st in stages:
            ev, seen = st['event'], set()
            for role in ('nearest', 'other_side', 'recommended'):
                d = st[role]
                if d is None:
                    continue
                if d['step'] in seen:                       # 권고 = 가장 가까운 것과 같으면 한 줄 (role 에 둘 다)
                    continue
                roles = [r for r in ('nearest', 'other_side', 'recommended') if st[r] is not None and st[r]['step'] == d['step']]
                seen.add(d['step'])
                w.writerow([st['stage'], ev['step'], f'{ev["pressure_mpa"]:.8g}', '+'.join(roles), d['step'], d['delta_steps'], d['phase'],
                            f'{d["pressure_mpa"]:.8g}', f'{d["plate_um"]:.4f}', d['atoms'],
                            '' if d['eps_sphere_pct_draft2'] is None else f'{d["eps_sphere_pct_draft2"]:.4f}', d['atom_file'], d['mesh_file']])

    on = {f'{t:g}': next(([s, p] for s, p in load if p >= t), None) for t in (0.1, 1.0, 10.0, 50.0, 100.0, 200.0, 300.0)}
    counts = [[cv['rows'][0]['step'], cv['rows'][0]['atoms']]] + [[r2['step'], r2['atoms']] for r1, r2 in zip(cv['rows'], cv['rows'][1:])
                                                                 if r2['atoms'] != r1['atoms']]
    ke_steps = sorted({cv['first_step'], b['2'] - 1} | set(range(50000, b['3'], 50000)))
    fnz = next(((s, p) for s, p in load if p != 0.0), None)      # 판이 침대에 처음 닿은 때 (압력 첫 0 아닌 thermo 줄)
    key = {
        'what': '50kg D1 (kg50_d1_b50 · SE D50 1 µm) compaction curve — left column of the ps73-style slide (thickness · plate velocity · '
                'measured pressure) · stage frames for the right-side 3D pore renders',
        'generator': rel(Path(__file__)),
        'inputs': {'log': {'path': rel(LOG), 'sha256': LOG_SHA256}, 'deck_repo': {'path': rel(DECK), 'sha256': DECK_SHA256},
                   'd1_readme': rel(D1_README), 'draft2_metrics': rel(METRICS), 'draft2_curve': rel(CURVE_D1)},
        'deck': {k: dk[k] for k in ('units', 'scale_r', 'scale_E', 'scale_P', 'um_per_deck_m', 'mpa_per_deck_mpa', 'dt_s',
                                     'press_speed_deck_m_s', 'target_deck', 'target_mpa', 'area_deck_m2', 'box_xy_deck', 'r_am_p_deck',
                                     'plate_margin_deck', 'zmax_center_deck', 'plate_z0_deck', 'loop_run_steps', 'atom_dump_every',
                                     'mesh_dump_every', 'post_dir')},
        'x_axis': {'label': XLABEL, 'time_ms': f'step × {ms_per_step:g} (= step × dt {dk["dt_s"]:g} s × 1000 · dt from the deck echo in the log)',
                   'range_ms': [X0, X1],
                   't0': f'step 0 = start of the insertion-only run (NP 1 · insertion at step 1); this log starts at step {cv["first_step"]} '
                         f'(read_restart {cv["read_restart"]})',
                   'note': 'scaled deck time (Scale r×1000 · E×0.001 · P×0.001) — not the real pressing time (ps73 README §5)'},
        'phase_bounds_step': {'packing_settling': [1, b['2'] - 1], 'plate_placed_stabilization': b['2'], 'compression_start': b['3'],
                              'relaxation_plate_stop': b['4'], 'end': end},
        'phase_bounds_ms': {'packing_settling_start': 0.0, 'plate_placed_stabilization': b['2'] * ms_per_step,
                            'compression_start': b['3'] * ms_per_step, 'relaxation_plate_stop': b['4'] * ms_per_step, 'end': end * ms_per_step},
        'phase_markers_in_log': cv['bounds'],
        'compression': {'n_runs': len(cv['judges']), 'steps': b['4'] - b['3'], 'duration_ms': (b['4'] - b['3']) * ms_per_step,
                        'duration_s': round((b['4'] - b['3']) * dk['dt_s'], 12)},
        'thickness': {'definition': 'plate position (bottom wall z = 0 → plate), computed from the deck: fixed at PLATE HEIGHT during '
                                    'stabilization · −press_speed·dt per step during compression · fixed during relaxation',
                      'plate_z0_um': dk['plate_z0_deck'] * um, 'zmax_center_at_settling_end_um': round(dk['zmax_center_deck'] * um, 9),
                      'stop_um': zfn(b['4']) * um, 'end_um_computed': z_end * um, 'end_um_mesh_end': mesh_end_um,
                      'residual_um': res_um, 'tolerance_um': tol_um, 'descent_um': round((dk['plate_z0_deck'] - z_end) * um, 9),
                      'n_points': len(tser), 'grid': f'mesh-dump steps (every {dk["mesh_dump_every"]}) + four phase corners',
                      'packing_segment': 'NOT DRAWN — needs atom positions during settling (not in the repository · README §4)'},
        'velocity': {'deck_m_per_s': dk['press_speed_deck_m_s'], 'um_per_s': v_um_s, 'mm_per_s': v_um_s / 1000.0,
                     'note': 'real length per simulation second (ps73 README §8)', 'series': [list(p) for p in vser]},
        'pressure': {'source': 'thermo pressMPa × 1000 (setup line of every run dropped · scripts/compaction_curve.py rule)',
                     'n_points': len(pser), 'prepended': list(pser[0]), 'first_step_ge_mpa': on,
                     'first_nonzero_in_compression': None if fnz is None else {'step': fnz[0], 'ms': fnz[0] * ms_per_step, 'mpa': fnz[1],
                                                                               'plate_um': zfn(fnz[0]) * um},
                     'stop': [b['4'], pmap[b['4']]], 'relax_first': list(relax[0]), 'relax_min': list(min(relax, key=lambda t: t[1])),
                     'end': list(relax[-1]), 'max': list(max(px, key=lambda t: t[1])), 'target_mpa': dk['target_mpa']},
        'atoms': {'count_changes': counts, 'note': 'SE lost at the start of relaxation (D1 README §2)'},
        'checks': {'deck_log_vs_repo_deck': 'same settings', 'judge_lines_vs_thermo': len(cv['judges']),
                   'plate_end_vs_mesh_end': {'residual_um': res_um, 'within_um': tol_um},
                   'draft2_crosscheck': dict(xstat, status='same'),
                   'mesh_dumps': 'not in the repository — plate position checked only at the end (mesh_end)'},
        'arrows': {'relaxation_start': {'x_ms': arrows[0][0], 'y_um': arrows[0][1], 'drawn': True},
                   'packing_start': {'drawn': False, 'why': 'no thickness data before plate placement (packing segment not drawn)'}},
        'stage_frames': stages,
        'cluster_tar': {'steps': tar_steps, 'run_dir': f'{RUN_PARENT}/{RUN_CASE}', 'bundle': f'$HOME/{TAR_TAG}.tgz', 'command': cmd},
        'packing_segment_requirements': {
            'checkpoints_run0': [f'{RUN_CASE}/restart_{RUN_CASE}/restart_settling_{cv["first_step"]}.bin'] +
                                [f'{RUN_CASE}/restart_{RUN_CASE}/restart_settling_{s}.bin' for s in range(50000, b['2'], 50000)] +
                                [f'{RUN_CASE}/restart_{RUN_CASE}/restart_after_settling.bin'],
            'checkpoints_stabilization_expected': [f'{RUN_CASE}/restart_{RUN_CASE}/restart_settling_{s}.bin' for s in range(250000, b['3'], 50000)],
            'ke_reference_from_log': {str(s): list(cv['ke'][s]) for s in ke_steps if s in cv['ke']},
            'insertion_replay': 'input_kg50_d1_b50_insert.liggghts at NP 1 (same as the insertion run) + atom dump; check inserted counts '
                                'and KE against log_kg50_d1_b50_ins.out (end bundle, outside the repository)',
            'atom_dumps_for_one_criterion': f'{len(dumps) - 1} compression/relaxation dumps (every {dk["atom_dump_every"]}) + atom_end',
        },
    }
    KEY_JSON.write_text(json.dumps(key, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'dt {dk["dt_s"]:g} s · ms/step {ms_per_step:g} · 판 {dk["plate_z0_deck"] * um:.6f} → {z_end * um:.6f} µm (mesh_end {mesh_end_um} · '
          f'잔차 {res_um:+.6f} µm) · 압축 {len(cv["judges"])} run = {(b["4"] - b["3"]) * ms_per_step:g} ms · 정지 {pmap[b["4"]]:.5f} MPa · '
          f'끝 {relax[-1][1]:.5f} MPa · 판 속도 {v_um_s:g} µm/s · 초안 2 대조 {xstat["n_rows_compared"]} 행 같음')
    for st in stages:
        n, r = st['nearest'], st['recommended']
        print(f'  {st["label"]:<22} 사건 {st["event"]["step"]:>9,} ({st["event"]["pressure_mpa"]:.2f} MPa) → 가장 가까운 덤프 {n["step"]:,} '
              f'(Δ {n["delta_steps"]:+,} · 단계 {n["phase"]} · {n["pressure_mpa"]:.2f} MPa) · 권고 {r["step"]:,}')


# ───────────────────────────── 자기 시험 (합성 로그) ─────────────────────────────
def _synth_log(**kw):
    """D1 로그 꼴의 작은 합성 로그 — 정착 1,000 · zmax run 1 · 안정화 2,000 · 압축 5 run × run_len · 이완 3,000 · run 0.
    kw (반례): judge_bias · targets · phase4_shift · drop_pcol · nan_at · run_len · last_p · mid_hit · restart_step · plate ·
    dt_line · ts_line · move_line · scale_line · area · units."""
    g = kw.get
    run_len = g('run_len', 5000)
    s_set, s_ss = 20001, 21001
    b2, b3 = s_ss + 1, s_ss + 1 + 2000
    n_runs = 5
    b4 = b3 + n_runs * run_len
    gap = 1000 if g('phase4_shift') else 0
    end = b4 + gap + 3000
    k = g('last_p', 0.301) / (b4 - b3 - 8000)

    def pc(s):
        if g('mid_hit') and s == b3 + 2 * run_len:
            return 0.35
        return max(0.0, (s - (b3 + 8000)) * k)

    def block(cols, s0, s1, fn, every=1000):
        steps = [s0] + list(range((s0 // every + 1) * every, s1, every)) + [s1]
        return ['    ' + '    '.join(cols)] + [fn(s) for s in steps] + [f'Loop time of 1.0 on 20 procs for {s1 - s0} steps with 168457 atoms', '']

    def row_p(s, pfn, atoms=168457):
        if g('nan_at') == s:
            return f'{s:>9} {atoms:>8} {1e-6:>14.8g} {0.0:>14.8g} {"nan":>14}'
        return f'{s:>9} {atoms:>8} {1e-6:>14.8g} {0.0:>14.8g} {pfn(s):>14.8g}'

    pcol = ['Step', 'Atoms', 'KinEng', 'CPU', 'pressMPa']
    L = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)',
         g('scale_line', '# Scale: r×1000, E×0.001, P×0.001'), g('units', 'units           si'),
         'variable target_press equal 0.30          # 300 MPa × 0.001', 'variable r_AM_P  equal 3e-3',
         g('dt_line', 'variable dt      equal 1.0e-6'), 'variable plate_margin equal 0.003', 'timestep        ${dt}',
         g('ts_line', 'timestep        1e-06'), f'read_restart    restart_x/restart_settling_{g("restart_step", s_set)}.bin',
         '  orthogonal box = (0 0 -0.01) to (0.05 0.05 1)', 'thermo_style    custom step atoms ke cpu',
         'print "====== PHASE 1: SETTLING ======"', '====== PHASE 1: SETTLING ======', 'run 1000']
    L += block(pcol[:4], s_set, s_ss, lambda s: f'{s:>9} {168457:>8} {2.0:>14.8g} {0.0:>14.8g}')
    L += ['thermo_style    custom step atoms c_zmax', 'run 1']
    L += block(['Step', 'Atoms', 'zmax'], s_ss, s_ss + 1, lambda s: f'{s:>9} {168457:>8} {0.13944572:>14.8g}', every=10 ** 9)
    L += ['====== Z_MAX (center): 0.139445726030801 ======', f'====== PLATE HEIGHT: {g("plate", 0.145445726030801)!r} ======',
          'dump dmp_mesh all mesh/stl 5000 post_x/mesh_*.stl top_mesh', '====== PHASE 2: STABILIZE ======',
          'variable pressMPa equal abs(f_top_mesh[3])/' + g('area', '0.0025') + '/1000000',
          'thermo_style    custom step atoms ke cpu v_pressMPa', 'run 2000']
    if g('drop_pcol'):
        L += block(pcol[:4], b2, b3, lambda s: f'{s:>9} {168457:>8} {1e-6:>14.8g} {0.0:>14.8g}')
    else:
        L += block(pcol, b2, b3, lambda s: row_p(s, lambda _s: 0.0))
    L += ['====== PHASE 3: COMPRESSION (Speed 0.01) ======', 'dump dmp_atom all custom 50000 post_x/atom_*.liggghts id type x y z radius',
          'variable press_speed equal 0.01', 'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}',
          g('move_line', 'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -0.01'), 'label loop_press', f'    run {run_len}']
    targets = g('targets', [0.3] * n_runs)
    for i in range(n_runs):
        s0, s1 = b3 + i * run_len, b3 + (i + 1) * run_len
        L += block(pcol, s0, s1, lambda s: row_p(s, pc))
        x = pc(s1) * ((1 + g('judge_bias', 0.0)) if i == n_runs - 1 else 1)
        L += ['    variable current_press equal "abs(f_top_mesh[3]) / 0.0025 / 1000000"',
              f'Current Pressure: {x!r} MPa (Target: {targets[i]!r})']
    L += ['unfix move_press']
    if gap:                                                    # 루프 탈출과 PHASE 4 표지 사이에 run 하나 더 (표지가 다른 step 으로 풀린다)
        L += block(pcol, b4, b4 + gap, lambda s: row_p(s, lambda _s: 0.2))
    relax_p = lambda s: 0.156 + 0.05 * math.exp(-(s - b4) / 1000.0)  # noqa: E731
    L += ['====== PHASE 4: RELAXATION ======', 'run 3000']
    L += block(pcol, b4 + gap, end, lambda s: row_p(s, relax_p, 168457 if s < b4 + 2000 else 168452))
    L += ['run 0', '    ' + '    '.join(pcol), row_p(end, lambda _s: 0.161, 168452), 'Loop time of 1e-05 on 20 procs for 0 steps', '']
    return '\n'.join(L) + '\n', {'b2': b2, 'b3': b3, 'b4': b4, 'end': end, 'k': k}


def selftest():
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        ok, fail = ok + bool(cond), fail + (not cond)
        print(('PASS ' if cond else 'FAIL ') + name)

    def raises(fn):
        """거부 = ValueError 만 (다른 예외 · 통과 = 실패 — 기능을 뺀 판 (NotImplementedError) 이 반례를 통과하지 못하게)."""
        try:
            fn()
        except ValueError:
            return True
        except Exception:            # noqa: BLE001
            return False
        return False

    def safe(fn, default=None):
        try:
            return fn()
        except Exception:            # noqa: BLE001
            return default

    with tempfile.TemporaryDirectory(prefix='d1ms_') as tmp:
        counter = itertools.count()

        def curve(**kw):
            text, bb = _synth_log(**kw)
            p = Path(tmp) / f'log_{next(counter)}.txt'
            p.write_text(text, encoding='utf-8')
            return text, bb, p

        text, b, path0 = curve()
        dk = safe(lambda: deck_settings(text), {})
        chk('D0 합성 로그 덱: dt · 판 속도 · 배율 · 면적 · 목표 · 판 높이 · 루프 run · 덤프 간격 · 덤프 폴더',
            dk.get('dt_s') == 1e-6 and dk.get('press_speed_deck_m_s') == 0.01 and dk.get('um_per_deck_m') == 1000.0
            and dk.get('mpa_per_deck_mpa') == 1000.0 and dk.get('area_deck_m2') == 0.0025 and dk.get('target_mpa') == 300.0
            and dk.get('plate_z0_deck') == 0.145445726030801 and dk.get('loop_run_steps') == 5000 and dk.get('atom_dump_every') == 50000
            and dk.get('mesh_dump_every') == 5000 and dk.get('post_dir') == 'post_x')
        for name, kw in [('D1 timestep ≠ variable dt', {'ts_line': 'timestep 2e-06'}),
                         ('D2 variable dt 둘', {'dt_line': 'variable dt equal 1.0e-6\nvariable dt equal 2.0e-6'}),
                         ('D3 판이 옆으로 움직인다', {'move_line': 'fix m all move/mesh mesh top linear 0.001 0.0 -0.01'}),
                         ('D4 판 속도 둘 (숫자 줄 ≠ press_speed)', {'move_line': 'fix m all move/mesh mesh top linear 0.0 0.0 -0.02'}),
                         ('D5 Scale 머리 없음', {'scale_line': '# (no scale)'}),
                         ('D6 pressMPa 면적 ≠ 판정 식 · 상자 x·y 면적', {'area': '0.0036'}),
                         ('D7 PLATE HEIGHT ≠ Z_MAX + r_AM_P + margin', {'plate': 0.1455}),
                         ('D8 units ≠ si', {'units': 'units lj'}),
                         ('D9 로그에 풀린 timestep 숫자 줄 없음', {'ts_line': ''}),
                         ('D10 로그에 풀린 move/mesh 숫자 줄 없음', {'move_line': ''})]:
            t2, _ = _synth_log(**kw)
            chk(name + ' = 거부', raises(lambda: deck_settings(t2)))
        chk('D11 PLATE HEIGHT 둘 = 거부', raises(lambda: deck_settings(text + '====== PLATE HEIGHT: 0.15 ======\n')))
        chk('D12 undump dmp_atom (덤프 끊김) = 거부', raises(lambda: deck_settings(text + 'undump dmp_atom\n')))
        deck_only = '\n'.join(ln for ln in text.splitlines()[1:] if not re.match(r'\s*(=|orthogonal|timestep\s+1e|fix move_press .* -0\.01)', ln))
        dd = safe(lambda: deck_settings(deck_only), {})
        chk('D13 덱 글 (LIGGGHTS 머리 없음 · ${dt} · ${press_speed} 만) = 읽힘 · 판 높이 없음',
            dd.get('dt_s') == 1e-6 and dd.get('press_speed_deck_m_s') == 0.01 and 'plate_z0_deck' not in dd)

        cv = safe(lambda: read_curve(path0, 0.3, 5000))
        chk('L0 합성 로그: 단계 경계 · 판정 줄 5 · 설정 줄 버림 · 경계 줄의 단계 · KE 참고 (설정 줄 포함)',
            cv is not None and [cv['bounds'][k]['step'] for k in '1234'] == [20001, b['b2'], b['b3'], b['b4']]
            and len(cv['judges']) == 5 and cv['last_step'] == b['end'] and cv['first_step'] == 20001
            and all(r['step'] != 20001 for r in cv['rows']) and cv['ke'].get(20001) == (168457, 2.0)
            and {r['phase'] for r in cv['rows'] if r['step'] == b['b4']} == {3} and {r['phase'] for r in cv['rows'] if r['step'] == b['b3']} == {2})
        for name, kw in [('L1 판정 줄 ≠ thermo', {'judge_bias': 0.01}),
                         ('L2 목표 둘', {'targets': [0.3, 0.3, 0.25, 0.3, 0.3]}),
                         ('L3 단계 ≥ 2 긴 블록에 압력 열 없음', {'drop_pcol': True}),
                         ('L4 비유한 압력', {'nan_at': b['b3'] + 6998}),
                         ('L5 마지막 판정 < 목표 (루프 탈출 안 함)', {'last_p': 0.29}),
                         ('L6 중간 판정이 목표 이상 (더 일찍 나갔어야)', {'mid_hit': True}),
                         ('L7 read_restart step ≠ 첫 thermo step', {'restart_step': 20000}),
                         ('L8 PHASE 4 표지 ≠ 루프 탈출 step', {'phase4_shift': True})]:
            _, _, p2 = curve(**kw)
            chk(name + ' = 거부', raises(lambda: read_curve(p2, 0.3, kw.get('run_len', 5000))))
        _, _, p4 = curve(run_len=4000)
        cv4 = safe(lambda: read_curve(p4, 0.3, 4000))
        chk('L9 run 4,000 덱 = 그 길이로 이어짐 (일반화) · 5,000 으로 읽으면 거부',
            cv4 is not None and len(cv4['judges']) == 5 and raises(lambda: read_curve(p4, 0.3, 5000)))
        chk('L10 판정 목표 ≠ 덱 target_press = 거부', raises(lambda: read_curve(path0, 0.25, 5000)))

        z = safe(lambda: plate_model(200002, 400002, 2685002, 2785002, 0.145445726030801, 0.01, 1e-6))
        chk('T1 판 궤적: 안정화 고정 · 압축 등속 · 이완 고정 · 끝 122.595726 µm',
            z is not None and z(200002) == z(400002) == 0.145445726030801 and abs(z(500002) * 1000 - 144.445726030801) < 1e-9
            and z(2685002) == z(2785002) and abs(z(2785002) * 1000 - 122.595726030801) < 1e-9)
        chk('T2 판 놓기 전 · 끝 뒤 step = 거부', z is not None and raises(lambda: z(200001)) and raises(lambda: z(2785003)))
        chk('T3 단계 경계 순서 어긋남 = 거부', raises(lambda: plate_model(400002, 200002, 2685002, 2785002, 0.1454, 0.01, 1e-6)))
        r = safe(lambda: check_plate_end(0.122595726030801, 122.596, 1000.0))
        chk('T4 끝 대조: 잔차 −0.000274 µm (반폭 0.0005 안) = 통과', r is not None and abs(r[0] + 0.000273969199) < 1e-9)
        chk('T5 끝 대조: mesh_end 122.597 (1 nm 어긋남) = 거부', raises(lambda: check_plate_end(0.122595726030801, 122.597, 1000.0)))
        chk('T6 끝 대조: 판 속도 0.0101 로 계산한 끝 = 거부',
            raises(lambda: check_plate_end(plate_model(200002, 400002, 2685002, 2785002, 0.145445726030801, 0.0101, 1e-6)(2785002), 122.596, 1000.0)))
        chk('T7 끝 대조: NaN = 거부', raises(lambda: check_plate_end(float('nan'), 122.596, 1000.0)))
        ts = safe(lambda: thickness_series(z, (200002, 400002, 2685002, 2785002), 5000, 1e-3, 1000.0), [])
        chk('T8 두께 점: 메시 step 517 + 모서리 4 · 시각 엄격 증가 · 모서리 출처',
            len(ts) == 521 and all(q[0] > p[0] for p, q in zip(ts, ts[1:])) and ts[0][2] == SRC['placed'] and ts[-1][2] == SRC['end']
            and abs(ts[0][1] - 145.445726030801) < 1e-9 and any(t == 2685.002 and s == SRC['stop'] for t, _, s in ts))
        vs = velocity_series((200002, 400002, 2685002, 2785002), 10.0, 1e-3)
        chk('V1 판 속도 계단 7 점 · 400.002 → 2685.002 ms 만 10 µm/s',
            [v for _, v, _ in vs] == [0, 0, 0, 10.0, 10.0, 0, 0] and [t for t, _, _ in vs] == [0.0, 200.002, 400.002, 400.002, 2685.002, 2685.002, 2785.002])
        if cv is not None:
            px, ps = safe(lambda: pressure_series(cv['rows'], 1000.0, 1e-3), (None, None))
            chk('P1 압력: 앞에 (0 ms, 0 MPa, 판 없음) · 단계 ≥ 2 원값 × 1000',
                ps is not None and ps[0] == (0.0, 0.0, SRC['noplate']) and len(ps) == len(px) + 1 and px[0] == (b['b2'] + 998, 0.0))
            rows_bad = [dict(rr, p_deck=(0.001 if rr['phase'] == 2 else rr['p_deck'])) for rr in cv['rows']]
            chk('P2 판 놓은 뒤 첫 압력 ≠ 0 = 거부', raises(lambda: pressure_series(rows_bad, 1000.0, 1e-3)))
            zs = plate_model(b['b2'], b['b3'], b['b4'], b['end'], 0.145445726030801, 0.01, 1e-6)
            dps = dump_steps(b['b3'], b['end'], 5000)
            am = {rr['step']: rr['atoms'] for rr in cv['rows']}
            st = safe(lambda: stage_table(px, cv['bounds'], dps, b['end'], zs, 1000.0, am, 1e-3), []) if px else []
            want50 = next(s for s, p in px if b['b3'] < s and p >= 50.0) if px else None
            chk('S1 단계 표: 50 MPa = 압축 중 처음 ≥ 50 thermo 줄 · 가장 가까운 덤프 · 반대쪽 덤프',
                len(st) == 4 and st[1]['event']['step'] == want50 and st[1]['nearest']['step'] == min(dps, key=lambda d: (abs(d - want50), -d))
                and st[1]['other_side'] is not None and (st[1]['other_side']['step'] - want50) * st[1]['nearest']['delta_steps'] < 0)
            chk('S2 판 정지: 가장 가까운 덤프가 이완 단계면 표지 · 권고 = 같은 압축 단계 덤프 · 끝 = atom_end (Δ 0 · 반대쪽 없음)',
                len(st) == 4 and st[2]['nearest']['phase'] == 4 and not st[2]['nearest_is_same_phase']
                and st[2]['recommended']['phase'] == 3 and st[2]['recommended']['step'] < b['b4']
                and st[3]['nearest']['step'] == b['end'] and st[3]['nearest']['delta_steps'] == 0 and st[3]['other_side'] is None)
            chk('S3 압축 중 그 압력에 닿지 않으면 거부', bool(px) and raises(lambda: stage_table(px, cv['bounds'], dps, b['end'], zs, 1000.0, am, 1e-3,
                                                                                           p_stage=400.0)))
        else:
            for nm in ('P1', 'P2', 'S1', 'S2', 'S3'):
                chk(nm + ' (합성 로그 읽기 실패)', False)
        dsr = dump_steps(400002, 2785002, 50000)
        chk('S4 덤프 일정: 압축 시작 400,002 뒤 첫 덤프 450,000 · 50,000 마다 · 끝 덤프 2,785,002 (47 + 1)',
            dsr[:2] == [450000, 500000] and dsr[-2:] == [2750000, 2785002] and len(dsr) == 48)
        cmd = safe(lambda: cluster_command([450000, 2785002], 2785002, 'post_kg50_d1_b50', {450000: 168457, 2785002: 168452}), '')
        chk('C1 클러스터 명령: bash -s · set -e · 끝 묶음 sha256 둘 · TIMESTEP/원자 수 검사 · 주소 · 포트 없음',
            cmd.startswith("bash -s <<'EOF'\nset -euo pipefail") and ATOM_END_SHA256 in cmd and MESH_END_SHA256 in cmd
            and 'check kg50_d1_b50/post_kg50_d1_b50/atom_450000.liggghts 450000 168457' in cmd
            and 'kg50_d1_b50/post_kg50_d1_b50/mesh_end_2785002.stl' in cmd and '@' not in cmd and 'scp' not in cmd and 'ssh' not in cmd)
        chk('C2 클러스터 명령: 로그에 없는 step 의 원자 수를 모르면 거부 (KeyError — 지어내지 않는다)',
            safe(lambda: cluster_command([450001], 2785002, 'p', {}), 'refused') == 'refused')
        pth = Path(tmp) / 'o.csv'
        write_origin_csv(pth, ['Time', 'Thickness', 'Source'], ['ms', 'µm', ''], [('0.000', '1.0000', 'x')])
        raw = pth.read_bytes()
        chk('C3 Origin CSV: BOM · LF · 머리 두 줄', raw.startswith(b'\xef\xbb\xbfTime,Thickness,Source\nms,') and b'\r' not in raw)
        met = {'compaction': {'compress_start_step': 3, 'stop_step': 4, 'n_compress_runs': 1, 'plate_z0_um': 1.0, 'z_end_pred_um': 0.5,
                              'z_end_mesh_um': 0.5, 'p_t0minus_MPa': 300.0, 'p_relax_first_MPa': 200.0, 'p_end_MPa': 150.0,
                              'n_load_rows': 1, 'n_relax_rows': 1}}
        ours = {'b3': 3, 'b4': 4, 'n_runs': 1, 'z0_um': 1.0, 'z_end_um': 0.5, 'mesh_end_um': 0.5, 'p_stop': 300.0, 'p_relax_first': 200.0,
                'p_end': 150.0, 'n_load': 1, 'n_relax': 1, 'px': [(4, 300.0), (5, 200.0)], 'zfn_um': lambda s: 0.5}
        rows_ok = [{'branch': 'loading', 'step': '4', 'plate_pressure_MPa': '300.0', 'plate_gap_um': '0.5'},
                   {'branch': 'fixed_height_relaxation', 'step': '5', 'plate_pressure_MPa': '200.0', 'plate_gap_um': '0.5'}]
        chk('X1 초안 2 대조: 같으면 통과', safe(lambda: crosscheck_draft2(met, rows_ok, ours)[0]) == [])
        chk('X2 초안 2 대조: 판 높이 0.01 µm 다름 = 문제', bool(safe(lambda: crosscheck_draft2(met, [dict(rows_ok[0], plate_gap_um='0.51'), rows_ok[1]], ours)[0], [])))
        chk('X3 초안 2 대조: 끝 압력 다름 = 문제', bool(safe(lambda: crosscheck_draft2({'compaction': dict(met['compaction'], p_end_MPa=150.1)},
                                                                                rows_ok, ours)[0], [])))
        chk('X4 초안 2 대조: 행 하나 빠짐 = 문제', bool(safe(lambda: crosscheck_draft2(met, rows_ok[:1], ours)[0], [])))
        chk('X5 초안 2 대조: 압력 NaN = 문제', bool(safe(lambda: crosscheck_draft2(met, [dict(rows_ok[0], plate_pressure_MPa='nan'), rows_ok[1]], ours)[0], [])))
    print(f'make_fig_d1_ms selftest: {ok} PASS · {fail} FAIL')
    return fail == 0


if __name__ == '__main__':
    if '--selftest' in sys.argv[1:]:
        sys.exit(0 if selftest() else 1)
    main()
