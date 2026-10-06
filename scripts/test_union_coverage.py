#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 피복률 ⑥ — **합집합 cap** (C2-⑥ · 1저자 비준 10-06 *"권고대로"* · 원장 LHS-25).

  python3 scripts/test_union_coverage.py          # 종료코드 0 = PASS

결정 (C2 설계 요약 ⑥): *"LHS-25 Coverage 분모 · 100 % 클립 → 합집합 cap 피복 (`*_physics_union` 새 키) — Coverage 를 바꾸는
유일한 수정"*.  옛 Physics 피복 (`coverage_*_mean_physics`) = AM 마다 접촉 면적 **합** ÷ 자유 표면 → 100 % 클립 — 표면 한도가 없어
SE 가 많은 침대에서 포화한다 (LHS-25).  새 규칙 = AM 마다 SE 접촉 하나에 **구면 cap 하나** (cap 넓이 = 세대 2 표면 소비자 면적
`film_area_g2(consumer='surface')`) · 겹친 cap 은 **한 번만** · AM–AM 접촉이 가린 표면은 분자 · 분모에서 뺀다 · Fibonacci 점 N = 6000 으로 잰다.

★ 시험 먼저 — 옛 코드 (a0a24c538) 에는 `plastic_coverage.union_cap_coverage` · `fibonacci_sphere` 가 없고 피복 단계가 `*_physics_union`
  키를 쓰지 않는다 → [F] [P] [R] 이 빨갛다.

  [F] 순수 함수 — 해석해 대조 (한 cap = cap 넓이 비 · 같은 cap 둘 = 한 번 · 떨어진 cap 은 더한다 · 부분 겹침 = 두 cap 교집합 닫힌 식 ·
      AM–AM 가림 · 접촉 0 = 측정된 0 · 전부 가림 = None · 반구 넘는 cap = 반구로 자르고 센다 · 무효 입력 = 예외 · 결정적)
  [P] 생산자 `coverage_physics_vs_hertzian.compute_case` — 키 이름 · 값 · 고립 AM 0 · 주기 경계 최소영상 · 표면 소비자 상한 ·
      빈칸 + 사유 (상자 없음 · 상자 어긋남 · δ NaN · 반경 NaN · 전부 가림 · c_cpl[22] < 0) · 옛 키 · v2 무영향 · 옛 세대 걷기
  [R] 실침대 (커밋 덤프 · parse_liggghts → compute_case 실제 사슬) — real_14: 합-클립 51.522 → 합집합 43.22 (×0.839 · 설계 원형
      cov_union2.py N 6000 과 같은 값) · case15: 생산 경로는 빈칸 (c_cpl[22] < 0 두 접촉 = 통째로 AM 안의 SE · v2 와 같은 사유) ·
      원형의 ×0.87 은 그 두 행을 원판 넓이로 바꿔 넣은 값임을 재현 · 표본 오차 (N 6000 ↔ 24000)

표본 허용폭 근거 (10-06 실측 · 이 리포 밖 원형 작업 · fiberr.py): N 6000 Fibonacci 로 무작위 cap 5,000 개 (넓이 비 1e-4–0.5) 의
|오차| 최대 0.23 %p · p99 0.13 %p · 평균 0.037 %p → 한 cap 시험 허용 0.3 %p.  침대 평균은 AM 수백 개 · cap 수만 개의 평균이라
표본 오차가 줄어든다 (case15 원형: N 6000 ↔ 24000 평균 차 0.001 %p) → 실침대 허용 0.05 %p (부동소수 경계 뒤집힘 + 표본).
"""
import contextlib
import gzip
import io
import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
_ok, _fail = 0, []

SINGLE_CAP_TOL = 0.3      # %p — N 6000 한 cap 표본 오차 (위 근거)
BED_TOL = 0.05            # %p — 실침대 평균 (위 근거)


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}' + (f'   {extra}' if extra else ''))
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {extra}' if extra else ''))
    return bool(cond)


def _guard(label, fn):
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001 — 옛 코드 = 없는 함수 · 키도 FAIL 로 센다
        import traceback
        traceback.print_exc()
        chk(f'{label} — 예외 {type(e).__name__}: {e}', False)


# ── 독립 oracle (생산 코드를 빌리지 않는다) ─────────────────────────────────────────────
def fib_ref(n):
    """문서에 적힌 Fibonacci 격자 식 그대로 (점 i: i + ½ · z = 1 − 2(i + ½)/n · φ = π(1 + √5)(i + ½))."""
    i = np.arange(n) + 0.5
    z = 1 - 2 * i / n
    rho = np.sqrt(1 - z * z)
    phi = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([rho * np.cos(phi), rho * np.sin(phi), z], 1)


def cap_frac(area, R):
    """넓이 A 인 cap 의 구면 비 = A / (4πR²) (반구로 자른다)."""
    return min(area, 2 * math.pi * R * R) / (4 * math.pi * R * R)


def cap_theta(area, R):
    return math.acos(1.0 - min(area, 2 * math.pi * R * R) / (2 * math.pi * R * R))


def cap_int(t1, t2, g):
    """단위 구면 위 두 cap (각반경 t1 · t2 · 중심 사이 각 g) 의 교집합 넓이 — 닫힌 식 (Tovchigrechko & Vakser 2001 꼴 ·
    4 M 점 몬테카를로로 네 경우 1.4σ 안 확인)."""
    if g >= t1 + t2:
        return 0.0
    if g <= abs(t1 - t2):
        return 2 * math.pi * (1 - math.cos(min(t1, t2)))
    a = math.acos((math.cos(g) - math.cos(t1) * math.cos(t2)) / (math.sin(t1) * math.sin(t2)))
    b = math.acos((math.cos(t2) - math.cos(g) * math.cos(t1)) / (math.sin(g) * math.sin(t1)))
    c = math.acos((math.cos(t1) - math.cos(g) * math.cos(t2)) / (math.sin(g) * math.sin(t2)))
    return 2 * (math.pi - a - math.cos(t1) * b - math.cos(t2) * c)


def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


def disc_area(r1, r2, delta):
    """두 구의 교차 원판 (c_cpl[22] 기하) — 독립 구현."""
    d = r1 + r2 - delta
    if d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    x = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    return max(math.pi * (r1 * r1 - x * x), 0.0)


# ── [F] 순수 함수 ─────────────────────────────────────────────────────────────────────
def section_f():
    print('[F] 순수 함수 plastic_coverage.union_cap_coverage — 해석해 대조')
    import plastic_coverage as PC
    f = getattr(PC, 'union_cap_coverage', None)
    fs = getattr(PC, 'fibonacci_sphere', None)
    if not chk('F0 union_cap_coverage · fibonacci_sphere · 규칙 이름 · N 이 있다',
               callable(f) and callable(fs) and getattr(PC, 'UNION_COVERAGE_RULE', None) == 'union_caps_g2_surface'
               and getattr(PC, 'UNION_FIB_N', None) == 6000):
        return
    U = fs(6000)
    chk('F1 Fibonacci 격자 = 문서 식 그대로 (6000 × 3 · 단위 벡터 · 결정적)',
        U.shape == (6000, 3) and np.allclose(U, fib_ref(6000), atol=0, rtol=0)
        and np.allclose(np.linalg.norm(U, axis=1), 1.0, atol=1e-12) and np.array_equal(U, fs(6000)))
    R = 2.0
    n1 = unit([0.3, -0.2, 0.93])
    for A in (0.37, 3.1, 11.0):
        c, info = f(R, [n1], [A])
        want = 100 * cap_frac(A, R)
        chk(f'F2 cap 하나 (A {A} · R {R}) = 100·A/(4πR²) ± {SINGLE_CAP_TOL} %p · 가림 없음 (free 1)',
            c is not None and abs(c - want) <= SINGLE_CAP_TOL and info['free_frac'] == 1.0 and info['n_se_caps'] == 1,
            f'{c} vs {want:.4f}')
    c1, _ = f(R, [n1], [3.1])
    c2, _ = f(R, [n1, n1], [3.1, 3.1])
    chk('F3 같은 cap 둘 = cap 하나와 **같은 값** (겹침 한 번 — 합이면 두 배)', c1 == c2 and c1 > 0, f'{c1} · {c2}')
    na, nb = unit([0, 0, 1]), unit([0, 0, -1])
    ca, _ = f(R, [na], [4.0])
    cb, _ = f(R, [nb], [6.0])
    cab, _ = f(R, [na, nb], [4.0, 6.0])
    chk('F4 떨어진 cap 둘 = 각 값의 합 (같은 점 집합 — 정확히) · 해석해 ± 2·허용',
        abs(cab - (ca + cb)) < 1e-9 and abs(cab - 100 * (cap_frac(4.0, R) + cap_frac(6.0, R))) <= 2 * SINGLE_CAP_TOL,
        f'{cab} vs {ca}+{cb}')
    g = 0.6
    m1, m2 = unit([0, 0, 1]), unit([math.sin(g), 0, math.cos(g)])
    A1, A2 = 2 * math.pi * R * R * (1 - math.cos(0.5)), 2 * math.pi * R * R * (1 - math.cos(0.4))
    cu, _ = f(R, [m1, m2], [A1, A2])
    s1, _ = f(R, [m1], [A1])
    s2, _ = f(R, [m2], [A2])
    want = 100 * (cap_frac(A1, R) + cap_frac(A2, R) - cap_int(0.5, 0.4, g) / (4 * math.pi))
    chk('F5 부분 겹침 cap 둘 = 합집합 닫힌 식 (f₁ + f₂ − 교집합) ± 2·허용 · 합보다 작다',
        abs(cu - want) <= 2 * SINGLE_CAP_TOL and cu < s1 + s2 - 0.5, f'{cu:.4f} vs {want:.4f} (합 {s1 + s2:.4f})')
    # AM–AM 가림 — SE cap 위 · AM cap 아래 (떨어짐) → cov = f_s / (1 − f_a)
    As, Aa = 3.0, 9.0
    cg, ig = f(R, [na], [As], [nb], [Aa])
    want = 100 * cap_frac(As, R) / (1 - cap_frac(Aa, R))
    chk('F6 AM–AM 가림: 분모 = 가리지 않은 표면 (떨어진 두 cap → f_s/(1 − f_a)) ± 2·허용 · free 비 ≈ 1 − f_a',
        cg is not None and abs(cg - want) <= 2 * SINGLE_CAP_TOL and abs(ig['free_frac'] - (1 - cap_frac(Aa, R))) <= 0.003,
        f'{cg} vs {want:.4f} · free {ig["free_frac"]:.4f}')
    ci, _ = f(R, [na], [1.0], [na], [9.0])
    chk('F6b SE cap 이 AM–AM cap 안에 통째로 → 0 (가린 표면은 덮인 것으로 세지 않는다)', ci == 0.0, repr(ci))
    c0, i0 = f(R, [], [])
    chk('F7 접촉 0 → 측정된 0.0 (None 아님) · free 1 · cap 0', c0 == 0.0 and isinstance(c0, float)
        and i0['free_frac'] == 1.0 and i0['n_se_caps'] == 0, repr((c0, i0)))
    # 전부 가림 — 반구 cap 둘 (±z) 이 구 전체를 덮는다 (n 6000 의 z 는 0 이 아니다)
    big = 2 * math.pi * R * R
    cn, inn = f(R, [n1], [1.0], [na, nb], [big, big])
    chk('F8 AM–AM 이 표면 전부를 가림 → None + 사유 (0.0 으로 조용히 넣지 않는다)',
        cn is None and inn.get('reason') == 'free_surface_empty' and inn['n_free'] == 0, repr((cn, inn.get('reason'))))
    ch, ih = f(R, [na], [3 * math.pi * R * R])
    chk('F9 반구보다 큰 cap → 반구 (2πR² = 표면 소비자 상한) 로 자르고 센다 → 50 % ± 허용 · n_caps_clipped_hemisphere 1',
        ch is not None and abs(ch - 50.0) <= SINGLE_CAP_TOL and ih['n_caps_clipped_hemisphere'] == 1, repr((ch, ih)))
    bad = {
        '반경 NaN': lambda: f(float('nan'), [na], [1.0]),
        '반경 0': lambda: f(0.0, [na], [1.0]),
        '반경 음수': lambda: f(-1.0, [na], [1.0]),
        '반경 문자열': lambda: f('2', [na], [1.0]),
        '반경 bool': lambda: f(True, [na], [1.0]),
        '방향 NaN': lambda: f(R, [[float('nan'), 0, 1]], [1.0]),
        '방향 길이 0': lambda: f(R, [[0, 0, 0]], [1.0]),
        '방향 꼴 (k, 2)': lambda: f(R, [[0, 1]], [1.0]),
        '면적 NaN': lambda: f(R, [na], [float('nan')]),
        '면적 음수': lambda: f(R, [na], [-1.0]),
        '면적 inf': lambda: f(R, [na], [float('inf')]),
        '개수 어긋남': lambda: f(R, [na, nb], [1.0]),
        'AM 면적 음수': lambda: f(R, [na], [1.0], [nb], [-2.0]),
    }
    leaked = []
    for nm, fn in bad.items():
        try:
            fn()
            leaked.append(nm)
        except (ValueError, TypeError):
            pass
    chk('F10 무효 입력은 예외 (조용히 면적 · 0 을 내지 않는다)', not leaked, f'통과해 버린 입력 {leaked}')
    rng = np.random.default_rng(3)
    dirs = [unit(rng.normal(size=3)) for _ in range(40)]
    areas = list(rng.uniform(0.05, 2.0, size=40))
    a, _ = f(R, dirs, areas, [dirs[0]], [1.5])
    perm = rng.permutation(40)
    b, _ = f(R, [dirs[k] for k in perm], [areas[k] for k in perm], [dirs[0]], [1.5])
    chk('F11 결정적 · cap 순서와 무관 (같은 입력 → 같은 값)', a == b and a == f(R, dirs, areas, [dirs[0]], [1.5])[0], f'{a} · {b}')
    # 독립 몬테카를로 (4 M 점) 와 다수 cap 대조 — Fibonacci 격자가 아닌 표본기
    P = np.random.default_rng(11).normal(size=(4_000_000, 3))
    P /= np.linalg.norm(P, axis=1)[:, None]
    cov = np.zeros(len(P), bool)
    for d_, a_ in zip(dirs, areas):
        cov |= P @ d_ >= 1 - min(a_, 2 * math.pi * R * R) / (2 * math.pi * R * R)
    occ = P @ dirs[0] >= 1 - 1.5 / (2 * math.pi * R * R)
    mc = 100 * (cov & ~occ).sum() / (~occ).sum()
    chk('F12 cap 40 개 + 가림 = 독립 몬테카를로 (4 M 점) ± 0.5 %p', abs(a - mc) <= 0.5, f'{a:.4f} vs MC {mc:.4f}')


# ── [P] 생산자 ──────────────────────────────────────────────────────────────────────────
UM = 1e-3                     # 덤프 단위 (scale 1000: sim 0.001 = 1 µm)
BOX = 0.02                    # 20 µm 주기 상자


def _write_bed(cd, atoms, contacts, *, box=BOX, fm_extra=None, ip=True):
    """atoms = {id: (type, r, x, y, z)} · contacts = [(id1, id2, delta, area)] (덤프 단위)."""
    cd = Path(cd)
    cd.mkdir(parents=True, exist_ok=True)
    with open(cd / 'atoms.csv', 'w') as fh:                     # float() — numpy 2 의 repr 은 'np.float64(…)' 라 CSV 가 깨진다
        fh.write('id,type,x,y,z,radius\n')
        for i in sorted(atoms):
            t, r, x, y, z = atoms[i]
            fh.write(f'{i},{t},{float(x)!r},{float(y)!r},{float(z)!r},{float(r)!r}\n')
    with open(cd / 'contacts.csv', 'w') as fh:
        fh.write('id1,id2,delta,contact_area\n')
        for a, b, dl, ar in contacts:
            fh.write(f'{a},{b},{float(dl)!r},{float(ar)!r}\n')
    fm = {'porosity': 15.6, 'kept_key': 'keep'}
    fm.update(fm_extra or {})
    (cd / 'full_metrics.json').write_text(json.dumps(fm))
    if ip:
        (cd / 'input_params.json').write_text(json.dumps({'box_x': box, 'box_y': box}))
    (cd / 'meta.json').write_text(json.dumps({'name': cd.name, 'type_map': '1:AM_P,2:AM_S,3:SE', 'scale': 1000}))
    return cd


def _touch(center, r_c, r_o, direction, delta):
    """중심 center (반경 r_c) 에서 direction 쪽으로 깊이 delta 로 겹친 반경 r_o 구의 중심."""
    return tuple(np.asarray(center, float) + unit(direction) * (r_c + r_o - delta))


def _base_bed():
    """AM_P 1 (r 2 µm · 상자 가운데) + SE 넷 (+x · +y · −y · 깊은 −x) · AM_S 2 (−z 쪽 AM–AM) · 고립 AM_S 3 ·
    AM_S 4 (x 경계 근처) — SE 20 은 −x 쪽 (주기 경계 너머에 저장) · AM_S 5 는 +x 쪽 AM–AM (가림)."""
    a, c = {}, []
    c1 = (0.010, 0.010, 0.010)
    a[1] = (1, 2 * UM) + c1
    se_specs = [(10, [1, 0, 0], 0.05 * UM), (11, [0, 1, 0], 0.05 * UM), (12, [0, -1, 0.2], 0.03 * UM),
                (13, [-1, 0, 0.1], 0.4 * UM)]                          # 13 = 깊은 겹침 (δ/R* 1) — 표면 소비자 상한이 묶는다
    for sid, dvec, dl in se_specs:
        a[sid] = (3, 0.5 * UM) + _touch(c1, 2 * UM, 0.5 * UM, dvec, dl)
        c.append((1, sid, dl, disc_area(2 * UM, 0.5 * UM, dl)))
    a[2] = (2, 1 * UM) + _touch(c1, 2 * UM, 1 * UM, [0, 0, -1], 0.1 * UM)
    c.append((1, 2, 0.1 * UM, disc_area(2 * UM, 1 * UM, 0.1 * UM)))
    a[3] = (2, 1 * UM, 0.003, 0.003, 0.003)                            # 접촉 0 — 참 피복률 0
    c4 = (0.0008, 0.015, 0.015)
    a[4] = (2, 1 * UM) + c4
    sx, sy, sz = _touch(c4, 1 * UM, 0.5 * UM, [-1, 0, 0], 0.05 * UM)
    a[20] = (3, 0.5 * UM, sx + BOX, sy, sz)                            # 경계 너머 → 저장 좌표는 상자 안 (x + L)
    c.append((4, 20, 0.05 * UM, disc_area(1 * UM, 0.5 * UM, 0.05 * UM)))
    a[5] = (2, 1 * UM) + _touch(c4, 1 * UM, 1 * UM, [1, 0, 0], 0.3 * UM)
    c.append((4, 5, 0.3 * UM, disc_area(1 * UM, 1 * UM, 0.3 * UM)))
    return a, c


def _expected(atoms, contacts, box=BOX):
    """기대 피복률 — 방향은 배치 기하에서 (최소영상) · 면적은 세대 2 표면 소비자 (`film_area_g2` · µm) · 합집합은 순수 함수
    ([F] 가 해석해로 따로 묶는다).  생산자의 배선 (상 쌍 · 방향 · 단위 · 소비자 · 집계) 을 따로 다시 센다."""
    from plastic_coverage import film_area_g2, union_cap_coverage
    caps = {i: {'se': [], 'am': []} for i, v in atoms.items() if v[0] in (1, 2)}
    for i1, i2, dl, ar in contacts:
        t1, t2 = atoms[i1][0], atoms[i2][0]
        am1, am2 = t1 in (1, 2), t2 in (1, 2)
        if not (am1 or am2) or (not am1 and not am2):
            continue
        pair = 'AM_AM' if (am1 and am2) else 'AM_SE'
        A, _ = film_area_g2(dl * 1000, atoms[i1][1] * 1000, atoms[i2][1] * 1000, pair=pair, ligg_area=ar * 1e6,
                            length_scale=1e6, consumer='surface')
        for me, ot in ((i1, i2), (i2, i1)):
            if atoms[me][0] not in (1, 2):
                continue
            if pair == 'AM_SE' and atoms[ot][0] in (1, 2):
                continue
            v = np.asarray(atoms[ot][2:], float) - np.asarray(atoms[me][2:], float)
            v[:2] -= box * np.round(v[:2] / box)
            caps[me]['am' if pair == 'AM_AM' else 'se'].append((unit(v), A))
    out = {}
    for i, cc in caps.items():
        R = atoms[i][1] * 1000
        out[i] = union_cap_coverage(R, [d for d, _ in cc['se']], [A for _, A in cc['se']],
                                    [d for d, _ in cc['am']], [A for _, A in cc['am']])[0]
    return out


def _run(cd, tm=None):
    import coverage_physics_vs_hertzian as CV
    tm = tm or {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
    with contextlib.redirect_stdout(io.StringIO()):
        CV.compute_case(Path(cd).name, Path(cd), tm, scale=1000, write_csv=True, update_metrics=True)
    return json.loads((Path(cd) / 'full_metrics.json').read_text())


VALUE_KEYS = ('coverage_AM_P_mean_physics_union', 'coverage_AM_P_std_physics_union', 'coverage_AM_S_mean_physics_union',
              'coverage_AM_S_std_physics_union', 'coverage_AM_mean_physics_union')


def section_p(tmp):
    print('[P] 생산자 coverage_physics_vs_hertzian.compute_case — *_physics_union 키')
    atoms, contacts = _base_bed()
    cd = _write_bed(tmp / 'base', atoms, contacts)
    fm = _run(cd)
    uk = sorted(k for k in fm if k.endswith('_physics_union'))
    want = set(VALUE_KEYS) | {'coverage_status_physics_union', 'coverage_rule_physics_union', 'coverage_n_fib_physics_union',
                              'coverage_diag_physics_union'}
    chk('P1 키 이름 = legacy 규약 (coverage_<상>_{mean,std}_physics_union · coverage_AM_mean_physics_union) + 상태 · 규칙 · N · 진단',
        set(uk) == want and fm.get('coverage_status_physics_union') == 'ok'
        and fm.get('coverage_rule_physics_union') == 'union_caps_g2_surface' and fm.get('coverage_n_fib_physics_union') == 6000,
        f'없음 {sorted(want - set(uk))} · 남음 {sorted(set(uk) - want)} · status {fm.get("coverage_status_physics_union")!r}')
    if fm.get('coverage_status_physics_union') != 'ok':
        return
    e = _expected(atoms, contacts)
    covP = e[1]
    covS = [e[2], e[3], e[4], e[5]]
    chk('P2 AM_P 값 = 기대 (최소영상 방향 · 세대 2 표면 면적 · 합집합) — 셋째 자리',
        fm['coverage_AM_P_mean_physics_union'] == round(covP, 3) and fm['coverage_AM_P_std_physics_union'] == 0.0,
        f"{fm['coverage_AM_P_mean_physics_union']} vs {round(covP, 3)}")
    chk('P3 AM_S 평균 · std = 넷 (고립 AM 3 의 측정된 0 포함 · 빼지 않는다) · 전체 = AM 다섯의 입자 수 가중',
        fm['coverage_AM_S_mean_physics_union'] == round(float(np.mean(covS)), 3)
        and fm['coverage_AM_S_std_physics_union'] == round(float(np.std(covS)), 3)
        and fm['coverage_AM_mean_physics_union'] == round(float(np.mean([covP] + covS)), 3) and e[3] == 0.0,
        f"S {fm['coverage_AM_S_mean_physics_union']} vs {round(float(np.mean(covS)), 3)} · all "
        f"{fm['coverage_AM_mean_physics_union']} vs {round(float(np.mean([covP] + covS)), 3)}")
    chk('P4 주기 경계 너머 SE (저장 x = 실제 + L) → 최소영상 방향 (−x) — 원 좌표차 (+x) 면 AM–AM 가림 안이라 0 이 된다',
        e[4] > 1.0, f'AM 4 = {e[4]:.3f}')
    dg = fm.get('coverage_diag_physics_union') or {}
    chk('P5 진단 — AM 5 · cap AM–SE 5 · AM–AM 2 접촉 (양쪽 cap 4) · SE 접촉 없는 AM 3 (2 · 3 · 5) · 접촉 실패 0 · 방향 어긋남 0 · '
        '상자 기록 · 면적 규칙 g2 표면',
        dg.get('n_am') == 5 and dg.get('n_caps_am_se') == 5 and dg.get('n_caps_am_am') == 4 and dg.get('n_contact_failures') == 0
        and dg.get('n_dir_inconsistent') == 0 and dg.get('box_xy_sim') == [BOX, BOX] and dg.get('area_rule') == 'physics_g2'
        and dg.get('area_consumer') == 'surface' and dg.get('n_am_no_se_contact') == 3, repr(dg))
    # 표면 소비자: 깊은 SE 13 의 cap = 2π r_SE² (수송 소비자면 π r_SE²) — 둘이 다른 값을 내는 배치
    from plastic_coverage import film_area_g2, union_cap_coverage
    a_s = film_area_g2(0.4, 2.0, 0.5, pair='AM_SE', ligg_area=disc_area(2.0, 0.5, 0.4), length_scale=1e6, consumer='surface')[0]
    a_t = film_area_g2(0.4, 2.0, 0.5, pair='AM_SE', ligg_area=disc_area(2.0, 0.5, 0.4), length_scale=1e6, consumer='transport')[0]
    chk('P6 깊은 접촉의 cap = 표면 소비자 상한 2π r_SE² (수송 π r_SE² 와 다르다 — 배치가 소비자를 가른다)',
        abs(a_s - 2 * math.pi * 0.25) < 1e-12 and abs(a_t - math.pi * 0.25) < 1e-12, f'{a_s} · {a_t}')
    # 옛 키 · v2 는 그대로 (같은 침대에서 union 줄을 지운 것과 같아야 한다 — 다른 장부)
    leg = {k: v for k, v in fm.items() if not k.endswith('_physics_union')}
    import coverage_physics_vs_hertzian as CV
    chk('P7 legacy · v2 키는 union 장부와 독립 (legacy 피복 = 접촉 면적 합 · v2 상태 ok) · 원래 키 그대로',
        isinstance(leg.get('coverage_AM_P_mean_physics'), float) and leg.get('coverage_status_physics_v2') == 'ok'
        and leg.get('kept_key') == 'keep' and leg.get('porosity') == 15.6)
    with contextlib.redirect_stdout(io.StringIO()):
        rc = CV._selftest()
    chk('P8 피복 모듈 selftest (① legacy 바이트 핀 · v2 계약 ⑬–⑮) 그대로 통과', rc == 0, f'rc={rc}')
    # 옛 세대 걷기
    cd9 = _write_bed(tmp / 'stale', atoms, contacts, fm_extra={'coverage_AM_P_mean_physics_union': 999.0,
                                                               'bogus_physics_union': 1})
    fm9 = _run(cd9)
    chk('P9 미리 있던 *_physics_union 키는 전부 걷고 새로 쓴다 (bogus 없음 · 999 덮임)',
        'bogus_physics_union' not in fm9 and fm9.get('coverage_AM_P_mean_physics_union') == fm['coverage_AM_P_mean_physics_union'])

    def blank(name, cd, needle, diag_key=None, diag_val=None):
        f2 = _run(cd)
        st = str(f2.get('coverage_status_physics_union'))
        d2 = f2.get('coverage_diag_physics_union') or {}
        ok = (st.startswith('blank') and needle in st and all(f2.get(k) is None for k in VALUE_KEYS if k in f2)
              and isinstance(f2.get('coverage_AM_P_mean_physics'), float)
              and (diag_key is None or d2.get(diag_key) == diag_val))
        chk(name, ok, f'status={st[:160]!r} · {diag_key}={d2.get(diag_key)!r}')

    blank('P10 ★ 상자 없음 (input_params.json 없음) → 빈칸 + 사유 (0.05 기본값으로 떨어지지 않는다) · legacy 는 계산',
          _write_bed(tmp / 'nobox', atoms, contacts, ip=False), 'box')
    blank('P11 ★ 상자 어긋남 (0.019 — 주기 쌍의 최소영상 거리 ≠ r1 + r2 − δ) → 빈칸 + 방향 어긋남 수',
          _write_bed(tmp / 'badbox', atoms, contacts, box=0.019), '방향', 'n_dir_inconsistent', 1)
    c_nan = [(i1, i2, (float('nan') if (i1, i2) == (1, 11) else dl), ar) for i1, i2, dl, ar in contacts]
    blank('P12 ★ δ NaN 한 행 → 빈칸 + 접촉 실패 1 (조용히 건너뛰지 않는다)', _write_bed(tmp / 'nandelta', atoms, c_nan), '접촉',
          'n_contact_failures', 1)
    a_nr = dict(atoms)
    a_nr[3] = (2, float('nan'), 0.003, 0.003, 0.003)
    blank('P13 ★ 고립 AM 반경 NaN (접촉 0 이라 접촉 검사를 안 지난다) → 빈칸 + 반경 무효 1', _write_bed(tmp / 'nanr', a_nr, contacts),
          '반경', 'n_radius_invalid', 1)
    # 전부 가림 — AM_S 30 을 AM_S 여섯 (±x ±y ±z) 이 원판 넓이 π r² 로 감싼다 (cap 반각 60° > 덮개 반경 54.7°)
    a_oc, c_oc = dict(atoms), list(contacts)
    c30 = (0.010, 0.016, 0.016)
    a_oc[30] = (2, 1 * UM) + c30
    for k, dv in enumerate(([1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1])):
        a_oc[31 + k] = (2, 1 * UM) + _touch(c30, 1 * UM, 1 * UM, dv, 0.6 * UM)
        c_oc.append((30, 31 + k, 0.6 * UM, math.pi * UM * UM))
    blank('P14 ★ AM–AM 이 AM 표면 전부를 가림 → 빈칸 + 분모 무효 1 (LHSC-01 (a) 와 같은 계약)', _write_bed(tmp / 'occl', a_oc, c_oc),
          '분모', 'n_free_surface_empty', 1)
    c_neg = [(i1, i2, dl, (-abs(ar) if (i1, i2) == (1, 10) else ar)) for i1, i2, dl, ar in contacts]
    blank('P15 ★ c_cpl[22] < 0 (통째로 포함된 쌍의 생산자 값) → film_area_g2 거부 → 빈칸 (v2 와 같은 사유 · 원판으로 바꿔 넣지 않는다)',
          _write_bed(tmp / 'negarea', atoms, c_neg), 'ligg_area < 0', 'n_contact_failures', 1)
    # SE 만 (AM 0) → ok · 피복 키 없음
    cd16 = _write_bed(tmp / 'seonly', {7: (3, 0.5 * UM, 0.01, 0.01, 0.01), 8: (3, 0.5 * UM, 0.01, 0.01, 0.0109)},
                      [(7, 8, 0.1 * UM, disc_area(0.5 * UM, 0.5 * UM, 0.1 * UM))])
    f16 = _run(cd16)
    chk('P16 AM 0 개 (SE 만) → ok · 피복 값 키 없음 (적용 대상 없음 — 0 으로 채우지 않는다)',
        f16.get('coverage_status_physics_union') == 'ok' and not any(k in f16 for k in VALUE_KEYS)
        and (f16.get('coverage_diag_physics_union') or {}).get('n_am') == 0)


# ── [R] 실침대 ──────────────────────────────────────────────────────────────────────────
BEDS = {
    'real14': ('docs/data/real14_reference_20260928', 'atom_2060000.liggghts.gz', 'contact_2060000.liggghts.gz',
               'input_real_14.liggghts', {1: 'AM_P', 2: 'AM_S', 3: 'SE'}),
    'case15': ('docs/data/case15_corner_20261001', 'atom_v4_1710000.liggghts.gz', 'contact_v4_1710000.liggghts.gz',
               'input_case15.liggghts', {1: 'AM_P', 2: 'SE'}),
}


def build_real_bed(bed, out):
    """웹앱 파이프라인과 같은 파서 (parse_liggghts) 로 커밋 덤프 → atoms.csv · contacts.csv · input_params.json (덱) · meta.json."""
    import parse_liggghts as PL
    d, fa, fc, deck, tm = BEDS[bed]
    base = os.path.join(ROOT, d)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for src, nm, dst in ((fa, 'atom', 'atoms.csv'), (fc, 'contact', 'contacts.csv')):
        raw = out / f'_{nm}.liggghts'
        raw.write_bytes(gzip.open(os.path.join(base, src)).read())
        h, rows = (PL.parse_atom_file if nm == 'atom' else PL.parse_contact_file)(str(raw))
        with open(out / dst, 'w') as fh:
            fh.write(','.join(h) + '\n')
            for r in rows:
                fh.write(','.join(r) + '\n')
        raw.unlink()
    (out / 'input_params.json').write_text(json.dumps(PL.parse_input_script(os.path.join(base, deck))))
    (out / 'meta.json').write_text(json.dumps({'name': bed, 'type_map': ','.join(f'{k}:{v}' for k, v in tm.items()),
                                               'scale': 1000}))
    (out / 'full_metrics.json').write_text(json.dumps({'kept': 1}))
    return out, tm


def section_r(tmp):
    print('[R] 실침대 — parse_liggghts → compute_case (웹앱과 같은 사슬)')
    import coverage_physics_vs_hertzian as CV
    cd, tm = build_real_bed('real14', tmp / 'real14')
    fm = _run(cd, tm)
    leg = (fm.get('coverage_AM_mean_physics'), fm.get('coverage_AM_P_mean_physics'), fm.get('coverage_AM_S_mean_physics'))
    chk('R1 real_14 legacy 합-클립 (Physics v1) 그대로 = 51.522 · AM_P 48.286 · AM_S 51.798 (a0a24c538 실측 · 설계 원형 sumclip 과 같다)',
        leg == (51.522, 48.286, 51.798), repr(leg))
    u = (fm.get('coverage_AM_mean_physics_union'), fm.get('coverage_AM_P_mean_physics_union'),
         fm.get('coverage_AM_S_mean_physics_union'))
    st = fm.get('coverage_status_physics_union')
    ok_u = st == 'ok' and None not in u and all(isinstance(x, float) for x in u)
    chk(f'R2 ★ real_14 합집합 = 43.218 · AM_P 39.718 · AM_S 43.518 (원형 cov_union2.py N 6000) ± {BED_TOL} %p',
        ok_u and abs(u[0] - 43.218) <= BED_TOL and abs(u[1] - 39.718) <= BED_TOL and abs(u[2] - 43.518) <= BED_TOL,
        f'status={st!r} · {u}')
    if ok_u:
        chk('R3 real_14 합집합 / 합-클립 = 0.839 ± 0.002 (×0.84 · C2-⑥ 기록)', abs(u[0] / leg[0] - 0.8388) <= 0.002,
            f'{u[0] / leg[0]:.4f}')
    dg = fm.get('coverage_diag_physics_union') or {}
    chk('R4 real_14 진단 — AM 457 · 접촉 실패 0 · 방향 어긋남 0 (상자 0.05 · 최소영상 거리 = r1 + r2 − δ) · 반구 자름 0 · 분모 무효 0',
        dg.get('n_am') == 457 and dg.get('n_contact_failures') == 0 and dg.get('n_dir_inconsistent') == 0
        and dg.get('n_caps_clipped_hemisphere') == 0 and dg.get('n_free_surface_empty') == 0
        and dg.get('box_xy_sim') == [0.05, 0.05], repr({k: dg.get(k) for k in ('n_am', 'n_contact_failures', 'n_dir_inconsistent',
                                                                                'n_caps_clipped_hemisphere', 'dist_err_max_sim')}))
    # 표본 오차 — 같은 침대를 N 24000 으로
    import pandas as pd
    at, ct = pd.read_csv(cd / 'atoms.csv'), pd.read_csv(cd / 'contacts.csv', low_memory=False)
    k24, _ = CV.union_coverage_bed(at, ct, tm, scale=1000, box_xy=(0.05, 0.05), n_points=24000)
    chk(f'R5 표본: real_14 합집합 N 24000 ↔ 6000 차 ≤ {BED_TOL} %p (결정적 격자 · N 은 키로 기록)',
        ok_u and k24.get('coverage_n_fib_physics_union') == 24000
        and abs(k24['coverage_AM_mean_physics_union'] - u[0]) <= BED_TOL,
        f"N24000 {k24.get('coverage_AM_mean_physics_union')} vs {u[0]}")
    # case15 — 생산 경로 = 빈칸 (c_cpl[22] < 0 두 행) · 원형의 ×0.87 = 그 두 행을 원판으로 바꿔 넣은 값
    cd15, tm15 = build_real_bed('case15', tmp / 'case15')
    f15 = _run(cd15, tm15)
    s15 = str(f15.get('coverage_status_physics_union'))
    d15 = f15.get('coverage_diag_physics_union') or {}
    chk('R6 ★ case15 생산 경로 = 빈칸 + 사유 (c_cpl[22] < 0 두 접촉 · 첫 사례 31–29241 = 반경 0.5 µm SE 가 6 µm AM 안에 통째로) · '
        'v2 도 같은 사유로 빈칸 · legacy 18.324 그대로',
        s15.startswith('blank') and 'ligg_area < 0' in s15 and '31–29241' in s15 and d15.get('n_contact_failures') == 2
        and str(f15.get('coverage_status_physics_v2', '')).startswith('blank') and f15.get('coverage_AM_mean_physics') == 18.324,
        f'{s15[:200]!r}')
    at15, ct15 = pd.read_csv(cd15 / 'atoms.csv'), pd.read_csv(cd15 / 'contacts.csv', low_memory=False)
    proto = ct15.copy()
    neg = proto['contact_area'] < 0
    proto.loc[neg, 'contact_area'] = math.pi * (0.0005 ** 2)          # 원형 (g2lib.area_variant) 의 대체: 원판 π r_min² (포함 기하)
    kp, _ = CV.union_coverage_bed(at15, proto, tm15, scale=1000, box_xy=(0.1, 0.1))
    v = kp.get('coverage_AM_mean_physics_union')
    chk('R7 case15 원형 재현 — 음수 c_cpl[22] 두 행을 원판 π r_SE² 로 바꿔 넣으면 15.984 ± 허용 = ×0.872 (C2-⑥ 기록의 ×0.87 이 이 값)',
        kp.get('coverage_status_physics_union') == 'ok' and v is not None and abs(v - 15.984) <= BED_TOL
        and abs(v / 18.324 - 0.8723) <= 0.003 and int(neg.sum()) == 2, f'{v} · 음수 행 {int(neg.sum())}')


def main():
    tmp = Path(tempfile.mkdtemp(prefix='union_cov_'))
    try:
        _guard('[F]', section_f)
        _guard('[P]', lambda: section_p(tmp))
        _guard('[R]', lambda: section_r(tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
