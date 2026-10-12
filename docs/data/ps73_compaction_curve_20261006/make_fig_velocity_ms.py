#!/usr/bin/env python3
"""ps_7_3_r45 시뮬레이션 시간 (ms)–판 속도 — Origin CSV · .ogs · 미리보기 PNG/SVG · key_numbers_velocity_ms.json (10-12).

1저자 10-12: 압력 그래프에 맞춘 시간–속도 그래프 (권고 Q4 = 압력 ms 판과 같은 x 축 · 같은 단계 점선 · Origin CSV · 비준) ·
*"그냥 40만 이후에 1e-5 일정하게 그리고 relaxation에서 그치면 되니까 괜찮을듯"*.

값 = 덱 설정 `variable press_speed equal 0.01` (덱 9 개 모두 — 원 덱 · .orig15000 · r2–r8 · log.liggghts 풀린 값 -0.01) =
0.01 덱 m/s → 실제 길이 환산 **0.01 mm/s (= 1 × 10⁻⁵ m/s)** (덱 길이 ×1000 ⇒ 덱 1 m = 실제 1 mm).
발표 · 보고 용어 = *plate velocity 0.01 mm/s* (1저자 10-12 · `docs/dem_governing_equations_background_20261011.md` §9-1).
판 메시 (`curve/plate.csv` · 5,000 step 간격) 로 확인한다: 안정화 · 이완 = 판 고정 · 압축 = 한 직선 (기울기 = 덱 속도) · 경계에서 끊김 없음.
x 축 = Simulation time (ms) = step × 1e-3 (축척 덱 시간 — 실제 압착 시간 아님 · README §5 · §7).

    python3 docs/data/ps73_compaction_curve_20261006/make_fig_velocity_ms.py             # 산출
    python3 docs/data/ps73_compaction_curve_20261006/make_fig_velocity_ms.py --selftest  # 검사 반례
"""
import csv
import json
import re
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_fig_ms as M  # noqa: E402  같은 폴더 — 같은 x 축 · 서식 · 단계 점선

SPEED_DECK = 0.01                 # 덱 m/s (덱 9 개 `variable press_speed equal 0.01`)
MM_PER_DECK_M = M.UM / 1000.0     # 덱 1 m = 실제 1000 µm = 1 mm
N_DECKS = 9                       # 원 덱 · .orig15000 · r2–r8 (README §1)
END_STEP = 3225000                # 런 끝 (README §4)
TOL_FIXED = 1e-9                  # 판 고정 구간 판 높이 차 (덱 m) — plate.csv 는 소수 6 자리라 고정이면 같은 값
TOL_RESID = 1e-6                  # 압축 직선 잔차 (덱 m) — 소수 6 자리 반올림 반폭 5e-7 + 여유
TOL_SLOPE_REL = 1e-3              # 압축 기울기 ↔ 덱 속도 (상대)
YLABEL = 'Plate velocity (mm/s)'
NAME = 'ps73_ms_plate_velocity'
SRC = {'noplate': 'no plate (0 by definition)', 'placed': 'plate placed (fixed)', 'fixed': 'plate fixed (mesh)',
       'start': 'compression start (deck press_speed)', 'end': 'compression end (deck press_speed)',
       'relax': 'relaxation (plate fixed · mesh)', 'last': 'end of run (plate fixed · mesh)'}


# ───────────────────────────── 읽기 · 검사 ─────────────────────────────
def deck_speed(text):
    """덱 → 판 속도 (덱 m/s).  move/mesh linear z 성분이 -${press_speed} 또는 숫자 · press_speed 변수 하나."""
    body = '\n'.join(ln.split('#', 1)[0] for ln in text.splitlines())
    body = re.sub(r'&\s*\n\s*', ' ', body)
    mv = re.findall(r'^\s*fix\s+\S+\s+\S+\s+move/mesh\s+mesh\s+\S+\s+linear\s+(\S+)\s+(\S+)\s+(\S+)', body, re.M)
    var = re.findall(r'^\s*variable\s+press_speed\s+equal\s+(\S+)', body, re.M)
    if not mv:
        raise ValueError('move/mesh linear 줄 없음')
    speeds = set()
    for vx, vy, vz in mv:
        if float(vx) != 0.0 or float(vy) != 0.0:
            raise ValueError(f'판이 옆으로 움직인다: {vx} {vy}')
        if vz == '-${press_speed}':
            if len(set(var)) != 1:
                raise ValueError(f'press_speed 변수 {var}')
            speeds.add(float(var[0]))
        else:
            speeds.add(-float(vz))
    if len(speeds) != 1:
        raise ValueError(f'판 속도가 여럿: {sorted(speeds)}')
    return speeds.pop()


def decks_in_tgz(tgz):
    out = {}
    with tarfile.open(tgz) as t:
        for m in t.getmembers():
            if m.isfile() and re.search(r'/input_ps_7_3_r45[^/]*\.liggghts(\.orig\d+)?$', m.name):
                out[m.name] = deck_speed(t.extractfile(m).read().decode('utf-8', 'replace'))
    return out


def read_plate(path):
    with open(path, newline='', encoding='utf-8') as f:
        return [(int(r['step']), int(r['phase']), float(r['plate_z_deck'])) for r in csv.DictReader(f)]


def check_plate(rows, b, speed=SPEED_DECK, every=M.DUMP_EVERY):
    """판 메시 ↔ 단계 경계 · 덱 속도.  문제가 있으면 ValueError (전부 모아서)."""
    prob = []
    steps = [s for s, _, _ in rows]
    if not steps or steps != sorted(set(steps)):
        raise ValueError('step 이 엄격 증가가 아님')
    if any(s2 - s1 != every for s1, s2 in zip(steps, steps[1:])):
        prob.append(f'step 간격 ≠ {every} (빠진 메시)')
    if steps[-1] != b['5']:
        prob.append(f'마지막 메시 {steps[-1]} ≠ 런 끝 {b["5"]}')
    fixed2 = [z for s, _, z in rows if b['2'] <= s < b['3']]
    comp = [(s, z) for s, _, z in rows if b['3'] < s <= b['4']]
    relax = [z for s, _, z in rows if s > b['4']]
    if len(fixed2) < 2 or len(comp) < 3 or len(relax) < 2:
        raise ValueError(f'구간 점 수 부족: 안정화 {len(fixed2)} · 압축 {len(comp)} · 이완 {len(relax)}')
    if max(fixed2) - min(fixed2) > TOL_FIXED:
        prob.append(f'안정화 구간 판이 움직인다 (Δz {max(fixed2) - min(fixed2):.3g} 덱 m)')
    if max(relax) - min(relax) > TOL_FIXED:
        prob.append(f'이완 구간 판이 움직인다 (Δz {max(relax) - min(relax):.3g} 덱 m)')
    t = [s * 1e-6 for s, _ in comp]           # s (Δt 1e-6 — main 이 key_numbers.json 과 대조)
    z = [zz for _, zz in comp]
    n, tm, zm = len(t), sum(t) / len(t), sum(z) / len(z)
    slope = sum((a - tm) * (c - zm) for a, c in zip(t, z)) / sum((a - tm) ** 2 for a in t)
    icpt = zm - slope * tm
    resid = max(abs(c - (icpt + slope * a)) for a, c in zip(t, z))
    if abs(-slope - speed) > TOL_SLOPE_REL * speed:
        prob.append(f'압축 기울기 {-slope:.6g} 덱 m/s ≠ 덱 속도 {speed:g}')
    if resid > TOL_RESID:
        prob.append(f'압축 구간이 한 직선이 아님 (최대 잔차 {resid:.3g} 덱 m)')
    z_at_b3 = icpt + slope * b['3'] * 1e-6
    z_at_b4 = icpt + slope * b['4'] * 1e-6
    if abs(z_at_b3 - fixed2[-1]) > TOL_RESID:
        prob.append(f'압축 시작 {b["3"]} 에서 끊김 ({z_at_b3 - fixed2[-1]:.3g} 덱 m)')
    if abs(z_at_b4 - relax[0]) > TOL_RESID:
        prob.append(f'이완 시작 {b["4"]} 에서 끊김 ({z_at_b4 - relax[0]:.3g} 덱 m)')
    if prob:
        raise ValueError(' · '.join(prob))
    return {'n_mesh': len(rows), 'n_stabilization': len(fixed2), 'n_compression': n, 'n_relaxation': len(relax),
            'slope_deck_m_per_s': -slope, 'max_residual_deck_m': resid,
            'plate_z_stabilization_deck_m': fixed2[-1], 'plate_z_relaxation_deck_m': relax[0],
            'line_at_compression_start_minus_fixed_deck_m': z_at_b3 - fixed2[-1],
            'line_at_relaxation_start_minus_fixed_deck_m': z_at_b4 - relax[0]}


def velocity_series(b, speed=SPEED_DECK):
    """계단 선 (ms, mm/s, Source) — 0 ms 판 없음 · 판 놓음 · 압축 시작에서 0 → 속도 · 이완 시작에서 속도 → 0 · 런 끝."""
    v = speed * MM_PER_DECK_M
    ms = {k: b[k] * M.STEP_MS for k in ('2', '3', '4', '5')}
    return [(0.0, 0.0, SRC['noplate']), (ms['2'], 0.0, SRC['placed']), (ms['3'], 0.0, SRC['fixed']),
            (ms['3'], v, SRC['start']), (ms['4'], v, SRC['end']), (ms['4'], 0.0, SRC['relax']), (ms['5'], 0.0, SRC['last'])]


def yfmt(y, _pos=None):
    """보고 원칙 — 0 은 '0' (0.000 아님) · 나머지는 필요한 자리만."""
    return '0' if abs(y) < 1e-12 else f'{y:g}'


# ───────────────────────────── 산출 ─────────────────────────────
def main():
    key_old = json.loads((HERE / 'key_numbers.json').read_text(encoding='utf-8'))
    if key_old['x_axis']['dt_s'] != 1.0e-6:
        raise SystemExit(f'⛔ Δt 가 1e-6 s 가 아님: {key_old["x_axis"]["dt_s"]}')
    b = {k: int(v) for k, v in key_old['phase_bounds'].items()}
    if [b.get(k) for k in ('2', '3', '4')] != [200002, 400002, 3125000]:
        raise SystemExit(f'⛔ 단계 경계가 README §4 와 다름: {b}')
    rows = read_plate(M.CURVE / 'plate.csv')
    b['5'] = rows[-1][0]                       # 런 끝 = 마지막 판 메시 (key_numbers.json 에는 경계 넷뿐)
    if b['5'] != END_STEP:
        raise SystemExit(f'⛔ 마지막 판 메시 {b["5"]} ≠ 런 끝 {END_STEP} (README §4)')
    if abs(key_old['plate_speed_um_per_1000step'] - SPEED_DECK * 1e-3 * M.UM) > 1e-12:
        raise SystemExit(f'⛔ key_numbers.json 판 하강 {key_old["plate_speed_um_per_1000step"]} µm/1000 step ≠ 덱 속도 환산')
    decks = decks_in_tgz(M.LOGS_TGZ)
    if len(decks) != N_DECKS or set(decks.values()) != {SPEED_DECK}:
        raise SystemExit(f'⛔ 덱 판 속도: {decks}')
    chk = check_plate(rows, b)
    bounds_ms = [b['3'] * M.STEP_MS, b['4'] * M.STEP_MS]
    ser = velocity_series(b)
    M.ORIGIN.mkdir(exist_ok=True)
    M.PREV.mkdir(exist_ok=True)
    M.write_origin_csv(M.ORIGIN / f'{NAME}.csv', ['Simulation time', 'Plate velocity', 'Source'], ['ms', 'mm/s', ''],
                       [(f'{t:.3f}', f'{v:g}', s) for t, v, s in ser])
    (M.ORIGIN / f'{NAME}.ogs').write_text(
        M.ogs_text(NAME, '시뮬레이션 시간 (ms)–판 속도 · 0 ms 부터 · 덱 설정 0.01 = 0.01 mm/s', '112,48,160', 0, 0.015, 0.005,
                   YLABEL, bounds_ms), encoding='utf-8')
    M.draw_preview(ser, '#7030A0', YLABEL, (0, 0.015), 0.005, NAME, bounds_ms, settle_label_at='top', yfmt=yfmt)
    key = {'x_axis': {'label': M.XLABEL, 'time_ms': 'step × 1e-3', 'dt_s': 1.0e-6},
           'phase_bounds_step': b, 'phase_bounds_ms': {k: round(v * M.STEP_MS, 6) for k, v in b.items()},
           'velocity': {'deck_m_per_s': SPEED_DECK, 'real_mm_per_s': SPEED_DECK * MM_PER_DECK_M,
                        'real_m_per_s': SPEED_DECK * MM_PER_DECK_M * 1e-3,
                        'term': 'plate velocity 0.01 mm/s (1st author 10-12 · dem_governing_equations_background_20261011.md §9-1)',
                        'decks_checked': {Path(k).name: v for k, v in sorted(decks.items())}},
           'mesh_check': chk,
           'series': [{'ms': t, 'mm_per_s': v, 'source': s} for t, v, s in ser]}
    (HERE / 'key_numbers_velocity_ms.json').write_text(json.dumps(key, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'덱 {len(decks)} 개 판 속도 {SPEED_DECK} 덱 m/s = {SPEED_DECK * MM_PER_DECK_M:g} mm/s · '
          f'메시 {chk["n_mesh"]} 장 (안정화 {chk["n_stabilization"]} · 압축 {chk["n_compression"]} · 이완 {chk["n_relaxation"]}) · '
          f'압축 기울기 {chk["slope_deck_m_per_s"]:.6g} · 최대 잔차 {chk["max_residual_deck_m"]:.2e} 덱 m → {NAME}.*')


# ───────────────────────────── 자체시험 ─────────────────────────────
def selftest():
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        ok, fail = ok + bool(cond), fail + (not cond)
        print(('PASS ' if cond else 'FAIL ') + name)

    def raises(fn):
        try:
            fn()
        except (ValueError, KeyError):
            return True
        return False

    b = {'1': 1, '2': 200002, '3': 400002, '4': 3125000, '5': 3225000}
    z0 = 0.138302

    def good(speed=SPEED_DECK):
        out = []
        for s in range(205000, 3225001, 5000):
            ph = 2 if s <= 400000 else (3 if s <= 3125000 else 4)
            sc = min(max(s - b['3'], 0), b['4'] - b['3'])
            out.append((s, ph, round(z0 - speed * sc * 1e-6, 6)))
        return out

    st = check_plate(good(), b)
    chk('G1 정상 = 통과 · 기울기 · 잔차', abs(st['slope_deck_m_per_s'] - SPEED_DECK) < 1e-6 and st['max_residual_deck_m'] < TOL_RESID
        and (st['n_stabilization'], st['n_compression'], st['n_relaxation']) == (40, 545, 20))
    r = good()
    r[300] = (r[300][0], r[300][1], r[300][2] + 5e-6)
    chk('N1 압축 한 점 5e-6 덱 m 어긋남 = 거부 (한 직선 아님)', raises(lambda: check_plate(r, b)))
    chk('N2 덱 속도 0.02 로 눌린 메시 = 거부 (기울기)', raises(lambda: check_plate(good(0.02), b)))
    r = good()
    r[-3] = (r[-3][0], r[-3][1], r[-3][2] - 2e-6)
    chk('N3 이완 구간에서 판이 움직임 = 거부', raises(lambda: check_plate(r, b)))
    r = good()
    r[5] = (r[5][0], r[5][1], r[5][2] + 2e-6)
    chk('N4 안정화 구간에서 판이 움직임 = 거부', raises(lambda: check_plate(r, b)))
    r = good()
    del r[100]
    chk('N5 빠진 메시 = 거부', raises(lambda: check_plate(r, b)))
    b_late = dict(b, **{'3': 450002})
    chk('N6 압축 시작 경계가 메시와 다름 = 거부 (끊김)', raises(lambda: check_plate(good(), b_late)))
    deck_ok = 'variable press_speed equal 0.01\nfix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}\n'
    chk('D1 덱 속도 읽기 (변수)', deck_speed(deck_ok) == 0.01)
    chk('D2 덱 속도 읽기 (숫자 · 주석 무시)', deck_speed('# x\nfix m all move/mesh mesh top linear 0 0 -0.01 # y\n') == 0.01)
    chk('D3 속도 둘 = 거부', raises(lambda: deck_speed(deck_ok + 'fix m2 all move/mesh mesh top_mesh linear 0 0 -0.02\n')))
    chk('D4 옆으로 움직이는 판 = 거부', raises(lambda: deck_speed('fix m all move/mesh mesh top linear 0.001 0 -0.01\n')))
    ser = velocity_series(b)
    chk('S1 계단 선 7 점 · 400.002 → 3125 ms 만 0.01 mm/s',
        len(ser) == 7 and [v for _, v, _ in ser] == [0, 0, 0, 0.01, 0.01, 0, 0]
        and [t for t, _, _ in ser] == [0.0, 200.002, 400.002, 400.002, 3125.0, 3125.0, 3225.0])
    chk('S2 y 눈금 글자 0 → "0" · 0.005 · 0.01', [yfmt(v) for v in (0.0, 0.005, 0.01, 0.015)] == ['0', '0.005', '0.01', '0.015'])
    print(f'make_fig_velocity_ms selftest: {ok} PASS · {fail} FAIL')
    return fail == 0


if __name__ == '__main__':
    if '--selftest' in sys.argv[1:]:
        sys.exit(0 if selftest() else 1)
    main()
