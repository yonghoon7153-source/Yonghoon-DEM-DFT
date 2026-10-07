#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ps73 감쇠 가지 런 하나를 읽는다 — 두께 · 공극률 (ε_sphere) · 감쇠 저항 · 판 압력 (읽기 전용 · 표준 라이브러리만).

    python3 docs/data/ps73_damping_branch_20261007/analyze_branch.py <런 폴더>           # 화면 표 + <런 폴더>/analysis_branch.json
    python3 docs/data/ps73_damping_branch_20261007/analyze_branch.py <런 폴더> --force   # 있는 json 을 새로 쓴다
    python3 docs/data/ps73_damping_branch_20261007/analyze_branch.py --selftest

정의 (README §5 와 같다):
  두께      = 판 높이 − 바닥 (덱 `zplane 0.0`) · 판 높이 = 그 상태 폴더 mesh_<step>.stl 꼭짓점 z (평평해야 한다 · 1e-12 m)
  ε_sphere  = 1 − Σ (4/3)π r³ / (lx · ly · 판 높이) — 웹앱 eps_sphere_web 과 같은 정의 (구 부피 합 · 겹침을 빼지 않는다)
  감쇠 저항 = −γ Σ v_z (덱 N · fix viscous 는 F = −γ v · 질량과 무관) · 몫 = 저항 ÷ 750 N (= 0.30 덱 MPa × 0.0025 m²)
              γ = 그 상태에서 켜져 있던 값: stop = arm 의 압축 감쇠 (요약 gamma_comp) · end · end_relax = 1e-5
  판 압력   = 요약 · 기록의 press_deckMPa × 1000 (실제 MPa · 덱 축척 P × 0.001)
⚠ 길이 · 힘은 덱 단위 그대로 (길이 × 1000 = µm) · 원자 덤프는 데이터로만 읽는다.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import tempfile

F_TARGET_N = 750.0
GAMMA_RELAX = 1.0e-5
FLAT_TOL = 1e-12


def read_summary(run: str) -> dict:
    out = {}
    p = os.path.join(run, 'branch_summary.txt')
    if not os.path.exists(p):
        return out
    with open(p, encoding='utf-8', errors='replace') as f:
        for ln in f:
            ln = ln.strip()
            if '=' in ln:
                k, v = ln.split('=', 1)
                out[k.strip()] = v.strip()          # 마지막 줄이 이긴다 (가드는 덧붙인다)
    return out


def read_mesh_z(path: str):
    zs = []
    with open(path, encoding='utf-8', errors='replace') as f:
        for ln in f:
            w = ln.split()
            if len(w) == 4 and w[0] == 'vertex':
                zs.append(float(w[3]))
    if not zs:
        raise ValueError(f'꼭짓점이 없다: {path}')
    lo, hi = min(zs), max(zs)
    return lo, hi


def read_atoms(path: str) -> dict:
    """원자 덤프 한 장 → 상자 · 종류별 개수 · Σ r³ · Σ v_z (줄 단위로 읽는다 · 21 MB 급)."""
    n = 0
    by_type = {}
    sum_r3 = 0.0
    sum_vz = 0.0
    box = []
    cols = None
    step = None
    with open(path, encoding='utf-8', errors='replace') as f:
        it = iter(f)
        for ln in it:
            if ln.startswith('ITEM: TIMESTEP'):
                step = int(next(it).split()[0])
            elif ln.startswith('ITEM: BOX BOUNDS'):
                for _ in range(3):
                    lo, hi = next(it).split()[:2]
                    box.append((float(lo), float(hi)))
            elif ln.startswith('ITEM: ATOMS'):
                cols = ln.split()[2:]
                need = ('type', 'radius', 'vz')
                if not all(c in cols for c in need):
                    raise ValueError(f'열 {need} 이 없다: {cols}')
                it_, ir, iv = (cols.index(c) for c in need)
                for row in it:
                    w = row.split()
                    if len(w) != len(cols):
                        if row.startswith('ITEM:'):
                            raise ValueError(f'덤프에 프레임이 둘 이상이다: {path}')
                        continue
                    t = int(float(w[it_]))
                    r = float(w[ir])
                    by_type[t] = by_type.get(t, 0) + 1
                    sum_r3 += r ** 3
                    sum_vz += float(w[iv])
                    n += 1
    if cols is None or len(box) != 3:
        raise ValueError(f'원자 덤프 머리가 없다: {path}')
    return dict(step=step, n=n, by_type=by_type, sum_r3=sum_r3, sum_vz=sum_vz, box=box)


def pick(dirpath: str, prefix: str, ext: str, step=None):
    if not os.path.isdir(dirpath):
        return None
    names = sorted(x for x in os.listdir(dirpath) if x.startswith(prefix) and x.endswith(ext))
    if step is not None:
        want = f'{prefix}{step}{ext}'
        return os.path.join(dirpath, want) if want in names else None
    return os.path.join(dirpath, names[-1]) if len(names) == 1 else None


def state_metrics(run: str, state: str, step, gamma: float) -> dict:
    d = os.path.join(run, state)
    ap = pick(d, 'atom_', '.liggghts', step)
    mp = pick(d, 'mesh_', '.stl', step)
    if not ap or not mp:
        return dict(state=state, status='MISSING', note=f'{state}/ 의 atom_·mesh_ 를 못 찾았다 (step {step})')
    a = read_atoms(ap)
    zlo, zhi = read_mesh_z(mp)
    out = dict(state=state, status='OK', atom_file=os.path.relpath(ap, run), mesh_file=os.path.relpath(mp, run),
               step=a['step'], n_atoms=a['n'], n_by_type={str(k): v for k, v in sorted(a['by_type'].items())})
    if zhi - zlo > FLAT_TOL:
        out['status'] = 'CHECK'
        out['note'] = f'판이 평평하지 않다 (z {zlo} … {zhi})'
    lx = a['box'][0][1] - a['box'][0][0]
    ly = a['box'][1][1] - a['box'][1][0]
    pz = 0.5 * (zlo + zhi)
    v_solid = 4.0 / 3.0 * math.pi * a['sum_r3']
    out.update(plate_z_deck=pz, thickness_um=pz * 1000.0, box_x_deck=lx, box_y_deck=ly,
               solid_volume_deck=v_solid, eps_sphere_pct=100.0 * (1.0 - v_solid / (lx * ly * pz)),
               gamma=gamma, drag_N=-gamma * a['sum_vz'], drag_share_of_750N_pct=100.0 * (-gamma * a['sum_vz']) / F_TARGET_N)
    return out


def trace_metrics(run: str) -> dict:
    p = os.path.join(run, 'branch_trace.csv')
    if not os.path.exists(p):
        return {}
    rows = []
    with open(p, encoding='utf-8', errors='replace') as f:
        for r in csv.DictReader(f):
            try:
                rows.append(dict(step=int(float(r['step'])), phase=r['phase'], plate_z=float(r['plate_z_deck']),
                                 press=float(r['press_deckMPa']), ke=float(r['ke_J']), atoms=int(float(r['atoms'])),
                                 leak=int(float(r['leak_delta']))))
            except (KeyError, ValueError):
                continue
    if not rows:
        return {}
    hold = [r for r in rows if r['phase'] == 'hold']
    comp = [r for r in rows if r['phase'] == 'comp']
    out = dict(n_rows=len(rows), n_comp_chunks=len(comp), n_hold_chunks=len(hold),
               atoms_min=min(r['atoms'] for r in rows), leak_delta_max=max(r['leak'] for r in rows))
    if comp:
        out['comp_ke_max_J'] = max(r['ke'] for r in comp)
    if hold:
        out['hold_ke_max_first10_J'] = max(r['ke'] for r in hold[:10])
        if len(hold) > 10:
            out['hold_ke_max_after10_J'] = max(r['ke'] for r in hold[10:])
        out['hold_plate_z_first_deck'] = hold[0]['plate_z']
        out['hold_plate_z_last_deck'] = hold[-1]['plate_z']
        out['hold_press_last_MPa'] = hold[-1]['press'] * 1000.0
    return out


def analyze(run: str) -> dict:
    s = read_summary(run)
    gamma_comp = float(s.get('gamma_comp', 'nan'))
    res = dict(run=os.path.abspath(run), arm=s.get('arm'), result=s.get('result'), summary=s,
               definitions=__doc__.split('정의 (README §5 와 같다):')[1].split('⚠')[0].strip())
    st = []
    if s.get('stop_step'):
        st.append(state_metrics(run, 'stop', int(float(s['stop_step'])), gamma_comp))
    if os.path.isdir(os.path.join(run, 'end_relax')) and os.listdir(os.path.join(run, 'end_relax')):
        st.append(state_metrics(run, 'end_relax', None, GAMMA_RELAX))
    if s.get('end_step'):
        st.append(state_metrics(run, 'end', int(float(s['end_step'])), GAMMA_RELAX))
    res['states'] = st
    for k in ('stop_press_deckMPa', 'end_press_deckMPa'):
        if k in s:
            res[k.replace('_deckMPa', '_MPa')] = float(s[k]) * 1000.0
    ok = {x['state']: x for x in st if x.get('status') in ('OK', 'CHECK')}
    if 'stop' in ok and 'end' in ok:
        res['delta_thickness_um_end_minus_stop'] = ok['end']['thickness_um'] - ok['stop']['thickness_um']
        res['delta_eps_pct_end_minus_stop'] = ok['end']['eps_sphere_pct'] - ok['stop']['eps_sphere_pct']
    res['trace'] = trace_metrics(run)
    return res


def show(res: dict):
    print(f"  분석 arm={res.get('arm')} result={res.get('result')}")
    for x in res['states']:
        if x.get('status') == 'MISSING':
            print(f"    {x['state']:>9}: {x['note']}")
            continue
        print(f"    {x['state']:>9}: step {x['step']} · 두께 {x['thickness_um']:.3f} µm · ε_sphere {x['eps_sphere_pct']:.3f} % · "
              f"원자 {x['n_atoms']} · 감쇠 저항 {x['drag_N']:.4g} N ({x['drag_share_of_750N_pct']:.2f} % · γ {x['gamma']:g})"
              + (f"  ⚠ {x['note']}" if x.get('note') else ''))
    for k in ('stop_press_MPa', 'end_press_MPa', 'delta_thickness_um_end_minus_stop', 'delta_eps_pct_end_minus_stop'):
        if k in res:
            print(f"    {k} = {res[k]:.4f}")


def main(argv=None):
    ap = argparse.ArgumentParser(description='ps73 감쇠 가지 런 분석 (읽기 전용)')
    ap.add_argument('run', nargs='?', help='런 폴더 (run_branch.sh 가 만든 <arm>_<시각>)')
    ap.add_argument('--force', action='store_true', help='있는 analysis_branch.json 을 새로 쓴다')
    ap.add_argument('--selftest', action='store_true', help='합성 런 폴더로 검사')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.run:
        ap.error('런 폴더를 주거나 --selftest')
    res = analyze(a.run)
    show(res)
    out = os.path.join(a.run, 'analysis_branch.json')
    if os.path.exists(out) and not a.force:
        print(f'  · {out} 가 이미 있다 — 새로 쓰지 않는다 (--force)')
        return 0
    with open(out, 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, indent=2, ensure_ascii=False) + '\n')
    print(f'  → {out}')
    return 0


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def _atom_dump(step, rows, box=((0.0, 0.05), (0.0, 0.05), (-0.01, 1.0))):
    head = (f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(rows)}\nITEM: BOX BOUNDS pp pp ff\n'
            + ''.join(f'{lo} {hi}\n' for lo, hi in box)
            + 'ITEM: ATOMS id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke\n')
    return head + ''.join(' '.join(str(v) for v in r) + '\n' for r in rows)


def _mesh(z, z2=None):
    z2 = z if z2 is None else z2
    return ('solid t\nfacet normal 0 0 -1\nouter loop\n'
            f'vertex 0 0 {z}\nvertex 0 0.05 {z}\nvertex 0.05 0.05 {z2}\nendloop\nendfacet\nendsolid t\n')


def selftest() -> int:
    fails = []

    def chk(name, ok, detail=''):
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory() as td:
        run = os.path.join(td, 'B_x')
        # 원자 셋: r 0.001 · 0.002 · 0.003 · v_z −0.004 · −0.002 · 0
        rows = [(1, 3, 0.01, 0.01, 0.01, 0.001, 0, 0, -0.004, 0, 0, 0, 0),
                (2, 2, 0.02, 0.02, 0.02, 0.002, 0, 0, -0.002, 0, 0, 0, 0),
                (3, 1, 0.03, 0.03, 0.03, 0.003, 0, 0, 0.0, 0, 0, 0, 0)]
        _write(os.path.join(run, 'stop', 'atom_3125000.liggghts'), _atom_dump(3125000, rows))
        _write(os.path.join(run, 'stop', 'mesh_3125000.stl'), _mesh(0.1))
        _write(os.path.join(run, 'end', 'atom_3800000.liggghts'), _atom_dump(3800000, rows))
        _write(os.path.join(run, 'end', 'mesh_3800000.stl'), _mesh(0.095))
        _write(os.path.join(run, 'branch_summary.txt'),
               'arm=B\ngamma_comp=0.5\nstop_step=3125000\nstop_press_deckMPa=0.301\nend_step=3800000\n'
               'end_press_deckMPa=0.2995\nresult=DONE\n')
        _write(os.path.join(run, 'branch_trace.csv'),
               'step,phase,plate_z_deck,press_deckMPa,force_N,ke_J,atoms,leak_delta\n'
               '3105000,comp,0.11125,0.297,743,1.7e-05,160420,0\n'
               '3130000,hold,0.11100,0.20,500,0.05,160418,2\n')
        res = analyze(run)
        st = {x['state']: x for x in res['states']}
        v = 4.0 / 3.0 * math.pi * (0.001 ** 3 + 0.002 ** 3 + 0.003 ** 3)
        chk('ε_sphere = 1 − Σ구 부피 / (lx·ly·판 높이)',
            abs(st['stop']['eps_sphere_pct'] - 100 * (1 - v / (0.05 * 0.05 * 0.1))) < 1e-9, st['stop'])
        chk('두께 µm = 판 z × 1000', abs(st['end']['thickness_um'] - 95.0) < 1e-9)
        chk('stop 감쇠 저항 = −γ Σ v_z (γ = gamma_comp 0.5)', abs(st['stop']['drag_N'] - 0.5 * 0.006) < 1e-12, st['stop']['drag_N'])
        chk('end 감쇠 저항은 γ 1e-5', abs(st['end']['drag_N'] - 1e-5 * 0.006) < 1e-15)
        chk('두께 차 end − stop = −5 µm', abs(res['delta_thickness_um_end_minus_stop'] + 5.0) < 1e-9)
        chk('판 압력 실제 MPa = 덱 × 1000', abs(res['stop_press_MPa'] - 301.0) < 1e-9)
        chk('기록: 압축 1 · 유지 1 덩어리 · 원자 최소', res['trace']['n_comp_chunks'] == 1 and res['trace']['n_hold_chunks'] == 1
            and res['trace']['atoms_min'] == 160418)
        chk('종류별 개수', st['stop']['n_by_type'] == {'1': 1, '2': 1, '3': 1}, st['stop']['n_by_type'])
        # 평평하지 않은 판 → CHECK
        _write(os.path.join(run, 'end', 'mesh_3800000.stl'), _mesh(0.095, 0.0951))
        chk('판이 평평하지 않으면 CHECK', {x['state']: x for x in analyze(run)['states']}['end']['status'] == 'CHECK')
        # 없는 스냅숏 → MISSING (값 없음)
        os.remove(os.path.join(run, 'end', 'mesh_3800000.stl'))
        chk('스냅숏이 없으면 MISSING', {x['state']: x for x in analyze(run)['states']}['end']['status'] == 'MISSING')
        # 덮어쓰지 않는다
        main([run])
        before = open(os.path.join(run, 'analysis_branch.json'), encoding='utf-8').read()
        _write(os.path.join(run, 'branch_summary.txt'), 'arm=B\ngamma_comp=0.5\nstop_step=3125000\nresult=GUARD_TRIP\n')
        main([run])
        chk('analysis_branch.json 을 --force 없이 덮어쓰지 않는다',
            open(os.path.join(run, 'analysis_branch.json'), encoding='utf-8').read() == before)
        # 열이 빠진 덤프 → 거부
        _write(os.path.join(run, 'stop', 'atom_3125000.liggghts'),
               _atom_dump(3125000, rows).replace(' radius', ' rad'))
        try:
            analyze(run)
            chk('radius 열이 없으면 거부', False, '통과함')
        except ValueError:
            chk('radius 열이 없으면 거부', True)
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
