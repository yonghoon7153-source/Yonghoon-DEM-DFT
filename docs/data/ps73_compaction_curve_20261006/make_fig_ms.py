#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ps_7_3_r45 압밀 곡선 ms 판 — 두께 = 원자 기준 (모든 원자의 max(z + r)) · 0 ms 부터 · 압력도 0 ms 부터 (1저자 10-08 밤).

    python3 docs/data/ps73_compaction_curve_20261006/make_fig_ms.py            # 그림 · Origin CSV · .ogs · key_numbers_ms.json
    python3 docs/data/ps73_compaction_curve_20261006/make_fig_ms.py --selftest

1저자 10-08 밤: *"mesh 의 높이가 아니고 atom 의 최대 높이로 0 초부터 msec 로"* · *"압력도 0 MPa 부터 다시"* · *"하나의 기준으로 해야지 —
mesh 기준도 있는 거고 atom 기준도 있는 거고"* · *"이번 보고는 atom 기준으로 하자"*.  ⇒ 두께는 **원자 기준 하나** — 판 높이로 원자를 거르지 않고
모형 곡선도 섞지 않는다 (판 기준 두께 = 옛 판 `make_fig.py` 그대로).  판 높이는 검사 · 기록에만 쓴다 (그림 값에는 안 들어간다).

두께 점 (CSV Source 열 · README §7):
  replay      — 1 · 1,000 step: 투입 재현 (원 덱 · 원 런과 같은 2 코어 · `early_ckpt/`) — 원 로그 KE 와 같아야 쓴다
  checkpoint  — 50,000 … 400,000 step (50 ms 마다) · 200,001 (정착 끝): 원 런 체크포인트를 `run 0` 으로 연 원자 덤프 — setup KE = 원 로그
  atom dump   — 405,000 … 3,225,000 step (5 ms 마다): 원 런 atom 덤프 565 장 (1저자 ibb 스캔 `raw/ps73_atom_top_20261008.csv`)
압력: 0 ms = 판 없음 → 0 MPa (정의상) · 그 뒤 = `curve/pressure.csv` 원값 · 슬라이드판 = 이완 모식 (`make_fig.py` 와 같은 식).
x 축 = Simulation time (ms) = step × 1e-3 (Δt = 1e-6 s · `key_numbers.json`) — 축척 덱의 시간이라 실제 압착 시간이 아니다.
"""
import csv
import json
import math
import re
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGS_TGZ = HERE / 'raw' / 'ps73_logs.tgz'
SCAN_CSV = HERE / 'raw' / 'ps73_atom_top_20261008.csv'
EARLY_CSV = HERE / 'raw' / 'ps73_early_atomtop_20261008.csv'
DECK_IN_TGZ = 'home/yonghoon/dem_test/ps45/ps_7_3_r45/input_ps_7_3_r45.liggghts'
R1_LOG_IN_TGZ = 'home/yonghoon/dem_test/ps45/logs/output_ps_7_3_r45_181338.out'
CURVE, ORIGIN, PREV = HERE / 'curve', HERE / 'origin', HERE / 'previews'

STEP_MS = 1.0e-3            # ms / step (Δt = 1e-6 s — key_numbers.json x_axis.dt_s 와 대조)
UM = 1000.0                 # µm / 덱 m (덱 길이 ×1000)
DUMP_EVERY = 5000           # 원 런 atom 덤프 간격
EARLY_STEPS = [1, 1000, 50000, 100000, 150000, 200000, 200001, 250000, 300000, 350000, 400000]
REPLAY_STEPS = (1, 1000)
#: 그림에서 뺄 점 (1저자 10-08 밤 — 100 ms 의 튀는 점 "보간": 빼고 앞뒤 점을 잇는다).  외톨이 확인 = 윗면 최댓값 − p99.9 ≥ OUTLIER_MIN_UM
#: (튀어 오른 입자 하나일 때만 뺀다 · 아니면 거부).  값은 원자료 CSV · key_numbers_ms.json 에 그대로 남긴다.
DROP_STEPS = {100000: 'bounced single particle (1st author: interpolate)'}
OUTLIER_MIN_UM = 20.0
KE_RTOL = 1e-6              # 재개 G1 규칙 — 체크포인트 · 재현 KE ↔ 원 로그 (상대)
INSERT_REF = ('160421', '9.005968e-01')   # 원 로그 투입 줄 (개수 · 질량)
X0, X1 = 0.0, 3250.0        # ms
XLABEL = 'Simulation time (ms)'
TARGET_MPA = 300.0
SLIDE_TAU_STEP = 15000      # make_fig.py 와 같은 그림용 이완 시간 상수
SCAN_HEAD = ['step', 'dump_timestep', 'n_header', 'n_rows', 'n_bad_lines', 'zc_max_deck_m', 'ztop_max_deck_m',
             'ztop_id', 'ztop_type', 'ztop_radius_deck_m', 'ztop_p999_deck_m', 'bytes', 'mtime']
EARLY_HEAD = ['step', 'dump_timestep', 'n_header', 'n_rows', 'n_bad_lines', 'zc_max_deck_m', 'ztop_max_deck_m', 'ztop_id',
              'ztop_type', 'ztop_radius_deck_m', 'ztop_p999_deck_m', 'log', 'log_atoms', 'log_ke']
SRC_REPLAY, SRC_CKPT, SRC_DUMP = 'replay (insertion · 2 cores)', 'checkpoint (run 0)', 'atom dump'
SRC_NOPLATE, SRC_THERMO, SRC_RELAX = 'no plate (0 by definition)', 'measured (thermo)', 'schematic relaxation'
SRC_INTERP = 'interpolated (PCHIP between measured points)'
INTERP_DT_MS = 1.0         # 앞 구간 곡선 채움 간격 (1저자 10-08 밤 *"초반 저 3 점 보간 · 곡선 형식으로"*)


# ───────────────────────────── 덱 · 로그 읽기 ─────────────────────────────
def deck_params(text):
    """원 덱 → {z_top_deck (투입 영역 위 끝), radii_deck} — 반경 검사 · 기록용."""
    body = '\n'.join(ln.split('#', 1)[0] for ln in text.splitlines())
    body = re.sub(r'&\s*\n\s*', ' ', body)
    reg = re.findall(r'^\s*region\s+reg_mix\s+block\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', body, re.M)
    if len(reg) != 1:
        raise ValueError(f'region reg_mix 가 {len(reg)} 개')
    radii = {k: float(v) for k, v in re.findall(r'^\s*variable\s+r_(AM_P|AM_S|SE)\s+equal\s+(\S+)', body, re.M)}
    if sorted(radii) != ['AM_P', 'AM_S', 'SE']:
        raise ValueError(f'반경 변수 {sorted(radii)}')
    return {'z_top_deck': float(reg[0][5]), 'radii_deck': radii}


def log_thermo_ke(text):
    """원 런 로그 → {step: (atoms, KE 글자)} — 머리에 KinEng 가 있는 thermo 블록만 (zmax 블록 제외) · 같은 step 은 처음 것."""
    out, on = {}, False
    for ln in text.splitlines():
        t = ln.split()
        if t[:2] == ['Step', 'Atoms']:
            on = 'KinEng' in t
            continue
        if on and len(t) >= 3 and t[0].isdigit() and t[1].isdigit():
            out.setdefault(int(t[0]), (int(t[1]), t[2]))
        elif on:
            on = False
    return out


def tgz_text(tgz, name):
    """tgz 안 파일 하나를 풀지 않고 읽는다 (경로를 쓰지 않으므로 경로 공격 없음 · 일반 파일만)."""
    with tarfile.open(tgz) as t:
        m = t.getmember(name)
        if not m.isfile():
            raise ValueError(f'{name} 이 일반 파일이 아님')
        return t.extractfile(m).read().decode('utf-8', errors='replace')


# ───────────────────────────── ibb 스캔 읽기 · 검사 ─────────────────────────────
def _typed(d):
    for k in ('step', 'dump_timestep', 'n_header', 'n_rows', 'n_bad_lines'):
        d[k] = int(d[k])
    for k in ('zc_max_deck_m', 'ztop_max_deck_m', 'ztop_radius_deck_m', 'ztop_p999_deck_m'):
        d[k] = float(d[k])
    return d


def read_scan(path):
    with open(path, newline='', encoding='utf-8') as f:
        rd = csv.reader(f)
        head = next(rd)
        if head != SCAN_HEAD:
            raise ValueError(f'스캔 CSV 머리가 다르다: {head}')
        rows = []
        for r in rd:
            if r:
                d = _typed(dict(zip(head, r)))
                d['bytes'] = int(d['bytes'])
                rows.append(d)
    return rows


def read_early(path):
    """앞 구간 CSV → (행들, 투입 줄).  끝의 `#insertion` 줄은 투입 기록으로 뺀다."""
    with open(path, newline='', encoding='utf-8') as f:
        rd = csv.reader(f)
        head = next(rd)
        if head != EARLY_HEAD:
            raise ValueError(f'앞 구간 CSV 머리가 다르다: {head}')
        rows, ins = [], None
        for r in rd:
            if not r:
                continue
            if r[0] == '#insertion':
                ins = r[1] if len(r) > 1 else ''
                continue
            d = _typed(dict(zip(head, r)))
            d['log_atoms'] = int(d['log_atoms']) if d['log_atoms'] != '' else None
            rows.append(d)
    return rows, ins


def _common(r, radii_deck, prob, tag):
    s = r['step']
    if r['dump_timestep'] != s:
        prob.append(f'{tag}② {s}: 덤프 TIMESTEP {r["dump_timestep"]}')
    if r['n_header'] != r['n_rows'] or r['n_bad_lines']:
        prob.append(f'{tag}③ {s}: 원자 수 머리 {r["n_header"]} · 줄 {r["n_rows"]} · 깨진 줄 {r["n_bad_lines"]}')
    if not (r['ztop_p999_deck_m'] <= r['ztop_max_deck_m'] and r['zc_max_deck_m'] <= r['ztop_max_deck_m']):
        prob.append(f'{tag}⑥ {s}: p99.9 {r["ztop_p999_deck_m"]} · 중심 {r["zc_max_deck_m"]} · 윗면 {r["ztop_max_deck_m"]}')
    if not any(abs(r['ztop_radius_deck_m'] - v) <= 1e-12 + 1e-9 * v for v in radii_deck.values()):
        prob.append(f'{tag}⑦ {s}: 맨 위 입자 반경 {r["ztop_radius_deck_m"]} ∉ 덱 반경 {sorted(radii_deck.values())}')


def check_scan(rows, first, last, radii_deck, plate_um, every=DUMP_EVERY):
    """원 런 atom 덤프 스캔 (원자 기준) — 문제 목록 (빈 목록 = 통과) · 통계.
    ① step = first … last 를 every 마다 빠짐 · 중복 없이 ② TIMESTEP = 파일 이름 ③ 머리 원자 수 = 줄 수 · 깨진 줄 0
    ④ 파일 시각이 step 순서로 단조 증가 (궤적 잇기) ⑥ p99.9 ≤ 최댓값 · 중심 ≤ 윗면 ⑦ 맨 위 입자 반경 = 덱 반경.
    원자 수가 줄어드는 것 · 맨 위가 판보다 높은 것은 **거부가 아니라 기록** (원자 기준 값은 그대로 그린다 · 1저자 *"하나의 기준"*)."""
    prob = []
    steps = [r['step'] for r in rows]
    want = list(range(first, last + 1, every))
    if steps != want:
        prob.append(f'① step 목록이 {first}…{last}/{every} 와 다르다 (빠짐 {sorted(set(want) - set(steps))[:5]} · '
                    f'남음 {sorted(set(steps) - set(want))[:5]} · 중복 {len(steps) - len(set(steps))})')
    for r in rows:
        _common(r, radii_deck, prob, '')
    mt = [r['mtime'] for r in rows]
    back = [(rows[i]['step'], mt[i], mt[i + 1]) for i in range(len(mt) - 1) if mt[i + 1] < mt[i]]
    if back:
        prob.append(f'④ 파일 시각이 거꾸로 가는 곳 {len(back)} — 처음 {back[:3]}')
    counts = [(rows[0]['step'], rows[0]['n_header'])] if rows else []
    counts += [(rows[i + 1]['step'], rows[i + 1]['n_header']) for i in range(len(rows) - 1)
               if rows[i + 1]['n_header'] != rows[i]['n_header']]
    on_plate = [r for r in rows if r['step'] in plate_um]
    contact = next((r['step'] for r in on_plate if r['ztop_max_deck_m'] * UM >= plate_um[r['step']]), None)
    esc = [r['step'] for r in on_plate if r['zc_max_deck_m'] * UM > plate_um[r['step']]]
    over = [(round(r['ztop_max_deck_m'] * UM - plate_um[r['step']], 3), r['step']) for r in on_plate]
    stats = {'n': len(rows), 'first_step': steps[0] if steps else None, 'last_step': steps[-1] if steps else None,
             'atom_count_changes': counts, 'first_step_top_reaches_plate': contact,
             'first_step_top_center_above_plate': esc[0] if esc else None, 'n_steps_top_center_above_plate': len(esc),
             'max_top_minus_plate_um': max(over) if over else None}
    return prob, stats


def check_early(rows, ins, ke_log, radii_deck):
    """앞 구간 (투입 재현 · 체크포인트 run 0) — ① step = EARLY_STEPS ②③⑥⑦ 공통 ⑤ 덤프 원자 수 = 그 로그 setup 원자 수
    ⑧ 로그 KE = 원 런 로그 그 step KE (상대 1e-6 · 재현 = 원 런 궤적 · 체크포인트 = 원 런 상태) ⑨ 투입 줄 = 원 로그 (개수 · 질량)."""
    prob = []
    steps = [r['step'] for r in rows]
    if steps != EARLY_STEPS:
        prob.append(f'E① step 목록 {steps} ≠ {EARLY_STEPS}')
    for r in rows:
        s = r['step']
        _common(r, radii_deck, prob, 'E')
        if r['log_atoms'] != r['n_header']:
            prob.append(f'E⑤ {s}: 덤프 원자 수 {r["n_header"]} ≠ 로그 {r["log_atoms"]}')
        ref = ke_log.get(s)
        try:
            ke = float(r['log_ke'])
        except ValueError:
            ke = None
        if ref is None or ke is None or abs(ke - float(ref[1])) > KE_RTOL * abs(float(ref[1])):
            prob.append(f'E⑧ {s}: KE {r["log_ke"]} ≠ 원 로그 {ref[1] if ref else "없음"}')
        elif ref[0] != r['n_header']:
            prob.append(f'E⑧ {s}: 원자 수 {r["n_header"]} ≠ 원 로그 {ref[0]}')
    if not ins or not all(x in ins for x in INSERT_REF):
        prob.append(f'E⑨ 투입 줄이 원 로그와 다르다: {ins!r} (기대 {INSERT_REF})')
    return prob


# ───────────────────────────── 곡선 만들기 ─────────────────────────────
def pchip(xs, ys, xq):
    """단조 3 차 Hermite (Fritsch–Carlson · 안쪽 기울기 = 가중 조화평균 · 끝 = 할선) — 매듭을 지나고, 구간마다 값이 그 구간 두 매듭 값 사이에 있다
    (넘침 없음).  scipy 없이 (그림 스크립트 의존 최소)."""
    import bisect
    n = len(xs)
    if n < 2 or any(b <= a for a, b in zip(xs, xs[1:])):
        raise ValueError('매듭 x 가 엄격히 증가해야 한다')
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    d = [(ys[i + 1] - ys[i]) / h[i] for i in range(n - 1)]
    m = [d[0]] + [0.0] * (n - 2) + [d[-1]]
    for i in range(1, n - 1):
        if d[i - 1] * d[i] > 0:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    out = []
    for x in xq:
        k = min(max(bisect.bisect_right(xs, x) - 1, 0), n - 2)
        t = (x - xs[k]) / h[k]
        out.append((2 * t ** 3 - 3 * t ** 2 + 1) * ys[k] + (t ** 3 - 2 * t ** 2 + t) * h[k] * m[k]
                   + (-2 * t ** 3 + 3 * t ** 2) * ys[k + 1] + (t ** 3 - t ** 2) * h[k] * m[k + 1])
    return out


def thickness_series(early_rows, scan_rows, drop=None, interp=True):
    """(t_ms, µm, 출처) — 원자 기준 하나: 재현 → 체크포인트 → 원 덤프 (값 = max(z + r) × 1000).
    drop = 뺄 step (DROP_STEPS) — 그 점이 외톨이 (최댓값 − p99.9 ≥ OUTLIER_MIN_UM) 일 때만 빼고, 아니면 거부한다."""
    drop = DROP_STEPS if drop is None else drop
    for r in early_rows + scan_rows:
        if r['step'] in drop and (r['ztop_max_deck_m'] - r['ztop_p999_deck_m']) * UM < OUTLIER_MIN_UM:
            raise ValueError(f"뺄 점 {r['step']} 이 외톨이가 아니다 (최댓값 − p99.9 = {(r['ztop_max_deck_m'] - r['ztop_p999_deck_m']) * UM:.3f} µm)")
    missing = set(drop) - {r['step'] for r in early_rows + scan_rows}
    if missing:
        raise ValueError(f'뺄 점이 자료에 없다: {sorted(missing)}')
    out = [(r['step'] * STEP_MS, r['ztop_max_deck_m'] * UM, SRC_REPLAY if r['step'] in REPLAY_STEPS else SRC_CKPT)
           for r in early_rows if r['step'] not in drop]
    out += [(r['step'] * STEP_MS, r['ztop_max_deck_m'] * UM, SRC_DUMP) for r in scan_rows if r['step'] not in drop]
    if interp and early_rows and scan_rows:                       # 앞 구간 (첫 점 → 첫 원 덤프) 을 측정점 사이 단조 곡선으로 채운다
        n_knot = sum(1 for _, _, s in out if s != SRC_DUMP) + 1
        xs, ys = [t for t, _, _ in out[:n_knot]], [y for _, y, _ in out[:n_knot]]
        known = set(xs)
        q = [k * INTERP_DT_MS for k in range(int(xs[0] // INTERP_DT_MS) + 1, int(xs[-1] / INTERP_DT_MS + 1e-9) + 1)
             if xs[0] < k * INTERP_DT_MS < xs[-1] and k * INTERP_DT_MS not in known]
        out = sorted(out + [(x, y, SRC_INTERP) for x, y in zip(q, pchip(xs, ys, q))], key=lambda p: p[0])
    if any(b[0] <= a[0] for a, b in zip(out, out[1:])):
        raise ValueError('두께 점의 시각이 엄격히 증가하지 않는다')
    return out


def pressure_series(prow):
    """make_fig.py 와 같은 원값 (phase ≥ 2 · 압력 있는 줄) 앞에 (0 ms, 0 MPa, 판 없음) 한 점."""
    px = [(int(r['step']), float(r['pressure_mpa'])) for r in prow if r['pressure_mpa'] != '' and int(r['phase']) >= 2]
    if not px or px[0][1] != 0.0:
        raise ValueError(f'판을 놓은 뒤 첫 압력이 0 이 아니다: {px[:1]}')
    return px, [(0.0, 0.0, SRC_NOPLATE)] + [(s * STEP_MS, p, SRC_THERMO) for s, p in px]


def slide_series(px, b4, tau_step=SLIDE_TAU_STEP):
    """make_fig.py 슬라이드판과 같은 식 — 압축 끝 (b4) 까지 원값 · 그 뒤 p_end + (p_c − p_end)·exp(−(s − b4)/τ) 를 1,000 step 마다."""
    comp = [(s, p) for s, p in px if s <= b4]
    if not comp or comp[-1][0] != b4:
        raise ValueError('판 정지 step 의 압력 줄이 없다')
    p_c, (s_end, p_end) = comp[-1][1], px[-1]
    sch = [(s, p_end + (p_c - p_end) * math.exp(-(s - b4) / tau_step)) for s in range(b4 + 1000, s_end + 1, 1000)]
    return ([(0.0, 0.0, SRC_NOPLATE)] + [(s * STEP_MS, p, SRC_THERMO) for s, p in comp]
            + [(s * STEP_MS, p, SRC_RELAX) for s, p in sch]), sch


# ───────────────────────────── 산출 ─────────────────────────────
def write_origin_csv(path, head, units, rows):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(head)
        w.writerow(units)
        w.writerows(rows)


def ogs_text(name, what, color, y_from, y_to, y_inc, ylabel, bounds_ms, target=None):
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
    return (f'// {name}.ogs — ps_7_3_r45 압밀 곡선 ({what})\n'
            f'// 사용: {name}.csv 를 가져온 워크북을 활성으로 두고 Script Window 에 붙여 넣기 → Enter.\n'
            '// 결과: 새 그래프 + BML 서식 · 단계 경계 점선 둘 (압축 시작 400.002 ms · 이완 시작 3125 ms).  C 열 (Source) 은 그리지 않는다.\n'
            'string bk$ = %H;\n'
            'plotxy iy:=[%(bk$)]1!(1,2) plot:=200 ogl:=<new>;\n'
            f'set %C -c color({color}); set %C -w 1500;\n' + ax +
            f'layer.y.from = {y_from:g}; layer.y.to = {y_to:g}; layer.y.inc = {y_inc:g}; layer.y.minor = 1;\nlabel -yl {ylabel};\n' + vb + tgt)


def draw_preview(series, color, ylabel, ylim, ystep, name, bounds_ms, target=None, settle_label_at='top', marker_sources=()):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator
    gray, light = '#404040', '#9AA0A8'
    plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11, 'axes.edgecolor': gray, 'axes.labelcolor': gray,
                         'xtick.color': gray, 'ytick.color': gray, 'axes.linewidth': 1.0, 'xtick.direction': 'out',
                         'ytick.direction': 'out', 'xtick.major.size': 5, 'ytick.major.size': 5, 'xtick.minor.size': 2.5,
                         'ytick.minor.size': 2.5, 'xtick.minor.visible': True, 'ytick.minor.visible': True,
                         'axes.labelsize': 12.5, 'svg.hashsalt': 'ps73ms'})
    fig, ax = plt.subplots(figsize=(4.3, 3.35))
    ax.tick_params(top=False, right=False, which='both')
    ax.plot([t for t, _, _ in series], [y for _, y, _ in series], '-', color=color, lw=1.6)
    mk = [(t, y) for t, y, s in series if s in marker_sources]
    if mk:
        ax.plot([t for t, _ in mk], [y for _, y in mk], 'o', color=color, ms=3.2, mew=0)
    for t in bounds_ms:
        ax.axvline(t, color=light, lw=0.9, ls=':')
    y_top = ylim[1] - 0.04 * (ylim[1] - ylim[0])
    y_bot = ylim[0] + 0.04 * (ylim[1] - ylim[0])
    b3, b4 = bounds_ms
    if target is not None:
        ax.axhline(target, color=gray, lw=0.9, ls='--')
        ax.text(b3 + 60, target + 5, 'Target 300 MPa', fontsize=9, color=gray, va='bottom')
    ys = y_top if settle_label_at == 'top' else y_bot
    va = 'top' if settle_label_at == 'top' else 'bottom'
    ax.text(b3 / 2, ys, 'Settling', rotation=90, fontsize=8.5, color=light, ha='center', va=va)   # 정착 + 안정화 (0 → 400.002 ms)
    ax.text((b3 + b4) / 2, y_top, 'Compression', fontsize=9, color=light, ha='center', va='top')
    ax.text(min((b4 + X1) / 2, X1 - 30), y_top, 'Relaxation', rotation=90, fontsize=8.5, color=light, ha='center', va='top')
    ax.set_xlim(X0, X1)
    ax.set_ylim(*ylim)
    ax.xaxis.set_major_locator(MultipleLocator(1000))
    ax.xaxis.set_minor_locator(MultipleLocator(500))
    ax.yaxis.set_major_locator(MultipleLocator(ystep))
    ax.yaxis.set_minor_locator(MultipleLocator(ystep / 2))
    ax.set_xlabel(XLABEL)
    ax.set_ylabel(ylabel)
    fig.tight_layout(pad=0.4)
    fig.savefig(PREV / f'{name}.png', dpi=300)
    fig.savefig(PREV / f'{name}.svg', metadata={'Date': None})
    plt.close(fig)


def main():
    key_old = json.loads((HERE / 'key_numbers.json').read_text(encoding='utf-8'))
    if key_old['x_axis']['dt_s'] != 1.0e-6:
        raise SystemExit(f'⛔ Δt 가 1e-6 s 가 아님: {key_old["x_axis"]["dt_s"]}')
    b = {k: int(v) for k, v in key_old['phase_bounds'].items()}
    bounds_ms = [b['3'] * STEP_MS, b['4'] * STEP_MS]   # 정착 + 안정화 = 한 구간 (1저자 10-08 밤 *"settling stabilization 합쳐서"*) · 경계 = 압축 시작 · 이완 시작
    deck = deck_params(tgz_text(LOGS_TGZ, DECK_IN_TGZ))
    ke_log = log_thermo_ke(tgz_text(LOGS_TGZ, R1_LOG_IN_TGZ))
    with open(CURVE / 'pressure.csv', newline='', encoding='utf-8') as f:
        prow = list(csv.DictReader(f))
    with open(CURVE / 'plate.csv', newline='', encoding='utf-8') as f:
        plate_um = {int(r['step']): float(r['thickness_um']) for r in csv.DictReader(f)}
    for p in (ORIGIN, PREV):
        p.mkdir(exist_ok=True)

    px, pser = pressure_series(prow)
    sl, _ = slide_series(px, b['4'])
    write_origin_csv(ORIGIN / 'ps73_ms_pressure.csv', ['Simulation time', 'Pressure', 'Source'], ['ms', 'MPa', ''],
                     [(f'{t:.3f}', f'{p:.4f}', s) for t, p, s in pser])
    write_origin_csv(ORIGIN / 'ps73_ms_pressure_slide.csv', ['Simulation time', 'Pressure', 'Source'], ['ms', 'MPa', ''],
                     [(f'{t:.3f}', f'{p:.4f}', s) for t, p, s in sl])
    (ORIGIN / 'ps73_ms_pressure.ogs').write_text(
        ogs_text('ps73_ms_pressure', '시뮬레이션 시간 (ms)–압력 · 0 ms 부터', '241,64,64', 0, 330, 100, 'Pressure (MPa)', bounds_ms, TARGET_MPA),
        encoding='utf-8')
    draw_preview(pser, '#F14040', 'Pressure (MPa)', (0, 330), 100, 'ps73_ms_pressure', bounds_ms, TARGET_MPA, settle_label_at='bottom')
    draw_preview(sl, '#F14040', 'Pressure (MPa)', (0, 330), 100, 'ps73_ms_pressure_slide', bounds_ms, TARGET_MPA, settle_label_at='bottom')
    key = {'x_axis': {'label': XLABEL, 'time_ms': 'step × 1e-3', 'dt_s': 1.0e-6,
                      'note': 'scaled deck time (r×1000 · E×0.001) — not the real pressing time (README §5)'},
           'phase_bounds_ms': {'settling_incl_stabilization': 0.0, 'compression': bounds_ms[0], 'relaxation': bounds_ms[1],
                               'plate_placed_not_drawn': b['2'] * STEP_MS},
           'pressure': {'n_points': len(pser), 'prepended': [0.0, 0.0, SRC_NOPLATE],
                        'slide_relax_tau_step': SLIDE_TAU_STEP, 'slide_end_value_mpa': px[-1][1]},
           'deck': {'z_top_deck': deck['z_top_deck'], 'radii_deck': deck['radii_deck']}}

    if not SCAN_CSV.exists():
        raise SystemExit(f'⛔ 원 덤프 스캔 CSV 없음: {SCAN_CSV.relative_to(HERE)}')
    rows = read_scan(SCAN_CSV)
    first = (b['3'] // DUMP_EVERY + 1) * DUMP_EVERY
    prob, stats = check_scan(rows, first, max(plate_um), deck['radii_deck'], plate_um)
    if prob:
        raise SystemExit('⛔ 원 덤프 스캔 거부 — ' + ' | '.join(prob[:8]) + (f' … 외 {len(prob) - 8}' if len(prob) > 8 else ''))
    key['scan'] = stats
    if not EARLY_CSV.exists():
        key['thickness'] = {'status': 'WAITING_EARLY', 'needs': str(EARLY_CSV.relative_to(HERE))}
        print(f'⏸ 두께 = 앞 구간 CSV 대기 ({EARLY_CSV.relative_to(HERE)}) — 압력 그림 · 원 덤프 스캔 검사만')
    else:
        erows, ins = read_early(EARLY_CSV)
        eprob = check_early(erows, ins, ke_log, deck['radii_deck'])
        if eprob:
            raise SystemExit('⛔ 앞 구간 거부 — ' + ' | '.join(eprob[:8]) + (f' … 외 {len(eprob) - 8}' if len(eprob) > 8 else ''))
        tser = thickness_series(erows, rows)
        write_origin_csv(ORIGIN / 'ps73_ms_thickness_atomtop.csv', ['Simulation time', 'Thickness', 'Source'], ['ms', 'µm', ''],
                         [(f'{t:.3f}', f'{z:.3f}', s) for t, z, s in tser])
        (ORIGIN / 'ps73_ms_thickness_atomtop.ogs').write_text(
            ogs_text('ps73_ms_thickness_atomtop', '시뮬레이션 시간 (ms)–두께 (원자 기준 · 모든 원자 max(z + r)) · 0 ms 부터',
                     '79,189,255', 100, 320, 50, 'Thickness (\\g(m)m)', bounds_ms), encoding='utf-8')
        draw_preview(tser, '#4FBDFF', 'Thickness (µm)', (100, 320), 50, 'ps73_ms_thickness_atomtop', bounds_ms,
                     settle_label_at='top', marker_sources=(SRC_REPLAY, SRC_CKPT))
        key['thickness'] = {'status': 'OK', 'definition': 'max over ALL atoms of (z + r) − floor (z = 0) · µm (atom criterion only)',
                            'n_points': len(tser), 'insertion_line': ins,
                            'early_um': [[r['step'], round(r['ztop_max_deck_m'] * UM, 4)] for r in erows],
                            'last_um': round(tser[-1][1], 4),
                            'dropped_points': [{'step': r['step'], 'ms': r['step'] * STEP_MS, 'max_um': round(r['ztop_max_deck_m'] * UM, 4),
                                                'p999_um': round(r['ztop_p999_deck_m'] * UM, 4), 'top_id': r['ztop_id'], 'why': DROP_STEPS[r['step']]}
                                               for r in erows + rows if r['step'] in DROP_STEPS]}
    (HERE / 'key_numbers_ms.json').write_text(json.dumps(key, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(key, ensure_ascii=False))


# ───────────────────────────── 자기 시험 ─────────────────────────────
def selftest():
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            print('  ✗', name)

    def raises(fn):
        try:
            fn()
        except (ValueError, KeyError, IndexError):
            return True
        except NotImplementedError:
            return False
        return False

    def safe(fn, default=None):
        try:
            return fn()
        except NotImplementedError:
            return default

    deck = ('variable r_AM_P  equal 4.5e-3   # x\nvariable r_AM_S  equal 2.0e-3\nvariable r_SE    equal 0.5e-3\n'
            'region reg_mix block 0.0 0.05 0.0 0.05 0.005 0.30 units box\n')
    radii = {'AM_P': 4.5e-3, 'AM_S': 2.0e-3, 'SE': 0.5e-3}
    d = safe(lambda: deck_params(deck), {})
    chk('D1 덱 반경 셋 · 투입 위 끝', d == {'z_top_deck': 0.30, 'radii_deck': radii})
    chk('D2 reg_mix 없음 = 거부', raises(lambda: deck_params(deck.replace('reg_mix block', 'reg_x block'))))
    log = (' Step Atoms KinEng CPU \n 1 160421 0.1125746 0 \n 1000 160421 0.16042536 57.0 \nLoop time\n'
           ' Step Atoms zmax \n 200001 160420 0.13080182 \n'
           ' Step Atoms KinEng CPU pressMPa \n 200001 160420 0.00013331599 0 0 \n')
    kl = safe(lambda: log_thermo_ke(log), {})
    chk('K1 KinEng 블록만 · 같은 step 처음 것 · zmax 블록 제외',
        kl.get(1) == (160421, '0.1125746') and kl.get(1000) == (160421, '0.16042536') and kl.get(200001) == (160420, '0.00013331599'))

    def good_scan():
        return [{'step': s, 'dump_timestep': s, 'n_header': 10, 'n_rows': 10, 'n_bad_lines': 0, 'zc_max_deck_m': 0.1308,
                 'ztop_max_deck_m': 0.1313, 'ztop_id': '7', 'ztop_type': '3', 'ztop_radius_deck_m': 5e-4,
                 'ztop_p999_deck_m': 0.1300, 'bytes': 100, 'mtime': f'2026-09-17T21:{i:02d}:00'}
                for i, s in enumerate(range(405000, 425001, 5000))]
    plate = {s: 140.0 for s in range(405000, 425001, 5000)}

    def sprobs(rows):
        r = safe(lambda: check_scan(rows, 405000, 425000, radii, plate))
        return None if r is None else r[0]
    chk('S0 정상 합성 = 문제 없음', sprobs(good_scan()) == [])
    for name, mut, tag in [('S1 빠진 step', lambda r: r.pop(2), '①'),
                           ('S2 덤프 TIMESTEP 어긋남', lambda r: r[1].update(dump_timestep=999), '②'),
                           ('S3 원자 수 줄 ≠ 머리', lambda r: r[3].update(n_rows=9), '③'),
                           ('S4 깨진 줄', lambda r: r[0].update(n_bad_lines=1), '③'),
                           ('S5 파일 시각 거꾸로 (버린 조각이 덮은 덤프)', lambda r: r[2].update(mtime='2026-09-17T20:00:00'), '④'),
                           ('S6 p99.9 > 최댓값', lambda r: r[1].update(ztop_p999_deck_m=0.2), '⑥'),
                           ('S7 덱에 없는 반경', lambda r: r[1].update(ztop_radius_deck_m=1e-3), '⑦'),
                           ('S8 중복 step', lambda r: r.insert(1, dict(r[1])), '①')]:
        rows = good_scan()
        mut(rows)
        p = sprobs(rows)
        chk(name, p is not None and any(x.startswith(tag) for x in p))
    rows = good_scan()
    for r in rows[3:]:
        r.update(n_header=9, n_rows=9)
    rows[4].update(zc_max_deck_m=0.1405, ztop_max_deck_m=0.1410)
    res = safe(lambda: check_scan(rows, 405000, 425000, radii, plate))
    chk('S9 원자 수 감소 · 판 위 맨 위 = 거부 아님 (원자 기준 그대로) · 기록됨',
        res is not None and res[0] == [] and res[1]['atom_count_changes'] == [(405000, 10), (420000, 9)]
        and res[1]['first_step_top_center_above_plate'] == 425000 and res[1]['max_top_minus_plate_um'] == (1.0, 425000))

    ke = {1: (160421, '0.1125746'), 1000: (160421, '0.16042536')}
    ke.update({s: (160420, f'{1e-3 * (i + 1):.8g}') for i, s in enumerate(EARLY_STEPS[2:])})
    ins = 'INFO: Particle insertion ins_mix: inserted 160421 particle templates (mass 9.005968e-01) at step 1'

    def good_early():
        out = []
        for s in EARLY_STEPS:
            n = ke[s][0]
            out.append({'step': s, 'dump_timestep': s, 'n_header': n, 'n_rows': n, 'n_bad_lines': 0, 'zc_max_deck_m': 0.2,
                        'ztop_max_deck_m': 0.2005, 'ztop_id': '2', 'ztop_type': '3', 'ztop_radius_deck_m': 5e-4,
                        'ztop_p999_deck_m': 0.19, 'log': 'log.x', 'log_atoms': n, 'log_ke': ke[s][1]})
        return out

    def eprobs(rows, ins_line=ins):
        return safe(lambda: check_early(rows, ins_line, ke, radii))
    chk('E0 정상 합성 = 문제 없음', eprobs(good_early()) == [])
    for name, mut, tag in [('E1 체크포인트 하나 빠짐', lambda r: r.pop(4), 'E①'),
                           ('E2 체크포인트 KE ≠ 원 로그 (원 런 상태 아님)', lambda r: r[5].update(log_ke='0.0123'), 'E⑧'),
                           ('E3 재현 1000 step KE ≠ 원 로그 (궤적 갈림)', lambda r: r[1].update(log_ke='0.1604'), 'E⑧'),
                           ('E4 덤프 원자 수 ≠ 로그', lambda r: r[3].update(log_atoms=5), 'E⑤'),
                           ('E5 KE 칸 비어 있음', lambda r: r[2].update(log_ke=''), 'E⑧')]:
        rows = good_early()
        mut(rows)
        p = eprobs(rows)
        chk(name, p is not None and any(x.startswith(tag) for x in p))
    p = eprobs(good_early(), ins.replace('160421', '160400'))
    chk('E6 투입 줄 개수 다름 = 거부', p is not None and any(x.startswith('E⑨') for x in p))

    ser = safe(lambda: thickness_series(good_early(), good_scan(), drop={}, interp=False))
    chk('J1 출처 순서 재현 → 체크포인트 → 원 덤프 · 값 ×1000 · 시각 증가',
        ser is not None and [s for _, _, s in ser[:3]] == [SRC_REPLAY, SRC_REPLAY, SRC_CKPT] and ser[-1][2] == SRC_DUMP
        and abs(ser[0][1] - 200.5) < 1e-9 and ser[0][0] == 0.001)
    bad = good_early()
    bad[3]['step'] = 40
    chk('J2 시각 역전 = 거부', raises(lambda: thickness_series(bad, good_scan(), drop={}, interp=False)))
    fly = good_early()
    fly[3].update(ztop_max_deck_m=0.2016, ztop_p999_deck_m=0.1308)          # 100,000 step = 튀어 오른 입자 하나 (실측 꼴)
    ser = safe(lambda: thickness_series(fly, good_scan(), drop={100000: 'x'}, interp=False))
    chk('J3 외톨이 점 (100 ms) 은 빼고 앞뒤를 잇는다', ser is not None and 100.0 not in [t for t, _, _ in ser] and len(ser) == len(fly) - 1 + len(good_scan()))
    chk('J4 외톨이 아닌 점을 빼라고 하면 거부', raises(lambda: thickness_series(good_early(), good_scan(), drop={100000: 'x'})))
    chk('J5 자료에 없는 점을 빼라고 하면 거부', raises(lambda: thickness_series(fly, good_scan(), drop={123456: 'x'})))

    xs, ys = [0.001, 1.0, 50.0, 150.0, 200.0, 400.0], [304.28, 303.73, 175.39, 132.34, 131.79, 132.04]   # 실측 꼴 (무릎이 날카롭다)
    dense = [0.001 + k * 0.5 for k in range(800)]
    v = safe(lambda: pchip(xs, ys, dense))
    chk('I1 매듭을 지난다', v is not None and all(abs(a - b) < 1e-9 for a, b in zip(safe(lambda: pchip(xs, ys, xs), []), ys)))
    chk('I2 구간마다 두 매듭 값 사이 (넘침 없음 — 150–200 ms 에서 131.79 아래로 안 꺼진다)',
        v is not None and all(min(ys[k], ys[k + 1]) - 1e-9 <= y <= max(ys[k], ys[k + 1]) + 1e-9
                              for x, y in zip(dense, v) for k in [max(i for i in range(len(xs) - 1) if xs[i] <= x)] if x <= xs[-1]))
    chk('I3 감소 구간에서 늘지 않는다', v is not None and all(b <= a + 1e-9 for (xa, a), (xb, b) in zip(zip(dense, v), zip(dense[1:], v[1:])) if xb <= 150.0))
    chk('I4 매듭 x 가 증가하지 않으면 거부', raises(lambda: pchip([0.0, 1.0, 1.0], [1.0, 2.0, 3.0], [0.5])))
    ser = safe(lambda: thickness_series(fly, good_scan(), drop={100000: 'x'}))
    meas = [p for p in (ser or []) if p[2] != SRC_INTERP]
    chk('I5 채움: 측정점 그대로 · 채운 점은 첫 점 ~ 첫 원 덤프 사이 1 ms 마다 · 시각 엄격 증가',
        ser is not None and meas == safe(lambda: thickness_series(fly, good_scan(), drop={100000: 'x'}, interp=False))
        and all(0.001 < t < 405.0 for t, _, s in ser if s == SRC_INTERP) and sum(1 for p in ser if p[2] == SRC_INTERP) == 404 - 8
        and all(b[0] > a[0] for a, b in zip(ser, ser[1:])))
    prow = ([{'step': '1', 'phase': '0', 'pressure_mpa': ''}, {'step': '200002', 'phase': '1', 'pressure_mpa': ''}]
            + [{'step': str(s), 'phase': '2', 'pressure_mpa': '0.0'} for s in (201000, 202000)]
            + [{'step': '3125000', 'phase': '3', 'pressure_mpa': '300.95'}, {'step': '3126000', 'phase': '4', 'pressure_mpa': '204.6'},
               {'step': '3127000', 'phase': '4', 'pressure_mpa': '165.0'}])
    r = safe(lambda: pressure_series(prow))
    chk('P1 앞에 (0 ms, 0 MPa, 판 없음) 하나 · 원값 그대로',
        r is not None and r[1][0] == (0.0, 0.0, SRC_NOPLATE) and len(r[1]) == len(r[0]) + 1 and r[1][1] == (201.0, 0.0, SRC_THERMO))
    if r is not None:
        s = safe(lambda: slide_series(r[0], 3125000))
        chk('P2 슬라이드: 압축 끝까지 원값 + 모식', s is not None and s[0][-1][2] == SRC_RELAX and s[0][-3][1] == 300.95
            and abs(s[1][0][1] - (165.0 + (300.95 - 165.0) * math.exp(-1000 / SLIDE_TAU_STEP))) < 1e-12)
    else:
        chk('P2 슬라이드', False)
    chk('P3 판 놓은 뒤 첫 압력 ≠ 0 = 거부', raises(lambda: pressure_series([{'step': '201000', 'phase': '2', 'pressure_mpa': '3.0'}])))
    print(f'make_fig_ms selftest: {ok} PASS · {fail} FAIL')
    return fail == 0


if __name__ == '__main__':
    if '--selftest' in sys.argv[1:]:
        sys.exit(0 if selftest() else 1)
    main()
