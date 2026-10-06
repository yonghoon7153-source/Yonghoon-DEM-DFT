#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 압밀 곡선 — LIGGGHTS 로그 thermo + 판 메시 덤프 → step 별 압력 · 판 높이 (읽기 전용).

    python3 scripts/compaction_curve.py --segment <r1 로그> --segment <r3 로그> --mesh-dir <post_…> --out <새 폴더>
시험: scripts/test_compaction_curve.py (합성 로그 · 반례).

왜 (1저자 2026-10-06 밤 — 이종기술 2-1 장 7:3: *"모든 step 에서 데이터를 얻어서 … 압축이 됐다는 걸 보여주게"* · x 축 = step):
  압밀 기록은 지금까지 끝 한 점 (`lhs_pressure_record.py` = 루프 탈출 판정 줄) 과 마지막 프레임 두께뿐이었다.
  덱이 남기는 시계열 — thermo 압력 열 (1,000 step 마다) · 판 메시 `mesh_<step>.stl` (5,000 step 마다) — 을 그대로 잇는다.
  매 step 이 저장되지는 않는다 (가장 촘촘한 것 = thermo 간격).

규약 (덱 `in.ps_*_r45.liggghts` 계열 — Scale r×1000 · E×0.001 · P×0.001):
  압력 MPa = thermo 압력 열 (`v_pressMPa` = |판 수직 힘| / 면적, 덱 단위) × 1000 (`press_units.SIM_TO_MPA`).
  두께 µm = (판 메시 꼭짓점 z − 바닥 zplane) × 1000 (`lhs_descriptor_harvest.SIM_TO_UM` · 평판 검사 `plate_z_from_stl`).
  이 두께는 **판 위치**다 — 판이 침대에 닿기 전 (덱이 판을 맨 위 입자보다 몇 µm 위에 놓는다) 은 침대 두께가 아니다.

이어 붙이기 (재시작 런):
  `--segment` 를 **궤적 순서**로 준다.  뒤 조각은 자기 첫 step (read_restart 의 step) 뒤부터 앞 조각을 **대신한다**
  (덤프 덮어쓰기와 같은 뜻).  주지 않은 로그는 쓰지 않는다 — 예: 재시작 때 판이 다시 들린 r2 (2026-09-21 진행 기록).
  run 마다 첫 thermo 줄 (설정 줄) 은 버린다 — 같은 step 의 앞 run 마지막 줄과 압력이 다르게 찍힌다
  (CLAUDE.md 재개 체크리스트 ⑤ · 원 런 실측 최대 1.08 배 · read_restart 직후 설정 줄은 0).

검사 (fail-closed — 하나라도 어긋나면 곡선을 내지 않는다):
  C1 조각마다 thermo 가 있다 · 단계 ≥ 2 의 블록은 압력 열 (`v_pressMPa` · `pressMPa`) 을 이름으로 갖는다 · 압력 값 유한
  C2 뒤 조각이 앞 조각보다 늦게 시작 · 빈 구간 없음 (뒤 조각 첫 step ≤ 앞 조각 마지막 step) · read_restart 파일 이름의 step = 첫 step
  C3 `PLATE HEIGHT` 줄 = 그 step 의 판 메시 z (|Δ| ≤ Z_TOL) · 잇는 자리 압력 붕괴 (판 재부양 증상) 없음
  C4 판정 줄 `Current Pressure: X MPa (Target: T)` 의 X = 같은 step thermo 압력 · T 하나 · PHASE 4 표지 = 루프 탈출 step
  C5 판 메시 평판 · 안정화 · 이완 단계에서 z 불변 · 압축 단계에서 z 가 오르지 않고 직선 (등속 하강)
  C6 이은 뒤 step 엄격 증가
산출 (`--out` = 새 폴더): pressure.csv (step · 단계 · 조각 · 압력 MPa) · plate.csv (step · 단계 · 판 z · 두께 µm) · curve_summary.json.
거부면 curve_summary.json (status REFUSED · why) 만 쓰고 rc 2.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lhs_descriptor_harvest as LDH     # noqa: E402  — 판 STL 평판 검사 · 덱 길이 → µm (사본 금지)
import lhs_pressure_record as LPR        # noqa: E402  — 판정 줄 꼴 (PRESS_LINE) 하나만 쓴다
import press_units as PU                 # noqa: E402  — 덱 압력 → MPa (필드 이름이 단위를 정한다)

SCHEMA = 'compaction_curve/v1'
Z_TOL = 2e-6          # 덱 m (= 2 nm 실물) — 메시 STL 꼭짓점 소수 6 자리 (1e-6) 의 두 칸
FIT_TOL = 5e-6        # 덱 m — 압축 단계 판 높이의 직선 잔차 한계 (등속 `fix move/mesh linear`)
JUDGE_REL = 1e-5      # 판정 줄 ↔ thermo 압력 상대 허용 (thermo 인쇄 자릿수)
COLLAPSE_RATIO = 0.01   # 잇는 자리: 뒤 조각 첫 줄들이 앞 압력의 1 % 밑이면 붕괴 (판 재부양 증상)
COLLAPSE_MIN_FRAC = 0.05  # … 단 앞 압력이 목표의 5 % 이상일 때만 (접촉 전은 원래 0)
COLLAPSE_ROWS = 5

RX_MARK = re.compile(r'^\s*=+\s*PHASE\s+(\d+)\s*:\s*(.*?)\s*=+\s*$')
RX_PLATE = re.compile(r'^\s*=+\s*PLATE HEIGHT:\s*(\S+)\s*=+\s*$')
RX_RESTART = re.compile(r'^\s*read_restart\s+(\S+)')
RX_ZPLANE = re.compile(r'\bzplane\s+(\S+)')
RX_MESH = re.compile(r'^mesh_(\d+)\.stl$')
RX_DIGITS = re.compile(r'(\d+)')


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _num(tok):
    try:
        return float(tok)
    except (TypeError, ValueError):
        return None


def _is_press_col(name, want=None):
    if want:
        return name == want
    n = name.lower()
    return (n[2:] if n.startswith('v_') else n) == 'pressmpa'


def parse_log(path, press_col=None):
    """로그 → 사건 목록 (순서 그대로).  ('block', 블록) · ('mark', 번호, 이름) · ('plate', z) · ('judge', X, T) · ('restart', 파일)."""
    ev, blk, zplane = [], None, None

    def close(complete):
        nonlocal blk
        blk['complete'] = complete
        ev.append(('block', blk))
        blk = None

    with open(path, encoding='utf-8', errors='replace') as fh:
        for raw in fh:
            ln = raw.rstrip('\r\n')
            tok = ln.split()
            if blk is not None:
                if ln.lstrip().startswith('Loop time of'):
                    close(True)
                    continue
                if tok and tok[0] == 'Step' and len(tok) >= 2:      # 끝맺지 못한 블록 뒤 새 머리
                    close(False)
                elif len(tok) == len(blk['cols']) and tok[0].isdigit():
                    vals = [_num(t) for t in tok]
                    if all(v is not None for v in vals):
                        blk['rows'].append((int(tok[0]), vals))
                        continue
                    blk['n_other'] += 1
                    continue
                else:
                    blk['n_other'] += 1                              # 경고 · 잘린 줄 · 블록 안 출력
                    continue
            if tok and tok[0] == 'Step' and len(tok) >= 2:
                pc = next((i for i, c in enumerate(tok) if _is_press_col(c, press_col)), None)
                blk = {'cols': tok, 'pcol': pc, 'rows': [], 'complete': False, 'n_other': 0}
                continue
            m = RX_MARK.match(ln)
            if m:
                ev.append(('mark', int(m.group(1)), m.group(2).strip()))
                continue
            m = RX_PLATE.match(ln)
            if m:
                ev.append(('plate', _num(m.group(1))))
                continue
            m = LPR.PRESS_LINE.match(ln)
            if m:
                ev.append(('judge', _num(m.group(1)), _num(m.group(2))))
                continue
            m = RX_RESTART.match(ln)
            if m:
                ev.append(('restart', m.group(1)))
                continue
            if zplane is None:
                m = RX_ZPLANE.search(ln)
                if m and 'wall/gran' in ln:
                    zplane = _num(m.group(1))
    if blk is not None:
        close(False)
    return {'events': ev, 'zplane': zplane}


def resolve(seg):
    """사건에 step 을 붙인다 — 표지 · 판 높이 = **다음** 블록의 설정 줄 step · 판정 줄 = **앞** 블록의 마지막 줄 step."""
    ev = seg['events']
    blocks = [e[1] for e in ev if e[0] == 'block' and e[1]['rows']]
    seg['blocks'] = blocks
    seg['first'] = blocks[0]['rows'][0][0] if blocks else None
    seg['last'] = max((b['rows'][-1][0] for b in blocks), default=None)
    marks, plates, judges, restarts = [], [], [], []
    for i, e in enumerate(ev):
        if e[0] in ('mark', 'plate'):
            nxt = next((x[1] for x in ev[i + 1:] if x[0] == 'block' and x[1]['rows']), None)
            step = nxt['rows'][0][0] if nxt else None
            (marks if e[0] == 'mark' else plates).append((step,) + e[1:])
        elif e[0] == 'judge':
            prv = next((x[1] for x in reversed(ev[:i]) if x[0] == 'block' and x[1]['rows']), None)
            judges.append((prv['rows'][-1][0] if prv else None, e[1], e[2], prv))
        elif e[0] == 'restart':
            restarts.append(e[1])
    seg.update(marks=marks, plates=plates, judges=judges, restarts=restarts)
    return seg


def read_meshes(mesh_dir):
    """→ (목록 [(step, z)], 문제).  평판이 아니면 문제 (HND-06 — 평균을 높이로 받지 않는다)."""
    out, bad = [], []
    try:
        names = sorted(os.listdir(mesh_dir))
    except OSError as e:
        return [], [f'메시 폴더를 못 읽었다 ({type(e).__name__}: {mesh_dir})']
    for n in names:
        m = RX_MESH.match(n)
        if not m:
            continue
        try:
            out.append((int(m.group(1)), float(LDH.plate_z_from_stl(os.path.join(mesh_dir, n)))))
        except Exception as e:      # BedRefusal (평판 아님 · 꼭짓점 없음) · 읽기 실패
            bad.append(f'{n}: {e}')
    out.sort()
    return out, bad


def _phase_at(bounds, step):
    """경계 step b = 새 단계 첫 run 의 설정 줄 step.  b 의 줄 (설정 줄은 버리므로 앞 run 의 마지막 줄) 은 **앞 단계**의 끝 상태다
    ⇒ 단계 p 는 b_p **보다 큰** step 부터 (예: zmax `run 1` 의 끝 줄 = 정착 끝 · 루프 탈출 줄 = 압축 끝)."""
    ph = 0
    for k, b in bounds.items():
        if b['step'] is not None and b['step'] < step and int(k) > ph:
            ph = int(k)
    return ph


def build(seg_paths, mesh_dir, press_col=None):
    """→ (요약 dict, 압력 행, 판 행).  요약['status'] = OK | REFUSED."""
    why, checks = [], {f'C{i}': {'ok': True, 'detail': []} for i in range(1, 7)}

    def fail(c, msg):
        checks[c]['ok'] = False
        checks[c]['detail'].append(msg)
        why.append(f'{c}: {msg}')

    def note(c, msg):
        checks[c]['detail'].append(msg)

    segs = []
    for p in seg_paths:
        s = parse_log(p, press_col)
        s.update(path=p, label=os.path.basename(p), sha256=sha256_of(p), size=os.path.getsize(p))
        segs.append(resolve(s))
    n = len(segs)

    # ── C1 · C2 조각 · 잇기 ──
    for k, s in enumerate(segs):
        if not s['blocks']:
            fail('C1', f'{s["label"]}: thermo 블록이 없다')
    if not all(s['blocks'] for s in segs):
        return _refused(segs, why, checks), [], []
    starts = [s['first'] for s in segs]
    for k in range(1, n):
        s, prev = segs[k], segs[k - 1]
        if starts[k] <= starts[k - 1]:
            fail('C2', f'{s["label"]} 첫 step {starts[k]} 이 앞 조각 {prev["label"]} 첫 step {starts[k - 1]} 보다 늦지 않다 — 같은 체크포인트에서 갈라진 두 궤적을 함께 줄 수 없다')
        if starts[k] > prev['last']:
            fail('C2', f'빈 구간 — {s["label"]} 은 {starts[k]} 에서 시작하는데 {prev["label"]} 는 {prev["last"]} 에서 끝났다')
        if not s['restarts']:
            fail('C2', f'{s["label"]}: read_restart 줄이 없다 — 재시작 조각이 아니다')
        for rf in s['restarts']:
            d = RX_DIGITS.findall(os.path.basename(rf))
            if not d:
                note('C2', f'{s["label"]}: read_restart {rf} — 파일 이름에 step 이 없어 대조 못 함')
            elif int(d[-1]) != starts[k]:
                fail('C2', f'{s["label"]}: read_restart {rf} 의 step {int(d[-1])} ≠ 첫 thermo step {starts[k]}')

    def kept(k, step, inclusive_lo=False):
        lo_ok = k == 0 or (step >= starts[k] if inclusive_lo else step > starts[k])
        hi_ok = k == n - 1 or step <= starts[k + 1]
        return lo_ok and hi_ok

    # ── 행 · 단계 경계 ──
    rows, n_setup = [], 0
    for k, s in enumerate(segs):
        for b in s['blocks']:
            n_setup += 1
            for step, vals in b['rows'][1:]:                 # 설정 줄 (첫 줄) 버림
                if kept(k, step):
                    rows.append({'step': step, 'segment': s['label'], 'k': k, 'pcol': b['pcol'],
                                 'p_deck': (vals[b['pcol']] if b['pcol'] is not None else None)})
    bounds = {}
    for k, s in enumerate(segs):
        for step, num, name in s['marks']:
            if step is not None and kept(k, step, inclusive_lo=True) and str(num) not in bounds:
                bounds[str(num)] = {'step': step, 'name': name, 'source': 'marker', 'segment': s['label']}

    # ── C4 판정 줄 ──
    judges = []
    for k, s in enumerate(segs):
        for step, x, t, blk in s['judges']:
            if step is None or not kept(k, step):
                continue
            judges.append((step, x, t, s['label']))
            p = next((v[blk['pcol']] for st, v in blk['rows'] if st == step), None) if blk['pcol'] is not None else None
            if x is None or t is None or p is None or not (math.isfinite(x) and math.isfinite(p)):
                fail('C4', f'{s["label"]} step {step}: 판정 줄 {x} ↔ thermo 압력 {p} 를 대조할 수 없다')
            elif abs(x - p) > 1e-12 + JUDGE_REL * max(abs(x), abs(p)):
                fail('C4', f'{s["label"]} step {step}: 판정 줄 {x!r} ≠ thermo 압력 {p!r} (덱 단위) — 압력 열을 잘못 읽었거나 로그가 섞였다')
    targets = sorted({t for _, _, t, _ in judges if t is not None})
    if len(targets) > 1:
        fail('C4', f'판정 줄 목표가 하나가 아니다 {targets}')
    target = targets[0] if len(targets) == 1 else None
    exit_step = None
    if judges and target is not None and judges[-1][1] is not None and judges[-1][1] >= target:
        exit_step = judges[-1][0]
    if '4' in bounds and exit_step is not None and bounds['4']['step'] != exit_step:
        fail('C4', f'PHASE 4 표지 step {bounds["4"]["step"]} ≠ 루프 탈출 판정 줄 step {exit_step}')
    if '4' not in bounds and exit_step is not None:
        bounds['4'] = {'step': exit_step, 'name': '(표지 없음 — 판정 줄 루프 탈출)', 'source': 'loop_exit', 'segment': judges[-1][3]}
    for r in rows:
        r['phase'] = _phase_at(bounds, r['step'])

    # ── C1 압력 열 · 유한 ──
    nopc = [r for r in rows if r['phase'] >= 2 and r['pcol'] is None]
    if nopc:
        fail('C1', f'단계 ≥ 2 의 thermo 에 압력 열 (v_pressMPa · pressMPa) 이 없다 — {nopc[0]["segment"]} step {nopc[0]["step"]} 외 {len(nopc) - 1}')
    nonfin = [r for r in rows if r['p_deck'] is not None and not math.isfinite(r['p_deck'])]
    if nonfin:
        fail('C1', f'비유한 압력 {len(nonfin)} 줄 — 첫 {nonfin[0]["segment"]} step {nonfin[0]["step"]}')
    if not any(r['p_deck'] is not None for r in rows):
        fail('C1', '압력 값이 한 줄도 없다')

    # ── C6 step 증가 ──
    bad6 = [(a['step'], b['step']) for a, b in zip(rows, rows[1:]) if b['step'] <= a['step']]
    if bad6:
        fail('C6', f'이은 뒤 step 이 엄격히 증가하지 않는다 — {bad6[:3]}')

    # ── C5 판 메시 ──
    meshes, mbad = read_meshes(mesh_dir)
    for m in mbad:
        fail('C5', m)
    if len(meshes) < 2:
        fail('C5', f'판 메시 mesh_<step>.stl 이 {len(meshes)} 장 — 두께 곡선을 만들 수 없다')
    mz = dict(meshes)
    b3 = bounds.get('3', {}).get('step')
    b4 = bounds.get('4', {}).get('step')
    speed = None
    if meshes and b3 is not None:
        ph2 = [z for s, z in meshes if _phase_at(bounds, s) == 2]
        if ph2 and max(ph2) - min(ph2) > Z_TOL:
            fail('C5', f'안정화 단계 (판 고정) 에서 판 z 가 변한다 — 폭 {max(ph2) - min(ph2):.3g} 덱 m')
        ph4 = [z for s, z in meshes if _phase_at(bounds, s) == 4]
        if ph4 and max(ph4) - min(ph4) > Z_TOL:
            fail('C5', f'이완 단계 (판 고정) 에서 판 z 가 변한다 — 폭 {max(ph4) - min(ph4):.3g} 덱 m (재부양 의심)')
        ph3 = [(s, z) for s, z in meshes if _phase_at(bounds, s) == 3]
        ups = [(a[0], b[0], b[1] - a[1]) for a, b in zip(ph3, ph3[1:]) if b[1] - a[1] > Z_TOL]
        if ups:
            fail('C5', f'압축 단계에서 판 z 가 오른다 — {ups[0][0]}→{ups[0][1]} +{ups[0][2]:.3g} 덱 m 외 {len(ups) - 1} (재부양 · 섞인 궤적)')
        if len(ph3) >= 3:
            xs = [s for s, _ in ph3]
            ys = [z for _, z in ph3]
            mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
            sxx = sum((x - mx) ** 2 for x in xs)
            slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
            res = max(abs(y - (my + slope * (x - mx))) for x, y in zip(xs, ys))
            speed = -slope * LDH.SIM_TO_UM * 1000.0
            if slope >= 0:
                fail('C5', f'압축 단계에서 판이 내려가지 않는다 (기울기 {slope:.3g})')
            if res > FIT_TOL:
                fail('C5', f'압축 단계 판 높이가 직선이 아니다 — 최대 잔차 {res:.3g} 덱 m > {FIT_TOL}')
            note('C5', f'압축 단계 메시 {len(ph3)} 장 · 직선 최대 잔차 {res:.3g} 덱 m')
    elif meshes:
        fail('C5', 'PHASE 3 경계를 몰라 판 메시를 단계별로 검사할 수 없다')

    # ── C3 판 높이 줄 · 잇는 자리 압력 ──
    for k, s in enumerate(segs):
        pl = [(st, z) for st, z in s['plates'] if st is not None and kept(k, st, inclusive_lo=True)]
        if k >= 1 and not pl:
            note('C3', f'{s["label"]}: PLATE HEIGHT 줄 없음 — 판 높이 대조 못 함 (압력 붕괴 검사 · C5 메시 검사로만 본다)')
        for st, z in pl:
            if z is None:
                fail('C3', f'{s["label"]} PLATE HEIGHT 값을 못 읽었다 (step {st})')
                continue
            ref, how = mz.get(st), f'mesh_{st}'
            if ref is None:
                # 같은 step 메시가 없으면 다음 메시 — 단 그 사이에 판이 움직이지 않을 때만 (압축 구간 (b3, b4] 과 안 겹침)
                nxt = next(((ms, mzv) for ms, mzv in meshes if ms > st), None)
                if nxt and (b3 is None or nxt[0] <= b3 or (b4 is not None and st >= b4)):
                    ref, how = nxt[1], f'mesh_{nxt[0]} (판 고정 구간)'
            if ref is None:
                note('C3', f'{s["label"]} PLATE HEIGHT {z} (step {st}) — 같은 step 메시가 없어 대조 못 함')
            elif abs(z - ref) > Z_TOL:
                fail('C3', f'{s["label"]} PLATE HEIGHT {z} ≠ {how} z {ref} (Δ {z - ref:+.6g} 덱 m) — 재시작이 판을 다른 높이에 놓았다')
            else:
                note('C3', f'{s["label"]} PLATE HEIGHT {z} = {how}')
    splices = []
    for k in range(1, n):
        prev_rows = [r for r in rows if r['k'] == k - 1 and r['p_deck'] is not None]
        next_rows = [r for r in rows if r['k'] == k and r['p_deck'] is not None][:COLLAPSE_ROWS]
        p_prev = prev_rows[-1]['p_deck'] if prev_rows else None
        p_next = max((r['p_deck'] for r in next_rows), default=None)
        splices.append({'restart_step': starts[k], 'segment': segs[k]['label'],
                        'p_before_mpa': None if p_prev is None else p_prev * PU.SIM_TO_MPA,
                        'p_after_max_first_mpa': None if p_next is None else p_next * PU.SIM_TO_MPA})
        if (p_prev is not None and p_next is not None and target and p_prev >= COLLAPSE_MIN_FRAC * target
                and p_next < COLLAPSE_RATIO * p_prev):
            fail('C3', f'잇는 자리 {starts[k]} 압력 붕괴 — 앞 {p_prev * PU.SIM_TO_MPA:.4g} MPa → 뒤 첫 {len(next_rows)} 줄 최대 '
                       f'{p_next * PU.SIM_TO_MPA:.4g} MPa (판 재부양 증상)')

    zplane = segs[0]['zplane']
    summary = {
        'schema': SCHEMA, 'status': 'OK' if not why else 'REFUSED', 'why': why, 'checks': checks,
        'segments': [{'label': s['label'], 'path': s['path'], 'sha256': s['sha256'], 'size': s['size'],
                      'first_step': s['first'], 'last_step': s['last'], 'read_restart': s['restarts'],
                      'kept_after': None if k == 0 else starts[k], 'kept_through': None if k == n - 1 else starts[k + 1],
                      'n_blocks': len(s['blocks']), 'n_incomplete_blocks': sum(1 for b in s['blocks'] if not b['complete']),
                      'n_other_lines_in_blocks': sum(b['n_other'] for b in s['blocks']),
                      'n_rows_kept': sum(1 for r in rows if r['k'] == k)} for k, s in enumerate(segs)],
        'n_setup_lines_dropped': n_setup, 'phase_bounds': bounds, 'splices': splices,
        'target_mpa': None if target is None else target * PU.SIM_TO_MPA, 'reached': exit_step is not None,
        'loop_exit_step': exit_step, 'n_judge_lines': len(judges),
        'mesh': {'dir': mesh_dir, 'n': len(meshes), 'first_step': meshes[0][0] if meshes else None,
                 'last_step': meshes[-1][0] if meshes else None,
                 'digest': hashlib.sha256(''.join(f'{s}:{z!r};' for s, z in meshes).encode()).hexdigest()},
        'plate_speed_um_per_1000step': speed,
        'floor_zplane_deck': 0.0 if zplane is None else zplane,
        'floor_source': 'assumed 0 (로그에 wall/gran zplane 없음)' if zplane is None else 'log wall/gran zplane',
        'units': {'pressure_mpa': 'thermo 압력 열 (덱) × 1000 (press_units.SIM_TO_MPA)',
                  'thickness_um': '(판 메시 z − zplane) (덱 m) × 1000 (lhs_descriptor_harvest.SIM_TO_UM) — 판 위치',
                  'x': 'step (thermo step · 메시 파일 이름)'},
    }
    if why:
        return summary, [], []
    floor = summary['floor_zplane_deck']
    prow = [{'step': r['step'], 'phase': r['phase'], 'segment': r['segment'],
             'pressure_mpa': '' if r['p_deck'] is None else repr(r['p_deck'] * PU.SIM_TO_MPA)} for r in rows]
    zrow = [{'step': s, 'phase': _phase_at(bounds, s), 'plate_z_deck': repr(z),
             'thickness_um': repr((z - floor) * LDH.SIM_TO_UM)} for s, z in meshes]
    pv = [r['p_deck'] * PU.SIM_TO_MPA for r in rows if r['p_deck'] is not None]
    summary.update(n_pressure_rows=len(pv), max_pressure_mpa=max(pv), last_pressure_mpa=pv[-1],
                   thickness_first_um=(meshes[0][1] - floor) * LDH.SIM_TO_UM,
                   thickness_last_um=(meshes[-1][1] - floor) * LDH.SIM_TO_UM)
    return summary, prow, zrow


def _refused(segs, why, checks):
    return {'schema': SCHEMA, 'status': 'REFUSED', 'why': why, 'checks': checks,
            'segments': [{'label': s['label'], 'path': s['path'], 'sha256': s['sha256']} for s in segs]}


def _write_csv(path, rows, cols):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main(argv=None):
    ap = argparse.ArgumentParser(description='DEM 압밀 곡선 — LIGGGHTS 로그 thermo + 판 메시 → step 별 압력 · 판 높이 (읽기 전용)')
    ap.add_argument('--segment', action='append', required=True,
                    help='로그 (궤적 순서대로 반복) — 뒤 조각은 자기 첫 step 뒤부터 앞 조각을 대신한다.  주지 않은 로그는 안 쓴다')
    ap.add_argument('--mesh-dir', required=True, help='판 메시 덤프 mesh_<step>.stl 폴더 (post_…)')
    ap.add_argument('--out', required=True, help='산출 폴더 — 없거나 비어 있어야 한다')
    ap.add_argument('--press-col', default=None, help='압력 열 이름 (기본: v_pressMPa · pressMPa 자동)')
    a = ap.parse_args(argv)
    if os.path.exists(a.out) and (not os.path.isdir(a.out) or os.listdir(a.out)):
        print(f'⛔ --out {a.out} 가 비어 있지 않다 — 새 폴더를 준다 (옛 산출을 덮지 않는다)', file=sys.stderr)
        return 2
    for p in a.segment:
        if not os.path.isfile(p):
            print(f'⛔ 로그 없음: {p}', file=sys.stderr)
            return 2
    summary, prow, zrow = build(a.segment, a.mesh_dir, a.press_col)
    os.makedirs(a.out, exist_ok=True)
    if summary['status'] == 'OK':
        _write_csv(os.path.join(a.out, 'pressure.csv'), prow, ['step', 'phase', 'segment', 'pressure_mpa'])
        _write_csv(os.path.join(a.out, 'plate.csv'), zrow, ['step', 'phase', 'plate_z_deck', 'thickness_um'])
    with open(os.path.join(a.out, 'curve_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    if summary['status'] != 'OK':
        print('⛔ REFUSED')
        for w in summary['why']:
            print('   ' + w)
        return 2
    b = summary['phase_bounds']
    print(f'OK · 압력 {summary["n_pressure_rows"]} 줄 · 판 메시 {summary["mesh"]["n"]} 장 · 설정 줄 버림 {summary["n_setup_lines_dropped"]}')
    print('   단계 경계 ' + ' · '.join(f'{k}={v["step"]} ({v["source"]})' for k, v in sorted(b.items())))
    print(f'   두께 {summary["thickness_first_um"]:.3f} → {summary["thickness_last_um"]:.3f} µm · 최대 압력 {summary["max_pressure_mpa"]:.2f} MPa · '
          f'목표 {summary["target_mpa"]} MPa · 도달 {summary["reached"]} · 판 하강 {summary["plate_speed_um_per_1000step"]} µm/1,000 step')
    for sp in summary['splices']:
        print(f'   잇는 자리 {sp["restart_step"]} ({sp["segment"]}) — 앞 {sp["p_before_mpa"]} MPa · 뒤 첫 줄들 최대 {sp["p_after_max_first_mpa"]} MPa')
    return 0


if __name__ == '__main__':
    sys.exit(main())
